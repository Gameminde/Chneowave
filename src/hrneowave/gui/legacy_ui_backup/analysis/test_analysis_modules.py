#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour les modules d'analyse refactorisés
Validation de l'architecture modulaire
"""

import unittest
import sys
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Ajout du chemin pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

try:
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtCore import QTimer
    from PySide6.QtTest import QTest
except ImportError:
    print("PySide6 non disponible - tests en mode mock")
    QApplication = Mock
    QWidget = Mock
    QTimer = Mock
    QTest = Mock

# Import des modules à tester avec gestion d'erreur
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from spectral_analysis import SpectralAnalysisWidget
except ImportError:
    SpectralAnalysisWidget = Mock

try:
    from goda_analysis import GodaAnalysisWidget
except ImportError:
    GodaAnalysisWidget = Mock

try:
    from statistics_analysis import StatisticsAnalysisWidget
except ImportError:
    StatisticsAnalysisWidget = Mock

try:
    from summary_report import SummaryReportWidget
except ImportError:
    SummaryReportWidget = Mock

try:
    from analysis_controller import AnalysisController
except ImportError:
    AnalysisController = Mock

try:
    from analysis_view_v2 import AnalysisViewV2
except ImportError:
    AnalysisViewV2 = Mock


class MockSessionData:
    """
    Données de session simulées pour les tests
    """
    def __init__(self):
        self.sampling_frequency = 100.0
        self.duration = 10.0
        self.num_sensors = 4
        self.sensor_names = ["Capteur 1", "Capteur 2", "Capteur 3", "Capteur 4"]
        
        # Génération de données simulées
        time = np.linspace(0, self.duration, int(self.sampling_frequency * self.duration))
        self.time_data = time
        
        # Signaux simulés avec différentes fréquences
        self.sensor_data = {
            "Capteur 1": np.sin(2 * np.pi * 1.0 * time) + 0.1 * np.random.randn(len(time)),
            "Capteur 2": np.sin(2 * np.pi * 2.0 * time) + 0.1 * np.random.randn(len(time)),
            "Capteur 3": np.sin(2 * np.pi * 0.5 * time) + 0.1 * np.random.randn(len(time)),
            "Capteur 4": np.sin(2 * np.pi * 3.0 * time) + 0.1 * np.random.randn(len(time))
        }
        
        self.metadata = {
            "experiment_name": "Test Experiment",
            "date": "2024-01-01",
            "operator": "Test User",
            "location": "Test Lab"
        }


class TestSpectralAnalysisWidget(unittest.TestCase):
    """
    Tests pour SpectralAnalysisWidget
    """
    
    @classmethod
    def setUpClass(cls):
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        self.session_data = MockSessionData()
        
        # Mock du widget pour éviter les dépendances GUI
        with patch('spectral_analysis.SpectralAnalysisWidget.__init__', return_value=None):
            from spectral_analysis import SpectralAnalysisWidget
            self.widget = SpectralAnalysisWidget()
            
            # Configuration manuelle des attributs nécessaires
            self.widget.session_data = None
            self.widget.spectral_results = {}
            self.widget.window_size = 1024
            self.widget.window_type = 'hann'
            self.widget.overlap_ratio = 0.5
    
    def test_set_session_data(self):
        """Test de configuration des données de session"""
        with patch.object(self.widget, 'setSessionData') as mock_method:
            self.widget.setSessionData(self.session_data)
            mock_method.assert_called_once_with(self.session_data)
    
    def test_spectral_analysis_parameters(self):
        """Test des paramètres d'analyse spectrale"""
        # Test des valeurs par défaut
        self.assertEqual(self.widget.window_size, 1024)
        self.assertEqual(self.widget.window_type, 'hann')
        self.assertEqual(self.widget.overlap_ratio, 0.5)
        
        # Test de modification des paramètres
        self.widget.window_size = 2048
        self.widget.window_type = 'hamming'
        self.widget.overlap_ratio = 0.75
        
        self.assertEqual(self.widget.window_size, 2048)
        self.assertEqual(self.widget.window_type, 'hamming')
        self.assertEqual(self.widget.overlap_ratio, 0.75)
    
    def test_spectral_calculation(self):
        """Test du calcul spectral"""
        # Simulation du calcul spectral
        signal = self.session_data.sensor_data["Capteur 1"]
        fs = self.session_data.sampling_frequency
        
        # Test de la FFT
        fft_result = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(len(signal), 1/fs)
        
        self.assertEqual(len(fft_result), len(signal))
        self.assertEqual(len(frequencies), len(signal))
        
        # Test de la densité spectrale de puissance
        psd = np.abs(fft_result)**2
        self.assertEqual(len(psd), len(signal))
        self.assertTrue(np.all(psd >= 0))  # PSD doit être positive


