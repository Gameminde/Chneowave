# -*- coding: utf-8 -*-
"""
Module des layouts pour CHNeoWave
Contient les layouts personnalisés basés sur le nombre d'or

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

from .golden_ratio_layout import (
    GoldenRatioLayout,
    GoldenRatioGridLayout,
    create_golden_ratio_sizes,
    create_golden_ratio_spacing
)

__all__ = [
    'GoldenRatioLayout',
    'GoldenRatioGridLayout', 
    'create_golden_ratio_sizes',
    'create_golden_ratio_spacing'
]