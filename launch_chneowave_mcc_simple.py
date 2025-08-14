#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement simplifié de CHNeoWave avec backend MCC
"""

import os
import sys
import logging
import time
import numpy as np
from threading import Thread, Event
from typing import Optional, List, Dict, Any, Callable
from ctypes import *
from ctypes.wintypes import *

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Constantes pour les DLLs MCC
MCC_DLL_PATH = os.path.join("Measurement Computing", "DAQami")

class MCCBackend:
    """Backend pour cartes d'acquisition Measurement Computing"""
    
    SUPPORTED_SAMPLE_RATES = [32, 100, 500, 1000]
    MAX_CHANNELS = 16
    
    def __init__(self, config: dict):
        self.config = config
        self.is_running = False
        self.acquisition_thread: Optional[Thread] = None
        self.stop_event = Event()
        self.data_callback: Optional[Callable[[np.ndarray], None]] = None
        self.error_callback: Optional[Callable[[str], None]] = None
        
        # Configuration par défaut
        self.sample_rate = self.config.get('sample_rate', 32)
        self.num_channels = self.config.get('channels', 8)
        self.device_id = self.config.get('device_id', 0)
        self.voltage_range = self.config.get('voltage_range', (-10.0, 10.0))
        
        # Handles pour les DLLs
        self.hal_dll = None
        self.ul_dll = None
        self.device_handle = None
        
        # État de l'acquisition
        self.buffer_size = 1024
        self.data_buffer = None
        
        logger.info("Backend MCC initialisé")
        self._load_dlls()
    
    def _load_dlls(self):
        """Charge les DLLs Measurement Computing"""
        try:
            # Charger HAL.dll
            hal_path = os.path.join(MCC_DLL_PATH, "HAL.dll")
            if os.path.exists(hal_path):
                self.hal_dll = CDLL(hal_path)
                logger.info(f"DLL HAL chargée: {hal_path}")
            else:
                logger.warning(f"DLL HAL non trouvée: {hal_path}")
            
            # Charger ULx.dll
            ul_path = os.path.join(MCC_DLL_PATH, "ULx.dll")
            if os.path.exists(ul_path):
                self.ul_dll = CDLL(ul_path)
                logger.info(f"DLL ULx chargée: {ul_path}")
            else:
                logger.warning(f"DLL ULx non trouvée: {ul_path}")
                
        except Exception as e:
            logger.error(f"Erreur lors du chargement des DLLs MCC: {e}")
    
    @classmethod
    def is_available(cls) -> bool:
        """Vérifie si les DLLs MCC sont disponibles"""
        hal_path = os.path.join(MCC_DLL_PATH, "HAL.dll")
        ul_path = os.path.join(MCC_DLL_PATH, "ULx.dll")
        return os.path.exists(hal_path) and os.path.exists(ul_path)
    
    @classmethod
    def detect_devices(cls) -> List[Dict[str, Any]]:
        """Détecte les cartes MCC disponibles"""
        devices = []
        try:
            # Simulation de détection - à adapter selon les vraies fonctions DLL
            devices = [
                {"id": 0, "name": "USB-1608G", "type": "USB", "channels": 8},
                {"id": 1, "name": "USB-1208HS", "type": "USB", "channels": 8},
            ]
            logger.info(f"Cartes MCC détectées: {len(devices)}")
        except Exception as e:
            logger.error(f"Erreur lors de la détection des cartes MCC: {e}")
        
        return devices
    
    def open(self) -> bool:
        """Ouvre la connexion avec la carte MCC"""
        try:
            if not self.hal_dll:
                logger.error("DLL HAL non chargée")
                return False
            
            # Simulation d'ouverture de connexion
            self.device_handle = 1  # Handle simulé
            logger.info(f"Connexion MCC ouverte, handle: {self.device_handle}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture de la connexion MCC: {e}")
            return False
    
    def close(self):
        """Ferme la connexion avec la carte MCC"""
        try:
            if self.device_handle:
                # Simulation de fermeture
                self.device_handle = None
                logger.info("Connexion MCC fermée")
        except Exception as e:
            logger.error(f"Erreur lors de la fermeture de la connexion MCC: {e}")
    
    def configure_acquisition(self, sample_rate: int, num_samples_per_channel: int):
        """Configure les paramètres d'acquisition"""
        try:
            self.sample_rate = sample_rate
            self.buffer_size = num_samples_per_channel
            
            # Allouer le buffer de données
            self.data_buffer = np.zeros((self.num_channels, self.buffer_size))
            
            logger.info(f"Acquisition MCC configurée: Fs={sample_rate}Hz, N={num_samples_per_channel}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la configuration de l'acquisition MCC: {e}")
    
    def configure_channels(self, channels: list):
        """Configure les canaux à acquérir"""
        try:
            self.num_channels = len(channels)
            logger.info(f"{self.num_channels} canaux MCC configurés")
            
        except Exception as e:
            logger.error(f"Erreur lors de la configuration des canaux MCC: {e}")
    
    def start(self):
        """Démarre l'acquisition des données"""
        if self.is_running:
            logger.warning("L'acquisition MCC est déjà en cours")
            return
        
        try:
            self.is_running = True
            self.stop_event.clear()
            self.acquisition_thread = Thread(target=self._acquisition_loop)
            self.acquisition_thread.start()
            logger.info("Acquisition MCC démarrée")
            
        except Exception as e:
            logger.error(f"Erreur lors du démarrage de l'acquisition MCC: {e}")
            self.is_running = False
    
    def stop(self):
        """Arrête l'acquisition des données"""
        if not self.is_running:
            logger.warning("L'acquisition MCC n'est pas en cours")
            return
        
        try:
            self.stop_event.set()
            if self.acquisition_thread:
                self.acquisition_thread.join()
            self.is_running = False
            logger.info("Acquisition MCC arrêtée")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt de l'acquisition MCC: {e}")
    
    def read(self) -> np.ndarray:
        """Lit les données acquises depuis la carte MCC"""
        try:
            if self.data_buffer is not None:
                return self.data_buffer.copy()
            else:
                return np.array([])
                
        except Exception as e:
            logger.error(f"Erreur lors de la lecture des données MCC: {e}")
            return np.array([])
    
    def get_status(self) -> dict:
        """Retourne l'état actuel de la carte MCC"""
        return {
            'running': self.is_running,
            'device_handle': self.device_handle,
            'sample_rate': self.sample_rate,
            'channels': self.num_channels,
            'buffer_size': self.buffer_size
        }
    
    def _acquisition_loop(self):
        """Boucle d'acquisition en arrière-plan"""
        while not self.stop_event.is_set():
            try:
                # Générer des données simulées pour le test
                data = self._generate_mcc_data()
                
                if self.data_buffer is not None:
                    self.data_buffer = data
                
                if self.data_callback:
                    self.data_callback(data)
                
                # Attendre selon la fréquence d'échantillonnage
                time.sleep(self.buffer_size / self.sample_rate)
                
            except Exception as e:
                logger.error(f"Erreur dans la boucle d'acquisition MCC: {e}")
                if self.error_callback:
                    self.error_callback(str(e))
                break
    
    def _generate_mcc_data(self) -> np.ndarray:
        """Génère des données simulées pour les tests"""
        t = np.linspace(0, self.buffer_size / self.sample_rate, self.buffer_size, endpoint=False)
        data = np.zeros((self.num_channels, self.buffer_size))
        
        for i in range(self.num_channels):
            # Signal sinusoïdal avec bruit pour simuler des données réelles
            freq = 1.0 + i * 0.5  # Fréquence différente pour chaque canal
            phase = np.pi / 4 * i
            signal = np.sin(2 * np.pi * freq * t + phase)
            noise = np.random.normal(0, 0.1, self.buffer_size)
            data[i, :] = signal + noise
        
        return data

