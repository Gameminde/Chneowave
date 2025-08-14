#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de graphiques optimisé pour CHNeoWave

Ce module fournit une interface de haut niveau pour la création et la gestion
de graphiques haute performance avec PyQtGraph.

Auteur: Assistant IA - Architecte Logiciel en Chef
Version: 1.0.0
Date: 2024
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Union

import numpy as np

# Import conditionnel de PyQt
try:
    from PyQt6.QtCore import QObject, QThread, QTimer, QMutex, pyqtSignal
    from PyQt6.QtWidgets import QWidget
    from PyQt6.QtCore import Qt
    QT_AVAILABLE = True
except ImportError:
    try:
        from PySide6.QtCore import QObject, QThread, QTimer, QMutex, Signal
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
        QT_AVAILABLE = True
    except ImportError:
        QT_AVAILABLE = False
        # Classes factices pour les tests
        class QObject:
            def __init__(self, parent=None): pass
        class QThread:
            def start(self): pass
            def quit(self): pass
            def wait(self, ms): pass
            def isRunning(self): return False
        class QTimer:
            def __init__(self): pass
            def timeout(self): pass
            def setSingleShot(self, single): pass
            def setInterval(self, ms): pass
            def start(self): pass
            def stop(self): pass
            def isActive(self): return False
        class QMutex:
            def __init__(self): pass
        def pyqtSignal(*args): return lambda: None
        class QWidget:
            def __init__(self, parent=None): pass
        class Qt:
            class PenStyle:
                SolidLine = 1
                DashLine = 2
                DotLine = 3
                DashDotLine = 4

try:
    # import pyqtgraph as pg
# from pyqtgraph import PlotWidget
# Utilisation de l'adaptateur matplotlib pour compatibilité PySide6
from .matplotlib_adapter import pg, PlotWidget
    PG_AVAILABLE = True
except ImportError:
    PG_AVAILABLE = False
    # Classe factice pour les tests
    class PlotWidget:
        def __init__(self, parent=None): pass
    pg = None

# Configuration du logging
logger = logging.getLogger(__name__)

# Constantes
DEFAULT_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]

@dataclass
class PlotData:
    """Structure de données pour un tracé"""
    x: np.ndarray
    y: np.ndarray
    name: str = ""
    color: str = "#1f77b4"
    line_width: float = 1.0
    style: str = "solid"  # solid, dash, dot, dashdot
    symbol: Optional[str] = None  # o, s, t, d, +, x
    symbol_size: float = 5.0
    alpha: float = 1.0
    z_order: int = 0

@dataclass
class GraphConfiguration:
    """Configuration d'un graphique"""
    title: str = ""
    x_label: str = "X"
    y_label: str = "Y"
    x_unit: str = ""
    y_unit: str = ""
    grid: bool = True
    legend: bool = True
    auto_range: bool = True
    background_color: str = "white"
    text_color: str = "black"
    
    # Paramètres de performance
    update_rate_ms: int = 50
    max_points: int = 10000
    downsample_threshold: int = 5000
    downsample_method: str = "lttb"  # lttb, uniform, peak
    
    # Paramètres d'export
    export_dpi: int = 300
    export_width: int = 1920
    export_height: int = 1080

def _ensure_qt_imports():
    """S'assure que PyQt est disponible"""
    if not QT_AVAILABLE:
        raise ImportError("PySide6 requis pour les fonctionnalités graphiques")
    if not PG_AVAILABLE:
        raise ImportError("PyQtGraph requis pour les graphiques")

