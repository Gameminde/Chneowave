#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Performance Widget v2.0
Widget de surveillance des performances système

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import time
import threading
from datetime import datetime, timedelta
import psutil
import gc

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QProgressBar, QFrame,
    QScrollArea, QGroupBox, QSizePolicy
)
from PySide6.QtCore import (
    Qt, QTimer, Signal, QObject, QThread,
    QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import QColor, QFont, QPalette

from .material_components import (
    MaterialCard, MaterialButton, MaterialProgressBar,
    MaterialTheme, MaterialTypography, MaterialColor
)

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types de métriques de performance"""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_USAGE = "disk_usage"
    NETWORK_IO = "network_io"
    PROCESS_COUNT = "process_count"
    THREAD_COUNT = "thread_count"
    GPU_USAGE = "gpu_usage"
    TEMPERATURE = "temperature"
    CUSTOM = "custom"

@dataclass
class PerformanceMetric:
    """Métrique de performance"""
    name: str
    value: float
    unit: str
    max_value: float = 100.0
    min_value: float = 0.0
    warning_threshold: float = 80.0
    critical_threshold: float = 95.0
    metric_type: MetricType = MetricType.CUSTOM
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @property
    def percentage(self) -> float:
        """Retourne la valeur en pourcentage"""
        if self.max_value == self.min_value:
            return 0.0
        return ((self.value - self.min_value) / (self.max_value - self.min_value)) * 100.0
    
    @property
    def status(self) -> str:
        """Retourne le statut de la métrique"""
        if self.percentage >= self.critical_threshold:
            return "critical"
        elif self.percentage >= self.warning_threshold:
            return "warning"
        else:
            return "normal"
    
    @property
    def color(self) -> str:
        """Retourne la couleur associée au statut"""
        status_colors = {
            "normal": MaterialColor.PRIMARY.value,
            "warning": MaterialColor.TERTIARY.value,
            "critical": MaterialColor.ERROR.value
        }
        return status_colors.get(self.status, MaterialColor.PRIMARY.value)

class SystemMonitor(QObject):
    """Moniteur système pour collecter les métriques"""
    
    metrics_updated = Signal(dict)  # Dict[str, PerformanceMetric]
    
    def __init__(self, update_interval: int = 1000):
        super().__init__()
        self.update_interval = update_interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.collect_metrics)
        self.enabled_metrics = set()
        self.custom_collectors = {}
        self.history = {}  # Historique des métriques
        self.max_history_size = 100
        
        # Métriques système disponibles
        self.available_metrics = {
            MetricType.CPU_USAGE: self._collect_cpu_usage,
            MetricType.MEMORY_USAGE: self._collect_memory_usage,
            MetricType.DISK_USAGE: self._collect_disk_usage,
            MetricType.NETWORK_IO: self._collect_network_io,
            MetricType.PROCESS_COUNT: self._collect_process_count,
            MetricType.THREAD_COUNT: self._collect_thread_count
        }
    
    def start_monitoring(self):
        """Démarre la surveillance"""
        if not self.timer.isActive():
            self.timer.start(self.update_interval)
            logger.info("Surveillance des performances démarrée")
    
    def stop_monitoring(self):
        """Arrête la surveillance"""
        if self.timer.isActive():
            self.timer.stop()
            logger.info("Surveillance des performances arrêtée")
    
    def enable_metric(self, metric_type: MetricType):
        """Active une métrique"""
        self.enabled_metrics.add(metric_type)
    
    def disable_metric(self, metric_type: MetricType):
        """Désactive une métrique"""
        self.enabled_metrics.discard(metric_type)
    
    def add_custom_collector(self, name: str, collector_func):
        """Ajoute un collecteur personnalisé"""
        self.custom_collectors[name] = collector_func
    
    def collect_metrics(self):
        """Collecte toutes les métriques activées"""
        metrics = {}
        
        # Métriques système
        for metric_type in self.enabled_metrics:
            if metric_type in self.available_metrics:
                try:
                    metric = self.available_metrics[metric_type]()
                    if metric:
                        metrics[metric.name] = metric
                        self._update_history(metric.name, metric)
                except Exception as e:
                    logger.error(f"Erreur lors de la collecte de {metric_type}: {e}")
        
        # Collecteurs personnalisés
        for name, collector in self.custom_collectors.items():
            try:
                metric = collector()
                if isinstance(metric, PerformanceMetric):
                    metrics[name] = metric
                    self._update_history(name, metric)
            except Exception as e:
                logger.error(f"Erreur lors de la collecte personnalisée {name}: {e}")
        
        if metrics:
            self.metrics_updated.emit(metrics)
    
    def _update_history(self, metric_name: str, metric: PerformanceMetric):
        """Met à jour l'historique d'une métrique"""
        if metric_name not in self.history:
            self.history[metric_name] = []
        
        self.history[metric_name].append(metric)
        
        # Limiter la taille de l'historique
        if len(self.history[metric_name]) > self.max_history_size:
            self.history[metric_name] = self.history[metric_name][-self.max_history_size:]
    
    def get_history(self, metric_name: str, duration_minutes: int = 10) -> List[PerformanceMetric]:
        """Retourne l'historique d'une métrique"""
        if metric_name not in self.history:
            return []
        
        cutoff_time = datetime.now() - timedelta(minutes=duration_minutes)
        return [m for m in self.history[metric_name] if m.timestamp >= cutoff_time]
    
    def _collect_cpu_usage(self) -> Optional[PerformanceMetric]:
        """Collecte l'utilisation CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            return PerformanceMetric(
                name="CPU Usage",
                value=cpu_percent,
                unit="%",
                metric_type=MetricType.CPU_USAGE,
                warning_threshold=70.0,
                critical_threshold=90.0
            )
        except Exception as e:
            logger.error(f"Erreur collecte CPU: {e}")
            return None
    
    def _collect_memory_usage(self) -> Optional[PerformanceMetric]:
        """Collecte l'utilisation mémoire"""
        try:
            memory = psutil.virtual_memory()
            return PerformanceMetric(
                name="Memory Usage",
                value=memory.percent,
                unit="%",
                metric_type=MetricType.MEMORY_USAGE,
                warning_threshold=80.0,
                critical_threshold=95.0
            )
        except Exception as e:
            logger.error(f"Erreur collecte mémoire: {e}")
            return None
    
    def _collect_disk_usage(self) -> Optional[PerformanceMetric]:
        """Collecte l'utilisation disque"""
        try:
            disk = psutil.disk_usage('/')
            return PerformanceMetric(
                name="Disk Usage",
                value=disk.percent,
                unit="%",
                metric_type=MetricType.DISK_USAGE,
                warning_threshold=85.0,
                critical_threshold=95.0
            )
        except Exception as e:
            logger.error(f"Erreur collecte disque: {e}")
            return None
    
    def _collect_network_io(self) -> Optional[PerformanceMetric]:
        """Collecte les I/O réseau"""
        try:
            net_io = psutil.net_io_counters()
            # Calcul du débit (nécessite un historique)
            total_bytes = net_io.bytes_sent + net_io.bytes_recv
            return PerformanceMetric(
                name="Network I/O",
                value=total_bytes / (1024 * 1024),  # MB
                unit="MB",
                max_value=1000.0,  # 1GB
                metric_type=MetricType.NETWORK_IO
            )
        except Exception as e:
            logger.error(f"Erreur collecte réseau: {e}")
            return None
    
    def _collect_process_count(self) -> Optional[PerformanceMetric]:
        """Collecte le nombre de processus"""
        try:
            process_count = len(psutil.pids())
            return PerformanceMetric(
                name="Process Count",
                value=process_count,
                unit="processes",
                max_value=1000.0,
                metric_type=MetricType.PROCESS_COUNT
            )
        except Exception as e:
            logger.error(f"Erreur collecte processus: {e}")
            return None
    
    def _collect_thread_count(self) -> Optional[PerformanceMetric]:
        """Collecte le nombre de threads"""
        try:
            thread_count = threading.active_count()
            return PerformanceMetric(
                name="Thread Count",
                value=thread_count,
                unit="threads",
                max_value=100.0,
                metric_type=MetricType.THREAD_COUNT
            )
        except Exception as e:
            logger.error(f"Erreur collecte threads: {e}")
            return None

