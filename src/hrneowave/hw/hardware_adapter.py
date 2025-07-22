#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptateur matériel générique pour CHNeoWave
Interface unifiée pour différents backends d'acquisition
"""

import logging
import numpy as np
from typing import Optional, List, Dict, Any, Callable
from threading import Thread, Event
import time

logger = logging.getLogger(__name__)

# Import des backends disponibles
try:
    from .iotech_backend import IOtechBackend
    IOTECH_AVAILABLE = True
except ImportError:
    IOTECH_AVAILABLE = False
    logger.warning("Backend IOtech non disponible")

try:
    from .ni_daqmx_backend import NIDaqmxBackend
    NI_AVAILABLE = True
except ImportError:
    NI_AVAILABLE = False
    logger.warning("Backend NI-DAQmx non disponible")


class SimulationBackend:
    """
    Backend de simulation pour tests et développement
    """
    
    def __init__(self):
        self.is_running = False
        self.sample_rate = 100
        self.channels = 4
        self.data_callback = None
        self.error_callback = None
        self.acquisition_thread = None
        self.stop_event = Event()
        
    @classmethod
    def is_available(cls) -> bool:
        return True
        
    @classmethod
    def detect_devices(cls) -> List[str]:
        return ["Simulation_Device_0"]
        
    def configure(self, sample_rate: int, channels: int, **kwargs) -> bool:
        """Configure le backend de simulation"""
        self.sample_rate = sample_rate
        self.channels = channels
        logger.info(f"Backend simulation configuré: {sample_rate} Hz, {channels} canaux")
        return True
        
    def start_acquisition(self, data_callback: Callable, error_callback: Optional[Callable] = None) -> bool:
        """Démarre l'acquisition simulée"""
        if self.is_running:
            return False
            
        self.data_callback = data_callback
        self.error_callback = error_callback
        self.stop_event.clear()
        
        self.acquisition_thread = Thread(target=self._simulation_loop, daemon=True)
        self.acquisition_thread.start()
        self.is_running = True
        
        logger.info("Acquisition simulée démarrée")
        return True
        
    def stop_acquisition(self) -> bool:
        """Arrête l'acquisition simulée"""
        if not self.is_running:
            return False
            
        self.stop_event.set()
        if self.acquisition_thread:
            self.acquisition_thread.join(timeout=2.0)
            
        self.is_running = False
        logger.info("Acquisition simulée arrêtée")
        return True
        
    def _simulation_loop(self):
        """Boucle de simulation des données"""
        dt = 1.0 / self.sample_rate
        t = 0.0
        
        while not self.stop_event.is_set():
            # Génération de données simulées (vagues sinusoïdales + bruit)
            data = np.zeros((self.channels, 1))
            
            for ch in range(self.channels):
                # Fréquence différente pour chaque canal
                freq = 0.1 + ch * 0.05  # 0.1 à 0.35 Hz
                amplitude = 0.5 + ch * 0.1  # Amplitude variable
                noise = np.random.normal(0, 0.01)  # Bruit
                
                data[ch, 0] = amplitude * np.sin(2 * np.pi * freq * t) + noise
                
            if self.data_callback:
                try:
                    self.data_callback(data, t)
                except Exception as e:
                    if self.error_callback:
                        self.error_callback(f"Erreur callback: {e}")
                        
            t += dt
            time.sleep(dt)
            
    def cleanup(self):
        """Nettoyage des ressources"""
        self.stop_acquisition()


