#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôleur principal pour l'acquisition de données de houle
Supporte différents backends: simulate, NI-DAQ, IOTech, Arduino
Intégration complète avec l'interface utilisateur PyQt5
"""

import numpy as np
import time
import threading
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import os
import logging
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread
from PyQt5.QtWidgets import QApplication

# Import du nouveau système de signaux unifié
try:
    from hrneowave.core.signal_bus import (
        get_signal_bus, get_error_bus, ErrorLevel, SessionState
    )
    UNIFIED_SIGNALS_AVAILABLE = True
except ImportError:
    UNIFIED_SIGNALS_AVAILABLE = False
    print("⚠️ Système de signaux unifié non disponible, utilisation des signaux legacy")

# Tentative d'import du circular_buffer
try:
    from hrneowave.core.circular_buffer import create_circular_buffer, BufferConfig
except ImportError:
    print("⚠️ Module circular_buffer non trouvé, utilisation d'un buffer simple")
    
    # Définition de BufferConfig en fallback
    @dataclass
    class BufferConfig:
        n_channels: int
        buffer_size: int
        sample_rate: float
    
    def create_circular_buffer(config):
        return SimpleCircularBuffer(config.buffer_size, config.n_channels)
    
    class SimpleCircularBuffer:
        def __init__(self, capacity, num_channels):
            self.capacity = capacity
            self.num_channels = num_channels
            self.data = [[] for _ in range(num_channels)]
            self.write_pos = 0
            self.samples_written = 0
        
        def write(self, samples):
            if isinstance(samples, (list, tuple)):
                for i, sample in enumerate(samples[:self.num_channels]):
                    if len(self.data[i]) >= self.capacity:
                        self.data[i].pop(0)
                    self.data[i].append(sample)
            else:
                if len(self.data[0]) >= self.capacity:
                    self.data[0].pop(0)
                self.data[0].append(samples)
            self.samples_written += 1
        
        def read(self, num_samples, channel=0):
            if channel < len(self.data):
                return np.array(self.data[channel][-num_samples:] if num_samples <= len(self.data[channel]) else self.data[channel])
            return np.array([])
        
        def available_samples(self, channel=0):
            return len(self.data[channel]) if channel < len(self.data) else 0
        
        def reset(self):
            self.data = [[] for _ in range(self.num_channels)]
            self.write_pos = 0
            self.samples_written = 0
        
        def get_usage(self) -> float:
            """Retourne le pourcentage d'utilisation du buffer (0.0 à 100.0)"""
            if self.capacity == 0:
                return 0.0
            max_usage = max(len(channel_data) for channel_data in self.data) if self.data else 0
            return (max_usage / self.capacity) * 100.0
        
        def get_data(self, n_samples=None):
            """Retourne les données disponibles sans les consommer"""
            if not self.data or not any(self.data):
                return None
            
            if n_samples is None:
                # Retourner toutes les données disponibles
                max_len = max(len(channel_data) for channel_data in self.data)
                result = np.zeros((self.num_channels, max_len))
                for i, channel_data in enumerate(self.data):
                    if channel_data:
                        result[i, :len(channel_data)] = channel_data
                return result
            else:
                # Retourner les n derniers échantillons
                result = np.zeros((self.num_channels, n_samples))
                for i, channel_data in enumerate(self.data):
                    if channel_data:
                        data_slice = channel_data[-n_samples:] if len(channel_data) >= n_samples else channel_data
                        result[i, :len(data_slice)] = data_slice
                return result
        
        def get_all_data(self):
            """Retourne toutes les données disponibles et les consomme"""
            result = self.get_data()
            self.reset()  # Consommer les données
            return result


class AcquisitionMode(Enum):
    """Modes d'acquisition supportés"""
    SIMULATE = "simulate"
    NI_DAQ = "ni"
    IOTECH = "iotech"
    ARDUINO = "arduino"

class AcquisitionState(Enum):
    """États de l'acquisition"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class AcquisitionConfig:
    """Configuration pour l'acquisition"""
    mode: AcquisitionMode = AcquisitionMode.SIMULATE
    sample_rate: float = 32.0  # Hz par défaut pour houle
    n_channels: int = 4
    buffer_size: int = 10000
    duration: Optional[float] = None  # secondes, None = infini
    
    # Paramètres spécifiques aux backends
    device_config: Dict[str, Any] = None
    
    # Paramètres de calibration
    calibration_params: List[Dict[str, Any]] = None
    
    # Paramètres d'interface
    update_interval_ms: int = 15  # 60+ FPS pour fluidité
    
    def __post_init__(self):
        if self.device_config is None:
            self.device_config = {}
        if self.calibration_params is None:
            self.calibration_params = []


