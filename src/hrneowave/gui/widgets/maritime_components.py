# -*- coding: utf-8 -*-
"""
CHNeoWave Maritime Components 2025
Composants UI standardisés pour laboratoires océanographiques
Conformes au Maritime Design System

Auteur: Claude Sonnet 4 - Architecte Logiciel en Chef
Date: 2025-01-27
Version: 1.0.0
"""

import sys
from typing import Optional, List, Dict, Any, Union
from enum import Enum

# Import hiérarchique PySide6 > PyQt6 > PyQt5
try:
    from PySide6.QtWidgets import (
        QWidget, QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
        QGridLayout, QProgressBar, QSizePolicy, QSpacerItem
    )
    from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal as Signal
    from PySide6.QtGui import QFont, QPalette, QColor, QPainter, QBrush
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QWidget, QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
            QGridLayout, QProgressBar, QSizePolicy, QSpacerItem
        )
        from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal as Signal
        from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QBrush
    except ImportError:
        from PyQt5.QtWidgets import (
            QWidget, QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
            QGridLayout, QProgressBar, QSizePolicy, QSpacerItem
        )
        from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal as Signal
        from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush


class MaritimeTheme:
    """Thème maritime centralisé - Palette certifiée"""
    
    # Couleurs principales
    OCEAN_DEEP = "#0A1929"
    HARBOR_BLUE = "#1565C0"
    STEEL_BLUE = "#1976D2"
    TIDAL_CYAN = "#00BCD4"
    FOAM_WHITE = "#FAFBFC"
    FROST_LIGHT = "#F5F7FA"
    STORM_GRAY = "#37474F"
    SLATE_GRAY = "#546E7A"
    CORAL_ALERT = "#FF5722"
    EMERALD_SUCCESS = "#4CAF50"
    
    # Espacements Golden Ratio
    SPACE_XS = 8
    SPACE_SM = 13
    SPACE_MD = 21
    SPACE_LG = 34
    SPACE_XL = 55
    
    # Typographie
    FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
    FONT_H1 = 32
    FONT_H2 = 24
    FONT_H3 = 20
    FONT_BODY = 14
    FONT_CAPTION = 12
    
    # Rayons de bordure
    RADIUS_SM = 4
    RADIUS_MD = 8
    RADIUS_LG = 12


class StatusType(Enum):
    """Types de statut pour les composants"""
    ACTIVE = "active"
    WARNING = "warning"
    ERROR = "error"
    INACTIVE = "inactive"
    SUCCESS = "success"


class MaritimeCard(QFrame):
    """Carte maritime standardisée avec élévation"""
    
    def __init__(self, parent: Optional[QWidget] = None, title: str = "", elevated: bool = True):
        super().__init__(parent)
        self.title = title
        self.elevated = elevated
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configuration de l'interface"""
        self.setObjectName("MaritimeCard")
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            MaritimeTheme.SPACE_MD, MaritimeTheme.SPACE_MD,
            MaritimeTheme.SPACE_MD, MaritimeTheme.SPACE_MD
        )
        self.main_layout.setSpacing(MaritimeTheme.SPACE_SM)
        
        # Titre si fourni
        if self.title:
            self.title_label = QLabel(self.title)
            self.title_label.setObjectName("card-title")
            font = QFont()
            font.setPointSize(MaritimeTheme.FONT_H3)
            font.setWeight(QFont.Weight.Medium)
            self.title_label.setFont(font)
            self.main_layout.addWidget(self.title_label)
        
        # Zone de contenu
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.content_widget)
    
    def _apply_styles(self):
        """Application des styles maritimes"""
        elevation_style = ""
        if self.elevated:
            elevation_style = "border: 1px solid rgba(21, 101, 192, 0.12);"
        
        self.setStyleSheet(f"""
            QFrame#MaritimeCard {{
                background-color: {MaritimeTheme.FOAM_WHITE};
                {elevation_style}
                border-radius: {MaritimeTheme.RADIUS_MD}px;
            }}
            QFrame#MaritimeCard:hover {{
                border: 1px solid rgba(21, 101, 192, 0.3);
            }}
            QLabel#card-title {{
                color: {MaritimeTheme.STORM_GRAY};
                font-weight: 500;
            }}
        """)
    
    def add_content(self, widget: QWidget):
        """Ajouter du contenu à la carte"""
        self.content_layout.addWidget(widget)
    
    def set_title(self, title: str):
        """Modifier le titre de la carte"""
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)


