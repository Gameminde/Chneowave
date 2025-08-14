#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface de configuration de l'acquisition MCC DAQ pour CHNeoWave
Vue pour configurer et tester la carte USB-1608FS

Auteur: CHNeoWave Development Team
Version: 1.0.0
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QTabWidget, QTextEdit, QProgressBar, QCheckBox,
    QLineEdit, QFormLayout, QFrame, QSplitter,
    QHeaderView, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread, pyqtSignal
from PySide6.QtGui import QFont, QPixmap, QIcon

from ...acquisition.acquisition_controller import AcquisitionController, create_default_maritime_config
from ...acquisition.mcc_daq_wrapper import MCCRanges

logger = logging.getLogger(__name__)

class AcquisitionTestThread(QThread):
    """Thread pour les tests d'acquisition en arrière-plan"""
    data_received = pyqtSignal(object)
    status_updated = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, controller: AcquisitionController):
        super().__init__()
        self.controller = controller
        self.is_running = False
        
    def run(self):
        """Exécute le test d'acquisition"""
        self.is_running = True
        
        try:
            # Test d'acquisition courte
            success = self.controller.start_acquisition_session(
                "Test_Acquisition",
                sampling_rate=1000.0,
                duration_seconds=10.0
            )
            
            if success:
                while self.is_running and self.controller.is_acquiring:
                    status = self.controller.get_acquisition_status()
                    self.status_updated.emit(status)
                    
                    recent_data = self.controller.get_recent_data(100)
                    if recent_data:
                        self.data_received.emit(recent_data)
                        
                    self.msleep(500)  # Mise à jour toutes les 500ms
                    
        except Exception as e:
            self.error_occurred.emit(str(e))
            
    def stop(self):
        """Arrête le test"""
        self.is_running = False
        if self.controller.is_acquiring:
            self.controller.stop_acquisition()