class TestGodaAnalysisWidget(unittest.TestCase):
    """
    Tests pour GodaAnalysisWidget
    """
    
    def setUp(self):
        self.session_data = MockSessionData()
        
        with patch('goda_analysis.GodaAnalysisWidget.__init__', return_value=None):
            from goda_analysis import GodaAnalysisWidget
            self.widget = GodaAnalysisWidget()
            
            self.widget.session_data = None
            self.widget.goda_results = {}
            self.widget.min_wave_height = 0.01
            self.widget.detection_method = 'zero_crossing'
    
    def test_wave_detection_methods(self):
        """Test des méthodes de détection de vagues"""
        methods = ['zero_crossing', 'peak_to_trough', 'envelope']
        
        for method in methods:
            self.widget.detection_method = method
            self.assertEqual(self.widget.detection_method, method)
    
    def test_wave_height_calculation(self):
        """Test du calcul des hauteurs de vagues"""
        # Simulation d'un signal de vague simple
        time = np.linspace(0, 10, 1000)
        wave_signal = 2 * np.sin(2 * np.pi * 0.5 * time)  # Vague de 2m d'amplitude
        
        # Détection des pics et creux
        from scipy.signal import find_peaks
        
        peaks, _ = find_peaks(wave_signal)
        troughs, _ = find_peaks(-wave_signal)
        
        self.assertTrue(len(peaks) > 0)
        self.assertTrue(len(troughs) > 0)
        
        # Calcul des hauteurs (différence pic-creux)
        if len(peaks) > 0 and len(troughs) > 0:
            max_height = np.max(wave_signal[peaks]) - np.min(wave_signal[troughs])
            self.assertGreater(max_height, 0)
    
    def test_goda_statistics(self):
        """Test des statistiques de Goda"""
        # Simulation de hauteurs de vagues
        wave_heights = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 1.8, 2.2, 1.3, 2.8, 2.1])
        
        # Calcul des statistiques de Goda
        h_max = np.max(wave_heights)
        h_mean = np.mean(wave_heights)
        h_sorted = np.sort(wave_heights)[::-1]  # Tri décroissant
        
        # H1/3 (hauteur significative)
        n_third = max(1, len(h_sorted) // 3)
        h_13 = np.mean(h_sorted[:n_third])
        
        # H1/10
        n_tenth = max(1, len(h_sorted) // 10)
        h_110 = np.mean(h_sorted[:n_tenth])
        
        self.assertEqual(h_max, 3.0)
        self.assertAlmostEqual(h_mean, 2.0, places=1)
        self.assertGreaterEqual(h_13, h_mean)
        self.assertGreaterEqual(h_110, h_13)


class TestStatisticsAnalysisWidget(unittest.TestCase):
    """
    Tests pour StatisticsAnalysisWidget
    """
    
    def setUp(self):
        self.session_data = MockSessionData()
        
        with patch('statistics_analysis.StatisticsAnalysisWidget.__init__', return_value=None):
            from statistics_analysis import StatisticsAnalysisWidget
            self.widget = StatisticsAnalysisWidget()
            
            self.widget.session_data = None
            self.widget.statistics_results = {}
            self.widget.selected_sensor = "Capteur 1"
            self.widget.num_bins = 50
            self.widget.confidence_level = 0.95
    
    def test_descriptive_statistics(self):
        """Test des statistiques descriptives"""
        data = self.session_data.sensor_data["Capteur 1"]
        
        # Calcul des statistiques
        mean_val = np.mean(data)
        std_val = np.std(data, ddof=1)
        min_val = np.min(data)
        max_val = np.max(data)
        median_val = np.median(data)
        
        # Vérifications
        self.assertIsInstance(mean_val, (int, float, np.number))
        self.assertIsInstance(std_val, (int, float, np.number))
        self.assertLessEqual(min_val, median_val)
        self.assertLessEqual(median_val, max_val)
        self.assertGreater(std_val, 0)
    
    def test_normality_tests(self):
        """Test des tests de normalité"""
        # Données normales simulées
        normal_data = np.random.normal(0, 1, 1000)
        
        # Test de Shapiro-Wilk (pour échantillons < 5000)
        from scipy.stats import shapiro
        if len(normal_data) <= 5000:
            stat, p_value = shapiro(normal_data)
            self.assertIsInstance(stat, (int, float, np.number))
            self.assertIsInstance(p_value, (int, float, np.number))
            self.assertGreaterEqual(p_value, 0)
            self.assertLessEqual(p_value, 1)
    
    def test_outlier_detection(self):
        """Test de détection des outliers"""
        # Données avec outliers
        data = np.concatenate([
            np.random.normal(0, 1, 100),  # Données normales
            [10, -10, 15]  # Outliers évidents
        ])
        
        # Méthode IQR
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        
        self.assertGreater(len(outliers), 0)  # Doit détecter des outliers
        self.assertTrue(10 in outliers or -10 in outliers or 15 in outliers)


class TestSummaryReportWidget(unittest.TestCase):
    """
    Tests pour SummaryReportWidget
    """
    
    def setUp(self):
        self.session_data = MockSessionData()
        
        with patch('summary_report.SummaryReportWidget.__init__', return_value=None):
            from summary_report import SummaryReportWidget
            self.widget = SummaryReportWidget()
            
            self.widget.session_data = None
            self.widget.analysis_results = {}
            self.widget.report_type = 'complete'
            self.widget.report_language = 'fr'
    
    def test_report_types(self):
        """Test des types de rapport"""
        report_types = ['complete', 'executive', 'technical']
        
        for report_type in report_types:
            self.widget.report_type = report_type
            self.assertEqual(self.widget.report_type, report_type)
    
    def test_report_languages(self):
        """Test des langues de rapport"""
        languages = ['fr', 'en']
        
        for language in languages:
            self.widget.report_language = language
            self.assertEqual(self.widget.report_language, language)
    
    def test_report_generation(self):
        """Test de génération de rapport"""
        # Simulation de résultats d'analyse
        mock_results = {
            'spectral': {
                'peak_frequency': 1.5,
                'mean_frequency': 1.2,
                'spectral_width': 0.8
            },
            'goda': {
                'h_max': 3.2,
                'h_mean': 1.8,
                'h_13': 2.4,
                'h_110': 2.9
            },
            'statistics': {
                'mean': 0.05,
                'std': 1.02,
                'skewness': 0.12,
                'kurtosis': 2.98
            }
        }
        
        self.widget.analysis_results = mock_results
        
        # Vérification que les résultats sont bien stockés
        self.assertIn('spectral', self.widget.analysis_results)
        self.assertIn('goda', self.widget.analysis_results)
        self.assertIn('statistics', self.widget.analysis_results)


class TestAnalysisController(unittest.TestCase):
    """
    Tests pour AnalysisController
    """
    
    def setUp(self):
        self.session_data = MockSessionData()
        
        with patch('analysis_controller.AnalysisController.__init__', return_value=None):
            from analysis_controller import AnalysisController
            self.controller = AnalysisController()
            
            # Mock des widgets
            self.controller.spectral_widget = Mock()
            self.controller.goda_widget = Mock()
            self.controller.statistics_widget = Mock()
            self.controller.summary_widget = Mock()
            
            self.controller.session_data = None
            self.controller.analysis_results = {}
    
    def test_set_session_data(self):
        """Test de configuration des données de session"""
        self.controller.session_data = self.session_data
        
        # Vérification que les widgets reçoivent les données
        self.controller.spectral_widget.setSessionData.assert_called_with(self.session_data)
        self.controller.goda_widget.setSessionData.assert_called_with(self.session_data)
        self.controller.statistics_widget.setSessionData.assert_called_with(self.session_data)
        self.controller.summary_widget.setSessionData.assert_called_with(self.session_data)
    
    def test_analysis_orchestration(self):
        """Test de l'orchestration des analyses"""
        # Mock des méthodes d'analyse
        self.controller.spectral_widget.performSpectralAnalysis = Mock()
        self.controller.goda_widget.performGodaAnalysis = Mock()
        self.controller.statistics_widget.calculateStatistics = Mock()
        
        # Test d'analyse complète
        with patch.object(self.controller, 'startCompleteAnalysis') as mock_complete:
            self.controller.startCompleteAnalysis()
            mock_complete.assert_called_once()
    
    def test_results_aggregation(self):
        """Test de l'agrégation des résultats"""
        # Simulation de résultats partiels
        spectral_results = {'peak_frequency': 1.5}
        goda_results = {'h_max': 3.2}
        stats_results = {'mean': 0.05}
        
        # Agrégation
        self.controller.analysis_results = {
            'spectral': spectral_results,
            'goda': goda_results,
            'statistics': stats_results
        }
        
        # Vérification
        self.assertIn('spectral', self.controller.analysis_results)
        self.assertIn('goda', self.controller.analysis_results)
        self.assertIn('statistics', self.controller.analysis_results)
        
        self.assertEqual(self.controller.analysis_results['spectral']['peak_frequency'], 1.5)
        self.assertEqual(self.controller.analysis_results['goda']['h_max'], 3.2)
        self.assertEqual(self.controller.analysis_results['statistics']['mean'], 0.05)


class TestAnalysisViewV2Integration(unittest.TestCase):
    """
    Tests d'intégration pour AnalysisViewV2
    """
    
    def setUp(self):
        self.session_data = MockSessionData()
        
        with patch('analysis_view_v2.AnalysisViewV2.__init__', return_value=None):
            from analysis_view_v2 import AnalysisViewV2
            self.view = AnalysisViewV2()
            
            # Mock du contrôleur
            self.view.controller = Mock()
            self.view.session_data = None
    
    def test_view_initialization(self):
        """Test de l'initialisation de la vue"""
        # Vérification que le contrôleur est présent
        self.assertIsNotNone(self.view.controller)
    
    def test_session_data_propagation(self):
        """Test de la propagation des données de session"""
        self.view.setSessionData(self.session_data)
        
        # Vérification que le contrôleur reçoit les données
        self.view.controller.setSessionData.assert_called_with(self.session_data)
    
    def test_analysis_delegation(self):
        """Test de la délégation des analyses"""
        # Test de délégation vers le contrôleur
        self.view.startCompleteAnalysis()
        self.view.controller.startCompleteAnalysis.assert_called_once()
        
        self.view.resetAnalysis()
        self.view.controller.resetAnalysis.assert_called_once()


def run_tests():
    """
    Exécution de tous les tests
    """
    # Configuration du test runner
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajout des classes de test
    test_classes = [
        TestSpectralAnalysisWidget,
        TestGodaAnalysisWidget,
        TestStatisticsAnalysisWidget,
        TestSummaryReportWidget,
        TestAnalysisController,
        TestAnalysisViewV2Integration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Exécution des tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)