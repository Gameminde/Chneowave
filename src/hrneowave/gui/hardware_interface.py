"""
Module de détection et interface hardware pour HRNeoWave
Supporte les cartes d'acquisition USB/RS232/HID standards
"""

import sys
import time
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Dépendances hardware
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("⚠️ pyserial non installé - support RS232/USB-série désactivé")

try:
    import hid
    HID_AVAILABLE = True
except ImportError:
    HID_AVAILABLE = False
    print("⚠️ hidapi non installé - support USB-HID désactivé")

try:
    import nidaqmx
    import nidaqmx.system
    NIDAQ_AVAILABLE = True
except ImportError:
    NIDAQ_AVAILABLE = False
    print("⚠️ nidaqmx non installé - support NI-DAQ désactivé")


class DeviceType(Enum):
    """Types de périphériques supportés"""
    SERIAL_USB = "USB-Série"
    SERIAL_RS232 = "RS232"
    USB_HID = "USB-HID"
    NI_DAQ = "NI-DAQmx"
    SIMULATION = "Simulation"


@dataclass
class AcquisitionDevice:
    """Représente un périphérique d'acquisition détecté"""
    device_type: DeviceType
    port_name: str
    description: str
    vendor_id: Optional[int] = None
    product_id: Optional[int] = None
    serial_number: Optional[str] = None
    max_channels: int = 16
    sampling_rate_max: int = 10000  # Hz


