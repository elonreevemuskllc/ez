# 🎰 SPINGRANNY - Configuration & Restrictions Horaires

## 📊 INFORMATIONS GÉNÉRALES

| Paramètre | Valeur |
|-----------|--------|
| **Nom** | SpinGranny |
| **Commission CPA** | **75 EUR** (le meilleur!) |
| **Plateforme** | Everflow |
| **Offer ID dans le router** | 7 |
| **Status** | ✅ Actif |

---

## 🕐 RESTRICTIONS HORAIRES

**IMPORTANT** : SpinGranny n'accepte les conversions QUE pendant ces plages horaires (fuseau Europe/Paris) :

### ✅ DISPONIBLE

**Weekend (Samedi-Dimanche)** :
- Toute la journée (00h00 → 24h00)

**Semaine (Lundi-Vendredi)** :
- **Soirée** : 19h00 → 00h00
- **Nuit** : 00h00 → 06h00

### ❌ INDISPONIBLE

**Lundi-Vendredi** :
- 06h00 → 19h00 (journée)

---

## 🔧 CONFIGURATION AUTOMATIQUE

Le Casino Router vérifie **AUTOMATIQUEMENT** l'heure actuelle et :
- ✅ Inclut SpinGranny dans la rotation pendant les plages autorisées
- ❌ Exclut SpinGranny en dehors de ces plages
- 🔄 Redirige vers MyStake ou iCE si SpinGranny n'est pas disponible

**Tu n'as RIEN à faire** : le système gère tout automatiquement ! 🎯

---

## 📡 CONFIGURATION POSTBACK (À FAIRE DANS EVERFLOW)

### URL Postback à Configurer

```
https://subrictal-fallon-precomprehensively.ngrok-free.dev/postback?click_id={transaction_id}&event=ftd&payout=75&secret=dev-shared-secret-token-12345
```

### Détails de Configuration

Dans l'interface Everflow de SpinGranny :

1. **Va dans** : Offers > SpinGranny > Postback Settings
2. **Postback URL** : 
   ```
   https://subrictal-fallon-precomprehensively.ngrok-free.dev/postback
   ```
3. **Paramètres** :
   - `click_id` = `{transaction_id}` ← Macro Everflow
   - `event` = `ftd` (texte fixe)
   - `payout` = `75` ← **FIXE (pas de macro !)**
   - `secret` = `dev-shared-secret-token-12345`

4. **Méthode HTTP** : GET ou POST (les deux fonctionnent)
5. **Event Type** : FTD / First Deposit
6. **Sauvegarde** ✅

---

## 🎯 POURQUOI C'EST RENTABLE

### Avantages de SpinGranny

1. **Commission la plus élevée** : 75€ vs 55€ (MyStake) vs 50€ (iCE)
2. **Horaires premium** : Soirées + weekends = meilleurs taux de conversion
3. **Moins de concurrence** : Restrictions horaires = moins d'affiliés

### Calcul d'Impact

Si tu génères **100 FTDs/mois** avec une distribution optimale :

**AVANT** (seulement MyStake + iCE) :
```
50 FTDs × 55€ (MyStake) = 2,750€
50 FTDs × 50€ (iCE)     = 2,500€
─────────────────────────────────
TOTAL                   = 5,250€
```

**APRÈS** (avec SpinGranny sur les horaires premium) :
```
30 FTDs × 75€ (SpinGranny) = 2,250€
40 FTDs × 55€ (MyStake)    = 2,200€
30 FTDs × 50€ (iCE)        = 1,500€
──────────────────────────────────
TOTAL                      = 5,950€
```

**GAIN : +700€/mois (+13%)** 💰

---

## 📊 VÉRIFIER LES STATISTIQUES

### Dashboard
```
https://subrictal-fallon-precomprehensively.ngrok-free.dev/dashboard
```

### API Stats
```bash
Invoke-RestMethod -Uri "https://subrictal-fallon-precomprehensively.ngrok-free.dev/admin/stats" `
  -Headers @{Authorization="Basic YWRtaW46YWRtaW4xMjM="}
```

Tu verras :
- Combien de clicks SpinGranny a reçu
- Combien de FTDs à 75€
- L'EPC de SpinGranny vs les autres

---

## 🧪 TESTER LE SYSTÈME

### 1. Vérifier la disponibilité actuelle

```bash
docker exec casino_router_app python time_restrictions.py
```

### 2. Simuler un click

```bash
Invoke-WebRequest -Uri "https://subrictal-fallon-precomprehensively.ngrok-free.dev/click?sub1=test_spingranny" -MaximumRedirection 0
```

### 3. Simuler un FTD (après avoir cliqué)

```bash
Invoke-RestMethod -Uri "https://subrictal-fallon-precomprehensively.ngrok-free.dev/postback?click_id=VOTRE_CLICK_ID&event=ftd&payout=75&secret=dev-shared-secret-token-12345"
```

---

## 💡 CONSEILS D'OPTIMISATION

### Concentre ton trafic sur les horaires SpinGranny

Si tu peux contrôler QUAND tu postes ton contenu :

- 📱 **TikTok/Instagram** : Poste en fin d'après-midi (17h-18h) pour que les vues arrivent à 19h+
- 🎥 **YouTube Shorts** : Poste le vendredi soir pour maximiser les vues du weekend
- 📧 **Email** : Envoie les campagnes à 18h pour qu'elles soient lues en soirée

**Résultat** : Plus de trafic pendant les plages SpinGranny = Plus de FTDs à 75€ ! 🎯

---

## ⚠️ IMPORTANT À RETENIR

1. **Montant fixe 75€** : NE PAS utiliser de macro variable dans le postback
2. **Restrictions automatiques** : Le router gère tout, tu n'as rien à faire
3. **Everflow utilise `{transaction_id}`** : Pas `[trackingcode]` ou `{clickid}`
4. **URL ngrok permanente** : `subrictal-fallon-precomprehensively.ngrok-free.dev` (payé)

---

## 🎉 RÉSULTAT

Tu as maintenant **3 casinos optimisés** :
- 🥇 SpinGranny : 75€ (horaires premium)
- 🥈 MyStake : 55€ (24/7)
- 🥉 iCE : 50€ (24/7)

Le système choisit **AUTOMATIQUEMENT** le meilleur casino en fonction :
- ✅ De l'heure actuelle
- ✅ Des performances réelles (EPC)
- ✅ De l'exploration/exploitation (80/20)

**TON ROUTEUR EST AU TOP ! 🚀💰**

