#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend IOtech pour CHNeoWave
Wrapper pour daqx.dll (Personal DAQ 3000)
"""

import logging
import numpy as np
from typing import Optional, List, Dict, Any
from threading import Thread, Event
import time
import ctypes
from ctypes import wintypes, byref, c_double, c_int, c_uint, c_void_p, POINTER
import os

logger = logging.getLogger(__name__)

# Tentative de chargement de la DLL IOtech
try:
    # Recherche de daqx.dll dans les emplacements standards
    dll_paths = [
        r"C:\Program Files\IOtech\Personal DAQ\daqx.dll",
        r"C:\Program Files (x86)\IOtech\Personal DAQ\daqx.dll",
        r"C:\Windows\System32\daqx.dll",
        r"C:\Windows\SysWOW64\daqx.dll",
        "daqx.dll"  # Dans le PATH
    ]
    
    daqx_dll = None
    for dll_path in dll_paths:
        try:
            if os.path.exists(dll_path) or dll_path == "daqx.dll":
                daqx_dll = ctypes.WinDLL(dll_path)
                logger.info(f"DLL IOtech chargée: {dll_path}")
                break
        except OSError:
            continue
    
    IOTECH_AVAILABLE = daqx_dll is not None
    
except Exception as e:
    logger.warning(f"Impossible de charger daqx.dll: {e}")
    IOTECH_AVAILABLE = False
    daqx_dll = None

# Constantes IOtech DAQ
DAQ_SUCCESS = 0
DAQ_CONTINUOUS = 1
DAQ_SINGLE_ENDED = 0
DAQ_DIFFERENTIAL = 1

class IOtechBackend:
    """
    Backend pour cartes d'acquisition IOtech Personal DAQ 3000
    Support 8/16 voies analogiques, 32/100/500 Hz
    """
    
    SUPPORTED_SAMPLE_RATES = [32, 100, 500]
    MAX_CHANNELS = 16
    
    def __init__(self):
        self.device_handle = None
        self.is_running = False
        self.acquisition_thread: Optional[Thread] = None
        self.stop_event = Event()
        self.data_callback = None
        self.error_callback = None
        
        # Configuration par défaut
        self.sample_rate = 32
        self.channels = 8
        self.device_id = 0  # Premier périphérique
        self.input_mode = DAQ_SINGLE_ENDED
        self.voltage_range = 10.0  # ±10V
        
        # Buffer pour les données
        self.buffer_size = 1024
        self.data_buffer = None
        
        if not IOTECH_AVAILABLE:
            logger.warning("daqx.dll non disponible - mode simulation activé")
        else:
            self._setup_dll_functions()
    
    def _setup_dll_functions(self):
        """Configure les signatures des fonctions DLL"""
        if not daqx_dll:
            return
        
        try:
            # daqOpen
            self.daqOpen = daqx_dll.daqOpen
            self.daqOpen.argtypes = [c_int]
            self.daqOpen.restype = c_void_p
            
            # daqClose
            self.daqClose = daqx_dll.daqClose
            self.daqClose.argtypes = [c_void_p]
            self.daqClose.restype = c_int
            
            # daqAdcSetAcq
            self.daqAdcSetAcq = daqx_dll.daqAdcSetAcq
            self.daqAdcSetAcq.argtypes = [c_void_p, c_int, c_int, c_int]
            self.daqAdcSetAcq.restype = c_int
            
            # daqAdcSetScan
            self.daqAdcSetScan = daqx_dll.daqAdcSetScan
            self.daqAdcSetScan.argtypes = [c_void_p, POINTER(c_int), POINTER(c_int), c_int]
            self.daqAdcSetScan.restype = c_int
            
            # daqAdcSetFreq
            self.daqAdcSetFreq = daqx_dll.daqAdcSetFreq
            self.daqAdcSetFreq.argtypes = [c_void_p, c_double]
            self.daqAdcSetFreq.restype = c_int
            
            # daqAdcArm
            self.daqAdcArm = daqx_dll.daqAdcArm
            self.daqAdcArm.argtypes = [c_void_p]
            self.daqAdcArm.restype = c_int
            
            # daqAdcDisarm
            self.daqAdcDisarm = daqx_dll.daqAdcDisarm
            self.daqAdcDisarm.argtypes = [c_void_p]
            self.daqAdcDisarm.restype = c_int
            
            # daqAdcTransferGetStat
            self.daqAdcTransferGetStat = daqx_dll.daqAdcTransferGetStat
            self.daqAdcTransferGetStat.argtypes = [c_void_p, POINTER(c_uint), POINTER(c_uint)]
            self.daqAdcTransferGetStat.restype = c_int
            
            # daqAdcTransferBufData
            self.daqAdcTransferBufData = daqx_dll.daqAdcTransferBufData
            self.daqAdcTransferBufData.argtypes = [c_void_p, POINTER(c_double), c_uint, c_int]
            self.daqAdcTransferBufData.restype = c_int
            
            logger.info("Fonctions DLL IOtech configurées")
            
        except AttributeError as e:
            logger.error(f"Fonction DLL manquante: {e}")
            global IOTECH_AVAILABLE
            IOTECH_AVAILABLE = False
    
    @classmethod
    def is_available(cls) -> bool:
        """Vérifie si le backend IOtech est disponible"""
        return IOTECH_AVAILABLE
    
    @classmethod
    def detect_devices(cls) -> List[str]:
        """Détecte les périphériques IOtech disponibles"""
        if not IOTECH_AVAILABLE:
            return []
        
        devices = []
        # Tenter d'ouvrir les périphériques 0-3
        for device_id in range(4):
            try:
                instance = cls()
                if instance._test_device(device_id):
                    devices.append(f"IOtech_DAQ_{device_id}")
            except Exception:
                continue
        
        logger.info(f"Périphériques IOtech détectés: {devices}")
        return devices
    
    def _test_device(self, device_id: int) -> bool:
        """Teste si un périphérique est disponible"""
        if not daqx_dll:
            return False
        
        try:
            handle = self.daqOpen(device_id)
            if handle:
                self.daqClose(handle)
                return True
        except Exception:
            pass
        return False
    
    def configure(self, sample_rate: int, channels: int, device_id: int = 0, **kwargs) -> bool:
        """
        Configure le backend
        
        Args:
            sample_rate: Fréquence d'échantillonnage (32, 100, 500 Hz)
            channels: Nombre de canaux (1-16)
            device_id: ID du périphérique IOtech
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
        self.device_id = device_id
        
        # Paramètres optionnels
        self.input_mode = kwargs.get('input_mode', DAQ_SINGLE_ENDED)
        self.voltage_range = kwargs.get('voltage_range', 10.0)
        
        # Calculer la taille du buffer
        self.buffer_size = max(64, self.sample_rate // 4)  # 250ms de données minimum
        
        logger.info(f"Configuration IOtech: {sample_rate} Hz, {channels} canaux, device {device_id}")
        return True
    
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
        
        if not IOTECH_AVAILABLE:
            # Mode simulation
            logger.info("Démarrage acquisition en mode simulation")
            self._start_simulation()
            return True
        
        if not self._setup_device():
            return False
        
        try:
            self.stop_event.clear()
            self.is_running = True
            
            # Démarrer le thread d'acquisition
            self.acquisition_thread = Thread(target=self._acquisition_loop, daemon=True)
            self.acquisition_thread.start()
            
            logger.info("Acquisition IOtech démarrée")
            return True
            
        except Exception as e:
            logger.error(f"Erreur démarrage acquisition: {e}")
            self._cleanup()
            return False
    
    def _setup_device(self) -> bool:
        """Configure le périphérique IOtech"""
        try:
            # Ouvrir le périphérique
            self.device_handle = self.daqOpen(self.device_id)
            if not self.device_handle:
                logger.error(f"Impossible d'ouvrir le périphérique {self.device_id}")
                return False
            
            # Configuration de l'acquisition
            result = self.daqAdcSetAcq(self.device_handle, DAQ_CONTINUOUS, 0, 0)
            if result != DAQ_SUCCESS:
                logger.error(f"Erreur configuration acquisition: {result}")
                return False
            
            # Configuration des canaux
            channels_array = (c_int * self.channels)()
            gains_array = (c_int * self.channels)()
            
            for i in range(self.channels):
                channels_array[i] = i
                gains_array[i] = 1  # Gain unitaire
            
            result = self.daqAdcSetScan(self.device_handle, channels_array, gains_array, self.channels)
            if result != DAQ_SUCCESS:
                logger.error(f"Erreur configuration canaux: {result}")
                return False
            
            # Configuration de la fréquence
            result = self.daqAdcSetFreq(self.device_handle, float(self.sample_rate))
            if result != DAQ_SUCCESS:
                logger.error(f"Erreur configuration fréquence: {result}")
                return False
            
            # Armer l'acquisition
            result = self.daqAdcArm(self.device_handle)
            if result != DAQ_SUCCESS:
                logger.error(f"Erreur armement acquisition: {result}")
                return False
            
            # Allouer le buffer de données
            self.data_buffer = (c_double * (self.buffer_size * self.channels))()
            
            logger.info("Périphérique IOtech configuré et armé")
            return True
            
        except Exception as e:
            logger.error(f"Erreur configuration périphérique: {e}")
            return False
    
    def _acquisition_loop(self):
        """Boucle principale d'acquisition"""
        samples_per_read = max(1, self.sample_rate // 10)  # 100ms de données
        
        while not self.stop_event.is_set():
            try:
                # Vérifier le statut du transfert
                active = c_uint()
                retCount = c_uint()
                
                result = self.daqAdcTransferGetStat(self.device_handle, byref(active), byref(retCount))
                if result != DAQ_SUCCESS:
                    logger.error(f"Erreur statut transfert: {result}")
                    break
                
                # Lire les données si disponibles
                if retCount.value >= samples_per_read * self.channels:
                    result = self.daqAdcTransferBufData(
                        self.device_handle,
                        self.data_buffer,
                        samples_per_read * self.channels,
                        1  # Wait for data
                    )
                    
                    if result == DAQ_SUCCESS:
                        # Convertir en numpy array
                        data_flat = np.array([self.data_buffer[i] for i in range(samples_per_read * self.channels)])
                        data_array = data_flat.reshape((samples_per_read, self.channels))
                        
                        # Appeler le callback
                        if self.data_callback:
                            self.data_callback(data_array)
                    else:
                        logger.error(f"Erreur lecture données: {result}")
                
                time.sleep(0.01)  # 10ms
                
            except Exception as e:
                logger.error(f"Erreur boucle acquisition: {e}")
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
                
                # Signaux sinusoidaux avec bruit (différents de NI pour distinction)
                data = np.zeros((samples_per_read, self.channels))
                for ch in range(self.channels):
                    freq = 0.2 + ch * 0.03  # Fréquences légèrement différentes
                    amplitude = 0.8 + ch * 0.15
                    phase = ch * np.pi / 4  # Déphasage par canal
                    data[:, ch] = amplitude * np.sin(2 * np.pi * freq * time_array + phase)
                    data[:, ch] += 0.05 * np.random.randn(samples_per_read)  # Moins de bruit
                
                if self.data_callback:
                    self.data_callback(data)
                
                t += samples_per_read / self.sample_rate
                time.sleep(0.1)  # 100ms
        
        self.acquisition_thread = Thread(target=simulation_loop, daemon=True)
        self.acquisition_thread.start()
        
        logger.info(f"Simulation IOtech démarrée: {self.channels} canaux à {self.sample_rate} Hz")
    
    def stop_acquisition(self) -> bool:
        """
        Arrête l'acquisition
        
        Returns:
            bool: True si arrêt réussi
        """
        if not self.is_running:
            return True
        
        logger.info("Arrêt acquisition IOtech...")
        self.stop_event.set()
        self.is_running = False
        
        # Attendre la fin du thread
        if self.acquisition_thread and self.acquisition_thread.is_alive():
            self.acquisition_thread.join(timeout=2.0)
        
        self._cleanup()
        logger.info("Acquisition IOtech arrêtée")
        return True
    
    def _cleanup(self):
        """Nettoie les ressources"""
        if self.device_handle and daqx_dll:
            try:
                self.daqAdcDisarm(self.device_handle)
                self.daqClose(self.device_handle)
            except Exception as e:
                logger.error(f"Erreur nettoyage périphérique: {e}")
            finally:
                self.device_handle = None
        
        self.data_buffer = None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du backend"""
        return {
            'backend': 'IOtech',
            'available': IOTECH_AVAILABLE,
            'running': self.is_running,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'device_id': self.device_id,
            'simulation': not IOTECH_AVAILABLE
        }
    
    def __del__(self):
        """Destructeur - nettoie les ressources"""
        if self.is_running:
            self.stop_acquisition()
