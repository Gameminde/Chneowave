@echo off
echo 🌊 CHNeoWave - Lancement complet
echo ===================================

REM Activer l'environnement virtuel
call venv\Scripts\activate

echo 📋 Démarrage backend...
start "CHNeoWave-Backend" cmd /k "python main_backend_only.py"

echo ⏳ Attente backend (5s)...
timeout /t 5 /nobreak >nul

echo 📋 Démarrage interface...
start "CHNeoWave-UI" cmd /k "cd i-prototype-tailwind && npm run dev"

echo ✅ CHNeoWave démarré !
echo 📚 Backend: http://127.0.0.1:3001/docs
echo 🎨 Interface: http://127.0.0.1:5173
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
