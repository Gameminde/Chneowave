#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend NI-DAQmx pour CHNeoWave
Support des cartes National Instruments avec nidaqmx >= 0.6
"""

import logging
import numpy as np
from typing import Optional, List, Dict, Any
from threading import Thread, Event
import time

try:
    import nidaqmx
    from nidaqmx.constants import AcquisitionType, TerminalConfiguration
    from nidaqmx import Task
    NI_AVAILABLE = True
except ImportError:
    NI_AVAILABLE = False
    nidaqmx = None

logger = logging.getLogger(__name__)

class NIDAQmxBackend:
    """
    Backend pour cartes d'acquisition National Instruments
    Support 8/16 voies analogiques, 32/100/500 Hz
    """
    
    SUPPORTED_SAMPLE_RATES = [32, 100, 500]
    MAX_CHANNELS = 16
    
    def __init__(self):
        self.task: Optional[Task] = None
        self.is_running = False
        self.acquisition_thread: Optional[Thread] = None
        self.stop_event = Event()
        self.data_callback = None
        self.error_callback = None
        
        # Configuration par défaut
        self.sample_rate = 32
        self.channels = 8
        self.device_name = "Dev1"  # Nom par défaut NI
        self.terminal_config = TerminalConfiguration.RSE
        self.voltage_range = (-10.0, 10.0)
        
        if not NI_AVAILABLE:
            logger.warning("nidaqmx non disponible - mode simulation activé")
    
    @classmethod
    def is_available(cls) -> bool:
        """Vérifie si le backend NI-DAQmx est disponible"""
        return NI_AVAILABLE
    
    @classmethod
    def detect_devices(cls) -> List[str]:
        """Détecte les périphériques NI disponibles"""
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
    
    def configure(self, sample_rate: int, channels: int, device: str = "Dev1", **kwargs) -> bool:
        """
        Configure le backend
        
        Args:
            sample_rate: Fréquence d'échantillonnage (32, 100, 500 Hz)
            channels: Nombre de canaux (1-16)
            device: Nom du périphérique NI
            **kwargs: Paramètres additionnels
        
        Returns:
            bool: True si configuration réussie
        """
        if sample_rate not in self.SUPPORTED_SAMPLE_RATES:
            logger.error(f"Fréquence non supportée: {sample_rate} Hz")
            return False
        
        if not (1 <= channels <= self.MAX_CHANNELS):
            logger.error(f"Nombre de canaux invalide: {channels}")
            return False
        
        self.sample_rate = sample_rate
        self.channels = channels
        self.device_name = device
        
        # Paramètres optionnels
        self.terminal_config = kwargs.get('terminal_config', TerminalConfiguration.RSE)
        self.voltage_range = kwargs.get('voltage_range', (-10.0, 10.0))
        
        logger.info(f"Configuration NI: {sample_rate} Hz, {channels} canaux, {device}")
        return True
    
    def _create_task(self) -> bool:
        """Crée et configure la tâche DAQmx"""
        if not NI_AVAILABLE:
            return False
        
        try:
            self.task = Task()
            
            # Ajouter les canaux analogiques
            for i in range(self.channels):
                channel_name = f"{self.device_name}/ai{i}"
                self.task.ai_channels.add_ai_voltage_chan(
                    channel_name,
                    terminal_config=self.terminal_config,
                    min_val=self.voltage_range[0],
                    max_val=self.voltage_range[1]
                )
            
            # Configuration du timing
            self.task.timing.cfg_samp_clk_timing(
                rate=self.sample_rate,
                sample_mode=AcquisitionType.CONTINUOUS
            )
            
            logger.info(f"Tâche DAQmx créée: {self.channels} canaux à {self.sample_rate} Hz")
            return True
            
        except Exception as e:
            logger.error(f"Erreur création tâche DAQmx: {e}")
            if self.task:
                self.task.close()
                self.task = None
            return False
    
    def start_acquisition(self, data_callback, error_callback=None) -> bool:
        """
        Démarre l'acquisition continue
        
        Args:
            data_callback: Fonction appelée avec les nouvelles données
            error_callback: Fonction appelée en cas d'erreur
        
        Returns:
            bool: True si démarrage réussi
        """
        if self.is_running:
            logger.warning("Acquisition déjà en cours")
            return False
        
        self.data_callback = data_callback
        self.error_callback = error_callback
        
        if not NI_AVAILABLE:
            # Mode simulation
            logger.info("Démarrage acquisition en mode simulation")
            self._start_simulation()
            return True
        
        if not self._create_task():
            return False
        
        try:
            self.task.start()
            self.stop_event.clear()
            self.is_running = True
            
            # Démarrer le thread d'acquisition
            self.acquisition_thread = Thread(target=self._acquisition_loop, daemon=True)
            self.acquisition_thread.start()
            
            logger.info("Acquisition NI-DAQmx démarrée")
            return True
            
        except Exception as e:
            logger.error(f"Erreur démarrage acquisition: {e}")
            self._cleanup()
            return False
    
    def _acquisition_loop(self):
        """Boucle principale d'acquisition"""
        samples_per_read = max(1, self.sample_rate // 10)  # 100ms de données
        
        while not self.stop_event.is_set():
            try:
                # Lire les données
                data = self.task.read(
                    number_of_samples_per_channel=samples_per_read,
                    timeout=1.0
                )
                
                # Convertir en numpy array
                if self.channels == 1:
                    data_array = np.array([data])
                else:
                    data_array = np.array(data)
                
                # Transposer pour avoir (samples, channels)
                data_array = data_array.T
                
                # Appeler le callback
                if self.data_callback:
                    self.data_callback(data_array)
                
            except Exception as e:
                logger.error(f"Erreur lecture données: {e}")
                if self.error_callback:
                    self.error_callback(e)
                break
    
    def _start_simulation(self):
        """Démarre l'acquisition en mode simulation"""
        self.stop_event.clear()
        self.is_running = True
        
        def simulation_loop():
            samples_per_read = max(1, self.sample_rate // 10)
            t = 0
            
            while not self.stop_event.is_set():
                # Générer des données simulées
                time_array = np.linspace(t, t + samples_per_read/self.sample_rate, samples_per_read)
                
                # Signaux sinusoidaux avec bruit
                data = np.zeros((samples_per_read, self.channels))
                for ch in range(self.channels):
                    freq = 0.1 + ch * 0.05  # Fréquences différentes par canal
                    amplitude = 1.0 + ch * 0.1
                    data[:, ch] = amplitude * np.sin(2 * np.pi * freq * time_array)
                    data[:, ch] += 0.1 * np.random.randn(samples_per_read)  # Bruit
                
                if self.data_callback:
                    self.data_callback(data)
                
                t += samples_per_read / self.sample_rate
                time.sleep(0.1)  # 100ms
        
        self.acquisition_thread = Thread(target=simulation_loop, daemon=True)
        self.acquisition_thread.start()
        
        logger.info(f"Simulation démarrée: {self.channels} canaux à {self.sample_rate} Hz")
    
    def stop_acquisition(self) -> bool:
        """
        Arrête l'acquisition
        
        Returns:
            bool: True si arrêt réussi
        """
        if not self.is_running:
            return True
        
        logger.info("Arrêt acquisition...")
        self.stop_event.set()
        self.is_running = False
        
        # Attendre la fin du thread
        if self.acquisition_thread and self.acquisition_thread.is_alive():
            self.acquisition_thread.join(timeout=2.0)
        
        self._cleanup()
        logger.info("Acquisition arrêtée")
        return True
    
    def _cleanup(self):
        """Nettoie les ressources"""
        if self.task:
            try:
                if self.task._handle is not None:
                    self.task.stop()
                    self.task.close()
            except Exception as e:
                logger.error(f"Erreur nettoyage tâche: {e}")
            finally:
                self.task = None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du backend"""
        return {
            'backend': 'NI-DAQmx',
            'available': NI_AVAILABLE,
            'running': self.is_running,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'device': self.device_name,
            'simulation': not NI_AVAILABLE
        }
    
    def __del__(self):
        """Destructeur - nettoie les ressources"""
        if self.is_running:
            self.stop_acquisition()