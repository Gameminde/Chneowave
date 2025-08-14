#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet MainWindow avec boucle d'événements
"""

import sys
import traceback
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_mainwindow_complete():
    """Test complet MainWindow"""
    print("🚀 TEST MAINWINDOW COMPLET")
    print("=" * 50)
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Complete Test")
        
        print("✅ QApplication créé")
        
        # Test import MainWindow
        print("🔄 Test import MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importé")
        
        # Test création MainWindow
        print("🔄 Test création MainWindow...")
        main_window = MainWindow()
        print("✅ MainWindow créée")
        
        # Configuration
        main_window.setWindowTitle("CHNeoWave - Test Complet")
        main_window.resize(1200, 800)
        
        # Centrer la fenêtre
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = main_window.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        main_window.move(x, y)
        
        print("✅ MainWindow configurée et centrée")
        
        # Test affichage
        print("🔄 Test affichage MainWindow...")
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        visible = main_window.isVisible()
        print(f"✅ MainWindow visible: {visible}")
        
        if visible:
            print("🎉 SUCCÈS: MainWindow visible, test boucle d'événements...")
            
            # Timer pour fermer après 15 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(15000)
            
            print("🔄 Lancement boucle d'événements (15 secondes)...")
            print("🔍 Vérifiez que la fenêtre CHNeoWave est visible sur votre écran")
            
            exit_code = app.exec()
            print(f"✅ Boucle d'événements terminée (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: MainWindow non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_mainwindow_complete() else 1)
