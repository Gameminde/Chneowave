@echo off
echo ========================================
echo    CHNeoWave Project Cleaner
echo    Nettoyage du projet maritime
echo ========================================
echo.

REM Aller dans le répertoire du projet
cd /d "%~dp0"

REM Supprimer les fichiers dupliqués et non utilisés
echo Suppression des fichiers dupliques et non utilises...

REM Doublons dans HRNeoWave/gui (versions obsolètes)
if exist "HRNeoWave\gui\theme.py" del "HRNeoWave\gui\theme.py" && echo   Supprime: HRNeoWave/gui/theme.py
if exist "HRNeoWave\gui\welcome.py" del "HRNeoWave\gui\welcome.py" && echo   Supprime: HRNeoWave/gui/welcome.py
if exist "HRNeoWave\gui\calibration.py" del "HRNeoWave\gui\calibration.py" && echo   Supprime: HRNeoWave/gui/calibration.py
if exist "HRNeoWave\gui\acquisition.py" del "HRNeoWave\gui\acquisition.py" && echo   Supprime: HRNeoWave/gui/acquisition.py
if exist "HRNeoWave\gui\Traitementdonnee.py" del "HRNeoWave\gui\Traitementdonnee.py" && echo   Supprime: HRNeoWave/gui/Traitementdonnee.py
if exist "HRNeoWave\gui\main.py" del "HRNeoWave\gui\main.py" && echo   Supprime: HRNeoWave/gui/main.py

REM Doublons à la racine
if exist "hardware_adapter.py" del "hardware_adapter.py" && echo   Supprime: hardware_adapter.py
if exist "test_acquisition.py" del "test_acquisition.py" && echo   Supprime: test_acquisition.py
if exist "acquisition.py" del "acquisition.py" && echo   Supprime: acquisition.py

REM Archive des fixes
if exist "__fixes__.zip" del "__fixes__.zip" && echo   Supprime: __fixes__.zip

REM Fichiers HTML temporaires
if exist "logiciel hrneowave\documentation.html" del "logiciel hrneowave\documentation.html" && echo   Supprime: documentation.html
if exist "logiciel hrneowave\guide_utilisateur.html" del "logiciel hrneowave\guide_utilisateur.html" && echo   Supprime: guide_utilisateur.html
if exist "logiciel hrneowave\rapport_technique.html" del "logiciel hrneowave\rapport_technique.html" && echo   Supprime: rapport_technique.html

echo.
echo Suppression des dossiers non utilises...

REM Supprimer les dossiers non utilisés
if exist "HRNeoWave\advanced_visualization" rmdir /s /q "HRNeoWave\advanced_visualization" && echo   Supprime: HRNeoWave/advanced_visualization
if exist "HRNeoWave\advanced_wave_analysis" rmdir /s /q "HRNeoWave\advanced_wave_analysis" && echo   Supprime: HRNeoWave/advanced_wave_analysis
if exist "HRNeoWave\hardware_improvements" rmdir /s /q "HRNeoWave\hardware_improvements" && echo   Supprime: HRNeoWave/hardware_improvements
if exist "HRNeoWave\numerical_model_interface" rmdir /s /q "HRNeoWave\numerical_model_interface" && echo   Supprime: HRNeoWave/numerical_model_interface
if exist "HRNeoWave\probe_positioning" rmdir /s /q "HRNeoWave\probe_positioning" && echo   Supprime: HRNeoWave/probe_positioning
if exist "HRNeoWave\reflection_analysis" rmdir /s /q "HRNeoWave\reflection_analysis" && echo   Supprime: HRNeoWave/reflection_analysis
if exist "HRNeoWave\uncertainty_analysis" rmdir /s /q "HRNeoWave\uncertainty_analysis" && echo   Supprime: HRNeoWave/uncertainty_analysis
if exist "HRNeoWave\wave_generation" rmdir /s /q "HRNeoWave\wave_generation" && echo   Supprime: HRNeoWave/wave_generation
if exist "HRNeoWave\gui\gamemind" rmdir /s /q "HRNeoWave\gui\gamemind" && echo   Supprime: HRNeoWave/gui/gamemind

REM Supprimer le dossier gui s'il est vide
if exist "HRNeoWave\gui" rmdir "HRNeoWave\gui" 2>nul && echo   Supprime: HRNeoWave/gui (vide)

echo.
echo Nettoyage des caches Python...

REM Supprimer tous les dossiers __pycache__
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        rmdir /s /q "%%d"
        echo   Supprime cache: %%d
    )
)

REM Supprimer les fichiers .pyc
for /r . %%f in (*.pyc) do (
    if exist "%%f" (
        del "%%f"
        echo   Supprime: %%f
    )
)

echo.
echo ========================================
echo    NETTOYAGE TERMINE!
echo ========================================
echo.
echo Structure finale conservee:
echo   logiciel hrneowave/     (application principale)
echo   __fixes__/              (scripts d'amelioration)
echo   mcp_jobs/               (configurations MCP)
echo   venv/                   (environnement virtuel)
echo   pyproject.toml          (configuration projet)
echo   requirements.txt        (dependances)
echo   AUDIT_CHNEOWAVE_2025.md (documentation)
echo.
echo Le projet CHNeoWave est maintenant nettoye et optimise
echo pour les laboratoires d'etudes maritimes en modele reduit!
echo.
pause