# -*- coding: utf-8 -*-
"""
Module implémentant le gestionnaire de matériel pour NI-DAQmx.
"""

import nidaqmx
import numpy as np
from nidaqmx.task import Task

from .daq_handler import DAQHandler

class NIDAQmxHandler(DAQHandler):
    """Implémentation du DAQHandler pour le matériel NI-DAQmx."""

    def __init__(self, config: dict):
        """Initialise le gestionnaire NI-DAQmx."""
        super().__init__(config)
        self.device_name = config.get('device', 'Dev1')
        self.task: Task = None

    def open(self) -> bool:
        """Ouvre la connexion avec le matériel."""
        try:
            self.task = nidaqmx.Task()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ouverture de la tâche NI-DAQmx: {e}")
            return False

    def close(self):
        """Ferme la connexion avec le matériel."""
        if self.task:
            self.task.close()
            self.task = None

    def configure_acquisition(self, sample_rate: int, num_samples_per_channel: int):
        """Configure les paramètres de l'acquisition."""
        if self.task:
            self.task.timing.cfg_samp_clk_timing(
                rate=sample_rate,
                samps_per_chan=num_samples_per_channel,
                sample_mode=nidaqmx.constants.AcquisitionType.FINITE
            )

    def configure_channels(self, channels: list):
        """Configure les canaux à acquérir."""
        if self.task:
            for channel in channels:
                self.task.ai_channels.add_ai_voltage_chan(
                    f"{self.device_name}/{channel['id']}",
                    min_val=channel.get('min_val', -10.0),
                    max_val=channel.get('max_val', 10.0)
                )

    def start(self):
        """Démarre l'acquisition des données."""
        if self.task:
            self.task.start()

    def stop(self):
        """Arrête l'acquisition des données."""
        if self.task:
            self.task.stop()

    def read(self) -> np.ndarray:
        """Lit les données acquises."""
        if self.task:
            return self.task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)
        return np.array([])

    def get_status(self) -> dict:
        """Retourne l'état actuel du matériel."""
        return {'task_name': self.task.name if self.task else 'N/A'}