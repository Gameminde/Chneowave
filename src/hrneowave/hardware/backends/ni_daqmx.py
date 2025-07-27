# -*- coding: utf-8 -*-
"""
Backend NI-DAQmx pour CHNeoWave
"""

import logging
import numpy as np
from typing import Optional, List, Dict, Any, Callable
from threading import Thread, Event
import time

from ..base import DAQHandler

try:
    import nidaqmx
    from nidaqmx.constants import AcquisitionType, TerminalConfiguration
    from nidaqmx import Task
    NI_AVAILABLE = True
except ImportError:
    NI_AVAILABLE = False
    nidaqmx = None

logger = logging.getLogger(__name__)

class NIDaqmxBackend(DAQHandler):
    """Backend pour cartes d'acquisition National Instruments"""

    SUPPORTED_SAMPLE_RATES = [32, 100, 500]
    MAX_CHANNELS = 16

    def __init__(self, config: dict):
        super().__init__(config)
        self.config = config
        self.task: Optional[Task] = None
        self.is_running = False
        self.acquisition_thread: Optional[Thread] = None
        self.stop_event = Event()
        self.data_callback = None
        self.error_callback = None

        self.sample_rate = self.config.get('sample_rate', 32)
        self.channels = self.config.get('channels', 8)
        self.device_name = self.config.get('device', 'Dev1')
        self.terminal_config = self.config.get('terminal_config', TerminalConfiguration.RSE)
        self.voltage_range = self.config.get('voltage_range', (-10.0, 10.0))

        if not NI_AVAILABLE:
            logger.warning("nidaqmx non disponible - mode simulation activé")

    @classmethod
    def is_available(cls) -> bool:
        return NI_AVAILABLE

    @classmethod
    def detect_devices(cls) -> List[str]:
        if not NI_AVAILABLE:
            return []
        try:
            system = nidaqmx.system.System.local()
            devices = [device.name for device in system.devices]
            logger.info(f"Périphériques NI détectés: {devices}")
            return devices
        except Exception as e:
            logger.error(f"Erreur détection périphériques NI: {e}")
            return []

    def open(self) -> bool:
        if not NI_AVAILABLE:
            return False
        try:
            self.task = nidaqmx.Task()
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture de la tâche NI-DAQmx: {e}")
            return False

    def close(self):
        if self.task:
            self.task.close()
            self.task = None

    def configure_acquisition(self, sample_rate: int, num_samples_per_channel: int):
        if self.task:
            self.task.timing.cfg_samp_clk_timing(
                rate=sample_rate,
                samps_per_chan=num_samples_per_channel,
                sample_mode=nidaqmx.constants.AcquisitionType.FINITE
            )

    def configure_channels(self, channels: list):
        if self.task:
            for channel in channels:
                self.task.ai_channels.add_ai_voltage_chan(
                    f"{self.device_name}/{channel['id']}",
                    min_val=channel.get('min_val', -10.0),
                    max_val=channel.get('max_val', 10.0)
                )

    def start(self):
        if self.task:
            self.task.start()

    def stop(self):
        if self.task:
            self.task.stop()

    def read(self) -> np.ndarray:
        if self.task:
            return self.task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)
        return np.array([])

    def get_status(self) -> dict:
        return {'task_name': self.task.name if self.task else 'N/A'}