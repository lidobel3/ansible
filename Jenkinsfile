pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Choisir l’environnement')
        choice(name: 'GROUP', choices: ['frontend', 'middle', 'bdd'], description: 'Choisir le groupe d’hôtes')
        password(name: 'VAULT_PASS', defaultValue: '', description: 'Mot de passe pour Ansible Vault')
        string(name: 'GIT_REPO', defaultValue: 'git@github.com:lidobel3/ansible.git', description: 'URL du repository Git')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Branche Git à utiliser')
    }

    environment {
        INVENTORY = "inventaires/${params.ENV}/hosts.ini"
        PLAYBOOK = "playbooks/site.yml"
    }

    stages {
        stage('Checkout Git') {
            steps {
                git branch: params.GIT_BRANCH, url: params.GIT_REPO
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                script {
                    ansiblePlaybook(
                        installation: 'Ansible',
                        playbook: "${PLAYBOOK}",
                        inventory: "${INVENTORY}",
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

/*node {
    stage('clone'){
        git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
    }
    
    stage('ansible'){
        ansiblePlaybook credentialsId: 'private_key', inventory: '${workspace}/hosts.yaml', playbook: '${workspace}/playbook.yaml'
    }
    
}*/