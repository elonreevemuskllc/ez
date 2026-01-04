# 🎰 Exemples d'Intégration - Casino Router avec Bolt

Ce document montre comment intégrer vos landing pages Bolt avec le Casino Router.

---

## 📋 Principe de Base

**AVANT (hardcodé) :**
```html
<a href="https://casino-alpha.com/register">Jouer Maintenant</a>
```

**APRÈS (dynamique via router) :**
```html
<a href="https://VOTRE_DOMAINE.com/click?sub1=landing_1">Jouer Maintenant</a>
```

---

## 🌐 Exemples par Type de Landing

### 1. Landing Page Facebook

```html
<!DOCTYPE html>
<html>
<head>
    <title>Casino - Promotion Facebook</title>
</head>
<body>
    <h1>🎰 Gagnez Jusqu'à 500€ de Bonus !</h1>
    <p>Offre exclusive pour nos visiteurs Facebook</p>
    
    <!-- Bouton principal -->
    <a href="https://VOTRE_DOMAINE.com/click?sub1=fb_landing_winter&source=facebook&campaign=winter2024"
       class="cta-button">
        Jouer Maintenant
    </a>
</body>
</html>
```

**Paramètres expliqués :**
- `sub1=fb_landing_winter` : Identifie cette landing Facebook
- `source=facebook` : Source de trafic
- `campaign=winter2024` : Campagne en cours

---

### 2. Landing Page Google Ads

```html
<!DOCTYPE html>
<html>
<head>
    <title>Casino - Meilleur Bonus 2024</title>
</head>
<body>
    <h1>🏆 Bonus de Bienvenue : 200% jusqu'à 1000€</h1>
    
    <a href="https://VOTRE_DOMAINE.com/click?sub1=google_ads_main&source=google&campaign=casino_jan_2024"
       class="cta-button">
        Réclamez Votre Bonus
    </a>
</body>
</html>
```

---

### 3. Landing Page Affilié Spécifique

```html
<!DOCTYPE html>
<html>
<head>
    <title>Casino VIP - Accès Privilégié</title>
</head>
<body>
    <h1>♠️ Accès VIP Exclusif</h1>
    <p>Réservé aux membres de notre communauté</p>
    
    <a href="https://VOTRE_DOMAINE.com/click?sub1=affiliate_john&source=referral"
       class="cta-button">
        Accéder au Casino VIP
    </a>
</body>
</html>
```

---

### 4. Landing Page Email Marketing

```html
<!DOCTYPE html>
<html>
<head>
    <title>Casino - Offre Newsletter</title>
</head>
<body>
    <h1>📧 Offre Spéciale Abonnés</h1>
    
    <a href="https://VOTRE_DOMAINE.com/click?sub1=email_newsletter_01&source=email&campaign=newsletter_jan"
       class="cta-button">
        Profiter de l'Offre
    </a>
</body>
</html>
```

---

## 🔄 Landing Page Dynamique (plusieurs CTAs)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Top 3 Casinos 2024</title>
</head>
<body>
    <h1>🎯 Meilleurs Casinos en Ligne</h1>
    
    <!-- Casino #1 -->
    <div class="casino-card">
        <h2>Casino Alpha</h2>
        <a href="https://VOTRE_DOMAINE.com/click?sub1=top3_landing&source=organic&position=1"
           class="cta-button">
            Jouer Maintenant
        </a>
    </div>
    
    <!-- Casino #2 -->
    <div class="casino-card">
        <h2>Casino Beta</h2>
        <a href="https://VOTRE_DOMAINE.com/click?sub1=top3_landing&source=organic&position=2"
           class="cta-button">
            Découvrir
        </a>
    </div>
    
    <!-- Casino #3 -->
    <div class="casino-card">
        <h2>Casino Gamma</h2>
        <a href="https://VOTRE_DOMAINE.com/click?sub1=top3_landing&source=organic&position=3"
           class="cta-button">
            Essayer
        </a>
    </div>
</body>
</html>
```

**Note :** Tous les clics iront vers le même `sub1` mais vous pouvez tracker la position avec le paramètre `position`.

---

## 🎨 Intégration avec Bolt

### Dans Bolt, modifiez vos boutons comme ceci :

**Exemple 1 : Bouton Simple**
```html
<Button 
  as="a" 
  href="https://VOTRE_DOMAINE.com/click?sub1=bolt_landing_1"
  target="_self"
>
  Jouer Maintenant
</Button>
```

**Exemple 2 : Link Stylisé**
```html
<Link 
  href="https://VOTRE_DOMAINE.com/click?sub1=bolt_promo_page&source=organic"
  className="cta-primary"
>
  Réclamez 500€ de Bonus
</Link>
```

**Exemple 3 : Bouton avec Tracking Avancé**
```html
<a 
  href="https://VOTRE_DOMAINE.com/click?sub1=bolt_hero_section&source=homepage&campaign=main_cta"
  className="hero-cta"
  data-analytics="main-cta-click"
