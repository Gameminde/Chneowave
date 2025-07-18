@echo off
REM Script de démarrage rapide CHNeoWave
REM Mode laboratoire offline avec validation matérielle

setlocal EnableDelayedExpansion

echo ========================================
echo    CHNeoWave - Lancement Laboratoire
echo ========================================
echo.

REM Vérification de l'environnement Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python non trouvé dans le PATH
    echo Veuillez installer Python ou activer l'environnement virtuel
    pause
    exit /b 1
)

REM Affichage de la version Python
echo Python détecté:
for /f "tokens=*" %%i in ('python --version') do echo   %%i
echo.

REM Vérification du répertoire de travail
if not exist "__fixes__" (
    echo ERREUR: Répertoire __fixes__ non trouvé
    echo Veuillez exécuter ce script depuis le répertoire racine de CHNeoWave
    pause
    exit /b 1
)

if not exist "mcp_jobs\launch_local.yml" (
    echo ERREUR: Configuration launch_local.yml non trouvée
    echo Veuillez vérifier l'installation
    pause
    exit /b 1
)

echo Configuration trouvée: mcp_jobs\launch_local.yml
echo.

REM Création des répertoires nécessaires
echo Préparation de l'environnement...
if not exist "logs" mkdir logs
if not exist "config" mkdir config
if not exist "exports" mkdir exports
if not exist "local_packages" mkdir local_packages
echo   - Répertoires créés: logs, config, exports, local_packages
echo.

REM Configuration des variables d'environnement par défaut
set CHNW_MODE=offline
set CHNW_FS=500
set CHNW_N_PROBES=16
set CHNW_GEOM=config\probes_geom.json
set CHNW_LOG_LEVEL=INFO
set PYTHONUNBUFFERED=1
set PYTHONDONTWRITEBYTECODE=1

echo Variables d'environnement configurées:
echo   CHNW_MODE=%CHNW_MODE%
echo   CHNW_FS=%CHNW_FS% Hz
echo   CHNW_N_PROBES=%CHNW_N_PROBES% sondes
echo   CHNW_GEOM=%CHNW_GEOM%
echo.

REM Menu de sélection
echo Sélectionnez une option:
echo   1. Lancement complet (installation + validation + démarrage)
echo   2. Validation matérielle uniquement
echo   3. Lancement direct (sans installation)
echo   4. Test de performance
echo   5. Lister les tâches disponibles
echo   6. Configuration personnalisée
echo   0. Quitter
echo.
set /p choice="Votre choix (1-6, 0 pour quitter): "

if "%choice%"=="0" goto :end
if "%choice%"=="1" goto :full_launch
if "%choice%"=="2" goto :validate_only
if "%choice%"=="3" goto :direct_launch
if "%choice%"=="4" goto :performance_test
if "%choice%"=="5" goto :list_tasks
if "%choice%"=="6" goto :custom_config

echo Choix invalide, lancement complet par défaut...
goto :full_launch

:full_launch
echo.
echo ========================================
echo    LANCEMENT COMPLET CHNEOWAVE
echo ========================================
echo.
echo Démarrage du processus complet...
python mcp_jobs\launcher.py --config mcp_jobs\launch_local.yml
goto :check_result

:validate_only
echo.
echo ========================================
echo    VALIDATION MATÉRIELLE UNIQUEMENT
echo ========================================
echo.
echo Validation des exigences matérielles...
python -m __fixes__.hardware_requirements --validate --strict --report logs\hw_validation.json
if errorlevel 1 (
    echo.
    echo ATTENTION: Validation matérielle échouée
    echo Consultez logs\hw_validation.json pour les détails
    pause
) else (
    echo.
    echo ✅ Validation matérielle réussie
    echo Rapport disponible: logs\hw_validation.json
)
goto :end

:direct_launch
echo.
echo ========================================
echo    LANCEMENT DIRECT CHNEOWAVE
echo ========================================
echo.
echo Lancement direct du logiciel...
python mcp_jobs\launcher.py --config mcp_jobs\launch_local.yml --task launch_chneowave
goto :check_result

:performance_test
echo.
echo ========================================
echo    TEST DE PERFORMANCE
echo ========================================
echo.
echo Exécution des tests de performance...
python -m __fixes__.benchmark_performance --quick-test --config __fixes__\bench_results_2025-07-15.json
if errorlevel 1 (
    echo.
    echo ATTENTION: Tests de performance échoués
    pause
) else (
    echo.
    echo ✅ Tests de performance terminés
    echo Résultats disponibles dans __fixes__\bench_results_2025-07-15.json
)
goto :end

:list_tasks
echo.
echo ========================================
echo    TÂCHES DISPONIBLES
echo ========================================
echo.
python mcp_jobs\launcher.py --config mcp_jobs\launch_local.yml --list-tasks
pause
goto :end

:custom_config
echo.
echo ========================================
echo    CONFIGURATION PERSONNALISÉE
echo ========================================
echo.
echo Configuration actuelle:
echo   Fréquence d'échantillonnage: %CHNW_FS% Hz
echo   Nombre de sondes: %CHNW_N_PROBES%
echo   Fichier géométrie: %CHNW_GEOM%
echo.
set /p new_fs="Nouvelle fréquence (Hz) [%CHNW_FS%]: "
set /p new_probes="Nombre de sondes [%CHNW_N_PROBES%]: "
set /p new_geom="Fichier géométrie [%CHNW_GEOM%]: "

if not "%new_fs%"=="" set CHNW_FS=%new_fs%
if not "%new_probes%"=="" set CHNW_N_PROBES=%new_probes%
if not "%new_geom%"=="" set CHNW_GEOM=%new_geom%

echo.
echo Nouvelle configuration:
echo   CHNW_FS=%CHNW_FS%
echo   CHNW_N_PROBES=%CHNW_N_PROBES%
echo   CHNW_GEOM=%CHNW_GEOM%
echo.
set /p confirm="Confirmer et lancer? (o/N): "
if /i "%confirm%"=="o" goto :full_launch
if /i "%confirm%"=="oui" goto :full_launch
goto :end

:check_result
if errorlevel 1 (
    echo.
    echo ========================================
    echo    ERREUR DE LANCEMENT
    echo ========================================
    echo.
    echo Le lancement a échoué. Vérifiez:
    echo   1. Les logs dans le répertoire logs\
    echo   2. La configuration matérielle
    echo   3. Les dépendances Python
    echo.
    echo Actions de diagnostic disponibles:
    echo   - python -m __fixes__.validate_optimizations --diagnose
    echo   - python -m __fixes__.hardware_requirements --requirements-only
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo    LANCEMENT RÉUSSI
    echo ========================================
    echo.
    echo CHNeoWave a été lancé avec succès!
    echo.
    echo Fichiers générés:
    echo   - Logs: logs\
    echo   - Exports: exports\
    echo   - Configuration: config\
    echo.
    echo Pour arrêter le logiciel, fermez cette fenêtre ou utilisez Ctrl+C
)

:end
echo.
echo Session terminée.
if "%choice%"=="1" (
    echo.
    echo CHNeoWave peut continuer à fonctionner en arrière-plan.
    echo Fermez cette fenêtre pour terminer complètement.
    pause
)
endlocal