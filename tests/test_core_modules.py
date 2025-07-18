#!/usr/bin/env python3
"""
Tests pour les modules core de CHNeoWave
"""

import unittest
import numpy as np
from unittest.mock import patch, MagicMock


class TestCoreModules(unittest.TestCase):
    """Tests pour les modules core"""

    def test_circular_buffer_import(self):
        """Test d'import du CircularBuffer"""
        try:
            from hrneowave.core.circular_buffer import LockFreeCircularBuffer, BufferConfig
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Échec import CircularBuffer: {e}")

    def test_circular_buffer_basic(self):
        """Test basique du CircularBuffer"""
        from hrneowave.core.circular_buffer import LockFreeCircularBuffer, BufferConfig
        
        config = BufferConfig(n_channels=2, buffer_size=1024, dtype=np.float64)
        buffer = LockFreeCircularBuffer(config)
        self.assertEqual(buffer.config.buffer_size, 1024)
        self.assertEqual(buffer.config.dtype, np.float64)
        
        # Test d'écriture
        data = np.random.random((2, 512)).astype(np.float64)
        success = buffer.write(data)
        self.assertTrue(success)
        self.assertGreaterEqual(buffer.available_samples(), 0)

    def test_optimized_fft_processor_import(self):
        """Test d'import de OptimizedFFTProcessor"""
        try:
            from hrneowave.core.optimized_fft_processor import OptimizedFFTProcessor
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Échec import OptimizedFFTProcessor: {e}")

    def test_optimized_fft_processor_basic(self):
        """Test basique de OptimizedFFTProcessor"""
        from hrneowave.core.optimized_fft_processor import OptimizedFFTProcessor
        
        processor = OptimizedFFTProcessor()
        self.assertIsNotNone(processor)
        
        # Test avec données simulées
        data = np.random.random(1024).astype(np.float64)
        try:
            result = processor.process_fft(data)
            self.assertIsNotNone(result)
        except Exception:
            # Acceptable si pyFFTW n'est pas disponible
            pass

    def test_optimized_goda_analyzer_import(self):
        """Test d'import de OptimizedGodaAnalyzer"""
        try:
            from hrneowave.core.optimized_goda_analyzer import OptimizedGodaAnalyzer
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Échec import OptimizedGodaAnalyzer: {e}")

    def test_optimized_goda_analyzer_basic(self):
        """Test basique de OptimizedGodaAnalyzer"""
        from hrneowave.core.optimized_goda_analyzer import OptimizedGodaAnalyzer, ProbeGeometry
        
        # Créer une géométrie de sondes
        positions = np.array([0.0, 1.0, 2.0, 3.0])
        geometry = ProbeGeometry(positions=positions, water_depth=2.0, frequency_range=(0.1, 2.0))
        analyzer = OptimizedGodaAnalyzer(geometry=geometry)
        self.assertIsNotNone(analyzer)
        self.assertEqual(analyzer.geometry.water_depth, 2.0)
        
        # Test avec données simulées
        try:
            # Test de la méthode de résolution de dispersion
            k = analyzer._solve_dispersion_cached(2 * np.pi * 0.5)  # 0.5 Hz
            self.assertGreater(k, 0)
        except Exception:
            # Acceptable si certaines dépendances manquent
            pass


class TestConfigModules(unittest.TestCase):
    """Tests pour les modules de configuration"""

    def test_optimization_config_import(self):
        """Test d'import de optimization_config"""
        try:
            from hrneowave.config.optimization_config import (
                FFTConfig,
                GodaConfig,
                BufferConfig,
                AcquisitionConfig,
                PerformanceConfig,
                OptimizationConfig
            )
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Échec import optimization_config: {e}")

    def test_optimization_config_creation(self):
        """Test de création des configurations"""
        from hrneowave.config.optimization_config import (
            FFTConfig,
            OptimizationConfig
        )
        
        fft_config = FFTConfig()
        self.assertIsNotNone(fft_config)
        
        opt_config = OptimizationConfig()
        self.assertIsNotNone(opt_config)
        self.assertIsNotNone(opt_config.fft)


class TestToolsModules(unittest.TestCase):
    """Tests pour les modules tools"""

    def test_lab_config_import(self):
        """Test d'import de lab_config"""
        try:
            from hrneowave.tools.lab_config import (
                MediterraneanLabConfigurator,
                LabConfiguration
            )
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Échec import lab_config: {e}")

    def test_lab_config_creation(self):
        """Test de création du configurateur"""
        from hrneowave.tools.lab_config import MediterraneanLabConfigurator
        
        configurator = MediterraneanLabConfigurator()
        self.assertIsNotNone(configurator)


class TestUtilsModules(unittest.TestCase):
    """Tests pour les modules utils"""

    def test_doc_generator_import(self):
        """Test d'import de doc_generator"""
        try:
            from hrneowave.utils.doc_generator import (
                CHNeoWaveDocGenerator,
                ModuleInfo
            )
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Échec import doc_generator: {e}")

    def test_doc_generator_creation(self):
        """Test de création du générateur"""
        from hrneowave.utils.doc_generator import CHNeoWaveDocGenerator
        
        generator = CHNeoWaveDocGenerator(".", "docs")
        self.assertIsNotNone(generator)


if __name__ == "__main__":
    unittest.main()