class DownsamplingEngine:
    """Moteur de down-sampling pour optimiser les performances"""
    
    @staticmethod
    def uniform_downsample(x: np.ndarray, y: np.ndarray, n_out: int) -> Tuple[np.ndarray, np.ndarray]:
        """Down-sampling uniforme"""
        if len(x) <= n_out:
            return x, y
        
        indices = np.linspace(0, len(x) - 1, n_out, dtype=int)
        return x[indices], y[indices]
    
    @staticmethod
    def lttb_downsample(x: np.ndarray, y: np.ndarray, n_out: int) -> Tuple[np.ndarray, np.ndarray]:
        """Largest Triangle Three Buckets algorithm"""
        if len(x) <= n_out:
            return x, y
        
        if n_out < 3:
            return DownsamplingEngine.uniform_downsample(x, y, n_out)
        
        # Initialisation
        sampled_x = np.zeros(n_out)
        sampled_y = np.zeros(n_out)
        
        # Premier et dernier points
        sampled_x[0] = x[0]
        sampled_y[0] = y[0]
        sampled_x[-1] = x[-1]
        sampled_y[-1] = y[-1]
        
        # Taille des buckets
        bucket_size = (len(x) - 2) / (n_out - 2)
        
        a = 0  # Point précédent
        
        for i in range(1, n_out - 1):
            # Calcul des indices du bucket
            avg_range_start = int(np.floor((i - 1) * bucket_size) + 1)
            avg_range_end = int(np.floor(i * bucket_size) + 1)
            avg_range_end = min(avg_range_end, len(x))
            
            # Point moyen du bucket suivant
            avg_range_start_next = int(np.floor(i * bucket_size) + 1)
            avg_range_end_next = int(np.floor((i + 1) * bucket_size) + 1)
            avg_range_end_next = min(avg_range_end_next, len(x))
            
            if avg_range_start_next < len(x):
                avg_x = np.mean(x[avg_range_start_next:avg_range_end_next])
                avg_y = np.mean(y[avg_range_start_next:avg_range_end_next])
            else:
                avg_x = x[-1]
                avg_y = y[-1]
            
            # Trouver le point avec la plus grande aire
            max_area = -1
            max_area_point = avg_range_start
            
            for j in range(avg_range_start, avg_range_end):
                if j < len(x):
                    area = abs((x[a] - avg_x) * (y[j] - y[a]) - (x[a] - x[j]) * (avg_y - y[a]))
                    if area > max_area:
                        max_area = area
                        max_area_point = j
            
            sampled_x[i] = x[max_area_point]
            sampled_y[i] = y[max_area_point]
            a = max_area_point
        
        return sampled_x, sampled_y
    
    @staticmethod
    def peak_downsample(x: np.ndarray, y: np.ndarray, n_out: int) -> Tuple[np.ndarray, np.ndarray]:
        """Down-sampling préservant les pics"""
        if len(x) <= n_out:
            return x, y
        
        # Calcul des dérivées pour identifier les pics
        dy = np.diff(y)
        peaks = np.where(np.diff(np.sign(dy)))[0] + 1
        
        # Ajout des points de début et fin
        important_indices = np.concatenate(([0], peaks, [len(x) - 1]))
        important_indices = np.unique(important_indices)
        
        if len(important_indices) <= n_out:
            return x[important_indices], y[important_indices]
        
        # Si trop de pics, sélection des plus importants
        peak_values = np.abs(y[important_indices[1:-1]])
        peak_order = np.argsort(peak_values)[::-1]
        selected_peaks = important_indices[1:-1][peak_order[:n_out-2]]
        
        final_indices = np.concatenate(([0], selected_peaks, [len(x) - 1]))
        final_indices = np.sort(final_indices)
        
        return x[final_indices], y[final_indices]
    
    @classmethod
    def downsample(cls, x: np.ndarray, y: np.ndarray, n_out: int, method: str = "lttb") -> Tuple[np.ndarray, np.ndarray]:
        """Interface principale de down-sampling"""
        if method == "uniform":
            return cls.uniform_downsample(x, y, n_out)
        elif method == "peak":
            return cls.peak_downsample(x, y, n_out)
        else:
            return cls.lttb_downsample(x, y, n_out)  # Fallback

# Classes créées dynamiquement après import PyQt
GraphWorker = None
OptimizedPlotWidget = None

