#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour isoler le problème MainWindow
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_simple_main_window():
    """Test simple de MainWindow"""
    print("🚀 TEST SIMPLE MAINWINDOW")
    print("=" * 40)
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Simple Test")
        
        print("✅ QApplication créé")
        
        # Test import MainWindow
        print("🔄 Import MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importé")
        
        # Test création MainWindow
        print("🔄 Création MainWindow...")
        main_window = MainWindow()
        print("✅ MainWindow créée")
        
        # Test affichage
        print("🔄 Affichage MainWindow...")
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        visible = main_window.isVisible()
        print(f"✅ MainWindow visible: {visible}")
        
        if visible:
            print("🎉 SUCCÈS: MainWindow visible!")
            
            # Maintenir ouvert 5 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(5000)
            
            print("🔄 Maintien ouvert 5 secondes...")
            exit_code = app.exec()
            print(f"✅ Test terminé (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: MainWindow non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_simple_main_window() else 1)
