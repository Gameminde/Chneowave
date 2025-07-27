# -*- coding: utf-8 -*-
"""
Widget d'analyse de Goda CHNeoWave
Extrait de analysis_view.py pour une meilleure modularité
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QSplitter, QFormLayout, QSpinBox, QComboBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

import numpy as np
from ...components.matplotlib_adapter import pg


class GodaAnalysisWidget(QWidget):
    """
    Widget spécialisé pour l'analyse de Goda
    Responsabilité unique : analyse statistique des hauteurs de vagues
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
        Configuration de l'interface utilisateur pour l'analyse de Goda
        """
        layout = QVBoxLayout(self)
        
        # Splitter horizontal
        splitter = QSplitter(Qt.Horizontal)
        
        # Zone des graphiques
        graphs_widget = self._createGraphsWidget()
        splitter.addWidget(graphs_widget)
        
        # Zone de contrôle
        control_widget = self._createControlWidget()
        control_widget.setMaximumWidth(300)
        splitter.addWidget(control_widget)
        
        layout.addWidget(splitter)
    
    def _createGraphsWidget(self):
        """
        Création de la zone des graphiques
        """
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        
        # Graphique de la distribution de Goda
        self.goda_plot = pg.PlotWidget()
        self.goda_plot.setLabel('left', 'Hauteur de Vague (m)')
        self.goda_plot.setLabel('bottom', 'Probabilité de Dépassement')
        self.goda_plot.setTitle('Distribution de Goda')
        graphs_layout.addWidget(self.goda_plot)
        
        # Graphique de l'évolution des hauteurs
        self.wave_height_plot = pg.PlotWidget()
        self.wave_height_plot.setLabel('left', 'Hauteur (m)')
        self.wave_height_plot.setLabel('bottom', 'Temps (s)')
        self.wave_height_plot.setTitle('Évolution des Hauteurs de Vagues')
        graphs_layout.addWidget(self.wave_height_plot)
        
        return graphs_widget
    
    def _createControlWidget(self):
        """
        Création de la zone de contrôle
        """
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Paramètres de Goda
        params_group = QGroupBox("Paramètres de Goda")
        params_layout = QFormLayout(params_group)
        
        self.min_wave_height_spin = QSpinBox()
        self.min_wave_height_spin.setRange(1, 100)
        self.min_wave_height_spin.setValue(10)
        self.min_wave_height_spin.setSuffix(" mm")
        params_layout.addRow("Hauteur min:", self.min_wave_height_spin)
        
        self.detection_method_combo = QComboBox()
        self.detection_method_combo.addItems(["Zero-crossing", "Peak-to-trough", "Envelope"])
        params_layout.addRow("Méthode détection:", self.detection_method_combo)
        
        control_layout.addWidget(params_group)
        
        # Bouton d'analyse
        self.analyze_goda_btn = QPushButton("Analyser Goda")
        control_layout.addWidget(self.analyze_goda_btn)
        
        # Résultats
        results_group = QGroupBox("Résultats de Goda")
        results_layout = QVBoxLayout(results_group)
        
        self.goda_results_text = QTextEdit()
        self.goda_results_text.setMaximumHeight(250)
        self.goda_results_text.setReadOnly(True)
        results_layout.addWidget(self.goda_results_text)
        
        control_layout.addWidget(results_group)
        control_layout.addStretch()
        
        return control_widget
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.analyze_goda_btn.clicked.connect(self.performGodaAnalysis)
    
    def setSessionData(self, session_data):
        """
        Configuration des données de session
        """
        self.session_data = session_data
        self.updateDataInfo()
    
    def updateDataInfo(self):
        """
        Mise à jour des informations sur les données
        """
        if not self.session_data:
            return
        
        sensor_data = self.session_data.get('sensor_data', [])
        duration = self.session_data.get('duration', 0)
        
        info_text = f"""Données disponibles pour l'analyse de Goda:

Capteur principal: {len(sensor_data[0]) if sensor_data else 0} échantillons
Durée d'acquisition: {duration:.1f} s

