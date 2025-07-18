# modern_acquisition_ui.py - Interface d'acquisition modernisée avec PyQtGraph
import sys
import os
import json
import csv
import time
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
    QFileDialog, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox, QFrame, QScrollArea, QCheckBox,
    QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QDialogButtonBox, QTabWidget, QProgressBar, QSplitter, QTextEdit, QGridLayout,
    QSizePolicy, QDockWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, pyqtSignal, QThread, QEvent
from PyQt5.QtGui import QPalette, QColor, QFont

import pyqtgraph as pg
from pyqtgraph import PlotWidget, mkPen, mkBrush

# Import des modules optimisés
try:
    from optimized_processing_worker import OptimizedProcessingWorker
except ImportError:
    print("⚠️ OptimizedProcessingWorker non disponible, fonctionnalités limitées")
    OptimizedProcessingWorker = None

try:
    from acquisition_controller import AcquisitionController
except ImportError:
    print("⚠️ AcquisitionController non disponible")
    AcquisitionController = None

class SimpleConfig:
    """Configuration simple avec méthode get compatible dictionnaire"""
    def __init__(self, config_dict=None):
        if config_dict:
            for key, value in config_dict.items():
                setattr(self, key, value)
    
    def get(self, key, default=None):
        """Méthode get compatible avec les dictionnaires"""
        return getattr(self, key, default)

