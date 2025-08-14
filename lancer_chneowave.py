#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur Principal CHNeoWave
Point d'entrée simplifié pour l'utilisation quotidienne

Usage:
    python lancer_chneowave.py

Auteur: Architecte Logiciel en Chef
Version: 1.1.0
"""

import sys
import os
from pathlib import Path

def main():
    """Point d'entrée principal simplifié"""
    print("🚀 CHNeoWave - Laboratoire Maritime")
    print("=" * 50)
    
    try:
        # Ajouter le chemin du projet
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # Import des modules Qt
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave")
            app.setApplicationVersion("1.1.0")
            app.setOrganizationName("Laboratoire Maritime")
        
        print("✅ Application Qt initialisée")
        
        # Import et création de l'interface principale
        from hrneowave.gui.main_window import MainWindow
        
        # Créer la fenêtre principale
        window = MainWindow()
        print("✅ Interface CHNeoWave créée")
        
        # Afficher l'interface
        window.show()
        window.raise_()
        window.activateWindow()
        
        print("✅ Interface affichée")
        print(f"✅ Statut: {window.isVisible() and 'Visible' or 'Masquée'}")
        print("🎉 CHNeoWave est opérationnel !")
        print("")
        print("📋 Modules disponibles:")
        print("   🏠 Accueil et gestion de projets")
        print("   📊 Tableau de bord maritime")
        print("   📡 Acquisition de données")
        print("   ⚙️  Calibration des capteurs")
        print("   📈 Analyse des données")
        print("   📄 Génération de rapports")
        print("")
        print("🌊 Interface maritime prête à l'utilisation")
        
        # Lancer la boucle d'événements
        return app.exec()
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que PySide6 est installé: pip install PySide6")
        return 1
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)