#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation des exigences matérielles pour CHNeoWave

Ce module définit et valide les exigences matérielles pour le bon fonctionnement
des optimisations CHNeoWave en laboratoire d'étude maritime.

Exigences:
- Sondes: 3-11 kHz de bande passante
- Anti-aliasing: < 250 Hz pour éviter le repliement
- Fréquence d'échantillonnage: configurable 100-2000 Hz
- Nombre de sondes: 4-16 sondes simultanées
"""

import os
import sys
import json
import numpy as np
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
import warnings


@dataclass
class ProbeSpecifications:
    """Spécifications d'une sonde de houle"""

    model: str
    bandwidth_hz: Tuple[float, float]  # (min_freq, max_freq)
    sensitivity_mv_m: float  # Sensibilité en mV/m
    noise_level_mv: float  # Niveau de bruit en mV RMS
    max_wave_height_m: float  # Hauteur de vague maximale
    calibration_date: Optional[str] = None
    serial_number: Optional[str] = None


@dataclass
class AcquisitionSystemSpecs:
    """Spécifications du système d'acquisition"""

    model: str
    max_channels: int
    max_sample_rate_hz: float
    resolution_bits: int
    input_range_v: Tuple[float, float]
    anti_alias_cutoff_hz: float
    anti_alias_order: int
    noise_floor_db: float


@dataclass
class LaboratorySetup:
    """Configuration complète du laboratoire"""

    basin_length_m: float
    basin_width_m: float
    water_depth_m: float
    wave_maker_type: str
    probe_positions_m: List[float]
    acquisition_system: AcquisitionSystemSpecs
    probes: List[ProbeSpecifications]
    environmental_conditions: Dict[str, float]


