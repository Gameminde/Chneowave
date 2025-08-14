@echo off
echo ========================================
echo Installation des dependances CHNeoWave
echo ========================================

echo.
echo Verification de Python...
python --version
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Veuillez installer Python depuis python.org ou Microsoft Store
    pause
    exit /b 1
)

echo.
echo Creation de l'environnement virtuel...
if exist venv (
    echo Suppression de l'ancien environnement virtuel...
    rmdir /s /q venv
)
python -m venv venv

echo.
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo Mise a jour de pip...
python -m pip install --upgrade pip

echo.
echo Installation des dependances principales...
pip install -r requirements.txt

echo.
echo Installation des dependances de developpement...
pip install -r requirements-dev.txt

echo.
echo Installation du projet en mode developpement...
pip install -e .

echo.
echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.
echo Pour activer l'environnement virtuel:
echo   venv\Scripts\activate.bat
echo.
echo Pour lancer CHNeoWave:
echo   python main.py
echo.
pause
