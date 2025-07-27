# -*- coding: utf-8 -*-
"""
Unified Calibration View - Maritime Design System 2025
Vue de calibration unifiée avec design maritime industriel et Golden Ratio
Architecture: Sidebar (20%) + Zone principale (80%) selon spécifications maritimes

Auteur: Architecte Logiciel en Chef - CHNeoWave
Date: 2025-01-27
Version: 2.0.0 Maritime
"""

import logging
import json
from datetime import datetime
from pathlib import Path

# Initialisation du logger
logger = logging.getLogger(__name__)

# Utiliser directement PySide6 pour être cohérent avec le ViewManager
from PySide6.QtCore import Qt, Signal as pyqtSignal, Property as pyqtProperty, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QProgressBar, QScrollArea, QSpacerItem, QSizePolicy, QStackedWidget,
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QTextEdit, QSplitter, QApplication, QMainWindow
)
from PySide6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPixmap

# Import des widgets maritimes
try:
    from ..components.maritime_widgets import (
        MaritimeCard, KPIIndicator,
        apply_maritime_theme
    )
except ImportError:
    logging.warning("Widgets maritimes non disponibles, utilisation des widgets de base")
    MaritimeCard = QFrame
    KPIIndicator = QLabel
    apply_maritime_theme = lambda x: None

# Définition des widgets simplifiés pour éviter les problèmes d'import

