"""Tests unitaires pour OptimizedGodaAnalyzer.

Ce module teste toutes les fonctionnalités de l'analyseur Goda optimisé.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import time

try:
    from src.hrneowave.core.optimized_goda_analyzer import OptimizedGodaAnalyzer
    from src.hrneowave.config.optimization_config import GodaOptimizationConfig
except ImportError:
    pytest.skip("OptimizedGodaAnalyzer non disponible", allow_module_level=True)


class TestOptimizedGodaAnalyzer:
    """Tests pour OptimizedGodaAnalyzer."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.config = GodaOptimizationConfig(
            sampling_rate=1000.0,
            analysis_window=10.0,
            overlap_ratio=0.5,
            min_wave_height=0.01,
            max_wave_height=10.0
        )
        self.analyzer = OptimizedGodaAnalyzer(self.config)
    
    def test_initialization(self):
        """Test l'initialisation de l'analyseur."""
        assert self.analyzer.config == self.config
        assert self.analyzer.sampling_rate == 1000.0
        assert self.analyzer.analysis_window == 10.0
        assert self.analyzer.overlap_ratio == 0.5
    
    def test_analyze_basic(self):
        """Test l'analyse Goda basique."""
        # Données de test - signal de vague simulé
        t = np.linspace(0, 10, 10000)
        wave_data = 2.0 * np.sin(2 * np.pi * 0.1 * t) + 0.5 * np.sin(2 * np.pi * 0.3 * t)
        
        # Analyse
        result = self.analyzer.analyze(wave_data)
        
        # Vérifications
        assert isinstance(result, dict)
        assert 'significant_wave_height' in result
        assert 'peak_period' in result
        assert 'mean_period' in result
        assert 'wave_count' in result
    
    def test_analyze_empty_data(self):
        """Test avec des données vides."""
        data = np.array([])
        
        with pytest.raises((ValueError, IndexError)):
            self.analyzer.analyze(data)
    
    def test_analyze_single_value(self):
        """Test avec une seule valeur."""
        data = np.array([1.0])
        
        result = self.analyzer.analyze(data)
        assert isinstance(result, dict)
    
    def test_analyze_constant_signal(self):
        """Test avec un signal constant."""
        data = np.ones(1000)
        
        result = self.analyzer.analyze(data)
        
        assert isinstance(result, dict)
        assert result['significant_wave_height'] == 0.0 or result['significant_wave_height'] is None
    
    def test_analyze_sinusoidal_wave(self):
        """Test avec une vague sinusoïdale parfaite."""
        # Vague sinusoïdale de 1m d'amplitude, période 10s
        t = np.linspace(0, 100, 10000)  # 100 secondes
        amplitude = 1.0
        period = 10.0
        wave_data = amplitude * np.sin(2 * np.pi * t / period)
        
        result = self.analyzer.analyze(wave_data)
        
        assert isinstance(result, dict)
        assert 'significant_wave_height' in result
        assert 'peak_period' in result
        
        # Vérifier que la hauteur significative est proche de 4*amplitude
        if result['significant_wave_height'] is not None:
            assert 3.0 < result['significant_wave_height'] < 5.0
    
    def test_analyze_multiple_frequencies(self):
        """Test avec plusieurs fréquences de vagues."""
        t = np.linspace(0, 100, 10000)
        wave_data = (
            1.0 * np.sin(2 * np.pi * 0.1 * t) +  # Vague principale 10s
            0.5 * np.sin(2 * np.pi * 0.2 * t) +  # Vague secondaire 5s
            0.2 * np.sin(2 * np.pi * 0.5 * t)    # Vague haute fréquence 2s
        )
        
        result = self.analyzer.analyze(wave_data)
        
        assert isinstance(result, dict)
        assert all(key in result for key in [
            'significant_wave_height', 'peak_period', 'mean_period', 'wave_count'
        ])
    
    def test_wave_height_calculation(self):
        """Test le calcul de hauteur de vague."""
        # Créer des vagues avec des hauteurs connues
        heights = [0.5, 1.0, 1.5, 2.0, 2.5]
        t = np.linspace(0, 50, 5000)
        wave_data = np.zeros_like(t)
        
        for i, height in enumerate(heights):
            start_idx = i * 1000
            end_idx = (i + 1) * 1000
            wave_data[start_idx:end_idx] = height * np.sin(2 * np.pi * 0.1 * t[start_idx:end_idx])
        
        result = self.analyzer.analyze(wave_data)
        
        assert isinstance(result, dict)
        assert 'significant_wave_height' in result
    
    def test_period_calculation(self):
        """Test le calcul de période."""
        # Vague avec période connue
        period = 8.0  # 8 secondes
        t = np.linspace(0, 80, 8000)  # 10 périodes
        wave_data = np.sin(2 * np.pi * t / period)
        
        result = self.analyzer.analyze(wave_data)
        
        assert isinstance(result, dict)
        assert 'peak_period' in result
        assert 'mean_period' in result
        
        # Vérifier que la période est proche de la valeur attendue
        if result['peak_period'] is not None:
            assert 6.0 < result['peak_period'] < 10.0
    
    def test_wave_counting(self):
        """Test le comptage de vagues."""
        # Créer 5 vagues distinctes
        t = np.linspace(0, 50, 5000)
        wave_data = np.sin(2 * np.pi * 0.1 * t)  # Période 10s, donc 5 vagues en 50s
        
        result = self.analyzer.analyze(wave_data)
        
        assert isinstance(result, dict)
        assert 'wave_count' in result
        
        # Le nombre de vagues devrait être proche de 5
        if result['wave_count'] is not None:
            assert 3 <= result['wave_count'] <= 7
    
    def test_noise_handling(self):
        """Test la gestion du bruit."""
        # Signal avec bruit
        t = np.linspace(0, 50, 5000)
        clean_signal = 2.0 * np.sin(2 * np.pi * 0.1 * t)
        noise = 0.1 * np.random.randn(len(t))
        noisy_data = clean_signal + noise
        
        result = self.analyzer.analyze(noisy_data)
        
        assert isinstance(result, dict)
        assert all(key in result for key in [
            'significant_wave_height', 'peak_period', 'mean_period', 'wave_count'
        ])
    
    def test_performance_benchmark(self):
        """Test de performance - doit être < 5ms pour 1024 échantillons."""
        data = np.random.randn(1024)
        
        # Mesure du temps
        start_time = time.perf_counter()
        result = self.analyzer.analyze(data)
        end_time = time.perf_counter()
        
        processing_time = (end_time - start_time) * 1000  # en ms
        
        assert processing_time < 5.0, f"Analyse trop lente: {processing_time:.2f}ms"
        assert isinstance(result, dict)
    
    def test_different_sampling_rates(self):
        """Test avec différentes fréquences d'échantillonnage."""
        sampling_rates = [100, 500, 1000, 2000]
        
        for fs in sampling_rates:
            config = GodaOptimizationConfig(sampling_rate=float(fs))
            analyzer = OptimizedGodaAnalyzer(config)
            
            # Données adaptées à la fréquence d'échantillonnage
            t = np.linspace(0, 10, fs * 10)
            data = np.sin(2 * np.pi * 0.1 * t)
            
            result = analyzer.analyze(data)
            
            assert isinstance(result, dict)
            assert 'significant_wave_height' in result
    
    def test_different_window_sizes(self):
        """Test avec différentes tailles de fenêtre d'analyse."""
        windows = [5.0, 10.0, 20.0, 30.0]
        
        for window in windows:
            config = GodaOptimizationConfig(analysis_window=window)
            analyzer = OptimizedGodaAnalyzer(config)
            
            # Données suffisamment longues
            t = np.linspace(0, window * 2, int(1000 * window * 2))
            data = np.sin(2 * np.pi * 0.1 * t)
            
            result = analyzer.analyze(data)
            
            assert isinstance(result, dict)
    
    def test_overlap_processing(self):
        """Test le traitement avec recouvrement."""
        overlaps = [0.0, 0.25, 0.5, 0.75]
        data = np.random.randn(5000)
        
        for overlap in overlaps:
            config = GodaOptimizationConfig(overlap_ratio=overlap)
            analyzer = OptimizedGodaAnalyzer(config)
            
            result = analyzer.analyze(data)
            assert isinstance(result, dict)
    
    def test_wave_height_limits(self):
        """Test les limites de hauteur de vague."""
        # Configuration avec limites strictes
        config = GodaOptimizationConfig(
            min_wave_height=0.1,
            max_wave_height=5.0
        )
        analyzer = OptimizedGodaAnalyzer(config)
        
        # Données avec vagues de différentes hauteurs
        t = np.linspace(0, 50, 5000)
        data = 3.0 * np.sin(2 * np.pi * 0.1 * t)  # Vagues de 6m crête-à-crête
        
        result = analyzer.analyze(data)
        
        assert isinstance(result, dict)
        assert 'significant_wave_height' in result
    
    def test_statistical_parameters(self):
        """Test les paramètres statistiques calculés."""
        # Données de test avec statistiques connues
        t = np.linspace(0, 100, 10000)
        wave_data = 2.0 * np.sin(2 * np.pi * 0.1 * t)
        
        result = self.analyzer.analyze(wave_data)
        
        # Vérifier la présence des paramètres statistiques
        expected_keys = [
            'significant_wave_height',
            'peak_period',
            'mean_period',
            'wave_count'
        ]
        
        for key in expected_keys:
            assert key in result
    
    def test_zero_crossing_analysis(self):
        """Test l'analyse des passages par zéro."""
        # Signal avec passages par zéro connus
        t = np.linspace(0, 20, 2000)
        wave_data = np.sin(2 * np.pi * 0.5 * t)  # 0.5 Hz, période 2s
        
        result = self.analyzer.analyze(wave_data)
        
        assert isinstance(result, dict)
        # Le nombre de vagues devrait être proche de 10 (20s / 2s)
        if 'wave_count' in result and result['wave_count'] is not None:
            assert 8 <= result['wave_count'] <= 12
    
    def test_extreme_values(self):
        """Test avec des valeurs extrêmes."""
        # Données avec valeurs très grandes
        large_data = np.array([1e6, -1e6, 1e5, -1e5] * 250)
        
        result = self.analyzer.analyze(large_data)
        assert isinstance(result, dict)
        
        # Données avec valeurs très petites
        small_data = np.array([1e-6, -1e-6, 1e-7, -1e-7] * 250)
        
        result = self.analyzer.analyze(small_data)
        assert isinstance(result, dict)
    
    def test_irregular_waves(self):
        """Test avec des vagues irrégulières."""
        # Simulation de vagues irrégulières (spectre JONSWAP simplifié)
        t = np.linspace(0, 100, 10000)
        frequencies = np.linspace(0.05, 0.5, 20)
        wave_data = np.zeros_like(t)
        
        for f in frequencies:
            amplitude = np.exp(-(f - 0.1)**2 / 0.01)  # Pic à 0.1 Hz
            phase = np.random.uniform(0, 2*np.pi)
            wave_data += amplitude * np.sin(2 * np.pi * f * t + phase)
        
        result = self.analyzer.analyze(wave_data)
        
        assert isinstance(result, dict)
        assert all(key in result for key in [
            'significant_wave_height', 'peak_period', 'mean_period', 'wave_count'
        ])
    
    def test_configuration_validation(self):
        """Test la validation de la configuration."""
        # Configuration invalide
        with pytest.raises((ValueError, TypeError)):
            invalid_config = GodaOptimizationConfig(sampling_rate=-1)
            OptimizedGodaAnalyzer(invalid_config)
    
    def test_memory_efficiency(self):
        """Test l'efficacité mémoire."""
        # Traitement de gros volumes de données
        large_data = np.random.randn(50000)
        
        result = self.analyzer.analyze(large_data)
        
        assert isinstance(result, dict)
        # Le résultat doit être compact
        assert len(str(result)) < 1000  # Résultat compact
    
    @patch('numpy.mean')
    def test_numpy_calls(self, mock_mean):
        """Test que les fonctions numpy sont appelées."""
        mock_mean.return_value = 1.0
        
        data = np.random.randn(1000)
        result = self.analyzer.analyze(data)
        
        # Vérifier que numpy.mean a été appelé
        mock_mean.assert_called()
        assert isinstance(result, dict)
    
    def test_thread_safety(self):
        """Test basique de thread safety."""
        import threading
        import queue
        
        results_queue = queue.Queue()
        data = np.random.randn(1000)
        
        def worker():
            try:
                result = self.analyzer.analyze(data)
                results_queue.put(('success', result))
            except Exception as e:
                results_queue.put(('error', str(e)))
        
        # Lancer plusieurs threads
        threads = []
        for _ in range(3):
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
                assert isinstance(result, dict)
        
        assert success_count == 3


