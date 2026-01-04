#!/bin/bash

# ============================================
# CASINO ROUTER - Script de Setup Rapide
# ============================================

echo "🎰 Casino Router - Setup Automatique"
echo "====================================="
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier Docker
echo "📦 Vérification de Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    echo "Installez Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose n'est pas installé${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker est installé${NC}"
echo ""

# Créer le fichier .env si inexistant
if [ ! -f .env ]; then
    echo "⚙️  Création du fichier .env..."
    cp env.example .env
    
    # Générer des secrets aléatoires
    POSTBACK_SECRET=$(openssl rand -base64 32)
    ADMIN_PASSWORD=$(openssl rand -base64 16)
    
    # Remplacer dans .env
    sed -i "s/changez-moi-secret-minimum-32-caracteres-aleatoires/$POSTBACK_SECRET/" .env
    sed -i "s/changez-moi-password-securise-minimum-16-caracteres/$ADMIN_PASSWORD/" .env
    
    echo -e "${GREEN}✅ Fichier .env créé avec secrets sécurisés${NC}"
    echo ""
    echo -e "${YELLOW}🔐 Credentials Admin:${NC}"
    echo "   Username: admin"
    echo "   Password: $ADMIN_PASSWORD"
    echo ""
    echo -e "${YELLOW}🔑 Postback Secret:${NC}"
    echo "   $POSTBACK_SECRET"
    echo ""
    echo "⚠️  SAUVEGARDEZ CES INFORMATIONS !"
    echo ""
    read -p "Appuyez sur Entrée pour continuer..."
else
    echo -e "${YELLOW}ℹ️  Fichier .env existant détecté${NC}"
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants (si présents)..."
docker-compose down 2>/dev/null

# Construire et démarrer
echo ""
echo "🏗️  Construction et démarrage des services..."
docker-compose up --build -d

# Attendre que PostgreSQL soit prêt
echo ""
echo "⏳ Attente du démarrage de PostgreSQL..."
sleep 10

# Vérifier que tout est démarré
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Services démarrés avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors du démarrage${NC}"
    docker-compose logs
    exit 1
fi

# Seed des données
echo ""
echo "🌱 Initialisation des données de test..."
docker-compose exec -T app python seed_data.py

# Health check
echo ""
echo "🏥 Vérification de l'état du service..."
sleep 3
HEALTH=$(curl -s http://localhost:5000/health | grep -o '"status":"healthy"')

if [ ! -z "$HEALTH" ]; then
    echo -e "${GREEN}✅ API is healthy!${NC}"
else
    echo -e "${RED}❌ API health check failed${NC}"
    docker-compose logs app
    exit 1
fi

# Résumé
echo ""
echo "============================================"
echo -e "${GREEN}🎉 Installation terminée avec succès !${NC}"
echo "============================================"
echo ""
echo "📍 URLs disponibles:"
echo "   • API:          http://localhost:5000"
echo "   • Health:       http://localhost:5000/health"
echo "   • Docs (Swagger): http://localhost:5000/docs"
echo ""
echo "🔧 Commandes utiles:"
echo "   • Voir les logs:     docker-compose logs -f app"
echo "   • Arrêter:           docker-compose down"
echo "   • Redémarrer:        docker-compose restart"
echo "   • Stats admin:       curl http://localhost:5000/admin/stats -u admin:VOTRE_PASSWORD"
echo ""
echo "📚 Documentation:"
echo "   • README.md"
echo "   • API_DOCS.md"
echo "   • BOLT_INTEGRATION.md"
echo ""
echo "🧪 Test rapide:"
echo "   http://localhost:5000/click?sub1=test_affilié"
echo ""
echo -e "${YELLOW}⚠️  N'oubliez pas de:${NC}"
echo "   1. Configurer vos vrais casinos (supprimer les exemples)"
echo "   2. Mettre à jour vos landing pages Bolt"
echo "   3. Configurer les postbacks côté casinos"
echo ""






