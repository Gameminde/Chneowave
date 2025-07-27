#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Utilities
Fonctions utilitaires pour Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from typing import Optional
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import QTimer

from .theme import MaterialTheme
from .feedback import MaterialToast


def show_toast(message: str, 
               toast_type: MaterialToast.Type = MaterialToast.Type.INFO,
               duration: int = 3000,
               parent: Optional[QWidget] = None) -> MaterialToast:
    """
    Affiche une notification toast Material Design 3
    
    Args:
        message: Le message à afficher
        toast_type: Le type de toast (INFO, SUCCESS, WARNING, ERROR)
        duration: Durée d'affichage en millisecondes (0 = permanent)
        parent: Widget parent (optionnel)
    
    Returns:
        L'instance du toast créé
    """
    toast = MaterialToast(message, toast_type, duration, parent)
    
    # Positionnement automatique si pas de parent
    if parent is None:
        app = QApplication.instance()
        if app:
            # Centrer sur l'écran principal
            screen = app.primaryScreen().geometry()
            toast_size = toast.sizeHint()
            x = (screen.width() - toast_size.width()) // 2
            y = screen.height() - toast_size.height() - 50  # 50px du bas
            toast.move(x, y)
    else:
        # Centrer sur le parent
        parent_rect = parent.geometry()
        toast_size = toast.sizeHint()
        x = parent_rect.x() + (parent_rect.width() - toast_size.width()) // 2
        y = parent_rect.y() + parent_rect.height() - toast_size.height() - 20
        toast.move(x, y)
    
    toast.show_toast()
    return toast


def apply_material_theme_to_app(app: QApplication, theme: Optional[MaterialTheme] = None):
    """
    Applique un thème Material Design 3 à l'application Qt
    
    Args:
        app: L'instance de QApplication
        theme: Le thème à appliquer (par défaut: thème clair)
    """
    if theme is None:
        theme = MaterialTheme()
    
    # Configuration de la palette globale
    palette = QPalette()
    
    # Couleurs de base
    palette.setColor(QPalette.ColorRole.Window, QColor(theme.surface))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(theme.on_surface))
    palette.setColor(QPalette.ColorRole.Base, QColor(theme.surface_variant))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme.surface_variant))
    palette.setColor(QPalette.ColorRole.Text, QColor(theme.on_surface))
    palette.setColor(QPalette.ColorRole.Button, QColor(theme.surface_variant))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme.on_surface))
    
    # Couleurs de sélection
    palette.setColor(QPalette.ColorRole.Highlight, QColor(theme.primary))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(theme.on_primary))
    
    # Couleurs désactivées
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, 
                    QColor(theme.on_surface_variant))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, 
                    QColor(theme.on_surface_variant))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, 
                    QColor(theme.on_surface_variant))
    
    # Appliquer la palette
    app.setPalette(palette)
    
    # Style global pour les composants Qt standard
    global_style = f"""
    QWidget {{
        font-family: 'Roboto', 'Segoe UI', sans-serif;
        font-size: 14px;
    }}
    
    QMainWindow {{
        background-color: {theme.surface};
        color: {theme.on_surface};
    }}
    
    QMenuBar {{
        background-color: {theme.surface_variant};
        color: {theme.on_surface};
        border-bottom: 1px solid {theme.outline_variant};
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 12px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {theme.surface};
        border-radius: 4px;
    }}
    
    QMenu {{
        background-color: {theme.surface_variant};
        color: {theme.on_surface};
        border: 1px solid {theme.outline_variant};
        border-radius: 8px;
    }}
    
    QMenu::item {{
        padding: 8px 16px;
    }}
    
    QMenu::item:selected {{
        background-color: {theme.surface};
    }}
    
    QToolBar {{
        background-color: {theme.surface_variant};
        border: none;
        spacing: 4px;
    }}
    
    QStatusBar {{
        background-color: {theme.surface_variant};
        color: {theme.on_surface};
        border-top: 1px solid {theme.outline_variant};
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
    
    QScrollBar:horizontal {{
        background-color: {theme.surface_variant};
        height: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {theme.outline};
        border-radius: 6px;
        min-width: 20px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {theme.on_surface_variant};
    }}
    
    QTabWidget::pane {{
        background-color: {theme.surface};
        border: 1px solid {theme.outline_variant};
        border-radius: 8px;
    }}
    
    QTabBar::tab {{
        background-color: {theme.surface_variant};
        color: {theme.on_surface_variant};
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {theme.surface};
        color: {theme.primary};
        border-bottom: 2px solid {theme.primary};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {theme.surface};
    }}
    
    QSplitter::handle {{
        background-color: {theme.outline_variant};
    }}
    
    QSplitter::handle:horizontal {{
        width: 2px;
    }}
    
    QSplitter::handle:vertical {{
        height: 2px;
    }}
    
    QGroupBox {{
        font-weight: 500;
        border: 1px solid {theme.outline_variant};
        border-radius: 8px;
        margin-top: 8px;
        padding-top: 8px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px 0 4px;
        color: {theme.primary};
    }}
    """
    
    app.setStyleSheet(global_style)


def create_material_palette(theme: MaterialTheme) -> QPalette:
    """
    Crée une palette Qt à partir d'un thème Material Design
    
    Args:
        theme: Le thème Material Design
    
    Returns:
        La palette Qt configurée
    """
    palette = QPalette()
    
    # Couleurs de base
    palette.setColor(QPalette.ColorRole.Window, QColor(theme.surface))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(theme.on_surface))
    palette.setColor(QPalette.ColorRole.Base, QColor(theme.surface_variant))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme.surface_variant))
    palette.setColor(QPalette.ColorRole.Text, QColor(theme.on_surface))
    palette.setColor(QPalette.ColorRole.Button, QColor(theme.surface_variant))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme.on_surface))
    
    # Couleurs de sélection
    palette.setColor(QPalette.ColorRole.Highlight, QColor(theme.primary))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(theme.on_primary))
    
    # Couleurs désactivées
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, 
                    QColor(theme.on_surface_variant))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, 
                    QColor(theme.on_surface_variant))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, 
                    QColor(theme.on_surface_variant))
    
    return palette


def get_material_color_scheme(dark_mode: bool = False) -> dict:
    """
    Retourne un schéma de couleurs Material Design 3
    
    Args:
        dark_mode: Si True, retourne le schéma sombre
    
    Returns:
        Dictionnaire avec les couleurs du schéma
    """
    theme = MaterialTheme(dark_mode=dark_mode)
    
    return {
        'primary': theme.primary,
        'on_primary': theme.on_primary,
        'primary_container': theme.primary_container,
        'on_primary_container': theme.on_primary_container,
        'secondary': theme.secondary,
        'on_secondary': theme.on_secondary,
        'secondary_container': theme.secondary_container,
        'on_secondary_container': theme.on_secondary_container,
        'tertiary': theme.tertiary,
        'on_tertiary': theme.on_tertiary,
        'tertiary_container': theme.tertiary_container,
        'on_tertiary_container': theme.on_tertiary_container,
        'error': theme.error,
        'on_error': theme.on_error,
        'error_container': theme.error_container,
        'on_error_container': theme.on_error_container,
        'surface': theme.surface,
        'on_surface': theme.on_surface,
        'surface_variant': theme.surface_variant,
        'on_surface_variant': theme.on_surface_variant,
        'outline': theme.outline,
        'outline_variant': theme.outline_variant,
        'background': theme.background,
        'on_background': theme.on_background
    }