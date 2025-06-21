#!groovy
pipeline { //Le niveau supérieur du pipeline doit être un bloc, c'est-à-dire : pipeline { }.
    agent any
    //node {
    /*parameters {
        string(name: 'Greeting', defaultValue: 'Hello', description: 'How should I greet the world?')
    }*/
    stages {
        stage('clone'){
            steps {
                git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
            }
        }
        stage('ansible'){

             steps {
                ansiblePlaybook credentialsId: 'private_key', inventory: '${workspace}/hosts.yaml', playbook: '${workspace}/playbook.yaml'
                ansiColor('xterm') {
                    ansiblePlaybook(
                        playbook: '${workspace}/playbook.yaml',
                        inventory: 'https://github.com/lidobel3/ansible/blob/main/hosts.yaml',
                        credentialsId: 'sample-ssh-key',
                        colorized: true)
                    }
              }       
        }
    }
}    