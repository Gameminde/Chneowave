@echo off
echo ============================================
echo    CHNeoWave - Logiciel d'etude maritime
echo    Laboratoire de modeles reduits
echo    Mediterranee - Bassins et canaux
echo ============================================
echo.
echo Lancement de l'interface graphique...
echo.

cd /d "%~dp0\logciel hrneowave"

REM Verifier que l'environnement virtuel existe
if not exist "..\venv\Scripts\python.exe" (
    echo ERREUR: Environnement virtuel non trouve!
    echo Veuillez d'abord installer les dependances.
    pause
    exit /b 1
)

REM Lancer l'application
"..\venv\Scripts\python.exe" main.py

if errorlevel 1 (
    echo.
    echo ERREUR: Echec du lancement de l'application
    echo Verifiez les dependances et les logs d'erreur
    pause
)