# -*- coding: utf-8 -*-
"""
Thème CHNeoWave - En cours de reconstruction
"""

class CHNeoWaveTheme:
    """
    Thème CHNeoWave - Interface en reconstruction
    """
    
    @classmethod
    def get_stylesheet(cls):
        """
        Feuille de style CHNeoWave - Thème sombre professionnel
        """
        # Import des classes Qt seulement quand nécessaire
        from PySide6.QtGui import QPalette, QColor
        from PySide6.QtWidgets import QApplication
        
        return """
        /* Thème CHNeoWave - Laboratoire Maritime */
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
        }
        
        QWidget {
            background-color: #2d2d2d;
            color: #ffffff;
            border: none;
        }
        
        QStackedWidget {
            background-color: #2d2d2d;
            border: 1px solid #404040;
        }
        
        QLabel {
            color: #ffffff;
            background-color: transparent;
        }
        
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #106ebe;
        }
        
        QPushButton:pressed {
            background-color: #005a9e;
        }
        
        QLineEdit {
            background-color: #404040;
            color: #ffffff;
            border: 1px solid #606060;
            padding: 6px;
            border-radius: 3px;
        }
        
        QLineEdit:focus {
            border: 2px solid #0078d4;
        }
        
        QComboBox {
            background-color: #404040;
            color: #ffffff;
            border: 1px solid #606060;
            padding: 6px;
            border-radius: 3px;
        }
        
        QGroupBox {
            color: #ffffff;
            border: 2px solid #606060;
            border-radius: 5px;
            margin-top: 10px;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """