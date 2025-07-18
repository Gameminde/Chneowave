#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Point d'entrée principal
Logiciel d'acquisition et d'analyse de houle pour laboratoires maritimes

Version 3.0.0 - Architecture refactorisée
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def main():
    """Point d'entrée principal de CHNeoWave"""
    try:
        # Import de l'interface graphique
        from hrneowave.gui.main import main as gui_main
        
        print("🌊 CHNeoWave v3.0.0 - Laboratoire Maritime")
        print("Démarrage de l'interface graphique...")
        
        # Lancer l'interface
        return gui_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Vérifiez que tous les modules sont installés.")
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())