class TestOptimizedGodaAnalyzerIntegration:
    """Tests d'intégration pour OptimizedGodaAnalyzer."""
    
    def test_real_time_analysis(self):
        """Test analyse en temps réel simulée."""
        config = GodaOptimizationConfig()
        analyzer = OptimizedGodaAnalyzer(config)
        
        # Simuler des blocs de données en temps réel
        block_size = 1000
        total_blocks = 10
        
        results = []
        for i in range(total_blocks):
            # Générer un bloc de données
            t = np.linspace(i, i+1, block_size)
            block_data = np.sin(2 * np.pi * 0.1 * t) + 0.1 * np.random.randn(block_size)
            
            result = analyzer.analyze(block_data)
            results.append(result)
        
        # Vérifier tous les résultats
        for result in results:
            assert isinstance(result, dict)
            assert 'significant_wave_height' in result
    
    def test_batch_analysis(self):
        """Test analyse par lots."""
        config = GodaOptimizationConfig()
        analyzer = OptimizedGodaAnalyzer(config)
        
        # Analyser plusieurs ensembles de données
        datasets = []
        for i in range(5):
            t = np.linspace(0, 20, 2000)
            amplitude = 1.0 + i * 0.5
            data = amplitude * np.sin(2 * np.pi * 0.1 * t)
            datasets.append(data)
        
        results = []
        for data in datasets:
            result = analyzer.analyze(data)
            results.append(result)
        
        # Vérifier que les hauteurs augmentent avec l'amplitude
        heights = [r.get('significant_wave_height', 0) for r in results]
        heights = [h for h in heights if h is not None and h > 0]
        
        if len(heights) > 1:
            # Les hauteurs devraient généralement augmenter
            assert max(heights) > min(heights)
    
    def test_configuration_impact(self):
        """Test l'impact des changements de configuration."""
        data = np.random.randn(2000)
        
        # Configuration standard
        config1 = GodaOptimizationConfig(analysis_window=10.0)
        analyzer1 = OptimizedGodaAnalyzer(config1)
        result1 = analyzer1.analyze(data)
        
        # Configuration avec fenêtre différente
        config2 = GodaOptimizationConfig(analysis_window=20.0)
        analyzer2 = OptimizedGodaAnalyzer(config2)
        result2 = analyzer2.analyze(data)
        
        # Les résultats peuvent être différents
        assert isinstance(result1, dict)
        assert isinstance(result2, dict)