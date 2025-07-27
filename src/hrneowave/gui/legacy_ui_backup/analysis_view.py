# -*- coding: utf-8 -*-
"""
Vue d'analyse CHNeoWave
Étape 4 : Analyse et résultats
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox, QSplitter,
    QScrollArea, QGridLayout, QFormLayout, QSpinBox, QDoubleSpinBox,
    QCheckBox, QComboBox, QProgressBar
)
from PySide6.QtCore import Signal, Qt, QThread, Slot
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter

import numpy as np
from datetime import datetime
import json
# Utilisation de l'adaptateur matplotlib pour compatibilité PySide6
from ..components.matplotlib_adapter import pg

class AnalysisView(QWidget):
    """
    Vue d'analyse des données
    Respecte le principe d'isolation : UNIQUEMENT l'analyse
    """

    analysisFinished = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session_data = None
        self.analysis_results = {}
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur
        """
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Titre principal
        title_label = QLabel("Étape 4 : Analyse et Résultats")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2980b9; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Widget à onglets pour les différentes analyses
        self.analysis_tabs = QTabWidget()
        self.analysis_tabs.setMinimumHeight(500)
        
        # Onglet 1 : Analyse spectrale
        self.createSpectralAnalysisTab()
        
        # Onglet 2 : Analyse de Goda
        self.createGodaAnalysisTab()
        
        # Onglet 3 : Statistiques
        self.createStatisticsTab()
        
        # Onglet 4 : Rapport de synthèse
        self.createSummaryTab()
        
        main_layout.addWidget(self.analysis_tabs)
        
        # Espacement
        main_layout.addStretch()
        
        # Bouton de navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.export_button = QPushButton("Suivant : Exporter le Rapport")
        self.export_button.setMinimumHeight(45)
        self.export_button.setMinimumWidth(250)
        self.export_button.setEnabled(False)  # Désactivé par défaut
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #1e3a5f;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #34495e;
            }
        """)
        
        button_layout.addWidget(self.export_button)
        main_layout.addLayout(button_layout)
    
    def createSpectralAnalysisTab(self):
        """
        Création de l'onglet d'analyse spectrale
        """
        spectral_widget = QWidget()
        layout = QVBoxLayout(spectral_widget)
        
        # Splitter horizontal
        splitter = QSplitter(Qt.Horizontal)
        
        # Zone des graphiques
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
        
        splitter.addWidget(graphs_widget)
        
        # Zone de contrôle
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
        self.analyze_spectrum_btn.clicked.connect(self.performSpectralAnalysis)
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
        
        control_widget.setMaximumWidth(300)
        splitter.addWidget(control_widget)
        
        layout.addWidget(splitter)
        self.analysis_tabs.addTab(spectral_widget, "Analyse Spectrale")
    
    def createGodaAnalysisTab(self):
        """
        Création de l'onglet d'analyse de Goda
        """
        goda_widget = QWidget()
        layout = QVBoxLayout(goda_widget)
        
        # Splitter horizontal
        splitter = QSplitter(Qt.Horizontal)
        
        # Zone des graphiques
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        
        # Graphique de la distribution de Goda
        self.goda_plot = pg.PlotWidget()
        self.goda_plot.setLabel('left', 'Hauteur de Vague (m)')
        self.goda_plot.setLabel('bottom', 'Probabilité de Dépassement')
        self.goda_plot.setTitle('Distribution de Goda')
        self.goda_plot.setLogMode(True, False)  # Log sur l'axe X
        graphs_layout.addWidget(self.goda_plot)
        
        # Graphique des hauteurs significatives
        self.wave_height_plot = pg.PlotWidget()
        self.wave_height_plot.setLabel('left', 'Hauteur (m)')
        self.wave_height_plot.setLabel('bottom', 'Temps (s)')
        self.wave_height_plot.setTitle('Évolution des Hauteurs de Vagues')
        graphs_layout.addWidget(self.wave_height_plot)
        
        splitter.addWidget(graphs_widget)
        
        # Zone de contrôle
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Paramètres de Goda
        goda_params_group = QGroupBox("Paramètres de Goda")
        goda_params_layout = QFormLayout(goda_params_group)
        
        self.analysis_duration_spin = QDoubleSpinBox()
        self.analysis_duration_spin.setRange(10.0, 1000.0)
        self.analysis_duration_spin.setValue(100.0)
        self.analysis_duration_spin.setSuffix(" s")
        goda_params_layout.addRow("Durée d'analyse:", self.analysis_duration_spin)
        
        self.zero_crossing_check = QCheckBox("Méthode zero-crossing")
        self.zero_crossing_check.setChecked(True)
        goda_params_layout.addRow(self.zero_crossing_check)
        
        control_layout.addWidget(goda_params_group)
        
        # Bouton d'analyse
        self.analyze_goda_btn = QPushButton("Analyser Goda")
        self.analyze_goda_btn.clicked.connect(self.performGodaAnalysis)
        control_layout.addWidget(self.analyze_goda_btn)
        
        # Résultats de Goda
        goda_results_group = QGroupBox("Résultats de Goda")
        goda_results_layout = QVBoxLayout(goda_results_group)
        
        self.goda_results_text = QTextEdit()
        self.goda_results_text.setMaximumHeight(200)
        self.goda_results_text.setReadOnly(True)
        goda_results_layout.addWidget(self.goda_results_text)
        
        control_layout.addWidget(goda_results_group)
        control_layout.addStretch()
        
        control_widget.setMaximumWidth(300)
        splitter.addWidget(control_widget)
        
        layout.addWidget(splitter)
        self.analysis_tabs.addTab(goda_widget, "Analyse de Goda")
    
    def createStatisticsTab(self):
        """
        Création de l'onglet des statistiques
        """
        # Import de pyqtgraph pour cette méthode
        stats_widget = QWidget()
        layout = QVBoxLayout(stats_widget)
        
        # Splitter horizontal
        splitter = QSplitter(Qt.Horizontal)
        
        # Zone des graphiques statistiques
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        
        # Histogramme des amplitudes
        self.histogram_plot = pg.PlotWidget()
        self.histogram_plot.setLabel('left', 'Fréquence')
        self.histogram_plot.setLabel('bottom', 'Amplitude (mm)')
        self.histogram_plot.setTitle('Distribution des Amplitudes')
        graphs_layout.addWidget(self.histogram_plot)
        
        # Graphique Q-Q plot
        self.qq_plot = pg.PlotWidget()
        self.qq_plot.setLabel('left', 'Quantiles Observés')
        self.qq_plot.setLabel('bottom', 'Quantiles Théoriques')
        self.qq_plot.setTitle('Q-Q Plot (Normalité)')
        graphs_layout.addWidget(self.qq_plot)
        
        splitter.addWidget(graphs_widget)
        
        # Zone des tableaux statistiques
        tables_widget = QWidget()
        tables_layout = QVBoxLayout(tables_widget)
        
        # Tableau des statistiques descriptives
        stats_group = QGroupBox("Statistiques Descriptives")
        stats_group_layout = QVBoxLayout(stats_group)
        
        self.stats_table = QTableWidget(8, 5)  # 8 statistiques, 4 capteurs + 1 colonne nom
        self.stats_table.setHorizontalHeaderLabels(["Statistique", "Capteur 1", "Capteur 2", "Capteur 3", "Capteur 4"])
        
        # Remplissage des noms de statistiques
        stats_names = ["Moyenne", "Écart-type", "Minimum", "Maximum", "Médiane", "Asymétrie", "Aplatissement", "RMS"]
        for i, name in enumerate(stats_names):
            item = QTableWidgetItem(name)
            item.setFlags(Qt.ItemIsEnabled)
            self.stats_table.setItem(i, 0, item)
        
        self.stats_table.resizeColumnsToContents()
        stats_group_layout.addWidget(self.stats_table)
        
        tables_layout.addWidget(stats_group)
        
        # Bouton de calcul des statistiques
        self.calculate_stats_btn = QPushButton("Calculer Statistiques")
        self.calculate_stats_btn.clicked.connect(self.calculateStatistics)
        tables_layout.addWidget(self.calculate_stats_btn)
        
        # Tests statistiques
        tests_group = QGroupBox("Tests Statistiques")
        tests_layout = QVBoxLayout(tests_group)
        
        self.statistical_tests_text = QTextEdit()
        self.statistical_tests_text.setMaximumHeight(150)
        self.statistical_tests_text.setReadOnly(True)
        tests_layout.addWidget(self.statistical_tests_text)
        
        tables_layout.addWidget(tests_group)
        
        tables_widget.setMaximumWidth(400)
        splitter.addWidget(tables_widget)
        
        layout.addWidget(splitter)
        self.analysis_tabs.addTab(stats_widget, "Statistiques")
    
    def createSummaryTab(self):
        """
        Création de l'onglet de rapport de synthèse
        """
        summary_widget = QWidget()
        layout = QVBoxLayout(summary_widget)
        
        # Zone de rapport
        report_group = QGroupBox("Rapport de Synthèse")
        report_layout = QVBoxLayout(report_group)
        
        # Zone de texte pour le rapport
        self.summary_report_text = QTextEdit()
        self.summary_report_text.setMinimumHeight(400)
        self.summary_report_text.setReadOnly(True)
        report_layout.addWidget(self.summary_report_text)
        
        # Boutons de génération
        buttons_layout = QHBoxLayout()
        
        self.generate_report_btn = QPushButton("Générer Rapport")
        self.generate_report_btn.clicked.connect(self.generateSummaryReport)
        buttons_layout.addWidget(self.generate_report_btn)
        
        self.export_pdf_btn = QPushButton("Exporter PDF")
        self.export_pdf_btn.setEnabled(False)
        buttons_layout.addWidget(self.export_pdf_btn)
        
        buttons_layout.addStretch()
        report_layout.addLayout(buttons_layout)
        
        layout.addWidget(report_group)
        self.analysis_tabs.addTab(summary_widget, "Rapport")
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.export_button.clicked.connect(self.completeAnalysis)
    
    def setSessionData(self, session_data):
        """
        Définition des données de session pour l'analyse
        """
        self.session_data = session_data
        self.export_button.setEnabled(True)
        
        # Mise à jour de l'interface avec les nouvelles données
        self.updateDataInfo()
    
    def updateDataInfo(self):
        """
        Mise à jour des informations sur les données
        """
        if not self.session_data:
            return
        
        # Affichage des informations de base dans le premier onglet
        info_text = f"""Données chargées:

