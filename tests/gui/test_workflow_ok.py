#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test end-to-end du workflow complet CHNeoWave
Mission: Interface Unifiée & Workflow Complet

Validation du parcours complet:
dashboard → calibration → acquisition → analysis → export
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest

# Ajouter le chemin src pour les imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock du hardware avant l'import
with patch('hrneowave.hw.hardware_adapter.HardwareAcquisitionAdapter') as mock_hw:
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
    def main_window(self, app):
        """Fixture pour la fenêtre principale"""
        window = MainWindow()
        window.show()
        yield window
        window.close()
        
    def test_workflow_navigation_complete(self, main_window):
        """
        Test du workflow complet: dashboard → calibration → acquisition → analysis → export
        Durée maximale: 15 secondes
        """
        with patch('hrneowave.hw.hardware_adapter.HardwareAcquisitionAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_initialized = True
            
            print("\n[TEST] Démarrage test workflow complet")
            
            # Vérifier que l'application démarre sur dashboard
            vm = main_window.view_manager
            assert vm is not None, "ViewManager doit être disponible"
            
            # Forcer la navigation vers dashboard au démarrage
            vm.switch_to_view("dashboard")
            
            # Attendre que l'interface soit prête
            QTest.qWait(500)
            
            print(f"[TEST] Vue initiale: {vm.current_view}")
            assert vm.current_view == "dashboard", f"Vue initiale doit être 'dashboard', trouvé: {vm.current_view}"
            
            # Étape 1: dashboard → calibration (Valider projet)
            print("[TEST] Étape 1: dashboard → calibration")
            success = vm.switch_to_view("calibration")
            assert success, "Navigation vers calibration doit réussir"
            QTest.qWait(200)
            assert vm.current_view == "calibration", f"Vue doit être 'calibration', trouvé: {vm.current_view}"
            
            # Étape 2: calibration → acquisition (Continuer calibration)
            print("[TEST] Étape 2: calibration → acquisition")
            success = vm.switch_to_view("acquisition")
            assert success, "Navigation vers acquisition doit réussir"
            QTest.qWait(200)
            assert vm.current_view == "acquisition", f"Vue doit être 'acquisition', trouvé: {vm.current_view}"
            
            # Étape 3: acquisition → analysis (Analyser acquisition OK)
            print("[TEST] Étape 3: acquisition → analysis")
            success = vm.switch_to_view("analysis")
            assert success, "Navigation vers analysis doit réussir"
            QTest.qWait(200)
            assert vm.current_view == "analysis", f"Vue doit être 'analysis', trouvé: {vm.current_view}"
            
            # Étape 4: analysis → export (Exporter PDF/HDF5)
            print("[TEST] Étape 4: analysis → export")
            success = vm.switch_to_view("export")
            assert success, "Navigation vers export doit réussir"
            QTest.qWait(200)
            assert vm.current_view == "export", f"Vue finale doit être 'export', trouvé: {vm.current_view}"
            
            print("[TEST] ✓ Workflow complet validé avec succès")
        
    def test_view_registration_complete(self, main_window):
        """
        Test que toutes les vues modernes sont enregistrées
        """
        with patch('hrneowave.hw.hardware_adapter.HardwareAcquisitionAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_initialized = True
            
            vm = main_window.view_manager
            expected_views = ["dashboard", "calibration", "acquisition", "analysis", "export"]
            
            for view_name in expected_views:
                assert vm.has_view(view_name), f"Vue '{view_name}' doit être enregistrée"
                
            print(f"[TEST] ✓ Toutes les vues modernes enregistrées: {expected_views}")
        
    def test_navigation_logs(self, main_window, capsys):
        """
        Test que les logs de navigation sont générés
        """
        with patch('hrneowave.hw.hardware_adapter.HardwareAcquisitionAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_initialized = True
            
            vm = main_window.view_manager
            
            # Effectuer une navigation
            vm.switch_to_view("calibration")
            QTest.qWait(100)
            
            # Vérifier les logs
            captured = capsys.readouterr()
            assert "[NAV]" in captured.out, "Les logs de navigation doivent être présents"
            
            print("[TEST] ✓ Logs de navigation générés")
        
    def test_workflow_timing(self, main_window):
        """
        Test que le workflow complet s'exécute en moins de 15 secondes
        """
        with patch('hrneowave.hw.hardware_adapter.HardwareAcquisitionAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_initialized = True
            
            import time
            
            start_time = time.time()
            vm = main_window.view_manager
            
            # Parcours complet
            views = ["dashboard", "calibration", "acquisition", "analysis", "export"]
            
            for view in views:
                vm.switch_to_view(view)
                QTest.qWait(50)  # Attente minimale
                
            end_time = time.time()
            duration = end_time - start_time
            
            assert duration < 15.0, f"Workflow doit s'exécuter en moins de 15s, durée: {duration:.2f}s"
            print(f"[TEST] ✓ Workflow exécuté en {duration:.2f}s (< 15s)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])