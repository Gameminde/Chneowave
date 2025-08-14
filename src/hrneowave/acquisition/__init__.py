#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'acquisition de données pour CHNeoWave
Intégration de la carte MCC DAQ USB-1608FS pour l'acquisition maritime

Auteur: CHNeoWave Development Team
Version: 1.0.0
"""

from .mcc_daq_wrapper import (
    MCCDAQ_USB1608FS,
    MCCRanges,
    MCCErrorCodes,
    MCCOptions,
    AcquisitionConfig,
    ChannelConfig,
    scan_available_boards,
    get_error_message
)

from .acquisition_controller import (
    AcquisitionController,
    MaritimeChannelConfig,
    AcquisitionSession,
    create_default_maritime_config
)

__all__ = [
    # Wrapper MCC DAQ
    'MCCDAQ_USB1608FS',
    'MCCRanges',
    'MCCErrorCodes', 
    'MCCOptions',
    'AcquisitionConfig',
    'ChannelConfig',
    'scan_available_boards',
    'get_error_message',
    
    # Contrôleur d'acquisition
    'AcquisitionController',
    'MaritimeChannelConfig',
    'AcquisitionSession',
    'create_default_maritime_config'
]

# Informations du module
__version__ = "1.0.0"
__author__ = "CHNeoWave Development Team"
__description__ = "Module d'acquisition maritime avec carte MCC DAQ USB-1608FS"

# Configuration par défaut
DEFAULT_SAMPLING_RATE = 1000.0  # Hz
DEFAULT_BUFFER_SIZE = 10000      # échantillons
DEFAULT_EXPORT_FORMAT = 'csv'

# Constantes maritimes
MARITIME_SENSOR_TYPES = [
    'wave_height',      # Capteur de hauteur de houle
    'pressure',         # Capteur de pression hydrostatique
    'accelerometer',    # Accéléromètre
    'temperature',      # Capteur de température
    'flow_velocity',    # Vélocimètre
    'force',           # Capteur de force
    'displacement',    # Capteur de déplacement
    'strain',          # Jauge de contrainte
    'generic'          # Capteur générique
]

VOLTAGE_RANGES = {
    '±1V': MCCRanges.BIP1VOLTS,
    '±2V': MCCRanges.BIP2VOLTS,
    '±5V': MCCRanges.BIP5VOLTS,
    '±10V': MCCRanges.BIP10VOLTS
}

# Configurations prédéfinies pour capteurs maritimes
SENSOR_PRESETS = {
    'wave_height_sonic': {
        'sensor_type': 'wave_height',
        'typical_range': '±10V',
        'typical_sensitivity': 2.0,  # V/m
        'units': 'm',
        'description': 'Capteur ultrasonique de hauteur de houle'
    },
    'wave_height_capacitive': {
        'sensor_type': 'wave_height',
        'typical_range': '±5V',
        'typical_sensitivity': 1.0,  # V/m
        'units': 'm',
        'description': 'Capteur capacitif de hauteur de houle'
    },
    'pressure_piezoresistive': {
        'sensor_type': 'pressure',
        'typical_range': '±5V',
        'typical_sensitivity': 0.01,  # V/hPa
        'units': 'hPa',
        'description': 'Capteur de pression piézorésistif'
    },
    'accelerometer_piezoelectric': {
        'sensor_type': 'accelerometer',
        'typical_range': '±10V',
        'typical_sensitivity': 1.0,  # V/(m/s²)
        'units': 'm/s²',
        'description': 'Accéléromètre piézoélectrique'
    },
    'temperature_thermocouple': {
        'sensor_type': 'temperature',
        'typical_range': '±2V',
        'typical_sensitivity': 0.1,  # V/°C
        'units': '°C',
        'description': 'Thermocouple type K'
    },
    'force_load_cell': {
        'sensor_type': 'force',
        'typical_range': '±10V',
        'typical_sensitivity': 0.002,  # V/N
        'units': 'N',
        'description': 'Cellule de charge pour mesure de force'
    }
}

def get_sensor_preset(preset_name: str) -> dict:
    """
    Récupère une configuration prédéfinie de capteur
    
    Args:
        preset_name: Nom de la configuration prédéfinie
        
    Returns:
        Dictionnaire avec la configuration du capteur
    """
    return SENSOR_PRESETS.get(preset_name, {})

def list_sensor_presets() -> list:
    """
    Liste toutes les configurations prédéfinies disponibles
    
    Returns:
        Liste des noms de configurations prédéfinies
    """
    return list(SENSOR_PRESETS.keys())

def create_maritime_laboratory_config() -> dict:
    """
    Crée une configuration complète pour laboratoire maritime
    
    Returns:
        Configuration 8 canaux pour laboratoire d'hydrodynamique
    """
    config = {
        0: MaritimeChannelConfig(
            channel=0,
            sensor_type='wave_height',
            label='Houle_Amont',
            units='V',
            range_type=MCCRanges.BIP10VOLTS,
            physical_units='m',
            sensor_sensitivity=2.0,
            enabled=True
        ),
        1: MaritimeChannelConfig(
            channel=1,
            sensor_type='wave_height',
            label='Houle_Aval',
            units='V',
            range_type=MCCRanges.BIP10VOLTS,
            physical_units='m',
            sensor_sensitivity=2.0,
            enabled=True
        ),
        2: MaritimeChannelConfig(
            channel=2,
            sensor_type='pressure',
            label='Pression_Hydrostatique',
            units='V',
            range_type=MCCRanges.BIP5VOLTS,
            physical_units='hPa',
            sensor_sensitivity=0.01,
            enabled=True
        ),
        3: MaritimeChannelConfig(
            channel=3,
            sensor_type='accelerometer',
            label='Acceleration_X',
            units='V',
            range_type=MCCRanges.BIP10VOLTS,
            physical_units='m/s²',
            sensor_sensitivity=1.0,
            enabled=True
        ),
        4: MaritimeChannelConfig(
            channel=4,
            sensor_type='accelerometer',
            label='Acceleration_Y',
            units='V',
            range_type=MCCRanges.BIP10VOLTS,
            physical_units='m/s²',
            sensor_sensitivity=1.0,
            enabled=True
        ),
        5: MaritimeChannelConfig(
            channel=5,
            sensor_type='force',
            label='Force_Modele',
            units='V',
            range_type=MCCRanges.BIP10VOLTS,
            physical_units='N',
            sensor_sensitivity=0.002,
            enabled=True
        ),
        6: MaritimeChannelConfig(
            channel=6,
            sensor_type='temperature',
            label='Temperature_Eau',
            units='V',
            range_type=MCCRanges.BIP2VOLTS,
            physical_units='°C',
            sensor_sensitivity=0.1,
            enabled=True
        ),
        7: MaritimeChannelConfig(
            channel=7,
            sensor_type='wave_height',
            label='Reference_Houle',
            units='V',
            range_type=MCCRanges.BIP10VOLTS,
            physical_units='m',
            sensor_sensitivity=2.0,
            enabled=False  # Canal de référence, activé au besoin
        )
    }
    
    return config

def validate_hardware_compatibility() -> dict:
    """
    Valide la compatibilité matérielle du système
    
    Returns:
        Dictionnaire avec les résultats de validation
    """
    validation_results = {
        'timestamp': None,
        'hardware_detected': False,
        'dll_availability': False,
        'driver_version': None,
        'board_count': 0,
        'supported_features': [],
        'warnings': [],
        'errors': []
    }
    
    try:
        import datetime
        validation_results['timestamp'] = datetime.datetime.now().isoformat()
        
        # Test de scan des cartes
        boards = scan_available_boards()
        validation_results['board_count'] = len(boards)
        validation_results['hardware_detected'] = len(boards) > 0
        
        if boards:
            validation_results['supported_features'].extend([
                '8 canaux simultanés',
                'Résolution 16 bits',
                'Fréquences jusqu\'à 50 kS/s par canal',
                'Plages ±1V, ±2V, ±5V, ±10V',
                'Buffer FIFO 32K échantillons'
            ])
        else:
            validation_results['warnings'].append(
                'Aucune carte MCC DAQ détectée - vérifier connexion et drivers'
            )
            
    except Exception as e:
        validation_results['errors'].append(f'Erreur de validation: {e}')
        
    return validation_results

# Informations de debug
def get_module_info() -> dict:
    """
    Retourne les informations du module d'acquisition
    
    Returns:
        Dictionnaire avec les informations du module
    """
    return {
        'module': __name__,
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'supported_hardware': 'MCC DAQ USB-1608FS',
        'sensor_types': MARITIME_SENSOR_TYPES,
        'voltage_ranges': list(VOLTAGE_RANGES.keys()),
        'preset_count': len(SENSOR_PRESETS),
        'default_sampling_rate': DEFAULT_SAMPLING_RATE,
        'default_buffer_size': DEFAULT_BUFFER_SIZE
    }

if __name__ == "__main__":
    # Affichage des informations du module
    import json
    
    print("🌊 Module d'Acquisition Maritime CHNeoWave")
    print("=" * 50)
    
    info = get_module_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))
    
    print("\n📋 Configurations Prédéfinies:")
    for preset_name in list_sensor_presets():
        preset = get_sensor_preset(preset_name)
        print(f"  - {preset_name}: {preset.get('description', 'N/A')}")
        
    print("\n🔍 Validation Matérielle:")
    validation = validate_hardware_compatibility()
    
    if validation['hardware_detected']:
        print(f"✅ {validation['board_count']} carte(s) détectée(s)")
        print("📋 Fonctionnalités supportées:")
        for feature in validation['supported_features']:
            print(f"  - {feature}")
    else:
        print("⚠️ Aucune carte détectée")
        
    if validation['warnings']:
        print("\n⚠️ Avertissements:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
            
    if validation['errors']:
        print("\n❌ Erreurs:")
        for error in validation['errors']:
            print(f"  - {error}")
