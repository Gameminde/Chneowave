"""Tests unitaires pour OptimizedFFTProcessor.

Ce module teste toutes les fonctionnalités du processeur FFT optimisé.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import time

try:
    from src.hrneowave.core.optimized_fft_processor import OptimizedFFTProcessor
    from src.hrneowave.config.optimization_config import FFTOptimizationConfig
except ImportError:
    pytest.skip("OptimizedFFTProcessor non disponible", allow_module_level=True)


class TestOptimizedFFTProcessor:
    """Tests pour OptimizedFFTProcessor."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.config = FFTOptimizationConfig(
            window_size=1024,
            overlap=0.5,
            window_type='hann',
            zero_padding=True,
            use_gpu=False
        )
        self.processor = OptimizedFFTProcessor(self.config)
    
    def test_initialization(self):
        """Test l'initialisation du processeur."""
        assert self.processor.config == self.config
        assert self.processor.window_size == 1024
        assert self.processor.overlap == 0.5
        assert self.processor.window_type == 'hann'
    
    def test_process_basic(self):
        """Test le traitement FFT basique."""
        # Données de test
        data = np.random.randn(1024)
        
        # Traitement
        result = self.processor.process(data)
        
        # Vérifications
        assert isinstance(result, np.ndarray)
        assert len(result) > 0
        assert np.all(np.isfinite(result))
    
    def test_process_different_sizes(self):
        """Test avec différentes tailles de données."""
        sizes = [512, 1024, 2048, 4096]
        
        for size in sizes:
            data = np.random.randn(size)
            result = self.processor.process(data)
            
            assert isinstance(result, np.ndarray)
            assert len(result) > 0
    
    def test_process_empty_data(self):
        """Test avec des données vides."""
        data = np.array([])
        
        with pytest.raises((ValueError, IndexError)):
            self.processor.process(data)
    
    def test_process_single_value(self):
        """Test avec une seule valeur."""
        data = np.array([1.0])
        
        result = self.processor.process(data)
        assert isinstance(result, np.ndarray)
    
    def test_window_functions(self):
        """Test différentes fonctions de fenêtrage."""
        windows = ['hann', 'hamming', 'blackman', 'bartlett']
        data = np.random.randn(1024)
        
        for window in windows:
            config = FFTOptimizationConfig(window_type=window)
            processor = OptimizedFFTProcessor(config)
            
            result = processor.process(data)
            assert isinstance(result, np.ndarray)
            assert len(result) > 0
    
    def test_zero_padding(self):
        """Test le zero padding."""
        data = np.random.randn(1000)  # Taille non-puissance de 2
        
        # Avec zero padding
        config_with_padding = FFTOptimizationConfig(zero_padding=True)
        processor_with = OptimizedFFTProcessor(config_with_padding)
        result_with = processor_with.process(data)
        
        # Sans zero padding
        config_without_padding = FFTOptimizationConfig(zero_padding=False)
        processor_without = OptimizedFFTProcessor(config_without_padding)
        result_without = processor_without.process(data)
        
        assert isinstance(result_with, np.ndarray)
        assert isinstance(result_without, np.ndarray)
    
    def test_overlap_processing(self):
        """Test le traitement avec recouvrement."""
        overlaps = [0.0, 0.25, 0.5, 0.75]
        data = np.random.randn(2048)
        
        for overlap in overlaps:
            config = FFTOptimizationConfig(overlap=overlap)
            processor = OptimizedFFTProcessor(config)
            
            result = processor.process(data)
            assert isinstance(result, np.ndarray)
    
    def test_performance_benchmark(self):
        """Test de performance - doit être < 5ms pour 1024 échantillons."""
        data = np.random.randn(1024)
        
        # Mesure du temps
        start_time = time.perf_counter()
        result = self.processor.process(data)
        end_time = time.perf_counter()
        
        processing_time = (end_time - start_time) * 1000  # en ms
        
        assert processing_time < 5.0, f"Traitement trop lent: {processing_time:.2f}ms"
        assert isinstance(result, np.ndarray)
    
    def test_multiple_consecutive_processing(self):
        """Test traitement consécutif multiple."""
        data = np.random.randn(1024)
        results = []
        
        for _ in range(10):
            result = self.processor.process(data)
            results.append(result)
        
        # Vérifier que tous les résultats sont valides
        for result in results:
            assert isinstance(result, np.ndarray)
            assert len(result) > 0
            assert np.all(np.isfinite(result))
    
    def test_frequency_domain_properties(self):
        """Test les propriétés du domaine fréquentiel."""
        # Signal sinusoïdal de test
        fs = 1000  # Fréquence d'échantillonnage
        f_signal = 100  # Fréquence du signal
        t = np.linspace(0, 1, fs, endpoint=False)
        data = np.sin(2 * np.pi * f_signal * t)
        
        result = self.processor.process(data)
        
        # Le résultat doit avoir un pic à la fréquence du signal
        assert isinstance(result, np.ndarray)
        assert len(result) > 0
        assert np.max(result) > np.mean(result) * 2  # Pic significatif
    
    def test_noise_handling(self):
        """Test la gestion du bruit."""
        # Signal avec bruit
        signal = np.sin(2 * np.pi * 50 * np.linspace(0, 1, 1024))
        noise = np.random.normal(0, 0.1, 1024)
        data = signal + noise
        
        result = self.processor.process(data)
        
        assert isinstance(result, np.ndarray)
        assert len(result) > 0
        assert np.all(np.isfinite(result))
    
    def test_edge_cases(self):
        """Test les cas limites."""
        # Données avec des valeurs extrêmes
        extreme_data = np.array([1e10, -1e10, 0, 1e-10, -1e-10] * 200 + [0] * 24)
        
        result = self.processor.process(extreme_data)
        assert isinstance(result, np.ndarray)
        assert np.all(np.isfinite(result))
    
    def test_configuration_validation(self):
        """Test la validation de la configuration."""
        # Configuration invalide
        with pytest.raises((ValueError, TypeError)):
            invalid_config = FFTOptimizationConfig(window_size=-1)
            OptimizedFFTProcessor(invalid_config)
    
    def test_memory_efficiency(self):
        """Test l'efficacité mémoire."""
        # Traitement de gros volumes de données
        large_data = np.random.randn(10000)
        
        result = self.processor.process(large_data)
        
        assert isinstance(result, np.ndarray)
        # Vérifier que le résultat n'est pas disproportionnellement grand
        assert result.nbytes < large_data.nbytes * 2
    
    @patch('numpy.fft.fft')
    def test_fft_call(self, mock_fft):
        """Test que la FFT numpy est appelée correctement."""
        mock_fft.return_value = np.array([1+1j, 2+2j, 3+3j])
        
        data = np.random.randn(1024)
        result = self.processor.process(data)
        
        # Vérifier que numpy.fft.fft a été appelé
        mock_fft.assert_called()
        assert isinstance(result, np.ndarray)
    
    def test_thread_safety(self):
        """Test basique de thread safety."""
        import threading
        import queue
        
        results_queue = queue.Queue()
        data = np.random.randn(1024)
        
        def worker():
            try:
                result = self.processor.process(data)
                results_queue.put(('success', result))
            except Exception as e:
                results_queue.put(('error', str(e)))
        
        # Lancer plusieurs threads
        threads = []
        for _ in range(5):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        # Attendre la fin
        for t in threads:
            t.join()
        
        # Vérifier les résultats
        success_count = 0
        while not results_queue.empty():
            status, result = results_queue.get()
            if status == 'success':
                success_count += 1
                assert isinstance(result, np.ndarray)
        
        assert success_count == 5
    
    def test_get_frequency_bins(self):
        """Test la méthode get_frequency_bins si elle existe."""
        if hasattr(self.processor, 'get_frequency_bins'):
            fs = 1000
            bins = self.processor.get_frequency_bins(fs)
            
            assert isinstance(bins, np.ndarray)
            assert len(bins) > 0
    
    def test_reset_processor(self):
        """Test la méthode reset si elle existe."""
        if hasattr(self.processor, 'reset'):
            # Traiter quelques données
            data = np.random.randn(1024)
            self.processor.process(data)
            
            # Reset
            self.processor.reset()
            
            # Vérifier que le processeur fonctionne encore
            result = self.processor.process(data)
            assert isinstance(result, np.ndarray)


