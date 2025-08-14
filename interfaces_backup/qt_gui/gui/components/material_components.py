#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Components v2.0
Composants Material Design 3 réutilisables

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import math

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QProgressBar,
    QFrame, QScrollArea, QGroupBox, QSizePolicy,
    QGraphicsDropShadowEffect, QApplication, QToolTip
)
from PySide6.QtCore import (
    Qt, QTimer, Signal, QObject, QPropertyAnimation,
    QEasingCurve, QRect, QPoint, QSize, QParallelAnimationGroup,
    QSequentialAnimationGroup, Property
)
from PySide6.QtGui import (
    QColor, QFont, QPalette, QPainter, QPen, QBrush,
    QLinearGradient, QRadialGradient, QPainterPath,
    QFontMetrics, QPixmap, QIcon
)

logger = logging.getLogger(__name__)

class MaterialColor(Enum):
    """Couleurs Material Design 3"""
    # Couleurs primaires
    PRIMARY = "#6750A4"
    ON_PRIMARY = "#FFFFFF"
    PRIMARY_CONTAINER = "#EADDFF"
    ON_PRIMARY_CONTAINER = "#21005D"
    
    # Couleurs secondaires
    SECONDARY = "#625B71"
    ON_SECONDARY = "#FFFFFF"
    SECONDARY_CONTAINER = "#E8DEF8"
    ON_SECONDARY_CONTAINER = "#1D192B"
    
    # Couleurs tertiaires
    TERTIARY = "#7D5260"
    ON_TERTIARY = "#FFFFFF"
    TERTIARY_CONTAINER = "#FFD8E4"
    ON_TERTIARY_CONTAINER = "#31111D"
    
    # Couleurs d'erreur
    ERROR = "#BA1A1A"
    ON_ERROR = "#FFFFFF"
    ERROR_CONTAINER = "#FFDAD6"
    ON_ERROR_CONTAINER = "#410002"
    
    # Couleurs de surface
    SURFACE = "#FFFBFE"
    ON_SURFACE = "#1C1B1F"
    SURFACE_VARIANT = "#E7E0EC"
    ON_SURFACE_VARIANT = "#49454F"
    
    # Couleurs d'arrière-plan
    BACKGROUND = "#FFFBFE"
    ON_BACKGROUND = "#1C1B1F"
    
    # Couleurs d'outline
    OUTLINE = "#79747E"
    OUTLINE_VARIANT = "#CAC4D0"
    
    # Couleurs spéciales
    SHADOW = "#000000"
    SCRIM = "#000000"
    INVERSE_SURFACE = "#313033"
    INVERSE_ON_SURFACE = "#F4EFF4"
    INVERSE_PRIMARY = "#D0BCFF"

class MaterialElevation(Enum):
    """Niveaux d'élévation Material Design 3"""
    LEVEL_0 = 0
    LEVEL_1 = 1
    LEVEL_2 = 3
    LEVEL_3 = 6
    LEVEL_4 = 8
    LEVEL_5 = 12

class MaterialShape(Enum):
    """Formes Material Design 3"""
    NONE = 0
    EXTRA_SMALL = 4
    SMALL = 8
    MEDIUM = 12
    LARGE = 16
    EXTRA_LARGE = 28
    FULL = 9999  # Complètement arrondi

class MaterialTypography(Enum):
    """Typographie Material Design 3 (famille, taille, poids)"""
    DISPLAY_LARGE = ("Roboto", 57, 400)
    DISPLAY_MEDIUM = ("Roboto", 45, 400)
    DISPLAY_SMALL = ("Roboto", 36, 400)
    
    HEADLINE_LARGE = ("Roboto", 32, 400)
    HEADLINE_MEDIUM = ("Roboto", 28, 400)
    HEADLINE_SMALL = ("Roboto", 24, 400)
    
    TITLE_LARGE = ("Roboto", 22, 400)
    TITLE_MEDIUM = ("Roboto", 16, 500)
    TITLE_SMALL = ("Roboto", 14, 500)
    
    LABEL_LARGE = ("Roboto", 14, 500)
    LABEL_MEDIUM = ("Roboto", 12, 500)
    LABEL_SMALL = ("Roboto", 11, 500)
    
    BODY_LARGE = ("Roboto", 16, 400)
    BODY_MEDIUM = ("Roboto", 14, 400)
    BODY_SMALL = ("Roboto", 12, 400)

