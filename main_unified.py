#!/usr/bin/env python3
"""
CHNeoWave - Point d'entrée unique
Lancement complet: Backend API + Interface React + Core Python
"""

import os
import time
import threading
import subprocess
import sys
import socket
import webbrowser
from pathlib import Path

import uvicorn
import requests

# Configuration
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 3001
UI_HOST = "127.0.0.1"  
UI_PORT = 5173

PROJECT_ROOT = Path(__file__).parent
FRONTEND_DIR = PROJECT_ROOT / "i-prototype-tailwind"

def log(category, message):
    """Logger simple"""
    print(f"[{category}] {message}")

def port_in_use(host, port):
    """Vérifie si un port est utilisé"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_free_port(host, start_port):
    """Trouve un port libre"""
    port = start_port
    for _ in range(20):
        if not port_in_use(host, port):
            return port
        port += 1
    raise RuntimeError(f"Aucun port libre trouvé à partir de {start_port}")

def setup_environment():
    """Configure l'environnement"""
    os.environ["BACKEND_MODE"] = "real"
    os.environ["VITE_API_URL"] = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
    os.environ["VITE_WS_URL"] = f"ws://{BACKEND_HOST}:{BACKEND_PORT}"
    
    # Ajouter src au path Python
    src_path = str(PROJECT_ROOT / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

def start_backend():
    """Lance le backend FastAPI"""
    log("API", f"Démarrage sur {BACKEND_HOST}:{BACKEND_PORT}")
    uvicorn.run(
        "backend_bridge_api:app",
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        reload=False,
        log_level="info"
    )

def wait_for_health(timeout=30):
    """Attend que l'API soit prête"""
    log("HEALTH", "Attente healthcheck...")
    url = f"http://{BACKEND_HOST}:{BACKEND_PORT}/health"
    
    for _ in range(timeout):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    log("HEALTH", "API prête !")
                    return True
        except:
            pass
        time.sleep(1)
    
    log("ERROR", "Healthcheck échoué")
    return False

def start_ui():
    """Lance l'interface React"""
    log("UI", "Démarrage interface React...")
    
    # Vérifier que le dossier frontend existe
    if not FRONTEND_DIR.exists():
        log("ERROR", f"Dossier frontend non trouvé: {FRONTEND_DIR}")
        return None
    
    # Vérifier package.json
    package_json = FRONTEND_DIR / "package.json"
    if not package_json.exists():
        log("ERROR", f"package.json non trouvé dans {FRONTEND_DIR}")
        return None
    
    env = os.environ.copy()
    env["VITE_API_URL"] = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
    env["VITE_WS_URL"] = f"ws://{BACKEND_HOST}:{BACKEND_PORT}"
    
    # Utiliser le chemin complet de npm sur Windows
    npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
    cmd = [npm_cmd, "run", "dev"]
    
    try:
        return subprocess.Popen(
            cmd,
            cwd=str(FRONTEND_DIR),
            env=env,
            shell=True  # Utiliser shell pour Windows
        )
    except FileNotFoundError as e:
        log("ERROR", f"npm non trouvé: {e}")
        log("ERROR", "Installer Node.js ou ajouter npm au PATH")
        return None

def main():
    """Point d'entrée principal"""
    print("🌊 CHNeoWave - Lancement complet")
    print("=" * 50)
    
    global BACKEND_PORT, UI_PORT
    
    # Configuration
    setup_environment()
    
    # Vérification ports
    if port_in_use(BACKEND_HOST, BACKEND_PORT):
        BACKEND_PORT = find_free_port(BACKEND_HOST, BACKEND_PORT)
        log("MAIN", f"Nouveau port API: {BACKEND_PORT}")
    
    if port_in_use(UI_HOST, UI_PORT):
        UI_PORT = find_free_port(UI_HOST, UI_PORT)
        log("MAIN", f"Nouveau port UI: {UI_PORT}")
    
    try:
        # Démarrage backend
        api_thread = threading.Thread(target=start_backend, daemon=True)
        api_thread.start()
        
        # Attente healthcheck
        if not wait_for_health():
            log("ERROR", "Backend non opérationnel")
            return False
        
        # Démarrage UI
        ui_process = start_ui()
        if not ui_process:
            log("ERROR", "Échec démarrage interface React")
            log("ERROR", "Vérifier Node.js et npm installation")
            return False
        
        # Attente UI
        time.sleep(5)
        
        # Ouverture navigateur
        url = f"http://{UI_HOST}:{UI_PORT}"
        log("MAIN", f"Ouverture: {url}")
        try:
            webbrowser.open(url)
        except:
            pass
        
        print("\n✅ CHNeoWave démarré !")
        print(f"🌐 Interface: http://{UI_HOST}:{UI_PORT}")
        print(f"📚 API: http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
        print("Ctrl+C pour arrêter\n")
        
        # Attente
        ui_process.wait()
        
    except KeyboardInterrupt:
        log("MAIN", "Arrêt demandé")
        if 'ui_process' in locals():
            ui_process.terminate()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
