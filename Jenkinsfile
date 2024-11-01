node {
    stage('clone'){
        git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
    }
    
    stage('ansible'){
        //ansiblePlaybook credentialsId: 'private_key', inventory: '${workspace}/hosts.yaml', playbook: '${workspace}/playbook.yaml'
        ansiColor('xterm') {
            ansiblePlaybook(
                playbook: '${workspace}/playbook.yaml',
                inventory: '${workspace}/hosts.yaml',
                credentialsId: 'sample-ssh-key',
                colorized: true)
}
    }
    
}