@dataclass
class MaterialTheme:
    """Thème Material Design 3"""
    primary: str = MaterialColor.PRIMARY.value
    on_primary: str = MaterialColor.ON_PRIMARY.value
    primary_container: str = MaterialColor.PRIMARY_CONTAINER.value
    on_primary_container: str = MaterialColor.ON_PRIMARY_CONTAINER.value
    
    secondary: str = MaterialColor.SECONDARY.value
    on_secondary: str = MaterialColor.ON_SECONDARY.value
    secondary_container: str = MaterialColor.SECONDARY_CONTAINER.value
    on_secondary_container: str = MaterialColor.ON_SECONDARY_CONTAINER.value
    
    tertiary: str = MaterialColor.TERTIARY.value
    on_tertiary: str = MaterialColor.ON_TERTIARY.value
    tertiary_container: str = MaterialColor.TERTIARY_CONTAINER.value
    on_tertiary_container: str = MaterialColor.ON_TERTIARY_CONTAINER.value
    
    error: str = MaterialColor.ERROR.value
    on_error: str = MaterialColor.ON_ERROR.value
    error_container: str = MaterialColor.ERROR_CONTAINER.value
    on_error_container: str = MaterialColor.ON_ERROR_CONTAINER.value
    
    surface: str = MaterialColor.SURFACE.value
    on_surface: str = MaterialColor.ON_SURFACE.value
    surface_variant: str = MaterialColor.SURFACE_VARIANT.value
    on_surface_variant: str = MaterialColor.ON_SURFACE_VARIANT.value
    
    background: str = MaterialColor.BACKGROUND.value
    on_background: str = MaterialColor.ON_BACKGROUND.value
    
    outline: str = MaterialColor.OUTLINE.value
    outline_variant: str = MaterialColor.OUTLINE_VARIANT.value
    
    # Mode sombre
    is_dark: bool = False
    
    # Instance globale du thème actuel
    _current_theme: Optional['MaterialTheme'] = None
    
    @classmethod
    def get_current_theme(cls) -> 'MaterialTheme':
        """Retourne le thème actuel ou un thème par défaut"""
        if cls._current_theme is None:
            cls._current_theme = cls()
        return cls._current_theme
    
    @classmethod
    def set_current_theme(cls, theme: 'MaterialTheme'):
        """Définit le thème actuel"""
        cls._current_theme = theme
    
    def to_dark_theme(self) -> 'MaterialTheme':
        """Convertit vers un thème sombre"""
        return MaterialTheme(
            primary="#D0BCFF",
            on_primary="#381E72",
            primary_container="#4F378B",
            on_primary_container="#EADDFF",
            
            secondary="#CCC2DC",
            on_secondary="#332D41",
            secondary_container="#4A4458",
            on_secondary_container="#E8DEF8",
            
            tertiary="#EFB8C8",
            on_tertiary="#492532",
            tertiary_container="#633B48",
            on_tertiary_container="#FFD8E4",
            
            error="#FFB4AB",
            on_error="#690005",
            error_container="#93000A",
            on_error_container="#FFDAD6",
            
            surface="#10131C",
            on_surface="#E6E1E5",
            surface_variant="#49454F",
            on_surface_variant="#CAC4D0",
            
            background="#10131C",
            on_background="#E6E1E5",
            
            outline="#938F99",
            outline_variant="#49454F",
            
            is_dark=True
        )

