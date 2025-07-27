# -*- coding: utf-8 -*-
"""
Widget d'analyse statistique CHNeoWave
Extrait de analysis_view.py pour une meilleure modularité
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox, QSplitter,
    QFormLayout, QSpinBox, QComboBox, QCheckBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

import numpy as np
from scipy import stats
from ...components.matplotlib_adapter import pg


class StatisticsAnalysisWidget(QWidget):
    """
    Widget spécialisé pour l'analyse statistique
    Responsabilité unique : calculs statistiques et tests de normalité
    """
    
    analysisCompleted = Signal(dict)  # Signal émis quand l'analyse est terminée
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session_data = None
        self.analysis_results = {}
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur pour l'analyse statistique
        """
        layout = QVBoxLayout(self)
        
        # Splitter horizontal
        splitter = QSplitter(Qt.Horizontal)
        
        # Zone des graphiques
        graphs_widget = self._createGraphsWidget()
        splitter.addWidget(graphs_widget)
        
        # Zone de contrôle et résultats
        control_widget = self._createControlWidget()
        control_widget.setMaximumWidth(350)
        splitter.addWidget(control_widget)
        
        layout.addWidget(splitter)
    
    def _createGraphsWidget(self):
        """
        Création de la zone des graphiques
        """
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        
        # Histogramme des amplitudes
        self.histogram_plot = pg.PlotWidget()
        self.histogram_plot.setLabel('left', 'Fréquence')
        self.histogram_plot.setLabel('bottom', 'Amplitude (mm)')
        self.histogram_plot.setTitle('Histogramme des Amplitudes')
        graphs_layout.addWidget(self.histogram_plot)
        
        # Q-Q plot pour test de normalité
        self.qq_plot = pg.PlotWidget()
        self.qq_plot.setLabel('left', 'Quantiles Observés')
        self.qq_plot.setLabel('bottom', 'Quantiles Théoriques')
        self.qq_plot.setTitle('Q-Q Plot (Test de Normalité)')
        graphs_layout.addWidget(self.qq_plot)
        
        return graphs_widget
    
    def _createControlWidget(self):
        """
        Création de la zone de contrôle et résultats
        """
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Paramètres d'analyse
        params_group = QGroupBox("Paramètres Statistiques")
        params_layout = QFormLayout(params_group)
        
        self.sensor_combo = QComboBox()
        params_layout.addRow("Capteur à analyser:", self.sensor_combo)
        
        self.bins_spin = QSpinBox()
        self.bins_spin.setRange(10, 100)
        self.bins_spin.setValue(30)
        params_layout.addRow("Nombre de bins:", self.bins_spin)
        
        self.confidence_spin = QSpinBox()
        self.confidence_spin.setRange(90, 99)
        self.confidence_spin.setValue(95)
        self.confidence_spin.setSuffix("%")
        params_layout.addRow("Niveau de confiance:", self.confidence_spin)
        
        self.outliers_check = QCheckBox("Détecter les outliers")
        self.outliers_check.setChecked(True)
        params_layout.addRow(self.outliers_check)
        
        control_layout.addWidget(params_group)
        
        # Bouton de calcul
        self.calculate_stats_btn = QPushButton("Calculer Statistiques")
        control_layout.addWidget(self.calculate_stats_btn)
        
        # Tableau des statistiques descriptives
        stats_group = QGroupBox("Statistiques Descriptives")
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Paramètre", "Valeur"])
        self.stats_table.setMaximumHeight(200)
        stats_layout.addWidget(self.stats_table)
        
        control_layout.addWidget(stats_group)
        
        # Zone des tests statistiques
        tests_group = QGroupBox("Tests Statistiques")
        tests_layout = QVBoxLayout(tests_group)
        
        self.statistical_tests_text = QTextEdit()
        self.statistical_tests_text.setMaximumHeight(150)
        self.statistical_tests_text.setReadOnly(True)
        tests_layout.addWidget(self.statistical_tests_text)
        
        control_layout.addWidget(tests_group)
        control_layout.addStretch()
        
        return control_widget
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.calculate_stats_btn.clicked.connect(self.calculateStatistics)
        self.sensor_combo.currentIndexChanged.connect(self.onSensorChanged)
    
    def setSessionData(self, session_data):
        """
        Configuration des données de session
        """
        self.session_data = session_data
        self.updateSensorList()
        self.updateDataInfo()
    
    def updateSensorList(self):
        """
        Mise à jour de la liste des capteurs
        """
        self.sensor_combo.clear()
        if self.session_data and self.session_data.get('sensor_data'):
            sensor_data = self.session_data['sensor_data']
            for i in range(len(sensor_data)):
                self.sensor_combo.addItem(f"Capteur {i+1}")
    
    def updateDataInfo(self):
        """
        Mise à jour des informations sur les données
        """
        if not self.session_data:
            return
        
        sensor_data = self.session_data.get('sensor_data', [])
        
        info_text = f"""Données disponibles pour l'analyse statistique:

Nombre de capteurs: {len(sensor_data)}
Nombre d'échantillons: {len(sensor_data[0]) if sensor_data else 0}

Analyses disponibles:
- Statistiques descriptives
- Tests de normalité (Shapiro-Wilk)
- Détection d'outliers
- Distribution des amplitudes

Sélectionnez un capteur et cliquez sur 'Calculer Statistiques'."""
        
        self.statistical_tests_text.setPlainText(info_text)
    
    def onSensorChanged(self):
        """
        Gestion du changement de capteur sélectionné
        """
        if self.session_data:
            self.calculateStatistics()
    
    def calculateStatistics(self):
        """
        Calcul des statistiques descriptives
        """
        if not self.session_data or not self.session_data.get('sensor_data'):
            self.statistical_tests_text.setPlainText("Aucune donnée disponible pour l'analyse.")
            return
        
        try:
            sensor_data = self.session_data['sensor_data']
            sensor_index = self.sensor_combo.currentIndex()
            
            if sensor_index < 0 or sensor_index >= len(sensor_data):
                return
            
            data = np.array(sensor_data[sensor_index])
            
            # Calcul des statistiques descriptives
            stats_results = self._calculateDescriptiveStats(data)
            
            # Affichage dans le tableau
            self._displayStatsTable(stats_results)
            
            # Création des graphiques
            self._plotHistogram(data)
            self._plotQQPlot(data)
            
            # Tests statistiques
            test_results = self._performStatisticalTests(data)
            
            # Détection d'outliers si demandée
            outliers_results = {}
            if self.outliers_check.isChecked():
                outliers_results = self._detectOutliers(data)
            
            # Compilation des résultats
            self.analysis_results = {
                'sensor_index': sensor_index,
                'descriptive_stats': stats_results,
                'statistical_tests': test_results,
                'outliers': outliers_results,
                'parameters': {
                    'bins': self.bins_spin.value(),
                    'confidence_level': self.confidence_spin.value(),
                    'detect_outliers': self.outliers_check.isChecked()
                }
            }
            
            # Affichage des tests
            self._displayTestResults(test_results, outliers_results)
            
            # Émission du signal de fin d'analyse
            self.analysisCompleted.emit(self.analysis_results)
            
        except Exception as e:
            error_msg = f"Erreur lors du calcul des statistiques: {str(e)}"
            self.statistical_tests_text.setPlainText(error_msg)
    
    def _calculateDescriptiveStats(self, data):
        """
        Calcul des statistiques descriptives
        """
        return {
            'count': len(data),
            'mean': np.mean(data),
            'std': np.std(data, ddof=1),
            'min': np.min(data),
            'max': np.max(data),
            'median': np.median(data),
            'q25': np.percentile(data, 25),
            'q75': np.percentile(data, 75),
            'skewness': stats.skew(data),
            'kurtosis': stats.kurtosis(data),
            'range': np.max(data) - np.min(data),
            'iqr': np.percentile(data, 75) - np.percentile(data, 25),
            'cv': np.std(data, ddof=1) / np.mean(data) * 100 if np.mean(data) != 0 else 0
        }
    
    def _displayStatsTable(self, stats_results):
        """
        Affichage des statistiques dans le tableau
        """
        stats_items = [
            ("Nombre d'échantillons", f"{stats_results['count']}"),
            ("Moyenne", f"{stats_results['mean']:.3f}"),
            ("Écart-type", f"{stats_results['std']:.3f}"),
            ("Minimum", f"{stats_results['min']:.3f}"),
            ("Maximum", f"{stats_results['max']:.3f}"),
            ("Médiane", f"{stats_results['median']:.3f}"),
            ("Q1 (25%)", f"{stats_results['q25']:.3f}"),
            ("Q3 (75%)", f"{stats_results['q75']:.3f}"),
            ("Asymétrie", f"{stats_results['skewness']:.3f}"),
            ("Aplatissement", f"{stats_results['kurtosis']:.3f}"),
            ("Étendue", f"{stats_results['range']:.3f}"),
            ("IQR", f"{stats_results['iqr']:.3f}"),
            ("CV (%)", f"{stats_results['cv']:.2f}")
        ]
        
        self.stats_table.setRowCount(len(stats_items))
        
        for i, (param, value) in enumerate(stats_items):
            self.stats_table.setItem(i, 0, QTableWidgetItem(param))
            self.stats_table.setItem(i, 1, QTableWidgetItem(value))
        
        self.stats_table.resizeColumnsToContents()
    
    def _plotHistogram(self, data):
        """
        Création de l'histogramme
        """
        self.histogram_plot.clear()
        
        bins = self.bins_spin.value()
        hist, bin_edges = np.histogram(data, bins=bins)
        
        # Calcul des centres des bins
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Affichage de l'histogramme
        self.histogram_plot.plot(bin_centers, hist, stepMode=True, fillLevel=0, brush='b')
        
        # Ajout de la courbe normale théorique
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        x_norm = np.linspace(np.min(data), np.max(data), 100)
        y_norm = stats.norm.pdf(x_norm, mean, std) * len(data) * (bin_edges[1] - bin_edges[0])
        
        self.histogram_plot.plot(x_norm, y_norm, pen='r', name='Distribution normale')
    
    def _plotQQPlot(self, data):
        """
        Création du Q-Q plot
        """
        self.qq_plot.clear()
        
        # Calcul des quantiles
        theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(data)))
        sample_quantiles = np.sort(data)
        
        # Normalisation des quantiles observés
        sample_quantiles_norm = (sample_quantiles - np.mean(sample_quantiles)) / np.std(sample_quantiles, ddof=1)
        
        # Affichage des points
        self.qq_plot.plot(theoretical_quantiles, sample_quantiles_norm, pen=None, symbol='o', symbolSize=3)
        
        # Ligne de référence y=x
        min_val = min(np.min(theoretical_quantiles), np.min(sample_quantiles_norm))
        max_val = max(np.max(theoretical_quantiles), np.max(sample_quantiles_norm))
        self.qq_plot.plot([min_val, max_val], [min_val, max_val], pen='r')
    
    def _performStatisticalTests(self, data):
        """
        Exécution des tests statistiques
        """
        results = {}
        
        # Test de normalité de Shapiro-Wilk
        if len(data) <= 5000:  # Limitation de Shapiro-Wilk
            shapiro_stat, shapiro_p = stats.shapiro(data)
            results['shapiro'] = {
                'statistic': shapiro_stat,
                'p_value': shapiro_p,
                'is_normal': shapiro_p > 0.05
            }
        
        # Test de Kolmogorov-Smirnov
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        ks_stat, ks_p = stats.kstest(data, lambda x: stats.norm.cdf(x, mean, std))
        results['kolmogorov_smirnov'] = {
            'statistic': ks_stat,
            'p_value': ks_p,
            'is_normal': ks_p > 0.05
        }
        
        # Test de D'Agostino-Pearson
        try:
            dp_stat, dp_p = stats.normaltest(data)
            results['dagostino_pearson'] = {
                'statistic': dp_stat,
                'p_value': dp_p,
                'is_normal': dp_p > 0.05
            }
        except:
            results['dagostino_pearson'] = None
        
        return results
    
    def _detectOutliers(self, data):
        """
        Détection des outliers
        """
        # Méthode IQR
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers_iqr = data[(data < lower_bound) | (data > upper_bound)]
        
        # Méthode Z-score
        z_scores = np.abs(stats.zscore(data))
        outliers_zscore = data[z_scores > 3]
        
        return {
            'iqr_method': {
                'outliers': outliers_iqr.tolist(),
                'count': len(outliers_iqr),
                'percentage': len(outliers_iqr) / len(data) * 100,
                'bounds': [lower_bound, upper_bound]
            },
            'zscore_method': {
                'outliers': outliers_zscore.tolist(),
                'count': len(outliers_zscore),
                'percentage': len(outliers_zscore) / len(data) * 100
            }
        }
    
    def _displayTestResults(self, test_results, outliers_results):
        """
        Affichage des résultats des tests
        """
        results_text = "Résultats des tests statistiques:\n\n"
        
        # Tests de normalité
        if 'shapiro' in test_results:
            shapiro = test_results['shapiro']
            results_text += f"Test de Shapiro-Wilk:\n"
            results_text += f"  Statistique: {shapiro['statistic']:.4f}\n"
            results_text += f"  p-value: {shapiro['p_value']:.4f}\n"
            results_text += f"  Normal: {'Oui' if shapiro['is_normal'] else 'Non'}\n\n"
        
        ks = test_results['kolmogorov_smirnov']
        results_text += f"Test de Kolmogorov-Smirnov:\n"
        results_text += f"  Statistique: {ks['statistic']:.4f}\n"
        results_text += f"  p-value: {ks['p_value']:.4f}\n"
        results_text += f"  Normal: {'Oui' if ks['is_normal'] else 'Non'}\n\n"
        
        if test_results.get('dagostino_pearson'):
            dp = test_results['dagostino_pearson']
            results_text += f"Test de D'Agostino-Pearson:\n"
            results_text += f"  Statistique: {dp['statistic']:.4f}\n"
            results_text += f"  p-value: {dp['p_value']:.4f}\n"
            results_text += f"  Normal: {'Oui' if dp['is_normal'] else 'Non'}\n\n"
        
        # Outliers
        if outliers_results:
            iqr = outliers_results['iqr_method']
            zscore = outliers_results['zscore_method']
            
            results_text += f"Détection d'outliers:\n"
            results_text += f"  Méthode IQR: {iqr['count']} outliers ({iqr['percentage']:.1f}%)\n"
            results_text += f"  Méthode Z-score: {zscore['count']} outliers ({zscore['percentage']:.1f}%)\n"
        
        self.statistical_tests_text.setPlainText(results_text)
    
    def getResults(self):
        """
        Retourne les résultats de l'analyse statistique
        """
        return self.analysis_results
    
    def resetAnalysis(self):
        """
        Réinitialise l'analyse
        """
        self.histogram_plot.clear()
        self.qq_plot.clear()
        self.stats_table.setRowCount(0)
        self.statistical_tests_text.clear()
        self.analysis_results = {}