import sys
import os
import json
import csv
import time
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
    QFileDialog, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox, QFrame, QScrollArea, QCheckBox,
    QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QDialogButtonBox, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QPalette, QColor
import pyqtgraph as pg
import traceback
# Legacy import removed - Traitementdonneé deprecated
from hardware_adapter import HardwareAcquisitionAdapter
from .controllers.acquisition_controller import AcquisitionController
from processing_worker import ProcessingWorker, LatencyMonitor
from hrneowave.core.circular_buffer import CircularBuffer

# --- Constante Globale ---
MAX_SONDES_PERMITTED = 16


def set_light_mode(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(240, 240, 240))
    palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(200, 200, 200))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    app.setPalette(palette)
    app.setStyleSheet('''
        QWidget {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
            color: #000; 
        }
        QLabel#titleLabel {
            font-size: 22px; 
            font-weight: bold;
            color: #00bfff;
            letter-spacing: 1px; 
            padding-bottom: 10px;
            margin-bottom: 10px; 
        }
        QLabel#leftPanelTitleLabel {
            font-size: 18px; 
            font-weight: bold;
            color: #00bfff;
            padding-bottom: 8px;
            margin-bottom: 8px;
        }
        QLineEdit, QSpinBox, QComboBox {
            background-color: #f0f0f0;
            border: 1px solid #aaa; 
            border-radius: 6px;
            padding: 6px 10px; 
            color: #000;
            min-height: 20px; 
        }
        QTableWidget {
            background-color: #f0f0f0;
            border: 1px solid #aaa;
            border-radius: 6px;
            color: #000;
            gridline-color: #aaa;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            color: #00bfff;
            font-weight: bold;
            padding: 4px;
            border-bottom: 1px solid #aaa; 
            border-right: 1px solid #aaa;
        }
        QComboBox::drop-down { border: none; }
        QPushButton {
            background: #00bfff;
            color: white;
            border-radius: 8px;
            padding: 9px 20px; 
            font-weight: bold;
            font-size: 14px;
            min-height: 22px; 
        }
        QPushButton:hover {
            background: #005fa3;
        }
        QPushButton:disabled {
            background-color: #aaa;
            color: #777;
        }
        QGroupBox { font-weight: bold; color: #00bfff; margin-top: 8px; padding-top: 12px; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px 2px 5px; left: 7px; } 
        QScrollArea { border: 1px solid #aaa; background-color: #f0f0f0; border-radius: 4px;} 
        QCheckBox { padding: 5px; color: #000; } 
    ''')

def set_dark_mode(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 36))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(24, 24, 28))
    palette.setColor(QPalette.AlternateBase, QColor(36, 36, 42))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0)) 
    palette.setColor(QPalette.Text, QColor(220, 220, 220))    
    palette.setColor(QPalette.Button, QColor(40, 40, 48))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220)) 
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    app.setStyleSheet('''
        QWidget {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
            color: #e0e0e0; 
        }
        QLabel#titleLabel {
            font-size: 22px; 
            font-weight: bold;
            color: #00bfff;
            letter-spacing: 1px; 
            padding-bottom: 10px;
            margin-bottom: 10px; 
        }
        QLabel#leftPanelTitleLabel {
            font-size: 18px; 
            font-weight: bold;
            color: #00bfff;
            padding-bottom: 8px;
            margin-bottom: 8px;
        }
        QLineEdit, QSpinBox, QComboBox {
            background-color: #23232b;
            border: 1px solid #505058; 
            border-radius: 6px;
            padding: 6px 10px; 
            color: #e0e0e0;
            min-height: 20px; 
        }
        QTableWidget {
            background-color: #23232b;
            border: 1px solid #505058;
            border-radius: 6px;
            color: #e0e0e0;
            gridline-color: #3a3a42;
        }
        QHeaderView::section {
            background-color: #2c2c34;
            color: #00bfff;
            font-weight: bold;
            padding: 4px;
            border-bottom: 1px solid #444; 
            border-right: 1px solid #3a3a42;
        }
        QComboBox::drop-down { border: none; }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00bfff, stop:1 #005fa3);
            color: white;
            border-radius: 8px;
            padding: 9px 20px; 
            font-weight: bold;
            font-size: 14px;
            min-height: 22px; 
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #005fa3, stop:1 #00bfff);
        }
        QPushButton:disabled {
            background-color: #35353f;
            color: #777;
        }
        QGroupBox { font-weight: bold; color: #00bfff; margin-top: 8px; padding-top: 12px; }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px 2px 5px; left: 7px; } 
        QScrollArea { border: 1px solid #3a3a42; background-color: #202026; border-radius: 4px;} 
        QCheckBox { padding: 5px; color: #e0e0e0; } 
        QCheckBox::indicator { 
            width: 16px; height: 16px; 
            border-radius: 4px; 
            border: 1px solid #777; 
            background-color: #2c2c34; 
        }
        QCheckBox::indicator:checked { 
            background-color: #00bfff; 
            border: 1px solid #00bfff; 
        }
        QCheckBox::indicator:disabled { background-color: #444; border: 1px solid #555; }
    ''')

def analyse_vagues_zero_crossing(time, eta):
    eta = np.asarray(eta)
    time = np.asarray(time)
    if len(eta) < 4 or len(time) < 4:
        return {"Hmax": np.nan, "Hmin": np.nan, "Hmean": np.nan, "Tmax": np.nan, "Tmin": np.nan, "Tmean": np.nan, "Nwaves": 0}
    eta_centered = eta - np.mean(eta)
    crossings = np.where((eta_centered[:-1] < 0) & (eta_centered[1:] >= 0))[0]
    t_up = []
    for idx in crossings:
        t0, t1 = time[idx], time[idx+1]
        y0, y1 = eta_centered[idx], eta_centered[idx+1]
        if y1 - y0 == 0: continue
        t_cross = t0 - y0 * (t1 - t0) / (y1 - y0)
        t_up.append(t_cross)
    t_up = np.array(t_up)
    H_list, T_list = [], []
    for k in range(len(t_up)-1):
        mask = (time >= t_up[k]) & (time < t_up[k+1])
        if not np.any(mask): continue
        eta_vague = eta_centered[mask]
        H = np.max(eta_vague) - np.min(eta_vague)
        T = t_up[k+1] - t_up[k]
        H_list.append(H)
        T_list.append(T)
    H_arr = np.array(H_list)
    T_arr = np.array(T_list)
    return {
        "Hmax": np.max(H_arr) if H_arr.size else np.nan,
        "Hmin": np.min(H_arr) if H_arr.size else np.nan,
        "Hmean": np.mean(H_arr) if H_arr.size else np.nan,
        "Tmax": np.max(T_arr) if T_arr.size else np.nan,
        "Tmin": np.min(T_arr) if T_arr.size else np.nan,
        "Tmean": np.mean(T_arr) if T_arr.size else np.nan,
        "Nwaves": len(H_arr)
    }

class ProbePositionDialog(QDialog):
    """Dialog pour configurer les positions des sondes"""
    def __init__(self, n_sondes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration des positions des sondes")
        self.setModal(True)
        self.positions = []
        
        layout = QVBoxLayout()
        
        # Info importante
        info_label = QLabel("⚠️ Entrez la distance de chaque sonde depuis la structure réfléchissante (en mètres)")
        info_label.setStyleSheet("color: #00bfff; font-weight: bold;")
        layout.addWidget(info_label)
        
        # Profondeur d'eau
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Profondeur d'eau (m):"))
        self.depth_input = QDoubleSpinBox()
        self.depth_input.setRange(0.1, 10.0)
        self.depth_input.setValue(0.5)
        self.depth_input.setSingleStep(0.1)
        depth_layout.addWidget(self.depth_input)
        layout.addLayout(depth_layout)
        
        # Positions des sondes
        self.position_inputs = []
        for i in range(n_sondes):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(f"Sonde {i+1} - Distance (m):"))
            pos_input = QDoubleSpinBox()
            pos_input.setRange(0.0, 100.0)
            pos_input.setValue(0.5 + i * 0.3)  # Espacement par défaut 30cm
            pos_input.setSingleStep(0.01)
            self.position_inputs.append(pos_input)
            h_layout.addWidget(pos_input)
            layout.addLayout(h_layout)
        
        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_positions(self):
        """Retourne les positions et la profondeur"""
        positions = [input.value() for input in self.position_inputs]
        depth = self.depth_input.value()
        return positions, depth