>
  Commencer à Gagner
</a>
```

---

## 📊 Convention de Nommage sub1

Pour une organisation optimale :

### Format Recommandé : `{source}_{page}_{variant}`

| sub1 | Usage |
|------|-------|
| `fb_lp1_variantA` | Facebook, Landing Page 1, Variante A |
| `google_main_winter` | Google Ads, Page principale, Campagne hiver |
| `email_promo_vip` | Email, Page promo, Segment VIP |
| `organic_homepage` | Trafic organique, Homepage |
| `affiliate_john_ref` | Affilié John, Liens de référence |
| `tiktok_video1` | TikTok, Vidéo #1 |
| `instagram_story2` | Instagram, Story #2 |

---

## 🔗 URLs Complètes - Exemples Réels

### Production
```
https://router.votredomaine.com/click?sub1=fb_landing_1&source=facebook&campaign=winter2024
```

### Développement Local
```
http://localhost:5000/click?sub1=fb_landing_1&source=facebook&campaign=winter2024
```

---

## 🧪 Tester Vos Intégrations

### 1. Test Manuel
Cliquez sur votre bouton → Vous devez être redirigé vers un casino avec `click_id` dans l'URL

### 2. Vérifier les Stats
```bash
curl http://localhost:5000/admin/stats/sub1/fb_landing_1 \
  -u admin:admin123
```

### 3. Simuler un Cycle Complet

**Étape 1 : Click**
```
http://localhost:5000/click?sub1=test_integration
```

**Étape 2 : Copier le click_id de l'URL de redirection**

**Étape 3 : Simuler un FTD**
```bash
curl -X POST http://localhost:5000/postback \
  -H "Content-Type: application/json" \
  -d '{
    "click_id": "VOTRE_CLICK_ID",
    "event": "ftd",
    "payout": 150.00,
    "secret": "dev-shared-secret-token-12345"
  }'
```

**Étape 4 : Vérifier les stats**
```bash
curl http://localhost:5000/admin/stats/sub1/test_integration \
  -u admin:admin123
```

---

## 🚀 Checklist de Déploiement

Avant de mettre en production vos landing pages :

- [ ] Router backend déployé et fonctionnel
- [ ] URL du router configurée (HTTPS obligatoire)
- [ ] Tous les boutons/liens pointent vers le router
- [ ] sub1 unique par landing/source
- [ ] Tests de redirection effectués
- [ ] Stats visibles dans l'admin
- [ ] Postbacks configurés côté casinos
- [ ] Test complet du flow (click → FTD → stats)

---

## ⚡ Performance & Optimisation

### Cache DNS
Vos landing pages Bolt peuvent rester **statiques** et **cachées** (CDN, etc.) car :
- Aucune logique côté landing
- Toute la logique est dans le router backend
- Les landings sont ultra-rapides

### Suivi des Conversions
Chaque `sub1` est optimisé **indépendamment** :
- Landing Facebook peut router vers Casino A
- Landing Google peut router vers Casino B
- Le système apprend automatiquement ce qui fonctionne le mieux pour chaque source

---

## 🎯 Cas d'Usage Avancés

### A/B Testing de Landings
```html
<!-- Landing A -->
<a href="https://router.com/click?sub1=test_landing_a&campaign=ab_test">CTA A</a>

<!-- Landing B -->
<a href="https://router.com/click?sub1=test_landing_b&campaign=ab_test">CTA B</a>
```

Comparez ensuite les stats :
```bash
curl http://localhost:5000/admin/stats/sub1/test_landing_a
curl http://localhost:5000/admin/stats/sub1/test_landing_b
```

### Geo-Targeting (via paramètre custom)
```html
<a href="https://router.com/click?sub1=fr_landing&source=seo&country=FR">Jouer</a>
<a href="https://router.com/click?sub1=uk_landing&source=seo&country=UK">Play</a>
```

---

## 💡 Conseils Pro

1. **Un sub1 = une source de trafic homogène**
   - Ne mélangez pas Facebook et Google sous le même sub1
   - Chaque source a son propre comportement

2. **Gardez vos sub1 lisibles**
   - ✅ `fb_landing_winter`
   - ❌ `x7f9_lp_v2_final_COPY`

3. **Documentez vos sub1**
   - Maintenez un fichier Excel/Notion avec tous vos sub1 et leur usage

4. **Surveillez vos stats régulièrement**
   - Vérifiez que les FTD remontent bien
   - Validez que les poids s'ajustent

---

## 🆘 Problèmes Courants

### "Ma landing ne redirige pas"
→ Vérifiez que l'URL du router est correcte et accessible

### "Pas de stats pour mon sub1"
→ Vérifiez l'orthographe exacte du sub1 (sensible à la casse)

### "Tous mes clicks vont au même casino"
→ Normal au début ! Le système apprend avec les FTD. Attendez quelques conversions.

---

**Besoin d'aide ?** Contactez votre développeur ou consultez la documentation API complète.






