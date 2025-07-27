# -*- coding: utf-8 -*-
"""
Module de monitoring des performances pour CHNeoWave
Collecte et surveille les métriques système en temps réel
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
from enum import Enum

# Import conditionnel pour Qt
try:
    from PySide6.QtCore import QObject, Signal
    QT_AVAILABLE = True
except ImportError:
    try:
        from PyQt6.QtCore import QObject, pyqtSignal as Signal
        QT_AVAILABLE = True
    except ImportError:
        QT_AVAILABLE = False
        QObject = object
        Signal = lambda *args: None

class AlertLevel(Enum):
    """Niveaux d'alerte pour le monitoring"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class PerformanceMetrics:
    """Structure pour stocker les métriques de performance"""
    timestamp: datetime = None
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_used_mb: float = 0.0
    memory_available_mb: float = 0.0
    disk_usage_percent: float = 0.0
    active_threads: int = 0
    process_count: int = 0
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit les métriques en dictionnaire"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_used_mb': self.memory_used_mb,
            'memory_available_mb': self.memory_available_mb,
            'disk_usage_percent': self.disk_usage_percent,
            'active_threads': self.active_threads,
            'process_count': self.process_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerformanceMetrics':
        """Crée une instance depuis un dictionnaire"""
        timestamp = data.get('timestamp', datetime.now())
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        return cls(
            timestamp=timestamp,
            cpu_percent=data.get('cpu_percent', 0.0),
            memory_percent=data.get('memory_percent', 0.0),
            memory_used_mb=data.get('memory_used_mb', 0.0),
            memory_available_mb=data.get('memory_available_mb', 0.0),
            disk_usage_percent=data.get('disk_usage_percent', 0.0),
            active_threads=data.get('active_threads', 0),
            process_count=data.get('process_count', 0)
        )

@dataclass
class PerformanceThresholds:
    """Seuils d'alerte pour les métriques"""
    cpu_warning: float = 70.0
    cpu_critical: float = 90.0
    memory_warning: float = 75.0
    memory_critical: float = 90.0
    disk_warning: float = 80.0
    disk_critical: float = 95.0
    threads_warning: int = 100
    threads_critical: int = 200

