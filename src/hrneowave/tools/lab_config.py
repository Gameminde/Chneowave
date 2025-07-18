#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration automatique pour laboratoires maritimes CHNeoWave

Ce module fournit des outils de configuration automatique pour différents
types de laboratoires d'études maritimes, avec des presets optimisés pour
les environnements méditerranéens (bassins et canaux).
"""

import os
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import datetime


@dataclass
class HardwareConfig:
    """Configuration hardware pour acquisition"""

    sampling_rate_hz: float
    num_channels: int
    buffer_duration_seconds: float
    anti_aliasing_cutoff_hz: float
    adc_resolution_bits: int
    voltage_range_v: Tuple[float, float]
    coupling: str  # 'AC' ou 'DC'
    impedance_ohms: float


@dataclass
class ProcessingConfig:
    """Configuration traitement signal"""

    fft_window_type: str
    fft_overlap_percent: float
    fft_zero_padding_factor: int
    goda_svd_threshold: float
    enable_real_time_processing: bool
    processing_chunk_size: int
    max_frequency_hz: float
    spectral_resolution_hz: float


@dataclass
class EnvironmentConfig:
    """Configuration environnement laboratoire"""

    laboratory_type: str  # 'basin', 'canal', 'flume'
    location: str
    water_depth_m: float
    basin_length_m: Optional[float]
    basin_width_m: Optional[float]
    wave_maker_type: str
    probe_spacing_m: float
    coordinate_system: str  # 'cartesian', 'polar'
    reference_level_m: float


@dataclass
class CalibrationConfig:
    """Configuration étalonnage"""

    probe_sensitivity_mv_per_m: List[float]
    probe_offset_m: List[float]
    temperature_coefficient: float
    last_calibration_date: str
    calibration_method: str
    reference_wave_height_m: float
    calibration_frequency_hz: float


@dataclass
class LabConfiguration:
    """Configuration complète laboratoire"""

    name: str
    preset_type: str
    description: str
    hardware: HardwareConfig
    processing: ProcessingConfig
    environment: EnvironmentConfig
    calibration: CalibrationConfig
    created_date: str
    version: str


class MediterraneanLabConfigurator:
    """Configurateur pour laboratoires méditerranéens"""

    def __init__(self):
        self.presets = self._initialize_presets()
        self.config_dir = Path.home() / ".chneowave" / "configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _initialize_presets(self) -> Dict[str, LabConfiguration]:
        """Initialise les presets de laboratoire"""
        presets = {}

        # Preset Bassin Méditerranéen Standard
        presets["mediterranean_basin"] = LabConfiguration(
            name="Bassin Méditerranéen Standard",
            preset_type="mediterranean_basin",
            description="Configuration optimisée pour bassins d'études maritimes méditerranéens",
            hardware=HardwareConfig(
                sampling_rate_hz=1000.0,
                num_channels=8,
                buffer_duration_seconds=15.0,
                anti_aliasing_cutoff_hz=200.0,
                adc_resolution_bits=16,
                voltage_range_v=(-5.0, 5.0),
                coupling="AC",
                impedance_ohms=1e6,
            ),
            processing=ProcessingConfig(
                fft_window_type="hanning",
                fft_overlap_percent=50.0,
                fft_zero_padding_factor=2,
                goda_svd_threshold=1e-10,
                enable_real_time_processing=True,
                processing_chunk_size=512,
                max_frequency_hz=5.0,
                spectral_resolution_hz=0.01,
            ),
            environment=EnvironmentConfig(
                laboratory_type="basin",
                location="Méditerranée",
                water_depth_m=1.5,
                basin_length_m=50.0,
                basin_width_m=30.0,
                wave_maker_type="piston",
                probe_spacing_m=2.0,
                coordinate_system="cartesian",
                reference_level_m=0.0,
            ),
            calibration=CalibrationConfig(
                probe_sensitivity_mv_per_m=[100.0] * 8,
                probe_offset_m=[0.0] * 8,
                temperature_coefficient=0.002,
                last_calibration_date=datetime.date.today().isoformat(),
                calibration_method="static_immersion",
                reference_wave_height_m=0.1,
                calibration_frequency_hz=1.0,
            ),
            created_date=datetime.datetime.now().isoformat(),
            version="1.0.0",
        )

        # Preset Canal d'Essais
        presets["test_canal"] = LabConfiguration(
            name="Canal d'Essais Haute Fréquence",
            preset_type="test_canal",
            description="Configuration pour tests en canal avec acquisition haute fréquence",
            hardware=HardwareConfig(
                sampling_rate_hz=2000.0,
                num_channels=4,
                buffer_duration_seconds=5.0,
                anti_aliasing_cutoff_hz=400.0,
                adc_resolution_bits=18,
                voltage_range_v=(-2.5, 2.5),
                coupling="AC",
                impedance_ohms=1e6,
            ),
            processing=ProcessingConfig(
                fft_window_type="blackman",
                fft_overlap_percent=75.0,
                fft_zero_padding_factor=4,
                goda_svd_threshold=1e-12,
                enable_real_time_processing=True,
                processing_chunk_size=256,
                max_frequency_hz=10.0,
                spectral_resolution_hz=0.005,
            ),
            environment=EnvironmentConfig(
                laboratory_type="canal",
                location="Canal d'essais",
                water_depth_m=0.8,
                basin_length_m=100.0,
                basin_width_m=3.0,
                wave_maker_type="flap",
                probe_spacing_m=1.0,
                coordinate_system="cartesian",
                reference_level_m=0.0,
            ),
            calibration=CalibrationConfig(
                probe_sensitivity_mv_per_m=[150.0] * 4,
                probe_offset_m=[0.0] * 4,
                temperature_coefficient=0.001,
                last_calibration_date=datetime.date.today().isoformat(),
                calibration_method="dynamic_calibration",
                reference_wave_height_m=0.05,
                calibration_frequency_hz=2.0,
            ),
            created_date=datetime.datetime.now().isoformat(),
            version="1.0.0",
        )

        # Preset Haute Performance
        presets["high_performance"] = LabConfiguration(
            name="Configuration Haute Performance",
            preset_type="high_performance",
            description="Configuration pour acquisition haute performance avec monitoring avancé",
            hardware=HardwareConfig(
                sampling_rate_hz=2000.0,
                num_channels=16,
                buffer_duration_seconds=30.0,
                anti_aliasing_cutoff_hz=500.0,
                adc_resolution_bits=24,
                voltage_range_v=(-10.0, 10.0),
                coupling="DC",
                impedance_ohms=1e9,
            ),
            processing=ProcessingConfig(
                fft_window_type="kaiser",
                fft_overlap_percent=87.5,
                fft_zero_padding_factor=8,
                goda_svd_threshold=1e-15,
                enable_real_time_processing=True,
                processing_chunk_size=1024,
                max_frequency_hz=20.0,
                spectral_resolution_hz=0.001,
            ),
            environment=EnvironmentConfig(
                laboratory_type="basin",
                location="Laboratoire haute performance",
                water_depth_m=2.0,
                basin_length_m=80.0,
                basin_width_m=50.0,
                wave_maker_type="multi_paddle",
                probe_spacing_m=1.5,
                coordinate_system="polar",
                reference_level_m=0.0,
            ),
            calibration=CalibrationConfig(
                probe_sensitivity_mv_per_m=[200.0] * 16,
                probe_offset_m=[0.0] * 16,
                temperature_coefficient=0.0005,
                last_calibration_date=datetime.date.today().isoformat(),
                calibration_method="automated_calibration",
                reference_wave_height_m=0.2,
                calibration_frequency_hz=0.5,
            ),
            created_date=datetime.datetime.now().isoformat(),
            version="1.0.0",
        )

        # Preset Développement/Test
        presets["development"] = LabConfiguration(
            name="Configuration Développement",
            preset_type="development",
            description="Configuration pour développement et tests avec logging étendu",
            hardware=HardwareConfig(
                sampling_rate_hz=500.0,
                num_channels=2,
                buffer_duration_seconds=10.0,
                anti_aliasing_cutoff_hz=100.0,
                adc_resolution_bits=12,
                voltage_range_v=(-1.0, 1.0),
                coupling="AC",
                impedance_ohms=1e5,
            ),
            processing=ProcessingConfig(
                fft_window_type="hanning",
                fft_overlap_percent=25.0,
                fft_zero_padding_factor=1,
                goda_svd_threshold=1e-8,
                enable_real_time_processing=False,
                processing_chunk_size=128,
                max_frequency_hz=2.0,
                spectral_resolution_hz=0.02,
            ),
            environment=EnvironmentConfig(
                laboratory_type="flume",
                location="Laboratoire de développement",
                water_depth_m=0.5,
                basin_length_m=10.0,
                basin_width_m=1.0,
                wave_maker_type="piston",
                probe_spacing_m=0.5,
                coordinate_system="cartesian",
                reference_level_m=0.0,
            ),
            calibration=CalibrationConfig(
                probe_sensitivity_mv_per_m=[50.0] * 2,
                probe_offset_m=[0.0] * 2,
                temperature_coefficient=0.01,
                last_calibration_date=datetime.date.today().isoformat(),
                calibration_method="manual_calibration",
                reference_wave_height_m=0.02,
                calibration_frequency_hz=0.1,
            ),
            created_date=datetime.datetime.now().isoformat(),
            version="1.0.0",
        )

        return presets

    def list_presets(self) -> List[str]:
        """Liste les presets disponibles"""
        return list(self.presets.keys())

    def get_preset(self, preset_name: str) -> Optional[LabConfiguration]:
        """Récupère un preset par nom"""
        return self.presets.get(preset_name)

    def create_custom_config(
        self, base_preset: str, modifications: Dict[str, Any]
    ) -> LabConfiguration:
        """Crée une configuration personnalisée basée sur un preset"""
        if base_preset not in self.presets:
            raise ValueError(f"Preset '{base_preset}' non trouvé")

        # Copie du preset de base
        config = self.presets[base_preset]
        config_dict = asdict(config)

        # Application des modifications
        self._apply_modifications(config_dict, modifications)

        # Reconstruction de la configuration
        return self._dict_to_config(config_dict)

    def _apply_modifications(
        self, config_dict: Dict[str, Any], modifications: Dict[str, Any]
    ):
        """Applique les modifications à un dictionnaire de configuration"""
        for key, value in modifications.items():
            if "." in key:
                # Clé imbriquée (ex: 'hardware.sampling_rate_hz')
                parts = key.split(".")
                current = config_dict
                for part in parts[:-1]:
                    if part in current:
                        current = current[part]
                    else:
                        raise KeyError(
                            f"Clé '{part}' non trouvée dans la configuration"
                        )
                current[parts[-1]] = value
            else:
                # Clé de premier niveau
                config_dict[key] = value

    def _dict_to_config(self, config_dict: Dict[str, Any]) -> LabConfiguration:
        """Convertit un dictionnaire en LabConfiguration"""
        return LabConfiguration(
            name=config_dict["name"],
            preset_type=config_dict["preset_type"],
            description=config_dict["description"],
            hardware=HardwareConfig(**config_dict["hardware"]),
            processing=ProcessingConfig(**config_dict["processing"]),
            environment=EnvironmentConfig(**config_dict["environment"]),
            calibration=CalibrationConfig(**config_dict["calibration"]),
            created_date=config_dict["created_date"],
            version=config_dict["version"],
        )

    def save_config(
        self, config: LabConfiguration, filename: Optional[str] = None
    ) -> str:
        """Sauvegarde une configuration"""
        if filename is None:
            filename = f"{config.preset_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        config_file = self.config_dir / filename

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(asdict(config), f, indent=2, ensure_ascii=False)

        return str(config_file)

    def load_config(self, filename: str) -> LabConfiguration:
        """Charge une configuration depuis un fichier"""
        config_file = Path(filename)
        if not config_file.is_absolute():
            config_file = self.config_dir / filename

        with open(config_file, "r", encoding="utf-8") as f:
            config_dict = json.load(f)

        return self._dict_to_config(config_dict)

    def export_to_chneowave_config(self, config: LabConfiguration, output_file: str):
        """Exporte vers le format de configuration CHNeoWave"""
        chneowave_config = {
            "acquisition": {
                "sampling_rate_hz": config.hardware.sampling_rate_hz,
                "num_channels": config.hardware.num_channels,
                "buffer_duration_seconds": config.hardware.buffer_duration_seconds,
                "voltage_range_v": list(config.hardware.voltage_range_v),
                "coupling": config.hardware.coupling,
                "anti_aliasing_cutoff_hz": config.hardware.anti_aliasing_cutoff_hz,
            },
            "fft": {
                "window_type": config.processing.fft_window_type,
                "overlap_percent": config.processing.fft_overlap_percent,
                "zero_padding_factor": config.processing.fft_zero_padding_factor,
                "threads": min(8, os.cpu_count() or 4),
                "planning_effort": "FFTW_MEASURE",
                "cache_size": 200,
            },
            "goda": {
                "svd_threshold": config.processing.goda_svd_threshold,
                "use_svd_decomposition": True,
                "cache_geometry_matrices": True,
                "max_cache_size": 2000,
                "enable_parallel_processing": True,
            },
            "buffer": {
                "enable_lock_free": True,
                "alignment_bytes": 64,
                "enable_overflow_detection": True,
                "processing_chunk_size": config.processing.processing_chunk_size,
            },
            "monitoring": {
                "enable_profiling": config.preset_type == "high_performance",
                "log_level": "DEBUG" if config.preset_type == "development" else "INFO",
                "performance_metrics": True,
                "export_interval_seconds": 60,
            },
            "laboratory": {
                "name": config.name,
                "type": config.environment.laboratory_type,
                "location": config.environment.location,
                "water_depth_m": config.environment.water_depth_m,
                "probe_spacing_m": config.environment.probe_spacing_m,
                "coordinate_system": config.environment.coordinate_system,
            },
            "calibration": {
                "probe_sensitivity_mv_per_m": config.calibration.probe_sensitivity_mv_per_m,
                "probe_offset_m": config.calibration.probe_offset_m,
                "temperature_coefficient": config.calibration.temperature_coefficient,
                "last_calibration_date": config.calibration.last_calibration_date,
                "method": config.calibration.calibration_method,
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chneowave_config, f, indent=2, ensure_ascii=False)

        return output_file

    def generate_config_report(self, config: LabConfiguration) -> str:
        """Génère un rapport de configuration"""
        report = f"""
