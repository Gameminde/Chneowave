#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des thèmes pour HRNeoWave
Exporte les fonctions de thème avec alias de rétro-compatibilité
"""

# On importe *localement* pour éviter la boucle d'import.
from importlib import import_module

_styles = import_module("hrneowave.gui.theme.styles")
set_dark_mode = _styles.set_dark_mode
set_light_mode = _styles.set_light_mode
current_theme = _styles.current_theme
register_theme_callback = _styles.register_theme_callback

# Nouvelles fonctions HRNeoWave
apply_skin = _styles.apply_skin
get_current_theme_bool = _styles.get_current_theme
toggle_theme_new = _styles.toggle_theme
get_color = _styles.get_color
apply_widget_class = _styles.apply_widget_class

# Constantes de classes CSS
CLASS_ACCENT = _styles.CLASS_ACCENT
CLASS_LARGE = _styles.CLASS_LARGE
CLASS_TITLE = _styles.CLASS_TITLE
CLASS_SUBTITLE = _styles.CLASS_SUBTITLE
CLASS_PROBE_STATUS = _styles.CLASS_PROBE_STATUS
CLASS_PROBE_OK = _styles.CLASS_PROBE_OK
CLASS_PROBE_WARNING = _styles.CLASS_PROBE_WARNING
CLASS_PROBE_ERROR = _styles.CLASS_PROBE_ERROR
CLASS_VALUE = _styles.CLASS_VALUE

# Nouvelles API unifiées
def apply_theme(app, theme_name="dark"):
    """Applique un thème à l'application
    
    Args:
        app: Instance QApplication
        theme_name: "dark" ou "light"
    """
    if theme_name.lower() == "light":
        set_light_mode(app)
    else:
        set_dark_mode(app)

def toggle_theme(app):
    """Bascule entre thème sombre et clair
    
    Args:
        app: Instance QApplication
    """
    if current_theme() == "dark":
        apply_theme(app, "light")
    else:
        apply_theme(app, "dark")

def get_current_theme():
    """Retourne le thème actuel"""
    return current_theme()

def get_theme_colors(theme=None):
    """Retourne les couleurs du thème actuel"""
    if theme is None:
        theme = current_theme()
    if theme == "dark":
        # Utilise la nouvelle palette HRNeoWave
        return {
            'background': get_color('background'),
            'foreground': get_color('text'),
            'accent': get_color('accent'),
            'success': get_color('success'),
            'warning': get_color('warning'),
            'error': get_color('error')
        }
    else:
        return {
            'background': '#ffffff',
            'foreground': '#000000',
            'accent': '#2980b9',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c'
        }

# Alias de rétro-compatibilité
apply_theme_light = apply_theme  # legacy alias
toggle_dark_light = toggle_theme  # legacy alias

# Exports
__all__ = [
    "apply_theme",
    "toggle_theme", 
    "toggle_dark_light",
    "apply_theme_light",
    "set_dark_mode",
    "set_light_mode",
    "current_theme",
    "get_current_theme",
    "get_theme_colors",
    "register_theme_callback",
    # Nouvelles fonctions HRNeoWave
    "apply_skin",
    "get_current_theme_bool",
    "toggle_theme_new",
    "get_color",
    "apply_widget_class",
    # Constantes CSS
    "CLASS_ACCENT",
    "CLASS_LARGE",
    "CLASS_TITLE",
    "CLASS_SUBTITLE",
    "CLASS_PROBE_STATUS",
    "CLASS_PROBE_OK",
    "CLASS_PROBE_WARNING",
    "CLASS_PROBE_ERROR",
    "CLASS_VALUE"
]