#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test pour le widget MaritimeCalibrationSidebar
"""

import sys
import os

# Ajouter le chemin source au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from hrneowave.gui.views.calibration_view import MaritimeCalibrationSidebar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test MaritimeCalibrationSidebar")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Créer et ajouter le sidebar
        self.sidebar = MaritimeCalibrationSidebar()
        layout.addWidget(self.sidebar)

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()