class ModernAcquisitionUI(QMainWindow):
    """Interface d'acquisition modernisée avec PyQtGraph et modules optimisés
    
    Fonctionnalités:
    - Graphiques temps réel haute performance avec PyQtGraph
    - Contrôles Start/Stop/Export intuitifs
    - Métriques de performance en temps réel
    - Interface responsive et moderne
    - Intégration complète avec les modules optimisés
    """
    
    # Signaux pour la communication
    acquisitionStarted = pyqtSignal()
    acquisitionStopped = pyqtSignal()
    dataExported = pyqtSignal(str)  # Chemin du fichier exporté
    
    def __init__(self, config: Dict[str, Any], acquisition_controller: Optional[AcquisitionController] = None):
        super().__init__()
        self.config = config
        self.acquisition_controller = acquisition_controller
        
        # Constante du nombre d'or pour les proportions
        self.GOLDEN_RATIO = 1.618
        
        # Configuration par défaut
        self.n_sondes = config.get('n_channels', 4)
        self.sample_rate = config.get('sample_rate', 32.0)
        self.duration = config.get('duration', 300)  # 5 minutes par défaut
        self.save_folder = config.get('save_folder', './data')
        
        # État de l'acquisition
        self.is_acquiring = False
        self.start_time = None
        self.total_samples = 0
        
        # Données pour l'export
        self.time_data = []
        self.probe_data = [[] for _ in range(self.n_sondes)]
        self.spectral_data = {}
        self.goda_results = []
        
        # Worker de traitement optimisé
        self.processing_worker = None
        
        # Timers
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_displays)
        
        # Initialisation de l'interface
        self._init_ui()
        self._setup_pyqtgraph()
        self._init_processing_worker()
        
        # Configuration du thème par défaut
        self._apply_modern_theme()
        
        # Configuration de la validation des champs
        self._setup_field_validation()
        
    def _init_ui(self):
        """Initialise l'interface utilisateur moderne avec layout responsive basé sur le nombre d'or"""
        self.setWindowTitle("HRNeoWave - Acquisition Temps Réel Optimisée")
        
        # Dimensions basées sur le nombre d'or pour une harmonie visuelle
        base_width = 1280
        base_height = int(base_width / self.GOLDEN_RATIO)  # ~791px
        
        # Taille minimale pour assurer la visibilité complète sans barres de scroll
        min_width = 1280
        min_height = 720
        
        # Configuration des dimensions - SUPPRESSION des tailles fixes
        self.resize(base_width, base_height)
        self.setMinimumSize(min_width, min_height)
        
        # Support mode plein écran F11
        self.installEventFilter(self)
        
        # Créer le layout responsive
        self._create_responsive_layout()
        
    def _create_responsive_layout(self):
        """Crée un layout responsive basé sur le nombre d'or avec QSplitter"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal sans marges fixes
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(0)
        
        # QSplitter horizontal principal (contrôles : 0.38, graphiques : 0.62)
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(2)
        self.main_splitter.setChildrenCollapsible(False)
        
        # Panneau de contrôle (38% selon nombre d'or)
        control_panel = self._create_control_panel()
        control_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Zone graphiques avec QSplitter vertical interne (62% selon nombre d'or)
        graphics_area = self._create_visualization_panel()
        graphics_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.main_splitter.addWidget(control_panel)
        self.main_splitter.addWidget(graphics_area)
        
        # Proportions golden ratio: 38% / 62%
        self.main_splitter.setStretchFactor(0, 38)
        self.main_splitter.setStretchFactor(1, 62)
        
        # Tailles initiales basées sur 1280px de largeur
        self.main_splitter.setSizes([487, 793])  # 38% et 62% de 1280px
        
        main_layout.addWidget(self.main_splitter)
        
        # Créer QDockWidget pour remplacer la bande rouge vide
        self._create_status_dock()
    
    def _create_status_dock(self):
        """Crée un QDockWidget pour remplacer la bande vide latérale"""
        self.status_dock = QDockWidget("État du Système", self)
        self.status_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        
        # Widget de contenu du dock
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(8, 8, 8, 8)
        
        # Informations système
        system_group = QGroupBox("Système")
        system_layout = QFormLayout(system_group)
        
        self.system_fps_label = QLabel("-- FPS")
        self.system_latency_label = QLabel("-- ms")
        self.system_memory_label = QLabel("-- MB")
        
        system_layout.addRow("FPS:", self.system_fps_label)
        system_layout.addRow("Latence:", self.system_latency_label)
        system_layout.addRow("Mémoire:", self.system_memory_label)
        
        status_layout.addWidget(system_group)
        status_layout.addStretch()
        
        self.status_dock.setWidget(status_widget)
        self.status_dock.setMinimumWidth(200)
        self.status_dock.setMaximumWidth(300)
        
        # Masquer par défaut pour éviter la bande vide
        self.status_dock.hide()
        self.addDockWidget(Qt.RightDockWidgetArea, self.status_dock)
    
    def eventFilter(self, obj, event):
        """Filtre les événements pour gérer F11 (mode plein écran)"""
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
            return True
        return super().eventFilter(obj, event)
    
    def resizeEvent(self, event):
        """Gère le redimensionnement en maintenant les proportions dorées"""
        super().resizeEvent(event)
        if hasattr(self, 'main_splitter') and self.main_splitter:
            # Maintenir les proportions 38% / 62%
            total_width = self.width() - 8  # Marges
            if total_width > 0:
                control_width = int(total_width * 0.38)
                graphics_width = int(total_width * 0.62)
                self.main_splitter.setSizes([control_width, graphics_width])
        
    def _setup_field_validation(self):
        """Configure la validation des champs"""
        # Validation durée (1-3600 secondes)
        self.duration_spinbox.valueChanged.connect(self._validate_duration)
        
        # Validation fréquence (0.1-1000 Hz)
        self.sample_rate_spinbox.valueChanged.connect(self._validate_sample_rate)
        
        # Validation nombre de sondes (1-16)
        self.n_sondes_spinbox.valueChanged.connect(self._validate_probes)
    
    def _validate_duration(self, value):
        """Valide la durée d'acquisition"""
        if value < 1 or value > 3600:
            self.duration_spinbox.setStyleSheet("border: 2px solid red;")
            return False
        self.duration_spinbox.setStyleSheet("")
        return True
    
    def _validate_sample_rate(self, value):
        """Valide la fréquence d'échantillonnage"""
        if value < 0.1 or value > 1000.0:
            self.sample_rate_spinbox.setStyleSheet("border: 2px solid red;")
            return False
        self.sample_rate_spinbox.setStyleSheet("")
        return True
    
    def _validate_probes(self, value):
        """Valide le nombre de sondes"""
        if value < 1 or value > 16:
            self.n_sondes_spinbox.setStyleSheet("border: 2px solid red;")
            return False
        self.n_sondes_spinbox.setStyleSheet("")
        return True
        
    def _create_control_panel(self) -> QWidget:
        """Crée le panneau de contrôle responsive"""
        panel = QWidget()
        panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # ScrollArea pour éviter le débordement vertical
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget de contenu
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        # Titre
        title = QLabel("Contrôle d'Acquisition")
        title.setObjectName("panelTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Contrôles de configuration
        config_group = self._create_config_controls()
        layout.addWidget(config_group)
        
        # Contrôles principaux
        controls_group = self._create_main_controls()
        layout.addWidget(controls_group)
        
        # Informations de session
        session_group = self._create_session_info()
        layout.addWidget(session_group)
        
        # Métriques de performance
        performance_group = self._create_performance_metrics()
        layout.addWidget(performance_group)
        
        # Configuration des sondes (compacte)
        probe_group = self._create_probe_config_compact()
        layout.addWidget(probe_group)
        
        # Contrôles d'export
        export_group = self._create_export_controls()
        layout.addWidget(export_group)
        
        # Log des événements compact
        event_log = self._create_event_log_compact()
        layout.addWidget(event_log)
        
        layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        
        # Layout principal du panel
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.addWidget(scroll_area)
        
        return panel
        
    def _create_main_controls(self) -> QGroupBox:
        """Crée les contrôles principaux Start/Stop"""
        group = QGroupBox("Contrôles Principaux")
        layout = QVBoxLayout(group)
        
        # Boutons Start/Stop
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("🚀 Démarrer")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self._start_acquisition)
        
        self.stop_button = QPushButton("⏹️ Arrêter")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self._stop_acquisition)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # Bouton Paramètres Avancés
        settings_layout = QHBoxLayout()
        self.settings_button = QPushButton("⚙️ Paramètres Avancés")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.clicked.connect(self._open_advanced_settings)
        settings_layout.addWidget(self.settings_button)
        layout.addLayout(settings_layout)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        # Statut
        self.status_label = QLabel("Prêt à démarrer")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        return group
        
    def _create_config_controls(self) -> QGroupBox:
        """Crée les contrôles de configuration"""
        group = QGroupBox("Configuration d'Acquisition")
        layout = QFormLayout(group)
        
        # Durée d'acquisition
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 3600)
        self.duration_spinbox.setValue(self.config.get('duration', 300))
        self.duration_spinbox.setSuffix(" s")
        layout.addRow("Durée:", self.duration_spinbox)
        
        # Fréquence d'échantillonnage
        self.sample_rate_spinbox = QDoubleSpinBox()
        self.sample_rate_spinbox.setRange(0.1, 1000.0)
        self.sample_rate_spinbox.setValue(self.config.get('sample_rate', 32.0))
        self.sample_rate_spinbox.setSuffix(" Hz")
        self.sample_rate_spinbox.setDecimals(1)
        layout.addRow("Fréquence:", self.sample_rate_spinbox)
        
        # Nombre de sondes
        self.n_sondes_spinbox = QSpinBox()
        self.n_sondes_spinbox.setRange(1, 16)
        self.n_sondes_spinbox.setValue(self.config.get('n_channels', 4))
        layout.addRow("Nb Sondes:", self.n_sondes_spinbox)
        
        return group
        
    def _create_session_info(self) -> QGroupBox:
        """Crée le groupe d'informations de session"""
        group = QGroupBox("Informations de Session")
        layout = QFormLayout(group)
        
        self.duration_label = QLabel("00:00 / 05:00")
        self.samples_label = QLabel("0 / 9600")
        self.frequency_label = QLabel(f"{self.sample_rate} Hz")
        self.probes_label = QLabel(f"{self.n_sondes} sondes")
        
        layout.addRow("Durée:", self.duration_label)
        layout.addRow("Échantillons:", self.samples_label)
        layout.addRow("Fréquence:", self.frequency_label)
        layout.addRow("Sondes:", self.probes_label)
        
        return group
        
    def _create_performance_metrics(self) -> QGroupBox:
        """Crée le groupe de métriques de performance"""
        group = QGroupBox("Performance Temps Réel")
        layout = QFormLayout(group)
        
        self.fft_time_label = QLabel("-- ms")
        self.goda_time_label = QLabel("-- ms")
        self.total_time_label = QLabel("-- ms")
        self.throughput_label = QLabel("-- sps")
        self.cache_hits_label = QLabel("--")
        
        layout.addRow("FFT:", self.fft_time_label)
        layout.addRow("Goda:", self.goda_time_label)
        layout.addRow("Total:", self.total_time_label)
        layout.addRow("Débit:", self.throughput_label)
        layout.addRow("Cache:", self.cache_hits_label)
        
        return group
        

        
    def _create_export_controls(self) -> QGroupBox:
        """Crée les contrôles d'export"""
        group = QGroupBox("Export des Données")
        layout = QVBoxLayout(group)
        
        # Sélection du format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        
        self.export_format = QComboBox()
        self.export_format.addItems(["CSV", "JSON", "MAT", "HDF5"])
        format_layout.addWidget(self.export_format)
        layout.addLayout(format_layout)
        
        # Options d'export
        self.export_raw_data = QCheckBox("Données brutes")
        self.export_raw_data.setChecked(True)
        
        self.export_spectra = QCheckBox("Spectres FFT")
        self.export_spectra.setChecked(True)
        
        self.export_goda = QCheckBox("Résultats Goda")
        self.export_goda.setChecked(True)
        
        layout.addWidget(self.export_raw_data)
        layout.addWidget(self.export_spectra)
        layout.addWidget(self.export_goda)
        
        # Bouton d'export
        self.export_button = QPushButton("💾 Exporter Données")
        self.export_button.clicked.connect(self._export_data)
        self.export_button.setEnabled(False)
        layout.addWidget(self.export_button)
        
        return group
        
    def _create_event_log_compact(self) -> QGroupBox:
        """Crée un log des événements compact"""
        group = QGroupBox("Log")
        layout = QVBoxLayout(group)
        layout.setSpacing(2)
        
        self.event_log = QTextEdit()
        self.event_log.setMaximumHeight(80)
        self.event_log.setReadOnly(True)
        self.event_log.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                font-size: 9px;
                font-family: 'Consolas', monospace;
            }
        """)
        layout.addWidget(self.event_log)
        
        # Bouton compact pour effacer
        clear_button = QPushButton("🗑️")
        clear_button.setMaximumWidth(30)
        clear_button.setMaximumHeight(25)
        clear_button.clicked.connect(self.event_log.clear)
        layout.addWidget(clear_button)
        
        return group
        
    def _create_probe_config_compact(self) -> QGroupBox:
        """Crée une configuration compacte des sondes"""
        group = QGroupBox("Sondes")
        layout = QVBoxLayout(group)
        layout.setSpacing(4)
        
        # Nombre de sondes actives
        active_layout = QHBoxLayout()
        active_layout.addWidget(QLabel("Actives:"))
        
        self.active_probes_label = QLabel(f"{self.n_sondes}/{self.n_sondes}")
        self.active_probes_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        active_layout.addWidget(self.active_probes_label)
        active_layout.addStretch()
        
        # Bouton de configuration rapide
        config_button = QPushButton("⚙️")
        config_button.setMaximumWidth(30)
        config_button.clicked.connect(self._configure_probe_positions)
        active_layout.addWidget(config_button)
        
        layout.addLayout(active_layout)
        
        # Indicateurs visuels des sondes
        indicators_layout = QHBoxLayout()
        self.probe_indicators = []
        
        for i in range(min(4, self.n_sondes)):
            indicator = QLabel("●")
            indicator.setStyleSheet("color: #4CAF50; font-size: 16px;")
            indicator.setAlignment(Qt.AlignCenter)
            self.probe_indicators.append(indicator)
            indicators_layout.addWidget(indicator)
            
        layout.addLayout(indicators_layout)
        return group
        
    def _create_visualization_panel(self) -> QWidget:
        """Crée le panneau de visualisation avec QSplitter vertical (3 graphiques)"""
        panel = QWidget()
        panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout principal
        main_layout = QVBoxLayout(panel)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(0)
        
        # QSplitter vertical pour 3 graphiques (proportions: 0.33 / 0.33 / 0.34)
        self.graphics_splitter = QSplitter(Qt.Vertical)
        self.graphics_splitter.setHandleWidth(2)
        self.graphics_splitter.setChildrenCollapsible(False)
        
        # Graphique 1: Signaux temporels (33%)
        time_widget = self._create_time_signals_widget()
        time_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Graphique 2: Spectres FFT (33%)
        spectrum_widget = self._create_spectrum_widget()
        spectrum_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Graphique 3: Analyse Goda + Métriques (34%)
        goda_widget = self._create_goda_metrics_widget()
        goda_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.graphics_splitter.addWidget(time_widget)
        self.graphics_splitter.addWidget(spectrum_widget)
        self.graphics_splitter.addWidget(goda_widget)
        
        # Proportions: 33% / 33% / 34%
        self.graphics_splitter.setStretchFactor(0, 33)
        self.graphics_splitter.setStretchFactor(1, 33)
        self.graphics_splitter.setStretchFactor(2, 34)
        
        # Tailles initiales pour 720px de hauteur
        self.graphics_splitter.setSizes([238, 238, 244])  # 33%, 33%, 34% de 720px
        
        main_layout.addWidget(self.graphics_splitter)
        return panel
        
    def _create_time_signals_widget(self) -> QWidget:
        """Crée le widget des signaux temporels"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # Titre compact
        title_label = QLabel("📈 Signaux Temporels")
        title_label.setStyleSheet("font-weight: bold; color: #4CAF50; font-size: 12px;")
        title_label.setMaximumHeight(20)
        layout.addWidget(title_label)
        
        # Graphique principal
        self.time_plot = PlotWidget()
        self.time_plot.setLabel('left', 'Amplitude', units='m')
        self.time_plot.setLabel('bottom', 'Temps', units='s')
        self.time_plot.showGrid(x=True, y=True)
        self.time_plot.setBackground('#2b2b2b')
        
        # Courbes pour chaque sonde
        self.time_curves = []
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
        
        for i in range(self.n_sondes):
            color = colors[i % len(colors)]
            curve = self.time_plot.plot(pen=mkPen(color, width=2), name=f'Sonde {i+1}')
            self.time_curves.append(curve)
            
        layout.addWidget(self.time_plot)
        return widget
        
    def _create_spectrum_widget(self) -> QWidget:
        """Crée le widget des spectres FFT"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # Titre compact
        title_label = QLabel("🌊 Spectres FFT")
        title_label.setStyleSheet("font-weight: bold; color: #2196F3; font-size: 12px;")
        title_label.setMaximumHeight(20)
        layout.addWidget(title_label)
        
        # Graphique principal
        self.spectrum_plot = PlotWidget()
        self.spectrum_plot.setLabel('left', 'PSD', units='m²/Hz')
        self.spectrum_plot.setLabel('bottom', 'Fréquence', units='Hz')
        self.spectrum_plot.setLogMode(y=True)
        self.spectrum_plot.showGrid(x=True, y=True)
        self.spectrum_plot.setBackground('#2b2b2b')
        
        # Courbes spectrales
        self.spectrum_curves = []
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
        
        for i in range(self.n_sondes):
            color = colors[i % len(colors)]
            curve = self.spectrum_plot.plot(pen=mkPen(color, width=2), name=f'Sonde {i+1}')
            self.spectrum_curves.append(curve)
            
        layout.addWidget(self.spectrum_plot)
        
        # Informations spectrales compactes
        info_layout = QHBoxLayout()
        self.peak_freq_label = QLabel("Pic: -- Hz")
        self.total_energy_label = QLabel("Énergie: -- m²")
        
        for label in [self.peak_freq_label, self.total_energy_label]:
            label.setStyleSheet("color: #2196F3; font-size: 10px; font-weight: bold;")
            label.setMaximumHeight(16)
        
        info_layout.addWidget(self.peak_freq_label)
        info_layout.addWidget(self.total_energy_label)
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
        return widget
        
    def _create_goda_metrics_widget(self) -> QWidget:
        """Crée le widget combiné Goda + Métriques"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # Titre compact
        title_label = QLabel("🔬 Analyse Goda & Métriques")
        title_label.setStyleSheet("font-weight: bold; color: #FF9800; font-size: 12px;")
        title_label.setMaximumHeight(20)
        layout.addWidget(title_label)
        
        # Splitter horizontal pour graphique + stats
        h_splitter = QSplitter(Qt.Horizontal)
        
        # Graphique Goda (70%)
        goda_widget = QWidget()
        goda_layout = QVBoxLayout(goda_widget)
        goda_layout.setContentsMargins(0, 0, 0, 0)
        
        self.hs_plot = PlotWidget()
        self.hs_plot.setLabel('left', 'Hs', units='m')
        self.hs_plot.setLabel('bottom', 'Temps', units='s')
        self.hs_plot.showGrid(x=True, y=True)
        self.hs_plot.setBackground('#2b2b2b')
        self.hs_curve = self.hs_plot.plot(pen=mkPen('#ff6b6b', width=2))
        goda_layout.addWidget(self.hs_plot)
        
        # Panneau de statistiques (30%)
        stats_widget = self._create_compact_stats_panel()
        
        h_splitter.addWidget(goda_widget)
        h_splitter.addWidget(stats_widget)
        h_splitter.setStretchFactor(0, 70)
        h_splitter.setStretchFactor(1, 30)
        
        layout.addWidget(h_splitter)
        return widget
        
    def _create_compact_stats_panel(self) -> QWidget:
        """Crée un panneau de statistiques compact"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Statistiques Goda
        goda_group = QGroupBox("Goda")
        goda_layout = QFormLayout(goda_group)
        goda_layout.setSpacing(2)
        
        self.current_hs_label = QLabel("-- m")
        self.current_tp_label = QLabel("-- s")
        self.current_cr_label = QLabel("--")
        
        for label in [self.current_hs_label, self.current_tp_label, self.current_cr_label]:
            label.setStyleSheet("color: #4ecdc4; font-weight: bold; font-size: 10px;")
        
        goda_layout.addRow("Hs:", self.current_hs_label)
        goda_layout.addRow("Tp:", self.current_tp_label)
        goda_layout.addRow("Cr:", self.current_cr_label)
        
        # Métriques de performance
        perf_group = QGroupBox("Performance")
        perf_layout = QFormLayout(perf_group)
        perf_layout.setSpacing(2)
        
        # Créer des labels uniques pour éviter les conflits
        self.compact_fps_label = QLabel("-- FPS")
        self.compact_latency_label = QLabel("-- ms")
        self.compact_memory_label = QLabel("-- MB")
        
        for label in [self.compact_fps_label, self.compact_latency_label, self.compact_memory_label]:
            label.setStyleSheet("color: #45b7d1; font-weight: bold; font-size: 10px;")
        
        perf_layout.addRow("FPS:", self.compact_fps_label)
        perf_layout.addRow("Latence:", self.compact_latency_label)
        perf_layout.addRow("Mémoire:", self.compact_memory_label)
        
        # Assigner aux attributs principaux pour compatibilité
        self.fps_label = self.compact_fps_label
        self.latency_label = self.compact_latency_label
        self.memory_label = self.compact_memory_label
        
        layout.addWidget(goda_group)
        layout.addWidget(perf_group)
        layout.addStretch()
        
        return widget
        

        
    def _setup_pyqtgraph(self):
        """Configure PyQtGraph pour de meilleures performances"""
        # Configuration globale de PyQtGraph
        pg.setConfigOptions(
            antialias=True,
            useOpenGL=True,  # Accélération GPU si disponible
            enableExperimental=True
        )
        
        # Thème sombre pour PyQtGraph
        pg.setConfigOption('background', '#2b2b2b')
        pg.setConfigOption('foreground', '#ffffff')
        
    def _init_processing_worker(self):
        """Initialise le worker de traitement optimisé"""
        try:
            worker_config = {
                'sample_rate': self.sample_rate,
                'n_channels': self.n_sondes,
                'window_size': 1024,
                'update_interval': 50,
                'buffer_size': 4096,
                'water_depth': 10.0,
                'probe_positions': [0.5 + i*0.3 for i in range(self.n_sondes)]
            }
            
            # Créer un objet de configuration simple
            config_obj = SimpleConfig(worker_config)
            
            self.processing_worker = OptimizedProcessingWorker(
                self, 
                config_obj
            )
            
            # Connexion des signaux
            self.processing_worker.newSpectra.connect(self._update_spectra)
            self.processing_worker.newStats.connect(self._update_goda_stats)
            self.processing_worker.performanceStats.connect(self._update_performance_stats)
            self.processing_worker.processingError.connect(self._handle_processing_error)
            
        except Exception as e:
            print(f"⚠️ Erreur initialisation worker: {e}")
            self.processing_worker = None
            
    def _apply_modern_theme(self):
        """Applique le thème moderne"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
            }
            
            QLabel#panelTitle {
                font-size: 18px;
                font-weight: bold;
                color: #00bfff;
                padding: 10px;
                border-bottom: 2px solid #00bfff;
                margin-bottom: 10px;
            }
            
            QGroupBox {
                font-weight: bold;
                color: #00bfff;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00bfff, stop:1 #005fa3);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #005fa3, stop:1 #00bfff);
            }
            
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
            
            QPushButton#startButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #4CAF50, stop:1 #45a049);
            }
            
            QPushButton#stopButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #f44336, stop:1 #da190b);
            }
            
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 5px;
                text-align: center;
                background-color: #1e1e1e;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00bfff, stop:1 #005fa3);
                border-radius: 3px;
            }
            
            QLabel#statusLabel {
                font-weight: bold;
                color: #4CAF50;
                padding: 5px;
            }
            
            QTableWidget {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 4px;
                gridline-color: #404040;
            }
            
            QHeaderView::section {
                background-color: #404040;
                color: #00bfff;
                font-weight: bold;
                padding: 4px;
                border: none;
            }
            
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 4px;
                color: #ffffff;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
            
            QTabWidget::pane {
                border: 1px solid #404040;
                background-color: #2b2b2b;
            }
            
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #00bfff;
                color: #ffffff;
            }
            
            QComboBox {
                background-color: #404040;
                border: 1px solid #606060;
                border-radius: 4px;
                padding: 4px 8px;
                color: #ffffff;
            }
            
            QCheckBox {
                color: #ffffff;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #606060;
                border-radius: 3px;
                background-color: #2b2b2b;
            }
            
            QCheckBox::indicator:checked {
                background-color: #00bfff;
                border-color: #00bfff;
            }
            
            QSpinBox, QDoubleSpinBox {
                background-color: #404040;
                border: 1px solid #606060;
                border-radius: 4px;
                padding: 4px 8px;
                color: #ffffff;
                min-height: 20px;
            }
            
            QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #00bfff;
            }
            
            QSpinBox::up-button, QDoubleSpinBox::up-button {
                background-color: #606060;
                border: none;
                border-radius: 2px;
                width: 16px;
            }
            
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background-color: #606060;
                border: none;
                border-radius: 2px;
                width: 16px;
            }
            
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #00bfff;
            }
        """)
        
    def _log_event(self, message: str):
        """Ajoute un événement au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.event_log.append(f"[{timestamp}] {message}")
        
    def _start_acquisition(self):
        """Démarre l'acquisition"""
        try:
            if not self.acquisition_controller:
                self._log_event("❌ Erreur: Contrôleur d'acquisition non disponible")
                return
                
            # Démarrer l'acquisition
            self.acquisition_controller.start_acquisition()
            
            # Démarrer le worker de traitement
            if self.processing_worker:
                self.processing_worker.start_processing()
                
            # Démarrer les timers
            self.update_timer.start(50)  # 20 FPS
            
            # Mettre à jour l'interface
            self.is_acquiring = True
            self.start_time = datetime.now()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.export_button.setEnabled(False)
            
            self.status_label.setText("🔴 Acquisition en cours...")
            self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
            
            self._log_event("🚀 Acquisition démarrée")
            self.acquisitionStarted.emit()
            
        except Exception as e:
            self._log_event(f"❌ Erreur démarrage: {str(e)}")
            QMessageBox.critical(self, "Erreur", f"Impossible de démarrer l'acquisition:\n{str(e)}")
            
    def _stop_acquisition(self):
        """Arrête l'acquisition"""
        try:
            # Arrêter l'acquisition
            if self.acquisition_controller:
                self.acquisition_controller.stop_acquisition()
                
            # Arrêter le worker de traitement
            if self.processing_worker:
                self.processing_worker.stop_processing()
                
            # Arrêter les timers
            self.update_timer.stop()
            
            # Mettre à jour l'interface
            self.is_acquiring = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.export_button.setEnabled(True)
            
            self.status_label.setText("⏹️ Acquisition arrêtée")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            
            self._log_event("⏹️ Acquisition arrêtée")
            self.acquisitionStopped.emit()
            
        except Exception as e:
            self._log_event(f"❌ Erreur arrêt: {str(e)}")
            
    def _update_displays(self):
        """Met à jour tous les affichages"""
        if not self.is_acquiring:
            return
            
        try:
            # Mettre à jour la durée
            if self.start_time:
                elapsed = datetime.now() - self.start_time
                elapsed_str = str(elapsed).split('.')[0]  # Enlever les microsecondes
                total_str = f"{self.duration//60:02d}:{self.duration%60:02d}"
                self.duration_label.setText(f"{elapsed_str} / {total_str}")
                
                # Mettre à jour la barre de progression
                progress = min(100, (elapsed.total_seconds() / self.duration) * 100)
                self.progress_bar.setValue(int(progress))
                
            # Mettre à jour le compteur d'échantillons
            max_samples = int(self.duration * self.sample_rate)
            self.samples_label.setText(f"{self.total_samples} / {max_samples}")
            
        except Exception as e:
            self._log_event(f"❌ Erreur mise à jour affichage: {str(e)}")
            
    @pyqtSlot(dict)
    def _update_spectra(self, spectra_data: Dict[str, Any]):
        """Met à jour les spectres"""
        try:
            for i, (probe_id, data) in enumerate(spectra_data.items()):
                if i < len(self.spectrum_curves):
                    freqs = data.get('freqs', [])
                    psd = data.get('psd', [])
                    
                    if len(freqs) > 0 and len(psd) > 0:
                        self.spectrum_curves[i].setData(freqs, psd)
                        
            # Mettre à jour les informations spectrales
            if spectra_data:
                first_probe = list(spectra_data.values())[0]
                freqs = first_probe.get('freqs', [])
                psd = first_probe.get('psd', [])
                
                if len(freqs) > 0 and len(psd) > 0:
                    peak_idx = np.argmax(psd)
                    peak_freq = freqs[peak_idx]
                    total_energy = np.trapz(psd, freqs)
                    
                    self.peak_freq_label.setText(f"Pic: {peak_freq:.3f} Hz")
                    self.total_energy_label.setText(f"Énergie: {total_energy:.6f} m²")
                    
        except Exception as e:
            self._log_event(f"❌ Erreur mise à jour spectres: {str(e)}")
            
    @pyqtSlot(dict)
    def _update_goda_stats(self, stats_data: Dict[str, Any]):
        """Met à jour les statistiques Goda"""
        try:
            # Mettre à jour les labels actuels
            hs = stats_data.get('Hs', 0)
            tp = stats_data.get('Tp', 0)
            cr = stats_data.get('Cr', 0)
            direction = stats_data.get('direction', 0)
            
            self.current_hs_label.setText(f"{hs:.3f} m")
            self.current_tp_label.setText(f"{tp:.2f} s")
            self.current_cr_label.setText(f"{cr:.3f}")
            
            # Ajouter aux données temporelles pour les graphiques
            current_time = len(self.goda_results) * 0.05  # Supposer 20 Hz
            self.goda_results.append(stats_data)
            
            # Mettre à jour les courbes Goda (garder seulement les 1000 derniers points)
            if len(self.goda_results) > 1000:
                self.goda_results = self.goda_results[-1000:]
                
            times = np.arange(len(self.goda_results)) * 0.05
            hs_values = [r.get('Hs', 0) for r in self.goda_results]
            cr_values = [r.get('Cr', 0) for r in self.goda_results]
            
            self.hs_curve.setData(times, hs_values)
            
        except Exception as e:
            self._log_event(f"❌ Erreur mise à jour Goda: {str(e)}")
            
    @pyqtSlot(dict)
    def _update_performance_stats(self, perf_data: Dict[str, Any]):
        """Met à jour les statistiques de performance"""
        try:
            fft_time = perf_data.get('fft_time', 0)
            goda_time = perf_data.get('goda_time', 0)
            total_time = perf_data.get('total_time', 0)
            throughput = perf_data.get('throughput', 0)
            cache_hits = perf_data.get('cache_hits', 0)
            
            # Calculer FPS et latence pour les labels compacts
            fps = 1000 / total_time if total_time > 0 else 0
            memory_usage = perf_data.get('memory_usage', 50)
            
            # Mettre à jour les labels de performance détaillés (si présents)
            if hasattr(self, 'fft_time_label'):
                self.fft_time_label.setText(f"{fft_time:.2f} ms")
            if hasattr(self, 'goda_time_label'):
                self.goda_time_label.setText(f"{goda_time:.2f} ms")
            if hasattr(self, 'total_time_label'):
                self.total_time_label.setText(f"{total_time:.2f} ms")
            if hasattr(self, 'throughput_label'):
                self.throughput_label.setText(f"{throughput:.0f} sps")
            if hasattr(self, 'cache_hits_label'):
                self.cache_hits_label.setText(f"{cache_hits}")
            
            # Mettre à jour les labels compacts du panneau de stats
            if hasattr(self, 'fps_label'):
                self.fps_label.setText(f"{fps:.1f} FPS")
            if hasattr(self, 'latency_label'):
                self.latency_label.setText(f"{total_time:.1f} ms")
            if hasattr(self, 'memory_label'):
                self.memory_label.setText(f"{memory_usage:.1f} MB")
            
            # Colorer selon les performances
            if hasattr(self, 'total_time_label'):
                if total_time < 16:  # Objectif < 16ms
                    self.total_time_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
                else:
                    self.total_time_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                
        except Exception as e:
            self._log_event(f"❌ Erreur mise à jour performance: {str(e)}")
            
    @pyqtSlot(str)
    def _handle_processing_error(self, error_message: str):
        """Gère les erreurs de traitement"""
        self._log_event(f"❌ Erreur traitement: {error_message}")
        
    def _configure_probe_positions(self):
        """Configure les positions des sondes"""
        # TODO: Implémenter le dialogue de configuration
        self._log_event("⚙️ Configuration des positions des sondes")
    
    def _open_advanced_settings(self):
        """Ouvre la fenêtre de paramètres avancés"""
        try:
            dialog = AdvancedSettingsDialog(self.config, self)
            result = dialog.exec_()
            
            if result == QDialog.Accepted:
                # Mettre à jour les paramètres de l'interface
                self._update_interface_from_config()
                self._log_event("⚙️ Paramètres avancés mis à jour")
            
        except Exception as e:
            self._log_event(f"❌ Erreur ouverture paramètres: {str(e)}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ouverture des paramètres:\n{str(e)}")
    
    def _update_interface_from_config(self):
        """Met à jour l'interface selon la configuration modifiée"""
        try:
            # Mettre à jour les spinboxes
            self.duration_spinbox.setValue(self.config.get('duration', 300))
            self.sample_rate_spinbox.setValue(self.config.get('sample_rate', 32.0))
            self.n_sondes_spinbox.setValue(self.config.get('n_channels', 4))
            
            # Mettre à jour les variables internes
            self.duration = self.config.get('duration', 300)
            self.sample_rate = self.config.get('sample_rate', 32.0)
            self.n_sondes = self.config.get('n_channels', 4)
            
            # Mettre à jour les labels d'information
            self.frequency_label.setText(f"{self.sample_rate} Hz")
            self.probes_label.setText(f"{self.n_sondes} sondes")
            self.active_probes_label.setText(f"{self.n_sondes}/{self.n_sondes}")
            
            # Reconfigurer le worker de traitement si nécessaire
            if self.processing_worker:
                self._init_processing_worker()
            
        except Exception as e:
            self._log_event(f"❌ Erreur mise à jour interface: {str(e)}")
        
    def _export_data(self):
        """Exporte les données"""
        try:
            # Sélection du fichier
            format_ext = {
                'CSV': '.csv',
                'JSON': '.json', 
                'MAT': '.mat',
                'HDF5': '.h5'
            }
            
            ext = format_ext[self.export_format.currentText()]
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Exporter les données", 
                f"acquisition_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}",
                f"Fichiers {self.export_format.currentText()} (*{ext})"
            )
            
            if filename:
                # TODO: Implémenter l'export selon le format
                self._log_event(f"💾 Données exportées: {filename}")
                self.dataExported.emit(filename)
                
        except Exception as e:
            self._log_event(f"❌ Erreur export: {str(e)}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export:\n{str(e)}")


