# 🎰 Casino Router - Smart Traffic Optimization

Système intelligent d'optimisation de trafic pour l'affiliation casino avec géo-ciblage, restrictions horaires et algorithme d'apprentissage automatique.

## 🚀 Quick Start

### Sur Windows (Développement)

```powershell
cd david
docker-compose up -d
```

Ton API : `http://localhost:5000`

### Sur VPS (Production)

**Installation automatique** :

```bash
wget https://raw.githubusercontent.com/TON_USERNAME/casino-router/main/install_vps.sh
chmod +x install_vps.sh
./install_vps.sh
```

**Installation manuelle** :

```bash
git clone https://github.com/TON_USERNAME/casino-router.git /opt/casino-router
cd /opt/casino-router
docker-compose up -d
```

Voir le guide complet : [DEPLOIEMENT_VPS.md](DEPLOIEMENT_VPS.md)

---

## 📊 Fonctionnalités

### ✅ 4 Casinos Configurés

| Casino | CPA | Disponibilité | Géo-Ciblage |
|--------|-----|---------------|-------------|
| **SpinGranny** | 75 EUR | Weekend + Soirées (19h-06h) | Mondial |
| **7ladies** | 70 EUR | 24/7 | BE/CH/IT/DE/CA exclusif |
| **MyStake** | 55 EUR | 24/7 | Mondial (sauf pays 7ladies) |
| **iCE** | 50 EUR | 24/7 | Mondial (sauf pays 7ladies) |

### 🌍 Géo-Ciblage Automatique

- **BE/CH/IT/DE/CA** → UNIQUEMENT 7ladies (70€)
- **Autres pays** → MyStake, iCE, SpinGranny

Détection via ipapi.co avec fallback intelligent.

### ⏰ Restrictions Horaires

- **SpinGranny** : Disponible weekend + soirées (19h-06h)
- Fuseau horaire : Europe/Paris

### 🎯 Algorithme d'Optimisation

- **80% Exploitation** : Trafic vers le meilleur EPC
- **20% Exploration** : Test continu pour découvrir de meilleures opportunités
- **EPC = (FTDs × CPA) ÷ Clicks**
- Recalcul automatique toutes les 10 minutes

### 📊 Dashboard Live Interactif

- Refresh automatique toutes les 3 secondes
- Affiche les clicks en temps réel
- Montre les casinos disponibles/bloqués
- Explique POURQUOI chaque casino a été choisi

---

## 🔗 Endpoints Principaux

| Endpoint | Description |
|----------|-------------|
| `GET /click?sub1=SOURCE` | Point d'entrée du trafic |
| `GET/POST /postback` | Réception des FTDs |
| `GET /health` | Health check |
| `GET /dashboard-live` | Dashboard interactif |
| `GET /admin/stats` | Statistiques (auth requise) |

---

## 📁 Structure du Projet

```
.
├── app.py                      # Application FastAPI principale
├── models.py                   # Modèles SQLAlchemy
├── performance.py              # Algorithme de sélection EPC
├── geo_restrictions.py         # Géo-ciblage
├── time_restrictions.py        # Restrictions horaires
├── admin.py                    # Endpoints admin
├── config.py                   # Configuration
├── cron.py                     # Tâches planifiées
├── docker-compose.yml          # Orchestration Docker
├── Dockerfile                  # Image Docker
├── requirements.txt            # Dépendances Python
├── .env                        # Variables d'environnement
├── dashboard_live.html         # Dashboard interactif
├── install_vps.sh             # Script d'installation VPS
├── deploy.sh                   # Script de mise à jour
└── [documentation...]          # Guides et docs
```

---

## 🛠️ Commandes Utiles

### Développement (Windows)

```powershell
# Démarrer
docker-compose up -d

# Logs
docker-compose logs -f app

# Redémarrer
docker-compose restart

# Arrêter
docker-compose down
```

### Production (VPS)

```bash
# Déployer
./deploy.sh

# Logs
docker-compose logs -f app

# Backup DB
docker exec casino_router_db pg_dump -U casino_user casino_router > backup.sql

# Restaurer DB
docker exec -i casino_router_db psql -U casino_user -d casino_router < backup.sql
```

---

## 📚 Documentation