def _create_graph_classes():
    """Crée les classes PyQt dynamiquement après import"""
    global GraphWorker, OptimizedPlotWidget
    
    if GraphWorker is not None:
        return GraphWorker, OptimizedPlotWidget  # Déjà créées
    
    _ensure_qt_imports()
    
    class GraphWorker(QObject):
        """Worker thread pour le traitement des graphiques"""
        
        data_processed = pyqtSignal(str, object)  # graph_id, processed_data
        error_occurred = pyqtSignal(str, str)  # graph_id, error_message
    
        def __init__(self):
            super().__init__()
            self.processing_queue = []
            self.mutex = QMutex()
            self.executor = ThreadPoolExecutor(max_workers=2)
        
        def process_data(self, graph_id: str, plot_data: PlotData, config: GraphConfiguration):
            """
            Traite les données de graphique de manière asynchrone
            """
            future = self.executor.submit(self._process_data_sync, graph_id, plot_data, config)
            future.add_done_callback(lambda f: self._on_processing_complete(graph_id, f))
        
        def _process_data_sync(self, graph_id: str, plot_data: PlotData, config: GraphConfiguration) -> PlotData:
            """
            Traitement synchrone des données
            """
            try:
                # Copie des données pour éviter les modifications concurrentes
                x = plot_data.x.copy()
                y = plot_data.y.copy()
                
                # Validation des données
                if len(x) != len(y):
                    raise ValueError("Les arrays x et y doivent avoir la même longueur")
                
                if len(x) == 0:
                    raise ValueError("Les données ne peuvent pas être vides")
                
                # Nettoyage des données (NaN, Inf)
                valid_mask = np.isfinite(x) & np.isfinite(y)
                x = x[valid_mask]
                y = y[valid_mask]
                
                if len(x) == 0:
                    raise ValueError("Aucune donnée valide après nettoyage")
                
                # Down-sampling si nécessaire
                if len(x) > config.downsample_threshold:
                    target_points = min(config.downsample_threshold, config.max_points)
                    x, y = DownsamplingEngine.downsample(x, y, target_points, config.downsample_method)
                    logger.debug(f"Down-sampling: {len(plot_data.x)} -> {len(x)} points")
                
                # Création des données traitées
                processed_data = PlotData(
                    x=x,
                    y=y,
                    name=plot_data.name,
                    color=plot_data.color,
                    line_width=plot_data.line_width,
                    style=plot_data.style,
                    symbol=plot_data.symbol,
                    symbol_size=plot_data.symbol_size,
                    alpha=plot_data.alpha,
                    z_order=plot_data.z_order
                )
                
                return processed_data
            
            except Exception as e:
                logger.error(f"Erreur lors du traitement des données pour {graph_id}: {e}")
                raise
        
        def _on_processing_complete(self, graph_id: str, future):
            """
            Callback de fin de traitement
            """
            try:
                processed_data = future.result()
                self.data_processed.emit(graph_id, processed_data)
            except Exception as e:
                self.error_occurred.emit(graph_id, str(e))
    
    class OptimizedPlotWidget(PlotWidget):
        """Widget de graphique optimisé"""
            
        def __init__(self, config: GraphConfiguration, parent=None):
            super().__init__(parent)
            self.config = config
            self.plot_items = {}  # Stockage des éléments de tracé
            self.last_update_time = 0
            self.update_timer = QTimer()
            self.pending_updates = []
            
            self.setup_plot()
            self.setup_timer()
            
        def setup_plot(self):
            """
            Configure le graphique
            """
            # Configuration de base
            self.setBackground(self.config.background_color)
            self.showGrid(x=self.config.grid, y=self.config.grid, alpha=0.3)
            
            # Labels
            if self.config.title:
                self.setTitle(self.config.title, color=self.config.text_color)
            
            self.setLabel('left', self.config.y_label, units=self.config.y_unit, color=self.config.text_color)
            self.setLabel('bottom', self.config.x_label, units=self.config.x_unit, color=self.config.text_color)
            
            # Légende
            if self.config.legend:
                self.addLegend()
            
            # Configuration avancée
            self.getPlotItem().getViewBox().setMouseEnabled(x=True, y=True)
            self.getPlotItem().enableAutoRange()
            
            # Anti-aliasing pour de meilleurs rendus
            self.getPlotItem().setAntialiasing(True)
            
        def setup_timer(self):
            """
            Configure le timer de mise à jour
            """
            self.update_timer.timeout.connect(self.process_pending_updates)
            self.update_timer.setSingleShot(False)
            self.update_timer.setInterval(self.config.update_rate_ms)
        
        def add_plot_data(self, plot_data: PlotData, update_immediately: bool = True):
            """
            Ajoute des données de tracé
            """
            if update_immediately:
                self._add_plot_data_immediate(plot_data)
            else:
                self.pending_updates.append(('add', plot_data))
                if not self.update_timer.isActive():
                    self.update_timer.start()
        
        def _add_plot_data_immediate(self, plot_data: PlotData):
            """
            Ajoute immédiatement des données de tracé
            """
            # Conversion du style de ligne
            pen_style = Qt.PenStyle.SolidLine
            if plot_data.style == "dash":
                pen_style = Qt.PenStyle.DashLine
            elif plot_data.style == "dot":
                pen_style = Qt.PenStyle.DotLine
            elif plot_data.style == "dashdot":
                pen_style = Qt.PenStyle.DashDotLine
            
            # Création du pen
            pen = pg.mkPen(
                color=plot_data.color,
                width=plot_data.line_width,
                style=pen_style
            )
            
            # Symbole
            symbol = None
            if plot_data.symbol:
                symbol = plot_data.symbol
            
            # Création de l'élément de tracé
            plot_item = self.plot(
                plot_data.x,
                plot_data.y,
                pen=pen,
                symbol=symbol,
                symbolSize=plot_data.symbol_size,
                symbolBrush=plot_data.color,
                name=plot_data.name if plot_data.name else None
            )
            
            # Stockage pour référence future
            self.plot_items[plot_data.name] = plot_item
            
            # Auto-range si configuré
            if self.config.auto_range:
                self.autoRange()
            
        def update_plot_data(self, name: str, plot_data: PlotData, update_immediately: bool = True):
            """
            Met à jour des données de tracé existantes
            """
            if update_immediately:
                self._update_plot_data_immediate(name, plot_data)
            else:
                self.pending_updates.append(('update', name, plot_data))
                if not self.update_timer.isActive():
                    self.update_timer.start()
            
        def _update_plot_data_immediate(self, name: str, plot_data: PlotData):
            """
            Met à jour immédiatement des données de tracé
            """
            if name in self.plot_items:
                # Suppression de l'ancien tracé
                self.removeItem(self.plot_items[name])
                del self.plot_items[name]
            
            # Ajout du nouveau tracé
            self._add_plot_data_immediate(plot_data)
        
        def remove_plot_data(self, name: str):
            """
            Supprime des données de tracé
            """
            if name in self.plot_items:
                self.removeItem(self.plot_items[name])
                del self.plot_items[name]
        
        def clear_all_plots(self):
            """
            Efface tous les tracés
            """
            self.clear()
            self.plot_items.clear()
            self.pending_updates.clear()
        
        def process_pending_updates(self):
            """
            Traite les mises à jour en attente
            """
            if not self.pending_updates:
                self.update_timer.stop()
                return
            
            # Traitement par batch pour optimiser les performances
            batch_size = 5
            processed = 0
            
            while self.pending_updates and processed < batch_size:
                update = self.pending_updates.pop(0)
                
                if update[0] == 'add':
                    self._add_plot_data_immediate(update[1])
                elif update[0] == 'update':
                    self._update_plot_data_immediate(update[1], update[2])
                
                processed += 1
            
            # Arrêter le timer si plus de mises à jour
            if not self.pending_updates:
                self.update_timer.stop()
        
        def export_plot(self, file_path: str, width: int = 1920, height: int = 1080, dpi: int = 300):
            """
            Exporte le graphique
            """
            try:
                exporter = pg.exporters.ImageExporter(self.getPlotItem())
                exporter.parameters()['width'] = width
                exporter.parameters()['height'] = height
                exporter.export(file_path)
                logger.info(f"Graphique exporté: {file_path}")
            except Exception as e:
                logger.error(f"Erreur lors de l'export: {e}")
                raise
    
    # Retourner les classes créées
    return GraphWorker, OptimizedPlotWidget