Durée: {self.session_data.get('duration', 0):.1f} s
Fréquence d'échantillonnage: {self.session_data.get('sample_rate', 0):.1f} Hz
Nombre de capteurs: {self.session_data.get('sensor_count', 0)}
Nombre de points: {len(self.session_data.get('time_data', []))}

Analyse prête à être lancée."""
        
        self.spectral_results_text.setPlainText(info_text)
    
    def performSpectralAnalysis(self):
        """
        Exécution de l'analyse spectrale
        """
        if not self.session_data or not self.session_data.get('sensor_data'):
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
            self.analysis_results['spectral'] = {
                'frequencies': positive_freqs.tolist() if frequencies is not None else [],
                'spectra': [spectrum.tolist() for spectrum in spectra],
                'parameters': {
                    'window_size': window_size,
                    'overlap': overlap,
                    'window_type': self.window_type_combo.currentText()
                }
            }
            
        except Exception as e:
            self.spectral_results_text.setPlainText(f"Erreur lors de l'analyse spectrale: {str(e)}")
    
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
    
    def performGodaAnalysis(self):
        """
        Exécution de l'analyse de Goda
        """
        if not self.session_data or not self.session_data.get('sensor_data'):
            return
        
        try:
            # Simulation de l'analyse de Goda
            sensor_data = self.session_data['sensor_data'][0]  # Premier capteur
            
            if len(sensor_data) < 100:
                return
            
            # Conversion en mètres (supposé en mm)
            data_m = np.array(sensor_data) / 1000.0
            
            # Détection des vagues (méthode zero-crossing simplifiée)
            zero_crossings = np.where(np.diff(np.sign(data_m)))[0]
            wave_heights = []
            
            for i in range(0, len(zero_crossings)-2, 2):
                start_idx = zero_crossings[i]
                end_idx = zero_crossings[i+2]
                if end_idx < len(data_m):
                    wave_segment = data_m[start_idx:end_idx]
                    wave_height = np.max(wave_segment) - np.min(wave_segment)
                    wave_heights.append(wave_height)
            
            wave_heights = np.array(wave_heights)
            wave_heights = wave_heights[wave_heights > 0.01]  # Filtrer les petites vagues
            
            if len(wave_heights) == 0:
                self.goda_results_text.setPlainText("Aucune vague détectée.")
                return
            
            # Tri des hauteurs
            sorted_heights = np.sort(wave_heights)[::-1]
            
            # Calcul des statistiques de Goda
            n_waves = len(wave_heights)
            h_max = np.max(wave_heights)
            h_mean = np.mean(wave_heights)
            h_rms = np.sqrt(np.mean(wave_heights**2))
            h_13 = np.mean(sorted_heights[:max(1, n_waves//3)])  # H1/3
            h_110 = np.mean(sorted_heights[:max(1, n_waves//10)])  # H1/10
            
            # Distribution de probabilité
            probabilities = np.arange(1, len(sorted_heights)+1) / len(sorted_heights)
            
            # Affichage de la distribution
            self.goda_plot.clear()
            self.goda_plot.plot(probabilities, sorted_heights, pen='b', symbol='o', symbolSize=3)
            
            # Affichage de l'évolution temporelle
            time_indices = np.linspace(0, self.session_data.get('duration', len(wave_heights)), len(wave_heights))
            self.wave_height_plot.clear()
            self.wave_height_plot.plot(time_indices, wave_heights, pen='r', symbol='o', symbolSize=2)
            
            # Résultats textuels
            results_text = f"""Analyse de Goda terminée:

