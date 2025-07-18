"""Tests complets pour optimization_config.py.

Ce module teste toutes les configurations et la sérialisation/désérialisation.
"""

import pytest
import numpy as np
import tempfile
import os
import json
from unittest.mock import Mock, patch, mock_open
from dataclasses import asdict

try:
    from src.hrneowave.config.optimization_config import (
        FFTOptimizationConfig,
        GodaOptimizationConfig,
        CircularBufferConfig,
        AcquisitionConfig,
        PerformanceConfig,
        CHNeoWaveOptimizationConfig,
        FFTConfig,  # Alias
        GodaConfig,  # Alias
        BufferConfig  # Alias
    )
except ImportError:
    pytest.skip("optimization_config non disponible", allow_module_level=True)


class TestFFTOptimizationConfig:
    """Tests pour FFTOptimizationConfig."""
    
    def test_default_initialization(self):
        """Test l'initialisation par défaut."""
        config = FFTOptimizationConfig()
        
        assert config.use_pyfftw is True
        assert config.wisdom_file == 'fftw_wisdom.dat'
        assert config.threads == 4
        assert config.enable_simd is True
        assert config.planning_effort == 'FFTW_MEASURE'
        assert config.cache_size == 100
    
    def test_custom_initialization(self):
        """Test l'initialisation avec paramètres personnalisés."""
        config = FFTOptimizationConfig(
            use_pyfftw=False,
            wisdom_file='custom_wisdom.dat',
            threads=8,
            enable_simd=False,
            planning_effort='FFTW_ESTIMATE',
            cache_size=50
        )
        
        assert config.use_pyfftw is False
        assert config.wisdom_file == 'custom_wisdom.dat'
        assert config.threads == 8
        assert config.enable_simd is False
        assert config.planning_effort == 'FFTW_ESTIMATE'
        assert config.cache_size == 50
    
    def test_validation(self):
        """Test la validation des paramètres."""
        # Nombre de threads invalide (sera corrigé automatiquement)
        config = FFTOptimizationConfig(threads=0)
        assert config.threads == 1  # Corrigé automatiquement
        
        config = FFTOptimizationConfig(threads=100)
        assert config.threads <= 32  # Limité automatiquement
        
        # Fichier wisdom vide (sera corrigé automatiquement)
        config = FFTOptimizationConfig(wisdom_file='')
        assert config.wisdom_file == 'fftw_wisdom.dat'  # Valeur par défaut
    
    def test_serialization(self):
        """Test la sérialisation."""
        config = FFTOptimizationConfig(
            wisdom_file='test_wisdom.dat',
            threads=6
        )
        
        # Conversion en dictionnaire
        config_dict = asdict(config)
        
        assert isinstance(config_dict, dict)
        assert config_dict['wisdom_file'] == 'test_wisdom.dat'
        assert config_dict['threads'] == 6
    
    def test_alias_compatibility(self):
        """Test la compatibilité avec l'alias FFTConfig."""
        config1 = FFTOptimizationConfig()
        config2 = FFTConfig()
        
        # Les deux doivent être du même type
        assert type(config1) == type(config2)
        assert config1.use_pyfftw == config2.use_pyfftw


class TestGodaOptimizationConfig:
    """Tests pour GodaOptimizationConfig."""
    
    def test_default_initialization(self):
        """Test l'initialisation par défaut."""
        config = GodaOptimizationConfig()
        
        assert config.use_svd_decomposition is True
        assert config.svd_threshold == 1e-12
        assert config.cache_geometry_matrices is True
        assert config.cache_dispersion_relation is True
        assert config.max_cache_size == 1000
    
    def test_custom_initialization(self):
        """Test l'initialisation avec paramètres personnalisés."""
        config = GodaOptimizationConfig(
            use_svd_decomposition=False,
            svd_threshold=1e-10,
            cache_geometry_matrices=False,
            max_cache_size=500,
            enable_parallel_processing=False
        )
        
        assert config.use_svd_decomposition is False
        assert config.svd_threshold == 1e-10
        assert config.cache_geometry_matrices is False
        assert config.max_cache_size == 500
        assert config.enable_parallel_processing is False
    
    def test_validation(self):
        """Test la validation des paramètres."""
        # Seuil SVD invalide
        with pytest.raises((ValueError, TypeError)):
            GodaOptimizationConfig(svd_threshold=-1)
        
        with pytest.raises((ValueError, TypeError)):
            GodaOptimizationConfig(svd_threshold=0)
        
        # Taille de cache invalide (sera corrigée automatiquement)
        config = GodaOptimizationConfig(max_cache_size=5)
        assert config.max_cache_size == 10  # Corrigé automatiquement
    
    def test_serialization(self):
        """Test la sérialisation."""
        config = GodaOptimizationConfig(
            svd_threshold=1e-10,
            max_cache_size=500
        )
        
        config_dict = asdict(config)
        
        assert isinstance(config_dict, dict)
        assert config_dict['svd_threshold'] == 1e-10
        assert config_dict['max_cache_size'] == 500
    
    def test_alias_compatibility(self):
        """Test la compatibilité avec l'alias GodaConfig."""
        config1 = GodaOptimizationConfig()
        config2 = GodaConfig()
        
        assert type(config1) == type(config2)
        assert config1.use_svd_decomposition == config2.use_svd_decomposition