# Créer les classes dynamiquement
if QT_AVAILABLE and PG_AVAILABLE:
    GraphWorker, OptimizedPlotWidget = _create_graph_classes()

class GraphManager(QObject):
    """Gestionnaire principal des graphiques"""
    
    # Signaux
    graph_updated = pyqtSignal(str)  # graph_id
    error_occurred = pyqtSignal(str, str)  # graph_id, error_message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graphs: Dict[str, OptimizedPlotWidget] = {}
        self.configurations: Dict[str, GraphConfiguration] = {}
        self.worker_thread = QThread()
        self.worker = GraphWorker()
        self.worker.moveToThread(self.worker_thread)
        
        # Connexions
        self.worker.data_processed.connect(self.on_data_processed)
        self.worker.error_occurred.connect(self.on_worker_error)
        
        # Démarrage du thread worker
        self.worker_thread.start()
        
        logger.info("GraphManager initialisé")
        
    def create_graph(self, graph_id: str, config: GraphConfiguration, parent: QWidget = None) -> OptimizedPlotWidget:
        """
        Crée un nouveau graphique
        """
        if graph_id in self.graphs:
            logger.warning(f"Graphique {graph_id} existe déjà")
            return self.graphs[graph_id]
        
        # Création du widget
        plot_widget = OptimizedPlotWidget(config, parent)
        
        # Stockage
        self.graphs[graph_id] = plot_widget
        self.configurations[graph_id] = config
        
        logger.info(f"Graphique créé: {graph_id}")
        return plot_widget
    
    def get_graph(self, graph_id: str) -> Optional[OptimizedPlotWidget]:
        """
        Récupère un graphique existant
        """
        return self.graphs.get(graph_id)
    
    def update_graph_data(self, graph_id: str, plot_data: PlotData, async_processing: bool = True):
        """
        Met à jour les données d'un graphique
        """
        if graph_id not in self.graphs:
            logger.error(f"Graphique {graph_id} non trouvé")
            return
        
        config = self.configurations[graph_id]
        
        if async_processing and len(plot_data.x) > 1000:
            # Traitement asynchrone pour les gros datasets
            self.worker.process_data(graph_id, plot_data, config)
        else:
            # Traitement synchrone pour les petits datasets
            try:
                processed_data = self.worker._process_data_sync(graph_id, plot_data, config)
                self.graphs[graph_id].add_plot_data(processed_data)
                self.graph_updated.emit(graph_id)
            except Exception as e:
                self.error_occurred.emit(graph_id, str(e))
    
    def on_data_processed(self, graph_id: str, processed_data: PlotData):
        """
        Gestionnaire de données traitées
        """
        if graph_id in self.graphs:
            self.graphs[graph_id].add_plot_data(processed_data)
            self.graph_updated.emit(graph_id)
    
    def on_worker_error(self, graph_id: str, error_message: str):
        """
        Gestionnaire d'erreur du worker
        """
        logger.error(f"Erreur worker pour {graph_id}: {error_message}")
        self.error_occurred.emit(graph_id, error_message)
    
    def clear_graph(self, graph_id: str):
        """
        Efface un graphique
        """
        if graph_id in self.graphs:
            self.graphs[graph_id].clear_all_plots()
    
    def remove_graph(self, graph_id: str):
        """
        Supprime un graphique
        """
        if graph_id in self.graphs:
            self.graphs[graph_id].deleteLater()
            del self.graphs[graph_id]
            del self.configurations[graph_id]
            logger.info(f"Graphique supprimé: {graph_id}")
    
    def export_graph(self, graph_id: str, file_path: str, **kwargs):
        """
        Exporte un graphique
        """
        if graph_id in self.graphs:
            self.graphs[graph_id].export_plot(file_path, **kwargs)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques de performance
        """
        stats = {
            'total_graphs': len(self.graphs),
            'worker_thread_active': self.worker_thread.isRunning(),
            'graphs': {}
        }
        
        for graph_id, graph in self.graphs.items():
            stats['graphs'][graph_id] = {
                'plot_items_count': len(graph.plot_items),
                'pending_updates': len(graph.pending_updates),
                'timer_active': graph.update_timer.isActive()
            }
        
        return stats
    
    def cleanup(self):
        """
        Nettoyage des ressources
        """
        # Arrêt du thread worker
        if self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait(1000)
            
        # Suppression des graphiques
        for graph_id in list(self.graphs.keys()):
            self.remove_graph(graph_id)
            
        logger.info("GraphManager nettoyé")

# Fonctions utilitaires
def create_sample_data(n_points: int = 1000, noise_level: float = 0.1) -> PlotData:
    """Crée des données d'exemple pour les tests"""
    x = np.linspace(0, 10, n_points)
    y = np.sin(x) + noise_level * np.random.randn(n_points)
    
    return PlotData(
        x=x,
        y=y,
        name="Données d'exemple",
        color="#1f77b4"
    )