class HardwareAcquisitionAdapter:
    """
    Adaptateur matériel principal pour CHNeoWave
    Gère automatiquement la sélection du backend approprié
    """
    
    def __init__(self, backend_preference: Optional[str] = None):
        self.backend = None
        self.backend_name = None
        self.is_initialized = False
        self.current_config = {}
        
        # Sélection automatique du backend
        self._select_backend(backend_preference)
        
    def _select_backend(self, preference: Optional[str] = None):
        """Sélectionne le meilleur backend disponible"""
        
        # Si une préférence est spécifiée
        if preference:
            if preference.lower() == 'iotech' and IOTECH_AVAILABLE:
                if IOtechBackend.is_available():
                    self.backend = IOtechBackend()
                    self.backend_name = 'IOtech'
                    logger.info("Backend IOtech sélectionné (préférence)")
                    return
                    
            elif preference.lower() == 'ni' and NI_AVAILABLE:
                if NIDaqmxBackend.is_available():
                    self.backend = NIDaqmxBackend()
                    self.backend_name = 'NI-DAQmx'
                    logger.info("Backend NI-DAQmx sélectionné (préférence)")
                    return
                    
            elif preference.lower() == 'simulation':
                self.backend = SimulationBackend()
                self.backend_name = 'Simulation'
                logger.info("Backend simulation sélectionné (préférence)")
                return
        
        # Sélection automatique par ordre de priorité
        if IOTECH_AVAILABLE and IOtechBackend.is_available():
            self.backend = IOtechBackend()
            self.backend_name = 'IOtech'
            logger.info("Backend IOtech sélectionné automatiquement")
            
        elif NI_AVAILABLE and NIDaqmxBackend.is_available():
            self.backend = NIDaqmxBackend()
            self.backend_name = 'NI-DAQmx'
            logger.info("Backend NI-DAQmx sélectionné automatiquement")
            
        else:
            # Fallback vers simulation
            self.backend = SimulationBackend()
            self.backend_name = 'Simulation'
            logger.warning("Aucun matériel détecté - backend simulation activé")
    
    def get_available_backends(self) -> List[str]:
        """Retourne la liste des backends disponibles"""
        backends = ['Simulation']  # Toujours disponible
        
        if IOTECH_AVAILABLE and IOtechBackend.is_available():
            backends.append('IOtech')
            
        if NI_AVAILABLE and NIDaqmxBackend.is_available():
            backends.append('NI-DAQmx')
            
        return backends
    
    def get_available_devices(self) -> List[str]:
        """Retourne la liste des périphériques disponibles"""
        if not self.backend:
            return []
            
        return self.backend.detect_devices()
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialise l'adaptateur avec la configuration donnée
        
        Args:
            config: Configuration d'acquisition
                - sample_rate: Fréquence d'échantillonnage (Hz)
                - channels: Nombre de canaux
                - device_id: ID du périphérique (optionnel)
                - autres paramètres spécifiques au backend
        
        Returns:
            bool: True si l'initialisation a réussi
        """
        if not self.backend:
            logger.error("Aucun backend disponible")
            return False
            
        try:
            # Configuration par défaut
            default_config = {
                'sample_rate': 100,
                'channels': 4,
                'device_id': 0
            }
            
            # Fusion avec la configuration fournie
            self.current_config = {**default_config, **config}
            
            # Configuration du backend
            success = self.backend.configure(**self.current_config)
            
            if success:
                self.is_initialized = True
                logger.info(f"Adaptateur initialisé avec {self.backend_name}")
                logger.info(f"Configuration: {self.current_config}")
            else:
                logger.error("Échec de la configuration du backend")
                
            return success
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}")
            return False
    
    def start_acquisition(self, data_callback: Callable, error_callback: Optional[Callable] = None) -> bool:
        """
        Démarre l'acquisition de données
        
        Args:
            data_callback: Fonction appelée pour chaque bloc de données
                          Signature: callback(data: np.ndarray, timestamp: float)
            error_callback: Fonction appelée en cas d'erreur (optionnel)
                           Signature: callback(error_message: str)
        
        Returns:
            bool: True si l'acquisition a démarré
        """
        if not self.is_initialized:
            logger.error("Adaptateur non initialisé")
            return False
            
        if not self.backend:
            logger.error("Aucun backend disponible")
            return False
            
        try:
            return self.backend.start_acquisition(data_callback, error_callback)
        except Exception as e:
            logger.error(f"Erreur lors du démarrage de l'acquisition: {e}")
            if error_callback:
                error_callback(f"Erreur démarrage: {e}")
            return False
    
    def stop_acquisition(self) -> bool:
        """
        Arrête l'acquisition de données
        
        Returns:
            bool: True si l'acquisition a été arrêtée
        """
        if not self.backend:
            return False
            
        try:
            return self.backend.stop_acquisition()
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt de l'acquisition: {e}")
            return False
    
    def is_acquiring(self) -> bool:
        """
        Vérifie si l'acquisition est en cours
        
        Returns:
            bool: True si l'acquisition est active
        """
        if not self.backend:
            return False
            
        return getattr(self.backend, 'is_running', False)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut actuel de l'adaptateur
        
        Returns:
            dict: Informations de statut
        """
        return {
            'backend': self.backend_name,
            'initialized': self.is_initialized,
            'acquiring': self.is_acquiring(),
            'config': self.current_config.copy(),
            'available_backends': self.get_available_backends(),
            'available_devices': self.get_available_devices()
        }
    
    def cleanup(self):
        """
        Nettoie les ressources et arrête l'acquisition
        """
        if self.backend:
            try:
                self.backend.cleanup()
                logger.info("Nettoyage de l'adaptateur terminé")
            except Exception as e:
                logger.error(f"Erreur lors du nettoyage: {e}")
        
        self.is_initialized = False


# Fonction utilitaire pour créer un adaptateur
def create_hardware_adapter(backend_preference: Optional[str] = None) -> HardwareAcquisitionAdapter:
    """
    Crée et retourne un adaptateur matériel
    
    Args:
        backend_preference: Backend préféré ('iotech', 'ni', 'simulation')
    
    Returns:
        HardwareAcquisitionAdapter: Instance de l'adaptateur
    """
    return HardwareAcquisitionAdapter(backend_preference)


if __name__ == "__main__":
    # Test de l'adaptateur
    logging.basicConfig(level=logging.INFO)
    
    adapter = create_hardware_adapter()
    print(f"Backend sélectionné: {adapter.backend_name}")
    print(f"Backends disponibles: {adapter.get_available_backends()}")
    print(f"Périphériques disponibles: {adapter.get_available_devices()}")
    
    # Test d'initialisation
    config = {
        'sample_rate': 100,
        'channels': 4
    }
    
    if adapter.initialize(config):
        print("Initialisation réussie")
        print(f"Statut: {adapter.get_status()}")
    else:
        print("Échec de l'initialisation")
    
    adapter.cleanup()