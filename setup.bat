@echo off
REM ============================================
REM CASINO ROUTER - Script de Setup Windows
REM ============================================

echo.
echo ==========================================
echo   Casino Router - Setup Automatique
echo ==========================================
echo.

REM Verification Docker
echo [1/6] Verification de Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Docker n'est pas installe
    echo Installez Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo [OK] Docker est installe
echo.

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Docker Compose n'est pas installe
    pause
    exit /b 1
)
echo [OK] Docker Compose est installe
echo.

REM Creation du fichier .env si inexistant
if not exist .env (
    echo [2/6] Creation du fichier .env...
    copy env.example .env >nul
    echo [OK] Fichier .env cree
    echo.
    echo [INFO] Editez le fichier .env pour configurer vos secrets
    echo.
) else (
    echo [2/6] Fichier .env existant detecte
    echo.
)

REM Arret des conteneurs existants
echo [3/6] Arret des conteneurs existants...
docker-compose down >nul 2>&1
echo [OK] Conteneurs arretes
echo.

REM Construction et demarrage
echo [4/6] Construction et demarrage des services...
echo      (Cela peut prendre quelques minutes...)
docker-compose up --build -d
if errorlevel 1 (
    echo [ERREUR] Echec du demarrage
    docker-compose logs
    pause
    exit /b 1
)
echo [OK] Services demarres
echo.

REM Attente PostgreSQL
echo [5/6] Attente du demarrage de PostgreSQL (15 secondes)...
timeout /t 15 /nobreak >nul
echo [OK] PostgreSQL pret
echo.

REM Seed des donnees
echo [6/6] Initialisation des donnees de test...
docker-compose exec -T app python seed_data.py
echo [OK] Donnees initialisees
echo.

REM Health check
echo Verification de l'etat du service...
timeout /t 3 /nobreak >nul
curl -s http://localhost:5000/health >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] Health check impossible
    echo Verifiez manuellement: http://localhost:5000/health
) else (
    echo [OK] API operationnelle
)
echo.

REM Résumé
echo ==========================================
echo   Installation terminee avec succes !
echo ==========================================
echo.
echo URLs disponibles:
echo   * API:              http://localhost:5000
echo   * Health:           http://localhost:5000/health
echo   * Documentation:    http://localhost:5000/docs
echo.
echo Commandes utiles:
echo   * Voir les logs:     docker-compose logs -f app
echo   * Arreter:           docker-compose down
echo   * Redemarrer:        docker-compose restart
echo.
echo Test rapide:
echo   Ouvrez: http://localhost:5000/click?sub1=test_affilie
echo.
echo Documentation:
echo   * README.md
echo   * API_DOCS.md
echo   * BOLT_INTEGRATION.md
echo   * GUIDE_COMPLET_FR.md
echo.
echo N'oubliez pas de:
echo   1. Configurer vos vrais casinos
echo   2. Mettre a jour vos landing pages Bolt
echo   3. Configurer les postbacks cote casinos
echo.
pause






