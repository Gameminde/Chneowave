#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour les composants CHNeoWave v1.1.0-RC
Test des nouveaux modules: certificats, métadonnées, validation
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import tempfile
import shutil

# Ajouter le chemin source
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from hrneowave.core.calibration_certificate import (
        CalibrationCertificateGenerator,
        CalibrationData,
        CertificateConfig,
        create_sample_calibration_data
    )
    from hrneowave.core.metadata_manager import (
        MetadataManager,
        SessionMetadata,
        ExperimentType,
        create_sample_session_metadata
    )
    from hrneowave.core.data_validator import (
        DataValidator,
        ValidationConfig,
        ValidationLevel,
        create_wave_probe_config,
        create_pressure_sensor_config
    )
except ImportError as e:
    print(f"❌ Erreur import modules: {e}")
    sys.exit(1)

def test_calibration_certificates():
    """Test du générateur de certificats de calibration"""
    print("\n🧪 Test des certificats de calibration...")
    
    try:
        # Créer le générateur
        generator = CalibrationCertificateGenerator()
        print(f"✓ Générateur créé (PDF disponible: {generator.available})")
        
        # Créer des données d'exemple
        calib_data = create_sample_calibration_data()
        print(f"✓ {len(calib_data)} données de calibration créées")
        
        # Configuration du certificat
        config = CertificateConfig(
            laboratory_name="Laboratoire Méditerranéen d'Études Maritimes",
            laboratory_address="Université de la Méditerranée, 13000 Marseille",
            certificate_number="CERT-2024-001",
            client_name="Laboratoire Client",
            equipment_model="CHNeoWave v1.1.0",
            equipment_serial="CHN-2024-001"
        )
        print("✓ Configuration certificat créée")
        
        # Générer le certificat si PDF disponible
        if generator.available:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                success = generator.generate_certificate(calib_data, config, tmp.name)
                if success:
                    print(f"✓ Certificat PDF généré: {tmp.name}")
                    # Vérifier que le fichier existe et n'est pas vide
                    if Path(tmp.name).exists() and Path(tmp.name).stat().st_size > 0:
                        print(f"✓ Fichier PDF valide ({Path(tmp.name).stat().st_size} bytes)")
                    else:
                        print("❌ Fichier PDF invalide")
                        return False
                else:
                    print("❌ Échec génération certificat")
                    return False
        else:
            print("⚠️ Génération PDF non disponible (ReportLab manquant)")
        
        # Test des données de calibration
        for i, calib in enumerate(calib_data):
            if len(calib.reference_values) != len(calib.measured_values):
                print(f"❌ Données incohérentes pour capteur {i}")
                return False
            
            if calib.r_squared < 0.9:
                print(f"⚠️ R² faible pour {calib.sensor_id}: {calib.r_squared:.4f}")
        
        print("✅ Test certificats de calibration réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test certificats: {e}")
        return False

def test_metadata_manager():
    """Test du gestionnaire de métadonnées"""
    print("\n📋 Test du gestionnaire de métadonnées...")
    
    try:
        # Créer un répertoire temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer le gestionnaire
            manager = MetadataManager(temp_dir)
            print("✓ Gestionnaire de métadonnées créé")
            
            # Créer des métadonnées d'exemple
            metadata = create_sample_session_metadata()
            print(f"✓ Métadonnées créées (ID: {metadata.session_id})")
            
            # Vérifier l'intégrité
            if not metadata.verify_integrity():
                print("❌ Intégrité des métadonnées compromise")
                return False
            print("✓ Intégrité vérifiée")
            
            # Sauvegarder
            file_path = manager.save_metadata(metadata)
            print(f"✓ Métadonnées sauvegardées: {file_path.name}")
            
            # Charger et vérifier
            loaded_metadata = manager.load_metadata(file_path)
            print("✓ Métadonnées rechargées")
            
            # Vérifier que les données sont identiques
            if loaded_metadata.session_id != metadata.session_id:
                print("❌ ID de session différent après rechargement")
                return False
            
            if loaded_metadata.experiment_type != metadata.experiment_type:
                print("❌ Type d'expérience différent après rechargement")
                return False
            
            if len(loaded_metadata.sensors) != len(metadata.sensors):
                print("❌ Nombre de capteurs différent après rechargement")
                return False
            
            print("✓ Données cohérentes après rechargement")
            
            # Test de recherche
            sessions = manager.search_sessions(experiment_type=ExperimentType.WAVE_PROPAGATION)
            if len(sessions) != 1:
                print(f"❌ Recherche incorrecte: {len(sessions)} résultats")
                return False
            print("✓ Recherche fonctionnelle")
            
            # Test d'export de résumé
            summary_path = Path(temp_dir) / "summary.json"
            success = manager.export_metadata_summary(summary_path)
            if not success or not summary_path.exists():
                print("❌ Échec export résumé")
                return False
            print("✓ Export résumé réussi")
            
            # Compter les sessions existantes avant d'ajouter
            initial_sessions = len(manager.list_sessions())
            
            # Créer plusieurs sessions pour test
            for i in range(3):
                test_metadata = create_sample_session_metadata()
                test_metadata.session_name = f"Test Session {i+1}"
                test_metadata.test_number = f"TEST_{i+1:03d}"
                manager.save_metadata(test_metadata)
            
            # Lister les sessions
            session_files = manager.list_sessions()
            expected_count = initial_sessions + 3
            if len(session_files) != expected_count:
                print(f"❌ Nombre de sessions incorrect: {len(session_files)} (attendu: {expected_count})")
                return False
            print(f"✓ {len(session_files)} sessions listées")
        
        print("✅ Test gestionnaire de métadonnées réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test métadonnées: {e}")
        return False

