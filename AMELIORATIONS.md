# 🎰 Casino Router - Améliorations & Sécurité

**Version Améliorée - Janvier 2026**

---

## 🆕 Nouvelles Fonctionnalités

### 🔒 Sécurité

✅ **Authentification Admin**
- Tous les endpoints `/admin/*` sont maintenant protégés
- Login/password configurables via variables d'environnement
- Utilisation de HTTP Basic Auth

✅ **Rate Limiting**
- `/click` : 100 requêtes/minute par IP (configurable)
- `/postback` : 200 requêtes/minute par IP (configurable)
- Protection contre l'abus et le spam

✅ **Secrets Sécurisés**
- Support de secrets aléatoires générés automatiquement
- Séparation claire dev/production
- Pas de secrets hardcodés dans le code

### 📚 Documentation

✅ **Guide Complet en Français** (`GUIDE_COMPLET_FR.md`)
- Setup pas-à-pas détaillé
- Exemples concrets
- Dépannage complet

✅ **Guide d'Intégration Bolt** (`BOLT_INTEGRATION.md`)
- Exemples HTML prêts à l'emploi
- Convention de nommage sub1
- Cas d'usage avancés

✅ **Démarrage Rapide** (`QUICKSTART.md`)
- Installation en 5 minutes
- Checklist complète
- Accès rapides

### 🛠️ Scripts de Setup

✅ **Setup Automatique**
- `setup.bat` pour Windows
- `setup.sh` pour Linux/macOS
- Génération automatique de secrets sécurisés

### 📊 Dashboard Web

✅ **Dashboard HTML** (`dashboard.html`)
- Interface visuelle simple
- Stats en temps réel
- Liste des sub1 actifs
- Auto-refresh toutes les 30 secondes

---

## 📁 Nouveaux Fichiers

```
david/
├── security.py                 # Module d'authentification
├── env.example                 # Template de configuration
├── setup.bat                   # Script setup Windows
├── setup.sh                    # Script setup Linux/macOS
├── dashboard.html              # Dashboard web simple
├── GUIDE_COMPLET_FR.md         # Guide utilisateur complet
├── BOLT_INTEGRATION.md         # Guide d'intégration Bolt
├── QUICKSTART.md               # Démarrage rapide
└── AMELIORATIONS.md            # Ce fichier
```

---

## 🔧 Modifications du Code

### `config.py`
```python
# Ajout des nouvelles variables
ADMIN_USERNAME
ADMIN_PASSWORD
ENVIRONMENT
RATE_LIMIT_CLICK
RATE_LIMIT_POSTBACK
```

### `admin.py`
```python
# Protection globale du router
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin)]  # ← NOUVEAU
)
```

### `app.py`
```python
# Ajout du rate limiting
from slowapi import Limiter

@app.get("/click")
@limiter.limit(f"{Config.RATE_LIMIT_CLICK}/minute")  # ← NOUVEAU
async def handle_click(...):

@app.post("/postback")
@limiter.limit(f"{Config.RATE_LIMIT_POSTBACK}/minute")  # ← NOUVEAU
async def handle_postback(...):
```

### `requirements.txt`
```
slowapi==0.1.9  # ← NOUVEAU
```

### `docker-compose.yml`
```yaml
environment:
  ADMIN_USERNAME: admin          # ← NOUVEAU
  ADMIN_PASSWORD: admin123       # ← NOUVEAU
  ENVIRONMENT: development       # ← NOUVEAU
  RATE_LIMIT_CLICK: 100         # ← NOUVEAU
  RATE_LIMIT_POSTBACK: 200      # ← NOUVEAU
```

---

## 🚀 Guide de Migration

Si vous avez déjà le projet installé :

### 1. Sauvegarder les données existantes

```powershell
# Backup de la base de données
docker-compose exec postgres pg_dump -U casino_user casino_router > backup.sql
```

### 2. Arrêter les services

```powershell
docker-compose down
```

### 3. Mettre à jour les fichiers

Remplacez tous les fichiers par les nouveaux.

### 4. Mettre à jour la configuration

```powershell
# Copier le template
cp env.example .env

# Éditer .env avec vos valeurs
notepad .env
```

### 5. Rebuilder et redémarrer

```powershell
docker-compose build --no-cache
docker-compose up -d
```

### 6. Restaurer les données (si nécessaire)

