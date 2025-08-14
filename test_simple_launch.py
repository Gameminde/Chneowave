#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test simple pour CHNeoWave
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer

def test_simple_launch():
    """Test de lancement simple"""
    print("🧪 Test de lancement simple CHNeoWave")
    
    app = QApplication(sys.argv)
    
    # Fenêtre simple
    window = QMainWindow()
    window.setWindowTitle("CHNeoWave - Test Simple")
    window.setGeometry(200, 200, 600, 400)
    
    # Widget central
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    # Label
    label = QLabel("CHNeoWave - Test de Lancement")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)
    
    window.setCentralWidget(central_widget)
    
    # Affichage
    window.show()
    window.raise_()
    window.activateWindow()
    
    print(f"✅ Fenêtre créée: Visible={window.isVisible()}")
    
    # Timer pour fermer
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(3000)
    
    print("🔄 Démarrage boucle d'événements...")
    exit_code = app.exec()
    print(f"✅ Test terminé (code: {exit_code})")
    return exit_code

if __name__ == "__main__":
    exit(test_simple_launch())