class HardwareValidator:
    """Validateur des exigences matérielles"""

    # Exigences minimales CHNeoWave
    MIN_PROBE_BANDWIDTH = (0.05, 3.0)  # Hz - bande passante minimale
    MAX_PROBE_BANDWIDTH = (0.01, 11.0)  # Hz - bande passante optimale
    MAX_ANTI_ALIAS_FREQ = 250.0  # Hz - fréquence anti-aliasing max
    MIN_SAMPLE_RATE = 100.0  # Hz - fréquence d'échantillonnage min
    MAX_SAMPLE_RATE = 2000.0  # Hz - fréquence d'échantillonnage max
    MIN_PROBES = 3  # Nombre minimal de sondes
    MAX_PROBES = 16  # Nombre maximal de sondes
    MIN_RESOLUTION = 12  # Bits - résolution ADC minimale
    MAX_NOISE_LEVEL = 1.0  # mV RMS - niveau de bruit maximal

    def __init__(self):
        self.validation_results = []
        self.warnings_list = []
        self.errors_list = []

    def validate_probe(self, probe: ProbeSpecifications) -> bool:
        """Valide une sonde individuelle"""
        valid = True

        # Vérifier la bande passante
        min_freq, max_freq = probe.bandwidth_hz
        if min_freq > self.MIN_PROBE_BANDWIDTH[0]:
            self.warnings_list.append(
                f"Sonde {probe.model}: fréquence minimale {min_freq} Hz > {self.MIN_PROBE_BANDWIDTH[0]} Hz recommandée"
            )

        if max_freq < self.MIN_PROBE_BANDWIDTH[1]:
            self.errors_list.append(
                f"Sonde {probe.model}: fréquence maximale {max_freq} Hz < {self.MIN_PROBE_BANDWIDTH[1]} Hz requise"
            )
            valid = False

        # Vérifier le niveau de bruit
        if probe.noise_level_mv > self.MAX_NOISE_LEVEL:
            self.warnings_list.append(
                f"Sonde {probe.model}: niveau de bruit {probe.noise_level_mv} mV > {self.MAX_NOISE_LEVEL} mV recommandé"
            )

        # Vérifier la sensibilité
        if probe.sensitivity_mv_m < 10.0:
            self.warnings_list.append(
                f"Sonde {probe.model}: sensibilité {probe.sensitivity_mv_m} mV/m faible (< 10 mV/m)"
            )

        return valid

    def validate_acquisition_system(self, system: AcquisitionSystemSpecs) -> bool:
        """Valide le système d'acquisition"""
        valid = True

        # Vérifier la fréquence d'échantillonnage
        if system.max_sample_rate_hz < self.MAX_SAMPLE_RATE:
            self.warnings_list.append(
                f"Système {system.model}: fréquence max {system.max_sample_rate_hz} Hz < {self.MAX_SAMPLE_RATE} Hz optimale"
            )

        # Vérifier la résolution
        if system.resolution_bits < self.MIN_RESOLUTION:
            self.errors_list.append(
                f"Système {system.model}: résolution {system.resolution_bits} bits < {self.MIN_RESOLUTION} bits requise"
            )
            valid = False

        # Vérifier l'anti-aliasing
        if system.anti_alias_cutoff_hz > self.MAX_ANTI_ALIAS_FREQ:
            self.errors_list.append(
                f"Système {system.model}: anti-aliasing {system.anti_alias_cutoff_hz} Hz > {self.MAX_ANTI_ALIAS_FREQ} Hz max"
            )
            valid = False

        # Vérifier le nombre de canaux
        if system.max_channels < self.MIN_PROBES:
            self.errors_list.append(
                f"Système {system.model}: {system.max_channels} canaux < {self.MIN_PROBES} canaux minimum"
            )
            valid = False

        return valid

    def validate_laboratory_setup(self, setup: LaboratorySetup) -> bool:
        """Valide la configuration complète du laboratoire"""
        valid = True

        # Vérifier le nombre de sondes
        n_probes = len(setup.probe_positions_m)
        if n_probes < self.MIN_PROBES:
            self.errors_list.append(
                f"Configuration: {n_probes} sondes < {self.MIN_PROBES} sondes minimum"
            )
            valid = False
        elif n_probes > self.MAX_PROBES:
            self.warnings_list.append(
                f"Configuration: {n_probes} sondes > {self.MAX_PROBES} sondes optimales"
            )

        # Vérifier l'espacement des sondes
        positions = np.array(setup.probe_positions_m)
        spacings = np.diff(positions)
        min_spacing = np.min(spacings)
        max_spacing = np.max(spacings)

        if min_spacing < 0.1:
            self.warnings_list.append(
                f"Configuration: espacement minimal {min_spacing:.2f} m < 0.1 m recommandé"
            )

        if max_spacing > 1.0:
            self.warnings_list.append(
                f"Configuration: espacement maximal {max_spacing:.2f} m > 1.0 m recommandé"
            )

        # Vérifier la profondeur d'eau
        if setup.water_depth_m < 0.3:
            self.warnings_list.append(
                f"Configuration: profondeur {setup.water_depth_m} m < 0.3 m recommandée"
            )
        elif setup.water_depth_m > 2.0:
            self.warnings_list.append(
                f"Configuration: profondeur {setup.water_depth_m} m > 2.0 m (vérifier théorie eau peu profonde)"
            )

        # Valider chaque sonde
        for i, probe in enumerate(setup.probes):
            if not self.validate_probe(probe):
                valid = False

        # Valider le système d'acquisition
        if not self.validate_acquisition_system(setup.acquisition_system):
            valid = False

        return valid

    def calculate_nyquist_requirements(self, max_frequency: float) -> Dict[str, float]:
        """Calcule les exigences de Nyquist pour une fréquence maximale"""
        nyquist_freq = 2 * max_frequency
        recommended_fs = 2.5 * nyquist_freq  # Facteur de sécurité
        anti_alias_freq = 0.8 * nyquist_freq  # Marge pour l'anti-aliasing

        return {
            "max_frequency_hz": max_frequency,
            "nyquist_frequency_hz": nyquist_freq,
            "min_sample_rate_hz": nyquist_freq,
            "recommended_sample_rate_hz": recommended_fs,
            "anti_alias_cutoff_hz": anti_alias_freq,
        }

    def generate_report(self, setup: LaboratorySetup) -> Dict:
        """Génère un rapport de validation complet"""
        self.validation_results.clear()
        self.warnings_list.clear()
        self.errors_list.clear()

        # Validation principale
        is_valid = self.validate_laboratory_setup(setup)

        # Calculs de Nyquist
        max_probe_freq = max(probe.bandwidth_hz[1] for probe in setup.probes)
        nyquist_req = self.calculate_nyquist_requirements(max_probe_freq)

        # Recommandations de configuration
        recommendations = self._generate_recommendations(setup, nyquist_req)

        report = {
            "validation_date": np.datetime64("now").astype(str),
            "setup_valid": is_valid,
            "errors": self.errors_list,
            "warnings": self.warnings_list,
            "nyquist_requirements": nyquist_req,
            "recommendations": recommendations,
            "setup_summary": {
                "n_probes": len(setup.probes),
                "probe_spacing_m": np.diff(setup.probe_positions_m).tolist(),
                "water_depth_m": setup.water_depth_m,
                "acquisition_system": setup.acquisition_system.model,
                "max_sample_rate_hz": setup.acquisition_system.max_sample_rate_hz,
            },
        }

        return report

    def _generate_recommendations(
        self, setup: LaboratorySetup, nyquist_req: Dict
    ) -> List[str]:
        """Génère des recommandations d'amélioration"""
        recommendations = []

        # Recommandations de fréquence d'échantillonnage
        if (
            setup.acquisition_system.max_sample_rate_hz
            < nyquist_req["recommended_sample_rate_hz"]
        ):
            recommendations.append(
                f"Augmenter la fréquence d'échantillonnage à {nyquist_req['recommended_sample_rate_hz']:.0f} Hz"
            )

        # Recommandations d'anti-aliasing
        if (
            setup.acquisition_system.anti_alias_cutoff_hz
            > nyquist_req["anti_alias_cutoff_hz"]
        ):
            recommendations.append(
                f"Réduire la fréquence de coupure anti-aliasing à {nyquist_req['anti_alias_cutoff_hz']:.0f} Hz"
            )

        # Recommandations de sondes
        if len(setup.probes) < 6:
            recommendations.append(
                "Ajouter des sondes pour améliorer la résolution spatiale (6-8 sondes recommandées)"
            )

        # Recommandations d'espacement
        spacings = np.diff(setup.probe_positions_m)
        if np.std(spacings) > 0.1:
            recommendations.append(
                "Uniformiser l'espacement des sondes pour une meilleure analyse"
            )

        return recommendations