def test_data_validator():
    """Test du validateur de données"""
    print("\n🔍 Test du validateur de données...")
    
    try:
        # Créer le validateur
        validator = DataValidator(sampling_rate=100.0)
        print("✓ Validateur créé")
        
        # Ajouter des canaux
        wave_config = create_wave_probe_config(channel=0, measurement_range=(-300, 300))
        pressure_config = create_pressure_sensor_config(channel=1, measurement_range=(0, 1000))
        
        validator.add_channel(wave_config)
        validator.add_channel(pressure_config)
        print("✓ Canaux ajoutés")
        
        # Callback pour collecter les résultats
        validation_results = []
        def collect_results(result):
            validation_results.append(result)
        
        validator.add_result_callback(collect_results)
        print("✓ Callback ajouté")
        
        # Test avec données normales
        print("\n  Test données normales...")
        for i in range(100):
            timestamp = datetime.now() + timedelta(seconds=i*0.01)
            samples = {
                0: 50 * np.sin(2 * np.pi * 0.5 * i * 0.01) + np.random.normal(0, 1),  # Houle
                1: 500 + 50 * np.sin(2 * np.pi * 0.2 * i * 0.01) + np.random.normal(0, 5)  # Pression
            }
            results = validator.validate_samples(samples, timestamp)
        
        normal_errors = len([r for r in validation_results if r.level == ValidationLevel.ERROR])
        print(f"  ✓ {len(validation_results)} résultats, {normal_errors} erreurs")
        
        # Test avec données hors limites
        print("\n  Test données hors limites...")
        validation_results.clear()
        
        out_of_range_samples = {
            0: 500,  # Au-dessus de la limite (300)
            1: -100  # En-dessous de la limite (0)
        }
        results = validator.validate_samples(out_of_range_samples)
        
        range_errors = len([r for r in validation_results if r.rule_type.value == "range_check"])
        if range_errors < 2:
            print(f"❌ Détection hors limites insuffisante: {range_errors} erreurs")
            return False
        print(f"  ✓ {range_errors} erreurs de plage détectées")
        
        # Test avec changement rapide
        print("\n  Test changement rapide...")
        validation_results.clear()
        
        # Valeur normale puis saut important
        validator.validate_samples({0: 0, 1: 500})
        validator.validate_samples({0: 200, 1: 900})  # Changement rapide
        
        rate_warnings = len([r for r in validation_results if r.rule_type.value == "rate_of_change"])
        if rate_warnings == 0:
            print("⚠️ Aucun avertissement de taux de changement détecté")
        else:
            print(f"  ✓ {rate_warnings} avertissements de taux détectés")
        
        # Test statistiques
        stats = validator.get_global_statistics()
        print(f"\n  Statistiques globales:")
        print(f"    Échantillons traités: {stats['total_samples_processed']}")
        print(f"    Résultats validation: {stats['total_validation_results']}")
        print(f"    Erreurs: {stats['total_errors']}")
        print(f"    Avertissements: {stats['total_warnings']}")
        print(f"    Canaux actifs: {stats['active_channels']}")
        
        # Statistiques par canal
        for channel in [0, 1]:
            channel_stats = validator.get_channel_statistics(channel)
            if channel_stats:
                print(f"    Canal {channel}: {channel_stats['total_samples']} échantillons, "
                      f"{channel_stats['error_count']} erreurs")
        
        # Test nettoyage
        validator.clear_history()
        stats_after_clear = validator.get_global_statistics()
        if stats_after_clear['total_samples_processed'] != 0:
            print("❌ Nettoyage historique échoué")
            return False
        print("  ✓ Nettoyage historique réussi")
        
        print("✅ Test validateur de données réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test validateur: {e}")
        return False

