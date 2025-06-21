pipeline {
    agent any

    parameters {
        choice(name: 'ANSIBLE_VERBOSITY', choices: ['-v', '-vv', '-vvv', '-vvvv'], description: 'Choisis le niveau de verbosité Ansible')
    }

    options {
        ansiColor('xterm') // Active les couleurs ANSI pour la sortie console
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                ansiColor('xterm') {
                    ansiblePlaybook(
                        playbook: "${env.WORKSPACE}/playbook.yaml",
                        inventory: "${env.WORKSPACE}/hosts.yaml",
                        credentialsId: 'private_key',
                        colorized: true,
                        options: "${params.ANSIBLE_VERBOSITY}"
                    )
                }
            }
        }
    }
}
