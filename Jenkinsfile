pipeline {
    agent any

    parameters {
        choice(name: 'ANSIBLE_VERBOSITY', choices: ['-v', '-vv', '-vvv', '-vvvv'], description: 'Niveau de verbosité Ansible')
    }

    options {
        ansiColor('xterm')
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
            }
        }

        stage('Run Ansible') {
            steps {
                ansiColor('xterm') {
                    sh """
                        ansible-playbook ${params.ANSIBLE_VERBOSITY} \
                          -i ${env.WORKSPACE}/hosts.yaml \
                          ${env.WORKSPACE}/playbook.yaml \
                          --private-key ~/.ssh/private_key
                    """
                }
            }
        }
    }
}
