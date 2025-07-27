# -*- coding: utf-8 -*-
"""
Acquisition View - Maritime Theme 2025
Vue d'acquisition de données avec design maritime et Golden Ratio
"""

from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QTextEdit, QSplitter, QProgressBar, QSlider,
    QTabWidget, QScrollArea, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPixmap

# Golden Ratio Constants
FIBONACCI_SPACING = [8, 13, 21, 34, 55, 89]
GOLDEN_RATIO = 1.618

class AcquisitionControlPanel(QFrame):
    """
    Panneau de contrôle pour l'acquisition de données
    """
    
    # Signaux
    acquisition_started = Signal()
    acquisition_stopped = Signal()
    acquisition_paused = Signal()
    parameters_changed = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_acquiring = False
        self.is_paused = False
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configure l'interface du panneau de contrôle"""
        self.setObjectName("acquisition_control_panel")
        self.setFixedWidth(int(300 * GOLDEN_RATIO))  # ~485px
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                      FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        main_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # En-tête
        self.setup_header(main_layout)
        
        # Zone de défilement
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Widget conteneur
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Sections du panneau
        self.setup_acquisition_controls(content_layout)
        self.setup_parameters_section(content_layout)
        self.setup_status_section(content_layout)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Style du panneau
        self.setStyleSheet("""
            QFrame#acquisition_control_panel {
                background-color: #F5FBFF;
                border-right: 2px solid #E0E7FF;
            }
        """)
        
    def setup_header(self, parent_layout):
        """Configure l'en-tête du panneau"""
        header_frame = QFrame()
        header_frame.setObjectName("control_panel_header")
        header_frame.setFixedHeight(89)  # Fibonacci
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, FIBONACCI_SPACING[1], 0, FIBONACCI_SPACING[1])
        header_layout.setSpacing(FIBONACCI_SPACING[0])
        
        # Titre
        title_label = QLabel("Contrôle d'Acquisition")
        title_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #0A1929;")
        
        # Sous-titre
        subtitle_label = QLabel("Configuration et pilotage")
        subtitle_label.setFont(QFont("Inter", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #445868;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        # Style du header
        header_frame.setStyleSheet("""
            QFrame#control_panel_header {
                background-color: #F5FBFF;
                border-bottom: 2px solid #E0E7FF;
            }
        """)
        
        parent_layout.addWidget(header_frame)
        
    def setup_acquisition_controls(self, parent_layout):
        """Configure les contrôles d'acquisition"""
        controls_group = QGroupBox("Contrôles")
        controls_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        controls_layout = QVBoxLayout(controls_group)
        controls_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Boutons principaux
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Bouton Start/Stop
        self.start_stop_button = QPushButton("🚀 Démarrer l'Acquisition")
        self.start_stop_button.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        self.start_stop_button.setFixedHeight(FIBONACCI_SPACING[4])  # 55px
        self.start_stop_button.clicked.connect(self.toggle_acquisition)
        
        # Bouton Pause/Resume
        self.pause_button = QPushButton("⏸️ Pause")
        self.pause_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.pause_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.toggle_pause)
        
        # Bouton Reset
        self.reset_button = QPushButton("🔄 Reset")
        self.reset_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.reset_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        self.reset_button.clicked.connect(self.reset_acquisition)
        
        buttons_layout.addWidget(self.start_stop_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.reset_button)
        
        controls_layout.addLayout(buttons_layout)
        
        # Style des boutons
        self.apply_button_styles()
        
        parent_layout.addWidget(controls_group)
        
    def setup_parameters_section(self, parent_layout):
        """Configure la section des paramètres"""
        params_group = QGroupBox("Paramètres d'Acquisition")
        params_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        params_layout = QGridLayout(params_group)
        params_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Fréquence d'échantillonnage
        freq_label = QLabel("Fréquence (Hz):")
        freq_label.setFont(QFont("Inter", 12))
        
        self.frequency_spinbox = QSpinBox()
        self.frequency_spinbox.setRange(1, 10000)
        self.frequency_spinbox.setValue(1000)
        self.frequency_spinbox.setSuffix(" Hz")
        self.frequency_spinbox.setFont(QFont("Inter", 12))
        
        # Durée d'acquisition
        duration_label = QLabel("Durée (s):")
        duration_label.setFont(QFont("Inter", 12))
        
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 3600)
        self.duration_spinbox.setValue(60)
        self.duration_spinbox.setSuffix(" s")
        self.duration_spinbox.setFont(QFont("Inter", 12))
        
        # Mode d'acquisition
        mode_label = QLabel("Mode:")
        mode_label.setFont(QFont("Inter", 12))
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Continu", "Déclenché", "Burst"])
        self.mode_combo.setFont(QFont("Inter", 12))
        
        # Gain
        gain_label = QLabel("Gain:")
        gain_label.setFont(QFont("Inter", 12))
        
        self.gain_slider = QSlider(Qt.Orientation.Horizontal)
        self.gain_slider.setRange(1, 100)
        self.gain_slider.setValue(50)
        
        self.gain_value_label = QLabel("50")
        self.gain_value_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.gain_value_label.setStyleSheet("color: #00ACC1;")
        self.gain_value_label.setFixedWidth(FIBONACCI_SPACING[3])
        
        # Connexions
        self.gain_slider.valueChanged.connect(
            lambda v: self.gain_value_label.setText(str(v))
        )
        
        # Assemblage
        params_layout.addWidget(freq_label, 0, 0)
        params_layout.addWidget(self.frequency_spinbox, 0, 1)
        
        params_layout.addWidget(duration_label, 1, 0)
        params_layout.addWidget(self.duration_spinbox, 1, 1)
        
        params_layout.addWidget(mode_label, 2, 0)
        params_layout.addWidget(self.mode_combo, 2, 1)
        
        params_layout.addWidget(gain_label, 3, 0)
        
        gain_layout = QHBoxLayout()
        gain_layout.addWidget(self.gain_slider)
        gain_layout.addWidget(self.gain_value_label)
        params_layout.addLayout(gain_layout, 3, 1)
        
        parent_layout.addWidget(params_group)
        
    def setup_status_section(self, parent_layout):
        """Configure la section de statut"""
        status_group = QGroupBox("Statut")
        status_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Indicateur d'état
        self.status_label = QLabel("⏹️ Arrêté")
        self.status_label.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            background-color: #E0E7FF;
            color: #445868;
            padding: 8px;
            border-radius: 8px;
        """)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(FIBONACCI_SPACING[2])  # 21px
        
        # Compteurs
        counters_layout = QGridLayout()
        
        # Échantillons collectés
        samples_label = QLabel("Échantillons:")
        samples_label.setFont(QFont("Inter", 11))
        
        self.samples_count_label = QLabel("0")
        self.samples_count_label.setFont(QFont("Inter", 11, QFont.Weight.Bold))
        self.samples_count_label.setStyleSheet("color: #00ACC1;")
        
        # Temps écoulé
        time_label = QLabel("Temps:")
        time_label.setFont(QFont("Inter", 11))
        
        self.elapsed_time_label = QLabel("00:00")
        self.elapsed_time_label.setFont(QFont("Inter", 11, QFont.Weight.Bold))
        self.elapsed_time_label.setStyleSheet("color: #2B79B6;")
        
        counters_layout.addWidget(samples_label, 0, 0)
        counters_layout.addWidget(self.samples_count_label, 0, 1)
        counters_layout.addWidget(time_label, 1, 0)
        counters_layout.addWidget(self.elapsed_time_label, 1, 1)
        
        # Assemblage
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        status_layout.addLayout(counters_layout)
        
        # Style de la barre de progression
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #E0E7FF;
                border-radius: 10px;
                background-color: #F5FBFF;
                text-align: center;
                font: 10px "Inter";
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ACC1, stop:1 #2B79B6);
                border-radius: 9px;
            }
        """)
        
        parent_layout.addWidget(status_group)
        
    def apply_button_styles(self):
        """Applique les styles aux boutons"""
        # Style du bouton principal
        primary_style = """
            QPushButton {
                background-color: #00ACC1;
                color: #F5FBFF;
                border: none;
                border-radius: 27px;
                padding: 13px 21px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #0097A7;
            }
            
            QPushButton:pressed {
                background-color: #00838F;
            }
            
            QPushButton:disabled {
                background-color: #E0E7FF;
                color: #445868;
            }
        """
        
        # Style des boutons secondaires
        secondary_style = """
            QPushButton {
                background-color: #2B79B6;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 8px 13px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #1565C0;
            }
            
            QPushButton:disabled {
                background-color: #E0E7FF;
                color: #445868;
            }
        """
        
        self.start_stop_button.setStyleSheet(primary_style)
        self.pause_button.setStyleSheet(secondary_style)
        self.reset_button.setStyleSheet(secondary_style)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        # Connexions des paramètres
        self.frequency_spinbox.valueChanged.connect(self.on_parameters_changed)
        self.duration_spinbox.valueChanged.connect(self.on_parameters_changed)
        self.mode_combo.currentTextChanged.connect(self.on_parameters_changed)
        self.gain_slider.valueChanged.connect(self.on_parameters_changed)
        
    def toggle_acquisition(self):
        """Bascule l'état d'acquisition"""
        if not self.is_acquiring:
            self.start_acquisition()
        else:
            self.stop_acquisition()
            
    def start_acquisition(self):
        """Démarre l'acquisition"""
        self.is_acquiring = True
        self.is_paused = False
        
        # Mettre à jour l'interface
        self.start_stop_button.setText("⏹️ Arrêter l'Acquisition")
        self.pause_button.setEnabled(True)
        self.status_label.setText("🔴 En cours...")
        self.status_label.setStyleSheet("""
            background-color: rgba(255, 107, 71, 0.1);
            color: #FF6B47;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
        """)
        
        # Émettre le signal
        self.acquisition_started.emit()
        
    def stop_acquisition(self):
        """Arrête l'acquisition"""
        self.is_acquiring = False
        self.is_paused = False
        
        # Mettre à jour l'interface
        self.start_stop_button.setText("🚀 Démarrer l'Acquisition")
        self.pause_button.setEnabled(False)
        self.pause_button.setText("⏸️ Pause")
        self.status_label.setText("⏹️ Arrêté")
        self.status_label.setStyleSheet("""
            background-color: #E0E7FF;
            color: #445868;
            padding: 8px;
            border-radius: 8px;
        """)
        
        # Émettre le signal
        self.acquisition_stopped.emit()
        
    def toggle_pause(self):
        """Bascule l'état de pause"""
        if not self.is_paused:
            self.pause_acquisition()
        else:
            self.resume_acquisition()
            
    def pause_acquisition(self):
        """Met en pause l'acquisition"""
        self.is_paused = True
        
        # Mettre à jour l'interface
        self.pause_button.setText("▶️ Reprendre")
        self.status_label.setText("⏸️ En pause")
        self.status_label.setStyleSheet("""
            background-color: rgba(255, 152, 0, 0.1);
            color: #FF9800;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
        """)
        
        # Émettre le signal
        self.acquisition_paused.emit()
        
    def resume_acquisition(self):
        """Reprend l'acquisition"""
        self.is_paused = False
        
        # Mettre à jour l'interface
        self.pause_button.setText("⏸️ Pause")
        self.status_label.setText("🔴 En cours...")
        self.status_label.setStyleSheet("""
            background-color: rgba(255, 107, 71, 0.1);
            color: #FF6B47;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
        """)
        
        # Émettre le signal
        self.acquisition_started.emit()
        
    def reset_acquisition(self):
        """Remet à zéro l'acquisition"""
        # Arrêter si en cours
        if self.is_acquiring:
            self.stop_acquisition()
            
        # Réinitialiser les compteurs
        self.progress_bar.setValue(0)
        self.samples_count_label.setText("0")
        self.elapsed_time_label.setText("00:00")
        
    def on_parameters_changed(self):
        """Gestionnaire de changement de paramètres"""
        params = {
            'frequency': self.frequency_spinbox.value(),
            'duration': self.duration_spinbox.value(),
            'mode': self.mode_combo.currentText(),
            'gain': self.gain_slider.value()
        }
        
        self.parameters_changed.emit(params)
        
    def update_progress(self, progress: int):
        """Met à jour la progression"""
        self.progress_bar.setValue(progress)
        
    def update_samples_count(self, count: int):
        """Met à jour le compteur d'échantillons"""
        self.samples_count_label.setText(f"{count:,}")
        
    def update_elapsed_time(self, seconds: int):
        """Met à jour le temps écoulé"""
        minutes = seconds // 60
        secs = seconds % 60
        self.elapsed_time_label.setText(f"{minutes:02d}:{secs:02d}")


