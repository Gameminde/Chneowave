#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test simplifié pour le backend MCC de CHNeoWave
"""

import sys
import os
import logging
import time
import numpy as np

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import direct du backend MCC
try:
    from hrneowave.hardware.backends.mcc_backend import MCCBackend
    print("✅ Import du backend MCC réussi")
except Exception as e:
    print(f"❌ Erreur lors de l'import du backend MCC: {e}")
    sys.exit(1)

def test_mcc_backend_basic():
    """Test basique du backend MCC"""
    print("\n" + "=" * 60)
    print("TEST BASIQUE DU BACKEND MCC")
    print("=" * 60)
    
    # Test 1: Vérification de la disponibilité
    print("\n1. Vérification de la disponibilité...")
    if MCCBackend.is_available():
        print("✅ Backend MCC disponible")
    else:
        print("⚠️  Backend MCC non disponible (DLLs manquantes)")
    
    # Test 2: Détection des cartes
    print("\n2. Détection des cartes...")
    devices = MCCBackend.detect_devices()
    print(f"📊 Cartes détectées: {len(devices)}")
    for device in devices:
        print(f"   - {device['name']} (ID: {device['id']})")
    
    # Test 3: Création du backend
    print("\n3. Création du backend...")
    config = {
        'sample_rate': 100,
        'channels': 4,
        'device_id': 0,
        'voltage_range': (-10.0, 10.0)
    }
    
    try:
        backend = MCCBackend(config)
        print("✅ Backend MCC créé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False
    
    # Test 4: Ouverture de connexion
    print("\n4. Test d'ouverture de connexion...")
    if backend.open():
        print("✅ Connexion ouverte")
    else:
        print("❌ Échec de l'ouverture")
        return False
    
    # Test 5: Configuration
    print("\n5. Configuration de l'acquisition...")
    try:
        backend.configure_acquisition(100, 512)
        backend.configure_channels([{'id': i} for i in range(4)])
        print("✅ Configuration réussie")
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False
    
    # Test 6: Acquisition
    print("\n6. Test d'acquisition...")
    try:
        backend.start()
        print("✅ Acquisition démarrée")
        
        # Attendre et lire des données
        time.sleep(2)
        data = backend.read()
        
        if data.size > 0:
            print(f"✅ Données reçues: {data.shape}")
            print(f"   Min: {data.min():.3f}, Max: {data.max():.3f}")
        else:
            print("⚠️  Aucune donnée")
        
        backend.stop()
        print("✅ Acquisition arrêtée")
        
    except Exception as e:
        print(f"❌ Erreur d'acquisition: {e}")
        return False
    
    # Test 7: Fermeture
    print("\n7. Fermeture de la connexion...")
    backend.close()
    print("✅ Connexion fermée")
    
    return True

def test_mcc_data_generation():
    """Test de génération de données"""
    print("\n" + "=" * 60)
    print("TEST DE GÉNÉRATION DE DONNÉES")
    print("=" * 60)
    
    config = {
        'sample_rate': 32,
        'channels': 8,
        'device_id': 0,
        'voltage_range': (-10.0, 10.0)
    }
    
    try:
        backend = MCCBackend(config)
        backend.open()
        
        # Configuration
        backend.configure_acquisition(32, 1024)
        backend.configure_channels([{'id': i} for i in range(8)])
        
        # Test de génération de données
        data = backend._generate_mcc_data()
        print(f"📊 Données générées: {data.shape}")
        print(f"   Canaux: {data.shape[0]}")
        print(f"   Échantillons: {data.shape[1]}")
        print(f"   Min: {data.min():.3f}")
        print(f"   Max: {data.max():.3f}")
        print(f"   Moyenne: {data.mean():.3f}")
        print(f"   Écart-type: {data.std():.3f}")
        
        backend.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test du Backend MCC - CHNeoWave")
    print("=" * 60)
    
    # Test basique
    success1 = test_mcc_backend_basic()
    
    # Test de génération de données
    success2 = test_mcc_data_generation()
    
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Test basique: {'✅ SUCCÈS' if success1 else '❌ ÉCHEC'}")
    print(f"Génération données: {'✅ SUCCÈS' if success2 else '❌ ÉCHEC'}")
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont passés!")
        print("Le backend MCC fonctionne correctement.")
    else:
        print("\n⚠️  Certains tests ont échoué.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
