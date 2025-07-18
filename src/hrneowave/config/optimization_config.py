#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration des optimisations CHNeoWave

Ce module centralise tous les paramètres d'optimisation pour les algorithmes
FFT, Goda et les buffers circulaires utilisés dans CHNeoWave.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FFTOptimizationConfig:
    """Configuration pour l'optimisation FFT"""

    use_pyfftw: bool = True
    wisdom_file: Optional[str] = "fftw_wisdom.dat"
    threads: int = field(default_factory=lambda: os.cpu_count() or 4)
    planning_effort: str = "FFTW_MEASURE"  # FFTW_ESTIMATE, FFTW_MEASURE, FFTW_PATIENT
    cache_size: int = 100  # Nombre de plans FFT en cache
    enable_simd: bool = True

    def __post_init__(self):
        """Validation des paramètres FFT"""
        valid_efforts = [
            "FFTW_ESTIMATE",
            "FFTW_MEASURE",
            "FFTW_PATIENT",
            "FFTW_EXHAUSTIVE",
        ]
        if self.planning_effort not in valid_efforts:
            raise ValueError(f"planning_effort doit être dans {valid_efforts}")

        if self.threads < 1:
            self.threads = 1
        elif self.threads > 32:
            self.threads = 32


@dataclass
class GodaOptimizationConfig:
    """Configuration pour l'optimisation de l'analyse Goda"""

    use_svd_decomposition: bool = True
    svd_threshold: float = 1e-12
    cache_geometry_matrices: bool = True
    cache_dispersion_relation: bool = True
    max_cache_size: int = 1000
    enable_parallel_processing: bool = True
    numerical_stability_check: bool = True

    def __post_init__(self):
        """Validation des paramètres Goda"""
        if self.svd_threshold <= 0:
            raise ValueError("svd_threshold doit être positif")

        if self.max_cache_size < 10:
            self.max_cache_size = 10


@dataclass
class CircularBufferConfig:
    """Configuration pour les buffers circulaires"""

    default_size: int = 1000
    enable_lock_free: bool = True
    enable_overflow_detection: bool = True
    enable_statistics: bool = True
    memory_mapping: bool = False
    alignment_bytes: int = 64  # Alignement mémoire pour SIMD

    def __post_init__(self):
        """Validation des paramètres buffer"""
        if self.default_size < 100:
            raise ValueError("default_size doit être >= 100")

        if self.alignment_bytes not in [16, 32, 64]:
            self.alignment_bytes = 64


@dataclass
class AcquisitionConfig:
    """Configuration pour l'acquisition temps réel"""

    sampling_rate_hz: float = 1000.0
    num_channels: int = 4
    buffer_duration_seconds: float = 10.0
    enable_anti_aliasing: bool = True
    anti_aliasing_cutoff_hz: float = 250.0
    enable_real_time_processing: bool = True
    processing_chunk_size: int = 512

    def __post_init__(self):
        """Validation des paramètres acquisition"""
        if self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz doit être positif")

        if self.num_channels < 1 or self.num_channels > 16:
            raise ValueError("num_channels doit être entre 1 et 16")

        if self.anti_aliasing_cutoff_hz >= self.sampling_rate_hz / 2:
            self.anti_aliasing_cutoff_hz = self.sampling_rate_hz / 2.5


@dataclass
class PerformanceConfig:
    """Configuration pour le monitoring des performances"""

    enable_profiling: bool = False
    enable_benchmarking: bool = True
    benchmark_iterations: int = 100
    memory_monitoring: bool = True
    latency_monitoring: bool = True
    export_metrics: bool = True
    metrics_file: str = "performance_metrics.json"


# Alias pour compatibilité avec les tests
FFTConfig = FFTOptimizationConfig
GodaConfig = GodaOptimizationConfig
BufferConfig = CircularBufferConfig


