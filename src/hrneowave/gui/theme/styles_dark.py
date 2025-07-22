#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feuille de style sombre pour CHNeoWave
"""

# Feuille de style sombre moderne pour CHNeoWave
DARK_STYLESHEET = """
/* Style principal pour CHNeoWave - Thème sombre */

/* Fenêtre principale */
QMainWindow {
    background-color: #2b2b2b;
    color: #ffffff;
}

/* Widgets généraux */
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9pt;
}

/* Boutons */
QPushButton {
    background-color: #404040;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px 12px;
    color: #ffffff;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #4a4a4a;
    border-color: #666666;
}

QPushButton:pressed {
    background-color: #353535;
    border-color: #444444;
}

QPushButton:disabled {
    background-color: #2a2a2a;
    color: #666666;
    border-color: #333333;
}

/* Boutons primaires */
QPushButton[class="primary"] {
    background-color: #0078d4;
    border-color: #106ebe;
}

QPushButton[class="primary"]:hover {
    background-color: #106ebe;
    border-color: #005a9e;
}

/* Labels */
QLabel {
    color: #ffffff;
    background-color: transparent;
}

/* Champs de saisie */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 4px;
    color: #ffffff;
    selection-background-color: #0078d4;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #0078d4;
}

/* ComboBox */
QComboBox {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 4px;
    color: #ffffff;
    min-width: 100px;
}

QComboBox:hover {
    border-color: #666666;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iI0ZGRkZGRiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
    width: 12px;
    height: 8px;
}

QComboBox QAbstractItemView {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    selection-background-color: #0078d4;
    color: #ffffff;
}

/* SpinBox */
QSpinBox, QDoubleSpinBox {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 4px;
    color: #ffffff;
}

/* CheckBox et RadioButton */
QCheckBox, QRadioButton {
    color: #ffffff;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 2px;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border: 1px solid #0078d4;
    border-radius: 2px;
}

/* GroupBox */
QGroupBox {
    font-weight: bold;
    border: 1px solid #555555;
    border-radius: 4px;
    margin-top: 8px;
    padding-top: 8px;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px 0 4px;
}

/* TabWidget */
QTabWidget::pane {
    border: 1px solid #555555;
    background-color: #2b2b2b;
}

QTabBar::tab {
    background-color: #404040;
    border: 1px solid #555555;
    padding: 6px 12px;
    margin-right: 2px;
    color: #ffffff;
}

QTabBar::tab:selected {
    background-color: #0078d4;
    border-color: #0078d4;
}

QTabBar::tab:hover:!selected {
    background-color: #4a4a4a;
}

/* Barres de défilement */
QScrollBar:vertical {
    background-color: #2b2b2b;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #666666;
}

QScrollBar:horizontal {
    background-color: #2b2b2b;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #555555;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #666666;
}

/* Menu */
QMenuBar {
    background-color: #2b2b2b;
    color: #ffffff;
    border-bottom: 1px solid #555555;
}

QMenuBar::item {
    padding: 4px 8px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #404040;
}

QMenu {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    color: #ffffff;
}

QMenu::item {
    padding: 4px 20px;
}

QMenu::item:selected {
    background-color: #0078d4;
}

/* Barre d'état */
QStatusBar {
    background-color: #2b2b2b;
    color: #ffffff;
    border-top: 1px solid #555555;
}

/* Barres d'outils */
QToolBar {
    background-color: #2b2b2b;
    border: 1px solid #555555;
    spacing: 2px;
}

QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 3px;
    padding: 4px;
    color: #ffffff;
}

QToolButton:hover {
    background-color: #404040;
    border-color: #555555;
}

QToolButton:pressed {
    background-color: #353535;
}

/* Barres de progression */
QProgressBar {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 4px;
    text-align: center;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

/* Tables */
QTableWidget, QTableView {
    background-color: #2b2b2b;
    alternate-background-color: #353535;
    gridline-color: #555555;
    color: #ffffff;
    selection-background-color: #0078d4;
}

QHeaderView::section {
    background-color: #404040;
    color: #ffffff;
    padding: 4px;
    border: 1px solid #555555;
    font-weight: bold;
}

/* Listes */
QListWidget, QListView {
    background-color: #2b2b2b;
    alternate-background-color: #353535;
    color: #ffffff;
    selection-background-color: #0078d4;
    border: 1px solid #555555;
}

/* Splitter */
QSplitter::handle {
    background-color: #555555;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

/* Dock Widgets */
QDockWidget {
    color: #ffffff;
    titlebar-close-icon: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDRMNCA0TDQgMTJMMTIgMTJMMTIgNFoiIGZpbGw9IiNGRkZGRkYiLz4KPC9zdmc+);
    titlebar-normal-icon: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNEwxMiA0TDEyIDEyTDQgMTJMNCA0WiIgZmlsbD0iI0ZGRkZGRiIvPgo8L3N2Zz4K);
}

QDockWidget::title {
    background-color: #404040;
    padding: 4px;
    text-align: left;
}

/* Tooltips */
QToolTip {
    background-color: #404040;
    color: #ffffff;
    border: 1px solid #555555;
    padding: 4px;
    border-radius: 3px;
}

/* Classes spécifiques CHNeoWave */
.chneowave-header {
    background-color: #1e1e1e;
    color: #ffffff;
    font-size: 12pt;
    font-weight: bold;
    padding: 8px;
    border-bottom: 2px solid #0078d4;
}

.chneowave-status {
    background-color: #404040;
    color: #ffffff;
    padding: 4px 8px;
    border-radius: 3px;
    font-size: 8pt;
}

.chneowave-warning {
    background-color: #ff8c00;
    color: #000000;
    padding: 4px 8px;
    border-radius: 3px;
    font-weight: bold;
}

.chneowave-error {
    background-color: #dc3545;
    color: #ffffff;
    padding: 4px 8px;
    border-radius: 3px;
    font-weight: bold;
}

.chneowave-success {
    background-color: #28a745;
    color: #ffffff;
    padding: 4px 8px;
    border-radius: 3px;
    font-weight: bold;
}
"""

# Couleurs du thème sombre
DARK_COLORS = {
    'background': '#2b2b2b',
    'surface': '#3c3c3c',
    'primary': '#0078d4',
    'secondary': '#404040',
    'text': '#ffffff',
    'text_secondary': '#cccccc',
    'border': '#555555',
    'hover': '#4a4a4a',
    'pressed': '#353535',
    'disabled': '#666666',
    'success': '#28a745',
    'warning': '#ff8c00',
    'error': '#dc3545'
}