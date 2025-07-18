# enhanced_analysis_tab.py - Module d'analyse avec graphiques statiques et transitions
import sys
import os
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import json

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QPushButton,
    QTextEdit, QFormLayout, QSpinBox, QDoubleSpinBox, QComboBox, 
    QCheckBox, QFrame, QSplitter, QScrollArea, QGridLayout, QTabWidget,
    QSizePolicy, QMessageBox, QApplication, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QSlider, QFileDialog
)
from PyQt5.QtCore import (
    Qt, pyqtSignal, pyqtSlot, QTimer, QThread, QObject, QPropertyAnimation,
    QEasingCurve, QRect, QSize
)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QPainter

try:
    import pyqtgraph as pg
    from pyqtgraph import PlotWidget, mkPen, mkBrush
    import numpy as np
    PYQTGRAPH_AVAILABLE = True
    NUMPY_AVAILABLE = True
except ImportError as e:
    PYQTGRAPH_AVAILABLE = False
    NUMPY_AVAILABLE = False
    print(f"⚠️ Modules d'analyse non disponibles: {e}")

try:
    from .field_validator import FieldValidator
    from .theme import get_theme_colors, register_theme_callback
except ImportError as e:
    print(f"⚠️ Import manquant: {e}")
    FieldValidator = None

