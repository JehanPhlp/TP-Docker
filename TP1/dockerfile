# Étape 1 : Image de base
FROM python:3.11-slim

# Étape 2 : Répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY requirements.txt .

# Étape 4 : Installer Flask
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier l'application
COPY . .

# Étape 6 : Exposer le port Flask
EXPOSE 5000

# Étape 7 : Commande de démarrage
CMD ["python", "app.py"]