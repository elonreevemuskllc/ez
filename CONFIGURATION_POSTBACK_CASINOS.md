# 📧 Guide : Comment Configurer les Postbacks avec les Casinos

## 🎯 Ce Document Explique

- Quoi dire à votre affiliate manager
- Comment trouver les bonnes macros
- Configuration étape par étape par plateforme

---

## 📧 Email Type à Envoyer à Votre Affiliate Manager

```
Objet : Configuration Postback S2S pour tracking

Bonjour [Nom],

Je souhaite configurer un postback S2S (serveur-à-serveur) pour tracker 
les conversions de manière plus précise.

Voici les informations dont j'ai besoin :

1. Quelles sont vos macros pour :
   - Le click_id / transaction_id
   - Le payout / commission

2. Acceptez-vous les postbacks au format JSON ?

3. Y a-t-il un secret/token requis de votre côté ?

Voici l'URL où envoyer les postbacks :
http://VOTRE_DOMAINE.com/postback

Format JSON attendu :
{
  "click_id": "{VOTRE_MACRO}",
  "event": "ftd",
  "payout": {VOTRE_MACRO_PAYOUT},
  "secret": "mon_secret_securise"
}

Merci !

Cordialement,
[Votre Nom]
```

---

## 🔍 Comment Trouver les Macros Vous-Même

### Méthode 1 : Dans leur interface affilié

La plupart des plateformes ont une page "Postback" ou "Tracking". 
Cherchez des mots-clés comme :
- Postback
- S2S Tracking
- Server-to-Server
- Webhooks
- API Callbacks

### Méthode 2 : Documentation

Cherchez dans Google :
```
[Nom du casino] + "postback macros"
[Nom de la plateforme] + "tracking macros"
```

### Méthode 3 : Support

