#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour les backends CHNeoWave v1.1.0-RC
Usage: python test_backends.py --backend [ni|iotech|simulate] --fs [32|100|500]
"""

import sys
import os
import argparse
import time
import numpy as np
from pathlib import Path

# Ajouter le répertoire src au path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from hrneowave.gui.controllers.acquisition_controller import (
    AcquisitionController, AcquisitionConfig, AcquisitionMode
)

def test_backend(backend_name: str, sample_rate: float, duration: float = 10.0):
    """
    Teste un backend spécifique
    
    Args:
        backend_name: 'ni', 'iotech', ou 'simulate'
        sample_rate: Fréquence d'échantillonnage (32, 100, 500 Hz)
        duration: Durée du test en secondes
    """
    print(f"\n=== Test Backend {backend_name.upper()} ===")
    print(f"Fréquence: {sample_rate} Hz")
    print(f"Durée: {duration} s")
    print(f"Canaux: 8")
    
    # Mapper le nom vers l'enum
    mode_map = {
        'ni': AcquisitionMode.NI_DAQ,
        'iotech': AcquisitionMode.IOTECH,
        'simulate': AcquisitionMode.SIMULATE
    }
    
    if backend_name not in mode_map:
        print(f"❌ Backend '{backend_name}' non supporté")
        return False
    
    # Configuration
    config = AcquisitionConfig(
        mode=mode_map[backend_name],
        sample_rate=sample_rate,
        n_channels=8,
        buffer_size=int(sample_rate * 60),  # Buffer de 60s
        device_config={
            'device': 'Dev1',  # Pour NI-DAQ
            'voltage_range': [-10.0, 10.0]
        }
    )
    
    # Créer le contrôleur
    try:
        controller = AcquisitionController(config)
        print(f"✓ Contrôleur créé avec backend {backend_name}")
    except Exception as e:
        print(f"❌ Erreur création contrôleur: {e}")
        return False
    
    # Variables de test
    samples_received = 0
    errors_count = 0
    start_time = None
    
    def on_data_ready(data, timestamp):
        nonlocal samples_received, start_time
        if start_time is None:
            start_time = timestamp
        samples_received += 1
        
        # Afficher le progrès toutes les 2 secondes
        elapsed = timestamp - start_time
        if samples_received % (int(sample_rate * 2)) == 0:
            expected_samples = int(elapsed * sample_rate)
            rate = samples_received / elapsed if elapsed > 0 else 0
            print(f"  {elapsed:.1f}s: {samples_received} échantillons (taux: {rate:.1f} Hz, attendu: {sample_rate} Hz)")
    
    def on_error(error_msg):
        nonlocal errors_count
        errors_count += 1
        print(f"  ⚠️ Erreur #{errors_count}: {error_msg}")
    
    # Connecter les signaux
    controller.data_ready.connect(on_data_ready)
    controller.error_occurred.connect(on_error)
    
    # Test de connexion
    print("\n1. Test de connexion...")
    if not controller.connect():
        print(f"❌ Échec de connexion au backend {backend_name}")
        return False
    print(f"✓ Connexion réussie")
    
    # Test d'acquisition
    print("\n2. Démarrage de l'acquisition...")
    if not controller.start():
        print(f"❌ Échec de démarrage de l'acquisition")
        controller.disconnect()
        return False
    print(f"✓ Acquisition démarrée")
    
    # Attendre la durée spécifiée avec traitement des événements Qt
    print(f"\n3. Acquisition en cours ({duration}s)...")
    from PySide6.QtCore import QTimer, QEventLoop
    
    loop = QEventLoop()
    timer = QTimer()
    timer.timeout.connect(loop.quit)
    timer.start(int(duration * 1000))  # Convertir en millisecondes
    loop.exec_()
    
    # Arrêter l'acquisition
    print("\n4. Arrêt de l'acquisition...")
    controller.stop()
    controller.disconnect()
    
    # Résultats
    expected_samples = int(duration * sample_rate)
    success_rate = (samples_received / expected_samples) * 100 if expected_samples > 0 else 0
    
    print(f"\n=== Résultats ===")
    print(f"Échantillons reçus: {samples_received}")
    print(f"Échantillons attendus: {expected_samples}")
    print(f"Taux de réussite: {success_rate:.1f}%")
    print(f"Erreurs: {errors_count}")
    
    # Critères de succès
    success = (
        samples_received > 0 and
        success_rate >= 90.0 and  # Au moins 90% des échantillons
        errors_count == 0
    )
    
    if success:
        print(f"✅ Test {backend_name.upper()} RÉUSSI")
    else:
        print(f"❌ Test {backend_name.upper()} ÉCHOUÉ")
    
    return success

def main():
    # Créer QApplication pour les signaux Qt
    from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication([])
    
    parser = argparse.ArgumentParser(
        description="Test des backends CHNeoWave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python test_backends.py --backend ni --fs 100
  python test_backends.py --backend iotech --fs 32
  python test_backends.py --backend simulate --fs 500
  python test_backends.py --all
        """
    )
    
    parser.add_argument('--backend', choices=['ni', 'iotech', 'simulate'],
                       help='Backend à tester')
    parser.add_argument('--fs', type=float, choices=[32, 100, 500], default=100,
                       help='Fréquence d\'échantillonnage (Hz)')
    parser.add_argument('--duration', type=float, default=10.0,
                       help='Durée du test (secondes)')
    parser.add_argument('--all', action='store_true',
                       help='Tester tous les backends')
    
    args = parser.parse_args()
    
    if not args.backend and not args.all:
        parser.print_help()
        return 1
    
    print("CHNeoWave v1.1.0-RC - Test des Backends")
    print("=" * 50)
    
    results = []
    
    if args.all:
        # Tester tous les backends
        backends = ['simulate', 'ni', 'iotech']
        for backend in backends:
            success = test_backend(backend, args.fs, args.duration)
            results.append((backend, success))
            time.sleep(1)  # Pause entre les tests
    else:
        # Tester un backend spécifique
        success = test_backend(args.backend, args.fs, args.duration)
        results.append((args.backend, success))
    
    # Résumé final
    print("\n" + "=" * 50)
    print("RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    all_success = True
    for backend, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"{backend.upper():10} : {status}")
        if not success:
            all_success = False
    
    if all_success:
        print("\n🎉 Tous les tests sont RÉUSSIS !")
        return 0
    else:
        print("\n💥 Certains tests ont ÉCHOUÉ")
        return 1

if __name__ == '__main__':
    sys.exit(main())