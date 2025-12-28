Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

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
