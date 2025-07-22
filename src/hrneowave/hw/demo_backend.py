#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend de démonstration pour CHNeoWave
Utilisé pour les tests et la validation
"""

import numpy as np
import time
import threading
from typing import Optional, Callable, Any
from threading import Event
import logging

logger = logging.getLogger(__name__)

class DemoBackend:
    """
    Backend de démonstration avec données simulées
    Utilisé pour les tests et la validation du système
    """
    
    def __init__(self):
        self.is_running = False
        self.sample_rate = 100.0
        self.channels = 4
        self.data_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
        self.acquisition_thread: Optional[threading.Thread] = None
        self.stop_event = Event()
        self._sample_count = 0
        self.is_connected = False
        self.amplitude = 1.0
        self.frequency = 0.1  # Hz pour simulation de houle
        self.noise_level = 0.05
    
    def initialize(self, config):
        """
        Initialise le backend avec la configuration donnée
        """
        self.sample_rate = config.get('sample_rate', 100.0)
        self.channels = config.get('channels', 4)
        self.amplitude = config.get('amplitude', 1.0)
        self.frequency = config.get('frequency', 0.1)
        self.noise_level = config.get('noise_level', 0.05)
        self.is_connected = True
        return True
        
    def configure(self, sample_rate: float, channels: int, **kwargs) -> bool:
        """
        Configure le backend de démonstration
        
        Args:
            sample_rate: Fréquence d'échantillonnage en Hz
            channels: Nombre de canaux
            **kwargs: Paramètres additionnels
            
        Returns:
            bool: True si configuration réussie
        """
        if self.is_running:
            logger.warning("Impossible de configurer pendant l'acquisition")
            return False
            
        self.sample_rate = float(sample_rate)
        self.channels = int(channels)
        
        logger.info(f"Backend démo configuré: {self.sample_rate} Hz, {self.channels} canaux")
        return True
        
    def set_data_callback(self, callback: Callable[[np.ndarray, float], None]):
        """
        Définit la fonction de callback pour les données
        
        Args:
            callback: Fonction appelée avec (data, timestamp)
        """
        self.data_callback = callback
        
    def set_error_callback(self, callback: Callable[[str], None]):
        """
        Définit la fonction de callback pour les erreurs
        
        Args:
            callback: Fonction appelée avec le message d'erreur
        """
        self.error_callback = callback
        
    def start_acquisition(self) -> bool:
        """
        Démarre l'acquisition de données simulées
        
        Returns:
            bool: True si démarrage réussi
        """
        if self.is_running:
            logger.warning("Acquisition déjà en cours")
            return False
            
        if not self.data_callback:
            logger.error("Callback de données non défini")
            return False
            
        self.stop_event.clear()
        self.is_running = True
        self._sample_count = 0
        
        self.acquisition_thread = threading.Thread(
            target=self._acquisition_loop,
            name="DemoBackend-Acquisition"
        )
        self.acquisition_thread.start()
        
        logger.info("Acquisition démo démarrée")
        return True
        
    def stop_acquisition(self):
        """
        Arrête l'acquisition
        """
        if not self.is_running:
            return
            
        self.stop_event.set()
        self.is_running = False
        
        if self.acquisition_thread and self.acquisition_thread.is_alive():
            self.acquisition_thread.join(timeout=2.0)
            
        logger.info("Acquisition démo arrêtée")
        
    def _acquisition_loop(self):
        """
        Boucle principale d'acquisition avec génération de données simulées
        """
        samples_per_block = max(1, int(self.sample_rate / 10))  # 10 blocs par seconde
        block_duration = samples_per_block / self.sample_rate
        
        start_time = time.time()
        
        while not self.stop_event.is_set():
            try:
                block_start = time.time()
                
                # Générer des données simulées
                data = self._generate_demo_data(samples_per_block)
                
                # Timestamp relatif au début de l'acquisition
                timestamp = block_start - start_time
                
                # Envoyer les données via callback
                if self.data_callback:
                    self.data_callback(data, timestamp)
                    
                self._sample_count += samples_per_block
                
                # Attendre pour respecter la fréquence d'échantillonnage
                elapsed = time.time() - block_start
                sleep_time = max(0, block_duration - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            except Exception as e:
                logger.error(f"Erreur dans la boucle d'acquisition: {e}")
                if self.error_callback:
                    self.error_callback(f"Erreur acquisition: {e}")
                break
                
    def _generate_demo_data(self, num_samples: int) -> np.ndarray:
        """
        Génère des données de démonstration
        
        Args:
            num_samples: Nombre d'échantillons à générer
            
        Returns:
            np.ndarray: Données simulées (num_samples, channels)
        """
        # Temps pour ce bloc
        t_start = self._sample_count / self.sample_rate
        t = np.linspace(t_start, t_start + num_samples/self.sample_rate, num_samples)
        
        # Générer des signaux différents pour chaque canal
        data = np.zeros((num_samples, self.channels))
        
        for ch in range(self.channels):
            # Fréquence principale différente pour chaque canal
            freq_main = 0.5 + ch * 0.2  # 0.5, 0.7, 0.9, 1.1 Hz
            
            # Signal principal sinusoïdal
            signal = np.sin(2 * np.pi * freq_main * t)
            
            # Ajouter des harmoniques
            signal += 0.3 * np.sin(2 * np.pi * freq_main * 2 * t)
            signal += 0.1 * np.sin(2 * np.pi * freq_main * 3 * t)
            
            # Ajouter du bruit
            noise = np.random.normal(0, 0.05, num_samples)
            signal += noise
            
            # Amplitude différente pour chaque canal
            amplitude = 1.0 + ch * 0.2
            data[:, ch] = signal * amplitude
            
        return data
        
    def has_data(self) -> bool:
        """
        Vérifie si des données ont été acquises
        
        Returns:
            bool: True si des données sont disponibles
        """
        return self._sample_count > 0
        
    def get_status(self) -> dict:
        """
        Retourne le statut du backend
        
        Returns:
            dict: Informations de statut
        """
        return {
            'backend_type': 'demo',
            'is_running': self.is_running,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'samples_acquired': self._sample_count,
            'duration': self._sample_count / self.sample_rate if self.sample_rate > 0 else 0
        }
        
    @staticmethod
    def is_available() -> bool:
        """
        Vérifie si le backend est disponible
        
        Returns:
            bool: Toujours True pour le backend de démonstration
        """
        return True
        
    def __del__(self):
        """
        Destructeur - nettoie les ressources
        """
        if self.is_running:
            self.stop_acquisition()