class DataVisualizationArea(QFrame):
    """
    Zone de visualisation des données en temps réel
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface de visualisation"""
        self.setObjectName("data_visualization_area")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                      FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        main_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # En-tête
        self.setup_header(main_layout)
        
        # Onglets de visualisation
        self.setup_tabs(main_layout)
        
        # Style de base
        self.setStyleSheet("""
            QFrame#data_visualization_area {
                background-color: #F5FBFF;
            }
        """)
        
    def setup_header(self, parent_layout):
        """Configure l'en-tête de la zone de visualisation"""
        header_frame = QFrame()
        header_frame.setFixedHeight(55)  # Fibonacci
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, FIBONACCI_SPACING[1], 0, FIBONACCI_SPACING[1])
        header_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title_label = QLabel("Visualisation des Données")
        title_label.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0A1929;")
        
        # Indicateurs de statut
        status_layout = QHBoxLayout()
        status_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Fréquence d'affichage
        refresh_label = QLabel("📊 Temps réel")
        refresh_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        refresh_label.setStyleSheet("""
            background-color: rgba(0, 172, 193, 0.1);
            color: #00ACC1;
            padding: 5px 10px;
            border-radius: 10px;
        """)
        
        # Nombre de canaux
        channels_label = QLabel("4 Canaux")
        channels_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        channels_label.setStyleSheet("""
            background-color: rgba(43, 121, 182, 0.1);
            color: #2B79B6;
            padding: 5px 10px;
            border-radius: 10px;
        """)
        
        status_layout.addWidget(refresh_label)
        status_layout.addWidget(channels_label)
        
        # Assemblage
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addLayout(status_layout)
        
        parent_layout.addWidget(header_frame)
        
    def setup_tabs(self, parent_layout):
        """Configure les onglets de visualisation"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Inter", 12))
        
        # Onglet Graphiques temporels
        time_series_tab = self.create_time_series_tab()
        self.tab_widget.addTab(time_series_tab, "📈 Séries Temporelles")
        
        # Onglet Spectrogramme
        spectrum_tab = self.create_spectrum_tab()
        self.tab_widget.addTab(spectrum_tab, "🌊 Spectrogramme")
        
        # Onglet Données brutes
        raw_data_tab = self.create_raw_data_tab()
        self.tab_widget.addTab(raw_data_tab, "📋 Données Brutes")
        
        # Style des onglets
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #E0E7FF;
                border-radius: 13px;
                background-color: white;
            }
            
            QTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background-color: #F5FBFF;
                color: #445868;
                padding: 8px 21px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
            }
            
            QTabBar::tab:selected {
                background-color: #00ACC1;
                color: #F5FBFF;
                font-weight: 600;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: rgba(0, 172, 193, 0.1);
                color: #00ACC1;
            }
        """)
        
        parent_layout.addWidget(self.tab_widget)
        
    def create_time_series_tab(self) -> QWidget:
        """Crée l'onglet des séries temporelles"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                 FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Zone de graphique principal
        main_graph_frame = QFrame()
        main_graph_frame.setObjectName("main_graph")
        main_graph_frame.setMinimumHeight(400)
        main_graph_frame.setStyleSheet("""
            QFrame#main_graph {
                background-color: #F5FBFF;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
            }
        """)
        
        main_graph_layout = QVBoxLayout(main_graph_frame)
        main_graph_placeholder = QLabel("📈 Graphique Principal - Séries Temporelles")
        main_graph_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_graph_placeholder.setFont(QFont("Inter", 16))
        main_graph_placeholder.setStyleSheet("color: #445868;")
        main_graph_layout.addWidget(main_graph_placeholder)
        
        # Graphiques secondaires (miniatures)
        mini_graphs_layout = QHBoxLayout()
        mini_graphs_layout.setSpacing(FIBONACCI_SPACING[1])
        
        for i in range(4):
            mini_frame = QFrame()
            mini_frame.setFixedHeight(150)
            mini_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #E0E7FF;
                    border-radius: 8px;
                }
            """)
            
            mini_layout = QVBoxLayout(mini_frame)
            mini_label = QLabel(f"Canal {i+1}")
            mini_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mini_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
            mini_label.setStyleSheet("color: #445868;")
            mini_layout.addWidget(mini_label)
            
            mini_graphs_layout.addWidget(mini_frame)
            
        layout.addWidget(main_graph_frame)
        layout.addLayout(mini_graphs_layout)
        
        return tab
        
    def create_spectrum_tab(self) -> QWidget:
        """Crée l'onglet du spectrogramme"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                 FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Contrôles du spectrogramme
        controls_frame = QFrame()
        controls_frame.setFixedHeight(55)  # Fibonacci
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Sélection de canal
        channel_label = QLabel("Canal:")
        channel_label.setFont(QFont("Inter", 12))
        
        channel_combo = QComboBox()
        channel_combo.addItems(["Canal 1", "Canal 2", "Canal 3", "Canal 4"])
        channel_combo.setFont(QFont("Inter", 12))
        
        # Fenêtre FFT
        window_label = QLabel("Fenêtre:")
        window_label.setFont(QFont("Inter", 12))
        
        window_combo = QComboBox()
        window_combo.addItems(["Hanning", "Hamming", "Blackman", "Rectangular"])
        window_combo.setFont(QFont("Inter", 12))
        
        controls_layout.addWidget(channel_label)
        controls_layout.addWidget(channel_combo)
        controls_layout.addWidget(window_label)
        controls_layout.addWidget(window_combo)
        controls_layout.addStretch()
        
        # Zone de spectrogramme
        spectrum_frame = QFrame()
        spectrum_frame.setObjectName("spectrum_graph")
        spectrum_frame.setStyleSheet("""
            QFrame#spectrum_graph {
                background-color: #F5FBFF;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
            }
        """)
        
        spectrum_layout = QVBoxLayout(spectrum_frame)
        spectrum_placeholder = QLabel("🌊 Spectrogramme - Analyse Fréquentielle")
        spectrum_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spectrum_placeholder.setFont(QFont("Inter", 16))
        spectrum_placeholder.setStyleSheet("color: #445868;")
        spectrum_layout.addWidget(spectrum_placeholder)
        
        layout.addWidget(controls_frame)
        layout.addWidget(spectrum_frame)
        
        return tab
        
    def create_raw_data_tab(self) -> QWidget:
        """Crée l'onglet des données brutes"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                 FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Contrôles des données
        controls_frame = QFrame()
        controls_frame.setFixedHeight(55)  # Fibonacci
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Boutons d'export
        export_csv_button = QPushButton("💾 Export CSV")
        export_csv_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        export_csv_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        export_excel_button = QPushButton("📊 Export Excel")
        export_excel_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        export_excel_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        # Style des boutons d'export
        export_style = """
            QPushButton {
                background-color: #2B79B6;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 8px 13px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """
        
        export_csv_button.setStyleSheet(export_style)
        export_excel_button.setStyleSheet(export_style)
        
        controls_layout.addWidget(export_csv_button)
        controls_layout.addWidget(export_excel_button)
        controls_layout.addStretch()
        
        # Tableau de données
        data_text = QTextEdit()
        data_text.setReadOnly(True)
        data_text.setFont(QFont("Consolas", 10))
        data_text.setPlainText(
            "Timestamp\t\tCanal 1\t\tCanal 2\t\tCanal 3\t\tCanal 4\n"
            "2025-01-XX 10:00:00.000\t1.234\t\t2.567\t\t3.890\t\t4.123\n"
            "2025-01-XX 10:00:00.001\t1.235\t\t2.568\t\t3.891\t\t4.124\n"
            "2025-01-XX 10:00:00.002\t1.236\t\t2.569\t\t3.892\t\t4.125\n"
            "...\n"
        )
        
        data_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        
        layout.addWidget(controls_frame)
        layout.addWidget(data_text)
        
        return tab


