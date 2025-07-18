@echo off
echo ========================================
echo     Lancement de CHNeoWave
echo ========================================
echo.

cd /d "C:\Users\LEM\Desktop\chneowave\logciel hrneowave"

echo Verification de l'environnement virtuel...
if not exist "..\venv\Scripts\python.exe" (
    echo ❌ Environnement virtuel non trouve!
    echo Veuillez installer l'environnement virtuel d'abord.
    pause
    exit /b 1
)

echo ✅ Environnement virtuel trouve
echo.
echo Lancement de CHNeoWave...
echo.

"..\venv\Scripts\python.exe" main.py

echo.
echo CHNeoWave s'est arrete.
pause