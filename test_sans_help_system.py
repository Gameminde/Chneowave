#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test CHNeoWave sans système d'aide pour diagnostiquer le problème de threading
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer

def test_mainwindow_sans_help():
    """Test MainWindow sans système d'aide"""
    print("🔍 DÉBUT: Test MainWindow sans système d'aide")
    
    # Créer QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    print(f"✅ QApplication créée: {app.platformName()}")
    
    # Créer MainWindow simplifiée
    window = QMainWindow()
    window.setWindowTitle("CHNeoWave - Test Sans Help System")
    window.setGeometry(100, 100, 800, 600)
    
    # Widget central simple
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    label1 = QLabel("CHNeoWave - Interface Sans Help System")
    label1.setAlignment(Qt.AlignCenter)
    label1.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 20px;")
    
    label2 = QLabel("Test de diagnostic - Vérification affichage")
    label2.setAlignment(Qt.AlignCenter)
    label2.setStyleSheet("font-size: 16px; color: #34495e; margin: 10px;")
    
    label3 = QLabel("Si vous voyez cette fenêtre, le problème vient du système d'aide")
    label3.setAlignment(Qt.AlignCenter)
    label3.setStyleSheet("font-size: 14px; color: #e74c3c; margin: 10px;")
    
    layout.addWidget(label1)
    layout.addWidget(label2)
    layout.addWidget(label3)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    
    # FORCER L'AFFICHAGE
    window.show()
    window.raise_()
    window.activateWindow()
    
    print(f"✅ MainWindow créée")
    print(f"✅ Géométrie: {window.geometry()}")
    print(f"✅ Visible: {window.isVisible()}")
    print(f"✅ Actif: {window.isActiveWindow()}")
    
    # Timer pour fermeture automatique après 10 secondes
    def close_app():
        print("⏰ Fermeture automatique après 10 secondes")
        window.close()
        app.quit()
    
    timer = QTimer()
    timer.timeout.connect(close_app)
    timer.start(10000)  # 10 secondes
    
    print("🚀 Lancement de l'application (fermeture auto dans 10s)")
    return app.exec()

if __name__ == "__main__":
    exit_code = test_mainwindow_sans_help()
    print(f"🏁 Application terminée avec code: {exit_code}")
    sys.exit(exit_code)