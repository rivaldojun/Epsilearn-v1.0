# Utilisez une image de base Python
FROM python:3.7

# Créez un répertoire de travail dans le conteneur
WORKDIR /LERNENDER

# Copiez les fichiers de votre application dans le conteneur
COPY . .

# Installez les dépendances de l'application
RUN pip install -r requirements.txt

# Exposez le port sur lequel l'application Flask écoute (par défaut : 5000)
EXPOSE 5000

# Démarrez l'application Flask
CMD ["flask", "run"]