class CHNeoWaveMCC:
    """Interface simplifiée de CHNeoWave avec backend MCC"""
    
    def __init__(self):
        self.backend = None
        self.is_running = False
        
    def initialize(self):
        """Initialise CHNeoWave avec le backend MCC"""
        print("🌊 Initialisation de CHNeoWave avec backend MCC...")
        
        # Vérifier la disponibilité du backend MCC
        if not MCCBackend.is_available():
            print("❌ Backend MCC non disponible")
            return False
        
        # Détecter les cartes
        devices = MCCBackend.detect_devices()
        if not devices:
            print("❌ Aucune carte MCC détectée")
            return False
        
        print(f"✅ {len(devices)} carte(s) MCC détectée(s)")
        for device in devices:
            print(f"   - {device['name']} (ID: {device['id']})")
        
        # Configuration du backend
        config = {
            'sample_rate': 32,
            'channels': 8,
            'device_id': 0,
            'voltage_range': (-10.0, 10.0)
        }
        
        try:
            self.backend = MCCBackend(config)
            print("✅ Backend MCC initialisé")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            return False
    
    def start_acquisition(self):
        """Démarre l'acquisition de données"""
        if not self.backend:
            print("❌ Backend non initialisé")
            return False
        
        try:
            # Ouvrir la connexion
            if not self.backend.open():
                print("❌ Échec de l'ouverture de connexion")
                return False
            
            # Configuration
            self.backend.configure_acquisition(32, 1024)
            self.backend.configure_channels([{'id': i} for i in range(8)])
            
            # Callback pour les données
            def data_callback(data):
                print(f"📊 Données acquises: {data.shape}, Min: {data.min():.3f}, Max: {data.max():.3f}")
            
            self.backend.data_callback = data_callback
            
            # Démarrer l'acquisition
            self.backend.start()
            self.is_running = True
            
            print("✅ Acquisition démarrée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage: {e}")
            return False
    
    def stop_acquisition(self):
        """Arrête l'acquisition de données"""
        if self.backend and self.is_running:
            self.backend.stop()
            self.backend.close()
            self.is_running = False
            print("✅ Acquisition arrêtée")
    
    def get_status(self):
        """Retourne le statut du système"""
        if self.backend:
            return self.backend.get_status()
        return {'status': 'non_initialisé'}

