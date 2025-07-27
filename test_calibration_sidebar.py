#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du widget MaritimeCalibrationSidebar
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from PySide6.QtCore import Qt
except ImportError:
    print("❌ PySide6 non disponible. Installation requise: pip install PySide6")
    sys.exit(1)

# Import direct du module contenant MaritimeCalibrationSidebar
try:
    from hrneowave.gui.views.calibration_view import MaritimeCalibrationSidebar
except ImportError as e:
    print(f"❌ Erreur d'import du widget MaritimeCalibrationSidebar: {e}")
    sys.exit(1)

class TestWindow(QMainWindow):
    """Fenêtre de test pour le widget MaritimeCalibrationSidebar"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test MaritimeCalibrationSidebar")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Création et ajout du widget MaritimeCalibrationSidebar
        try:
            self.sidebar = MaritimeCalibrationSidebar()
            main_layout.addWidget(self.sidebar)
            print("✅ MaritimeCalibrationSidebar créé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de la création du widget: {e}")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()