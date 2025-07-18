"""Tests de performance pour modules optimisés

Objectifs:
- FFT optimisée ≥ 2x plus rapide
- Analyse Goda ≥ 1.5x plus rapide
- Buffer lock-free ≥ 3x plus rapide
- Validation précision numérique
"""

import pytest
import numpy as np
import time
from typing import Dict, Any, Tuple
import warnings
from pathlib import Path

# Imports modules optimisés
try:
    from hrneowave.core.optimized_fft_processor import OptimizedFFTProcessor
    from hrneowave.core.optimized_goda_analyzer import OptimizedGodaAnalyzer
    from hrneowave.core.lock_free_circular_buffer import LockFreeCircularBuffer
    from hrneowave.core.buffer_config import BufferConfig
    OPTIMIZED_AVAILABLE = True
except ImportError as e:
    OPTIMIZED_AVAILABLE = False
    pytest.skip(f"Modules optimisés non disponibles: {e}", allow_module_level=True)

# Imports modules de référence (si disponibles)
try:
    from hrneowave.analysis.fft_processor import FFTProcessor
    from hrneowave.analysis.goda_analyzer import GodaAnalyzer
    from hrneowave.core.circular_buffer import CircularBuffer
    REFERENCE_AVAILABLE = True
except ImportError:
    REFERENCE_AVAILABLE = False


class PerformanceBenchmark:
    """Classe utilitaire pour benchmarks de performance"""
    
    @staticmethod
    def time_function(func, *args, **kwargs) -> Tuple[Any, float]:
        """Mesure le temps d'exécution d'une fonction"""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return result, end_time - start_time
    
    @staticmethod
    def generate_wave_signal(n_samples: int, sample_rate: float, n_channels: int = 1) -> np.ndarray:
        """Génère un signal de houle réaliste pour tests"""
        t = np.linspace(0, n_samples / sample_rate, n_samples)
        
        # Fréquences typiques de houle (0.05 - 0.5 Hz)
        frequencies = [0.1, 0.15, 0.25, 0.35]
        amplitudes = [2.0, 1.5, 1.0, 0.5]
        
        signal = np.zeros((n_channels, n_samples))
        
        for ch in range(n_channels):
            channel_signal = np.zeros(n_samples)
            
            for freq, amp in zip(frequencies, amplitudes):
                # Variation par canal
                freq_var = freq * (1 + ch * 0.1)
                amp_var = amp * (1 + ch * 0.05)
                
                channel_signal += amp_var * np.sin(2 * np.pi * freq_var * t)
            
            # Ajout bruit réaliste
            noise = np.random.normal(0, 0.1, n_samples)
            signal[ch] = channel_signal + noise
        
        return signal.astype(np.float32)
    
    @staticmethod
    def compare_results(result1: np.ndarray, result2: np.ndarray, tolerance: float = 1e-5) -> bool:
        """Compare deux résultats numériques avec tolérance"""
        if result1.shape != result2.shape:
            return False
        
        # Utiliser allclose pour comparaison robuste
        return np.allclose(result1, result2, rtol=tolerance, atol=tolerance)


