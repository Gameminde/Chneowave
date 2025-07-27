#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la CalibrationView unifiée
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication
from hrneowave.gui.views.calibration_view import CalibrationView

def test_calibration_view():
    """Test de la vue de calibration"""
    app = QApplication(sys.argv)
    
    # Créer la vue de calibration
    calibration_view = CalibrationView()
    calibration_view.setWindowTitle("CHNeoWave - Test Calibration View")
    calibration_view.resize(1200, 800)
    calibration_view.show()
    
    print("Vue de calibration lancée avec succès!")
    print(f"Étape actuelle: {calibration_view.current_step}")
    print(f"Nombre de capteurs: {calibration_view.sensor_count}")
    print(f"Points de mesure: {calibration_view.measurement_points}")
    
    # Lancer l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_calibration_view()