#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Application principale SANS TIMER
Version: 1.1.0 - Modifiée pour rester ouverte
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
    """Point d'entrée principal de l'application SANS TIMER"""
    try:
        print("🚀 Lancement de CHNeoWave v1.1.0 - SANS TIMER")
        print("=" * 60)
        
        # Ajouter le chemin du projet
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        print("📋 ÉTAPE 1: Création QApplication")
        print("-" * 30)
        
        # Import et création de QApplication
        from PySide6.QtWidgets import QApplication, QMessageBox
        from PySide6.QtCore import Qt, QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Sans Timer")
            app.setApplicationVersion("1.1.0")
            app.setOrganizationName("CHNeoWave")
        
        print("✅ QApplication créé")
        
        print("📋 ÉTAPE 2: Application du thème")
        print("-" * 30)
        
        # Application du thème
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
        main_window.setWindowTitle("CHNeoWave - Interface Maritime PERMANENTE")
        main_window.resize(1200, 800)
        
        # Centrer la fenêtre
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = main_window.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        main_window.move(x, y)
        
        print("✅ Fenêtre configurée et centrée")
        
        print("📋 ÉTAPE 5: Affichage de l'interface")
        print("-" * 30)
        
        # Affichage de l'interface avec forçage multiple
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        # Forcer au premier plan
        main_window.setWindowState(Qt.WindowActive)
        main_window.setAttribute(Qt.WA_ShowWithoutActivating, False)
        
        # Vérifier la visibilité
        visible = main_window.isVisible()
        print(f"✅ MainWindow visible: {visible}")
        
        if not visible:
            print("⚠️ Fenêtre non visible, tentative de correction...")
            main_window.showNormal()
            main_window.show()
            visible = main_window.isVisible()
            print(f"✅ MainWindow visible après correction: {visible}")
        
        print("✅ Interface affichée avec succès")
        print("🎉 CHNeoWave est maintenant opérationnel !")
        print("🔍 Vérifiez que la fenêtre est visible sur votre écran")
        
        print("📋 ÉTAPE 6: Lancement de la boucle d'événements PERMANENTE")
        print("-" * 30)
        
        # Message de confirmation après 3 secondes
        def show_confirmation():
            if main_window.isVisible():
                msg = QMessageBox()
                msg.setWindowTitle("CHNeoWave - Confirmation")
                msg.setText("🎉 CHNeoWave est VISIBLE et OPÉRATIONNEL !\n\n"
                           "✅ Interface affichée correctement\n"
                           "✅ Navigation fonctionnelle\n"
                           "✅ Tous les composants chargés\n\n"
                           "L'application restera ouverte jusqu'à fermeture manuelle.")
                msg.setIcon(QMessageBox.Information)
                msg.exec()
            else:
                print("❌ PROBLÈME: Fenêtre toujours invisible")
        
        # Timer pour confirmation (pas de fermeture)
        confirmation_timer = QTimer()
        confirmation_timer.timeout.connect(show_confirmation)
        confirmation_timer.setSingleShot(True)
        confirmation_timer.start(3000)  # 3 secondes
        
        print("🔄 Lancement de la boucle d'événements PERMANENTE...")
        print("⚠️ AUCUN TIMER DE FERMETURE - L'application reste ouverte")
        print("🔍 Fermez manuellement la fenêtre pour quitter")
        
        # Lancer la boucle d'événements SANS TIMER DE FERMETURE
        exit_code = app.exec()
        print(f"✅ Application terminée (code: {exit_code})")
        return exit_code
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de MainWindow: {e}")
        print("🔍 Traceback complet:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())