# 🌊 Rapport de Configuration CHNeoWave

**Configuration**: {config.name}
**Type**: {config.preset_type}
**Version**: {config.version}
**Créée le**: {config.created_date}

## 📝 Description

{config.description}

## ⚙️ Configuration Hardware

- **Fréquence d'échantillonnage**: {config.hardware.sampling_rate_hz} Hz
- **Nombre de canaux**: {config.hardware.num_channels}
- **Durée du buffer**: {config.hardware.buffer_duration_seconds} s
- **Filtre anti-aliasing**: {config.hardware.anti_aliasing_cutoff_hz} Hz
- **Résolution ADC**: {config.hardware.adc_resolution_bits} bits
- **Plage de tension**: {config.hardware.voltage_range_v[0]} à {config.hardware.voltage_range_v[1]} V
- **Couplage**: {config.hardware.coupling}
- **Impédance**: {config.hardware.impedance_ohms:.0e} Ω

## 🔧 Configuration Traitement

- **Fenêtre FFT**: {config.processing.fft_window_type}
- **Recouvrement FFT**: {config.processing.fft_overlap_percent}%
- **Zero-padding**: x{config.processing.fft_zero_padding_factor}
- **Seuil SVD Goda**: {config.processing.goda_svd_threshold:.0e}
- **Traitement temps réel**: {'✅ Activé' if config.processing.enable_real_time_processing else '❌ Désactivé'}
- **Taille des chunks**: {config.processing.processing_chunk_size} échantillons
- **Fréquence max**: {config.processing.max_frequency_hz} Hz
- **Résolution spectrale**: {config.processing.spectral_resolution_hz} Hz