class MaterialAnimations:
    """Animations Material Design 3"""
    
    # Durées d'animation (ms)
    DURATION_SHORT1 = 50
    DURATION_SHORT2 = 100
    DURATION_SHORT3 = 150
    DURATION_SHORT4 = 200
    DURATION_MEDIUM1 = 250
    DURATION_MEDIUM2 = 300
    DURATION_MEDIUM3 = 350
    DURATION_MEDIUM4 = 400
    DURATION_LONG1 = 450
    DURATION_LONG2 = 500
    DURATION_LONG3 = 550
    DURATION_LONG4 = 600
    
    # Courbes d'animation
    EASING_STANDARD = QEasingCurve.Type.OutCubic
    EASING_DECELERATE = QEasingCurve.Type.OutQuart
    EASING_ACCELERATE = QEasingCurve.Type.InQuart
    EASING_ACCELERATE_DECELERATE = QEasingCurve.Type.InOutQuart
    
    @staticmethod
    def create_fade_animation(widget: QWidget, duration: int = DURATION_MEDIUM2, 
                            start_opacity: float = 0.0, end_opacity: float = 1.0) -> QPropertyAnimation:
        """Crée une animation de fondu"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
        return animation
    
    @staticmethod
    def create_scale_animation(widget: QWidget, duration: int = DURATION_MEDIUM2,
                             start_scale: float = 0.8, end_scale: float = 1.0) -> QPropertyAnimation:
        """Crée une animation d'échelle"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        
        # Calculer les géométries de début et de fin
        current_rect = widget.geometry()
        center = current_rect.center()
        
        start_size = QSize(int(current_rect.width() * start_scale), 
                          int(current_rect.height() * start_scale))
        start_rect = QRect(center.x() - start_size.width() // 2,
                          center.y() - start_size.height() // 2,
                          start_size.width(), start_size.height())
        
        animation.setStartValue(start_rect)
        animation.setEndValue(current_rect)
        animation.setEasingCurve(MaterialAnimations.EASING_DECELERATE)
        return animation
    
    @staticmethod
    def create_slide_animation(widget: QWidget, direction: str = "up", 
                             duration: int = DURATION_MEDIUM3, distance: int = 50) -> QPropertyAnimation:
        """Crée une animation de glissement"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        
        current_pos = widget.pos()
        
        if direction == "up":
            start_pos = QPoint(current_pos.x(), current_pos.y() + distance)
        elif direction == "down":
            start_pos = QPoint(current_pos.x(), current_pos.y() - distance)
        elif direction == "left":
            start_pos = QPoint(current_pos.x() + distance, current_pos.y())
        elif direction == "right":
            start_pos = QPoint(current_pos.x() - distance, current_pos.y())
        else:
            start_pos = current_pos
        
        animation.setStartValue(start_pos)
        animation.setEndValue(current_pos)
        animation.setEasingCurve(MaterialAnimations.EASING_DECELERATE)
        return animation

class MaterialCard(QFrame):
    """Carte Material Design 3"""
    
    clicked = Signal()
    
    def __init__(self, parent=None, elevation: MaterialElevation = MaterialElevation.LEVEL_1,
                 shape: MaterialShape = MaterialShape.MEDIUM, clickable: bool = False):
        super().__init__(parent)
        self.elevation = elevation
        self.shape = shape
        self.clickable = clickable
        self.theme = MaterialTheme()
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Configuration du frame
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Ombre portée
        if self.elevation.value > 0:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(self.elevation.value * 2)
            shadow.setOffset(0, self.elevation.value)
            shadow.setColor(QColor(0, 0, 0, 30))
            self.setGraphicsEffect(shadow)
        
        # Curseur pour les cartes cliquables
        if self.clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def apply_theme(self):
        """Applique le thème"""
        border_radius = self.shape.value
        
        style = f"""
        MaterialCard {{
            background-color: {self.theme.surface};
            border: 1px solid {self.theme.outline_variant};
            border-radius: {border_radius}px;
        }}
        MaterialCard:hover {{
            background-color: {self._lighten_color(self.theme.surface, 0.05)};
        }}
        """
        
        if self.clickable:
            style += f"""
            MaterialCard:pressed {{
                background-color: {self._lighten_color(self.theme.surface, 0.1)};
            }}
            """
        
        self.setStyleSheet(style)
    
    def _lighten_color(self, color_hex: str, factor: float) -> str:
        """Éclaircit une couleur"""
        color = QColor(color_hex)
        h, s, l, a = color.getHslF()
        l = min(1.0, l + factor)
        color.setHslF(h, s, l, a)
        return color.name()
    
    def mousePressEvent(self, event):
        """Gestionnaire de clic"""
        if self.clickable and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

class MaterialButton(QPushButton):
    """Bouton Material Design 3"""
    
    class Style(Enum):
        ELEVATED = "elevated"
        FILLED = "filled"
        FILLED_TONAL = "filled_tonal"
        OUTLINED = "outlined"
        TEXT = "text"
    
    def __init__(self, text: str = "", style: Style = Style.FILLED, 
                 icon: Optional[QIcon] = None, parent=None):
        super().__init__(text, parent)
        self.button_style = style
        self.theme = MaterialTheme()
        self.icon_widget = icon
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Configuration de base
        self.setMinimumHeight(40)
        self.setFont(QFont(*MaterialTypography.LABEL_LARGE.value))
        
        if self.icon_widget:
            self.setIcon(self.icon_widget)
            self.setIconSize(QSize(18, 18))
        
        # Curseur
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def apply_theme(self):
        """Applique le thème selon le style"""
        styles = {
            self.Style.ELEVATED: self._get_elevated_style(),
            self.Style.FILLED: self._get_filled_style(),
            self.Style.FILLED_TONAL: self._get_filled_tonal_style(),
            self.Style.OUTLINED: self._get_outlined_style(),
            self.Style.TEXT: self._get_text_style()
        }
        
        self.setStyleSheet(styles.get(self.button_style, self._get_filled_style()))
    
    def _get_elevated_style(self) -> str:
        """Style élevé"""
        return f"""
        MaterialButton {{
            background-color: {self.theme.surface};
            color: {self.theme.primary};
            border: none;
            border-radius: 20px;
            padding: 10px 24px;
        }}
        MaterialButton:hover {{
            background-color: {self._lighten_color(self.theme.surface, 0.05)};
        }}
        MaterialButton:pressed {{
            background-color: {self._lighten_color(self.theme.surface, 0.1)};
        }}
        MaterialButton:disabled {{
            background-color: {self.theme.surface_variant};
            color: {self.theme.on_surface_variant};
        }}
        """
    
    def _get_filled_style(self) -> str:
        """Style rempli"""
        return f"""
        MaterialButton {{
            background-color: {self.theme.primary};
            color: {self.theme.on_primary};
            border: none;
            border-radius: 20px;
            padding: 10px 24px;
        }}
        MaterialButton:hover {{
            background-color: {self._darken_color(self.theme.primary, 0.05)};
        }}
        MaterialButton:pressed {{
            background-color: {self._darken_color(self.theme.primary, 0.1)};
        }}
        MaterialButton:disabled {{
            background-color: {self.theme.surface_variant};
            color: {self.theme.on_surface_variant};
        }}
        """
    
    def _get_filled_tonal_style(self) -> str:
        """Style rempli tonal"""
        return f"""
        MaterialButton {{
            background-color: {self.theme.secondary_container};
            color: {self.theme.on_secondary_container};
            border: none;
            border-radius: 20px;
            padding: 10px 24px;
        }}
        MaterialButton:hover {{
            background-color: {self._darken_color(self.theme.secondary_container, 0.05)};
        }}
        MaterialButton:pressed {{
            background-color: {self._darken_color(self.theme.secondary_container, 0.1)};
        }}
        MaterialButton:disabled {{
            background-color: {self.theme.surface_variant};
            color: {self.theme.on_surface_variant};
        }}
        """
    
    def _get_outlined_style(self) -> str:
        """Style contouré"""
        return f"""
        MaterialButton {{
            background-color: transparent;
            color: {self.theme.primary};
            border: 1px solid {self.theme.outline};
            border-radius: 20px;
            padding: 10px 24px;
        }}
        MaterialButton:hover {{
            background-color: {self.theme.primary}10;
        }}
        MaterialButton:pressed {{
            background-color: {self.theme.primary}20;
        }}
        MaterialButton:disabled {{
            border-color: {self.theme.outline_variant};
            color: {self.theme.on_surface_variant};
        }}
        """
    
    def _get_text_style(self) -> str:
        """Style texte"""
        return f"""
        MaterialButton {{
            background-color: transparent;
            color: {self.theme.primary};
            border: none;
            border-radius: 20px;
            padding: 10px 12px;
        }}
        MaterialButton:hover {{
            background-color: {self.theme.primary}10;
        }}
        MaterialButton:pressed {{
            background-color: {self.theme.primary}20;
        }}
        MaterialButton:disabled {{
            color: {self.theme.on_surface_variant};
        }}
        """
    
    def _lighten_color(self, color_hex: str, factor: float) -> str:
        """Éclaircit une couleur"""
        color = QColor(color_hex)
        h, s, l, a = color.getHslF()
        l = min(1.0, l + factor)
        color.setHslF(h, s, l, a)
        return color.name()
    
    def _darken_color(self, color_hex: str, factor: float) -> str:
        """Assombrit une couleur"""
        color = QColor(color_hex)
        h, s, l, a = color.getHslF()
        l = max(0.0, l - factor)
        color.setHslF(h, s, l, a)
        return color.name()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

class MaterialTextField(QLineEdit):
    """Champ de texte Material Design 3"""
    
    class Style(Enum):
        FILLED = "filled"
        OUTLINED = "outlined"
    
    def __init__(self, placeholder: str = "", style: Style = Style.OUTLINED, 
                 helper_text: str = "", parent=None):
        super().__init__(parent)
        self.field_style = style
        self.helper_text = helper_text
        self.theme = MaterialTheme()
        self.is_error = False
        
        self.setPlaceholderText(placeholder)
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setMinimumHeight(56)
        self.setFont(QFont(*MaterialTypography.BODY_LARGE.value))
        
        # Marges internes
        if self.field_style == self.Style.FILLED:
            self.setContentsMargins(16, 8, 16, 8)
        else:
            self.setContentsMargins(16, 16, 16, 16)
    
    def apply_theme(self):
        """Applique le thème selon le style"""
        if self.field_style == self.Style.FILLED:
            style = self._get_filled_style()
        else:
            style = self._get_outlined_style()
        
        self.setStyleSheet(style)
    
    def _get_filled_style(self) -> str:
        """Style rempli"""
        bg_color = self.theme.error_container if self.is_error else self.theme.surface_variant
        text_color = self.theme.on_error_container if self.is_error else self.theme.on_surface
        
        return f"""
        MaterialTextField {{
            background-color: {bg_color};
            color: {text_color};
            border: none;
            border-bottom: 2px solid {self.theme.outline};
            border-radius: 4px 4px 0px 0px;
            padding: 16px;
        }}
        MaterialTextField:focus {{
            border-bottom: 2px solid {self.theme.primary};
        }}
        MaterialTextField:disabled {{
            background-color: {self.theme.surface_variant};
            color: {self.theme.on_surface_variant};
        }}
        """
    
    def _get_outlined_style(self) -> str:
        """Style contouré"""
        border_color = self.theme.error if self.is_error else self.theme.outline
        text_color = self.theme.on_error_container if self.is_error else self.theme.on_surface
        
        return f"""
        MaterialTextField {{
            background-color: transparent;
            color: {text_color};
            border: 1px solid {border_color};
            border-radius: 4px;
            padding: 16px;
        }}
        MaterialTextField:focus {{
            border: 2px solid {self.theme.primary};
        }}
        MaterialTextField:disabled {{
            border-color: {self.theme.outline_variant};
            color: {self.theme.on_surface_variant};
        }}
        """
    
    def set_error(self, is_error: bool, error_message: str = ""):
        """Définit l'état d'erreur"""
        self.is_error = is_error
        if is_error and error_message:
            self.setToolTip(error_message)
        else:
            self.setToolTip("")
        self.apply_theme()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

class MaterialProgressBar(QProgressBar):
    """Barre de progression Material Design 3"""
    
    class Style(Enum):
        LINEAR = "linear"
        CIRCULAR = "circular"
    
    def __init__(self, style: Style = Style.LINEAR, parent=None):
        super().__init__(parent)
        self.progress_style = style
        self.theme = MaterialTheme()
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        if self.progress_style == self.Style.LINEAR:
            self.setMinimumHeight(4)
            self.setMaximumHeight(4)
        else:
            self.setMinimumSize(48, 48)
            self.setMaximumSize(48, 48)
        
        self.setTextVisible(False)
    
    def apply_theme(self):
        """Applique le thème"""
        if self.progress_style == self.Style.LINEAR:
            style = self._get_linear_style()
        else:
            style = self._get_circular_style()
        
        self.setStyleSheet(style)
    
    def _get_linear_style(self) -> str:
        """Style linéaire"""
        return f"""
        MaterialProgressBar {{
            background-color: {self.theme.surface_variant};
            border: none;
            border-radius: 2px;
        }}
        MaterialProgressBar::chunk {{
            background-color: {self.theme.primary};
            border-radius: 2px;
        }}
        """
    
    def _get_circular_style(self) -> str:
        """Style circulaire"""
        return f"""
        MaterialProgressBar {{
            background-color: transparent;
            border: 3px solid {self.theme.surface_variant};
            border-radius: 24px;
        }}
        MaterialProgressBar::chunk {{
            background-color: {self.theme.primary};
            border-radius: 21px;
        }}
        """
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

class MaterialChip(QPushButton):
    """Chip Material Design 3"""
    
    class Type(Enum):
        ASSIST = "assist"
        FILTER = "filter"
        INPUT = "input"
        SUGGESTION = "suggestion"
    
    def __init__(self, text: str, chip_type: Type = Type.ASSIST, 
                 icon: Optional[QIcon] = None, removable: bool = False, parent=None):
        super().__init__(text, parent)
        self.chip_type = chip_type
        self.removable = removable
        self.theme = MaterialTheme()
        self.is_selected = False
        
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(16, 16))
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setMinimumHeight(32)
        self.setFont(QFont(*MaterialTypography.LABEL_MEDIUM.value))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Gestion de la sélection pour les chips filtre
        if self.chip_type == self.Type.FILTER:
            self.setCheckable(True)
            self.toggled.connect(self._on_toggled)
    
    def _on_toggled(self, checked: bool):
        """Gestionnaire de basculement"""
        self.is_selected = checked
        self.apply_theme()
    
    def apply_theme(self):
        """Applique le thème selon le type"""
        styles = {
            self.Type.ASSIST: self._get_assist_style(),
            self.Type.FILTER: self._get_filter_style(),
            self.Type.INPUT: self._get_input_style(),
            self.Type.SUGGESTION: self._get_suggestion_style()
        }
        
        self.setStyleSheet(styles.get(self.chip_type, self._get_assist_style()))
    
    def _get_assist_style(self) -> str:
        """Style assist"""
        return f"""
        MaterialChip {{
            background-color: transparent;
            color: {self.theme.on_surface};
            border: 1px solid {self.theme.outline};
            border-radius: 8px;
            padding: 6px 16px;
        }}
        MaterialChip:hover {{
            background-color: {self.theme.on_surface}10;
        }}
        MaterialChip:pressed {{
            background-color: {self.theme.on_surface}20;
        }}
        """
    
    def _get_filter_style(self) -> str:
        """Style filter"""
        if self.is_selected:
            bg_color = self.theme.secondary_container
            text_color = self.theme.on_secondary_container
            border_color = "transparent"
        else:
            bg_color = "transparent"
            text_color = self.theme.on_surface_variant
            border_color = self.theme.outline
        
        return f"""
        MaterialChip {{
            background-color: {bg_color};
            color: {text_color};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 6px 16px;
        }}
        MaterialChip:hover {{
            background-color: {self.theme.on_surface}10;
        }}
        """
    
    def _get_input_style(self) -> str:
        """Style input"""
        return f"""
        MaterialChip {{
            background-color: {self.theme.surface_variant};
            color: {self.theme.on_surface_variant};
            border: none;
            border-radius: 8px;
            padding: 6px 16px;
        }}
        MaterialChip:hover {{
            background-color: {self.theme.on_surface}10;
        }}
        """
    
    def _get_suggestion_style(self) -> str:
        """Style suggestion"""
        return f"""
        MaterialChip {{
            background-color: transparent;
            color: {self.theme.on_surface_variant};
            border: 1px solid {self.theme.outline};
            border-radius: 8px;
            padding: 6px 16px;
        }}
        MaterialChip:hover {{
            background-color: {self.theme.surface_variant};
        }}
        """
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

class ToastNotification(QWidget):
    """Notification toast Material Design 3"""
    
    class Type(Enum):
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"
    
    def __init__(self, message: str, notification_type: Type = Type.INFO, 
                 duration: int = 3000, parent=None):
        super().__init__(parent)
        self.message = message
        self.notification_type = notification_type
        self.duration = duration
        self.theme = MaterialTheme()
        
        self.setup_ui()
        self.apply_theme()
        
        # Timer pour auto-fermeture
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.setSingleShot(True)
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Message
        self.message_label = QLabel(self.message)
        self.message_label.setFont(QFont(*MaterialTypography.BODY_MEDIUM.value))
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        # Bouton de fermeture
        self.close_button = MaterialButton("×", MaterialButton.Style.TEXT)
        self.close_button.setMaximumSize(24, 24)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        
        # Taille fixe
        self.setFixedWidth(300)
        self.adjustSize()
    
    def apply_theme(self):
        """Applique le thème selon le type"""
        colors = {
            self.Type.INFO: (self.theme.primary_container, self.theme.on_primary_container),
            self.Type.SUCCESS: ("#4CAF50", "#FFFFFF"),
            self.Type.WARNING: (self.theme.tertiary_container, self.theme.on_tertiary_container),
            self.Type.ERROR: (self.theme.error_container, self.theme.on_error_container)
        }
        
        bg_color, text_color = colors.get(self.notification_type, colors[self.Type.INFO])
        
        style = f"""
        ToastNotification {{
            background-color: {bg_color};
            border-radius: 12px;
        }}
        """
        
        self.setStyleSheet(style)
        self.message_label.setStyleSheet(f"color: {text_color};")
        self.close_button.setStyleSheet(f"color: {text_color}; background: transparent;")
    
    def show_toast(self):
        """Affiche le toast avec animation"""
        # Position en bas à droite de l'écran
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, screen.height() - self.height() - 20)
        
        # Animation d'apparition
        self.setWindowOpacity(0.0)
        self.show()
        
        fade_in = MaterialAnimations.create_fade_animation(self, 
                                                          MaterialAnimations.DURATION_MEDIUM2,
                                                          0.0, 0.95)
        slide_in = MaterialAnimations.create_slide_animation(self, "up", 
                                                           MaterialAnimations.DURATION_MEDIUM2)
        
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(fade_in)
        self.animation_group.addAnimation(slide_in)
        self.animation_group.start()
        
        # Démarrer le timer
        if self.duration > 0:
            self.timer.start(self.duration)
    
    def closeEvent(self, event):
        """Animation de fermeture"""
        fade_out = MaterialAnimations.create_fade_animation(self,
                                                          MaterialAnimations.DURATION_SHORT4,
                                                          0.95, 0.0)
        fade_out.finished.connect(lambda: super(ToastNotification, self).close())
        fade_out.start()
        
        event.ignore()

class MaterialNavigationRail(QWidget):
    """Rail de navigation Material Design 3"""
    
    item_selected = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = MaterialTheme()
        self.items = []
        self.selected_index = -1
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setFixedWidth(80)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 12, 0, 12)
        self.layout.setSpacing(12)
        
        # Bouton FAB (optionnel)
        self.fab_button = None
    
    def add_item(self, icon: QIcon, text: str, badge_count: int = 0):
        """Ajoute un élément au rail"""
        item_widget = self._create_item_widget(icon, text, len(self.items), badge_count)
        self.items.append({
            'widget': item_widget,
            'icon': icon,
            'text': text,
            'badge_count': badge_count
        })
        
        self.layout.addWidget(item_widget)
        
        # Sélectionner le premier élément par défaut
        if len(self.items) == 1:
            self.select_item(0)
    
    def _create_item_widget(self, icon: QIcon, text: str, index: int, badge_count: int) -> QWidget:
        """Crée un widget d'élément"""
        widget = QWidget()
        widget.setFixedSize(56, 56)
        widget.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Gestionnaire de clic
        def on_click():
            self.select_item(index)
        
        widget.mousePressEvent = lambda event: on_click() if event.button() == Qt.MouseButton.LeftButton else None
        
        return widget
    
    def select_item(self, index: int):
        """Sélectionne un élément"""
        if 0 <= index < len(self.items):
            self.selected_index = index
            self._update_selection()
            self.item_selected.emit(index)
    
    def _update_selection(self):
        """Met à jour l'affichage de la sélection"""
        for i, item in enumerate(self.items):
            widget = item['widget']
            if i == self.selected_index:
                # Style sélectionné
                widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.theme.secondary_container};
                    border-radius: 16px;
                }}
                """)
            else:
                # Style normal
                widget.setStyleSheet(f"""
                QWidget {{
                    background-color: transparent;
                    border-radius: 16px;
                }}
                QWidget:hover {{
                    background-color: {self.theme.on_surface}10;
                }}
                """)
    
    def apply_theme(self):
        """Applique le thème"""
        style = f"""
        MaterialNavigationRail {{
            background-color: {self.theme.surface};
            border-right: 1px solid {self.theme.outline_variant};
        }}
        """
        
        self.setStyleSheet(style)
        self._update_selection()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

# Fonctions utilitaires
def create_custom_theme(primary_color: str, secondary_color: str = None, 
                       tertiary_color: str = None, is_dark: bool = False) -> MaterialTheme:
    """Crée un thème personnalisé"""
    theme = MaterialTheme()
    
    if is_dark:
        theme = theme.to_dark_theme()
    
    # Personnalisation des couleurs
    theme.primary = primary_color
    
    if secondary_color:
        theme.secondary = secondary_color
    
    if tertiary_color:
        theme.tertiary = tertiary_color
    
    return theme

class MaterialToast(QWidget):
    """Notification toast Material Design 3"""
    
    class Type(Enum):
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"
    
    def __init__(self, message: str, toast_type: Type = Type.INFO, 
                 duration: int = 3000, parent=None):
        super().__init__(parent)
        self.message = message
        self.toast_type = toast_type
        self.duration = duration
        self.theme = MaterialTheme()
        
        self.setup_ui()
        self.apply_theme()
        
        # Timer pour auto-fermeture
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide)
        
    def setup_ui(self):
        """Configure l'interface"""
        self.setFixedHeight(48)
        self.setMinimumWidth(200)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Message
        self.label = QLabel(self.message)
        layout.addWidget(self.label)
        
        # Bouton fermer
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(24, 24)
        self.close_button.clicked.connect(self.hide)
        layout.addWidget(self.close_button)
        
    def apply_theme(self):
        """Applique le thème"""
        colors = {
            self.Type.INFO: (self.theme.primary, self.theme.on_primary),
            self.Type.SUCCESS: ("#4CAF50", "#FFFFFF"),
            self.Type.WARNING: ("#FF9800", "#FFFFFF"),
            self.Type.ERROR: (self.theme.error, self.theme.on_error)
        }
        
        bg_color, text_color = colors.get(self.toast_type, colors[self.Type.INFO])
        
        style = f"""
        MaterialToast {{
            background-color: {bg_color};
            color: {text_color};
            border-radius: 24px;
        }}
        QPushButton {{
            background-color: transparent;
            color: {text_color};
            border: none;
            font-weight: bold;
        }}
        """
        self.setStyleSheet(style)
        
    def show_toast(self):
        """Affiche le toast"""
        self.show()
        if self.duration > 0:
            self.timer.start(self.duration)
            
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

