# -*- coding: utf-8 -*-
"""
Module implémentant un gestionnaire de matériel d'acquisition simulé.
"""

import time
import numpy as np
from .daq_handler import DAQHandler

class SimulatedDAQHandler(DAQHandler):
    """Gestionnaire de matériel d'acquisition simulé pour les tests et le développement."""

    def __init__(self, config: dict):
        self._config = config
        self._is_open = False
        self._is_running = False
        self._channels = []
        self._sample_rate = 0
        self._num_samples = 0
        self._start_time = 0

    def open(self) -> bool:
        print("Simulated DAQ: Opening connection...")
        self._is_open = True
        print("Simulated DAQ: Connection opened.")
        return True

    def close(self):
        if not self._is_open:
            return
        print("Simulated DAQ: Closing connection...")
        self._is_open = False
        self._is_running = False
        print("Simulated DAQ: Connection closed.")

    def configure_acquisition(self, sample_rate: int, num_samples_per_channel: int):
        print(f"Simulated DAQ: Configuring acquisition - Sample Rate: {sample_rate}, Samples: {num_samples_per_channel}")
        self._sample_rate = sample_rate
        self._num_samples = num_samples_per_channel

    def configure_channels(self, channels: list):
        print(f"Simulated DAQ: Configuring channels: {channels}")
        self._channels = channels

    def start(self):
        if not self._is_open:
            raise RuntimeError("Simulated DAQ is not open.")
        print("Simulated DAQ: Starting acquisition...")
        self._is_running = True
        self._start_time = time.time()

    def stop(self):
        if not self._is_running:
            return
        print("Simulated DAQ: Stopping acquisition...")
        self._is_running = False

    def read(self) -> np.ndarray:
        if not self._is_running:
            # Retourne un tableau vide si l'acquisition n'est pas en cours
            return np.array([[] for _ in self._channels])

        num_channels = len(self._channels)
        if num_channels == 0:
            return np.array([])

        # Simuler des données sinusoïdales avec un peu de bruit
        elapsed_time = time.time() - self._start_time
        t = elapsed_time + np.arange(self._num_samples) / self._sample_rate
        
        data = np.zeros((num_channels, self._num_samples))
        for i in range(num_channels):
            frequency = 5 + i * 2 # Fréquence différente par canal
            amplitude = 1 + i * 0.1
            noise = np.random.normal(0, 0.1, self._num_samples)
            data[i, :] = amplitude * np.sin(2 * np.pi * frequency * t) + noise
        
        # Simuler le temps que prendrait une lecture réelle
        time.sleep(self._num_samples / self._sample_rate)

        return data

    def get_status(self) -> dict:
        return {
            "is_open": self._is_open,
            "is_running": self._is_running,
            "channels": self._channels,
            "sample_rate": self._sample_rate,
            "num_samples": self._num_samples
        }