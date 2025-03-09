#!groovy
pipeline { //Le niveau supérieur du pipeline doit être un bloc, c'est-à-dire : pipeline { }.
    agent any
    //node {
    stages {
        stage('clone'){
            //git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
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
                        //playbook: 'https://github.com/lidobel3/ansible/blob/main/playbook.yaml',
                        //playbook: 'https://raw.githubusercontent.com/lidobel3/ansible/main/playbook.yaml',
                        //inventory: '${workspace}/hosts.yaml',
                        inventory: 'https://github.com/lidobel3/ansible/blob/main/hosts.yaml',
                        credentialsId: 'sample-ssh-key',
                        colorized: true)
                    }
              }       
        }
    }
}    