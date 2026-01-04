import uuid
from fastapi import FastAPI, Request, HTTPException, status, Query
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from models import init_db, get_session, Offer, Click, FTDEvent, Payout
from performance import select_offer
from cron import start_scheduler
from config import Config
from admin import router as admin_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Pydantic models for request validation
class PostbackRequest(BaseModel):
    click_id: str = Field(..., description="Unique click identifier")
    event: str = Field(..., description="Event type (ftd)")
    payout: float = Field(..., ge=0, description="Payout amount")
    secret: str = Field(..., description="Shared postback secret")
    external_player_id: Optional[str] = Field(None, description="Casino player ID")


class PostbackResponse(BaseModel):
    status: str
    message: str
    click_id: str


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Casino Offer Router...")
    init_db()
    scheduler = start_scheduler()
    logger.info("✓ Application started successfully")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    logger.info("✓ Application stopped")


# Initialize FastAPI app
app = FastAPI(
    title="Casino Offer Router",
    description="Automatically routes landing page traffic to best-performing casino offers (per sub1)",
    version="2.0.0",
    lifespan=lifespan
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include admin router
app.include_router(admin_router)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "service": "Casino Offer Router",
        "version": "2.0.0",
        "endpoints": {
            "click": "/click?sub1=XXX - Handle click and redirect (sub1 required)",
            "postback": "/postback - Receive FTD/payout events",
            "health": "/health - Health check",
            "docs": "/docs - API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    session = get_session()
    try:
        # Test database connection
        offer_count = session.query(Offer).filter(Offer.active == True).count()
        return {
            "status": "healthy",
            "database": "connected",
            "active_offers": offer_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )
    finally:
        session.close()


@app.get("/click")
@limiter.limit(f"{Config.RATE_LIMIT_CLICK}/minute")
async def handle_click(
    request: Request,
    sub1: str = Query(..., description="Tracking code (affiliate/source identifier) - REQUIRED"),
    source: Optional[str] = Query(None, description="Traffic source"),
    campaign: Optional[str] = Query(None, description="Campaign identifier")
):
    """
    Handle click from landing page:
    1. Validate sub1 parameter (REQUIRED)
    2. Generate unique click_id
    3. Select offer based on per-sub1 weights
    4. Store click in database
    5. 302 redirect to casino URL with click_id
    """
    session = get_session()
    
    try:
        # Generate unique click_id
        click_id = str(uuid.uuid4())
        
        # Extract metadata first (need IP for geo-targeting)
        user_agent = request.headers.get("user-agent", "")
        client_ip = request.client.host if request.client else None
        referrer = request.headers.get("referer", "")
        
        # Select offer based on performance for this sub1 + geo-targeting
        try:
            selected_offer = select_offer(sub1, ip_address=client_ip)
        except ValueError as e:
            logger.error(f"No offers available: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No offers available"
            )
        
        # Copy offer data before any db operations (in case object gets detached)
        offer_id = selected_offer.id
        offer_name = selected_offer.name
        casino_url_template = selected_offer.casino_url
        
        # Store click in database
        click = Click(
            click_id=click_id,
            sub1=sub1,
            offer_id=offer_id,
            user_agent=user_agent,
            ip_address=client_ip,
            referrer=referrer,
            source=source,
            campaign=campaign
        )
        session.add(click)
        session.commit()
        
        # Build redirect URL with click_id and sub1
        # Replace {click_id} placeholder in casino URL
        casino_url = casino_url_template.replace("{click_id}", click_id)
        # Replace {sub1} placeholder with user's sub1
        casino_url = casino_url.replace("{sub1}", sub1)
        
        # Add click_id as parameter if not already in URL
        if "{click_id}" in casino_url_template or "click_id=" in casino_url:
            # URL already has click_id, don't add it again
            redirect_url = casino_url
        else:
            # Add click_id as parameter
            separator = "&" if "?" in casino_url else "?"
            redirect_url = f"{casino_url}{separator}click_id={click_id}"
        
        logger.info(f"Click {click_id} → sub1={sub1}, Offer {offer_id} ({offer_name})")
        
        # 302 redirect to casino
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error handling click: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    finally:
        session.close()


@app.api_route("/postback", methods=["GET", "POST"], response_model=PostbackResponse)
@limiter.limit(f"{Config.RATE_LIMIT_POSTBACK}/minute")
async def handle_postback(
    request: Request,
    click_id: Optional[str] = Query(None),
    event: Optional[str] = Query(None),
    payout: Optional[float] = Query(None),
    secret: Optional[str] = Query(None),
    external_player_id: Optional[str] = Query(None),
    postback: Optional[PostbackRequest] = None
):
    """
    Generic postback endpoint for FTD and payout events.
    Accepts both GET (query params) and POST (JSON body).
    Validates shared secret token and stores event in database.
    """
    # Handle GET request (query parameters)
    if request.method == "GET":
        if not all([click_id, event, payout, secret]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required parameters: click_id, event, payout, secret"
            )
        postback_data = PostbackRequest(
            click_id=click_id,
            event=event,
            payout=payout,
            secret=secret,
            external_player_id=external_player_id
        )
    else:
        # Handle POST request (JSON body)
        if postback is None:
            # Try to parse JSON body manually
            try:
                body = await request.json()
                postback_data = PostbackRequest(**body)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid JSON body: {str(e)}"
                )
        else:
            postback_data = postback
    
    session = get_session()
    
    try:
        # Verify shared postback secret
        if postback_data.secret != Config.SHARED_POSTBACK_SECRET:
            logger.warning(f"Invalid postback secret for click_id: {postback_data.click_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid secret"
            )
        
        # Find the click
        click = session.query(Click).filter(Click.click_id == postback_data.click_id).first()
        
        if not click:
            logger.warning(f"Postback for unknown click_id: {postback_data.click_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Click not found"
            )
        
        # Handle FTD event
        if postback_data.event.lower() == "ftd":
            # Check if FTD already exists
            existing_ftd = session.query(FTDEvent).filter(
                FTDEvent.click_id == postback_data.click_id
            ).first()
            
            if existing_ftd:
                logger.info(f"FTD already exists for click_id: {postback_data.click_id}")
                return PostbackResponse(
                    status="success",
                    message="FTD already recorded",
                    click_id=postback_data.click_id
                )
            
            # Create FTD event
            ftd_event = FTDEvent(
                click_id=postback_data.click_id,
                offer_id=click.offer_id,
                external_player_id=postback_data.external_player_id
            )
            session.add(ftd_event)
            session.flush()  # Get ftd_event.id
            
            # Create payout
            payout_record = Payout(
                ftd_event_id=ftd_event.id,
                amount=postback_data.payout
            )
            session.add(payout_record)
            session.commit()
            
            logger.info(f"✓ FTD recorded: click_id={postback_data.click_id}, sub1={click.sub1}, payout={postback_data.payout}")
            
            return PostbackResponse(
                status="success",
                message="FTD and payout recorded",
                click_id=postback_data.click_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported event type: {postback_data.event}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error handling postback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    finally:
        session.close()


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """
    Web dashboard to view traffic, stats, and leaks
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Casino Router - Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }
            .container { max-width: 1400px; margin: 0 auto; }
            h1 {
                color: white;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: transform 0.3s;
            }
            .stat-card:hover { transform: translateY(-5px); }
            .stat-card h3 { color: #667eea; margin-bottom: 10px; font-size: 1.1em; }
            .stat-card .value {
                font-size: 2.5em;
                font-weight: bold;
                color: #333;
                margin: 10px 0;
            }
            .stat-card .label { color: #666; font-size: 0.9em; }
            .section {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .section h2 {
                color: #667eea;
                margin-bottom: 20px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background: #667eea;
                color: white;
                font-weight: bold;
            }
            tr:hover { background: #f5f5f5; }
            .good { color: #28a745; font-weight: bold; }
            .warning { color: #ffc107; font-weight: bold; }
            .bad { color: #dc3545; font-weight: bold; }
            .refresh-btn {
                background: #28a745;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 1.1em;
                cursor: pointer;
                display: block;
                margin: 20px auto;
                box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
                transition: all 0.3s;
            }
            .refresh-btn:hover {
                background: #218838;
                transform: translateY(-2px);
                box-shadow: 0 7px 20px rgba(40, 167, 69, 0.4);
            }
            .badge {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: bold;
            }
            .badge-tiktok { background: #000; color: white; }
            .badge-youtube { background: #FF0000; color: white; }
            .badge-instagram { background: #E4405F; color: white; }
            .badge-facebook { background: #1877F2; color: white; }
            .badge-google { background: #4285F4; color: white; }
            .badge-other { background: #6c757d; color: white; }
            .leak-alert {
                background: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }
            .leak-alert h4 { color: #856404; margin-bottom: 10px; }
            .progress-bar {
                height: 20px;
                background: #e9ecef;
                border-radius: 10px;
                overflow: hidden;
                margin: 10px 0;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transition: width 0.3s;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎰 Casino Router - Dashboard Live</h1>
            
            <button class="refresh-btn" onclick="loadData()">🔄 Rafraîchir</button>
            
            <div class="stats-grid" id="globalStats">
                <div class="stat-card">
                    <h3>📊 Total Clicks</h3>
                    <div class="value" id="totalClicks">-</div>
                    <div class="label">Tous affiliés</div>
                </div>
                <div class="stat-card">
                    <h3>💰 Total FTDs</h3>
                    <div class="value" id="totalFtds">-</div>
                    <div class="label">Conversions</div>
                </div>
                <div class="stat-card">
                    <h3>💵 Total Payout</h3>
                    <div class="value" id="totalPayout">-</div>
                    <div class="label">Revenus</div>
                </div>
                <div class="stat-card">
                    <h3>📈 Taux de Conversion</h3>
                    <div class="value" id="conversionRate">-</div>
                    <div class="label">Global</div>
                </div>
            </div>
            
            <div class="section" id="leakSection">
                <h2>🚨 Détection de Leaks</h2>
                <div id="leakAlerts"></div>
            </div>
            
            <div class="section">
                <h2>🌐 Trafic par Source</h2>
                <table id="sourceTable">
                    <thead>
                        <tr>
                            <th>Source</th>
                            <th>Clicks</th>
                            <th>FTDs</th>
                            <th>Payout</th>
                            <th>Taux Conv.</th>
                            <th>EV/Click</th>
                        </tr>
                    </thead>
                    <tbody id="sourceTableBody">
                        <tr><td colspan="6" style="text-align: center;">Chargement...</td></tr>
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>👥 Trafic par Affilié (sub1)</h2>
                <table id="affiliateTable">
                    <thead>
                        <tr>
                            <th>Affilié (sub1)</th>
                            <th>Source</th>
                            <th>Casino Principal</th>
                            <th>Clicks</th>
                            <th>FTDs</th>
                            <th>Payout</th>
                            <th>Conv. %</th>
                        </tr>
                    </thead>
                    <tbody id="affiliateTableBody">
                        <tr><td colspan="7" style="text-align: center;">Chargement...</td></tr>
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>🎰 Performance par Casino</h2>
                <table id="casinoTable">
                    <thead>
                        <tr>
                            <th>Casino</th>
                            <th>Clicks</th>
                            <th>FTDs</th>
                            <th>Payout</th>
                            <th>Taux Conv.</th>
                            <th>Part du Trafic</th>
                        </tr>
                    </thead>
                    <tbody id="casinoTableBody">
                        <tr><td colspan="6" style="text-align: center;">Chargement...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <script>
            const USERNAME = 'admin';
            const PASSWORD = 'admin123';
            const auth = btoa(`${USERNAME}:${PASSWORD}`);
            const headers = {
                'Authorization': `Basic ${auth}`,
                'Content-Type': 'application/json'
            };
            
            async function loadData() {
                try {
                    const statsResponse = await fetch('/admin/stats', { headers });
                    const stats = await statsResponse.json();
                    
                    // Les stats contiennent déjà tout ce qu'il faut !
                    updateGlobalStats(stats);
                    updateAffiliateTable(stats);
                    analyzeTrafficSources(stats);
                    detectLeaks(stats);
                    
                    const offersResponse = await fetch('/admin/offers', { headers });
                    const offers = await offersResponse.json();
                    
                    updateCasinoTable(stats, offers);
                    
                } catch (error) {
                    console.error('Erreur:', error);
                    alert('Erreur de chargement: ' + error.message);
                }
            }
            
            function updateGlobalStats(stats) {
                const totalClicks = stats.reduce((sum, s) => sum + s.total_clicks, 0);
                const totalFtds = stats.reduce((sum, s) => sum + s.total_ftds, 0);
                const totalPayout = stats.reduce((sum, s) => sum + s.total_payout, 0);
                const convRate = totalClicks > 0 ? ((totalFtds / totalClicks) * 100).toFixed(2) : 0;
                
                document.getElementById('totalClicks').textContent = totalClicks.toLocaleString();
                document.getElementById('totalFtds').textContent = totalFtds.toLocaleString();
                document.getElementById('totalPayout').textContent = totalPayout.toFixed(2) + '€';
                document.getElementById('conversionRate').textContent = convRate + '%';
            }
            
            function updateAffiliateTable(stats) {
                const tbody = document.getElementById('affiliateTableBody');
                tbody.innerHTML = '';
                
                if (!stats || stats.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">Aucune donnée</td></tr>';
                    return;
                }
                
                const grouped = {};
                stats.forEach(stat => {
                    // Ignorer les stats sans sub1
                    if (!stat.sub1) return;
                    
                    if (!grouped[stat.sub1]) {
                        grouped[stat.sub1] = {
                            sub1: stat.sub1,
                            clicks: 0,
                            ftds: 0,
                            payout: 0,
                            offers: []
                        };
                    }
                    grouped[stat.sub1].clicks += stat.total_clicks || 0;
                    grouped[stat.sub1].ftds += stat.total_ftds || 0;
                    grouped[stat.sub1].payout += stat.total_payout || 0;
                    grouped[stat.sub1].offers.push(stat);
                });
                
                if (Object.keys(grouped).length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">Aucun affilié avec des données</td></tr>';
                    return;
                }
                
                Object.values(grouped).forEach(aff => {
                    const convRate = aff.clicks > 0 ? ((aff.ftds / aff.clicks) * 100).toFixed(2) : 0;
                    const topOffer = aff.offers.sort((a, b) => b.total_clicks - a.total_clicks)[0];
                    const source = extractSource(aff.sub1);
                    
                    const row = `
                        <tr>
                            <td><strong>${aff.sub1}</strong></td>
                            <td>${getSourceBadge(source)}</td>
                            <td>${topOffer.offer_name || 'N/A'}</td>
                            <td>${aff.clicks}</td>
                            <td class="${aff.ftds > 0 ? 'good' : ''}">${aff.ftds}</td>
                            <td>${aff.payout.toFixed(2)}€</td>
                            <td class="${convRate > 3 ? 'good' : convRate > 1 ? 'warning' : 'bad'}">${convRate}%</td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                });
            }
            
            function analyzeTrafficSources(stats) {
                const sources = {};
                
                stats.forEach(stat => {
                    const source = extractSource(stat.sub1);
                    if (!sources[source]) {
                        sources[source] = { clicks: 0, ftds: 0, payout: 0 };
                    }
                    sources[source].clicks += stat.total_clicks;
                    sources[source].ftds += stat.total_ftds;
                    sources[source].payout += stat.total_payout;
                });
                
                const tbody = document.getElementById('sourceTableBody');
                tbody.innerHTML = '';
                
                Object.entries(sources).forEach(([source, data]) => {
                    const convRate = data.clicks > 0 ? ((data.ftds / data.clicks) * 100).toFixed(2) : 0;
                    const evPerClick = data.clicks > 0 ? (data.payout / data.clicks).toFixed(2) : 0;
                    
                    const row = `
                        <tr>
                            <td>${getSourceBadge(source)}</td>
                            <td>${data.clicks}</td>
                            <td>${data.ftds}</td>
                            <td>${data.payout.toFixed(2)}€</td>
                            <td class="${convRate > 3 ? 'good' : convRate > 1 ? 'warning' : 'bad'}">${convRate}%</td>
                            <td>${evPerClick}€</td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                });
            }
            
            function detectLeaks(stats) {
                const leakAlerts = document.getElementById('leakAlerts');
                leakAlerts.innerHTML = '';
                
                const grouped = {};
                stats.forEach(stat => {
                    if (!grouped[stat.sub1]) {
                        grouped[stat.sub1] = { clicks: 0, ftds: 0 };
                    }
                    grouped[stat.sub1].clicks += stat.total_clicks;
                    grouped[stat.sub1].ftds += stat.total_ftds;
                });
                
                let leaksDetected = false;
                
                Object.entries(grouped).forEach(([sub1, data]) => {
                    if (data.clicks > 50 && data.ftds === 0) {
                        leaksDetected = true;
                        leakAlerts.innerHTML += `
                            <div class="leak-alert">
                                <h4>⚠️ Leak potentiel : ${sub1}</h4>
                                <p>${data.clicks} clicks mais AUCUNE conversion !</p>
                            </div>
                        `;
                    }
                });
                
                if (!leaksDetected) {
                    leakAlerts.innerHTML = '<p style="color: #28a745; font-weight: bold;">✅ Aucun leak détecté !</p>';
                }
            }
            
            function updateCasinoTable(stats, offers) {
                const tbody = document.getElementById('casinoTableBody');
                tbody.innerHTML = '';
                
                const casinoStats = {};
                
                stats.forEach(stat => {
                    if (!casinoStats[stat.offer_id]) {
                        casinoStats[stat.offer_id] = {
                            name: stat.offer_name,
                            clicks: 0,
                            ftds: 0,
                            payout: 0
                        };
                    }
                    casinoStats[stat.offer_id].clicks += stat.total_clicks;
                    casinoStats[stat.offer_id].ftds += stat.total_ftds;
                    casinoStats[stat.offer_id].payout += stat.total_payout;
                });
                
                const totalClicks = Object.values(casinoStats).reduce((sum, c) => sum + c.clicks, 0);
                
                Object.values(casinoStats).forEach(casino => {
                    const convRate = casino.clicks > 0 ? ((casino.ftds / casino.clicks) * 100).toFixed(2) : 0;
                    const trafficShare = totalClicks > 0 ? ((casino.clicks / totalClicks) * 100).toFixed(1) : 0;
                    
                    const row = `
                        <tr>
                            <td><strong>${casino.name}</strong></td>
                            <td>${casino.clicks}</td>
                            <td>${casino.ftds}</td>
                            <td>${casino.payout.toFixed(2)}€</td>
                            <td class="${convRate > 3 ? 'good' : convRate > 1 ? 'warning' : 'bad'}">${convRate}%</td>
                            <td>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${trafficShare}%"></div>
                                </div>
                                ${trafficShare}%
                            </td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                });
            }
            
            function extractSource(sub1) {
                if (!sub1 || typeof sub1 !== 'string') return 'other';
                const lower = sub1.toLowerCase();
                if (lower.includes('tiktok')) return 'tiktok';
                if (lower.includes('youtube') || lower.includes('yt')) return 'youtube';
                if (lower.includes('instagram') || lower.includes('insta') || lower.includes('ig')) return 'instagram';
                if (lower.includes('facebook') || lower.includes('fb')) return 'facebook';
                if (lower.includes('google') || lower.includes('ads')) return 'google';
                return 'other';
            }
            
            function getSourceBadge(source) {
                const badges = {
                    'tiktok': '<span class="badge badge-tiktok">TikTok</span>',
                    'youtube': '<span class="badge badge-youtube">YouTube</span>',
                    'instagram': '<span class="badge badge-instagram">Instagram</span>',
                    'facebook': '<span class="badge badge-facebook">Facebook</span>',
                    'google': '<span class="badge badge-google">Google</span>',
                    'other': '<span class="badge badge-other">Autre</span>'
                };
                return badges[source] || badges['other'];
            }
            
            loadData();
            setInterval(loadData, 30000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/admin/live-clicks")
async def get_live_clicks(request: Request, limit: int = Query(default=20, le=100)):
    """
    Get recent clicks with detailed information for live dashboard
    """
    # Simple auth check (same as other admin endpoints)
    import base64
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        credentials = base64.b64decode(auth_header[6:]).decode("utf-8")
        username, password = credentials.split(":", 1)
        if username != Config.ADMIN_USERNAME or password != Config.ADMIN_PASSWORD:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    session = get_session()
    
    try:
        # Get recent clicks with offer info
        from sqlalchemy import desc
        from geo_restrictions import get_country_from_ip
        
        clicks = session.query(Click).order_by(desc(Click.timestamp)).limit(limit).all()
        
        result = []
        for click in clicks:
            # Get offer info
            offer = session.query(Offer).filter(Offer.id == click.offer_id).first()
            
            # Detect country from IP (but don't make external API call for past clicks)
            country = None
            # Just leave country as None for now to avoid rate limiting ipapi
            
            # Get all active offers to show what was available
            all_offers = session.query(Offer).filter(Offer.active == True).all()
            available_offer_ids = [o.id for o in all_offers]
            
            result.append({
                "click_id": click.click_id,
                "timestamp": click.timestamp.isoformat(),
                "sub1": click.sub1,
                "country": country,
                "ip_address": click.ip_address[:10] + "..." if click.ip_address else None,
                "selected_offer_id": click.offer_id,
                "selected_offer_name": offer.name if offer else "Unknown",
                "available_offer_ids": available_offer_ids
            })
        
        return JSONResponse(content=result)
        
    finally:
        session.close()


@app.get("/dashboard-live")
async def dashboard_live():
    """
    Serve the interactive live dashboard
    """
    with open("dashboard_live.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    )
