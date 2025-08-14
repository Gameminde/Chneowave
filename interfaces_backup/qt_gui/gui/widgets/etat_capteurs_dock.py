# -*- coding: utf-8 -*-
"""
Etat Capteurs Dock

Widget dock pour afficher l'état des capteurs en temps réel
avec design maritime moderne et proportions basées sur le nombre d'or.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

import math
from PySide6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGridLayout, QGroupBox, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QBrush

from ..components.modern_card import ModernCard
from .kpi_card import KPICard
from ..components.animated_button import AnimatedButton
from ..styles.maritime_theme import MaritimeTheme


class SensorStatusWidget(QWidget):
    """Widget pour afficher l'état d'un capteur individuel"""
    
    def __init__(self, sensor_id, sensor_name, parent=None):
        super().__init__(parent)
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.status = "disconnected"  # connected, disconnected, error, calibrating
        self.value = 0.0
        self.unit = "mm"
        self.theme = MaritimeTheme()
        
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface du capteur"""
        self.setObjectName(f"sensor-{self.sensor_id}")
        self.setFixedHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Indicateur de statut (cercle coloré)
        self.status_indicator = QLabel()
        self.status_indicator.setFixedSize(16, 16)
        self.status_indicator.setObjectName("status-indicator")
        
        # Informations du capteur
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        self.name_label = QLabel(self.sensor_name)
        self.name_label.setObjectName("sensor-name")
        self.name_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.id_label = QLabel(f"ID: {self.sensor_id}")
        self.id_label.setObjectName("sensor-id")
        self.id_label.setFont(QFont("Arial", 8))
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.id_label)
        
        # Valeur du capteur
        value_layout = QVBoxLayout()
        value_layout.setSpacing(2)
        
        self.value_label = QLabel("--")
        self.value_label.setObjectName("sensor-value")
        self.value_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignRight)
        
        self.unit_label = QLabel(self.unit)
        self.unit_label.setObjectName("sensor-unit")
        self.unit_label.setFont(QFont("Arial", 8))
        self.unit_label.setAlignment(Qt.AlignRight)
        
        value_layout.addWidget(self.value_label)
        value_layout.addWidget(self.unit_label)
        
        layout.addWidget(self.status_indicator)
        layout.addLayout(info_layout, 2)
        layout.addLayout(value_layout, 1)
        
        self.update_status_indicator()
        
    def update_status(self, status, value=None):
        """Mise à jour du statut du capteur"""
        self.status = status
        if value is not None:
            self.value = value
            self.value_label.setText(f"{value:.2f}")
        else:
            self.value_label.setText("--")
            
        self.update_status_indicator()
        
    def update_status_indicator(self):
        """Mise à jour de l'indicateur de statut"""
        colors = {
            "connected": "#10B981",      # Vert
            "disconnected": "#6B7280",  # Gris
            "error": "#EF4444",         # Rouge
            "calibrating": "#F59E0B"    # Orange
        }
        
        color = colors.get(self.status, "#6B7280")
        self.status_indicator.setStyleSheet(f"""
            QLabel#status-indicator {{
                background-color: {color};
                border-radius: 8px;
                border: 2px solid white;
            }}
        """)
        
    def apply_styles(self):
        """Application des styles CSS"""
        self.setStyleSheet(f"""
            QWidget#sensor-{self.sensor_id} {{
                background-color: {self.theme.colors['surface']};
                border: 1px solid {self.theme.colors['border']};
                border-radius: 8px;
                margin: 2px;
            }}
            
            QWidget#sensor-{self.sensor_id}:hover {{
                border-color: {self.theme.colors['primary']};
                background-color: {self.theme.colors['background']};
            }}
            
            QLabel#sensor-name {{
                color: {self.theme.colors['on_surface']};
            }}
            
            QLabel#sensor-id {{
                color: {self.theme.colors['on_surface_variant']};
            }}
            
            QLabel#sensor-value {{
                color: {self.theme.colors['primary']};
            }}
            
            QLabel#sensor-unit {{
                color: {self.theme.colors['on_surface_variant']};
            }}
        """)


