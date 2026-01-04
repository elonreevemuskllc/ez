# 🚀 DÉPLOIEMENT SUR VPS - GUIDE COMPLET

## 📋 PRÉREQUIS

- VPS avec Ubuntu 20.04+ (Contabo, Hetzner, OVH, DigitalOcean)
- Au moins 2GB RAM, 20GB disque
- Accès SSH root
- Domaine pointé vers l'IP du VPS (optionnel)

---

## 🎯 MÉTHODE 1 : INSTALLATION AUTOMATIQUE (RECOMMANDÉ)

### Étape 1 : Push ton code sur Git

```powershell
# Sur Windows, dans PowerShell
cd "C:\Users\trooz\Desktop\Nouveau dossier (2)\david\david"

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Commit initial
git commit -m "Casino Router v1.0 - Production ready"

# Ajouter le remote (remplace par ton repo)
git remote add origin https://github.com/TON_USERNAME/casino-router.git

# Push
git branch -M main
git push -u origin main
```

### Étape 2 : Sur le VPS

```bash
# Se connecter au VPS
ssh root@TON_VPS_IP

# Télécharger et exécuter le script d'installation
wget https://raw.githubusercontent.com/TON_USERNAME/casino-router/main/install_vps.sh
chmod +x install_vps.sh
./install_vps.sh
```

**C'EST TOUT !** Le script fait tout automatiquement. ⚡

---

## 🎯 MÉTHODE 2 : INSTALLATION MANUELLE

### Étape 1 : Connexion et préparation

```bash
# Se connecter au VPS
ssh root@TON_VPS_IP

# Mettre à jour le système
apt update && apt upgrade -y

# Installer les dépendances
apt install docker.io docker-compose git nginx certbot python3-certbot-nginx ufw -y

# Démarrer Docker
systemctl start docker
systemctl enable docker
```

### Étape 2 : Cloner le projet

```bash
# Créer le dossier
mkdir -p /opt/casino-router
cd /opt

# Cloner depuis Git
git clone https://github.com/TON_USERNAME/casino-router.git
cd casino-router
```

### Étape 3 : Configurer le firewall

```bash
# Ouvrir les ports nécessaires
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### Étape 4 : Lancer Docker

```bash
# Démarrer les containers
docker-compose up -d

# Vérifier que ça tourne
docker ps

