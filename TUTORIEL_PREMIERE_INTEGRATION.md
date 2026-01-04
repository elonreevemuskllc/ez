# 🎓 TUTORIEL PAS-À-PAS - Votre Première Intégration

## 🎯 Objectif de ce Guide

À la fin, vous aurez :
- ✅ 1 landing page Bolt connectée au router
- ✅ 1 casino configuré avec postback
- ✅ 1 test complet qui fonctionne

**Temps estimé : 30 minutes**

---

## 📍 ÉTAPE 0 : Vérification Initiale

### Assurez-vous que le router fonctionne

Ouvrez votre navigateur :
```
http://localhost:5000/health
```

**Résultat attendu :**
```json
{
  "status": "healthy",
  "database": "connected",
  "active_offers": 4
}
```

✅ **Si vous voyez ça → Passez à l'étape 1**  
❌ **Sinon → Relancez** `setup.bat` et attendez 2 minutes

---

## 📍 ÉTAPE 1 : Créez Votre Première Landing Bolt (5 min)

### 1.1 : Dans Bolt.new, créez une nouvelle page

Utilisez ce prompt pour Bolt :

```
Crée-moi une landing page de casino avec :
- Un titre accrocheur "Gagnez 500€ de Bonus"
- Une description courte
- Un gros bouton CTA "Jouer Maintenant"
- Design moderne et coloré
```

### 1.2 : Modifiez le bouton

**Trouvez dans le code généré :**
```html
<button ...>Jouer Maintenant</button>
```

**Remplacez par :**
```html
<a 
  href="http://localhost:5000/click?sub1=ma_premiere_landing"
  style="..."
  class="..."
>
  Jouer Maintenant
</a>
```

**OU si c'est un composant React/Bolt :**
```jsx
<Button 
  as="a"
  href="http://localhost:5000/click?sub1=ma_premiere_landing"
>
  Jouer Maintenant
</Button>
```

### 1.3 : Testez

- Sauvegardez dans Bolt
- Cliquez sur le bouton
- Vous devez être redirigé vers un casino de test

✅ **Ça redirige ? → Passez à l'étape 2**

---

## 📍 ÉTAPE 2 : Ajoutez Votre Premier Casino (10 min)

### 2.1 : Vous avez déjà un lien d'affilié ?

**OUI → Passez à 2.2**  
**NON → Utilisez un casino de test pour l'instant**

### 2.2 : Préparez l'URL

**Votre lien d'origine :**
```
https://track.votre-casino.com/click?affid=12345
```

**Ajoutez `&subid={click_id}` :**
```
https://track.votre-casino.com/click?affid=12345&subid={click_id}
```

💡 **Note :** Parfois c'est `&sub1=` ou `&s1=` ou `&clickid=` → Demandez à votre affiliate manager !

### 2.3 : Ajoutez dans le router

Ouvrez : http://localhost:5000/docs

1. Cherchez `POST /admin/offers`
2. Cliquez sur "Try it out"
3. Entrez vos credentials :
   - Username: `admin`
   - Password: `admin123`
4. Body :
```json
{
  "name": "Mon Premier Casino",
  "casino_url": "https://track.votre-casino.com/click?affid=12345&subid={click_id}",
  "active": true
}
```
5. Cliquez "Execute"

**Résultat :**
```json
{
  "id": 5,
  "name": "Mon Premier Casino",
  ...
}
```

✅ **Casino ajouté ! → Passez à l'étape 3**

---

## 📍 ÉTAPE 3 : Configurez le Postback (10 min)

### 3.1 : Contactez votre affiliate manager

**Copiez-collez cet email :**

```
Objet : Configuration Postback S2S

Bonjour,

Je souhaite configurer un postback pour le tracking des conversions.

Informations nécessaires :

URL Postback : http://localhost:5000/postback
Méthode : POST
Format : JSON

Pourriez-vous me confirmer :
1. La macro pour le click_id (ex: {clickid}, {transaction_id}, etc.)
2. La macro pour le payout (ex: {payout}, {commission}, etc.)
3. Dois-je utiliser un token/secret spécifique ?

Merci !

[Votre nom]
```

### 3.2 : Attendez la réponse

**Exemple de réponse typique :**
```
Bonjour,

Utilisez ces macros :
- Click ID : {clickid}
- Payout : {payout}

Pas de token requis de notre côté.

Cordialement
```

### 3.3 : Configurez dans leur dashboard

**Connectez-vous** au dashboard affilié du casino

**Cherchez la section :**
- "Postback"
- "S2S Tracking"
- "Webhooks"
- "Server-to-Server"

**Remplissez :**

**URL :**
```
http://localhost:5000/postback
```

**Method/Méthode :**
```
POST
```

**Content-Type :**
```
application/json
```

**Body/Corps :**
```json
{
  "click_id": "{clickid}",
  "event": "ftd",
  "payout": {payout},
  "secret": "dev-shared-secret-token-12345"
}
```

⚠️ **Remplacez `{clickid}` et `{payout}` par LEURS macros !**

**Enregistrez** ✅

---

## 📍 ÉTAPE 4 : Test Complet (5 min)

### 4.1 : Test du Click

Dans votre navigateur :
```
http://localhost:5000/click?sub1=ma_premiere_landing
```

**Vous êtes redirigé vers votre casino ?** ✅

**Copiez le `click_id` dans l'URL** (ex: `click_abc123xyz`)

### 4.2 : Simuler une Conversion

Ouvrez PowerShell :

```powershell
$body = @{
    click_id = "COLLEZ_VOTRE_CLICK_ID_ICI"
    event = "ftd"
    payout = 150.00
    secret = "dev-shared-secret-token-12345"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/postback" -Method POST -Body $body -ContentType "application/json"
```

