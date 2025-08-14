#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour le backend MCC de CHNeoWave
"""

import sys
import os
import logging
import time
import numpy as np

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hrneowave.hardware.backends.mcc_backend import MCCBackend
from hrneowave.hardware.manager import HardwareManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_mcc_backend():
    """Test du backend MCC"""
    print("=" * 60)
    print("TEST DU BACKEND MCC - CHNeoWave")
    print("=" * 60)
    
    # Test 1: Vérification de la disponibilité
    print("\n1. Vérification de la disponibilité du backend MCC...")
    if MCCBackend.is_available():
        print("✅ Backend MCC disponible")
    else:
        print("⚠️  Backend MCC non disponible (DLLs manquantes)")
    
    # Test 2: Détection des cartes
    print("\n2. Détection des cartes MCC...")
    devices = MCCBackend.detect_devices()
    print(f"📊 Cartes détectées: {len(devices)}")
    for device in devices:
        print(f"   - {device['name']} (ID: {device['id']}, Type: {device['type']}, Canaux: {device['channels']})")
    
    # Test 3: Configuration du backend
    print("\n3. Configuration du backend MCC...")
    config = {
        'backend': 'mcc',
        'settings': {
            'sample_rate': 100,
            'channels': 4,
            'device_id': 0,
            'voltage_range': (-10.0, 10.0)
        }
    }
    
    try:
        backend = MCCBackend(config['settings'])
        print("✅ Backend MCC configuré avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False
    
    # Test 4: Ouverture de la connexion
    print("\n4. Test d'ouverture de connexion...")
    if backend.open():
        print("✅ Connexion MCC ouverte")
    else:
        print("❌ Échec de l'ouverture de connexion")
        return False
    
    # Test 5: Configuration de l'acquisition
    print("\n5. Configuration de l'acquisition...")
    try:
        backend.configure_acquisition(sample_rate=100, num_samples_per_channel=1024)
        backend.configure_channels([{'id': i, 'min_val': -10.0, 'max_val': 10.0} for i in range(4)])
        print("✅ Acquisition configurée")
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False
    
    # Test 6: Démarrage de l'acquisition
    print("\n6. Test d'acquisition de données...")
    
    def data_callback(data):
        """Callback pour les données acquises"""
        print(f"📊 Données reçues: {data.shape}, Min: {data.min():.3f}, Max: {data.max():.3f}")
    
    def error_callback(error):
        """Callback pour les erreurs"""
        print(f"❌ Erreur: {error}")
    
    backend.set_data_callback(data_callback)
    backend.set_error_callback(error_callback)
    
    try:
        backend.start()
        print("✅ Acquisition démarrée")
        
        # Attendre quelques secondes pour recevoir des données
        print("⏳ Attente de données (5 secondes)...")
        time.sleep(5)
        
        # Test de lecture directe
        data = backend.read()
        if data.size > 0:
            print(f"✅ Lecture directe réussie: {data.shape}")
        else:
            print("⚠️  Aucune donnée disponible")
        
        # Arrêt de l'acquisition
        backend.stop()
        print("✅ Acquisition arrêtée")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'acquisition: {e}")
        return False
    
    # Test 7: Fermeture de la connexion
    print("\n7. Fermeture de la connexion...")
    backend.close()
    print("✅ Connexion fermée")
    
    # Test 8: Test du HardwareManager
    print("\n8. Test du HardwareManager avec backend MCC...")
    try:
        manager = HardwareManager(config)
        backend_from_manager = manager.get_backend()
        
        if backend_from_manager:
            print("✅ HardwareManager fonctionne avec backend MCC")
            status = backend_from_manager.get_status()
            print(f"📊 Statut: {status}")
        else:
            print("❌ HardwareManager n'a pas pu charger le backend MCC")
            
    except Exception as e:
        print(f"❌ Erreur avec HardwareManager: {e}")
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)
    
    return True

def test_mcc_integration():
    """Test d'intégration complète avec CHNeoWave"""
    print("\n" + "=" * 60)
    print("TEST D'INTÉGRATION MCC - CHNeoWave")
    print("=" * 60)
    
    # Configuration pour l'intégration
    config = {
        'hardware': {
            'backend': 'mcc',
            'settings': {
                'sample_rate': 32,
                'channels': 8,
                'device_id': 0,
                'voltage_range': (-10.0, 10.0)
            }
        }
    }
    
    try:
        # Créer le gestionnaire de matériel
        manager = HardwareManager(config)
        
        # Obtenir le backend
        backend = manager.get_backend()
        
        if not backend:
            print("❌ Impossible d'obtenir le backend MCC")
            return False
        
        print("✅ Backend MCC obtenu via HardwareManager")
        
        # Tester les fonctionnalités de base
        if backend.open():
            print("✅ Connexion ouverte")
            
            # Configuration
            backend.configure_acquisition(32, 512)
            backend.configure_channels([{'id': i} for i in range(4)])
            
            # Test d'acquisition courte
            backend.start()
            time.sleep(2)
            
            data = backend.read()
            if data.size > 0:
                print(f"✅ Données acquises: {data.shape}")
            else:
                print("⚠️  Aucune donnée")
            
            backend.stop()
            backend.close()
            
            print("✅ Test d'intégration réussi")
            return True
        else:
            print("❌ Échec de l'ouverture de connexion")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests MCC pour CHNeoWave")
    
    # Test du backend seul
    success1 = test_mcc_backend()
    
    # Test d'intégration
    success2 = test_mcc_integration()
    
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Backend MCC: {'✅ SUCCÈS' if success1 else '❌ ÉCHEC'}")
    print(f"Intégration: {'✅ SUCCÈS' if success2 else '❌ ÉCHEC'}")
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont passés avec succès!")
        print("Le backend MCC est prêt à être utilisé avec CHNeoWave.")
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("Vérifiez la configuration et les DLLs MCC.")
