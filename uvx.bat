@echo off
REM Script uvx.bat pour résoudre l'erreur MCP "uvx not found"
REM Redirige les commandes uvx vers uv run

REM Activer l'environnement virtuel CHNeoWave
call "%~dp0venv\Scripts\activate.bat"

REM Exécuter uv run avec tous les arguments passés
"%~dp0venv\Scripts\uv.exe" run %*
