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
                script {

                    // Générer un fichier temporaire sécurisé pour vault_pass.txt
                    sh """
                        umask 077
                        echo "${params.VAULT_PASSWORD}" > vault_pass.txt
                    """

                    // Construction dynamique de la commande
                    def cmd = "ansible-playbook ${params.PLAYBOOK} -i ${params.INVENTORY} --vault-password-file vault_pass.txt"

                    if (params.LIMIT?.trim()) {
                        cmd += " --limit '${params.LIMIT}'"
                    }

                    if (params.TAGS?.trim()) {
                        cmd += " --tags '${params.TAGS}'"
                    }

                    if (params.EXTRA_VARS?.trim()) {
                        cmd += " --extra-vars '${params.EXTRA_VARS}'"
                    }

                    echo "Commande exécutée (sanitisée) :"
                    echo cmd.replace("--vault-password-file vault_pass.txt", "--vault-password-file *****")

                    sh """#!/bin/bash
                        set -e
                        ${cmd}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Nettoyage du fichier vault..."
            sh "rm -f vault_pass.txt || true"
        }
    }
}
