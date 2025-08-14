#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow Isolation - Phase 2 du diagnostic
Test MainWindow CHNeoWave en isolation complète
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer

def test_mainwindow_isolation():
    """Test MainWindow CHNeoWave en isolation complète"""
    print("=== TEST MAINWINDOW ISOLATION ===")
    
    app = QApplication(sys.argv)
    print(f"✅ QApplication créée sur plateforme: {app.platformName()}")
    
    try:
        # Import MainWindow CHNeoWave
        print("🔍 Import MainWindow CHNeoWave...")
        from hrneowave.gui.main_window import MainWindow
        print("✅ Import MainWindow réussi")
        
        # Création MainWindow
        print("🔍 Création MainWindow...")
        window = MainWindow()
        print("✅ MainWindow créée")
        
        # Vérifications détaillées
        print(f"✅ Titre: {window.windowTitle()}")
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ Taille minimale: {window.minimumSize()}")
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Widget central: {window.centralWidget()}")
        print(f"✅ Actif: {window.isActiveWindow()}")
        
        # FORCER L'AFFICHAGE MAXIMUM
        print("🔍 Forçage affichage...")
        window.show()
        window.raise_()
        window.activateWindow()
        window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        
        # Vérifications post-affichage
        print(f"✅ Visible après show(): {window.isVisible()}")
        print(f"✅ Actif après activation: {window.isActiveWindow()}")
        print(f"✅ État fenêtre: {window.windowState()}")
        
        # Capture d'écran pour diagnostic
        try:
            screen = app.primaryScreen()
            screenshot = screen.grabWindow(0)
            screenshot.save("mainwindow_isolation_screenshot.png")
            print("✅ Capture d'écran sauvegardée: mainwindow_isolation_screenshot.png")
        except Exception as e:
            print(f"⚠️ Capture d'écran échouée: {e}")
        
        # Timer pour fermer automatiquement
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(5000)  # 5 secondes
        
        print("✅ Test MainWindow isolation lancé - Fenêtre visible pendant 5 secondes")
        return app.exec()
        
    except Exception as e:
        print(f"❌ ERREUR lors du test MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    result = test_mainwindow_isolation()
    print(f"✅ Test MainWindow isolation terminé avec code: {result}")
    sys.exit(result)