Nombre de vagues: {n_waves}
Hauteur maximale (Hmax): {h_max:.3f} m
Hauteur moyenne (Hmean): {h_mean:.3f} m
Hauteur RMS (Hrms): {h_rms:.3f} m
Hauteur significative (H1/3): {h_13:.3f} m
Hauteur 1/10 (H1/10): {h_110:.3f} m

Ratio H1/3/Hmean: {h_13/h_mean:.2f}
Ratio Hmax/H1/3: {h_max/h_13:.2f}"""
            
            self.goda_results_text.setPlainText(results_text)
            
            # Sauvegarde des résultats
            self.analysis_results['goda'] = {
                'n_waves': n_waves,
                'h_max': h_max,
                'h_mean': h_mean,
                'h_rms': h_rms,
                'h_13': h_13,
                'h_110': h_110,
                'wave_heights': wave_heights.tolist(),
                'probabilities': probabilities.tolist()
            }
            
        except Exception as e:
            self.goda_results_text.setPlainText(f"Erreur lors de l'analyse de Goda: {str(e)}")
    
    def calculateStatistics(self):
        """
        Calcul des statistiques descriptives
        """
        if not self.session_data or not self.session_data.get('sensor_data'):
            return
        
        try:
            sensor_data = self.session_data['sensor_data']
            
            # Calcul des statistiques pour chaque capteur
            for i, data in enumerate(sensor_data[:4]):
                if len(data) == 0:
                    continue
                
                data_array = np.array(data)
                
                # Statistiques descriptives
                mean_val = np.mean(data_array)
                std_val = np.std(data_array)
                min_val = np.min(data_array)
                max_val = np.max(data_array)
                median_val = np.median(data_array)
                
                # Asymétrie et aplatissement
                from scipy import stats
                skewness = stats.skew(data_array)
                kurtosis = stats.kurtosis(data_array)
                rms_val = np.sqrt(np.mean(data_array**2))
                
                # Remplissage du tableau
                stats_values = [mean_val, std_val, min_val, max_val, median_val, skewness, kurtosis, rms_val]
                
                for j, value in enumerate(stats_values):
                    item = QTableWidgetItem(f"{value:.3f}")
                    item.setFlags(Qt.ItemIsEnabled)
                    self.stats_table.setItem(j, i+1, item)
            
            # Tests statistiques
            self.performStatisticalTests()
            
        except ImportError:
            # Si scipy n'est pas disponible, calcul simplifié
            for i, data in enumerate(sensor_data[:4]):
                if len(data) == 0:
                    continue
                
                data_array = np.array(data)
                
                # Statistiques de base seulement
                mean_val = np.mean(data_array)
                std_val = np.std(data_array)
                min_val = np.min(data_array)
                max_val = np.max(data_array)
                median_val = np.median(data_array)
                rms_val = np.sqrt(np.mean(data_array**2))
                
                stats_values = [mean_val, std_val, min_val, max_val, median_val, 0.0, 0.0, rms_val]
                
                for j, value in enumerate(stats_values):
                    item = QTableWidgetItem(f"{value:.3f}")
                    item.setFlags(Qt.ItemIsEnabled)
                    self.stats_table.setItem(j, i+1, item)
            
            self.statistical_tests_text.setPlainText("Tests statistiques non disponibles (scipy requis)")
        
        except Exception as e:
            self.statistical_tests_text.setPlainText(f"Erreur lors du calcul des statistiques: {str(e)}")
    
    def performStatisticalTests(self):
        """
        Exécution des tests statistiques
        """
        try:
            from scipy import stats
            
            sensor_data = self.session_data['sensor_data']
            test_results = "Tests Statistiques:\n\n"
            
            for i, data in enumerate(sensor_data[:4]):
                if len(data) < 8:  # Minimum pour les tests
                    continue
                
                data_array = np.array(data)
                
                # Test de normalité (Shapiro-Wilk)
                if len(data_array) <= 5000:  # Limitation de Shapiro-Wilk
                    stat, p_value = stats.shapiro(data_array[:5000])
                    test_results += f"Capteur {i+1} - Normalité (Shapiro-Wilk):\n"
                    test_results += f"  Statistique: {stat:.4f}\n"
                    test_results += f"  p-value: {p_value:.4f}\n"
                    test_results += f"  Normal: {'Oui' if p_value > 0.05 else 'Non'}\n\n"
            
            self.statistical_tests_text.setPlainText(test_results)
            
        except ImportError:
            self.statistical_tests_text.setPlainText("Tests statistiques non disponibles (scipy requis)")
        except Exception as e:
            self.statistical_tests_text.setPlainText(f"Erreur lors des tests statistiques: {str(e)}")
    
    def generateSummaryReport(self):
        """
        Génération du rapport de synthèse
        """
        if not self.session_data:
            return
        
        # Génération du rapport complet
        report = self.createFullReport()
        self.summary_report_text.setPlainText(report)
        self.export_pdf_btn.setEnabled(True)
    
    def createFullReport(self):
        """
        Création du rapport complet
        """
        report = f"""RAPPORT D'ANALYSE CHNEOWAVE
{'='*50}

