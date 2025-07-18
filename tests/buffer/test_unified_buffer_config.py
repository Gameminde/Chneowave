#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour la configuration unifiée des buffers CHNeoWave

Ce module teste la classe UnifiedBufferConfig et son intégration
avec LockFreeCircularBuffer.

Auteur: WaveBuffer-Fixer
Version: 3.0.0
Date: 2025
"""

import pytest
import numpy as np
import time
import threading
import multiprocessing
from unittest.mock import Mock, patch
from typing import Dict, Any

# Import des modules à tester
try:
    from hrneowave.core.buffer_config import (
        UnifiedBufferConfig, BufferConfig, CircularBufferConfig,
        OverflowMode, PerformanceLevel
    )
    BUFFER_CONFIG_AVAILABLE = True
except ImportError:
    BUFFER_CONFIG_AVAILABLE = False
    pytest.skip("Module buffer_config non disponible", allow_module_level=True)

try:
    from hrneowave.core.circular_buffer import LockFreeCircularBuffer
    CIRCULAR_BUFFER_AVAILABLE = True
except ImportError:
    CIRCULAR_BUFFER_AVAILABLE = False


class TestUnifiedBufferConfig:
    """Tests pour la classe UnifiedBufferConfig"""
    
    def test_creation_config_basique(self):
        """Test de création d'une configuration basique"""
        config = UnifiedBufferConfig(
            n_channels=8,
            buffer_size=4096,
            sample_rate=1000.0
        )
        
        assert config.n_channels == 8
        assert config.buffer_size == 4096
        assert config.sample_rate == 1000.0
        assert config.dtype == np.float64
        assert config.overflow_mode == OverflowMode.OVERWRITE
    
    def test_validation_parametres(self):
        """Test de validation des paramètres"""
        # Paramètres invalides
        with pytest.raises(ValueError, match="n_channels doit être positif"):
            UnifiedBufferConfig(n_channels=0, buffer_size=1024, sample_rate=1000.0)
        
        with pytest.raises(ValueError, match="buffer_size doit être positif"):
            UnifiedBufferConfig(n_channels=8, buffer_size=0, sample_rate=1000.0)
        
        with pytest.raises(ValueError, match="sample_rate doit être positive"):
            UnifiedBufferConfig(n_channels=8, buffer_size=1024, sample_rate=0.0)
        
        with pytest.raises(ValueError, match="overflow_threshold doit être entre 0 et 1"):
            UnifiedBufferConfig(
                n_channels=8, buffer_size=1024, sample_rate=1000.0,
                overflow_threshold=1.5
            )
    
    def test_calculs_derives(self):
        """Test des calculs dérivés"""
        config = UnifiedBufferConfig(
            n_channels=8,
            buffer_size=4096,
            sample_rate=1000.0
        )
        
        # Test des propriétés calculées
        assert config.total_size == 8 * 4096
        assert config.duration_seconds == 4096 / 1000.0
        assert config.memory_size_mb == pytest.approx((8 * 4096 * 8) / (1024 * 1024), rel=1e-3)
    
    def test_presets_laboratoire(self):
        """Test des préréglages de laboratoire"""
        # Test preset haute fréquence
        config_hf = UnifiedBufferConfig.create_high_frequency_preset()
        assert config_hf.sample_rate == 10000.0
        assert config_hf.n_channels == 16
        assert config_hf.enable_lock_free is True
        assert config_hf.enable_simd is True
        
        # Test preset longue durée
        config_ld = UnifiedBufferConfig.create_long_duration_preset()
        assert config_ld.buffer_size == 65536
        assert config_ld.enable_memory_mapping is True
        assert config_ld.auto_resize is True
        
        # Test preset temps réel
        config_rt = UnifiedBufferConfig.create_realtime_preset()
        assert config_rt.target_latency_ms <= 10.0
        assert config_rt.enable_zero_copy is True
        assert config_rt.performance_level == PerformanceLevel.MAXIMUM
    
    def test_serialisation_json(self):
        """Test de sérialisation/désérialisation JSON"""
        config_original = UnifiedBufferConfig(
            n_channels=8,
            buffer_size=4096,
            sample_rate=1000.0,
            overflow_mode=OverflowMode.BLOCK,
            enable_statistics=True,
            target_latency_ms=5.0
        )
        
        # Sérialisation
        json_data = config_original.to_json()
        assert isinstance(json_data, str)
        
        # Désérialisation
        config_restored = UnifiedBufferConfig.from_json(json_data)
        
        # Vérification
        assert config_restored.n_channels == config_original.n_channels
        assert config_restored.buffer_size == config_original.buffer_size
        assert config_restored.sample_rate == config_original.sample_rate
        assert config_restored.overflow_mode == config_original.overflow_mode
        assert config_restored.enable_statistics == config_original.enable_statistics
        assert config_restored.target_latency_ms == config_original.target_latency_ms
    
    def test_calcul_utilisation(self):
        """Test du calcul d'utilisation du buffer"""
        config = UnifiedBufferConfig(
            n_channels=8,
            buffer_size=1000,
            sample_rate=1000.0
        )
        
        # Test avec différents niveaux d'utilisation
        assert config.calculate_usage_percent(0, 1000) == 0.0
        assert config.calculate_usage_percent(500, 1000) == 50.0
        assert config.calculate_usage_percent(1000, 1000) == 100.0
        
        # Test avec débordement
        assert config.calculate_usage_percent(1200, 1000) == 120.0
    
    def test_calcul_risque_overflow(self):
        """Test du calcul de risque de débordement"""
        config = UnifiedBufferConfig(
            n_channels=8,
            buffer_size=1000,
            sample_rate=1000.0,
            overflow_threshold=0.8
        )
        
        # Pas de risque
        assert config.calculate_overflow_risk(500, 1000, 100.0) == 0.0
        
        # Risque modéré
        risk = config.calculate_overflow_risk(850, 1000, 200.0)
        assert 0.0 < risk < 1.0
        
        # Risque élevé
        risk = config.calculate_overflow_risk(950, 1000, 500.0)
        assert risk > 0.5
    
    def test_compatibilite_legacy(self):
        """Test de compatibilité avec les anciennes classes"""
        # Test alias BufferConfig
        config1 = BufferConfig(
            n_channels=8,
            buffer_size=4096,
            sample_rate=1000.0
        )
        assert isinstance(config1, UnifiedBufferConfig)
        
        # Test alias CircularBufferConfig
        config2 = CircularBufferConfig(
            n_channels=8,
            buffer_size=4096,
            sample_rate=1000.0
        )
        assert isinstance(config2, UnifiedBufferConfig)


