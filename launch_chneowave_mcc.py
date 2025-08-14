#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement de CHNeoWave avec backend MCC
"""

import sys
import os
import logging
import json
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hrneowave.hardware.manager import HardwareManager
from hrneowave.hardware.backends.mcc_backend import MCCBackend

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_mcc_config():
    """Crée une configuration pour le backend MCC"""
    config = {
        'hardware': {
            'backend': 'mcc',
            'settings': {
                'sample_rate': 32,
                'channels': 8,
                'device_id': 0,
                'voltage_range': (-10.0, 10.0),
                'buffer_size': 1024
            }
        },
        'acquisition': {
            'duration': 60,  # secondes
            'auto_save': True,
            'save_format': 'hdf5'
        },
        'calibration': {
            'points': 5,
            'min_r2': 0.995
        }
    }
    return config

def check_mcc_availability():
    """Vérifie la disponibilité du backend MCC"""
    print("🔍 Vérification de la disponibilité du backend MCC...")
    
    if MCCBackend.is_available():
        print("✅ Backend MCC disponible")
        
        # Détecter les cartes
        devices = MCCBackend.detect_devices()
        print(f"📊 Cartes MCC détectées: {len(devices)}")
        
        for device in devices:
            print(f"   - {device['name']} (ID: {device['id']})")
        
        return True
    else:
        print("❌ Backend MCC non disponible")
        print("   Vérifiez que les DLLs Measurement Computing sont présentes")
        return False

def test_mcc_connection():
    """Teste la connexion avec la carte MCC"""
    print("\n🔌 Test de connexion avec la carte MCC...")
    
    config = create_mcc_config()
    
    try:
        # Créer le gestionnaire de matériel
        manager = HardwareManager(config)
        backend = manager.get_backend()
        
        if not backend:
            print("❌ Impossible d'obtenir le backend MCC")
            return False
        
        # Tester l'ouverture de connexion
        if backend.open():
            print("✅ Connexion MCC établie")
            
            # Configuration de base
            backend.configure_acquisition(32, 512)
            backend.configure_channels([{'id': i} for i in range(4)])
            
            # Test rapide d'acquisition
            backend.start()
            import time
            time.sleep(1)
            
            data = backend.read()
            if data.size > 0:
                print(f"✅ Données acquises: {data.shape}")
            else:
                print("⚠️  Aucune donnée reçue")
            
            backend.stop()
            backend.close()
            
            print("✅ Test de connexion réussi")
            return True
        else:
            print("❌ Échec de la connexion MCC")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")
        return False

def launch_chneowave_with_mcc():
    """Lance CHNeoWave avec le backend MCC"""
    print("\n🚀 Lancement de CHNeoWave avec backend MCC...")
    
    # Vérifier la disponibilité
    if not check_mcc_availability():
        print("❌ Impossible de lancer CHNeoWave - Backend MCC non disponible")
        return False
    
    # Tester la connexion
    if not test_mcc_connection():
        print("❌ Impossible de lancer CHNeoWave - Échec de connexion MCC")
        return False
    
    # Configuration pour le lancement
    config = create_mcc_config()
    
    try:
        # Créer le gestionnaire de matériel
        manager = HardwareManager(config)
        
        print("✅ CHNeoWave configuré avec backend MCC")
        print("📋 Configuration:")
        print(f"   - Backend: {config['hardware']['backend']}")
        print(f"   - Fréquence: {config['hardware']['settings']['sample_rate']} Hz")
        print(f"   - Canaux: {config['hardware']['settings']['channels']}")
        print(f"   - Plage: {config['hardware']['settings']['voltage_range']}")
        
        # Ici, vous pouvez lancer l'interface graphique de CHNeoWave
        # Pour l'instant, on simule le lancement
        print("\n🎯 CHNeoWave est prêt à être utilisé avec la carte MCC!")
        print("   L'interface graphique peut maintenant être lancée.")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 70)
    print("🌊 CHNeoWave - Lancement avec Backend MCC")
    print("=" * 70)
    
    print("📋 Objectif: Lancer CHNeoWave avec support des cartes Measurement Computing")
    print("🔧 Backend: MCC (Measurement Computing)")
    print("📊 Fonctionnalités: Acquisition temps réel, calibration, analyse")
    
    # Vérifications préliminaires
    print("\n🔍 Vérifications préliminaires...")
    
    # Vérifier la présence des DLLs
    dll_path = os.path.join("Measurement Computing", "DAQami")
    if os.path.exists(dll_path):
        print(f"✅ Répertoire DLLs trouvé: {dll_path}")
        
        # Lister les DLLs importantes
        important_dlls = ["HAL.dll", "ULx.dll", "HAL.UL.dll"]
        for dll in important_dlls:
            dll_file = os.path.join(dll_path, dll)
            if os.path.exists(dll_file):
                print(f"   ✅ {dll} trouvé")
            else:
                print(f"   ⚠️  {dll} manquant")
    else:
        print(f"❌ Répertoire DLLs non trouvé: {dll_path}")
    
    # Lancer CHNeoWave avec MCC
    success = launch_chneowave_with_mcc()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 CHNeoWave est prêt avec le backend MCC!")
        print("   Vous pouvez maintenant utiliser le logiciel avec votre carte MCC.")
    else:
        print("❌ Échec du lancement avec backend MCC")
        print("   Vérifiez la configuration et la connexion matérielle.")
    print("=" * 70)

if __name__ == "__main__":
    main()
