# Casino Router API Documentation

**Base URL:** `https://your-router-domain.com`  
**Version:** 2.0.0  
**Auto-generated docs:** `{BASE_URL}/docs` (Swagger UI)

---

## Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/click` | GET | Handle landing page click → redirect to casino |
| `/postback` | POST | Receive FTD/payout events from casinos |
| `/health` | GET | Health check |
| `/admin/offers` | GET/POST | List or create offers |
| `/admin/offers/{id}` | GET/PUT/DELETE | Manage specific offer |
| `/admin/stats` | GET | Global statistics |
| `/admin/stats/sub1` | GET | List all tracked sub1 codes |
| `/admin/stats/sub1/{sub1}` | GET | Stats for specific sub1 |
| `/admin/update-weights` | POST | Trigger weight recalculation |

---

## Core Endpoints

### 1. Click Tracking & Redirect

**Endpoint:** `GET /click`

This is what your Bolt landing page CTAs call.

#### Request

```
GET /click?sub1={tracking_code}&source={source}&campaign={campaign}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `sub1` | ✅ **Yes** | Tracking code (affiliate ID, traffic source, etc.) |
| `source` | No | Traffic source identifier |
| `campaign` | No | Campaign identifier |

#### Response

```
HTTP 302 Found
Location: https://casino-url.com/register?click_id=550e8400-e29b-41d4-a716-446655440000
```

#### Example

**Bolt Landing CTA:**
```html
<a href="https://router.yourdomain.com/click?sub1=fb_campaign_winter">
  Play Now
</a>
```

**Result:** User redirected to best-performing casino for `fb_campaign_winter`

---

### 2. Postback (FTD Events)

**Endpoint:** `POST /postback`

Casinos call this when a user makes their first deposit (FTD).

#### Request

```json
POST /postback
Content-Type: application/json