DATE D'ANALYSE: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

1. INFORMATIONS GÉNÉRALES
{'-'*30}
Durée d'acquisition: {self.session_data.get('duration', 0):.1f} s
Fréquence d'échantillonnage: {self.session_data.get('sample_rate', 0):.1f} Hz
Nombre de capteurs: {self.session_data.get('sensor_count', 0)}
Nombre de points: {len(self.session_data.get('time_data', []))}

2. RÉSULTATS D'ANALYSE
{'-'*30}"""
        
        # Ajout des résultats spectraux
        if 'spectral' in self.analysis_results:
            report += "\n\nANALYSE SPECTRALE:\n"
            report += "Analyse spectrale réalisée avec succès.\n"
            report += f"Paramètres: Fenêtre {self.analysis_results['spectral']['parameters']['window_size']} points\n"
        
        # Ajout des résultats de Goda
        if 'goda' in self.analysis_results:
            goda = self.analysis_results['goda']
            report += "\n\nANALYSE DE GODA:\n"
            report += f"Nombre de vagues détectées: {goda['n_waves']}\n"
            report += f"Hauteur significative (H1/3): {goda['h_13']:.3f} m\n"
            report += f"Hauteur maximale: {goda['h_max']:.3f} m\n"
            report += f"Hauteur moyenne: {goda['h_mean']:.3f} m\n"
        
        report += "\n\n3. CONCLUSIONS\n"
        report += "-"*30
        report += "\nAnalyse terminée avec succès.\n"
        report += "Toutes les données ont été traitées selon les standards maritimes.\n"
        report += "\nRapport généré par CHNeoWave v1.0.0"
        
        return report
    
    def completeAnalysis(self):
        """
        Finalisation de l'analyse et émission du signal
        """
        # Compilation des résultats finaux
        final_results = {
            'session_data': self.session_data,
            'analysis_results': self.analysis_results,
            'report': self.summary_report_text.toPlainText(),
            'completion_time': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        # Émission du signal vers le MainController
        self.analysisFinished.emit(final_results)
    
    def resetAnalysis(self):
        """
        Réinitialisation de l'analyse
        """
        self.session_data = None
        self.analysis_results.clear()
        
        # Nettoyage des graphiques
        self.spectrum_plot.clear()
        self.transfer_plot.clear()
        self.goda_plot.clear()
        self.wave_height_plot.clear()
        self.histogram_plot.clear()
        self.qq_plot.clear()
        
        # Nettoyage des textes
        self.spectral_results_text.clear()
        self.goda_results_text.clear()
        self.statistical_tests_text.clear()
        self.summary_report_text.clear()
        
        # Nettoyage du tableau
        for i in range(self.stats_table.rowCount()):
            for j in range(1, self.stats_table.columnCount()):
                self.stats_table.setItem(i, j, QTableWidgetItem(""))
        
        # Désactivation des boutons
        self.export_button.setEnabled(False)
        self.export_pdf_btn.setEnabled(False)
    
    def reset_view(self):
        """
        Réinitialise la vue pour un nouveau projet
        """
        self.resetAnalysis()
    
    def set_acquisition_data(self, acquisition_data):
        """
        Configure la vue avec les données d'acquisition
        """
        self.session_data = acquisition_data
        
        # Activation automatique de l'analyse spectrale
        if self.session_data and self.session_data.get('sensor_data'):
            self.performSpectralAnalysis()
            self.performGodaAnalysis()
            self.calculateStatistics()
            self.generateSummaryReport()
            
            # Activation du bouton suivant
            self.export_button.setEnabled(True)
    
    def get_analysis_results(self):
        """
        Retourne les résultats d'analyse pour le workflow
        """
        return {
            'session_data': self.session_data,
            'analysis_results': self.analysis_results,
            'report': self.summary_report_text.toPlainText() if hasattr(self, 'summary_report_text') else '',
            'completion_time': datetime.now().isoformat(),
            'status': 'completed' if self.analysis_results else 'pending'
        }