class TestOptimizedFFTProcessorIntegration:
    """Tests d'intégration pour OptimizedFFTProcessor."""
    
    def test_with_real_wave_data(self):
        """Test avec des données de vagues simulées."""
        # Simulation de données de vagues
        t = np.linspace(0, 10, 1024)
        wave_data = (
            2.0 * np.sin(2 * np.pi * 0.1 * t) +  # Vague principale
            0.5 * np.sin(2 * np.pi * 0.3 * t) +  # Harmonique
            0.1 * np.random.randn(len(t))        # Bruit
        )
        
        config = FFTOptimizationConfig()
        processor = OptimizedFFTProcessor(config)
        
        result = processor.process(wave_data)
        
        assert isinstance(result, np.ndarray)
        assert len(result) > 0
        assert np.all(np.isfinite(result))
    
    def test_batch_processing(self):
        """Test traitement par lots."""
        config = FFTOptimizationConfig()
        processor = OptimizedFFTProcessor(config)
        
        # Traiter plusieurs lots
        batch_results = []
        for i in range(10):
            data = np.random.randn(1024) + i * 0.1  # Données légèrement différentes
            result = processor.process(data)
            batch_results.append(result)
        
        # Vérifier tous les résultats
        for result in batch_results:
            assert isinstance(result, np.ndarray)
            assert len(result) > 0
            assert np.all(np.isfinite(result))
    
    def test_configuration_changes(self):
        """Test changement de configuration."""
        data = np.random.randn(1024)
        
        # Configuration initiale
        config1 = FFTOptimizationConfig(window_type='hann')
        processor = OptimizedFFTProcessor(config1)
        result1 = processor.process(data)
        
        # Nouvelle configuration
        config2 = FFTOptimizationConfig(window_type='hamming')
        processor = OptimizedFFTProcessor(config2)
        result2 = processor.process(data)
        
        # Les résultats doivent être différents
        assert isinstance(result1, np.ndarray)
        assert isinstance(result2, np.ndarray)
        assert not np.array_equal(result1, result2)