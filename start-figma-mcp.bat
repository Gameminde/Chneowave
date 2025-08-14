@echo off
echo ========================================
echo Demarrage du serveur MCP Figma
echo ========================================

REM Configuration des variables d'environnement
set FIGMA_ACCESS_TOKEN=figd_NiidvIEL-LM3Ih_frDWYgpzkxHengsh74a4NEvwb
set FIGMA_WEBSOCKET_PORT=3055
set FIGMA_WEBSOCKET_HOST=localhost

echo Token Figma configure: %FIGMA_ACCESS_TOKEN:~0,20%...
echo Port WebSocket: %FIGMA_WEBSOCKET_PORT%
echo Host WebSocket: %FIGMA_WEBSOCKET_HOST%

echo.
echo Demarrage du serveur MCP Figma...
echo Appuyez sur Ctrl+C pour arreter

REM Demarrer le serveur MCP Figma
node "C:\Users\youcef cheriet\AppData\Roaming\npm\node_modules\@sethdouglasford\mcp-figma\dist\talk_to_figma_mcp\server.js"

pause
