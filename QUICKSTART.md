# 🚀 Démarrage Rapide - Casino Router

**Setup en 5 minutes chrono !**

---

## ⚡ Installation Express

### Windows

1. **Double-cliquez sur `setup.bat`**
2. Attendez la fin de l'installation (2-3 minutes)
3. Ouvrez http://localhost:5000/health
4. ✅ **C'est prêt !**

### macOS / Linux

```bash
chmod +x setup.sh
./setup.sh
```

---

## 🎯 Premier Test (30 secondes)

### 1. Ouvrir la documentation interactive
```
http://localhost:5000/docs
```

### 2. Tester un click
```
http://localhost:5000/click?sub1=test_devin
```

→ Vous serez redirigé vers un casino exemple

### 3. Voir le dashboard
```
Ouvrir: dashboard.html dans votre navigateur
Login: admin / admin123
```

---

## 📊 Accès Rapide

| Service | URL | Credentials |
|---------|-----|-------------|
| **API** | http://localhost:5000 | - |
| **Health Check** | http://localhost:5000/health | - |
| **Swagger UI** | http://localhost:5000/docs | - |
| **Stats Admin** | http://localhost:5000/admin/stats | admin / admin123 |
| **Dashboard** | Ouvrir `dashboard.html` | admin / admin123 |

---

## 🔧 Commandes Essentielles

```powershell
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f app

# Restart
docker-compose restart

# Stats via PowerShell
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
Invoke-RestMethod "http://localhost:5000/admin/stats" -Headers @{Authorization="Basic $cred"}
```

---

## 📚 Documentation

- **Guide Complet** → `GUIDE_COMPLET_FR.md` (COMMENCEZ ICI)
- **Intégration Bolt** → `BOLT_INTEGRATION.md`
- **API** → `API_DOCS.md`
- **Production** → `PRODUCTION_DEPLOYMENT.md`

---

## ✅ Checklist Setup

- [ ] Docker installé et démarré
- [ ] `docker-compose up -d` exécuté
- [ ] http://localhost:5000/health renvoie "healthy"
- [ ] Dashboard accessible (dashboard.html)
- [ ] Test click effectué
- [ ] Stats visibles

**Si tout est coché → Vous êtes prêt ! 🎉**

---

## 🆘 Problème ?

### Port 5000 déjà utilisé
```powershell
# Changer le port dans docker-compose.yml
ports:
  - "5001:5000"  # Utiliser 5001
```

### Docker ne démarre pas
1. Ouvrir Docker Desktop
2. Attendre qu'il soit prêt (icône verte)
3. Réessayer

### Base de données ne répond pas
```powershell
# Attendre 15 secondes puis:
docker-compose restart
```

---

## 🎓 Prochaines Étapes

1. ✅ Lisez `GUIDE_COMPLET_FR.md`
2. ✅ Supprimez les casinos de test
3. ✅ Ajoutez vos vrais casinos
4. ✅ Intégrez vos landing pages Bolt
5. ✅ Configurez les postbacks
6. 🚀 Profitez de l'optimisation automatique !

---

**Questions ? Consultez `GUIDE_COMPLET_FR.md` pour plus de détails.**

**Let's go ! 🎰💰**