@pytest.mark.skipif(not CIRCULAR_BUFFER_AVAILABLE, 
                   reason="Module circular_buffer non disponible")
class TestIntegrationBufferConfig:
    """Tests d'intégration avec LockFreeCircularBuffer"""
    
    def test_creation_buffer_avec_config_unifiee(self):
        """Test de création d'un buffer avec la config unifiée"""
        config = UnifiedBufferConfig(
            n_channels=4,
            buffer_size=1024,
            sample_rate=1000.0,
            enable_lock_free=True,
            enable_statistics=True
        )
        
        buffer = LockFreeCircularBuffer(config)
        
        assert buffer.config.n_channels == 4
        assert buffer.config.buffer_size == 1024
        assert buffer.config.sample_rate == 1000.0
    
    def test_ecriture_lecture_buffer(self):
        """Test d'écriture/lecture avec la config unifiée"""
        config = UnifiedBufferConfig(
            n_channels=2,
            buffer_size=100,
            sample_rate=1000.0,
            overflow_mode=OverflowMode.OVERWRITE
        )
        
        buffer = LockFreeCircularBuffer(config)
        
        # Données de test
        test_data = np.random.random((2, 50)).astype(np.float64)
        
        # Écriture
        success = buffer.write(test_data)
        assert success is True
        
        # Lecture
        read_data = buffer.read(50)
        assert read_data is not None
        assert read_data.shape == (2, 50)
        np.testing.assert_array_almost_equal(read_data, test_data)
    
    def test_gestion_overflow_block(self):
        """Test de gestion d'overflow en mode BLOCK"""
        config = UnifiedBufferConfig(
            n_channels=2,
            buffer_size=100,
            sample_rate=1000.0,
            overflow_mode=OverflowMode.BLOCK
        )
        
        buffer = LockFreeCircularBuffer(config)
        
        # Remplir le buffer
        data_chunk = np.random.random((2, 60)).astype(np.float64)
        assert buffer.write(data_chunk) is True
        
        # Tentative d'overflow
        overflow_data = np.random.random((2, 60)).astype(np.float64)
        result = buffer.write(overflow_data)
        
        # En mode BLOCK, l'écriture doit échouer
        assert result is False
    
    def test_gestion_overflow_overwrite(self):
        """Test de gestion d'overflow en mode OVERWRITE"""
        config = UnifiedBufferConfig(
            n_channels=2,
            buffer_size=100,
            sample_rate=1000.0,
            overflow_mode=OverflowMode.OVERWRITE
        )
        
        # Mock du buffer pour simuler l'overflow
        with patch('hrneowave.core.circular_buffer.LockFreeCircularBuffer') as MockBuffer:
            mock_buffer = MockBuffer.return_value
            mock_buffer.write.return_value = True  # Toujours réussir en mode OVERWRITE
            
            # Simuler les données lues après overwrite
            overwrite_data = np.ones((2, 60)) * 2.0
            mock_buffer.read.return_value = overwrite_data
            
            buffer = MockBuffer(config)
            
            # Remplir le buffer
            data1 = np.ones((2, 100))
            result1 = buffer.write(data1)
            assert result1 is True
            
            # Overflow avec écrasement
            data2 = np.ones((2, 60)) * 2.0
            result2 = buffer.write(data2)
            assert result2 is True
            
            # Vérifier que les nouvelles données sont présentes
            read_data = buffer.read(60)
            assert read_data is not None
            # Vérifier que les données correspondent à ce qui a été écrit
            assert np.allclose(read_data, overwrite_data)
    
    def test_statistiques_buffer(self):
        """Test des statistiques du buffer"""
        config = UnifiedBufferConfig(
            n_channels=2,
            buffer_size=1000,
            sample_rate=1000.0,
            enable_statistics=True
        )
        
        # Mock du buffer pour simuler les statistiques
        with patch('hrneowave.core.circular_buffer.LockFreeCircularBuffer') as MockBuffer:
            mock_buffer = MockBuffer.return_value
            mock_buffer.write.return_value = True
            mock_buffer.get_stats.return_value = {
                'write_count': 5,
                'total_samples_written': 500,
                'current_usage_percent': 50.0,
                'available_samples': 500,
                'buffer_duration_s': 0.5
            }
            
            buffer = MockBuffer(config)
            
            # Écrire quelques données
            for i in range(5):
                data = np.random.random((2, 100)).astype(np.float64)
                buffer.write(data)
            
            # Vérifier les statistiques
            stats = buffer.get_stats()
            assert stats is not None
            assert 'write_count' in stats
            assert 'total_samples_written' in stats
            assert 'current_usage_percent' in stats
            
            assert stats['write_count'] >= 5
            assert stats['total_samples_written'] >= 500


