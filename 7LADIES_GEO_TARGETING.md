# 🌍 7LADIES - Géo-Ciblage Automatique

## 📊 INFORMATIONS GÉNÉRALES

| Paramètre | Valeur |
|-----------|--------|
| **Nom** | 7ladies |
| **Commission CPA** | **70 EUR** |
| **Plateforme** | Cellxpert (identique à MyStake) |
| **Offer ID dans le router** | 8 |
| **Status** | ✅ Actif |

---

## 🌍 GÉO-CIBLAGE AUTOMATIQUE

**IMPORTANT** : 7ladies n'est disponible QUE pour ces 5 pays :

### ✅ PAYS CIBLÉS

| Code | Pays | Devise |
|------|------|--------|
| **BE** | 🇧🇪 Belgique | EUR |
| **CH** | 🇨🇭 Suisse | CHF |
| **IT** | 🇮🇹 Italie | EUR |
| **DE** | 🇩🇪 Allemagne | EUR |
| **CA** | 🇨🇦 Canada | CAD |

### ❌ AUTRES PAYS

Tous les autres pays (FR, US, UK, etc.) seront automatiquement redirigés vers les autres casinos.

---

## 🔧 FONCTIONNEMENT AUTOMATIQUE

Le Casino Router détecte **AUTOMATIQUEMENT** le pays du visiteur grâce à :

1. **ipapi.co** : API de géolocalisation par IP
2. **Détection temps réel** : Chaque click vérifie le pays
3. **Fallback intelligent** : Si le pays ne correspond pas, utilise les autres casinos

### Exemple de Flux

```
┌─────────────────────────────────────────────────────────────┐
│  VISITEUR CLIQUE SUR TON LIEN                                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUTER : Détecte l'IP → 185.xxx.xxx.xxx                    │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  IPAPI.CO : IP → Pays = CH (Suisse) 🇨🇭                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUTER : CH est dans [BE,CH,IT,DE,CA] ?                    │
│           ✅ OUI → 7ladies est DISPONIBLE                     │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  CALCUL EPC : Compare 7ladies vs autres casinos             │
│               7ladies: 70€                                   │
│               SpinGranny: 75€ (mais horaire restreint)       │
│               MyStake: 55€                                   │
│               iCE: 50€                                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  REDIRECTION → 7ladies (ou meilleur EPC disponible)         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📡 CONFIGURATION POSTBACK (À FAIRE DANS CELLXPERT)

### URL Postback à Configurer

Cellxpert utilise les mêmes macros que MyStake :

```
https://subrictal-fallon-precomprehensively.ngrok-free.dev/postback?click_id=[trackingcode]&event=ftd&payout=70&secret=dev-shared-secret-token-12345
```

### Détails de Configuration

Dans l'interface Cellxpert de 7ladies :

1. **Va dans** : Offers > 7ladies > Postback Settings
2. **Postback URL** : 
   ```
   https://subrictal-fallon-precomprehensively.ngrok-free.dev/postback
   ```
3. **Paramètres** :
   - `click_id` = `[trackingcode]` ← Macro Cellxpert
   - `event` = `ftd` (texte fixe)
   - `payout` = `70` ← **FIXE (pas de macro !)**
   - `secret` = `dev-shared-secret-token-12345`

4. **Méthode HTTP** : GET ou POST (les deux fonctionnent)
5. **Event Type** : FTD / First Deposit
6. **Sauvegarde** ✅

---

## 💰 STRATÉGIE DE REVENUS

### Pourquoi 7ladies est Rentable

1. **Pays riches** : BE/CH/DE/CA ont des dépôts moyens élevés
2. **Concurrence limitée** : Moins d'affiliés ciblent ces pays spécifiquement
3. **CPA attractif** : 70€ est excellent pour ces marchés

### Comparaison de Revenus

**Scénario : 100 FTDs d'utilisateurs suisses** 🇨🇭

**AVANT** (sans 7ladies) :
```
100 FTDs × 55€ (MyStake)  = 5,500€
```

**APRÈS** (avec 7ladies) :
```
100 FTDs × 70€ (7ladies)  = 7,000€
```

**GAIN : +1,500€ (+27%) !** 💰

---

## 🎯 TES 4 CASINOS OPTIMISÉS

| Casino | CPA | Disponibilité | Géo-Ciblage |
|--------|-----|---------------|-------------|
| **SpinGranny** | **75 EUR** 🥇 | Weekend + Soirées | Mondial 🌍 |
| **7ladies** | **70 EUR** 🥈 | 24/7 | **BE/CH/IT/DE/CA** 🎯 |
| **MyStake** | 55 EUR 🥉 | 24/7 | Mondial 🌍 |
| **iCE** | 50 EUR | 24/7 | Mondial 🌍 |

---

## 🧪 TESTER LE GÉO-CIBLAGE

### Test 1 : Vérifier le pays d'une IP

```bash
docker exec casino_router_app python -c "from geo_restrictions import get_country_from_ip; print(get_country_from_ip('8.8.8.8'))"
```

### Test 2 : Simuler un click depuis la Suisse

Utilise un VPN ou proxy suisse, puis :

```
https://subrictal-fallon-precomprehensively.ngrok-free.dev/click?sub1=test_swiss
```

Le router devrait rediriger vers **7ladies** si c'est le meilleur EPC.

### Test 3 : Vérifier les logs

```bash
docker-compose logs --tail=20 app | grep "Geo-filtering"
```

Tu verras :
```
Geo-filtering: 4 offers → 4 available for country CH
Geo-filtering: 4 offers → 3 available for country FR  (7ladies exclue)
```

---

## 📊 MONITORING

### Dashboard
```
https://subrictal-fallon-precomprehensively.ngrok-free.dev/dashboard
```

Tu verras :
- Combien de clicks 7ladies a reçu
- Combien de FTDs à 70€
- L'EPC de 7ladies vs les autres
- **Répartition géographique** (bientôt disponible)

### API Stats
```powershell
Invoke-RestMethod -Uri "https://subrictal-fallon-precomprehensively.ngrok-free.dev/admin/stats" `
  -Headers @{Authorization="Basic YWRtaW46YWRtaW4xMjM="}
```

