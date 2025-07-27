#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test end-to-end du workflow complet CHNeoWave
Mission: Interface Unifiée & Workflow Complet

Validation du parcours: dashboard → acquisition → analysis
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtTest import QTest

# Ajouter le chemin src pour les imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock du hardware avant l'import
with patch('hrneowave.hardware.manager.HardwareManager') as mock_hw:
    mock_hw.return_value = MagicMock()
    mock_hw.return_value.is_initialized = True
    
    from hrneowave.gui.main_window import MainWindow
    from hrneowave.gui.view_manager import ViewManager
    from hrneowave.gui.controllers.main_controller import MainController


class TestWorkflowComplete:
    """Tests du workflow complet de l'interface unifiée"""
    
    @pytest.fixture
    def app(self):
        """Fixture pour l'application Qt"""
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        yield app
        
    @pytest.fixture
    def main_window(self, app, qtbot):
        """Fixture pour la fenêtre principale"""
        window = MainWindow()
        window.show()
        qtbot.add_widget(window)
        yield window
        window.close()
        
    def test_workflow_navigation_complete(self, main_window, qtbot):
        """
        Test du workflow complet: dashboard → acquisition → analysis
        """
        with patch('hrneowave.hardware.manager.HardwareManager') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_initialized = True
            
            print("\n[TEST] Démarrage test workflow complet")
            
            vm = main_window.view_manager
            assert vm is not None, "ViewManager doit être disponible"
            
            qtbot.wait_for_window_shown(main_window)
            
            print(f"[TEST] Vue initiale: {vm.current_view}")
            assert vm.current_view == "welcome", f"Vue initiale doit être 'welcome', trouvé: {vm.current_view}"

            # welcome -> dashboard
            main_window.welcome_view.projectCreationRequested.emit({'name': 'test_project'})
            from PySide6.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            from PySide6.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            qtbot.waitUntil(lambda: vm.current_view == "dashboard", timeout=5000)
            assert vm.current_view == "dashboard", f"Vue doit être 'dashboard', trouvé: {vm.current_view}"
            
            # Étape 1: dashboard → acquisition
            print("[TEST] Étape 1: dashboard → acquisition")
            dashboard_view = main_window.dashboard_view
            qtbot.mouseClick(dashboard_view.start_calibration_button, Qt.LeftButton)
            qtbot.waitUntil(lambda: vm.current_view == "acquisition", timeout=5000)
            assert vm.current_view == "acquisition", f"Vue doit être 'acquisition', trouvé: {vm.current_view}"
            
            # Étape 2: acquisition → analysis
            print("[TEST] Étape 2: acquisition → analysis")
            acquisition_view = main_window.acquisition_view
            # Simuler la fin de l'acquisition pour déclencher la navigation
            acquisition_view.acquisitionFinished.emit({})
            qtbot.waitUntil(lambda: vm.current_view == "analysis", timeout=5000)
            assert vm.current_view == "analysis", f"Vue doit être 'analysis', trouvé: {vm.current_view}"
            
            print("[TEST] ✓ Workflow complet validé avec succès")
        
    def test_view_registration_complete(self, main_window):
        """
        Test que toutes les vues modernes sont enregistrées
        """
        vm = main_window.view_manager
        expected_views = ["welcome", "dashboard", "acquisition", "analysis", "project_settings", "manual_calibration", "live_acquisition_v2"]
        
        for view_name in expected_views:
            assert view_name in vm.views, f"Vue '{view_name}' doit être enregistrée"
            
        print(f"[TEST] ✓ Toutes les vues modernes enregistrées: {expected_views}")
        
    def test_navigation_logs(self, main_window, qtbot, caplog):
        """
        Test que les logs de navigation sont générés
        """
        vm = main_window.view_manager
        
        # Effectuer une navigation
        with caplog.at_level('INFO'):
            vm.switch_to_view('dashboard')
        
        assert "Changement vers la vue" in caplog.text, "Les logs de navigation doivent être présents"
        
        print("[TEST] ✓ Logs de navigation générés")
        
    def test_workflow_timing(self, main_window, qtbot):
        """
        Test que le workflow complet s'exécute en moins de 5 secondes
        """
        import time
        
        start_time = time.time()
        vm = main_window.view_manager
        
        # Parcours complet
        qtbot.mouseClick(main_window.dashboard_view.start_calibration_button, Qt.LeftButton)
        qtbot.waitUntil(lambda: vm.current_view == "acquisition", timeout=2000)
        
        main_window.acquisition_view.acquisitionFinished.emit({})
        qtbot.waitUntil(lambda: vm.current_view == "analysis", timeout=2000)
            
        end_time = time.time()
        duration = end_time - start_time
        
        assert duration < 5.0, f"Workflow doit s'exécuter en moins de 5s, durée: {duration:.2f}s"
        print(f"[TEST] ✓ Workflow exécuté en {duration:.2f}s (< 5s)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])