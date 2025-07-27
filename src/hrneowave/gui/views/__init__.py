# -*- coding: utf-8 -*-
"""CHNeoWave GUI Views - Maritime Theme 2025
Vues principales de l'application avec design maritime et Golden Ratio
Version: 2.0.0
"""

# Import direct des vues principales
from .dashboard_view import DashboardViewMaritime
from .welcome_view import WelcomeView

# Variables pour le lazy loading
_calibration_view = None
_acquisition_view = None
_analysis_view = None
_export_view = None
_settings_view = None

# Fonctions d'accès pour le ViewManager avec lazy loading
def get_calibration_view(parent=None):
    """Retourne une instance de CalibrationView"""
    global _calibration_view
    if _calibration_view is None:
        from .calibration_view import CalibrationView
        _calibration_view = CalibrationView
    return _calibration_view(parent=parent)

def get_acquisition_view(parent=None):
    """Retourne une instance de AcquisitionView"""
    global _acquisition_view
    if _acquisition_view is None:
        from .acquisition_view import AcquisitionView
        _acquisition_view = AcquisitionView
    return _acquisition_view(parent=parent)

def get_analysis_view(parent=None):
    """Retourne une instance de AnalysisView refactorisée"""
    global _analysis_view
    if _analysis_view is None:
        from .analysis_view import AnalysisView
        _analysis_view = AnalysisView
    return _analysis_view(parent=parent)

def get_export_view(parent=None):
    """Retourne une instance de ExportView (utilise ReportView comme substitut)"""
    global _export_view
    if _export_view is None:
        from .report_view import ReportView as ExportView
        _export_view = ExportView
    return _export_view(parent=parent)

def get_settings_view(parent=None):
    """Retourne une instance de SettingsView (utilise ProjectSettingsView comme substitut)"""
    global _settings_view
    if _settings_view is None:
        from .project_settings_view import ProjectSettingsView as SettingsView
        _settings_view = SettingsView
    return _settings_view(parent=parent)

__all__ = [
    'DashboardViewMaritime',
    'WelcomeView',
    # Fonctions d'accès pour les vues
    'get_calibration_view',
    'get_acquisition_view',
    'get_analysis_view',
    'get_export_view',
    'get_settings_view'
]

# Version du module views
__version__ = '2.0.0'

# Configuration des vues
VIEWS_CONFIG = {
    'welcome': {
        'class': 'WelcomeView',
        'title': '👋 Bienvenue',
        'icon': '👋',
        'description': 'Écran d\'accueil et création de projet'
    },
    'dashboard': {
        'class': 'DashboardViewMaritime',
        'title': '🏠 Tableau de Bord',
        'icon': '🏠',
        'description': 'Vue d\'ensemble du système et monitoring'
    },
    'calibration': {
        'class': 'CalibrationView', 
        'title': '⚖️ Calibration',
        'icon': '⚖️',
        'description': 'Calibration unifiée des capteurs',
        'loader': get_calibration_view
    },
    'acquisition': {
        'class': 'AcquisitionView',
        'title': '📊 Acquisition',
        'icon': '📊', 
        'description': 'Acquisition de données en temps réel',
        'loader': get_acquisition_view
    },
    'analysis': {
        'class': 'AnalysisView',
        'title': '🔬 Analyse',
        'icon': '🔬',
        'description': 'Analyse et traitement des données',
        'loader': get_analysis_view
    },
    'export': {
        'class': 'ExportView',
        'title': '📋 Export',
        'icon': '📋',
        'description': 'Export et génération de rapports',
        'loader': get_export_view
    },
    'settings': {
        'class': 'SettingsView',
        'title': '⚙️ Paramètres',
        'icon': '⚙️',
        'description': 'Configuration du système',
        'loader': get_settings_view
    }
}

# Navigation par défaut
DEFAULT_VIEW = 'welcome'

# Ordre de navigation
NAVIGATION_ORDER = [
    'welcome',
    'dashboard',
    'calibration', 
    'acquisition',
    'analysis',
    'export',
    'settings'
]