# Voir les logs
docker-compose logs -f app
```

### Étape 5 : Configurer Nginx (reverse proxy)

```bash
# Créer la config Nginx
cat > /etc/nginx/sites-available/casino-router << 'EOF'
server {
    listen 80;
    server_name _;  # Remplace par ton-domaine.com si tu as un domaine

    # Limite la taille des requêtes
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

# Activer la config
ln -s /etc/nginx/sites-available/casino-router /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default  # Supprimer la config par défaut

# Tester la config
nginx -t

# Redémarrer Nginx
systemctl restart nginx
```

### Étape 6 : Installer SSL (HTTPS) - Optionnel mais recommandé

```bash
# Si tu as un domaine (exemple: casino-router.com)
certbot --nginx -d ton-domaine.com

# Suivre les instructions, accepter les redirections HTTPS
```

### Étape 7 : Tester le système

```bash
# Test local
curl http://localhost:5000/health

# Test via Nginx
curl http://TON_VPS_IP/health

# Si domaine configuré
curl https://ton-domaine.com/health
```

---

## 🔧 CONFIGURATION POST-INSTALLATION

### Mettre à jour les postbacks des casinos

Remplace `ngrok` par ton IP ou domaine dans les postbacks :

**Avant** :
```
https://subrictal-fallon-precomprehensively.ngrok-free.dev/postback
```

**Après (avec IP)** :
```
http://TON_VPS_IP/postback
```

**Après (avec domaine + SSL)** :
```
https://ton-domaine.com/postback
```

### Mettre à jour ton lien de tracking

**Nouveau lien** :
```
http://TON_VPS_IP/click?sub1=TA_SOURCE
```

Ou avec domaine :
```
https://ton-domaine.com/click?sub1=TA_SOURCE
```

---

## 🛠️ COMMANDES UTILES

### Gestion Docker

```bash
# Voir les containers
docker ps

# Voir les logs
docker-compose logs -f app
docker-compose logs --tail=100 app

# Redémarrer
docker-compose restart

# Arrêter
docker-compose down

# Redémarrer un container spécifique
docker-compose restart app

# Rebuild complet
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Mise à jour depuis Git

```bash
cd /opt/casino-router

# Pull les derniers changements
git pull

# Rebuild et redémarrer
docker-compose down
docker-compose build
docker-compose up -d
```

### Backup de la base de données

```bash
# Backup manuel
docker exec casino_router_db pg_dump -U casino_user casino_router > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurer depuis un backup
docker exec -i casino_router_db psql -U casino_user -d casino_router < backup_20260104_123456.sql
```

### Monitoring

```bash
# Utilisation disque
df -h

# Utilisation RAM
free -h

# Processus Docker
docker stats

# Logs système
journalctl -u docker -f
```

---

## 📊 MONITORING ET ALERTES

### Installer Uptime Monitor (gratuit)

1. Va sur https://uptimerobot.com
2. Crée un compte gratuit
3. Ajoute un monitor HTTP(s) :
   - URL : `http://TON_VPS_IP/health`
   - Interval : 5 minutes
   - Alert : Email

### Logs en temps réel

```bash
# Créer un alias pour voir les logs facilement
echo "alias casinologs='docker-compose -f /opt/casino-router/docker-compose.yml logs -f app'" >> ~/.bashrc
source ~/.bashrc

# Utilisation
casinologs
```

---

## 🔐 SÉCURITÉ (OPTIONNEL MAIS RECOMMANDÉ)

### Changer le port SSH (éviter les bots)

```bash
nano /etc/ssh/sshd_config
# Changer Port 22 en Port 2222

systemctl restart ssh

# Ne pas oublier d'ouvrir le nouveau port
ufw allow 2222/tcp
```

### Désactiver le login root direct

```bash
# Créer un utilisateur
adduser casino
usermod -aG sudo casino

# Se connecter avec ce user à l'avenir
```

### Rate limiting avec fail2ban

```bash
apt install fail2ban -y
systemctl enable fail2ban
```

---

## 🚨 TROUBLESHOOTING

### Problème 1 : Docker ne démarre pas

```bash
# Vérifier le status
systemctl status docker

# Redémarrer Docker
systemctl restart docker

# Voir les logs
journalctl -u docker --no-pager
```

### Problème 2 : Port 5000 déjà utilisé

```bash
# Voir ce qui utilise le port 5000
lsof -i :5000

# Tuer le processus
kill -9 PID
```

### Problème 3 : Nginx ne démarre pas

```bash
# Tester la config
nginx -t

# Voir les logs
tail -f /var/log/nginx/error.log

# Redémarrer
systemctl restart nginx
```

### Problème 4 : Base de données corrompue

```bash
# Arrêter les containers
docker-compose down

# Supprimer les volumes
docker volume rm casino_router_pgdata

# Redémarrer (recrée la DB)
docker-compose up -d
```

---

## 🔄 AUTOMATISATION

### Cron job pour backup quotidien

```bash
# Éditer crontab
crontab -e

# Ajouter cette ligne (backup tous les jours à 3h du matin)
0 3 * * * docker exec casino_router_db pg_dump -U casino_user casino_router > /root/backup_casino_$(date +\%Y\%m\%d).sql

# Garder seulement les 7 derniers backups
0 4 * * * find /root/backup_casino_*.sql -mtime +7 -delete
```

### Script de déploiement automatique

Créer `/opt/deploy.sh` :

```bash
#!/bin/bash
cd /opt/casino-router
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
echo "✅ Déploiement terminé !"
docker-compose logs --tail=20 app
```

```bash
chmod +x /opt/deploy.sh
```

Utilisation :
```bash
/opt/deploy.sh
```

---

## 📈 SCALING (Si beaucoup de trafic)

### Load Balancer avec plusieurs instances

```yaml
# docker-compose.yml modifié
version: '3.8'

services:
  app1:
    build: .
    # ... config

  app2:
    build: .
    # ... config

  nginx:
    image: nginx
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
```

### Nginx Load Balancer Config

```nginx
upstream casino_backend {
    server app1:5000;
    server app2:5000;
}

server {
    location / {
        proxy_pass http://casino_backend;
    }
}
```

---

## ✅ CHECKLIST DÉPLOIEMENT COMPLET

```
☐ VPS acheté et accessible via SSH
☐ Docker installé
☐ Code pushé sur Git
☐ Repo cloné sur le VPS
☐ Firewall configuré (ports 22, 80, 443)
☐ Docker démarré (docker-compose up -d)
☐ Nginx installé et configuré
☐ SSL configuré (si domaine)
☐ Health check OK (http://IP/health)
☐ Postbacks des casinos mis à jour
☐ Lien de tracking mis à jour
☐ Backup automatique configuré
☐ Monitoring configuré (UptimeRobot)
☐ Test complet avec clicks réels
```

---

## 🎉 RÉSULTAT FINAL

Ton système est maintenant :
- ✅ En production 24/7
- ✅ Accessible publiquement
- ✅ Sécurisé (firewall + SSL)
- ✅ Monitoré
- ✅ Backupé automatiquement
- ✅ Facile à mettre à jour (git pull)

**Plus besoin de ton PC ! Plus besoin de ngrok !** 🚀

---

## 📞 SUPPORT

Si tu as des problèmes :

1. Vérifie les logs : `docker-compose logs -f app`
2. Vérifie Nginx : `nginx -t`
3. Vérifie le firewall : `ufw status`
4. Vérifie Docker : `docker ps`

**Tout est documenté et automatisé ! 💪**

