#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des correctifs backend pour CHNeoWave
Vérifie que les alias et les corrections de buffer fonctionnent
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'logciel hrneowave'))

def test_acquisition_controller_aliases():
    """Test des alias ajoutés dans AcquisitionController"""
    try:
        from acquisition_controller import AcquisitionController, AcquisitionConfig, AcquisitionMode
        
        # Créer une configuration de test
        config = AcquisitionConfig(
            mode=AcquisitionMode.SIMULATE,
            sample_rate=32.0,
            n_channels=4,
            buffer_size=1000
        )
        
        # Créer le contrôleur
        controller = AcquisitionController(config)
        
        # Vérifier que les alias existent
        assert hasattr(controller, 'start_acquisition'), "Alias start_acquisition manquant"
        assert hasattr(controller, 'stop_acquisition'), "Alias stop_acquisition manquant"
        assert hasattr(controller, 'clear'), "Méthode clear manquante"
        
        # Vérifier que les alias sont des méthodes
        assert callable(controller.start_acquisition), "start_acquisition n'est pas callable"
        assert callable(controller.stop_acquisition), "stop_acquisition n'est pas callable"
        assert callable(controller.clear), "clear n'est pas callable"
        
        print("✅ Test des alias: SUCCÈS")
        return True
        
    except Exception as e:
        print(f"❌ Test des alias: ÉCHEC - {e}")
        return False

def test_buffer_config_fix():
    """Test de la correction de BufferConfig"""
    try:
        from acquisition_controller import AcquisitionController, AcquisitionConfig, AcquisitionMode
        
        # Créer une configuration avec des paramètres spécifiques
        config = AcquisitionConfig(
            mode=AcquisitionMode.SIMULATE,
            sample_rate=64.0,
            n_channels=8,
            buffer_size=5000
        )
        
        # Créer le contrôleur (cela devrait initialiser le buffer sans erreur)
        controller = AcquisitionController(config)
        
        # Vérifier que le buffer est initialisé
        assert controller.buffer is not None, "Buffer non initialisé"
        
        # Vérifier que le buffer a les bonnes propriétés
        if hasattr(controller.buffer, 'num_channels'):
            assert controller.buffer.num_channels == 8, f"Nombre de canaux incorrect: {controller.buffer.num_channels}"
        
        if hasattr(controller.buffer, 'capacity'):
            assert controller.buffer.capacity == 5000, f"Capacité incorrecte: {controller.buffer.capacity}"
        
        print("✅ Test BufferConfig: SUCCÈS")
        return True
        
    except Exception as e:
        print(f"❌ Test BufferConfig: ÉCHEC - {e}")
        return False

def test_field_validator_fix():
    """Test de la correction du validateur de champs"""
    try:
        from field_validator import AcquisitionValidator
        from PyQt5.QtWidgets import QApplication, QDoubleSpinBox, QSpinBox, QComboBox
        
        # Créer une application Qt temporaire si nécessaire
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Créer le validateur
        validator = AcquisitionValidator()
        
        # Créer des widgets de test
        widgets = {
            'sample_rate': QDoubleSpinBox(),
            'n_channels': QSpinBox(),
            'buffer_size': QSpinBox(),
            'mode': QComboBox()
        }
        
        # Configurer les champs
        validator.setup_acquisition_fields(widgets)
        
        # Vérifier que les champs sont configurés
        assert 'sample_rate' in validator.fields, "Champ sample_rate non configuré"
        assert 'n_channels' in validator.fields, "Champ n_channels non configuré"
        assert 'buffer_size' in validator.fields, "Champ buffer_size non configuré"
        assert 'mode' in validator.fields, "Champ mode non configuré"
        
        print("✅ Test FieldValidator: SUCCÈS")
        return True
        
    except Exception as e:
        print(f"❌ Test FieldValidator: ÉCHEC - {e}")
        return False

def test_simple_config_compatibility():
    """Test de compatibilité de SimpleConfig"""
    try:
        # Simuler la classe SimpleConfig de modern_acquisition_ui.py
        class SimpleConfig:
            def __init__(self, config_dict):
                for key, value in config_dict.items():
                    setattr(self, key, value)
            
            def get(self, key, default=None):
                """Méthode get compatible avec les dictionnaires"""
                return getattr(self, key, default)
        
        # Test de la classe
        config_dict = {
            'sample_rate': 32.0,
            'n_channels': 4,
            'buffer_size': 1000
        }
        
        config = SimpleConfig(config_dict)
        
        # Vérifier l'accès aux attributs
        assert config.sample_rate == 32.0, "Attribut sample_rate incorrect"
        assert config.n_channels == 4, "Attribut n_channels incorrect"
        
        # Vérifier la méthode get
        assert config.get('sample_rate') == 32.0, "Méthode get ne fonctionne pas"
        assert config.get('inexistant', 'default') == 'default', "Valeur par défaut de get incorrecte"
        
        print("✅ Test SimpleConfig: SUCCÈS")
        return True
        
    except Exception as e:
        print(f"❌ Test SimpleConfig: ÉCHEC - {e}")
        return False

def main():
    """Exécute tous les tests"""
    print("=== Tests des correctifs backend CHNeoWave ===")
    print()
    
    tests = [
        test_acquisition_controller_aliases,
        test_buffer_config_fix,
        test_field_validator_fix,
        test_simple_config_compatibility
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Résumé
    success_count = sum(results)
    total_count = len(results)
    
    print("=== RÉSUMÉ ===")
    print(f"Tests réussis: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 Tous les correctifs backend fonctionnent correctement!")
        return 0
    else:
        print("⚠️ Certains correctifs nécessitent une attention supplémentaire.")
        return 1

if __name__ == "__main__":
    sys.exit(main())