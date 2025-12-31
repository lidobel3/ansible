# prometheus.yml
global:
  scrape_interval: 15s      # MTTD ≈ 15-30s
  evaluation_interval: 15s  # Temps d'évaluation des règles
```

| Scrape Interval | MTTD moyen |
|-----------------|------------|
| 15s | **15-30s** |
| 30s | 30-60s |
| 1m | 1-2 min |

**Objectif recommandé : MTTD < 1 minute**

---

### **2. MTTA (Mean Time To Acknowledge)**

Avec auto-remédiation = **quasi instantané** (1-5 secondes)

**Décomposition :**
- Alertmanager reçoit l'alerte : 1-2s
- Webhook envoyé : 0.5-2s
- Endpoint Python reçoit : 0.5-1s

**Objectif : MTTA < 10 secondes**

---

### **3. MTTR (Mean Time To Repair)**

**Dépend du type d'action :**

| Action | Temps d'exécution | MTTR total |
|--------|-------------------|------------|
| **Restart container Docker** | 5-15s | **~1-2 min** |
| **Restart service systemd** | 3-10s | **~1 min** |
| **Scale K8s deployment** | 10-30s | **~1-2 min** |
| **Cleanup logs** | 5-20s | **~1 min** |
| **Restart VM** | 30-120s | **~3-5 min** |
| **Rollback deployment** | 30-60s | **~2-3 min** |

**Objectif général : MTTR < 5 minutes**

---

### **4. RTO (Recovery Time Objective)**

**Formule :**
```
RTO = MTTD + MTTA + MTTR + buffer
```

**Exemple concret - Service down :**
```
MTTD  : 30s  (détection)
MTTA  : 5s   (webhook déclenché)
MTTR  : 15s  (restart container)
Buffer: 10s  (marge de sécurité)
────────────────────────────
RTO   : 60s = 1 minute
```

**Objectifs par type d'incident :**

| Incident | RTO cible |
|----------|-----------|
| Service crash | **2-3 minutes** |
| Disque plein | **3-5 minutes** |
| High CPU/Memory | **2-4 minutes** |
| Database connection failed | **3-5 minutes** |
| Pod crash loop | **1-2 minutes** |

---

### **5. RPO (Recovery Point Objective)**

**Avec auto-remédiation, le RPO dépend de tes backups, pas de la remédiation !**

| Stratégie de backup | RPO |
|---------------------|-----|
| Réplication synchrone | **0 seconde** (aucune perte) |
| Backup continu (WAL) | **< 1 minute** |
| Snapshot toutes les 15 min | **15 minutes** |
| Backup quotidien | **24 heures** |

**L'auto-remédiation ne protège PAS contre la perte de données !**
Elle **réduit l'indisponibilité** mais ne remplace pas les backups.

---

## **📈 Tableau récapitulatif des objectifs**

| Métrique | Sans auto-remédiation | Avec auto-remédiation | Amélioration |
|----------|----------------------|----------------------|--------------|
| **MTTD** | 2-5 min | 15-60s | **70-80%** |
| **MTTA** | 5-30 min (humain) | 5-10s | **99%** |
| **MTTR** | 10-30 min | 1-5 min | **80-90%** |
| **RTO** | 20-60 min | 2-5 min | **90-95%** |
| **Disponibilité** | 99.9% (8h downtime/an) | 99.95%+ (4h/an) | **50%** |

---

## **🎯 SLA réalistes avec auto-remédiation**

### **Tier 1 - Services critiques**
```
RTO  : 2 minutes
RPO  : 0 (réplication sync)
MTTR : 1 minute
Disponibilité : 99.95% (4.4h downtime/an)
```

### **Tier 2 - Services importants**
```
RTO  : 5 minutes
RPO  : 5 minutes
MTTR : 3 minutes
Disponibilité : 99.9% (8.8h downtime/an)
```

### **Tier 3 - Services standard**
```
RTO  : 15 minutes
RPO  : 15 minutes
MTTR : 10 minutes
Disponibilité : 99.5% (1.8j downtime/an)
```

---

## **⚠️ Limites de l'auto-remédiation**

### **Ce que ça améliore :**
- ✅ Incidents simples et répétitifs (crash, OOM, disk full)
- ✅ Problèmes avec solution connue
- ✅ Réduction massive du RTO

### **Ce que ça n'améliore PAS :**
- ❌ Bugs applicatifs complexes
- ❌ Corruptions de données
- ❌ Failles de sécurité
- ❌ Problèmes réseau majeurs
- ❌ Incidents nécessitant une analyse humaine

**Taux de résolution automatique réaliste : 60-80% des incidents**

---

## **📊 Exemple de calcul de disponibilité**

**Sans auto-remédiation :**
```
10 incidents/mois × 20 min/incident = 200 min downtime/mois
200 min ÷ 43800 min (1 mois) = 0.46% indisponibilité
Disponibilité = 99.54%
```

**Avec auto-remédiation (80% auto-résolus) :**
```
8 incidents auto-résolus × 2 min = 16 min
2 incidents manuels × 20 min = 40 min
Total = 56 min downtime/mois
56 min ÷ 43800 min = 0.13% indisponibilité
Disponibilité = 99.87%
```

**Gain : +0.33% de disponibilité = 144 min/mois économisées !**

---

## **🚀 Pour aller plus loin**

### **Améliorer encore les métriques :**

1. **Réduire MTTD :**
   - Diminuer scrape_interval à 10s
   - Utiliser des health checks actifs
   - Monitoring synthétique

2. **Réduire MTTR :**
   - Pré-chauffer des instances de secours (warm standby)
   - Utiliser des circuit breakers
   - Implémenter du chaos engineering pour tester

3. **Réduire RPO :**
   - Réplication synchrone multi-region
   - Backup continu (WAL streaming)
   - CQRS/Event Sourcing

---

## **📋 Dashboard recommandé**

**Métriques à suivre dans Grafana :**
```
- Nombre d'incidents/jour
- Taux de résolution automatique (%)
- MTTD moyen
- MTTR moyen
- RTO réel vs cible
- Disponibilité (%)
- Faux positifs (alertes inutiles)
- Échecs d'auto-remédiation