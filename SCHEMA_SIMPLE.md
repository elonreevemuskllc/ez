# 📊 SCHÉMA CASINO ROUTER - SIMPLE & EFFICACE

## 🎯 OBJECTIF
Envoyer automatiquement ton trafic vers le casino qui paie le MIEUX, basé sur les performances réelles.

---

## 🔄 FLUX COMPLET

```
┌─────────────────────────────────────────────────────────────────┐
│                    CASINO ROUTER - FLUX COMPLET                  │
└─────────────────────────────────────────────────────────────────┘

1️⃣ TRAFIC ARRIVE (TikTok, YouTube, Instagram...)
   │
   │ Clique sur: https://ton-domaine.ngrok/click?sub1=tiktok_video1
   │
   ▼
┌──────────────────────────┐
│   CASINO ROUTER          │  ← Hébergé sur Docker (localhost:5000)
│   (Ton Serveur)          │  ← Exposé via ngrok au monde extier
└──────────────────────────┘
   │
   │ ✓ Génère un click_id unique
   │ ✓ Enregistre: sub1=tiktok_video1, timestamp
   │ ✓ Calcule l'EPC de chaque casino:
   │    • Mystake: FTDs × 55€ ÷ total clicks
   │    • iCE: FTDs × 50€ ÷ total clicks
   │ ✓ Choisit le MEILLEUR casino (EPC le plus élevé)
   │
   ▼
2️⃣ REDIRECTION VERS LE CASINO GAGNANT
   │
   ├─> Si Mystake gagne: https://mystake.com/signup?aff=xxx&clickid=abc123
   │
   └─> Si iCE gagne: https://direct.midas-affiliate.com/click?pid=656&offer_id=1616&sub1=abc123

3️⃣ JOUEUR S'INSCRIT & DÉPOSE
   │
   │ Le joueur joue sur le casino
   │
   ▼
┌──────────────────────────┐
│   CASINO AFFILIATE       │
│   (Mystake ou iCE)       │
└──────────────────────────┘
   │
   │ Détecte un FTD (First Time Deposit)
   │
   ▼
4️⃣ POSTBACK (CASINO → TON ROUTER)
   │
   │ Casino envoie:
   │ https://ton-domaine.ngrok/postback?click_id=abc123&event=ftd&payout=55&secret=xxx
   │
   ▼
┌──────────────────────────┐
│   CASINO ROUTER          │
│   Reçoit le FTD          │
└──────────────────────────┘
   │
   │ ✓ Vérifie le secret
   │ ✓ Retrouve le click original (sub1=tiktok_video1)
   │ ✓ Enregistre: FTD + 55€ (Mystake) ou 50€ (iCE)
   │ ✓ Recalcule l'EPC de chaque casino
   │ ✓ Ajuste le routing automatiquement
   │
   ▼
5️⃣ OPTIMISATION CONTINUE
   │
   │ Le routeur apprend:
   │ • Quel casino convertit le mieux
   │ • Quelle source (sub1) performe le mieux
   │ • Envoie + de traffic au casino gagnant
   │
   ▼
💰 TU GAGNES PLUS D'ARGENT !
```

---

## 💡 FORMULE EPC (Earnings Per Click)

```
EPC = (Nombre de FTDs × Commission CPA) ÷ Nombre total de clicks

Exemple:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Casino     | Clicks | FTDs | CPA   | EPC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mystake    | 100    | 3    | 55€   | (3×55)÷100 = 1.65€
iCE        | 100    | 4    | 50€   | (4×50)÷100 = 2.00€
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

➡️ Le routeur enverra 80% du trafic vers iCE (meilleur EPC)
```

---

## 🎯 COMMISSIONS CPA FIXES

**IMPORTANT:** Les casinos paient des commissions FIXES par FTD (pas le montant du dépôt)

| Casino  | Commission CPA |
|---------|----------------|
| Mystake | **55 EUR**     |
| iCE     | **50 EUR**     |

---

## 📍 TRACKING PAR SOURCE (sub1)

Le paramètre `sub1` te permet de tracker QUELLE source performe le mieux:

```
https://ton-domaine.ngrok/click?sub1=tiktok_video1
https://ton-domaine.ngrok/click?sub1=tiktok_video2
https://ton-domaine.ngrok/click?sub1=youtube_short1
https://ton-domaine.ngrok/click?sub1=instagram_reel1
```

Le dashboard te montre ensuite:
- Quelle vidéo TikTok a le meilleur EPC
- Quel réseau social convertit le mieux
- Où concentrer tes efforts

---

## 🔑 POSTBACKS À CONFIGURER

### Mystake
```
URL: https://ton-domaine.ngrok/postback
Méthode: GET ou POST
Paramètres:
  - click_id=[trackingcode]
  - event=ftd
  - payout=55          ← FIXE à 55€
  - secret=dev-shared-secret-token-12345
```

### iCE Affiliate
```
URL: https://ton-domaine.ngrok/postback
Méthode: GET ou POST
Paramètres:
  - click_id={clickid}
  - event=ftd
  - payout=50          ← FIXE à 50€
  - secret=dev-shared-secret-token-12345
```

---

## 📊 DASHBOARD

Accède à ton dashboard: `https://ton-domaine.ngrok/dashboard`

Tu y verras:
- ✅ Clicks par casino
- ✅ FTDs par casino
- ✅ EPC par casino (en temps réel)
- ✅ Performance par source (sub1)
- ✅ Graphiques d'évolution

---

## 🚀 RÉSUMÉ EN 3 POINTS

1. **Le trafic clique sur ton lien** → Le routeur choisit le meilleur casino
2. **Le joueur dépose** → Le casino envoie un postback avec 55€ ou 50€
3. **Le routeur apprend** → Il envoie plus de trafic vers le casino qui convertit mieux

**C'EST AUTOMATIQUE. C'EST INTELLIGENT. C'EST PROFITABLE.** 💰