## 🏊 Configuration Environnement

- **Type de laboratoire**: {config.environment.laboratory_type}
- **Localisation**: {config.environment.location}
- **Profondeur d'eau**: {config.environment.water_depth_m} m
- **Dimensions bassin**: {config.environment.basin_length_m} x {config.environment.basin_width_m} m
- **Type de générateur**: {config.environment.wave_maker_type}
- **Espacement sondes**: {config.environment.probe_spacing_m} m
- **Système de coordonnées**: {config.environment.coordinate_system}
- **Niveau de référence**: {config.environment.reference_level_m} m

## 🎯 Configuration Étalonnage

- **Sensibilité sondes**: {config.calibration.probe_sensitivity_mv_per_m[0]} mV/m (moyenne)
- **Offset sondes**: {config.calibration.probe_offset_m[0]} m (moyenne)
- **Coefficient température**: {config.calibration.temperature_coefficient}
- **Dernière calibration**: {config.calibration.last_calibration_date}
- **Méthode**: {config.calibration.calibration_method}
- **Hauteur de référence**: {config.calibration.reference_wave_height_m} m
- **Fréquence de calibration**: {config.calibration.calibration_frequency_hz} Hz

## 📊 Performances Estimées

### Acquisition
- **Débit de données**: {config.hardware.sampling_rate_hz * config.hardware.num_channels * 4 / 1024:.1f} KB/s
- **Mémoire buffer**: {config.hardware.sampling_rate_hz * config.hardware.buffer_duration_seconds * config.hardware.num_channels * 4 / 1024 / 1024:.1f} MB
- **Latence estimée**: {1000 / config.hardware.sampling_rate_hz:.1f} ms