{
  "click_id": "550e8400-e29b-41d4-a716-446655440000",
  "event": "ftd",
  "payout": 150.00,
  "secret": "your-shared-postback-secret",
  "external_player_id": "player123"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `click_id` | ✅ Yes | Click ID from redirect URL |
| `event` | ✅ Yes | Event type (currently only `ftd`) |
| `payout` | ✅ Yes | Commission/payout amount |
| `secret` | ✅ Yes | Shared postback secret |
| `external_player_id` | No | Casino's player ID |

#### Response

**Success (200):**
```json
{
  "status": "success",
  "message": "FTD and payout recorded",
  "click_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Errors:**
- `401 Unauthorized` - Invalid secret
- `404 Not Found` - Click ID not found
- `400 Bad Request` - Invalid event type

---

### 3. Health Check

**Endpoint:** `GET /health`

#### Response

```json
{
  "status": "healthy",
  "database": "connected",
  "active_offers": 4,
  "timestamp": "2025-12-31T16:30:00.000000"
}
```

---

## Admin Endpoints

### 4. List Offers

**Endpoint:** `GET /admin/offers`

| Parameter | Description |
|-----------|-------------|
| `active_only` | If `true`, return only active offers |

#### Response

```json
[
  {
    "id": 1,
    "name": "Casino Alpha",
    "casino_url": "https://casino-alpha.com/register",
    "active": true,
    "created_at": "2025-12-31T10:00:00.000000"
  },
  {
    "id": 2,
    "name": "Casino Beta",
    "casino_url": "https://casino-beta.com/signup",
    "active": true,
    "created_at": "2025-12-31T10:00:00.000000"
  }
]
```

---

### 5. Create Offer

**Endpoint:** `POST /admin/offers`

#### Request

```json
{
  "name": "New Casino",
  "casino_url": "https://new-casino.com/register?affid=123",
  "active": true
}
```

#### Response

```json
{
  "id": 5,
  "name": "New Casino",
  "casino_url": "https://new-casino.com/register?affid=123",
  "active": true,
  "created_at": "2025-12-31T16:30:00.000000"
}
```

---

### 6. Update Offer

**Endpoint:** `PUT /admin/offers/{id}`

#### Request

```json
{
  "name": "Updated Name",
  "casino_url": "https://updated-url.com",
  "active": false
}
```

All fields optional - only provided fields are updated.

---

### 7. Delete Offer

**Endpoint:** `DELETE /admin/offers/{id}`

#### Response

```
HTTP 204 No Content
```

---

### 8. Global Statistics

**Endpoint:** `GET /admin/stats`

Returns aggregated stats for all offers (across all sub1 codes).

#### Response

```json
[
  {
    "id": 1,
    "name": "Casino Alpha",
    "total_clicks": 1500,
    "total_ftds": 45,
    "total_payout": 6750.00,
    "active": true
  }
]
```

---

### 9. List All Sub1 Codes

**Endpoint:** `GET /admin/stats/sub1`

Returns all unique tracking codes that have generated clicks.

#### Response

```json
{
  "sub1_codes": [
    "fb_campaign_winter",
    "google_ads_jan",
    "affiliate_john",
    "partner_xyz"
  ],
  "total": 4
}
```

---

### 10. Per-Sub1 Statistics

**Endpoint:** `GET /admin/stats/sub1/{sub1}`

Returns detailed per-offer statistics for a specific tracking code.

#### Response

```json
[
  {
    "sub1": "affiliate_john",
    "offer_id": 1,
    "offer_name": "Casino Alpha",
    "total_clicks": 100,
    "total_ftds": 3,
    "total_payout": 450.00,
    "conversion_rate": 3.0,
    "ev": 4.50,
    "weight": 0.45
  },
  {
    "sub1": "affiliate_john",
    "offer_id": 2,
    "offer_name": "Casino Beta",
    "total_clicks": 100,
    "total_ftds": 5,
    "total_payout": 1000.00,
    "conversion_rate": 5.0,
    "ev": 10.00,
    "weight": 1.0
  }
]
```

**Key Fields:**
- `ev` - Expected Value: `(FTD / clicks) × payout`
- `weight` - Routing weight (1.0 = best performer)

---

### 11. Manual Weight Update

**Endpoint:** `POST /admin/update-weights`

Triggers immediate weight recalculation (normally runs every 10 minutes).

| Parameter | Description |
|-----------|-------------|
| `sub1` | If provided, update only this sub1. Otherwise, update all. |

#### Response

```json
{
  "status": "success",
  "message": "Weights updated for all sub1 codes"
}
```

---

## Bolt Landing Integration

### Step 1: Set CTA URL

In your Bolt landing page, set the button/link to:

```
https://router.yourdomain.com/click?sub1=YOUR_UNIQUE_ID
```

### Step 2: Choose sub1 Values

| Landing | sub1 Value |
|---------|-----------|
| Facebook Landing A | `fb_landing_a` |
| Google Ads Landing | `google_ads_main` |
| Partner Landing | `partner_xyz` |

### Step 3: That's It!

- Landing pages stay **completely static**
- Backend handles all routing decisions
- Check stats via `/admin/stats/sub1/{sub1}`

---

## Casino Postback Setup

Give your casino partners this configuration:

**Postback URL:**
```
POST https://router.yourdomain.com/postback
```

**Request Format:**
```json
{
  "click_id": "{CLICK_ID}",
  "event": "ftd",
  "payout": {PAYOUT},
  "secret": "YOUR_SHARED_SECRET"
}
```

**Platform-Specific Macros:**
- SoftGamings: `{{click_id}}`, `{{commission}}`
- EveryMatrix: `%%CLICKID%%`, `%%PAYOUT%%`
- BetConstruct: `[clickid]`, `[payout]`

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 302 | Redirect (click endpoint) |
| 400 | Bad request / invalid data |
| 401 | Invalid postback secret |
| 404 | Resource not found |
| 422 | Missing required parameter (e.g., sub1) |
| 500 | Server error |
| 503 | No active offers available |

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LAST_N_CLICKS` | 100 | Clicks used for EV calculation |
| `EXPLORATION_RATE` | 0.20 | 20% traffic for exploration |
| `CRON_INTERVAL_MINUTES` | 10 | Weight update frequency |
| `SHARED_POSTBACK_SECRET` | - | Postback authentication token |

---

## Live Testing

Interactive API documentation with "Try it out" feature:

```
https://router.yourdomain.com/docs
```
