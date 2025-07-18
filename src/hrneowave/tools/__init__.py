#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outils CLI et utilitaires pour CHNeoWave

Ce module contient les outils en ligne de commande et les utilitaires
pour la configuration et la gestion du système CHNeoWave.
"""

from .lab_config import (
    MediterraneanLabConfigurator,
    LabConfiguration,
    HardwareConfig,
    ProcessingConfig,
    EnvironmentConfig,
    CalibrationConfig,
)

__all__ = [
    "MediterraneanLabConfigurator",
    "LabConfiguration",
    "HardwareConfig",
    "ProcessingConfig",
    "EnvironmentConfig",
    "CalibrationConfig",
]

__version__ = "1.0.0"