def test_integration():
    """Test d'intégration des composants"""
    print("\n🔗 Test d'intégration...")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer une session complète avec tous les composants
            metadata_manager = MetadataManager(temp_dir)
            validator = DataValidator(100.0)
            
            # Créer une session
            session = create_sample_session_metadata()
            session.session_name = "Test Intégration v1.1.0"
            
            # Configurer la validation selon les capteurs de la session
            for sensor in session.sensors:
                if sensor.sensor_type == "wave_probe":
                    config = create_wave_probe_config(channel=sensor.channel, measurement_range=(-300, 300))
                    validator.add_channel(config)
            
            # Simuler une acquisition avec validation
            validation_summary = []
            
            def log_validation(result):
                validation_summary.append({
                    'timestamp': result.timestamp.isoformat(),
                    'channel': result.channel,
                    'level': result.level.value,
                    'message': result.message
                })
            
            validator.add_result_callback(log_validation)
            
            # Générer des données d'acquisition
            session.started_at = datetime.now()
            
            for i in range(200):
                timestamp = session.started_at + timedelta(seconds=i*0.01)
                samples = {}
                
                for sensor in session.sensors:
                    if sensor.sensor_type == "wave_probe":
                        # Simuler une houle avec un peu de bruit
                        value = 30 * np.sin(2 * np.pi * 0.8 * i * 0.01) + np.random.normal(0, 2)
                        samples[sensor.channel] = value
                
                validator.validate_samples(samples, timestamp)
            
            session.completed_at = datetime.now()
            session.total_samples = 200 * len(session.sensors)
            
            # Ajouter les résultats de validation aux métadonnées
            validation_stats = validator.get_global_statistics()
            session.data_quality_score = max(0, 100 - validation_stats['total_errors'] * 10)
            session.validation_status = "validated" if session.data_quality_score > 80 else "warning"
            
            # Sauvegarder la session
            session_file = metadata_manager.save_metadata(session)
            print(f"✓ Session intégrée sauvegardée: {session_file.name}")
            
            # Créer des données de calibration correspondantes
            calib_data = []
            for sensor in session.sensors:
                if sensor.sensor_type == "wave_probe":
                    # Simuler des données de calibration
                    ref_values = [0, 50, 100, 150, 200]
                    measured_values = [0.1 + val * 0.02 + np.random.normal(0, 0.001) for val in ref_values]
                    
                    slope, intercept = np.polyfit(measured_values, ref_values, 1)
                    r_squared = np.corrcoef(measured_values, ref_values)[0, 1] ** 2
                    
                    calib = CalibrationData(
                        sensor_id=sensor.sensor_id,
                        sensor_type=sensor.sensor_type,
                        channel=sensor.channel,
                        reference_values=ref_values,
                        measured_values=measured_values,
                        slope=slope,
                        intercept=intercept,
                        r_squared=r_squared,
                        calibration_date=session.created_at,
                        operator=session.operator,
                        equipment_used="Étalon laboratoire",
                        environmental_conditions={
                            "température": "20°C",
                            "humidité": "50%"
                        },
                        measurement_range=(-300, 300),
                        accuracy_spec=1.0,
                        linearity_spec=0.5
                    )
                    calib_data.append(calib)
            
            print(f"✓ {len(calib_data)} données de calibration créées")
            print(f"✓ Score qualité session: {session.data_quality_score:.1f}%")
            print(f"✓ Statut validation: {session.validation_status}")
            print(f"✓ {len(validation_summary)} événements de validation")
            
            # Vérifier la cohérence
            if len(calib_data) != len(session.sensors):
                print("❌ Incohérence nombre capteurs/calibrations")
                return False
            
            if session.data_quality_score < 0 or session.data_quality_score > 100:
                print("❌ Score qualité invalide")
                return False
            
            print("✅ Test d'intégration réussi")
            return True
            
    except Exception as e:
        print(f"❌ Erreur test intégration: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Tests des composants CHNeoWave v1.1.0-RC")
    print("=" * 50)
    
    tests = [
        ("Certificats de calibration", test_calibration_certificates),
        ("Gestionnaire de métadonnées", test_metadata_manager),
        ("Validateur de données", test_data_validator),
        ("Intégration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 30)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"{test_name:.<40} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed} réussis, {failed} échoués")
    
    if failed == 0:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("CHNeoWave v1.1.0-RC est prêt pour la validation finale.")
        return 0
    else:
        print(f"\n💥 {failed} test(s) ont ÉCHOUÉ")
        print("Correction nécessaire avant validation finale.")
        return 1

if __name__ == "__main__":
    sys.exit(main())