class RealTimeAcquisitionWindow(QWidget):
    def __init__(self, n_sondes, freq, duree, save_folder, sonde_names, calibration_params, calib_file_name, parent_setup_window=None):
        super().__init__()
        self.setWindowTitle("Acquisition Temps Réel - HRNeoWave")
        self.resize(1600, 900) 
        
        self.n_sondes_total_calib = n_sondes 
        self.freq = freq
        self.duree_s = duree 
        self.save_folder = save_folder
        self.sonde_names_calib = sonde_names
        self.calibration_params_all = calibration_params 
        self.calib_file_name_short = os.path.basename(calib_file_name) if calib_file_name else "N/A"
        self.calib_file_path_full = calib_file_name
        self.parent_setup_window = parent_setup_window

        self.data_storage_full = [[] for _ in range(self.n_sondes_total_calib)]
        self.time_storage_full = []
        
        self.sample_count = 0
        self.max_samples = int(self.duree_s * self.freq)
        self.running = False

        # Nouveau système d'acquisition avec buffer circulaire
        try:
            from hrneowave.core.circular_buffer import BufferConfig, create_circular_buffer
            buffer_config = BufferConfig(
                n_channels=self.n_sondes_total_calib,
                buffer_size=int(self.freq * 60),  # 60s de buffer
                sample_rate=self.freq
            )
            self.circular_buffer = create_circular_buffer(buffer_config)
            print(f"✅ Buffer circulaire initialisé: {self.n_sondes_total_calib} canaux, {int(self.freq * 60)} échantillons")
        except Exception as e:
            print(f"⚠️ Erreur initialisation buffer: {e}")
            self.circular_buffer = None
        
        # Créer la configuration pour AcquisitionController
        try:
            from .controllers.acquisition_controller import AcquisitionConfig, AcquisitionMode
            acquisition_config = AcquisitionConfig(
                mode=AcquisitionMode.SIMULATE,
                sample_rate=self.freq,
                n_channels=self.n_sondes_total_calib,
                buffer_size=int(self.freq * 60)  # 1 minute de buffer
            )
            self.acquisition_controller = AcquisitionController(acquisition_config)
            print(f"✅ Contrôleur d'acquisition initialisé: mode=simulate, fs={self.freq}Hz")
        except Exception as e:
            print(f"⚠️ Erreur initialisation contrôleur: {e}")
            self.acquisition_controller = None
        
        # Worker de traitement en temps réel
        processing_config = {
            'sample_rate': self.freq,
            'n_channels': self.n_sondes_total_calib,
            'window_size': 1024,
            'overlap': 0.5,
            'update_interval': 0.05,  # 50ms
            'water_depth': 10.0,
            'probe_positions': [(i * 1.0, 0.0) for i in range(self.n_sondes_total_calib)]
        }
        self.processing_worker = ProcessingWorker(self, processing_config)
        
        # Moniteur de latence
        self.latency_monitor = LatencyMonitor()
        
        # Timer PyQtGraph haute fréquence (15ms = ~67 FPS)
        self.plot_refresh_timer = QTimer(self)
        self.plot_refresh_timer.timeout.connect(self.update_pyqtgraph_plots)
        self.plot_refresh_interval = 15  # 15ms pour 67 FPS
        
        # Timer pour mise à jour des infos (plus lent)
        self.info_update_timer = QTimer(self)
        self.info_update_timer.timeout.connect(self.update_info_display)
        
        # Variables pour les données temps réel
        self.current_spectra = {}
        self.current_stats = {'Hs': 0.0, 'Tp': 0.0, 'Cr': 0.0}
        self.last_read_time = 0
        
        self.curves_for_all_sondes_plot = []
        self.individual_plot_selectors = [] 
        
        self.theme_switch = QCheckBox("Mode sombre")
        self.theme_switch.setChecked(True)
        self.theme_switch.stateChanged.connect(self.toggle_theme)
        
        self.next_step = QPushButton("Continuer")
        self.next_step.setMinimumHeight(40)
        
        # Initialize DataProcessingWindow
        self.traitement = DataProcessingWindow(self)
        
        # Initialize hardware adapter
        self.hardware_adapter = HardwareAcquisitionAdapter(self)
        
        # Connecter les signaux du ProcessingWorker
        self._connect_processing_signals()
        
        self._init_modern_ui_layout()
        
        # Ajouter barre de statut pour latence
        self._init_status_bar()
    
    def _connect_processing_signals(self):
        """Connecte les signaux du ProcessingWorker"""
        self.processing_worker.newSpectra.connect(self.on_new_spectra)
        self.processing_worker.newStats.connect(self.on_new_stats)
        self.processing_worker.processingError.connect(self.on_processing_error)
        self.processing_worker.performanceStats.connect(self.on_performance_update)
    
    def _init_status_bar(self):
        """Initialise la barre de statut simplifiée"""
        if not hasattr(self, 'status_bar'):
            self.status_bar = QStatusBar()
            self.status_label = QLabel("Prêt pour l'acquisition")
            self.status_label.setStyleSheet("color: #50fa7b; font-weight: bold; padding: 5px;")
            
            self.status_bar.addWidget(self.status_label)
            self.status_bar.setStyleSheet("""
                QStatusBar {
                    background-color: #2a2a30;
                    border-top: 1px solid #444;
                    color: #c8c8c8;
                    font-size: 12px;
                }
            """)
            
            # Ajouter à la layout principale si elle existe
            if hasattr(self, 'layout') and self.layout():
                self.layout().addWidget(self.status_bar)
    
    @pyqtSlot(dict)
    def on_new_spectra(self, spectra_data):
        """Reçoit les nouveaux spectres du ProcessingWorker"""
        self.current_spectra = spectra_data
        self.last_read_time = time.time()
    
    @pyqtSlot(dict)
    def on_new_stats(self, stats_data):
        """Reçoit les nouvelles statistiques du ProcessingWorker"""
        self.current_stats = stats_data
        
        # Mettre à jour l'affichage des statistiques temps réel
        self.update_realtime_stats_display(stats_data)
    
    @pyqtSlot(str)
    def on_processing_error(self, error_msg):
        """Gère les erreurs de traitement"""
        print(f"❌ Erreur traitement: {error_msg}")
        if hasattr(self, 'status_label'):
            self.status_label.setText(f"Erreur: {error_msg}")
    
    @pyqtSlot(dict)
    def on_performance_update(self, perf_data):
        """Met à jour les indicateurs de performance (simplifié)"""
        # Performance monitoring en arrière-plan sans affichage
        pass

    def _init_modern_ui_layout(self):
        """Interface moderne optimisée pour plein écran avec proportions nombre d'or"""
        # Configuration de la fenêtre pour plein écran avec proportions nombre d'or
        golden_ratio = 1.618
        min_width = 1200
        min_height = int(min_width / golden_ratio)  # 741
        self.setMinimumSize(min_width, min_height)
        
        # Taille initiale optimisée
        initial_width = 1366
        initial_height = int(initial_width / golden_ratio)  # 844
        self.resize(initial_width, initial_height)
        
        # Layout principal avec proportions optimisées (38% panneau, 62% graphiques)
        main_hbox_layout = QHBoxLayout(self) 
        main_hbox_layout.setContentsMargins(6, 6, 6, 6)  # Marges réduites pour plein écran
        main_hbox_layout.setSpacing(8)

        # --- Panneau de Gauche ---
        left_panel_scroll_area = QScrollArea() 
        left_panel_scroll_area.setWidgetResizable(True)
        left_panel_scroll_area.setFrameShape(QFrame.NoFrame)
        left_panel_scroll_area.setStyleSheet("""
            QScrollArea { 
                background-color: #25252c; 
                border-radius: 8px;
                border: 1px solid #444;
            }
        """)
        
        left_panel_widget = QWidget() 
        # IMPORTANT : Faire de left_panel_vbox un attribut de classe
        self.left_panel_vbox = QVBoxLayout(left_panel_widget)
        self.left_panel_vbox.setContentsMargins(12,12,12,12) 
        self.left_panel_vbox.setSpacing(12) 
        self.left_panel_vbox.setAlignment(Qt.AlignTop)

        # En-tête avec titre et commutateur de thème
        header_layout = QVBoxLayout()
        panel_title_label = QLabel("Tableau de Bord d'Acquisition")
        panel_title_label.setObjectName("leftPanelTitleLabel") 
        panel_title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(panel_title_label)
        
        # Commutateur de thème dans l'en-tête
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        self.theme_switch.setText("Mode Sombre")
        self.theme_switch.setStyleSheet("""
            QCheckBox {
                color: #c8c8c8;
                font-size: 11px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        theme_layout.addWidget(self.theme_switch)
        theme_layout.addStretch()
        header_layout.addLayout(theme_layout)
        
        self.left_panel_vbox.addLayout(header_layout)

        # Setup hardware controls APRÈS la création de left_panel_vbox
        if hasattr(self, 'hardware_adapter'):
            self.hardware_adapter.setup_hardware_controls()

        # Infos Session avec style amélioré
        general_info_group = QGroupBox("📊 Informations de Session")
        general_info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #444;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                color: #00bfff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)
        general_info_layout = QFormLayout(general_info_group)
        general_info_layout.setSpacing(10)
        general_info_layout.setLabelAlignment(Qt.AlignLeft)
        general_info_layout.setFormAlignment(Qt.AlignLeft)
        
        self.elapsed_time_label = QLabel("00:00 / --:--")
        self.elapsed_time_label.setStyleSheet("font-weight: bold; color: #50fa7b; font-size: 13px;")
        
        self.calib_file_display_label = QLabel(self.calib_file_name_short)
        self.calib_file_display_label.setToolTip(self.calib_file_path_full)
        self.calib_file_display_label.setStyleSheet("color: #c8c8c8; font-size: 11px;")
        
        self.sample_counter_label = QLabel("0 / 0")
        self.sample_counter_label.setStyleSheet("color: #c8c8c8; font-size: 11px;")
        
        general_info_layout.addRow("📁 Fichier Calibration:", self.calib_file_display_label)
        general_info_layout.addRow("📈 Progression:", self.sample_counter_label)
        general_info_layout.addRow("⏱️ Durée:", self.elapsed_time_label) 
        self.left_panel_vbox.addWidget(general_info_group)

        # Sélection Graphes Individuels avec style amélioré
        indiv_selectors_group = QGroupBox("📈 Graphiques Individuels")
        indiv_selectors_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #444;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                color: #ff79c6;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)
        indiv_selectors_layout_main = QVBoxLayout(indiv_selectors_group)
        indiv_selectors_layout_main.setSpacing(12)
        
        for i in range(2): 
            selector_form_layout = QFormLayout() 
            selector_form_layout.setSpacing(8)
            
            # Labels avec icônes et couleurs
            if i == 0:
                label = QLabel("🔵 Graphique 1:")
                label.setStyleSheet("color: #8be9fd; font-weight: bold; font-size: 11px;")
            else:
                label = QLabel("🟢 Graphique 2:")
                label.setStyleSheet("color: #50fa7b; font-weight: bold; font-size: 11px;")
            
            combo = QComboBox()
            combo.setStyleSheet("""
                QComboBox {
                    padding: 6px;
                    border: 1px solid #555;
                    border-radius: 4px;
                    background-color: #2b2b2b;
                    color: #f8f8f2;
                    font-size: 10px;
                    min-height: 20px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 20px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 4px solid #f8f8f2;
                }
                QComboBox QAbstractItemView {
                    background-color: #2b2b2b;
                    color: #f8f8f2;
                    selection-background-color: #44475a;
                }
            """)
            
            if self.sonde_names_calib:
                combo.addItems(self.sonde_names_calib)
                default_idx = i if i < self.n_sondes_total_calib and i < len(self.sonde_names_calib) else 0
                if self.n_sondes_total_calib > 0:
                    combo.setCurrentIndex(default_idx)
            self.individual_plot_selectors.append(combo)
            selector_form_layout.addRow(label, combo)
            indiv_selectors_layout_main.addLayout(selector_form_layout)
        self.left_panel_vbox.addWidget(indiv_selectors_group)

        # Sondes sur Graphe Global avec style amélioré
        global_plot_selector_group = QGroupBox("🌐 Vue Globale - Sélection Sondes")
        global_plot_selector_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #444;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                color: #ffb86c;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)
        global_plot_selector_scroll_layout = QVBoxLayout(global_plot_selector_group)
        global_plot_scroll_area = QScrollArea()
        global_plot_scroll_area.setWidgetResizable(True)
        global_plot_scroll_area.setStyleSheet("""
            QScrollArea { 
                min-height: 120px; 
                max-height: 200px;
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #2b2b2b;
            }
            QScrollBar:vertical {
                background-color: #44475a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #6272a4;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #8be9fd;
            }
        """)
        
        global_plot_scroll_content_widget = QWidget()
        self.global_plot_checkboxes_layout = QVBoxLayout(global_plot_scroll_content_widget)
        self.global_plot_checkboxes_layout.setSpacing(6) 
        self.global_plot_checkboxes_layout.setContentsMargins(8,8,8,8) 
        
        self.global_plot_checkboxes_list = []
        for i in range(self.n_sondes_total_calib):
            sonde_name = self.sonde_names_calib[i]
            checkbox = QCheckBox(f"📊 {sonde_name}")
            checkbox.setChecked(False)
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #f8f8f2;
                    font-size: 10px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 2px solid #6272a4;
                    border-radius: 3px;
                    background-color: #2b2b2b;
                }
                QCheckBox::indicator:checked {
                    background-color: #50fa7b;
                    border-color: #50fa7b;
                }
                QCheckBox::indicator:hover {
                    border-color: #8be9fd;
                }
            """)
            checkbox.stateChanged.connect(self.update_global_plot_visibility_trigger)
            self.global_plot_checkboxes_layout.addWidget(checkbox)
            self.global_plot_checkboxes_list.append(checkbox)
        
        self.global_plot_checkboxes_layout.addStretch(1)
        global_plot_scroll_area.setWidget(global_plot_scroll_content_widget)
        global_plot_selector_scroll_layout.addWidget(global_plot_scroll_area)
        self.left_panel_vbox.addWidget(global_plot_selector_group, stretch=1)

        # Statistiques avec style amélioré
        stats_group = QGroupBox("📈 Statistiques Temps Réel")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #444;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                color: #bd93f9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_table_widget = QTableWidget()
        self.stats_table_widget.setColumnCount(3)
        self.stats_table_widget.setHorizontalHeaderLabels(["📊 Sonde", "🌊 Hmax (m)", "⏱️ Tmean (s)"])
        self.stats_table_widget.setRowCount(self.n_sondes_total_calib)
        self.stats_table_widget.verticalHeader().setVisible(False)
        self.stats_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stats_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Style du tableau
        self.stats_table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: #f8f8f2;
                border: 1px solid #555;
                border-radius: 4px;
                gridline-color: #44475a;
                font-size: 10px;
            }
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid #44475a;
            }
            QTableWidget::item:selected {
                background-color: #44475a;
            }
            QHeaderView::section {
                background-color: #44475a;
                color: #f8f8f2;
                padding: 6px;
                border: 1px solid #555;
                font-weight: bold;
                font-size: 9px;
            }
        """)
        
        for i in range(self.n_sondes_total_calib):
            name_item = QTableWidgetItem(self.sonde_names_calib[i])
            hmax_item = QTableWidgetItem("N/A")
            tmean_item = QTableWidgetItem("N/A")
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            hmax_item.setTextAlignment(Qt.AlignCenter)
            tmean_item.setTextAlignment(Qt.AlignCenter)
            self.stats_table_widget.setItem(i, 0, name_item)
            self.stats_table_widget.setItem(i, 1, hmax_item)
            self.stats_table_widget.setItem(i, 2, tmean_item)
        
        stats_layout.addWidget(self.stats_table_widget)
        self.left_panel_vbox.addWidget(stats_group, stretch=2)
        
        # Boutons de contrôle avec style amélioré
        self.start_button = QPushButton("▶️ Démarrer l'Acquisition")
        self.start_button.setMinimumHeight(45)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #50fa7b;
                color: #282a36;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5af78e;
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background-color: #4dd865;
            }
            QPushButton:disabled {
                background-color: #6272a4;
                color: #44475a;
            }
        """)
        self.start_button.clicked.connect(self.start_acquisition_timers)
        self.left_panel_vbox.addWidget(self.start_button)

        # Style pour le bouton suivant
        self.next_step.setEnabled(False)
        self.next_step.setStyleSheet("""
            QPushButton {
                background-color: #ff79c6;
                color: #282a36;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                padding: 6px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #ff92d0;
            }
            QPushButton:disabled {
                background-color: #6272a4;
                color: #44475a;
            }
        """)
        self.left_panel_vbox.addWidget(self.next_step)

        left_panel_scroll_area.setWidget(left_panel_widget)
        # Proportions nombre d'or: 38% panneau gauche
        main_hbox_layout.addWidget(left_panel_scroll_area, stretch=38)

        # --- Zone de Graphiques à Droite ---
        right_plotting_area_vbox = QVBoxLayout()
        right_plotting_area_vbox.setSpacing(6)  # Espacement réduit pour plein écran
        right_plotting_area_vbox.setContentsMargins(0, 0, 0, 0)

        # Graphe 1
        self.plot_widget_1 = pg.PlotWidget()
        title_g1_plot = self.individual_plot_selectors[0].currentText() if self.sonde_names_calib and self.individual_plot_selectors else "Graphe 1"
        self.apply_plot_style(self.plot_widget_1, f"Signal: {title_g1_plot}")
        self.curve_plot_1 = self.plot_widget_1.plot([], [], pen=pg.mkPen('#00bfff', width=2))
        right_plotting_area_vbox.addWidget(self.plot_widget_1, stretch=1)

        # Graphe 2
        self.plot_widget_2 = pg.PlotWidget()
        title_g2_plot = self.individual_plot_selectors[1].currentText() if len(self.individual_plot_selectors) > 1 and self.sonde_names_calib else "Graphe 2"
        self.apply_plot_style(self.plot_widget_2, f"Signal: {title_g2_plot}")
        self.curve_plot_2 = self.plot_widget_2.plot([], [], pen=pg.mkPen('#ff8800', width=2))
        right_plotting_area_vbox.addWidget(self.plot_widget_2, stretch=1)
        
        # Graphe global
        self.plot_widget_all_sondes_display = pg.PlotWidget()
        self.apply_plot_style(self.plot_widget_all_sondes_display, "Vue Globale (Sondes Sélectionnées)")
        
        if self.sonde_names_calib: 
            for i in range(self.n_sondes_total_calib):
                curve = self.plot_widget_all_sondes_display.plot([], [], 
                                                pen=pg.mkPen(pg.intColor(i, hues=self.n_sondes_total_calib, sat=255), width=2), 
                                                name=self.sonde_names_calib[i])
                curve.hide() 
                self.curves_for_all_sondes_plot.append(curve)
            
            if self.n_sondes_total_calib > 0: 
                self.legend_all_sondes = self.plot_widget_all_sondes_display.addLegend(offset=(10,10), brush=QColor(50,50,50,180), labelTextColor='w')
        
        right_plotting_area_vbox.addWidget(self.plot_widget_all_sondes_display, stretch=1)
        
        # Proportions nombre d'or: 62% zone graphique
        main_hbox_layout.addLayout(right_plotting_area_vbox, stretch=62)

        # Connexions
        if len(self.individual_plot_selectors) > 0:
            self.individual_plot_selectors[0].currentIndexChanged.connect(
                lambda: self.update_selected_sonde_for_plot(0, self.plot_widget_1, self.curve_plot_1))
        
        if len(self.individual_plot_selectors) > 1: 
            self.individual_plot_selectors[1].currentIndexChanged.connect(
                lambda: self.update_selected_sonde_for_plot(1, self.plot_widget_2, self.curve_plot_2))
    
    def update_global_plot_visibility_trigger(self):
        """Pour un effet immédiat"""
        self.refresh_all_plots_and_info()

    def apply_plot_style(self, plot_widget, title_text):
        plot_widget.setBackground('#23232b')
        plot_widget.setTitle(title_text, color="#00bfff", size="12pt")
        plot_widget.showGrid(x=True, y=True, alpha=0.2)
        axis_pen = pg.mkPen(color=(180, 180, 180), width=1)
        text_pen = pg.mkPen(color=(180, 180, 180))
        left_axis = plot_widget.getAxis('left')
        left_axis.setPen(axis_pen); left_axis.setTextPen(text_pen)
        left_axis.setLabel('Amplitude (m)', color='#c8c8c8')
        bottom_axis = plot_widget.getAxis('bottom')
        bottom_axis.setPen(axis_pen); bottom_axis.setTextPen(text_pen)
        bottom_axis.setLabel('Temps (s)', color='#c8c8c8')
        plot_widget.setYRange(-4.0, 4.0, padding=0.1) 
        plot_widget.setXRange(0, min(10.0, float(self.duree_s)), padding=0.02)

    def update_selected_sonde_for_plot(self, selector_idx, plot_widget_ref, curve_ref):
        if not self.sonde_names_calib or selector_idx >= len(self.individual_plot_selectors): 
            return
        
        combo_box = self.individual_plot_selectors[selector_idx]
        selected_sonde_name_in_combo = combo_box.currentText()
        plot_widget_ref.setTitle(f"Signal: {selected_sonde_name_in_combo}", color="#00bfff", size="12pt")
        
        curve_ref.setData([], []) 
        # Forcer une mise à jour pour voir le changement immédiatement
        self.refresh_all_plots_and_info()

    def acquire_data_sample(self):
        """Acquisition d'un échantillon de données"""
        if not self.running:
            return
        
        if self.sample_count >= self.max_samples:
            self.finalize_acquisition()
            return

        current_t = self.sample_count / self.freq
        self.time_storage_full.append(current_t)

        # Vérifier si hardware connecté
        hardware_connected = (hasattr(self, 'hardware_adapter') and 
                             hasattr(self.hardware_adapter, 'is_connected') and 
                             self.hardware_adapter.is_connected)
        
        if hardware_connected:
            try:
                # Lire tous les canaux actifs
                raw_values = self.hardware_adapter.hardware.read_all_channels()
                for i in range(self.n_sondes_total_calib):
                    if i < len(raw_values):
                        raw_value = raw_values[i]
                        calib = self.calibration_params_all[i]
                        calibrated_value = raw_value * calib['slope'] + calib['intercept']
                        if calib.get('unit', 'm') == 'cm':
                            calibrated_value /= 100.0
                        self.data_storage_full[i].append(calibrated_value)
                    else:
                        self.data_storage_full[i].append(0.0)
            except Exception as e:
                print(f"❌ Erreur acquisition hardware: {e}")
                # Fallback sur données simulées
                self._generate_simulated_data(current_t)
        else:
            # Mode simulation si pas de hardware
            self._generate_simulated_data(current_t)

        self.sample_count += 1

    def _generate_simulated_data(self, current_t):
        """Génère des données simulées pour toutes les sondes"""
        for i in range(self.n_sondes_total_calib):
            # Paramètres de simulation
            frequency = 1.5 + i * 0.1  # Fréquences légèrement différentes
            amplitude = 3.0 - i * 0.2  # Amplitudes décroissantes
            phase = i * np.pi / 4      # Déphasage entre sondes
            
            # Signal sinusoïdal avec bruit
            value = amplitude * np.sin(2 * np.pi * frequency * current_t + phase)
            value += 0.1 * np.random.randn()  # Ajouter du bruit
            
            self.data_storage_full[i].append(value)

    def start_acquisition_timers(self):
        """Démarre l'acquisition temps réel avec ProcessingWorker"""
        if self.running:
            print("⚠️ Acquisition déjà en cours")
            return
        
        print("🚀 Démarrage de l'acquisition temps réel...")
        
        # Réinitialiser les données
        self.running = True
        self.sample_count = 0
        self.time_storage_full = []
        self.data_storage_full = [[] for _ in range(self.n_sondes_total_calib)]
        
        # Nettoyer les graphiques PyQtGraph
        self._clear_pyqtgraph_plots()
        
        # Démarrer l'acquisition controller
        try:
            self.acquisition_controller.start_acquisition()
            print("✅ AcquisitionController démarré")
        except Exception as e:
            print(f"❌ Erreur démarrage acquisition: {e}")
            self.running = False
            return
        
        # Démarrer le worker de traitement
        try:
            self.processing_worker.start_processing()
            print("✅ ProcessingWorker démarré")
        except Exception as e:
            print(f"❌ Erreur démarrage traitement: {e}")
            self.acquisition_controller.stop_acquisition()
            self.running = False
            return
        
        # Démarrer les timers PyQtGraph
        self.plot_refresh_timer.start(self.plot_refresh_interval)
        self.info_update_timer.start(500)  # Mise à jour info toutes les 500ms
        
        # Mettre à jour l'interface
        self.start_button.setText("⏸️ Acquisition en cours...")
        self.start_button.setEnabled(False)
        
        if hasattr(self, 'status_label'):
            self.status_label.setText("Acquisition en cours")
        
        print(f"✅ Acquisition temps réel démarrée:")
        print(f"   - Fréquence d'acquisition: {self.freq} Hz")
        print(f"   - Refresh PyQtGraph: {1000/self.plot_refresh_interval:.1f} FPS")
        print(f"   - Durée totale: {self.duree_s} s")
        print(f"   - Buffer circulaire: {self.circular_buffer.max_size} échantillons")
    
    def _clear_pyqtgraph_plots(self):
        """Nettoie tous les graphiques PyQtGraph"""
        if hasattr(self, 'curve_plot_1'): 
            self.curve_plot_1.setData([], [])
        if hasattr(self, 'curve_plot_2'): 
            self.curve_plot_2.setData([], [])
        if hasattr(self, 'curves_for_all_sondes_plot'):
            for curve in self.curves_for_all_sondes_plot: 
                if curve:
                    curve.setData([], [])
                    curve.hide()
    
    def update_pyqtgraph_plots(self):
        """Met à jour les graphiques PyQtGraph en temps réel (67 FPS)"""
        if not self.running:
            return
        
        plot_start_time = time.time()
        
        try:
            # Récupérer les données du buffer circulaire
            window_size = int(self.freq * 10)  # 10 secondes de données
            data = self.circular_buffer.get_data(window_size)
            
            if data is None or len(data) < 10:
                return
            
            # Créer le vecteur temps
            n_samples = len(data)
            time_vector = np.arange(n_samples) / self.freq
            
            # Mettre à jour les graphiques individuels
            self._update_individual_plots(time_vector, data)
            
            # Mettre à jour le graphique global
            self._update_global_plot(time_vector, data)
            
            # Mettre à jour le moniteur de latence
            if hasattr(self, 'latency_monitor') and self.last_read_time > 0:
                self.latency_monitor.add_measurement(self.last_read_time, plot_start_time)
            
        except Exception as e:
            print(f"❌ Erreur mise à jour PyQtGraph: {e}")
    
    def _update_individual_plots(self, time_vector, data):
        """Met à jour les graphiques individuels"""
        if len(self.individual_plot_selectors) == 0 or not self.sonde_names_calib:
            return
        
        # Graphique 1
        if hasattr(self, 'curve_plot_1') and len(self.individual_plot_selectors) > 0:
            idx1 = self.individual_plot_selectors[0].currentIndex()
            if 0 <= idx1 < data.shape[1]:
                self.curve_plot_1.setData(time_vector, data[:, idx1])
        
        # Graphique 2
        if hasattr(self, 'curve_plot_2') and len(self.individual_plot_selectors) > 1:
            idx2 = self.individual_plot_selectors[1].currentIndex()
            if 0 <= idx2 < data.shape[1]:
                self.curve_plot_2.setData(time_vector, data[:, idx2])
    
    def _update_global_plot(self, time_vector, data):
        """Met à jour le graphique global avec les sondes sélectionnées"""
        if not hasattr(self, 'global_plot_checkboxes_list'):
            return
        
        for i, checkbox in enumerate(self.global_plot_checkboxes_list):
            if i >= len(self.curves_for_all_sondes_plot):
                continue
            
            curve = self.curves_for_all_sondes_plot[i]
            if curve is None:
                continue
            
            if checkbox.isChecked() and i < data.shape[1]:
                curve.setData(time_vector, data[:, i])
                curve.show()
            else:
                curve.hide()
    
    def update_info_display(self):
        """Met à jour l'affichage des informations (500ms)"""
        if not self.running:
            return
        
        # Calculer le temps écoulé
        buffer_usage = self.circular_buffer.get_usage()
        elapsed_time = buffer_usage / self.freq if buffer_usage > 0 else 0
        
        # Mettre à jour les labels de temps
        if hasattr(self, 'elapsed_time_label'):
            el_m, el_s = divmod(int(elapsed_time), 60)
            tot_m, tot_s = divmod(int(self.duree_s), 60)
            self.elapsed_time_label.setText(f"Durée: {el_m:02d}:{el_s:02d} / {tot_m:02d}:{tot_s:02d}")
        
        # Mettre à jour le compteur d'échantillons
        if hasattr(self, 'sample_counter_label'):
            self.sample_counter_label.setText(f"Échantillons: {buffer_usage} / {self.max_samples}")
        
        # Vérifier si l'acquisition doit se terminer
        if elapsed_time >= self.duree_s:
            self.finalize_acquisition()
    
    def update_realtime_stats_display(self, stats_data):
        """Met à jour l'affichage des statistiques temps réel"""
        if not hasattr(self, 'stats_table_widget'):
            return
        
        try:
            # Afficher Hs, Tp, Cr dans les premières lignes
            if self.stats_table_widget.rowCount() > 0:
                # Ligne 0: Hs
                if self.stats_table_widget.item(0, 1):
                    hs_value = stats_data.get('Hs', 0.0)
                    self.stats_table_widget.item(0, 1).setText(f"{hs_value:.3f}")
                
                # Ligne 1: Tp si disponible
                if self.stats_table_widget.rowCount() > 1 and self.stats_table_widget.item(1, 2):
                    tp_value = stats_data.get('Tp', 0.0)
                    self.stats_table_widget.item(1, 2).setText(f"{tp_value:.2f}")
        
        except Exception as e:
            print(f"❌ Erreur mise à jour stats: {e}")

    def refresh_all_plots_and_info(self):
        try:
            elapsed_s_display = self.time_storage_full[-1] if self.running and self.time_storage_full else \
                                self.duree_s if not self.running and self.sample_count >= self.max_samples else 0
            total_s_display = self.duree_s
            el_m_display, el_s_display = divmod(int(elapsed_s_display), 60)
            tot_m_display, tot_s_display = divmod(int(total_s_display), 60)
            if hasattr(self, 'elapsed_time_label'):
                self.elapsed_time_label.setText(f"Durée: {el_m_display:02d}:{el_s_display:02d} / {tot_m_display:02d}:{tot_s_display:02d}")
            if hasattr(self, 'sample_counter_label'):
                 self.sample_counter_label.setText(f"Échantillons: {self.sample_count} / {self.max_samples}")

            if not self.time_storage_full:
                if hasattr(self, 'stats_table_widget'):
                    for i in range(self.n_sondes_total_calib):
                        if self.stats_table_widget.item(i,1): self.stats_table_widget.item(i,1).setText("N/A")
                        if self.stats_table_widget.item(i,2): self.stats_table_widget.item(i,2).setText("N/A")
                return

            display_window_duration_s = 10.0 
            num_points_in_window = int(display_window_duration_s * self.freq) 
            
            if len(self.time_storage_full) > num_points_in_window:
                start_idx = len(self.time_storage_full) - num_points_in_window
                time_to_display = self.time_storage_full[start_idx:]
                data_to_display = [self.data_storage_full[k][start_idx:] if k < len(self.data_storage_full) else [] for k in range(self.n_sondes_total_calib)]
            else:
                time_to_display = self.time_storage_full[:] 
                data_to_display = [sonde_data[:] for sonde_data in self.data_storage_full]
            
            if not time_to_display: return

            # Mise à jour du tableau de statistiques
            if hasattr(self, 'stats_table_widget'):
                for sonde_idx in range(self.n_sondes_total_calib):
                    hmax_str, tmean_str = "N/A", "N/A"
                    if sonde_idx < len(data_to_display) and data_to_display[sonde_idx]:
                        try:
                            signal_vals = np.array(data_to_display[sonde_idx])
                            time_vals = np.array(time_to_display)
                            if len(signal_vals) > 20:
                                stats = analyse_vagues_zero_crossing(time_vals, signal_vals)
                                if not np.isnan(stats["Hmax"]): hmax_str = f"{stats['Hmax']:.3f}"
                                if not np.isnan(stats["Tmean"]): tmean_str = f"{stats['Tmean']:.2f}"
                        except Exception as e_stat:
                            hmax_str = "Err"
                            tmean_str = "Err"

                    if self.stats_table_widget.item(sonde_idx,1): 
                        self.stats_table_widget.item(sonde_idx,1).setText(hmax_str)
                    if self.stats_table_widget.item(sonde_idx,2): 
                        self.stats_table_widget.item(sonde_idx,2).setText(tmean_str)

            # Mise à jour des courbes des graphes INDIVIDUELS
            if self.sonde_names_calib:
                if len(self.individual_plot_selectors) > 0 and hasattr(self, 'curve_plot_1') and self.curve_plot_1:
                    idx1 = self.individual_plot_selectors[0].currentIndex()
                    if 0 <= idx1 < self.n_sondes_total_calib and idx1 < len(data_to_display) and data_to_display[idx1]:
                        min_len = min(len(time_to_display), len(data_to_display[idx1]))
                        if min_len > 0:
                            self.curve_plot_1.setData(time_to_display[:min_len], data_to_display[idx1][:min_len])
                        else:
                            self.curve_plot_1.setData([], [])
                    else: 
                        self.curve_plot_1.setData([], [])
                
                if len(self.individual_plot_selectors) > 1 and hasattr(self, 'curve_plot_2') and self.curve_plot_2:
                    idx2 = self.individual_plot_selectors[1].currentIndex()
                    if 0 <= idx2 < self.n_sondes_total_calib and idx2 < len(data_to_display) and data_to_display[idx2]:
                        min_len = min(len(time_to_display), len(data_to_display[idx2]))
                        if min_len > 0:
                            self.curve_plot_2.setData(time_to_display[:min_len], data_to_display[idx2][:min_len])
                        else:
                            self.curve_plot_2.setData([], [])
                    else: 
                        self.curve_plot_2.setData([], [])

            # Mise à jour du Graphe GLOBAL
            for i in range(self.n_sondes_total_calib):
                if not (i < len(self.curves_for_all_sondes_plot) and i < len(self.global_plot_checkboxes_list)):
                    continue

                curve = self.curves_for_all_sondes_plot[i]
                checkbox = self.global_plot_checkboxes_list[i]
                if curve is None: continue
                
                try:
                    if checkbox.isChecked():
                        if i < len(data_to_display) and data_to_display[i] and time_to_display:
                            sonde_data_slice = data_to_display[i]
                            min_len = min(len(time_to_display), len(sonde_data_slice))
                            if min_len > 0:
                                curve.setData(time_to_display[:min_len], sonde_data_slice[:min_len])
                                curve.show()
                            else:
                                curve.setData([], [])
                                curve.hide()
                        else:
                            curve.setData([], [])
                            curve.hide()
                    else:
                        curve.setData([], [])
                        curve.hide()
                except Exception as e_plot_global_curve:
                    print(f"ERREUR MAJ courbe globale (sonde {i}): {e_plot_global_curve}")
                    if curve.isVisible(): curve.hide()
            
            # Mise à jour des plages d'affichage
            if time_to_display: 
                max_t_disp = time_to_display[-1]
                min_t_disp = time_to_display[0]
                for pw_widget in [self.plot_widget_1, self.plot_widget_2, self.plot_widget_all_sondes_display]:
                    if pw_widget: 
                        try: 
                            pw_widget.setXRange(min_t_disp, max_t_disp, padding=0.02)
                            # Set y range to fit amplitude exactly (±3.5 to show ±3 with margin)
                            pw_widget.setYRange(-3.5, 3.5, padding=0)
                        except Exception as e_range: 
                            print(f"Erreur Range: {e_range}")

        except Exception as e_refresh_main: 
            print(f"ERREUR CRITIQUE dans refresh_all_plots_and_info: {e_refresh_main}")
            traceback.print_exc()

    def finalize_acquisition(self):
        """Finalise l'acquisition temps réel et sauvegarde les données"""
        if not self.running:
            return
            
        print("🏁 Finalisation de l'acquisition temps réel...")
        
        # Arrêter l'acquisition
        self.running = False
        
        # Arrêter les timers PyQtGraph
        if hasattr(self, 'plot_refresh_timer') and self.plot_refresh_timer.isActive(): 
            self.plot_refresh_timer.stop()
        if hasattr(self, 'info_update_timer') and self.info_update_timer.isActive(): 
            self.info_update_timer.stop()
        
        # Arrêter le worker de traitement
        if hasattr(self, 'processing_worker'):
            try:
                self.processing_worker.stop_processing()
                print("✅ ProcessingWorker arrêté")
            except Exception as e:
                print(f"❌ Erreur arrêt ProcessingWorker: {e}")
        
        # Arrêter l'acquisition controller
        if hasattr(self, 'acquisition_controller'):
            try:
                self.acquisition_controller.stop_acquisition()
                print("✅ AcquisitionController arrêté")
            except Exception as e:
                print(f"❌ Erreur arrêt AcquisitionController: {e}")
        
        print("⏹️ Système d'acquisition arrêté")
        
        # Récupérer les données finales du buffer
        self._extract_final_data_from_buffer()
        
        # Mise à jour finale des graphiques
        self._final_plot_update()
        
        # Réactiver le bouton de démarrage
        self.start_button.setText("▶️ Démarrer l'acquisition")
        self.start_button.setEnabled(True)
        
        # Activer le bouton suivant
        if hasattr(self, 'next_step'):
            self.next_step.setEnabled(True)
        
        # Mettre à jour la barre de statut
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage("Acquisition terminée", 3000)
        
        # Sauvegarder les données
        saved_file = self.save_all_data_to_csv()
        
        if saved_file:
            self.saved_data_file = saved_file
            print(f"✅ Données sauvegardées: {saved_file}")
            
            # Lancer automatiquement le traitement
            if hasattr(self, 'traitement'):
                self.process_data()
        else:
            print("❌ Échec de la sauvegarde des données")
    
    def _extract_final_data_from_buffer(self):
        """Extrait les données finales du buffer circulaire"""
        if not hasattr(self, 'circular_buffer'):
            return
        
        try:
            # Récupérer toutes les données du buffer
            all_data = self.circular_buffer.get_all_data()
            
            if all_data is not None and len(all_data) > 0:
                # Convertir en format compatible avec l'ancien système
                n_samples = len(all_data)
                n_channels = all_data.shape[1] if len(all_data.shape) > 1 else 1
                
                # Créer le vecteur temps
                self.time_storage_full = list(np.arange(n_samples) / self.freq)
                
                # Extraire les données par canal
                self.data_storage_full = []
                for ch in range(n_channels):
                    if len(all_data.shape) > 1:
                        channel_data = all_data[:, ch].tolist()
                    else:
                        channel_data = all_data.tolist()
                    self.data_storage_full.append(channel_data)
                
                self.sample_count = n_samples
                print(f"✅ Données extraites du buffer: {n_samples} échantillons, {n_channels} canaux")
            else:
                print("⚠️ Aucune donnée dans le buffer circulaire")
                
        except Exception as e:
            print(f"❌ Erreur extraction données buffer: {e}")
    
    def _final_plot_update(self):
        """Mise à jour finale des graphiques avec toutes les données"""
        try:
            if not self.time_storage_full or not self.data_storage_full:
                return
            
            time_vector = np.array(self.time_storage_full)
            
            # Mettre à jour les graphiques individuels
            if hasattr(self, 'curve_plot_1') and len(self.individual_plot_selectors) > 0:
                idx1 = self.individual_plot_selectors[0].currentIndex()
                if 0 <= idx1 < len(self.data_storage_full):
                    self.curve_plot_1.setData(time_vector, self.data_storage_full[idx1])
            
            if hasattr(self, 'curve_plot_2') and len(self.individual_plot_selectors) > 1:
                idx2 = self.individual_plot_selectors[1].currentIndex()
                if 0 <= idx2 < len(self.data_storage_full):
                    self.curve_plot_2.setData(time_vector, self.data_storage_full[idx2])
            
            # Mettre à jour le graphique global
            if hasattr(self, 'global_plot_checkboxes_list'):
                for i, checkbox in enumerate(self.global_plot_checkboxes_list):
                    if i >= len(self.curves_for_all_sondes_plot) or i >= len(self.data_storage_full):
                        continue
                    
                    curve = self.curves_for_all_sondes_plot[i]
                    if curve is None:
                        continue
                    
                    if checkbox.isChecked():
                        curve.setData(time_vector, self.data_storage_full[i])
                        curve.show()
                    else:
                        curve.hide()
            
            print("✅ Graphiques finaux mis à jour")
            
        except Exception as e:
            print(f"❌ Erreur mise à jour graphiques finaux: {e}")
    
    def process_data(self):
        print("Démarrage du traitement des données...")
        if hasattr(self, 'saved_data_file'):
            # Pass the saved file path to the processing window
            self.traitement.load_data(self.saved_data_file)
        
    def save_all_data_to_csv(self) -> str:
        if not self.time_storage_full:
            print("Aucune donnée à enregistrer.")
            return

        from datetime import datetime
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"acquisition_HRNeoWave_{timestamp_str}.csv"
        save_directory = self.save_folder if self.save_folder and os.path.isdir(self.save_folder) else os.getcwd()
        
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier d'acquisition", 
                                                  os.path.join(save_directory, default_filename),
                                                  "Fichiers CSV (*.csv);;Tous les fichiers (*)", options=options)
        if not filename:
            print("Sauvegarde annulée.")
            QMessageBox.information(self, "Sauvegarde Annulée", "L'enregistrement a été annulé.")
            return 

        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                header = ["Temps_s"] + (self.sonde_names_calib if self.sonde_names_calib else [f"Sonde_{i+1}" for i in range(self.n_sondes_total_calib)])
                writer.writerow(header)
                for i in range(len(self.time_storage_full)):
                    row = [f"{self.time_storage_full[i]:.4f}"] + [f"{self.data_storage_full[j][i]:.4f}" if j < len(self.data_storage_full) and i < len(self.data_storage_full[j]) else '' for j in range(self.n_sondes_total_calib)]
                    writer.writerow(row)
            print(f"Données enregistrées avec succès dans : {filename}")
            QMessageBox.information(self, "Sauvegarde Réussie", f"Données enregistrées dans : {filename}")
            return filename
        except IOError as e:
            QMessageBox.critical(self, "Erreur Sauvegarde Fichier", f"Impossible d'écrire : {filename}\n{e}")
            return None
        except Exception as e:
            QMessageBox.critical(self, "Erreur Sauvegarde", f"Erreur inattendue : {e}")
            return None

    def closeEvent(self, event):
        print("Fermeture de RealTimeAcquisitionWindow...")
        if self.running : 
            reply = QMessageBox.question(self, 'Confirmation Fermeture', 
                                         "L'acquisition est en cours. Voulez-vous vraiment arrêter, sauvegarder et quitter ?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.finalize_acquisition() 
                # Déconnecter le hardware
                self._cleanup_resources()
                if self.parent_setup_window:
                    self.parent_setup_window.setEnabled(True) 
                    self.parent_setup_window.rt_acquisition_window = None 
                super().closeEvent(event)
            else:
                event.ignore() 
                return
        else: 
            # Arrêter tous les timers et workers
            self._stop_all_timers_and_workers()
            # Déconnecter le hardware
            self._cleanup_resources()
            if self.parent_setup_window:
                self.parent_setup_window.setEnabled(True) 
                self.parent_setup_window.rt_acquisition_window = None 
            super().closeEvent(event)
    
    def _stop_all_timers_and_workers(self):
        """Arrête tous les timers et workers"""
        # Arrêter les timers PyQtGraph
        if hasattr(self, 'plot_refresh_timer') and self.plot_refresh_timer.isActive(): 
            self.plot_refresh_timer.stop()
        if hasattr(self, 'info_update_timer') and self.info_update_timer.isActive(): 
            self.info_update_timer.stop()
        
        # Arrêter le worker de traitement
        if hasattr(self, 'processing_worker'):
            try:
                self.processing_worker.stop_processing()
            except Exception as e:
                print(f"❌ Erreur arrêt ProcessingWorker lors de la fermeture: {e}")
        
        # Arrêter l'acquisition controller
        if hasattr(self, 'acquisition_controller'):
            try:
                self.acquisition_controller.stop_acquisition()
            except Exception as e:
                print(f"❌ Erreur arrêt AcquisitionController lors de la fermeture: {e}")
    
    def _cleanup_resources(self):
        """Nettoie toutes les ressources"""
        # Déconnecter le hardware
        if hasattr(self, 'hardware_adapter'):
            try:
                self.hardware_adapter.disconnect_device()
            except Exception as e:
                print(f"❌ Erreur déconnexion hardware: {e}")
        
        # Nettoyer le buffer circulaire
        if hasattr(self, 'circular_buffer') and self.circular_buffer:
            try:
                self.circular_buffer.reset()
                print("✅ Buffer circulaire nettoyé")
            except Exception as e:
                print(f"❌ Erreur nettoyage buffer: {e}")

    def toggle_theme(self):
        """Bascule entre thème sombre et clair"""
        try:
            if hasattr(self, 'theme_switch') and self.theme_switch.isChecked():
                self._apply_dark_theme()
                print("✅ Thème sombre activé")
            else:
                self._apply_light_theme()
                print("✅ Thème clair activé")
        except Exception as e:
            print(f"⚠️ Erreur changement thème: {e}")

    def _apply_dark_theme(self):
        """Applique le thème sombre"""
        try:
            app = QApplication.instance()
            if app:
                dark_style = """
                QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QGroupBox {
                    background-color: #3c3c3c;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    color: #ffffff;
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QPushButton {
                    background-color: #0078d4;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QScrollArea {
                    background-color: #25252c;
                    border: none;
                }
                QTableWidget {
                    background-color: #2b2b2b;
                    alternate-background-color: #3c3c3c;
                    gridline-color: #555555;
                }
                """
                app.setStyleSheet(dark_style)
                # S'assurer que l'attribut current_theme est défini
                self.current_theme = "dark"
                # Synchroniser le commutateur de thème si il existe
                if hasattr(self, 'theme_switch'):
                    self.theme_switch.setChecked(True)
                print("✅ Thème sombre appliqué")
        except Exception as e:
            print(f"⚠️ Erreur application thème sombre: {e}")
            # S'assurer que current_theme est défini même en cas d'erreur
            self.current_theme = "dark"

    def _apply_light_theme(self):
        """Applique le thème clair"""
        try:
            app = QApplication.instance()
            if app:
                light_style = """
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QMainWindow {
                    background-color: #ffffff;
                }
                QGroupBox {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    color: #000000;
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QPushButton {
                    background-color: #0078d4;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QScrollArea {
                    background-color: #f8f8f8;
                    border: none;
                }
                QTableWidget {
                    background-color: #ffffff;
                    alternate-background-color: #f0f0f0;
                    gridline-color: #cccccc;
                }
                """
                app.setStyleSheet(light_style)
                # S'assurer que l'attribut current_theme est défini
                self.current_theme = "light"
                # Synchroniser le commutateur de thème si il existe
                if hasattr(self, 'theme_switch'):
                    self.theme_switch.setChecked(False)
                print("✅ Thème clair appliqué")
        except Exception as e:
            print(f"⚠️ Erreur application thème clair: {e}")
            # S'assurer que current_theme est défini même en cas d'erreur
            self.current_theme = "light"

    def sync_theme_switch(self, theme):
        """Synchronise le commutateur de thème"""
        if hasattr(self, 'theme_switch'):
            if theme == "dark":
                self.theme_switch.setChecked(True)
            else:
                self.theme_switch.setChecked(False)

    def resizeEvent(self, event):
        """Gère le redimensionnement de la fenêtre en maintenant les proportions"""
        super().resizeEvent(event)
        try:
            # Maintenir les proportions du nombre d'or lors du redimensionnement
            new_size = event.size()
            width = new_size.width()
            height = new_size.height()
            
            # Calculer la hauteur idéale basée sur le nombre d'or
            golden_ratio = 1.618
            ideal_height = int(width / golden_ratio)
            
            # Ajuster si nécessaire (avec une tolérance plus large pour éviter les boucles)
            if abs(height - ideal_height) > 100 and width > 800:  # Tolérance élargie
                # Éviter les redimensionnements en boucle
                if not hasattr(self, '_resizing') or not self._resizing:
                    self._resizing = True
                    QTimer.singleShot(50, lambda: self._delayed_resize(width, ideal_height))
                
        except Exception as e:
            print(f"⚠️ Erreur redimensionnement: {e}")
    
    def _delayed_resize(self, width, height):
        """Redimensionnement différé pour éviter les boucles"""
        try:
            self.resize(width, height)
            self._resizing = False
        except Exception as e:
            print(f"⚠️ Erreur redimensionnement différé: {e}")
            self._resizing = False

    def showEvent(self, event):
        """Événement d'affichage de la fenêtre"""
        super().showEvent(event)
        try:
            # Initialiser l'attribut current_theme s'il n'existe pas
            if not hasattr(self, 'current_theme'):
                self.current_theme = "dark"
            
            # Initialiser l'attribut _resizing pour éviter les boucles de redimensionnement
            if not hasattr(self, '_resizing'):
                self._resizing = False
            
            # Appliquer le thème par défaut
            self._apply_dark_theme()
            
            # Vérifier et ajuster la géométrie si nécessaire
            self._ensure_golden_ratio_geometry()
            
            print("✅ Interface d'acquisition initialisée avec thème sombre")
        except Exception as e:
            print(f"⚠️ Erreur initialisation thème: {e}")
    
    def _ensure_golden_ratio_geometry(self):
        """S'assure que la fenêtre respecte les proportions du nombre d'or avec adaptation intelligente"""
        try:
            golden_ratio = 1.618
            screen = QApplication.primaryScreen().geometry()
            
            # Calcul intelligent des dimensions selon le nombre d'or
            if screen.width() >= 1920:  # Écrans haute résolution
                target_width = int(screen.width() * 0.80)
            elif screen.width() >= 1366:  # Écrans standards
                target_width = int(screen.width() * 0.85)
            else:  # Écrans plus petits
                target_width = int(screen.width() * 0.90)
                
            target_height = int(target_width / golden_ratio)
            
            # S'assurer que la fenêtre ne dépasse pas l'écran
            max_height = int(screen.height() * 0.90)
            if target_height > max_height:
                target_height = max_height
                target_width = int(target_height * golden_ratio)
            
            # Vérifier si ajustement nécessaire (tolérance de 30px)
            current_size = self.size()
            if (abs(current_size.width() - target_width) > 30 or 
                abs(current_size.height() - target_height) > 30):
                
                # Centrer la fenêtre
                x = max(0, (screen.width() - target_width) // 2)
                y = max(0, (screen.height() - target_height) // 2)
                
                self.setGeometry(x, y, target_width, target_height)
                
                # Définir les tailles minimales et maximales
                self.setMinimumSize(int(target_width * 0.6), int(target_height * 0.6))
                
                print(f"📐 Géométrie optimisée: {target_width}x{target_height} (ratio: {target_width/target_height:.3f})")
                
        except Exception as e:
            print(f"⚠️ Erreur ajustement géométrie: {e}")

    def debug_acquisition_state(self):
        """Affiche l'état actuel de l'acquisition pour débogage"""
        print("\n🔍 ÉTAT DE L'ACQUISITION:")
        print(f"   - Running: {self.running}")
        print(f"   - Sample count: {self.sample_count} / {self.max_samples}")
        print(f"   - Nombre de sondes: {self.n_sondes_total_calib}")
        print(f"   - Fréquence: {self.freq} Hz")
        print(f"   - Durée prévue: {self.duree_s} s")
        print(f"   - Données acquises: {len(self.time_storage_full)} points temporels")
        for i, sonde_data in enumerate(self.data_storage_full):
            print(f"     > Sonde {i+1} ({self.sonde_names_calib[i] if self.sonde_names_calib else i+1}): {len(sonde_data)} points")
        print(f"   - Hardware connecté: {getattr(self.hardware_adapter, 'is_connected', False) if hasattr(self, 'hardware_adapter') else 'N/A'}")
        print(f"   - Fichier de calibration: {self.calib_file_name_short}")
        print(f"   - Dossier de sauvegarde: {self.save_folder}")       
class AcquisitionSetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.rt_acquisition_window = None 
        self.loaded_sonde_names = [] 
        self.loaded_n_sondes = 0     
        self.loaded_calibration_params = [] 
        self._last_loaded_calib_file = None 
        self._init_ui_setup() 

    def _init_ui_setup(self):
        self.setWindowTitle("Configuration de l'Acquisition - HRNeoWave")
        self.setMinimumWidth(600) 
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15,15,15,15)
        layout.setSpacing(10)
        
        title_label_setup = QLabel("Configuration de l'Acquisition des Données")
        title_label_setup.setObjectName("titleLabel")
        title_label_setup.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label_setup)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)

        # Fichier de calibration
        self.calib_path_edit = QLineEdit()
        self.calib_path_edit.setPlaceholderText("Sélectionner un fichier .json ou .csv de calibration")
        calib_btn = QPushButton("Choisir...")
        calib_btn.setFixedWidth(120)
        calib_btn.clicked.connect(self.choose_calib_file_action)
        calib_file_layout = QHBoxLayout()
        calib_file_layout.addWidget(self.calib_path_edit)
        calib_file_layout.addWidget(calib_btn)
        form_layout.addRow("Fichier de calibration:", calib_file_layout)

        # Affichage des sondes détectées
        self.nsondes_display_edit = QLineEdit("Aucun fichier de calibration chargé.") 
        self.nsondes_display_edit.setReadOnly(True)
        self.nsondes_display_edit.setStyleSheet("background-color: #2a2a30; border: none; color: #aaa;")
        form_layout.addRow("Sondes Détectées:", self.nsondes_display_edit)

        # Durée du test
        self.duree_spinbox = QSpinBox()
        self.duree_spinbox.setRange(1, 7200) 
        self.duree_spinbox.setValue(60)
        self.duree_spinbox.setSuffix(" s")
        self.duree_spinbox.setFixedWidth(120)
        form_layout.addRow("Durée du test (s):", self.duree_spinbox)

        # Fréquence d'échantillonnage
        self.freq_spinbox = QSpinBox()
        self.freq_spinbox.setRange(1, 10000) 
        self.freq_spinbox.setValue(32)    
        self.freq_spinbox.setSuffix(" Hz")
        self.freq_spinbox.setFixedWidth(120)
        form_layout.addRow("Fréquence d'éch. (Hz):", self.freq_spinbox)
        
        # Dossier de sauvegarde
        self.save_path_edit = QLineEdit(os.getcwd()) 
        self.save_path_edit.setPlaceholderText("Dossier pour les fichiers .csv")
        save_btn = QPushButton("Choisir...") 
        save_btn.setFixedWidth(120)
        save_btn.clicked.connect(self.choose_save_folder_action)
        save_file_layout = QHBoxLayout()
        save_file_layout.addWidget(self.save_path_edit)
        save_file_layout.addWidget(save_btn)
        form_layout.addRow("Dossier sauvegarde:", save_file_layout)
        
        layout.addLayout(form_layout)
        layout.addStretch(1)
        
        # Bouton principal
        start_button_setup = QPushButton("Démarrer l'Acquisition")
        start_button_setup.setMinimumHeight(40)
        start_button_setup.clicked.connect(self.on_start_acquisition_action)
        layout.addWidget(start_button_setup, alignment=Qt.AlignCenter)
        self.show()

    def choose_calib_file_action(self): 
        path, _ = QFileDialog.getOpenFileName(self, "Choisir le fichier de calibration", 
                                             os.getcwd(), 
                                             "Fichiers Calibration (*.json *.csv);;Tous les fichiers (*)")
        if path:
            self.calib_path_edit.setText(path)
            self.try_load_calibration_info_action(path) 

    def try_load_calibration_info_action(self, file_path): 
        """Charge les informations de calibration depuis un fichier"""
        sonde_names_from_file = []
        calibration_params_from_file = []
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {file_path}")

            if file_path.endswith(".json"):
                with open(file_path, "r", encoding="utf-8") as f: 
                    data_calib = json.load(f)
                    
                if isinstance(data_calib, list) and data_calib and isinstance(data_calib[0], dict):
                    for i, params_sonde in enumerate(data_calib):
                        nom = params_sonde.get("nom_sonde", params_sonde.get("id", f"Sonde_JSON_{i+1}"))
                        slope = float(params_sonde.get("slope", 1.0))
                        intercept = float(params_sonde.get("intercept", 0.0))
                        unit = params_sonde.get("unit", "m")
                        sonde_names_from_file.append(nom)
                        calibration_params_from_file.append({
                            "nom_sonde": nom, 
                            "slope": slope, 
                            "intercept": intercept, 
                            "unit": unit
                        })
                elif isinstance(data_calib, dict):
                    for nom, params_sonde in data_calib.items():
                        slope = float(params_sonde.get("slope", 1.0))
                        intercept = float(params_sonde.get("intercept", 0.0))
                        unit = params_sonde.get("unit", "m")
                        sonde_names_from_file.append(nom)
                        calibration_params_from_file.append({
                            "nom_sonde": nom, 
                            "slope": slope, 
                            "intercept": intercept, 
                            "unit": unit
                        })
                        
            elif file_path.endswith(".csv"): 
                with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                    reader = csv.DictReader(f)
                    # Normaliser les noms de colonnes
                    expected_cols_norm = {"nom_sonde", "slope", "intercept"}
                    
                    if reader.fieldnames:
                        # Obtenir les noms de colonnes du fichier et les normaliser
                        file_fieldnames_norm = {fn.lower().strip().replace(" ", "_"): fn 
                                              for fn in reader.fieldnames}

                        # Vérifier si toutes les colonnes attendues sont présentes
                        if not all(col_exp in file_fieldnames_norm for col_exp in expected_cols_norm):
                            missing_norm = [col_exp for col_exp in expected_cols_norm 
                                          if col_exp not in file_fieldnames_norm]
                            raise ValueError(f"Colonnes CSV manquantes: {', '.join(missing_norm)}")

                        # Récupérer les noms de colonnes originaux
                        col_nom_orig = file_fieldnames_norm.get("nom_sonde")
                        col_slope_orig = file_fieldnames_norm.get("slope")
                        col_intercept_orig = file_fieldnames_norm.get("intercept")
                        col_unit_orig = file_fieldnames_norm.get("unit")

                        for i, row_dict in enumerate(reader):
                            nom = row_dict.get(col_nom_orig, f"Sonde_CSV_{i+1}")
                            slope = float(row_dict.get(col_slope_orig, "1.0"))
                            intercept = float(row_dict.get(col_intercept_orig, "0.0"))
                            unit = row_dict.get(col_unit_orig, "m") if col_unit_orig else "m"
                            sonde_names_from_file.append(nom)
                            calibration_params_from_file.append({
                                "nom_sonde": nom, 
                                "slope": slope, 
                                "intercept": intercept, 
                                "unit": unit
                            })
            
            if sonde_names_from_file:
                num_sondes_lues = len(sonde_names_from_file)
                if num_sondes_lues > MAX_SONDES_PERMITTED:
                    QMessageBox.warning(self, "Trop de Sondes",
                                        f"Le fichier contient {num_sondes_lues} sondes. "
                                        f"Seules les {MAX_SONDES_PERMITTED} premières seront utilisées.")
                    self.loaded_sonde_names = sonde_names_from_file[:MAX_SONDES_PERMITTED]
                    self.loaded_calibration_params = calibration_params_from_file[:MAX_SONDES_PERMITTED]
                    self.loaded_n_sondes = MAX_SONDES_PERMITTED
                else:
                    self.loaded_sonde_names = sonde_names_from_file
                    self.loaded_calibration_params = calibration_params_from_file
                    self.loaded_n_sondes = num_sondes_lues
                
                display_names = f"{self.loaded_n_sondes} sondes: {', '.join(self.loaded_sonde_names[:min(3, self.loaded_n_sondes)])}"
                if self.loaded_n_sondes > 3: 
                    display_names += "..."
                self.nsondes_display_edit.setText(display_names)
            else:
                self.nsondes_display_edit.setText("Aucune sonde trouvée ou format non reconnu.")
                self.loaded_sonde_names = []
                self.loaded_n_sondes = 0
                self.loaded_calibration_params = []
                
        except FileNotFoundError as fnf_e:
            self.nsondes_display_edit.setText("Fichier de calibration non trouvé.")
            QMessageBox.critical(self, "Erreur Fichier", str(fnf_e))
            self.loaded_sonde_names = []
            self.loaded_n_sondes = 0
            self.loaded_calibration_params = []
        except ValueError as ve: 
            self.nsondes_display_edit.setText("Erreur de format dans le fichier.")
            QMessageBox.warning(self, "Erreur Format Calibration", 
                              f"Valeur non numérique ou colonne attendue manquante : {ve}")
            self.loaded_sonde_names = []
            self.loaded_n_sondes = 0
            self.loaded_calibration_params = []
        except Exception as e:
            self.nsondes_display_edit.setText(f"Erreur lecture: {type(e).__name__}")
            QMessageBox.warning(self, "Erreur Lecture Calibration", 
                              f"Impossible de lire le fichier : {e}\n{traceback.format_exc()}")
            self.loaded_sonde_names = []
            self.loaded_n_sondes = 0
            self.loaded_calibration_params = []

    def on_start_acquisition_action(self): 
        """Lance la fenêtre d'acquisition temps réel"""
        calib_file_path = self.calib_path_edit.text() 
        save_dir = self.save_path_edit.text()
        
        if not calib_file_path or not os.path.exists(calib_file_path):
            QMessageBox.warning(self, "Erreur Configuration", 
                              "Veuillez choisir un fichier de calibration valide.")
            return
        if not save_dir or not os.path.isdir(save_dir):
            QMessageBox.warning(self, "Erreur Configuration", 
                              "Veuillez choisir un dossier de sauvegarde valide.")
            return
        
        if calib_file_path != getattr(self, '_last_loaded_calib_file', None) or self.loaded_n_sondes == 0:
            self.try_load_calibration_info_action(calib_file_path) 
            setattr(self, '_last_loaded_calib_file', calib_file_path)

        if self.loaded_n_sondes == 0:
            QMessageBox.warning(self, "Erreur Configuration Sondes", 
                                f"Aucune sonde valide (max {MAX_SONDES_PERMITTED}) n'a pu être chargée. "
                                f"Veuillez vérifier le fichier de calibration.")
            return

        duree_val = self.duree_spinbox.value()
        freq_val = self.freq_spinbox.value()
        
        if self.rt_acquisition_window and self.rt_acquisition_window.isVisible():
            QMessageBox.information(self, "Information", 
                                  "Une fenêtre d'acquisition est déjà ouverte. Veuillez la fermer d'abord.")
            return

        # Désactiver cette fenêtre pendant l'acquisition
        self.setEnabled(False)
        
        # Créer et afficher la fenêtre d'acquisition
        self.rt_acquisition_window = RealTimeAcquisitionWindow(
            self.loaded_n_sondes, 
            freq_val, 
            duree_val, 
            save_dir, 
            self.loaded_sonde_names, 
            self.loaded_calibration_params,
            calib_file_path, 
            parent_setup_window=self
        )
        self.rt_acquisition_window.show()
        
    def choose_save_folder_action(self): 
        """Sélection du dossier de sauvegarde"""
        current_path = self.save_path_edit.text()
        if not current_path or not os.path.isdir(current_path): 
            current_path = os.getcwd()
        path = QFileDialog.getExistingDirectory(self, "Choisir le dossier de sauvegarde", current_path)
        if path: 
            self.save_path_edit.setText(path)

    def closeEvent(self, event): 
        """Gestion de la fermeture de la fenêtre"""
        if self.rt_acquisition_window and self.rt_acquisition_window.isVisible():
            self.rt_acquisition_window.close() 
        super().closeEvent(event)


# Point d'entrée principal
if __name__ == "__main__":
    pg.setConfigOption('background', QColor(30, 30, 36)) 
    pg.setConfigOption('foreground', QColor(220, 220, 220))
    
    app = QApplication(sys.argv)
    set_dark_mode(app)
    
    main_setup_window = AcquisitionSetupWindow()
    main_setup_window.show()  # Afficher la fenêtre principale
    
    sys.exit(app.exec_())