class TestOptimizedFFTProcessor:
    """Tests de performance pour FFT optimisée"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.sample_rate = 32.0
        self.window_size = 2048
        self.overlap = 0.5
        
        # Processeur optimisé
        self.optimized_fft = OptimizedFFTProcessor(
            sample_rate=self.sample_rate,
            window_size=self.window_size,
            overlap=self.overlap
        )
        
        # Processeur de référence (si disponible)
        if REFERENCE_AVAILABLE:
            self.reference_fft = FFTProcessor(
                sample_rate=self.sample_rate,
                window_size=self.window_size,
                overlap=self.overlap
            )
    
    @pytest.mark.performance
    def test_fft_speed_improvement(self):
        """Test amélioration vitesse FFT (objectif: ≥ 2x)"""
        # Générer signal test
        n_samples = 32768  # ~17 minutes @ 32Hz
        signal = PerformanceBenchmark.generate_wave_signal(n_samples, self.sample_rate)
        
        print(f"\n⚡ Test performance FFT:")
        print(f"   Échantillons: {n_samples:,}")
        print(f"   Fréquence: {self.sample_rate} Hz")
        print(f"   Fenêtre: {self.window_size}")
        
        # Benchmark FFT optimisée
        result_opt, time_opt = PerformanceBenchmark.time_function(
            self.optimized_fft.compute_spectrum, signal[0]
        )
        
        print(f"   FFT optimisée: {time_opt:.3f}s")
        
        # Benchmark FFT référence (si disponible)
        if REFERENCE_AVAILABLE:
            result_ref, time_ref = PerformanceBenchmark.time_function(
                self.reference_fft.compute_spectrum, signal[0]
            )
            
            print(f"   FFT référence: {time_ref:.3f}s")
            
            # Calculer amélioration
            speedup = time_ref / time_opt if time_opt > 0 else float('inf')
            print(f"   Amélioration: {speedup:.1f}x")
            
            # Vérifier précision
            precision_ok = PerformanceBenchmark.compare_results(
                result_opt['magnitude'], result_ref['magnitude'], tolerance=1e-4
            )
            
            print(f"   Précision: {'✅' if precision_ok else '❌'}")
            
            # Assertions
            assert speedup >= 2.0, f"Amélioration insuffisante: {speedup:.1f}x < 2.0x"
            assert precision_ok, "Perte de précision détectée"
        else:
            # Test performance absolue
            throughput = n_samples / time_opt
            min_throughput = 50000  # 50k échantillons/s minimum
            
            print(f"   Débit: {throughput:.0f} échantillons/s")
            assert throughput >= min_throughput, f"Débit insuffisant: {throughput:.0f} < {min_throughput}"
        
        print(f"✅ Test FFT réussi")
    
    @pytest.mark.performance
    def test_fft_memory_efficiency(self):
        """Test efficacité mémoire FFT"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Mémoire initiale
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Test avec signal volumineux
        n_samples = 65536  # ~34 minutes @ 32Hz
        signal = PerformanceBenchmark.generate_wave_signal(n_samples, self.sample_rate)
        
        # Traitement FFT
        for _ in range(10):  # Répéter pour détecter fuites
            result = self.optimized_fft.compute_spectrum(signal[0])
            del result  # Forcer libération
        
        # Mémoire finale
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_growth = final_memory - initial_memory
        
        print(f"\n💾 Test mémoire FFT:")
        print(f"   Mémoire initiale: {initial_memory:.1f} MB")
        print(f"   Mémoire finale: {final_memory:.1f} MB")
        print(f"   Croissance: {memory_growth:+.1f} MB")
        
        # Vérifier croissance acceptable
        max_growth = 100  # Maximum 100 MB
        assert memory_growth < max_growth, f"Consommation mémoire excessive: +{memory_growth:.1f} MB"
        
        print(f"✅ Efficacité mémoire validée")


