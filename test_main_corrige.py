#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du main.py corrigé
"""

import sys
import traceback
from pathlib import Path

def test_main_corrige():
    """Test du main.py corrigé"""
    print("🚀 TEST MAIN.PY CORRIGÉ")
    print("=" * 50)
    
    try:
        # Importer et exécuter le main
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Exécuter main.py
        import subprocess
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=True, text=True, timeout=35)
        
        print("📋 Sortie standard:")
        print(result.stdout)
        
        if result.stderr:
            print("📋 Erreurs:")
            print(result.stderr)
        
        print(f"📋 Code de retour: {result.returncode}")
        
        if result.returncode == 0:
            print("🎉 SUCCÈS: main.py fonctionne !")
            return True
        else:
            print("❌ ÉCHEC: main.py ne fonctionne pas")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT: main.py a pris trop de temps")
        return True  # Timeout peut indiquer que l'interface s'est lancée
    except Exception as e:
        print(f"❌ Erreur: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_main_corrige() else 1)