class HardwareInterface:
    """
    Interface unifiée pour l'acquisition hardware
    Détecte automatiquement les cartes connectées et gère la communication
    """
    
    # Identifiants USB connus pour cartes d'acquisition courantes
    KNOWN_DEVICES = {
        # Format: (VID, PID): (description, max_channels)
        (0x0403, 0x6001): ("FTDI USB-Serial", 8),      # FTDI FT232
        (0x0403, 0x6014): ("FTDI FT232H", 16),         # FTDI haute vitesse
        (0x2341, 0x0043): ("Arduino Uno", 6),          # Arduino Uno
        (0x2341, 0x0010): ("Arduino Mega", 16),        # Arduino Mega
        (0x0483, 0x5740): ("STM32 Virtual COM", 12),   # STM32
        (0x10C4, 0xEA60): ("Silicon Labs CP210x", 8),  # CP2102
        (0x067B, 0x2303): ("Prolific PL2303", 4),      # PL2303
    }
    
    def __init__(self, simulation_mode: bool = False):
        """
        Initialise l'interface hardware
        
        Args:
            simulation_mode: Si True, utilise des données simulées
        """
        self.simulation_mode = simulation_mode
        self.connected_device: Optional[AcquisitionDevice] = None
        self.serial_conn = None
        self.hid_device = None
        self.daq_task = None
        self.channel_offsets = np.zeros(16)  # Offset par canal pour calibration
        self.channel_gains = np.ones(16)     # Gain par canal pour calibration
        
    def scan_devices(self) -> List[AcquisitionDevice]:
        """
        Scanne tous les périphériques d'acquisition disponibles
        
        Returns:
            Liste des périphériques détectés
        """
        devices = []
        
        # 1. Scanner les ports série (USB-Serial et RS232)
        if SERIAL_AVAILABLE:
            try:
                for port in serial.tools.list_ports.comports():
                    device_type = DeviceType.SERIAL_USB if "USB" in port.description else DeviceType.SERIAL_RS232
                    
                    # Extraire VID/PID si disponible
                    vid = port.vid if hasattr(port, 'vid') else None
                    pid = port.pid if hasattr(port, 'pid') else None
                    
                    # Vérifier si c'est un périphérique connu
                    max_channels = 8  # Par défaut
                    description = port.description
                    
                    if vid and pid and (vid, pid) in self.KNOWN_DEVICES:
                        known_desc, max_channels = self.KNOWN_DEVICES[(vid, pid)]
                        description = f"{known_desc} - {port.description}"
                    
                    device = AcquisitionDevice(
                        device_type=device_type,
                        port_name=port.device,
                        description=description,
                        vendor_id=vid,
                        product_id=pid,
                        serial_number=port.serial_number if hasattr(port, 'serial_number') else None,
                        max_channels=max_channels
                    )
                    devices.append(device)
                    print(f"✅ Détecté: {description} sur {port.device}")
                    
            except Exception as e:
                print(f"❌ Erreur scan ports série: {e}")
        
        # 2. Scanner les périphériques HID
        if HID_AVAILABLE:
            try:
                for device_info in hid.enumerate():
                    vid = device_info['vendor_id']
                    pid = device_info['product_id']
                    
                    # Filtrer les périphériques non pertinents (souris, claviers...)
                    if vid == 0 or pid == 0:
                        continue
                        
                    # Vérifier si c'est une carte d'acquisition connue
                    if (vid, pid) in self.KNOWN_DEVICES:
                        known_desc, max_channels = self.KNOWN_DEVICES[(vid, pid)]
                        
                        device = AcquisitionDevice(
                            device_type=DeviceType.USB_HID,
                            port_name=device_info['path'].decode() if isinstance(device_info['path'], bytes) else device_info['path'],
                            description=f"{known_desc} (HID)",
                            vendor_id=vid,
                            product_id=pid,
                            serial_number=device_info['serial_number'],
                            max_channels=max_channels
                        )
                        devices.append(device)
                        print(f"✅ Détecté HID: {known_desc}")
                        
            except Exception as e:
                print(f"❌ Erreur scan HID: {e}")
        
        # 3. Scanner les cartes NI-DAQ
        if NIDAQ_AVAILABLE:
            try:
                system = nidaqmx.system.System.local()
                for device in system.devices:
                    device_obj = AcquisitionDevice(
                        device_type=DeviceType.NI_DAQ,
                        port_name=device.name,
                        description=f"NI {device.product_type}",
                        serial_number=str(device.serial_num),
                        max_channels=len(device.ai_physical_chans)
                    )
                    devices.append(device_obj)
                    print(f"✅ Détecté NI-DAQ: {device.product_type}")
                    
            except Exception as e:
                print(f"❌ Erreur scan NI-DAQ: {e}")
        
        # 4. Ajouter option simulation si aucun périphérique
        if not devices or self.simulation_mode:
            sim_device = AcquisitionDevice(
                device_type=DeviceType.SIMULATION,
                port_name="SIM",
                description="Mode Simulation (données de test)",
                max_channels=16
            )
            devices.append(sim_device)
        
        print(f"\n📊 Total: {len(devices)} périphérique(s) détecté(s)")
        return devices
    
    def connect(self, device: AcquisitionDevice, baudrate: int = 115200) -> bool:
        """
        Se connecte au périphérique sélectionné
        
        Args:
            device: Périphérique à connecter
            baudrate: Vitesse pour connexions série
            
        Returns:
            True si connexion réussie
        """
        try:
            self.disconnect()  # Fermer toute connexion existante
            self.connected_device = device
            
            if device.device_type in [DeviceType.SERIAL_USB, DeviceType.SERIAL_RS232]:
                self.serial_conn = serial.Serial(
                    port=device.port_name,
                    baudrate=baudrate,
                    timeout=1.0,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE
                )
                print(f"✅ Connecté à {device.port_name} @ {baudrate} baud")
                
                # Envoyer commande d'initialisation
                self._send_init_commands()
                return True
                
            elif device.device_type == DeviceType.USB_HID:
                self.hid_device = hid.device()
                self.hid_device.open(device.vendor_id, device.product_id)
                self.hid_device.set_nonblocking(True)
                print(f"✅ Connecté en HID à {device.description}")
                return True
                
            elif device.device_type == DeviceType.NI_DAQ:
                # Configuration basique NI-DAQ
                self.daq_task = nidaqmx.Task()
                # Ajouter les canaux analogiques disponibles
                channels = f"{device.port_name}/ai0:{device.max_channels-1}"
                self.daq_task.ai_channels.add_ai_voltage_chan(channels)
                print(f"✅ Connecté à NI-DAQ {device.description}")
                return True
                
            elif device.device_type == DeviceType.SIMULATION:
                print("✅ Mode simulation activé")
                return True
                
        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            self.connected_device = None
            return False
    
    def disconnect(self):
        """Déconnecte le périphérique actuel"""
        try:
            if self.serial_conn:
                self.serial_conn.close()
                self.serial_conn = None
                
            if self.hid_device:
                self.hid_device.close()
                self.hid_device = None
                
            if self.daq_task:
                self.daq_task.close()
                self.daq_task = None
                
            self.connected_device = None
            print("🔌 Déconnecté")
            
        except Exception as e:
            print(f"⚠️ Erreur déconnexion: {e}")
    
    def read_channel(self, channel: int) -> float:
        """
        Lit la valeur d'un canal spécifique
        
        Args:
            channel: Numéro du canal (0-15)
            
        Returns:
            Valeur lue en Volts
        """
        if not self.connected_device:
            raise RuntimeError("Aucun périphérique connecté")
            
        if channel >= self.connected_device.max_channels:
            raise ValueError(f"Canal {channel} invalide (max: {self.connected_device.max_channels-1})")
        
        try:
            if self.connected_device.device_type == DeviceType.SIMULATION:
                # Générer données de test réalistes
                t = time.time()
                # Signal principal + bruit + dérive
                signal = (2.5 + 0.8 * np.sin(2 * np.pi * 0.5 * t + channel * np.pi/8) +
                         0.1 * np.random.randn() + 
                         0.01 * np.sin(2 * np.pi * 0.01 * t))
                return signal
                
            elif self.serial_conn:
                # Protocole série simple: "READ:CH{n}\n"
                cmd = f"READ:CH{channel}\n"
                self.serial_conn.write(cmd.encode())
                response = self.serial_conn.readline().decode().strip()
                
                # Parser la réponse (format attendu: "CH0:2.543V")
                if f"CH{channel}:" in response:
                    value_str = response.split(':')[1].replace('V', '')
                    return float(value_str)
                else:
                    raise ValueError(f"Réponse invalide: {response}")
                    
            elif self.hid_device:
                # Protocole HID: envoyer requête, lire réponse
                report = [0x00] * 64  # Report HID standard
                report[0] = 0x01      # Report ID
                report[1] = 0x10      # Commande READ
                report[2] = channel   # Numéro canal
                
                self.hid_device.write(report)
                time.sleep(0.001)  # Petit délai
                
                data = self.hid_device.read(64, timeout_ms=100)
                if data and len(data) >= 4:
                    # Convertir bytes en float (little-endian)
                    value_bytes = bytes(data[2:6])
                    value = np.frombuffer(value_bytes, dtype=np.float32)[0]
                    return value
                    
            elif self.daq_task:
                # Lecture NI-DAQ
                data = self.daq_task.read()
                if isinstance(data, list):
                    return data[channel]
                else:
                    return data
                    
        except Exception as e:
            print(f"❌ Erreur lecture canal {channel}: {e}")
            return 0.0
    
    def read_all_channels(self) -> List[float]:
        """
        Lit tous les canaux simultanément
        
        Returns:
            Liste des valeurs pour chaque canal
        """
        if not self.connected_device:
            raise RuntimeError("Aucun périphérique connecté")
            
        values = []
        n_channels = self.connected_device.max_channels
        
        try:
            if self.connected_device.device_type == DeviceType.SIMULATION:
                # Lecture simultanée simulée
                t = time.time()
                for ch in range(n_channels):
                    signal = (2.5 + 0.8 * np.sin(2 * np.pi * 0.5 * t + ch * np.pi/8) +
                             0.1 * np.random.randn())
                    values.append(signal)
                    
            elif self.serial_conn:
                # Commande de lecture groupée
                self.serial_conn.write(b"READ:ALL\n")
                response = self.serial_conn.readline().decode().strip()
                
                # Parser réponse (format: "2.54,2.48,2.51,...")
                values = [float(v) for v in response.split(',')[:n_channels]]
                
            elif self.daq_task:
                # NI-DAQ supporte la lecture simultanée native
                values = self.daq_task.read()
                if not isinstance(values, list):
                    values = [values]
                    
            else:
                # Lecture séquentielle par défaut
                for ch in range(n_channels):
                    values.append(self.read_channel(ch))
                    
        except Exception as e:
            print(f"❌ Erreur lecture multi-canaux: {e}")
            values = [0.0] * n_channels
            
        return values
    
    def configure_sampling(self, frequency: int, channels: List[int]) -> bool:
        """
        Configure l'acquisition pour les canaux spécifiés
        
        Args:
            frequency: Fréquence d'échantillonnage en Hz
            channels: Liste des canaux à activer
            
        Returns:
            True si configuration réussie
        """
        if not self.connected_device:
            return False
            
        try:
            if self.serial_conn:
                # Configuration via commandes série
                cmd = f"CONFIG:RATE:{frequency}\n"
                self.serial_conn.write(cmd.encode())
                
                # Activer les canaux sélectionnés
                ch_mask = sum(1 << ch for ch in channels)
                cmd = f"CONFIG:CHANNELS:{ch_mask:04X}\n"
                self.serial_conn.write(cmd.encode())
                
                # Vérifier ACK
                response = self.serial_conn.readline().decode().strip()
                return response == "OK"
                
            elif self.daq_task:
                # Reconfigurer la tâche NI-DAQ
                self.daq_task.timing.cfg_samp_clk_timing(frequency)
                return True
                
            else:
                # Simulation toujours OK
                return True
                
        except Exception as e:
            print(f"❌ Erreur configuration: {e}")
            return False
    
    def _send_init_commands(self):
        """Envoie les commandes d'initialisation au périphérique série"""
        if not self.serial_conn:
            return
            
        init_commands = [
            b"*IDN?\n",           # Identification
            b"RESET\n",           # Reset
            b"CONFIG:MODE:CONT\n" # Mode continu
        ]
        
        for cmd in init_commands:
            try:
                self.serial_conn.write(cmd)
                time.sleep(0.05)
                if self.serial_conn.in_waiting:
                    response = self.serial_conn.readline().decode().strip()
                    print(f"  → {response}")
            except:
                pass
    
    def apply_calibration(self, channel: int, offset: float, gain: float):
        """
        Applique les paramètres de calibration à un canal
        
        Args:
            channel: Numéro du canal
            offset: Offset à soustraire
            gain: Gain multiplicateur
        """
        if channel < 16:
            self.channel_offsets[channel] = offset
            self.channel_gains[channel] = gain
    
    def get_calibrated_value(self, channel: int, raw_value: float) -> float:
        """
        Applique la calibration à une valeur brute
        
        Args:
            channel: Numéro du canal
            raw_value: Valeur brute en Volts
            
        Returns:
            Valeur calibrée
        """
        return (raw_value - self.channel_offsets[channel]) * self.channel_gains[channel] 