### Traitement
- **Points FFT**: {config.processing.processing_chunk_size * config.processing.fft_zero_padding_factor}
- **Fréquence de traitement**: {config.hardware.sampling_rate_hz / config.processing.processing_chunk_size:.1f} Hz
- **Résolution temporelle**: {config.processing.processing_chunk_size / config.hardware.sampling_rate_hz:.3f} s

## 🎯 Recommandations

### Hardware
- **CPU**: Minimum 4 cœurs, recommandé 8 cœurs
- **RAM**: Minimum {config.hardware.sampling_rate_hz * config.hardware.buffer_duration_seconds * config.hardware.num_channels * 8 / 1024 / 1024:.0f} MB
- **Stockage**: SSD pour données temporaires

### Réseau
- **Bande passante**: {config.hardware.sampling_rate_hz * config.hardware.num_channels * 4 * 8 / 1024 / 1024:.1f} Mbps pour streaming

---

*Rapport généré automatiquement par CHNeoWave Lab Configurator*
"""

        return report

    def validate_config(self, config: LabConfiguration) -> List[str]:
        """Valide une configuration et retourne les avertissements"""
        warnings = []

        # Validation hardware
        if config.hardware.sampling_rate_hz < 100:
            warnings.append("⚠️ Fréquence d'échantillonnage très faible (<100 Hz)")

        if config.hardware.sampling_rate_hz > 10000:
            warnings.append("⚠️ Fréquence d'échantillonnage très élevée (>10 kHz)")

        if config.hardware.num_channels > 32:
            warnings.append("⚠️ Nombre de canaux très élevé (>32)")

        if config.hardware.buffer_duration_seconds > 60:
            warnings.append("⚠️ Durée de buffer très longue (>60s), risque de mémoire")

        # Validation traitement
        nyquist = config.hardware.sampling_rate_hz / 2
        if config.hardware.anti_aliasing_cutoff_hz > nyquist * 0.8:
            warnings.append(
                f"⚠️ Filtre anti-aliasing proche de Nyquist ({nyquist:.1f} Hz)"
            )

        if config.processing.fft_overlap_percent > 90:
            warnings.append("⚠️ Recouvrement FFT très élevé (>90%), impact performance")

        if config.processing.fft_zero_padding_factor > 8:
            warnings.append("⚠️ Zero-padding très élevé (>8x), impact mémoire")

        # Validation environnement
        if config.environment.water_depth_m < 0.1:
            warnings.append("⚠️ Profondeur d'eau très faible (<10 cm)")

        if config.environment.probe_spacing_m < 0.1:
            warnings.append("⚠️ Espacement sondes très faible (<10 cm)")

        # Validation calibration
        if any(s < 10 for s in config.calibration.probe_sensitivity_mv_per_m):
            warnings.append("⚠️ Sensibilité sonde très faible (<10 mV/m)")

        if any(s > 1000 for s in config.calibration.probe_sensitivity_mv_per_m):
            warnings.append("⚠️ Sensibilité sonde très élevée (>1000 mV/m)")

        return warnings


def main():
    """Interface en ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Configurateur de laboratoire CHNeoWave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s --list-presets
  %(prog)s --preset mediterranean_basin --output mon_labo.json
  %(prog)s --preset test_canal --modify hardware.sampling_rate_hz=1500
  %(prog)s --load mon_labo.json --export-chneowave config.json
  %(prog)s --preset high_performance --report