class CHNeoWaveOptimizationConfig:
    """Configuration principale des optimisations CHNeoWave"""

    def __init__(self, config_file: Optional[str] = None):
        self.fft = FFTOptimizationConfig()
        self.goda = GodaOptimizationConfig()
        self.buffer = CircularBufferConfig()
        self.acquisition = AcquisitionConfig()
        self.performance = PerformanceConfig()

        if config_file:
            self.load_from_file(config_file)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire"""
        from dataclasses import asdict
        return {
            "fft": asdict(self.fft),
            "goda": asdict(self.goda),
            "buffer": asdict(self.buffer),
            "acquisition": asdict(self.acquisition),
            "performance": asdict(self.performance),
        }

    def load_from_file(self, config_file: str):
        """Charge la configuration depuis un fichier JSON"""
        import json

        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(
                f"Fichier de configuration non trouvé: {config_file}"
            )

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        # Mise à jour des configurations
        if "fft" in config_data:
            for key, value in config_data["fft"].items():
                if hasattr(self.fft, key):
                    setattr(self.fft, key, value)

        if "goda" in config_data:
            for key, value in config_data["goda"].items():
                if hasattr(self.goda, key):
                    setattr(self.goda, key, value)

        if "buffer" in config_data:
            for key, value in config_data["buffer"].items():
                if hasattr(self.buffer, key):
                    setattr(self.buffer, key, value)

        if "acquisition" in config_data:
            for key, value in config_data["acquisition"].items():
                if hasattr(self.acquisition, key):
                    setattr(self.acquisition, key, value)

        if "performance" in config_data:
            for key, value in config_data["performance"].items():
                if hasattr(self.performance, key):
                    setattr(self.performance, key, value)

    def save_to_file(self, config_file: str):
        """Sauvegarde la configuration dans un fichier JSON"""
        import json
        from dataclasses import asdict

        config_data = {
            "fft": asdict(self.fft),
            "goda": asdict(self.goda),
            "buffer": asdict(self.buffer),
            "acquisition": asdict(self.acquisition),
            "performance": asdict(self.performance),
        }

        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

    def get_environment_config(self) -> Dict[str, Any]:
        """Récupère la configuration depuis les variables d'environnement"""
        env_config = {}

        # Configuration FFT
        if "CHNEOWAVE_FFT_THREADS" in os.environ:
            env_config.setdefault("fft", {})["threads"] = int(
                os.environ["CHNEOWAVE_FFT_THREADS"]
            )

        if "CHNEOWAVE_FFT_PLANNING" in os.environ:
            env_config.setdefault("fft", {})["planning_effort"] = os.environ[
                "CHNEOWAVE_FFT_PLANNING"
            ]

        # Configuration acquisition
        if "CHNEOWAVE_SAMPLING_RATE" in os.environ:
            env_config.setdefault("acquisition", {})["sampling_rate_hz"] = float(
                os.environ["CHNEOWAVE_SAMPLING_RATE"]
            )

        if "CHNEOWAVE_NUM_CHANNELS" in os.environ:
            env_config.setdefault("acquisition", {})["num_channels"] = int(
                os.environ["CHNEOWAVE_NUM_CHANNELS"]
            )

        # Configuration buffer
        if "CHNEOWAVE_BUFFER_SIZE" in os.environ:
            env_config.setdefault("buffer", {})["default_size"] = int(
                os.environ["CHNEOWAVE_BUFFER_SIZE"]
            )

        return env_config

    def apply_laboratory_preset(self, preset_name: str):
        """Applique un preset de configuration pour différents types de laboratoires"""
        presets = {
            "mediterranean_basin": {
                "acquisition": {
                    "sampling_rate_hz": 1000.0,
                    "num_channels": 8,
                    "buffer_duration_seconds": 15.0,
                    "anti_aliasing_cutoff_hz": 200.0,
                },
                "fft": {
                    "threads": 4,
                    "planning_effort": "FFTW_MEASURE",
                    "cache_size": 200,
                },
                "goda": {"cache_geometry_matrices": True, "max_cache_size": 2000},
            },
            "channel_testing": {
                "acquisition": {
                    "sampling_rate_hz": 2000.0,
                    "num_channels": 4,
                    "buffer_duration_seconds": 5.0,
                    "anti_aliasing_cutoff_hz": 400.0,
                },
                "fft": {
                    "threads": 2,
                    "planning_effort": "FFTW_ESTIMATE",
                    "cache_size": 50,
                },
            },
            "high_performance": {
                "acquisition": {
                    "sampling_rate_hz": 2000.0,
                    "num_channels": 16,
                    "buffer_duration_seconds": 30.0,
                },
                "fft": {
                    "threads": 8,
                    "planning_effort": "FFTW_PATIENT",
                    "cache_size": 500,
                },
                "goda": {"enable_parallel_processing": True, "max_cache_size": 5000},
                "performance": {"enable_profiling": True, "enable_benchmarking": True},
            },
        }

        if preset_name not in presets:
            available = list(presets.keys())
            raise ValueError(
                f"Preset '{preset_name}' non disponible. Disponibles: {available}"
            )

        preset = presets[preset_name]

        # Application du preset
        for section, config in preset.items():
            section_obj = getattr(self, section)
            for key, value in config.items():
                if hasattr(section_obj, key):
                    setattr(section_obj, key, value)


# Configuration globale par défaut
default_config = CHNeoWaveOptimizationConfig()


# Fonction utilitaire pour obtenir la configuration
def get_optimization_config(
    config_file: Optional[str] = None,
) -> CHNeoWaveOptimizationConfig:
    """Obtient la configuration d'optimisation CHNeoWave"""
    if config_file:
        return CHNeoWaveOptimizationConfig(config_file)
    return default_config


def main():
    """Interface CLI pour l'optimiseur de configuration CHNeoWave"""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Optimiseur de configuration CHNeoWave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s --preset mediterranean_basin --save config.json
  %(prog)s --load config.json --optimize
  %(prog)s --benchmark --threads 8
  %(prog)s --validate config.json