# Configurations prédéfinies pour différents laboratoires
CONFIGURATIONS_TYPES = {
    "laboratoire_standard": {
        "description": "Configuration standard pour laboratoire d'étude maritime",
        "basin_length_m": 15.0,
        "basin_width_m": 3.0,
        "water_depth_m": 0.5,
        "n_probes": 8,
        "probe_spacing_m": 0.3,
        "sample_rate_hz": 500,
        "anti_alias_hz": 200,
    },
    "laboratoire_haute_performance": {
        "description": "Configuration haute performance pour études avancées",
        "basin_length_m": 25.0,
        "basin_width_m": 5.0,
        "water_depth_m": 0.8,
        "n_probes": 16,
        "probe_spacing_m": 0.2,
        "sample_rate_hz": 2000,
        "anti_alias_hz": 250,
    },
    "laboratoire_compact": {
        "description": "Configuration compacte pour tests rapides",
        "basin_length_m": 8.0,
        "basin_width_m": 2.0,
        "water_depth_m": 0.3,
        "n_probes": 4,
        "probe_spacing_m": 0.5,
        "sample_rate_hz": 200,
        "anti_alias_hz": 80,
    },
}


def create_example_setup(config_type: str = "laboratoire_standard") -> LaboratorySetup:
    """Crée une configuration d'exemple"""
    if config_type not in CONFIGURATIONS_TYPES:
        raise ValueError(f"Type de configuration inconnu: {config_type}")

    config = CONFIGURATIONS_TYPES[config_type]

    # Positions des sondes
    n_probes = config["n_probes"]
    spacing = config["probe_spacing_m"]
    positions = [i * spacing for i in range(n_probes)]

    # Spécifications des sondes (exemple)
    probe_spec = ProbeSpecifications(
        model="HR-WaveProbe-2024",
        bandwidth_hz=(0.05, 5.0),
        sensitivity_mv_m=50.0,
        noise_level_mv=0.5,
        max_wave_height_m=0.3,
        calibration_date="2024-01-15",
    )

    probes = [probe_spec for _ in range(n_probes)]

    # Système d'acquisition (exemple)
    acquisition = AcquisitionSystemSpecs(
        model="NI-DAQ-9234",
        max_channels=16,
        max_sample_rate_hz=config["sample_rate_hz"],
        resolution_bits=16,
        input_range_v=(-5.0, 5.0),
        anti_alias_cutoff_hz=config["anti_alias_hz"],
        anti_alias_order=8,
        noise_floor_db=-90,
    )

    # Configuration complète
    setup = LaboratorySetup(
        basin_length_m=config["basin_length_m"],
        basin_width_m=config["basin_width_m"],
        water_depth_m=config["water_depth_m"],
        wave_maker_type="Piston",
        probe_positions_m=positions,
        acquisition_system=acquisition,
        probes=probes,
        environmental_conditions={
            "temperature_c": 20.0,
            "humidity_percent": 60.0,
            "atmospheric_pressure_hpa": 1013.25,
        },
    )

    return setup