class AcquisitionConfigView(QWidget):
    """
    Vue principale pour la configuration de l'acquisition MCC DAQ
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None
        self.test_thread = None
        self.update_timer = QTimer()
        
        self.setup_ui()
        self.setup_connections()
        self.initialize_controller()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setWindowTitle("Configuration Acquisition MCC DAQ USB-1608FS")
        self.setMinimumSize(1200, 800)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # En-tête
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panneau de configuration (gauche)
        config_widget = self.create_config_panel()
        splitter.addWidget(config_widget)
        
        # Panneau de surveillance (droite)
        monitor_widget = self.create_monitor_panel()
        splitter.addWidget(monitor_widget)
        
        # Splitter 70/30
        splitter.setSizes([700, 500])
        
    def create_header(self) -> QWidget:
        """Crée l'en-tête de l'interface"""
        header = QFrame()
        header.setFrameStyle(QFrame.StyledPanel)
        header.setMaximumHeight(80)
        
        layout = QHBoxLayout(header)
        
        # Titre et description
        title_layout = QVBoxLayout()
        
        title_label = QLabel("🌊 Acquisition Maritime MCC DAQ USB-1608FS")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1e3a5f;")
        
        subtitle_label = QLabel("Configuration et test de la carte d'acquisition 8 canaux simultanés")
        subtitle_label.setStyleSheet("color: #666; font-size: 11px;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Statut matériel
        self.hardware_status_label = QLabel("⚠️ Vérification...")
        self.hardware_status_label.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.hardware_status_label)
        
        return header
        
    def create_config_panel(self) -> QWidget:
        """Crée le panneau de configuration"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Onglets de configuration
        tab_widget = QTabWidget()
        
        # Onglet Matériel
        hardware_tab = self.create_hardware_tab()
        tab_widget.addTab(hardware_tab, "🔧 Matériel")
        
        # Onglet Canaux
        channels_tab = self.create_channels_tab()
        tab_widget.addTab(channels_tab, "📊 Canaux")
        
        # Onglet Acquisition
        acquisition_tab = self.create_acquisition_tab()
        tab_widget.addTab(acquisition_tab, "▶️ Acquisition")
        
        layout.addWidget(tab_widget)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        self.load_config_btn = QPushButton("📁 Charger Config")
        self.save_config_btn = QPushButton("💾 Sauver Config")
        self.reset_config_btn = QPushButton("🔄 Reset")
        self.test_connection_btn = QPushButton("🔍 Test Connexion")
        
        buttons_layout.addWidget(self.load_config_btn)
        buttons_layout.addWidget(self.save_config_btn)
        buttons_layout.addWidget(self.reset_config_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.test_connection_btn)
        
        layout.addLayout(buttons_layout)
        
        return widget
        
    def create_hardware_tab(self) -> QWidget:
        """Crée l'onglet de configuration matérielle"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Détection des cartes
        detection_group = QGroupBox("Détection du Matériel")
        detection_layout = QFormLayout(detection_group)
        
        self.board_combo = QComboBox()
        self.board_combo.setMinimumWidth(200)
        detection_layout.addRow("Carte Sélectionnée:", self.board_combo)
        
        self.scan_boards_btn = QPushButton("🔍 Scanner les Cartes")
        detection_layout.addRow("", self.scan_boards_btn)
        
        # Informations carte
        info_group = QGroupBox("Informations Carte")
        info_layout = QFormLayout(info_group)
        
        self.board_name_label = QLabel("Non détectée")
        self.dll_path_label = QLabel("Non trouvé")
        self.version_label = QLabel("Inconnue")
        
        info_layout.addRow("Nom de la Carte:", self.board_name_label)
        info_layout.addRow("Chemin DLLs:", self.dll_path_label)
        info_layout.addRow("Version Driver:", self.version_label)
        
        layout.addWidget(detection_group)
        layout.addWidget(info_group)
        layout.addStretch()
        
        return widget
        
    def create_channels_tab(self) -> QWidget:
        """Crée l'onglet de configuration des canaux"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Configuration globale
        global_group = QGroupBox("Configuration Globale")
        global_layout = QHBoxLayout(global_group)
        
        self.load_preset_btn = QPushButton("📋 Charger Preset Maritime")
        self.clear_channels_btn = QPushButton("🗑️ Effacer Tout")
        
        global_layout.addWidget(self.load_preset_btn)
        global_layout.addWidget(self.clear_channels_btn)
        global_layout.addStretch()
        
        layout.addWidget(global_group)
        
        # Table des canaux
        channels_group = QGroupBox("Configuration des Canaux (0-7)")
        channels_layout = QVBoxLayout(channels_group)
        
        self.channels_table = QTableWidget(8, 7)
        self.channels_table.setHorizontalHeaderLabels([
            "Canal", "Activé", "Type Capteur", "Étiquette", 
            "Plage (V)", "Sensibilité", "Unités"
        ])
        
        # Configuration de la table
        header = self.channels_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.channels_table.setAlternatingRowColors(True)
        
        channels_layout.addWidget(self.channels_table)
        
        # Initialisation de la table
        self.initialize_channels_table()
        
        layout.addWidget(channels_group)
        
        return widget
        
    def initialize_channels_table(self):
        """Initialise la table des canaux"""
        sensor_types = ["wave_height", "pressure", "accelerometer", "temperature", "generic"]
        voltage_ranges = ["±1V", "±2V", "±5V", "±10V"]
        
        for row in range(8):
            # Canal (lecture seule)
            self.channels_table.setItem(row, 0, QTableWidgetItem(str(row)))
            self.channels_table.item(row, 0).setFlags(Qt.ItemIsEnabled)
            
            # Activé (checkbox)
            checkbox = QCheckBox()
            checkbox.setChecked(row < 4)  # Activer les 4 premiers par défaut
            self.channels_table.setCellWidget(row, 1, checkbox)
            
            # Type de capteur
            sensor_combo = QComboBox()
            sensor_combo.addItems(sensor_types)
            if row < 2:
                sensor_combo.setCurrentText("wave_height")
            elif row == 2:
                sensor_combo.setCurrentText("pressure")
            elif row < 6:
                sensor_combo.setCurrentText("accelerometer")
            else:
                sensor_combo.setCurrentText("temperature")
            self.channels_table.setCellWidget(row, 2, sensor_combo)
            
            # Étiquette
            label_text = f"Canal {row}"
            if row < 2:
                label_text = f"Houle #{row+1}"
            elif row == 2:
                label_text = "Pression"
            elif row < 6:
                label_text = f"Accél. {'XYZ'[row-3]}"
            else:
                label_text = "Température"
                
            self.channels_table.setItem(row, 3, QTableWidgetItem(label_text))
            
            # Plage de tension
            range_combo = QComboBox()
            range_combo.addItems(voltage_ranges)
            range_combo.setCurrentText("±10V")
            self.channels_table.setCellWidget(row, 4, range_combo)
            
            # Sensibilité
            sensitivity = 1.0
            if row < 2:  # wave_height
                sensitivity = 2.0
            elif row == 2:  # pressure
                sensitivity = 0.01
            elif row >= 6:  # temperature
                sensitivity = 0.1
                
            self.channels_table.setItem(row, 5, QTableWidgetItem(str(sensitivity)))
            
            # Unités
            units = "V"
            if row < 2:
                units = "m"
            elif row == 2:
                units = "hPa"
            elif row < 6:
                units = "m/s²"
            else:
                units = "°C"
                
            self.channels_table.setItem(row, 6, QTableWidgetItem(units))
            
    def create_acquisition_tab(self) -> QWidget:
        """Crée l'onglet de configuration d'acquisition"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Paramètres d'acquisition
        params_group = QGroupBox("Paramètres d'Acquisition")
        params_layout = QFormLayout(params_group)
        
        self.sampling_rate_spin = QDoubleSpinBox()
        self.sampling_rate_spin.setRange(1.0, 50000.0)
        self.sampling_rate_spin.setValue(1000.0)
        self.sampling_rate_spin.setSuffix(" Hz")
        self.sampling_rate_spin.setDecimals(1)
        params_layout.addRow("Fréquence d'Échantillonnage:", self.sampling_rate_spin)
        
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.1, 3600.0)
        self.duration_spin.setValue(60.0)
        self.duration_spin.setSuffix(" s")
        self.duration_spin.setDecimals(1)
        params_layout.addRow("Durée d'Acquisition:", self.duration_spin)
        
        self.continuous_check = QCheckBox("Acquisition Continue")
        params_layout.addRow("", self.continuous_check)
        
        self.buffer_size_spin = QSpinBox()
        self.buffer_size_spin.setRange(1000, 100000)
        self.buffer_size_spin.setValue(10000)
        self.buffer_size_spin.setSuffix(" échantillons")
        params_layout.addRow("Taille Buffer:", self.buffer_size_spin)
        
        layout.addWidget(params_group)
        
        # Contrôles d'acquisition
        controls_group = QGroupBox("Contrôles")
        controls_layout = QHBoxLayout(controls_group)
        
        self.start_acquisition_btn = QPushButton("▶️ Démarrer Acquisition")
        self.start_acquisition_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        
        self.stop_acquisition_btn = QPushButton("⏹️ Arrêter")
        self.stop_acquisition_btn.setEnabled(False)
        self.stop_acquisition_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        
        self.test_acquisition_btn = QPushButton("🧪 Test Rapide")
        self.calibrate_btn = QPushButton("⚙️ Calibration")
        
        controls_layout.addWidget(self.start_acquisition_btn)
        controls_layout.addWidget(self.stop_acquisition_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.test_acquisition_btn)
        controls_layout.addWidget(self.calibrate_btn)
        
        layout.addWidget(controls_group)
        
        # Projet et export
        project_group = QGroupBox("Projet et Export")
        project_layout = QFormLayout(project_group)
        
        self.project_name_edit = QLineEdit("Acquisition_Maritime")
        project_layout.addRow("Nom du Projet:", self.project_name_edit)
        
        export_layout = QHBoxLayout()
        self.export_csv_btn = QPushButton("📊 Export CSV")
        self.export_json_btn = QPushButton("📄 Export JSON")
        export_layout.addWidget(self.export_csv_btn)
        export_layout.addWidget(self.export_json_btn)
        export_layout.addStretch()
        
        project_layout.addRow("Export:", export_layout)
        
        layout.addWidget(project_group)
        layout.addStretch()
        
        return widget
        
    def create_monitor_panel(self) -> QWidget:
        """Crée le panneau de surveillance"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Statut en temps réel
        status_group = QGroupBox("Statut Acquisition")
        status_layout = QFormLayout(status_group)
        
        self.acquisition_status_label = QLabel("⏸️ Arrêtée")
        self.samples_count_label = QLabel("0")
        self.acquisition_rate_label = QLabel("0.0 Hz")
        self.errors_count_label = QLabel("0")
        
        status_layout.addRow("Statut:", self.acquisition_status_label)
        status_layout.addRow("Échantillons:", self.samples_count_label)
        status_layout.addRow("Taux Réel:", self.acquisition_rate_label)
        status_layout.addRow("Erreurs:", self.errors_count_label)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addRow("Progression:", self.progress_bar)
        
        layout.addWidget(status_group)
        
        # Journal des événements
        log_group = QGroupBox("Journal des Événements")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
            }
        """)
        
        clear_log_btn = QPushButton("🗑️ Effacer Journal")
        
        log_layout.addWidget(self.log_text)
        log_layout.addWidget(clear_log_btn)
        
        layout.addWidget(log_group)
        
        # Données en temps réel
        data_group = QGroupBox("Aperçu Données Temps Réel")
        data_layout = QVBoxLayout(data_group)
        
        self.data_table = QTableWidget(0, 3)
        self.data_table.setHorizontalHeaderLabels(["Canal", "Valeur", "Unité"])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.setMaximumHeight(200)
        
        data_layout.addWidget(self.data_table)
        
        layout.addWidget(data_group)
        
        # Connexions
        clear_log_btn.clicked.connect(self.clear_log)
        
        return widget
        
    def setup_connections(self):
        """Configure les connexions des signaux"""
        # Boutons matériel
        self.scan_boards_btn.clicked.connect(self.scan_boards)
        self.test_connection_btn.clicked.connect(self.test_connection)
        
        # Boutons configuration
        self.load_preset_btn.clicked.connect(self.load_maritime_preset)
        self.clear_channels_btn.clicked.connect(self.clear_channels)
        self.load_config_btn.clicked.connect(self.load_configuration)
        self.save_config_btn.clicked.connect(self.save_configuration)
        self.reset_config_btn.clicked.connect(self.reset_configuration)
        
        # Boutons acquisition
        self.start_acquisition_btn.clicked.connect(self.start_acquisition)
        self.stop_acquisition_btn.clicked.connect(self.stop_acquisition)
        self.test_acquisition_btn.clicked.connect(self.test_acquisition)
        self.calibrate_btn.clicked.connect(self.calibrate_system)
        
        # Boutons export
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.export_json_btn.clicked.connect(self.export_json)
        
        # Timer pour mise à jour
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)  # Mise à jour chaque seconde
        
    def initialize_controller(self):
        """Initialise le contrôleur d'acquisition"""
        try:
            self.controller = AcquisitionController(self.data_received_callback)
            self.log_message("✅ Contrôleur d'acquisition initialisé")
            
            # Mise à jour de l'interface
            self.update_hardware_status()
            self.scan_boards()
            
        except Exception as e:
            self.log_message(f"❌ Erreur d'initialisation: {e}")
            
    def data_received_callback(self, data, session):
        """Callback appelé lors de réception de nouvelles données"""
        try:
            # Mise à jour de la table de données temps réel
            if hasattr(data, 'shape') and data.shape[1] > 0:
                self.update_realtime_data(data[-1])  # Dernière ligne
                
        except Exception as e:
            self.log_message(f"⚠️ Erreur callback données: {e}")
            
    def update_realtime_data(self, latest_sample):
        """Met à jour l'affichage des données temps réel"""
        if self.controller and self.controller.current_session:
            channels = self.controller.current_session.channels
            
            self.data_table.setRowCount(len(channels))
            
            for i, (channel_config, value) in enumerate(zip(channels, latest_sample)):
                self.data_table.setItem(i, 0, QTableWidgetItem(channel_config.label))
                self.data_table.setItem(i, 1, QTableWidgetItem(f"{value:.3f}"))
                self.data_table.setItem(i, 2, QTableWidgetItem(channel_config.physical_units))
                
    def scan_boards(self):
        """Scanner les cartes disponibles"""
        self.log_message("🔍 Scan des cartes MCC DAQ...")
        
        try:
            if self.controller:
                boards = self.controller.get_available_boards()
                
                self.board_combo.clear()
                if boards:
                    for board in boards:
                        self.board_combo.addItem(f"Carte {board}")
                    self.log_message(f"✅ {len(boards)} carte(s) détectée(s): {boards}")
                else:
                    self.board_combo.addItem("Aucune carte détectée")
                    self.log_message("⚠️ Aucune carte MCC DAQ détectée")
                    
                self.update_hardware_status()
                
        except Exception as e:
            self.log_message(f"❌ Erreur scan: {e}")
            
    def update_hardware_status(self):
        """Met à jour le statut matériel"""
        if self.controller and self.controller.is_hardware_available():
            self.hardware_status_label.setText("✅ Matériel Opérationnel")
            self.hardware_status_label.setStyleSheet("""
                QLabel {
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-radius: 4px;
                    padding: 8px 12px;
                    font-weight: bold;
                    color: #155724;
                }
            """)
        else:
            self.hardware_status_label.setText("⚠️ Mode Simulation")
            self.hardware_status_label.setStyleSheet("""
                QLabel {
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 4px;
                    padding: 8px 12px;
                    font-weight: bold;
                    color: #856404;
                }
            """)
            
    def test_connection(self):
        """Test la connexion avec la carte"""
        self.log_message("🔍 Test de connexion...")
        
        if not self.controller:
            self.log_message("❌ Pas de contrôleur disponible")
            return
            
        if self.controller.is_hardware_available():
            self.log_message("✅ Connexion matérielle OK")
            
            # Test de lecture d'un canal
            try:
                # Configuration d'un canal de test
                self.controller.configure_maritime_channel(0, 'generic', 'Test', 10.0, 1.0, 'V')
                self.log_message("✅ Configuration test OK")
                
            except Exception as e:
                self.log_message(f"⚠️ Erreur test: {e}")
        else:
            self.log_message("⚠️ Matériel non disponible - Mode simulation")
            
    def load_maritime_preset(self):
        """Charge le preset maritime par défaut"""
        self.log_message("📋 Chargement preset maritime...")
        
        try:
            default_config = create_default_maritime_config()
            
            # Application dans le contrôleur
            if self.controller:
                for channel, config in default_config.items():
                    self.controller.configure_maritime_channel(
                        config.channel,
                        config.sensor_type,
                        config.label,
                        10.0 if config.range_type.value == 1 else 5.0,
                        config.sensor_sensitivity,
                        config.physical_units
                    )
                    
            # Mise à jour de la table
            for row, (channel, config) in enumerate(default_config.items()):
                if row < self.channels_table.rowCount():
                    # Activé
                    checkbox = self.channels_table.cellWidget(row, 1)
                    if checkbox:
                        checkbox.setChecked(config.enabled)
                        
                    # Type capteur
                    sensor_combo = self.channels_table.cellWidget(row, 2)
                    if sensor_combo:
                        sensor_combo.setCurrentText(config.sensor_type)
                        
                    # Étiquette
                    self.channels_table.setItem(row, 3, QTableWidgetItem(config.label))
                    
                    # Sensibilité
                    self.channels_table.setItem(row, 5, QTableWidgetItem(str(config.sensor_sensitivity)))
                    
                    # Unités
                    self.channels_table.setItem(row, 6, QTableWidgetItem(config.physical_units))
                    
            self.log_message("✅ Preset maritime chargé")
            
        except Exception as e:
            self.log_message(f"❌ Erreur chargement preset: {e}")
            
    def clear_channels(self):
        """Efface la configuration des canaux"""
        reply = QMessageBox.question(
            self, "Confirmation", 
            "Êtes-vous sûr de vouloir effacer toute la configuration des canaux ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for row in range(self.channels_table.rowCount()):
                # Désactiver
                checkbox = self.channels_table.cellWidget(row, 1)
                if checkbox:
                    checkbox.setChecked(False)
                    
                # Reset étiquette
                self.channels_table.setItem(row, 3, QTableWidgetItem(f"Canal {row}"))
                
                # Reset sensibilité
                self.channels_table.setItem(row, 5, QTableWidgetItem("1.0"))
                
                # Reset unités
                self.channels_table.setItem(row, 6, QTableWidgetItem("V"))
                
            self.log_message("🗑️ Configuration des canaux effacée")
            
    def start_acquisition(self):
        """Démarre l'acquisition"""
        if not self.controller:
            self.log_message("❌ Pas de contrôleur disponible")
            return
            
        try:
            # Configuration des canaux actifs
            self.apply_channels_configuration()
            
            # Paramètres d'acquisition
            project_name = self.project_name_edit.text() or "Acquisition_Maritime"
            sampling_rate = self.sampling_rate_spin.value()
            duration = None if self.continuous_check.isChecked() else self.duration_spin.value()
            
            # Canaux actifs
            active_channels = []
            for row in range(self.channels_table.rowCount()):
                checkbox = self.channels_table.cellWidget(row, 1)
                if checkbox and checkbox.isChecked():
                    active_channels.append(row)
                    
            if not active_channels:
                self.log_message("⚠️ Aucun canal activé")
                return
                
            # Démarrage
            success = self.controller.start_acquisition_session(
                project_name, sampling_rate, duration, active_channels
            )
            
            if success:
                self.log_message(f"▶️ Acquisition démarrée: {project_name}")
                self.start_acquisition_btn.setEnabled(False)
                self.stop_acquisition_btn.setEnabled(True)
                
                if duration:
                    self.progress_bar.setMaximum(int(duration))
                    self.progress_bar.setValue(0)
                    self.progress_bar.setVisible(True)
                else:
                    self.progress_bar.setVisible(False)
                    
            else:
                self.log_message("❌ Erreur de démarrage d'acquisition")
                
        except Exception as e:
            self.log_message(f"❌ Erreur démarrage: {e}")
            
    def stop_acquisition(self):
        """Arrête l'acquisition"""
        if self.controller and self.controller.is_acquiring:
            success = self.controller.stop_acquisition()
            if success:
                self.log_message("⏹️ Acquisition arrêtée")
            else:
                self.log_message("⚠️ Erreur d'arrêt")
                
        self.start_acquisition_btn.setEnabled(True)
        self.stop_acquisition_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
    def test_acquisition(self):
        """Lance un test d'acquisition rapide"""
        if self.test_thread and self.test_thread.isRunning():
            self.log_message("⚠️ Test déjà en cours")
            return
            
        self.log_message("🧪 Démarrage test d'acquisition...")
        
        # Configuration des canaux pour le test
        self.apply_channels_configuration()
        
        # Lancement du thread de test
        self.test_thread = AcquisitionTestThread(self.controller)
        self.test_thread.data_received.connect(self.test_data_received)
        self.test_thread.status_updated.connect(self.test_status_updated)
        self.test_thread.error_occurred.connect(self.test_error_occurred)
        self.test_thread.finished.connect(self.test_finished)
        
        self.test_acquisition_btn.setEnabled(False)
        self.test_thread.start()
        
    def test_data_received(self, data):
        """Callback pour données de test"""
        if data and 'sample_count' in data:
            self.log_message(f"📊 Test: {data['sample_count']} échantillons reçus")
            
    def test_status_updated(self, status):
        """Callback pour statut de test"""
        if 'statistics' in status:
            stats = status['statistics']
            rate = stats.get('acquisition_rate', 0)
            samples = stats.get('samples_acquired', 0)
            self.log_message(f"📈 Test: {samples} échantillons, {rate:.1f} Hz")
            
    def test_error_occurred(self, error):
        """Callback pour erreur de test"""
        self.log_message(f"❌ Erreur test: {error}")
        
    def test_finished(self):
        """Callback fin de test"""
        self.log_message("✅ Test d'acquisition terminé")
        self.test_acquisition_btn.setEnabled(True)
        
    def calibrate_system(self):
        """Lance la calibration du système"""
        if not self.controller:
            self.log_message("❌ Pas de contrôleur disponible")
            return
            
        self.log_message("⚙️ Calibration système...")
        
        try:
            results = self.controller.calibrate_system()
            
            if results and 'channels' in results:
                self.log_message(f"✅ Calibration terminée: {len(results['channels'])} canaux")
                for channel, result in results['channels'].items():
                    status = result.get('calibration_status', 'unknown')
                    self.log_message(f"  Canal {channel}: {status}")
            else:
                self.log_message("⚠️ Calibration sans résultats")
                
        except Exception as e:
            self.log_message(f"❌ Erreur calibration: {e}")
            
    def apply_channels_configuration(self):
        """Applique la configuration des canaux au contrôleur"""
        if not self.controller:
            return
            
        for row in range(self.channels_table.rowCount()):
            checkbox = self.channels_table.cellWidget(row, 1)
            if checkbox and checkbox.isChecked():
                # Récupération des paramètres
                sensor_combo = self.channels_table.cellWidget(row, 2)
                range_combo = self.channels_table.cellWidget(row, 4)
                
                sensor_type = sensor_combo.currentText() if sensor_combo else 'generic'
                range_text = range_combo.currentText() if range_combo else '±10V'
                
                label_item = self.channels_table.item(row, 3)
                sensitivity_item = self.channels_table.item(row, 5)
                units_item = self.channels_table.item(row, 6)
                
                label = label_item.text() if label_item else f"Canal {row}"
                sensitivity = float(sensitivity_item.text()) if sensitivity_item else 1.0
                units = units_item.text() if units_item else 'V'
                
                # Conversion plage
                range_volts = 10.0
                if '±1V' in range_text:
                    range_volts = 1.0
                elif '±2V' in range_text:
                    range_volts = 2.0
                elif '±5V' in range_text:
                    range_volts = 5.0
                    
                # Configuration
                self.controller.configure_maritime_channel(
                    row, sensor_type, label, range_volts, sensitivity, units
                )
                
    def update_display(self):
        """Met à jour l'affichage en temps réel"""
        if not self.controller:
            return
            
        try:
            status = self.controller.get_acquisition_status()
            
            # Statut acquisition
            if status['is_acquiring']:
                self.acquisition_status_label.setText("▶️ En cours")
                self.acquisition_status_label.setStyleSheet("color: green; font-weight: bold;")
                
                # Mise à jour progression si durée définie
                if self.progress_bar.isVisible() and 'session' in status:
                    session = status['session']
                    duration_sec = session.get('duration_seconds', 0)
                    if duration_sec > 0:
                        self.progress_bar.setValue(int(duration_sec))
            else:
                self.acquisition_status_label.setText("⏸️ Arrêtée")
                self.acquisition_status_label.setStyleSheet("color: red; font-weight: bold;")
                
            # Statistiques
            stats = status.get('statistics', {})
            self.samples_count_label.setText(str(stats.get('samples_acquired', 0)))
            self.acquisition_rate_label.setText(f"{stats.get('acquisition_rate', 0):.1f} Hz")
            self.errors_count_label.setText(str(stats.get('errors', 0)))
            
        except Exception as e:
            # Log silencieux pour éviter le spam
            pass
            
    def export_csv(self):
        """Exporte les données en CSV"""
        if not self.controller or not self.controller.current_session:
            self.log_message("⚠️ Pas de session active à exporter")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter CSV", 
            f"{self.controller.current_session.session_id}.csv",
            "Fichiers CSV (*.csv)"
        )
        
        if file_path:
            try:
                success = self.controller.export_session_data(file_path, 'csv')
                if success:
                    self.log_message(f"📊 Export CSV réussi: {file_path}")
                else:
                    self.log_message("❌ Erreur export CSV")
            except Exception as e:
                self.log_message(f"❌ Erreur export: {e}")
                
    def export_json(self):
        """Exporte les métadonnées en JSON"""
        if not self.controller or not self.controller.current_session:
            self.log_message("⚠️ Pas de session active à exporter")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter JSON", 
            f"{self.controller.current_session.session_id}.json",
            "Fichiers JSON (*.json)"
        )
        
        if file_path:
            try:
                success = self.controller.export_session_data(file_path, 'json')
                if success:
                    self.log_message(f"📄 Export JSON réussi: {file_path}")
                else:
                    self.log_message("❌ Erreur export JSON")
            except Exception as e:
                self.log_message(f"❌ Erreur export: {e}")
                
    def load_configuration(self):
        """Charge une configuration depuis un fichier"""
        self.log_message("📁 Chargement configuration - Non implémenté")
        
    def save_configuration(self):
        """Sauvegarde la configuration dans un fichier"""
        self.log_message("💾 Sauvegarde configuration - Non implémenté")
        
    def reset_configuration(self):
        """Reset la configuration"""
        reply = QMessageBox.question(
            self, "Confirmation", 
            "Êtes-vous sûr de vouloir réinitialiser toute la configuration ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clear_channels()
            self.project_name_edit.setText("Acquisition_Maritime")
            self.sampling_rate_spin.setValue(1000.0)
            self.duration_spin.setValue(60.0)
            self.continuous_check.setChecked(False)
            self.log_message("🔄 Configuration réinitialisée")
            
    def clear_log(self):
        """Efface le journal"""
        self.log_text.clear()
        
    def log_message(self, message: str):
        """Ajoute un message au journal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_text.append(formatted_message)
        
        # Auto-scroll vers le bas
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def closeEvent(self, event):
        """Événement de fermeture"""
        if self.controller and self.controller.is_acquiring:
            reply = QMessageBox.question(
                self, "Acquisition en cours", 
                "Une acquisition est en cours. Voulez-vous l'arrêter et fermer ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.controller.stop_acquisition()
            else:
                event.ignore()
                return
                
        if self.test_thread and self.test_thread.isRunning():
            self.test_thread.stop()
            self.test_thread.wait(3000)
            
        if self.controller:
            self.controller.close()
            
        event.accept()

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    window = AcquisitionConfigView()
    window.show()
    
    sys.exit(app.exec())

