#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Migration Material Components
Script de migration pour rediriger les imports vers les nouveaux modules

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

import warnings

# Imports depuis les nouveaux modules
from .material import (
    MaterialColor,
    MaterialElevation,
    MaterialShape,
    MaterialTypography,
    MaterialTheme,
    MaterialAnimations,
    MaterialButton,
    MaterialTextField,
    MaterialCard,
    MaterialChip,
    MaterialProgressBar,
    MaterialNavigationRail,
    MaterialNavigationRailItem,
    MaterialToast,
    MaterialSwitch,
    show_toast,
    apply_material_theme_to_app,
    create_material_palette,
    get_material_color_scheme,
    ToastNotification
)

# Avertissement de dépréciation
warnings.warn(
    "Le module material_components.py est déprécié. "
    "Utilisez les imports depuis hrneowave.gui.components.material à la place.",
    DeprecationWarning,
    stacklevel=2
)

# Exposition des classes pour compatibilité
__all__ = [
    'MaterialColor',
    'MaterialElevation', 
    'MaterialShape',
    'MaterialTypography',
    'MaterialTheme',
    'MaterialAnimations',
    'MaterialButton',
    'MaterialTextField',
    'MaterialCard',
    'MaterialChip',
    'MaterialProgressBar',
    'MaterialNavigationRail',
    'MaterialNavigationRailItem',
    'MaterialToast',
    'MaterialSwitch',
    'show_toast',
    'apply_material_theme_to_app',
    'create_material_palette',
    'get_material_color_scheme',
    'ToastNotification'
]

# Message d'information pour les développeurs
print("[INFO] Material Components: Migration vers les modules spécialisés effectuée.")
print("[INFO] Utilisez 'from hrneowave.gui.components.material import ...' pour les nouveaux imports.")