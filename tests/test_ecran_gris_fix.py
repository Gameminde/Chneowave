#!/usr/bin/env python3
"""
Test de validation du correctif pour l'écran gris de CHNeoWave
"""

import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).resolve().parents[1]
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


class MockPerformanceMonitor:
    """Mock complet de PerformanceMonitor qui ne fait rien"""
    
    def __init__(self, *args, **kwargs):
        self.metrics_updated = MagicMock()
        self.thresholds = MagicMock()
        self._running = False
        
    def start_monitoring(self):
        """Ne fait rien"""
        pass
        
    def stop_monitoring(self):
        """Ne fait rien"""
        pass
        
    def get_current_metrics(self):
        """Retourne des métriques factices"""
        from hrneowave.core.performance_monitor import PerformanceMetrics
        from datetime import datetime
        return PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_percent=50.0,
            memory_percent=60.0,
            memory_used_mb=1024.0,
            memory_available_mb=512.0,
            disk_usage_percent=40.0,
            active_threads=5,
            process_count=100
        )


# Import des modules GUI avec mock
from PySide6.QtWidgets import QStackedWidget
from hrneowave.gui.view_manager import ViewManager

# Patch PerformanceMonitor avant l'importation de DashboardView
with patch('hrneowave.core.performance_monitor.PerformanceMonitor', MockPerformanceMonitor):
    from hrneowave.gui.views.dashboard_view import DashboardView
    
from hrneowave.gui.views.calibration_view import CalibrationView
from hrneowave.gui.views.acquisition_view import AcquisitionView
from hrneowave.gui.views.analysis_view import AnalysisView
from hrneowave.utils import setup_logging

# Configuration du logging
setup_logging()

def test_ecran_gris_fix(qtbot):
    """
    Test automatisé pour vérifier que l'interface s'affiche correctement
    et que la vue initiale est la bonne.
    """
    print("=== TEST CORRECTIF ÉCRAN GRIS ===")
    
    # 1. Création des composants UI
    stacked_widget = QStackedWidget()
    qtbot.addWidget(stacked_widget) # Géré par qtbot
    
    view_manager = ViewManager(stacked_widget)
    
    # 2. Enregistrement des vues
    view_manager.register_view("dashboard", DashboardView())
    view_manager.register_view("calibration", CalibrationView())
    view_manager.register_view("acquisition", AcquisitionView())
    view_manager.register_view("analysis", AnalysisView())
    
    # 3. Affichage et attente
    stacked_widget.show()
    qtbot.waitExposed(stacked_widget)

    # 4. Changement de vue vers le dashboard
    view_manager.switch_to_view("dashboard")
    
    # 5. Assertions
    assert stacked_widget.count() == 4, f"Attendait 4 vues, mais a obtenu {stacked_widget.count()}"
    assert stacked_widget.currentIndex() == 0, f"L'index courant devrait être 0, mais est {stacked_widget.currentIndex()}"
    
    current_widget = stacked_widget.currentWidget()
    assert current_widget is not None, "Le widget courant ne devrait pas être None"
    assert isinstance(current_widget, DashboardView), f"Le widget courant devrait être DashboardView, mais est {type(current_widget)}"
    assert current_widget.isVisible(), "Le widget courant (DashboardView) devrait être visible"
    
    print("✅ Test de l'écran gris réussi.")