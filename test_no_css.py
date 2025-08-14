#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test CHNeoWave sans CSS pour isoler le problème
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_mainwindow_no_css():
    """Test MainWindow sans CSS"""
    print("=== TEST MAINWINDOW SANS CSS ===")
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        from hrneowave.core.logging_config import setup_logging
        
        # Configuration logging
        setup_logging()
        print("✅ Logging configuré")
        
        # Création QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("CHNeoWave Sans CSS")
        print("✅ QApplication créée")
        
        # NE PAS appliquer de thème CSS
        print("⚠️ Pas de thème CSS appliqué (test sans styles)")
        
        # Import MainWindow
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importée")
        
        # Création MainWindow
        print("Création de MainWindow...")
        main_window = MainWindow()
        print("✅ MainWindow créée avec succès!")
        
        # Configuration basique
        main_window.setWindowTitle("CHNeoWave - Test Sans CSS")
        main_window.setGeometry(200, 200, 1000, 700)
        
        # Affichage
        print("Affichage de MainWindow...")
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        # Vérifications
        print(f"✅ MainWindow visible: {main_window.isVisible()}")
        print(f"✅ Taille: {main_window.size()}")
        print(f"✅ Position: {main_window.pos()}")
        print(f"✅ Titre: {main_window.windowTitle()}")
        
        if main_window.isVisible():
            print("\n🎉 SUCCÈS! MainWindow s'affiche sans CSS")
        else:
            print("\n⚠️ MainWindow créée mais pas visible")
        
        # Timer pour fermer après 8 secondes
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(8000)
        
        print("\nInterface affichée pendant 8 secondes...")
        print("(L'interface peut paraître basique sans CSS, c'est normal)")
        
        exit_code = app.exec()
        print(f"\n✅ Application fermée avec code: {exit_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mainwindow_with_minimal_css():
    """Test MainWindow avec CSS minimal"""
    print("\n=== TEST MAINWINDOW AVEC CSS MINIMAL ===")
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        
        # Réutiliser l'application existante ou en créer une nouvelle
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave CSS Minimal")
        
        print("✅ QApplication prête")
        
        # CSS minimal et sûr
        minimal_css = """
        QMainWindow {
            background-color: #f0f8ff;
        }
        QLabel {
            color: #1565C0;
            font-size: 12px;
        }
        QPushButton {
            background-color: #1976D2;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1565C0;
        }
        """
        
        app.setStyleSheet(minimal_css)
        print("✅ CSS minimal appliqué")
        
        # Import et création MainWindow
        from hrneowave.gui.main_window import MainWindow
        
        main_window = MainWindow()
        print("✅ MainWindow créée avec CSS minimal")
        
        main_window.setWindowTitle("CHNeoWave - Test CSS Minimal")
        main_window.setGeometry(250, 250, 1000, 700)
        
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        print(f"✅ MainWindow visible: {main_window.isVisible()}")
        
        if main_window.isVisible():
            print("\n🎉 SUCCÈS! MainWindow s'affiche avec CSS minimal")
        
        # Timer pour fermer après 8 secondes
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(8000)
        
        print("\nInterface avec CSS minimal affichée pendant 8 secondes...")
        
        exit_code = app.exec()
        print(f"\n✅ Application fermée avec code: {exit_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR CSS minimal: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("DIAGNOSTIC MAINWINDOW SANS/AVEC CSS")
    print("====================================")
    
    # Test 1: Sans CSS
    success_no_css = test_mainwindow_no_css()
    
    if success_no_css:
        print("\n✅ Test sans CSS réussi")
        
        # Petite pause
        import time
        time.sleep(2)
        
        # Test 2: Avec CSS minimal
        success_minimal_css = test_mainwindow_with_minimal_css()
        
        if success_minimal_css:
            print("\n🎉 TOUS LES TESTS RÉUSSIS!")
            print("L'interface CHNeoWave fonctionne.")
            print("Le problème vient des styles CSS complexes.")
            return 0
        else:
            print("\n⚠️ CSS minimal pose problème")
            return 1
    else:
        print("\n❌ MainWindow ne peut pas se créer")
        return 1

if __name__ == "__main__":
    sys.exit(main())