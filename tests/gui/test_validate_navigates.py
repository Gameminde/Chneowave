# -*- coding: utf-8 -*-
"""
Test pour vérifier que le bouton Valider navigue correctement
vers la vue suivante après création d'un projet.
"""

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

# Mock du hardware avant l'import
with patch('hrneowave.hardware.manager.HardwareManager') as mock_hw:
    mock_hw.return_value = MagicMock()
    mock_hw.return_value.is_initialized = True
    from hrneowave.gui.main_window import MainWindow

@pytest.fixture
def app(qtbot):
    """Crée une instance de l'application Qt et la fenêtre principale."""
    if not QApplication.instance():
        qapp = QApplication([])
    else:
        qapp = QApplication.instance()

    with patch('hrneowave.hardware.manager.HardwareManager') as mock_hw_inner:
        mock_hw_inner.return_value = MagicMock()
        mock_hw_inner.return_value.is_connected.return_value = False
        window = MainWindow()
        qtbot.addWidget(window)
        window.show()
        qtbot.waitForWindowShown(window)
        yield window
        window.close()

class TestDashboardNavigation:
    """Tests pour la navigation depuis le Dashboard en utilisant MainWindow."""

    def test_button_emits_signal(self, qtbot, app):
        """Vérifie que le bouton 'Démarrer une Acquisition' émet le bon signal."""
        main_window = app
        dashboard_view = main_window.dashboard_view

        with qtbot.waitSignal(dashboard_view.acquisitionRequested, raising=True, timeout=1000):
            qtbot.mouseClick(dashboard_view.start_calibration_button, Qt.LeftButton)

    def test_controller_navigates_to_acquisition(self, qtbot, app):
        """Vérifie que le contrôleur navigue vers la vue d'acquisition."""
        main_window = app
        controller = main_window.main_controller
        view_manager = main_window.view_manager
        
        controller.navigate_to_acquisition()

        assert view_manager.current_view == "acquisition"

    def test_integration_dashboard_navigates_to_acquisition(self, qtbot, app):
        """Test d'intégration complet : clic bouton -> contrôleur -> navigation."""
        main_window = app
        view_manager = main_window.view_manager
        dashboard_view = main_window.dashboard_view

        view_manager.change_view("dashboard")
        qtbot.waitUntil(lambda: view_manager.current_view == "dashboard")

        qtbot.mouseClick(dashboard_view.start_calibration_button, Qt.LeftButton)

        qtbot.waitUntil(lambda: view_manager.current_view == "acquisition", timeout=2000)
        assert view_manager.current_view == "acquisition"