def benchmark_downsampling(n_points: int = 100000, n_out: int = 1000):
    """Benchmark des méthodes de down-sampling"""
    x = np.linspace(0, 100, n_points)
    y = np.sin(x) + 0.1 * np.random.randn(n_points)
    
    methods = ["uniform", "lttb", "peak"]
    results = {}
    
    for method in methods:
        start_time = time.time()
        x_down, y_down = DownsamplingEngine.downsample(x, y, n_out, method)
        end_time = time.time()
        
        results[method] = {
            'time': end_time - start_time,
            'points_out': len(x_down),
            'compression_ratio': len(x) / len(x_down)
        }
        
        logger.info(f"{method}: {results[method]['time']:.4f}s, {results[method]['points_out']} points")
    
    return results

# Tests et exemples
if __name__ == "__main__":
    # Configuration du logging pour les tests
    logging.basicConfig(level=logging.INFO)
    
    # Test de création de données
    sample_data = create_sample_data(10000)
    logger.info(f"Données créées: {len(sample_data.x)} points")
    
    # Benchmark de down-sampling
    logger.info("Benchmark de down-sampling:")
    benchmark_results = benchmark_downsampling()
    
    # Test de configuration
    config = GraphConfiguration(
        title="Test Graph",
        x_label="Temps",
        y_label="Amplitude",
        x_unit="s",
        y_unit="V"
    )
    
    logger.info(f"Configuration créée: {config.title}")
    
    if QT_AVAILABLE and PG_AVAILABLE:
        logger.info("PyQt et PyQtGraph disponibles - Tests graphiques possibles")
    else:
        logger.warning("PyQt ou PyQtGraph non disponible - Mode test uniquement")