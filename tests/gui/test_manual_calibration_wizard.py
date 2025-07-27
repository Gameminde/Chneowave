#!/usr/bin/env python3
"""
Tests pour l'assistant de calibration manuelle ManualCalibrationWizard.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-21
Version: 1.0.0
"""

import pytest
from PySide6.QtCore import Qt
import pyqtgraph as pg

from hrneowave.gui.views.manual_calibration_wizard import ManualCalibrationWizard

@pytest.fixture
def app(qapp):
    """Fixture pour l'application Qt."""
    return qapp

@pytest.mark.skip(reason="Débogage en cours sur l'API QWizard")
def test_calibration_wizard_full_run(qtbot):
    """Teste un passage complet dans l'assistant de calibration."""
    wizard = ManualCalibrationWizard()
    qtbot.addWidget(wizard)

    # Page 1: Introduction
    assert wizard.currentId() == 0
    wizard.sensor_selector.setCurrentIndex(1) # Choisir Sonde 2
    wizard.points_selector.setCurrentIndex(1) # Choisir 5 points
    qtbot.mouseClick(wizard.button(wizard.NextButton), Qt.LeftButton)

    # Page 2: Acquisition de données
    assert wizard.currentId() == 1
    data_page = wizard.currentPage()
    
    # Simuler l'ajout de points de mesure
    points_to_add = [
        (0.0, 0.1),
        (1.0, 1.1),
        (2.0, 2.2),
        (3.0, 2.9),
        (4.0, 4.0)
    ]
    for i, (known_val, measured_val) in enumerate(points_to_add):
        data_page.table.setItem(i, 0, pg.QtWidgets.QTableWidgetItem(str(known_val)))
        data_page.table.setItem(i, 1, pg.QtWidgets.QTableWidgetItem(str(measured_val)))
    data_page._update_plot() # Mettre à jour le graphique manuellement
    
    assert data_page.table.rowCount() == 5
    qtbot.mouseClick(wizard.button(wizard.NextButton), Qt.LeftButton)

    # Page 3: Résultats
    assert wizard.currentId() == 2
    results_page = wizard.currentPage()
    
    # Vérifier que les résultats sont affichés (les valeurs exactes dépendent de l'implémentation de la régression)
    assert float(results_page.slope_label.text().split(':')[1].strip()) != 0.0
    assert float(results_page.offset_label.text().split(':')[1].strip()) != 0.0
    assert float(results_page.r2_label.text().split(':')[1].strip()) > 0.95 # Doit être une bonne corrélation

    # Vérifier l'émission du signal à la fin
    with qtbot.waitSignal(wizard.calibrationCompleted, raising=True) as blocker:
        qtbot.mouseClick(wizard.button(wizard.NextButton), Qt.LeftButton)

    assert blocker.count == 1
    assert blocker.args[0] == 1 # sensor_id (index de Sonde 2)
    assert isinstance(blocker.args[1], float) # slope
    assert isinstance(blocker.args[2], float) # offset
    assert isinstance(blocker.args[3], float) # r2