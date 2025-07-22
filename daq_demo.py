#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAQ Demo - CHNeoWave
LOT B - Driver-démo DAQ

Usage: python daq_demo.py --fs 32 --channels 8
→ émet vers stdout un bloc JSON {timestamp, values:[...]}

Génère sinusoïde + bruit.
Importe nidaqmx uniquement si présent, sinon simulate.
"""

import argparse
import json
import time
import numpy as np
import sys
from datetime import datetime

try:
    import nidaqmx
    from nidaqmx.constants import AcquisitionType
    NIDAQMX_AVAILABLE = True
except ImportError:
    NIDAQMX_AVAILABLE = False

class DAQDemo:
    """
    Démonstrateur d'acquisition de données
    Simule ou utilise NI-DAQmx selon disponibilité
    """
    
    def __init__(self, fs=32, channels=8, use_hardware=False):
        self.fs = fs  # Fréquence d'échantillonnage
        self.channels = channels  # Nombre de canaux
        self.use_hardware = use_hardware and NIDAQMX_AVAILABLE
        self.running = False
        
        # Paramètres de simulation
        self.time_offset = 0
        self.frequencies = np.random.uniform(0.5, 5.0, channels)  # Fréquences aléatoires
        self.amplitudes = np.random.uniform(0.1, 1.0, channels)   # Amplitudes aléatoires
        self.phases = np.random.uniform(0, 2*np.pi, channels)     # Phases aléatoires
        
        if self.use_hardware:
            self.setup_hardware()
        
    def setup_hardware(self):
        """
        Configuration du matériel NI-DAQmx
        """
        try:
            self.task = nidaqmx.Task()
            # Configuration des canaux analogiques
            for i in range(self.channels):
                self.task.ai_channels.add_ai_voltage_chan(f"Dev1/ai{i}")
            
            # Configuration du timing
            self.task.timing.cfg_samp_clk_timing(
                rate=self.fs,
                sample_mode=AcquisitionType.CONTINUOUS
            )
            
            print(f"Hardware NI-DAQmx configuré: {self.channels} canaux @ {self.fs} Hz", 
                  file=sys.stderr)
            
        except Exception as e:
            print(f"Erreur configuration hardware: {e}", file=sys.stderr)
            print("Basculement en mode simulation", file=sys.stderr)
            self.use_hardware = False
    
    def generate_simulated_data(self):
        """
        Génère des données simulées (sinusoïdes + bruit)
        """
        current_time = time.time()
        dt = 1.0 / self.fs
        
        values = []
        for i in range(self.channels):
            # Sinusoïde avec bruit
            signal = (self.amplitudes[i] * 
                     np.sin(2 * np.pi * self.frequencies[i] * current_time + self.phases[i]))
            noise = np.random.normal(0, 0.05)  # Bruit gaussien
            values.append(signal + noise)
        
        return values
    
    def read_hardware_data(self):
        """
        Lecture des données depuis le matériel NI-DAQmx
        """
        try:
            # Lecture d'un échantillon par canal
            data = self.task.read(number_of_samples_per_channel=1)
            if isinstance(data[0], list):
                # Données multi-canaux
                return [channel_data[0] for channel_data in data]
            else:
                # Canal unique
                return [data]
        except Exception as e:
            print(f"Erreur lecture hardware: {e}", file=sys.stderr)
            return self.generate_simulated_data()
    
    def acquire_sample(self):
        """
        Acquiert un échantillon de données
        """
        timestamp = datetime.now().isoformat()
        
        if self.use_hardware:
            values = self.read_hardware_data()
        else:
            values = self.generate_simulated_data()
        
        return {
            "timestamp": timestamp,
            "values": values,
            "fs": self.fs,
            "channels": self.channels,
            "source": "hardware" if self.use_hardware else "simulation"
        }
    
    def start_continuous_acquisition(self):
        """
        Démarre l'acquisition continue
        """
        self.running = True
        
        if self.use_hardware:
            try:
                self.task.start()
            except Exception as e:
                print(f"Erreur démarrage hardware: {e}", file=sys.stderr)
                self.use_hardware = False
        
        print(f"Acquisition démarrée: {self.channels} canaux @ {self.fs} Hz", 
              file=sys.stderr)
        print(f"Mode: {'Hardware' if self.use_hardware else 'Simulation'}", 
              file=sys.stderr)
        
        try:
            while self.running:
                sample = self.acquire_sample()
                print(json.dumps(sample, ensure_ascii=False))
                sys.stdout.flush()
                
                # Attente pour respecter la fréquence d'échantillonnage
                time.sleep(1.0 / self.fs)
                
        except KeyboardInterrupt:
            print("\nArrêt demandé par l'utilisateur", file=sys.stderr)
        finally:
            self.stop()
    
    def stop(self):
        """
        Arrête l'acquisition
        """
        self.running = False
        
        if self.use_hardware and hasattr(self, 'task'):
            try:
                self.task.stop()
                self.task.close()
            except Exception as e:
                print(f"Erreur arrêt hardware: {e}", file=sys.stderr)
        
        print("Acquisition arrêtée", file=sys.stderr)

def main():
    """
    Point d'entrée principal
    """
    parser = argparse.ArgumentParser(
        description="DAQ Demo - CHNeoWave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python daq_demo.py --fs 32 --channels 8
  python daq_demo.py --fs 100 --channels 4 --hardware
  python daq_demo.py --fs 32 --channels 8 | chneowave cli --stdin
"""
    )
    
    parser.add_argument(
        "--fs", 
        type=int, 
        default=32,
        help="Fréquence d'échantillonnage (Hz) [défaut: 32]"
    )
    
    parser.add_argument(
        "--channels", 
        type=int, 
        default=8,
        help="Nombre de canaux [défaut: 8]"
    )
    
    parser.add_argument(
        "--hardware", 
        action="store_true",
        help="Utiliser le matériel NI-DAQmx si disponible"
    )
    
    parser.add_argument(
        "--single", 
        action="store_true",
        help="Acquérir un seul échantillon puis quitter"
    )
    
    args = parser.parse_args()
    
    # Validation des paramètres
    if args.fs <= 0 or args.fs > 10000:
        print("Erreur: Fréquence d'échantillonnage invalide (1-10000 Hz)", file=sys.stderr)
        sys.exit(1)
    
    if args.channels <= 0 or args.channels > 32:
        print("Erreur: Nombre de canaux invalide (1-32)", file=sys.stderr)
        sys.exit(1)
    
    # Création et démarrage du démonstrateur
    daq = DAQDemo(fs=args.fs, channels=args.channels, use_hardware=args.hardware)
    
    if args.single:
        # Acquisition d'un seul échantillon
        sample = daq.acquire_sample()
        print(json.dumps(sample, ensure_ascii=False))
    else:
        # Acquisition continue
        daq.start_continuous_acquisition()

if __name__ == "__main__":
    main()