# Utilise Python 3.12 slim
FROM python:3.12-slim

# Ne pas créer de fichiers .pyc et forcer l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système (pour psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt /app/requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du projet
COPY .. /app

# Exposer le port Flask
EXPOSE 5000

# Commande pour lancer ton app Flask
CMD ["python", "main.py"]
