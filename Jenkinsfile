#!groovy
pipeline {
    agent any

    parameters {
        // Define your ANSIBLE_VERBOSITY parameter here
        choice(name: 'ANSIBLE_VERBOSITY',
               //choices: ['', '-v', '-vv', '-vvv', '-vvvv', '-vvvvv'],
               choices: ['', '0', '1', '2', '3', '4', '5','6'],
               description: 'Choisissez le niveau de verbosité pour Ansible.')
    }

    stages {
        stage('clone'){
            steps {
                git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
            }
        }
        //----------------------------------------------------------------------------------------------------
        stage('ansible'){
            steps { // <--- This is the correct and ONLY 'steps' block for this stage

                script {
                    // Check if a verbosity level was selected
                    def ansibleVerbosity = ""
                    if (params.ANSIBLE_VERBOSITY != "") {
                        ansibleVerbosity = params.ANSIBLE_VERBOSITY
                    }

                    // First ansiblePlaybook call (you might not need this if the second one is complete)
                    ansiblePlaybook credentialsId: 'private_key', inventory: "${workspace}/hosts.yaml", playbook: "${workspace}/playbook.yaml"

                    // ansiColor('xterm') {
                    //     ansiblePlaybook(
                    //         playbook: "${workspace}/playbook.yaml", // Use workspace path
                    //         inventory: "${workspace}/hosts.yaml", // Use workspace path, not a raw URL from GitHub
                    //         credentialsId: 'sample-ssh-key',
                    //         colorized: true,
                    //         extras: "-v ${ansibleVerbosity}"
                    //     )
                    // }
                }
            } // <--- Close of the 'steps' block for 'stage('ansible')'
        }
    }
}