class AcquisitionController(QObject):
    """Contrôleur principal pour l'acquisition de données avec intégration GUI complète
    
    Version 3.0.0 - Intégration du système de signaux unifié
    """
    
    # Signaux Qt unifiés (P0) - émis toutes les 0,5s
    dataBlockReady = pyqtSignal(object)  # DataBlock (émis toutes 0,5s)
    sessionFinished = pyqtSignal()       # émis après Stop
    error = pyqtSignal(str)              # erreur simplifiée
    
    # Signaux legacy (compatibilité)
    data_ready = pyqtSignal(np.ndarray, float)  # données, timestamp
    status_changed = pyqtSignal(str)  # nouveau statut
    state_changed = pyqtSignal(object)  # nouvel état (AcquisitionState)
    error_occurred = pyqtSignal(str)  # message d'erreur
    samples_acquired = pyqtSignal(int)  # nombre d'échantillons acquis
    
    def __init__(self, config: AcquisitionConfig):
        super().__init__()
        self.config = config
        self.state = AcquisitionState.STOPPED
        self.is_running = False
        self._stop_event = threading.Event()
        self._acquisition_thread = None
        self._samples_count = 0
        self._start_time = None
        self._sequence_id = 0
        
        # Initialiser le buffer circulaire
        buffer_config = BufferConfig(
            n_channels=config.n_channels,
            buffer_size=config.buffer_size,
            sample_rate=config.sample_rate
        )
        self.buffer = create_circular_buffer(buffer_config)
        
        # Backend d'acquisition
        self._backend = None
        self._init_backend()
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
        # Système de signaux unifié
        if UNIFIED_SIGNALS_AVAILABLE:
            self.signal_bus = get_signal_bus()
            self.error_bus = get_error_bus()
            self._connect_unified_signals()
        else:
            self.signal_bus = None
            self.error_bus = None
    
    def _init_backend(self):
        """Initialise le backend d'acquisition selon le mode"""
        try:
            if self.config.mode == AcquisitionMode.SIMULATE:
                self._backend = SimulateBackend(self.config)
            elif self.config.mode == AcquisitionMode.NI_DAQ:
                self._backend = NIDAQBackend(self.config)
            elif self.config.mode == AcquisitionMode.IOTECH:
                self._backend = IOTechBackend(self.config)
            elif self.config.mode == AcquisitionMode.ARDUINO:
                self._backend = ArduinoBackend(self.config)
            else:
                raise ValueError(f"Mode d'acquisition non supporté: {self.config.mode}")
        except Exception as e:
            print(f"⚠️ Erreur initialisation backend {self.config.mode}: {e}")
            # Fallback sur simulation
            self._backend = SimulateBackend(self.config)
    
    def connect(self) -> bool:
        """Connecte au hardware d'acquisition"""
        try:
            if self._backend.connect():
                self.status_changed.emit(f"Connecté - {self.config.mode.value}")
                return True
            else:
                self.error_occurred.emit(f"Échec de connexion - {self.config.mode.value}")
                return False
        except Exception as e:
            self.error_occurred.emit(f"Erreur de connexion: {str(e)}")
            return False
    
    def disconnect(self):
        """Déconnecte du hardware"""
        if self.is_running:
            self.stop()
        
        if self._backend:
            self._backend.disconnect()
        
        self.status_changed.emit("Déconnecté")
    
    def start(self) -> bool:
        """Démarre l'acquisition"""
        if self.is_running:
            error_msg = "Acquisition déjà en cours"
            self.error_occurred.emit(error_msg)
            if self.error_bus:
                self.error_bus.emit_warning(error_msg, "AcquisitionController")
            return False
        
        try:
            self._set_state(AcquisitionState.STARTING)
            
            # Réinitialiser le buffer et les compteurs
            self.buffer.reset()
            self._samples_count = 0
            self._sequence_id = 0
            self._start_time = time.time()
            
            # Configuration de session
            session_config = {
                'mode': self.config.mode.value,
                'sample_rate': self.config.sample_rate,
                'n_channels': self.config.n_channels,
                'buffer_size': self.config.buffer_size
            }
            
            # Démarrer la session via le bus unifié
            if self.signal_bus:
                self.signal_bus.start_session(session_config)
            
            # Connecter si nécessaire
            if not self.connect():
                error_msg = "Échec de connexion au backend"
                self.error_occurred.emit(error_msg)
                if self.error_bus:
                    self.error_bus.emit_error("ERROR", error_msg, "AcquisitionController")
                self._set_state(AcquisitionState.ERROR)
                return False
            
            # Démarrer le thread d'acquisition
            self._stop_event.clear()
            self._acquisition_thread = threading.Thread(target=self._acquisition_loop, daemon=True)
            self._acquisition_thread.start()
            
            self.is_running = True
            self._set_state(AcquisitionState.RUNNING)
            self.status_changed.emit("Acquisition démarrée")
            
            if self.error_bus:
                self.error_bus.emit_info(
                    f"Acquisition démarrée avec backend {self.config.mode.value}",
                    "AcquisitionController",
                    {'config': session_config}
                )
            
            return True
            
        except Exception as e:
            error_msg = f"Erreur lors du démarrage: {str(e)}"
            self.error_occurred.emit(error_msg)
            self.error.emit(str(e))
            
            if self.error_bus:
                self.error_bus.emit_critical(
                    "Erreur lors du démarrage de l'acquisition",
                    "AcquisitionController",
                    {'mode': self.config.mode.value},
                    e
                )
            
            self._set_state(AcquisitionState.ERROR)
            return False
    
    def stop(self):
        """Arrête l'acquisition"""
        if not self.is_running:
            return
        
        self._set_state(AcquisitionState.STOPPING)
        self._stop_event.set()
        
        # Calculer les statistiques de session
        session_stats = {
            'total_samples': self._samples_count,
            'duration': time.time() - self._start_time if self._start_time else 0,
            'mode': self.config.mode.value,
            'sample_rate': self.config.sample_rate,
            'n_channels': self.config.n_channels
        }
        
        if self._acquisition_thread and self._acquisition_thread.is_alive():
            self._acquisition_thread.join(timeout=2.0)
        
        if self._backend:
            self._backend.disconnect()
        
        self.is_running = False
        self._set_state(AcquisitionState.STOPPED)
        self.status_changed.emit("Acquisition arrêtée")
        
        # P0: Émettre sessionFinished() après Stop
        self.sessionFinished.emit()
        
        if self.signal_bus:
            self.signal_bus.finish_session(session_stats)
        
        if self.error_bus:
            self.error_bus.emit_info(
                "Acquisition arrêtée",
                "AcquisitionController",
                session_stats
            )
    
    def _set_state(self, new_state: AcquisitionState):
        """Change l'état et émet le signal"""
        if self.state != new_state:
            self.state = new_state
            self.state_changed.emit(new_state)
    
    def _acquisition_loop(self):
        """Boucle principale d'acquisition avec gestion de performance"""
        sample_interval = 1.0 / self.config.sample_rate
        last_emit_time = time.time()
        emit_interval = 0.5  # P0: émission toutes les 0,5s
        
        while not self._stop_event.is_set():
            try:
                start_time = time.time()
                
                # Lire les données du backend
                data = self._backend.read_sample()
                if data is not None:
                    # Appliquer la calibration si disponible
                    calibrated_data = self._apply_calibration(data)
                    
                    # Écrire dans le buffer
                    self.buffer.write(calibrated_data)
                    self._samples_count += 1
                    self._sequence_id += 1
                    
                    # Émettre les signaux à intervalle régulier pour éviter la surcharge
                    current_time = time.time()
                    if current_time - last_emit_time >= emit_interval:
                        # Signaux legacy
                        self.data_ready.emit(calibrated_data, current_time)
                        self.samples_acquired.emit(self._samples_count)
                        
                        # Nouveau système unifié - créer un DataBlock
                        if self.signal_bus:
                            data_block = {
                                'data': calibrated_data,
                                'timestamp': current_time,
                                'sequence_id': self._sequence_id,
                                'sample_rate': self.config.sample_rate,
                                'n_channels': self.config.n_channels
                            }
                            self.dataBlockReady.emit(data_block)
                            self.signal_bus.emit_data_block(
                                data=calibrated_data,
                                timestamp=current_time,
                                sample_rate=self.config.sample_rate,
                                n_channels=self.config.n_channels,
                                sequence_id=self._sequence_id
                            )
                        
                        last_emit_time = current_time
                    
                    # Vérifier la durée maximale si définie
                    if (self.config.duration and 
                        current_time - self._start_time >= self.config.duration):
                        break
                
                # Attendre pour maintenir la fréquence d'échantillonnage
                elapsed = time.time() - start_time
                sleep_time = max(0, sample_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            except Exception as e:
                error_msg = f"Erreur d'acquisition: {str(e)}"
                self.error_occurred.emit(error_msg)
                self.error.emit(str(e))
                
                if self.error_bus:
                    self.error_bus.emit_error(
                        "ERROR",
                        "Erreur dans la boucle d'acquisition",
                        "AcquisitionController",
                        {'samples_count': self._samples_count},
                        e
                    )
                
                self._set_state(AcquisitionState.ERROR)
                break
    
    def _apply_calibration(self, raw_data: np.ndarray) -> np.ndarray:
        """Applique la calibration aux données brutes"""
        if not self.config.calibration_params:
            return raw_data
        
        calibrated = np.copy(raw_data)
        for i, calib in enumerate(self.config.calibration_params):
            if i < len(calibrated):
                slope = calib.get('slope', 1.0)
                intercept = calib.get('intercept', 0.0)
                unit = calib.get('unit', 'm')
                
                calibrated[i] = calibrated[i] * slope + intercept
                
                # Conversion d'unités si nécessaire
                if unit == 'cm':
                    calibrated[i] /= 100.0  # Convertir en mètres
        
        return calibrated
    
    def read(self, n_samples: int, channel: Optional[int] = None) -> Optional[np.ndarray]:
        """Lit des données du buffer"""
        if channel is not None:
            return self.buffer.read(n_samples, channel)
        else:
            # Retourner toutes les chaînes
            data = []
            for ch in range(self.config.n_channels):
                data.append(self.buffer.read(n_samples, ch))
            return np.array(data)
    
    def get_available_samples(self, channel: int = 0) -> int:
        """Retourne le nombre d'échantillons disponibles"""
        return self.buffer.available_samples(channel)
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel"""
        elapsed_time = time.time() - self._start_time if self._start_time else 0
        return {
            'running': self.is_running,
            'state': self.state.value,
            'mode': self.config.mode.value,
            'sample_rate': self.config.sample_rate,
            'n_channels': self.config.n_channels,
            'samples_count': self._samples_count,
            'elapsed_time': elapsed_time,
            'buffer_fill': self.buffer.available_samples() if hasattr(self.buffer, 'available_samples') else 0
        }
    
    def get_real_time_data(self, window_duration: float = 10.0) -> Tuple[np.ndarray, List[np.ndarray]]:
        """Retourne les données pour affichage temps réel"""
        n_samples = int(window_duration * self.config.sample_rate)
        
        # Générer le vecteur temps
        if self._start_time:
            current_time = time.time() - self._start_time
            time_vector = np.linspace(max(0, current_time - window_duration), current_time, n_samples)
        else:
            time_vector = np.linspace(0, window_duration, n_samples)
        
        # Lire les données de tous les canaux
        channel_data = []
        for ch in range(self.config.n_channels):
            data = self.buffer.read(n_samples, ch)
            # Ajuster la taille si nécessaire
            if len(data) < n_samples:
                padded_data = np.zeros(n_samples)
                if len(data) > 0:
                    padded_data[-len(data):] = data
                data = padded_data
            elif len(data) > n_samples:
                data = data[-n_samples:]
            channel_data.append(data)
        
        return time_vector, channel_data
    
    def _connect_unified_signals(self):
        """Connecte les signaux au système unifié"""
        if not self.signal_bus or not self.error_bus:
            return
        
        # Connecter les signaux d'erreur
        self.error_occurred.connect(
            lambda msg: self.error_bus.emit_error("ERROR", msg, "AcquisitionController")
        )
    
    # === ALIAS POUR COMPATIBILITÉ UI ===
    def start_acquisition(self) -> bool:
        """Alias pour start() - compatibilité avec l'interface utilisateur"""
        return self.start()
    
    def stop_acquisition(self):
        """Alias pour stop() - compatibilité avec l'interface utilisateur"""
        self.stop()
    
    def clear(self):
        """Vide le buffer circulaire"""
        if hasattr(self.buffer, 'reset'):
            self.buffer.reset()
        self._samples_count = 0
        self._sequence_id = 0
        self.status_changed.emit("Buffer vidé")
        
        if self.error_bus:
            self.error_bus.emit_info(
                "Buffer vidé",
                "AcquisitionController"
            )


class AcquisitionBackend:
    """Interface de base pour les backends d'acquisition"""
    
    def __init__(self, config: AcquisitionConfig):
        self.config = config
    
    def connect(self) -> bool:
        raise NotImplementedError
    
    def disconnect(self):
        raise NotImplementedError
    
    def read_sample(self) -> Optional[np.ndarray]:
        raise NotImplementedError


class SimulateBackend(AcquisitionBackend):
    """Backend de simulation pour tests et développement"""
    
    def __init__(self, config: AcquisitionConfig):
        super().__init__(config)
        self.t = 0.0
        self.dt = 1.0 / config.sample_rate
        self.is_connected = False
        self.sample_count = 0
        self._wave_params = {
            'Hs': 2.0,  # Hauteur significative (m)
            'Tp': 8.0,  # Période de pic (s)
            'gamma': 3.3,  # Paramètre de forme JONSWAP
            'direction': 0.0  # Direction principale (rad)
        }
    
    def connect(self) -> bool:
        self.is_connected = True
        self.sample_count = 0
        return True
    
    def disconnect(self):
        self.is_connected = False
    
    def read_sample(self) -> Optional[np.ndarray]:
        """Génère des données de houle réalistes"""
        if not self.is_connected:
            return None
            
        t = self.sample_count / self.config.sample_rate
        self.sample_count += 1
        
        # Générer un spectre JONSWAP réaliste
        data = np.zeros(self.config.n_channels)
        
        # Fréquences principales
        fp = 1.0 / self._wave_params['Tp']   # Fréquence de pic
        
        for i in range(self.config.n_channels):
            # Composante principale (spectre JONSWAP simplifié)
            wave = 0.0
            
            # Plusieurs composantes fréquentielles
            for n in range(1, 6):
                freq = fp * n / 3.0
                amplitude = self._wave_params['Hs'] / 4.0 * np.exp(-((freq - fp) / (0.1 * fp))**2)
                phase = np.random.uniform(0, 2*np.pi) if self.sample_count == 1 else 0
                wave += amplitude * np.sin(2 * np.pi * freq * t + phase)
            
            # Ajouter du bruit réaliste
            noise_level = 0.02 * self._wave_params['Hs']
            wave += noise_level * np.random.randn()
            
            # Déphasage spatial entre sondes (propagation)
            spatial_phase = i * 0.1  # Déphasage entre sondes
            data[i] = wave * np.cos(spatial_phase)
            
        self.t += self.dt
        return data
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du backend"""
        return {
            'type': 'simulate',
            'connected': self.is_connected,
            'samples_generated': self.sample_count,
            'wave_params': self._wave_params
        }


class NIDAQBackend(AcquisitionBackend):
    """Backend pour cartes National Instruments DAQ"""
    
    def __init__(self, config: AcquisitionConfig):
        super().__init__(config)
        self.is_connected = False
        self._task = None
    
    def connect(self) -> bool:
        """Initialise la carte NI-DAQ"""
        try:
            # Tentative d'import du module NI-DAQmx
            import nidaqmx
            from nidaqmx.constants import AcquisitionType
            
            # Créer une tâche d'acquisition
            self._task = nidaqmx.Task()
            
            # Configurer les canaux analogiques
            device_name = self.config.device_config.get('device', 'Dev1')
            voltage_range = self.config.device_config.get('voltage_range', [-10.0, 10.0])
            
            for i in range(self.config.n_channels):
                channel_name = f"{device_name}/ai{i}"
                self._task.ai_channels.add_ai_voltage_chan(
                    channel_name,
                    min_val=voltage_range[0],
                    max_val=voltage_range[1]
                )
            
            # Configurer l'échantillonnage
            self._task.timing.cfg_samp_clk_timing(
                rate=self.config.sample_rate,
                samps_per_chan=1,
                sample_mode=AcquisitionType.CONTINUOUS
            )
            
            self._task.start()
            self.is_connected = True
            return True
            
        except ImportError:
            print("⚠️ Module nidaqmx non disponible, fallback sur simulation")
            return False
        except Exception as e:
            print(f"⚠️ Erreur NI-DAQ: {e}")
            return False
    
    def disconnect(self):
        """Nettoie les ressources NI-DAQ"""
        if self._task:
            try:
                self._task.stop()
                self._task.close()
            except:
                pass
        self.is_connected = False
    
    def read_sample(self) -> Optional[np.ndarray]:
        """Lit un échantillon de la carte NI-DAQ"""
        if not self.is_connected or not self._task:
            return None
        
        try:
            data = self._task.read(number_of_samples_per_channel=1)
            return np.array(data).flatten()
        except Exception as e:
            print(f"Erreur lecture NI-DAQ: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        return {
            'type': 'ni_daq',
            'connected': self.is_connected,
            'task_active': self._task is not None
        }


class IOTechBackend(AcquisitionBackend):
    """Backend pour cartes IOTech"""
    
    def __init__(self, config: AcquisitionConfig):
        super().__init__(config)
        self.is_connected = False
    
    def connect(self) -> bool:
        """Initialise la carte IOTech"""
        try:
            # Placeholder pour l'initialisation IOTech
            # À implémenter selon l'API IOTech spécifique
            print("⚠️ Backend IOTech non encore implémenté, fallback sur simulation")
            return False
        except Exception as e:
            print(f"⚠️ Erreur IOTech: {e}")
            return False
    
    def disconnect(self):
        """Nettoie les ressources IOTech"""
        self.is_connected = False
    
    def read_sample(self) -> Optional[np.ndarray]:
        """Lit un échantillon de la carte IOTech"""
        return None
    
    def get_status(self) -> Dict[str, Any]:
        return {
            'type': 'iotech',
            'connected': self.is_connected
        }


class ArduinoBackend(AcquisitionBackend):
    """Backend pour acquisition via Arduino"""
    
    def __init__(self, config: AcquisitionConfig):
        super().__init__(config)
        self.is_connected = False
        self._serial_port = None
    
    def connect(self) -> bool:
        """Initialise la connexion série Arduino"""
        try:
            import serial
            import serial.tools.list_ports
            
            # Détecter automatiquement le port Arduino
            arduino_port = None
            for port in serial.tools.list_ports.comports():
                if 'Arduino' in port.description or 'CH340' in port.description:
                    arduino_port = port.device
                    break
            
            if not arduino_port:
                arduino_port = self.config.device_config.get('port', 'COM3')
            
            # Ouvrir la connexion série
            self._serial_port = serial.Serial(
                port=arduino_port,
                baudrate=self.config.device_config.get('baudrate', 115200),
                timeout=1.0
            )
            
            # Attendre la stabilisation
            time.sleep(2)
            
            # Envoyer commande de configuration
            config_cmd = f"CONFIG:{self.config.sample_rate}:{self.config.n_channels}\n"
            self._serial_port.write(config_cmd.encode())
            
            self.is_connected = True
            return True
            
        except ImportError:
            print("⚠️ Module pyserial non disponible")
            return False
        except Exception as e:
            print(f"⚠️ Erreur Arduino: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion série"""
        if self._serial_port and self._serial_port.is_open:
            try:
                self._serial_port.close()
            except:
                pass
        self.is_connected = False
    
    def read_sample(self) -> Optional[np.ndarray]:
        """Lit un échantillon via série"""
        if not self.is_connected or not self._serial_port:
            return None
        
        try:
            # Lire une ligne de données
            line = self._serial_port.readline().decode().strip()
            if line:
                # Parser les données (format: "val1,val2,val3,val4")
                values = [float(x) for x in line.split(',')]
                if len(values) >= self.config.n_channels:
                    return np.array(values[:self.config.n_channels])
            return None
        except Exception as e:
            print(f"Erreur lecture Arduino: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        return {
            'type': 'arduino',
            'connected': self.is_connected,
            'port': self._serial_port.port if self._serial_port else None
        }


def create_acquisition_controller(mode_str: str = "simulate", fs: float = 32.0, 
                                sensor_type: str = "wave_probe") -> AcquisitionController:
    """Factory function pour créer un contrôleur d'acquisition"""
    
    # Utiliser les variables d'environnement si disponibles
    mode_str = os.getenv('CHNW_MODE', mode_str)
    fs = float(os.getenv('CHNW_FS', fs))
    sensor_type = os.getenv('CHNW_SENSOR_TYPE', sensor_type)
    
    # Convertir le mode string en enum
    mode_mapping = {
        'simulate': AcquisitionMode.SIMULATE,
        'offline': AcquisitionMode.SIMULATE,  # Alias
        'ni': AcquisitionMode.NI_DAQ,
        'iotech': AcquisitionMode.IOTECH,
        'arduino': AcquisitionMode.ARDUINO
    }
    
    mode = mode_mapping.get(mode_str, AcquisitionMode.SIMULATE)
    
    config = AcquisitionConfig(
        mode=mode,
        sample_rate=fs,
        n_channels=4  # Valeur par défaut pour houle
    )
    
    return AcquisitionController(config)