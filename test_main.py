#!/usr/bin/env python3
"""
Test du point d'entrée CHNeoWave avec diagnostics améliorés
"""

import os
import subprocess
import sys
from pathlib import Path

def test_environment():
    """Teste l'environnement avant lancement"""
    print("🔍 Diagnostic environnement CHNeoWave")
    print("=" * 50)
    
    # Test 1: Structure projet
    project_root = Path(__file__).parent
    frontend_dir = project_root / "i-prototype-tailwind"
    backend_file = project_root / "backend_bridge_api.py"
    
    print(f"📁 Projet: {project_root}")
    print(f"📁 Frontend: {frontend_dir}")
    print(f"📄 Backend: {backend_file}")
    
    if not backend_file.exists():
        print("❌ backend_bridge_api.py non trouvé")
        return False
    else:
        print("✅ backend_bridge_api.py trouvé")
    
    if not frontend_dir.exists():
        print("❌ Dossier i-prototype-tailwind non trouvé")
        return False
    else:
        print("✅ Dossier i-prototype-tailwind trouvé")
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json non trouvé dans i-prototype-tailwind")
        return False
    else:
        print("✅ package.json trouvé")
    
    # Test 2: Node.js et npm
    print("\n🚀 Test Node.js/npm")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js non accessible")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Node.js non trouvé")
        return False
    
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm non accessible")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ npm non trouvé")
        return False
    
    # Test 3: Test npm dans le dossier frontend
    print(f"\n📦 Test npm dans {frontend_dir}")
    try:
        result = subprocess.run(
            ["npm", "list", "--depth=0"], 
            cwd=str(frontend_dir),
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if "node_modules" in (frontend_dir / "node_modules").name if (frontend_dir / "node_modules").exists() else "":
            print("✅ node_modules existe")
        else:
            print("⚠️ node_modules manquant - npm install requis")
        
    except Exception as e:
        print(f"⚠️ Erreur test npm: {e}")
    
    # Test 4: Python modules
    print("\n🐍 Test modules Python")
    try:
        import uvicorn
        print("✅ uvicorn disponible")
    except ImportError:
        print("❌ uvicorn manquant: pip install uvicorn")
        return False
    
    try:
        import requests
        print("✅ requests disponible")
    except ImportError:
        print("❌ requests manquant: pip install requests")
        return False
    
    try:
        import fastapi
        print("✅ fastapi disponible")
    except ImportError:
        print("❌ fastapi manquant: pip install fastapi")
        return False
    
    print("\n✅ Environnement validé !")
    return True

def test_npm_run_dev():
    """Teste spécifiquement npm run dev"""
    print("\n🧪 Test npm run dev")
    
    frontend_dir = Path(__file__).parent / "i-prototype-tailwind"
    
    try:
        # Test avec timeout court pour voir si la commande se lance
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=str(frontend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("🚀 Processus npm run dev lancé...")
        
        # Attendre 3 secondes pour voir si ça démarre
        try:
            stdout, stderr = process.communicate(timeout=3)
            print(f"Stdout: {stdout}")
            print(f"Stderr: {stderr}")
        except subprocess.TimeoutExpired:
            print("✅ npm run dev se lance (timeout normal)")
            process.terminate()
            process.wait()
            return True
        
        if process.returncode == 0:
            print("✅ npm run dev OK")
            return True
        else:
            print(f"❌ npm run dev échec: code {process.returncode}")
            return False
        
    except FileNotFoundError as e:
        print(f"❌ npm non trouvé: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur npm run dev: {e}")
        return False

if __name__ == "__main__":
    print("🌊 CHNeoWave - Diagnostic d'environnement")
    
    if test_environment():
        print("\n" + "="*50)
        test_npm_run_dev()
        print("\n✅ Diagnostic terminé")
        print("\n🚀 Si tout est OK, lancer: python main_unified.py")
    else:
        print("\n❌ Problèmes détectés dans l'environnement")
        print("🔧 Corriger les erreurs ci-dessus avant de continuer")
        sys.exit(1)
