#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Theme
Définitions des thèmes, couleurs et constantes Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from enum import Enum
from PySide6.QtCore import QEasingCurve


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
    BACKGROUND = "#FFFBFE"
    ON_BACKGROUND = "#1C1B1F"
    SURFACE = "#FFFBFE"
    ON_SURFACE = "#1C1B1F"
    SURFACE_VARIANT = "#E7E0EC"
    ON_SURFACE_VARIANT = "#49454F"
    
    # Couleurs de contour
    OUTLINE = "#79747E"
    OUTLINE_VARIANT = "#CAC4D0"
    
    # Couleurs spéciales
    INVERSE_SURFACE = "#313033"
    INVERSE_ON_SURFACE = "#F4EFF4"
    INVERSE_PRIMARY = "#D0BCFF"
    SHADOW = "#000000"
    SCRIM = "#000000"
    SURFACE_TINT = "#6750A4"


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
    """Typographie Material Design 3"""
    # Display
    DISPLAY_LARGE = ("Roboto", 57, 700)  # (famille, taille, poids)
    DISPLAY_MEDIUM = ("Roboto", 45, 700)
    DISPLAY_SMALL = ("Roboto", 36, 700)
    
    # Headline
    HEADLINE_LARGE = ("Roboto", 32, 700)
    HEADLINE_MEDIUM = ("Roboto", 28, 700)
    HEADLINE_SMALL = ("Roboto", 24, 700)
    
    # Title
    TITLE_LARGE = ("Roboto", 22, 500)
    TITLE_MEDIUM = ("Roboto", 16, 500)
    TITLE_SMALL = ("Roboto", 14, 500)
    
    # Label
    LABEL_LARGE = ("Roboto", 14, 500)
    LABEL_MEDIUM = ("Roboto", 12, 500)
    LABEL_SMALL = ("Roboto", 11, 500)
    
    # Body
    BODY_LARGE = ("Roboto", 16, 400)
    BODY_MEDIUM = ("Roboto", 14, 400)
    BODY_SMALL = ("Roboto", 12, 400)


