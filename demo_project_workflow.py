#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du workflow de création de projet CHNeoWave
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

def main():
    """Point d'entrée principal de la démonstration"""
    app = QApplication(sys.argv)
    
    try:
        # Import des modules après configuration du path
        from hrneowave.gui.main_window import MainWindow
        
        # Créer et afficher la fenêtre principale
        window = MainWindow()
        window.show()
        
        # Message de bienvenue
        print("=" * 60)
        print("CHNeoWave - Démonstration du workflow de création de projet")
        print("=" * 60)
        print("Instructions:")
        print("1. Remplissez le formulaire de création de projet")
        print("2. Cliquez sur 'Créer le projet'")
        print("3. Observez l'activation des boutons d'acquisition")
        print("4. Le titre de la fenêtre se met à jour avec les métadonnées")
        print("=" * 60)
        
        # Lancer l'application
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"Erreur d'import: {e}")
        print("Vérifiez que tous les modules sont disponibles.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()