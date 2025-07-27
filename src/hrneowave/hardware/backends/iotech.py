# -*- coding: utf-8 -*-
"""
Backend IOtech pour CHNeoWave.
"""

import logging
import numpy as np
from typing import List, Dict, Any

from ..base import DAQHandler

logger = logging.getLogger(__name__)

class IOTechBackend(DAQHandler):
    """Backend pour cartes d'acquisition IOtech."""

    def __init__(self, config: dict):
        super().__init__(config)
        logger.warning("Le backend IOtech n'est pas encore implémenté.")

    def open(self) -> bool:
        logger.warning("IOTechBackend.open non implémenté.")
        return False

    def close(self):
        logger.warning("IOTechBackend.close non implémenté.")

    def configure_acquisition(self, sample_rate: int, num_samples_per_channel: int):
        logger.warning("IOTechBackend.configure_acquisition non implémenté.")

    def configure_channels(self, channels: list):
        logger.warning("IOTechBackend.configure_channels non implémenté.")

    def start(self):
        logger.warning("IOTechBackend.start non implémenté.")

    def stop(self):
        logger.warning("IOTechBackend.stop non implémenté.")

    def read(self) -> np.ndarray:
        logger.warning("IOTechBackend.read non implémenté.")
        return np.array([])

    def get_status(self) -> dict:
        logger.warning("IOTechBackend.get_status non implémenté.")
        return {'status': 'non implémenté'}