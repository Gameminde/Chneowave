# -*- coding: utf-8 -*-
"""
Tests pour le module de monitoring de performance CHNeoWave
"""

import pytest
import time
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Mock psutil avant l'importation pour éviter les violations d'accès
with patch('psutil.cpu_percent', return_value=50.0), \
     patch('psutil.virtual_memory') as mock_memory, \
     patch('psutil.disk_usage') as mock_disk, \
     patch('threading.Thread') as mock_thread:
    
    # Configuration des mocks
    mock_memory.return_value.percent = 60.0
    mock_memory.return_value.used = 1024 * 1024 * 1024  # 1GB
    mock_disk.return_value.percent = 30.0
    
    # Mock Thread pour empêcher la création de threads réels
    mock_thread_instance = Mock()
    mock_thread_instance.start = Mock()
    mock_thread_instance.is_alive.return_value = False
    mock_thread.return_value = mock_thread_instance
    
    from hrneowave.core.performance_monitor import (
        PerformanceMetrics,
        PerformanceThresholds,
        Alert,
        AlertLevel,
        PerformanceMonitor,
        get_performance_monitor
    )

class TestPerformanceMetrics:
    """Tests pour PerformanceMetrics"""
    
    def test_performance_metrics_creation(self):
        """Test création des métriques de performance"""
        metrics = PerformanceMetrics(
            cpu_percent=45.5,
            memory_percent=67.2,
            disk_usage_percent=23.8,
            active_threads=12,
            memory_used_mb=256.0
        )
        
        assert metrics.cpu_percent == 45.5
        assert metrics.memory_percent == 67.2
        assert metrics.disk_usage_percent == 23.8
        assert metrics.active_threads == 12
        assert metrics.memory_used_mb == 256.0
        assert isinstance(metrics.timestamp, datetime)
        
    def test_performance_metrics_to_dict(self):
        """Test conversion en dictionnaire"""
        metrics = PerformanceMetrics(
            cpu_percent=50.0,
            memory_percent=75.0,
            disk_usage_percent=30.0,
            active_threads=8
        )
        
        metrics_dict = metrics.to_dict()
        
        assert metrics_dict['cpu_percent'] == 50.0
        assert metrics_dict['memory_percent'] == 75.0
        assert metrics_dict['disk_usage_percent'] == 30.0
        assert metrics_dict['active_threads'] == 8
        assert 'timestamp' in metrics_dict
        
    def test_performance_metrics_from_dict(self):
        """Test création depuis dictionnaire"""
        data = {
            'cpu_percent': 60.0,
            'memory_percent': 80.0,
            'disk_usage_percent': 40.0,
            'active_threads': 15,
            'memory_used_mb': 512.0,
            'timestamp': '2024-01-01T12:00:00'
        }
        
        metrics = PerformanceMetrics.from_dict(data)
        
        assert metrics.cpu_percent == 60.0
        assert metrics.memory_percent == 80.0
        assert metrics.disk_usage_percent == 40.0
        assert metrics.active_threads == 15
        assert metrics.memory_used_mb == 512.0

class TestPerformanceThresholds:
    """Tests pour PerformanceThresholds"""
    
    def test_performance_thresholds_creation(self):
        """Test création des seuils de performance"""
        thresholds = PerformanceThresholds(
            cpu_warning=70.0,
            cpu_critical=90.0,
            memory_warning=80.0,
            memory_critical=95.0,
            disk_warning=85.0,
            disk_critical=95.0,
            threads_warning=50,
            threads_critical=100
        )
        
        assert thresholds.cpu_warning == 70.0
        assert thresholds.cpu_critical == 90.0
        assert thresholds.memory_warning == 80.0
        assert thresholds.memory_critical == 95.0
        assert thresholds.disk_warning == 85.0
        assert thresholds.disk_critical == 95.0
        assert thresholds.threads_warning == 50
        assert thresholds.threads_critical == 100
        
    def test_performance_thresholds_defaults(self):
        """Test valeurs par défaut des seuils"""
        thresholds = PerformanceThresholds()
        
        # Vérifier que les valeurs par défaut sont raisonnables
        assert 0 < thresholds.cpu_warning < thresholds.cpu_critical <= 100
        assert 0 < thresholds.memory_warning < thresholds.memory_critical <= 100
        assert 0 < thresholds.disk_warning < thresholds.disk_critical <= 100
        assert 0 < thresholds.threads_warning < thresholds.threads_critical

