# -*- coding: utf-8 -*-
"""
Infos Essai Dock

Widget dock pour afficher les informations d'essai en cours
avec design maritime moderne et proportions basées sur le nombre d'or.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

import math
from PySide6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGridLayout, QGroupBox, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QPixmap

from ..components.modern_card import ModernCard
from ..components.kpi_card import KPICard
from ..styles.maritime_theme import MaritimeTheme


class InfosEssaiDock(QDockWidget):
    """Widget dock pour les informations d'essai avec design maritime moderne"""
    
    # Constante du nombre d'or
    PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749
    
    # Signaux
    essaiUpdated = Signal(dict)
    parametersChanged = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__("📋 Informations d'Essai", parent)
        self.theme = MaritimeTheme()
        self.essai_data = {}
        self.update_timer = QTimer()
        
        self.setup_ui()
        self.setup_connections()
        self.apply_styles()
        self.load_default_data()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.setObjectName("infos-essai-dock")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetClosable
        )
        
        # Widget principal
        main_widget = QWidget()
        main_widget.setObjectName("dock-main-widget")
        self.setWidget(main_widget)
        
        # Layout principal avec scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("essai-scroll")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(
            self.theme.spacing['md'], self.theme.spacing['md'],
            self.theme.spacing['md'], self.theme.spacing['md']
        )
        content_layout.setSpacing(self.theme.spacing['md'])
        
        # Section informations générales
        general_info_widget = self.create_general_info_section()
        content_layout.addWidget(general_info_widget)
        
        # Section paramètres d'acquisition
        acquisition_params_widget = self.create_acquisition_params_section()
        content_layout.addWidget(acquisition_params_widget)
        
        # Section conditions d'essai
        conditions_widget = self.create_conditions_section()
        content_layout.addWidget(conditions_widget)
        
        # Section statistiques en temps réel
        stats_widget = self.create_stats_section()
        content_layout.addWidget(stats_widget)
        
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        
        # Layout du widget principal
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
    def create_general_info_section(self):
        """Création de la section informations générales"""
        info_card = ModernCard(
            title="ℹ️ Informations Générales"
        )
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(self.theme.spacing['sm'])
        
        # Nom de l'essai
        self.essai_name_label = QLabel("Nom: Essai Houle #001")
        self.essai_name_label.setObjectName("info-label")
        
        # Date et heure
        self.datetime_label = QLabel("Date: 26/01/2025 14:30")
        self.datetime_label.setObjectName("info-label")
        
        # Opérateur
        self.operator_label = QLabel("Opérateur: Dr. Marine")
        self.operator_label.setObjectName("info-label")
        
        # Projet
        self.project_label = QLabel("Projet: Méditerranée 2025")
        self.project_label.setObjectName("info-label")
        
        # Statut
        self.status_label = QLabel("Statut: 🔴 En cours")
        self.status_label.setObjectName("status-label")
        
        info_layout.addWidget(self.essai_name_label)
        info_layout.addWidget(self.datetime_label)
        info_layout.addWidget(self.operator_label)
        info_layout.addWidget(self.project_label)
        info_layout.addWidget(self.status_label)
        
        info_card.add_content_layout(info_layout)
        
        return info_card
        
    def create_acquisition_params_section(self):
        """Création de la section paramètres d'acquisition"""
        params_card = ModernCard(
            title="⚙️ Paramètres d'Acquisition"
        )
        
        params_layout = QVBoxLayout()
        params_layout.setSpacing(self.theme.spacing['sm'])
        
        # Fréquence d'échantillonnage
        self.sampling_freq_label = QLabel("Fréquence: 100 Hz")
        self.sampling_freq_label.setObjectName("param-label")
        
        # Durée d'acquisition
        self.duration_label = QLabel("Durée: 300 s")
        self.duration_label.setObjectName("param-label")
        
        # Nombre de capteurs
        self.sensors_count_label = QLabel("Capteurs: 4 actifs")
        self.sensors_count_label.setObjectName("param-label")
        
        # Mode d'acquisition
        self.acquisition_mode_label = QLabel("Mode: Continu")
        self.acquisition_mode_label.setObjectName("param-label")
        
        # Gain
        self.gain_label = QLabel("Gain: 1.0x")
        self.gain_label.setObjectName("param-label")
        
        # Filtre
        self.filter_label = QLabel("Filtre: Passe-bas 50Hz")
        self.filter_label.setObjectName("param-label")
        
        params_layout.addWidget(self.sampling_freq_label)
        params_layout.addWidget(self.duration_label)
        params_layout.addWidget(self.sensors_count_label)
        params_layout.addWidget(self.acquisition_mode_label)
        params_layout.addWidget(self.gain_label)
        params_layout.addWidget(self.filter_label)
        
        params_card.add_content_layout(params_layout)
        
        return params_card
        
    def create_conditions_section(self):
        """Création de la section conditions d'essai"""
        conditions_card = ModernCard(
            title="🌊 Conditions d'Essai"
        )
        
        conditions_layout = QVBoxLayout()
        conditions_layout.setSpacing(self.theme.spacing['sm'])
        
        # Température de l'eau
        self.water_temp_label = QLabel("Temp. eau: 20.5°C")
        self.water_temp_label.setObjectName("condition-label")
        
        # Température ambiante
        self.ambient_temp_label = QLabel("Temp. ambiante: 22.1°C")
        self.ambient_temp_label.setObjectName("condition-label")
        
        # Pression atmosphérique
        self.pressure_label = QLabel("Pression: 1013.2 hPa")
        self.pressure_label.setObjectName("condition-label")
        
        # Humidité
        self.humidity_label = QLabel("Humidité: 65%")
        self.humidity_label.setObjectName("condition-label")
        
        # Niveau d'eau
        self.water_level_label = QLabel("Niveau eau: 0.80 m")
        self.water_level_label.setObjectName("condition-label")
        
        # Vent (si applicable)
        self.wind_label = QLabel("Vent: 2.3 m/s NE")
        self.wind_label.setObjectName("condition-label")
        
        conditions_layout.addWidget(self.water_temp_label)
        conditions_layout.addWidget(self.ambient_temp_label)
        conditions_layout.addWidget(self.pressure_label)
        conditions_layout.addWidget(self.humidity_label)
        conditions_layout.addWidget(self.water_level_label)
        conditions_layout.addWidget(self.wind_label)
        
        conditions_card.add_content_layout(conditions_layout)
        
        return conditions_card
        
    def create_stats_section(self):
        """Création de la section statistiques temps réel"""
        stats_card = ModernCard(
            title="📊 Statistiques Temps Réel"
        )
        
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(self.theme.spacing['sm'])
        
        # KPIs compacts
        kpis_layout = QVBoxLayout()
        kpis_layout.setSpacing(self.theme.spacing['xs'])
        
        # Échantillons collectés
        self.samples_kpi = KPICard(
            title="Échantillons",
            value="0",
            unit="samples",
            status="info",
            size="sm"
        )
        
        # Temps écoulé
        self.elapsed_time_kpi = KPICard(
            title="Temps écoulé",
            value="00:00",
            unit="mm:ss",
            status="info",
            size="sm"
        )
        
        # Amplitude max
        self.max_amplitude_kpi = KPICard(
            title="Amplitude max",
            value="0.00",
            unit="mm",
            status="success",
            size="sm"
        )
        
        # Fréquence dominante
        self.dominant_freq_kpi = KPICard(
            title="Freq. dominante",
            value="0.0",
            unit="Hz",
            status="info",
            size="sm"
        )
        
        kpis_layout.addWidget(self.samples_kpi)
        kpis_layout.addWidget(self.elapsed_time_kpi)
        kpis_layout.addWidget(self.max_amplitude_kpi)
        kpis_layout.addWidget(self.dominant_freq_kpi)
        
        stats_layout.addLayout(kpis_layout)
        
        stats_card.add_content_layout(stats_layout)
        
        return stats_card
        
    def setup_connections(self):
        """Configuration des connexions de signaux"""
        # Timer pour mise à jour automatique
        self.update_timer.timeout.connect(self.update_real_time_stats)
        self.update_timer.start(1000)  # Mise à jour chaque seconde
        
    def load_default_data(self):
        """Chargement des données par défaut"""
        self.essai_data = {
            'name': 'Essai Houle #001',
            'date': '26/01/2025',
            'time': '14:30',
            'operator': 'Dr. Marine',
            'project': 'Méditerranée 2025',
            'status': 'En cours',
            'sampling_frequency': 100,
            'duration': 300,
            'sensors_count': 4,
            'mode': 'Continu',
            'gain': 1.0,
            'filter': 'Passe-bas 50Hz',
            'water_temperature': 20.5,
            'ambient_temperature': 22.1,
            'pressure': 1013.2,
            'humidity': 65,
            'water_level': 0.80,
            'wind_speed': 2.3,
            'wind_direction': 'NE'
        }
        
    def update_essai_info(self, essai_data):
        """Mise à jour des informations d'essai"""
        self.essai_data.update(essai_data)
        
        # Mettre à jour les labels
        if 'name' in essai_data:
            self.essai_name_label.setText(f"Nom: {essai_data['name']}")
            
        if 'operator' in essai_data:
            self.operator_label.setText(f"Opérateur: {essai_data['operator']}")
            
        if 'project' in essai_data:
            self.project_label.setText(f"Projet: {essai_data['project']}")
            
        if 'status' in essai_data:
            status_icon = "🔴" if essai_data['status'] == "En cours" else "⏹️"
            self.status_label.setText(f"Statut: {status_icon} {essai_data['status']}")
            
        self.essaiUpdated.emit(self.essai_data)
        
    def update_acquisition_params(self, params):
        """Mise à jour des paramètres d'acquisition"""
        if 'sampling_frequency' in params:
            self.sampling_freq_label.setText(f"Fréquence: {params['sampling_frequency']} Hz")
            
        if 'duration' in params:
            self.duration_label.setText(f"Durée: {params['duration']} s")
            
        if 'sensors_count' in params:
            self.sensors_count_label.setText(f"Capteurs: {params['sensors_count']} actifs")
            
        if 'mode' in params:
            self.acquisition_mode_label.setText(f"Mode: {params['mode']}")
            
        if 'gain' in params:
            self.gain_label.setText(f"Gain: {params['gain']}x")
            
        if 'filter' in params:
            self.filter_label.setText(f"Filtre: {params['filter']}")
            
        self.parametersChanged.emit(params)
        
    def update_conditions(self, conditions):
        """Mise à jour des conditions d'essai"""
        if 'water_temperature' in conditions:
            self.water_temp_label.setText(f"Temp. eau: {conditions['water_temperature']:.1f}°C")
            
        if 'ambient_temperature' in conditions:
            self.ambient_temp_label.setText(f"Temp. ambiante: {conditions['ambient_temperature']:.1f}°C")
            
        if 'pressure' in conditions:
            self.pressure_label.setText(f"Pression: {conditions['pressure']:.1f} hPa")
            
        if 'humidity' in conditions:
            self.humidity_label.setText(f"Humidité: {conditions['humidity']}%")
            
        if 'water_level' in conditions:
            self.water_level_label.setText(f"Niveau eau: {conditions['water_level']:.2f} m")
            
        if 'wind_speed' in conditions and 'wind_direction' in conditions:
            self.wind_label.setText(f"Vent: {conditions['wind_speed']:.1f} m/s {conditions['wind_direction']}")
            
    def update_real_time_stats(self):
        """Mise à jour des statistiques en temps réel"""
        # Simulation de données en temps réel
        import random
        import time
        
        # Simuler l'incrémentation des échantillons
        current_samples = int(self.samples_kpi.value) if self.samples_kpi.value.isdigit() else 0
        new_samples = current_samples + random.randint(1, 5)
        self.samples_kpi.update_value(str(new_samples))
        
        # Calculer le temps écoulé (simulation)
        elapsed_seconds = new_samples // 100  # Basé sur 100 Hz
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        self.elapsed_time_kpi.update_value(f"{minutes:02d}:{seconds:02d}")
        
        # Amplitude maximale simulée
        max_amplitude = random.uniform(0.1, 5.0)
        self.max_amplitude_kpi.update_value(f"{max_amplitude:.2f}")
        
        # Fréquence dominante simulée
        dominant_freq = random.uniform(0.5, 2.0)
        self.dominant_freq_kpi.update_value(f"{dominant_freq:.1f}")
        
    def start_acquisition(self):
        """Démarrer l'acquisition (mise à jour du statut)"""
        self.update_essai_info({'status': 'En cours'})
        
    def stop_acquisition(self):
        """Arrêter l'acquisition (mise à jour du statut)"""
        self.update_essai_info({'status': 'Arrêté'})
        
    def apply_styles(self):
        """Application des styles CSS"""
        self.setStyleSheet(f"""
            QDockWidget#infos-essai-dock {{
                background-color: {self.theme.colors['background']};
                color: {self.theme.colors['on_surface']};
                border: 2px solid {self.theme.colors['border']};
                border-radius: 8px;
            }}
            
            QDockWidget#infos-essai-dock::title {{
                background-color: {self.theme.colors['primary']};
                color: white;
                padding: {self.theme.spacing['sm']}px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }}
            
            QWidget#dock-main-widget {{
                background-color: {self.theme.colors['background']};
                border: none;
            }}
            
            QScrollArea#essai-scroll {{
                border: none;
                background-color: transparent;
            }}
            
            QScrollArea#essai-scroll QScrollBar:vertical {{
                border: none;
                background-color: {self.theme.colors['surface']};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollArea#essai-scroll QScrollBar::handle:vertical {{
                background-color: {self.theme.colors['border']};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollArea#essai-scroll QScrollBar::handle:vertical:hover {{
                background-color: {self.theme.colors['primary']};
            }}
            
            QLabel#info-label, QLabel#param-label, QLabel#condition-label {{
                color: {self.theme.colors['on_surface']};
                font-size: 12px;
                padding: 2px 0;
                border-bottom: 1px solid {self.theme.colors['border']};
            }}
            
            QLabel#status-label {{
                color: {self.theme.colors['on_surface']};
                font-weight: bold;
                font-size: 12px;
                padding: {self.theme.spacing['xs']}px;
                border-radius: 4px;
                background-color: {self.theme.colors['surface']};
            }}
        """)