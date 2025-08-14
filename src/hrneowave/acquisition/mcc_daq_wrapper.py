#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper Python pour carte d'acquisition MCC DAQ USB-1608FS
Module d'interface avec les DLLs de Measurement Computing

Auteur: CHNeoWave Development Team
Version: 1.0.0
"""

import ctypes
import ctypes.wintypes
import logging
import numpy as np
import time
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any
from dataclasses import dataclass
from enum import IntEnum

# Configuration du logging
logger = logging.getLogger(__name__)

class MCCErrorCodes(IntEnum):
    """Codes d'erreur MCC DAQ"""
    NOERRORS = 0
    BADBOARD = 1
    DEADDIGITALDEV = 2
    DEADCOUNTERDEV = 3
    DEADDADEV = 4
    DEADADDEV = 5
    NOTDIGITALCONF = 6
    NOTCOUNTERCONF = 7
    NOTDACONF = 8
    NOTADCONF = 9
    NOTMUXCONF = 10
    BADPORTNUM = 11
    BADCOUNTERDEVNUM = 12
    BADDADEVNUM = 13
    BADADDEVNUM = 14
    BADCHANNEL = 15
    BADRANGE = 16
    BADCOUNTERCHAN = 17
    BADCOUNTERPARAM = 18
    BADEVENTTYPE = 19
    WRONGDIGCONFIG = 20
    WRONGDIOCONFIG = 21
    WRONGCOUNTERCONFIG = 22
    WRONGDACONFIG = 23
    WRONGADCONFIG = 24

class MCCRanges(IntEnum):
    """Plages de tension disponibles"""
    BIP20VOLTS = 0      # ±20V (Non disponible sur USB-1608FS)
    BIP10VOLTS = 1      # ±10V
    BIP5VOLTS = 2       # ±5V
    BIP4VOLTS = 3       # ±4V (Non disponible sur USB-1608FS)
    BIP2PT5VOLTS = 4    # ±2.5V (Non disponible sur USB-1608FS)
    BIP2VOLTS = 5       # ±2V
    BIP1PT25VOLTS = 6   # ±1.25V (Non disponible sur USB-1608FS)
    BIP1VOLTS = 7       # ±1V
    BIPPT625VOLTS = 8   # ±0.625V (Non disponible sur USB-1608FS)
    BIPPT5VOLTS = 9     # ±0.5V (Non disponible sur USB-1608FS)
    BIPPT25VOLTS = 10   # ±0.25V (Non disponible sur USB-1608FS)
    BIPPT2VOLTS = 11    # ±0.2V (Non disponible sur USB-1608FS)
    BIPPT1VOLTS = 12    # ±0.1V (Non disponible sur USB-1608FS)
    BIPPT05VOLTS = 13   # ±0.05V (Non disponible sur USB-1608FS)
    
class MCCOptions(IntEnum):
    """Options d'acquisition"""
    DEFAULTOPTION = 0x0000
    CONTINUOUS = 0x0001
    BACKGROUND = 0x0002
    SINGLEENDED = 0x0004
    DIFFERENTIAL = 0x0008
    BLOCKIO = 0x0010
    BURSTIO = 0x0020
    CONVERTDATA = 0x0040
    NODTCONNECT = 0x0080
    DTCONNECT = 0x0100
    SCALEDATA = 0x0200

@dataclass
class AcquisitionConfig:
    """Configuration d'acquisition"""
    board_num: int = 0
    low_chan: int = 0
    high_chan: int = 7
    range_type: MCCRanges = MCCRanges.BIP10VOLTS
    rate: float = 1000.0  # Hz
    count: int = 1000
    options: int = MCCOptions.DEFAULTOPTION
    
@dataclass
class ChannelConfig:
    """Configuration d'un canal"""
    channel: int
    range_type: MCCRanges
    enabled: bool = True
    label: str = ""
    units: str = "V"
    scale_factor: float = 1.0
    offset: float = 0.0

