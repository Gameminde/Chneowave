#!/usr/bin/env python3
"""
Gestionnaire de thèmes centralisé pour CHNeoWave v1.1.0
Material Design 3 avec support des variables CSS et proportions Fibonacci/φ

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-19
Version: 1.1.0
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from enum import Enum

# Import Qt avec fallback PyQt5/PySide6
try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QObject, Signal, Slot
    from PySide6.QtGui import QPalette, QColor
    QT_BACKEND = "PySide6"
except ImportError:
    try:
        from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPalette, QColor
QT_BACKEND = "PySide6"
    except ImportError:
        raise ImportError("Aucun backend Qt disponible (PySide6 requis)")

class ThemeMode(Enum):
    """Modes de thème disponibles"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"

class ThemeManager(QObject):
    """Gestionnaire centralisé des thèmes Material Design 3"""
    
    # Signaux
    theme_changed = Signal(str)  # Émis quand le thème change
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_mode = ThemeMode.LIGHT
        self._theme_dir = Path(__file__).parent
        self._variables = self._load_variables()
        self._logger = logging.getLogger(__name__)
        
    def _load_variables(self) -> str:
        """Charge les variables CSS depuis variables.qss"""
        variables_file = self._theme_dir / "variables.qss"
        if variables_file.exists():
            try:
                return variables_file.read_text(encoding='utf-8')
            except Exception as e:
                self._logger.warning(f"Erreur lecture variables.qss: {e}")
                return ""
        return ""
    
    def _load_theme_file(self, mode: ThemeMode) -> str:
        """Charge un fichier de thème spécifique"""
        theme_file = self._theme_dir / f"theme_{mode.value}.qss"
        if theme_file.exists():
            try:
                return theme_file.read_text(encoding='utf-8')
            except Exception as e:
                self._logger.error(f"Erreur lecture {theme_file}: {e}")
                return ""
        return ""
    
    def get_theme_stylesheet(self, mode: ThemeMode) -> str:
        """Retourne la feuille de style complète pour le mode donné"""
        theme_content = self._load_theme_file(mode)
        if not theme_content:
            self._logger.warning(f"Thème {mode.value} non trouvé, utilisation du thème par défaut")
            return self._get_fallback_stylesheet()
        
        # Combine variables + thème
        return f"{self._variables}\n\n{theme_content}"
    
    def _get_fallback_stylesheet(self) -> str:
        """Retourne un thème de fallback minimal"""
        return """
        QWidget {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
        }
        
        QPushButton {
            background-color: #1976d2;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        QPushButton:hover {
            background-color: #1565c0;
        }
        """
    
    @Slot()
    def apply_theme(self, app: QApplication, mode: ThemeMode = None) -> bool:
        """Applique le thème à l'application"""
        if mode is None:
            mode = self._current_mode
        
        try:
            stylesheet = self.get_theme_stylesheet(mode)
            app.setStyleSheet(stylesheet)
            
            # Met à jour le mode actuel
            old_mode = self._current_mode
            self._current_mode = mode
            
            # Émet le signal si le mode a changé
            if old_mode != mode:
                self.theme_changed.emit(mode.value)
            
            self._logger.info(f"Thème {mode.value} appliqué avec succès")
            return True
            
        except Exception as e:
            self._logger.error(f"Erreur application thème {mode.value}: {e}")
            return False
    
    def set_theme_mode(self, mode: ThemeMode, app: QApplication = None) -> bool:
        """Change le mode de thème"""
        if app:
            return self.apply_theme(app, mode)
        else:
            self._current_mode = mode
            return True
    
    def get_current_mode(self) -> ThemeMode:
        """Retourne le mode de thème actuel"""
        return self._current_mode
    
    def toggle_theme(self, app: QApplication) -> ThemeMode:
        """Bascule entre thème clair et sombre"""
        new_mode = ThemeMode.DARK if self._current_mode == ThemeMode.LIGHT else ThemeMode.LIGHT
        self.apply_theme(app, new_mode)
        return new_mode
    
    def validate_theme_files(self) -> Dict[str, bool]:
        """Valide la présence des fichiers de thème"""
        files_status = {
            'variables': (self._theme_dir / "variables.qss").exists(),
            'light': (self._theme_dir / "theme_light.qss").exists(),
            'dark': (self._theme_dir / "theme_dark.qss").exists()
        }
        return files_status
    
    def get_theme_info(self) -> Dict[str, Any]:
        """Retourne les informations sur le système de thèmes"""
        validation = self.validate_theme_files()
        return {
            'current_mode': self._current_mode.value,
            'qt_backend': QT_BACKEND,
            'theme_directory': str(self._theme_dir),
            'files_validation': validation,
            'all_files_present': all(validation.values()),
            'available_modes': [mode.value for mode in ThemeMode]
        }
    
    def get_color_palette(self, mode: ThemeMode) -> Dict[str, str]:
        """Retourne la palette de couleurs pour un mode donné"""
        if mode == ThemeMode.LIGHT:
            return {
                'primary': '#1976d2',
                'secondary': '#03dac6',
                'surface': '#fefbff',
                'background': '#fefbff',
                'error': '#ba1a1a',
                'on_primary': '#ffffff',
                'on_secondary': '#000000',
                'on_surface': '#1c1b1f',
                'on_background': '#1c1b1f',
                'on_error': '#ffffff'
            }
        else:  # DARK
            return {
                'primary': '#a8c8ec',
                'secondary': '#4dd0e1',
                'surface': '#10131c',
                'background': '#10131c',
                'error': '#ffb4ab',
                'on_primary': '#003258',
                'on_secondary': '#00363d',
                'on_surface': '#e6e1e5',
                'on_background': '#e6e1e5',
                'on_error': '#690005'
            }

# Instance globale du gestionnaire
_theme_manager_instance: Optional[ThemeManager] = None

def get_theme_manager() -> ThemeManager:
    """Retourne l'instance globale du gestionnaire de thèmes (singleton)"""
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager()
    return _theme_manager_instance

def apply_theme(app: QApplication, mode: ThemeMode = ThemeMode.LIGHT) -> bool:
    """Fonction utilitaire pour appliquer un thème"""
    manager = get_theme_manager()
    return manager.apply_theme(app, mode)

def get_current_theme() -> ThemeMode:
    """Fonction utilitaire pour obtenir le thème actuel"""
    manager = get_theme_manager()
    return manager.get_current_mode()

def toggle_theme(app: QApplication) -> ThemeMode:
    """Fonction utilitaire pour basculer le thème"""
    manager = get_theme_manager()
    return manager.toggle_theme(app)

# Export des classes et fonctions principales
__all__ = [
    'ThemeManager',
    'ThemeMode', 
    'get_theme_manager',
    'apply_theme',
    'get_current_theme',
    'toggle_theme',
    'QT_BACKEND'
]