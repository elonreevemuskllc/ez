# 🎰 Guide Complet - Casino Router (Français)

**Guide pas-à-pas pour démarrer et utiliser votre système de routage de casino**

---

## 📖 Table des Matières

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Premiers Pas](#premiers-pas)
4. [Intégration Landing Pages](#intégration-landing-pages)
5. [Configuration Casinos](#configuration-casinos)
6. [Surveillance & Stats](#surveillance--stats)
7. [Production](#production)
8. [Dépannage](#dépannage)

---

## 🚀 Installation

### Prérequis

- **Docker Desktop** installé ([Télécharger](https://www.docker.com/products/docker-desktop))
- **Windows 10/11** ou Linux/macOS

### Installation Rapide

**Option 1 : Script Automatique (Windows)**

Double-cliquez sur `setup.bat`

**Option 2 : Commandes Manuelles**

```powershell
# Se placer dans le dossier
cd "chemin\vers\david"

# Démarrer les services
docker-compose up --build -d

# Attendre 15 secondes que PostgreSQL démarre

# Initialiser les données
docker-compose exec app python seed_data.py
```

### Vérification

Ouvrez votre navigateur : http://localhost:5000/health

**Réponse attendue :**
```json
{
  "status": "healthy",
  "database": "connected",
  "active_offers": 4
}
```

✅ **C'est bon ! Le système fonctionne.**

---

## ⚙️ Configuration

### Fichier .env

Le fichier `.env` contient toute la configuration. Valeurs importantes :

```bash
# Secret pour les postbacks (casinos doivent l'utiliser)
SHARED_POSTBACK_SECRET=dev-shared-secret-token-12345

# Login admin (pour accéder aux stats)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Paramètres d'optimisation
LAST_N_CLICKS=100           # Nombre de clicks analysés pour le calcul EV
EXPLORATION_RATE=0.20       # 20% du trafic en exploration
CRON_INTERVAL_MINUTES=10    # Mise à jour des poids toutes les 10 min
```

### ⚠️ IMPORTANT pour la Production

**Changez ABSOLUMENT ces valeurs :**

```bash
# Générer des secrets sécurisés (PowerShell)
# Pour SHARED_POSTBACK_SECRET:
$secret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
Write-Output $secret

# Pour ADMIN_PASSWORD:
$password = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | % {[char]$_})
Write-Output $password
```

Puis mettez ces valeurs dans `.env` et redémarrez :

```powershell
docker-compose down
docker-compose up -d
```

---

## 🎯 Premiers Pas

### 1. Accéder à la Documentation Interactive

Ouvrez : http://localhost:5000/docs

Vous avez **Swagger UI** : testez tous les endpoints directement !

### 2. Premier Test de Click

Dans votre navigateur :
```
http://localhost:5000/click?sub1=mon_premier_test
```

**Ce qui se passe :**
1. Vous êtes redirigé vers un casino (exemple)
2. Un `click_id` unique est dans l'URL
3. Le click est enregistré en base

### 3. Simuler un FTD (conversion)

Copiez le `click_id` de l'URL de redirection, puis dans PowerShell :

```powershell
$body = @{
    click_id = "VOTRE_CLICK_ID_ICI"
    event = "ftd"
    payout = 150.00
    secret = "dev-shared-secret-token-12345"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/postback" -Method POST -Body $body -ContentType "application/json"
```

**Réponse :**
```json
{
  "status": "success",
  "message": "FTD and payout recorded"
}
```

### 4. Voir les Statistiques

```powershell
# Stats globales
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-RestMethod -Uri "http://localhost:5000/admin/stats" -Headers @{Authorization="Basic $cred"}

# Stats pour un sub1 spécifique
Invoke-RestMethod -Uri "http://localhost:5000/admin/stats/sub1/mon_premier_test" -Headers @{Authorization="Basic $cred"}
```

Ou plus simple, dans votre navigateur (vous aurez une popup de login) :
```
http://localhost:5000/admin/stats
```

---

## 🌐 Intégration Landing Pages

### Modifier vos Landing Bolt

**AVANT :**
```html
<a href="https://casino-alpha.com/register">Jouer</a>
```

**APRÈS :**
```html
<a href="http://localhost:5000/click?sub1=bolt_landing_1">Jouer</a>
```

### Exemples par Source

**Landing Facebook :**
```html
<a href="http://localhost:5000/click?sub1=fb_winter_promo&source=facebook&campaign=winter2024">
  Réclamez 500€ de Bonus
</a>
```

**Landing Google Ads :**
```html
<a href="http://localhost:5000/click?sub1=google_main_lp&source=google&campaign=casino_jan">
  Jouer Maintenant
</a>
```

**Landing Email :**
```html
<a href="http://localhost:5000/click?sub1=email_newsletter_jan&source=email">
  Offre Exclusive Abonnés
</a>
```

### Convention de Nommage sub1

Format recommandé : `{source}_{page}_{variant}`

**Exemples :**
- `fb_lp1_varA` → Facebook, Landing Page 1, Variante A
- `google_hero_winter` → Google Ads, Section hero, Campagne hiver
- `email_promo_vip` → Email, Promo, Segment VIP
- `affiliate_john` → Affilié John

**Règle d'or :** Un sub1 = une source de trafic homogène

---

## 🎰 Configuration Casinos

### Étape 1 : Supprimer les Casinos de Test

```powershell
# Via API
curl -X DELETE http://localhost:5000/admin/offers/1 -u admin:admin123
curl -X DELETE http://localhost:5000/admin/offers/2 -u admin:admin123
curl -X DELETE http://localhost:5000/admin/offers/3 -u admin:admin123
curl -X DELETE http://localhost:5000/admin/offers/4 -u admin:admin123
```

Ou via Swagger UI : http://localhost:5000/docs

### Étape 2 : Ajouter Vos Vrais Casinos

```powershell
$casino1 = @{
    name = "Casino Alpha Réel"
    casino_url = "https://tracking.casino-alpha.com/click?affid=VOTRE_ID"
    active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/admin/offers" `
  -Method POST `
  -Body $casino1 `
  -ContentType "application/json" `
  -Headers @{Authorization="Basic $(Base64Encode('admin:admin123'))"}
```

**Répétez pour chaque casino.**

### Étape 3 : Configurer les Postbacks

Donnez cette configuration à chaque casino :

**URL Postback :**
```
POST http://VOTRE_DOMAINE.com/postback
```

**Format (JSON) :**
```json
{
  "click_id": "{CLICK_ID_MACRO}",
  "event": "ftd",
  "payout": {PAYOUT_MACRO},
  "secret": "VOTRE_SHARED_SECRET"
}
```

**Macros par plateforme :**

| Plateforme | Click ID | Payout |
|------------|----------|--------|
| Everflow | `{transaction_id}` | `{payout}` |
| Affise | `{clickid}` | `{payout}` |
| Cellxpert | `[clickid]` | `[commission]` |
| Voluum | `{click_id}` | `{payout}` |

---

## 📊 Surveillance & Stats

### Endpoints Principaux

**1. Stats Globales (tous sub1 agrégés)**
```
GET http://localhost:5000/admin/stats
```

**2. Liste de tous les sub1**
```
GET http://localhost:5000/admin/stats/sub1
```

**3. Stats détaillées par sub1**
```
GET http://localhost:5000/admin/stats/sub1/fb_landing_1
```

**Exemple de réponse :**
```json
[
  {
    "sub1": "fb_landing_1",
    "offer_id": 2,
    "offer_name": "Casino Beta",
    "total_clicks": 156,
    "total_ftds": 8,
    "total_payout": 1200.00,
    "conversion_rate": 5.13,
    "ev": 7.69,
    "weight": 1.0
  },
  {
    "sub1": "fb_landing_1",
    "offer_id": 1,
    "offer_name": "Casino Alpha",
    "total_clicks": 144,
    "total_ftds": 4,
    "total_payout": 600.00,
    "conversion_rate": 2.78,
    "ev": 4.17,
    "weight": 0.54
  }
]
```

**Interprétation :**
- Casino Beta (weight 1.0) = Meilleur performer
- Casino Alpha (weight 0.54) = 54% aussi bon que Beta
- Plus le weight est élevé, plus le casino reçoit de trafic

### Forcer une Mise à Jour des Poids

```powershell
# Mise à jour globale
Invoke-RestMethod -Method POST "http://localhost:5000/admin/update-weights" `
  -Headers @{Authorization="Basic $(Base64Encode('admin:admin123'))"}

# Mise à jour pour un sub1 spécifique
Invoke-RestMethod -Method POST "http://localhost:5000/admin/update-weights?sub1=fb_landing_1" `
  -Headers @{Authorization="Basic $(Base64Encode('admin:admin123'))"}
```

### Logs en Temps Réel

```powershell
# Voir tous les logs
docker-compose logs -f app

# Logs PostgreSQL
docker-compose logs -f postgres

# Filtre pour les erreurs
docker-compose logs app | Select-String "ERROR"

# Filtre pour les FTD
docker-compose logs app | Select-String "FTD"
```

---

## 🚀 Production

### Checklist Avant Déploiement

- [ ] Secrets changés dans `.env`
- [ ] Password admin sécurisé
- [ ] Docker Compose en mode production (enlever `--reload`)
- [ ] Firewall configuré (seulement ports 80/443/22)
- [ ] HTTPS configuré (Let's Encrypt)
- [ ] Backup base de données planifié
- [ ] Monitoring activé (UptimeRobot, etc.)

### Modifier pour Production

**docker-compose.yml :**
```yaml
# ENLEVER --reload
command: uvicorn app:app --host 0.0.0.0 --port 5000
```

**.env :**
```bash
ENVIRONMENT=production
SHARED_POSTBACK_SECRET=secret-super-securise-32-chars
ADMIN_PASSWORD=password-tres-complexe-16-chars
```

### Déploiement Serveur

**Option 1 : VPS Simple (DigitalOcean, Linode)**

1. Créer un droplet Ubuntu 22.04 (2GB RAM)
2. Installer Docker
3. Uploader le projet via Git ou SCP
4. Lancer `docker-compose up -d`
5. Configurer Nginx + Let's Encrypt pour HTTPS

**Option 2 : Cloud Managé (Render, Railway, Fly.io)**

Ces plateformes détectent automatiquement Docker Compose.

---

## 🔧 Dépannage

### Problème : Port 5000 déjà utilisé

```powershell
# Trouver le process
netstat -ano | findstr :5000

# Tuer le process (remplacer PID)
taskkill /PID <PID> /F

# Ou changer le port dans docker-compose.yml
ports:
  - "5001:5000"
```

### Problème : Docker ne démarre pas

```powershell
# Vérifier l'état
docker ps

# Voir les erreurs
docker-compose logs

# Redémarrer proprement
docker-compose down
docker-compose up --build
```

### Problème : Base de données inaccessible

```powershell
# Attendre 15-20 secondes après le démarrage
timeout /t 20

# Vérifier PostgreSQL
docker-compose logs postgres

# Se connecter manuellement
docker-compose exec postgres psql -U casino_user -d casino_router
```

### Problème : Postback retourne 401

**Cause :** Secret incorrect

**Solution :** Vérifier que le `secret` dans le postback correspond exactement à `SHARED_POSTBACK_SECRET` dans `.env`

### Problème : Pas de stats pour mon sub1

**Causes possibles :**
1. Orthographe du sub1 différente (sensible à la casse)
2. Aucun click enregistré
3. Erreur lors du click

**Vérification :**
```powershell
# Lister tous les sub1 existants
Invoke-RestMethod "http://localhost:5000/admin/stats/sub1" `
  -Headers @{Authorization="Basic $(Base64Encode('admin:admin123'))"}
```

---

## 📞 Support

### Commandes Utiles

```powershell
# Status des conteneurs
docker-compose ps

# Restart complet
docker-compose restart

# Arrêt propre
docker-compose down

# Nettoyage complet (⚠️ SUPPRIME LES DONNÉES)
docker-compose down -v

# Rebuild complet
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Accès Base de Données

```powershell
# Shell PostgreSQL
docker-compose exec postgres psql -U casino_user -d casino_router

# Requêtes utiles (dans psql):
SELECT * FROM offers;
SELECT * FROM clicks ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM ftd_events;
SELECT * FROM offer_weights ORDER BY sub1, weight DESC;
```

---

## 🎓 Prochaines Étapes

1. ✅ **Testez localement** avec quelques clicks
2. ✅ **Intégrez 1 landing Bolt** en test
3. ✅ **Configurez 1 casino réel** avec postback
4. ✅ **Vérifiez le cycle complet** (click → FTD → stats)
5. ✅ **Déployez en production**
6. ✅ **Intégrez toutes vos landings**
7. ✅ **Ajoutez tous vos casinos**
8. 🚀 **Profitez de l'optimisation automatique !**

---

**Besoin d'aide ?** Consultez les autres fichiers de documentation :
- `README.md` - Vue d'ensemble technique
- `API_DOCS.md` - Documentation API complète
- `BOLT_INTEGRATION.md` - Exemples d'intégration
- `PRODUCTION_DEPLOYMENT.md` - Guide de déploiement production

**Bon routage ! 🎰💰**






