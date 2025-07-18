#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark P0 pour CHNeoWave

Validation des objectifs P0 :
- 15 min @ 32 Hz × 8 sondes simulate → 0 overflow, usage ≤ 80%
- Performance du système de signaux unifié
- Couverture de tests ≥ 90%

Auteur: WaveBuffer-Fixer
Version: 3.0.0
Date: 2025
"""

import time
import numpy as np
import threading
import psutil
import gc
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import json
import sys
import os

# Ajouter le chemin source
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from hrneowave.core.buffer_config import UnifiedBufferConfig
    from hrneowave.core.circular_buffer import LockFreeCircularBuffer
    BUFFER_AVAILABLE = True
except ImportError as e:
    print(f"Modules buffer non disponibles: {e}")
    BUFFER_AVAILABLE = False

try:
    from hrneowave.core.signal_bus import (
        get_signal_bus, get_error_bus, reset_signal_buses,
        SignalBus, ErrorBus, ErrorLevel, SessionState
    )
    SIGNAL_BUS_AVAILABLE = True
except ImportError as e:
    print(f"Module signal_bus non disponible: {e}")
    SIGNAL_BUS_AVAILABLE = False


@dataclass
class BenchmarkResult:
    """Résultat d'un benchmark"""
    test_name: str
    duration: float
    success: bool
    metrics: Dict[str, Any]
    errors: List[str]
    timestamp: float


