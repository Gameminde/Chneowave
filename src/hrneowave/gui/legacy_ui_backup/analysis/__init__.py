# -*- coding: utf-8 -*-
"""
Module d'analyse CHNeoWave - Version refactorisée
Architecture modulaire avec widgets spécialisés
"""

# Import des widgets spécialisés
from .spectral_analysis import SpectralAnalysisWidget
from .goda_analysis import GodaAnalysisWidget
from .statistics_analysis import StatisticsAnalysisWidget
from .summary_report import SummaryReportWidget
from .analysis_controller import AnalysisController
from .analysis_view_v2 import AnalysisViewV2

# Exposition des classes principales
__all__ = [
    'SpectralAnalysisWidget',
    'GodaAnalysisWidget', 
    'StatisticsAnalysisWidget',
    'SummaryReportWidget',
    'AnalysisController',
    'AnalysisViewV2'
]