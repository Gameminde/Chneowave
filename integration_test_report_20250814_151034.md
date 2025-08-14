
🌊 CHNeoWave Integration Test Report
============================================================

📅 Date: 2025-08-14 15:10:34
📊 Tests: 9 total, 0 passed, 9 failed
✅ Success Rate: 0.0%

Detailed Results:
💥 API Health Check: ERROR (4.024s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /health (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000016747987770>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))
❌ UI Connectivity: FAIL (4.022s)
💥 CORS Configuration: ERROR (4.005s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /health (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000016747A78050>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))
💥 Hardware Backends: ERROR (4.007s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /hardware/backends (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001674796BBB0>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))
💥 Hardware Scan: ERROR (4.003s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /hardware/scan (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001674796B490>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))
💥 System Status: ERROR (4.019s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /system/status (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000016747A16690>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))
💥 Acquisition Status: ERROR (4.01s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /acquisition/status (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000016747A11040>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))
💥 Acquisition Start/Stop: ERROR (4.008s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /acquisition/start (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000016747A12140>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))
💥 FFT Processing: ERROR (4.016s)
   Error: HTTPConnectionPool(host='localhost', port=3001): Max retries exceeded with url: /processing/fft (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000016747A12360>: Failed to establish a new connection: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée'))

🎯 Integration Status: ISSUES DETECTED

📋 Next Steps:
⚠️ 9 test(s) en échec
🔧 Vérifier la configuration des serveurs
📡 Vérifier les ports 3001 et 5173
🐛 Consulter les logs pour plus de détails