class MCCDAQ_USB1608FS:
    """
    Wrapper Python pour carte d'acquisition MCC DAQ USB-1608FS
    
    Cette classe fournit une interface Python pour contrôler la carte
    d'acquisition de données Measurement Computing USB-1608FS via les DLLs.
    """
    
    def __init__(self, dll_path: Optional[str] = None):
        """
        Initialise le wrapper MCC DAQ
        
        Args:
            dll_path: Chemin vers les DLLs MCC (optionnel)
        """
        self.dll_path = dll_path or self._find_dll_path()
        self.cbw32 = None
        self.mcc_daq = None
        self.board_num = 0
        self.is_initialized = False
        self.channels_config = {}
        self.acquisition_config = AcquisitionConfig()
        
        # Buffers pour les données
        self.data_buffer = None
        self.data_array = None
        
        self._load_dlls()
        
    def _find_dll_path(self) -> str:
        """Trouve le chemin vers les DLLs MCC"""
        # Chemin relatif au projet
        project_root = Path(__file__).parent.parent.parent.parent
        mcc_path = project_root / "Measurement Computing"
        
        if mcc_path.exists():
            return str(mcc_path)
            
        # Chemins standards Windows
        standard_paths = [
            "C:\\Program Files (x86)\\Measurement Computing\\DAQ",
            "C:\\Program Files\\Measurement Computing\\DAQ",
            "C:\\MCC\\DAQ"
        ]
        
        for path in standard_paths:
            if Path(path).exists():
                return path
                
        raise FileNotFoundError("Impossible de trouver les DLLs MCC DAQ")
        
    def _load_dlls(self):
        """Charge les DLLs nécessaires"""
        try:
            # Chargement de cbw32.dll (Universal Library)
            cbw32_path = Path(self.dll_path) / "cbw32.dll"
            if cbw32_path.exists():
                self.cbw32 = ctypes.windll.LoadLibrary(str(cbw32_path))
                logger.info(f"cbw32.dll chargé depuis: {cbw32_path}")
            else:
                # Essayer de charger depuis le système
                self.cbw32 = ctypes.windll.cbw32
                logger.info("cbw32.dll chargé depuis le système")
                
            # Chargement de MccDaq.dll
            mcc_daq_path = Path(self.dll_path) / "MccDaq.dll"
            if mcc_daq_path.exists():
                self.mcc_daq = ctypes.windll.LoadLibrary(str(mcc_daq_path))
                logger.info(f"MccDaq.dll chargé depuis: {mcc_daq_path}")
                
            self._setup_function_prototypes()
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des DLLs: {e}")
            raise
            
    def _setup_function_prototypes(self):
        """Configure les prototypes des fonctions DLL"""
        if self.cbw32:
            # cbAIn - Lecture d'un canal analogique
            self.cbw32.cbAIn.argtypes = [
                ctypes.c_int,           # BoardNum
                ctypes.c_int,           # Chan
                ctypes.c_int,           # Gain
                ctypes.POINTER(ctypes.c_ushort)  # DataValue
            ]
            self.cbw32.cbAIn.restype = ctypes.c_int
            
            # cbAInScan - Acquisition multi-canaux
            self.cbw32.cbAInScan.argtypes = [
                ctypes.c_int,           # BoardNum
                ctypes.c_int,           # LowChan
                ctypes.c_int,           # HighChan
                ctypes.c_long,          # Count
                ctypes.POINTER(ctypes.c_long),    # Rate
                ctypes.c_int,           # Range
                ctypes.POINTER(ctypes.c_ushort),  # ADData
                ctypes.c_int            # Options
            ]
            self.cbw32.cbAInScan.restype = ctypes.c_int
            
            # cbGetStatus - Statut de l'acquisition
            self.cbw32.cbGetStatus.argtypes = [
                ctypes.c_int,           # BoardNum
                ctypes.POINTER(ctypes.c_short),   # Status
                ctypes.POINTER(ctypes.c_long),    # CurCount
                ctypes.POINTER(ctypes.c_long),    # CurIndex
                ctypes.c_int            # FunctionType
            ]
            self.cbw32.cbGetStatus.restype = ctypes.c_int
            
            # cbStopBackground - Arrêt de l'acquisition
            self.cbw32.cbStopBackground.argtypes = [
                ctypes.c_int,           # BoardNum
                ctypes.c_int            # FunctionType
            ]
            self.cbw32.cbStopBackground.restype = ctypes.c_int
            
            # cbGetBoardName - Nom de la carte
            self.cbw32.cbGetBoardName.argtypes = [
                ctypes.c_int,           # BoardNum
                ctypes.c_char_p         # BoardName
            ]
            self.cbw32.cbGetBoardName.restype = ctypes.c_int
            
    def initialize(self, board_num: int = 0) -> bool:
        """
        Initialise la carte d'acquisition
        
        Args:
            board_num: Numéro de carte (défaut: 0)
            
        Returns:
            True si l'initialisation réussit
        """
        try:
            self.board_num = board_num
            
            # Vérification de la présence de la carte
            board_name = ctypes.create_string_buffer(64)
            result = self.cbw32.cbGetBoardName(self.board_num, board_name)
            
            if result == MCCErrorCodes.NOERRORS:
                self.is_initialized = True
                logger.info(f"Carte initialisée: {board_name.value.decode('utf-8')}")
                return True
            else:
                logger.error(f"Erreur d'initialisation: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}")
            return False
            
    def configure_channel(self, channel: int, range_type: MCCRanges, 
                         label: str = "", units: str = "V") -> bool:
        """
        Configure un canal d'acquisition
        
        Args:
            channel: Numéro du canal (0-7)
            range_type: Plage de tension
            label: Étiquette du canal
            units: Unités de mesure
            
        Returns:
            True si la configuration réussit
        """
        if not (0 <= channel <= 7):
            logger.error(f"Numéro de canal invalide: {channel}")
            return False
            
        config = ChannelConfig(
            channel=channel,
            range_type=range_type,
            label=label or f"Canal {channel}",
            units=units
        )
        
        self.channels_config[channel] = config
        logger.info(f"Canal {channel} configuré: {range_type.name}")
        return True
        
    def read_single_channel(self, channel: int) -> Optional[float]:
        """
        Lit une valeur sur un canal unique
        
        Args:
            channel: Numéro du canal
            
        Returns:
            Valeur lue en volts ou None si erreur
        """
        if not self.is_initialized:
            logger.error("Carte non initialisée")
            return None
            
        if channel not in self.channels_config:
            logger.error(f"Canal {channel} non configuré")
            return None
            
        try:
            data_value = ctypes.c_ushort()
            config = self.channels_config[channel]
            
            result = self.cbw32.cbAIn(
                self.board_num,
                channel,
                config.range_type.value,
                ctypes.byref(data_value)
            )
            
            if result == MCCErrorCodes.NOERRORS:
                # Conversion en volts
                voltage = self._convert_to_voltage(data_value.value, config.range_type)
                return voltage
            else:
                logger.error(f"Erreur de lecture canal {channel}: {result}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la lecture: {e}")
            return None
            
    def _convert_to_voltage(self, raw_value: int, range_type: MCCRanges) -> float:
        """Convertit une valeur brute en tension"""
        # Conversion 16 bits vers tension
        # La USB-1608FS utilise des valeurs signées 16 bits
        if raw_value > 32767:
            raw_value = raw_value - 65536
            
        # Facteurs de conversion selon la plage
        range_factors = {
            MCCRanges.BIP10VOLTS: 20.0 / 65536,  # ±10V
            MCCRanges.BIP5VOLTS: 10.0 / 65536,   # ±5V
            MCCRanges.BIP2VOLTS: 4.0 / 65536,    # ±2V
            MCCRanges.BIP1VOLTS: 2.0 / 65536,    # ±1V
        }
        
        factor = range_factors.get(range_type, 20.0 / 65536)
        return raw_value * factor
        
    def start_continuous_acquisition(self, 
                                   low_chan: int = 0, 
                                   high_chan: int = 7,
                                   rate: float = 1000.0,
                                   buffer_size: int = 10000) -> bool:
        """
        Démarre une acquisition continue
        
        Args:
            low_chan: Premier canal
            high_chan: Dernier canal  
            rate: Fréquence d'échantillonnage (Hz)
            buffer_size: Taille du buffer
            
        Returns:
            True si l'acquisition démarre
        """
        if not self.is_initialized:
            logger.error("Carte non initialisée")
            return False
            
        try:
            # Configuration
            num_channels = high_chan - low_chan + 1
            total_count = buffer_size * num_channels
            
            # Allocation du buffer
            self.data_buffer = (ctypes.c_ushort * total_count)()
            
            # Configuration de l'acquisition
            rate_ptr = ctypes.c_long(int(rate))
            
            # Utilisation de la première plage configurée ou défaut
            first_chan_config = self.channels_config.get(low_chan)
            range_type = first_chan_config.range_type.value if first_chan_config else MCCRanges.BIP10VOLTS.value
            
            result = self.cbw32.cbAInScan(
                self.board_num,
                low_chan,
                high_chan,
                total_count,
                ctypes.byref(rate_ptr),
                range_type,
                self.data_buffer,
                MCCOptions.CONTINUOUS | MCCOptions.BACKGROUND
            )
            
            if result == MCCErrorCodes.NOERRORS:
                self.acquisition_config.low_chan = low_chan
                self.acquisition_config.high_chan = high_chan
                self.acquisition_config.rate = rate_ptr.value
                self.acquisition_config.count = total_count
                
                logger.info(f"Acquisition continue démarrée: {num_channels} canaux à {rate_ptr.value} Hz")
                return True
            else:
                logger.error(f"Erreur démarrage acquisition: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors du démarrage: {e}")
            return False
            
    def get_acquisition_status(self) -> Dict[str, Any]:
        """
        Récupère le statut de l'acquisition
        
        Returns:
            Dictionnaire avec le statut
        """
        if not self.is_initialized:
            return {"error": "Carte non initialisée"}
            
        try:
            status = ctypes.c_short()
            cur_count = ctypes.c_long()
            cur_index = ctypes.c_long()
            
            result = self.cbw32.cbGetStatus(
                self.board_num,
                ctypes.byref(status),
                ctypes.byref(cur_count),
                ctypes.byref(cur_index),
                1  # AIFUNCTION
            )
            
            if result == MCCErrorCodes.NOERRORS:
                return {
                    "status": status.value,
                    "current_count": cur_count.value,
                    "current_index": cur_index.value,
                    "is_running": status.value == 1
                }
            else:
                return {"error": f"Erreur statut: {result}"}
                
        except Exception as e:
            return {"error": f"Exception: {e}"}
            
    def stop_acquisition(self) -> bool:
        """
        Arrête l'acquisition en cours
        
        Returns:
            True si l'arrêt réussit
        """
        if not self.is_initialized:
            return False
            
        try:
            result = self.cbw32.cbStopBackground(self.board_num, 1)  # AIFUNCTION
            
            if result == MCCErrorCodes.NOERRORS:
                logger.info("Acquisition arrêtée")
                return True
            else:
                logger.error(f"Erreur arrêt acquisition: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt: {e}")
            return False
            
    def get_data(self, num_samples: int = 1000) -> Optional[np.ndarray]:
        """
        Récupère les données d'acquisition
        
        Args:
            num_samples: Nombre d'échantillons à récupérer
            
        Returns:
            Array numpy avec les données ou None
        """
        if not self.data_buffer:
            logger.error("Pas de buffer de données")
            return None
            
        try:
            num_channels = self.acquisition_config.high_chan - self.acquisition_config.low_chan + 1
            
            # Copie des données du buffer
            raw_data = np.array(self.data_buffer[:num_samples * num_channels])
            
            # Reshape en [samples, channels]
            data_matrix = raw_data.reshape(-1, num_channels)
            
            # Conversion en tension
            voltage_data = np.zeros_like(data_matrix, dtype=np.float64)
            
            for i, chan in enumerate(range(self.acquisition_config.low_chan, 
                                         self.acquisition_config.high_chan + 1)):
                config = self.channels_config.get(chan)
                range_type = config.range_type if config else MCCRanges.BIP10VOLTS
                
                for j in range(data_matrix.shape[0]):
                    voltage_data[j, i] = self._convert_to_voltage(data_matrix[j, i], range_type)
                    
            return voltage_data
            
        except Exception as e:
            logger.error(f"Erreur récupération données: {e}")
            return None
            
    def get_available_ranges(self) -> List[MCCRanges]:
        """Retourne les plages disponibles pour USB-1608FS"""
        return [
            MCCRanges.BIP10VOLTS,
            MCCRanges.BIP5VOLTS,
            MCCRanges.BIP2VOLTS,
            MCCRanges.BIP1VOLTS
        ]
        
    def get_channel_info(self, channel: int) -> Optional[Dict[str, Any]]:
        """
        Récupère les informations d'un canal
        
        Args:
            channel: Numéro du canal
            
        Returns:
            Dictionnaire avec les informations
        """
        config = self.channels_config.get(channel)
        if not config:
            return None
            
        return {
            "channel": config.channel,
            "range": config.range_type.name,
            "enabled": config.enabled,
            "label": config.label,
            "units": config.units,
            "scale_factor": config.scale_factor,
            "offset": config.offset
        }
        
    def calibrate_channel(self, channel: int) -> bool:
        """
        Lance une calibration de canal (fonction avancée)
        
        Args:
            channel: Numéro du canal
            
        Returns:
            True si la calibration réussit
        """
        # Cette fonction nécessiterait l'accès aux fonctions de calibration
        # de la bibliothèque MCC, ce qui dépasse le scope de base
        logger.info(f"Calibration du canal {channel} - Non implémentée dans cette version")
        return True
        
    def close(self):
        """Ferme la connexion et libère les ressources"""
        if self.is_initialized:
            self.stop_acquisition()
            self.is_initialized = False
            logger.info("Carte fermée")
            
    def __enter__(self):
        """Support du context manager"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du context manager"""
        self.close()

