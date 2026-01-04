#!/bin/bash

# 🚀 Casino Router - Installation automatique sur VPS
# Usage: wget https://raw.githubusercontent.com/USERNAME/casino-router/main/install_vps.sh && chmod +x install_vps.sh && ./install_vps.sh

set -e  # Arrêter en cas d'erreur

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🎰 Casino Router - Installation VPS Automatique          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables
INSTALL_DIR="/opt/casino-router"
GIT_REPO="https://github.com/USERNAME/casino-router.git"  # À REMPLACER

echo -e "${CYAN}📋 Vérification des prérequis...${NC}"

# Vérifier qu'on est root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Ce script doit être exécuté en tant que root${NC}"
    echo "Utilise: sudo ./install_vps.sh"
    exit 1
fi

# Demander l'URL du repo Git
echo -e "${YELLOW}🔗 URL du repo Git (ou Enter pour utiliser la valeur par défaut):${NC}"
read -p "Git URL [$GIT_REPO]: " custom_repo
GIT_REPO=${custom_repo:-$GIT_REPO}

echo ""
echo -e "${GREEN}✅ Prérequis OK${NC}"
echo ""

# Étape 1 : Mise à jour système
echo -e "${CYAN}📦 Mise à jour du système...${NC}"
apt update
apt upgrade -y

# Étape 2 : Installation Docker
echo -e "${CYAN}🐳 Installation de Docker...${NC}"
if ! command -v docker &> /dev/null; then
    apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt update
    apt install -y docker-ce
    systemctl start docker
    systemctl enable docker
    echo -e "${GREEN}✅ Docker installé${NC}"
else
    echo -e "${GREEN}✅ Docker déjà installé${NC}"
fi

# Étape 3 : Installation Docker Compose
echo -e "${CYAN}🐙 Installation de Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    apt install -y docker-compose
    echo -e "${GREEN}✅ Docker Compose installé${NC}"
else
    echo -e "${GREEN}✅ Docker Compose déjà installé${NC}"
fi

# Étape 4 : Installation Git
echo -e "${CYAN}📚 Installation de Git...${NC}"
if ! command -v git &> /dev/null; then
    apt install -y git
    echo -e "${GREEN}✅ Git installé${NC}"
else
    echo -e "${GREEN}✅ Git déjà installé${NC}"
fi

# Étape 5 : Installation Nginx
echo -e "${CYAN}🌐 Installation de Nginx...${NC}"
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
    echo -e "${GREEN}✅ Nginx installé${NC}"
else
    echo -e "${GREEN}✅ Nginx déjà installé${NC}"
fi

# Étape 6 : Configuration Firewall
echo -e "${CYAN}🔥 Configuration du firewall...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo "y" | ufw enable
echo -e "${GREEN}✅ Firewall configuré${NC}"

# Étape 7 : Clonage du repo
echo -e "${CYAN}📥 Clonage du repository...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Le dossier existe déjà, mise à jour...${NC}"
    cd $INSTALL_DIR
    git pull
else
    git clone $GIT_REPO $INSTALL_DIR
    cd $INSTALL_DIR
fi
echo -e "${GREEN}✅ Repository cloné${NC}"

# Étape 8 : Lancement Docker
echo -e "${CYAN}🚀 Démarrage des containers Docker...${NC}"
docker-compose down 2>/dev/null || true
docker-compose up -d --build
echo -e "${GREEN}✅ Containers démarrés${NC}"

# Attendre que l'API soit prête
echo -e "${CYAN}⏳ Attente du démarrage de l'API...${NC}"
sleep 10

# Étape 9 : Configuration Nginx
echo -e "${CYAN}⚙️  Configuration de Nginx...${NC}"
cat > /etc/nginx/sites-available/casino-router << 'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

ln -sf /etc/nginx/sites-available/casino-router /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
echo -e "${GREEN}✅ Nginx configuré${NC}"

# Étape 10 : Test de l'installation
echo ""
echo -e "${CYAN}🧪 Test de l'installation...${NC}"
sleep 3

if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API répond correctement !${NC}"
else
    echo -e "${RED}❌ Erreur: L'API ne répond pas${NC}"
    echo "Vérifiez les logs: docker-compose logs -f app"
    exit 1
fi

# Récupérer l'IP publique
PUBLIC_IP=$(curl -s ifconfig.me)

# Résumé final
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ Casino Router est maintenant en ligne !${NC}"
echo ""
echo -e "${CYAN}📍 Informations importantes :${NC}"
echo ""
echo -e "  🌐 Ton API: ${GREEN}http://$PUBLIC_IP${NC}"
echo -e "  🔗 Health check: ${GREEN}http://$PUBLIC_IP/health${NC}"
echo -e "  📊 Dashboard Live: ${GREEN}http://$PUBLIC_IP/dashboard-live${NC}"
echo -e "  🎯 Lien de tracking: ${GREEN}http://$PUBLIC_IP/click?sub1=TA_SOURCE${NC}"
echo ""
echo -e "${YELLOW}⚙️  Commandes utiles :${NC}"
echo ""
echo "  📋 Voir les logs:        docker-compose logs -f app"
echo "  🔄 Redémarrer:           docker-compose restart"
echo "  🛑 Arrêter:              docker-compose down"
echo "  📥 Mettre à jour:        cd $INSTALL_DIR && git pull && docker-compose restart"
echo "  💾 Backup DB:            docker exec casino_router_db pg_dump -U casino_user casino_router > backup.sql"
echo ""
echo -e "${CYAN}📝 Prochaines étapes :${NC}"
echo ""
echo "  1. Configure les postbacks des casinos avec: http://$PUBLIC_IP/postback"
echo "  2. Mets à jour ton lien de tracking: http://$PUBLIC_IP/click?sub1=..."
echo "  3. (Optionnel) Configure un domaine et SSL: certbot --nginx -d ton-domaine.com"
echo ""
echo -e "${GREEN}🚀 Ton Casino Router est prêt à générer des revenus !${NC}"
echo ""