class TestCircularBufferConfig:
    """Tests pour CircularBufferConfig."""
    
    def test_default_initialization(self):
        """Test l'initialisation par défaut."""
        config = CircularBufferConfig()
        
        assert config.default_size == 1000
        assert config.enable_lock_free is True
        assert config.enable_overflow_detection is True
        assert config.enable_statistics is True
        assert config.memory_mapping is False
        assert config.alignment_bytes == 64
    
    def test_custom_initialization(self):
        """Test l'initialisation avec paramètres personnalisés."""
        config = CircularBufferConfig(
            default_size=2048,
            enable_lock_free=False,
            enable_overflow_detection=False,
            enable_statistics=False,
            memory_mapping=True,
            alignment_bytes=32
        )
        
        assert config.default_size == 2048
        assert config.enable_lock_free is False
        assert config.enable_overflow_detection is False
        assert config.enable_statistics is False
        assert config.memory_mapping is True
        assert config.alignment_bytes == 32
    
    def test_validation(self):
        """Test la validation des paramètres."""
        # Test valeur invalide pour default_size
        with pytest.raises(ValueError):
            CircularBufferConfig(default_size=50)  # < 100
        
        # Test valeur valide
        config = CircularBufferConfig(default_size=500)
        assert config.default_size == 500
        
        # Test correction automatique alignment_bytes
        config = CircularBufferConfig(alignment_bytes=48)
        assert config.alignment_bytes == 64
    
    def test_serialization(self):
        """Test la sérialisation."""
        config = CircularBufferConfig(
            default_size=2048,
            memory_mapping=True
        )
        
        config_dict = asdict(config)
        
        assert isinstance(config_dict, dict)
        assert config_dict['default_size'] == 2048
        assert config_dict['memory_mapping'] is True
    
    def test_alias_compatibility(self):
        """Test la compatibilité avec l'alias BufferConfig."""
        config1 = CircularBufferConfig()
        config2 = BufferConfig()
        
        assert type(config1) == type(config2)
        assert config1.memory_mapping == config2.memory_mapping


class TestAcquisitionConfig:
    """Tests pour AcquisitionConfig."""
    
    def test_default_initialization(self):
        """Test l'initialisation par défaut."""
        config = AcquisitionConfig()
        
        assert config.sampling_rate_hz == 1000.0
        assert config.num_channels == 4
        assert config.buffer_duration_seconds == 10.0
        assert config.enable_anti_aliasing is True
        assert config.anti_aliasing_cutoff_hz == 250.0
        assert config.enable_real_time_processing is True
        assert config.processing_chunk_size == 512
    
    def test_custom_initialization(self):
        """Test l'initialisation avec paramètres personnalisés."""
        config = AcquisitionConfig(
            sampling_rate_hz=2000.0,
            num_channels=8,
            buffer_duration_seconds=15.0,
            enable_anti_aliasing=False,
            anti_aliasing_cutoff_hz=400.0,
            enable_real_time_processing=False,
            processing_chunk_size=1024
        )
        
        assert config.sampling_rate_hz == 2000.0
        assert config.num_channels == 8
        assert config.buffer_duration_seconds == 15.0
        assert config.enable_anti_aliasing is False
        assert config.anti_aliasing_cutoff_hz == 400.0
        assert config.enable_real_time_processing is False
        assert config.processing_chunk_size == 1024
    
    def test_validation(self):
        """Test la validation des paramètres."""
        # Test valeur invalide pour sampling_rate_hz
        with pytest.raises(ValueError):
            AcquisitionConfig(sampling_rate_hz=0)
        
        # Test valeur invalide pour num_channels
        with pytest.raises(ValueError):
            AcquisitionConfig(num_channels=0)
        
        with pytest.raises(ValueError):
            AcquisitionConfig(num_channels=20)
        
        # Test correction automatique anti_aliasing_cutoff_hz
        config = AcquisitionConfig(sampling_rate_hz=1000.0, anti_aliasing_cutoff_hz=600.0)
        assert config.anti_aliasing_cutoff_hz == 400.0  # 1000/2.5
    
    def test_serialization(self):
        """Test la sérialisation."""
        config = AcquisitionConfig(
            sampling_rate_hz=2000.0,
            num_channels=8
        )
        
        config_dict = asdict(config)
        
        assert isinstance(config_dict, dict)
        assert config_dict['sampling_rate_hz'] == 2000.0
        assert config_dict['num_channels'] == 8


