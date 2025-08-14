#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Application principale FINALE
Version: 1.1.0
"""

import sys
import logging
import traceback
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('src/hrneowave/chneowave_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('chneowave')

def main():
    """Point d'entrée principal de l'application"""
    try:
        print("🚀 Lancement de CHNeoWave v1.1.0")
        print("=" * 50)
        
        # Ajouter le chemin du projet
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        print("📋 ÉTAPE 1: Création QApplication")
        print("-" * 30)
        
        # Import et création de QApplication
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave")
            app.setApplicationVersion("1.1.0")
            app.setOrganizationName("CHNeoWave")
        
        print("✅ QApplication créé")
        
        print("📋 ÉTAPE 2: Application du thème")
        print("-" * 30)
        
        # Application du thème (simplifiée)
        try:
            from hrneowave.gui.styles.theme_manager import ThemeManager
            theme_manager = ThemeManager(app=app)
            theme_manager.apply_theme('maritime_modern')
            print("✅ Thème 'maritime_modern' appliqué avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'application du thème: {e}")
            print("⚠️ Continuation sans thème...")
        
        print("✅ Thème maritime appliqué")
        
        print("📋 ÉTAPE 3: Création MainWindow")
        print("-" * 30)
        
        # Import et création de MainWindow
        print("🔄 Import de MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importé")
        
        print("🔄 Création de l'instance MainWindow...")
        main_window = MainWindow()
        print("✅ MainWindow créée")
        
        print("📋 ÉTAPE 4: Configuration de l'affichage")
        print("-" * 30)
        
        # Configuration de l'affichage
        main_window.setWindowTitle("CHNeoWave - Interface Maritime")
        main_window.resize(1200, 800)
        
        # Centrer la fenêtre
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = main_window.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        main_window.move(x, y)
        
        print("✅ Fenêtre configurée et centrée")
        
        print("📋 ÉTAPE 5: Affichage avec boucle d'événements")
        print("-" * 30)
        
        # Utiliser la méthode show_and_exec
        print("🔄 Utilisation de show_and_exec...")
        exit_code = main_window.show_and_exec()
        
        print(f"✅ Application terminée (code: {exit_code})")
        return exit_code
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de MainWindow: {e}")
        print("🔍 Traceback complet:")
        traceback.print_exc()
        print(f"❌ ERREUR CRITIQUE: {e}")
        print("🔍 Traceback complet:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