""",
    )

    parser.add_argument(
        "--preset",
        type=str,
        choices=["mediterranean_basin", "channel_testing", "high_performance"],
        help="Appliquer un preset de laboratoire",
    )

    parser.add_argument(
        "--load", type=str, help="Charger une configuration depuis un fichier"
    )

    parser.add_argument(
        "--save", type=str, help="Sauvegarder la configuration vers un fichier"
    )

    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Optimiser automatiquement la configuration",
    )

    parser.add_argument(
        "--benchmark", action="store_true", help="Exécuter un benchmark de performance"
    )

    parser.add_argument("--threads", type=int, help="Nombre de threads FFT à utiliser")

    parser.add_argument(
        "--validate", type=str, help="Valider un fichier de configuration"
    )

    parser.add_argument(
        "--show", action="store_true", help="Afficher la configuration actuelle"
    )

    args = parser.parse_args()

    # Chargement de la configuration
    if args.load:
        print(f"📁 Chargement de {args.load}...")
        config = CHNeoWaveOptimizationConfig(args.load)
    else:
        config = get_optimization_config()

    # Application du preset
    if args.preset:
        print(f"🎯 Application du preset '{args.preset}'...")
        config.apply_laboratory_preset(args.preset)

    # Optimisation automatique
    if args.optimize:
        print("⚡ Optimisation automatique...")
        import os

        # Optimisation basée sur le hardware
        cpu_count = os.cpu_count() or 4
        config.fft.threads = min(cpu_count, 8)
        config.fft.planning_effort = "FFTW_MEASURE"
        config.goda.enable_parallel_processing = True
        config.buffer.enable_lock_free = True

        print(f"✅ Configuration optimisée pour {cpu_count} cœurs CPU")

    # Configuration manuelle des threads
    if args.threads:
        config.fft.threads = args.threads
        print(f"🔧 Threads FFT configurés: {args.threads}")

    # Benchmark
    if args.benchmark:
        print("📊 Exécution du benchmark...")
        try:
            import numpy as np
            import time

            # Test FFT simple
            data = np.random.random(1024)
            start_time = time.time()
            for _ in range(100):
                np.fft.fft(data)
            numpy_time = time.time() - start_time

            print(f"  - NumPy FFT (100x): {numpy_time:.3f}s")
            print(f"  - Threads configurés: {config.fft.threads}")
            print(f"  - Cache FFT: {config.fft.cache_size} plans")

        except ImportError:
            print("⚠️ NumPy non disponible pour le benchmark")

    # Validation
    if args.validate:
        print(f"🔍 Validation de {args.validate}...")
        try:
            test_config = CHNeoWaveOptimizationConfig(args.validate)
            print("✅ Configuration valide")
            print(f"  - FFT threads: {test_config.fft.threads}")
            print(f"  - Sampling rate: {test_config.acquisition.sampling_rate_hz} Hz")
            print(f"  - Channels: {test_config.acquisition.num_channels}")
        except Exception as e:
            print(f"❌ Configuration invalide: {e}")
            return 1

    # Affichage de la configuration
    if args.show or not any(
        [args.preset, args.load, args.optimize, args.benchmark, args.validate]
    ):
        print("\n🌊 Configuration CHNeoWave:")
        print(f"\n📡 Acquisition:")
        print(f"  - Fréquence: {config.acquisition.sampling_rate_hz} Hz")
        print(f"  - Canaux: {config.acquisition.num_channels}")
        print(f"  - Buffer: {config.acquisition.buffer_duration_seconds}s")

        print(f"\n⚡ FFT:")
        print(f"  - Threads: {config.fft.threads}")
        print(f"  - Planning: {config.fft.planning_effort}")
        print(f"  - Cache: {config.fft.cache_size} plans")

        print(f"\n🌊 Goda:")
        print(f"  - SVD: {'✅' if config.goda.use_svd_decomposition else '❌'}")
        print(f"  - Cache: {'✅' if config.goda.cache_geometry_matrices else '❌'}")
        print(
            f"  - Parallèle: {'✅' if config.goda.enable_parallel_processing else '❌'}"
        )

        print(f"\n💾 Buffer:")
        print(f"  - Lock-free: {'✅' if config.buffer.enable_lock_free else '❌'}")
        print(f"  - Alignement: {config.buffer.alignment_bytes} bytes")
        print(
            f"  - Overflow detection: {'✅' if config.buffer.enable_overflow_detection else '❌'}"
        )

    # Sauvegarde
    if args.save:
        config.save_to_file(args.save)
        print(f"💾 Configuration sauvegardée: {args.save}")

    print("\n🌊 CHNeoWave Config Optimizer terminé!")
    return 0


if __name__ == "__main__":
    exit(main())