class MetricWidget(MaterialCard):
    """Widget pour afficher une métrique individuelle"""
    
    def __init__(self, metric: PerformanceMetric, show_history: bool = False, parent=None):
        super().__init__(parent, clickable=show_history)
        self.metric = metric
        self.show_history = show_history
        self.history_data = []
        
        self.setup_ui()
        self.update_metric(metric)
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        # En-tête avec nom et valeur
        header_layout = QHBoxLayout()
        
        self.name_label = QLabel(self.metric.name)
        font = QFont(*MaterialTypography.LABEL_MEDIUM.value)
        self.name_label.setFont(font)
        header_layout.addWidget(self.name_label)
        
        header_layout.addStretch()
        
        self.value_label = QLabel()
        value_font = QFont(*MaterialTypography.TITLE_MEDIUM.value)
        self.value_label.setFont(value_font)
        header_layout.addWidget(self.value_label)
        
        layout.addLayout(header_layout)
        
        # Barre de progression
        self.progress_bar = MaterialProgressBar()
        self.progress_bar.setMaximumHeight(6)
        layout.addWidget(self.progress_bar)
        
        # Informations supplémentaires
        info_layout = QHBoxLayout()
        
        self.status_label = QLabel()
        status_font = QFont(*MaterialTypography.LABEL_SMALL.value)
        self.status_label.setFont(status_font)
        info_layout.addWidget(self.status_label)
        
        info_layout.addStretch()
        
        self.timestamp_label = QLabel()
        self.timestamp_label.setFont(status_font)
        info_layout.addWidget(self.timestamp_label)
        
        layout.addLayout(info_layout)
        
        self.layout.addLayout(layout)
    
    def update_metric(self, metric: PerformanceMetric):
        """Met à jour la métrique affichée"""
        self.metric = metric
        
        # Mise à jour des labels
        self.value_label.setText(f"{metric.value:.1f} {metric.unit}")
        self.status_label.setText(metric.status.upper())
        self.timestamp_label.setText(metric.timestamp.strftime("%H:%M:%S"))
        
        # Mise à jour de la barre de progression
        self.progress_bar.setValue(int(metric.percentage))
        
        # Couleurs selon le statut
        color = metric.color
        self.value_label.setStyleSheet(f"color: {color};")
        self.status_label.setStyleSheet(f"color: {color};")
        
        # Style de la barre de progression
        progress_style = f"""
        MaterialProgressBar::chunk {{
            background-color: {color};
        }}
        """
        self.progress_bar.setStyleSheet(progress_style)
    
    def add_history_point(self, metric: PerformanceMetric):
        """Ajoute un point à l'historique"""
        self.history_data.append(metric)
        if len(self.history_data) > 50:  # Limiter l'historique
            self.history_data = self.history_data[-50:]

