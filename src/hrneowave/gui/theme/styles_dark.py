#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Palette de couleurs et styles sombres pour HRNeoWave
Reprend l'ergonomie de l'ancienne interface
"""

# Palette de couleurs HRNeoWave
COLORS = {
    'background': '#202225',
    'surface': '#2F3136', 
    'surface_light': '#36393F',
    'text': '#E0E0E0',
    'text_secondary': '#B9BBBE',
    'accent': '#00B5AD',
    'accent_hover': '#009A93',
    'accent_pressed': '#007A74',
    'success': '#43B581',
    'warning': '#FAA61A',
    'error': '#F04747',
    'border': '#40444B',
    'disabled': '#72767D'
}

# Styles pour les widgets principaux
DARK_STYLESHEET = f"""
/* Application globale */
QApplication {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 9pt;
}}

/* Fenêtre principale */
QMainWindow {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
}}

/* Widgets de base */
QWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    border: none;
}}

/* Boutons */
QPushButton {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: 500;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {COLORS['surface_light']};
    border-color: {COLORS['accent']};
}}

QPushButton:pressed {{
    background-color: {COLORS['accent_pressed']};
}}

QPushButton:disabled {{
    background-color: {COLORS['surface']};
    color: {COLORS['disabled']};
    border-color: {COLORS['disabled']};
}}

/* Boutons d'accent */
QPushButton[class="accent"] {{
    background-color: {COLORS['accent']};
    color: white;
    border: none;
}}

QPushButton[class="accent"]:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton[class="accent"]:pressed {{
    background-color: {COLORS['accent_pressed']};
}}

/* Boutons larges pour acquisition */
QPushButton[class="large"] {{
    min-width: 120px;
    min-height: 48px;
    font-size: 11pt;
    font-weight: bold;
    border-radius: 6px;
}}

/* Champs de saisie */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 6px 8px;
    min-height: 20px;
}}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border-color: {COLORS['accent']};
    background-color: {COLORS['surface_light']};
}}

/* Labels */
QLabel {{
    color: {COLORS['text']};
    background: transparent;
}}

QLabel[class="title"] {{
    font-size: 14pt;
    font-weight: bold;
    color: {COLORS['accent']};
}}

QLabel[class="subtitle"] {{
    font-size: 10pt;
    font-weight: 500;
    color: {COLORS['text_secondary']};
}}

/* GroupBox */
QGroupBox {{
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 8px;
    font-weight: 500;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 8px 0 8px;
    color: {COLORS['accent']};
}}

/* Onglets */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    background-color: {COLORS['background']};
}}

QTabBar::tab {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_secondary']};
    border: 1px solid {COLORS['border']};
    padding: 8px 16px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['accent']};
    color: white;
    border-bottom-color: {COLORS['accent']};
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['surface_light']};
    color: {COLORS['text']};
}}

/* Dock Widgets */
QDockWidget {{
    color: {COLORS['text']};
    background-color: {COLORS['background']};
    border: 1px solid {COLORS['border']};
}}

QDockWidget::title {{
    background-color: {COLORS['surface']};
    color: {COLORS['accent']};
    padding: 8px;
    font-weight: bold;
    border-bottom: 1px solid {COLORS['border']};
}}

/* ToolBar */
QToolBar {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    spacing: 4px;
    padding: 4px;
}}

QToolBar::separator {{
    background-color: {COLORS['border']};
    width: 1px;
    margin: 0 4px;
}}

/* Status Bar */
QStatusBar {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border-top: 1px solid {COLORS['border']};
}}

/* Scrollbars */
QScrollBar:vertical {{
    background-color: {COLORS['surface']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['accent']};
}}

/* Indicateurs d'état des capteurs */
QLabel[class="probe-status"] {{
    border-radius: 8px;
    min-width: 16px;
    min-height: 16px;
    max-width: 16px;
    max-height: 16px;
}}

QLabel[class="probe-status-ok"] {{
    background-color: {COLORS['success']};
}}

QLabel[class="probe-status-warning"] {{
    background-color: {COLORS['warning']};
}}

QLabel[class="probe-status-error"] {{
    background-color: {COLORS['error']};
}}

/* Infos essai dock */
QDockWidget[objectName="InfosEssaiDock"] QLabel {{
    padding: 4px 8px;
    border-bottom: 1px solid {COLORS['border']};
}}

QDockWidget[objectName="InfosEssaiDock"] QLabel[class="value"] {{
    color: {COLORS['accent']};
    font-weight: bold;
}}
"""