""",
    )

    parser.add_argument(
        "--list-presets", action="store_true", help="Liste les presets disponibles"
    )

    parser.add_argument("--preset", type=str, help="Nom du preset à utiliser")

    parser.add_argument(
        "--load", type=str, help="Charge une configuration depuis un fichier"
    )

    parser.add_argument(
        "--output", type=str, help="Fichier de sortie pour la configuration"
    )

    parser.add_argument(
        "--export-chneowave", type=str, help="Exporte vers le format CHNeoWave"
    )

    parser.add_argument(
        "--modify", action="append", help="Modifications (format: clé=valeur)"
    )

    parser.add_argument(
        "--report", action="store_true", help="Génère un rapport de configuration"
    )

    parser.add_argument(
        "--validate", action="store_true", help="Valide la configuration"
    )

    args = parser.parse_args()

    configurator = MediterraneanLabConfigurator()

    # Liste des presets
    if args.list_presets:
        print("🌊 Presets disponibles:")
        for preset in configurator.list_presets():
            config = configurator.get_preset(preset)
            print(f"  - {preset}: {config.name}")
            print(f"    {config.description}")
        return

    # Chargement de la configuration
    config = None

    if args.load:
        print(f"📁 Chargement de {args.load}...")
        config = configurator.load_config(args.load)
    elif args.preset:
        print(f"🎯 Utilisation du preset '{args.preset}'...")
        config = configurator.get_preset(args.preset)
        if not config:
            print(f"❌ Preset '{args.preset}' non trouvé")
            return
    else:
        print("❌ Spécifiez --preset ou --load")
        return

    # Application des modifications
    if args.modify:
        print("🔧 Application des modifications...")
        modifications = {}
        for mod in args.modify:
            if "=" not in mod:
                print(f"❌ Format modification invalide: {mod}")
                return
            key, value = mod.split("=", 1)
            # Conversion automatique du type
            try:
                if "." in value:
                    value = float(value)
                elif value.isdigit():
                    value = int(value)
                elif value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
            except ValueError:
                pass  # Garder comme string
            modifications[key] = value

        config = configurator.create_custom_config(config.preset_type, modifications)

    # Validation
    if args.validate or args.report:
        warnings = configurator.validate_config(config)
        if warnings:
            print("⚠️ Avertissements de validation:")
            for warning in warnings:
                print(f"  {warning}")
        else:
            print("✅ Configuration valide")

    # Génération du rapport
    if args.report:
        print("\n" + configurator.generate_config_report(config))

    # Sauvegarde
    if args.output:
        output_file = configurator.save_config(config, args.output)
        print(f"💾 Configuration sauvegardée: {output_file}")

    # Export CHNeoWave
    if args.export_chneowave:
        configurator.export_to_chneowave_config(config, args.export_chneowave)
        print(f"📤 Configuration CHNeoWave exportée: {args.export_chneowave}")

    print(f"\n🌊 Configuration '{config.name}' prête à l'emploi!")


if __name__ == "__main__":
    main()
