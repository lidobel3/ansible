pipeline {
    agent any

    options {
        ansiColor('xterm')   // <<< Ajout AnsiColor
    }

    parameters {

        password(
            name: 'VAULT_PASSWORD',
            defaultValue: '',
            description: 'Mot de passe Ansible Vault'
        )

        string(
            name: 'PLAYBOOK',
            defaultValue: 'playbooks/playbook.yaml',
            description: 'Playbook Ansible à exécuter'
        )

        string(
            name: 'INVENTORY',
            defaultValue: 'inventaires/dev/hosts.ini',
            description: 'Fichier d’inventaire Ansible'
        )

        string(
            name: 'LIMIT',
            defaultValue: 'docker',
            description: 'Cible : groupe/host (ex: webservers). Laisser vide si non utilisé.'
        )

        string(
            name: 'TAGS',
            defaultValue: '',
            description: 'Tags Ansible (ex: app,deploy). Laisser vide si non utilisé.'
        )

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

                    // Création du fichier vault avec permissions sécurisées
                    sh """
                        umask 077
                        echo "${params.VAULT_PASSWORD}" > vault_pass.txt
                    """

                    // Construction dynamique
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

                    // Exécution
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
            echo "\u001B[36mNettoyage du fichier vault...\u001B[0m"
            sh "rm -f vault_pass.txt || true"
        }
    }
}