class MaterialTheme:
    """Thème Material Design 3"""
    
    # Instance globale du thème actuel
    _current_theme = None
    
    def __init__(self, dark_mode: bool = False):
        self.dark_mode = dark_mode
        
        if dark_mode:
            self._setup_dark_theme()
        else:
            self._setup_light_theme()
    
    @classmethod
    def get_current_theme(cls):
        """Retourne le thème actuel ou un thème par défaut"""
        if cls._current_theme is None:
            cls._current_theme = cls()
        return cls._current_theme
    
    @classmethod
    def set_current_theme(cls, theme):
        """Définit le thème actuel"""
        cls._current_theme = theme
    
    def _setup_light_theme(self):
        """Configure le thème clair"""
        self.primary = MaterialColor.PRIMARY.value
        self.on_primary = MaterialColor.ON_PRIMARY.value
        self.primary_container = MaterialColor.PRIMARY_CONTAINER.value
        self.on_primary_container = MaterialColor.ON_PRIMARY_CONTAINER.value
        
        self.secondary = MaterialColor.SECONDARY.value
        self.on_secondary = MaterialColor.ON_SECONDARY.value
        self.secondary_container = MaterialColor.SECONDARY_CONTAINER.value
        self.on_secondary_container = MaterialColor.ON_SECONDARY_CONTAINER.value
        
        self.tertiary = MaterialColor.TERTIARY.value
        self.on_tertiary = MaterialColor.ON_TERTIARY.value
        self.tertiary_container = MaterialColor.TERTIARY_CONTAINER.value
        self.on_tertiary_container = MaterialColor.ON_TERTIARY_CONTAINER.value
        
        self.error = MaterialColor.ERROR.value
        self.on_error = MaterialColor.ON_ERROR.value
        self.error_container = MaterialColor.ERROR_CONTAINER.value
        self.on_error_container = MaterialColor.ON_ERROR_CONTAINER.value
        
        self.background = MaterialColor.BACKGROUND.value
        self.on_background = MaterialColor.ON_BACKGROUND.value
        self.surface = MaterialColor.SURFACE.value
        self.on_surface = MaterialColor.ON_SURFACE.value
        self.surface_variant = MaterialColor.SURFACE_VARIANT.value
        self.on_surface_variant = MaterialColor.ON_SURFACE_VARIANT.value
        
        self.outline = MaterialColor.OUTLINE.value
        self.outline_variant = MaterialColor.OUTLINE_VARIANT.value
        
        self.inverse_surface = MaterialColor.INVERSE_SURFACE.value
        self.inverse_on_surface = MaterialColor.INVERSE_ON_SURFACE.value
        self.inverse_primary = MaterialColor.INVERSE_PRIMARY.value
        self.shadow = MaterialColor.SHADOW.value
        self.scrim = MaterialColor.SCRIM.value
        self.surface_tint = MaterialColor.SURFACE_TINT.value
    
    def _setup_dark_theme(self):
        """Configure le thème sombre"""
        # Inversion des couleurs pour le mode sombre
        self.primary = "#D0BCFF"
        self.on_primary = "#381E72"
        self.primary_container = "#4F378B"
        self.on_primary_container = "#EADDFF"
        
        self.secondary = "#CCC2DC"
        self.on_secondary = "#332D41"
        self.secondary_container = "#4A4458"
        self.on_secondary_container = "#E8DEF8"
        
        self.tertiary = "#EFB8C8"
        self.on_tertiary = "#492532"
        self.tertiary_container = "#633B48"
        self.on_tertiary_container = "#FFD8E4"
        
        self.error = "#FFB4AB"
        self.on_error = "#690005"
        self.error_container = "#93000A"
        self.on_error_container = "#FFDAD6"
        
        self.background = "#10131C"
        self.on_background = "#E6E1E5"
        self.surface = "#10131C"
        self.on_surface = "#E6E1E5"
        self.surface_variant = "#49454F"
        self.on_surface_variant = "#CAC4D0"
        
        self.outline = "#938F99"
        self.outline_variant = "#49454F"
        
        self.inverse_surface = "#E6E1E5"
        self.inverse_on_surface = "#313033"
        self.inverse_primary = "#6750A4"
        self.shadow = "#000000"
        self.scrim = "#000000"
        self.surface_tint = "#D0BCFF"
    
    def to_dark_theme(self) -> 'MaterialTheme':
        """Convertit vers le thème sombre"""
        return MaterialTheme(dark_mode=True)
    
    def to_light_theme(self) -> 'MaterialTheme':
        """Convertit vers le thème clair"""
        return MaterialTheme(dark_mode=False)


class MaterialAnimations:
    """Animations Material Design 3"""
    
    # Durées d'animation (en millisecondes)
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
    DURATION_EXTRA_LONG1 = 700
    DURATION_EXTRA_LONG2 = 800
    DURATION_EXTRA_LONG3 = 900
    DURATION_EXTRA_LONG4 = 1000
    
    # Courbes d'animation
    EASING_STANDARD = QEasingCurve.Type.OutCubic
    EASING_DECELERATE = QEasingCurve.Type.OutQuart
    EASING_ACCELERATE = QEasingCurve.Type.InQuart
    EASING_ACCELERATE_DECELERATE = QEasingCurve.Type.InOutQuart
    EASING_LINEAR = QEasingCurve.Type.Linear
    
    @staticmethod
    def get_fade_duration() -> int:
        """Durée pour les animations de fondu"""
        return MaterialAnimations.DURATION_SHORT4
    
    @staticmethod
    def get_slide_duration() -> int:
        """Durée pour les animations de glissement"""
        return MaterialAnimations.DURATION_MEDIUM2
    
    @staticmethod
    def get_scale_duration() -> int:
        """Durée pour les animations d'échelle"""
        return MaterialAnimations.DURATION_SHORT3
    
    @staticmethod
    def get_rotation_duration() -> int:
        """Durée pour les animations de rotation"""
        return MaterialAnimations.DURATION_MEDIUM1