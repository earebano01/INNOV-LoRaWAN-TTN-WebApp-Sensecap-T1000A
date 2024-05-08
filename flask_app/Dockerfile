FROM python:3.7-slim-buster

# Créer les répertoires
RUN mkdir -pv /home/project/flask_app \
    && mkdir -pv /var/ttn_tracker/ssl_certs

# Définir le répertoire de travail
WORKDIR /home/project/flask_app

# Définir les variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive

# Installer les outils de compilation et SQLite
RUN apt-get update && apt-get install -y build-essential sqlite3

# Copier les dépendances et installer les bibliothèques requises
COPY requirements.txt /home/project/flask_app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . /home/project/flask_app/

# Exécuter le script de génération de certificats SSL
RUN /bin/bash /home/project/flask_app/ssl-certs-generate.sh
