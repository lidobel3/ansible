node {
    stage('clone'){
        git branch: 'main', url: 'https://github.com/lidobel3/ansible.git'
    }
    
    stage('ansible'){
        ansiblePlaybook credentialsId: 'private_key', inventory: '${workspace}/hosts.yaml', playbook: '${workspace}/playbook.yaml'
    }
    
}