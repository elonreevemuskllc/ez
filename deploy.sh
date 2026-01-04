#!/bin/bash

# 🚀 Script de mise à jour rapide sur VPS
# Usage: ./deploy.sh

set -e

echo "🚀 Déploiement en cours..."

# Pull les derniers changements
git pull

# Rebuild et redémarrage
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Attendre le démarrage
sleep 5

# Vérifier que ça fonctionne
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Déploiement réussi !"
    docker-compose logs --tail=20 app
else
    echo "❌ Erreur: L'API ne répond pas"
    docker-compose logs --tail=50 app
    exit 1
fi

