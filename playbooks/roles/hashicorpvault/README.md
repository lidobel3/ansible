            HASHICORP VAULT 1.15.5

Documentation de prise en main de hashicorp vault pour la gestion externalisée des secrets.  

Script n°1 : Script d'installation de hashicorp vault 1.21.1

```shell
#!/bin/bash
set -euo pipefail

VAULT_VERSION="1.21.1"
VAULT_ZIP="vault_${VAULT_VERSION}_linux_amd64.zip"
VAULT_URL="https://releases.hashicorp.com/vault/${VAULT_VERSION}/${VAULT_ZIP}"
VAULT_BIN="/usr/local/bin/vault"
TMP_DIR="/tmp/vault-install"

echo "Installation Vault ${VAULT_VERSION} via ZIP..."

# Vérif architecture
[[ $(uname -m) == "x86_64" ]] || { echo "Erreur: x86_64 requis"; exit 1; }

# Dépendances
command -v wget >/dev/null || sudo apt update && sudo apt install -y wget unzip
command -v unzip >/dev/null || sudo apt install -y unzip

# Répertoire temp
mkdir -p "$TMP_DIR"
cd "$TMP_DIR"

# Téléchargement (si absent ou corrompu)
if [[ ! -f "$VAULT_ZIP" ]]; then
    echo "Téléchargement..."
    wget -q "$VAULT_URL"
else
    echo "ZIP existant, skip téléchargement"
fi

# Installation
unzip -o "$VAULT_ZIP"  # -o overwrite si existant
sudo mv vault "$VAULT_BIN"
sudo chmod +x "$VAULT_BIN"

# Nettoyage
cd /
rm -rf "$TMP_DIR"

# Vérif
if vault version | grep -q "Vault v${VAULT_VERSION}"; then
    echo "✅ Vault ${VAULT_VERSION} installé !"
    vault version
else
    echo "❌ Échec vérification"
    exit 1
fi

echo "Test: vault server -dev"


vault login -method=userpass \
  username="vagrant" \
  password="vagrant"
  
vault kv get -mount="ansible" "database/postgres"
```

```shell
vault kv get -token="****" -address="http://192.168.1.150" -mount="ansible" "database/postgres"

vault kv get -token="{{ vault_root_token }}" -address="{{ vault_addr }}" -mount="ansible" "database/postgres"
```

#### Tester si on à un token actif :
```shell
vault token lookup -address=http://192.168.1.150:8200
```
> Afficher son token 
vault print token -address=http://192.168.1.150:8200

Lorsque la CLI utilise un "Helper".
Dans le monde de Vault, un Token Helper est un petit utilitaire (un script ou un programme) qui sert de "mémoire" à la ligne de commande (CLI).

C’est le mécanisme qui permet à Vault de dire : "Ok, tu t'es connecté une fois, je vais me souvenir de toi pour que tu n'aies pas à retaper ton token à chaque commande."  

<details>
<summary>1. Comment ça fonctionne ?</summary>

Par défaut, Vault utilise le helper "internal".

    Quand tu fais vault login, le helper prend le token et le stocke (généralement dans ~/.vault-token).

    À chaque fois que tu tapes une commande (vault kv get, etc.), la CLI appelle le helper en cachette pour lui dire : "Hé, donne-moi le token de cet utilisateur pour que je l'envoie au serveur."
ℹ
Les tokens sont généralement rechercher dans le ~/.vault-token ou dans la variable d'environnement $VAULT_TOKEN.

> Lorsque vault est installé en mode snap ça diffère un peu. Comme Snap est un système de paquets "confinés" (sandboxed), le binaire Vault n'a pas le droit d'écrire directement à la racine de ton répertoire personnel (~/). Il est restreint à son propre petit espace isolé dans ~/snap/vault/current/.

```shell
ln -s ~/snap/vault/current/.vault-token ~/.vault-token
```
> ### 🛡️ Particularité Snap
> **Confinement (Sandboxing) :** Le binaire Vault installé par Snap n'a pas le droit d'écrire à la racine de `~/`.
> 
> 📍 **Chemin réel du token :** > `~/snap/vault/current/.vault-token`
>
> *Pensez à créer un lien symbolique ou à exporter la variable `VAULT_TOKEN` pour vos scripts Ansible.*

</details>

<details>
<summary>
</summary>
</details>
<!-- 
Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.
```yaml
#tasks file for vault
#tasks/main.yml


- name: Créer service systemd Vault
 become: true
 copy:
   dest: /etc/systemd/system/vault.service
   content: |
     [Unit]
     Description=HashiCorp Vault
     After=network.target

     [Service]
     ExecStart=/usr/bin/vault server -config={{ vault_config_path }}
     Restart=on-failure
     LimitNOFILE=65536

     [Install]
     WantedBy=multi-user.target
 notify: reload systemd



- name: Démarrer Vault
 become: true
 command: "nohup vault server -config={{ vault_config_path }} > /var/log/vault.log 2>&1 &"
 async: 10
 poll: 0
  creates: /var/run/vault.pid  # Créez ce fichier dans vault server

- name: Démarrer et activer Vault
 become: true
 systemd:
   name: vault
   state: started
   enabled: true
   daemon_reload: true

- name: Attendre que Vault démarre
 become: true
 wait_for:
   host: "{{ vault_listener_address }}"
   port: 8200
   delay: 10
   timeout: 60
   state: started

- name: Initialiser Vault
  become: true
  command: "vault operator init"
  environment:
    VAULT_ADDR: "http://192.168.1.150:8200"
  register: vault_init_output
  when: ansible_facts['distribution'] == "Ubuntu"
  #ignore_errors: true

- name: Déverrouiller Vault (unseal)
  become: true
  command: "vault operator unseal {{ item }}"
  loop: "{{ vault_init_output.stdout_lines[0:3] }}"

- name: Se connecter à Vault avec le token root
  become: true
  command: "vault login {{ vault_init_output.stdout_lines[3] }}"
```

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).

# MES CMD HASHICORP VAULT 

```shell

```


### Authentification et connexion
```bash
vault login                    # Se connecter à Vault
vault login -method=userpass   # Se connecter avec username/password
vault token lookup             # Voir les infos de votre token actuel
```

### Gestion des secrets (KV v2)
```bash
vault kv put secret/myapp password=secret123    # Créer/mettre à jour un secret
vault kv get secret/myapp                       # Lire un secret
vault kv get -field=password secret/myapp       # Lire un champ spécifique
vault kv list secret/                           # Lister les secrets
vault kv delete secret/myapp                    # Supprimer (soft delete)
vault kv metadata get secret/myapp              # Voir les métadonnées et versions
vault kv undelete -versions=2 secret/myapp      # Restaurer une version supprimée
```

### Politique et permissions
```bash
vault policy list              # Lister les politiques
vault policy read my-policy    # Lire une politique
vault policy write my-policy policy.hcl  # Créer/mettre à jour une politique
```

### Secrets engines
```bash
vault secrets list             # Lister les moteurs de secrets actifs
vault secrets enable -path=aws aws  # Activer un nouveau moteur
vault secrets disable aws      # Désactiver un moteur
```
### Statut et configuration
```bash
vault status                   # Voir le statut du serveur
vault operator init            # Initialiser Vault (première fois)
vault operator unseal          # Desceller Vault
vault operator seal            # Sceller Vault
```
### Audit
```bash
vault audit list               # Lister les logs d'audit
vault audit enable file file_path=/var/log/vault_audit.log
```

