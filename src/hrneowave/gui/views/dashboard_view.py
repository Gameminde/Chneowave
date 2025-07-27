# -*- coding: utf-8 -*-
"""
CHNeoWave Dashboard View Maritime 2025
Design System Industriel Maritime - Normes Laboratoires Océaniques
Architecture: Golden Ratio + Palette Maritime Certifiée
"""

import sys
from datetime import datetime
from typing import Dict, List, Optional
import logging

from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QFont, QPalette, QColor

# Alias pour compatibilité
pyqtSignal = Signal

# Imports CHNeoWave avec fallbacks
try:
    from ..components.maritime_widgets import (
        MaritimeCard, KPIIndicator, StatusBeacon, MaritimeButton,
        ProgressStepper, create_kpi_grid, create_action_bar
    )
except ImportError:
    # Fallback si les widgets maritimes ne sont pas encore disponibles
    MaritimeCard = QFrame
    KPIIndicator = QFrame
    StatusBeacon = QFrame
    MaritimeButton = QPushButton
    ProgressStepper = QFrame
    
    def create_kpi_grid(*args, **kwargs):
        return QFrame()
    def create_action_bar(*args, **kwargs):
        return QFrame()

try:
    from ..components.performance_widget import PerformanceWidget
except ImportError:
    # Widget de performance de base si non disponible
    class PerformanceWidget(QFrame):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setMinimumHeight(200)
        def start_monitoring(self):
            pass
        def stop_monitoring(self):
            pass
        def update_metrics(self, metrics):
            pass

try:
    from ..widgets.main_sidebar import MainSidebar
except ImportError:
    # Sidebar de base si non disponible
    class MainSidebar(QFrame):
        navigation_requested = pyqtSignal(str)
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setMinimumWidth(280)

# Classes utilitaires pour le Dashboard Maritime
class PerformanceMetric:
    """Classe pour encapsuler les métriques de performance"""
    def __init__(self, name: str, value: float, unit: str):
        self.name = name
        self.value = value
        self.unit = unit
        self.timestamp = datetime.now()
        
    def __str__(self):
        return f"{self.name}: {self.value}{self.unit}"
        
class ThemeToggle(QPushButton):
    """Bouton de basculement de thème maritime"""
    theme_changed = pyqtSignal(bool)  # True pour dark, False pour light
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = False
        self.setText("🌙")
        self.setToolTip("Basculer vers le thème sombre")
        self.setObjectName("theme-toggle")
        self.clicked.connect(self._toggle_theme)
        
        # Style maritime pour le bouton
        self.setStyleSheet("""
            QPushButton#theme-toggle {
                background-color: transparent;
                border: 2px solid #1565C0;
                border-radius: 20px;
                padding: 8px;
                font-size: 16px;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton#theme-toggle:hover {
                background-color: rgba(21, 101, 192, 0.1);
                border-color: #42A5F5;
            }
            QPushButton#theme-toggle:pressed {
                background-color: rgba(21, 101, 192, 0.2);
            }
        """)
        
    def _toggle_theme(self):
        """Bascule entre les thèmes"""
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.setText("☀️")
            self.setToolTip("Basculer vers le thème clair")
        else:
            self.setText("🌙")
            self.setToolTip("Basculer vers le thème sombre")
            
        self.theme_changed.emit(self.is_dark)

# Constantes Design System Maritime
GOLDEN_RATIO = 1.618
FIBONACCI_SPACES = [8, 13, 21, 34, 55, 89]  # Suite Fibonacci pour espacements
MARITIME_COLORS = {
    'ocean_deep': '#0A1929',
    'harbor_blue': '#1565C0', 
    'tidal_cyan': '#00BCD4',
    'foam_white': '#FAFBFC',
    'storm_gray': '#37474F'
}

logger = logging.getLogger(__name__)