class KPIIndicator(QWidget):
    """Indicateur KPI maritime avec valeur et unité"""
    
    def __init__(self, parent: Optional[QWidget] = None, 
                 label: str = "", value: str = "0", unit: str = "",
                 status: StatusType = StatusType.ACTIVE):
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.status = status
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configuration de l'interface"""
        self.setObjectName("KPIIndicator")
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(MaritimeTheme.SPACE_XS)
        
        # Valeur principale
        self.value_label = QLabel(self.value)
        self.value_label.setObjectName("kpi-value")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(MaritimeTheme.FONT_H1)
        font.setWeight(QFont.Weight.Bold)
        self.value_label.setFont(font)
        layout.addWidget(self.value_label)
        
        # Unité
        if self.unit:
            self.unit_label = QLabel(self.unit)
            self.unit_label.setObjectName("kpi-unit")
            self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.unit_label)
        
        # Label descriptif
        if self.label:
            self.label_widget = QLabel(self.label)
            self.label_widget.setObjectName("kpi-label")
            self.label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label_widget.setWordWrap(True)
            layout.addWidget(self.label_widget)
    
    def _apply_styles(self):
        """Application des styles selon le statut"""
        color_map = {
            StatusType.ACTIVE: MaritimeTheme.TIDAL_CYAN,
            StatusType.SUCCESS: MaritimeTheme.EMERALD_SUCCESS,
            StatusType.WARNING: "#FF9800",
            StatusType.ERROR: MaritimeTheme.CORAL_ALERT,
            StatusType.INACTIVE: MaritimeTheme.SLATE_GRAY
        }
        
        value_color = color_map.get(self.status, MaritimeTheme.TIDAL_CYAN)
        
        self.setStyleSheet(f"""
            QWidget#KPIIndicator {{
                background-color: {MaritimeTheme.FOAM_WHITE};
                border: 1px solid {value_color};
                border-radius: {MaritimeTheme.RADIUS_MD}px;
                padding: {MaritimeTheme.SPACE_MD}px;
                min-height: 120px;
            }}
            QLabel#kpi-value {{
                color: {value_color};
                font-weight: 600;
            }}
            QLabel#kpi-unit {{
                color: {MaritimeTheme.SLATE_GRAY};
                font-size: {MaritimeTheme.FONT_BODY}px;
            }}
            QLabel#kpi-label {{
                color: {MaritimeTheme.SLATE_GRAY};
                font-size: {MaritimeTheme.FONT_CAPTION}px;
                font-weight: 400;
            }}
        """)
    
    def update_value(self, value: str, status: Optional[StatusType] = None):
        """Mettre à jour la valeur et le statut"""
        self.value = value
        self.value_label.setText(value)
        
        if status:
            self.status = status
            self._apply_styles()
    
    def set_status(self, status: StatusType):
        """Changer le statut de l'indicateur"""
        self.status = status
        self._apply_styles()


class StatusBeacon(QWidget):
    """Beacon de statut maritime avec animation"""
    
    def __init__(self, parent: Optional[QWidget] = None, 
                 status: StatusType = StatusType.INACTIVE,
                 animated: bool = True):
        super().__init__(parent)
        self.status = status
        self.animated = animated
        self._setup_ui()
        self._setup_animation()
    
    def _setup_ui(self):
        """Configuration de l'interface"""
        self.setObjectName("StatusBeacon")
        self.setFixedSize(12, 12)
        self._apply_styles()
    
    def _setup_animation(self):
        """Configuration de l'animation de pulsation"""
        if self.animated and self.status == StatusType.ACTIVE:
            self.animation_timer = QTimer()
            self.animation_timer.timeout.connect(self._pulse_animation)
            self.animation_timer.start(1000)  # Pulse toutes les secondes
    
    def _apply_styles(self):
        """Application des styles selon le statut"""
        color_map = {
            StatusType.ACTIVE: MaritimeTheme.EMERALD_SUCCESS,
            StatusType.WARNING: "#FF9800",
            StatusType.ERROR: MaritimeTheme.CORAL_ALERT,
            StatusType.INACTIVE: MaritimeTheme.SLATE_GRAY,
            StatusType.SUCCESS: MaritimeTheme.EMERALD_SUCCESS
        }
        
        color = color_map.get(self.status, MaritimeTheme.SLATE_GRAY)
        
        self.setStyleSheet(f"""
            QWidget#StatusBeacon {{
                background-color: {color};
                border-radius: 6px;
                border: none;
            }}
        """)
    
    def _pulse_animation(self):
        """Animation de pulsation pour statut actif"""
        if self.status == StatusType.ACTIVE:
            # Effet de pulsation simple via changement d'opacité
            self.setStyleSheet(f"""
                QWidget#StatusBeacon {{
                    background-color: {MaritimeTheme.EMERALD_SUCCESS};
                    border-radius: 6px;
                    border: 2px solid rgba(76, 175, 80, 0.4);
                }}
            """)
            
            # Retour à l'état normal après 200ms
            QTimer.singleShot(200, self._reset_style)
    
    def _reset_style(self):
        """Retour au style normal"""
        self._apply_styles()
    
    def set_status(self, status: StatusType):
        """Changer le statut du beacon"""
        self.status = status
        self._apply_styles()
        
        # Redémarrer l'animation si nécessaire
        if hasattr(self, 'animation_timer'):
            self.animation_timer.stop()
        
        if self.animated and status == StatusType.ACTIVE:
            self._setup_animation()


