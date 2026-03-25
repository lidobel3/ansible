# Ansible Repository

Ceci est un **repo public** pour présenter mes travaux avec **Ansible**.

Ansible est un outil puissant d'automatisation développé en Python.  
Il est **agentless** et utilise des fichiers de configuration écrits en **YAML** pour décrire les tâches et les rôles.

---

## 📂 Branches du repository

Ce repo contient actuellement **7 branches**, chacune ayant un objectif spécifique :

### 1. `main`
- Branche principale, stable et à jour.
- Contient les configurations et playbooks validés et prêts pour usage réel.
- Destinée à servir de base pour toutes les autres branches.

### 2. `portfolio`
- Contient des exemples et projets personnels pour démontrer mes compétences Ansible.
- Inclut des playbooks simples et des templates pour le déploiement de petites applications ou environnements de test.
- Utilisé comme support de présentation et portfolio technique.

### 3. `intest`
- Branche dédiée aux **tests d’intégration**.
- Contient des playbooks expérimentaux ou des modifications en cours de validation.
- Idéal pour tester de nouvelles fonctionnalités ou rôles avant de les fusionner dans `main`.

⚠️ La branche de production du site https://lidobel.ovh est la branche intest inventaire int 
Evolution à venir : Création d'un repo portfolio 

### 4. `gpl`
- Branche dédiée au projet **GPL de monitoring**.
- Déploie la **stack complète de monitoring** :
  - **Prometheus** → collecte des métriques
  - **Grafana** → visualisation et tableaux de bord
  - **Loki** → centralisation des logs
  - **Alertmanager** → gestion des alertes
- Contient des playbooks et rôles pour installer, configurer et orchestrer cette stack sur des environnements Linux.
- Permet de déployer un monitoring complet en mode autonome ou intégré dans un cluster.

### 5. `test`
- Branche pour essais rapides et expérimentations.
- Playbooks non stables ou prototypes.
- Les modifications ici peuvent être supprimées ou réécrites fréquemment.

### 6. `master`
- Ancienne branche principale ou historique.
- Conservée pour référence ou compatibilité avec certains outils.
- Ne contient pas forcément les derniers changements.

### 7. `action`
- Branche dédiée au **déploiement automatisé du site internet lidobel.ovh**.
- Utilise un **pipeline GitHub Actions** pour automatiser le déploiement.
- S’exécute sur un **runner self-hosted** situé aux États-Unis chez AWS.
- Contient des playbooks et scripts pour orchestrer l’infrastructure et les services critiques via CI/CD.

---

## ⚡ Fonctionnalités principales d’Ansible dans ce repo
- Déploiement automatique de configurations sur serveurs Linux.
- Gestion des rôles, tâches et variables via YAML.
- Exécution sans agent sur les hôtes cibles.
- Intégration possible avec CI/CD pour déploiement automatisé.

---

## 📖 Comment utiliser ce repo
1. Cloner le repo :

```bash
git clone <URL_DU_REPO>