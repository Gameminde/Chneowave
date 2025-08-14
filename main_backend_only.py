#!/usr/bin/env python3
"""
CHNeoWave - Lancement backend uniquement
Point d'entrée simple pour tester le backend seul
"""

import os
import sys
from pathlib import Path
import webbrowser

# Ajouter src au path
PROJECT_ROOT = Path(__file__).parent
src_path = str(PROJECT_ROOT / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Configuration environnement
os.environ["BACKEND_MODE"] = "real"
os.environ["DEBUG"] = "1"

def main():
    print("🌊 CHNeoWave - Backend uniquement")
    print("=" * 50)
    print("🚀 Démarrage backend sur http://127.0.0.1:3001")
    print("📚 Documentation: http://127.0.0.1:3001/docs")
    print("🔗 WebSocket: ws://127.0.0.1:3001/ws/realtime")
    print("=" * 50)
    
    # Ouverture automatique documentation
    try:
        webbrowser.open("http://127.0.0.1:3001/docs")
    except:
        pass
    
    # Lancement backend
    import uvicorn
    uvicorn.run(
        "backend_bridge_api:app",
        host="127.0.0.1",
        port=3001,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