class DashboardViewMaritime(QWidget):
    """
    Dashboard Maritime CHNeoWave 2025
    Architecture Industrielle: Golden Ratio + Design System Maritime
    Optimisé pour laboratoires d'études océaniques sur modèles réduits
    """
    
    # Signaux PyQt6
    navigation_requested = pyqtSignal(str)  # Navigation vers autre vue
    theme_changed = pyqtSignal(bool)  # Changement de thème
    kpi_updated = pyqtSignal(str, str, str)  # KPI mis à jour (nom, valeur, statut)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # État du dashboard
        self.current_theme = "light"  # light | dark
        self.kpi_indicators = {}  # Dictionnaire des indicateurs KPI
        self.performance_widget = None
        self.status_beacons = {}  # Indicateurs d'état système
        self.animation_group = []
        self.is_monitoring_active = False
        
        # Données temps réel (simulation)
        self.system_metrics = {
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0,
            'network_rate': 0,
            'active_sensors': 0,
            'data_buffer': 0
        }
        
        logger.info("Initialisation Dashboard Maritime CHNeoWave")
        
        self._setup_ui()
        self._setup_animations()
        self._setup_data_refresh()
        self._apply_maritime_design_system()
        
    def _setup_ui(self):
        """Configuration interface utilisateur - Design System Maritime 2025"""
        logger.debug("Configuration UI Dashboard Maritime")
        
        # Layout principal horizontal - Architecture Golden Ratio
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === SIDEBAR MARITIME (280px fixe) ===
        self.sidebar = MainSidebar(self)
        self.sidebar.setFixedWidth(280)
        self.sidebar.setObjectName("maritime-sidebar")
        self.sidebar.navigation_requested.connect(self.navigation_requested)
        main_layout.addWidget(self.sidebar)
        
        # === ZONE PRINCIPALE (Golden Ratio) ===
        self.main_area = QWidget()
        self.main_area.setObjectName("maritime-main-area")
        main_layout.addWidget(self.main_area, int(GOLDEN_RATIO * 100))  # Proportion dorée
        
        # Layout vertical zone principale
        main_area_layout = QVBoxLayout(self.main_area)
        main_area_layout.setContentsMargins(
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2], 
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2]
        )
        main_area_layout.setSpacing(FIBONACCI_SPACES[2])
        
        # === HEADER MARITIME ===
        self._setup_maritime_header(main_area_layout)
        
        # === ZONE DE CONTENU SCROLLABLE ===
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setObjectName("maritime-scroll-area")
        
        # Contenu scrollable
        scroll_content = QWidget()
        scroll_content.setObjectName("maritime-scroll-content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, FIBONACCI_SPACES[2], 0)
        scroll_layout.setSpacing(FIBONACCI_SPACES[3])
        
        # === SECTIONS PRINCIPALES ===
        self._setup_status_overview(scroll_layout)  # Vue d'ensemble système
        self._setup_kpi_grid_section(scroll_layout)  # Grille KPI maritime
        self._setup_monitoring_section(scroll_layout)  # Monitoring temps réel
        self._setup_charts_section(scroll_layout)  # Graphiques océaniques
        
        # Finalisation
        scroll_area.setWidget(scroll_content)
        main_area_layout.addWidget(scroll_area)
        
        logger.debug("UI Dashboard Maritime configurée avec succès")
        
    def _setup_maritime_header(self, parent_layout):
        """Configuration header maritime avec identité laboratoire océanique"""
        header_card = MaritimeCard(elevation=2)
        header_card.setObjectName("maritime-header-card")
        header_card.setFixedHeight(FIBONACCI_SPACES[5] + FIBONACCI_SPACES[3])  # 89 + 34 = 123px
        
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2], 
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2]
        )
        
        # === SECTION IDENTITÉ ===
        identity_container = QWidget()
        identity_layout = QVBoxLayout(identity_container)
        identity_layout.setContentsMargins(0, 0, 0, 0)
        identity_layout.setSpacing(FIBONACCI_SPACES[1])  # 13px
        
        # Titre principal maritime
        title_label = QLabel("CHNeoWave Maritime")
        title_label.setObjectName("maritime-title")
        title_label.setStyleSheet("""
            QLabel#maritime-title {
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 28px;
                font-weight: 600;
                color: var(--maritime-ocean-deep);
                letter-spacing: -0.5px;
            }
        """)
        
        # Sous-titre laboratoire
        subtitle_label = QLabel(f"Laboratoire Océanique • Modèles Réduits • {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        subtitle_label.setObjectName("maritime-subtitle")
        subtitle_label.setStyleSheet("""
            QLabel#maritime-subtitle {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 400;
                color: var(--maritime-storm-gray);
                letter-spacing: 0.25px;
            }
        """)
        
        identity_layout.addWidget(title_label)
        identity_layout.addWidget(subtitle_label)
        
        # === SECTION STATUS SYSTÈME ===
        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(FIBONACCI_SPACES[2])
        
        # Beacon système principal
        self.system_beacon = StatusBeacon(status="operational")
        self.status_beacons['system'] = self.system_beacon
        
        # Beacon acquisition
        self.acquisition_beacon = StatusBeacon(status="inactive")
        self.status_beacons['acquisition'] = self.acquisition_beacon
        
        # Beacon réseau
        self.network_beacon = StatusBeacon(status="active")
        self.status_beacons['network'] = self.network_beacon
        
        status_layout.addWidget(self.system_beacon)
        status_layout.addWidget(self.acquisition_beacon)
        status_layout.addWidget(self.network_beacon)
        status_layout.addStretch()
        
        # === SECTION CONTRÔLES ===
        controls_container = QWidget()
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(FIBONACCI_SPACES[1])
        
        # Toggle thème maritime
        self.theme_toggle = ThemeToggle()
        self.theme_toggle.theme_changed.connect(self._on_theme_changed)
        
        # Bouton paramètres rapides
        settings_btn = MaritimeButton("Paramètres", button_type="secondary", size="small")
        settings_btn.clicked.connect(lambda: self.navigation_requested.emit("settings"))
        
        controls_layout.addWidget(settings_btn)
        controls_layout.addWidget(self.theme_toggle)
        
        # === ASSEMBLAGE HEADER ===
        header_layout.addWidget(identity_container, 2)  # 40% largeur
        header_layout.addWidget(status_container, 2)    # 40% largeur  
        header_layout.addWidget(controls_container, 1)  # 20% largeur
        
        parent_layout.addWidget(header_card)
        
        logger.debug("Header maritime configuré avec beacons de statut")
        
    def _setup_status_overview(self, parent_layout):
        """Vue d'ensemble rapide du statut système"""
        overview_card = MaritimeCard(elevation=1)
        overview_card.setObjectName("status-overview-card")
        
        overview_layout = QVBoxLayout(overview_card)
        overview_layout.setContentsMargins(
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2],
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2]
        )
        overview_layout.setSpacing(FIBONACCI_SPACES[2])
        
        # Titre section
        title_label = QLabel("Vue d'Ensemble Système")
        title_label.setObjectName("section-title")
        title_label.setStyleSheet("""
            QLabel#section-title {
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                font-weight: 600;
                color: var(--maritime-ocean-deep);
                margin-bottom: 8px;
            }
        """)
        overview_layout.addWidget(title_label)
        
        # Stepper de progression
        self.progress_stepper = ProgressStepper([
            "Initialisation",
            "Calibration", 
            "Acquisition",
            "Analyse"
        ], current_step=2)
        overview_layout.addWidget(self.progress_stepper)
        
        parent_layout.addWidget(overview_card)
        
    def _setup_kpi_grid_section(self, parent_layout):
        """Configuration grille KPI maritime avec design system"""
        # Titre section avec sous-titre
        section_header = QWidget()
        header_layout = QVBoxLayout(section_header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(FIBONACCI_SPACES[1])
        
        title_label = QLabel("Indicateurs de Performance Maritime")
        title_label.setObjectName("kpi-section-title")
        title_label.setStyleSheet("""
            QLabel#kpi-section-title {
                font-family: 'Segoe UI', sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: var(--maritime-ocean-deep);
            }
        """)
        
        subtitle_label = QLabel("Surveillance temps réel des systèmes d'acquisition océanique")
        subtitle_label.setObjectName("kpi-section-subtitle")
        subtitle_label.setStyleSheet("""
            QLabel#kpi-section-subtitle {
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 400;
                color: var(--maritime-storm-gray);
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        parent_layout.addWidget(section_header)
        
        # Grille KPI maritime optimisée
        kpi_definitions = [
            {"name": "Capteurs Océaniques", "value": "14", "unit": "/16 actifs", "status": "success", "icon": "sensor"},
            {"name": "Fréquence Échantillonnage", "value": "1000", "unit": "Hz", "status": "success", "icon": "frequency"},
            {"name": "Débit Acquisition", "value": "2.8", "unit": "MB/s", "status": "success", "icon": "data"},
            {"name": "Latence Réseau", "value": "8", "unit": "ms", "status": "success", "icon": "network"},
            {"name": "Charge Processeur", "value": "28", "unit": "%", "status": "success", "icon": "cpu"},
            {"name": "Mémoire Disponible", "value": "7.2", "unit": "GB", "status": "success", "icon": "memory"}
        ]
        
        # Création grille avec fonction utilitaire
        kpi_grid_widget = create_kpi_grid(kpi_definitions)
        parent_layout.addWidget(kpi_grid_widget)
        
        # Stockage des indicateurs pour mise à jour
        for i, kpi_def in enumerate(kpi_definitions):
            kpi_indicator = kpi_grid_widget.findChild(KPIIndicator, f"kpi-{i}")
            if kpi_indicator:
                self.kpi_indicators[kpi_def["name"]] = kpi_indicator
        
        logger.debug(f"Grille KPI maritime créée avec {len(kpi_definitions)} indicateurs")
        
    def _setup_monitoring_section(self, parent_layout):
        """Section monitoring temps réel avec métriques système"""
        monitoring_card = MaritimeCard(elevation=1)
        monitoring_card.setObjectName("monitoring-card")
        
        monitoring_layout = QVBoxLayout(monitoring_card)
        monitoring_layout.setContentsMargins(
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2],
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2]
        )
        monitoring_layout.setSpacing(FIBONACCI_SPACES[2])
        
        # Titre section
        title_label = QLabel("Monitoring Système Temps Réel")
        title_label.setObjectName("monitoring-title")
        title_label.setStyleSheet("""
            QLabel#monitoring-title {
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                font-weight: 600;
                color: var(--maritime-ocean-deep);
                margin-bottom: 8px;
            }
        """)
        monitoring_layout.addWidget(title_label)
        
        # Widget de performance maritime
        self.performance_widget = PerformanceWidget()
        self.performance_widget.setObjectName("maritime-performance-widget")
        self.performance_widget.setMinimumHeight(FIBONACCI_SPACES[5] * 3)  # 267px
        monitoring_layout.addWidget(self.performance_widget)
        
        parent_layout.addWidget(monitoring_card)
        
    def _setup_charts_section(self, parent_layout):
        """Section graphiques océaniques temps réel"""
        charts_card = MaritimeCard(elevation=1)
        charts_card.setObjectName("charts-card")
        
        charts_layout = QVBoxLayout(charts_card)
        charts_layout.setContentsMargins(
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2],
            FIBONACCI_SPACES[3], FIBONACCI_SPACES[2]
        )
        charts_layout.setSpacing(FIBONACCI_SPACES[2])
        
        # Header section avec contrôles
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(FIBONACCI_SPACES[2])
        
        # Titre
        title_label = QLabel("Visualisation Données Océaniques")
        title_label.setObjectName("charts-title")
        title_label.setStyleSheet("""
            QLabel#charts-title {
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                font-weight: 600;
                color: var(--maritime-ocean-deep);
            }
        """)
        
        # Barre d'actions
        action_bar = create_action_bar([
            {"text": "Temps Réel", "action": "realtime", "primary": True},
            {"text": "Historique", "action": "history", "primary": False},
            {"text": "Export", "action": "export", "primary": False}
        ])
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(action_bar)
        
        charts_layout.addWidget(header_widget)
        
        # Zone graphiques (placeholder maritime)
        charts_placeholder = QFrame()
        charts_placeholder.setObjectName("maritime-charts-placeholder")
        charts_placeholder.setMinimumHeight(FIBONACCI_SPACES[5] * 4)  # 356px
        charts_placeholder.setStyleSheet("""
            QFrame#maritime-charts-placeholder {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 var(--maritime-foam-white),
                    stop:1 #F0F9FF);
                border: 2px dashed var(--maritime-tidal-cyan);
                border-radius: 13px;
            }
        """)
        
        # Contenu placeholder
        placeholder_layout = QVBoxLayout(charts_placeholder)
        placeholder_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        placeholder_icon = QLabel("🌊")
        placeholder_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_icon.setStyleSheet("font-size: 48px; margin-bottom: 16px;")
        
        placeholder_title = QLabel("Graphiques Océaniques")
        placeholder_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_title.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: var(--maritime-harbor-blue);
            margin-bottom: 8px;
        """)
        
        placeholder_desc = QLabel("Visualisation temps réel des données d'acquisition\nIntégration en cours de développement")
        placeholder_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_desc.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
            color: var(--maritime-storm-gray);
            line-height: 1.4;
        """)
        
        placeholder_layout.addWidget(placeholder_icon)
        placeholder_layout.addWidget(placeholder_title)
        placeholder_layout.addWidget(placeholder_desc)
        
        charts_layout.addWidget(charts_placeholder)
        parent_layout.addWidget(charts_card)
        
        logger.debug("Section graphiques océaniques configurée")
        
    def _setup_animations(self):
        """Configuration animations fluides design system maritime"""
        logger.debug("Configuration animations maritimes")
        
        # Animations d'entrée pour les cartes (effet vague)
        for i, (name, indicator) in enumerate(self.kpi_indicators.items()):
            # Animation de fade-in avec décalage temporel
            fade_animation = QPropertyAnimation(indicator, b"windowOpacity")
            fade_animation.setDuration(600 + i * 150)  # Effet cascade
            fade_animation.setEasingCurve(QEasingCurve.Type.OutQuart)
            fade_animation.setStartValue(0.0)
            fade_animation.setEndValue(1.0)
            
            # Animation de slide-up
            slide_animation = QPropertyAnimation(indicator, b"geometry")
            slide_animation.setDuration(800 + i * 100)
            slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            # Position initiale (décalée vers le bas)
            start_rect = indicator.geometry()
            start_rect.moveTop(start_rect.top() + 50)
            slide_animation.setStartValue(start_rect)
            slide_animation.setEndValue(indicator.geometry())
            
            self.animation_group.extend([fade_animation, slide_animation])
            
        # Animation des beacons de statut (pulsation)
        for beacon in self.status_beacons.values():
            if hasattr(beacon, 'start_pulse_animation'):
                beacon.start_pulse_animation()
                
        logger.debug(f"Animations configurées pour {len(self.animation_group)} éléments")
            
    def _setup_data_refresh(self):
        """Configuration rafraîchissement temps réel des métriques"""
        # Timer principal pour KPI
        self.kpi_refresh_timer = QTimer()
        self.kpi_refresh_timer.timeout.connect(self._refresh_kpi_data)
        self.kpi_refresh_timer.start(3000)  # 3 secondes
        
        # Timer pour métriques système
        self.system_refresh_timer = QTimer()
        self.system_refresh_timer.timeout.connect(self._refresh_system_metrics)
        self.system_refresh_timer.start(1000)  # 1 seconde
        
        # Timer pour beacons de statut
        self.status_refresh_timer = QTimer()
        self.status_refresh_timer.timeout.connect(self._refresh_status_beacons)
        self.status_refresh_timer.start(2000)  # 2 secondes
        
        # Démarrage du monitoring de performance
        if self.performance_widget:
            self.performance_widget.start_monitoring()
        
        logger.debug("Timers de rafraîchissement configurés")
            
    def _refresh_kpi_data(self):
        """Rafraîchissement des données KPI maritimes (simulation temps réel)"""
        import random
        
        # Simulation de données océaniques variables
        kpi_updates = {
            "Capteurs Océaniques": {
                "value": str(random.randint(12, 16)),
                "unit": "/16 actifs",
                "status": "success" if random.randint(12, 16) >= 14 else "warning"
            },
            "Fréquence Échantillonnage": {
                "value": str(random.randint(950, 1000)),
                "unit": "Hz",
                "status": "success" if random.randint(950, 1000) >= 980 else "warning"
            },
            "Débit Acquisition": {
                "value": f"{random.uniform(2.5, 3.2):.1f}",
                "unit": "MB/s",
                "status": "success"
            },
            "Latence Réseau": {
                "value": str(random.randint(5, 15)),
                "unit": "ms",
                "status": "success" if random.randint(5, 15) <= 10 else "warning"
            },
            "Charge Processeur": {
                "value": str(random.randint(20, 45)),
                "unit": "%",
                "status": "success" if random.randint(20, 45) <= 35 else "warning"
            },
            "Mémoire Disponible": {
                "value": f"{random.uniform(6.8, 7.8):.1f}",
                "unit": "GB",
                "status": "success"
            }
        }
        
        # Mise à jour des indicateurs KPI
        for kpi_name, data in kpi_updates.items():
            if kpi_name in self.kpi_indicators:
                indicator = self.kpi_indicators[kpi_name]
                if hasattr(indicator, 'update_value'):
                    indicator.update_value(data["value"], data["status"])
                    
                # Émission du signal de mise à jour
                self.kpi_updated.emit(kpi_name, data["value"], data["status"])
                
        logger.debug(f"KPI maritimes mis à jour: {len(kpi_updates)} indicateurs")
        
    def _refresh_system_metrics(self):
        """Rafraîchissement des métriques système temps réel"""
        import random
        
        # Simulation métriques système
        self.system_metrics.update({
            'cpu_usage': random.randint(20, 60),
            'memory_usage': random.randint(40, 80),
            'disk_usage': random.randint(50, 90),
            'network_rate': random.uniform(1.0, 5.0),
            'active_sensors': random.randint(12, 16),
            'data_buffer': random.randint(70, 95)
        })
        
        # Mise à jour du widget de performance
        if self.performance_widget and hasattr(self.performance_widget, 'update_metrics'):
            metrics = {
                "CPU": PerformanceMetric("CPU", self.system_metrics['cpu_usage'], "%"),
                "RAM": PerformanceMetric("RAM", self.system_metrics['memory_usage'], "%"),
                "Disque": PerformanceMetric("Disque", self.system_metrics['disk_usage'], "%"),
                "Réseau": PerformanceMetric("Réseau", self.system_metrics['network_rate'], "MB/s")
            }
            self.performance_widget.update_metrics(metrics)
            
    def _refresh_status_beacons(self):
        """Rafraîchissement des beacons de statut système"""
        import random
        
        # Simulation des états système
        system_states = {
            'system': random.choice(['operational', 'operational', 'warning']),  # 66% operational
            'acquisition': random.choice(['active', 'standby', 'active']),  # 66% active
            'network': random.choice(['connected', 'connected', 'slow'])  # 66% connected
        }
        
        # Mise à jour des beacons
        for beacon_name, status in system_states.items():
            if beacon_name in self.status_beacons:
                beacon = self.status_beacons[beacon_name]
                if hasattr(beacon, 'update_status'):
                    beacon.update_status(status)
                
    def _on_theme_changed(self, is_dark: bool):
        """Gestionnaire de changement de thème maritime"""
        self.current_theme = "dark" if is_dark else "light"
        self._apply_maritime_design_system()
        self.theme_changed.emit(is_dark)
        logger.info(f"Thème maritime changé vers: {self.current_theme}")
        
    def _apply_maritime_design_system(self):
        """Application du design system maritime complet"""
        logger.debug(f"Application design system maritime - thème: {self.current_theme}")
        
        # Chargement du fichier QSS maritime
        try:
            import os
            # Chemin relatif depuis ce fichier vers le fichier CSS
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qss_path = os.path.join(current_dir, '..', 'styles', 'maritime_design_system.qss')
            qss_path = os.path.normpath(qss_path)
            
            with open(qss_path, 'r', encoding='utf-8') as f:
                maritime_qss = f.read()
                
            # Application du style global
            self.setStyleSheet(maritime_qss)
            
            # Configuration spécifique au thème
            if self.current_theme == "dark":
                self._apply_dark_theme_overrides()
            else:
                self._apply_light_theme_overrides()
                
            logger.info(f"Design system maritime appliqué avec succès depuis: {qss_path}")
            
        except FileNotFoundError as e:
            logger.warning(f"Fichier maritime_design_system.qss non trouvé: {e}, utilisation du style par défaut")
            self._apply_fallback_maritime_style()
        except Exception as e:
            logger.error(f"Erreur lors de l'application du design system: {e}")
            self._apply_fallback_maritime_style()
            
        # Forcer la mise à jour du style
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        
    def _apply_light_theme_overrides(self):
        """Surcharges spécifiques au thème clair"""
        light_overrides = """
            QWidget {
                background-color: var(--maritime-foam-white);
                color: var(--maritime-ocean-deep);
            }
            
            MaritimeCard {
                background-color: #FFFFFF;
                border: 1px solid #E3F2FD;
            }
        """
        current_style = self.styleSheet()
        self.setStyleSheet(current_style + light_overrides)
        
    def _apply_dark_theme_overrides(self):
        """Surcharges spécifiques au thème sombre"""
        dark_overrides = """
            QWidget {
                background-color: var(--maritime-ocean-deep);
                color: var(--maritime-foam-white);
            }
            
            MaritimeCard {
                background-color: #1A2332;
                border: 1px solid #263238;
            }
        """
        current_style = self.styleSheet()
        self.setStyleSheet(current_style + dark_overrides)
        
    def _apply_fallback_maritime_style(self):
        """Style maritime de secours si le fichier QSS n'est pas disponible"""
        fallback_style = """
            /* Style maritime de secours - Palette océanique */
            QMainWindow {
                background-color: #0A1929; /* ocean-deep */
                color: #37474F; /* storm-gray */
                font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }
            
            QWidget {
                background-color: #FAFBFC; /* foam-white */
                color: #0A1929; /* ocean-deep */
                font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }
            
            .MaritimeCard {
                background-color: #FAFBFC; /* foam-white */
                border: 1px solid #F5F7FA; /* frost-light */
                border-radius: 12px;
                padding: 21px;
                margin: 13px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .PrimaryButton {
                background-color: #1565C0; /* harbor-blue */
                color: #FAFBFC; /* foam-white */
                border: none;
                border-radius: 8px;
                padding: 13px 21px;
                font-size: 14px;
                font-weight: 500;
                min-height: 44px;
            }
            
            .PrimaryButton:hover {
                background-color: #1976D2; /* steel-blue */
            }
            
            .KPIIndicator {
                background-color: #FAFBFC; /* foam-white */
                border-radius: 8px;
                padding: 21px;
                min-width: 323px;
                min-height: 200px;
            }
        """
        self.setStyleSheet(fallback_style)
        logger.info("Style maritime de secours appliqué avec palette océanique")
        
    def showEvent(self, event):
        """Gestionnaire d'affichage avec animations d'entrée"""
        super().showEvent(event)
        
        # Démarrer les animations d'entrée
        for animation in self.animation_group:
            animation.start()
            
    def closeEvent(self, event):
        """Gestionnaire de fermeture avec nettoyage complet"""
        logger.info("Fermeture Dashboard Maritime")
        
        # Arrêter le monitoring de performance
        if self.performance_widget and hasattr(self.performance_widget, 'stop_monitoring'):
            self.performance_widget.stop_monitoring()
            
        # Arrêter tous les timers
        timers_to_stop = ['kpi_refresh_timer', 'system_refresh_timer', 'status_refresh_timer']
        for timer_name in timers_to_stop:
            if hasattr(self, timer_name):
                timer = getattr(self, timer_name)
                if timer.isActive():
                    timer.stop()
                    logger.debug(f"Timer {timer_name} arrêté")
                    
        # Arrêter les animations
        for animation in self.animation_group:
            if animation.state() == QPropertyAnimation.State.Running:
                animation.stop()
                
        # Nettoyage des beacons
        for beacon in self.status_beacons.values():
            if hasattr(beacon, 'stop_pulse_animation'):
                beacon.stop_pulse_animation()
                
        logger.info("Nettoyage Dashboard Maritime terminé")
        event.accept()
        
    def get_sidebar_width(self) -> int:
        """Retourne la largeur de la sidebar"""
        return self.sidebar.width()
        
    def get_main_area_width(self) -> int:
        """Retourne la largeur de la zone principale"""
        return self.main_area.width()
        
    def update_kpi_indicator(self, name: str, value: str, status: str = "success"):
        """Met à jour un indicateur KPI maritime spécifique"""
        if name in self.kpi_indicators:
            indicator = self.kpi_indicators[name]
            if hasattr(indicator, 'update_value'):
                indicator.update_value(value, status)
                self.kpi_updated.emit(name, value, status)
                logger.debug(f"KPI '{name}' mis à jour: {value} ({status})")
        else:
            logger.warning(f"Indicateur KPI '{name}' non trouvé")
            
    def add_custom_kpi(self, name: str, value: str, unit: str, status: str = "success"):
        """Ajoute un nouvel indicateur KPI maritime personnalisé"""
        try:
            # Création du nouvel indicateur KPI
            new_indicator = KPIIndicator(
                title=name,
                value=value,
                unit=unit,
                status=status,
                parent=self
            )
            
            # Ajout à la grille KPI existante
            if hasattr(self, 'kpi_grid_layout'):
                # Calcul de la position dans la grille
                current_count = len(self.kpi_indicators)
                row = current_count // 3
                col = current_count % 3
                
                self.kpi_grid_layout.addWidget(new_indicator, row, col)
                self.kpi_indicators[name] = new_indicator
                
                # Configuration de l'animation d'entrée
                fade_animation = QPropertyAnimation(new_indicator, b"windowOpacity")
                fade_animation.setDuration(600)
                fade_animation.setEasingCurve(QEasingCurve.Type.OutQuart)
                fade_animation.setStartValue(0.0)
                fade_animation.setEndValue(1.0)
                fade_animation.start()
                
                logger.info(f"Indicateur KPI maritime '{name}' ajouté avec succès")
                self.kpi_updated.emit(name, value, status)
                
            else:
                logger.error("Layout de grille KPI non trouvé")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du KPI '{name}': {e}")
            
    def remove_kpi_indicator(self, name: str):
        """Supprime un indicateur KPI maritime"""
        if name in self.kpi_indicators:
            indicator = self.kpi_indicators[name]
            
            # Animation de sortie
            fade_out = QPropertyAnimation(indicator, b"windowOpacity")
            fade_out.setDuration(400)
            fade_out.setEasingCurve(QEasingCurve.Type.InQuart)
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.0)
            fade_out.finished.connect(lambda: self._finalize_kpi_removal(name, indicator))
            fade_out.start()
            
        else:
            logger.warning(f"Indicateur KPI '{name}' non trouvé pour suppression")
            
    def _finalize_kpi_removal(self, name: str, indicator):
        """Finalise la suppression d'un indicateur KPI"""
        try:
            # Suppression du layout
            if hasattr(self, 'kpi_grid_layout'):
                self.kpi_grid_layout.removeWidget(indicator)
                
            # Suppression de la référence
            del self.kpi_indicators[name]
            
            # Destruction du widget
            indicator.deleteLater()
            
            logger.info(f"Indicateur KPI maritime '{name}' supprimé")
            
        except Exception as e:
            logger.error(f"Erreur lors de la finalisation de suppression KPI '{name}': {e}")
            
    def get_kpi_status_summary(self) -> dict:
        """Retourne un résumé des statuts des indicateurs KPI"""
        summary = {
            'total': len(self.kpi_indicators),
            'success': 0,
            'warning': 0,
            'error': 0,
            'info': 0
        }
        
        for indicator in self.kpi_indicators.values():
            if hasattr(indicator, 'current_status'):
                status = indicator.current_status
                if status in summary:
                    summary[status] += 1
                    
        return summary
        
    def export_kpi_data(self) -> dict:
        """Exporte les données KPI actuelles pour sauvegarde/analyse"""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'theme': self.current_theme,
            'system_metrics': self.system_metrics.copy(),
            'kpi_indicators': {},
            'status_summary': self.get_kpi_status_summary()
        }
        
        # Export des données KPI
        for name, indicator in self.kpi_indicators.items():
            if hasattr(indicator, 'get_export_data'):
                export_data['kpi_indicators'][name] = indicator.get_export_data()
            else:
                export_data['kpi_indicators'][name] = {
                    'name': name,
                    'timestamp': datetime.now().isoformat()
                }
                
        logger.info(f"Données KPI exportées: {len(export_data['kpi_indicators'])} indicateurs")
        return export_data


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Test du Dashboard Maritime
    dashboard = DashboardViewMaritime()
    dashboard.setWindowTitle("CHNeoWave Dashboard Maritime 2025 - Design System Océanique")
    dashboard.resize(1600, 1000)  # Ratio golden pour écrans modernes
    dashboard.show()
    
    logger.info("Application Dashboard Maritime démarrée")
    sys.exit(app.exec())