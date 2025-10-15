# Utilisation d'une image Python légère
FROM python:3.12-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation les dépendances sans cache
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet avec git clone....
COPY . .

# Expose le port de Flask
EXPOSE 5000

# Commande pour lancer l'app avec Gunicorn (production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
