#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaires CHNeoWave

Ce module contient les utilitaires pour la génération de documentation,
le monitoring et les outils de développement pour CHNeoWave.
"""

from .doc_generator import (
    CHNeoWaveDocGenerator,
    ModuleInfo,
    APIDocumentation,
    LabConfiguration,
)

__all__ = [
    "CHNeoWaveDocGenerator",
    "ModuleInfo",
    "APIDocumentation",
    "LabConfiguration",
]

__version__ = "1.0.0"