def main():
    """Fonction principale pour validation des exigences matérielles"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validation des exigences matérielles CHNeoWave"
    )
    parser.add_argument(
        "--config",
        choices=list(CONFIGURATIONS_TYPES.keys()),
        default="laboratoire_standard",
        help="Type de configuration",
    )
    parser.add_argument(
        "--output", default="hardware_validation_report.json", help="Fichier de rapport"
    )
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")

    args = parser.parse_args()

    print(f"🔧 Validation des exigences matérielles CHNeoWave")
    print(f"📋 Configuration: {args.config}")

    # Créer la configuration d'exemple
    setup = create_example_setup(args.config)

    # Valider
    validator = HardwareValidator()
    report = validator.generate_report(setup)

    # Afficher les résultats
    if args.verbose:
        print(f"\n📊 Résultats de validation:")
        print(f"  ✓ Configuration valide: {report['setup_valid']}")
        print(f"  ⚠️  Avertissements: {len(report['warnings'])}")
        print(f"  ❌ Erreurs: {len(report['errors'])}")

        if report["warnings"]:
            print("\n⚠️  Avertissements:")
            for warning in report["warnings"]:
                print(f"    - {warning}")

        if report["errors"]:
            print("\n❌ Erreurs:")
            for error in report["errors"]:
                print(f"    - {error}")

        if report["recommendations"]:
            print("\n💡 Recommandations:")
            for rec in report["recommendations"]:
                print(f"    - {rec}")

    # Sauvegarder le rapport
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Rapport sauvegardé: {args.output}")

    # Afficher les exigences de Nyquist
    nyquist = report["nyquist_requirements"]
    print(f"\n📐 Exigences de Nyquist:")
    print(f"  Fréquence max: {nyquist['max_frequency_hz']:.1f} Hz")
    print(f"  Fréquence Nyquist: {nyquist['nyquist_frequency_hz']:.1f} Hz")
    print(f"  Fréq. échantillonnage min: {nyquist['min_sample_rate_hz']:.1f} Hz")
    print(
        f"  Fréq. échantillonnage recommandée: {nyquist['recommended_sample_rate_hz']:.1f} Hz"
    )
    print(f"  Anti-aliasing recommandé: {nyquist['anti_alias_cutoff_hz']:.1f} Hz")

    return 0 if report["setup_valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
