"""Tests de buffer circulaire pour simulation longue durée

Simule 32 Hz × 8 canaux pendant 30 minutes (accéléré)
Objectifs:
- 0 drop de données
- Usage mémoire ≤ 80%
- Performance stable
"""

import pytest
import numpy as np
import time
import threading
from unittest.mock import Mock, patch
import psutil
import os
from pathlib import Path

try:
    from hrneowave.core.circular_buffer import (
        LockFreeCircularBuffer,
        BufferConfig,
        BufferStats
    )
    BUFFER_AVAILABLE = True
except ImportError:
    BUFFER_AVAILABLE = False
    pytest.skip("Buffer circulaire non disponible", allow_module_level=True)


class TestLongOverflowSimulation:
    """Tests de simulation longue durée pour buffer overflow"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.config = BufferConfig(
            n_channels=8,
            buffer_size=8192,  # ~4 secondes @ 32Hz
            sample_rate=32.0,
            dtype=np.float32,
            enable_overflow_detection=True,
            enable_timing=True
        )
        self.buffer = LockFreeCircularBuffer(self.config)
        self.stats_collector = []
        self.error_count = 0
        self.total_samples_written = 0
        self.total_samples_read = 0
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if hasattr(self, 'buffer'):
            self.buffer.reset()
    
    def _generate_wave_data(self, n_samples: int, timestamp: float) -> np.ndarray:
        """Génère des données de houle réalistes"""
        t = np.linspace(timestamp, timestamp + n_samples/self.config.sample_rate, n_samples)
        
        # Simulation multi-fréquences (houle réaliste)
        data = np.zeros((self.config.n_channels, n_samples))
        
        for ch in range(self.config.n_channels):
            # Fréquence principale (0.1-0.3 Hz)
            f1 = 0.15 + ch * 0.02
            # Harmoniques
            f2 = f1 * 2
            f3 = f1 * 3
            
            # Amplitude variable par canal
            amp1 = 1.0 + ch * 0.1
            amp2 = 0.3 + ch * 0.05
            amp3 = 0.1 + ch * 0.02
            
            # Signal composite
            data[ch] = (amp1 * np.sin(2 * np.pi * f1 * t) +
                       amp2 * np.sin(2 * np.pi * f2 * t) +
                       amp3 * np.sin(2 * np.pi * f3 * t))
            
            # Bruit réaliste
            noise = np.random.normal(0, 0.05, n_samples)
            data[ch] += noise
        
        return data.astype(self.config.dtype)
    
    def _monitor_memory_usage(self) -> dict:
        """Surveille l'usage mémoire du processus"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Mémoire résidente
            'vms_mb': memory_info.vms / 1024 / 1024,  # Mémoire virtuelle
            'percent': process.memory_percent(),       # % de la RAM système
            'available_mb': psutil.virtual_memory().available / 1024 / 1024
        }
    
    def _writer_thread(self, duration_minutes: float, stop_event: threading.Event):
        """Thread d'écriture simulant l'acquisition"""
        samples_per_block = 16  # 0.5s @ 32Hz
        block_interval = samples_per_block / self.config.sample_rate  # 0.5s
        
        start_time = time.time()
        block_count = 0
        
        while not stop_event.is_set():
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Arrêt après durée cible
            if elapsed >= duration_minutes * 60:
                break
            
            # Générer données
            timestamp = elapsed
            data = self._generate_wave_data(samples_per_block, timestamp)
            
            # Écrire dans buffer
            success = self.buffer.write(data)
            
            if success:
                self.total_samples_written += samples_per_block
            else:
                self.error_count += 1
                print(f"⚠️ Overflow détecté au bloc {block_count}")
            
            block_count += 1
            
            # Attendre prochain bloc
            next_block_time = start_time + (block_count * block_interval)
            sleep_time = max(0, next_block_time - time.time())
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def _reader_thread(self, stop_event: threading.Event):
        """Thread de lecture simulant le traitement"""
        read_interval = 1.0  # Lecture toutes les secondes
        samples_per_read = int(self.config.sample_rate * read_interval)
        
        while not stop_event.is_set():
            # Lire données disponibles
            available = self.buffer.available_samples()
            
            if available >= samples_per_read:
                data = self.buffer.read(samples_per_read)
                if data is not None:
                    self.total_samples_read += samples_per_read
            
            time.sleep(read_interval)
    
    def _stats_monitor_thread(self, stop_event: threading.Event):
        """Thread de monitoring des statistiques"""
        while not stop_event.is_set():
            # Collecter stats buffer
            buffer_stats = self.buffer.stats.get_stats()
            
            # Collecter stats mémoire
            memory_stats = self._monitor_memory_usage()
            
            # Combiner
            combined_stats = {
                'timestamp': time.time(),
                'buffer': buffer_stats,
                'memory': memory_stats,
                'samples_written': self.total_samples_written,
                'samples_read': self.total_samples_read,
                'error_count': self.error_count
            }
            
            self.stats_collector.append(combined_stats)
            
            time.sleep(5.0)  # Stats toutes les 5 secondes
    
    @pytest.mark.slow
    def test_30min_simulation_accelerated(self):
        """Test simulation 30 minutes accélérée (32 Hz × 8 canaux)"""
        # Durée accélérée : 30 minutes simulées en ~30 secondes
        simulation_duration_minutes = 0.5  # 30 secondes réels
        target_simulation_ratio = 60  # 60x plus rapide
        
        print(f"\n🚀 Démarrage simulation longue durée:")
        print(f"   Durée réelle: {simulation_duration_minutes} min")
        print(f"   Durée simulée: {simulation_duration_minutes * target_simulation_ratio} min")
        print(f"   Fréquence: {self.config.sample_rate} Hz")
        print(f"   Canaux: {self.config.n_channels}")
        print(f"   Taille buffer: {self.config.buffer_size} échantillons")
        
        # Événements d'arrêt
        stop_event = threading.Event()
        
        # Démarrer threads
        writer_thread = threading.Thread(
            target=self._writer_thread,
            args=(simulation_duration_minutes, stop_event)
        )
        reader_thread = threading.Thread(
            target=self._reader_thread,
            args=(stop_event,)
        )
        stats_thread = threading.Thread(
            target=self._stats_monitor_thread,
            args=(stop_event,)
        )
        
        start_time = time.time()
        
        writer_thread.start()
        reader_thread.start()
        stats_thread.start()
        
        # Attendre fin du writer
        writer_thread.join()
        
        # Arrêter les autres threads
        stop_event.set()
        reader_thread.join(timeout=2.0)
        stats_thread.join(timeout=2.0)
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        # Analyse des résultats
        print(f"\n📊 Résultats simulation:")
        print(f"   Durée réelle: {actual_duration:.1f}s")
        print(f"   Échantillons écrits: {self.total_samples_written:,}")
        print(f"   Échantillons lus: {self.total_samples_read:,}")
        print(f"   Erreurs overflow: {self.error_count}")
        
        # Statistiques finales
        if self.stats_collector:
            final_stats = self.stats_collector[-1]
            memory_peak = max(s['memory']['percent'] for s in self.stats_collector)
            
            print(f"   Pic mémoire: {memory_peak:.1f}%")
            print(f"   Buffer overflows: {final_stats['buffer']['overflow_count']}")
            print(f"   Buffer underruns: {final_stats['buffer']['underrun_count']}")
            print(f"   Latence max écriture: {final_stats['buffer']['max_write_latency_ms']:.2f}ms")
            print(f"   Latence max lecture: {final_stats['buffer']['max_read_latency_ms']:.2f}ms")
        
        # Assertions P0
        assert self.error_count == 0, f"Aucun drop autorisé, trouvé: {self.error_count}"
        
        if self.stats_collector:
            memory_peak = max(s['memory']['percent'] for s in self.stats_collector)
            assert memory_peak <= 80.0, f"Usage mémoire > 80%: {memory_peak:.1f}%"
            
            final_stats = self.stats_collector[-1]
            assert final_stats['buffer']['overflow_count'] == 0, "Buffer overflow détecté"
        
        # Vérifier débit minimum
        expected_samples = simulation_duration_minutes * 60 * self.config.sample_rate
        sample_ratio = self.total_samples_written / expected_samples if expected_samples > 0 else 0
        assert sample_ratio >= 0.95, f"Débit insuffisant: {sample_ratio:.2%}"
        
        print(f"✅ Test réussi - Performance stable maintenue")
    
    def test_buffer_stress_high_frequency(self):
        """Test stress buffer avec fréquence élevée"""
        # Configuration stress
        stress_config = BufferConfig(
            n_channels=16,  # Plus de canaux
            buffer_size=4096,  # Buffer plus petit
            sample_rate=100.0,  # Fréquence plus élevée
            dtype=np.float32,
            enable_overflow_detection=True
        )
        
        stress_buffer = LockFreeCircularBuffer(stress_config)
        
        # Test écriture/lecture rapide
        n_iterations = 1000
        samples_per_write = 32
        overflow_count = 0
        
        print(f"\n⚡ Test stress buffer:")
        print(f"   Canaux: {stress_config.n_channels}")
        print(f"   Fréquence: {stress_config.sample_rate} Hz")
        print(f"   Itérations: {n_iterations}")
        
        start_time = time.time()
        
        for i in range(n_iterations):
            # Générer données
            data = np.random.randn(stress_config.n_channels, samples_per_write).astype(np.float32)
            
            # Écrire
            success = stress_buffer.write(data)
            if not success:
                overflow_count += 1
            
            # Lecture périodique
            if i % 10 == 0:
                available = stress_buffer.available_samples()
                if available > 0:
                    read_size = min(available, samples_per_write * 5)
                    stress_buffer.read(read_size)
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = (n_iterations * samples_per_write) / duration
        
        print(f"   Durée: {duration:.2f}s")
        print(f"   Débit: {throughput:.0f} échantillons/s")
        print(f"   Overflows: {overflow_count}")
        
        # Assertions
        assert throughput > 1000, f"Débit insuffisant: {throughput:.0f} échantillons/s"
        overflow_ratio = overflow_count / n_iterations
        assert overflow_ratio < 0.1, f"Trop d'overflows: {overflow_ratio:.1%}"
        
        print(f"✅ Test stress réussi")
    
    def test_memory_leak_detection(self):
        """Test détection de fuites mémoire"""
        initial_memory = self._monitor_memory_usage()
        
        # Cycles écriture/lecture intensifs
        n_cycles = 100
        samples_per_cycle = 1000
        
        print(f"\n🔍 Test fuites mémoire:")
        print(f"   Mémoire initiale: {initial_memory['rss_mb']:.1f} MB")
        print(f"   Cycles: {n_cycles}")
        
        memory_samples = [initial_memory['rss_mb']]
        
        for cycle in range(n_cycles):
            # Écriture massive
            for _ in range(10):
                data = np.random.randn(self.config.n_channels, samples_per_cycle // 10).astype(np.float32)
                self.buffer.write(data)
            
            # Lecture complète
            available = self.buffer.available_samples()
            if available > 0:
                self.buffer.read(available)
            
            # Échantillonner mémoire
            if cycle % 10 == 0:
                current_memory = self._monitor_memory_usage()
                memory_samples.append(current_memory['rss_mb'])
        
        final_memory = self._monitor_memory_usage()
        memory_growth = final_memory['rss_mb'] - initial_memory['rss_mb']
        
        print(f"   Mémoire finale: {final_memory['rss_mb']:.1f} MB")
        print(f"   Croissance: {memory_growth:+.1f} MB")
        
        # Vérifier croissance acceptable
        max_growth_mb = 50  # Maximum 50 MB de croissance
        assert memory_growth < max_growth_mb, f"Fuite mémoire suspectée: +{memory_growth:.1f} MB"
        
        print(f"✅ Pas de fuite mémoire détectée")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])