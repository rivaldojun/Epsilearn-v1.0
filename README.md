# Mon Projet
Projet EPSILEARN 

## Clonage du Projet
```bash
cd repertoire/de/clonage
git clone https://github.com/rivaldojun/Lernender.git
```

## Environement virtuel
Creez un nouvel environnement virtuel hors du fichie du repo
Activer l'environnement virtuel dans vsccode (si vous utilisz vscode)

## Requirements
pip install -r requirements.txt

## Lancement de l'app
Lancer 'app.py'
Si le lien ne vient pas dans le terminal, connectez-vous sur http://127.0.0.1:5000/accueil

## Contribution
git add .
git commit -m "Ajout de ma nouvelle fonctionnalité"
git pull(s'il y'a des conflits contactez le dernier a modifier le fichier et regler les conflits ensemble )
git push 

## Architecture du code
Les vues flask sont dans le dossier /routes (chaque fichier de ce dossier contient les routes d'un pages ayant des points communs)
Le fichier fonction.py contient des fonctions utiliser pour traiter les donnees
Le fichier models.py contient les models ORM  (architecture des tables) pour la bd --c'est dans ce fichier que vous ajouter des tables ou des colonnes a la bd
Le dossier template contient les fichier html (un peu desorganisé)
Le dossier static contient les media,les fichier css,js et json
Le dossier api conotient les models & algorithmes d'IA
Le dossier instance contient le fichier de la base de donnees (Actuelement sqlite.Mais une migration vers postgres pour la mise en production)
Procfile s'agit du fichier de configuration Heroku .