class PerformanceWidget(QWidget):
    """Widget principal de surveillance des performances"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = MaterialTheme()
        self.monitor = SystemMonitor()
        self.metric_widgets = {}
        self.is_monitoring = False
        
        self.setup_ui()
        self.setup_connections()
        self.setup_default_metrics()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # En-tête avec contrôles
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Performance Monitor")
        title_font = QFont(*MaterialTypography.HEADLINE_SMALL.value)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Boutons de contrôle
        self.start_button = MaterialButton("Start", MaterialButton.Style.FILLED)
        self.stop_button = MaterialButton("Stop", MaterialButton.Style.OUTLINED)
        self.clear_button = MaterialButton("Clear", MaterialButton.Style.TEXT)
        
        self.stop_button.setEnabled(False)
        
        header_layout.addWidget(self.start_button)
        header_layout.addWidget(self.stop_button)
        header_layout.addWidget(self.clear_button)
        
        layout.addLayout(header_layout)
        
        # Zone de métriques avec scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.metrics_container = QWidget()
        self.metrics_layout = QGridLayout(self.metrics_container)
        self.metrics_layout.setSpacing(8)
        
        scroll_area.setWidget(self.metrics_container)
        layout.addWidget(scroll_area)
        
        # Informations système
        self.setup_system_info(layout)
    
    def setup_system_info(self, parent_layout):
        """Configure les informations système"""
        info_card = MaterialCard()
        info_layout = QVBoxLayout(info_card)
        
        info_title = QLabel("System Information")
        info_font = QFont(*MaterialTypography.TITLE_MEDIUM.value)
        info_title.setFont(info_font)
        info_layout.addWidget(info_title)
        
        # Informations système de base
        try:
            import platform
            system_info = [
                f"OS: {platform.system()} {platform.release()}",
                f"CPU: {psutil.cpu_count()} cores",
                f"Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB",
                f"Python: {platform.python_version()}"
            ]
            
            for info in system_info:
                info_label = QLabel(info)
                info_label.setFont(QFont(*MaterialTypography.BODY_SMALL.value))
                info_layout.addWidget(info_label)
        
        except Exception as e:
            error_label = QLabel(f"Error loading system info: {e}")
            info_layout.addWidget(error_label)
        
        parent_layout.addWidget(info_card)
    
    def setup_connections(self):
        """Configure les connexions de signaux"""
        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.clear_button.clicked.connect(self.clear_metrics)
        
        self.monitor.metrics_updated.connect(self.update_metrics)
    
    def setup_default_metrics(self):
        """Configure les métriques par défaut"""
        default_metrics = [
            MetricType.CPU_USAGE,
            MetricType.MEMORY_USAGE,
            MetricType.DISK_USAGE,
            MetricType.PROCESS_COUNT,
            MetricType.THREAD_COUNT
        ]
        
        for metric_type in default_metrics:
            self.monitor.enable_metric(metric_type)
    
    def start_monitoring(self):
        """Démarre la surveillance"""
        self.monitor.start_monitoring()
        self.is_monitoring = True
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        logger.info("Surveillance des performances démarrée")
    
    def stop_monitoring(self):
        """Arrête la surveillance"""
        self.monitor.stop_monitoring()
        self.is_monitoring = False
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        logger.info("Surveillance des performances arrêtée")
    
    def clear_metrics(self):
        """Efface toutes les métriques"""
        for widget in self.metric_widgets.values():
            widget.deleteLater()
        
        self.metric_widgets.clear()
        
        # Nettoyer le layout
        for i in reversed(range(self.metrics_layout.count())):
            item = self.metrics_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        
        logger.info("Métriques effacées")
    
    def update_metrics(self, metrics: Dict[str, PerformanceMetric]):
        """Met à jour l'affichage des métriques"""
        row = 0
        col = 0
        max_cols = 3
        
        for name, metric in metrics.items():
            # Vérifier que metric est bien un objet PerformanceMetric
            if not isinstance(metric, PerformanceMetric):
                logger.warning(f"Métrique invalide pour {name}: {type(metric)} - attendu PerformanceMetric")
                continue
            
            # Vérifier que la métrique a les attributs requis
            if not hasattr(metric, 'name') or not hasattr(metric, 'value'):
                logger.warning(f"Métrique incomplète pour {name}: attributs manquants")
                continue
                
            if name not in self.metric_widgets:
                # Créer un nouveau widget de métrique
                try:
                    metric_widget = MetricWidget(metric, show_history=True)
                    self.metric_widgets[name] = metric_widget
                    
                    # Ajouter au layout
                    self.metrics_layout.addWidget(metric_widget, row, col)
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                except Exception as e:
                    logger.error(f"Erreur lors de la création du widget pour {name}: {e}")
                    continue
            else:
                # Mettre à jour le widget existant
                try:
                    self.metric_widgets[name].update_metric(metric)
                    self.metric_widgets[name].add_history_point(metric)
                except Exception as e:
                    logger.error(f"Erreur lors de la mise à jour du widget {name}: {e}")
    
    def add_custom_metric(self, name: str, collector_func):
        """Ajoute une métrique personnalisée"""
        self.monitor.add_custom_collector(name, collector_func)
    
    def enable_metric(self, metric_type: MetricType):
        """Active une métrique"""
        self.monitor.enable_metric(metric_type)
    
    def disable_metric(self, metric_type: MetricType):
        """Désactive une métrique"""
        self.monitor.disable_metric(metric_type)
    
    def get_metric_history(self, metric_name: str, duration_minutes: int = 10) -> List[PerformanceMetric]:
        """Retourne l'historique d'une métrique"""
        return self.monitor.get_history(metric_name, duration_minutes)
    
    def export_metrics(self, file_path: str):
        """Exporte les métriques vers un fichier"""
        try:
            import json
            
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'metrics': {},
                'history': {}
            }
            
            # Métriques actuelles
            for name, widget in self.metric_widgets.items():
                metric = widget.metric
                export_data['metrics'][name] = {
                    'name': metric.name,
                    'value': metric.value,
                    'unit': metric.unit,
                    'percentage': metric.percentage,
                    'status': metric.status,
                    'timestamp': metric.timestamp.isoformat()
                }
            
            # Historique
            for name in self.metric_widgets.keys():
                history = self.get_metric_history(name, 60)  # 1 heure
                export_data['history'][name] = [
                    {
                        'value': m.value,
                        'timestamp': m.timestamp.isoformat()
                    } for m in history
                ]
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Métriques exportées vers {file_path}")
        
        except Exception as e:
            logger.error(f"Erreur lors de l'export: {e}")
            raise
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        
        # Appliquer le thème aux widgets enfants
        for widget in self.metric_widgets.values():
            widget.set_theme(theme)
    
    def closeEvent(self, event):
        """Gestionnaire de fermeture"""
        if self.is_monitoring:
            self.stop_monitoring()
        event.accept()

