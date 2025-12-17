pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    parameters {

        string(
            name: 'BRANCH',
            defaultValue: 'intest',
            description: 'Branche Git à cloner'
        )
        choice(
            name: 'ENV',
            choices: ['dev', 'staging', 'prod'],
            description: 'Environnement cible'
        )
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

        // string(
        //     name: 'INVENTORY',
        //     defaultValue: 'inventories/${params.ENV}/hosts.ini',
        //     description: 'Fichier d’inventaire Ansible'
        // )

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
        stage('Clone Repository') {
            steps {
                echo "\u001B[34m=== 🔄 Clonage du dépôt Git (branche ${params.BRANCH}) ===\u001B[0m"
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: "refs/heads/${params.BRANCH}"]],
                    userRemoteConfigs: [[url: 'https://github.com/lidobel3/ansible.git']]
                ])
            }
        }

        stage('Run Ansible') {
            steps {
                script {
                    
                    def inventory = "inventories/${params.ENV}/hosts.ini"

                    echo "\u001B[34m=== 📦 Préparation du vault ===\u001B[0m"

                    sh """
                        umask 077
                        echo "${params.VAULT_PASSWORD}" > vault_pass.txt
                    """

                    echo "\u001B[33m>>> Génération de la commande Ansible...\u001B[0m"

                    def cmd = "ansible-playbook ${params.PLAYBOOK} -i ${params.INVENTORY} --vault-password-file vault_pass.txt"

                    if (params.LIMIT?.trim()) {
                        cmd += " --limit '${params.LIMIT}'"
                        echo "\u001B[36m • LIMIT ajouté : ${params.LIMIT}\u001B[0m"
                    }

                    if (params.TAGS?.trim()) {
                        cmd += " --tags '${params.TAGS}'"
                        echo "\u001B[36m • TAGS ajoutés : ${params.TAGS}\u001B[0m"
                    }

                    if (params.EXTRA_VARS?.trim()) {
                        cmd += " --extra-vars '${params.EXTRA_VARS}'"
                        echo "\u001B[36m • EXTRA_VARS ajoutés\u001B[0m"
                    }

                    echo "\u001B[32m✔ Commande exécutée (sanitisée) :\u001B[0m"
                    echo cmd.replace("--vault-password-file vault_pass.txt", "--vault-password-file *****")

                    echo "\u001B[35m=== 🚀 Exécution du playbook ===\u001B[0m"

                    sh """#!/bin/bash
                    set -e
                    ANSIBLE_FORCE_COLOR=1 PY_COLORS=1 ${cmd}
                    """

                    echo "\u001B[32m✔ Playbook exécuté avec succès !\u001B[0m"
                }
            }
        }
    }

    post {
        always {
            echo "\u001B[36m=== 🧹 Nettoyage du fichier vault... ===\u001B[0m"
            sh "rm -f vault_pass.txt || true"
            echo "\u001B[32m✔ Nettoyage terminé.\u001B[0m"
        }
    }
}