| Fichier | Description |
|---------|-------------|
| [00_GUIDE_COMPLET_PROJET.md](00_GUIDE_COMPLET_PROJET.md) | Guide complet du projet |
| [DEPLOIEMENT_VPS.md](DEPLOIEMENT_VPS.md) | Déploiement sur VPS |
| [CHECK_FINAL.md](CHECK_FINAL.md) | Check final avant production |
| [SCHEMA_SIMPLE.md](SCHEMA_SIMPLE.md) | Schéma visuel du fonctionnement |
| [SPINGRANNY_SETUP.md](SPINGRANNY_SETUP.md) | Config SpinGranny |
| [7LADIES_GEO_TARGETING.md](7LADIES_GEO_TARGETING.md) | Config 7ladies |

---

## ⚙️ Configuration

### Variables d'Environnement (.env)

```bash
# Database
DATABASE_URL=postgresql://casino_user:casino_pass_2024@postgres:5432/casino_router

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123  # À CHANGER EN PRODUCTION

# Security
SHARED_POSTBACK_SECRET=dev-shared-secret-token-12345  # À CHANGER

# Performance
LAST_N_CLICKS=1000
EXPLORATION_RATE=0.20
CRON_INTERVAL_MINUTES=10

# API Géolocalisation
IPAPI_KEY=M3ZmorMRHUNe7BNL3Feg2Y4DJ4k5RMYZvyi5m7kf0ul7MlJPDq
```

### Postbacks à Configurer

**MyStake** :
```
https://TON_DOMAINE/postback?click_id=[trackingcode]&event=ftd&payout=55&secret=TON_SECRET
```

**iCE** :
```
https://TON_DOMAINE/postback?click_id={clickid}&event=ftd&payout=50&secret=TON_SECRET
```

**SpinGranny** (Everflow) :
```
https://TON_DOMAINE/postback?click_id={transaction_id}&event=ftd&payout=75&secret=TON_SECRET
```

**7ladies** (Cellxpert) :
```
https://TON_DOMAINE/postback?click_id=[trackingcode]&event=ftd&payout=70&secret=TON_SECRET
```

---

## 🔒 Sécurité

### En Production

1. **Change les secrets** dans `.env`
2. **Active le firewall** (ports 22, 80, 443)
3. **Installe SSL** : `certbot --nginx -d ton-domaine.com`
4. **Limite le rate limiting** si nécessaire
5. **Configure des backups** automatiques

---

## 📈 Monitoring

### UptimeRobot (Gratuit)

1. Crée un compte sur https://uptimerobot.com
2. Ajoute un monitor HTTP(s) : `https://ton-domaine.com/health`
3. Configure les alertes email

### Logs

```bash
# Temps réel
docker-compose logs -f app

# Dernières 100 lignes
docker-compose logs --tail=100 app

# Logs système
journalctl -u docker -f
```

---

## 🚨 Troubleshooting

### L'API ne répond pas

```bash
# Vérifier Docker
docker ps

# Voir les logs
docker-compose logs --tail=50 app

# Redémarrer
docker-compose restart
```

### Port déjà utilisé

```bash
# Trouver le processus
lsof -i :5000

# Tuer le processus
kill -9 PID
```

### Base de données corrompue

```bash
docker-compose down
docker volume rm casino_router_pgdata
docker-compose up -d
```

---

## 💰 Projection de Revenus

### Exemple : 1000 Clicks/Mois

**Sans Router** (MyStake uniquement) :
- 1000 clicks × 2.8% conversion × 55€ = **1,540€/mois**

**Avec Router** (optimisation intelligente) :
- 150 clicks BE/CH/IT/DE/CA × 3.3% × 70€ = 347€
- 250 clicks weekend/soirées × 3.2% × 75€ = 600€
- 400 clicks optimisés × 2.5% × 55€ = 550€
- 200 clicks optimisés × 3.5% × 50€ = 350€
- **TOTAL = 1,847€/mois**

**GAIN : +307€/mois (+20%)** 🚀

---

## 🤝 Support

Pour toute question :

1. Consulte la [documentation](00_GUIDE_COMPLET_PROJET.md)
2. Vérifie les [logs](#logs)
3. Consulte le [troubleshooting](#troubleshooting)

---

## 📝 Licence

Projet privé - Tous droits réservés

---

## 🎉 Résultat

Système professionnel de routing casino avec :

✅ Géo-ciblage automatique  
✅ Restrictions horaires  
✅ Optimisation EPC temps réel  
✅ Dashboard live interactif  
✅ 4 casinos configurés (50-75€ CPA)  
✅ Documentation exhaustive  
✅ Déploiement automatisé  

**Prêt pour la production ! 💰🚀**

