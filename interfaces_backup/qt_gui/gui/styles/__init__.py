# -*- coding: utf-8 -*-
"""
Module de thème pour CHNeoWave
"""

from .theme import CHNeoWaveTheme

# Fonctions d'accès simplifiées
def get_stylesheet():
    """Retourne la feuille de style CHNeoWave"""
    return CHNeoWaveTheme.get_stylesheet()

def get_dark_stylesheet() -> str:
    """Alias obsolète vers DARK_STYLESHEET pour anciens imports."""
    try:
        from .styles_dark import DARK_STYLESHEET
        return DARK_STYLESHEET
    except ImportError:
        # Fallback vers le thème principal si styles_dark n'existe pas
        return CHNeoWaveTheme.get_stylesheet()

def get_colors():
    """Retourne les couleurs du thème"""
    return {}

def apply_button_style(button):
    """Applique le style aux boutons"""
    pass

def apply_label_style(label):
    """Applique le style aux labels"""
    pass

def apply_widget_style(widget):
    """Applique le style aux widgets"""
    pass

__all__ = ['get_stylesheet', 'get_dark_stylesheet', 'get_colors', 'apply_button_style', 'apply_label_style', 'apply_widget_style', 'CHNeoWaveTheme']