#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration globale pour les tests pytest
Configure automatiquement les mocks pour éviter les violations d'accès
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime


class MockPerformanceMonitor:
    """Mock complet de PerformanceMonitor qui ne fait rien"""
    
    def __init__(self, collection_interval=5.0, max_history_size=1000, thresholds=None, log_file=None, *args, **kwargs):
        self.metrics_updated = MagicMock()
        self.thresholds = thresholds or MagicMock()
        self._running = False
        self.collection_interval = collection_interval
        self.max_history_size = max_history_size
        self.log_file = log_file
        self._metrics_history = []
        self._alert_callbacks = []
        self._monitoring_thread = None
        
    def start_monitoring(self):
        """Ne fait rien"""
        self._running = True
        
    def stop_monitoring(self):
        """Ne fait rien"""
        self._running = False
        
    def get_current_metrics(self):
        """Retourne des métriques factices"""
        try:
            from src.hrneowave.core.performance_monitor import PerformanceMetrics
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
        except ImportError:
            return None
            
    def get_metrics_history(self):
        """Retourne l'historique des métriques (vide)"""
        return self._metrics_history.copy()
        
    def export_metrics(self, file_path, format='json'):
        """Simule l'export des métriques"""
        import json
        from pathlib import Path
        
        data = {
            'export_timestamp': datetime.now().isoformat(),
            'metrics_count': 0,
            'metrics': []
        }
        
        if format.lower() == 'json':
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        
    def add_alert_callback(self, callback):
        """Ajoute un callback d'alerte"""
        self._alert_callbacks.append(callback)
        
    def remove_alert_callback(self, callback):
        """Supprime un callback d'alerte"""
        if callback in self._alert_callbacks:
            self._alert_callbacks.remove(callback)
        
    def set_thresholds(self, thresholds):
        """Définit les seuils"""
        self.thresholds = thresholds
        
    def is_monitoring(self):
        """Retourne l'état du monitoring"""
        return self._running


@pytest.fixture(autouse=True)
def mock_performance_monitor():
    """Mock automatique de PerformanceMonitor et psutil pour tous les tests"""
    # Arrêter et réinitialiser le moniteur global avant chaque test
    try:
        from src.hrneowave.core.performance_monitor import reset_global_monitor, set_global_monitor
        reset_global_monitor()
        
        # Créer un mock et le définir comme moniteur global
        mock_monitor = MockPerformanceMonitor()
        set_global_monitor(mock_monitor)
    except ImportError:
        pass
    
    # Mock des fonctions psutil qui peuvent causer des violations d'accès
    mock_cpu_percent = MagicMock(return_value=50.0)
    mock_virtual_memory = MagicMock()
    mock_virtual_memory.return_value.percent = 60.0
    mock_virtual_memory.return_value.used = 1024 * 1024 * 1024  # 1GB
    mock_virtual_memory.return_value.available = 512 * 1024 * 1024  # 512MB
    
    mock_disk_usage = MagicMock()
    mock_disk_usage.return_value.used = 40 * 1024 * 1024 * 1024  # 40GB
    mock_disk_usage.return_value.total = 100 * 1024 * 1024 * 1024  # 100GB
    
    mock_pids = MagicMock(return_value=list(range(100)))  # 100 processus factices
    mock_process = MagicMock()
    
    with patch('src.hrneowave.core.performance_monitor.PerformanceMonitor', MockPerformanceMonitor), \
         patch('hrneowave.core.performance_monitor.PerformanceMonitor', MockPerformanceMonitor), \
         patch('src.hrneowave.gui.views.dashboard_view.PerformanceMonitor', MockPerformanceMonitor), \
         patch('hrneowave.gui.views.dashboard_view.PerformanceMonitor', MockPerformanceMonitor), \
         patch('psutil.cpu_percent', mock_cpu_percent), \
         patch('psutil.virtual_memory', mock_virtual_memory), \
         patch('psutil.disk_usage', mock_disk_usage), \
         patch('psutil.pids', mock_pids), \
         patch('psutil.Process', mock_process):
        yield
    
    # Nettoyer après le test
    try:
        from src.hrneowave.core.performance_monitor import reset_global_monitor
        reset_global_monitor()
    except ImportError:
        pass


@pytest.fixture(autouse=True)
def qt_app_cleanup():
    """Nettoyage automatique des applications Qt après chaque test"""
    yield
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.quit()
            app.deleteLater()
    except ImportError:
        pass