**Résultat attendu :**
```json
{
  "status": "success",
  "message": "FTD and payout recorded"
}
```

✅ **Ça marche ? → Passez à l'étape 5**

### 4.3 : Vérifiez les Stats

Ouvrez dans votre navigateur :
```
http://localhost:5000/admin/stats/sub1/ma_premiere_landing
```

**Login :** admin  
**Password :** admin123

**Vous devez voir :**
```json
[
  {
    "sub1": "ma_premiere_landing",
    "offer_name": "Mon Premier Casino",
    "total_clicks": 1,
    "total_ftds": 1,
    "total_payout": 150.00,
    ...
  }
]
```

🎉 **FÉLICITATIONS ! Tout fonctionne !** 🎉

---

## 📍 ÉTAPE 5 : Test Avec Un Vrai Dépôt (Optionnel)

### Si vous voulez tester avec de l'argent réel :

1. Cliquez sur votre landing Bolt
2. Inscrivez-vous réellement sur le casino
3. Faites un petit dépôt (10-20€)
4. Attendez 5-10 minutes
5. Vérifiez vos stats : `http://localhost:5000/admin/stats`

**Le FTD apparaît dans les stats ?** 🎉 **C'EST BON !**

---

## 📍 ÉTAPE 6 : Ajoutez Plus de Casinos (Répétez Étape 2-3)

### Pour chaque nouveau casino :

1. Obtenez le lien d'affilié
2. Ajoutez `&subid={click_id}`
3. Ajoutez via `/docs` → POST /admin/offers
4. Configurez le postback chez eux
5. Testez

**Objectif :** Avoir 3-5 casinos minimum pour voir l'optimisation

---

## 📍 ÉTAPE 7 : Ajoutez Plus de Landings (Répétez Étape 1)

### Créez plusieurs landing pages :

1. **Landing Facebook** → `sub1=fb_landing_winter`
2. **Landing Google** → `sub1=google_ads_main`
3. **Landing Email** → `sub1=email_newsletter_jan`

**Important :** Chaque landing = 1 sub1 UNIQUE

---

## 📊 COMPRENDRE L'OPTIMISATION

### Après 20-30 conversions, le système va :

1. **Calculer** quel casino performe le mieux pour chaque landing
2. **Ajuster** les poids automatiquement
3. **Envoyer** plus de trafic vers les meilleurs casinos

### Exemple :

**Landing Facebook (`fb_landing_winter`) :**
- Casino A : 3 FTDs sur 100 clicks → EV = 4.50€
- Casino B : 9 FTDs sur 120 clicks → EV = 11.25€
- Casino C : 2 FTDs sur 80 clicks → EV = 3.75€

**Résultat :**
- 70% du trafic FB → Casino B (le meilleur)
- 20% du trafic FB → Casino A (exploration)
- 10% du trafic FB → Casino C (exploration)

**Landing Google (`google_ads_main`) :**
- Peut avoir des résultats DIFFÉRENTS !
- Le router optimise SÉPARÉMENT chaque sub1

---

## 🎯 Checklist Finale

Avant de passer en production :

### Configuration :
- [ ] Au moins 3 casinos configurés
- [ ] Au moins 2 landing pages intégrées
- [ ] Postbacks configurés pour tous les casinos
- [ ] Tests de click OK pour chaque landing
- [ ] Au moins 1 test complet (click → FTD → stats) réussi

### Sécurité :
- [ ] Changé `SHARED_POSTBACK_SECRET` dans `.env`
- [ ] Changé `ADMIN_PASSWORD` dans `.env`
- [ ] Redémarré le router après changement

### Production :
- [ ] Router déployé sur un serveur
- [ ] Domaine configuré (ex: `https://router.votre-domaine.com`)
- [ ] Remplacé `localhost:5000` par votre domaine dans TOUTES les landings
- [ ] IPs whitelistées si nécessaire

---

## 🚀 Vous Êtes Prêt pour la Prod !

### Commandes Finales :

```powershell
# Déployer sur serveur (via SSH)
ssh root@votre-serveur.com
git clone votre-repo
cd david
docker-compose up -d

# Surveiller les logs
docker-compose logs -f app

# Vérifier les stats quotidiennement
https://router.votre-domaine.com/admin/stats
```

---

## 📞 Si Vous Êtes Bloqué

### Problème à l'étape 1 ?
→ Lisez `EXPLICATION_SIMPLE.md` section "Intégration Bolt"

### Problème à l'étape 2 ?
→ Lisez `CONFIGURATION_POSTBACK_CASINOS.md`

### Problème à l'étape 4 ?
→ Lisez `GUIDE_TEST_COMPLET.md`

### Autre problème ?
→ Lisez `GUIDE_COMPLET_FR.md` section "Dépannage"

---

## 🎊 Félicitations !

Vous avez maintenant :
- ✅ Un système de routage intelligent qui fonctionne
- ✅ Au moins 1 landing connectée
- ✅ Au moins 1 casino configuré
- ✅ Les conversions qui remontent automatiquement

**Le système va maintenant optimiser SEUL pour vous rapporter plus ! 💰**

---

## 📈 Prochaines Étapes

**Cette semaine :**
- Ajoutez 3-5 casinos
- Créez 3-5 landings Bolt
- Surveillez les premiers FTDs

**Ce mois-ci :**
- Laissez le système apprendre (100+ conversions)
- Observez les poids s'ajuster
- Comparez les performances par sub1

**Dans 3 mois :**
- Analysez les revenus
- Ajoutez plus de casinos
- Optimisez vos meilleures sources de trafic

---

🚀 **BON ROUTAGE ET EXCELLENTS REVENUS !** 💰

**N'oubliez pas : Plus vous avez de conversions, mieux le système optimise !**