class TestPerformanceConfig:
    """Tests pour PerformanceConfig."""
    
    def test_default_initialization(self):
        """Test l'initialisation par défaut."""
        config = PerformanceConfig()
        
        assert config.enable_profiling is False
        assert config.enable_benchmarking is True
        assert config.benchmark_iterations == 100
        assert config.memory_monitoring is True
        assert config.latency_monitoring is True
        assert config.export_metrics is True
        assert config.metrics_file == "performance_metrics.json"
    
    def test_custom_initialization(self):
        """Test l'initialisation avec paramètres personnalisés."""
        config = PerformanceConfig(
            enable_profiling=True,
            enable_benchmarking=False,
            benchmark_iterations=200,
            memory_monitoring=False,
            latency_monitoring=False,
            export_metrics=False,
            metrics_file="custom_metrics.json"
        )
        
        assert config.enable_profiling is True
        assert config.enable_benchmarking is False
        assert config.benchmark_iterations == 200
        assert config.memory_monitoring is False
        assert config.latency_monitoring is False
        assert config.export_metrics is False
        assert config.metrics_file == "custom_metrics.json"
    
    def test_validation(self):
        """Test la validation des paramètres."""
        # Nombre d'itérations invalide
        with pytest.raises((ValueError, TypeError)):
            PerformanceConfig(benchmark_iterations=-1)
        
        # Fichier de métriques vide
        with pytest.raises((ValueError, TypeError)):
            PerformanceConfig(metrics_file="")
        
        # Nombre d'itérations trop faible
        with pytest.raises((ValueError, TypeError)):
            PerformanceConfig(benchmark_iterations=0)
    
    def test_serialization(self):
        """Test la sérialisation."""
        config = PerformanceConfig(
            enable_profiling=True,
            benchmark_iterations=150
        )
        
        config_dict = asdict(config)
        
        assert isinstance(config_dict, dict)
        assert config_dict['enable_profiling'] is True
        assert config_dict['benchmark_iterations'] == 150