class AnalysisWorker(QObject):
    """Worker thread pour l'analyse de données"""
    
    analysisProgress = pyqtSignal(int)  # pourcentage
    analysisFinished = pyqtSignal(dict)  # résultats
    errorOccurred = pyqtSignal(str)  # erreur
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__()
        self.data = data
        
    def analyze_data(self):
        """Effectue l'analyse des données"""
        try:
            results = {}
            
            # Simulation d'analyse progressive
            self.analysisProgress.emit(10)
            
            # Analyse statistique de base
            if 'time_series' in self.data and NUMPY_AVAILABLE:
                time_series = np.array(self.data['time_series'])
                
                results['statistics'] = {
                    'mean': float(np.mean(time_series)),
                    'std': float(np.std(time_series)),
                    'min': float(np.min(time_series)),
                    'max': float(np.max(time_series)),
                    'rms': float(np.sqrt(np.mean(time_series**2)))
                }
                
            self.analysisProgress.emit(30)
            
            # Analyse spectrale (simulation)
            if NUMPY_AVAILABLE and 'sample_rate' in self.data:
                sample_rate = self.data['sample_rate']
                n_samples = len(self.data.get('time_series', []))
                
                # Fréquences simulées
                freqs = np.linspace(0, sample_rate/2, n_samples//2)
                
                # Spectre simulé (houle typique)
                spectrum = self._simulate_wave_spectrum(freqs)
                
                results['spectrum'] = {
                    'frequencies': freqs.tolist(),
                    'power': spectrum.tolist(),
                    'peak_frequency': float(freqs[np.argmax(spectrum)]),
                    'significant_height': float(4 * np.sqrt(np.trapz(spectrum, freqs)))
                }
                
            self.analysisProgress.emit(60)
            
            # Analyse des vagues (simulation)
            results['wave_analysis'] = self._analyze_waves()
            
            self.analysisProgress.emit(80)
            
            # Paramètres de houle
            results['wave_parameters'] = self._calculate_wave_parameters()
            
            self.analysisProgress.emit(100)
            
            # Finaliser
            results['analysis_time'] = datetime.now().isoformat()
            results['data_duration'] = self.data.get('duration', 0)
            results['sample_count'] = len(self.data.get('time_series', []))
            
            self.analysisFinished.emit(results)
            
        except Exception as e:
            self.errorOccurred.emit(f"Erreur d'analyse: {e}")
            
    def _simulate_wave_spectrum(self, freqs: 'np.ndarray') -> 'np.ndarray':
        """Simule un spectre de houle JONSWAP"""
        if not NUMPY_AVAILABLE:
            return []
            
        # Paramètres JONSWAP typiques
        fp = 0.1  # Fréquence de pic (Hz)
        hs = 2.0  # Hauteur significative (m)
        gamma = 3.3  # Facteur de pic
        
        # Éviter division par zéro
        freqs = np.where(freqs == 0, 1e-10, freqs)
        
        # Spectre JONSWAP simplifié
        alpha = 0.0081
        sigma = np.where(freqs <= fp, 0.07, 0.09)
        
        spectrum = (alpha * 9.81**2 / (2 * np.pi)**4 / freqs**5 * 
                   np.exp(-1.25 * (fp / freqs)**4) *
                   gamma ** np.exp(-0.5 * ((freqs - fp) / (sigma * fp))**2))
                   
        return spectrum * (hs / 4)**2 / np.trapz(spectrum, freqs)
        
    def _analyze_waves(self) -> Dict[str, Any]:
        """Analyse des vagues individuelles"""
        # Simulation de détection de vagues
        n_waves = np.random.randint(50, 150) if NUMPY_AVAILABLE else 100
        
        # Hauteurs de vagues simulées (distribution Rayleigh)
        if NUMPY_AVAILABLE:
            wave_heights = np.random.rayleigh(1.0, n_waves)
            wave_periods = np.random.normal(8.0, 2.0, n_waves)
            wave_periods = np.clip(wave_periods, 3.0, 20.0)
        else:
            wave_heights = [1.0] * n_waves
            wave_periods = [8.0] * n_waves
            
        return {
            'wave_count': n_waves,
            'wave_heights': wave_heights.tolist() if NUMPY_AVAILABLE else wave_heights,
            'wave_periods': wave_periods.tolist() if NUMPY_AVAILABLE else wave_periods,
            'max_height': float(max(wave_heights)),
            'mean_height': float(np.mean(wave_heights)) if NUMPY_AVAILABLE else sum(wave_heights)/len(wave_heights),
            'mean_period': float(np.mean(wave_periods)) if NUMPY_AVAILABLE else sum(wave_periods)/len(wave_periods)
        }
        
    def _calculate_wave_parameters(self) -> Dict[str, Any]:
        """Calcule les paramètres de houle standards"""
        # Paramètres simulés basés sur des conditions méditerranéennes typiques
        return {
            'Hs': 1.8,  # Hauteur significative (m)
            'Tp': 7.2,  # Période de pic (s)
            'Tm': 6.8,  # Période moyenne (s)
            'H_max': 3.2,  # Hauteur maximale (m)
            'steepness': 0.045,  # Cambrure
            'direction': 225,  # Direction (°)
            'spreading': 25,  # Étalement directionnel (°)
            'energy': 1650,  # Énergie totale (J/m²)
            'power': 12.5  # Puissance (kW/m)
        }

class StaticPlotWidget(QWidget):
    """Widget de graphiques statiques pour l'analyse"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plots = {}
        self._init_ui()
        
    def _init_ui(self):
        """Initialise l'interface des graphiques"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        if not PYQTGRAPH_AVAILABLE:
            error_label = QLabel("PyQtGraph non disponible")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)
            return
            
        # Onglets pour différents types de graphiques
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Onglet série temporelle
        self.time_series_plot = PlotWidget()
        self.time_series_plot.setLabel('left', 'Amplitude (m)')
        self.time_series_plot.setLabel('bottom', 'Temps (s)')
        self.time_series_plot.setTitle('Série Temporelle')
        self.time_series_plot.showGrid(x=True, y=True, alpha=0.3)
        self.tab_widget.addTab(self.time_series_plot, "📈 Série Temporelle")
        
        # Onglet spectre
        self.spectrum_plot = PlotWidget()
        self.spectrum_plot.setLabel('left', 'Densité Spectrale (m²/Hz)')
        self.spectrum_plot.setLabel('bottom', 'Fréquence (Hz)')
        self.spectrum_plot.setTitle('Spectre de Houle')
        self.spectrum_plot.showGrid(x=True, y=True, alpha=0.3)
        self.spectrum_plot.setLogMode(x=False, y=True)
        self.tab_widget.addTab(self.spectrum_plot, "📊 Spectre")
        
        # Onglet statistiques des vagues
        self.waves_plot = PlotWidget()
        self.waves_plot.setLabel('left', 'Hauteur (m)')
        self.waves_plot.setLabel('bottom', 'Numéro de vague')
        self.waves_plot.setTitle('Hauteurs de Vagues')
        self.waves_plot.showGrid(x=True, y=True, alpha=0.3)
        self.tab_widget.addTab(self.waves_plot, "🌊 Vagues")
        
        # Onglet rose des directions
        self.direction_plot = PlotWidget()
        self.direction_plot.setLabel('left', 'Énergie')
        self.direction_plot.setLabel('bottom', 'Direction (°)')
        self.direction_plot.setTitle('Rose des Directions')
        self.direction_plot.showGrid(x=True, y=True, alpha=0.3)
        self.tab_widget.addTab(self.direction_plot, "🧭 Directions")
        
    def update_plots(self, analysis_results: Dict[str, Any]):
        """Met à jour tous les graphiques avec les résultats d'analyse"""
        if not PYQTGRAPH_AVAILABLE:
            return
            
        try:
            # Série temporelle
            if 'time_series' in analysis_results:
                self._plot_time_series(analysis_results['time_series'])
                
            # Spectre
            if 'spectrum' in analysis_results:
                self._plot_spectrum(analysis_results['spectrum'])
                
            # Vagues
            if 'wave_analysis' in analysis_results:
                self._plot_waves(analysis_results['wave_analysis'])
                
            # Directions
            if 'wave_parameters' in analysis_results:
                self._plot_directions(analysis_results['wave_parameters'])
                
        except Exception as e:
            print(f"⚠️ Erreur mise à jour graphiques: {e}")
            
    def _plot_time_series(self, time_data: List[float]):
        """Trace la série temporelle"""
        self.time_series_plot.clear()
        
        if not time_data:
            return
            
        # Créer l'axe temporel
        time_axis = list(range(len(time_data)))
        
        # Tracer la série
        pen = mkPen(color='#3498db', width=1)
        self.time_series_plot.plot(time_axis, time_data, pen=pen, name='Élévation')
        
        # Ajouter la moyenne
        if NUMPY_AVAILABLE:
            mean_val = np.mean(time_data)
            mean_line = pg.InfiniteLine(pos=mean_val, angle=0, pen=mkPen(color='#e74c3c', style=Qt.DashLine))
            self.time_series_plot.addItem(mean_line)
            
    def _plot_spectrum(self, spectrum_data: Dict[str, Any]):
        """Trace le spectre de puissance"""
        self.spectrum_plot.clear()
        
        freqs = spectrum_data.get('frequencies', [])
        power = spectrum_data.get('power', [])
        
        if not freqs or not power:
            return
            
        # Tracer le spectre
        pen = mkPen(color='#2ecc71', width=2)
        self.spectrum_plot.plot(freqs, power, pen=pen, name='Spectre')
        
        # Marquer la fréquence de pic
        peak_freq = spectrum_data.get('peak_frequency', 0)
        if peak_freq > 0:
            peak_line = pg.InfiniteLine(pos=peak_freq, angle=90, pen=mkPen(color='#e74c3c', style=Qt.DashLine))
            self.spectrum_plot.addItem(peak_line)
            
        # Remplir sous la courbe
        brush = mkBrush(color=(46, 204, 113, 50))
        self.spectrum_plot.plot(freqs, power, fillLevel=0, brush=brush)
        
    def _plot_waves(self, wave_data: Dict[str, Any]):
        """Trace les hauteurs de vagues"""
        self.waves_plot.clear()
        
        heights = wave_data.get('wave_heights', [])
        
        if not heights:
            return
            
        # Numéros de vagues
        wave_numbers = list(range(1, len(heights) + 1))
        
        # Tracer les hauteurs
        pen = mkPen(color='#9b59b6', width=1)
        brush = mkBrush(color=(155, 89, 182, 100))
        
        # Graphique en barres
        bargraph = pg.BarGraphItem(x=wave_numbers, height=heights, width=0.8, brush=brush, pen=pen)
        self.waves_plot.addItem(bargraph)
        
        # Ligne de hauteur significative (approximation)
        if NUMPY_AVAILABLE and heights:
            hs_approx = 4 * np.std(heights)
            hs_line = pg.InfiniteLine(pos=hs_approx, angle=0, pen=mkPen(color='#e74c3c', style=Qt.DashLine))
            self.waves_plot.addItem(hs_line)
            
    def _plot_directions(self, wave_params: Dict[str, Any]):
        """Trace la rose des directions (simulation)"""
        self.direction_plot.clear()
        
        if not NUMPY_AVAILABLE:
            return
            
        # Simulation d'une distribution directionnelle
        directions = np.linspace(0, 360, 36)
        main_dir = wave_params.get('direction', 225)
        spreading = wave_params.get('spreading', 25)
        
        # Distribution gaussienne centrée sur la direction principale
        energy = np.exp(-0.5 * ((directions - main_dir) / spreading)**2)
        energy = energy / np.max(energy)  # Normaliser
        
        # Tracer
        pen = mkPen(color='#f39c12', width=2)
        brush = mkBrush(color=(243, 156, 18, 100))
        
        self.direction_plot.plot(directions, energy, pen=pen, fillLevel=0, brush=brush, name='Énergie directionnelle')
        
        # Marquer la direction principale
        main_line = pg.InfiniteLine(pos=main_dir, angle=90, pen=mkPen(color='#e74c3c', style=Qt.DashLine))
        self.direction_plot.addItem(main_line)
        
    def clear_plots(self):
        """Efface tous les graphiques"""
        if PYQTGRAPH_AVAILABLE:
            self.time_series_plot.clear()
            self.spectrum_plot.clear()
            self.waves_plot.clear()
            self.direction_plot.clear()

