# -*- coding: utf-8 -*-
"""
Widgets Maritimes Standardisés
Design System Maritime 2025 - CHNeoWave

Composants de base pour l'interface maritime :
- MaritimeCard : Conteneur de base avec élévation
- KPIIndicator : Indicateur de métriques
- StatusBeacon : Indicateur d'état avec animation
- MaritimeButton : Boutons standardisés (Primary/Secondary/Outline/Ghost/Danger)
- ProgressStepper : Indicateur de progression par étapes
"""

# Imports des composants maritimes
from .maritime_card import MaritimeCard
from .kpi_indicator import KPIIndicator
from .status_beacon import StatusBeacon
from .maritime_button import (
    MaritimeButton,
    PrimaryButton,
    SecondaryButton,
    OutlineButton,
    GhostButton,
    DangerButton
)
from .progress_stepper import ProgressStepper

# Exports publics
__all__ = [
    'MaritimeCard',
    'KPIIndicator', 
    'StatusBeacon',
    'MaritimeButton',
    'PrimaryButton',
    'SecondaryButton',
    'OutlineButton',
    'GhostButton',
    'DangerButton',
    'ProgressStepper'
]

# Métadonnées du package
__version__ = '1.0.0'
__author__ = 'CHNeoWave Team'
__description__ = 'Design System Maritime 2025 - Widgets standardisés'