# acquisition_view.py - Vue d'acquisition temps réel simplifiée
import sys
import os
import time
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, 
    QDoubleSpinBox, QGroupBox, QFormLayout, QSplitter, QSizePolicy,
    QComboBox, QCheckBox, QScrollArea, QApplication
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QFont

import pyqtgraph as pg
from pyqtgraph import PlotWidget, mkPen

# P0: Import des signaux unifiés
from hrneowave.core.signal_bus import get_signal_bus, get_error_bus

class GraphManager:
    """Gestionnaire des graphiques PyQtGraph pour performance optimale
    
    Gère 3 graphiques :
    - Signal A : sonde individuelle sélectionnable
    - Signal B : autre sonde individuelle  
    - Vue globale : N sondes avec checkboxes
    """
    
    def __init__(self, n_sondes: int = 4):
        self.n_sondes = n_sondes
        self.colors = ['#FF5722', '#2196F3', '#4CAF50', '#FF9800', 
                      '#9C27B0', '#607D8B', '#795548', '#E91E63']
        
        # Graphiques
        self.signal_a_plot = None
        self.signal_b_plot = None
        self.global_plot = None
        
        # Courbes actives
        self.signal_a_curve = None
        self.signal_b_curve = None
        self.global_curves = {}  # {sonde_id: curve}
        
        # Sélections
        self.selected_probe_a = 0
        self.selected_probe_b = 1
        self.enabled_probes = set()  # Sondes actives pour vue globale
        
        # Cache données
        self.current_time = None
        self.current_signals = None
        
    def setup_plots(self, signal_a_widget: PlotWidget, signal_b_widget: PlotWidget, 
                   global_widget: PlotWidget):
        """Configure les 3 graphiques"""
        self.signal_a_plot = signal_a_widget
        self.signal_b_plot = signal_b_widget
        self.global_plot = global_widget
        
        # Configuration commune
        for plot in [self.signal_a_plot, self.signal_b_plot, self.global_plot]:
            plot.setLabel('left', 'Amplitude', units='m')
            plot.setLabel('bottom', 'Temps', units='s')
            plot.showGrid(x=True, y=True, alpha=0.3)
            plot.setBackground('#1e1e1e')
            
        # Titres
        self.signal_a_plot.setTitle("Signal A - Sonde 1")
        self.signal_b_plot.setTitle("Signal B - Sonde 2")
        self.global_plot.setTitle("Vue Globale")
        
        # Courbes initiales
        self._create_initial_curves()
        
    def _create_initial_curves(self):
        """Crée les courbes initiales"""
        # Courbes initiales
        self.signal_a_curve = self.signal_a_plot.plot(
            pen=pg.mkPen(self.colors[0], width=2), name=f"Sonde {self.selected_probe_a + 1}")
            
        # Signal B  
        self.signal_b_curve = self.signal_b_plot.plot(
            pen=pg.mkPen(self.colors[1], width=2), name=f"Sonde {self.selected_probe_b + 1}")
            
    def set_probe_a(self, probe_id: int):
        """Change la sonde pour Signal A"""
        if 0 <= probe_id < self.n_sondes:
            self.selected_probe_a = probe_id
            self.signal_a_plot.setTitle(f"Signal A - Sonde {probe_id + 1}")
            if self.signal_a_curve:
                self.signal_a_curve.setPen(pg.mkPen(self.colors[probe_id % len(self.colors)], width=2))
                
    def set_probe_b(self, probe_id: int):
        """Change la sonde pour Signal B"""
        if 0 <= probe_id < self.n_sondes:
            self.selected_probe_b = probe_id
            self.signal_b_plot.setTitle(f"Signal B - Sonde {probe_id + 1}")
            if self.signal_b_curve:
                self.signal_b_curve.setPen(pg.mkPen(self.colors[probe_id % len(self.colors)], width=2))
                
    def toggle_global_probe(self, probe_id: int, enabled: bool):
        """Active/désactive une sonde dans la vue globale"""
        if enabled and probe_id not in self.global_curves:
            # Ajouter courbe
            color = self.colors[probe_id % len(self.colors)]
            curve = self.global_plot.plot(pen=pg.mkPen(color, width=1.5), name=f"Sonde {probe_id + 1}")
            self.global_curves[probe_id] = curve
            self.enabled_probes.add(probe_id)
            
        elif not enabled and probe_id in self.global_curves:
            # Supprimer courbe
            self.global_plot.removeItem(self.global_curves[probe_id])
            del self.global_curves[probe_id]
            self.enabled_probes.discard(probe_id)
            
    def update_data(self, time_data, signals_data):
        """Met à jour toutes les courbes avec nouvelles données
        
        Args:
            time_data: array des temps
            signals_data: liste des signaux [signal_sonde_0, signal_sonde_1, ...]
        """
        self.current_time = time_data
        self.current_signals = signals_data
        
        # Signal A
        if self.signal_a_curve and self.selected_probe_a < len(signals_data):
            self.signal_a_curve.setData(time_data, signals_data[self.selected_probe_a])
        
        # Signal B
        if self.signal_b_curve and self.selected_probe_b < len(signals_data):
            self.signal_b_curve.setData(time_data, signals_data[self.selected_probe_b])
        
        # Vue globale
        for probe_id in self.enabled_probes:
            if probe_id < len(signals_data) and probe_id in self.global_curves:
                self.global_curves[probe_id].setData(time_data, signals_data[probe_id])
                
    def initialize_curves(self):
        """Initialise les courbes sur chaque graphique"""
        if not all([self.signal_a_plot, self.signal_b_plot, self.global_plot]):
            return
        
        # Signal A
        self.signal_a_curve = self.signal_a_plot.plot(
            pen=mkPen(color=self.colors[self.selected_probe_a], width=2),
            name=f'Sonde {self.selected_probe_a + 1}'
        )
        
        # Signal B
        self.signal_b_curve = self.signal_b_plot.plot(
            pen=mkPen(color=self.colors[self.selected_probe_b], width=2),
            name=f'Sonde {self.selected_probe_b + 1}'
        )
        
        # Vue globale - toutes les sondes activées par défaut
        for i in range(self.n_sondes):
            self.toggle_global_probe(i, True)
    
    def update_signal_a(self, new_index):
        """Change la sonde affichée sur Signal A"""
        if new_index == self.selected_probe_a or new_index >= self.n_sondes:
            return
        
        self.selected_probe_a = new_index
        
        # Recréer la courbe avec nouvelle couleur
        if self.signal_a_plot:
            self.signal_a_plot.clear()
            self.signal_a_curve = self.signal_a_plot.plot(
                pen=mkPen(color=self.colors[new_index], width=2),
                name=f'Sonde {new_index + 1}'
            )
            
            # Réappliquer données si disponibles
            if self.current_time is not None and self.current_signals:
                if new_index < len(self.current_signals):
                    self.signal_a_curve.setData(self.current_time, self.current_signals[new_index])
    
    def update_signal_b(self, new_index):
        """Change la sonde affichée sur Signal B"""
        if new_index == self.selected_probe_b or new_index >= self.n_sondes:
            return
        
        self.selected_probe_b = new_index
        
        # Recréer la courbe avec nouvelle couleur
        if self.signal_b_plot:
            self.signal_b_plot.clear()
            self.signal_b_curve = self.signal_b_plot.plot(
                pen=mkPen(color=self.colors[new_index], width=2),
                name=f'Sonde {new_index + 1}'
            )
            
            # Réappliquer données si disponibles
            if self.current_time is not None and self.current_signals:
                if new_index < len(self.current_signals):
                    self.signal_b_curve.setData(self.current_time, self.current_signals[new_index])
    
    def update_global_view(self, selected_indices):
        """Met à jour les sondes affichées dans la vue globale"""
        current_enabled = self.enabled_probes.copy()
        
        # Désactiver les sondes non sélectionnées
        for probe_id in current_enabled:
            if probe_id not in selected_indices:
                self.toggle_global_probe(probe_id, False)
        
        # Activer les nouvelles sondes sélectionnées
        for probe_id in selected_indices:
            if probe_id not in current_enabled:
                self.toggle_global_probe(probe_id, True)
    
    def clear_all(self):
        """Efface toutes les données"""
        if self.signal_a_curve:
            self.signal_a_curve.setData([], [])
        if self.signal_b_curve:
            self.signal_b_curve.setData([], [])
        for curve in self.global_curves.values():
            curve.setData([], [])

