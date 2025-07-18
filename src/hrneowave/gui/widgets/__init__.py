#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widgets personnalisés HRNeoWave
"""

# Import des widgets disponibles
try:
    from .infos_essai_dock import InfosEssaiDock
except ImportError:
    InfosEssaiDock = None

try:
    from .etat_capteurs_dock import EtatCapteursDock, CapteurWidget
except ImportError:
    EtatCapteursDock = None
    CapteurWidget = None

# Export des widgets
__all__ = [
    'InfosEssaiDock',
    'EtatCapteursDock',
    'CapteurWidget',
]