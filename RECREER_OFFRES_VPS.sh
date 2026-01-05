#!/bin/bash

# Script pour recréer toutes les offres sur le VPS
# Usage: ./RECREER_OFFRES_VPS.sh https://ton-domaine.com

if [ -z "$1" ]; then
  echo "❌ Usage: ./RECREER_OFFRES_VPS.sh https://ton-domaine.com"
  exit 1
fi

BASE_URL=$1
ADMIN_USER="admin"
ADMIN_PASS="change-this-in-production-123"

echo "=========================================="
echo "  CRÉATION DES OFFRES CASINO"
echo "=========================================="
echo ""

# 1. Mystake
echo "1️⃣  Création Mystake..."
curl -X POST "$BASE_URL/admin/offers" \
  -u "$ADMIN_USER:$ADMIN_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mystake",
    "casino_url": "https://go.affiliatemystake.com/visit/?bta=3162926&nci=5597&afp={click_id}&utm_campaign={sub1}",
    "payout": 55.0,
    "active": true
  }'
echo ""
echo ""

# 2. iCE
echo "2️⃣  Création iCE..."
curl -X POST "$BASE_URL/admin/offers" \
  -u "$ADMIN_USER:$ADMIN_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iCE",
    "casino_url": "https://direct.midas-affiliate.com/click?pid=656&offer_id=1616&ref_id={click_id}&sub1={sub1}",
    "payout": 50.0,
    "active": true
  }'
echo ""
echo ""

# 3. SpinGranny (restrictions horaires)
echo "3️⃣  Création SpinGranny..."
curl -X POST "$BASE_URL/admin/offers" \
  -u "$ADMIN_USER:$ADMIN_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SpinGranny",
    "casino_url": "https://www.nhlv1trk.com/BC4SXG3/B5RMCSR/?source_id={click_id}&sub1={sub1}",
    "payout": 75.0,
    "active": true,
    "time_restrictions": {
      "timezone": "Europe/Paris",
      "allowed_periods": [
        {"day": "saturday", "all_day": true},
        {"day": "sunday", "all_day": true},
        {"day": "monday", "start": "19:00", "end": "23:59"},
        {"day": "monday", "start": "00:00", "end": "06:00"},
        {"day": "tuesday", "start": "19:00", "end": "23:59"},
        {"day": "tuesday", "start": "00:00", "end": "06:00"},
        {"day": "wednesday", "start": "19:00", "end": "23:59"},
        {"day": "wednesday", "start": "00:00", "end": "06:00"},
        {"day": "thursday", "start": "19:00", "end": "23:59"},
        {"day": "thursday", "start": "00:00", "end": "06:00"},
        {"day": "friday", "start": "19:00", "end": "23:59"},
        {"day": "friday", "start": "00:00", "end": "06:00"}
      ]
    }
  }'
echo ""
echo ""

# 4. 7ladies (restrictions géographiques EXCLUSIVES)
echo "4️⃣  Création 7ladies..."
curl -X POST "$BASE_URL/admin/offers" \
  -u "$ADMIN_USER:$ADMIN_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "7ladies",
    "casino_url": "https://track.7ladies.com/visit/?bta=36063&nci=5390&afp1={click_id}&afp10=Tiktok&utm_campaign={sub1}",
    "payout": 70.0,
    "active": true,
    "geo_restrictions": {
      "allowed_countries": ["BE", "CH", "IT", "DE", "CA"],
      "exclusive": true
    }
  }'
echo ""
echo ""

echo "=========================================="
echo "  ✅ TOUTES LES OFFRES CRÉÉES !"
echo "=========================================="
echo ""
echo "Vérifie sur: $BASE_URL/admin/stats"
echo ""

