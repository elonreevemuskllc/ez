# 🧪 Guide de Test Complet - Casino Router

## Test 1 : Vérifier que le Router fonctionne

### Étape 1 : Cliquez sur ce lien dans votre navigateur
```
http://localhost:5000/click?sub1=test_integration
```

### Résultat attendu :
- Vous êtes redirigé vers un casino
- L'URL contient `click_id=click_XXXXXXXXX`
- **COPIEZ ce click_id** pour l'étape suivante

---

## Test 2 : Simuler un FTD (conversion)

### Étape 2 : Ouvrez PowerShell et exécutez (remplacez VOTRE_CLICK_ID) :

```powershell
$body = @{
    click_id = "VOTRE_CLICK_ID"
    event = "ftd"
    payout = 150.00
    secret = "dev-shared-secret-token-12345"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/postback" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### Résultat attendu :
```json
{
  "status": "success",
  "message": "FTD and payout recorded"
}
```

---

## Test 3 : Vérifier les statistiques

### Étape 3 : Ouvrez dans votre navigateur
```
http://localhost:5000/admin/stats/sub1/test_integration
```

- **Login :** admin
- **Password :** admin123

### Résultat attendu :
Vous devez voir :
- `total_clicks: 1`
- `total_ftds: 1`
- `total_payout: 150.00`

---

## ✅ SI TOUT ÇA FONCTIONNE → VOTRE SYSTÈME EST OPÉRATIONNEL !

---

## Test 4 : Tester avec vos Landings Bolt

### Étape 4 : Dans une landing Bolt, ajoutez ce bouton :

```html
<a href="http://localhost:5000/click?sub1=ma_landing_bolt_test&source=test">
  🎰 TESTER MAINTENANT
</a>
```

### Étape 5 : Cliquez dessus depuis votre landing

### Étape 6 : Vérifiez les stats
```
http://localhost:5000/admin/stats/sub1/ma_landing_bolt_test
```

---

## Test 5 : Vérifier l'optimisation automatique

### Après plusieurs conversions, le router va automatiquement :
1. Calculer quel casino performe le mieux pour chaque `sub1`
2. Envoyer plus de trafic vers les meilleurs casinos
3. Continuer à tester les autres (exploration)

### Pour forcer une mise à jour :
```
http://localhost:5000/admin/update-weights
```
(Login: admin / admin123)

---

## 🚨 Problèmes Courants

### "Je suis redirigé mais pas de click_id dans l'URL"
→ Vérifiez que votre URL casino contient `{click_id}`

### "Le postback retourne 401 Unauthorized"
→ Le secret est incorrect. Vérifiez dans `.env`

### "Pas de stats pour mon sub1"
→ Vérifiez l'orthographe exacte (sensible à la casse)

---

## 📞 Commandes Utiles

### Voir tous les sub1 existants :
```
http://localhost:5000/admin/stats/sub1
```

### Voir tous les casinos :
```
http://localhost:5000/admin/offers
```

### Voir les logs en temps réel :
```powershell
docker-compose -f "C:\Users\trooz\Desktop\Nouveau dossier (2)\david\david\docker-compose.yml" logs -f app
```

---

## 🎯 Une Fois les Tests OK

1. Remplacez les casinos de test par vos vrais casinos
2. Configurez les postbacks avec chaque casino
3. Intégrez tous vos boutons Bolt
4. Surveillez les stats quotidiennement
5. Profitez de l'optimisation automatique ! 💰

---

**Bon test ! 🚀**

