# ansible

### Updates :
<details>
<summary> 25/12/25 </summary>

- [X] MàJ de python 3 à python 3.8
  - [x] Installation de python3.8 & python3.8-distutils via ansible
  - [x] Modification du hosts.ini
  - [ ] Industrialisation des mise à jour pyhton sur les noeuds à admnistrer 


</details>

‼️ Le module docker était en erreur car il lui manquait des librairies.

## La branche Intest 

La branche intest sert à tester les nouvelles màj du playbook avant de les pousser sur la main (production)

```hosts.ini
[frontend]
node6 ansible_host=192.168.1.132 ansible_user=vagrant ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_python_interpreter=/usr/bin/python3

[middle]
worker5 ansible_host=192.168.1.101 ansible_user=vagrant ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_python_interpreter=/usr/bin/python3.8
worker7 ansible_host=192.168.1.150 ansible_user=vagrant ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_python_interpreter=/usr/bin/python3.8

[docker]
worker5
worker7 

[bdd]
bdd1 ansible_host=192.168.1.105 ansible_user=vagrant ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_python_interpreter=/usr/bin/python3.8

[all:children]
frontend
middle
bdd
```
> Le nouvelle host worker7 a été ajouté, pour tester l'automatisation de l'acceptation 

```shell
The authenticity of host 'server.example.com (192.168.1.150)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no)?
```

📌 À quoi correspond cette confirmation ?

* Cette demande correspond à la vérification de la clé d’hôte SSH (Host Key).
* Chaque serveur SSH possède une clé cryptographique unique (ED25519, RSA, ECDSA…).
* Lors de la première connexion, le client SSH ne connaît pas encore cette clé.
* Il demande donc à l’utilisateur de confirmer que le serveur contacté est bien le bon.

```shell
ssh-keyscan -H 192.168.1.150 >> ~/.ssh/known_hosts
```
> **Note :** ⚠️ Voici la seule alternative `ssh-keyscan` pour éviter la demande de validation, commande à executer dans le node controller ou automatiser via une task.

