@Grab(group='org.eclipse.jgit', module='org.eclipse.jgit', version='5.11.0.202103091610-r')
import org.eclipse.jgit.api.Git
import org.eclipse.jgit.api.errors.GitAPIException
import java.io.File

// Définir l'URL du dépôt Git et le répertoire où cloner le code
def gitRepoUrl = 'https://github.com/lidobel3/ansible.git' // Remplacez par l'URL de votre dépôt Git
def cloneDir = new File("/tmp/ansible_repo")  // Répertoire temporaire pour cloner le dépôt

// Cloner le dépôt Git
try {
    println "Clonage du dépôt Git..."
    if (!cloneDir.exists()) {
        cloneDir.mkdirs()
    }
    Git.cloneRepository()
       .setURI(gitRepoUrl)
       .setDirectory(cloneDir)
       .call()
    println "Clonage terminé dans : ${cloneDir.absolutePath}"
} catch (GitAPIException e) {
    println "Erreur lors du clonage du dépôt Git : ${e.message}"
    return
}

// Vérifier si le fichier 'playbook.yml' existe dans le répertoire cloné
def playbookPath = new File(cloneDir, "playbook.yml")
if (!playbookPath.exists()) {
    println "Le fichier playbook.yml n'a pas été trouvé dans le dépôt cloné."
    return
}

// Exécuter Ansible avec le playbook cloné
def ansibleCommand = "ansible-playbook ${playbookPath.absolutePath}"
println "Exécution de la commande : ${ansibleCommand}"

try {
    def process = ansibleCommand.execute()
    process.waitFor()
    
    if (process.exitValue() == 0) {
        println "Playbook exécuté avec succès."
    } else {
        println "Erreur lors de l'exécution du playbook. Code de sortie : ${process.exitValue()}"
    }
} catch (Exception e) {
    println "Erreur lors de l'exécution d'Ansible : ${e.message}"
}
