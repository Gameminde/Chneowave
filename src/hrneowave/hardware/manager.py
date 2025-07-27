# -*- coding: utf-8 -*-
"""
Module de gestion du matériel pour CHNeoWave.

Ce module fournit une classe `HardwareManager` qui agit comme une façade 
pour interagir avec différents backends matériels (NI-DAQmx, IOtech, Démo).
Il charge dynamiquement les backends disponibles et sélectionne celui 
spécifié dans la configuration.
"""

import logging
from typing import Optional, List, Dict, Type

from .base import DAQHandler
from .backends.ni_daqmx import NIDaqmxBackend
from .backends.iotech import IOTechBackend
from .backends.demo import DemoBackend

logger = logging.getLogger(__name__)

# Dictionnaire des backends disponibles
AVAILABLE_BACKENDS: Dict[str, Type[DAQHandler]] = {
    'ni-daqmx': NIDaqmxBackend,
    'iotech': IOTechBackend,
    'demo': DemoBackend,
}

class HardwareManager:
    """Gère la sélection et l'interaction avec le backend matériel."""

    def __init__(self, config: dict):
        """
        Initialise le gestionnaire de matériel.

        Args:
            config (dict): La configuration de l'application, contenant la section 'hardware'.
        """
        self.config = config.get('hardware', {})
        self.backend_name = self.config.get('backend', 'demo')
        self.backend: Optional[DAQHandler] = None

        logger.info(f"Initialisation du HardwareManager avec le backend: {self.backend_name}")
        self._load_backend()

    def _load_backend(self):
        """Charge le backend spécifié dans la configuration."""
        backend_class = AVAILABLE_BACKENDS.get(self.backend_name)

        if backend_class:
            try:
                self.backend = backend_class(self.config.get('settings', {}))
                logger.info(f"Backend '{self.backend_name}' chargé avec succès.")
            except Exception as e:
                logger.error(f"Erreur lors de l'instanciation du backend '{self.backend_name}': {e}")
                self._fallback_to_demo()
        else:
            logger.warning(f"Backend '{self.backend_name}' non trouvé. Fallback sur le backend de démonstration.")
            self._fallback_to_demo()

    def _fallback_to_demo(self):
        """Charge le backend de démonstration en cas d'échec."""
        self.backend_name = 'demo'
        self.backend = DemoBackend(self.config.get('settings', {}))
        logger.info("Backend de démonstration chargé en fallback.")

    def get_backend(self) -> Optional[DAQHandler]:
        """Retourne l'instance du backend actuellement chargé."""
        return self.backend

    @staticmethod
    def list_available_backends() -> List[str]:
        """Retourne la liste des noms des backends disponibles."""
        return list(AVAILABLE_BACKENDS.keys())