Contactez leur support affilié via :
- Email
- Chat en ligne
- Skype (beaucoup d'affiliate managers utilisent Skype)

---

## 🏢 Configuration par Plateforme Courante

### 1️⃣ EVERFLOW (très courant dans l'iGaming)

**Interface :** Network → Offers → [Votre Offre] → Tracking → Postback

**URL Postback :**
```
http://VOTRE_DOMAINE.com/postback
```

**Method :** POST

**Content-Type :** application/json

**Body :**
```json
{
  "click_id": "{transaction_id}",
  "event": "ftd",
  "payout": {payout},
  "secret": "VOTRE_SECRET"
}
```

---

### 2️⃣ AFFISE

**Interface :** Offers → [Offre] → Tracking → Global Postback

**URL Postback :**
```
http://VOTRE_DOMAINE.com/postback
```

**Method :** POST

**Headers :**
```
Content-Type: application/json
```

**Body :**
```json
{
  "click_id": "{clickid}",
  "event": "ftd",
  "payout": {payout},
  "secret": "VOTRE_SECRET"
}
```

---

### 3️⃣ CELLXPERT

**Interface :** Media → Campaigns → [Campagne] → Postback URL

**URL Postback :**
```
http://VOTRE_DOMAINE.com/postback
```

**Format :** JSON

**Body :**
```json
{
  "click_id": "[clickid]",
  "event": "ftd",
  "payout": [commission],
  "secret": "VOTRE_SECRET"
}
```

**Note :** Cellxpert utilise des crochets `[]` au lieu d'accolades `{}`

---

### 4️⃣ VOLUUM

**Interface :** Offers → [Offre] → Postback URL

**URL Postback :**
```
http://VOTRE_DOMAINE.com/postback?click_id={clickid}&event=ftd&payout={payout}&secret=VOTRE_SECRET
```

**Method :** POST ou GET (les deux fonctionnent)

**Alternative (JSON) :**
```json
{
  "click_id": "{clickid}",
  "event": "ftd",
  "payout": {payout},
  "secret": "VOTRE_SECRET"
}
```

---

### 5️⃣ HASOFFERS / TUNE

**Interface :** Offers → [Offre] → Tracking → Postback URL

**URL Postback :**
```
http://VOTRE_DOMAINE.com/postback
```

**Method :** POST

**Body :**
```json
{
  "click_id": "{transaction_id}",
  "event": "ftd",
  "payout": {payout},
  "secret": "VOTRE_SECRET"
}
```

---

### 6️⃣ POST AFFILIATE PRO

**Interface :** Tools → Tracking → Postback Scripts

**URL Postback :**
```
http://VOTRE_DOMAINE.com/postback
```

**Body :**
```json
{
  "click_id": "!clickid",
  "event": "ftd",
  "payout": !totalcost,
  "secret": "VOTRE_SECRET"
}
```

**Note :** Post Affiliate Pro utilise `!` au lieu de `{}`

---

## 🔧 Configuration dans Votre Router

### Étape 1 : Ajouter l'URL du casino avec {click_id}

Quand vous ajoutez un casino dans le router, incluez TOUJOURS `{click_id}` :

**Exemples corrects :**
```
https://track.casino.com/click?aid=123&subid={click_id}
https://aff.casino.com/click.php?pid=456&clickid={click_id}
https://tracking.casino.com/r?a=789&s1={click_id}
```

**❌ Incorrect (manque {click_id}) :**
```
https://track.casino.com/click?aid=123
```

### Étape 2 : Trouver où mettre le subid

Chaque plateforme a un paramètre différent pour passer le subid :

| Plateforme | Paramètre pour subid |
|------------|----------------------|
| Everflow | `&transaction_id={click_id}` |
| Affise | `&clickid={click_id}` |
| Cellxpert | `&clickid={click_id}` |
| Voluum | `&cid={click_id}` |
| HasOffers | `&aff_sub={click_id}` |

**Demandez à votre AM quel paramètre utiliser !**

---

## ✅ Checklist de Vérification

Avant de mettre en prod, vérifiez :

- [ ] Vous avez les bonnes macros du casino
- [ ] L'URL du casino contient `{click_id}` au bon endroit
- [ ] Le postback est configuré côté casino
- [ ] Le secret est identique des deux côtés
- [ ] Vous avez fait un test complet (click → conversion → stats)

---

## 🧪 Comment Tester

### Test 1 : URL du casino

Ajoutez le casino et faites un clic test :
```
http://localhost:5000/click?sub1=test_casino_alpha
```

Regardez l'URL finale - elle doit contenir un `click_id` unique

### Test 2 : Postback

Simulez manuellement un postback (PowerShell) :

```powershell
$body = @{
    click_id = "click_test_123"
    event = "ftd"
    payout = 100.00
    secret = "dev-shared-secret-token-12345"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/postback" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

Résultat attendu : `{"status": "success"}`

### Test 3 : Avec un vrai casino

1. Faites un clic depuis votre landing
2. Inscrivez-vous réellement sur le casino (ou demandez à un ami)
3. Faites un petit dépôt (10-20€)
4. Attendez 5-10 minutes
5. Vérifiez vos stats : `http://localhost:5000/admin/stats`

Si vous voyez le FTD → **C'EST BON !** ✅

---

## 🚨 Problèmes Courants

### "Le casino ne peut pas envoyer en JSON"

Certains vieux systèmes n'acceptent que les URL GET.

**Solution :** Modifiez votre endpoint pour accepter GET aussi (demandez-moi si besoin)

### "Le casino demande une IP whitelist"

Certains casinos veulent whitelister votre IP serveur.

**Solution :** 
1. Déployez votre router sur un VPS
2. Donnez l'IP du VPS à votre AM
3. Ils whitelist l'IP

### "Le postback arrive mais est rejeté (401)"

Le secret ne correspond pas.

**Solution :**
1. Vérifiez le `.env` : `SHARED_POSTBACK_SECRET=...`
2. Vérifiez que le casino envoie exactement le même secret

### "Le click_id n'est pas transmis"

L'URL du casino ne contient pas `{click_id}` ou utilise le mauvais paramètre.

**Solution :**
1. Vérifiez l'URL dans votre router : `/admin/offers`
2. Demandez au casino le bon paramètre pour le subid

---

## 📊 Surveiller les Conversions

### Dashboard quotidien

Mettez en favori :
```
http://localhost:5000/admin/stats
```

Vérifiez chaque jour :
- Nombre de clicks
- Nombre de FTDs
- Payout total
- Quel casino performe le mieux

### Logs en temps réel

```powershell
docker-compose -f "C:\Users\trooz\Desktop\Nouveau dossier (2)\david\david\docker-compose.yml" logs -f app | Select-String "FTD"
```

Vous verrez chaque conversion en direct ! 💰

---

## 🎯 Résumé Ultra-Simple

**Pour CHAQUE casino :**

1. **Obtenez votre lien affilié**
   → Ex: `https://track.casino.com/click?aid=123`

2. **Ajoutez `{click_id}` à la fin**
   → Ex: `https://track.casino.com/click?aid=123&subid={click_id}`

3. **Ajoutez le casino dans le router**
   → Via `http://localhost:5000/docs`

4. **Demandez les macros au casino**
   → Email à votre AM

5. **Configurez le postback côté casino**
   → Dans leur interface affilié

6. **Testez !**
   → Click → Inscription → Dépôt → Vérifiez stats

---

## 💬 Questions Fréquentes

**Q: Tous les casinos doivent utiliser le même secret ?**
R: OUI ! C'est le `SHARED_POSTBACK_SECRET` dans votre `.env`

**Q: Je peux avoir plusieurs casinos ?**
R: OUI ! Autant que vous voulez. C'est tout l'intérêt du router.

**Q: Le casino peut envoyer plusieurs types d'events ?**
R: OUI ! Mais le router ne traite que `"event": "ftd"` pour le moment.

**Q: Combien de temps pour voir l'optimisation ?**
R: Après ~20-30 conversions par sub1, vous verrez les poids s'ajuster.

---

**Besoin d'aide ?** Ouvrez `GUIDE_TEST_COMPLET.md` ou contactez votre développeur.

🚀 **Bon setup !**

