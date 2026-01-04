# Production Deployment Guide

Complete step-by-step guide to deploy the Casino Offer Router to production.

---

## Prerequisites

✅ A server (VPS/Cloud) with:
- Ubuntu 22.04+ / Debian 11+
- 2GB+ RAM
- 20GB+ disk space
- Public IP address
- Docker & Docker Compose installed

✅ A domain name (e.g., `router.yourdomain.com`)

✅ Real casino offers with tracking links

---

## Step 1: Server Setup

### 1.1 Get a Server

**Recommended providers:**
- **DigitalOcean:** $12/month (2GB RAM droplet)
- **Linode:** $12/month (2GB plan)
- **Vultr:** $12/month (2GB instance)
- **Hetzner:** €5/month (cheaper, Germany-based)

### 1.2 Connect to Server

```bash
ssh root@YOUR_SERVER_IP
```

### 1.3 Install Docker

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

---

## Step 2: Deploy Application

### 2.1 Upload Your Code

**Option A: Git (Recommended)**

```bash
# On server
cd /opt
git clone YOUR_REPO_URL casino-router
cd casino-router
```

**Option B: SCP/SFTP**

```bash
# On your local machine
scp -r c:\Users\HICHEM\Desktop\david root@YOUR_SERVER_IP:/opt/casino-router
```

### 2.2 Configure Environment

```bash
# On server, in project directory
cd /opt/casino-router

# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**CRITICAL: Update `.env` file:**

```bash
# Database Configuration
DATABASE_URL=postgresql://casino_user:CHANGE_THIS_PASSWORD@postgres:5432/casino_router

# Performance Engine
LAST_N_CLICKS=100
EXPLORATION_RATE=0.20
CRON_INTERVAL_MINUTES=10

# Postback Authentication - CHANGE THIS!
SHARED_POSTBACK_SECRET=your-super-secure-random-token-here-min-32-chars

# Server
HOST=0.0.0.0
PORT=5000
```

**Generate a secure secret:**

```bash
# On server
openssl rand -base64 32
# Use this output as your SHARED_POSTBACK_SECRET
```

### 2.3 Update Docker Compose for Production

Edit `docker-compose.yml`:

```bash
nano docker-compose.yml
```

Change:
```yaml
# Remove --reload for production
command: uvicorn app:app --host 0.0.0.0 --port 5000
```

Also update database password in `docker-compose.yml` to match `.env`

---

## Step 3: SSL Certificate & Domain

### 3.1 Point Domain to Server

In your domain DNS settings:
```
A record: router.yourdomain.com → YOUR_SERVER_IP
```

### 3.2 Install Nginx

```bash
apt install nginx certbot python3-certbot-nginx -y
```

### 3.3 Configure Nginx

```bash
nano /etc/nginx/sites-available/casino-router
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name router.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Important for redirects
        proxy_redirect off;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/casino-router /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 3.4 Get SSL Certificate

```bash
certbot --nginx -d router.yourdomain.com
```

Follow prompts. Certbot will automatically configure HTTPS.

---

## Step 4: Start Application

```bash
cd /opt/casino-router

# Start services
docker-compose up -d

# Check status
docker-compose ps

# Seed database with your real offers
docker-compose exec app python seed_data.py
```

---

## Step 5: Add Real Casino Offers

### 5.1 Delete Example Offers

```bash
# Via API
curl -X DELETE "https://router.yourdomain.com/admin/offers/1"
curl -X DELETE "https://router.yourdomain.com/admin/offers/2"
curl -X DELETE "https://router.yourdomain.com/admin/offers/3"
curl -X DELETE "https://router.yourdomain.com/admin/offers/4"
```

### 5.2 Add Your Real Offers

```bash
curl -X POST "https://router.yourdomain.com/admin/offers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Real Casino 1",
    "casino_url": "https://tracking.realcasino1.com/aff?affid=YOUR_ID",
    "active": true
  }'

curl -X POST "https://router.yourdomain.com/admin/offers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Real Casino 2",
    "casino_url": "https://tracking.realcasino2.com/click?pid=YOUR_PARTNER_ID",
    "active": true
  }'

# Add more offers...
```

---

## Step 6: Integrate Landing Pages

### 6.1 Update Your Landing Page CTAs

**Before:**
```html
<a href="https://casino-hardcoded.com/register">Play Now</a>
```

**After:**
```html
<a href="https://router.yourdomain.com/click?sub1=YOUR_TRACKING_CODE">Play Now</a>
```

**sub1 Examples:**
- Affiliate/partner ID: `sub1=affiliate_john123`
- Traffic source: `sub1=facebook_campaign_1`
- Geographic: `sub1=uk_traffic_source_a`

**Important:** Each unique `sub1` gets independent routing optimization!

### 6.2 Multiple Landing Pages

```html
<!-- Landing Page 1 -->
<a href="https://router.yourdomain.com/click?sub1=lp1_source_a&campaign=winter2024">
  Play Now
</a>

<!-- Landing Page 2 -->
<a href="https://router.yourdomain.com/click?sub1=lp2_source_b&campaign=winter2024">
  Join Casino
</a>

<!-- Partner Landing Page -->
<a href="https://router.yourdomain.com/click?sub1=partner_xyz&source=email">
  Start Playing
</a>
```

---

## Step 7: Configure Casino Postbacks

### 7.1 Get Your Shared Secret

```bash
# On server
cat .env | grep SHARED_POSTBACK_SECRET
```

### 7.2 Configure Each Casino Platform

**Casino 1 Postback URL:**
```
https://router.yourdomain.com/postback
```

