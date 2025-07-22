# -*- coding: utf-8 -*-
"""
Module des vues CHNeoWave v2.0.0
Flux séquentiel modernisé avec Material Design 3 :
Accueil -> Calibration -> Acquisition -> Analyse -> Export
"""

# Import conditionnel des vues pour éviter les erreurs QApplication
# Les imports seront faits dynamiquement quand nécessaire

# Variables pour le lazy loading
_welcome_view_v2 = None
_calibration_view_v2 = None
_acquisition_view_v2 = None
_analysis_view_v2 = None
_export_view_v2 = None
_settings_view_v2 = None

_welcome_view = None
_calibration_view = None
_acquisition_view = None
_analysis_view = None
_export_view = None

# Fonctions d'accès pour le ViewManager v2 avec lazy loading
def get_welcome_view_v2():
    """Retourne la classe WelcomeViewV2"""
    global _welcome_view_v2
    if _welcome_view_v2 is None:
        from .welcome_view_v2 import WelcomeViewV2
        _welcome_view_v2 = WelcomeViewV2
    return _welcome_view_v2

def get_calibration_view_v2():
    """Retourne la classe CalibrationViewV2"""
    global _calibration_view_v2
    if _calibration_view_v2 is None:
        from .calibration_view_v2 import CalibrationViewV2
        _calibration_view_v2 = CalibrationViewV2
    return _calibration_view_v2

def get_acquisition_view_v2():
    """Retourne la classe AcquisitionViewV2"""
    global _acquisition_view_v2
    if _acquisition_view_v2 is None:
        from .acquisition_view_v2 import AcquisitionViewV2
        _acquisition_view_v2 = AcquisitionViewV2
    return _acquisition_view_v2

def get_analysis_view_v2():
    """Retourne la classe AnalysisViewV2"""
    global _analysis_view_v2
    if _analysis_view_v2 is None:
        from .analysis_view_v2 import AnalysisViewV2
        _analysis_view_v2 = AnalysisViewV2
    return _analysis_view_v2

def get_export_view_v2():
    """Retourne la classe ExportViewV2"""
    global _export_view_v2
    if _export_view_v2 is None:
        from .export_view_v2 import ExportViewV2
        _export_view_v2 = ExportViewV2
    return _export_view_v2

def get_settings_view_v2():
    """Retourne la classe SettingsViewV2"""
    global _settings_view_v2
    if _settings_view_v2 is None:
        from .settings_view_v2 import SettingsViewV2
        _settings_view_v2 = SettingsViewV2
    return _settings_view_v2

# Fonctions d'accès pour le ViewManager v1 (deprecated) avec lazy loading
def get_welcome_view():
    """Retourne la classe WelcomeView (deprecated)"""
    global _welcome_view
    if _welcome_view is None:
        from .welcome_view import WelcomeView
        _welcome_view = WelcomeView
    return _welcome_view

def get_calibration_view():
    """Retourne la classe CalibrationView (deprecated)"""
    global _calibration_view
    if _calibration_view is None:
        from .calibration_view import CalibrationView
        _calibration_view = CalibrationView
    return _calibration_view

def get_acquisition_view():
    """Retourne la classe AcquisitionView (deprecated)"""
    global _acquisition_view
    if _acquisition_view is None:
        from .acquisition_view import AcquisitionView
        _acquisition_view = AcquisitionView
    return _acquisition_view

def get_analysis_view():
    """Retourne la classe AnalysisView (deprecated)"""
    global _analysis_view
    if _analysis_view is None:
        from .analysis_view import AnalysisView
        _analysis_view = AnalysisView
    return _analysis_view

def get_export_view():
    """Retourne la classe ExportView (deprecated)"""
    global _export_view
    if _export_view is None:
        from .export_view import ExportView
        _export_view = ExportView
    return _export_view

__all__ = [
    # Fonctions d'accès pour les vues v2 (recommandées)
    'get_welcome_view_v2',
    'get_calibration_view_v2',
    'get_acquisition_view_v2',
    'get_analysis_view_v2',
    'get_export_view_v2',
    'get_settings_view_v2',
    # Fonctions d'accès pour les vues v1 (deprecated)
    'get_welcome_view',
    'get_calibration_view',
    'get_acquisition_view',
    'get_analysis_view',
    'get_export_view'
]