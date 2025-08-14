#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de lancement CHNeoWave avec correction de visibilité
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_launch():
    """Test de lancement avec correction de visibilité"""
    print("🚀 TEST LANCEMENT CHNEOWAVE")
    print("=" * 40)
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, QTimer
        from hrneowave.gui.main_window import MainWindow
        from hrneowave.gui.styles.theme_manager import ThemeManager
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Test")
            app.setQuitOnLastWindowClosed(True)
        
        # Appliquer le thème
        theme_manager = ThemeManager(app)
        theme_manager.apply_theme('maritime_modern')
        print("✅ Thème appliqué")
        
        # Créer MainWindow
        main_window = MainWindow()
        print("✅ MainWindow créée")
        
        # Configuration de la fenêtre
        main_window.setWindowTitle("CHNeoWave Test")
        main_window.resize(1200, 800)
        
        # Centrer la fenêtre
        screen_geometry = app.primaryScreen().geometry()
        window_geometry = main_window.geometry()
        center_point = screen_geometry.center() - window_geometry.center()
        main_window.move(center_point)
        
        # Séquence d'affichage robuste
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        main_window.setWindowState(Qt.WindowActive)
        
        print("✅ Fenêtre affichée et configurée")
        
        # Vérifications
        visible = main_window.isVisible()
        active = main_window.isActiveWindow()
        
        print(f"✅ Visible: {visible}")
        print(f"✅ Active: {active}")
        print(f"✅ Position: {main_window.pos()}")
        print(f"✅ Taille: {main_window.size()}")
        
        if visible:
            print("🎉 SUCCÈS: Interface visible!")
            
            # Maintenir ouvert 10 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(10000)
            
            print("🔄 Maintien ouvert 10 secondes...")
            exit_code = app.exec()
            print(f"✅ Test terminé (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: Interface non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_launch() else 1)
