pipeline {
    agent any

    options {
        ansiColor('xterm')   // Active les couleurs ANSI
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

                    echo "\u001B[34m=== 📦 Préparation du vault ===\u001B[0m"

                    // Création du fichier vault avec permissions sécurisées
                    sh """
                        umask 077
                        echo "${params.VAULT_PASSWORD}" > vault_pass.txt
                    """

                    echo "\u001B[33m>>> Génération de la commande Ansible...\u001B[0m"

                    // Construction dynamique
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

                    // Exécution d’Ansible
                    sh """#!/bin/bash
                        set -e
                        ${cmd}
                    """

                    echo "\u001B[32m✔ Playbook exécuté avec succès !\u001B[0m"
                }
            }