class EtatCapteursDock(QDockWidget):
    """Widget dock pour l'état des capteurs avec design maritime moderne"""
    
    # Constante du nombre d'or
    PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749
    
    # Signaux
    sensorStatusChanged = Signal(str, str, float)  # sensor_id, status, value
    calibrationRequested = Signal(str)  # sensor_id
    diagnosticRequested = Signal()
    capteur_selected = Signal(str)  # sensor_id
    capteurs_updated = Signal()  # signal when sensors are updated
    
    def __init__(self, parent=None):
        super().__init__("🔧 État des Capteurs", parent)
        self.theme = MaritimeTheme()
        self.sensors = {}
        self.update_timer = QTimer()
        
        self.setup_ui()
        self.setup_connections()
        self.apply_styles()
        self.initialize_sensors()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.setObjectName("etat-capteurs-dock")
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
        
        # Layout principal
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(
            self.theme.spacing['sm'], self.theme.spacing['sm'],
            self.theme.spacing['sm'], self.theme.spacing['sm']
        )
        main_layout.setSpacing(self.theme.spacing['sm'])
        
        # Section résumé global
        summary_widget = self.create_summary_section()
        main_layout.addWidget(summary_widget)
        
        # Section liste des capteurs
        sensors_widget = self.create_sensors_section()
        main_layout.addWidget(sensors_widget)
        
        # Section actions
        actions_widget = self.create_actions_section()
        main_layout.addWidget(actions_widget)
        
        # Proportions basées sur le nombre d'or
        main_layout.setStretchFactor(summary_widget, 1)
        main_layout.setStretchFactor(sensors_widget, 4)
        main_layout.setStretchFactor(actions_widget, 1)
        
    def create_summary_section(self):
        """Création de la section résumé global"""
        summary_card = ModernCard(
            title="📊 Résumé Global"
        )
        
        summary_layout = QVBoxLayout()
        summary_layout.setSpacing(self.theme.spacing['xs'])
        
        # KPIs compacts
        self.total_sensors_kpi = KPICard(
            title="Total",
            value="8",
            unit="capteurs",
            status="normal"
        )
        
        self.active_sensors_kpi = KPICard(
            title="Actifs",
            value="6",
            unit="capteurs",
            status="success"
        )
        
        self.error_sensors_kpi = KPICard(
            title="Erreurs",
            value="0",
            unit="capteurs",
            status="normal"
        )
        
        summary_layout.addWidget(self.total_sensors_kpi)
        summary_layout.addWidget(self.active_sensors_kpi)
        summary_layout.addWidget(self.error_sensors_kpi)
        
        summary_card.add_content_layout(summary_layout)
        
        return summary_card
        
    def create_sensors_section(self):
        """Création de la section liste des capteurs"""
        sensors_card = ModernCard(
            title="🌊 Capteurs de Houle"
        )
        
        # Scroll area pour la liste des capteurs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("sensors-scroll")
        
        sensors_content = QWidget()
        self.sensors_layout = QVBoxLayout(sensors_content)
        self.sensors_layout.setContentsMargins(0, 0, 0, 0)
        self.sensors_layout.setSpacing(self.theme.spacing['xs'])
        
        scroll_area.setWidget(sensors_content)
        
        sensors_card.set_content_widget(scroll_area)
        
        return sensors_card
        
    def create_actions_section(self):
        """Création de la section actions"""
        actions_card = ModernCard(
            title="⚙️ Actions"
        )
        
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(self.theme.spacing['xs'])
        
        # Bouton calibration globale
        self.calibrate_all_button = AnimatedButton("🔧 Calibrer Tout")
        self.calibrate_all_button.set_primary_style()
        self.calibrate_all_button.clicked.connect(self.calibrate_all_sensors)
        
        # Bouton diagnostic
        self.diagnostic_button = AnimatedButton("🔍 Diagnostic")
        self.diagnostic_button.set_secondary_style()
        self.diagnostic_button.clicked.connect(self.run_diagnostic)
        
        # Bouton rafraîchir
        self.refresh_button = AnimatedButton("🔄 Rafraîchir")
        self.refresh_button.set_secondary_style()
        self.refresh_button.clicked.connect(self.refresh_sensors)
        
        actions_layout.addWidget(self.calibrate_all_button)
        actions_layout.addWidget(self.diagnostic_button)
        actions_layout.addWidget(self.refresh_button)
        
        actions_card.add_content_layout(actions_layout)
        
        return actions_card
        
    def initialize_sensors(self):
        """Initialisation des capteurs"""
        sensors_config = [
            {"id": "WS001", "name": "Capteur Houle #1", "unit": "mm"},
            {"id": "WS002", "name": "Capteur Houle #2", "unit": "mm"},
            {"id": "WS003", "name": "Capteur Houle #3", "unit": "mm"},
            {"id": "WS004", "name": "Capteur Houle #4", "unit": "mm"},
            {"id": "PS001", "name": "Capteur Pression", "unit": "hPa"},
            {"id": "TS001", "name": "Capteur Température", "unit": "°C"},
            {"id": "HS001", "name": "Capteur Humidité", "unit": "%"},
            {"id": "WL001", "name": "Capteur Niveau", "unit": "m"}
        ]
        
        for config in sensors_config:
            sensor_widget = SensorStatusWidget(
                config["id"], 
                config["name"]
            )
            sensor_widget.unit = config["unit"]
            sensor_widget.unit_label.setText(config["unit"])
            
            self.sensors[config["id"]] = sensor_widget
            self.sensors_layout.addWidget(sensor_widget)
            
        # Ajouter un stretch à la fin
        self.sensors_layout.addStretch()
        
        # Simuler des statuts initiaux
        self.simulate_initial_status()
        
    def simulate_initial_status(self):
        """Simulation des statuts initiaux des capteurs"""
        import random
        
        statuses = ["connected", "connected", "connected", "connected", 
                   "connected", "connected", "disconnected", "disconnected"]
        
        for i, (sensor_id, sensor_widget) in enumerate(self.sensors.items()):
            status = statuses[i] if i < len(statuses) else "disconnected"
            value = random.uniform(-2.0, 2.0) if status == "connected" else None
            sensor_widget.update_status(status, value)
            
        self.update_summary()
        
    def setup_connections(self):
        """Configuration des connexions de signaux"""
        # Timer pour simulation de données en temps réel
        self.update_timer.timeout.connect(self.update_sensor_values)
        self.update_timer.start(2000)  # Mise à jour toutes les 2 secondes
        
    def update_sensor_values(self):
        """Mise à jour des valeurs des capteurs (simulation)"""
        import random
        
        for sensor_id, sensor_widget in self.sensors.items():
            if sensor_widget.status == "connected":
                # Simuler de nouvelles valeurs
                if sensor_id.startswith("WS"):  # Capteurs de houle
                    new_value = random.uniform(-5.0, 5.0)
                elif sensor_id == "PS001":  # Pression
                    new_value = random.uniform(1010, 1020)
                elif sensor_id == "TS001":  # Température
                    new_value = random.uniform(18, 25)
                elif sensor_id == "HS001":  # Humidité
                    new_value = random.uniform(50, 80)
                elif sensor_id == "WL001":  # Niveau d'eau
                    new_value = random.uniform(0.75, 0.85)
                else:
                    new_value = random.uniform(0, 100)
                    
                sensor_widget.update_status("connected", new_value)
                self.sensorStatusChanged.emit(sensor_id, "connected", new_value)
                
    def update_summary(self):
        """Mise à jour du résumé global"""
        total_sensors = len(self.sensors)
        active_sensors = sum(1 for s in self.sensors.values() if s.status == "connected")
        error_sensors = sum(1 for s in self.sensors.values() if s.status == "error")
        
        self.total_sensors_kpi.update_value(str(total_sensors))
        self.active_sensors_kpi.update_value(str(active_sensors))
        self.error_sensors_kpi.update_value(str(error_sensors))
        
        # Mettre à jour le statut des KPIs
        if error_sensors > 0:
            self.error_sensors_kpi.set_status("critical")
        else:
            self.error_sensors_kpi.set_status("success")
            
        if active_sensors == total_sensors:
            self.active_sensors_kpi.set_status("success")
        elif active_sensors > total_sensors // 2:
            self.active_sensors_kpi.set_status("warning")
        else:
            self.active_sensors_kpi.set_status("critical")
            
    def update_sensor_status(self, sensor_id, status, value=None):
        """Mise à jour du statut d'un capteur spécifique"""
        if sensor_id in self.sensors:
            self.sensors[sensor_id].update_status(status, value)
            self.update_summary()
            self.sensorStatusChanged.emit(sensor_id, status, value or 0.0)
            
    def calibrate_all_sensors(self):
        """Calibration de tous les capteurs"""
        for sensor_id in self.sensors.keys():
            self.calibrationRequested.emit(sensor_id)
            
        # Simuler la calibration
        QTimer.singleShot(2000, self.finish_calibration)
        
    def finish_calibration(self):
        """Finaliser la calibration (simulation)"""
        for sensor_widget in self.sensors.values():
            if sensor_widget.status in ["connected", "calibrating"]:
                sensor_widget.update_status("connected", sensor_widget.value)
                
        self.update_summary()
        
    def run_diagnostic(self):
        """Lancer un diagnostic des capteurs"""
        self.diagnosticRequested.emit()
        
        # Simuler le diagnostic
        import random
        QTimer.singleShot(3000, lambda: self.finish_diagnostic(random.choice([True, False])))
        
    def finish_diagnostic(self, success):
        """Finaliser le diagnostic"""
        if success:
            # Tous les capteurs fonctionnent
            for sensor_widget in self.sensors.values():
                if sensor_widget.status == "disconnected":
                    sensor_widget.update_status("connected", 0.0)
        else:
            # Simuler quelques erreurs
            import random
            error_sensors = random.sample(list(self.sensors.keys()), 2)
            for sensor_id in error_sensors:
                self.sensors[sensor_id].update_status("error")
                
        self.update_summary()
        
    def refresh_sensors(self):
        """Rafraîchir l'état des capteurs"""
        self.simulate_initial_status()
        
    def apply_styles(self):
        """Application des styles CSS"""
        self.setStyleSheet(f"""
            QDockWidget#etat-capteurs-dock {{
                background-color: {self.theme.colors['background']};
                color: {self.theme.colors['on_surface']};
                border: 2px solid {self.theme.colors['border']};
                border-radius: 8px;
            }}
            
            QDockWidget#etat-capteurs-dock::title {{
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
            
            QScrollArea#sensors-scroll {{
                border: none;
                background-color: transparent;
            }}
            
            QScrollArea#sensors-scroll QScrollBar:vertical {{
                border: none;
                background-color: {self.theme.colors['surface']};
                width: 8px;
                border-radius: 4px;
            }}
            
            QScrollArea#sensors-scroll QScrollBar::handle:vertical {{
                background-color: {self.theme.colors['border']};
                border-radius: 4px;
                min-height: 20px;
            }}
            
            QScrollArea#sensors-scroll QScrollBar::handle:vertical:hover {{
                background-color: {self.theme.colors['primary']};
            }}
        """)