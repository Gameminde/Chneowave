#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow CHNeoWave ultra-simple - sans vues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer

def test_mainwindow_ultra_simple():
    """Test MainWindow CHNeoWave sans aucune vue"""
    print("🔍 DÉBUT: Test MainWindow CHNeoWave ultra-simple")
    
    # Créer QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    print(f"✅ QApplication créée: {app.platformName()}")
    
    # Créer MainWindow CHNeoWave de base
    try:
        # Importer juste la classe de base
        from PySide6.QtWidgets import QMainWindow
        
        # Créer une MainWindow basique qui hérite de QMainWindow
        class SimpleMainWindow(QMainWindow):
            def __init__(self, parent=None):
                super().__init__(parent)
                print("🔍 SimpleMainWindow.__init__ - Début")
                
                self.setWindowTitle("CHNeoWave - Test Ultra Simple")
                self.setGeometry(100, 100, 800, 600)
                
                # Widget central simple
                central_widget = QWidget()
                layout = QVBoxLayout()
                
                label = QLabel("CHNeoWave - MainWindow Ultra Simple")
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 20px;")
                
                layout.addWidget(label)
                central_widget.setLayout(layout)
                self.setCentralWidget(central_widget)
                
                print("🔍 SimpleMainWindow.__init__ - Terminé")
        
        # Créer l'instance
        window = SimpleMainWindow()
        print("✅ SimpleMainWindow créée")
        
        # FORCER L'AFFICHAGE
        window.show()
        window.raise_()
        window.activateWindow()
        
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Actif: {window.isActiveWindow()}")
        
        # Vérifier après 1 seconde
        def check_and_close():
            print(f"🔍 Vérification après 1s:")
            print(f"   - Visible: {window.isVisible()}")
            print(f"   - Géométrie: {window.geometry()}")
            
            if window.isVisible():
                print("✅ SUCCESS: MainWindow ultra-simple s'affiche parfaitement !")
                print("➡️  Le problème vient des vues ou du ViewManager")
            else:
                print("❌ ÉCHEC: Même MainWindow ultra-simple ne s'affiche pas")
            
            # Fermer l'application
            window.close()
            app.quit()
        
        timer = QTimer()
        timer.timeout.connect(check_and_close)
        timer.start(1000)  # 1 seconde
        
        print("🚀 Lancement MainWindow ultra-simple")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_mainwindow_ultra_simple()
    print(f"🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)