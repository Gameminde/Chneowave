#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration unifiée pour les buffers circulaires CHNeoWave

Ce module unifie les configurations BufferConfig et CircularBufferConfig
en une seule source de vérité pour tous les buffers du système.

Auteur: WaveBuffer-Fixer
Version: 3.0.0
Date: 2025
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from pathlib import Path
import time
from collections import deque
from enum import Enum


class OverflowMode(Enum):
    """Modes de gestion des débordements de buffer"""
    OVERWRITE = "overwrite"
    BLOCK = "block"
    EXPAND = "expand"


class PerformanceLevel(Enum):
    """Niveaux de performance pour l'optimisation"""
    MINIMUM = "minimum"
    BALANCED = "balanced"
    MAXIMUM = "maximum"


@dataclass
class UnifiedBufferConfig:
    """Configuration unifiée pour tous les buffers circulaires CHNeoWave"""
    
    # Paramètres principaux
    n_channels: int = 4
    buffer_size: int = 8192  # Nombre d'échantillons par canal
    sample_rate: float = 32.0  # Hz - fréquence d'échantillonnage
    dtype: np.dtype = field(default_factory=lambda: np.float64)
    
    # Gestion des débordements
    overflow_mode: OverflowMode = OverflowMode.OVERWRITE
    enable_overflow_detection: bool = True
    overflow_threshold: float = 0.85  # Seuil d'alerte (0-1)
    overflow_threshold_percent: float = 85.0  # Seuil d'alerte (legacy)
    
    # Optimisations performance
    enable_lock_free: bool = True
    enable_statistics: bool = True
    enable_timing: bool = True
    performance_level: PerformanceLevel = PerformanceLevel.BALANCED
    
    # Optimisations mémoire
    enable_memory_mapping: bool = False
    memory_mapping: bool = False  # Legacy alias
    alignment_bytes: int = 64  # Alignement SIMD
    enable_zero_copy: bool = True
    enable_simd: bool = True
    
    # Paramètres avancés
    target_latency_ms: float = 10.0  # Latence cible
    max_write_latency_ms: float = 1.0  # Latence max acceptable
    max_read_latency_ms: float = 0.5
    auto_resize: bool = False  # Redimensionnement automatique
    resize_factor: float = 1.5  # Facteur de redimensionnement
    
    def __post_init__(self):
        """Validation et calculs dérivés"""
        # Validation des paramètres
        if self.n_channels <= 0:
            raise ValueError("n_channels doit être positif")
        if self.buffer_size <= 0:
            raise ValueError("buffer_size doit être positif")
        if self.sample_rate <= 0:
            raise ValueError("sample_rate doit être positive")
        if not 0 < self.overflow_threshold <= 1:
            raise ValueError("overflow_threshold doit être entre 0 et 1")
        if not 0 < self.overflow_threshold_percent <= 100:
            raise ValueError("overflow_threshold_percent doit être entre 0 et 100")
        
        # Synchroniser les seuils
        if hasattr(self, 'overflow_threshold'):
            self.overflow_threshold_percent = self.overflow_threshold * 100
        
        # Validation alignement
        if self.alignment_bytes not in [16, 32, 64, 128]:
            self.alignment_bytes = 64
        
        # Calculs dérivés
        self.buffer_duration = self.buffer_size / self.sample_rate
        self.bytes_per_sample = np.dtype(self.dtype).itemsize
        self.total_bytes = self.n_channels * self.buffer_size * self.bytes_per_sample
        self.overflow_threshold_samples = int(self.buffer_size * self.overflow_threshold_percent / 100)
        
        # Optimisations automatiques
        if self.total_bytes > 100 * 1024 * 1024:  # > 100MB
            self.memory_mapping = True
        
        if self.sample_rate > 1000:  # Haute fréquence
            self.enable_lock_free = True
            self.enable_zero_copy = True
    
    def reset(self) -> None:
        """Remet la configuration aux valeurs par défaut"""
        self.__init__()
    
    def usage_percent(self, current_samples: int) -> float:
        """Calcule le pourcentage d'utilisation du buffer"""
        if self.buffer_size == 0:
            return 0.0
        return min(100.0, (current_samples / self.buffer_size) * 100.0)
    
    def is_overflow_risk(self, current_samples: int) -> bool:
        """Vérifie si le buffer risque un débordement"""
        return current_samples >= self.overflow_threshold_samples
    
    @property
    def total_size(self) -> int:
        """Taille totale du buffer (tous canaux)"""
        return self.n_channels * self.buffer_size
    
    @property
    def duration_seconds(self) -> float:
        """Durée du buffer en secondes."""
        return self.buffer_size / self.sample_rate
    
    @property
    def memory_size_mb(self) -> float:
        """Taille mémoire en MB"""
        return self.total_bytes / (1024 * 1024)
    
    def calculate_usage_percent(self, current_samples: int, buffer_size: int) -> float:
        """Calcule le pourcentage d'utilisation"""
        if buffer_size == 0:
            return 0.0
        return (current_samples / buffer_size) * 100.0
    
    def calculate_overflow_risk(self, current_samples: int, buffer_size: int, write_rate: float) -> float:
        """Calcule le risque de débordement (0-1)"""
        usage = current_samples / buffer_size if buffer_size > 0 else 0
        if usage < self.overflow_threshold:
            return 0.0
        
        # Facteur de risque basé sur l'usage et la vitesse d'écriture
        risk_factor = (usage - self.overflow_threshold) / (1.0 - self.overflow_threshold)
        rate_factor = min(1.0, write_rate / (self.sample_rate * 2))  # Normaliser par rapport à 2x sample_rate
        
        return min(1.0, risk_factor * (1 + rate_factor))
    
    def to_json(self) -> str:
        """Sérialise en JSON"""
        import json
        config_dict = self.to_dict()
        # Convertir les enums en valeurs
        if 'overflow_mode' in config_dict:
            config_dict['overflow_mode'] = config_dict['overflow_mode'].value if hasattr(config_dict['overflow_mode'], 'value') else str(config_dict['overflow_mode'])
        if 'performance_level' in config_dict:
            config_dict['performance_level'] = config_dict['performance_level'].value if hasattr(config_dict['performance_level'], 'value') else str(config_dict['performance_level'])
        # Convertir les types numpy en types Python natifs
        for key, value in config_dict.items():
            if hasattr(value, 'item'):  # numpy scalars
                config_dict[key] = value.item()
        return json.dumps(config_dict, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'UnifiedBufferConfig':
        """Désérialise depuis JSON"""
        import json
        config_dict = json.loads(json_str)
        # Convertir les valeurs en enums
        if 'overflow_mode' in config_dict and isinstance(config_dict['overflow_mode'], str):
            config_dict['overflow_mode'] = OverflowMode(config_dict['overflow_mode'])
        if 'performance_level' in config_dict and isinstance(config_dict['performance_level'], str):
            config_dict['performance_level'] = PerformanceLevel(config_dict['performance_level'])
        return cls.from_dict(config_dict)
    
    def get_optimal_chunk_size(self) -> int:
        """Calcule la taille optimale des chunks pour le traitement"""
        # Basé sur la fréquence d'échantillonnage et la latence cible
        target_latency_s = 0.01  # 10ms
        chunk_size = int(self.sample_rate * target_latency_s)
        
        # Arrondir à la puissance de 2 la plus proche pour FFT
        chunk_size = 2 ** int(np.log2(chunk_size) + 0.5)
        
        # Limiter entre 64 et 2048
        return max(64, min(2048, chunk_size))
    
    def stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de configuration"""
        return {
            'config_version': '3.0.0',
            'n_channels': self.n_channels,
            'buffer_size': self.buffer_size,
            'sample_rate': self.sample_rate,
            'buffer_duration_s': self.buffer_duration,
            'total_memory_mb': self.total_bytes / (1024 * 1024),
            'overflow_threshold': self.overflow_threshold_samples,
            'optimal_chunk_size': self.get_optimal_chunk_size(),
            'memory_mapping': self.memory_mapping,
            'lock_free': self.enable_lock_free,
            'zero_copy': self.enable_zero_copy
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire"""
        from dataclasses import asdict
        config_dict = asdict(self)
        # Convertir les énumérations en chaînes
        if 'overflow_mode' in config_dict:
            config_dict['overflow_mode'] = config_dict['overflow_mode'].value if hasattr(config_dict['overflow_mode'], 'value') else str(config_dict['overflow_mode'])
        if 'performance_level' in config_dict:
            config_dict['performance_level'] = config_dict['performance_level'].value if hasattr(config_dict['performance_level'], 'value') else str(config_dict['performance_level'])
        if 'dtype' in config_dict:
            config_dict['dtype'] = str(config_dict['dtype'])
        # Convertir les types numpy en types Python natifs
        for key, value in config_dict.items():
            if hasattr(value, 'item'):  # numpy scalars
                config_dict[key] = value.item()
            elif isinstance(value, np.dtype):
                config_dict[key] = str(value)
        return config_dict
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'UnifiedBufferConfig':
        """Crée une configuration depuis un dictionnaire"""
        # Copier le dictionnaire pour éviter les modifications
        config_dict = config_dict.copy()
        
        # Convertir le dtype depuis string
        if 'dtype' in config_dict and isinstance(config_dict['dtype'], str):
            try:
                config_dict['dtype'] = np.dtype(config_dict['dtype'])
            except TypeError:
                # Si la conversion échoue, utiliser float64 par défaut
                config_dict['dtype'] = np.float64
        
        # Convertir les enums depuis string si nécessaire
        if 'overflow_mode' in config_dict and isinstance(config_dict['overflow_mode'], str):
            config_dict['overflow_mode'] = OverflowMode(config_dict['overflow_mode'])
        if 'performance_level' in config_dict and isinstance(config_dict['performance_level'], str):
            config_dict['performance_level'] = PerformanceLevel(config_dict['performance_level'])
        
        return cls(**config_dict)
    
    def save_to_file(self, filepath: str) -> None:
        """Sauvegarde la configuration dans un fichier JSON"""
        import json
        
        config_path = Path(filepath)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'UnifiedBufferConfig':
        """Charge la configuration depuis un fichier JSON"""
        import json
        
        config_path = Path(filepath)
        if not config_path.exists():
            raise FileNotFoundError(f"Fichier de configuration non trouvé: {filepath}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        
        return cls.from_dict(config_dict)
    
    @classmethod
    def create_laboratory_preset(cls, preset_name: str) -> 'UnifiedBufferConfig':
        """Crée une configuration prédéfinie pour le laboratoire."""
        presets = {
            'high_frequency': cls(
                n_channels=16,
                buffer_size=16384,
                sample_rate=10000.0,
                dtype=np.float64,
                overflow_mode=OverflowMode.BLOCK,
                performance_level=PerformanceLevel.MAXIMUM,
                enable_lock_free=True,
                enable_simd=True
            ),
            'long_duration': cls(
                n_channels=8,
                buffer_size=65536,
                sample_rate=1000.0,
                dtype=np.float64,
                overflow_mode=OverflowMode.BLOCK,
                performance_level=PerformanceLevel.BALANCED,
                enable_memory_mapping=True,
                auto_resize=True
            ),
            'realtime': cls(
                n_channels=4,
                buffer_size=4096,
                sample_rate=8000.0,
                dtype=np.float32,
                overflow_mode=OverflowMode.OVERWRITE,
                performance_level=PerformanceLevel.MAXIMUM,
                target_latency_ms=5.0,
                enable_zero_copy=True
            ),
            'low_latency': cls(
                n_channels=4,
                buffer_size=4096,
                sample_rate=500.0,
                dtype=np.float32,
                overflow_mode=OverflowMode.OVERWRITE,
                performance_level=PerformanceLevel.MAXIMUM,
                target_latency_ms=1.0
            ),
            'balanced': cls(
                n_channels=6,
                buffer_size=8192,
                sample_rate=250.0,
                dtype=np.float64,
                overflow_mode=OverflowMode.BLOCK,
                performance_level=PerformanceLevel.BALANCED
            )
        }
        
        if preset_name not in presets:
            raise ValueError(f"Preset '{preset_name}' non disponible. Presets disponibles: {list(presets.keys())}")
        
        return presets[preset_name]
    
    @classmethod
    def create_high_frequency_preset(cls) -> 'UnifiedBufferConfig':
        """Crée un preset haute fréquence."""
        return cls.create_laboratory_preset('high_frequency')
    
    @classmethod
    def create_long_duration_preset(cls) -> 'UnifiedBufferConfig':
        """Crée un preset longue durée."""
        return cls.create_laboratory_preset('long_duration')
    
    @classmethod
    def create_realtime_preset(cls) -> 'UnifiedBufferConfig':
        """Crée un preset temps réel."""
        return cls.create_laboratory_preset('realtime')
    
    @classmethod
    def create_low_latency_preset(cls) -> 'UnifiedBufferConfig':
        """Crée un preset faible latence."""
        return cls.create_laboratory_preset('low_latency')
    
    @classmethod
    def create_balanced_preset(cls) -> 'UnifiedBufferConfig':
        """Crée un preset équilibré."""
        return cls.create_laboratory_preset('balanced')


# Alias pour compatibilité avec l'ancien code
BufferConfig = UnifiedBufferConfig
CircularBufferConfig = UnifiedBufferConfig


def get_default_buffer_config() -> UnifiedBufferConfig:
    """Retourne la configuration par défaut pour les buffers"""
    return UnifiedBufferConfig()


def get_laboratory_config(lab_type: str = 'mediterranean_basin') -> UnifiedBufferConfig:
    """Retourne une configuration optimisée pour un type de laboratoire"""
    base_config = get_default_buffer_config()
    return base_config.create_laboratory_preset(lab_type)