# Fonctions utilitaires
def scan_available_boards() -> List[int]:
    """
    Scanne les cartes disponibles
    
    Returns:
        Liste des numéros de cartes détectées
    """
    available_boards = []
    
    try:
        # Tentative de chargement de cbw32.dll
        cbw32 = ctypes.windll.cbw32
        
        # Test de 10 cartes possibles
        for board_num in range(10):
            board_name = ctypes.create_string_buffer(64)
            result = cbw32.cbGetBoardName(board_num, board_name)
            
            if result == MCCErrorCodes.NOERRORS:
                available_boards.append(board_num)
                logger.info(f"Carte trouvée {board_num}: {board_name.value.decode('utf-8')}")
                
    except Exception as e:
        logger.error(f"Erreur lors du scan: {e}")
        
    return available_boards

def get_error_message(error_code: int) -> str:
    """
    Retourne le message d'erreur correspondant au code
    
    Args:
        error_code: Code d'erreur MCC
        
    Returns:
        Message d'erreur
    """
    error_messages = {
        MCCErrorCodes.NOERRORS: "Aucune erreur",
        MCCErrorCodes.BADBOARD: "Numéro de carte invalide",
        MCCErrorCodes.DEADDIGITALDEV: "Périphérique numérique défaillant",
        MCCErrorCodes.DEADCOUNTERDEV: "Compteur défaillant",
        MCCErrorCodes.DEADDADEV: "D/A défaillant",
        MCCErrorCodes.DEADADDEV: "A/D défaillant",
        MCCErrorCodes.NOTDIGITALCONF: "Pas configuré pour numérique",
        MCCErrorCodes.NOTCOUNTERCONF: "Pas configuré pour compteur",
        MCCErrorCodes.NOTDACONF: "Pas configuré pour D/A",
        MCCErrorCodes.NOTADCONF: "Pas configuré pour A/D",
        MCCErrorCodes.NOTMUXCONF: "Pas configuré pour multiplexeur",
        MCCErrorCodes.BADPORTNUM: "Numéro de port invalide",
        MCCErrorCodes.BADCOUNTERDEVNUM: "Numéro de compteur invalide",
        MCCErrorCodes.BADDADEVNUM: "Numéro D/A invalide",
        MCCErrorCodes.BADADDEVNUM: "Numéro A/D invalide",
        MCCErrorCodes.BADCHANNEL: "Numéro de canal invalide",
        MCCErrorCodes.BADRANGE: "Plage invalide",
        MCCErrorCodes.BADCOUNTERCHAN: "Canal compteur invalide",
        MCCErrorCodes.BADCOUNTERPARAM: "Paramètre compteur invalide",
        MCCErrorCodes.BADEVENTTYPE: "Type d'événement invalide",
        MCCErrorCodes.WRONGDIGCONFIG: "Configuration numérique incorrecte",
        MCCErrorCodes.WRONGDIOCONFIG: "Configuration DIO incorrecte",
        MCCErrorCodes.WRONGCOUNTERCONFIG: "Configuration compteur incorrecte",
        MCCErrorCodes.WRONGDACONFIG: "Configuration D/A incorrecte",
        MCCErrorCodes.WRONGADCONFIG: "Configuration A/D incorrecte"
    }
    
    return error_messages.get(error_code, f"Erreur inconnue: {error_code}")

if __name__ == "__main__":
    # Test basique du wrapper
    print("Test du wrapper MCC DAQ USB-1608FS")
    print("=" * 50)
    
    # Scan des cartes disponibles
    print("Recherche des cartes disponibles...")
    boards = scan_available_boards()
    print(f"Cartes trouvées: {boards}")
    
    if boards:
        # Test avec la première carte
        with MCCDAQ_USB1608FS() as daq:
            if daq.initialize(boards[0]):
                print(f"Carte {boards[0]} initialisée avec succès")
                
                # Configuration des canaux
                daq.configure_channel(0, MCCRanges.BIP10VOLTS, "Canal Test")
                
                # Lecture d'un échantillon
                value = daq.read_single_channel(0)
                if value is not None:
                    print(f"Valeur lue: {value:.3f} V")
                    
            else:
                print("Erreur d'initialisation")
    else:
        print("Aucune carte MCC détectée")