class PerformanceMonitor:
    """Moniteur de performance système"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.cpu_samples = []
        self.memory_samples = []
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Démarrer le monitoring"""
        self.start_time = time.time()
        self.monitoring = True
        self.cpu_samples = []
        self.memory_samples = []
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Arrêter le monitoring"""
        self.end_time = time.time()
        self.monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
    
    def _monitor_loop(self):
        """Boucle de monitoring"""
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=None)
                memory_info = psutil.virtual_memory()
                
                self.cpu_samples.append(cpu_percent)
                self.memory_samples.append(memory_info.percent)
                
                time.sleep(0.1)  # Échantillonnage à 10 Hz
            except Exception:
                pass
    
    def get_stats(self) -> Dict[str, float]:
        """Obtenir les statistiques de performance"""
        if not self.cpu_samples or not self.memory_samples:
            return {}
        
        return {
            'duration': self.end_time - self.start_time if self.end_time else 0,
            'cpu_mean': np.mean(self.cpu_samples),
            'cpu_max': np.max(self.cpu_samples),
            'cpu_std': np.std(self.cpu_samples),
            'memory_mean': np.mean(self.memory_samples),
            'memory_max': np.max(self.memory_samples),
            'memory_std': np.std(self.memory_samples),
            'samples_count': len(self.cpu_samples)
        }


class BufferBenchmark:
    """Benchmark pour les buffers circulaires"""
    
    def __init__(self):
        self.results = []
        self.monitor = PerformanceMonitor()
    
    def run_p0_buffer_test(self) -> BenchmarkResult:
        """Test P0: 15 min @ 32 Hz × 8 sondes sans overflow"""
        if not BUFFER_AVAILABLE:
            return BenchmarkResult(
                test_name="P0_Buffer_Test",
                duration=0,
                success=False,
                metrics={},
                errors=["Modules buffer non disponibles"],
                timestamp=time.time()
            )
        
        print("\n=== Test P0: Buffer 15min @ 32Hz × 8 sondes ===")
        
        # Configuration P0
        sample_rate = 32.0  # Hz
        n_channels = 8
        test_duration = 15 * 60  # 15 minutes en secondes
        total_samples = int(sample_rate * test_duration)
        
        # Configuration buffer optimisée pour P0
        config = UnifiedBufferConfig(
            n_channels=n_channels,
            buffer_size=8192,  # Buffer plus grand pour 15 min
            sample_rate=sample_rate,
            dtype=np.float32,
            overflow_mode="BLOCK",
            enable_overflow_detection=True,
            overflow_threshold=80.0,  # P0: usage ≤ 80%
            enable_statistics=True,
            enable_lock_free=True,
            enable_simd_alignment=True
        )
        
        errors = []
        metrics = {}
        
        try:
            # Créer le buffer
            buffer = LockFreeCircularBuffer(config)
            
            # Démarrer le monitoring
            self.monitor.start_monitoring()
            start_time = time.time()
            
            # Variables de suivi
            overflow_count = 0
            max_usage = 0.0
            samples_written = 0
            
            print(f"Démarrage test: {total_samples} échantillons sur {test_duration}s")
            print(f"Fréquence cible: {sample_rate} Hz")
            
            # Simulation d'acquisition continue
            last_progress = 0
            for i in range(total_samples):
                # Générer des données simulées (8 canaux)
                data = np.random.random((n_channels,)).astype(np.float32)
                
                # Écrire dans le buffer
                try:
                    success = buffer.write(data)
                    if success:
                        samples_written += 1
                    else:
                        overflow_count += 1
                        if overflow_count == 1:
                            print(f"\n⚠️  Premier overflow détecté à l'échantillon {i}")
                except Exception as e:
                    errors.append(f"Erreur écriture échantillon {i}: {e}")
                    break
                
                # Vérifier l'usage du buffer
                current_usage = buffer.usage_percent()
                max_usage = max(max_usage, current_usage)
                
                # Affichage du progrès
                progress = int((i / total_samples) * 100)
                if progress > last_progress and progress % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    print(f"Progrès: {progress}% - {i}/{total_samples} échantillons - "
                          f"Taux: {rate:.1f} Hz - Usage: {current_usage:.1f}%")
                    last_progress = progress
                
                # Respecter la fréquence d'échantillonnage
                target_time = start_time + (i + 1) / sample_rate
                current_time = time.time()
                if current_time < target_time:
                    time.sleep(target_time - current_time)
                
                # Vérification P0: arrêt si usage > 80%
                if current_usage > 80.0:
                    errors.append(f"Usage buffer dépassé: {current_usage:.1f}% > 80%")
                    break
            
            # Arrêter le monitoring
            end_time = time.time()
            self.monitor.stop_monitoring()
            
            # Calculer les métriques
            actual_duration = end_time - start_time
            actual_rate = samples_written / actual_duration if actual_duration > 0 else 0
            
            # Statistiques du buffer
            buffer_stats = buffer.get_stats()
            perf_stats = self.monitor.get_stats()
            
            metrics = {
                'target_samples': total_samples,
                'samples_written': samples_written,
                'overflow_count': overflow_count,
                'max_usage_percent': max_usage,
                'target_duration': test_duration,
                'actual_duration': actual_duration,
                'target_rate': sample_rate,
                'actual_rate': actual_rate,
                'rate_accuracy': (actual_rate / sample_rate) * 100 if sample_rate > 0 else 0,
                'buffer_stats': buffer_stats,
                'performance_stats': perf_stats
            }
            
            # Vérification des critères P0
            p0_success = (
                overflow_count == 0 and
                max_usage <= 80.0 and
                actual_duration >= test_duration * 0.95  # Tolérance 5%
            )
            
            # Rapport final
            print(f"\n=== Résultats Test P0 ===")
            print(f"Durée: {actual_duration:.1f}s / {test_duration}s")
            print(f"Échantillons: {samples_written} / {total_samples}")
            print(f"Taux réel: {actual_rate:.2f} Hz / {sample_rate} Hz")
            print(f"Usage max: {max_usage:.1f}% (limite: 80%)")
            print(f"Overflows: {overflow_count} (limite: 0)")
            print(f"Critères P0: {'✅ RÉUSSI' if p0_success else '❌ ÉCHEC'}")
            
            if perf_stats:
                print(f"\nPerformance système:")
                print(f"  CPU moyen: {perf_stats['cpu_mean']:.1f}%")
                print(f"  CPU max: {perf_stats['cpu_max']:.1f}%")
                print(f"  Mémoire moyenne: {perf_stats['memory_mean']:.1f}%")
                print(f"  Mémoire max: {perf_stats['memory_max']:.1f}%")
            
            return BenchmarkResult(
                test_name="P0_Buffer_Test",
                duration=actual_duration,
                success=p0_success,
                metrics=metrics,
                errors=errors,
                timestamp=time.time()
            )
            
        except Exception as e:
            self.monitor.stop_monitoring()
            errors.append(f"Erreur critique: {e}")
            
            return BenchmarkResult(
                test_name="P0_Buffer_Test",
                duration=0,
                success=False,
                metrics=metrics,
                errors=errors,
                timestamp=time.time()
            )
    
    def run_stress_test(self) -> BenchmarkResult:
        """Test de stress pour les buffers"""
        if not BUFFER_AVAILABLE:
            return BenchmarkResult(
                test_name="Stress_Test",
                duration=0,
                success=False,
                metrics={},
                errors=["Modules buffer non disponibles"],
                timestamp=time.time()
            )
        
        print("\n=== Test de Stress Buffer ===")
        
        # Configuration stress
        config = UnifiedBufferConfig(
            n_channels=16,  # Plus de canaux
            buffer_size=2048,  # Buffer plus petit
            sample_rate=1000.0,  # Fréquence élevée
            dtype=np.float32,
            overflow_mode="OVERWRITE",
            enable_overflow_detection=True,
            overflow_threshold=95.0,
            enable_statistics=True
        )
        
        errors = []
        metrics = {}
        
        try:
            buffer = LockFreeCircularBuffer(config)
            
            self.monitor.start_monitoring()
            start_time = time.time()
            
            # Test haute fréquence pendant 30 secondes
            test_duration = 30.0
            target_samples = int(1000 * test_duration)  # 1000 Hz
            
            overflow_count = 0
            samples_written = 0
            max_usage = 0.0
            
            for i in range(target_samples):
                data = np.random.random((16,)).astype(np.float32)
                
                try:
                    success = buffer.write(data)
                    if success:
                        samples_written += 1
                    else:
                        overflow_count += 1
                except Exception as e:
                    errors.append(f"Erreur écriture: {e}")
                    break
                
                current_usage = buffer.usage_percent()
                max_usage = max(max_usage, current_usage)
                
                # Pas de délai - stress maximum
            
            end_time = time.time()
            self.monitor.stop_monitoring()
            
            actual_duration = end_time - start_time
            actual_rate = samples_written / actual_duration if actual_duration > 0 else 0
            
            metrics = {
                'target_samples': target_samples,
                'samples_written': samples_written,
                'overflow_count': overflow_count,
                'max_usage_percent': max_usage,
                'actual_duration': actual_duration,
                'actual_rate': actual_rate,
                'performance_stats': self.monitor.get_stats()
            }
            
            success = samples_written > target_samples * 0.8  # 80% minimum
            
            print(f"Stress test: {samples_written}/{target_samples} échantillons")
            print(f"Taux: {actual_rate:.0f} Hz, Usage max: {max_usage:.1f}%")
            print(f"Overflows: {overflow_count}")
            
            return BenchmarkResult(
                test_name="Stress_Test",
                duration=actual_duration,
                success=success,
                metrics=metrics,
                errors=errors,
                timestamp=time.time()
            )
            
        except Exception as e:
            self.monitor.stop_monitoring()
            errors.append(f"Erreur stress test: {e}")
            
            return BenchmarkResult(
                test_name="Stress_Test",
                duration=0,
                success=False,
                metrics=metrics,
                errors=errors,
                timestamp=time.time()
            )


class SignalBusBenchmark:
    """Benchmark pour le système de signaux"""
    
    def run_signal_performance_test(self) -> BenchmarkResult:
        """Test de performance du système de signaux"""
        if not SIGNAL_BUS_AVAILABLE:
            return BenchmarkResult(
                test_name="Signal_Performance_Test",
                duration=0,
                success=False,
                metrics={},
                errors=["Module signal_bus non disponible"],
                timestamp=time.time()
            )
        
        print("\n=== Test Performance Signaux ===")
        
        # Reset des bus
        reset_signal_buses()
        
        signal_bus = get_signal_bus()
        error_bus = get_error_bus()
        
        # Compteurs
        data_signals_received = 0
        error_signals_received = 0
        
        def count_data_signals(data_block):
            nonlocal data_signals_received
            data_signals_received += 1
        
        def count_error_signals(error_msg):
            nonlocal error_signals_received
            error_signals_received += 1
        
        # Connexions
        signal_bus.dataBlockReady.connect(count_data_signals)
        error_bus.error_occurred.connect(count_error_signals)
        
        errors = []
        
        try:
            start_time = time.time()
            
            # Test haute fréquence de signaux
            n_data_signals = 1000
            n_error_signals = 100
            
            # Émettre des signaux de données
            for i in range(n_data_signals):
                test_data = np.random.random((4, 32))
                signal_bus.emit_data_block(
                    data=test_data,
                    timestamp=time.time(),
                    sample_rate=1000.0,
                    n_channels=4,
                    sequence_id=i
                )
            
            # Émettre des signaux d'erreur
            for i in range(n_error_signals):
                if i % 4 == 0:
                    error_bus.emit_info(f"Info {i}", "TestModule")
                elif i % 4 == 1:
                    error_bus.emit_warning(f"Warning {i}", "TestModule")
                elif i % 4 == 2:
                    error_bus.emit_error(ErrorLevel.ERROR, f"Error {i}", "TestModule")
                else:
                    error_bus.emit_critical(f"Critical {i}", "TestModule")
            
            # Attendre le traitement
            time.sleep(0.5)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Métriques
            data_rate = data_signals_received / duration if duration > 0 else 0
            error_rate = error_signals_received / duration if duration > 0 else 0
            
            metrics = {
                'data_signals_sent': n_data_signals,
                'data_signals_received': data_signals_received,
                'error_signals_sent': n_error_signals,
                'error_signals_received': error_signals_received,
                'duration': duration,
                'data_signal_rate': data_rate,
                'error_signal_rate': error_rate,
                'data_loss_percent': ((n_data_signals - data_signals_received) / n_data_signals) * 100,
                'error_loss_percent': ((n_error_signals - error_signals_received) / n_error_signals) * 100
            }
            
            # Critères de succès
            success = (
                data_signals_received >= n_data_signals * 0.95 and  # 95% minimum
                error_signals_received >= n_error_signals * 0.95 and
                data_rate > 100  # Au moins 100 Hz
            )
            
            print(f"Signaux données: {data_signals_received}/{n_data_signals} ({data_rate:.0f} Hz)")
            print(f"Signaux erreurs: {error_signals_received}/{n_error_signals} ({error_rate:.0f} Hz)")
            print(f"Performance: {'✅ RÉUSSI' if success else '❌ ÉCHEC'}")
            
            return BenchmarkResult(
                test_name="Signal_Performance_Test",
                duration=duration,
                success=success,
                metrics=metrics,
                errors=errors,
                timestamp=time.time()
            )
            
        except Exception as e:
            errors.append(f"Erreur test signaux: {e}")
            
            return BenchmarkResult(
                test_name="Signal_Performance_Test",
                duration=0,
                success=False,
                metrics={},
                errors=errors,
                timestamp=time.time()
            )


def run_coverage_analysis() -> Dict[str, Any]:
    """Analyser la couverture de tests"""
    print("\n=== Analyse Couverture Tests ===")
    
    try:
        import coverage
        
        # Démarrer la mesure de couverture
        cov = coverage.Coverage()
        cov.start()
        
        # Importer et tester les modules principaux
        modules_tested = []
        
        if BUFFER_AVAILABLE:
            from hrneowave.core.buffer_config import UnifiedBufferConfig
            from hrneowave.core.circular_buffer import LockFreeCircularBuffer
            modules_tested.extend(['buffer_config', 'circular_buffer'])
        
        if SIGNAL_BUS_AVAILABLE:
            from hrneowave.core.signal_bus import SignalBus, ErrorBus
            modules_tested.extend(['signal_bus'])
        
        # Arrêter la mesure
        cov.stop()
        cov.save()
        
        # Générer le rapport
        coverage_percent = cov.report(show_missing=False)
        
        return {
            'coverage_percent': coverage_percent,
            'modules_tested': modules_tested,
            'target_coverage': 90.0,
            'meets_target': coverage_percent >= 90.0
        }
        
    except ImportError:
        print("Module coverage non disponible")
        return {
            'coverage_percent': 0,
            'modules_tested': [],
            'target_coverage': 90.0,
            'meets_target': False,
            'error': 'Module coverage non installé'
        }
    except Exception as e:
        print(f"Erreur analyse couverture: {e}")
        return {
            'coverage_percent': 0,
            'modules_tested': [],
            'target_coverage': 90.0,
            'meets_target': False,
            'error': str(e)
        }


def save_benchmark_report(results: List[BenchmarkResult], coverage_info: Dict[str, Any]):
    """Sauvegarder le rapport de benchmark"""
    report = {
        'timestamp': time.time(),
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'system_info': {
            'python_version': sys.version,
            'platform': sys.platform,
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total
        },
        'p0_objectives': {
            'buffer_test': '15 min @ 32 Hz × 8 sondes → 0 overflow, usage ≤ 80%',
            'signal_performance': 'Communication inter-fenêtres fluide',
            'test_coverage': 'Couverture ≥ 90%'
        },
        'results': [{
            'test_name': r.test_name,
            'duration': r.duration,
            'success': r.success,
            'metrics': r.metrics,
            'errors': r.errors,
            'timestamp': r.timestamp
        } for r in results],
        'coverage': coverage_info,
        'summary': {
            'total_tests': len(results),
            'passed_tests': sum(1 for r in results if r.success),
            'failed_tests': sum(1 for r in results if not r.success),
            'overall_success': all(r.success for r in results) and coverage_info.get('meets_target', False)
        }
    }
    
    # Sauvegarder le rapport
    report_file = Path(__file__).parent / "benchmark_p0_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nRapport sauvegardé: {report_file}")
    return report


def main():
    """Fonction principale du benchmark P0"""
    print("🚀 Benchmark P0 CHNeoWave")
    print("=" * 50)
    
    # Nettoyage mémoire initial
    gc.collect()
    
    results = []
    
    # 1. Test P0 Buffer (objectif principal)
    buffer_bench = BufferBenchmark()
    p0_result = buffer_bench.run_p0_buffer_test()
    results.append(p0_result)
    
    # 2. Test de stress
    stress_result = buffer_bench.run_stress_test()
    results.append(stress_result)
    
    # 3. Test performance signaux
    signal_bench = SignalBusBenchmark()
    signal_result = signal_bench.run_signal_performance_test()
    results.append(signal_result)
    
    # 4. Analyse couverture
    coverage_info = run_coverage_analysis()
    
    # 5. Rapport final
    report = save_benchmark_report(results, coverage_info)
    
    # Affichage du résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ BENCHMARK P0")
    print("=" * 50)
    
    for result in results:
        status = "✅ RÉUSSI" if result.success else "❌ ÉCHEC"
        print(f"{result.test_name}: {status} ({result.duration:.1f}s)")
        
        if result.errors:
            for error in result.errors[:3]:  # Afficher max 3 erreurs
                print(f"  ⚠️  {error}")
    
    print(f"\nCouverture tests: {coverage_info.get('coverage_percent', 0):.1f}% "
          f"(objectif: {coverage_info.get('target_coverage', 90)}%)")
    
    overall_success = report['summary']['overall_success']
    print(f"\n🎯 OBJECTIFS P0: {'✅ ATTEINTS' if overall_success else '❌ NON ATTEINTS'}")
    
    if overall_success:
        print("\n🎉 Félicitations! Tous les objectifs P0 sont atteints.")
        print("   Le système CHNeoWave est prêt pour la production.")
    else:
        print("\n⚠️  Certains objectifs P0 ne sont pas atteints.")
        print("   Vérifiez les erreurs ci-dessus et corrigez avant la production.")
    
    return 0 if overall_success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)