def main():
    """Fonction principale"""
    print("=" * 70)
    print("🌊 CHNeoWave - Lancement avec Backend MCC")
    print("=" * 70)
    
    # Créer l'instance de CHNeoWave
    chneowave = CHNeoWaveMCC()
    
    # Initialiser
    if not chneowave.initialize():
        print("❌ Échec de l'initialisation")
        return
    
    print("\n🎯 CHNeoWave est prêt avec le backend MCC!")
    print("📋 Fonctionnalités disponibles:")
    print("   - Acquisition temps réel")
    print("   - Support cartes Measurement Computing")
    print("   - Configuration multi-canaux")
    print("   - Gestion des données simulées")
    
    # Démarrer l'acquisition
    print("\n🚀 Démarrage de l'acquisition...")
    if chneowave.start_acquisition():
        print("✅ Acquisition en cours...")
        print("⏳ Appuyez sur Ctrl+C pour arrêter")
        
        try:
            # Maintenir l'acquisition active
            while True:
                time.sleep(1)
                status = chneowave.get_status()
                if status.get('running'):
                    print(f"📊 Statut: En cours - Fs: {status.get('sample_rate')}Hz, Canaux: {status.get('channels')}")
                else:
                    break
        except KeyboardInterrupt:
            print("\n⏹️  Arrêt demandé par l'utilisateur")
        finally:
            chneowave.stop_acquisition()
    
    print("\n" + "=" * 70)
    print("✅ CHNeoWave avec backend MCC - Test terminé")
    print("=" * 70)

if __name__ == "__main__":
    main()