# Fonctions utilitaires
def create_memory_collector() -> PerformanceMetric:
    """Collecteur de mémoire Python"""
    import sys
    
    # Mémoire utilisée par le processus Python
    process = psutil.Process()
    memory_mb = process.memory_info().rss / (1024 * 1024)
    
    return PerformanceMetric(
        name="Python Memory",
        value=memory_mb,
        unit="MB",
        max_value=1024.0,  # 1GB
        warning_threshold=70.0,
        critical_threshold=90.0
    )

def create_gc_collector() -> PerformanceMetric:
    """Collecteur de garbage collection"""
    gc_stats = gc.get_stats()
    total_collections = sum(stat['collections'] for stat in gc_stats)
    
    return PerformanceMetric(
        name="GC Collections",
        value=total_collections,
        unit="collections",
        max_value=1000.0,
        metric_type=MetricType.CUSTOM
    )

def create_thread_collector() -> PerformanceMetric:
    """Collecteur de threads actifs"""
    active_threads = threading.active_count()
    
    return PerformanceMetric(
        name="Active Threads",
        value=active_threads,
        unit="threads",
        max_value=50.0,
        warning_threshold=80.0,
        critical_threshold=95.0
    )

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    # Test du PerformanceWidget
    window = QMainWindow()
    performance_widget = PerformanceWidget()
    
    # Ajout de collecteurs personnalisés
    performance_widget.add_custom_metric("python_memory", lambda: create_memory_collector())
    performance_widget.add_custom_metric("gc_collections", lambda: create_gc_collector())
    performance_widget.add_custom_metric("active_threads", lambda: create_thread_collector())
    
    window.setCentralWidget(performance_widget)
    window.setWindowTitle("CHNeoWave - Performance Monitor")
    window.resize(800, 600)
    window.show()
    
    # Démarrage automatique de la surveillance
    performance_widget.start_monitoring()
    
    sys.exit(app.exec())