# -*- coding: utf-8 -*-
"""
Widget d'analyse spectrale CHNeoWave
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


class SpectralAnalysisWidget(QWidget):
    """
    Widget spécialisé pour l'analyse spectrale
    Responsabilité unique : analyse des spectres de densité de puissance
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
        Configuration de l'interface utilisateur pour l'analyse spectrale
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
        
        # Graphique des spectres
        self.spectrum_plot = pg.PlotWidget()
        self.spectrum_plot.setLabel('left', 'Densité Spectrale (m²/Hz)')
        self.spectrum_plot.setLabel('bottom', 'Fréquence (Hz)')
        self.spectrum_plot.setTitle('Spectres de Densité de Puissance')
        self.spectrum_plot.setLogMode(False, True)  # Log sur l'axe Y
        graphs_layout.addWidget(self.spectrum_plot)
        
        # Graphique des fonctions de transfert
        self.transfer_plot = pg.PlotWidget()
        self.transfer_plot.setLabel('left', 'Cohérence')
        self.transfer_plot.setLabel('bottom', 'Fréquence (Hz)')
        self.transfer_plot.setTitle('Fonctions de Cohérence')
        graphs_layout.addWidget(self.transfer_plot)
        
        return graphs_widget
    
    def _createControlWidget(self):
        """
        Création de la zone de contrôle
        """
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Paramètres d'analyse
        params_group = QGroupBox("Paramètres d'Analyse")
        params_layout = QFormLayout(params_group)
        
        self.window_size_spin = QSpinBox()
        self.window_size_spin.setRange(64, 2048)
        self.window_size_spin.setValue(512)
        params_layout.addRow("Taille fenêtre:", self.window_size_spin)
        
        self.overlap_spin = QSpinBox()
        self.overlap_spin.setRange(0, 90)
        self.overlap_spin.setValue(50)
        self.overlap_spin.setSuffix("%")
        params_layout.addRow("Recouvrement:", self.overlap_spin)
        
        self.window_type_combo = QComboBox()
        self.window_type_combo.addItems(["Hanning", "Hamming", "Blackman", "Rectangular"])
        params_layout.addRow("Type fenêtre:", self.window_type_combo)
        
        control_layout.addWidget(params_group)
        
        # Bouton d'analyse
        self.analyze_spectrum_btn = QPushButton("Analyser Spectres")
        control_layout.addWidget(self.analyze_spectrum_btn)
        
        # Résultats
        results_group = QGroupBox("Résultats Spectraux")
        results_layout = QVBoxLayout(results_group)
        
        self.spectral_results_text = QTextEdit()
        self.spectral_results_text.setMaximumHeight(200)
        self.spectral_results_text.setReadOnly(True)
        results_layout.addWidget(self.spectral_results_text)
        
        control_layout.addWidget(results_group)
        control_layout.addStretch()
        
        return control_widget
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.analyze_spectrum_btn.clicked.connect(self.performSpectralAnalysis)
    
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
        sample_rate = self.session_data.get('sample_rate', 100.0)
        duration = self.session_data.get('duration', 0)
        
        info_text = f"""Données disponibles pour l'analyse spectrale:

Nombre de capteurs: {len(sensor_data)}
Fréquence d'échantillonnage: {sample_rate} Hz
Durée d'acquisition: {duration:.1f} s
Nombre d'échantillons: {len(sensor_data[0]) if sensor_data else 0}

Paramètres recommandés:
- Taille de fenêtre: {min(512, len(sensor_data[0])//4 if sensor_data else 512)}
- Recouvrement: 50%
- Type de fenêtre: Hanning"""
        
        self.spectral_results_text.setPlainText(info_text)
    
    def performSpectralAnalysis(self):
        """
        Exécution de l'analyse spectrale
        """
        if not self.session_data or not self.session_data.get('sensor_data'):
            self.spectral_results_text.setPlainText("Aucune donnée disponible pour l'analyse.")
            return
        
        try:
            # Paramètres d'analyse
            window_size = self.window_size_spin.value()
            overlap = self.overlap_spin.value() / 100.0
            
            # Analyse pour chaque capteur
            sensor_data = self.session_data['sensor_data']
            sample_rate = self.session_data.get('sample_rate', 100.0)
            
            # Calcul des spectres
            frequencies = None
            spectra = []
            
            colors = ['r', 'g', 'b', 'y']
            self.spectrum_plot.clear()
            
            for i, data in enumerate(sensor_data[:4]):  # Maximum 4 capteurs
                if len(data) < window_size:
                    continue
                
                # FFT avec fenêtrage
                data_array = np.array(data)
                
                # Application d'une fenêtre de Hanning
                windowed_data = data_array * np.hanning(len(data_array))
                
                # Calcul de la FFT
                fft = np.fft.fft(windowed_data)
                frequencies = np.fft.fftfreq(len(windowed_data), 1/sample_rate)
                
                # Densité spectrale de puissance
                psd = np.abs(fft)**2 / (sample_rate * len(windowed_data))
                
                # Garder seulement les fréquences positives
                positive_freqs = frequencies[:len(frequencies)//2]
                positive_psd = psd[:len(psd)//2]
                
                spectra.append(positive_psd)
                
                # Affichage
                self.spectrum_plot.plot(positive_freqs, positive_psd, 
                                      pen=colors[i], name=f'Capteur {i+1}')
            
            # Calcul des statistiques spectrales
            if frequencies is not None and spectra:
                self.calculateSpectralStatistics(positive_freqs, spectra)
            
            # Sauvegarde des résultats
            self.analysis_results = {
                'frequencies': positive_freqs.tolist() if frequencies is not None else [],
                'spectra': [spectrum.tolist() for spectrum in spectra],
                'parameters': {
                    'window_size': window_size,
                    'overlap': overlap,
                    'window_type': self.window_type_combo.currentText()
                }
            }
            
            # Émission du signal de fin d'analyse
            self.analysisCompleted.emit(self.analysis_results)
            
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse spectrale: {str(e)}"
            self.spectral_results_text.setPlainText(error_msg)
    
    def calculateSpectralStatistics(self, frequencies, spectra):
        """
        Calcul des statistiques spectrales
        """
        try:
            results_text = "Résultats de l'analyse spectrale:\n\n"
            
            for i, spectrum in enumerate(spectra):
                # Fréquence de pic
                peak_idx = np.argmax(spectrum)
                peak_freq = frequencies[peak_idx]
                
                # Fréquence moyenne
                mean_freq = np.sum(frequencies * spectrum) / np.sum(spectrum)
                
                # Largeur spectrale
                total_power = np.sum(spectrum)
                cumulative_power = np.cumsum(spectrum)
                f25_idx = np.where(cumulative_power >= 0.25 * total_power)[0][0]
                f75_idx = np.where(cumulative_power >= 0.75 * total_power)[0][0]
                spectral_width = frequencies[f75_idx] - frequencies[f25_idx]
                
                results_text += f"Capteur {i+1}:\n"
                results_text += f"  Fréquence de pic: {peak_freq:.3f} Hz\n"
                results_text += f"  Fréquence moyenne: {mean_freq:.3f} Hz\n"
                results_text += f"  Largeur spectrale: {spectral_width:.3f} Hz\n\n"
            
            self.spectral_results_text.setPlainText(results_text)
            
        except Exception as e:
            self.spectral_results_text.setPlainText(f"Erreur dans le calcul des statistiques: {str(e)}")
    
    def getResults(self):
        """
        Retourne les résultats de l'analyse spectrale
        """
        return self.analysis_results
    
    def resetAnalysis(self):
        """
        Réinitialise l'analyse
        """
        self.spectrum_plot.clear()
        self.transfer_plot.clear()
        self.spectral_results_text.clear()
        self.analysis_results = {}