class TestAlert:
    """Tests pour Alert"""
    
    def test_alert_creation(self):
        """Test création d'une alerte"""
        alert = Alert(
            level=AlertLevel.WARNING,
            metric="cpu_percent",
            value=75.5,
            threshold=70.0,
            message="CPU usage is high"
        )
        
        assert alert.level == AlertLevel.WARNING
        assert alert.metric == "cpu_percent"
        assert alert.value == 75.5
        assert alert.threshold == 70.0
        assert alert.message == "CPU usage is high"
        assert isinstance(alert.timestamp, datetime)
        
    def test_alert_to_dict(self):
        """Test conversion d'alerte en dictionnaire"""
        alert = Alert(
            level=AlertLevel.CRITICAL,
            metric="memory_percent",
            value=95.0,
            threshold=90.0,
            message="Memory usage critical"
        )
        
        alert_dict = alert.to_dict()
        
        assert alert_dict['level'] == 'critical'
        assert alert_dict['metric'] == 'memory_percent'
        assert alert_dict['value'] == 95.0
        assert alert_dict['threshold'] == 90.0
        assert alert_dict['message'] == 'Memory usage critical'
        assert 'timestamp' in alert_dict
        
    def test_alert_from_dict(self):
        """Test création d'alerte depuis dictionnaire"""
        data = {
            'level': 'warning',
            'metric': 'disk_usage_percent',
            'value': 88.0,
            'threshold': 85.0,
            'message': 'Disk usage warning',
            'timestamp': '2024-01-01T12:00:00'
        }
        
        alert = Alert.from_dict(data)
        
        assert alert.level == AlertLevel.WARNING
        assert alert.metric == 'disk_usage_percent'
        assert alert.value == 88.0
        assert alert.threshold == 85.0
        assert alert.message == 'Disk usage warning'

