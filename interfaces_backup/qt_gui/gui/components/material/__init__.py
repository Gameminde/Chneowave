#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Components
Module principal pour les composants Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

# Imports des modules spécialisés
from .theme import (
    MaterialColor,
    MaterialElevation,
    MaterialShape,
    MaterialTypography,
    MaterialTheme,
    MaterialAnimations
)

from .buttons import MaterialButton
from .inputs import MaterialTextField
from .cards import MaterialCard
from .chips import MaterialChip
from .progress import MaterialProgressBar
from .navigation import MaterialNavigationRail, MaterialNavigationRailItem
from .feedback import MaterialToast, MaterialSwitch, ToastNotification
from .utils import (
    show_toast,
    apply_material_theme_to_app,
    create_material_palette,
    get_material_color_scheme
)

__version__ = "2.0.0"
__author__ = "Architecte Logiciel en Chef (ALC)"

# Exposition des classes principales
__all__ = [
    # Thème et constantes
    'MaterialColor',
    'MaterialElevation', 
    'MaterialShape',
    'MaterialTypography',
    'MaterialTheme',
    'MaterialAnimations',
    
    # Composants
    'MaterialButton',
    'MaterialTextField',
    'MaterialCard',
    'MaterialChip',
    'MaterialProgressBar',
    'MaterialNavigationRail',
    'MaterialNavigationRailItem',
    'MaterialToast',
    'MaterialSwitch',
    
    # Utilitaires
    'show_toast',
    'apply_material_theme_to_app',
    'create_material_palette',
    'get_material_color_scheme',
    
    # Compatibilité
    'ToastNotification'
]