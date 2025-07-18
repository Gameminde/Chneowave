"""Backend pour carte d'acquisition IOTech Personal Daq 3000"""

import os
import ctypes
import numpy as np
from typing import Optional, Tuple
from abc import ABC, abstractmethod


class DAQSession(ABC):
    """Interface abstraite pour les sessions d'acquisition"""

    @abstractmethod
    def open(self) -> bool:
        pass

    @abstractmethod
    def start(self, fs: float) -> bool:
        pass

    @abstractmethod
    def read(self, n_samples: int) -> np.ndarray:
        pass

    @abstractmethod
    def stop(self) -> bool:
        pass

    @abstractmethod
    def close(self) -> bool:
        pass


class IOTechSession(DAQSession):
    """Session d'acquisition pour carte IOTech Personal Daq 3000"""

    def __init__(self, device_name: Optional[str] = None):
        self.device_name = device_name or os.getenv("CHNW_IO_DEVICE", "DaqBoard3K0")
        self.dll = None
        self.handle = None
        self.is_open = False
        self.is_started = False
        self.fs = 500.0
        self.n_channels = int(os.getenv("CHNW_N_PROBES", "16"))

    def open(self) -> bool:
        """Ouvre la connexion avec la carte IOTech"""
        try:
            # Charger la DLL IOTech
            self.dll = ctypes.WinDLL("daqx.dll")

            # Configurer les types de retour
            self.dll.daqOpen.restype = ctypes.c_int
            self.dll.daqOpen.argtypes = [ctypes.c_char_p]

            # Ouvrir le device
            device_bytes = self.device_name.encode("ascii")
            self.handle = self.dll.daqOpen(device_bytes)

            if self.handle < 0:
                raise RuntimeError(f"Impossible d'ouvrir {self.device_name}")

            self.is_open = True
            return True

        except Exception as e:
            print(f"Erreur ouverture IOTech: {e}")
            return False

    def start(self, fs: float) -> bool:
        """Démarre l'acquisition à la fréquence spécifiée"""
        if not self.is_open:
            raise RuntimeError("Device non ouvert")

        try:
            self.fs = fs

            # Configuration acquisition
            self.dll.daqAdcSetAcq.argtypes = [
                ctypes.c_int,  # handle
                ctypes.c_int,  # mode
                ctypes.c_int,  # channels
                ctypes.c_float,  # frequency
            ]

            result = self.dll.daqAdcSetAcq(
                self.handle, 1, self.n_channels, ctypes.c_float(fs)  # mode continu
            )

            if result != 0:
                raise RuntimeError(f"Erreur configuration acquisition: {result}")

            # Démarrer acquisition
            start_result = self.dll.daqAdcArm(self.handle)
            if start_result != 0:
                raise RuntimeError(f"Erreur démarrage acquisition: {start_result}")

            self.is_started = True
            return True

        except Exception as e:
            print(f"Erreur démarrage IOTech: {e}")
            return False

    def read(self, n_samples: int) -> np.ndarray:
        """Lit n_samples échantillons sur tous les canaux"""
        if not self.is_started:
            raise RuntimeError("Acquisition non démarrée")

        try:
            # Buffer pour les données
            buffer_size = n_samples * self.n_channels
            buffer = (ctypes.c_float * buffer_size)()

            # Lecture des données
            self.dll.daqAdcRead.argtypes = [
                ctypes.c_int,  # handle
                ctypes.POINTER(ctypes.c_float),  # buffer
                ctypes.c_int,  # count
                ctypes.c_int,  # timeout
            ]

            result = self.dll.daqAdcRead(
                self.handle, buffer, buffer_size, 5000  # timeout 5s
            )

            if result != buffer_size:
                print(f"Attention: lu {result}/{buffer_size} échantillons")

            # Convertir en numpy array
            data = np.array(buffer[:result], dtype=np.float32)

            # Reshape en (n_samples, n_channels)
            if len(data) >= self.n_channels:
                n_complete_samples = len(data) // self.n_channels
                data = data[: n_complete_samples * self.n_channels]
                data = data.reshape(n_complete_samples, self.n_channels)
            else:
                data = data.reshape(1, -1)

            return data

        except Exception as e:
            print(f"Erreur lecture IOTech: {e}")
            return np.array([])

    def stop(self) -> bool:
        """Arrête l'acquisition"""
        if not self.is_started:
            return True

        try:
            result = self.dll.daqAdcDisarm(self.handle)
            self.is_started = False
            return result == 0

        except Exception as e:
            print(f"Erreur arrêt IOTech: {e}")
            return False

    def close(self) -> bool:
        """Ferme la connexion"""
        if self.is_started:
            self.stop()

        if not self.is_open:
            return True

        try:
            result = self.dll.daqClose(self.handle)
            self.is_open = False
            self.handle = None
            return result == 0

        except Exception as e:
            print(f"Erreur fermeture IOTech: {e}")
            return False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def create_daq_session(device_type: str = "iotech") -> DAQSession:
    """Factory pour créer une session DAQ"""
    device_name = os.getenv("CHNW_IO_DEVICE", "DaqBoard3K0")

    if device_type.lower() == "iotech":
        return IOTechSession(device_name)
    else:
        raise ValueError(f"Type de device non supporté: {device_type}")