class MaritimeButton(QPushButton):
    """Bouton maritime standardisé avec variantes"""
    
    class Variant(Enum):
        PRIMARY = "primary"
        SECONDARY = "secondary"
        DANGER = "danger"
    
    def __init__(self, parent: Optional[QWidget] = None, 
                 text: str = "", variant: Variant = Variant.PRIMARY):
        super().__init__(text, parent)
        self.variant = variant
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configuration de l'interface"""
        self.setObjectName(f"MaritimeButton-{self.variant.value}")
        self.setMinimumSize(120, 44)
        
        # Police
        font = QFont()
        font.setPointSize(MaritimeTheme.FONT_BODY)
        font.setWeight(QFont.Weight.Medium)
        self.setFont(font)
    
    def _apply_styles(self):
        """Application des styles selon la variante"""
        if self.variant == self.Variant.PRIMARY:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {MaritimeTheme.HARBOR_BLUE};
                    color: {MaritimeTheme.FOAM_WHITE};
                    border: none;
                    border-radius: 6px;
                    padding: {MaritimeTheme.SPACE_SM}px {MaritimeTheme.SPACE_MD}px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {MaritimeTheme.STEEL_BLUE};
                }}
                QPushButton:pressed {{
                    background-color: #0D47A1;
                }}
                QPushButton:disabled {{
                    background-color: {MaritimeTheme.SLATE_GRAY};
                    color: #B0BEC5;
                }}
            """)
        
        elif self.variant == self.Variant.SECONDARY:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {MaritimeTheme.HARBOR_BLUE};
                    border: 1px solid {MaritimeTheme.HARBOR_BLUE};
                    border-radius: 6px;
                    padding: {MaritimeTheme.SPACE_SM}px {MaritimeTheme.SPACE_MD}px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: rgba(21, 101, 192, 0.08);
                }}
                QPushButton:pressed {{
                    background-color: rgba(21, 101, 192, 0.16);
                }}
                QPushButton:disabled {{
                    border-color: #B0BEC5;
                    color: #B0BEC5;
                }}
            """)
        
        elif self.variant == self.Variant.DANGER:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {MaritimeTheme.CORAL_ALERT};
                    color: {MaritimeTheme.FOAM_WHITE};
                    border: none;
                    border-radius: 6px;
                    padding: {MaritimeTheme.SPACE_SM}px {MaritimeTheme.SPACE_MD}px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: #E64A19;
                }}
                QPushButton:pressed {{
                    background-color: #D84315;
                }}
                QPushButton:disabled {{
                    background-color: {MaritimeTheme.SLATE_GRAY};
                    color: #B0BEC5;
                }}
            """)


class MaritimeProgressBar(QProgressBar):
    """Barre de progression maritime avec animation fluide"""
    
    def __init__(self, parent: Optional[QWidget] = None, 
                 color: str = MaritimeTheme.HARBOR_BLUE):
        super().__init__(parent)
        self.color = color
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configuration de l'interface"""
        self.setObjectName("MaritimeProgressBar")
        self.setMinimumHeight(8)
        self.setMaximumHeight(8)
        self.setTextVisible(False)
    
    def _apply_styles(self):
        """Application des styles maritimes"""
        self.setStyleSheet(f"""
            QProgressBar {{
                background-color: {MaritimeTheme.FROST_LIGHT};
                border: none;
                border-radius: 4px;

            }}
            QProgressBar::chunk {{
                background-color: {self.color};
                border-radius: 4px;
            }}
        """)
    
    def set_color(self, color: str):
        """Changer la couleur de la barre"""
        self.color = color
        self._apply_styles()


# MaritimeGrid supprimé - utiliser maritime_grid.MaritimeGrid à la place
# pour éviter les conflits de layout


# Fonctions utilitaires pour le design system
def create_maritime_spacer(size: int = MaritimeTheme.SPACE_MD, 
                          orientation: Qt.Orientation = Qt.Orientation.Vertical) -> QSpacerItem:
    """Créer un espaceur maritime standardisé"""
    if orientation == Qt.Orientation.Vertical:
        return QSpacerItem(0, size, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    else:
        return QSpacerItem(size, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)


def apply_maritime_font(widget: QWidget, size: int = MaritimeTheme.FONT_BODY, 
                       weight: QFont.Weight = QFont.Weight.Normal):
    """Appliquer la police maritime standardisée"""
    font = QFont()
    font.setFamily("Inter")
    font.setPointSize(size)
    font.setWeight(weight)
    widget.setFont(font)


def create_maritime_layout(spacing: int = MaritimeTheme.SPACE_MD, 
                          margins: tuple = None) -> QVBoxLayout:
    """Créer un layout maritime standardisé"""
    layout = QVBoxLayout()
    layout.setSpacing(spacing)
    
    if margins:
        layout.setContentsMargins(*margins)
    else:
        layout.setContentsMargins(
            MaritimeTheme.SPACE_MD, MaritimeTheme.SPACE_MD,
            MaritimeTheme.SPACE_MD, MaritimeTheme.SPACE_MD
        )
    
    return layout