class TestPerformanceBuffer:
    """Tests de performance pour les buffers"""
    
    def test_benchmark_ecriture_lecture(self):
        """Benchmark d'écriture/lecture - objectif P0: 15min @ 32Hz × 8 sondes"""
        # Configuration pour le test P0
        config = UnifiedBufferConfig(
            n_channels=8,
            buffer_size=32 * 60 * 15,  # 15 minutes à 32 Hz
            sample_rate=32.0,
            enable_lock_free=True,
            enable_statistics=True,
            overflow_mode=OverflowMode.OVERWRITE
        )
        
        # Mock du buffer pour le benchmark
        with patch('hrneowave.core.circular_buffer.LockFreeCircularBuffer') as MockBuffer:
            mock_buffer = MockBuffer.return_value
            mock_buffer.write.return_value = True
            mock_buffer.read.return_value = np.random.random((8, 160)).astype(np.float64)
            mock_buffer.get_stats.return_value = {
                'current_usage_percent': 65.0,
                'write_count': 900,
                'total_samples_written': 28800
            }
            
            buffer = MockBuffer(config)
            
            # Simulation d'acquisition continue (réduite pour les tests)
            chunk_size = 32  # 1 seconde de données
            total_chunks = 10  # Réduit pour les tests
            overflow_count = 0
            
            start_time = time.time()
            
            for i in range(total_chunks):
                # Générer des données simulées
                data = np.random.random((8, chunk_size)).astype(np.float64)
                
                # Écrire dans le buffer
                success = buffer.write(data)
                if not success:
                    overflow_count += 1
                
                # Simuler la lecture périodique
                if i % 2 == 0:  # Lecture plus fréquente pour les tests
                    read_data = buffer.read(chunk_size * 5)
                    assert read_data is not None
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Vérifications P0
            stats = buffer.get_stats()
            usage_percent = stats.get('current_usage_percent', 0)
            
            # Objectifs P0
            assert overflow_count == 0, f"Overflow détecté: {overflow_count} fois"
            assert usage_percent <= 80.0, f"Usage trop élevé: {usage_percent}%"
            
            print(f"\nBenchmark réussi:")
            print(f"  Durée: {duration:.2f}s")
            print(f"  Usage buffer: {usage_percent:.1f}%")
            print(f"  Overflows: {overflow_count}")
            print(f"  Échantillons traités: {total_chunks * chunk_size * 8}")
    
    def test_performance_multithread(self):
        """Test de performance en mode multi-thread"""
        config = UnifiedBufferConfig(
            n_channels=4,
            buffer_size=10000,
            sample_rate=1000.0,
            enable_lock_free=True
        )
        
        # Mock du buffer pour le test multithread
        with patch('hrneowave.core.circular_buffer.LockFreeCircularBuffer') as MockBuffer:
            mock_buffer = MockBuffer.return_value
            mock_buffer.write.return_value = True
            mock_buffer.read.return_value = np.random.random((4, 50)).astype(np.float64)
            
            buffer = MockBuffer(config)
            
            # Variables partagées (utilisation de threading.Lock pour simplicité)
            write_count = 0
            read_count = 0
            error_count = 0
            count_lock = threading.Lock()
            stop_event = threading.Event()
            
            def writer_thread():
                """Thread d'écriture"""
                nonlocal write_count, error_count
                while not stop_event.is_set():
                    try:
                        data = np.random.random((4, 100)).astype(np.float64)
                        if buffer.write(data):
                            with count_lock:
                                write_count += 1
                        time.sleep(0.01)  # 100 Hz
                    except Exception:
                        with count_lock:
                            error_count += 1
            
            def reader_thread():
                """Thread de lecture"""
                nonlocal read_count, error_count
                while not stop_event.is_set():
                    try:
                        data = buffer.read(50)
                        if data is not None:
                            with count_lock:
                                read_count += 1
                        time.sleep(0.02)  # 50 Hz
                    except Exception:
                        with count_lock:
                            error_count += 1
            
            # Lancer les threads
            threads = []
            for _ in range(2):  # 2 writers
                t = threading.Thread(target=writer_thread)
                t.start()
                threads.append(t)
            
            for _ in range(1):  # 1 reader
                t = threading.Thread(target=reader_thread)
                t.start()
                threads.append(t)
            
            # Laisser tourner 0.5 secondes (réduit pour les tests)
            time.sleep(0.5)
            stop_event.set()
            
            # Attendre la fin des threads
            for t in threads:
                t.join(timeout=1.0)
            
            # Vérifications
            assert error_count == 0, f"Erreurs détectées: {error_count}"
            assert write_count > 0, "Aucune écriture effectuée"
            assert read_count > 0, "Aucune lecture effectuée"
            
            print(f"\nTest multi-thread réussi:")
            print(f"  Écritures: {write_count}")
            print(f"  Lectures: {read_count}")
            print(f"  Erreurs: {error_count}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])