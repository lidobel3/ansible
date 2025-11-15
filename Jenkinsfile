pipeline {
    agent any

    parameters {

        // Mot de passe Ansible Vault (masqué)
        password(
            name: 'VAULT_PASSWORD',
            defaultValue: '',
            description: 'Mot de passe Ansible Vault'
        )

        // Playbook à lancer
        string(
            name: 'PLAYBOOK',
            defaultValue: 'playbooks/playbook.yml',
            description: 'Playbook Ansible à exécuter'
        )

        // Inventory
        string(
            name: 'INVENTORY',
            defaultValue: 'inventaires/dev/hosts.ini',
            description: 'Fichier d’inventaire Ansible'
        )

        // Limit (optionnel, groupe ou host)
        string(
            name: 'LIMIT',
            defaultValue: 'docker',
            description: 'Cible : groupe/host (ex: webservers). Laisser vide si non utilisé.'
        )

        // Tags (optionnel)
        string(
            name: 'TAGS',
            defaultValue: '',
            description: 'Tags Ansible (ex: app,deploy). Laisser vide si non utilisé.'
        )

        // Extra vars (optionnelles)
        text(
            name: 'EXTRA_VARS',
            defaultValue: '',
            description: 'Variables supplémentaires (JSON ou KEY=VALUE). Exemple: {"env":"prod"}'
        )
    }

    stages {

        stage('Run Ansible') {
            steps {

                sh """
                    # On crée le fichier vault temporaire
                    echo "${params.VAULT_PASSWORD}" > vault_pass.txt

                    # Construction dynamique de la commande
                    CMD="ansible-playbook ${params.PLAYBOOK} -i ${params.INVENTORY} --vault-password-file vault_pass.txt"

                    # Add limit if provided
                    if [ ! -z "${params.LIMIT}" ]; then
                        CMD="$CMD --limit ${params.LIMIT}"
                    fi

                    # Add tags if provided
                    if [ ! -z "${params.TAGS}" ]; then
                        CMD="$CMD --tags ${params.TAGS}"
                    fi

                    # Add extra vars if provided
                    if [ ! -z "${params.EXTRA_VARS}" ]; then
                        CMD="$CMD --extra-vars '${params.EXTRA_VARS}'"
                    fi

                    echo "Commande exécutée :"
                    echo "\$CMD"

                    # Run ansible
                    eval \$CMD

                    # Nettoyage
                    rm -f vault_pass.txt
                """
            }
        }
    }
}