---

## 💡 CONSEILS D'OPTIMISATION

### Cible spécifiquement ces pays

Si tu peux contrôler ta publicité :

1. **TikTok/Instagram** : Cible BE/CH/DE/CA dans tes campagnes
2. **YouTube** : Active les sous-titres en allemand, français (CH/BE), italien
3. **Landing Pages** : Crée des versions traduites pour ces pays

### Utilise des sub1 spécifiques

```
?sub1=tiktok_swiss
?sub1=youtube_germany
?sub1=instagram_belgium
```

Cela te permet de voir **quel pays performe le mieux** dans le dashboard.

---

## ⚠️ POINTS IMPORTANTS

1. **ipapi.co** : Limite gratuite de 30K lookups/mois
   - Tu as une clé API : `M3ZmorMRHUNe7BNL3Feg2Y4DJ4k5RMYZvyi5m7kf0ul7MlJPDq`
   - Surveille ton usage sur [ipapi.co/account](https://ipapi.co/)

2. **Fallback automatique** : Si ipapi.co ne répond pas, le système exclut les offres géo-restreintes

3. **IPs locales** : Les IPs 127.0.0.1, 192.168.x.x sont ignorées (tests locaux)

4. **Timeout** : La requête ipapi.co a un timeout de 2 secondes pour ne pas ralentir l'expérience utilisateur

---

## 🎉 RÉSULTAT

Tu as maintenant un système **ultra-intelligent** :

✅ **Géo-ciblage automatique** pour maximiser les revenus par pays  
✅ **Restrictions horaires** pour SpinGranny (weekend + soirées)  
✅ **Optimisation EPC** automatique basée sur les performances réelles  
✅ **4 casinos** avec des CPA de 50€ à 75€  

**TON ROUTEUR EST AU NIVEAU PROFESSIONNEL ! 🚀💰**