L'analyse de Goda permet de calculer:
- Hauteurs significatives (H1/3, H1/10)
- Distribution statistique des vagues
- Paramètres de Goda

Cliquez sur 'Analyser Goda' pour commencer."""
        
        self.goda_results_text.setPlainText(info_text)
    
    def performGodaAnalysis(self):
        """
        Exécution de l'analyse de Goda
        """
        if not self.session_data or not self.session_data.get('sensor_data'):
            self.goda_results_text.setPlainText("Aucune donnée disponible pour l'analyse.")
            return
        
        try:
            # Simulation de l'analyse de Goda
            sensor_data = self.session_data['sensor_data'][0]  # Premier capteur
            
            if len(sensor_data) < 100:
                self.goda_results_text.setPlainText("Données insuffisantes pour l'analyse.")
                return
            
            # Conversion en mètres (supposé en mm)
            data_m = np.array(sensor_data) / 1000.0
            
            # Détection des vagues selon la méthode choisie
            wave_heights = self._detectWaves(data_m)
            
            if len(wave_heights) == 0:
                self.goda_results_text.setPlainText("Aucune vague détectée.")
                return
            
            # Calcul des statistiques de Goda
            goda_stats = self._calculateGodaStatistics(wave_heights)
            
            # Affichage des graphiques
            self._plotGodaDistribution(goda_stats)
            self._plotWaveHeightEvolution(wave_heights)
            
            # Affichage des résultats textuels
            self._displayResults(goda_stats)
            
            # Sauvegarde des résultats
            self.analysis_results = goda_stats
            
            # Émission du signal de fin d'analyse
            self.analysisCompleted.emit(self.analysis_results)
            
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse de Goda: {str(e)}"
            self.goda_results_text.setPlainText(error_msg)
    
    def _detectWaves(self, data_m):
        """
        Détection des vagues selon la méthode sélectionnée
        """
        method = self.detection_method_combo.currentText()
        min_height = self.min_wave_height_spin.value() / 1000.0  # Conversion en mètres
        
        if method == "Zero-crossing":
            return self._detectWavesZeroCrossing(data_m, min_height)
        elif method == "Peak-to-trough":
            return self._detectWavesPeakToTrough(data_m, min_height)
        else:  # Envelope
            return self._detectWavesEnvelope(data_m, min_height)
    
    def _detectWavesZeroCrossing(self, data_m, min_height):
        """
        Détection des vagues par méthode zero-crossing
        """
        # Détection des passages par zéro
        zero_crossings = np.where(np.diff(np.sign(data_m)))[0]
        wave_heights = []
        
        for i in range(0, len(zero_crossings)-2, 2):
            start_idx = zero_crossings[i]
            end_idx = zero_crossings[i+2]
            if end_idx < len(data_m):
                wave_segment = data_m[start_idx:end_idx]
                wave_height = np.max(wave_segment) - np.min(wave_segment)
                if wave_height > min_height:
                    wave_heights.append(wave_height)
        
        return np.array(wave_heights)
    
    def _detectWavesPeakToTrough(self, data_m, min_height):
        """
        Détection des vagues par méthode peak-to-trough
        """
        # Détection des pics et creux
        from scipy.signal import find_peaks
        
        peaks, _ = find_peaks(data_m, height=min_height/2)
        troughs, _ = find_peaks(-data_m, height=min_height/2)
        
        wave_heights = []
        for peak in peaks:
            # Trouver les creux avant et après le pic
            before_troughs = troughs[troughs < peak]
            after_troughs = troughs[troughs > peak]
            
            if len(before_troughs) > 0 and len(after_troughs) > 0:
                trough_before = before_troughs[-1]
                trough_after = after_troughs[0]
                
                height = data_m[peak] - min(data_m[trough_before], data_m[trough_after])
                if height > min_height:
                    wave_heights.append(height)
        
        return np.array(wave_heights)
    
    def _detectWavesEnvelope(self, data_m, min_height):
        """
        Détection des vagues par méthode d'enveloppe
        """
        # Calcul de l'enveloppe par transformée de Hilbert
        from scipy.signal import hilbert
        
        analytic_signal = hilbert(data_m)
        envelope = np.abs(analytic_signal)
        
        # Détection des pics dans l'enveloppe
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(envelope, height=min_height, distance=10)
        
        wave_heights = envelope[peaks]
        return wave_heights[wave_heights > min_height]
    
    def _calculateGodaStatistics(self, wave_heights):
        """
        Calcul des statistiques de Goda
        """
        # Tri des hauteurs
        sorted_heights = np.sort(wave_heights)[::-1]
        
        # Calcul des statistiques de base
        n_waves = len(wave_heights)
        h_max = np.max(wave_heights)
        h_mean = np.mean(wave_heights)
        h_rms = np.sqrt(np.mean(wave_heights**2))
        h_13 = np.mean(sorted_heights[:max(1, n_waves//3)])  # H1/3
        h_110 = np.mean(sorted_heights[:max(1, n_waves//10)])  # H1/10
        
        # Distribution de probabilité
        probabilities = np.arange(1, len(sorted_heights)+1) / len(sorted_heights)
        
        return {
            'n_waves': n_waves,
            'h_max': h_max,
            'h_mean': h_mean,
            'h_rms': h_rms,
            'h_13': h_13,
            'h_110': h_110,
            'wave_heights': wave_heights.tolist(),
            'sorted_heights': sorted_heights.tolist(),
            'probabilities': probabilities.tolist(),
            'ratios': {
                'h13_hmean': h_13/h_mean if h_mean > 0 else 0,
                'hmax_h13': h_max/h_13 if h_13 > 0 else 0
            }
        }
    
    def _plotGodaDistribution(self, goda_stats):
        """
        Affichage de la distribution de Goda
        """
        self.goda_plot.clear()
        
        probabilities = goda_stats['probabilities']
        sorted_heights = goda_stats['sorted_heights']
        
        self.goda_plot.plot(probabilities, sorted_heights, pen='b', symbol='o', symbolSize=3)
        
        # Ajout de lignes de référence pour H1/3 et H1/10
        h_13 = goda_stats['h_13']
        h_110 = goda_stats['h_110']
        
        # Ligne H1/3
        self.goda_plot.addLine(y=h_13, pen='r', label='H1/3')
        # Ligne H1/10
        self.goda_plot.addLine(y=h_110, pen='g', label='H1/10')
    
    def _plotWaveHeightEvolution(self, wave_heights):
        """
        Affichage de l'évolution temporelle des hauteurs
        """
        self.wave_height_plot.clear()
        
        duration = self.session_data.get('duration', len(wave_heights))
        time_indices = np.linspace(0, duration, len(wave_heights))
        
        self.wave_height_plot.plot(time_indices, wave_heights, pen='r', symbol='o', symbolSize=2)
    
    def _displayResults(self, goda_stats):
        """
        Affichage des résultats textuels
        """
        results_text = f"""Analyse de Goda terminée:

Nombre de vagues: {goda_stats['n_waves']}
Hauteur maximale (Hmax): {goda_stats['h_max']:.3f} m
Hauteur moyenne (Hmean): {goda_stats['h_mean']:.3f} m
Hauteur RMS (Hrms): {goda_stats['h_rms']:.3f} m
Hauteur significative (H1/3): {goda_stats['h_13']:.3f} m
Hauteur 1/10 (H1/10): {goda_stats['h_110']:.3f} m

Ratios caractéristiques:
H1/3/Hmean: {goda_stats['ratios']['h13_hmean']:.2f}
Hmax/H1/3: {goda_stats['ratios']['hmax_h13']:.2f}

Méthode de détection: {self.detection_method_combo.currentText()}
Hauteur minimale: {self.min_wave_height_spin.value()} mm"""
        
        self.goda_results_text.setPlainText(results_text)
    
    def getResults(self):
        """
        Retourne les résultats de l'analyse de Goda
        """
        return self.analysis_results
    
    def resetAnalysis(self):
        """
        Réinitialise l'analyse
        """
        self.goda_plot.clear()
        self.wave_height_plot.clear()
        self.goda_results_text.clear()
        self.analysis_results = {}