class ParametersTable(QTableWidget):
    """Tableau des paramètres de houle"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_table()
        
    def _init_table(self):
        """Initialise le tableau"""
        # Configuration du tableau
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Paramètre", "Valeur", "Unité"])
        
        # Ajuster les colonnes
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # Style
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        
    def update_parameters(self, wave_params: Dict[str, Any], statistics: Dict[str, Any] = None):
        """Met à jour les paramètres affichés"""
        # Définir les paramètres à afficher
        params_info = [
            ("Hauteur significative", wave_params.get('Hs', 0), "m"),
            ("Période de pic", wave_params.get('Tp', 0), "s"),
            ("Période moyenne", wave_params.get('Tm', 0), "s"),
            ("Hauteur maximale", wave_params.get('H_max', 0), "m"),
            ("Cambrure", wave_params.get('steepness', 0), "-"),
            ("Direction principale", wave_params.get('direction', 0), "°"),
            ("Étalement directionnel", wave_params.get('spreading', 0), "°"),
            ("Énergie totale", wave_params.get('energy', 0), "J/m²"),
            ("Puissance", wave_params.get('power', 0), "kW/m")
        ]
        
        # Ajouter les statistiques si disponibles
        if statistics:
            params_info.extend([
                ("", "", ""),  # Ligne vide
                ("Moyenne", statistics.get('mean', 0), "m"),
                ("Écart-type", statistics.get('std', 0), "m"),
                ("Minimum", statistics.get('min', 0), "m"),
                ("Maximum", statistics.get('max', 0), "m"),
                ("RMS", statistics.get('rms', 0), "m")
            ])
            
        # Configurer le nombre de lignes
        self.setRowCount(len(params_info))
        
        # Remplir le tableau
        for i, (param, value, unit) in enumerate(params_info):
            self.setItem(i, 0, QTableWidgetItem(str(param)))
            
            if isinstance(value, (int, float)) and value != 0:
                formatted_value = f"{value:.3f}" if isinstance(value, float) else str(value)
            else:
                formatted_value = str(value)
                
            self.setItem(i, 1, QTableWidgetItem(formatted_value))
            self.setItem(i, 2, QTableWidgetItem(str(unit)))
            
        # Redimensionner
        self.resizeRowsToContents()

class EnhancedAnalysisTab(QWidget):
    """Onglet d'analyse amélioré avec graphiques statiques"""
    
    analysisCompleted = pyqtSignal(dict)  # résultats
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.analysis_data = None
        self.analysis_results = None
        self.analysis_worker = None
        self.worker_thread = None
        
        self._init_ui()
        
        # Enregistrer callback thème
        register_theme_callback(self._on_theme_changed)
        
    def _init_ui(self):
        """Initialise l'interface d'analyse"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Titre
        title_label = QLabel("📊 Analyse des Données")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_splitter)
        
        # Panneau de contrôle (gauche)
        control_panel = self._create_control_panel()
        main_splitter.addWidget(control_panel)
        
        # Panneau graphiques (droite)
        plot_panel = self._create_plot_panel()
        main_splitter.addWidget(plot_panel)
        
        # Ratio golden
        main_splitter.setSizes([int(self.width() * 0.3), int(self.width() * 0.7)])
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
    def _create_control_panel(self) -> QWidget:
        """Crée le panneau de contrôle"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Informations sur les données
        info_group = QGroupBox("ℹ️ Informations")
        info_layout = QFormLayout(info_group)
        
        self.data_status_label = QLabel("Aucune donnée")
        info_layout.addRow("Statut:", self.data_status_label)
        
        self.duration_label = QLabel("-")
        info_layout.addRow("Durée:", self.duration_label)
        
        self.samples_label = QLabel("-")
        info_layout.addRow("Échantillons:", self.samples_label)
        
        self.rate_label = QLabel("-")
        info_layout.addRow("Fréquence:", self.rate_label)
        
        layout.addWidget(info_group)
        
        # Contrôles d'analyse
        analysis_group = QGroupBox("🔬 Analyse")
        analysis_layout = QVBoxLayout(analysis_group)
        
        # Boutons d'analyse
        self.analyze_btn = QPushButton("🚀 Analyser")
        self.analyze_btn.setObjectName("analyzeButton")
        self.analyze_btn.clicked.connect(self._start_analysis)
        self.analyze_btn.setEnabled(False)
        analysis_layout.addWidget(self.analyze_btn)
        
        self.clear_btn = QPushButton("🗑 Effacer")
        self.clear_btn.clicked.connect(self._clear_analysis)
        analysis_layout.addWidget(self.clear_btn)
        
        # Options d'analyse
        options_layout = QVBoxLayout()
        
        self.spectral_check = QCheckBox("Analyse spectrale")
        self.spectral_check.setChecked(True)
        options_layout.addWidget(self.spectral_check)
        
        self.waves_check = QCheckBox("Détection de vagues")
        self.waves_check.setChecked(True)
        options_layout.addWidget(self.waves_check)
        
        self.direction_check = QCheckBox("Analyse directionnelle")
        self.direction_check.setChecked(True)
        options_layout.addWidget(self.direction_check)
        
        analysis_layout.addLayout(options_layout)
        
        layout.addWidget(analysis_group)
        
        # Tableau des paramètres
        params_group = QGroupBox("📋 Paramètres")
        params_layout = QVBoxLayout(params_group)
        
        self.params_table = ParametersTable()
        params_layout.addWidget(self.params_table)
        
        layout.addWidget(params_group)
        
        # Export
        export_group = QGroupBox("💾 Export")
        export_layout = QVBoxLayout(export_group)
        
        self.export_csv_btn = QPushButton("📄 Export CSV")
        self.export_csv_btn.clicked.connect(self._export_csv)
        self.export_csv_btn.setEnabled(False)
        export_layout.addWidget(self.export_csv_btn)
        
        self.export_json_btn = QPushButton("📋 Export JSON")
        self.export_json_btn.clicked.connect(self._export_json)
        self.export_json_btn.setEnabled(False)
        export_layout.addWidget(self.export_json_btn)
        
        self.export_plots_btn = QPushButton("🖼 Export Graphiques")
        self.export_plots_btn.clicked.connect(self._export_plots)
        self.export_plots_btn.setEnabled(False)
        export_layout.addWidget(self.export_plots_btn)
        
        layout.addWidget(export_group)
        
        layout.addStretch()
        return panel
        
    def _create_plot_panel(self) -> QWidget:
        """Crée le panneau de graphiques"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Widget de graphiques statiques
        self.plot_widget = StaticPlotWidget()
        layout.addWidget(self.plot_widget)
        
        return panel
        
    def load_acquisition_data(self, data: Dict[str, Any]):
        """Charge les données d'acquisition pour analyse"""
        self.analysis_data = data
        
        # Mettre à jour les informations
        self.data_status_label.setText("Données chargées")
        self.data_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        
        duration = data.get('duration', 0)
        self.duration_label.setText(f"{duration:.1f} s")
        
        sample_count = data.get('samples', 0)
        self.samples_label.setText(str(sample_count))
        
        sample_rate = data.get('sample_rate', 0)
        self.rate_label.setText(f"{sample_rate:.1f} Hz")
        
        # Activer l'analyse
        self.analyze_btn.setEnabled(True)
        
    def _start_analysis(self):
        """Démarre l'analyse des données"""
        if not self.analysis_data:
            QMessageBox.warning(self, "Analyse", "Aucune donnée à analyser.")
            return
            
        try:
            # Simuler des données de série temporelle si pas présentes
            if 'time_series' not in self.analysis_data and NUMPY_AVAILABLE:
                # Générer une série temporelle simulée
                duration = self.analysis_data.get('duration', 60)
                sample_rate = self.analysis_data.get('sample_rate', 32)
                n_samples = int(duration * sample_rate)
                
                # Simulation d'une houle
                t = np.linspace(0, duration, n_samples)
                signal = (0.5 * np.sin(0.2 * 2 * np.pi * t) + 
                         0.3 * np.sin(0.15 * 2 * np.pi * t) + 
                         0.1 * np.random.randn(n_samples))
                         
                self.analysis_data['time_series'] = signal.tolist()
                
            # Créer le worker d'analyse
            self.analysis_worker = AnalysisWorker(self.analysis_data)
            self.worker_thread = QThread()
            self.analysis_worker.moveToThread(self.worker_thread)
            
            # Connecter les signaux
            self.analysis_worker.analysisProgress.connect(self.progress_bar.setValue)
            self.analysis_worker.analysisFinished.connect(self._on_analysis_finished)
            self.analysis_worker.errorOccurred.connect(self._on_analysis_error)
            
            # Démarrer l'analyse
            self.worker_thread.started.connect(self.analysis_worker.analyze_data)
            
            # Mettre à jour l'interface
            self.analyze_btn.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.worker_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de démarrer l'analyse: {e}")
            
    @pyqtSlot(dict)
    def _on_analysis_finished(self, results: dict):
        """Gère la fin d'analyse"""
        self.analysis_results = results
        
        # Mettre à jour l'interface
        self.analyze_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Nettoyer le thread
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            
        # Mettre à jour les graphiques
        plot_data = {
            'time_series': self.analysis_data.get('time_series', []),
            'spectrum': results.get('spectrum', {}),
            'wave_analysis': results.get('wave_analysis', {}),
            'wave_parameters': results.get('wave_parameters', {})
        }
        
        self.plot_widget.update_plots(plot_data)
        
        # Mettre à jour le tableau des paramètres
        wave_params = results.get('wave_parameters', {})
        statistics = results.get('statistics', {})
        self.params_table.update_parameters(wave_params, statistics)
        
        # Activer l'export
        self.export_csv_btn.setEnabled(True)
        self.export_json_btn.setEnabled(True)
        self.export_plots_btn.setEnabled(True)
        
        # Émettre le signal
        self.analysisCompleted.emit(results)
        
        # Message de succès
        QMessageBox.information(self, "Analyse", "Analyse terminée avec succès!")
        
    @pyqtSlot(str)
    def _on_analysis_error(self, error_msg: str):
        """Gère les erreurs d'analyse"""
        self.analyze_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            
        QMessageBox.critical(self, "Erreur d'analyse", error_msg)
        
    def _clear_analysis(self):
        """Efface l'analyse"""
        self.analysis_results = None
        self.plot_widget.clear_plots()
        self.params_table.setRowCount(0)
        
        # Désactiver l'export
        self.export_csv_btn.setEnabled(False)
        self.export_json_btn.setEnabled(False)
        self.export_plots_btn.setEnabled(False)
        
    def _export_csv(self):
        """Exporte les résultats en CSV"""
        if not self.analysis_results:
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter CSV", "analysis_results.csv", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                # TODO: Implémenter l'export CSV
                QMessageBox.information(self, "Export", f"Export CSV vers {filename} (à implémenter)")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur export CSV: {e}")
                
    def _export_json(self):
        """Exporte les résultats en JSON"""
        if not self.analysis_results:
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter JSON", "analysis_results.json", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Export", f"Export JSON réussi: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur export JSON: {e}")
                
    def _export_plots(self):
        """Exporte les graphiques"""
        # TODO: Implémenter l'export des graphiques
        QMessageBox.information(self, "Export", "Export graphiques à implémenter")
        
    def _on_theme_changed(self, theme_name: str):
        """Callback pour changement de thème"""
        # Mettre à jour les couleurs des graphiques
        pass
        
    def has_data(self) -> bool:
        """Vérifie si des données sont chargées"""
        return self.analysis_data is not None
        
    def has_results(self) -> bool:
        """Vérifie si des résultats d'analyse sont disponibles"""
        return self.analysis_results is not None
        
    def get_analysis_results(self) -> Optional[Dict[str, Any]]:
        """Retourne les résultats d'analyse"""
        return self.analysis_results
        
    def cleanup(self):
        """Nettoie les ressources"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()