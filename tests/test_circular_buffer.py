"""Tests unitaires pour CircularBuffer.

Ce module teste toutes les fonctionnalités du buffer circulaire optimisé.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import time
import threading

try:
    from src.hrneowave.core.circular_buffer import CircularBuffer
except ImportError:
    pytest.skip("CircularBuffer non disponible", allow_module_level=True)


class TestCircularBuffer:
    """Tests pour CircularBuffer."""
    
    def setup_method(self):
        """Configuration avant chaque test."""
        self.buffer_size = 1024
        self.buffer = CircularBuffer(self.buffer_size)
    
    def test_initialization(self):
        """Test l'initialisation du buffer."""
        assert self.buffer.size == self.buffer_size
        assert self.buffer.count == 0
        assert self.buffer.is_empty()
        assert not self.buffer.is_full()
    
    def test_initialization_invalid_size(self):
        """Test l'initialisation avec une taille invalide."""
        with pytest.raises((ValueError, TypeError)):
            CircularBuffer(-1)
        
        with pytest.raises((ValueError, TypeError)):
            CircularBuffer(0)
    
    def test_add_single_value(self):
        """Test l'ajout d'une seule valeur."""
        value = 42.0
        self.buffer.add(value)
        
        assert self.buffer.count == 1
        assert not self.buffer.is_empty()
        assert not self.buffer.is_full()
    
    def test_add_multiple_values(self):
        """Test l'ajout de plusieurs valeurs."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        for value in values:
            self.buffer.add(value)
        
        assert self.buffer.count == len(values)
        assert not self.buffer.is_empty()
    
    def test_add_array(self):
        """Test l'ajout d'un tableau."""
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.buffer.add_data(data)
        
        assert self.buffer.count == len(data)
        assert not self.buffer.is_empty()
    
    def test_fill_buffer(self):
        """Test le remplissage complet du buffer."""
        # Remplir exactement le buffer
        for i in range(self.buffer_size):
            self.buffer.add(float(i))
        
        assert self.buffer.count == self.buffer_size
        assert self.buffer.is_full()
        assert not self.buffer.is_empty()
    
    def test_overflow_behavior(self):
        """Test le comportement en cas de débordement."""
        # Remplir le buffer
        for i in range(self.buffer_size):
            self.buffer.add(float(i))
        
        # Ajouter des valeurs supplémentaires
        overflow_values = [1000.0, 1001.0, 1002.0]
        for value in overflow_values:
            self.buffer.add(value)
        
        # Le buffer doit toujours être plein
        assert self.buffer.is_full()
        assert self.buffer.count == self.buffer_size
    
    def test_get_data(self):
        """Test la récupération des données."""
        test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        for value in test_data:
            self.buffer.add(value)
        
        retrieved_data = self.buffer.get_data()
        
        assert isinstance(retrieved_data, np.ndarray)
        assert len(retrieved_data) == len(test_data)
        np.testing.assert_array_equal(retrieved_data, test_data)
    
    def test_get_data_partial(self):
        """Test la récupération partielle des données."""
        test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        for value in test_data:
            self.buffer.add(value)
        
        # Récupérer seulement 3 éléments
        partial_data = self.buffer.get_data(3)
        
        assert isinstance(partial_data, np.ndarray)
        assert len(partial_data) == 3
        np.testing.assert_array_equal(partial_data, test_data[-3:])  # Les 3 derniers
    
    def test_get_data_more_than_available(self):
        """Test la récupération de plus de données que disponible."""
        test_data = [1.0, 2.0, 3.0]
        
        for value in test_data:
            self.buffer.add(value)
        
        # Demander plus que disponible
        retrieved_data = self.buffer.get_data(10)
        
        assert isinstance(retrieved_data, np.ndarray)
        assert len(retrieved_data) == len(test_data)
        np.testing.assert_array_equal(retrieved_data, test_data)
    
    def test_get_latest(self):
        """Test la récupération de la dernière valeur."""
        test_values = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        for value in test_values:
            self.buffer.add(value)
        
        latest = self.buffer.get_latest()
        assert latest == test_values[-1]
    
    def test_get_latest_empty_buffer(self):
        """Test la récupération de la dernière valeur sur buffer vide."""
        with pytest.raises((IndexError, ValueError)):
            self.buffer.get_latest()
    
    def test_clear(self):
        """Test la remise à zéro du buffer."""
        # Ajouter des données
        for i in range(10):
            self.buffer.add(float(i))
        
        assert not self.buffer.is_empty()
        
        # Vider le buffer
        self.buffer.reset()
        
        assert self.buffer.is_empty()
        assert self.buffer.count == 0
    
    def test_usage_percentage(self):
        """Test le calcul du pourcentage d'utilisation."""
        # Buffer vide
        assert self.buffer.get_usage_percentage() == 0.0
        
        # Buffer à moitié plein
        for i in range(self.buffer_size // 2):
            self.buffer.add(float(i))
        
        usage = self.buffer.get_usage_percentage()
        assert 45.0 <= usage <= 55.0  # Environ 50%
        
        # Buffer plein
        for i in range(self.buffer_size // 2, self.buffer_size):
            self.buffer.add(float(i))
        
        assert self.buffer.get_usage_percentage() == 100.0
    
    def test_circular_behavior(self):
        """Test le comportement circulaire."""
        # Remplir le buffer avec des valeurs connues
        for i in range(self.buffer_size):
            self.buffer.add(float(i))
        
        # Ajouter des valeurs qui vont écraser les premières
        new_values = [9999.0, 9998.0, 9997.0]
        for value in new_values:
            self.buffer.add(value)
        
        # Récupérer toutes les données
        all_data = self.buffer.get_data()
        
        # Les nouvelles valeurs doivent être à la fin
        assert all_data[-len(new_values):].tolist() == new_values
    
    def test_add_large_array(self):
        """Test l'ajout d'un grand tableau."""
        large_data = np.random.randn(2000)  # Plus grand que le buffer
        
        self.buffer.add_data(large_data)
        
        # Le buffer doit être plein
        assert self.buffer.is_full()
        
        # Les données récupérées doivent être les dernières du tableau
        retrieved = self.buffer.get_data()
        expected = large_data[-self.buffer_size:]
        
        np.testing.assert_array_equal(retrieved, expected)
    
    def test_performance_add(self):
        """Test de performance pour l'ajout."""
        data = np.random.randn(1000)
        
        start_time = time.perf_counter()
        self.buffer.add_data(data)
        end_time = time.perf_counter()
        
        add_time = (end_time - start_time) * 1000  # en ms
        assert add_time < 10.0, f"Ajout trop lent: {add_time:.2f}ms"
    
    def test_performance_get(self):
        """Test de performance pour la récupération."""
        # Remplir le buffer
        data = np.random.randn(self.buffer_size)
        self.buffer.add_data(data)
        
        start_time = time.perf_counter()
        retrieved = self.buffer.get_data()
        end_time = time.perf_counter()
        
        get_time = (end_time - start_time) * 1000  # en ms
        assert get_time < 5.0, f"Récupération trop lente: {get_time:.2f}ms"
        assert isinstance(retrieved, np.ndarray)
    
    def test_thread_safety_basic(self):
        """Test basique de thread safety."""
        import queue
        
        results_queue = queue.Queue()
        
        def writer_thread(start_val):
            try:
                for i in range(100):
                    self.buffer.add(float(start_val + i))
                results_queue.put(('write_success', start_val))
            except Exception as e:
                results_queue.put(('write_error', str(e)))
        
        def reader_thread():
            try:
                for _ in range(10):
                    if not self.buffer.is_empty():
                        data = self.buffer.get_data(10)
                        assert isinstance(data, np.ndarray)
                    time.sleep(0.001)
                results_queue.put(('read_success', None))
            except Exception as e:
                results_queue.put(('read_error', str(e)))
        
        # Lancer les threads
        threads = []
        
        # 2 threads d'écriture
        for i in range(2):
            t = threading.Thread(target=writer_thread, args=(i * 1000,))
            threads.append(t)
            t.start()
        
        # 1 thread de lecture
        t = threading.Thread(target=reader_thread)
        threads.append(t)
        t.start()
        
        # Attendre la fin
        for t in threads:
            t.join()
        
        # Vérifier les résultats
        success_count = 0
        while not results_queue.empty():
            status, result = results_queue.get()
            if 'success' in status:
                success_count += 1
        
        assert success_count >= 2  # Au moins les écritures
    
    def test_memory_efficiency(self):
        """Test l'efficacité mémoire."""
        # Le buffer ne doit pas consommer plus que sa taille allouée
        initial_size = self.buffer.size
        
        # Ajouter beaucoup de données
        for _ in range(10):
            large_data = np.random.randn(self.buffer_size)
            self.buffer.add_data(large_data)
        
        # La taille du buffer ne doit pas avoir changé
        assert self.buffer.size == initial_size
        assert self.buffer.count <= self.buffer_size
    
    def test_data_types(self):
        """Test avec différents types de données."""
        # Float
        self.buffer.add(3.14)
        assert self.buffer.count == 1
        
        # Int (converti en float)
        self.buffer.add(42)
        assert self.buffer.count == 2
        
        # Numpy scalar
        self.buffer.add(np.float64(2.71))
        assert self.buffer.count == 3
        
        # Récupérer et vérifier
        data = self.buffer.get_data()
        assert len(data) == 3
        assert data.dtype == np.float64 or data.dtype == np.float32
    
    def test_edge_cases(self):
        """Test les cas limites."""
        # Valeurs extrêmes
        extreme_values = [1e10, -1e10, 1e-10, -1e-10, 0.0, np.inf, -np.inf]
        
        for value in extreme_values:
            if np.isfinite(value):  # Ignorer inf pour ce test
                self.buffer.add(value)
        
        data = self.buffer.get_data()
        assert len(data) > 0
        assert np.all(np.isfinite(data))
    
    def test_nan_handling(self):
        """Test la gestion des NaN."""
        # Ajouter des valeurs normales
        self.buffer.add(1.0)
        self.buffer.add(2.0)
        
        # Ajouter NaN
        self.buffer.add(np.nan)
        
        # Ajouter d'autres valeurs
        self.buffer.add(3.0)
        
        data = self.buffer.get_data()
        assert len(data) == 4
        
        # Vérifier que NaN est présent
        nan_count = np.sum(np.isnan(data))
        assert nan_count == 1
    
    def test_resize_buffer(self):
        """Test le redimensionnement du buffer si supporté."""
        if hasattr(self.buffer, 'resize'):
            # Ajouter des données
            for i in range(100):
                self.buffer.add(float(i))
            
            original_count = self.buffer.count
            
            # Redimensionner
            new_size = 2048
            self.buffer.resize(new_size)
            
            assert self.buffer.size == new_size
            assert self.buffer.count <= original_count  # Données préservées ou tronquées
    
    def test_statistics(self):
        """Test les statistiques du buffer si supportées."""
        # Ajouter des données avec statistiques connues
        test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        for value in test_data:
            self.buffer.add(value)
        
        if hasattr(self.buffer, 'get_mean'):
            mean = self.buffer.get_mean()
            assert abs(mean - 3.0) < 0.1
        
        if hasattr(self.buffer, 'get_std'):
            std = self.buffer.get_std()
            assert std > 0
        
        if hasattr(self.buffer, 'get_min'):
            min_val = self.buffer.get_min()
            assert min_val == 1.0
        
        if hasattr(self.buffer, 'get_max'):
            max_val = self.buffer.get_max()
            assert max_val == 5.0
    
    def test_copy_buffer(self):
        """Test la copie du buffer si supportée."""
        # Ajouter des données
        test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
        for value in test_data:
            self.buffer.add(value)
        
        if hasattr(self.buffer, 'copy'):
            buffer_copy = self.buffer.copy()
            
            # Vérifier que la copie est identique
            original_data = self.buffer.get_data()
            copied_data = buffer_copy.get_data()
            
            np.testing.assert_array_equal(original_data, copied_data)
            
            # Vérifier que c'est une vraie copie
            self.buffer.add(999.0)
            assert not np.array_equal(self.buffer.get_data(), buffer_copy.get_data())


class TestCircularBufferIntegration:
    """Tests d'intégration pour CircularBuffer."""
    
    def test_real_time_simulation(self):
        """Test simulation temps réel."""
        buffer = CircularBuffer(1000)
        
        # Simuler l'acquisition en temps réel
        sample_rate = 1000  # Hz
        duration = 5  # secondes
        
        for i in range(duration * sample_rate):
            # Simuler un signal sinusoïdal avec bruit
            t = i / sample_rate
            signal = np.sin(2 * np.pi * 10 * t) + 0.1 * np.random.randn()
            
            buffer.add(signal)
            
            # Vérifier périodiquement
            if i % 100 == 0 and i > 0:
                data = buffer.get_data(100)
                assert len(data) == min(100, buffer.count)
        
        # Vérifications finales
        assert buffer.is_full()
        final_data = buffer.get_data()
        assert len(final_data) == 1000
    
    def test_streaming_analysis(self):
        """Test analyse en streaming."""
        buffer = CircularBuffer(512)
        
        # Simuler un flux de données avec analyse périodique
        analysis_results = []
        
        for block in range(20):
            # Ajouter un bloc de données
            block_data = np.random.randn(100)
            buffer.add_data(block_data)
            
            # Analyser si suffisamment de données
            if buffer.count >= 256:
                analysis_data = buffer.get_data(256)
                
                # Analyse simple
                result = {
                    'mean': np.mean(analysis_data),
                    'std': np.std(analysis_data),
                    'block': block
                }
                analysis_results.append(result)
        
        # Vérifier les résultats
        assert len(analysis_results) > 0
        for result in analysis_results:
            assert 'mean' in result
            assert 'std' in result
            assert np.isfinite(result['mean'])
            assert np.isfinite(result['std'])
    
    def test_multiple_buffers(self):
        """Test utilisation de plusieurs buffers."""
        # Créer plusieurs buffers pour différents canaux
        buffers = {
            'channel_1': CircularBuffer(1024),
            'channel_2': CircularBuffer(1024),
            'channel_3': CircularBuffer(1024)
        }
        
        # Simuler des données multi-canaux
        for i in range(2000):
            for channel, buffer in buffers.items():
                # Données différentes par canal
                if channel == 'channel_1':
                    value = np.sin(2 * np.pi * 0.1 * i)
                elif channel == 'channel_2':
                    value = np.cos(2 * np.pi * 0.2 * i)
                else:
                    value = np.random.randn()
                
                buffer.add(value)
        
        # Vérifier tous les buffers
        for channel, buffer in buffers.items():
            assert buffer.is_full()
            data = buffer.get_data()
            assert len(data) == 1024
            assert np.all(np.isfinite(data))
    
    def test_buffer_synchronization(self):
        """Test synchronisation entre buffers."""
        buffer1 = CircularBuffer(100)
        buffer2 = CircularBuffer(100)
        
        # Ajouter des données synchronisées
        for i in range(150):
            buffer1.add(float(i))
            buffer2.add(float(i * 2))  # Données liées
        
        # Récupérer les données
        data1 = buffer1.get_data()
        data2 = buffer2.get_data()
        
        # Vérifier la synchronisation
        assert len(data1) == len(data2)
        np.testing.assert_array_equal(data2, data1 * 2)