class AcquisitionView(QWidget):
    """
    Vue principale d'acquisition avec design maritime
    """
    
    # Signaux
    acquisition_started = Signal()
    acquisition_stopped = Signal()
    acquisitionFinished = Signal(dict)  # Signal émis lorsque la session d'acquisition est terminée
    data_exported = Signal(str)  # Chemin du fichier exporté
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_dark_mode = False
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configure l'interface principale"""
        self.setObjectName("acquisition_view")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter horizontal (panneau de contrôle + visualisation)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panneau de contrôle
        self.control_panel = AcquisitionControlPanel()
        splitter.addWidget(self.control_panel)
        
        # Zone de visualisation
        self.visualization_area = DataVisualizationArea()
        splitter.addWidget(self.visualization_area)
        
        # Proportions du splitter (Golden Ratio)
        control_width = int(300 * GOLDEN_RATIO)  # ~485px
        viz_width = int(control_width * GOLDEN_RATIO)  # ~785px
        splitter.setSizes([control_width, viz_width])
        splitter.setCollapsible(0, False)  # Panneau non collapsible
        splitter.setCollapsible(1, False)  # Visualisation non collapsible
        
        main_layout.addWidget(splitter)
        
        # Style de base
        self.setStyleSheet("""
            QWidget#acquisition_view {
                background-color: #F5FBFF;
            }
        """)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        # Connexions du panneau de contrôle
        self.control_panel.acquisition_started.connect(self.on_acquisition_started)
        self.control_panel.acquisition_stopped.connect(self.on_acquisition_stopped)
        self.control_panel.acquisition_paused.connect(self.on_acquisition_paused)
        self.control_panel.parameters_changed.connect(self.on_parameters_changed)
        
    def on_acquisition_started(self):
        """Gestionnaire de démarrage d'acquisition"""
        print("Acquisition démarrée")
        self.acquisition_started.emit()
        
    def on_acquisition_stopped(self):
        """Gestionnaire d'arrêt d'acquisition"""
        print("Acquisition arrêtée")
        self.acquisition_stopped.emit()
        
    def on_acquisition_paused(self):
        """Gestionnaire de pause d'acquisition"""
        print("Acquisition en pause")
        
    def on_parameters_changed(self, params: dict):
        """Gestionnaire de changement de paramètres"""
        print(f"Paramètres modifiés: {params}")
        
    def set_theme(self, is_dark: bool):
        """Applique le thème sombre ou clair"""
        self.is_dark_mode = is_dark
        
        if is_dark:
            # Thème sombre
            self.setStyleSheet("""
                QWidget#acquisition_view {
                    background-color: #0A1929;
                    color: #F5FBFF;
                }
            """)
        else:
            # Thème clair
            self.setStyleSheet("""
                QWidget#acquisition_view {
                    background-color: #F5FBFF;
                    color: #0A1929;
                }
            """)
            
    def update_real_time_data(self, data: dict):
        """Met à jour les données en temps réel"""
        # Mettre à jour les compteurs
        if 'samples_count' in data:
            self.control_panel.update_samples_count(data['samples_count'])
            
        if 'elapsed_time' in data:
            self.control_panel.update_elapsed_time(data['elapsed_time'])
            
        if 'progress' in data:
            self.control_panel.update_progress(data['progress'])
            
    def export_data(self, format_type: str = 'csv') -> str:
        """Exporte les données acquises"""
        # Logique d'export (placeholder)
        filename = f"acquisition_data.{format_type}"
        print(f"Export des données vers {filename}")
        
        self.data_exported.emit(filename)
        return filename
        
    def get_acquisition_parameters(self) -> dict:
        """Retourne les paramètres d'acquisition actuels"""
        return {
            'frequency': self.control_panel.frequency_spinbox.value(),
            'duration': self.control_panel.duration_spinbox.value(),
            'mode': self.control_panel.mode_combo.currentText(),
            'gain': self.control_panel.gain_slider.value()
        }
        
    def is_acquiring(self) -> bool:
        """Retourne l'état d'acquisition"""
        return self.control_panel.is_acquiring
        
    def set_controller(self, controller):
        """
        Définit le contrôleur d'acquisition pour cette vue
        """
        self.controller = controller
        print(f"[DEBUG] Contrôleur d'acquisition défini: {controller}")
        
        # Connecter les signaux du contrôleur si nécessaire
        if hasattr(controller, 'acquisition_started'):
            controller.acquisition_started.connect(self._on_controller_acquisition_started)
        if hasattr(controller, 'acquisition_stopped'):
            controller.acquisition_stopped.connect(self._on_controller_acquisition_stopped)
    
    def _on_controller_acquisition_started(self):
        """Gestionnaire pour le démarrage d'acquisition depuis le contrôleur"""
        print("[DEBUG] Acquisition démarrée depuis le contrôleur")
    
    def _on_controller_acquisition_stopped(self):
        """Gestionnaire pour l'arrêt d'acquisition depuis le contrôleur"""
        print("[DEBUG] Acquisition arrêtée depuis le contrôleur")