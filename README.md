# ansible
##

### Informations 

La branche portfolio contient l'ensemble du code permettant de déployer le site portfolio <https://lidobel.ovh>

L'inventaire contient trois environnements dev, prod et staging

La branche dev est la seule contenant un inventaire : /Users/lidobel3/ansible/ansible/inventories/dev/hosts.ini

Le déploiement se fait en environnement de test sur une VM (vbox) déployé via avec vagrant.

Commande utile :

```bash
git remote get-url origin
```

Le déploiement s'effectue sur la vm node_5 dans /var/root/node_5 sur MacBookPro 11.7.10

```ruby
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

L'adresse du site en environnement de test : https://192.168.1.101

Le pipeline de déploiement : http://192.168.1.17:8081