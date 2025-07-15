#!groovy
pipeline {
    agent any

    parameters {
        // Define your ANSIBLE_VERBOSITY parameter here
        choice(name: 'ANSIBLE_VERBOSITY',
               // We're using numerical choices because the 'verbosity' parameter of the plugin expects an integer.
               choices: ['0', '1', '2', '3', '4', '5', '6'], // '0' for no verbosity, '1' for -v, '2' for -vv, etc.
               description: 'Choisissez le niveau de verbosité pour Ansible (0=silencieux, 6=très verbeux).')
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
                    // Initialize verbosity to 0 (no verbosity) if nothing is selected or if it's an empty string.
                    def ansibleVerbosity = 0
                    if (params.ANSIBLE_VERBOSITY != "") {
                        // Convert the string parameter (e.g., "3") to an integer (e.g., 3)
                        ansibleVerbosity = params.ANSIBLE_VERBOSITY.toInteger()
                    }

                    // REMOVE OR COMMENT OUT THIS LINE:
                    // This ansiblePlaybook call does NOT support 'colorized' or 'verbosity' parameters directly.
                    // ansiblePlaybook credentialsId: 'private_key', inventory: "${workspace}/hosts.yaml", playbook: "${workspace}/playbook.yaml"

                    // THIS IS THE BLOCK THAT NEEDS TO BE ACTIVE FOR COLORS AND VERBOSITY
                    ansiColor('xterm') { // <-- UNCOMMENT THIS LINE
                        ansiblePlaybook(
                            playbook: "${workspace}/playbook.yaml", // Use workspace path
                            inventory: "${workspace}/hosts.yaml", // Use workspace path, not a raw URL from GitHub
                            credentialsId: 'private_key', // Ensure this matches your Jenkins credential ID
                            colorized: true, // <-- UNCOMMENT THIS LINE: ESSENTIAL for Ansible to output colors
                            verbosity: ansibleVerbosity // <-- UNCOMMENT THIS LINE: Pass the integer verbosity level
                        )
                    }
                }
            } // <--- Close of the 'steps' block for 'stage('ansible')'
        }
    }
}