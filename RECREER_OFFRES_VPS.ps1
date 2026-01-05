# Script PowerShell pour recréer toutes les offres sur le VPS
# Usage: .\RECREER_OFFRES_VPS.ps1 https://ton-domaine.com

param(
    [Parameter(Mandatory=$true)]
    [string]$BaseUrl
)

$AdminUser = "admin"
$AdminPass = "change-this-in-production-123"
$base64Auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${AdminUser}:${AdminPass}"))

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  CRÉATION DES OFFRES CASINO" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Mystake
Write-Host "1️⃣  Création Mystake..." -ForegroundColor Yellow
$body1 = @{
    name = "Mystake"
    casino_url = "https://go.affiliatemystake.com/visit/?bta=3162926&nci=5597&afp={click_id}&utm_campaign={sub1}"
    payout = 55.0
    active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BaseUrl/admin/offers" `
    -Method Post `
    -Headers @{Authorization="Basic $base64Auth"} `
    -ContentType "application/json" `
    -Body $body1
Write-Host "✅ Mystake créé" -ForegroundColor Green
Write-Host ""

# 2. iCE
Write-Host "2️⃣  Création iCE..." -ForegroundColor Yellow
$body2 = @{
    name = "iCE"
    casino_url = "https://direct.midas-affiliate.com/click?pid=656&offer_id=1616&ref_id={click_id}&sub1={sub1}"
    payout = 50.0
    active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BaseUrl/admin/offers" `
    -Method Post `
    -Headers @{Authorization="Basic $base64Auth"} `
    -ContentType "application/json" `
    -Body $body2
Write-Host "✅ iCE créé" -ForegroundColor Green
Write-Host ""

# 3. SpinGranny
Write-Host "3️⃣  Création SpinGranny..." -ForegroundColor Yellow
$body3 = @{
    name = "SpinGranny"
    casino_url = "https://www.nhlv1trk.com/BC4SXG3/B5RMCSR/?source_id={click_id}&sub1={sub1}"
    payout = 75.0
    active = $true
    time_restrictions = @{
        timezone = "Europe/Paris"
        allowed_periods = @(
            @{day="saturday"; all_day=$true},
            @{day="sunday"; all_day=$true},
            @{day="monday"; start="19:00"; end="23:59"},
            @{day="monday"; start="00:00"; end="06:00"},
            @{day="tuesday"; start="19:00"; end="23:59"},
            @{day="tuesday"; start="00:00"; end="06:00"},
            @{day="wednesday"; start="19:00"; end="23:59"},
            @{day="wednesday"; start="00:00"; end="06:00"},
            @{day="thursday"; start="19:00"; end="23:59"},
            @{day="thursday"; start="00:00"; end="06:00"},
            @{day="friday"; start="19:00"; end="23:59"},
            @{day="friday"; start="00:00"; end="06:00"}
        )
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "$BaseUrl/admin/offers" `
    -Method Post `
    -Headers @{Authorization="Basic $base64Auth"} `
    -ContentType "application/json" `
    -Body $body3
Write-Host "✅ SpinGranny créé" -ForegroundColor Green
Write-Host ""

# 4. 7ladies
Write-Host "4️⃣  Création 7ladies..." -ForegroundColor Yellow
$body4 = @{
    name = "7ladies"
    casino_url = "https://track.7ladies.com/visit/?bta=36063&nci=5390&afp1={click_id}&afp10=Tiktok&utm_campaign={sub1}"
    payout = 70.0
    active = $true
    geo_restrictions = @{
        allowed_countries = @("BE", "CH", "IT", "DE", "CA")
        exclusive = $true
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "$BaseUrl/admin/offers" `
    -Method Post `
    -Headers @{Authorization="Basic $base64Auth"} `
    -ContentType "application/json" `
    -Body $body4
Write-Host "✅ 7ladies créé" -ForegroundColor Green
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ✅ TOUTES LES OFFRES CRÉÉES !" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Vérifie sur: $BaseUrl/admin/stats" -ForegroundColor Yellow
Write-Host ""

