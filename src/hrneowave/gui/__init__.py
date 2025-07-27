# -*- coding: utf-8 -*-
"""
Module GUI moderne pour CHNeoWave v3.0.0
Architecture MVC avec workflow guidé en 5 étapes
"""

# Import du thème (sans dépendances)
from .styles.theme_manager import ThemeManager as CHNeoWaveTheme

# Les autres imports seront faits à la demande pour éviter les importations circulaires
def get_main_controller():
    from .controllers.main_controller import MainController
    return MainController


def get_views():
    from .views import (
        WelcomeView,
        CalibrationView,
        AcquisitionView,
        AnalysisView,
        ExportView
    )
    return WelcomeView, CalibrationView, AcquisitionView, AnalysisView, ExportView

# Fonctions individuelles pour le ViewManager

def get_calibration_view():
    try:
        from .views.calibration_view import CalibrationView
        return CalibrationView
    except ImportError:
        return None

def get_acquisition_view():
    try:
        from .views.acquisition_view import AcquisitionView
        return AcquisitionView
    except ImportError:
        return None

def get_analysis_view():
    try:
        from .views.analysis_view import AnalysisView
        return AnalysisView
    except ImportError:
        return None

def get_export_view():
    try:
        from .views.export_view import ExportView
        return ExportView
    except ImportError:
        return None

__all__ = [
    # Contrôleurs
    'MainController',
    'AcquisitionController', 
    'OptimizedProcessingWorker',
    
    # Gestionnaire de vues
    'ViewManager',
    'WorkflowStep',
    
    # Vues modernes
    'WelcomeView',
    'CalibrationView',
    'AcquisitionView',
    'AnalysisView',
    'ExportView',
    
    # Thème
    'CHNeoWaveTheme'
]