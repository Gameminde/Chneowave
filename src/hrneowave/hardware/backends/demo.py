# -*- coding: utf-8 -*-
"""
Backend de démonstration pour CHNeoWave.
"""

import logging
import numpy as np
import time
from threading import Thread, Event
from typing import Optional, List, Dict, Any, Callable

from ..base import DAQHandler

logger = logging.getLogger(__name__)

class DemoBackend(DAQHandler):
    """Backend de démonstration avec données simulées."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.config = config
        self.is_running = False
        self.acquisition_thread: Optional[Thread] = None
        self.stop_event = Event()
        self.data_callback: Optional[Callable[[np.ndarray], None]] = None
        self.error_callback: Optional[Callable[[str], None]] = None

        self.sample_rate = self.config.get('sample_rate', 32)
        self.num_channels = self.config.get('channels', 8)
        self.num_samples = self.config.get('num_samples', 1024)
        self.noise_level = self.config.get('noise_level', 0.1)
        self.signal_frequency = self.config.get('signal_frequency', 1.0)

        logger.info("Backend de démonstration initialisé.")

    def open(self) -> bool:
        logger.info("Connexion simulée ouverte.")
        return True

    def close(self):
        logger.info("Connexion simulée fermée.")

    def configure_acquisition(self, sample_rate: int, num_samples_per_channel: int):
        self.sample_rate = sample_rate
        self.num_samples = num_samples_per_channel
        logger.info(f"Acquisition configurée: Fs={sample_rate}Hz, N={num_samples_per_channel} échantillons.")

    def configure_channels(self, channels: list):
        self.num_channels = len(channels)
        logger.info(f"{self.num_channels} canaux configurés.")

    def start(self):
        if self.is_running:
            logger.warning("L'acquisition est déjà en cours.")
            return

        self.is_running = True
        self.stop_event.clear()
        self.acquisition_thread = Thread(target=self._acquisition_loop)
        self.acquisition_thread.start()
        logger.info("Acquisition simulée démarrée.")

    def stop(self):
        if not self.is_running:
            logger.warning("L'acquisition n'est pas en cours.")
            return

        self.stop_event.set()
        if self.acquisition_thread:
            self.acquisition_thread.join()
        self.is_running = False
        logger.info("Acquisition simulée arrêtée.")

    def read(self) -> np.ndarray:
        return self._generate_data()

    def get_status(self) -> dict:
        return {'running': self.is_running}

    def _acquisition_loop(self):
        while not self.stop_event.is_set():
            data = self._generate_data()
            if self.data_callback:
                self.data_callback(data)
            time.sleep(self.num_samples / self.sample_rate)

    def _generate_data(self) -> np.ndarray:
        t = np.linspace(0, self.num_samples / self.sample_rate, self.num_samples, endpoint=False)
        data = np.zeros((self.num_channels, self.num_samples))
        for i in range(self.num_channels):
            # Signal sinusoïdal avec une fréquence et une phase légèrement différentes pour chaque canal
            freq = self.signal_frequency * (1 + i * 0.1)
            phase = np.pi / 4 * i
            signal = np.sin(2 * np.pi * freq * t + phase)
            noise = np.random.normal(0, self.noise_level, self.num_samples)
            data[i, :] = signal + noise
        return data