class MaterialSwitch(QWidget):
    """Switch Material Design 3"""
    
    toggled = Signal(bool)
    
    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self.theme = MaterialTheme()
        
        self.setFixedSize(52, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.apply_theme()
        
    def is_checked(self) -> bool:
        """Retourne l'état du switch"""
        return self._checked
        
    def set_checked(self, checked: bool):
        """Définit l'état du switch"""
        if self._checked != checked:
            self._checked = checked
            self.toggled.emit(checked)
            self.update()
            
    def mousePressEvent(self, event):
        """Gère le clic"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_checked(not self._checked)
            
    def paintEvent(self, event):
        """Dessine le switch"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Couleurs selon l'état
        if self._checked:
            track_color = QColor(self.theme.primary)
            thumb_color = QColor(self.theme.on_primary)
        else:
            track_color = QColor(self.theme.outline)
            thumb_color = QColor(self.theme.outline_variant)
            
        # Track (rail)
        track_rect = QRect(6, 12, 40, 8)
        painter.setBrush(QBrush(track_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(track_rect, 4, 4)
        
        # Thumb (bouton)
        thumb_x = 32 if self._checked else 6
        thumb_rect = QRect(thumb_x, 6, 20, 20)
        painter.setBrush(QBrush(thumb_color))
        painter.drawEllipse(thumb_rect)
        
    def apply_theme(self):
        """Applique le thème"""
        self.update()
        
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()

def show_toast(message: str, toast_type: MaterialToast.Type = MaterialToast.Type.INFO,
              duration: int = 3000, parent=None):
    """Affiche une notification toast"""
    toast = MaterialToast(message, toast_type, duration, parent)
    toast.show_toast()
    return toast

def apply_material_theme_to_app(app: QApplication, theme: MaterialTheme):
    """Applique un thème Material à toute l'application"""
    palette = QPalette()
    
    # Couleurs de base
    palette.setColor(QPalette.ColorRole.Window, QColor(theme.background))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(theme.on_background))
    palette.setColor(QPalette.ColorRole.Base, QColor(theme.surface))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme.surface_variant))
    palette.setColor(QPalette.ColorRole.Text, QColor(theme.on_surface))
    palette.setColor(QPalette.ColorRole.Button, QColor(theme.primary))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme.on_primary))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(theme.primary))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(theme.on_primary))
    
    app.setPalette(palette)
    
    # Style global
    global_style = f"""
    QApplication {{
        font-family: "Roboto", sans-serif;
        font-size: 14px;
    }}
    
    QToolTip {{
        background-color: {theme.surface};
        color: {theme.on_surface};
        border: 1px solid {theme.outline};
        border-radius: 4px;
        padding: 8px;
    }}
    
    QScrollBar:vertical {{
        background-color: {theme.surface_variant};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {theme.outline};
        border-radius: 6px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {theme.on_surface_variant};
    }}
    """
    
    app.setStyleSheet(global_style)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
    
    app = QApplication(sys.argv)
    
    # Test des composants Material
    window = QMainWindow()
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout(central_widget)
    
    # Thème
    theme = MaterialTheme()
    apply_material_theme_to_app(app, theme)
    
    # Test des cartes
    card1 = MaterialCard()
    card1_layout = QVBoxLayout(card1)
    card1_layout.addWidget(QLabel("Carte Material Design 3"))
    layout.addWidget(card1)
    
    # Test des boutons
    button_layout = QHBoxLayout()
    button_layout.addWidget(MaterialButton("Filled", MaterialButton.Style.FILLED))
    button_layout.addWidget(MaterialButton("Outlined", MaterialButton.Style.OUTLINED))
    button_layout.addWidget(MaterialButton("Text", MaterialButton.Style.TEXT))
    layout.addLayout(button_layout)
    
    # Test des champs de texte
    text_field1 = MaterialTextField("Champ outlined", MaterialTextField.Style.OUTLINED)
    text_field2 = MaterialTextField("Champ filled", MaterialTextField.Style.FILLED)
    layout.addWidget(text_field1)
    layout.addWidget(text_field2)
    
    # Test de la barre de progression
    progress = MaterialProgressBar()
    progress.setValue(65)
    layout.addWidget(progress)
    
    # Test des chips
    chip_layout = QHBoxLayout()
    chip_layout.addWidget(MaterialChip("Assist", MaterialChip.Type.ASSIST))
    chip_layout.addWidget(MaterialChip("Filter", MaterialChip.Type.FILTER))
    chip_layout.addWidget(MaterialChip("Input", MaterialChip.Type.INPUT))
    layout.addLayout(chip_layout)
    
    window.setWindowTitle("CHNeoWave - Material Components Test")
    window.resize(600, 400)
    window.show()
    
    # Test du toast
    QTimer.singleShot(1000, lambda: show_toast("Test de notification!", ToastNotification.Type.SUCCESS))
    
    sys.exit(app.exec())