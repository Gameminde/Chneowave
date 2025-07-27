# -*- coding: utf-8 -*-
"""
Live Acquisition View V2

Vue d'acquisition en temps réel version 2 pour CHNeoWave
avec design maritime moderne et proportions basées sur le nombre d'or.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFrame, QGridLayout,
    QGroupBox, QSpinBox, QDoubleSpinBox, QComboBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap

from ..components.modern_card import ModernCard
from ..components.animated_button import AnimatedButton
from ..components.kpi_card import KPICard
from ..styles.maritime_theme import MaritimeTheme


class LiveAcquisitionViewV2(QWidget):
    """Vue d'acquisition en temps réel avec design maritime moderne"""
    
    # Constante du nombre d'or
    PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749
    
    # Signaux
    acquisitionStarted = Signal()
    acquisitionStopped = Signal()
    acquisitionPaused = Signal()
    acquisitionResumed = Signal()
    dataReceived = Signal(dict)
    errorOccurred = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = MaritimeTheme()
        self.is_acquiring = False
        self.is_paused = False
        self.acquisition_data = {}
        self.sample_count = 0
        self.acquisition_timer = QTimer()
        
        self.setup_ui()
        self.setup_connections()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.setObjectName("live-acquisition-view")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            self.theme.spacing['lg'], self.theme.spacing['lg'],
            self.theme.spacing['lg'], self.theme.spacing['lg']
        )
        main_layout.setSpacing(self.theme.spacing['md'])
        
        # Header avec titre et contrôles
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Zone principale avec KPIs et graphiques
        content_widget = self.create_content_area()
        main_layout.addWidget(content_widget)
        
        # Footer avec statut et contrôles
        footer_widget = self.create_footer()
        main_layout.addWidget(footer_widget)
        
        # Proportions basées sur le nombre d'or
        main_layout.setStretchFactor(header_widget, 1)  # 16%
        main_layout.setStretchFactor(content_widget, 4)  # 64%
        main_layout.setStretchFactor(footer_widget, 1)  # 20%
        
    def create_header(self):
        """Création de l'en-tête avec titre et contrôles"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(self.theme.spacing['md'])
        
        # Titre principal
        title_label = QLabel("🌊 Acquisition en Temps Réel")
        title_label.setObjectName("acquisition-title")
        
        # Font du titre
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Contrôles d'acquisition
        controls_widget = self.create_acquisition_controls()
        header_layout.addWidget(controls_widget)
        
        return header_widget
        
    def create_acquisition_controls(self):
        """Création des contrôles d'acquisition"""
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(self.theme.spacing['sm'])
        
        # Bouton Start/Stop
        self.start_stop_button = AnimatedButton(
            "▶ Démarrer"
        )
        self.start_stop_button.clicked.connect(self.toggle_acquisition)
        
        # Bouton Pause/Resume
        self.pause_resume_button = AnimatedButton(
            "⏸ Pause"
        )
        self.pause_resume_button.clicked.connect(self.toggle_pause)
        self.pause_resume_button.setEnabled(False)
        
        # Bouton Reset
        self.reset_button = AnimatedButton(
            "🔄 Reset"
        )
        self.reset_button.clicked.connect(self.reset_acquisition)
        
        controls_layout.addWidget(self.start_stop_button)
        controls_layout.addWidget(self.pause_resume_button)
        controls_layout.addWidget(self.reset_button)
        
        return controls_widget
        
    def create_content_area(self):
        """Création de la zone de contenu principal"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(self.theme.spacing['md'])
        
        # Zone des KPIs
        kpis_widget = self.create_kpis_section()
        content_layout.addWidget(kpis_widget)
        
        # Zone des paramètres d'acquisition
        params_widget = self.create_parameters_section()
        content_layout.addWidget(params_widget)
        
        # Zone de visualisation (placeholder)
        viz_widget = self.create_visualization_section()
        content_layout.addWidget(viz_widget)
        
        # Proportions
        content_layout.setStretchFactor(kpis_widget, 1)
        content_layout.setStretchFactor(params_widget, 1)
        content_layout.setStretchFactor(viz_widget, 3)
        
        return content_widget
        
    def create_kpis_section(self):
        """Création de la section des KPIs"""
        kpis_widget = QWidget()
        kpis_layout = QHBoxLayout(kpis_widget)
        kpis_layout.setContentsMargins(0, 0, 0, 0)
        kpis_layout.setSpacing(self.theme.spacing['md'])
        
        # KPI: Échantillons collectés
        self.samples_kpi = KPICard(
            title="Échantillons",
            value="0",
            unit="samples",
            status="info",
            size="sm"
        )
        
        # KPI: Fréquence d'échantillonnage
        self.frequency_kpi = KPICard(
            title="Fréquence",
            value="0",
            unit="Hz",
            status="info",
            size="sm"
        )
        
        # KPI: Durée d'acquisition
        self.duration_kpi = KPICard(
            title="Durée",
            value="00:00",
            unit="mm:ss",
            status="info",
            size="sm"
        )
        
        # KPI: Statut des capteurs
        self.sensors_kpi = KPICard(
            title="Capteurs",
            value="4/4",
            unit="actifs",
            status="success",
            size="sm"
        )
        
        kpis_layout.addWidget(self.samples_kpi)
        kpis_layout.addWidget(self.frequency_kpi)
        kpis_layout.addWidget(self.duration_kpi)
        kpis_layout.addWidget(self.sensors_kpi)
        
        return kpis_widget
        
    def create_parameters_section(self):
        """Création de la section des paramètres"""
        params_card = ModernCard(
            title="⚙️ Paramètres d'Acquisition"
        )
        
        params_layout = QGridLayout()
        params_layout.setSpacing(self.theme.spacing['sm'])
        
        # Fréquence d'échantillonnage
        freq_label = QLabel("Fréquence (Hz):")
        self.frequency_spinbox = QSpinBox()
        self.frequency_spinbox.setRange(1, 1000)
        self.frequency_spinbox.setValue(100)
        self.frequency_spinbox.setSuffix(" Hz")
        
        # Durée d'acquisition
        duration_label = QLabel("Durée (s):")
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 3600)
        self.duration_spinbox.setValue(60)
        self.duration_spinbox.setSuffix(" s")
        
        # Mode d'acquisition
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Continu", "Burst", "Trigger"])
        
        # Gain
        gain_label = QLabel("Gain:")
        self.gain_spinbox = QDoubleSpinBox()
        self.gain_spinbox.setRange(0.1, 10.0)
        self.gain_spinbox.setValue(1.0)
        self.gain_spinbox.setSingleStep(0.1)
        self.gain_spinbox.setSuffix("x")
        
        # Disposition en grille
        params_layout.addWidget(freq_label, 0, 0)
        params_layout.addWidget(self.frequency_spinbox, 0, 1)
        params_layout.addWidget(duration_label, 0, 2)
        params_layout.addWidget(self.duration_spinbox, 0, 3)
        params_layout.addWidget(mode_label, 1, 0)
        params_layout.addWidget(self.mode_combo, 1, 1)
        params_layout.addWidget(gain_label, 1, 2)
        params_layout.addWidget(self.gain_spinbox, 1, 3)
        
        params_card.add_content_layout(params_layout)
        
        return params_card
        
    def create_visualization_section(self):
        """Création de la section de visualisation"""
        viz_card = ModernCard(
            title="📊 Visualisation en Temps Réel"
        )
        
        viz_layout = QVBoxLayout()
        
        # Placeholder pour les graphiques
        placeholder_label = QLabel(
            "Zone de visualisation des données en temps réel\n\n"
            "Les graphiques s'afficheront ici pendant l'acquisition:\n"
            "• Signal temporel des capteurs de houle\n"
            "• Spectre de fréquence\n"
            "• Statistiques en temps réel\n"
            "• Indicateurs de qualité du signal"
        )
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setStyleSheet(
            f"color: {self.theme.colors['on_surface_variant']}; "
            f"background-color: {self.theme.colors['surface']}; "
            f"border: 2px dashed {self.theme.colors['border']}; "
            f"border-radius: 12px; "
            f"padding: {self.theme.spacing['xl']}px;"
        )
        
        viz_layout.addWidget(placeholder_label)
        viz_card.add_content_layout(viz_layout)
        
        return viz_card
        
    def create_footer(self):
        """Création du footer avec statut"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(self.theme.spacing['md'])
        
        # Statut de l'acquisition
        self.status_label = QLabel("📴 Acquisition arrêtée")
        self.status_label.setObjectName("acquisition-status")
        
        status_font = QFont()
        status_font.setPointSize(12)
        status_font.setWeight(QFont.Bold)
        self.status_label.setFont(status_font)
        
        footer_layout.addWidget(self.status_label)
        footer_layout.addStretch()
        
        # Barre de progression (pour acquisitions à durée limitée)
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("acquisition-progress")
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        
        footer_layout.addWidget(self.progress_bar)
        
        return footer_widget
        
    def setup_connections(self):
        """Configuration des connexions de signaux"""
        # Timer pour simulation de données
        self.acquisition_timer.timeout.connect(self.simulate_data_acquisition)
        
    def toggle_acquisition(self):
        """Basculer l'état d'acquisition"""
        if not self.is_acquiring:
            self.start_acquisition()
        else:
            self.stop_acquisition()
            
    def start_acquisition(self):
        """Démarrer l'acquisition"""
        self.is_acquiring = True
        self.is_paused = False
        self.sample_count = 0
        
        # Mettre à jour l'interface
        self.start_stop_button.setText("⏹ Arrêter")
        self.start_stop_button.set_type("error")
        self.pause_resume_button.setEnabled(True)
        self.status_label.setText("🔴 Acquisition en cours...")
        
        # Démarrer le timer de simulation
        frequency = self.frequency_spinbox.value()
        self.acquisition_timer.start(1000 // frequency)  # Intervalle en ms
        
        # Afficher la barre de progression si durée limitée
        if self.mode_combo.currentText() != "Continu":
            self.progress_bar.setVisible(True)
            
        self.acquisitionStarted.emit()
        
    def stop_acquisition(self):
        """Arrêter l'acquisition"""
        self.is_acquiring = False
        self.is_paused = False
        
        # Arrêter le timer
        self.acquisition_timer.stop()
        
        # Mettre à jour l'interface
        self.start_stop_button.setText("▶ Démarrer")
        self.start_stop_button.set_type("primary")
        self.pause_resume_button.setEnabled(False)
        self.pause_resume_button.setText("⏸ Pause")
        self.status_label.setText("📴 Acquisition arrêtée")
        self.progress_bar.setVisible(False)
        
        self.acquisitionStopped.emit()
        
    def toggle_pause(self):
        """Basculer l'état de pause"""
        if not self.is_paused:
            self.pause_acquisition()
        else:
            self.resume_acquisition()
            
    def pause_acquisition(self):
        """Mettre en pause l'acquisition"""
        self.is_paused = True
        self.acquisition_timer.stop()
        
        self.pause_resume_button.setText("▶ Reprendre")
        self.status_label.setText("⏸ Acquisition en pause")
        
        self.acquisitionPaused.emit()
        
    def resume_acquisition(self):
        """Reprendre l'acquisition"""
        self.is_paused = False
        frequency = self.frequency_spinbox.value()
        self.acquisition_timer.start(1000 // frequency)
        
        self.pause_resume_button.setText("⏸ Pause")
        self.status_label.setText("🔴 Acquisition en cours...")
        
        self.acquisitionResumed.emit()
        
    def reset_acquisition(self):
        """Réinitialiser l'acquisition"""
        if self.is_acquiring:
            self.stop_acquisition()
            
        self.sample_count = 0
        self.acquisition_data = {}
        
        # Réinitialiser les KPIs
        self.samples_kpi.update_value("0")
        self.frequency_kpi.update_value("0")
        self.duration_kpi.update_value("00:00")
        
    def simulate_data_acquisition(self):
        """Simulation de l'acquisition de données"""
        if not self.is_acquiring or self.is_paused:
            return
            
        self.sample_count += 1
        
        # Simuler des données
        import random
        data = {
            'timestamp': self.sample_count / self.frequency_spinbox.value(),
            'wave_sensor_1': random.uniform(-0.1, 0.1),
            'wave_sensor_2': random.uniform(-0.1, 0.1),
            'pressure': random.uniform(1000, 1020),
            'temperature': random.uniform(18, 22)
        }
        
        # Mettre à jour les KPIs
        self.samples_kpi.update_value(str(self.sample_count))
        self.frequency_kpi.update_value(str(self.frequency_spinbox.value()))
        
        # Calculer la durée
        duration_seconds = self.sample_count // self.frequency_spinbox.value()
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        self.duration_kpi.update_value(f"{minutes:02d}:{seconds:02d}")
        
        # Émettre les données
        self.dataReceived.emit(data)
        
        # Vérifier si l'acquisition doit s'arrêter (mode non-continu)
        if self.mode_combo.currentText() != "Continu":
            max_duration = self.duration_spinbox.value()
            if duration_seconds >= max_duration:
                self.stop_acquisition()
                
    def apply_styles(self):
        """Application des styles CSS"""
        self.setStyleSheet(f"""
            QWidget#live-acquisition-view {{
                background-color: {self.theme.colors['background']};
                color: {self.theme.colors['on_surface']};
            }}
            
            QLabel#acquisition-title {{
                color: {self.theme.colors['primary']};
                font-weight: bold;
                margin: {self.theme.spacing['md']}px 0;
            }}
            
            QLabel#acquisition-status {{
                color: {self.theme.colors['on_surface_variant']};
                padding: {self.theme.spacing['sm']}px {self.theme.spacing['md']}px;
                border-radius: 8px;
                background-color: {self.theme.colors['surface']};
            }}
            
            QProgressBar#acquisition-progress {{
                border: 2px solid {self.theme.colors['border']};
                border-radius: 8px;
                text-align: center;
                height: 24px;
                min-width: 200px;
            }}
            
            QProgressBar#acquisition-progress::chunk {{
                background-color: {self.theme.colors['primary']};
                border-radius: 6px;
            }}
            
            QSpinBox, QDoubleSpinBox, QComboBox {{
                border: 2px solid {self.theme.colors['border']};
                border-radius: 6px;
                padding: 4px 8px;
                background-color: {self.theme.colors['surface']};
                min-width: 80px;
            }}
            
            QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
                border-color: {self.theme.colors['primary']};
            }}
        """)