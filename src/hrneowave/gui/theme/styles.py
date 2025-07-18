#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de thèmes pour HRNeoWave
Applique les styles sombres/clairs selon les préférences
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPalette, QColor
from .styles_dark import DARK_STYLESHEET, COLORS

# Variables globales pour compatibilité
_current_theme = "dark"
_theme_callbacks = []

def apply_skin(app: QApplication, dark: bool = True):
    """
    Applique le skin HRNeoWave à l'application
    
    Args:
        app: Instance QApplication
        dark: True pour thème sombre, False pour thème clair
    """
    global _current_theme
    
    if dark:
        # Appliquer le thème sombre HRNeoWave
        app.setStyleSheet(DARK_STYLESHEET)
        _current_theme = "dark"
        
        # Sauvegarder la préférence
        settings = QSettings('HRNeoWave', 'CHNeoWave')
        settings.setValue('theme/dark_mode', True)
        
        print("✅ Thème sombre HRNeoWave appliqué")
    else:
        # Thème clair (utilise le style système par défaut)
        app.setStyleSheet("")
        _current_theme = "light"
        
        # Sauvegarder la préférence
        settings = QSettings('HRNeoWave', 'CHNeoWave')
        settings.setValue('theme/dark_mode', False)
        
        print("✅ Thème clair appliqué")
    
    # Notifier les callbacks pour compatibilité
    for cb in _theme_callbacks:
        cb(_current_theme)

def get_current_theme() -> bool:
    """
    Retourne le thème actuel depuis les paramètres
    
    Returns:
        bool: True si thème sombre, False si thème clair
    """
    settings = QSettings('HRNeoWave', 'CHNeoWave')
    return settings.value('theme/dark_mode', True, type=bool)

def toggle_theme(app: QApplication) -> bool:
    """
    Bascule entre thème sombre et clair
    
    Args:
        app: Instance QApplication
        
    Returns:
        bool: Nouvel état du thème (True = sombre)
    """
    current_dark = get_current_theme()
    new_dark = not current_dark
    apply_skin(app, new_dark)
    return new_dark

def get_color(color_name: str) -> str:
    """
    Retourne une couleur de la palette HRNeoWave
    
    Args:
        color_name: Nom de la couleur (ex: 'accent', 'background')
        
    Returns:
        str: Code couleur hexadécimal
    """
    return COLORS.get(color_name, '#FFFFFF')

def apply_widget_class(widget, class_name: str):
    """
    Applique une classe CSS à un widget
    
    Args:
        widget: Widget PyQt5
        class_name: Nom de la classe CSS
    """
    widget.setProperty('class', class_name)
    widget.style().unpolish(widget)
    widget.style().polish(widget)

# === FONCTIONS DE COMPATIBILITÉ ===

def current_theme():
    """Retourne le thème actuel (compatibilité)"""
    return _current_theme

def set_light_mode(app=None):
    """Active le mode clair (compatibilité)"""
    if app is None:
        app = QApplication.instance()
    if app is not None:
        apply_skin(app, dark=False)

def set_dark_mode(app=None):
    """Active le mode sombre (compatibilité)"""
    if app is None:
        app = QApplication.instance()
    if app is not None:
        apply_skin(app, dark=True)

def register_theme_callback(cb):
    """Enregistre un callback de changement de thème (compatibilité)"""
    _theme_callbacks.append(cb)

# Constantes pour les classes CSS
CLASS_ACCENT = 'accent'
CLASS_LARGE = 'large'
CLASS_TITLE = 'title'
CLASS_SUBTITLE = 'subtitle'
CLASS_PROBE_STATUS = 'probe-status'
CLASS_PROBE_OK = 'probe-status-ok'
CLASS_PROBE_WARNING = 'probe-status-warning'
CLASS_PROBE_ERROR = 'probe-status-error'
CLASS_VALUE = 'value'