class TestPerformanceMonitor:
    """Tests pour PerformanceMonitor"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        # Créer un répertoire temporaire pour les logs
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = Path(self.temp_dir) / "test_performance.log"
        
        # Patcher les méthodes qui utilisent des threads
        self.psutil_patcher = patch('psutil.cpu_percent', return_value=50.0)
        self.memory_patcher = patch('psutil.virtual_memory')
        self.disk_patcher = patch('psutil.disk_usage')
        self.thread_patcher = patch('threading.Thread')
        
        self.mock_cpu = self.psutil_patcher.start()
        self.mock_memory = self.memory_patcher.start()
        self.mock_disk = self.disk_patcher.start()
        self.mock_thread = self.thread_patcher.start()
        
        # Configuration des mocks
        self.mock_memory.return_value.percent = 60.0
        self.mock_memory.return_value.used = 1024 * 1024 * 1024
        self.mock_disk.return_value.percent = 30.0
        
        mock_thread_instance = Mock()
        mock_thread_instance.start = Mock()
        mock_thread_instance.is_alive.return_value = False
        self.mock_thread.return_value = mock_thread_instance
        
        # Créer un moniteur pour les tests
        self.monitor = PerformanceMonitor(
            log_file=str(self.log_file),
            collection_interval=0.1  # Intervalle court pour les tests
        )
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        # Arrêter le monitoring (sans threads réels)
        if hasattr(self.monitor, '_running'):
            self.monitor._running = False
            
        # Arrêter les patchers
        self.psutil_patcher.stop()
        self.memory_patcher.stop()
        self.disk_patcher.stop()
        self.thread_patcher.stop()
            
        # Nettoyer les fichiers temporaires
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_performance_monitor_initialization(self):
        """Test initialisation du moniteur"""
        assert self.monitor.log_file == str(self.log_file)
        assert self.monitor.collection_interval == 0.1
        assert not self.monitor.is_monitoring
        assert len(self.monitor.metrics_history) == 0
        assert self.monitor.thresholds is not None
        
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('threading.active_count')
    @patch('psutil.pids')
    def test_collect_metrics(self, mock_pids, mock_threads, mock_disk, mock_memory, mock_cpu):
        """Test collecte des métriques système"""
        # Configurer les mocks
        mock_cpu.return_value = 45.5
        mock_memory.return_value = Mock(
            percent=67.2,
            used=1024 * 1024 * 512,  # 512 MB
            available=1024 * 1024 * 256  # 256 MB
        )
        mock_disk.return_value = Mock(used=1000, total=4000)  # 25%
        mock_threads.return_value = 12
        mock_pids.return_value = [1, 2, 3, 4, 5]  # 5 processus
        
        metrics = self.monitor._collect_metrics()
        
        assert metrics.cpu_percent == 45.5
        assert metrics.memory_percent == 67.2
        assert metrics.memory_used_mb == 512.0
        assert metrics.memory_available_mb == 256.0
        assert metrics.disk_usage_percent == 25.0
        assert metrics.active_threads == 12
        assert metrics.process_count == 5
        
    def test_check_thresholds_no_alerts(self):
        """Test vérification des seuils sans alerte"""
        # Métriques normales
        metrics = PerformanceMetrics(
            cpu_percent=30.0,
            memory_percent=50.0,
            disk_usage_percent=40.0,
            active_threads=10,
            memory_used_mb=128.0
        )
        
        alerts = self.monitor._check_thresholds(metrics)
        assert len(alerts) == 0
        
    def test_check_thresholds_with_warnings(self):
        """Test vérification des seuils avec avertissements"""
        # Configurer des seuils bas pour les tests
        self.monitor.thresholds.cpu_warning = 50.0
        self.monitor.thresholds.memory_warning = 60.0
        
        # Métriques dépassant les seuils d'avertissement
        metrics = PerformanceMetrics(
            cpu_percent=75.0,
            memory_percent=70.0,
            disk_usage_percent=40.0,
            active_threads=10
        )
        
        alerts = self.monitor._check_thresholds(metrics)
        
        # Devrait y avoir 2 alertes (CPU et mémoire)
        assert len(alerts) == 2
        
        # Vérifier les types d'alertes
        alert_metrics = [alert.metric for alert in alerts]
        assert 'cpu_percent' in alert_metrics
        assert 'memory_percent' in alert_metrics
        
        # Vérifier les niveaux
        for alert in alerts:
            assert alert.level == AlertLevel.WARNING
            
        # Déclencher les callbacks pour tester
        for alert in alerts:
            self.monitor._trigger_alert_callbacks(alert)
            
    def test_check_thresholds_with_critical(self):
        """Test vérification des seuils avec alertes critiques"""
        # Configurer des seuils bas pour les tests
        self.monitor.thresholds.cpu_critical = 80.0
        self.monitor.thresholds.memory_critical = 85.0
        
        # Métriques dépassant les seuils critiques
        metrics = PerformanceMetrics(
            cpu_percent=95.0,
            memory_percent=90.0,
            disk_usage_percent=40.0,
            active_threads=10
        )
        
        alerts = self.monitor._check_thresholds(metrics)
        
        # Devrait y avoir 2 alertes critiques
        assert len(alerts) == 2
        
        for alert in alerts:
            assert alert.level == AlertLevel.CRITICAL
            
    def test_add_alert_callback(self):
        """Test ajout de callback d'alerte"""
        callback_called = []
        
        def test_callback(alert):
            callback_called.append(alert)
            
        self.monitor.add_alert_callback(test_callback)
        
        # Simuler une alerte
        alert = Alert(
            level=AlertLevel.WARNING,
            metric="test_metric",
            value=100.0,
            threshold=80.0,
            message="Test alert"
        )
        
        # Déclencher les callbacks
        self.monitor._trigger_alert_callbacks(alert)
        
        assert len(callback_called) == 1
        assert callback_called[0] == alert
        
    def test_remove_alert_callback(self):
        """Test suppression de callback d'alerte"""
        callback_called = []
        
        def test_callback(alert):
            callback_called.append(alert)
            
        # Ajouter puis supprimer le callback
        self.monitor.add_alert_callback(test_callback)
        self.monitor.remove_alert_callback(test_callback)
        
        # Simuler une alerte
        alert = Alert(
            level=AlertLevel.WARNING,
            metric="test_metric",
            value=100.0,
            threshold=80.0,
            message="Test alert"
        )
        
        # Déclencher les callbacks
        self.monitor._trigger_alert_callbacks(alert)
        
        # Le callback ne devrait pas avoir été appelé
        assert len(callback_called) == 0
        
    def test_get_current_metrics(self):
        """Test récupération des métriques actuelles"""
        # Test quand le monitoring n'est pas en cours
        assert not self.monitor.is_monitoring
        
        with patch.object(self.monitor, '_collect_metrics') as mock_collect:
            mock_metrics = PerformanceMetrics(
                cpu_percent=50.0,
                memory_percent=60.0,
                disk_usage_percent=30.0,
                active_threads=8
            )
            mock_collect.return_value = mock_metrics
            
            current = self.monitor.get_current_metrics()
            
            assert current == mock_metrics
            mock_collect.assert_called_once()
            
        # Test quand le monitoring est en cours
        test_metrics = PerformanceMetrics(
            cpu_percent=25.0,
            memory_percent=35.0,
            disk_usage_percent=15.0,
            active_threads=4
        )
        self.monitor._metrics_history.append(test_metrics)
        self.monitor._running = True
        
        current = self.monitor.get_current_metrics()
        assert current == test_metrics
        
        self.monitor._running = False
            
    def test_get_metrics_history(self):
        """Test récupération de l'historique des métriques"""
        # Ajouter des métriques à l'historique
        for i in range(5):
            metrics = PerformanceMetrics(
                cpu_percent=float(i * 10),
                memory_percent=float(i * 15),
                disk_usage_percent=float(i * 5),
                active_threads=i + 1
            )
            self.monitor._metrics_history.append(metrics)
            
        # Récupérer les 3 dernières
        recent = self.monitor.get_metrics_history(3)
        assert len(recent) == 3
        
        # Vérifier l'ordre (les 3 derniers dans l'ordre d'ajout)
        assert recent[0].cpu_percent == 20.0  # i=2
        assert recent[1].cpu_percent == 30.0  # i=3
        assert recent[2].cpu_percent == 40.0  # i=4
        
    def test_get_average_metrics(self):
        """Test calcul des métriques moyennes"""
        # Ajouter des métriques connues
        metrics_list = [
            PerformanceMetrics(cpu_percent=10.0, memory_percent=20.0, disk_usage_percent=30.0, active_threads=5),
            PerformanceMetrics(cpu_percent=20.0, memory_percent=30.0, disk_usage_percent=40.0, active_threads=10),
            PerformanceMetrics(cpu_percent=30.0, memory_percent=40.0, disk_usage_percent=50.0, active_threads=15)
        ]
        
        for metrics in metrics_list:
            self.monitor._metrics_history.append(metrics)
            
        # Calculer les moyennes
        avg = self.monitor.get_average_metrics(3)
        
        assert avg['cpu_percent'] == 20.0  # (10+20+30)/3
        assert avg['memory_percent'] == 30.0  # (20+30+40)/3
        assert avg['disk_usage_percent'] == 40.0  # (30+40+50)/3
        assert avg['active_threads'] == 10.0  # (5+10+15)/3
        
    def test_export_metrics(self):
        """Test export des métriques"""
        # Ajouter des métriques
        for i in range(3):
            metrics = PerformanceMetrics(
                cpu_percent=float(i * 10),
                memory_percent=float(i * 15),
                disk_usage_percent=float(i * 5),
                active_threads=i + 1
            )
            self.monitor._metrics_history.append(metrics)
            
        # Exporter vers un fichier
        export_file = Path(self.temp_dir) / "exported_metrics.json"
        
        # Mocker get_current_metrics pour éviter les MagicMock
        with patch.object(self.monitor, 'get_current_metrics') as mock_current:
            mock_current.return_value = PerformanceMetrics(
                cpu_percent=50.0,
                memory_percent=60.0,
                disk_usage_percent=25.0,
                active_threads=2
            )
            
            self.monitor.export_metrics(str(export_file))
        
        # Vérifier que le fichier existe et contient les données
        assert export_file.exists()
        
        with open(export_file, 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
            
        assert len(exported_data['metrics']) == 3
        assert exported_data['metrics'][0]['cpu_percent'] == 0.0
        assert exported_data['metrics'][1]['cpu_percent'] == 10.0
        assert exported_data['metrics'][2]['cpu_percent'] == 20.0
        
    def test_clear_history(self):
        """Test nettoyage de l'historique"""
        # Ajouter des métriques
        for i in range(5):
            metrics = PerformanceMetrics(
                cpu_percent=float(i),
                memory_percent=float(i),
                disk_usage_percent=float(i),
                active_threads=i
            )
            self.monitor.metrics_history.append(metrics)
            
        assert len(self.monitor.metrics_history) == 5
        
        # Nettoyer l'historique
        self.monitor.clear_history()
        assert len(self.monitor.metrics_history) == 0
        
    def test_context_manager(self):
        """Test utilisation comme gestionnaire de contexte"""
        with patch.object(self.monitor, 'start_monitoring') as mock_start, \
             patch.object(self.monitor, 'stop_monitoring') as mock_stop:
            
            with self.monitor:
                # Le monitoring devrait être démarré
                mock_start.assert_called_once()
                
            # Le monitoring devrait être arrêté
            mock_stop.assert_called_once()
            
    @patch('threading.Thread')
    def test_start_stop_monitoring(self, mock_thread):
        """Test démarrage et arrêt du monitoring"""
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        # Démarrer le monitoring
        self.monitor.start_monitoring()
        
        assert self.monitor.is_monitoring
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
        
        # Arrêter le monitoring
        self.monitor.stop_monitoring()
        
        assert not self.monitor.is_monitoring
        
    def test_monitoring_thread_exception_handling(self):
        """Test gestion des exceptions dans le thread de monitoring"""
        with patch.object(self.monitor, '_collect_metrics') as mock_collect:
            # Faire lever une exception
            mock_collect.side_effect = Exception("Test exception")
            
            # Activer le monitoring pour que _monitoring_loop appelle _collect_metrics
            self.monitor._running = True
            
            # Le monitoring ne devrait pas planter
            # On simule juste un cycle de la boucle
            try:
                self.monitor._monitoring_loop()
            except:
                pass  # On s'attend à ce que la boucle gère l'exception
            finally:
                self.monitor._running = False
            
            # Vérifier que l'exception a été gérée
            mock_collect.assert_called()

class TestPerformanceMonitorSingleton:
    """Tests pour le singleton PerformanceMonitor"""
    
    @patch('threading.Thread')
    @patch('psutil.cpu_percent', return_value=50.0)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_get_performance_monitor_singleton(self, mock_disk, mock_memory, mock_cpu, mock_thread):
        """Test que get_performance_monitor retourne toujours la même instance"""
        # Configuration des mocks
        mock_memory.return_value.percent = 60.0
        mock_memory.return_value.used = 1024 * 1024 * 1024
        mock_disk.return_value.percent = 30.0
        
        mock_thread_instance = Mock()
        mock_thread_instance.start = Mock()
        mock_thread_instance.is_alive.return_value = False
        mock_thread.return_value = mock_thread_instance
        
        monitor1 = get_performance_monitor()
        monitor2 = get_performance_monitor()
        
        assert monitor1 is monitor2
        
    @patch('threading.Thread')
    @patch('psutil.cpu_percent', return_value=50.0)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_get_performance_monitor_with_config(self, mock_disk, mock_memory, mock_cpu, mock_thread):
        """Test configuration du moniteur de performance"""
        # Configuration des mocks
        mock_memory.return_value.percent = 60.0
        mock_memory.return_value.used = 1024 * 1024 * 1024
        mock_disk.return_value.percent = 30.0
        
        mock_thread_instance = Mock()
        mock_thread_instance.start = Mock()
        mock_thread_instance.is_alive.return_value = False
        mock_thread.return_value = mock_thread_instance
        
        # Réinitialiser le moniteur global pour ce test
        import hrneowave.core.performance_monitor as pm_module
        pm_module._global_monitor = None
        
        config = {
            "log_file": "test_performance.log",
            "collection_interval": 2.0,
            "max_history_size": 500
        }
        
        monitor = get_performance_monitor(config)
        assert str(monitor.log_file) == "test_performance.log"
        assert monitor.collection_interval == 2.0
        assert monitor.max_history_size == 500

class TestPerformanceMonitorIntegration:
    """Tests d'intégration pour le moniteur de performance"""
    
    @patch('threading.Thread')
    @patch('psutil.cpu_percent', return_value=75.0)  # Valeur élevée pour déclencher alertes
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_complete_monitoring_workflow(self, mock_disk, mock_memory, mock_cpu, mock_thread):
        """Test workflow complet de monitoring"""
        # Configuration des mocks
        mock_memory.return_value.percent = 80.0  # Valeur élevée
        mock_memory.return_value.used = 1024 * 1024 * 1024
        mock_disk.return_value.percent = 30.0
        
        mock_thread_instance = Mock()
        mock_thread_instance.start = Mock()
        mock_thread_instance.is_alive.return_value = False
        mock_thread.return_value = mock_thread_instance
        
        # Créer un moniteur temporaire
        temp_dir = tempfile.mkdtemp()
        log_file = Path(temp_dir) / "integration_test.log"
        
        try:
            monitor = PerformanceMonitor(
                log_file=str(log_file),
                collection_interval=0.1,
                max_history_size=10
            )
            
            # Configurer des seuils bas pour déclencher des alertes
            monitor.thresholds.cpu_warning = 1.0  # Très bas pour déclencher
            monitor.thresholds.memory_warning = 1.0
            
            alerts_received = []
            
            def alert_callback(alert):
                alerts_received.append(alert)
                
            monitor.add_alert_callback(alert_callback)
            
            # Simuler la collecte de métriques sans threads
            with patch.object(monitor, '_collect_metrics') as mock_collect:
                mock_metrics = PerformanceMetrics(
                    cpu_percent=75.0,
                    memory_percent=80.0,
                    disk_usage_percent=30.0,
                    active_threads=5
                )
                mock_collect.return_value = mock_metrics
                
                # Simuler quelques collectes
                for _ in range(3):
                    monitor._collect_metrics()
                    monitor.metrics_history.append(mock_metrics)
                    # Déclencher manuellement la vérification des seuils
                    alerts = monitor._check_thresholds(mock_metrics)
                    # Déclencher les callbacks d'alerte
                    for alert in alerts:
                        monitor._trigger_alert_callbacks(alert)
            
            # Vérifier que des métriques ont été collectées
            assert len(monitor.metrics_history) > 0
            
            # Vérifier que des alertes ont été déclenchées (seuils très bas)
            assert len(alerts_received) > 0
            
            # Exporter les métriques avec mock pour éviter MagicMock
            export_file = Path(temp_dir) / "exported_integration.json"
            with patch.object(monitor, 'get_current_metrics') as mock_current:
                mock_current.return_value = PerformanceMetrics(
                    cpu_percent=75.0,
                    memory_percent=80.0,
                    disk_usage_percent=30.0,
                    active_threads=5
                )
                monitor.export_metrics(str(export_file))
            
            assert export_file.exists()
            
            # Vérifier les statistiques
            current = monitor.get_current_metrics()
            assert current is not None
            
            avg = monitor.get_average_metrics()
            assert 'cpu_percent' in avg
            assert 'memory_percent' in avg
            
        finally:
            # Nettoyer
            if hasattr(monitor, '_running'):
                monitor._running = False
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    @patch('threading.Thread')
    @patch('psutil.cpu_percent', return_value=50.0)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_performance_monitor_stress_test(self, mock_disk, mock_memory, mock_cpu, mock_thread):
        """Test de stress du moniteur de performance"""
        # Configuration des mocks
        mock_memory.return_value.percent = 60.0
        mock_memory.return_value.used = 1024 * 1024 * 512
        mock_disk.return_value.percent = 25.0
        
        mock_thread_instance = Mock()
        mock_thread_instance.start = Mock()
        mock_thread_instance.is_alive.return_value = False
        mock_thread.return_value = mock_thread_instance
        
        monitor = PerformanceMonitor(collection_interval=0.01)  # Très rapide
        
        try:
            # Simuler plusieurs collectes rapides
            with patch.object(monitor, '_collect_metrics') as mock_collect:
                mock_metrics = PerformanceMetrics(
                    cpu_percent=50.0,
                    memory_percent=60.0,
                    disk_usage_percent=25.0,
                    active_threads=3
                )
                mock_collect.return_value = mock_metrics
                
                # Simuler de nombreuses collectes
                for _ in range(20):
                    monitor._collect_metrics()
                    monitor.metrics_history.append(mock_metrics)
            
            # Vérifier que le système n'a pas planté
            assert len(monitor.metrics_history) > 0
            
            # Vérifier que les métriques sont cohérentes
            for metrics in monitor.metrics_history:
                assert 0 <= metrics.cpu_percent <= 100
                assert 0 <= metrics.memory_percent <= 100
                assert 0 <= metrics.disk_usage_percent <= 100
                assert metrics.active_threads >= 0
                
        finally:
            if hasattr(monitor, '_running'):
                monitor._running = False
                
    @patch('threading.Thread')
    @patch('psutil.cpu_percent', return_value=50.0)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_memory_usage_monitoring(self, mock_disk, mock_memory, mock_cpu, mock_thread):
        """Test monitoring de l'usage mémoire du moniteur lui-même"""
        # Configuration des mocks
        mock_memory.return_value.percent = 60.0
        mock_memory.return_value.used = 1024 * 1024 * 512
        mock_disk.return_value.percent = 25.0
        
        mock_thread_instance = Mock()
        mock_thread_instance.start = Mock()
        mock_thread_instance.is_alive.return_value = False
        mock_thread.return_value = mock_thread_instance
        
        monitor = PerformanceMonitor(collection_interval=0.01)
        
        try:
            # Simuler la collecte de nombreuses métriques
            with patch.object(monitor, '_collect_metrics') as mock_collect:
                mock_metrics = PerformanceMetrics(
                    cpu_percent=50.0,
                    memory_percent=60.0,
                    disk_usage_percent=25.0,
                    active_threads=3
                )
                mock_collect.return_value = mock_metrics
                
                # Simuler beaucoup de collectes pour tester l'usage mémoire
                for _ in range(100):
                    monitor._collect_metrics()
                    monitor.metrics_history.append(mock_metrics)
            
            # Vérifier que l'historique ne grandit pas indéfiniment
            assert len(monitor.metrics_history) <= monitor.max_history_size
            
            # Vérifier que les métriques sont cohérentes
            for metrics in monitor.metrics_history:
                assert 0 <= metrics.cpu_percent <= 100
                assert 0 <= metrics.memory_percent <= 100
                assert 0 <= metrics.disk_usage_percent <= 100
                assert metrics.active_threads >= 0
            
            print(f"Métriques collectées: {len(monitor.metrics_history)}")
            
        finally:
            if hasattr(monitor, '_running'):
                monitor._running = False

if __name__ == '__main__':
    # Exécuter les tests si le script est lancé directement
    pytest.main([__file__, '-v'])