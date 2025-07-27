"""Tests pour DashboardView sans PerformanceMonitor pour éviter les violations d'accès"""

import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QTimer


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


# Patch PerformanceMonitor avant l'importation
with patch('hrneowave.core.performance_monitor.PerformanceMonitor', MockPerformanceMonitor):
    from hrneowave.gui.views.dashboard_view import DashboardView


class TestDashboardViewSafe:
    """Tests sécurisés pour DashboardView"""
    
    @pytest.fixture
    def app(self):
        """Fixture pour l'application Qt"""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        yield app
        
    def test_dashboard_view_initialization_safe(self, app, qtbot):
        """Test l'initialisation de DashboardView de manière sécurisée"""
        # Créer la vue
        view = DashboardView()
        qtbot.addWidget(view)
        
        # Vérifier que la vue est créée
        assert view is not None
        assert hasattr(view, 'performance_monitor')
        
        # Vérifier que les cartes KPI sont créées
        assert hasattr(view, 'cpu_card')
        assert hasattr(view, 'buffer_card')  # Correspond à memory
        assert hasattr(view, 'disk_card')
        assert hasattr(view, 'probes_card')  # Correspond à threads
        assert hasattr(view, 'time_card')
        
        # Vérifier que le bouton est créé
        assert hasattr(view, 'start_calibration_button')
        
        # Nettoyer
        view.close()
        
    def test_dashboard_view_kpi_update_safe(self, app, qtbot):
        """Test la mise à jour des KPI de manière sécurisée"""
        view = DashboardView()
        qtbot.addWidget(view)
        
        # Simuler une mise à jour des métriques avec la méthode legacy
        view.update_kpis(75.5, 45.2)
        
        # Vérifier que les cartes existent toujours
        assert view.cpu_card is not None
        assert view.buffer_card is not None
        assert view.disk_card is not None
        assert view.probes_card is not None
        assert view.time_card is not None
        
        # Nettoyer
        view.close()
        
    def test_dashboard_view_button_signal_safe(self, app, qtbot):
        """Test l'émission du signal lors du clic sur un bouton de manière sécurisée"""
        view = DashboardView()
        qtbot.addWidget(view)
        
        # Connecter un signal spy pour vérifier l'émission du signal
        with qtbot.waitSignal(view.acquisitionRequested, timeout=1000) as blocker:
            # Simuler un clic sur le bouton de calibration
            qtbot.mouseClick(view.start_calibration_button, Qt.LeftButton)
        
        # Vérifier que le signal a été émis (pas d'arguments pour ce signal)
        assert blocker.signal_triggered
        
        # Nettoyer
        view.close()