"""Worker optimisé pour le traitement en temps réel des données d'acquisition.

Ce module implémente un QThread optimisé pour le traitement des données
avec FFT et analyse Goda, incluant des mécanismes de repli pour les imports.
"""

import time
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

try:
    from PySide6.QtCore import QThread, Signal, QTimer
except ImportError:
    from PySide6.QtCore import QThread, Signal, QTimer

import numpy as np

# Imports avec mécanisme de repli
try:
    from src.hrneowave.core.optimized_fft_processor import OptimizedFFTProcessor
except ImportError:
    OptimizedFFTProcessor = None

try:
    from src.hrneowave.core.optimized_goda_analyzer import OptimizedGodaAnalyzer
except ImportError:
    OptimizedGodaAnalyzer = None

try:
    from hrneowave.core.circular_buffer import CircularBuffer
except ImportError:
    CircularBuffer = None

try:
    from src.hrneowave.config.optimization_config import CHNeoWaveOptimizationConfig
except ImportError:
    CHNeoWaveOptimizationConfig = None


@dataclass
class ProcessingStats:
    """Statistiques de traitement."""
    processing_time: float = 0.0
    fft_time: float = 0.0
    goda_time: float = 0.0
    buffer_usage: float = 0.0
    samples_processed: int = 0
    errors_count: int = 0


class OptimizedProcessingWorker(QThread):
    """Worker optimisé pour le traitement en temps réel.
    
    Ce worker gère le traitement des données d'acquisition avec:
    - FFT optimisée
    - Analyse Goda
    - Buffer circulaire
    - Métriques de performance
    """
    
    # Signaux PyQt
    newSpectra = Signal(np.ndarray)  # Nouveau spectre FFT
    newStats = Signal(dict)  # Nouvelles statistiques Goda
    performanceStats = Signal(dict)  # Métriques de performance
    processingError = Signal(str)  # Erreurs de traitement
    
    def __init__(self, parent, config: Optional[Any] = None):
        """Initialise le worker optimisé.
        
        Args:
            parent: Widget parent
            config: Configuration d'optimisation
        """
        super().__init__(parent)
        self.parent = parent
        self.config = config or (CHNeoWaveOptimizationConfig() if CHNeoWaveOptimizationConfig else None)
        
        # Composants de traitement
        self.fft_processor = None
        self.goda_analyzer = None
        self.circular_buffer = None
        
        # État du worker
        self.is_running = False
        self.data_queue = []
        self.stats = ProcessingStats()
        
        # Timer pour les métriques
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self._emit_performance_stats)
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
        # Initialisation des composants
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialise les composants de traitement."""
        try:
            # FFT Processor
            if OptimizedFFTProcessor and self.config:
                self.fft_processor = OptimizedFFTProcessor(self.config.fft)
            
            # Goda Analyzer
            if OptimizedGodaAnalyzer and self.config:
                self.goda_analyzer = OptimizedGodaAnalyzer(self.config.goda)
            
            # Circular Buffer
            if CircularBuffer and self.config:
                buffer_size = getattr(self.config.buffer, 'size', 8192)
                self.circular_buffer = CircularBuffer(buffer_size)
                
        except Exception as e:
            self.logger.error(f"Erreur initialisation composants: {e}")
            self.processingError.emit(f"Erreur initialisation: {e}")
    
    def start_processing(self):
        """Démarre le traitement."""
        if not self.is_running:
            self.is_running = True
            self.start()
            self.metrics_timer.start(1000)  # Métriques chaque seconde
            self.logger.info("Traitement démarré")
    
    def stop_processing(self):
        """Arrête le traitement."""
        if self.is_running:
            self.is_running = False
            self.metrics_timer.stop()
            self.quit()
            self.wait()
            self.logger.info("Traitement arrêté")
    
    def add_data(self, data: np.ndarray):
        """Ajoute des données à traiter.
        
        Args:
            data: Données à traiter
        """
        if self.is_running and len(self.data_queue) < 100:  # Limite la queue
            self.data_queue.append(data.copy())
    
    def run(self):
        """Boucle principale du worker."""
        self.logger.info("Worker démarré")
        
        while self.is_running:
            try:
                if self.data_queue:
                    data = self.data_queue.pop(0)
                    self._process_data(data)
                else:
                    self.msleep(1)  # Attente courte si pas de données
                    
            except Exception as e:
                self.logger.error(f"Erreur dans run(): {e}")
                self.processingError.emit(f"Erreur traitement: {e}")
                self.stats.errors_count += 1
        
        self.logger.info("Worker arrêté")
    
    def _process_data(self, data: np.ndarray):
        """Traite un bloc de données.
        
        Args:
            data: Données à traiter
        """
        start_time = time.perf_counter()
        
        try:
            # Ajout au buffer circulaire
            if self.circular_buffer:
                self.circular_buffer.add_data(data)
                self.stats.buffer_usage = self.circular_buffer.get_usage_percentage()
            
            # Traitement FFT
            fft_start = time.perf_counter()
            if self.fft_processor:
                spectrum = self.fft_processor.process(data)
                self.newSpectra.emit(spectrum)
            else:
                # FFT basique de repli
                spectrum = np.abs(np.fft.fft(data))
                self.newSpectra.emit(spectrum)
            
            self.stats.fft_time = time.perf_counter() - fft_start
            
            # Analyse Goda
            goda_start = time.perf_counter()
            if self.goda_analyzer:
                goda_stats = self.goda_analyzer.analyze(data)
                self.newStats.emit(goda_stats)
            else:
                # Statistiques basiques de repli
                basic_stats = {
                    'mean': float(np.mean(data)),
                    'std': float(np.std(data)),
                    'max': float(np.max(data)),
                    'min': float(np.min(data))
                }
                self.newStats.emit(basic_stats)
            
            self.stats.goda_time = time.perf_counter() - goda_start
            
            # Mise à jour des statistiques
            self.stats.processing_time = time.perf_counter() - start_time
            self.stats.samples_processed += len(data)
            
        except Exception as e:
            self.logger.error(f"Erreur traitement données: {e}")
            self.processingError.emit(f"Erreur traitement: {e}")
            self.stats.errors_count += 1
    
    def _emit_performance_stats(self):
        """Émet les statistiques de performance."""
        try:
            perf_stats = {
                'processing_time_ms': self.stats.processing_time * 1000,
                'fft_time_ms': self.stats.fft_time * 1000,
                'goda_time_ms': self.stats.goda_time * 1000,
                'buffer_usage_percent': self.stats.buffer_usage,
                'samples_processed': self.stats.samples_processed,
                'errors_count': self.stats.errors_count,
                'queue_size': len(self.data_queue)
            }
            
            self.performanceStats.emit(perf_stats)
            
        except Exception as e:
            self.logger.error(f"Erreur émission stats: {e}")
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques actuelles.
        
        Returns:
            Dictionnaire des statistiques
        """
        return {
            'processing_time_ms': self.stats.processing_time * 1000,
            'fft_time_ms': self.stats.fft_time * 1000,
            'goda_time_ms': self.stats.goda_time * 1000,
            'buffer_usage_percent': self.stats.buffer_usage,
            'samples_processed': self.stats.samples_processed,
            'errors_count': self.stats.errors_count,
            'is_running': self.is_running,
            'queue_size': len(self.data_queue)
        }
    
    def reset_stats(self):
        """Remet à zéro les statistiques."""
        self.stats = ProcessingStats()
        self.logger.info("Statistiques remises à zéro")