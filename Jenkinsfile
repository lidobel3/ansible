pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Choisir l’environnement')
        choice(name: 'GROUP', choices: ['frontend', 'middle', 'bdd'], description: 'Choisir le groupe d’hôtes')
        /*password(name: 'VAULT_PASS', defaultValue: '', description: 'Mot de passe pour Ansible Vault')*/
        string(name: 'GIT_REPO', defaultValue: 'https://github.com/lidobel3/ansible.git', description: 'URL du repository Git')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Branche Git à utiliser')
    }

    environment {
        PLAYBOOK = "playbooks/playbook.yml"
    }

    stages {
        stage('Afficher les paramètres') {
            steps {
                script {
                    echo "=== Paramètres du pipeline ==="
                    echo "ENV : ${params.ENV}"
                    echo "GROUP : ${params.GROUP}"
                    echo "VAULT_PASS : ******** (non affiché pour sécurité)"
                    echo "GIT_REPO : ${params.GIT_REPO}"
                    echo "GIT_BRANCH : ${params.GIT_BRANCH}"
                }
            }
        }

        stage('Checkout Git') {
            steps {
                git branch: "${params.GIT_BRANCH}", url: "${params.GIT_REPO}"
            }
        }

        stage('Exécuter le playbook Ansible') {
            steps {
                script {
                    def inventoryPath = "inventaires/${params.ENV}/hosts.ini"
                    ansiblePlaybook(
                        installation: 'Ansible', // Nom configuré dans Jenkins (Manage Jenkins > Global Tool Configuration)
                        playbook: "${PLAYBOOK}",
                        inventory: "${inventoryPath}",
                        vaultPassword: params.VAULT_PASS,
                        limit: params.GROUP,
                        extraVars: [
                            env: params.ENV
                        ],
                        colorized: true
                    )
                }
            }
        }
    }
}
