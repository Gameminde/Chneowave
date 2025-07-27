# -*- coding: utf-8 -*-
"""
Module définissant l'interface abstraite pour les gestionnaires de matériel d'acquisition (DAQ).
"""

from abc import ABC, abstractmethod
import numpy as np

class DAQHandler(ABC):
    """Classe de base abstraite pour les gestionnaires de matériel d'acquisition."""

    @abstractmethod
    def __init__(self, config: dict):
        """Initialise le gestionnaire de matériel avec une configuration donnée."""
        pass

    @abstractmethod
    def open(self) -> bool:
        """Ouvre la connexion avec le matériel et le prépare pour l'acquisition."""
        pass

    @abstractmethod
    def close(self):
        """Ferme la connexion avec le matériel."""
        pass

    @abstractmethod
    def configure_acquisition(self, sample_rate: int, num_samples_per_channel: int):
        """Configure les paramètres de l'acquisition."""
        pass

    @abstractmethod
    def configure_channels(self, channels: list):
        """Configure les canaux à acquérir."""
        pass

    @abstractmethod
    def start(self):
        """Démarre l'acquisition des données."""
        pass

    @abstractmethod
    def stop(self):
        """Arrête l'acquisition des données."""
        pass

    @abstractmethod
    def read(self) -> np.ndarray:
        """Lit les données acquises depuis le buffer du matériel.

        Returns:
            np.ndarray: Un tableau 2D de forme (n_channels, n_samples).
        """
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """Retourne l'état actuel du matériel."""
        pass