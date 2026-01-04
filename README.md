# Casino Offer Router

Backend system that automatically routes landing page traffic to the best-performing casino offers based on real-time performance data (EV/EPC).

## Features

- **Automatic Traffic Routing**: Redirects landing page clicks to casino offers based on performance
- **Weight-Based Selection**: Uses EV (Expected Value) calculation to optimize traffic distribution
- **Exploration Traffic**: Fixed percentage (20%) for testing all offers evenly
- **Generic Postback System**: Receives FTD and payout events from any casino platform
- **Automated Optimization**: Cron job recalculates weights every 6 hours
- **Admin API**: Full CRUD for offer management + performance statistics
- **Auto-Generated Docs**: FastAPI provides `/docs` endpoint with Swagger UI

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Scheduler**: APScheduler
- **Containerization**: Docker + Docker Compose

## Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Git (to clone the repository)

### 1. Clone & Setup

```bash
# Copy environment variables
cp .env.example .env

# Edit .env if needed (optional, defaults work out of the box)
```

### 2. Start Services

```bash
docker-compose up --build
```

This will:
- Start PostgreSQL database
- Build and start the FastAPI application
- Initialize database tables
- Start the scheduler for automatic weight updates

### 3. Seed Initial Data

```bash
docker-compose exec app python seed_data.py
```

This creates 3 example casino offers with generated postback secrets.

### 4. Access Services

- **API**: http://localhost:5000
- **API Docs**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/health

## API Endpoints

### Core Endpoints

#### `GET /click`

Handle click from landing page and redirect to selected casino offer.

**Query Parameters:**
- `source` (optional): Traffic source identifier
- `campaign` (optional): Campaign identifier

**Example:**
```bash
curl -L "http://localhost:5000/click?source=facebook&campaign=winter2024"
```

**Response:** 302 redirect to casino URL with `click_id` parameter

---

#### `POST /postback`

Receive FTD (First Time Deposit) and payout events from casino platforms.

**Request Body:**
```json
{
  "click_id": "uuid-from-redirect",
  "event": "ftd",
  "payout": 100.50,
  "secret": "offer-postback-secret",
  "external_player_id": "player123" // optional
}
```

**Example:**
```bash
curl -X POST "http://localhost:5000/postback" \
  -H "Content-Type: application/json" \
  -d '{
    "click_id": "abc-123-def",
    "event": "ftd",
    "payout": 100,
    "secret": "your_offer_secret_here"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "FTD and payout recorded",
  "click_id": "abc-123-def"
}
```

---

### Admin Endpoints

#### `POST /admin/offers`

Create a new casino offer.

**Request Body:**
```json
{
  "name": "Casino Delta",
  "casino_url": "https://casino-delta.com/register",
  "weight": 1.0,
  "postback_secret": "your-secure-secret-token",
  "active": true
}
```

---

#### `GET /admin/offers`

List all offers. Use `?active_only=true` to filter active offers only.

---

#### `GET /admin/offers/{offer_id}`

Get a specific offer by ID.

---

#### `PUT /admin/offers/{offer_id}`

Update an existing offer.

---

#### `DELETE /admin/offers/{offer_id}`

Delete an offer.

---

#### `GET /admin/stats`

Get performance statistics for all offers.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Casino Alpha",
    "total_clicks": 1500,
    "total_ftds": 45,
    "total_payout": 4500.0,
    "conversion_rate": 3.0,
    "ev": 3.0,
    "weight": 1.0,
    "active": true
  }
]
```

---

#### `POST /admin/update-weights`

Manually trigger weight recalculation (normally runs automatically every 6 hours).

---

## How It Works

### 1. Landing Page Integration

Your landing page CTA buttons should point to the `/click` endpoint:

```html
<a href="https://your-backend.com/click?source=homepage">Play Now</a>
```

### 2. Click Flow

1. User clicks button → backend receives request
2. Backend generates unique `click_id`
3. Backend selects offer based on weights (80% exploitation + 20% exploration)
4. Backend stores click in database
5. Backend redirects user to casino with: `casino_url?click_id=xyz`

### 3. Casino Integration

Casino platforms send postbacks to your `/postback` endpoint when FTD occurs:

```
POST https://your-backend.com/postback
{
  "click_id": "xyz",
  "event": "ftd",
  "payout": 100,
  "secret": "offer_secret"
}
```

### 4. Automatic Optimization

Every 6 hours (configurable), the system:

1. Calculates EV for each offer: `EV = (FTD / clicks) × payout`
2. Uses last 1000 clicks (configurable)
3. Updates weights proportionally to EV
4. Best performers get more traffic automatically

## Configuration

Edit `.env` file to customize:

```bash
# Database
DATABASE_URL=postgresql://casino_user:casino_pass_2024@postgres:5432/casino_router

# Performance Engine
LAST_N_CLICKS=1000          # Number of recent clicks for EV calculation
EXPLORATION_RATE=0.20       # 20% exploration traffic
CRON_INTERVAL_HOURS=6       # Weight update frequency

# Server
HOST=0.0.0.0
PORT=5000
```

## Performance Formula

**EV (Expected Value) Calculation:**

```
EV = (FTD_count / total_clicks) × average_payout
```

**Weight Assignment:**

- Weights are normalized: `weight = EV / max_EV`
- Minimum weight of 0.1 to keep exploring
- 20% of traffic is distributed evenly (exploration)
- 80% of traffic follows weight distribution (exploitation)

## Database Schema

```
offers
├── id (PK)
├── name
├── casino_url
├── weight
├── postback_secret
├── created_at
└── active

clicks
├── id (PK)
├── click_id (unique)
├── offer_id (FK)
├── timestamp
├── user_agent
├── ip_address
├── referrer
├── source
└── campaign

ftd_events
├── id (PK)
├── click_id (FK, unique)
├── offer_id (FK)
├── ftd_timestamp
└── external_player_id

payouts
├── id (PK)
├── ftd_event_id (FK, unique)
├── amount
└── received_at
```

## Development

### Run Locally (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL locally and update .env

# Initialize database
python seed_data.py

# Run application
python app.py
```

### Access Database

```bash
docker-compose exec postgres psql -U casino_user -d casino_router
```

### View Logs

```bash
docker-compose logs -f app
```

## Testing

### Test Click Flow

```bash
# Make a click request
curl -v "http://localhost:5000/click"

# Check it redirects and includes click_id in URL
```

### Test Postback

```bash
# Get offer secret from seed data output or admin API
# Then send postback
curl -X POST "http://localhost:5000/postback" \
  -H "Content-Type: application/json" \
  -d '{
    "click_id": "YOUR_CLICK_ID_FROM_PREVIOUS_STEP",
    "event": "ftd",
    "payout": 150,
    "secret": "YOUR_OFFER_SECRET"
  }'
```

### Verify Statistics

```bash
curl "http://localhost:5000/admin/stats"
```

## Production Deployment

1. **Environment Variables**: Update `.env` with production database credentials
2. **HTTPS**: Use a reverse proxy (nginx) with SSL certificate
3. **Authentication**: Add JWT authentication to admin endpoints
4. **Monitoring**: Integrate logging (Sentry, LogDNA, etc.)
5. **Scaling**: Use gunicorn workers: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app`

## License

MIT

## Support

For issues or questions, please open an issue in the repository.
