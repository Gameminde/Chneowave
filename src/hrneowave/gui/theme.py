from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings

try:
    import pyqtgraph as pg
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False
    print("⚠️ PyQtGraph non disponible pour les thèmes")

current_theme = "dark"
theme_callbacks = []

# Styles CSS centralisés
LIGHT_STYLESHEET = '''
/* Style général */
QWidget {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
    color: #2c3e50;
    background-color: #ecf0f1;
}

/* Titres */
QLabel#titleLabel {
    font-size: 22px;
    font-weight: bold;
    color: #2980b9;
    letter-spacing: 1px;
    padding: 10px;
    margin-bottom: 15px;
    border-bottom: 2px solid #3498db;
}

/* Groupes */
QGroupBox {
    font-weight: bold;
    border: 2px solid #bdc3c7;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #2980b9;
    background-color: #ffffff;
}

/* Boutons */
QPushButton {
    background-color: #3498db;
    border: none;
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #21618c;
}

QPushButton:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
}

/* Champs de saisie */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px;
    background-color: #ffffff;
    selection-background-color: #3498db;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #3498db;
}

/* ComboBox */
QComboBox {
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px;
    background-color: #ffffff;
    min-width: 120px;
}

QComboBox:focus {
    border-color: #3498db;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzJjM2U1MCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
}

/* Barre d'outils */
QToolBar {
    background-color: #34495e;
    border: none;
    spacing: 3px;
    padding: 4px;
}

QToolBar QToolButton {
    background-color: transparent;
    border: none;
    color: #ecf0f1;
    padding: 8px 12px;
    border-radius: 4px;
    font-weight: bold;
}

QToolBar QToolButton:hover {
    background-color: #2c3e50;
}

QToolBar QToolButton:checked {
    background-color: #3498db;
    color: white;
}

/* Barre de statut */
QStatusBar {
    background-color: #34495e;
    color: #ecf0f1;
    border-top: 1px solid #2c3e50;
}

QStatusBar QPushButton {
    background-color: #2980b9;
    margin: 2px;
}

/* Validation des champs */
.field-error {
    border: 2px solid #e74c3c !important;
    background-color: #fdf2f2 !important;
}

.field-valid {
    border: 2px solid #27ae60 !important;
    background-color: #f2fdf2 !important;
}
'''

DARK_STYLESHEET = '''
/* Style général */
QWidget {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
    color: #ecf0f1;
    background-color: #2c3e50;
}

/* Titres */
QLabel#titleLabel {
    font-size: 22px;
    font-weight: bold;
    color: #3498db;
    letter-spacing: 1px;
    padding: 10px;
    margin-bottom: 15px;
    border-bottom: 2px solid #3498db;
}

/* Groupes */
QGroupBox {
    font-weight: bold;
    border: 2px solid #34495e;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: #34495e;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #3498db;
    background-color: #34495e;
}

/* Boutons */
QPushButton {
    background-color: #3498db;
    border: none;
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #21618c;
}

QPushButton:disabled {
    background-color: #7f8c8d;
    color: #bdc3c7;
}

/* Champs de saisie */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    border: 2px solid #34495e;
    border-radius: 4px;
    padding: 6px;
    background-color: #2c3e50;
    color: #ecf0f1;
    selection-background-color: #3498db;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #3498db;
}

/* ComboBox */
QComboBox {
    border: 2px solid #34495e;
    border-radius: 4px;
    padding: 6px;
    background-color: #2c3e50;
    color: #ecf0f1;
    min-width: 120px;
}

QComboBox:focus {
    border-color: #3498db;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iI2VjZjBmMSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
}

QComboBox QAbstractItemView {
    background-color: #34495e;
    color: #ecf0f1;
    selection-background-color: #3498db;
    border: 1px solid #2c3e50;
}

/* Barre d'outils */
QToolBar {
    background-color: #1a252f;
    border: none;
    spacing: 3px;
    padding: 4px;
}

QToolBar QToolButton {
    background-color: transparent;
    border: none;
    color: #ecf0f1;
    padding: 8px 12px;
    border-radius: 4px;
    font-weight: bold;
}

QToolBar QToolButton:hover {
    background-color: #34495e;
}

QToolBar QToolButton:checked {
    background-color: #3498db;
    color: white;
}

/* Barre de statut */
QStatusBar {
    background-color: #1a252f;
    color: #ecf0f1;
    border-top: 1px solid #34495e;
}

QStatusBar QPushButton {
    background-color: #2980b9;
    margin: 2px;
}

/* Validation des champs */
.field-error {
    border: 2px solid #e74c3c !important;
    background-color: #4a2c2c !important;
}

.field-valid {
    border: 2px solid #27ae60 !important;
    background-color: #2c4a2c !important;
}

/* Scrollbars */
QScrollBar:vertical {
    background-color: #34495e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #3498db;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #2980b9;
}

QScrollBar:horizontal {
    background-color: #34495e;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #3498db;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #2980b9;
}
'''

def set_light_mode(app=None):
    """Applique le thème clair avec style Fusion et PyQtGraph"""
    global current_theme
    current_theme = "light"
    
    if app is None:
        app = QApplication.instance()
    if app is None:
        return
    
    # Utiliser le style Fusion pour un rendu moderne
    app.setStyle('Fusion')
    
    # Palette Fusion pour thème clair
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(44, 62, 80))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(44, 62, 80))
    palette.setColor(QPalette.Button, QColor(220, 220, 220))
    palette.setColor(QPalette.ButtonText, QColor(44, 62, 80))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(41, 128, 185))
    palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # États désactivés
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 140, 141))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 140, 141))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 140, 141))
    
    app.setPalette(palette)
    app.setStyleSheet(LIGHT_STYLESHEET)
    
    # Configurer PyQtGraph pour thème clair
    if PYQTGRAPH_AVAILABLE:
        _configure_pyqtgraph_light()
    
    # Sauvegarder le thème
    _save_theme_preference('light')
    
    # Notifier les callbacks
    for cb in theme_callbacks:
        cb("light")