```powershell
# Restaurer le backup
docker-compose exec -T postgres psql -U casino_user casino_router < backup.sql
```

---

## 🔐 Configuration Sécurisée

### Générer des Secrets Forts

**PowerShell (Windows) :**
```powershell
# Générer un secret de 32 caractères
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
```

**Linux/macOS :**
```bash
# Générer un secret avec openssl
openssl rand -base64 32
```

### Fichier .env de Production

```bash
# Base de données (changer le password !)
DATABASE_URL=postgresql://casino_user:MOT_DE_PASSE_FORT@postgres:5432/casino_router

# Secrets (générer avec commandes ci-dessus)
SHARED_POSTBACK_SECRET=Xy9Kp2Lm8Nq4Rt6Vw1Az3Bx5Cy7Dz9E
ADMIN_PASSWORD=Pq7Rs9Tx2Uy4Wz6Aa8Bc0D

# Environnement
ENVIRONMENT=production

# Rate limits (ajuster selon votre trafic)
RATE_LIMIT_CLICK=500
RATE_LIMIT_POSTBACK=1000
```

---

## 📊 Utilisation du Dashboard

### Accès

1. Ouvrir `dashboard.html` dans votre navigateur
2. Login : `admin` / votre password (défini dans .env)
3. Voir les stats en temps réel

### Fonctionnalités

- **Stats Globales** : Clics, FTD, Payout total
- **Tableau Offres** : Performance par casino
- **Liste sub1** : Toutes les sources de trafic
- **Auto-refresh** : Mise à jour automatique toutes les 30s

---

## 🧪 Tests de Sécurité

### Test 1 : Authentification Admin

```powershell
# Sans auth (doit échouer)
curl http://localhost:5000/admin/stats

# Avec auth (doit fonctionner)
curl http://localhost:5000/admin/stats -u admin:admin123
```

### Test 2 : Rate Limiting

```powershell
# Faire 150 requêtes rapidement (devrait bloquer après 100)
1..150 | ForEach-Object {
    Invoke-RestMethod "http://localhost:5000/click?sub1=test_rate_limit"
}
```

### Test 3 : Postback Secret

```powershell
# Mauvais secret (doit échouer avec 401)
curl -X POST http://localhost:5000/postback `
  -H "Content-Type: application/json" `
  -d '{"click_id":"test","event":"ftd","payout":100,"secret":"mauvais_secret"}'
```

---

## 📈 Améliorations de Performance

### Avant
- ❌ Pas d'authentification
- ❌ Pas de rate limiting
- ❌ Secrets en clair
- ❌ Documentation minimale

### Après
- ✅ Authentification HTTP Basic
- ✅ Rate limiting par IP
- ✅ Secrets configurables
- ✅ Documentation complète en français
- ✅ Dashboard web
- ✅ Scripts de setup automatisés

---

## 🎯 Prochaines Améliorations Possibles

### Court Terme
- [ ] Dashboard plus avancé avec graphiques
- [ ] Export CSV des stats
- [ ] Alertes par email (FTD, erreurs)
- [ ] Tests unitaires automatisés

### Long Terme
- [ ] Interface web complète (React/Vue)
- [ ] Multi-utilisateurs avec rôles
- [ ] API webhooks pour événements
- [ ] Intégration Telegram/Slack
- [ ] Machine Learning pour prédictions

---

## 📞 Support

### Documentation
- `QUICKSTART.md` - Démarrage rapide
- `GUIDE_COMPLET_FR.md` - Guide utilisateur complet
- `BOLT_INTEGRATION.md` - Intégration landing pages
- `API_DOCS.md` - Documentation API
- `PRODUCTION_DEPLOYMENT.md` - Déploiement production

### Problèmes Courants

**Authentification ne fonctionne pas**
→ Vérifiez que `ADMIN_USERNAME` et `ADMIN_PASSWORD` sont bien définis dans `.env`

**Rate limiting trop strict**
→ Augmentez `RATE_LIMIT_CLICK` et `RATE_LIMIT_POSTBACK` dans `.env`

**Dashboard ne charge pas les stats**
→ Vérifiez les credentials et que l'API est accessible

---

## 🎓 Conclusion

Votre Casino Router est maintenant **production-ready** avec :

✅ Sécurité renforcée  
✅ Documentation complète  
✅ Dashboard fonctionnel  
✅ Setup automatisé  
✅ Protection rate limiting  

**Bon routage ! 🎰💰**






