# 🎰 CASINO ROUTER - GUIDE COMPLET DU PROJET

## 📖 TABLE DES MATIÈRES

1. [Qu'est-ce que le Casino Router ?](#quest-ce-que-le-casino-router)
2. [Pourquoi ce projet ?](#pourquoi-ce-projet)
3. [Architecture du système](#architecture-du-système)
4. [Ce qui a été construit](#ce-qui-a-été-construit)
5. [Installation complète (de zéro)](#installation-complète-de-zéro)
6. [Configuration des casinos](#configuration-des-casinos)
7. [Utilisation](#utilisation)
8. [Monitoring et analyse](#monitoring-et-analyse)
9. [Maintenance](#maintenance)
10. [Troubleshooting](#troubleshooting)

---

## 📌 QU'EST-CE QUE LE CASINO ROUTER ?

Le **Casino Router** est un système intelligent d'optimisation de trafic pour l'affiliation casino. Il analyse en temps réel les performances de plusieurs casinos et redirige automatiquement chaque visiteur vers le casino qui maximisera tes revenus.

### Concept Simple

```
┌─────────────────────────────────────────────────────────────────┐
│  TON TRAFIC (TikTok, YouTube, Instagram, etc.)                   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  CASINO ROUTER (Système Intelligent)                             │
│  • Détecte le pays du visiteur                                   │
│  • Vérifie les restrictions horaires                             │
│  • Calcule l'EPC de chaque casino                                │
│  • Choisit le casino le plus rentable                            │
└─────────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Casino A │    │ Casino B │    │ Casino C │
    │  75€ CPA │    │  70€ CPA │    │  55€ CPA │
    └──────────┘    └──────────┘    └──────────┘
```

---

## 💡 POURQUOI CE PROJET ?

### Problème Sans Router

Tu as 4 casinos avec des CPA différents :
- MyStake : 55€
- iCE : 50€
- SpinGranny : 75€
- 7ladies : 70€

**Comment savoir lequel choisir ?** 🤔

Si tu envoies tout ton trafic vers SpinGranny (75€) parce que c'est le plus cher, tu perds de l'argent si :
- Un visiteur vient d'un pays où SpinGranny ne convertit pas bien
- Il clique en semaine (SpinGranny est restreint aux soirées/weekends)
- MyStake ou iCE convertissent mieux avec ton type de trafic

### Solution Avec Router

Le router **teste automatiquement** tous les casinos, **apprend** lesquels performent le mieux, et **optimise** la distribution du trafic pour **maximiser tes revenus**.

**Résultat : +15% à +30% de revenus** sur le même trafic ! 💰

---

## 🏗️ ARCHITECTURE DU SYSTÈME

### Stack Technique

```
┌─────────────────────────────────────────────────────────────────┐
│  FRONTEND                                                         │
│  • Dashboard HTML/CSS/JavaScript (temps réel)                    │
│  • Refresh automatique toutes les 3 secondes                     │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  BACKEND (FastAPI - Python)                                       │
│  • API REST pour clicks, postbacks, stats                        │
│  • Authentification admin (Basic Auth)                           │
│  • Rate limiting (protection contre spam)                        │
│  • Logging complet                                               │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  LOGIQUE MÉTIER                                                   │
│  • Géo-ciblage (ipapi.co)                                        │
│  • Restrictions horaires (pytz)                                  │
│  • Calcul EPC (Expected Value)                                   │
│  • Algorithme 80/20 (Exploitation/Exploration)                   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  BASE DE DONNÉES (PostgreSQL)                                     │
│  • Clicks (click_id, sub1, IP, timestamp)                        │
│  • Offers (casinos, URLs, CPA)                                   │
│  • FTD Events (conversions)                                      │
│  • Payouts (commissions)                                         │
│  • Offer Weights (poids par source)                              │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE                                                   │
│  • Docker (containerisation)                                      │
│  • Docker Compose (orchestration)                                │
│  • ngrok (exposition publique)                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Fichiers Clés

```
david/
├── david/
│   ├── app.py                    # Application principale FastAPI
│   ├── models.py                 # Modèles de base de données (SQLAlchemy)
│   ├── performance.py            # Algorithme de sélection des casinos
│   ├── geo_restrictions.py       # Géo-ciblage avec ipapi.co
│   ├── time_restrictions.py      # Restrictions horaires
│   ├── admin.py                  # Endpoints admin
│   ├── cron.py                   # Tâches planifiées (recalcul EPC)
│   ├── config.py                 # Configuration
│   ├── requirements.txt          # Dépendances Python
│   ├── Dockerfile                # Image Docker
│   ├── docker-compose.yml        # Orchestration Docker
│   ├── .env                      # Variables d'environnement
│   ├── dashboard_live.html       # Dashboard interactif temps réel
│   └── [documentation...]        # Guides et docs
```

---

## 🔧 CE QUI A ÉTÉ CONSTRUIT

### 1. Système de Routing Intelligent

**Algorithme de sélection** :
1. Filtre les casinos actifs
2. Applique les restrictions géographiques
3. Applique les restrictions horaires
4. Calcule l'EPC de chaque casino restant
5. Sélection 80/20 (80% meilleur EPC, 20% exploration)

**Formule EPC** :
```
EPC = (Nombre de FTDs × CPA) ÷ Nombre total de clicks
```

### 2. Géo-Ciblage Automatique

**Pays BE/CH/IT/DE/CA** → **UNIQUEMENT 7ladies** (70€ CPA)
- Détection via ipapi.co
- Exclusivité géographique (autres casinos bloqués)
- Fallback intelligent si l'IP est inconnue

**Autres pays** → MyStake, iCE, SpinGranny

### 3. Restrictions Horaires

**SpinGranny (75€ CPA)** :
- ✅ Disponible : Weekend + Soirées (19h-06h)
- ❌ Bloqué : Semaine en journée (06h-19h)

**Fuseau horaire** : Europe/Paris (configurable)

### 4. API Complète

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/click?sub1=XXX` | GET | Point d'entrée du trafic |
| `/postback` | GET/POST | Réception des FTDs des casinos |
| `/health` | GET | Status de l'API |
| `/admin/stats` | GET | Statistiques globales |
| `/admin/offers` | GET/POST/PUT/DELETE | Gestion des casinos |
| `/admin/live-clicks` | GET | Clicks en temps réel |
| `/dashboard` | GET | Dashboard classique |
| `/dashboard-live` | GET | Dashboard interactif temps réel |

### 5. Dashboard Live Interactif

**Fonctionnalités** :
- ✅ Refresh automatique toutes les 3 secondes
- ✅ Affiche les clicks en temps réel
- ✅ Montre les casinos disponibles/bloqués
- ✅ Explique POURQUOI chaque casino a été choisi
- ✅ Stats globales (clicks, FTDs, revenus, EPC)

### 6. Sécurité

- Rate limiting (protection DDoS)
- Authentification admin (Basic Auth)
- Validation des secrets postback
- Détection des FTDs dupliqués
- Logs complets pour audit

---

## 💻 INSTALLATION COMPLÈTE (DE ZÉRO)

### Prérequis

- Windows 10/11
- 8 GB RAM minimum
- Connexion Internet

---

### ÉTAPE 1 : INSTALLER DOCKER

#### 1.1 Télécharger Docker Desktop

Va sur : https://www.docker.com/products/docker-desktop/

Télécharge **Docker Desktop for Windows**

#### 1.2 Installer Docker

1. Double-clic sur `Docker Desktop Installer.exe`
2. Suis l'assistant d'installation
3. Accepte les paramètres par défaut
4. Redémarre ton PC si demandé

#### 1.3 Vérifier l'installation

Ouvre **PowerShell** et tape :

```powershell
docker --version
docker-compose --version
```

Tu dois voir :
```
Docker version 24.x.x
docker-compose version 1.29.x
```

✅ **Docker est installé !**

---

### ÉTAPE 2 : INSTALLER NGROK

#### 2.1 Créer un compte ngrok

Va sur : https://ngrok.com/

Clique sur **"Sign Up"** et crée un compte gratuit

#### 2.2 Télécharger ngrok

Une fois connecté, va sur : https://dashboard.ngrok.com/get-started/setup

Télécharge **ngrok for Windows**

#### 2.3 Installer ngrok

1. Extrais le ZIP
2. Place `ngrok.exe` dans `C:\ngrok\`
3. Ajoute `C:\ngrok` au PATH :
   - Cherche "Variables d'environnement" dans Windows
   - Édite "Path"
   - Ajoute `C:\ngrok`

#### 2.4 Authentifier ngrok

Copie ton **Authtoken** depuis le dashboard ngrok, puis dans PowerShell :

```powershell
ngrok config add-authtoken TON_AUTHTOKEN
```

#### 2.5 (Optionnel) Acheter un domaine ngrok permanent

- Va sur https://dashboard.ngrok.com/cloud-edge/domains
- Achète un domaine statique (environ 8$/mois)
- Note ton domaine : `xxx-yyy-zzz.ngrok-free.dev`

✅ **ngrok est installé !**

---

### ÉTAPE 3 : OBTENIR LE CODE DU ROUTER

Tu as déjà le dossier `david/` avec tout le code.

Structure :
```
C:\Users\TON_USER\Desktop\Nouveau dossier (2)\
└── david/
    └── david/
        ├── app.py
        ├── models.py
        ├── docker-compose.yml
        ├── Dockerfile
        ├── requirements.txt
        ├── .env
        └── [autres fichiers...]
```

---

### ÉTAPE 4 : CONFIGURER L'ENVIRONNEMENT

#### 4.1 Modifier le fichier .env

Ouvre `david/david/.env` et vérifie :

```bash
# Database
DATABASE_URL=postgresql://casino_user:casino_pass_2024@postgres:5432/casino_router

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Postback Security
SHARED_POSTBACK_SECRET=dev-shared-secret-token-12345

# Performance Engine
LAST_N_CLICKS=1000
EXPLORATION_RATE=0.20
CRON_INTERVAL_MINUTES=10

# Server
HOST=0.0.0.0
PORT=5000

# Rate Limiting
RATE_LIMIT_CLICK=1000
RATE_LIMIT_POSTBACK=500

# API Géolocalisation
IPAPI_KEY=M3ZmorMRHUNe7BNL3Feg2Y4DJ4k5RMYZvyi5m7kf0ul7MlJPDq
```

**⚠️ EN PRODUCTION, change au minimum** :
- `ADMIN_PASSWORD`
- `SHARED_POSTBACK_SECRET`

---

### ÉTAPE 5 : DÉMARRER DOCKER

#### 5.1 Ouvrir PowerShell dans le dossier

```powershell
cd "C:\Users\TON_USER\Desktop\Nouveau dossier (2)\david\david"
```

#### 5.2 Builder et démarrer les containers

```powershell
docker-compose up -d
```

**Première fois** : Prend 5-10 minutes (téléchargement des images)

#### 5.3 Vérifier que ça tourne

```powershell
docker ps
```

Tu dois voir :
```
casino_router_app    Up X seconds
casino_router_db     Up X seconds (healthy)
```

#### 5.4 Vérifier les logs

```powershell
docker-compose logs --tail=20 app
```

Tu dois voir :
```
✓ Application started successfully
```

✅ **Docker tourne !**

---

### ÉTAPE 6 : DÉMARRER NGROK

#### 6.1 Avec domaine permanent (recommandé)

```powershell
ngrok http --domain=ton-domaine.ngrok-free.dev 5000
```

Exemple :
```powershell
ngrok http --domain=subrictal-fallon-precomprehensively.ngrok-free.dev 5000
```

#### 6.2 Sans domaine (gratuit, URL change à chaque redémarrage)

```powershell
ngrok http 5000
```

Note l'URL affichée : `https://xxxx-yyyy-zzzz.ngrok-free.app`

#### 6.3 Laisser ngrok tourner

**Ne ferme PAS cette fenêtre PowerShell !**

ngrok doit tourner 24/7 pour que ton système soit accessible.

✅ **ngrok tourne !**

---

### ÉTAPE 7 : TESTER LE SYSTÈME

#### 7.1 Tester l'API

Ouvre un nouveau PowerShell :

```powershell
Invoke-RestMethod -Uri "https://ton-domaine.ngrok-free.dev/health"
```

Tu dois voir :
```
status : ok
```

#### 7.2 Tester un click

```powershell
Invoke-WebRequest -Uri "https://ton-domaine.ngrok-free.dev/click?sub1=test_installation" -MaximumRedirection 0
```

Tu dois voir une redirection 302.

#### 7.3 Ouvrir le dashboard

```powershell
Start-Process "https://ton-domaine.ngrok-free.dev/dashboard-live"
```

Ton navigateur s'ouvre sur le dashboard ! 🎉

✅ **Le système fonctionne !**

---

## 🎰 CONFIGURATION DES CASINOS

### Casinos Actuellement Configurés

| ID | Casino | CPA | Géo | Horaire | Postback |
|----|--------|-----|-----|---------|----------|
| 5 | MyStake | 55€ | Mondial (sauf BE/CH/IT/DE/CA) | 24/7 | ✅ |
| 6 | iCE | 50€ | Mondial (sauf BE/CH/IT/DE/CA) | 24/7 | ✅ |
| 7 | SpinGranny | 75€ | Mondial | Weekend + 19h-06h | ⏳ |
| 8 | 7ladies | 70€ | BE/CH/IT/DE/CA EXCLUSIF | 24/7 | ⏳ |

### Configuration des Postbacks

#### MyStake (✅ Configuré)

```
URL: https://ton-domaine.ngrok-free.dev/postback
Paramètres:
  - click_id = [trackingcode]
  - event = ftd
  - payout = 55
  - secret = dev-shared-secret-token-12345
Méthode: GET
```

#### iCE (✅ Configuré)

```
URL: https://ton-domaine.ngrok-free.dev/postback
Paramètres:
  - click_id = {clickid}
  - event = ftd
  - payout = 50
  - secret = dev-shared-secret-token-12345
Méthode: GET
```

#### SpinGranny (⏳ À Configurer - Everflow)

```
URL: https://ton-domaine.ngrok-free.dev/postback
Paramètres:
  - click_id = {transaction_id}
  - event = ftd
  - payout = 75
  - secret = dev-shared-secret-token-12345
Méthode: GET ou POST
```

#### 7ladies (⏳ À Configurer - Cellxpert)

```
URL: https://ton-domaine.ngrok-free.dev/postback
Paramètres:
  - click_id = [trackingcode]
  - event = ftd
  - payout = 70
  - secret = dev-shared-secret-token-12345
Méthode: GET ou POST
```

### Ajouter un Nouveau Casino

```powershell
$body = @{
    name = "Nouveau Casino"
    casino_url = "https://casino.com/signup?clickid={click_id}"
    postback_secret = "dev-shared-secret-token-12345"
    active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://ton-domaine.ngrok-free.dev/admin/offers" `
    -Method Post `
    -Body $body `
    -ContentType "application/json" `
    -Headers @{Authorization="Basic YWRtaW46YWRtaW4xMjM="}
```

---

## 🚀 UTILISATION

### Ton Lien de Tracking

```
https://ton-domaine.ngrok-free.dev/click?sub1=TA_SOURCE
```

### Exemples de sub1

**Par plateforme** :
```
?sub1=tiktok
?sub1=youtube
?sub1=instagram
?sub1=facebook
```

**Par contenu** :
```
?sub1=tiktok_video1
?sub1=tiktok_video2
?sub1=youtube_gaming_short
?sub1=instagram_reel_casino
```

**Par campagne** :
```
?sub1=tiktok_promo_janvier
?sub1=youtube_test_A
?sub1=instagram_story_weekend
```

### Flux Utilisateur

```
1. Utilisateur voit ton contenu (TikTok, YouTube, etc.)
2. Il clique sur ton lien
3. Le router détecte son pays via son IP
4. Le router vérifie l'heure actuelle
5. Le router calcule l'EPC de chaque casino disponible
6. Le router redirige vers le meilleur casino
7. L'utilisateur s'inscrit et dépose
8. Le casino envoie un postback au router
9. Le router enregistre le FTD et recalcule l'EPC
10. L'algorithme s'améliore pour les prochains clicks
```

---

## 📊 MONITORING ET ANALYSE

### Dashboard Live

```
https://ton-domaine.ngrok-free.dev/dashboard-live
```

**Fonctionnalités** :
- Refresh automatique toutes les 3 secondes
- Clicks en temps réel
- Pays détecté
- Casinos disponibles/bloqués
- Raison de la sélection
- Stats globales

### Dashboard Classique

```
https://ton-domaine.ngrok-free.dev/dashboard
```

**Fonctionnalités** :
- Vue d'ensemble des performances
- EPC par casino
- Performance par source (sub1)
- Graphiques d'évolution

### API Stats

```powershell
Invoke-RestMethod -Uri "https://ton-domaine.ngrok-free.dev/admin/stats" `
    -Headers @{Authorization="Basic YWRtaW46YWRtaW4xMjM="}
```

### Métriques Importantes

**EPC (Earnings Per Click)** :
- Combien tu gagnes en moyenne par click
- Plus l'EPC est élevé, meilleur est le casino

**Taux de Conversion** :
- Pourcentage de clicks qui deviennent des FTDs
- Varie selon le casino et la source de trafic

**Revenue Total** :
- Somme de tous les payouts reçus

---

## 🔧 MAINTENANCE

### Redémarrer le Système

```powershell
cd "C:\Users\TON_USER\Desktop\Nouveau dossier (2)\david\david"
docker-compose restart
```

### Arrêter le Système

```powershell
docker-compose down
```

### Démarrer le Système

```powershell
docker-compose up -d
```

### Voir les Logs

```powershell
# Dernières 50 lignes
docker-compose logs --tail=50 app

# Logs en temps réel
docker-compose logs -f app
```

### Sauvegarder la Base de Données

```powershell
docker exec casino_router_db pg_dump -U casino_user casino_router > backup.sql
```

### Restaurer la Base de Données

```powershell
docker exec -i casino_router_db psql -U casino_user casino_router < backup.sql
```

### Nettoyer les Anciens Clicks (Optionnel)

```powershell
docker exec -i casino_router_db psql -U casino_user -d casino_router -c "DELETE FROM clicks WHERE timestamp < NOW() - INTERVAL '30 days';"
```

---

## 🆘 TROUBLESHOOTING

### Problème 1 : Docker ne démarre pas

**Symptômes** :
```
Error response from daemon: driver failed programming external connectivity
```

**Solution** :
```powershell
# Redémarre Docker Desktop
# Puis
docker-compose down
docker-compose up -d
```

### Problème 2 : ngrok ne se connecte pas

**Symptômes** :
```
ERR_NGROK_8012
```

**Solution** :
1. Vérifie que Docker tourne
2. Vérifie que le port 5000 est bien exposé
3. Redémarre ngrok :
```powershell
ngrok http --domain=ton-domaine.ngrok-free.dev 5000
```

### Problème 3 : Dashboard affiche "Loading..."

**Solution** :
```powershell
# Vérifie que l'API répond
Invoke-RestMethod -Uri "https://ton-domaine.ngrok-free.dev/health"

# Vérifie les logs
docker-compose logs --tail=50 app
```

### Problème 4 : Postback ne fonctionne pas

**Vérifications** :
1. Secret token correct ?
2. click_id valide ?
3. Format de la requête correct (GET/POST) ?

**Debug** :
```powershell
# Simule un postback
Invoke-RestMethod -Uri "https://ton-domaine.ngrok-free.dev/postback?click_id=TEST&event=ftd&payout=55&secret=dev-shared-secret-token-12345"
```

### Problème 5 : Géo-ciblage ne fonctionne pas

**Vérifications** :
1. Clé API ipapi.co valide ?
2. Limite de 30K requêtes/mois non atteinte ?

**Debug** :
```powershell
docker exec casino_router_app python geo_restrictions.py
```

---

## 📚 FICHIERS DE DOCUMENTATION

| Fichier | Description |
|---------|-------------|
| `00_GUIDE_COMPLET_PROJET.md` | ✅ Ce document |
| `CHECK_FINAL.md` | Check final avant production |
| `CONFIGURATION_FINALE.md` | Configuration des 4 casinos |
| `SPINGRANNY_SETUP.md` | SpinGranny + restrictions horaires |
| `7LADIES_GEO_TARGETING.md` | 7ladies + géo-ciblage |
| `SCHEMA_SIMPLE.md` | Schéma visuel du fonctionnement |
| `RECAP_SESSION_02_JANVIER.md` | Historique de développement |

---

## 🎓 CONCEPTS CLÉS

### EPC (Expected Value / Earnings Per Click)

**Formule** :
```
EPC = (Nombre de FTDs × CPA) ÷ Nombre total de clicks
```

**Exemple** :
- Casino A : 100 clicks, 3 FTDs à 55€ → EPC = 1.65€
- Casino B : 100 clicks, 4 FTDs à 50€ → EPC = 2.00€
→ Casino B est meilleur malgré un CPA plus faible !

### Algorithme 80/20 (Exploitation / Exploration)

- **80% Exploitation** : Envoie le trafic vers le casino avec le meilleur EPC
- **20% Exploration** : Envoie du trafic aléatoirement pour continuer à tester

**Pourquoi ?**
- Évite de se "bloquer" sur un casino qui n'est plus optimal
- Continue de découvrir de meilleures opportunités
- S'adapte aux changements de marché

### sub1 (Tracking Code)

Le `sub1` est ton identifiant de source de trafic.

**Utilité** :
- Tracker quelle source performe le mieux
- Calculer l'EPC par source
- Optimiser tes investissements publicitaires

**Exemples** :
```
?sub1=tiktok_video1  →  Vidéo TikTok #1
?sub1=youtube_gaming →  YouTube Gaming
?sub1=insta_story_A  →  Instagram Story A
```

---

## 💰 PROJECTION DE REVENUS

### Scénario : 1000 Clicks/Mois

**Sans Router (un seul casino - MyStake 55€)** :
```
1000 clicks × 2.8% conversion × 55€ = 1,540€/mois
```

**Avec Router (optimisation intelligente)** :
```
150 clicks BE/CH/IT/DE/CA × 3.3% conv × 70€ = 347€
250 clicks weekend/soirées × 3.2% conv × 75€ = 600€
400 clicks optimisés × 2.5% conv × 55€ = 550€
200 clicks optimisés × 3.5% conv × 50€ = 350€
─────────────────────────────────────────────
TOTAL = 1,847€/mois
```

**GAIN : +307€/mois (+20%)** 🚀

*Note : Taux de conversion moyens estimés, les résultats réels peuvent varier.*

---

## 🎉 FÉLICITATIONS !

Tu as maintenant un **Casino Router professionnel** avec :

✅ **4 casinos** optimisés (50€ à 75€ CPA)  
✅ **Géo-ciblage automatique** (BE/CH/IT/DE/CA → 7ladies exclusif)  
✅ **Restrictions horaires** (SpinGranny weekend + soirées)  
✅ **Optimisation EPC** automatique et continue  
✅ **Dashboard LIVE** interactif temps réel  
✅ **Tracking avancé** par source (sub1)  
✅ **API complète** pour monitoring  
✅ **Documentation exhaustive**  

**TU ES PRÊT À GÉNÉRER DES REVENUS ! 🚀💰**

---

## 📞 SUPPORT

Si tu as des questions ou des problèmes :

1. Vérifie la section **Troubleshooting**
2. Consulte les **logs** : `docker-compose logs app`
3. Vérifie que **Docker** et **ngrok** tournent
4. Relance le système : `docker-compose restart`

---

**Créé le 4 janvier 2026**  
**Version : 1.0.0**  
**Casino Router - Smart Traffic Optimization**

