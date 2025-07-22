#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaires CHNeoWave

Ce module contient les utilitaires pour la génération de documentation,
le monitoring et les outils de développement pour CHNeoWave.
"""

# Import depuis core au lieu de utils (après nettoyage des doublons)
from ..core.logging_config import setup_logging

__all__ = [
    "setup_logging",
]

__version__ = "1.0.0"
