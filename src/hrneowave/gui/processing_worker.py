#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProcessingWorker - Worker pour le traitement temps réel des données d'acquisition

Ce module implémente un worker QThread pour le traitement en temps réel
des données d'acquisition avec FFT et analyse spectrale.
"""

import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QMutex, QMutexLocker
from typing import Dict, Any, Optional, List, Tuple

try:
    from hrneowave.core.circular_buffer import create_circular_buffer, BufferConfig
    CircularBuffer = create_circular_buffer
except ImportError:
    CircularBuffer = None
    BufferConfig = None
    print("⚠️ CircularBuffer non disponible")


class LatencyMonitor:
    """Moniteur de latence pour le traitement temps réel"""
    
    def __init__(self):
        self.start_times = {}
        self.latencies = []
        self.max_latency = 0.0
        self.avg_latency = 0.0
    
    def start_measurement(self, measurement_id: str):
        """Démarre une mesure de latence"""
        self.start_times[measurement_id] = time.perf_counter()
    
    def end_measurement(self, measurement_id: str) -> float:
        """Termine une mesure de latence et retourne la durée"""
        if measurement_id in self.start_times:
            latency = time.perf_counter() - self.start_times[measurement_id]
            self.latencies.append(latency)
            
            # Garder seulement les 100 dernières mesures
            if len(self.latencies) > 100:
                self.latencies = self.latencies[-100:]
            
            self.max_latency = max(self.latencies)
            self.avg_latency = np.mean(self.latencies)
            
            del self.start_times[measurement_id]
            return latency
        return 0.0
    
    def get_stats(self) -> Dict[str, float]:
        """Retourne les statistiques de latence"""
        return {
            'max_latency': self.max_latency,
            'avg_latency': self.avg_latency,
            'current_measurements': len(self.start_times)
        }


class ProcessingWorker(QThread):
    """
    Worker pour le traitement temps réel des données d'acquisition.
    
    Signaux émis:
    - newSpectra: Nouveaux spectres calculés
    - newStats: Nouvelles statistiques
    - performanceStats: Métriques de performance
    - processingError: Erreurs de traitement
    """
    
    # Signaux PyQt
    newSpectra = pyqtSignal(dict)
    newStats = pyqtSignal(dict)
    performanceStats = pyqtSignal(dict)
    processingError = pyqtSignal(str)
    
    def __init__(self, parent, config: Dict[str, Any]):
        """
        Initialise le worker.
        
        Args:
            parent: Widget parent (généralement AcquisitionController)
            config: Configuration du traitement
        """
        super().__init__(parent)
        
        self.parent = parent
        self.config = config
        self.running = False
        self.mutex = QMutex()
        
        # Configuration par défaut
        self.sampling_rate = config.get('sample_rate', 1000.0)
        self.window_size = config.get('window_size', 1024)
        self.overlap = config.get('overlap', 0.5)
        self.update_interval = config.get('update_interval', 2.0)
        self.n_channels = config.get('n_channels', 4)
        
        # Initialiser les buffers
        self._init_buffers()
        
        # Timer pour le traitement périodique
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self.process_data)
        
        # Moniteur de latence
        self.latency_monitor = LatencyMonitor()
        
        # Métriques de performance
        self.performance_metrics = {
            'fft_time': 0.0,
            'processing_time': 0.0,
            'total_time': 0.0,
            'throughput': 0.0,
            'processed_samples': 0
        }
        
        print("✅ ProcessingWorker initialisé")
    
    def _init_buffers(self):
        """Initialise les buffers circulaires"""
        try:
            buffer_size = int(self.sampling_rate * 10)  # 10 secondes de données
            
            if CircularBuffer and BufferConfig:
                # Buffer pour le temps (1 canal)
                time_config = BufferConfig(
                    n_channels=1,
                    buffer_size=buffer_size,
                    sample_rate=self.sampling_rate
                )
                self.time_buffer = CircularBuffer(time_config)
                
                # Buffers pour les données (1 canal chacun)
                self.data_buffers = []
                for i in range(self.n_channels):
                    data_config = BufferConfig(
                        n_channels=1,
                        buffer_size=buffer_size,
                        sample_rate=self.sampling_rate
                    )
                    self.data_buffers.append(CircularBuffer(data_config))
            else:
                # Fallback vers des listes Python
                self.time_buffer = []
                self.data_buffers = [[] for _ in range(self.n_channels)]
                
        except Exception as e:
            print(f"⚠️ Erreur initialisation buffers: {e}")
            self.time_buffer = []
            self.data_buffers = [[] for _ in range(self.n_channels)]
    
    def start_processing(self):
        """Démarre le traitement en arrière-plan"""
        with QMutexLocker(self.mutex):
            if not self.running:
                self.running = True
                self.start()
                
                # Démarrer le timer de traitement
                interval_ms = int(self.update_interval * 1000)
                self.process_timer.start(interval_ms)
                
                print("🚀 ProcessingWorker démarré")
    
    def stop_processing(self):
        """Arrête le traitement"""
        with QMutexLocker(self.mutex):
            if self.running:
                self.running = False
                self.process_timer.stop()
                self.quit()
                self.wait(5000)  # Attendre max 5 secondes
                
                print("⏹️ ProcessingWorker arrêté")
    
    def run(self):
        """Boucle principale du thread"""
        print("🔄 ProcessingWorker en cours d'exécution")
        
        while self.running:
            try:
                # Récupérer les nouvelles données
                self._collect_data()
                
                # Attendre un peu avant la prochaine collecte
                self.msleep(100)  # 100ms
                
            except Exception as e:
                self.processingError.emit(f"Erreur dans la boucle principale: {e}")
                break
    
    def _collect_data(self):
        """Collecte les données depuis le parent"""
        try:
            if hasattr(self.parent, 'get_latest_data'):
                data = self.parent.get_latest_data()
                if data is not None:
                    self._add_data_to_buffers(data)
                    
        except Exception as e:
            print(f"⚠️ Erreur collecte données: {e}")
    
    def _add_data_to_buffers(self, data):
        """Ajoute les données aux buffers"""
        try:
            if isinstance(data, dict) and 'time' in data and 'channels' in data:
                time_data = data['time']
                channel_data = data['channels']
                
                # Ajouter aux buffers
                if isinstance(self.time_buffer, list):
                    self.time_buffer.extend(time_data)
                    for i, channel in enumerate(channel_data):
                        if i < len(self.data_buffers):
                            self.data_buffers[i].extend(channel)
                else:
                    # CircularBuffer
                    import numpy as np
                    if time_data:
                        time_array = np.array(time_data).reshape(-1, 1)  # Reshape pour 1 canal
                        self.time_buffer.write(time_array)
                    
                    for i, channel in enumerate(channel_data):
                        if i < len(self.data_buffers) and channel:
                            channel_array = np.array(channel).reshape(-1, 1)  # Reshape pour 1 canal
                            self.data_buffers[i].write(channel_array)
                                
        except Exception as e:
            print(f"⚠️ Erreur ajout données aux buffers: {e}")
    
    def process_data(self):
        """Traite les données disponibles"""
        try:
            self.latency_monitor.start_measurement('processing')
            
            # Récupérer les données des buffers
            if self._has_sufficient_data():
                data = self._get_processing_data()
                
                if data is not None:
                    # Calculer FFT
                    spectra = self._compute_fft(data)
                    
                    # Calculer statistiques
                    stats = self._compute_stats(data)
                    
                    # Émettre les résultats
                    if spectra:
                        self.newSpectra.emit(spectra)
                    
                    if stats:
                        self.newStats.emit(stats)
                    
                    # Métriques de performance
                    processing_time = self.latency_monitor.end_measurement('processing')
                    self.performance_metrics['processing_time'] = processing_time
                    self.performance_metrics['processed_samples'] += len(data.get('time', []))
                    
                    self.performanceStats.emit(self.performance_metrics.copy())
                    
        except Exception as e:
            self.processingError.emit(f"Erreur traitement: {e}")
    
    def _has_sufficient_data(self) -> bool:
        """Vérifie s'il y a suffisamment de données pour traiter"""
        try:
            if isinstance(self.time_buffer, list):
                return len(self.time_buffer) >= self.window_size
            else:
                return self.time_buffer.available_samples() >= self.window_size
        except:
            return False
    
    def _get_processing_data(self) -> Optional[Dict]:
        """Récupère les données pour le traitement"""
        try:
            if isinstance(self.time_buffer, list):
                # Prendre les dernières données
                time_data = self.time_buffer[-self.window_size:]
                channel_data = []
                for buffer in self.data_buffers:
                    if len(buffer) >= self.window_size:
                        channel_data.append(buffer[-self.window_size:])
                    else:
                        channel_data.append([])
            else:
                # CircularBuffer
                time_buffer_data = self.time_buffer.get_data(self.window_size)
                time_data = time_buffer_data.flatten().tolist() if time_buffer_data is not None else []
                
                channel_data = []
                for buffer in self.data_buffers:
                    buffer_data = buffer.get_data(self.window_size)
                    if buffer_data is not None:
                        channel_data.append(buffer_data.flatten().tolist())
                    else:
                        channel_data.append([])
            
            return {
                'time': time_data,
                'channels': channel_data
            }
            
        except Exception as e:
            print(f"⚠️ Erreur récupération données: {e}")
            return None
    
    def _compute_fft(self, data: Dict) -> Optional[Dict]:
        """Calcule la FFT des données"""
        try:
            self.latency_monitor.start_measurement('fft')
            
            spectra = {}
            time_data = np.array(data['time'])
            
            if len(time_data) < 2:
                return None
            
            # Calculer la fréquence d'échantillonnage
            dt = np.mean(np.diff(time_data))
            fs = 1.0 / dt if dt > 0 else self.sampling_rate
            
            for i, channel_data in enumerate(data['channels']):
                if len(channel_data) >= self.window_size:
                    # Appliquer une fenêtre
                    windowed_data = np.array(channel_data) * np.hanning(len(channel_data))
                    
                    # Calculer FFT
                    fft_result = np.fft.fft(windowed_data)
                    freqs = np.fft.fftfreq(len(windowed_data), 1/fs)
                    
                    # Prendre seulement les fréquences positives
                    positive_freqs = freqs[:len(freqs)//2]
                    positive_fft = np.abs(fft_result[:len(fft_result)//2])
                    
                    spectra[f'channel_{i}'] = {
                        'frequencies': positive_freqs.tolist(),
                        'amplitudes': positive_fft.tolist()
                    }
            
            fft_time = self.latency_monitor.end_measurement('fft')
            self.performance_metrics['fft_time'] = fft_time
            
            return spectra
            
        except Exception as e:
            print(f"⚠️ Erreur calcul FFT: {e}")
            return None
    
    def _compute_stats(self, data: Dict) -> Optional[Dict]:
        """Calcule les statistiques des données"""
        try:
            stats = {}
            
            for i, channel_data in enumerate(data['channels']):
                if len(channel_data) > 0:
                    channel_array = np.array(channel_data)
                    
                    stats[f'channel_{i}'] = {
                        'mean': float(np.mean(channel_array)),
                        'std': float(np.std(channel_array)),
                        'min': float(np.min(channel_array)),
                        'max': float(np.max(channel_array)),
                        'rms': float(np.sqrt(np.mean(channel_array**2)))
                    }
            
            return stats
            
        except Exception as e:
            print(f"⚠️ Erreur calcul statistiques: {e}")
            return None
    
    def add_data(self, time_data, channel_data):
        """Ajoute des données au worker (interface publique)"""
        data = {
            'time': time_data if isinstance(time_data, list) else [time_data],
            'channels': channel_data if isinstance(channel_data[0], list) else [channel_data]
        }
        self._add_data_to_buffers(data)
    
    def get_latency_stats(self) -> Dict[str, float]:
        """Retourne les statistiques de latence"""
        return self.latency_monitor.get_stats()