class AdvancedSettingsDialog(QDialog):
    """Fenêtre de paramètres avancés"""
    
    def __init__(self, config: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Paramètres Avancés")
        self.setModal(True)
        self.resize(500, 400)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Onglets de configuration
        tabs = QTabWidget()
        
        # Onglet Acquisition
        acq_tab = self._create_acquisition_tab()
        tabs.addTab(acq_tab, "Acquisition")
        
        # Onglet Performance
        perf_tab = self._create_performance_tab()
        tabs.addTab(perf_tab, "Performance")
        
        # Onglet Calibration
        calib_tab = self._create_calibration_tab()
        tabs.addTab(calib_tab, "Calibration")
        
        layout.addWidget(tabs)
        
        # Boutons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Apply).clicked.connect(self._apply_settings)
        
        layout.addWidget(buttons)
    
    def _create_acquisition_tab(self):
        """Crée l'onglet de paramètres d'acquisition"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Paramètres d'acquisition
        self.sample_rate_spin = QDoubleSpinBox()
        self.sample_rate_spin.setRange(0.1, 1000.0)
        self.sample_rate_spin.setValue(self.config.get('sample_rate', 32.0))
        self.sample_rate_spin.setSuffix(' Hz')
        layout.addRow("Fréquence d'échantillonnage:", self.sample_rate_spin)
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 3600)
        self.duration_spin.setValue(self.config.get('duration', 300))
        self.duration_spin.setSuffix(' s')
        layout.addRow("Durée d'acquisition:", self.duration_spin)
        
        self.n_channels_spin = QSpinBox()
        self.n_channels_spin.setRange(1, 16)
        self.n_channels_spin.setValue(self.config.get('n_channels', 4))
        layout.addRow("Nombre de sondes:", self.n_channels_spin)
        
        # Filtrage
        filter_group = QGroupBox("Filtrage")
        filter_layout = QFormLayout(filter_group)
        
        self.enable_filter = QCheckBox()
        self.enable_filter.setChecked(self.config.get('enable_filter', True))
        filter_layout.addRow("Activer le filtrage:", self.enable_filter)
        
        self.low_freq = QDoubleSpinBox()
        self.low_freq.setRange(0.001, 10.0)
        self.low_freq.setValue(self.config.get('low_freq', 0.05))
        self.low_freq.setSuffix(' Hz')
        filter_layout.addRow("Fréquence basse:", self.low_freq)
        
        self.high_freq = QDoubleSpinBox()
        self.high_freq.setRange(0.1, 100.0)
        self.high_freq.setValue(self.config.get('high_freq', 5.0))
        self.high_freq.setSuffix(' Hz')
        filter_layout.addRow("Fréquence haute:", self.high_freq)
        
        layout.addRow(filter_group)
        
        return widget
    
    def _create_performance_tab(self):
        """Crée l'onglet de paramètres de performance"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Paramètres de traitement
        self.buffer_size = QSpinBox()
        self.buffer_size.setRange(512, 8192)
        self.buffer_size.setValue(self.config.get('buffer_size', 2048))
        layout.addRow("Taille du buffer:", self.buffer_size)
        
        self.overlap_ratio = QDoubleSpinBox()
        self.overlap_ratio.setRange(0.0, 0.9)
        self.overlap_ratio.setValue(self.config.get('overlap_ratio', 0.5))
        self.overlap_ratio.setSingleStep(0.1)
        layout.addRow("Ratio de recouvrement:", self.overlap_ratio)
        
        # Optimisations
        optim_group = QGroupBox("Optimisations")
        optim_layout = QFormLayout(optim_group)
        
        self.enable_cache = QCheckBox()
        self.enable_cache.setChecked(self.config.get('enable_cache', True))
        optim_layout.addRow("Cache FFT:", self.enable_cache)
        
        self.enable_parallel = QCheckBox()
        self.enable_parallel.setChecked(self.config.get('enable_parallel', True))
        optim_layout.addRow("Traitement parallèle:", self.enable_parallel)
        
        self.max_threads = QSpinBox()
        self.max_threads.setRange(1, 16)
        self.max_threads.setValue(self.config.get('max_threads', 4))
        optim_layout.addRow("Threads max:", self.max_threads)
        
        layout.addRow(optim_group)
        
        # Mémoire
        memory_group = QGroupBox("Gestion mémoire")
        memory_layout = QFormLayout(memory_group)
        
        self.max_memory = QSpinBox()
        self.max_memory.setRange(100, 4000)
        self.max_memory.setValue(self.config.get('max_memory_mb', 1000))
        self.max_memory.setSuffix(' MB')
        memory_layout.addRow("Mémoire max:", self.max_memory)
        
        self.auto_cleanup = QCheckBox()
        self.auto_cleanup.setChecked(self.config.get('auto_cleanup', True))
        memory_layout.addRow("Nettoyage auto:", self.auto_cleanup)
        
        layout.addRow(memory_group)
        
        return widget
    
    def _create_calibration_tab(self):
        """Crée l'onglet de paramètres de calibration"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Facteurs de calibration
        calib_group = QGroupBox("Facteurs de calibration")
        calib_layout = QGridLayout(calib_group)
        
        self.calib_factors = []
        n_channels = self.config.get('n_channels', 4)
        
        for i in range(n_channels):
            label = QLabel(f"Sonde {i+1}:")
            spin = QDoubleSpinBox()
            spin.setRange(0.001, 1000.0)
            spin.setValue(self.config.get(f'calib_factor_{i}', 1.0))
            spin.setDecimals(6)
            spin.setSuffix(' m/V')
            
            calib_layout.addWidget(label, i, 0)
            calib_layout.addWidget(spin, i, 1)
            self.calib_factors.append(spin)
        
        layout.addWidget(calib_group)
        
        # Positions des sondes
        pos_group = QGroupBox("Positions des sondes")
        pos_layout = QGridLayout(pos_group)
        
        pos_layout.addWidget(QLabel("X (m)"), 0, 1)
        pos_layout.addWidget(QLabel("Y (m)"), 0, 2)
        pos_layout.addWidget(QLabel("Z (m)"), 0, 3)
        
        self.probe_positions = []
        for i in range(n_channels):
            label = QLabel(f"Sonde {i+1}:")
            pos_layout.addWidget(label, i+1, 0)
            
            row_positions = []
            for j, coord in enumerate(['x', 'y', 'z']):
                spin = QDoubleSpinBox()
                spin.setRange(-100.0, 100.0)
                spin.setValue(self.config.get(f'probe_{i}_{coord}', 0.0))
                spin.setDecimals(3)
                spin.setSuffix(' m')
                
                pos_layout.addWidget(spin, i+1, j+1)
                row_positions.append(spin)
            
            self.probe_positions.append(row_positions)
        
        layout.addWidget(pos_group)
        
        # Boutons de calibration
        button_layout = QHBoxLayout()
        
        load_calib_btn = QPushButton("Charger calibration")
        load_calib_btn.clicked.connect(self._load_calibration)
        button_layout.addWidget(load_calib_btn)
        
        save_calib_btn = QPushButton("Sauvegarder calibration")
        save_calib_btn.clicked.connect(self._save_calibration)
        button_layout.addWidget(save_calib_btn)
        
        auto_calib_btn = QPushButton("Calibration automatique")
        auto_calib_btn.clicked.connect(self._auto_calibration)
        button_layout.addWidget(auto_calib_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return widget
    
    def _apply_settings(self):
        """Applique les paramètres modifiés"""
        try:
            # Paramètres d'acquisition
            self.config['sample_rate'] = self.sample_rate_spin.value()
            self.config['duration'] = self.duration_spin.value()
            self.config['n_channels'] = self.n_channels_spin.value()
            
            # Filtrage
            self.config['enable_filter'] = self.enable_filter.isChecked()
            self.config['low_freq'] = self.low_freq.value()
            self.config['high_freq'] = self.high_freq.value()
            
            # Performance
            self.config['buffer_size'] = self.buffer_size.value()
            self.config['overlap_ratio'] = self.overlap_ratio.value()
            self.config['enable_cache'] = self.enable_cache.isChecked()
            self.config['enable_parallel'] = self.enable_parallel.isChecked()
            self.config['max_threads'] = self.max_threads.value()
            self.config['max_memory_mb'] = self.max_memory.value()
            self.config['auto_cleanup'] = self.auto_cleanup.isChecked()
            
            # Calibration
            for i, factor_spin in enumerate(self.calib_factors):
                self.config[f'calib_factor_{i}'] = factor_spin.value()
            
            for i, pos_row in enumerate(self.probe_positions):
                for j, coord in enumerate(['x', 'y', 'z']):
                    self.config[f'probe_{i}_{coord}'] = pos_row[j].value()
            
            QMessageBox.information(self, "Succès", "Paramètres appliqués avec succès")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'application des paramètres:\n{str(e)}")
    
    def _load_calibration(self):
        """Charge un fichier de calibration"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Charger calibration", "", "Fichiers JSON (*.json)"
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    calib_data = json.load(f)
                
                # Charger les facteurs de calibration
                for i, factor_spin in enumerate(self.calib_factors):
                    if f'calib_factor_{i}' in calib_data:
                        factor_spin.setValue(calib_data[f'calib_factor_{i}'])
                
                # Charger les positions
                for i, pos_row in enumerate(self.probe_positions):
                    for j, coord in enumerate(['x', 'y', 'z']):
                        key = f'probe_{i}_{coord}'
                        if key in calib_data:
                            pos_row[j].setValue(calib_data[key])
                
                QMessageBox.information(self, "Succès", "Calibration chargée avec succès")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement:\n{str(e)}")
    
    def _save_calibration(self):
        """Sauvegarde la calibration actuelle"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder calibration", "", "Fichiers JSON (*.json)"
        )
        if filename:
            try:
                calib_data = {}
                
                # Sauvegarder les facteurs
                for i, factor_spin in enumerate(self.calib_factors):
                    calib_data[f'calib_factor_{i}'] = factor_spin.value()
                
                # Sauvegarder les positions
                for i, pos_row in enumerate(self.probe_positions):
                    for j, coord in enumerate(['x', 'y', 'z']):
                        calib_data[f'probe_{i}_{coord}'] = pos_row[j].value()
                
                with open(filename, 'w') as f:
                    json.dump(calib_data, f, indent=2)
                
                QMessageBox.information(self, "Succès", "Calibration sauvegardée avec succès")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")
    
    def _auto_calibration(self):
        """Lance une calibration automatique"""
        QMessageBox.information(
            self, "Calibration automatique", 
            "Fonctionnalité de calibration automatique à implémenter.\n"
            "Cette fonction analysera les signaux de référence pour "
            "déterminer automatiquement les facteurs de calibration."
        )


def main():
    """Fonction principale pour tester l'interface"""
    app = QApplication(sys.argv)
    
    # Configuration de test
    config = {
        'n_channels': 4,
        'sample_rate': 32.0,
        'duration': 300,
        'save_folder': './data'
    }
    
    # Créer l'interface
    window = ModernAcquisitionUI(config)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()