class TestOptimizedGodaAnalyzer:
    """Tests de performance pour analyse Goda optimisée"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.sample_rate = 32.0
        
        # Analyseur optimisé
        self.optimized_goda = OptimizedGodaAnalyzer(sample_rate=self.sample_rate)
        
        # Analyseur de référence (si disponible)
        if REFERENCE_AVAILABLE:
            self.reference_goda = GodaAnalyzer(sample_rate=self.sample_rate)
    
    @pytest.mark.performance
    def test_goda_speed_improvement(self):
        """Test amélioration vitesse Goda (objectif: ≥ 1.5x)"""
        # Générer signal test
        n_samples = 16384  # ~8.5 minutes @ 32Hz
        signal = PerformanceBenchmark.generate_wave_signal(n_samples, self.sample_rate)
        
        print(f"\n🌊 Test performance Goda:")
        print(f"   Échantillons: {n_samples:,}")
        print(f"   Fréquence: {self.sample_rate} Hz")
        
        # Benchmark Goda optimisé
        result_opt, time_opt = PerformanceBenchmark.time_function(
            self.optimized_goda.analyze, signal[0]
        )
        
        print(f"   Goda optimisé: {time_opt:.3f}s")
        
        # Benchmark Goda référence (si disponible)
        if REFERENCE_AVAILABLE:
            result_ref, time_ref = PerformanceBenchmark.time_function(
                self.reference_goda.analyze, signal[0]
            )
            
            print(f"   Goda référence: {time_ref:.3f}s")
            
            # Calculer amélioration
            speedup = time_ref / time_opt if time_opt > 0 else float('inf')
            print(f"   Amélioration: {speedup:.1f}x")
            
            # Vérifier précision des paramètres clés
            precision_checks = [
                ('Hs', result_opt.get('Hs', 0), result_ref.get('Hs', 0)),
                ('Tp', result_opt.get('Tp', 0), result_ref.get('Tp', 0)),
                ('Tm', result_opt.get('Tm', 0), result_ref.get('Tm', 0))
            ]
            
            precision_ok = True
            for param, val_opt, val_ref in precision_checks:
                if abs(val_opt - val_ref) > 0.01 * abs(val_ref):  # 1% tolérance
                    precision_ok = False
                    print(f"   ❌ {param}: {val_opt:.3f} vs {val_ref:.3f}")
                else:
                    print(f"   ✅ {param}: {val_opt:.3f}")
            
            # Assertions
            assert speedup >= 1.5, f"Amélioration insuffisante: {speedup:.1f}x < 1.5x"
            assert precision_ok, "Perte de précision détectée"
        else:
            # Test performance absolue
            throughput = n_samples / time_opt
            min_throughput = 10000  # 10k échantillons/s minimum
            
            print(f"   Débit: {throughput:.0f} échantillons/s")
            assert throughput >= min_throughput, f"Débit insuffisant: {throughput:.0f} < {min_throughput}"
        
        print(f"✅ Test Goda réussi")
    
    @pytest.mark.performance
    def test_goda_batch_processing(self):
        """Test traitement par lots Goda"""
        # Générer plusieurs signaux
        n_signals = 10
        n_samples = 8192
        signals = []
        
        for i in range(n_signals):
            signal = PerformanceBenchmark.generate_wave_signal(n_samples, self.sample_rate)
            signals.append(signal[0])
        
        print(f"\n📦 Test traitement par lots Goda:")
        print(f"   Signaux: {n_signals}")
        print(f"   Échantillons/signal: {n_samples:,}")
        
        # Test traitement séquentiel
        start_time = time.perf_counter()
        results_sequential = []
        for signal in signals:
            result = self.optimized_goda.analyze(signal)
            results_sequential.append(result)
        sequential_time = time.perf_counter() - start_time
        
        print(f"   Séquentiel: {sequential_time:.3f}s")
        
        # Test traitement par lots (si supporté)
        if hasattr(self.optimized_goda, 'analyze_batch'):
            start_time = time.perf_counter()
            results_batch = self.optimized_goda.analyze_batch(signals)
            batch_time = time.perf_counter() - start_time
            
            print(f"   Par lots: {batch_time:.3f}s")
            
            # Calculer amélioration
            speedup = sequential_time / batch_time if batch_time > 0 else float('inf')
            print(f"   Amélioration: {speedup:.1f}x")
            
            assert speedup >= 1.2, f"Amélioration par lots insuffisante: {speedup:.1f}x"
        
        print(f"✅ Test traitement par lots réussi")


class TestLockFreeCircularBuffer:
    """Tests de performance pour buffer circulaire lock-free"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.config = BufferConfig(
            n_channels=8,
            buffer_size=8192,
            sample_rate=32.0,
            dtype=np.float32
        )
        
        # Buffer optimisé
        self.optimized_buffer = LockFreeCircularBuffer(self.config)
        
        # Buffer de référence (si disponible)
        if REFERENCE_AVAILABLE:
            self.reference_buffer = CircularBuffer(self.config)
    
    @pytest.mark.performance
    def test_buffer_speed_improvement(self):
        """Test amélioration vitesse buffer (objectif: ≥ 3x)"""
        # Données test
        n_operations = 1000
        samples_per_op = 64
        
        print(f"\n🔄 Test performance buffer:")
        print(f"   Opérations: {n_operations:,}")
        print(f"   Échantillons/op: {samples_per_op}")
        
        # Générer données
        test_data = PerformanceBenchmark.generate_wave_signal(
            samples_per_op, self.config.sample_rate, self.config.n_channels
        )
        
        # Benchmark buffer optimisé
        start_time = time.perf_counter()
        for i in range(n_operations):
            success = self.optimized_buffer.write(test_data)
            if i % 10 == 0:  # Lecture périodique
                available = self.optimized_buffer.available_samples()
                if available > 0:
                    self.optimized_buffer.read(min(available, samples_per_op * 5))
        optimized_time = time.perf_counter() - start_time
        
        print(f"   Buffer optimisé: {optimized_time:.3f}s")
        
        # Benchmark buffer référence (si disponible)
        if REFERENCE_AVAILABLE:
            self.reference_buffer.reset()
            
            start_time = time.perf_counter()
            for i in range(n_operations):
                success = self.reference_buffer.write(test_data)
                if i % 10 == 0:  # Lecture périodique
                    available = self.reference_buffer.available_samples()
                    if available > 0:
                        self.reference_buffer.read(min(available, samples_per_op * 5))
            reference_time = time.perf_counter() - start_time
            
            print(f"   Buffer référence: {reference_time:.3f}s")
            
            # Calculer amélioration
            speedup = reference_time / optimized_time if optimized_time > 0 else float('inf')
            print(f"   Amélioration: {speedup:.1f}x")
            
            # Assertions
            assert speedup >= 3.0, f"Amélioration insuffisante: {speedup:.1f}x < 3.0x"
        else:
            # Test performance absolue
            throughput = (n_operations * samples_per_op) / optimized_time
            min_throughput = 100000  # 100k échantillons/s minimum
            
            print(f"   Débit: {throughput:.0f} échantillons/s")
            assert throughput >= min_throughput, f"Débit insuffisant: {throughput:.0f} < {min_throughput}"
        
        print(f"✅ Test buffer réussi")
    
    @pytest.mark.performance
    def test_buffer_concurrent_access(self):
        """Test accès concurrent au buffer"""
        import threading
        import queue
        
        n_writers = 3
        n_readers = 2
        operations_per_thread = 500
        samples_per_op = 32
        
        print(f"\n🔀 Test accès concurrent buffer:")
        print(f"   Writers: {n_writers}")
        print(f"   Readers: {n_readers}")
        print(f"   Opérations/thread: {operations_per_thread}")
        
        # Queues pour résultats
        write_times = queue.Queue()
        read_times = queue.Queue()
        errors = queue.Queue()
        
        def writer_thread(thread_id: int):
            """Thread d'écriture"""
            try:
                start_time = time.perf_counter()
                
                for i in range(operations_per_thread):
                    data = PerformanceBenchmark.generate_wave_signal(
                        samples_per_op, self.config.sample_rate, self.config.n_channels
                    )
                    success = self.optimized_buffer.write(data)
                    
                    if not success:
                        # Attendre un peu et réessayer
                        time.sleep(0.001)
                        self.optimized_buffer.write(data)
                
                end_time = time.perf_counter()
                write_times.put(end_time - start_time)
                
            except Exception as e:
                errors.put(f"Writer {thread_id}: {e}")
        
        def reader_thread(thread_id: int):
            """Thread de lecture"""
            try:
                start_time = time.perf_counter()
                total_read = 0
                
                while total_read < operations_per_thread * samples_per_op:
                    available = self.optimized_buffer.available_samples()
                    if available > 0:
                        read_size = min(available, samples_per_op * 2)
                        data = self.optimized_buffer.read(read_size)
                        if data is not None:
                            total_read += read_size
                    else:
                        time.sleep(0.001)  # Attendre données
                
                end_time = time.perf_counter()
                read_times.put(end_time - start_time)
                
            except Exception as e:
                errors.put(f"Reader {thread_id}: {e}")
        
        # Démarrer threads
        threads = []
        
        # Writers
        for i in range(n_writers):
            t = threading.Thread(target=writer_thread, args=(i,))
            threads.append(t)
            t.start()
        
        # Readers
        for i in range(n_readers):
            t = threading.Thread(target=reader_thread, args=(i,))
            threads.append(t)
            t.start()
        
        # Attendre fin
        for t in threads:
            t.join(timeout=30.0)  # Timeout sécurité
        
        # Collecter résultats
        write_times_list = []
        while not write_times.empty():
            write_times_list.append(write_times.get())
        
        read_times_list = []
        while not read_times.empty():
            read_times_list.append(read_times.get())
        
        errors_list = []
        while not errors.empty():
            errors_list.append(errors.get())
        
        # Analyser résultats
        if write_times_list:
            avg_write_time = sum(write_times_list) / len(write_times_list)
            print(f"   Temps écriture moyen: {avg_write_time:.3f}s")
        
        if read_times_list:
            avg_read_time = sum(read_times_list) / len(read_times_list)
            print(f"   Temps lecture moyen: {avg_read_time:.3f}s")
        
        print(f"   Erreurs: {len(errors_list)}")
        
        # Assertions
        assert len(errors_list) == 0, f"Erreurs détectées: {errors_list}"
        assert len(write_times_list) == n_writers, "Tous les writers doivent terminer"
        assert len(read_times_list) == n_readers, "Tous les readers doivent terminer"
        
        print(f"✅ Test accès concurrent réussi")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short", "-m", "performance"])