def set_dark_mode(app=None):
    """Applique le thème sombre avec style Fusion et PyQtGraph"""
    global current_theme
    current_theme = "dark"
    
    if app is None:
        app = QApplication.instance()
    if app is None:
        return
    
    # Utiliser le style Fusion pour un rendu moderne
    app.setStyle('Fusion')
    
    # Palette Fusion pour thème sombre
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(44, 62, 80))
    palette.setColor(QPalette.WindowText, QColor(236, 240, 241))
    palette.setColor(QPalette.Base, QColor(52, 73, 94))
    palette.setColor(QPalette.AlternateBase, QColor(44, 62, 80))
    palette.setColor(QPalette.ToolTipBase, QColor(52, 73, 94))
    palette.setColor(QPalette.ToolTipText, QColor(236, 240, 241))
    palette.setColor(QPalette.Text, QColor(236, 240, 241))
    palette.setColor(QPalette.Button, QColor(52, 73, 94))
    palette.setColor(QPalette.ButtonText, QColor(236, 240, 241))
    palette.setColor(QPalette.BrightText, QColor(231, 76, 60))
    palette.setColor(QPalette.Link, QColor(52, 152, 219))
    palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # États désactivés
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 140, 141))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 140, 141))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 140, 141))
    
    app.setPalette(palette)
    app.setStyleSheet(DARK_STYLESHEET)
    
    # Configurer PyQtGraph pour thème sombre
    if PYQTGRAPH_AVAILABLE:
        _configure_pyqtgraph_dark()
    
    # Sauvegarder le thème
    _save_theme_preference('dark')
    
    # Notifier les callbacks
    for cb in theme_callbacks:
        cb("dark")

def _configure_pyqtgraph_light():
    """Configure PyQtGraph pour le thème clair"""
    try:
        # Couleurs pour thème clair
        pg.setConfigOption('background', '#ecf0f1')
        pg.setConfigOption('foreground', '#2c3e50')
        pg.setConfigOptions(
            antialias=True,
            useOpenGL=True,
            leftButtonPan=False
        )
        
        # Style des axes
        pg.setConfigOption('axisColor', '#34495e')
        pg.setConfigOption('gridColor', '#bdc3c7')
        
    except Exception as e:
        print(f"⚠️ Erreur configuration PyQtGraph clair: {e}")

def _configure_pyqtgraph_dark():
    """Configure PyQtGraph pour le thème sombre"""
    try:
        # Couleurs pour thème sombre
        pg.setConfigOption('background', '#2c3e50')
        pg.setConfigOption('foreground', '#ecf0f1')
        pg.setConfigOptions(
            antialias=True,
            useOpenGL=True,
            leftButtonPan=False
        )
        
        # Style des axes
        pg.setConfigOption('axisColor', '#ecf0f1')
        pg.setConfigOption('gridColor', '#34495e')
        
    except Exception as e:
        print(f"⚠️ Erreur configuration PyQtGraph sombre: {e}")

def _save_theme_preference(theme_name: str):
    """Sauvegarde la préférence de thème"""
    try:
        settings = QSettings('CHNeoWave', 'Theme')
        settings.setValue('current_theme', theme_name)
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde thème: {e}")

def load_theme_preference() -> str:
    """Charge la préférence de thème sauvegardée"""
    try:
        settings = QSettings('CHNeoWave', 'Theme')
        return settings.value('current_theme', 'dark')
    except Exception as e:
        print(f"⚠️ Erreur chargement thème: {e}")
        return 'dark'

def toggle_theme(app=None):
    """Bascule entre thème clair et sombre"""
    if current_theme == "dark":
        set_light_mode(app)
    else:
        set_dark_mode(app)

def apply_field_validation_style(widget, is_valid: bool, theme: str = None):
    """Applique le style de validation aux champs"""
    if theme is None:
        theme = current_theme
        
    try:
        if is_valid:
            widget.setProperty('class', 'field-valid')
        else:
            widget.setProperty('class', 'field-error')
            
        # Forcer la mise à jour du style
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        
    except Exception as e:
        print(f"⚠️ Erreur application style validation: {e}")

def get_current_theme() -> str:
    """Retourne le thème actuel"""
    return current_theme

def get_theme_colors(theme: str = None) -> dict:
    """Retourne les couleurs du thème actuel"""
    if theme is None:
        theme = current_theme
        
    if theme == "light":
        return {
            'background': '#ecf0f1',
            'foreground': '#2c3e50',
            'primary': '#3498db',
            'secondary': '#2980b9',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'border': '#bdc3c7'
        }
    else:  # dark
        return {
            'background': '#2c3e50',
            'foreground': '#ecf0f1',
            'primary': '#3498db',
            'secondary': '#2980b9',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'border': '#34495e'
        }

def register_theme_callback(cb):
    """Enregistre un callback pour les changements de thème"""
    theme_callbacks.append(cb)

def unregister_theme_callback(cb):
    """Désenregistre un callback"""
    if cb in theme_callbacks:
        theme_callbacks.remove(cb)