@dataclass
class Alert:
    """Structure pour les alertes de performance"""
    level: AlertLevel
    metric: str
    value: float
    threshold: float
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'alerte en dictionnaire"""
        return {
            'level': self.level.value,
            'metric': self.metric,
            'value': self.value,
            'threshold': self.threshold,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Alert':
        """Crée une instance depuis un dictionnaire"""
        timestamp = data.get('timestamp', datetime.now())
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        level = data['level']
        if isinstance(level, str):
            level = AlertLevel(level)
        
        return cls(
            level=level,
            metric=data['metric'],
            value=data['value'],
            threshold=data['threshold'],
            message=data['message'],
            timestamp=timestamp
        )

class PerformanceMonitor(QObject):
    """Moniteur de performance en temps réel pour CHNeoWave"""
    
    # Signaux Qt pour l'intégration GUI
    metrics_updated = Signal(object)  # PerformanceMetrics
    alert_triggered = Signal(object)  # Alert
    
    def __init__(self, 
                 collection_interval: float = 5.0,
                 max_history_size: int = 1000,
                 thresholds: Optional[PerformanceThresholds] = None,
                 log_file: Optional[Path] = None):
        """
        Initialise le moniteur de performance
        
        Args:
            collection_interval: Intervalle de collecte en secondes
            max_history_size: Taille maximale de l'historique
            thresholds: Seuils d'alerte personnalisés
            log_file: Fichier de log pour les métriques
        """
        if QT_AVAILABLE:
            super().__init__()
        
        self.collection_interval = collection_interval
        self.max_history_size = max_history_size
        self.thresholds = thresholds or PerformanceThresholds()
        self.log_file = log_file
        
        # État du monitoring
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # Stockage des données
        self._metrics_history: List[PerformanceMetrics] = []
        self._alerts_history: List[Alert] = []
        
        # Callbacks pour les alertes
        self._alert_callbacks: List[Callable[[Alert], None]] = []
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
        # Métriques de base du processus
        self._process = psutil.Process()
    
    @property
    def is_monitoring(self) -> bool:
        """Retourne True si le monitoring est en cours"""
        return self._running
    
    @property
    def metrics_history(self) -> List[PerformanceMetrics]:
        """Retourne l'historique des métriques"""
        return self._metrics_history
    
    def clear_history(self):
        """Nettoie l'historique des métriques"""
        with self._lock:
            self._metrics_history.clear()
            self._alerts_history.clear()
        
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Ajoute un callback pour les alertes"""
        self._alert_callbacks.append(callback)
        
    def remove_alert_callback(self, callback: Callable[[Alert], None]):
        """Supprime un callback d'alerte"""
        if callback in self._alert_callbacks:
            self._alert_callbacks.remove(callback)
            
    def start_monitoring(self):
        """Démarre le monitoring en arrière-plan"""
        if self._running:
            self.logger.warning("Le monitoring est déjà en cours")
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._thread.start()
        
        self.logger.info(f"Monitoring démarré (intervalle: {self.collection_interval}s)")
        
    def stop_monitoring(self):
        """Arrête le monitoring"""
        if not self._running:
            return
            
        self._running = False
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
            
        self.logger.info("Monitoring arrêté")
        
    def _monitoring_loop(self):
        """Boucle principale de monitoring"""
        while self._running:
            try:
                # Collecter les métriques
                metrics = self._collect_metrics()
                
                # Stocker dans l'historique
                with self._lock:
                    self._metrics_history.append(metrics)
                    
                    # Limiter la taille de l'historique
                    if len(self._metrics_history) > self.max_history_size:
                        self._metrics_history.pop(0)
                
                # Émettre le signal de mise à jour des métriques
                if QT_AVAILABLE:
                    self.metrics_updated.emit(metrics)
                
                # Vérifier les seuils et générer des alertes
                alerts = self._check_thresholds(metrics)
                
                for alert in alerts:
                    self._handle_alert(alert)
                
                # Logger les métriques si configuré
                if self.log_file:
                    self._log_metrics(metrics)
                    
            except Exception as e:
                self.logger.error(f"Erreur dans la boucle de monitoring: {e}")
                
            # Attendre avant la prochaine collecte
            time.sleep(self.collection_interval)
            
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collecte les métriques système actuelles"""
        # Métriques CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Métriques mémoire
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_mb = memory.used / (1024 * 1024)
        memory_available_mb = memory.available / (1024 * 1024)
        
        # Métriques disque (partition racine)
        import os
        if os.name == 'nt':  # Windows
            disk_path = 'C:\\'
        else:  # Unix/Linux
            disk_path = '/'
        disk = psutil.disk_usage(disk_path)
        disk_usage_percent = (disk.used / disk.total) * 100
        
        # Métriques threads et processus
        active_threads = threading.active_count()
        process_count = len(psutil.pids())
        
        return PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_mb=memory_used_mb,
            memory_available_mb=memory_available_mb,
            disk_usage_percent=disk_usage_percent,
            active_threads=active_threads,
            process_count=process_count
        )
        
    def _check_thresholds(self, metrics: PerformanceMetrics) -> List[Alert]:
        """Vérifie les seuils et génère des alertes si nécessaire"""
        alerts = []
        
        # Vérifier CPU
        if metrics.cpu_percent >= self.thresholds.cpu_critical:
            alerts.append(Alert(
                level=AlertLevel.CRITICAL,
                metric="cpu_percent",
                value=metrics.cpu_percent,
                threshold=self.thresholds.cpu_critical,
                message=f"Utilisation CPU critique: {metrics.cpu_percent:.1f}%"
            ))
        elif metrics.cpu_percent >= self.thresholds.cpu_warning:
            alerts.append(Alert(
                level=AlertLevel.WARNING,
                metric="cpu_percent",
                value=metrics.cpu_percent,
                threshold=self.thresholds.cpu_warning,
                message=f"Utilisation CPU élevée: {metrics.cpu_percent:.1f}%"
            ))
            
        # Vérifier mémoire
        if metrics.memory_percent >= self.thresholds.memory_critical:
            alerts.append(Alert(
                level=AlertLevel.CRITICAL,
                metric="memory_percent",
                value=metrics.memory_percent,
                threshold=self.thresholds.memory_critical,
                message=f"Utilisation mémoire critique: {metrics.memory_percent:.1f}%"
            ))
        elif metrics.memory_percent >= self.thresholds.memory_warning:
            alerts.append(Alert(
                level=AlertLevel.WARNING,
                metric="memory_percent",
                value=metrics.memory_percent,
                threshold=self.thresholds.memory_warning,
                message=f"Utilisation mémoire élevée: {metrics.memory_percent:.1f}%"
            ))
            
        # Vérifier disque
        if metrics.disk_usage_percent >= self.thresholds.disk_critical:
            alerts.append(Alert(
                level=AlertLevel.CRITICAL,
                metric="disk_usage_percent",
                value=metrics.disk_usage_percent,
                threshold=self.thresholds.disk_critical,
                message=f"Espace disque critique: {metrics.disk_usage_percent:.1f}%"
            ))
        elif metrics.disk_usage_percent >= self.thresholds.disk_warning:
            alerts.append(Alert(
                level=AlertLevel.WARNING,
                metric="disk_usage_percent",
                value=metrics.disk_usage_percent,
                threshold=self.thresholds.disk_warning,
                message=f"Espace disque faible: {metrics.disk_usage_percent:.1f}%"
            ))
            
        # Vérifier threads
        if metrics.active_threads >= self.thresholds.threads_critical:
            alerts.append(Alert(
                level=AlertLevel.CRITICAL,
                metric="active_threads",
                value=metrics.active_threads,
                threshold=self.thresholds.threads_critical,
                message=f"Nombre de threads critique: {metrics.active_threads}"
            ))
        elif metrics.active_threads >= self.thresholds.threads_warning:
            alerts.append(Alert(
                level=AlertLevel.WARNING,
                metric="active_threads",
                value=metrics.active_threads,
                threshold=self.thresholds.threads_warning,
                message=f"Nombre de threads élevé: {metrics.active_threads}"
            ))
            
        return alerts
        
    def _handle_alert(self, alert: Alert):
        """Traite une alerte générée"""
        # Stocker l'alerte
        with self._lock:
            self._alerts_history.append(alert)
            
            # Limiter l'historique des alertes
            if len(self._alerts_history) > self.max_history_size:
                self._alerts_history.pop(0)
        
        # Logger l'alerte
        if alert.level == AlertLevel.CRITICAL:
            self.logger.critical(alert.message)
        elif alert.level == AlertLevel.WARNING:
            self.logger.warning(alert.message)
        else:
            self.logger.info(alert.message)
            
        # Émettre le signal d'alerte
        if QT_AVAILABLE:
            self.alert_triggered.emit(alert)
            
        # Appeler les callbacks
        self._trigger_alert_callbacks(alert)
                
    def _trigger_alert_callbacks(self, alert: Alert):
        """Déclenche tous les callbacks d'alerte"""
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Erreur dans callback d'alerte: {e}")
                
    def _log_metrics(self, metrics: PerformanceMetrics):
        """Enregistre les métriques dans un fichier"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(metrics.to_dict()) + '\n')
        except Exception as e:
            self.logger.error(f"Erreur écriture métriques: {e}")
            
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """Retourne les métriques actuelles"""
        if not self._running:
            return self._collect_metrics()
            
        with self._lock:
            return self._metrics_history[-1] if self._metrics_history else None
            
    def get_metrics_history(self, 
                           limit: Optional[int] = None,
                           start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None) -> List[PerformanceMetrics]:
        """Retourne l'historique des métriques dans une plage de temps ou limité en nombre"""
        with self._lock:
            history = self._metrics_history.copy()
            
        # Filtrer par temps si spécifié
        if start_time or end_time:
            filtered_history = []
            for metrics in history:
                if start_time and metrics.timestamp < start_time:
                    continue
                if end_time and metrics.timestamp > end_time:
                    continue
                filtered_history.append(metrics)
            history = filtered_history
            
        # Limiter le nombre si spécifié (prendre les plus récents)
        if limit is not None and len(history) > limit:
            history = history[-limit:]
            
        return history
        
    def get_alerts_history(self, 
                          level: Optional[AlertLevel] = None,
                          start_time: Optional[datetime] = None) -> List[Alert]:
        """Retourne l'historique des alertes"""
        with self._lock:
            alerts = self._alerts_history.copy()
            
        if level or start_time:
            filtered_alerts = []
            for alert in alerts:
                if level and alert.level != level:
                    continue
                if start_time and alert.timestamp < start_time:
                    continue
                filtered_alerts.append(alert)
            return filtered_alerts
            
        return alerts
        
    def get_average_metrics(self, minutes: int = 10) -> Dict[str, float]:
        """Retourne les métriques moyennes sur une période donnée"""
        time_ago = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = self.get_metrics_history(start_time=time_ago)
        
        if not recent_metrics:
            return {}
            
        return {
            'cpu_percent': sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
            'memory_percent': sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
            'disk_usage_percent': sum(m.disk_usage_percent for m in recent_metrics) / len(recent_metrics),
            'active_threads': sum(m.active_threads for m in recent_metrics) / len(recent_metrics)
        }
        
    def get_performance_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des performances"""
        current = self.get_current_metrics()
        if not current:
            return {"status": "no_data"}
            
        # Calculer les moyennes sur les dernières 10 minutes
        ten_minutes_ago = datetime.now() - timedelta(minutes=10)
        recent_metrics = self.get_metrics_history(start_time=ten_minutes_ago)
        
        if recent_metrics:
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        else:
            avg_cpu = current.cpu_percent
            avg_memory = current.memory_percent
            
        # Compter les alertes récentes
        recent_alerts = self.get_alerts_history(start_time=ten_minutes_ago)
        alert_counts = {
            "critical": len([a for a in recent_alerts if a.level == AlertLevel.CRITICAL]),
            "warning": len([a for a in recent_alerts if a.level == AlertLevel.WARNING]),
            "info": len([a for a in recent_alerts if a.level == AlertLevel.INFO])
        }
        
        return {
            "status": "monitoring" if self._running else "stopped",
            "current_metrics": current.to_dict(),
            "averages_10min": {
                "cpu_percent": round(avg_cpu, 1),
                "memory_percent": round(avg_memory, 1)
            },
            "recent_alerts": alert_counts,
            "total_metrics_collected": len(self._metrics_history),
            "monitoring_duration": self.collection_interval * len(self._metrics_history)
        }
        
    def export_metrics(self, file_path: Path, 
                      start_time: Optional[datetime] = None,
                      end_time: Optional[datetime] = None):
        """Exporte les métriques vers un fichier JSON"""
        metrics = self.get_metrics_history(start_time, end_time)
        alerts = self.get_alerts_history(start_time=start_time)
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "period": {
                "start": start_time.isoformat() if start_time else None,
                "end": end_time.isoformat() if end_time else None
            },
            "metrics": [m.to_dict() for m in metrics],
            "alerts": [a.to_dict() for a in alerts],
            "summary": self.get_performance_summary()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"Métriques exportées vers {file_path}")
        
    def __enter__(self):
        """Support du context manager"""
        self.start_monitoring()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du context manager"""
        self.stop_monitoring()

# Instance globale pour faciliter l'utilisation
_global_monitor: Optional[PerformanceMonitor] = None

def get_performance_monitor(config: Optional[Dict[str, Any]] = None) -> PerformanceMonitor:
    """Retourne l'instance globale du moniteur de performance"""
    global _global_monitor
    if _global_monitor is None:
        if config:
            _global_monitor = initialize_performance_monitoring(config)
        else:
            _global_monitor = PerformanceMonitor()
    return _global_monitor

def initialize_performance_monitoring(config: Optional[Dict[str, Any]] = None) -> PerformanceMonitor:
    """Initialise le monitoring de performance avec une configuration"""
    global _global_monitor
    
    if config is None:
        config = {}
        
    # Extraire les paramètres de configuration
    collection_interval = config.get('collection_interval', 5.0)
    max_history_size = config.get('max_history_size', 1000)
    log_file = config.get('log_file')
    
    # Créer les seuils personnalisés si fournis
    thresholds = None
    if 'thresholds' in config:
        threshold_config = config['thresholds']
        thresholds = PerformanceThresholds(
            cpu_warning=threshold_config.get('cpu_warning', 70.0),
            cpu_critical=threshold_config.get('cpu_critical', 90.0),
            memory_warning=threshold_config.get('memory_warning', 75.0),
            memory_critical=threshold_config.get('memory_critical', 90.0),
            disk_warning=threshold_config.get('disk_warning', 80.0),
            disk_critical=threshold_config.get('disk_critical', 95.0),
            threads_warning=threshold_config.get('threads_warning', 100),
            threads_critical=threshold_config.get('threads_critical', 200)
        )
    
    # Créer le moniteur
    _global_monitor = PerformanceMonitor(
        collection_interval=collection_interval,
        max_history_size=max_history_size,
        thresholds=thresholds,
        log_file=Path(log_file) if log_file else None
    )
    
    return _global_monitor

def reset_global_monitor():
    """Réinitialise le moniteur global (utile pour les tests)"""
    global _global_monitor
    if _global_monitor is not None:
        try:
            _global_monitor.stop_monitoring()
        except Exception:
            pass  # Ignorer les erreurs lors de l'arrêt
    _global_monitor = None

def set_global_monitor(monitor: Optional[PerformanceMonitor]):
    """Définit le moniteur global (utile pour les tests avec mocks)"""
    global _global_monitor
    _global_monitor = monitor