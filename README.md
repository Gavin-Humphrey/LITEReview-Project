Projet P9, LITReview

Mon projet OpenClassrooms de la formation D-A Python.
Il s'agit d'une application Web réalisée avec Django pour la société LitReview.
Une application de réseau social pour demander et publier des critiques de livres/articles.

Fonctionnalités:

    * Inscription / connexion.
    * Consulter un flux "Feeds" personnalisé en fonction de ses abonnements.
    * Consulter un flux "My Post" répertoriant toutes les demandes et critiques.
    * Trier les demandes et critiques sur chacune des pages les affichant.
    * Publier des demandes de critique.
    * Publier des critiques en réponse à une demande ou pas en réponse.
    * Modifier / supprimer ses demandes et critiques.
    * Consulter son profil, changer sa photo de profil.
    * Rechercher un utilisateur.
    * voir qui il suit et suivre qui il veut
    * Se désabonner d'un utilisateur.
    

Installation & lancement

Commencez par installer Python en premier.
Lancez ensuite la console, allez dans le dossier de votre choix et clonez ce repository :

git clone https://github.com/Gavin-Humphrey/LITEReview-Project.git

Allez dans le dossier LITEReview-Project, puis créez un nouvel environnement virtuel :

    python -m venv env

Ensuite, activez-le. 

MacOS et Linux :

    source env/bin/activate

    Installez ensuite les packages requis :

    pip install -r requirements.txt

Windows:

    env\scripts\activate.bat

    pip install -r requirements.txt

Effectuez ensuite la migration à la racine du projet, où se trouve le fichier manage.py, en procédant comme suit :

    python manage.py makemigrations

    Alors:

    python manage.py migrate

Il ne reste plus qu'à lancer le serveur de projet :

    python manage.py runserver

Vous pouvez ensuite utiliser l'application à l'adresse suivante :

    http://127.0.0.1:8000