class TestCHNeoWaveOptimizationConfig:
    """Tests pour CHNeoWaveOptimizationConfig."""
    
    def test_default_initialization(self):
        """Test l'initialisation par défaut."""
        config = CHNeoWaveOptimizationConfig()
        
        assert isinstance(config.fft, FFTOptimizationConfig)
        assert isinstance(config.goda, GodaOptimizationConfig)
        assert isinstance(config.buffer, CircularBufferConfig)
        assert isinstance(config.acquisition, AcquisitionConfig)
        assert isinstance(config.performance, PerformanceConfig)
    
    def test_to_dict(self):
        """Test la conversion en dictionnaire."""
        config = CHNeoWaveOptimizationConfig()
        
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert 'fft' in config_dict
        assert 'goda' in config_dict
        assert 'buffer' in config_dict
        assert 'acquisition' in config_dict
        assert 'performance' in config_dict
        
        # Vérifier que chaque section est un dictionnaire
        for section in config_dict.values():
            assert isinstance(section, dict)
    
    def test_save_to_file(self):
        """Test la sauvegarde dans un fichier."""
        config = CHNeoWaveOptimizationConfig()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Sauvegarder
            config.save_to_file(temp_file)
            
            # Vérifier que le fichier existe
            assert os.path.exists(temp_file)
            
            # Vérifier le contenu
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            
            assert isinstance(saved_data, dict)
            assert 'fft' in saved_data
            assert 'goda' in saved_data
            
        finally:
            # Nettoyer
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_load_from_file(self):
        """Test le chargement depuis un fichier."""
        # Créer une configuration de test
        test_config = {
            'fft': {
                'use_pyfftw': True,
                'wisdom_file': 'test_wisdom.dat',
                'threads': 8,
                'planning_effort': 'FFTW_MEASURE',
                'cache_size': 200,
                'enable_simd': True
            },
            'goda': {
                'use_svd_decomposition': True,
                'svd_threshold': 1e-10,
                'cache_geometry_matrices': True,
                'cache_dispersion_relation': True,
                'max_cache_size': 2000,
                'enable_parallel_processing': True,
                'numerical_stability_check': True
            },
            'buffer': {
                'default_size': 16384,
                'enable_lock_free': True,
                'enable_overflow_detection': True,
                'enable_statistics': True,
                'memory_mapping': True,
                'alignment_bytes': 64
            },
            'acquisition': {
                'sampling_rate_hz': 2000.0,
                'num_channels': 4,
                'buffer_duration_seconds': 10.0,
                'enable_anti_aliasing': True,
                'anti_aliasing_cutoff_hz': 500.0,
                'enable_real_time_processing': True,
                'processing_chunk_size': 1024
            },
            'performance': {
                'enable_profiling': True,
                'enable_benchmarking': True,
                'benchmark_iterations': 50,
                'memory_monitoring': True,
                'latency_monitoring': True,
                'export_metrics': True,
                'metrics_file': 'test_metrics.json'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name
        
        try:
            # Charger la configuration
            config = CHNeoWaveOptimizationConfig(temp_file)
            
            # Vérifier les valeurs chargées
            assert config.fft.use_pyfftw == True
            assert config.fft.wisdom_file == 'test_wisdom.dat'
            assert config.fft.threads == 8
            assert config.fft.planning_effort == 'FFTW_MEASURE'
            assert config.fft.cache_size == 200
            assert config.fft.enable_simd == True
            
            assert config.goda.use_svd_decomposition == True
            assert config.goda.svd_threshold == 1e-10
            assert config.goda.cache_geometry_matrices == True
            assert config.goda.cache_dispersion_relation == True
            assert config.goda.max_cache_size == 2000
            assert config.goda.enable_parallel_processing == True
            assert config.goda.numerical_stability_check == True
            
            assert config.buffer.default_size == 16384
            assert config.buffer.enable_lock_free == True
            assert config.buffer.enable_overflow_detection == True
            assert config.buffer.enable_statistics == True
            assert config.buffer.memory_mapping == True
            assert config.buffer.alignment_bytes == 64
            
            assert config.acquisition.sampling_rate_hz == 2000.0
            assert config.acquisition.num_channels == 4
            assert config.acquisition.buffer_duration_seconds == 10.0
            assert config.acquisition.enable_anti_aliasing == True
            assert config.acquisition.anti_aliasing_cutoff_hz == 500.0
            assert config.acquisition.enable_real_time_processing == True
            assert config.acquisition.processing_chunk_size == 1024
            
            assert config.performance.enable_profiling == True
            assert config.performance.enable_benchmarking == True
            assert config.performance.benchmark_iterations == 50
            assert config.performance.memory_monitoring == True
            assert config.performance.latency_monitoring == True
            assert config.performance.export_metrics == True
            assert config.performance.metrics_file == 'test_metrics.json'
            
        finally:
            # Nettoyer
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_load_from_nonexistent_file(self):
        """Test le chargement d'un fichier inexistant."""
        with pytest.raises(FileNotFoundError):
            CHNeoWaveOptimizationConfig('nonexistent_file.json')
    
    def test_load_from_invalid_json(self):
        """Test le chargement d'un JSON invalide."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('invalid json content {')
            temp_file = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                CHNeoWaveOptimizationConfig(temp_file)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_partial_configuration_loading(self):
        """Test le chargement d'une configuration partielle."""
        # Configuration partielle (seulement FFT)
        partial_config = {
            'fft': {
                'use_pyfftw': True,
                'threads': 8
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(partial_config, f)
            temp_file = f.name
        
        try:
            config = CHNeoWaveOptimizationConfig(temp_file)
            
            # FFT doit être mis à jour
            assert config.fft.use_pyfftw == True
            assert config.fft.threads == 8
            
            # Les autres doivent garder les valeurs par défaut
            assert config.goda.use_svd_decomposition == True  # Valeur par défaut
            assert config.buffer.memory_mapping == False  # Valeur par défaut
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_configuration_validation(self):
        """Test la validation de la configuration complète."""
        config = CHNeoWaveOptimizationConfig()
        
        # Modifier une valeur pour la rendre invalide
        config.fft.threads = -1
        
        # La validation devrait échouer lors de la sérialisation
        with pytest.raises((ValueError, TypeError)):
            config.to_dict()
    
    def test_configuration_copy(self):
        """Test la copie de configuration."""
        config1 = CHNeoWaveOptimizationConfig()
        config1.fft.use_pyfftw = True
        config1.goda.use_svd_decomposition = True
        
        # Créer une copie via sérialisation/désérialisation
        config_dict = config1.to_dict()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_dict, f)
            temp_file = f.name
        
        try:
            config2 = CHNeoWaveOptimizationConfig(temp_file)
            
            # Vérifier que les valeurs sont identiques
            assert config2.fft.use_pyfftw == config1.fft.use_pyfftw
            assert config2.goda.use_svd_decomposition == config1.goda.use_svd_decomposition
            
            # Modifier config1 ne doit pas affecter config2
            config1.fft.use_pyfftw = False
            assert config2.fft.use_pyfftw == True
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    @patch('builtins.open', mock_open(read_data='{"fft": {"use_pyfftw": true}}'))
    def test_load_with_mock(self):
        """Test le chargement avec mock."""
        config = CHNeoWaveOptimizationConfig('mock_file.json')
        
        # Vérifier que la valeur mockée est chargée
        assert config.fft.use_pyfftw == True
    
    def test_thread_safety(self):
        """Test basique de thread safety."""
        import threading
        import queue
        
        config = CHNeoWaveOptimizationConfig()
        results_queue = queue.Queue()
        
        def worker():
            try:
                # Opérations de lecture/écriture
                config_dict = config.to_dict()
                config.fft.use_pyfftw = True
                results_queue.put(('success', config_dict))
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


class TestConfigurationIntegration:
    """Tests d'intégration pour toutes les configurations."""
    
    def test_complete_workflow(self):
        """Test du workflow complet de configuration."""
        # 1. Créer une configuration
        config = CHNeoWaveOptimizationConfig()
        
        # 2. Modifier les paramètres
        config.fft.use_pyfftw = True
        config.fft.threads = 8
        config.goda.use_svd_decomposition = True
        config.buffer.memory_mapping = True
        config.acquisition.enable_real_time_processing = True
        config.performance.enable_profiling = True
        
        # 3. Sauvegarder
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            config.save_to_file(temp_file)
            
            # 4. Charger dans une nouvelle instance
            config2 = CHNeoWaveOptimizationConfig(temp_file)
            
            # 5. Vérifier que tout est identique
            assert config2.fft.use_pyfftw == True
            assert config2.fft.threads == 8
            assert config2.goda.use_svd_decomposition == True
            assert config2.buffer.memory_mapping == True
            assert config2.acquisition.enable_real_time_processing == True
            assert config2.performance.enable_profiling == True
            
            # 6. Vérifier la sérialisation
            dict1 = config.to_dict()
            dict2 = config2.to_dict()
            
            assert dict1 == dict2
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_configuration_compatibility(self):
        """Test la compatibilité entre versions de configuration."""
        # Simuler une ancienne version de configuration
        old_config = {
            'fft': {
                'use_pyfftw': True,
                'threads': 2
                # Champs manquants: wisdom_file, planning_effort, enable_simd
            },
            'goda': {
                'use_svd_decomposition': True
                # Champs manquants: svd_threshold, cache_geometry_matrices, etc.
            }
            # Sections manquantes: buffer, acquisition, performance
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(old_config, f)
            temp_file = f.name
        
        try:
            # Charger l'ancienne configuration
            config = CHNeoWaveOptimizationConfig(temp_file)
            
            # Vérifier que les valeurs par défaut sont utilisées pour les champs manquants
            assert config.fft.use_pyfftw == True  # Chargé
            assert config.fft.threads == 2  # Chargé
            assert config.fft.wisdom_file == 'fftw_wisdom.dat'  # Défaut
            assert config.goda.use_svd_decomposition == True  # Chargé
            assert config.buffer.memory_mapping == False  # Défaut (section manquante)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_performance_configuration(self):
        """Test la configuration de performance."""
        config = CHNeoWaveOptimizationConfig()
        
        # Configuration haute performance
        config.fft.use_pyfftw = True  # FFTW pour rapidité
        config.fft.threads = 8  # Multi-threading
        config.buffer.memory_mapping = True  # Memory mapping
        config.performance.enable_profiling = True  # Profiling activé
        
        # Vérifier la cohérence
        config_dict = config.to_dict()
        assert config_dict['fft']['use_pyfftw'] == True
        assert config_dict['fft']['threads'] == 8
        assert config_dict['performance']['enable_profiling'] == True
    
    def test_memory_configuration(self):
        """Test la configuration mémoire."""
        config = CHNeoWaveOptimizationConfig()
        
        # Configuration économe en mémoire
        config.buffer.memory_mapping = False  # Pas de memory mapping
        config.performance.enable_benchmarking = True  # Benchmarking activé
        
        # Vérifier la cohérence
        config_dict = config.to_dict()
        assert config_dict['buffer']['memory_mapping'] == False
        assert config_dict['performance']['enable_benchmarking'] == True