**Postback Parameters (JSON format):**
```json
{
  "click_id": "{CLICK_ID}",
  "event": "ftd",
  "payout": {PAYOUT_AMOUNT},
  "secret": "your-shared-secret-from-env",
  "external_player_id": "{PLAYER_ID}"
}
```

**Important Macros:**
- `{CLICK_ID}` - Replace with casino's click ID macro
- `{PAYOUT_AMOUNT}` - Replace with payout macro
- `{PLAYER_ID}` - Replace with player ID macro

**Example for different platforms:**

**BetConstruct:**
```
https://router.yourdomain.com/postback?click_id=[clickid]&event=ftd&payout=[payout]&secret=YOUR_SECRET&external_player_id=[playerid]
```

**EveryMatrix:**
```
POST https://router.yourdomain.com/postback
Body: {"click_id":"%%CLICKID%%","event":"ftd","payout":%%PAYOUT%%,"secret":"YOUR_SECRET"}
```

**SoftGamings:**
```
https://router.yourdomain.com/postback?click_id={{click_id}}&event=ftd&payout={{commission}}&secret=YOUR_SECRET
```

---

## Step 8: Monitoring & Maintenance

### 8.1 Set Up Auto-Restart

```bash
# Create systemd service
nano /etc/systemd/system/casino-router.service
```

Add:
```ini
[Unit]
Description=Casino Router
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/casino-router
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
systemctl enable casino-router
systemctl start casino-router
```

### 8.2 Monitor Logs

```bash
# Real-time logs
docker-compose logs -f app

# Check for errors
docker-compose logs app | grep ERROR

# Check weight updates
docker-compose logs app | grep "weight update"
```

### 8.3 Database Backup

```bash
# Create backup script
nano /opt/backup-casino-db.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

docker-compose exec -T postgres pg_dump -U casino_user casino_router > $BACKUP_DIR/casino_router_$TIMESTAMP.sql

# Keep only last 7 days
find $BACKUP_DIR -name "casino_router_*.sql" -mtime +7 -delete

echo "Backup completed: casino_router_$TIMESTAMP.sql"
```

Make executable and schedule:
```bash
chmod +x /opt/backup-casino-db.sh

# Add to crontab (daily at 3 AM)
crontab -e
# Add: 0 3 * * * /opt/backup-casino-db.sh
```

### 8.4 Health Check Monitoring

Use a service like **UptimeRobot** (free) or **Pingdom**:
- Monitor: `https://router.yourdomain.com/health`
- Expected response: `{"status":"healthy"}`
- Alert if down for 5+ minutes

---

## Step 9: Security Hardening

### 9.1 Firewall

```bash
# Install UFW
apt install ufw -y

# Allow SSH, HTTP, HTTPS
ufw allow 22
ufw allow 80
ufw allow 443

# Enable firewall
ufw enable
```

### 9.2 Protect Admin Endpoints

Add authentication to admin routes. Update `admin.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "YOUR_ADMIN_PASSWORD")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return credentials.username

# Add to all admin routes:
@router.get("/offers", dependencies=[Depends(verify_admin)])
```

### 9.3 Rate Limiting

Add to `app.py`:

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add to click endpoint
@app.get("/click")
@limiter.limit("100/minute")
async def handle_click(...):
```

---

## Step 10: Testing Production

### 10.1 Test Click Flow

```bash
curl -v "https://router.yourdomain.com/click?sub1=test_production"
# Should: redirect to casino with click_id
```

### 10.2 Test Postback

```bash
# Use a real click_id from step 10.1
curl -X POST "https://router.yourdomain.com/postback" \
  -H "Content-Type: application/json" \
  -d '{
    "click_id": "REAL_CLICK_ID_HERE",
    "event": "ftd",
    "payout": 100,
    "secret": "YOUR_SHARED_SECRET",
    "external_player_id": "test123"
  }'
# Should: return success
```

### 10.3 Check Stats

```bash
curl "https://router.yourdomain.com/admin/stats/sub1/test_production"
# Should: show 1 click, 1 FTD, $100 payout
```

---

## Checklist Before Going Live

- [ ] Domain configured and SSL working
- [ ] `.env` file updated with secure passwords and secret
- [ ] Real casino offers added (not example data)
- [ ] Landing pages pointing to your router URL
- [ ] Casino postbacks configured with correct URL and secret
- [ ] Tested full flow (click → redirect → postback → stats)
- [ ] Monitoring set up (UptimeRobot or similar)
- [ ] Database backups scheduled
- [ ] Firewall enabled
- [ ] Admin endpoints protected (optional but recommended)
- [ ] Logs accessible and readable

---

## Troubleshooting

### Issue: Click returns 500 error
**Check logs:** `docker-compose logs app`  
**Common cause:** Database connection issue

### Issue: Postback returns 401
**Solution:** Verify shared secret matches in `.env` and casino config

### Issue: Stats show 0 clicks
**Solution:** Check landing page URLs have `sub1` parameter

### Issue: Weights not updating
**Solution:** Check cron is running: `docker-compose logs app | grep Scheduler`

---

## Scaling for High Traffic

When you reach 1M+ clicks/month:

1. **Database:** Migrate to managed PostgreSQL (AWS RDS, DigitalOcean Managed DB)
2. **Application:** Add more app containers (load balancer)
3. **Caching:** Add Redis for offer weights
4. **CDN:** CloudFlare in front for DDoS protection

---

## Support & Maintenance

**Daily:** Check health endpoint  
**Weekly:** Review logs for errors  
**Monthly:** Check database size, rotate backups  
**Quarterly:** Update dependencies, security patches

Your router is now production-ready! 🚀
