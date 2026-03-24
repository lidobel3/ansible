# Déploiement du site Portfolio

## Informations générales
- La branche `portfolio` contient l'ensemble du code pour déployer le site [https://lidobel.ovh](https://lidobel.ovh).
- L'inventaire Ansible contient trois environnements : `dev`, `staging` et `prod`.
- La branche `dev` est la seule à contenir un inventaire complet :

/Users/lidobel3/ansible/ansible/inventories/dev/hosts.ini

- Le déploiement se fait sur une VM de test (VirtualBox) via Vagrant.

## Commandes utiles
- Vérifier l'URL du dépôt Git :
```bash
git remote get-url origin

Détails du déploiement
	•	VM cible : node_5
	•	Chemin de déploiement sur MacBookPro : /var/root/node_5
	•	Environnement de test accessible à l’adresse : https://192.168.1.101￼
	•	Pipeline de déploiement : http://192.168.1.17:8081￼

```

Configuration Vagrant

```bash
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.hostname = "worker5"
  config.vm.network "public_network", ip: "192.168.1.101", bridge: "en0: Wi-Fi (AirPort)"
  config.vm.provision "docker"

  config.vm.provider "virtualbox" do |v|
    v.name = "node_5"
  end
end
```
