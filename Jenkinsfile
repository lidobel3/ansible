pipeline {
    agent any
    options {
        ansiColor('xterm')
    }
    environment {
        LANG = "fr_FR.UTF-8"
        LC_ALL = "fr_FR.UTF-8"
    }
    parameters {
        string(name: 'BRANCH', defaultValue: 'intest', description: 'Branche Git à cloner')
        choice(name: 'ENV', choices: ['dev','int','staging','prod'], description: 'Environnement cible')
        password(name: 'VAULT_PASSWORD', description: 'Mot de passe Ansible Vault')
        string(name: 'PLAYBOOK', defaultValue: 'playbooks/test_vault.yaml', description: 'Playbook Ansible à exécuter')
        string(name: 'LIMIT', description: 'Cible : groupe/host (ex: webservers). Laisser vide si non utilisé.')
        string(name: 'TAGS', description: 'Tags Ansible (ex: app,deploy). Laisser vide si non utilisé.')
        text(name: 'EXTRA_VARS', description: 'Variables supplémentaires (JSON ou KEY=VALUE). Exemple: {"env":"prod"}')
        choice(name: 'VERBOSITY', choices: ['0 - Normal','1 - Verbose (-v)','2 - Plus verbose (-vv)','3 - Debug (-vvv)','4 - Connection debug (-vvvv)'], description: 'Niveau de verbosité Ansible')
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

                    // Extraire le niveau de verbosité du choix
                    def verbosityLevel = params.VERBOSITY.tokenize(' ')[0].toInteger()
                    def verbosityFlag = verbosityLevel > 0 ? '-' + 'v' * verbosityLevel : ''

                    if (verbosityFlag) {
                        echo "\u001B[36m • Verbosité : ${verbosityFlag} (niveau ${verbosityLevel})\u001B[0m"
                    }

                    // Construction de la commande
                    def cmd = "ansible-playbook ${params.PLAYBOOK} -i ${inventory} --vault-password-file vault_pass.txt"
                    if (verbosityFlag) cmd += " ${verbosityFlag}"
                    if (params.LIMIT?.trim()) cmd += " --limit '${params.LIMIT}'"
                    if (params.TAGS?.trim()) cmd += " --tags '${params.TAGS}'"
                    if (params.EXTRA_VARS?.trim()) cmd += " --extra-vars '${params.EXTRA_VARS}'"

                    echo "\u001B[32m✔ Commande exécutée (sanitisée) :\u001B[0m"
                    echo cmd.replace("--vault-password-file vault_pass.txt", "--vault-password-file *****")

                    echo "\u001B[35m=== 🚀 Exécution du playbook ===\u001B[0m"
                    sh """#!/bin/bash
                    set -e
                    export LANG=fr_FR.UTF-8
                    export LC_ALL=fr_FR.UTF-8
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