# MaritimeButton simplifié
class MaritimeButton(QPushButton):
    """Bouton maritime avec style et animations"""
    
    def __init__(self, text="", icon=None, button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        
        if icon:
            self.setIcon(icon)
        
        self.apply_style()
    
    def apply_style(self):
        # Styles de base
        base_style = """
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
        """
        
        # Styles spécifiques selon le type
        if self.button_type == "primary":
            color_style = """
                background-color: #1565C0;
                color: white;
                border: none;
            """
        elif self.button_type == "secondary":
            color_style = """
                background-color: #E3F2FD;
                color: #1565C0;
                border: 1px solid #1565C0;
            """
        else:  # outline ou autre
            color_style = """
                background-color: transparent;
                color: #1565C0;
                border: 1px solid #E0E0E0;
            """
        
        self.setStyleSheet(base_style + color_style)

# StatusBeacon simplifié
class StatusBeacon(QWidget):
    """Indicateur d'état maritime simplifié"""
    
    def __init__(self, status="inactive", size=12, animated=True, parent=None):
        super().__init__(parent)
        self.status = status
        self.beacon_size = size
        self.animated = animated
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.indicator = QFrame(self)
        self.indicator.setFixedSize(self.beacon_size, self.beacon_size)
        
        # Appliquer le style en fonction du statut
        color = "#4CAF50"  # Vert par défaut (actif)
        if self.status == "warning":
            color = "#FF9800"  # Orange
        elif self.status == "error":
            color = "#F44336"  # Rouge
        elif self.status == "inactive":
            color = "#9E9E9E"  # Gris
            
        self.indicator.setStyleSheet(f"background-color: {color}; border-radius: {self.beacon_size/2}px;")
        layout.addWidget(self.indicator)
        
    def update_status(self, status):
        self.status = status
        self.setup_ui()
class ProgressStepper(QWidget):
    """Stepper de progression maritime simplifié"""
    
    def __init__(self, steps, current_step=0, parent=None):
        super().__init__(parent)
        self.steps = steps
        self.current_step = current_step
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        
        for i, step_name in enumerate(self.steps):
            step_label = QLabel(f"{i+1}. {step_name}")
            if i < self.current_step:
                step_label.setStyleSheet("color: #1976D2; font-weight: bold;")
            elif i == self.current_step:
                step_label.setStyleSheet("color: #1976D2; font-weight: bold; text-decoration: underline;")
            else:
                step_label.setStyleSheet("color: #546E7A;")
            layout.addWidget(step_label)
            
            if i < len(self.steps) - 1:
                separator = QLabel(">")
                separator.setStyleSheet("color: #546E7A;")
                layout.addWidget(separator)

# Design System Maritime - Constantes 2025
GOLDEN_RATIO = 1.618
FIBONACCI_SPACES = [8, 13, 21, 34, 55, 89, 144]  # Suite Fibonacci pour espacements

# Palette Maritime Professionnelle
MARITIME_COLORS = {
    'ocean_deep': '#0A1929',      # Fond application
    'harbor_blue': '#1565C0',     # Boutons primaires
    'steel_blue': '#1976D2',      # Boutons secondaires
    'tidal_cyan': '#00BCD4',      # Graphiques, données temps réel
    'foam_white': '#FAFBFC',      # Cards, surfaces
    'frost_light': '#F5F7FA',     # Backgrounds sections
    'storm_gray': '#37474F',      # Texte principal
    'slate_gray': '#546E7A',      # Texte secondaire
    'coral_alert': '#FF5722',     # Alertes, erreurs
    'emerald_success': '#4CAF50', # Succès, validation
    'amber_warning': '#FF9800',   # Avertissements
    'azure_info': '#2196F3'       # Informations
}

# Configuration logger
logger = logging.getLogger(__name__)

class MaritimeCalibrationStep(QFrame):
    """
    Étape de calibration maritime avec design industriel 2025
    Intègre StatusBeacon, animations fluides et feedback visuel avancé
    Architecture: Numéro + Contenu + Statut selon Golden Ratio
    """
    
    step_clicked = pyqtSignal(int)
    step_status_changed = pyqtSignal(int, str)  # step_number, status
    
    def __init__(self, step_number: int, title: str, description: str = "", parent=None):
        # Initialisation des attributs avant l'appel au constructeur parent
        self.title = title
        self.content = ""
        self.step_number = step_number
        self.description = description
        # Appel du constructeur parent avec seulement le parent
        super().__init__(parent)
        
        # États de l'étape
        self.status = 'pending'  # pending, active, completed, error, locked
        self.is_accessible = True
        self.progress_value = 0
        
        # Configuration dimensions Golden Ratio
        self.setFixedHeight(int(FIBONACCI_SPACES[4] * GOLDEN_RATIO))  # ~89px
        self.setMinimumWidth(FIBONACCI_SPACES[6])  # 144px
        
        # Appliquer le style maritime
        self.setObjectName("MaritimeCalibrationStep")
        self.setStyleSheet("""
            #MaritimeCalibrationStep {
                background-color: #F5F7FA;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        self.setup_ui()
        
        logger.debug(f"Étape maritime {step_number} initialisée: {title}")
    
    def setup_ui(self):
        """Configuration interface maritime avec StatusBeacon"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(FIBONACCI_SPACES[2], FIBONACCI_SPACES[1], 
                                FIBONACCI_SPACES[2], FIBONACCI_SPACES[1])  # 21, 13
        layout.setSpacing(FIBONACCI_SPACES[1])  # 13
        
        # Zone numéro avec StatusBeacon
        number_container = QVBoxLayout()
        number_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Numéro de l'étape
        self.number_label = QLabel(str(self.step_number))
        self.number_label.setFixedSize(FIBONACCI_SPACES[3], FIBONACCI_SPACES[3])  # 34x34
        self.number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number_label.setStyleSheet("background-color: #1565C0; color: white; border-radius: 17px;")
        
        # StatusBeacon pour l'état
        self.status_beacon = StatusBeacon("pending", size=FIBONACCI_SPACES[1])  # 13px
        
        number_container.addWidget(self.number_label)
        number_container.addWidget(self.status_beacon)
        
        # Zone contenu textuel
        content_layout = QVBoxLayout()
        content_layout.setSpacing(FIBONACCI_SPACES[0])  # 8
        
        # Titre avec police maritime
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("maritimeStepTitle")
        
        # Description avec wrapping
        self.description_label = QLabel(self.description)
        self.description_label.setObjectName("maritimeStepDescription")
        self.description_label.setWordWrap(True)
        
        # Barre de progression micro (optionnelle)
        self.micro_progress = QProgressBar()
        self.micro_progress.setFixedHeight(FIBONACCI_SPACES[0] // 2)  # 4px
        self.micro_progress.setVisible(False)
        self.micro_progress.setObjectName("maritimeStepProgress")
        
        content_layout.addWidget(self.title_label)
        content_layout.addWidget(self.description_label)
        content_layout.addWidget(self.micro_progress)
        content_layout.addStretch()
        
        # Zone statut (droite)
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Indicateur temps estimé
        self.time_label = QLabel("~2min")
        self.time_label.setObjectName("maritimeStepTime")
        
        status_layout.addWidget(self.time_label)
        status_layout.addStretch()
        
        # Assembly final
        layout.addLayout(number_container)
        layout.addLayout(content_layout, 1)  # Expansion
        layout.addLayout(status_layout)
    
    def setup_animations(self):
        """Configuration animations fluides maritimes"""
        # Animation fade pour transitions d'état
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Animation scale pour feedback hover
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(200)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutBack)
    
    def apply_maritime_styling(self):
        """Application du style maritime selon l'état"""
        base_style = f"""
        MaritimeCalibrationStep {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MARITIME_COLORS['foam_white']},
                stop:1 {MARITIME_COLORS['frost_light']});
            border: 1px solid {MARITIME_COLORS['slate_gray']};
            border-radius: {FIBONACCI_SPACES[1]}px;
            margin: {FIBONACCI_SPACES[0]}px;
        }}
        
        MaritimeCalibrationStep:hover {{
            border: 2px solid {MARITIME_COLORS['harbor_blue']};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MARITIME_COLORS['foam_white']},
                stop:1 #E8F4FD);
        }}
        
        QLabel#maritimeStepTitle {{
            color: {MARITIME_COLORS['storm_gray']};
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 13px;
            font-weight: 600;
        }}
        
        QLabel#maritimeStepDescription {{
            color: {MARITIME_COLORS['slate_gray']};
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 11px;
            line-height: 1.4;
        }}
        
        QLabel#maritimeStepTime {{
            color: {MARITIME_COLORS['tidal_cyan']};
            font-family: 'Roboto Mono', monospace;
            font-size: 10px;
            font-weight: 500;
        }}
        
        QProgressBar#maritimeStepProgress {{
            border: none;
            background-color: {MARITIME_COLORS['frost_light']};
            border-radius: 2px;
        }}
        
        QProgressBar#maritimeStepProgress::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {MARITIME_COLORS['tidal_cyan']},
                stop:1 {MARITIME_COLORS['harbor_blue']});
            border-radius: 2px;
        }}
        """
        
        self.setStyleSheet(base_style)
        self.update_status_styling()
    
    def update_status_styling(self):
        """Mise à jour du style selon le statut"""
        # Styles simplifiés pour les différents états
        if self.status == 'active':
            self.number_label.setStyleSheet("background-color: #1565C0; color: white; font-weight: bold;")
        elif self.status == 'completed':
            self.number_label.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        elif self.status == 'error':
            self.number_label.setStyleSheet("background-color: #F44336; color: white; font-weight: bold;")
        elif self.status == 'locked':
            self.number_label.setStyleSheet("background-color: #EEEEEE; color: #9E9E9E;")
        else:  # pending
            self.number_label.setStyleSheet("background-color: #E0E0E0; color: #546E7A;")
        
        # Mise à jour du texte pour les états spéciaux
        if self.status == 'completed':
            self.number_label.setText("✓")
        elif self.status == 'error':
            self.number_label.setText("✗")
        elif self.status == 'locked':
            self.number_label.setText("🔒")
        else:
            self.number_label.setText(str(self.step_number))
        
        # Mise à jour du StatusBeacon
        if hasattr(self, 'status_beacon'):
            self.status_beacon.update_status(self.status)
    
    def set_status(self, status):
        """Définit le statut de l'étape"""
        if status != self.status:
            old_status = self.status
            self.status = status
            self.update_status_styling()
            self.step_status_changed.emit(self.step_number, status)
            logger.debug(f"Étape {self.step_number}: {old_status} → {status}")
    
    def set_progress(self, value):
        """Définit la progression (0-100)"""
        self.progress_value = max(0, min(100, value))
        self.micro_progress.setValue(self.progress_value)
        
        if self.progress_value > 0:
            self.micro_progress.setVisible(True)
        
        if self.progress_value >= 100:
            QTimer.singleShot(500, lambda: self.set_status('completed'))
    
    def set_accessible(self, accessible: bool):
        """Définit l'accessibilité de l'étape"""
        self.is_accessible = accessible
        if not accessible and self.status != 'completed':
            self.set_status('locked')
        elif accessible and self.status == 'locked':
            self.set_status('pending')
    
    def set_active(self, active: bool):
        """Définit l'état actif"""
        if active:
            self.set_status('active')
        elif self.status == 'active':
            self.set_status('pending')
    
    def set_completed(self, completed: bool):
        """Définit l'état complété"""
        if completed:
            self.set_status('completed')
        elif self.status == 'completed':
            self.set_status('pending')
    
    def set_estimated_time(self, minutes):
        """Définit le temps estimé"""
        if minutes < 1:
            self.time_label.setText("<1min")
        elif minutes < 60:
            self.time_label.setText(f"~{minutes}min")
        else:
            hours = minutes // 60
            mins = minutes % 60
            self.time_label.setText(f"~{hours}h{mins:02d}")
    
    def mousePressEvent(self, event):
        """Gestion du clic avec feedback visuel"""
        if self.is_accessible and event.button() == Qt.MouseButton.LeftButton:
            if self.status not in ['locked']:
                # Animation de feedback
                if self.scale_animation:
                    current_rect = self.geometry()
                    scaled_rect = QRect(
                        current_rect.x() + 2, current_rect.y() + 2,
                        current_rect.width() - 4, current_rect.height() - 4
                    )
                    
                    self.scale_animation.setStartValue(current_rect)
                    self.scale_animation.setEndValue(scaled_rect)
                    self.scale_animation.finished.connect(
                        lambda: self._restore_scale(current_rect)
                    )
                    self.scale_animation.start()
                
                self.step_clicked.emit(self.step_number)
                logger.debug(f"Clic sur étape {self.step_number}: {self.title}")
        
        super().mousePressEvent(event)
    
    def _restore_scale(self, original_rect):
        """Restaure la taille originale après animation"""
        if self.scale_animation:
            self.scale_animation.setStartValue(self.geometry())
            self.scale_animation.setEndValue(original_rect)
            self.scale_animation.finished.disconnect()
            self.scale_animation.start()
    
    def enterEvent(self, event):
        """Animation d'entrée de souris"""
        if self.is_accessible and self.status != 'locked':
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Animation de sortie de souris"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


class CalibrationView(QWidget):
    """
    Vue principale de calibration avec design maritime
    Intègre la barre latérale et la zone principale de calibration
    """
    
    # Signaux de calibration
    calibration_started = pyqtSignal()
    calibration_completed = pyqtSignal()
    calibration_step_changed = pyqtSignal(int)  # numéro d'étape
    calibration_error = pyqtSignal(str)  # message d'erreur
    
    def __init__(self, parent=None):
        # Vérifier si le parent est un QStackedWidget
        if parent is not None and not isinstance(parent, QWidget):
            logger.warning(f"Parent de type {type(parent).__name__} non supporté, utilisation de None")
            parent = None
        
        super().__init__(parent)
        
        # Initialisation des attributs
        self.current_step = 1
        
        # Configuration de l'interface
        self.setup_ui()
        
        # Configuration des connexions avec un délai
        QTimer.singleShot(100, self.setup_connections)
        
        logger.info("Vue de calibration initialisée")
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Barre latérale de calibration
        self.sidebar = MaritimeCalibrationSidebar(self)
        layout.addWidget(self.sidebar)
        
        # Zone principale de calibration
        self.main_area = QStackedWidget(self)
        layout.addWidget(self.main_area)
        
        # Configuration du ratio Golden
        layout.setStretch(0, 1)  # Sidebar
        layout.setStretch(1, int(GOLDEN_RATIO * 100))  # Zone principale
    
    def setup_connections(self):
        """Configuration des connexions entre composants"""
        self.sidebar.step_selected.connect(self.change_step)
        self.sidebar.calibration_progress_changed.connect(self.update_progress)
    
    def change_step(self, step_number):
        """Change l'étape de calibration active"""
        self.current_step = step_number
        self.main_area.setCurrentIndex(step_number - 1)
        self.calibration_step_changed.emit(step_number)
        logger.debug(f"Changement vers l'étape {step_number}")
    
    def update_progress(self, progress):
        """Met à jour la progression globale de la calibration"""
        if progress >= 100:
            self.calibration_completed.emit()
            logger.info("Calibration terminée avec succès")


class MaritimeCalibrationSidebar(QWidget):
    """
    Sidebar maritime pour les étapes de calibration
    Design industriel 2025 avec ProgressStepper et animations fluides
    Architecture: Header + Steps + Progress selon Golden Ratio
    """
    
    step_selected = pyqtSignal(int)
    calibration_progress_changed = pyqtSignal(int)  # Pourcentage global
    
    def __init__(self, parent=None):
        # Appel du constructeur parent
        super().__init__(parent)
        
        # Initialisation des attributs
        self.current_step = 1
        self.steps = {}
        self.total_steps = 5
        self.completed_steps = 0
        
        # Configuration dimensions Golden Ratio
        self.setFixedWidth(300)  # Largeur fixe simplifiée
        
        # Appliquer le style maritime
        self.setObjectName("MaritimeCalibrationSidebar")
        self.setStyleSheet("""
            #MaritimeCalibrationSidebar {
                background-color: #F5F7FA;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        self.setup_ui()
        
        logger.debug("Sidebar maritime de calibration initialisée")
        
    def setup_ui(self):
        """Configuration interface maritime simplifiée"""
        # Création du layout principal
        self.main_layout = QVBoxLayout(self)
        # Configuration des marges et espacement
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        # Titre
        title_label = QLabel("CALIBRATION MARITIME")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.main_layout.addWidget(title_label)
        
        # Sous-titre
        subtitle_label = QLabel("Système CHNeoWave")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 12px; color: #546E7A;")
        self.main_layout.addWidget(subtitle_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E0E0E0;")
        self.main_layout.addWidget(separator)
        
        # Étiquette d'information
        info_label = QLabel("Sidebar de calibration simplifiée")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 12px; color: #1976D2; margin: 20px;")
        self.main_layout.addWidget(info_label)
        
        # Spacer pour pousser le contenu vers le haut
        self.main_layout.addStretch()
    
    def setup_header(self, parent_layout):
        """Configuration de l'en-tête maritime"""
        header_container = QVBoxLayout()
        header_container.setSpacing(FIBONACCI_SPACES[1])  # 13px
        
        # Titre principal
        title_label = QLabel("CALIBRATION MARITIME")
        title_label.setObjectName("maritimeSidebarTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Sous-titre avec icône
        subtitle_layout = QHBoxLayout()
        subtitle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel("⚓")
        icon_label.setObjectName("maritimeSidebarIcon")
        
        subtitle_label = QLabel("Système CHNeoWave")
        subtitle_label.setObjectName("maritimeSidebarSubtitle")
        
        subtitle_layout.addWidget(icon_label)
        subtitle_layout.addWidget(subtitle_label)
        
        header_container.addWidget(title_label)
        header_container.addLayout(subtitle_layout)
        
        parent_layout.addLayout(header_container)
    
    def setup_progress_stepper(self, parent_layout):
        """Configuration du ProgressStepper global"""
        progress_container = QVBoxLayout()
        progress_container.setSpacing(FIBONACCI_SPACES[0])  # 8px
        
        # Label progression
        self.progress_label = QLabel("Progression Globale")
        self.progress_label.setObjectName("maritimeProgressLabel")
        
        # ProgressStepper maritime
        step_names = ["Préparation", "Configuration", "Calibration", "Vérification", "Finalisation"]
        self.progress_stepper = ProgressStepper(steps=step_names)
        self.progress_stepper.setObjectName("maritimeCalibrationStepper")
        
        # Pourcentage et temps estimé
        info_layout = QHBoxLayout()
        
        self.percentage_label = QLabel("0%")
        self.percentage_label.setObjectName("maritimePercentage")
        
        self.time_remaining_label = QLabel("~10min")
        self.time_remaining_label.setObjectName("maritimeTimeRemaining")
        
        info_layout.addWidget(self.percentage_label)
        info_layout.addStretch()
        info_layout.addWidget(self.time_remaining_label)
        
        progress_container.addWidget(self.progress_label)
        progress_container.addWidget(self.progress_stepper)
        progress_container.addLayout(info_layout)
        
        parent_layout.addLayout(progress_container)
    
    def setup_steps_area(self, parent_layout):
        """Configuration de la zone des étapes"""
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("maritimeSeparator")
        parent_layout.addWidget(separator)
        
        # Label étapes
        steps_label = QLabel("Étapes Détaillées")
        steps_label.setObjectName("maritimeStepsLabel")
        parent_layout.addWidget(steps_label)
        
        # Zone de défilement
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setObjectName("maritimeStepsScroll")
        
        # Widget conteneur pour les étapes
        steps_widget = QWidget()
        self.steps_layout = QVBoxLayout(steps_widget)
        self.steps_layout.setSpacing(FIBONACCI_SPACES[1])  # 13px
        self.steps_layout.setContentsMargins(0, 0, 0, 0)
        
        # Spacer pour alignement
        self.steps_layout.addStretch()
        
        scroll_area.setWidget(steps_widget)
        parent_layout.addWidget(scroll_area, 1)  # Expansion
    
    def setup_status_area(self, parent_layout):
        """Configuration de la zone de statut"""
        status_container = QVBoxLayout()
        status_container.setSpacing(FIBONACCI_SPACES[0])  # 8px
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("maritimeSeparator")
        status_container.addWidget(separator)
        
        # Statut système
        status_layout = QHBoxLayout()
        
        status_icon = StatusBeacon("active", size=FIBONACCI_SPACES[1])  # 13px
        status_text = QLabel("Système Prêt")
        status_text.setObjectName("maritimeStatusText")
        
        status_layout.addWidget(status_icon)
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        
        # Bouton d'aide
        help_button = MaritimeButton("?")
        help_button.setFixedSize(FIBONACCI_SPACES[3], FIBONACCI_SPACES[3])  # 34x34
        help_button.setObjectName("maritimeHelpButton")
        help_button.clicked.connect(self.show_help)
        
        status_layout.addWidget(help_button)
        
        status_container.addLayout(status_layout)
        parent_layout.addLayout(status_container)
        
    def setup_steps(self):
        """Configuration des étapes maritimes avec données complètes"""
        steps_data = [
            {"number": 1, "title": "Initialisation Système", "description": "Vérification capteurs et connexions réseau", "time": 2},
            {"number": 2, "title": "Calibration Zéro", "description": "Définition point de référence maritime", "time": 3},
            {"number": 3, "title": "Calibration Échelle", "description": "Ajustement sensibilité et plage", "time": 4},
            {"number": 4, "title": "Tests Validation", "description": "Vérification précision et stabilité", "time": 2},
            {"number": 5, "title": "Sauvegarde Config", "description": "Enregistrement paramètres système", "time": 1}
        ]
        
        for step_data in steps_data:
            step = MaritimeCalibrationStep(
                step_number=step_data["number"],
                title=step_data["title"],
                description=step_data["description"]
            )
            step.set_estimated_time(step_data["time"])
            step.step_clicked.connect(self.on_step_clicked)
            step.step_status_changed.connect(self.on_step_status_changed)
            
            # Configuration initiale
            if step_data["number"] == 1:
                step.set_status('active')
                step.set_accessible(True)
            else:
                step.set_accessible(False)
                
            self.steps[step_data["number"]] = step
            self.steps_layout.insertWidget(self.steps_layout.count() - 1, step)  # Avant le stretch
            
        logger.debug(f"{len(self.steps)} étapes maritimes créées")
    
    def setup_animations(self):
        """Configuration des animations de progression"""
        self.progress_animation = QPropertyAnimation(self.progress_stepper, b"value")
        self.progress_animation.setDuration(800)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def apply_maritime_styling(self):
        """Application du style maritime complet"""
        style = f"""
        MaritimeCalibrationSidebar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MARITIME_COLORS['foam_white']},
                stop:0.5 {MARITIME_COLORS['frost_light']},
                stop:1 {MARITIME_COLORS['foam_white']});
            border-right: 3px solid {MARITIME_COLORS['harbor_blue']};
        }}
        
        QLabel#maritimeSidebarTitle {{
            color: {MARITIME_COLORS['ocean_deep']};
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 1px;
            padding: {FIBONACCI_SPACES[1]}px;
        }}
        
        QLabel#maritimeSidebarIcon {{
            color: {MARITIME_COLORS['harbor_blue']};
            font-size: 18px;
        }}
        
        QLabel#maritimeSidebarSubtitle {{
            color: {MARITIME_COLORS['slate_gray']};
            font-family: 'Roboto', sans-serif;
            font-size: 11px;
            font-weight: 500;
        }}
        
        QLabel#maritimeProgressLabel,
        QLabel#maritimeStepsLabel {{
            color: {MARITIME_COLORS['storm_gray']};
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QLabel#maritimePercentage {{
            color: {MARITIME_COLORS['harbor_blue']};
            font-family: 'Roboto Mono', monospace;
            font-size: 14px;
            font-weight: 700;
        }}
        
        QLabel#maritimeTimeRemaining {{
            color: {MARITIME_COLORS['tidal_cyan']};
            font-family: 'Roboto Mono', monospace;
            font-size: 10px;
            font-weight: 500;
        }}
        
        QLabel#maritimeStatusText {{
            color: {MARITIME_COLORS['emerald_success']};
            font-family: 'Roboto', sans-serif;
            font-size: 11px;
            font-weight: 500;
        }}
        
        QFrame#maritimeSeparator {{
            color: {MARITIME_COLORS['slate_gray']};
            background-color: {MARITIME_COLORS['slate_gray']};
        }}
        
        QScrollArea#maritimeStepsScroll {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background-color: {MARITIME_COLORS['frost_light']};
            width: {FIBONACCI_SPACES[1]}px;
            border-radius: {FIBONACCI_SPACES[1] // 2}px;
        }}
        
        QScrollBar::handle:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MARITIME_COLORS['tidal_cyan']},
                stop:1 {MARITIME_COLORS['harbor_blue']});
            border-radius: {FIBONACCI_SPACES[1] // 2}px;
            min-height: {FIBONACCI_SPACES[2]}px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MARITIME_COLORS['harbor_blue']},
                stop:1 {MARITIME_COLORS['steel_blue']});
        }}
        
        QPushButton#maritimeHelpButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MARITIME_COLORS['azure_info']},
                stop:1 {MARITIME_COLORS['steel_blue']});
            border: 2px solid {MARITIME_COLORS['azure_info']};
            border-radius: {FIBONACCI_SPACES[3] // 2}px;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            font-weight: bold;
        }}
        
        QPushButton#maritimeHelpButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MARITIME_COLORS['steel_blue']},
                stop:1 {MARITIME_COLORS['harbor_blue']});
        }}
        
        QPushButton#maritimeHelpButton:pressed {{
            background: {MARITIME_COLORS['ocean_deep']};
        }}
        """
        
        self.setStyleSheet(style)
    
    def on_step_clicked(self, step_number: int):
        """Gestionnaire de clic sur une étape"""
        if step_number in self.steps and self.steps[step_number].is_accessible:
            self.set_current_step(step_number)
            self.step_selected.emit(step_number)
            logger.debug(f"Étape sélectionnée: {step_number}")
    
    def on_step_status_changed(self, step_number, status):
        """Gestionnaire de changement de statut d'étape"""
        if status == 'completed':
            self.completed_steps = sum(1 for step in self.steps.values() if step.status == 'completed')
            self.update_global_progress()
        
        logger.debug(f"Statut étape {step_number}: {status}")
            
    def set_current_step(self, step_number: int):
        """Définit l'étape actuelle avec animations"""
        if step_number in self.steps:
            # Désactiver l'ancienne étape
            if self.current_step in self.steps:
                if self.steps[self.current_step].status == 'active':
                    self.steps[self.current_step].set_status('pending')
            
            # Activer la nouvelle étape
            self.current_step = step_number
            self.steps[step_number].set_status('active')
            
            logger.debug(f"Étape courante: {step_number}")
            
    def complete_step(self, step_number: int):
        """Marque une étape comme complétée avec animations"""
        if step_number in self.steps:
            self.steps[step_number].set_status('completed')
            
            # Rendre accessible l'étape suivante
            next_step = step_number + 1
            if next_step in self.steps:
                self.steps[next_step].set_accessible(True)
            
            # Mise à jour progression globale
            self.update_global_progress()
            
            logger.info(f"Étape {step_number} complétée")
    
    def update_global_progress(self):
        """Met à jour la progression globale avec animation"""
        completed = sum(1 for step in self.steps.values() if step.status == 'completed')
        progress_percent = int((completed / self.total_steps) * 100)
        
        # Animation de la progression
        if self.progress_animation and hasattr(self.progress_stepper, 'value'):
            current_value = self.progress_stepper.value()
            self.progress_animation.setStartValue(current_value)
            self.progress_animation.setEndValue(progress_percent)
            self.progress_animation.start()
        
        # Mise à jour des labels
        self.percentage_label.setText(f"{progress_percent}%")
        
        # Calcul temps restant
        remaining_steps = self.total_steps - completed
        estimated_time = remaining_steps * 2  # 2 min par étape en moyenne
        
        if estimated_time <= 0:
            self.time_remaining_label.setText("Terminé")
        elif estimated_time < 60:
            self.time_remaining_label.setText(f"~{estimated_time}min")
        else:
            hours = estimated_time // 60
            mins = estimated_time % 60
            self.time_remaining_label.setText(f"~{hours}h{mins:02d}")
        
        # Émission du signal de progression
        self.calibration_progress_changed.emit(progress_percent)
        
        logger.debug(f"Progression globale: {progress_percent}% ({completed}/{self.total_steps})")
                
    def get_current_step(self) -> int:
        """Retourne l'étape actuelle"""
        return self.current_step
    
    def reset_steps(self):
        """Remet à zéro toutes les étapes avec animations"""
        for step_num, step in self.steps.items():
            if step_num == 1:
                step.set_status('active')
                step.set_accessible(True)
            else:
                step.set_status('pending')
                step.set_accessible(False)
            
            step.set_progress(0)
        
        self.current_step = 1
        self.completed_steps = 0
        self.update_global_progress()
        
        logger.info("Toutes les étapes ont été réinitialisées")
    
    def show_help(self):
        """Affiche l'aide contextuelle"""
        try:
            from PyQt6.QtWidgets import QMessageBox
        except ImportError:
            from PySide6.QtWidgets import QMessageBox
        
        help_text = """
        <h3>🔧 Aide Calibration Maritime</h3>
        <p><b>Processus de calibration CHNeoWave:</b></p>
        <ul>
        <li><b>Initialisation:</b> Vérification des capteurs</li>
        <li><b>Zéro:</b> Définition du point de référence</li>
        <li><b>Échelle:</b> Ajustement de la sensibilité</li>
        <li><b>Validation:</b> Tests de précision</li>
        <li><b>Sauvegarde:</b> Enregistrement des paramètres</li>
        </ul>
        <p><i>Durée estimée: 10-15 minutes</i></p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Aide Calibration")
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
        
        logger.debug("Aide contextuelle affichée")


class MaritimeCalibrationProgressBar(MaritimeCard):
    """
    Barre de progression maritime pour la calibration avec animations et métriques
    """
    
    # Signaux
    progress_changed = pyqtSignal(int, int)  # current_step, total_steps
    time_updated = pyqtSignal(str, str)      # elapsed_time, estimated_remaining
    
    def __init__(self, parent=None):
        # Initialisation des attributs avant l'appel au constructeur parent
        self.title = ""
        self.content = ""
        # Appel du constructeur parent avec seulement le parent
        super().__init__(parent)
        
        self.current_step = 1
        self.total_steps = 5
        self.start_time = None
        self.step_times = []  # Temps pour chaque étape
        
        # Animations
        self.progress_animation = QPropertyAnimation(self, b"value")
        self.progress_animation.setDuration(800)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.glow_animation = QPropertyAnimation(self, b"glow_intensity")
        self.glow_animation.setDuration(1500)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.valueChanged.connect(self.update)
        
        self._glow_intensity = 0.0
        
        self.setup_ui()
        self.start_timing()
        
    @pyqtProperty(float)
    def glow_intensity(self):
        return self._glow_intensity
        
    @glow_intensity.setter
    def glow_intensity(self, value):
        self._glow_intensity = value
        self.update()
        
    def setup_ui(self):
        """Configure l'interface de la barre de progression maritime"""
        self.setObjectName("maritime_calibration_progress")
        self.setFixedHeight(FIBONACCI_SPACES[6])  # 89px
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(FIBONACCI_SPACES[4], FIBONACCI_SPACES[3], 
                                 FIBONACCI_SPACES[4], FIBONACCI_SPACES[3])
        layout.setSpacing(FIBONACCI_SPACES[2])
        
        # En-tête avec titre et métriques
        header_layout = QHBoxLayout()
        
        # Titre de progression
        self.progress_label = QLabel(f"Calibration Maritime - Étape {self.current_step}/{self.total_steps}")
        self.progress_label.setFont(QFont("Inter", 14, QFont.Weight.DemiBold))
        self.progress_label.setStyleSheet(f"color: {MARITIME_COLORS['text_primary']};")
        
        # Métriques de temps
        self.time_metrics = QLabel("Temps écoulé: 00:00 | Restant estimé: --:--")
        self.time_metrics.setFont(QFont("JetBrains Mono", 10, QFont.Weight.Medium))
        self.time_metrics.setStyleSheet(f"color: {MARITIME_COLORS['text_secondary']};")
        self.time_metrics.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        header_layout.addWidget(self.progress_label)
        header_layout.addStretch()
        header_layout.addWidget(self.time_metrics)
        
        # Barre de progression avec pourcentage
        progress_layout = QHBoxLayout()
        
        # Barre de progression principale
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.total_steps * 100)  # Pour plus de précision
        self.progress_bar.setValue(self.current_step * 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(FIBONACCI_SPACES[3])  # 21px
        
        # Pourcentage avec badge
        self.percentage_label = QLabel(f"{int((self.current_step / self.total_steps) * 100)}%")
        self.percentage_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.percentage_label.setStyleSheet(f"""
            QLabel {{
                color: {MARITIME_COLORS['accent']};
                background-color: {MARITIME_COLORS['surface']};
                border: 2px solid {MARITIME_COLORS['accent']};
                border-radius: {FIBONACCI_SPACES[2]}px;
                padding: {FIBONACCI_SPACES[1]}px {FIBONACCI_SPACES[2]}px;
                min-width: {FIBONACCI_SPACES[5]}px;
            }}
        """)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.percentage_label)
        
        # Indicateurs d'étapes
        self.step_indicators = QHBoxLayout()
        self.step_dots = []
        self.create_step_indicators()
        
        # Assemblage
        layout.addLayout(header_layout)
        layout.addLayout(progress_layout)
        layout.addLayout(self.step_indicators)
        
        self.apply_maritime_style()
        
    def create_step_indicators(self):
        """Crée les indicateurs visuels pour chaque étape"""
        for i in range(self.total_steps):
            dot = QLabel()
            dot.setFixedSize(FIBONACCI_SPACES[2], FIBONACCI_SPACES[2])
            dot.setStyleSheet(f"""
                QLabel {{
                    background-color: {MARITIME_COLORS['border'] if i >= self.current_step else MARITIME_COLORS['accent']};
                    border-radius: {FIBONACCI_SPACES[2] // 2}px;
                    border: 1px solid {MARITIME_COLORS['accent'] if i < self.current_step else MARITIME_COLORS['border']};
                }}
            """)
            
            self.step_dots.append(dot)
            self.step_indicators.addWidget(dot)
            
            if i < self.total_steps - 1:
                # Ligne de connexion
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFixedHeight(2)
                line.setStyleSheet(f"""
                    QFrame {{
                        background-color: {MARITIME_COLORS['accent'] if i < self.current_step - 1 else MARITIME_COLORS['border']};
                        border: none;
                    }}
                """)
                self.step_indicators.addWidget(line)
        
    def apply_maritime_style(self):
        """Applique le style maritime à la barre de progression"""
        # Style de la barre de progression
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {MARITIME_COLORS['border']};
                border-radius: {FIBONACCI_SPACES[2]}px;
                background-color: {MARITIME_COLORS['surface']};
                text-align: center;
                font-family: 'Inter';
                font-weight: 600;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {MARITIME_COLORS['primary']}, 
                    stop:0.5 {MARITIME_COLORS['accent']}, 
                    stop:1 {MARITIME_COLORS['secondary']});
                border-radius: {FIBONACCI_SPACES[2] - 2}px;
                margin: 1px;
            }}
        """)
        
        # Style du conteneur principal
        self.setStyleSheet(f"""
            QFrame#maritime_calibration_progress {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MARITIME_COLORS['background']}, 
                    stop:1 {MARITIME_COLORS['surface']});
                border: 2px solid {MARITIME_COLORS['border']};
                border-radius: {FIBONACCI_SPACES[3]}px;
                box-shadow: 0 {FIBONACCI_SPACES[1]}px {FIBONACCI_SPACES[3]}px rgba(10, 25, 41, 0.1);
            }}
        """)
        
    def start_timing(self):
        """Démarre le chronométrage de la calibration"""
        from datetime import datetime
        self.start_time = datetime.now()
        
        # Timer pour mettre à jour les métriques
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time_metrics)
        self.time_timer.start(1000)  # Mise à jour chaque seconde
        
    def update_time_metrics(self):
        """Met à jour les métriques de temps"""
        if not self.start_time:
            return
            
        from datetime import datetime
        elapsed = datetime.now() - self.start_time
        elapsed_str = f"{elapsed.seconds // 60:02d}:{elapsed.seconds % 60:02d}"
        
        # Estimation du temps restant basée sur la progression
        if self.current_step > 1 and len(self.step_times) > 0:
            avg_step_time = sum(self.step_times) / len(self.step_times)
            remaining_steps = self.total_steps - self.current_step
            estimated_remaining = int(avg_step_time * remaining_steps)
            remaining_str = f"{estimated_remaining // 60:02d}:{estimated_remaining % 60:02d}"
        else:
            remaining_str = "--:--"
            
        self.time_metrics.setText(f"Temps écoulé: {elapsed_str} | Restant estimé: {remaining_str}")
        self.time_updated.emit(elapsed_str, remaining_str)
        
    def set_step(self, step: int, animate: bool = True):
        """Met à jour la progression avec animation"""
        old_step = self.current_step
        self.current_step = min(max(step, 1), self.total_steps)
        
        # Enregistrer le temps de l'étape précédente
        if old_step != self.current_step and self.start_time:
            from datetime import datetime
            step_duration = (datetime.now() - self.start_time).seconds
            if len(self.step_times) >= old_step - 1:
                self.step_times.append(step_duration)
            
        # Animation de la barre de progression
        if animate:
            self.progress_animation.setStartValue(self.progress_bar.value())
            self.progress_animation.setEndValue(self.current_step * 100)
            self.progress_animation.start()
        else:
            self.progress_bar.setValue(self.current_step * 100)
            
        # Mettre à jour les labels
        self.progress_label.setText(f"Calibration Maritime - Étape {self.current_step}/{self.total_steps}")
        
        percentage = int((self.current_step / self.total_steps) * 100)
        self.percentage_label.setText(f"{percentage}%")
        
        # Mettre à jour les indicateurs d'étapes
        self.update_step_indicators()
        
        # Démarrer l'animation de glow si on progresse
        if self.current_step > old_step:
            self.start_glow_animation()
            
        self.progress_changed.emit(self.current_step, self.total_steps)
        
    def update_step_indicators(self):
        """Met à jour l'apparence des indicateurs d'étapes"""
        for i, dot in enumerate(self.step_dots):
            if i < self.current_step:
                # Étape complétée
                dot.setStyleSheet(f"""
                    QLabel {{
                        background-color: {MARITIME_COLORS['accent']};
                        border-radius: {FIBONACCI_SPACES[2] // 2}px;
                        border: 2px solid {MARITIME_COLORS['accent']};
                    }}
                """)
            elif i == self.current_step:
                # Étape actuelle
                dot.setStyleSheet(f"""
                    QLabel {{
                        background-color: {MARITIME_COLORS['primary']};
                        border-radius: {FIBONACCI_SPACES[2] // 2}px;
                        border: 2px solid {MARITIME_COLORS['accent']};
                    }}
                """)
            else:
                # Étape future
                dot.setStyleSheet(f"""
                    QLabel {{
                        background-color: {MARITIME_COLORS['surface']};
                        border-radius: {FIBONACCI_SPACES[2] // 2}px;
                        border: 1px solid {MARITIME_COLORS['border']};
                    }}
                """)
                
    def start_glow_animation(self):
        """Démarre l'animation de glow pour indiquer la progression"""
        self.glow_animation.setStartValue(0.0)
        self.glow_animation.setEndValue(1.0)
        self.glow_animation.setDirection(QPropertyAnimation.Direction.Forward)
        self.glow_animation.start()
        
        # Arrêter l'animation après 3 secondes
        QTimer.singleShot(3000, self.glow_animation.stop)
        
    def reset_progress(self):
        """Remet à zéro la progression"""
        self.current_step = 1
        self.step_times.clear()
        self.start_timing()
        self.set_step(1, animate=False)
        
    def complete_calibration(self):
        """Marque la calibration comme terminée"""
        self.set_step(self.total_steps)
        self.time_timer.stop()
        
        # Animation finale de succès
        self.glow_animation.setStartValue(0.0)
        self.glow_animation.setEndValue(1.0)
        self.glow_animation.setLoopCount(3)
        self.glow_animation.start()
        
        logger.info(f"Calibration maritime terminée en {len(self.step_times)} étapes")


class MaritimeCalibrationView(QWidget):
    """
    Vue de calibration maritime complète avec design system 2025
    """
    
    # Signaux
    calibration_completed = pyqtSignal()  # Signal émis quand la calibration est terminée
    step_changed = pyqtSignal(int)        # Signal émis lors du changement d'étape
    calibration_started = pyqtSignal()    # Signal émis au début de la calibration
    calibration_paused = pyqtSignal()     # Signal émis lors de la pause
    calibration_resumed = pyqtSignal()    # Signal émis lors de la reprise
    error_occurred = pyqtSignal(str)      # Signal émis en cas d'erreur
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_step = 1
        self.is_dark_mode = False
        self.is_paused = False
        self.calibration_data = {}
        
        # Animations globales
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        
        self.setup_ui()
        self.setup_connections()
        self.apply_maritime_theme()
        
    def setup_ui(self):
        """Configure l'interface maritime principale"""
        self.setObjectName("maritime_calibration_view")
        
        # Layout principal avec espacement maritime
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(FIBONACCI_SPACES[2], FIBONACCI_SPACES[2], 
                                      FIBONACCI_SPACES[2], FIBONACCI_SPACES[2])
        main_layout.setSpacing(FIBONACCI_SPACES[2])
        
        # En-tête maritime avec titre et contrôles
        self.setup_maritime_header(main_layout)
        
        # Barre de progression maritime
        self.progress_bar = MaritimeCalibrationProgressBar()
        main_layout.addWidget(self.progress_bar)
        
        # Splitter horizontal avec design maritime
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("maritime_splitter")
        
        # Sidebar des étapes maritimes
        self.sidebar = MaritimeCalibrationSidebar()
        splitter.addWidget(self.sidebar)
        
        # Zone principale maritime
        self.main_area = MaritimeCard()
        self.main_area.setObjectName("maritime_calibration_main_area")
        self.setup_maritime_main_area()
        splitter.addWidget(self.main_area)
        
        # Proportions du splitter (Golden Ratio optimisé)
        sidebar_width = int(FIBONACCI_SPACES[9])  # 377px
        main_width = int(sidebar_width * GOLDEN_RATIO)  # ~610px
        splitter.setSizes([sidebar_width, main_width])
        splitter.setCollapsible(0, False)  # Sidebar non collapsible
        splitter.setCollapsible(1, False)  # Main area non collapsible
        
        # Style maritime du splitter
        splitter.setStyleSheet(f"""
            QSplitter#maritime_splitter {{
                background-color: {MARITIME_COLORS['background']};
            }}
            QSplitter#maritime_splitter::handle {{
                background-color: {MARITIME_COLORS['border']};
                width: {FIBONACCI_SPACES[1]}px;
                border-radius: {FIBONACCI_SPACES[1]}px;
            }}
            QSplitter#maritime_splitter::handle:hover {{
                background-color: {MARITIME_COLORS['accent']};
            }}
        """)
        
        main_layout.addWidget(splitter)
        
        # Barre d'état maritime
        self.setup_maritime_status_bar(main_layout)
        
    def setup_maritime_header(self, layout):
        """Configure l'en-tête maritime avec titre et contrôles"""
        header_card = MaritimeCard()
        header_card.setObjectName("maritime_header")
        header_card.setFixedHeight(FIBONACCI_SPACES[6])  # 89px
        
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(FIBONACCI_SPACES[3], FIBONACCI_SPACES[2], 
                                        FIBONACCI_SPACES[3], FIBONACCI_SPACES[2])
        
        # Titre principal avec icône maritime
        title_layout = QHBoxLayout()
        
        # Icône maritime (ancre)
        icon_label = QLabel("⚓")
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        icon_label.setStyleSheet(f"color: {MARITIME_COLORS['accent']};")
        
        # Titre
        title_label = QLabel("Calibration Maritime CHNeoWave")
        title_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {MARITIME_COLORS['text_primary']};")
        
        # Sous-titre
        subtitle_label = QLabel("Système de calibration pour modèles réduits maritimes")
        subtitle_label.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        subtitle_label.setStyleSheet(f"color: {MARITIME_COLORS['text_secondary']};")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.addStretch()
        
        # Contrôles de calibration
        controls_layout = QHBoxLayout()
        
        # Bouton Pause/Reprendre
        self.pause_button = MaritimeButton("⏸️ Pause", button_type="secondary")
        self.pause_button.setFixedSize(FIBONACCI_SPACES[7], FIBONACCI_SPACES[5])  # 144x55
        self.pause_button.clicked.connect(self.toggle_pause)
        
        # Bouton Arrêter
        self.stop_button = MaritimeButton("⏹️ Arrêter", button_type="danger")
        self.stop_button.setFixedSize(FIBONACCI_SPACES[7], FIBONACCI_SPACES[5])
        self.stop_button.clicked.connect(self.stop_calibration)
        
        # Indicateur de statut
        self.status_beacon = StatusBeacon("active")
        
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.status_beacon)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(controls_layout)
        
        # Style de l'en-tête
        header_card.setStyleSheet(f"""
            QFrame#maritime_header {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {MARITIME_COLORS['primary']}, 
                    stop:1 {MARITIME_COLORS['secondary']});
                border: 2px solid {MARITIME_COLORS['accent']};
                border-radius: {FIBONACCI_SPACES[3]}px;
                color: white;
            }}
        """)
        
        layout.addWidget(header_card)
        
    def setup_maritime_status_bar(self, layout):
        """Configure la barre d'état maritime"""
        status_card = MaritimeCard()
        status_card.setObjectName("maritime_status_bar")
        status_card.setFixedHeight(FIBONACCI_SPACES[5])  # 55px
        
        status_layout = QHBoxLayout(status_card)
        status_layout.setContentsMargins(FIBONACCI_SPACES[3], FIBONACCI_SPACES[1], 
                                        FIBONACCI_SPACES[3], FIBONACCI_SPACES[1])
        
        # Informations de session
        self.session_info = QLabel("Session: Nouvelle calibration")
        self.session_info.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        self.session_info.setStyleSheet(f"color: {MARITIME_COLORS['text_secondary']};")
        
        # Statut de connexion hardware
        self.hardware_status = QLabel("🔗 Hardware: Connecté")
        self.hardware_status.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        self.hardware_status.setStyleSheet(f"color: {MARITIME_COLORS['success']};")
        
        # Indicateur de qualité du signal
        self.signal_quality = QLabel("📶 Signal: Excellent (98%)")
        self.signal_quality.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        self.signal_quality.setStyleSheet(f"color: {MARITIME_COLORS['success']};")
        
        # Version du logiciel
        self.version_info = QLabel("CHNeoWave v1.0.0-maritime")
        self.version_info.setFont(QFont("JetBrains Mono", 9, QFont.Weight.Normal))
        self.version_info.setStyleSheet(f"color: {MARITIME_COLORS['text_tertiary']};")
        
        status_layout.addWidget(self.session_info)
        status_layout.addStretch()
        status_layout.addWidget(self.hardware_status)
        status_layout.addWidget(self.signal_quality)
        status_layout.addStretch()
        status_layout.addWidget(self.version_info)
        
        # Style de la barre d'état
        status_card.setStyleSheet(f"""
            QFrame#maritime_status_bar {{
                background-color: {MARITIME_COLORS['surface']};
                border: 1px solid {MARITIME_COLORS['border']};
                border-radius: {FIBONACCI_SPACES[2]}px;
            }}
        """)
        
        layout.addWidget(status_card)
        
    def setup_maritime_main_area(self):
        """Configure la zone principale maritime"""
        main_layout = QVBoxLayout(self.main_area)
        main_layout.setContentsMargins(FIBONACCI_SPACES[3], FIBONACCI_SPACES[3], 
                                      FIBONACCI_SPACES[3], FIBONACCI_SPACES[3])
        main_layout.setSpacing(FIBONACCI_SPACES[3])
        
        # En-tête de la zone principale
        self.setup_main_area_header(main_layout)
        
        # Stack widget pour les différentes étapes
        self.step_stack = QStackedWidget()
        self.step_stack.setObjectName("maritime_step_stack")
        
        # Créer les pages maritimes pour chaque étape
        self.create_maritime_step_pages()
        
        main_layout.addWidget(self.step_stack)
        
        # Boutons de navigation maritimes
        self.setup_maritime_navigation_buttons(main_layout)
        
        # Style de la zone principale maritime
        self.main_area.setStyleSheet(f"""
            QFrame#maritime_calibration_main_area {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MARITIME_COLORS['background']}, 
                    stop:1 {MARITIME_COLORS['surface']});
                border: 2px solid {MARITIME_COLORS['border']};
                border-radius: {FIBONACCI_SPACES[3]}px;
            }}
            QStackedWidget#maritime_step_stack {{
                background-color: transparent;
                border: none;
            }}
        """)
        
    def setup_main_area_header(self, layout):
        """Configure l'en-tête de la zone principale"""
        header_layout = QHBoxLayout()
        
        # Titre de l'étape actuelle
        self.step_title = QLabel("Initialisation des Capteurs")
        self.step_title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.step_title.setStyleSheet(f"color: {MARITIME_COLORS['text_primary']};")
        
        # Description de l'étape
        self.step_description = QLabel("Vérification et initialisation des capteurs maritimes")
        self.step_description.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.step_description.setStyleSheet(f"color: {MARITIME_COLORS['text_secondary']};")
        
        # Indicateur de temps estimé
        self.estimated_time = QLabel("⏱️ ~2 min")
        self.estimated_time.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        self.estimated_time.setStyleSheet(f"""
            QLabel {{
                color: {MARITIME_COLORS['accent']};
                background-color: {MARITIME_COLORS['surface']};
                border: 1px solid {MARITIME_COLORS['accent']};
                border-radius: {FIBONACCI_SPACES[2]}px;
                padding: {FIBONACCI_SPACES[1]}px {FIBONACCI_SPACES[2]}px;
            }}
        """)
        
        header_layout.addWidget(self.step_title)
        header_layout.addWidget(self.step_description)
        header_layout.addStretch()
        header_layout.addWidget(self.estimated_time)
        
        layout.addLayout(header_layout)
        
        # Ligne de séparation
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(2)
        separator.setStyleSheet(f"""
            QFrame {{
                background-color: {MARITIME_COLORS['border']};
                border: none;
                margin: {FIBONACCI_SPACES[2]}px 0;
            }}
        """)
        layout.addWidget(separator)
        
    def toggle_pause(self):
        """Bascule entre pause et reprise de la calibration"""
        if self.is_paused:
            self.resume_calibration()
        else:
            self.pause_calibration()
            
    def pause_calibration(self):
        """Met en pause la calibration"""
        self.is_paused = True
        self.pause_button.setText("▶️ Reprendre")
        self.status_beacon.set_status("warning")
        self.calibration_paused.emit()
        logger.info("Calibration maritime mise en pause")
        
    def resume_calibration(self):
        """Reprend la calibration"""
        self.is_paused = False
        self.pause_button.setText("⏸️ Pause")
        self.status_beacon.set_status("active")
        self.calibration_resumed.emit()
        logger.info("Calibration maritime reprise")
        
    def stop_calibration(self):
        """Arrête complètement la calibration"""
        reply = QMessageBox.question(
            self, 
            "Arrêter la Calibration",
            "Êtes-vous sûr de vouloir arrêter la calibration maritime ?\n\nToutes les données non sauvegardées seront perdues.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.reset_calibration()
            self.status_beacon.set_status("inactive")
            logger.warning("Calibration maritime arrêtée par l'utilisateur")
            
    def apply_maritime_theme(self):
        """Applique le thème maritime global"""
        self.setStyleSheet(f"""
            QWidget#maritime_calibration_view {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MARITIME_COLORS['background']}, 
                    stop:1 {MARITIME_COLORS['surface']});
                font-family: 'Inter', sans-serif;
            }}
            
            QLabel {{
                background-color: transparent;
            }}
            
            QMessageBox {{
                background-color: {MARITIME_COLORS['surface']};
                color: {MARITIME_COLORS['text_primary']};
            }}
            
            QMessageBox QPushButton {{
                background-color: {MARITIME_COLORS['primary']};
                color: white;
                border: none;
                border-radius: {FIBONACCI_SPACES[2]}px;
                padding: {FIBONACCI_SPACES[2]}px {FIBONACCI_SPACES[3]}px;
                font-weight: 600;
                min-width: {FIBONACCI_SPACES[6]}px;
            }}
            
            QMessageBox QPushButton:hover {{
                background-color: {MARITIME_COLORS['accent']};
            }}
        """)
        
    def create_step_pages(self):
        """Crée les pages pour chaque étape"""
        # Étape 1: Initialisation
        step1 = self.create_initialization_page()
        self.step_stack.addWidget(step1)
        
        # Étape 2: Étalonnage Zéro
        step2 = self.create_zero_calibration_page()
        self.step_stack.addWidget(step2)
        
        # Étape 3: Calibration Linéaire
        step3 = self.create_linear_calibration_page()
        self.step_stack.addWidget(step3)
        
        # Étape 4: Validation
        step4 = self.create_validation_page()
        self.step_stack.addWidget(step4)
        
        # Étape 5: Sauvegarde
        step5 = self.create_save_page()
        self.step_stack.addWidget(step5)
        
    def create_initialization_page(self) -> QWidget:
        """Crée la page d'initialisation"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title = QLabel("Initialisation des Capteurs")
        title.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title.setStyleSheet("color: #0A1929;")
        
        # Description
        description = QLabel(
            "Cette étape vérifie la connectivité et l'état des capteurs. "
            "Assurez-vous que tous les capteurs sont correctement connectés "
            "avant de continuer."
        )
        description.setFont(QFont("Inter", 13))
        description.setStyleSheet("color: #445868;")
        description.setWordWrap(True)
        
        # Zone de statut des capteurs
        sensors_group = QGroupBox("État des Capteurs")
        sensors_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        sensors_layout = QGridLayout(sensors_group)
        
        # Liste des capteurs (exemple)
        sensors = [
            ("Capteur de Pression 1", "✅ Connecté"),
            ("Capteur de Pression 2", "✅ Connecté"),
            ("Capteur de Température", "✅ Connecté"),
            ("Capteur de Débit", "⚠️ Vérification...")
        ]
        
        for i, (sensor_name, status) in enumerate(sensors):
            name_label = QLabel(sensor_name)
            name_label.setFont(QFont("Inter", 12))
            
            status_label = QLabel(status)
            status_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
            
            sensors_layout.addWidget(name_label, i, 0)
            sensors_layout.addWidget(status_label, i, 1)
            
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(sensors_group)
        layout.addStretch()
        
        return page
        
    def create_zero_calibration_page(self) -> QWidget:
        """Crée la page d'étalonnage zéro"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title = QLabel("Étalonnage du Point Zéro")
        title.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title.setStyleSheet("color: #0A1929; margin-bottom: 13px;")
        
        # Instructions
        instructions = QLabel(
            "Placez les capteurs dans leur position de référence (zéro). "
            "Cette étape définit le point de référence pour toutes les mesures."
        )
        instructions.setFont(QFont("Inter", 13))
        instructions.setStyleSheet("color: #445868; margin-bottom: 21px;")
        instructions.setWordWrap(True)
        
        # Zone de mesures
        measurements_group = QGroupBox("Mesures Actuelles")
        measurements_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        measurements_layout = QGridLayout(measurements_group)
        
        # Exemple de mesures
        measurements = [
            ("Pression 1", "0.001 bar", "#4CAF50"),
            ("Pression 2", "0.002 bar", "#4CAF50"),
            ("Température", "20.5°C", "#4CAF50"),
            ("Débit", "0.1 L/min", "#FF9800")
        ]
        
        for i, (param, value, color) in enumerate(measurements):
            param_label = QLabel(param)
            param_label.setFont(QFont("Inter", 12))
            
            value_label = QLabel(value)
            value_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
            value_label.setStyleSheet(f"color: {color};")
            
            measurements_layout.addWidget(param_label, i, 0)
            measurements_layout.addWidget(value_label, i, 1)
            
        layout.addWidget(title)
        layout.addWidget(instructions)
        layout.addWidget(measurements_group)
        layout.addStretch()
        
        return page
        
    def create_linear_calibration_page(self) -> QWidget:
        """Crée la page de calibration linéaire"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title = QLabel("Calibration Linéaire")
        title.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title.setStyleSheet("color: #0A1929;")
        
        # Description
        description = QLabel(
            "Cette étape mesure la linéarité des capteurs sur leur plage de fonctionnement. "
            "Plusieurs points de mesure seront pris pour établir la courbe de calibration."
        )
        description.setFont(QFont("Inter", 13))
        description.setStyleSheet("color: #445868;")
        description.setWordWrap(True)
        
        # Zone de graphique (placeholder)
        graph_frame = QFrame()
        graph_frame.setObjectName("calibration_graph")
        graph_frame.setMinimumHeight(300)
        graph_frame.setStyleSheet("""
            QFrame#calibration_graph {
                background-color: white;
                border: 2px solid #E0E7FF;
                border-radius: 13px;
            }
        """)
        
        graph_layout = QVBoxLayout(graph_frame)
        graph_placeholder = QLabel("📈 Graphique de Linéarité")
        graph_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_placeholder.setFont(QFont("Inter", 16))
        graph_placeholder.setStyleSheet("color: #445868;")
        graph_layout.addWidget(graph_placeholder)
        
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(graph_frame)
        
        return page
        
    def create_validation_page(self) -> QWidget:
        """Crée la page de validation"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title = QLabel("Validation de la Calibration")
        title.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title.setStyleSheet("color: #0A1929;")
        
        # Description
        description = QLabel(
            "Tests de précision et de répétabilité pour valider la calibration. "
            "Les résultats doivent être dans les tolérances spécifiées."
        )
        description.setFont(QFont("Inter", 13))
        description.setStyleSheet("color: #445868;")
        description.setWordWrap(True)
        
        # Résultats de validation
        results_group = QGroupBox("Résultats de Validation")
        results_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        results_layout = QGridLayout(results_group)
        
        # Exemple de résultats
        results = [
            ("Précision", "±0.1%", "✅ Conforme"),
            ("Répétabilité", "±0.05%", "✅ Conforme"),
            ("Linéarité", "R² = 0.9998", "✅ Excellent"),
            ("Dérive", "< 0.01%/h", "✅ Stable")
        ]
        
        for i, (test, value, status) in enumerate(results):
            test_label = QLabel(test)
            test_label.setFont(QFont("Inter", 12))
            
            value_label = QLabel(value)
            value_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
            
            status_label = QLabel(status)
            status_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
            status_label.setStyleSheet("color: #4CAF50;")
            
            results_layout.addWidget(test_label, i, 0)
            results_layout.addWidget(value_label, i, 1)
            results_layout.addWidget(status_label, i, 2)
            
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(results_group)
        layout.addStretch()
        
        return page
        
    def create_save_page(self) -> QWidget:
        """Crée la page de sauvegarde"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title = QLabel("Sauvegarde des Paramètres")
        title.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title.setStyleSheet("color: #0A1929;")
        
        # Description
        description = QLabel(
            "Enregistrement des paramètres de calibration. "
            "Ces paramètres seront utilisés pour toutes les mesures futures."
        )
        description.setFont(QFont("Inter", 13))
        description.setStyleSheet("color: #445868;")
        description.setWordWrap(True)
        
        # Résumé de la calibration
        summary_group = QGroupBox("Résumé de la Calibration")
        summary_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        summary_layout = QVBoxLayout(summary_group)
        
        summary_text = QTextEdit()
        summary_text.setReadOnly(True)
        summary_text.setMaximumHeight(150)
        summary_text.setPlainText(
            "Calibration terminée avec succès.\n"
            "Date: 2025-01-XX\n"
            "Capteurs calibrés: 4\n"
            "Précision moyenne: ±0.08%\n"
            "Temps total: 15 minutes"
        )
        summary_layout.addWidget(summary_text)
        
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(summary_group)
        layout.addStretch()
        
        return page
        
    def setup_navigation_buttons(self, parent_layout):
        """Configure les boutons de navigation"""
        nav_frame = QFrame()
        nav_frame.setFixedHeight(55)  # Fibonacci
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, FIBONACCI_SPACING[1], 0, FIBONACCI_SPACING[1])
        nav_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Bouton Précédent
        self.prev_button = QPushButton("← Précédent")
        self.prev_button.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        self.prev_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        self.prev_button.clicked.connect(self.go_to_previous_step)
        
        # Bouton Continuer/Terminer
        self.next_button = QPushButton("Continuer →")
        self.next_button.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        self.next_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        self.next_button.clicked.connect(self.go_to_next_step)
        
        # Style des boutons
        button_style = """
            QPushButton {
                background-color: #00ACC1;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 8px 21px;
                font-weight: 500;
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
        
        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)
        
        # Assemblage
        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        
        parent_layout.addWidget(nav_frame)
        
        # État initial
        self.update_navigation_buttons()
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        self.sidebar.step_selected.connect(self.go_to_step)
        
    def go_to_step(self, step_number: int):
        """Va à une étape spécifique"""
        if 1 <= step_number <= 5:
            self.current_step = step_number
            
            # Mettre à jour l'interface
            self.step_stack.setCurrentIndex(step_number - 1)
            self.progress_bar.set_step(step_number)
            self.sidebar.set_current_step(step_number)
            
            # Mettre à jour les boutons
            self.update_navigation_buttons()
            
            # Émettre le signal
            self.step_changed.emit(step_number)
            
    def go_to_previous_step(self):
        """Va à l'étape précédente"""
        if self.current_step > 1:
            self.go_to_step(self.current_step - 1)
            
    def go_to_next_step(self):
        """Va à l'étape suivante"""
        if self.current_step < 5:
            # Marquer l'étape actuelle comme complétée
            self.sidebar.complete_step(self.current_step)
            
            # Aller à l'étape suivante
            self.go_to_step(self.current_step + 1)
        else:
            # Dernière étape - terminer la calibration
            self.complete_calibration()
            
    def complete_calibration(self):
        """Termine la calibration"""
        # Marquer la dernière étape comme complétée
        self.sidebar.complete_step(self.current_step)
        
        # Émettre le signal de fin
        self.calibration_completed.emit()
        
    def update_navigation_buttons(self):
        """Met à jour l'état des boutons de navigation"""
        # Bouton Précédent
        self.prev_button.setEnabled(self.current_step > 1)
        
        # Bouton Suivant/Terminer
        if self.current_step == 5:
            self.next_button.setText("Terminer")
        else:
            self.next_button.setText("Continuer →")
            
    def set_theme(self, is_dark: bool):
        """Applique le thème sombre ou clair"""
        self.is_dark_mode = is_dark
        
        if is_dark:
            # Thème sombre
            self.setStyleSheet("""
                QWidget#unified_calibration_view {
                    background-color: #0A1929;
                    color: #F5FBFF;
                }
            """)
        else:
            # Thème clair
            self.setStyleSheet("""
                QWidget#unified_calibration_view {
                    background-color: #F5FBFF;
                    color: #0A1929;
                }
            """)
            
    def get_current_step(self) -> int:
        """Retourne l'étape actuelle"""
        return self.current_step
        
    def reset_calibration(self):
        """Remet à zéro la calibration"""
        self.go_to_step(1)
        
        # Réinitialiser les états des étapes
        for step_num in range(2, 6):
            if step_num in self.sidebar.steps:
                self.sidebar.steps[step_num].set_completed(False)
                self.sidebar.steps[step_num].set_accessible(False)
                
        # Rendre accessible la première étape
        if 1 in self.sidebar.steps:
            self.sidebar.steps[1].set_accessible(True)