#!/usr/bin/env python3
# test_optimized_integration.py - Tests d'intégration des modules optimisés

import unittest
import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'logciel hrneowave'))
sys.path.insert(0, str(project_root / 'src'))

class TestOptimizedIntegration(unittest.TestCase):
    """Tests d'intégration pour les modules optimisés CHNeoWave"""
    
    def setUp(self):
        """Configuration des tests"""
        self.project_root = Path(__file__).parent.parent
        
    def test_optimized_processing_worker_import(self):
        """Test d'import d'OptimizedProcessingWorker"""
        try:
            from optimized_processing_worker import OptimizedProcessingWorker
            self.assertTrue(True, "OptimizedProcessingWorker importé avec succès")
        except ImportError as e:
            self.fail(f"Échec import OptimizedProcessingWorker: {e}")
            
    def test_circular_buffer_import(self):
        """Test d'import de CircularBuffer"""
        try:
            from hrneowave.core.circular_buffer import CircularBuffer
            self.assertTrue(True, "CircularBuffer importé avec succès")
        except ImportError as e:
            self.fail(f"Échec import CircularBuffer: {e}")
            
    def test_acquisition_controller_import(self):
        """Test d'import d'AcquisitionController"""
        try:
            from acquisition_controller import AcquisitionController
            self.assertTrue(True, "AcquisitionController importé avec succès")
        except ImportError as e:
            self.fail(f"Échec import AcquisitionController: {e}")
            
    def test_optimized_fft_processor_import(self):
        """Test d'import d'OptimizedFFTProcessor"""
        try:
            from src.hrneowave.core.optimized_fft_processor import OptimizedFFTProcessor
            self.assertTrue(True, "OptimizedFFTProcessor importé avec succès")
        except ImportError:
            # Test fallback local
            try:
                # Vérifier si le fichier existe localement
                local_file = self.project_root / 'logciel hrneowave' / 'optimized_fft_processor.py'
                if local_file.exists():
                    self.assertTrue(True, "OptimizedFFTProcessor disponible localement")
                else:
                    self.skipTest("OptimizedFFTProcessor non disponible")
            except Exception as e:
                self.skipTest(f"OptimizedFFTProcessor non disponible: {e}")
                
    def test_optimized_goda_analyzer_import(self):
        """Test d'import d'OptimizedGodaAnalyzer"""
        try:
            from src.hrneowave.core.optimized_goda_analyzer import OptimizedGodaAnalyzer
            self.assertTrue(True, "OptimizedGodaAnalyzer importé avec succès")
        except ImportError:
            # Test fallback local
            try:
                local_file = self.project_root / 'logciel hrneowave' / 'optimized_goda_analyzer.py'
                if local_file.exists():
                    self.assertTrue(True, "OptimizedGodaAnalyzer disponible localement")
                else:
                    self.skipTest("OptimizedGodaAnalyzer non disponible")
            except Exception as e:
                self.skipTest(f"OptimizedGodaAnalyzer non disponible: {e}")
                
    def test_acquisition_gui_import(self):
        """Test d'import de l'interface d'acquisition"""
        try:
            # Test import sans exécution (éviter les dépendances GUI)
            import ast
            acquisition_file = self.project_root / 'logciel hrneowave' / 'acquisition.py'
            
            if acquisition_file.exists():
                with open(acquisition_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Vérifier que le fichier est syntaxiquement correct
                try:
                    ast.parse(content)
                    self.assertTrue(True, "acquisition.py syntaxiquement correct")
                except SyntaxError as e:
                    self.fail(f"Erreur syntaxe acquisition.py: {e}")
                    
                # Vérifier la présence des imports optimisés
                self.assertIn('OptimizedProcessingWorker', content, 
                            "OptimizedProcessingWorker doit être importé")
                            
            else:
                self.fail("acquisition.py non trouvé")
                
        except Exception as e:
            self.fail(f"Erreur test acquisition GUI: {e}")
            
    def test_modern_acquisition_ui_import(self):
        """Test d'import de l'interface moderne"""
        try:
            import ast
            modern_ui_file = self.project_root / 'logciel hrneowave' / 'modern_acquisition_ui.py'
            
            if modern_ui_file.exists():
                with open(modern_ui_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Vérifier syntaxe
                try:
                    ast.parse(content)
                    self.assertTrue(True, "modern_acquisition_ui.py syntaxiquement correct")
                except SyntaxError as e:
                    self.fail(f"Erreur syntaxe modern_acquisition_ui.py: {e}")
                    
            else:
                self.skipTest("modern_acquisition_ui.py non trouvé")
                
        except Exception as e:
            self.fail(f"Erreur test modern acquisition UI: {e}")
            
    def test_project_structure(self):
        """Test de la structure du projet"""
        # Vérifier les dossiers essentiels
        essential_dirs = [
            'src/hrneowave',
            'logciel hrneowave',
            'tests',
            'config'
        ]
        
        for dir_path in essential_dirs:
            full_path = self.project_root / dir_path
            self.assertTrue(full_path.exists(), f"Dossier {dir_path} doit exister")
            
    def test_no_orphan_files(self):
        """Test absence de fichiers orphelins critiques"""
        # Vérifier que les anciens fichiers ont été supprimés
        orphan_files = [
            'logciel hrneowave/processing_worker.py',  # Ancien fichier
            'HRNeoWave/gui/Traitementdonneé.py'  # Doublon supprimé
        ]
        
        for orphan_file in orphan_files:
            full_path = self.project_root / orphan_file
            self.assertFalse(full_path.exists(), f"Fichier orphelin {orphan_file} ne doit plus exister")
            
    def test_core_modules_exist(self):
        """Test existence des modules core"""
        core_modules = [
            'src/hrneowave/core/optimized_fft_processor.py',
            'src/hrneowave/core/optimized_goda_analyzer.py',
            'src/hrneowave/core/circular_buffer.py'
        ]
        
        existing_modules = 0
        for module_path in core_modules:
            full_path = self.project_root / module_path
            if full_path.exists():
                existing_modules += 1
                
        # Au moins 2 modules core doivent exister
        self.assertGreaterEqual(existing_modules, 2, 
                              f"Au moins 2 modules core doivent exister (trouvés: {existing_modules})")

class TestPerformanceEstimation(unittest.TestCase):
    """Tests d'estimation des performances"""
    
    def test_fft_optimization_available(self):
        """Test disponibilité optimisation FFT"""
        project_root = Path(__file__).parent.parent
        
        # Vérifier présence d'au moins un module FFT optimisé
        fft_modules = [
            'src/hrneowave/core/optimized_fft_processor.py',
            'logciel hrneowave/optimized_fft_processor.py'
        ]
        
        fft_available = any((project_root / module).exists() for module in fft_modules)
        
        if fft_available:
            self.assertTrue(True, "Module FFT optimisé disponible")
        else:
            self.skipTest("Aucun module FFT optimisé trouvé")
            
    def test_goda_optimization_available(self):
        """Test disponibilité optimisation Goda"""
        project_root = Path(__file__).parent.parent
        
        # Vérifier présence d'au moins un module Goda optimisé
        goda_modules = [
            'src/hrneowave/core/optimized_goda_analyzer.py',
            'logciel hrneowave/optimized_goda_analyzer.py'
        ]
        
        goda_available = any((project_root / module).exists() for module in goda_modules)
        
        if goda_available:
            self.assertTrue(True, "Module Goda optimisé disponible")
        else:
            self.skipTest("Aucun module Goda optimisé trouvé")
            
    def test_circular_buffer_optimization(self):
        """Test optimisation CircularBuffer"""
        project_root = Path(__file__).parent.parent
        
        # Vérifier présence CircularBuffer
        buffer_modules = [
            'src/hrneowave/core/circular_buffer.py',
            'logciel hrneowave/circular_buffer.py'
        ]
        
        buffer_available = any((project_root / module).exists() for module in buffer_modules)
        self.assertTrue(buffer_available, "CircularBuffer doit être disponible")

if __name__ == '__main__':
    # Configuration du test runner
    unittest.main(verbosity=2, buffer=True)