try:
    from acquisition_controller import AcquisitionController
except ImportError:
    print("⚠️ AcquisitionController non disponible")
    AcquisitionController = None

class AcquisitionView(QWidget):
    """Vue d'acquisition temps réel - Interface épurée pour l'acquisition
    
    Fonctionnalités:
    - Graphiques temps réel uniquement (PyQtGraph)
    - Stats live minimal : Hmax, Hmean, Tmean (zone 200px à droite)
    - Voyants sondes + compteur échantillons
    - Boutons Start, Stop, Export
    - QSplitter horizontal : contrôle (30%) / graphe (70%)
    - Taille minimale 1024×640, responsive jusqu'à 1280×720
    """
    
    # Signaux pour communication avec controller
    acquisitionStarted = pyqtSignal()
    acquisitionStopped = pyqtSignal()
    dataExported = pyqtSignal(str)  # Chemin fichier exporté
    analysisRequested = pyqtSignal(str)  # Demande ouverture vue analyse
    
    def __init__(self, config: Dict[str, Any], acquisition_controller: Optional[AcquisitionController] = None):
        super().__init__()
        self.config = config
        self.acquisition_controller = acquisition_controller
        
        # Configuration acquisition
        self.n_sondes = config.get('n_channels', 4)
        self.sample_rate = config.get('sample_rate', 32.0)
        self.duration = config.get('duration', 300)
        self.save_folder = config.get('save_folder', './data')
        
        # État acquisition
        self.is_acquiring = False
        self.start_time = None
        self.total_samples = 0
        self.current_data = [[] for _ in range(self.n_sondes)]
        
        # Stats live
        self.live_stats = {
            'hmax': 0.0,
            'hmean': 0.0,
            'tmean': 0.0
        }
        
        # GraphManager pour gestion optimisée des graphiques
        self.graph_manager = GraphManager(self.n_sondes)
        
        # Timer mise à jour
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_live_display)
        
        # P0: Connexion aux signaux unifiés
        self.signal_bus = get_signal_bus()
        self.error_bus = get_error_bus()
        self._connect_unified_signals()
        
        self._init_ui()
        self._setup_pyqtgraph()
        
    def _init_ui(self):
        """Initialise l'interface utilisateur épurée"""
        self.setWindowTitle("HRNeoWave - Acquisition Temps Réel")
        
        # Taille minimale selon spécifications
        self.setMinimumSize(1024, 640)
        self.resize(1280, 720)
        
        self._create_layout()
        self._apply_acquisition_theme()
        
    def _create_layout(self):
        """Crée le layout principal avec QSplitter horizontal 30%/70%"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(0)
        
        # QSplitter horizontal principal
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(2)
        self.main_splitter.setChildrenCollapsible(False)
        
        # Panneau contrôle (30%)
        control_panel = self._create_control_panel()
        control_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Zone graphique (70%)
        graphics_area = self._create_graphics_area()
        graphics_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.main_splitter.addWidget(control_panel)
        self.main_splitter.addWidget(graphics_area)
        
        # Proportions 30% / 70%
        self.main_splitter.setStretchFactor(0, 30)
        self.main_splitter.setStretchFactor(1, 70)
        self.main_splitter.setSizes([307, 717])  # Pour 1024px largeur
        
        main_layout.addWidget(self.main_splitter)
        
    def _create_control_panel(self) -> QWidget:
        """Crée le panneau de contrôle épuré"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Contrôles principaux
        layout.addWidget(self._create_main_controls())
        
        # Sélecteurs de sondes
        layout.addWidget(self._create_probe_selectors())
        
        # Configuration rapide
        layout.addWidget(self._create_quick_config())
        
        # Voyants sondes
        layout.addWidget(self._create_probe_status())
        
        # Compteur échantillons
        layout.addWidget(self._create_sample_counter())
        
        layout.addStretch()
        return panel
        
    def _create_main_controls(self) -> QGroupBox:
        """Crée les contrôles Start/Stop/Export"""
        group = QGroupBox("Contrôles")
        layout = QVBoxLayout(group)
        
        # Boutons Start/Stop
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self._start_acquisition)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._stop_acquisition)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # Bouton Export
        self.export_button = QPushButton("Export")
        self.export_button.setMinimumHeight(30)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self._export_data)
        layout.addWidget(self.export_button)
        
        return group
        
    def _create_quick_config(self) -> QGroupBox:
        """Configuration rapide durée/fréquence"""
        group = QGroupBox("Configuration")
        layout = QFormLayout(group)
        
        # Durée
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(10, 3600)
        self.duration_spinbox.setValue(self.duration)
        self.duration_spinbox.setSuffix(" s")
        layout.addRow("Durée:", self.duration_spinbox)
        
        # Fréquence
        self.sample_rate_spinbox = QDoubleSpinBox()
        self.sample_rate_spinbox.setRange(1.0, 100.0)
        self.sample_rate_spinbox.setValue(self.sample_rate)
        self.sample_rate_spinbox.setSuffix(" Hz")
        layout.addRow("Fréq.:", self.sample_rate_spinbox)
        
        return group
        
    def _create_probe_selectors(self) -> QGroupBox:
        """Crée les sélecteurs de sondes pour les graphiques"""
        group = QGroupBox("Sélection Sondes")
        layout = QVBoxLayout(group)
        
        # Sonde A
        sonde_a_layout = QHBoxLayout()
        sonde_a_layout.addWidget(QLabel("Signal A:"))
        self.sonde_a_combo = QComboBox()
        self.sonde_a_combo.addItems([f"Sonde {i+1}" for i in range(self.n_sondes)])
        self.sonde_a_combo.currentIndexChanged.connect(self._on_sonde_a_changed)
        sonde_a_layout.addWidget(self.sonde_a_combo)
        layout.addLayout(sonde_a_layout)
        
        # Sonde B
        sonde_b_layout = QHBoxLayout()
        sonde_b_layout.addWidget(QLabel("Signal B:"))
        self.sonde_b_combo = QComboBox()
        self.sonde_b_combo.addItems([f"Sonde {i+1}" for i in range(self.n_sondes)])
        self.sonde_b_combo.setCurrentIndex(1 if self.n_sondes > 1 else 0)
        self.sonde_b_combo.currentIndexChanged.connect(self._on_sonde_b_changed)
        sonde_b_layout.addWidget(self.sonde_b_combo)
        layout.addLayout(sonde_b_layout)
        
        # Vue globale - checkboxes dans scroll area
        global_label = QLabel("Vue Globale:")
        layout.addWidget(global_label)
        
        scroll_area = QScrollArea()
        scroll_area.setMaximumHeight(120)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        self.global_checkboxes = []
        for i in range(self.n_sondes):
            checkbox = QCheckBox(f"Sonde {i+1}")
            checkbox.setChecked(True)  # Toutes cochées par défaut
            checkbox.stateChanged.connect(self._on_global_selection_changed)
            self.global_checkboxes.append(checkbox)
            scroll_layout.addWidget(checkbox)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        return group
        
    def _create_probe_status(self) -> QGroupBox:
        """Voyants état des sondes"""
        group = QGroupBox("Sondes")
        layout = QVBoxLayout(group)
        
        self.probe_labels = []
        for i in range(self.n_sondes):
            label = QLabel(f"Sonde {i+1}: ⚫")
            label.setStyleSheet("color: #666;")
            self.probe_labels.append(label)
            layout.addWidget(label)
            
        return group
        
    def _create_sample_counter(self) -> QGroupBox:
        """Compteur d'échantillons"""
        group = QGroupBox("Échantillons")
        layout = QFormLayout(group)
        
        self.samples_label = QLabel("0")
        self.duration_label = QLabel("00:00")
        
        layout.addRow("Total:", self.samples_label)
        layout.addRow("Temps:", self.duration_label)
        
        return group
        
    def _create_graphics_area(self) -> QWidget:
        """Zone graphique avec 3 graphiques en splitter vertical"""
        # Splitter vertical pour les 3 graphiques
        splitter = QSplitter(Qt.Vertical)
        
        # Graphique Signal A
        self.signal_a_plot = PlotWidget(title="Signal A")
        self.signal_a_plot.setLabel('left', 'Amplitude', units='m')
        self.signal_a_plot.setLabel('bottom', 'Temps', units='s')
        self.signal_a_plot.showGrid(x=True, y=True)
        splitter.addWidget(self.signal_a_plot)
        
        # Graphique Signal B
        self.signal_b_plot = PlotWidget(title="Signal B")
        self.signal_b_plot.setLabel('left', 'Amplitude', units='m')
        self.signal_b_plot.setLabel('bottom', 'Temps', units='s')
        self.signal_b_plot.showGrid(x=True, y=True)
        splitter.addWidget(self.signal_b_plot)
        
        # Graphique Vue Globale
        self.global_plot = PlotWidget(title="Vue Globale")
        self.global_plot.setLabel('left', 'Amplitude', units='m')
        self.global_plot.setLabel('bottom', 'Temps', units='s')
        self.global_plot.showGrid(x=True, y=True)
        splitter.addWidget(self.global_plot)
        
        # Répartition 33/33/34%
        splitter.setSizes([330, 330, 340])
        
        # Configuration du GraphManager
        self.graph_manager.setup_plots(self.signal_a_plot, self.signal_b_plot, self.global_plot)
        
        # Widget conteneur avec stats
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Zone stats live (200px)
        stats_panel = self._create_live_stats_panel()
        stats_panel.setFixedWidth(200)
        
        layout.addWidget(splitter)
        layout.addWidget(stats_panel)
        
        return container
        
    def _create_live_stats_panel(self) -> QWidget:
        """Panneau stats live minimal : Hmax, Hmean, Tmean"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Titre
        title = QLabel("📊 Stats Live")
        title.setStyleSheet("font-weight: bold; color: #2196F3; font-size: 14px;")
        layout.addWidget(title)
        
        # Stats
        stats_group = QGroupBox()
        stats_layout = QFormLayout(stats_group)
        
        self.hmax_label = QLabel("-- m")
        self.hmean_label = QLabel("-- m")
        self.tmean_label = QLabel("-- s")
        
        stats_layout.addRow("Hmax:", self.hmax_label)
        stats_layout.addRow("Hmean:", self.hmean_label)
        stats_layout.addRow("Tmean:", self.tmean_label)
        
        layout.addWidget(stats_group)
        layout.addStretch()
        
        return panel
    
    def _on_sonde_a_changed(self, index):
        """Callback changement sonde A"""
        self.graph_manager.update_signal_a(index)
    
    def _on_sonde_b_changed(self, index):
        """Callback changement sonde B"""
        self.graph_manager.update_signal_b(index)
    
    def _on_global_selection_changed(self):
        """Callback changement sélection vue globale"""
        selected_probes = []
        for i, checkbox in enumerate(self.global_checkboxes):
            if checkbox.isChecked():
                selected_probes.append(i)
        self.graph_manager.update_global_view(selected_probes)
        
    def _setup_pyqtgraph(self):
        """Configuration PyQtGraph pour performance optimale"""
        pg.setConfigOptions(
            antialias=False,  # Performance
            useOpenGL=True,   # Accélération GPU
            enableExperimental=True
        )
        
        # Initialisation des courbes via GraphManager
        self.graph_manager.initialize_curves()
            
    def _apply_acquisition_theme(self):
        """Thème épuré pour l'acquisition"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
            }
            QPushButton {
                background-color: #2196F3;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        
    def _start_acquisition(self):
        """Démarre l'acquisition"""
        if self.acquisition_controller:
            self.is_acquiring = True
            self.start_time = time.time()
            self.total_samples = 0
            
            # Mise à jour UI
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.export_button.setEnabled(False)
            
            # Démarrer timer
            self.update_timer.start(50)  # 20 FPS
            
            # Signal
            self.acquisitionStarted.emit()
            
            # Mise à jour voyants
            for label in self.probe_labels:
                label.setText(label.text().replace("⚫", "🟢"))
                label.setStyleSheet("color: #4CAF50;")
                
    def _stop_acquisition(self):
        """Arrête l'acquisition et propose l'analyse"""
        self.is_acquiring = False
        
        # Arrêter timer
        self.update_timer.stop()
        
        # Mise à jour UI
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.export_button.setEnabled(True)
        
        # Signal
        self.acquisitionStopped.emit()
        
        # Mise à jour voyants
        for label in self.probe_labels:
            label.setText(label.text().replace("🟢", "⚫"))
            label.setStyleSheet("color: #666;")
            
        # Proposer ouverture vue analyse
        if self.total_samples > 0:
            self._propose_analysis()
            
    def _export_data(self):
        """Exporte les données acquises"""
        if not self.current_data or not any(self.current_data):
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"acquisition_HRNeoWave_{timestamp}.csv"
        filepath = os.path.join(self.save_folder, filename)
        
        # Export CSV simple
        try:
            with open(filepath, 'w', newline='') as f:
                import csv
                writer = csv.writer(f)
                
                # En-tête
                headers = ['Time'] + [f'Sonde_{i+1}' for i in range(self.n_sondes)]
                writer.writerow(headers)
                
                # Données
                max_len = max(len(data) for data in self.current_data if data)
                for i in range(max_len):
                    row = [i / self.sample_rate]  # Temps
                    for data in self.current_data:
                        row.append(data[i] if i < len(data) else 0.0)
                    writer.writerow(row)
                    
            self.dataExported.emit(filepath)
            
        except Exception as e:
            print(f"Erreur export: {e}")
            
    def _propose_analysis(self):
        """Propose l'ouverture de la vue analyse"""
        # Signal pour demander ouverture vue analyse
        # Le fichier sera exporté automatiquement
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"acquisition_HRNeoWave_{timestamp}.csv"
        filepath = os.path.join(self.save_folder, filename)
        
        # Export automatique pour analyse
        self._export_data()
        
        # Signal pour ouvrir vue analyse
        self.analysisRequested.emit(filepath)
        
    def _update_live_display(self):
        """Mise à jour affichage temps réel"""
        if not self.is_acquiring:
            return
            
        # Simulation données (à remplacer par vraies données)
        current_time = time.time() - self.start_time
        
        # Mise à jour compteurs
        self.total_samples = int(current_time * self.sample_rate)
        self.samples_label.setText(str(self.total_samples))
        
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        self.duration_label.setText(f"{minutes:02d}:{seconds:02d}")
        
        # Simulation données sondes
        if self.acquisition_controller:
            # Récupérer vraies données du controller
            pass
        else:
            # Données simulées
            t = np.linspace(current_time-10, current_time, 100)
            signals = []
            
            for i in range(self.n_sondes):
                # Signal sinusoïdal avec bruit
                freq = 0.1 + i * 0.05
                amplitude = 0.5 + i * 0.2
                signal = amplitude * np.sin(2 * np.pi * freq * t) + 0.1 * np.random.randn(len(t))
                signals.append(signal)
                
                # Stocker pour export
                if len(self.current_data[i]) > 1000:  # Limite mémoire
                    self.current_data[i] = self.current_data[i][-500:]
                self.current_data[i].extend(signal[-10:])  # Ajouter nouveaux points
            
            # Mise à jour via GraphManager
            self.graph_manager.update_data(t, signals)
                
        # Mise à jour stats live
        self._update_live_stats()
        
        # Arrêt automatique si durée atteinte
        if current_time >= self.duration:
            self._stop_acquisition()
            
    def _update_live_stats(self):
        """Calcule et affiche stats live"""
        if not any(self.current_data):
            return
            
        # Calcul stats sur données récentes
        all_data = []
        for data in self.current_data:
            if data:
                all_data.extend(data[-100:])  # 100 derniers points
                
        if all_data:
            # Hmax
            hmax = max(abs(x) for x in all_data)
            self.live_stats['hmax'] = hmax
            self.hmax_label.setText(f"{hmax:.3f} m")
            
            # Hmean
            hmean = np.mean([abs(x) for x in all_data])
            self.live_stats['hmean'] = hmean
            self.hmean_label.setText(f"{hmean:.3f} m")
            
            # Tmean (période moyenne approximative)
            tmean = 2.0 + np.random.normal(0, 0.1)  # Simulation
            self.live_stats['tmean'] = tmean
            self.tmean_label.setText(f"{tmean:.2f} s")
    
    def _connect_unified_signals(self):
        """P0: Connecte les signaux unifiés pour mise à jour des 3 graphes"""
        if self.signal_bus:
            # dataBlockReady(ndarray) émis toutes les 0,5s
            self.signal_bus.dataBlockReady.connect(self._on_data_block_ready)
            
            # sessionFinished() émis après Stop
            self.signal_bus.sessionFinished.connect(self._on_session_finished)
        
        if self.error_bus:
            # error(str) pour affichage toast rouge
            self.error_bus.error_occurred.connect(self._on_error_occurred)
    
    @pyqtSlot(object)
    def _on_data_block_ready(self, data_block):
        """P0: Met à jour les 3 graphes avec dataBlockReady"""
        if not self.is_acquiring:
            return
            
        try:
            # Extraire données du data_block (objet DataBlock)
            if hasattr(data_block, 'data'):
                data = data_block.data
                timestamp = data_block.timestamp
            else:
                # Fallback pour dictionnaire (compatibilité)
                data = data_block.get('data', [])
                timestamp = data_block.get('timestamp', time.time())
            
            if len(data) == 0:
                return
                
            # Convertir en format pour GraphManager
            if isinstance(data, np.ndarray):
                if data.ndim == 1:
                    # Un seul échantillon multi-canal
                    signals = [data] if len(data) == self.n_sondes else [data[:self.n_sondes]]
                else:
                    # Plusieurs échantillons
                    signals = [data[:, i] if i < data.shape[1] else np.zeros(data.shape[0]) 
                              for i in range(self.n_sondes)]
            else:
                # Liste de valeurs
                signals = [np.array([data[i] if i < len(data) else 0.0]) for i in range(self.n_sondes)]
            
            # Créer vecteur temps
            if len(signals[0]) > 1:
                time_vector = np.linspace(timestamp - len(signals[0])/self.sample_rate, 
                                        timestamp, len(signals[0]))
            else:
                time_vector = np.array([timestamp])
            
            # P0: Mettre à jour les 3 graphes via GraphManager
            self.graph_manager.update_data(time_vector, signals)
            
            # Stocker pour export et stats
            for i, signal in enumerate(signals):
                if i < len(self.current_data):
                    if len(self.current_data[i]) > 1000:  # Limite mémoire
                        self.current_data[i] = self.current_data[i][-500:]
                    self.current_data[i].extend(signal.tolist())
            
            # Mise à jour compteurs
            self.total_samples += len(signals[0]) if signals else 0
            self.samples_label.setText(str(self.total_samples))
            
            # Mise à jour stats live
            self._update_live_stats()
            
        except Exception as e:
            print(f"Erreur _on_data_block_ready: {e}")
    
    @pyqtSlot()
    def _on_session_finished(self):
        """P0: Gère sessionFinished() - arrête acquisition et propose analyse"""
        if self.is_acquiring:
            self._stop_acquisition()
    
    @pyqtSlot(object)
    def _on_error_occurred(self, error_msg):
        """P0: Gère error(object) - affichage via ErrorBus"""
        # error_msg est un objet ErrorMessage
        if hasattr(error_msg, 'message'):
            print(f"Erreur acquisition: {error_msg.message}")
        else:
            print(f"Erreur acquisition: {error_msg}")
        # L'ErrorBus gère déjà l'affichage toast rouge via ViewManager

# Test standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    config = {
        'n_channels': 4,
        'sample_rate': 32.0,
        'duration': 300,
        'save_folder': './data'
    }
    
    view = AcquisitionView(config)
    view.show()
    
    sys.exit(app.exec_())