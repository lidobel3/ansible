# ansible

Ce Playbook est conçu pour s'executer sur une instance ec2 faisant office de self-hosted runner GitHub Action.
Donc sur cette machine déployé via terraform et jenkins, le rôle docker va 
    1. vérifier si docker est installé, l'installer le cas écheant.  
    2. Télécharger une image publique lidobel3/portfolio depuis dockerHub
    3. Cloner un repo Git privé dans un repertoire de l'hôte
    4. Déployer un conteneur à base de cette image en montant le repertoire dans le conteneur.
    