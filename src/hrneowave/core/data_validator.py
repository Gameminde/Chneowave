#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de validation de données en temps réel pour CHNeoWave v1.1.0-RC
Pour laboratoires d'études maritimes en modèle réduit
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import deque
import warnings

# Import conditionnel pour l'analyse spectrale
try:
    from scipy import signal, stats
    from scipy.fft import fft, fftfreq
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("SciPy non disponible - analyses avancées désactivées")

class ValidationLevel(Enum):
    """Niveaux de validation"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ValidationRule(Enum):
    """Types de règles de validation"""
    RANGE_CHECK = "range_check"
    RATE_OF_CHANGE = "rate_of_change"
    STATISTICAL_OUTLIER = "statistical_outlier"
    SIGNAL_QUALITY = "signal_quality"
    CROSS_CORRELATION = "cross_correlation"
    SPECTRAL_ANALYSIS = "spectral_analysis"
    DRIFT_DETECTION = "drift_detection"
    NOISE_LEVEL = "noise_level"
    SATURATION_CHECK = "saturation_check"
    CONNECTIVITY_CHECK = "connectivity_check"

@dataclass
class ValidationResult:
    """Résultat d'une validation"""
    rule_type: ValidationRule
    level: ValidationLevel
    message: str
    channel: int
    timestamp: datetime
    value: Optional[float] = None
    expected_range: Optional[Tuple[float, float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"[{self.level.value.upper()}] Ch{self.channel}: {self.message}"

@dataclass
class ValidationConfig:
    """Configuration de validation pour un canal"""
    channel: int
    sensor_type: str = "generic"
    
    # Limites physiques
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    
    # Taux de changement maximum
    max_rate_of_change: Optional[float] = None  # unités/seconde
    
    # Détection d'outliers statistiques
    outlier_threshold: float = 3.0  # nombre d'écarts-types
    outlier_window_size: int = 100  # échantillons
    
    # Qualité du signal
    min_snr: Optional[float] = None  # dB
    max_noise_level: Optional[float] = None
    
    # Détection de saturation
    saturation_threshold: float = 0.95  # pourcentage de la pleine échelle
    saturation_duration: float = 0.1  # secondes
    
    # Détection de dérive
    drift_window_size: int = 1000  # échantillons
    max_drift_rate: Optional[float] = None  # unités/seconde
    
    # Connectivité
    connectivity_timeout: float = 5.0  # secondes
    
    # Analyse spectrale
    spectral_analysis_enabled: bool = False
    expected_frequency_range: Optional[Tuple[float, float]] = None
    
    # Règles actives
    active_rules: List[ValidationRule] = field(default_factory=lambda: [
        ValidationRule.RANGE_CHECK,
        ValidationRule.RATE_OF_CHANGE,
        ValidationRule.STATISTICAL_OUTLIER,
        ValidationRule.SATURATION_CHECK,
        ValidationRule.CONNECTIVITY_CHECK
    ])

class ChannelValidator:
    """Validateur pour un canal spécifique"""
    
    def __init__(self, config: ValidationConfig, sampling_rate: float):
        self.config = config
        self.sampling_rate = sampling_rate
        
        # Historique des données
        self.data_history = deque(maxlen=max(config.outlier_window_size, config.drift_window_size))
        self.timestamp_history = deque(maxlen=max(config.outlier_window_size, config.drift_window_size))
        
        # État de validation
        self.last_value = None
        self.last_timestamp = None
        self.saturation_start = None
        self.baseline_stats = {'mean': 0.0, 'std': 1.0}
        
        # Compteurs
        self.total_samples = 0
        self.error_count = 0
        self.warning_count = 0
    
    def validate_sample(self, value: float, timestamp: datetime) -> List[ValidationResult]:
        """Valide un échantillon"""
        results = []
        
        # Mettre à jour l'historique
        self.data_history.append(value)
        self.timestamp_history.append(timestamp)
        self.total_samples += 1
        
        # Appliquer les règles actives
        for rule in self.config.active_rules:
            try:
                if rule == ValidationRule.RANGE_CHECK:
                    result = self._check_range(value, timestamp)
                elif rule == ValidationRule.RATE_OF_CHANGE:
                    result = self._check_rate_of_change(value, timestamp)
                elif rule == ValidationRule.STATISTICAL_OUTLIER:
                    result = self._check_statistical_outlier(value, timestamp)
                elif rule == ValidationRule.SATURATION_CHECK:
                    result = self._check_saturation(value, timestamp)
                elif rule == ValidationRule.CONNECTIVITY_CHECK:
                    result = self._check_connectivity(timestamp)
                elif rule == ValidationRule.DRIFT_DETECTION:
                    result = self._check_drift(timestamp)
                elif rule == ValidationRule.SPECTRAL_ANALYSIS and SCIPY_AVAILABLE:
                    result = self._check_spectral_quality(timestamp)
                else:
                    continue
                
                if result:
                    results.append(result)
                    if result.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL]:
                        self.error_count += 1
                    elif result.level == ValidationLevel.WARNING:
                        self.warning_count += 1
                        
            except Exception as e:
                # Erreur dans la validation elle-même
                error_result = ValidationResult(
                    rule_type=rule,
                    level=ValidationLevel.ERROR,
                    message=f"Erreur validation: {e}",
                    channel=self.config.channel,
                    timestamp=timestamp,
                    value=value
                )
                results.append(error_result)
        
        # Mettre à jour l'état
        self.last_value = value
        self.last_timestamp = timestamp
        
        # Mettre à jour les statistiques de base
        if len(self.data_history) >= 10:
            self.baseline_stats['mean'] = np.mean(list(self.data_history)[-100:])
            self.baseline_stats['std'] = np.std(list(self.data_history)[-100:])
        
        return results
    
    def _check_range(self, value: float, timestamp: datetime) -> Optional[ValidationResult]:
        """Vérifie si la valeur est dans la plage autorisée"""
        if self.config.min_value is not None and value < self.config.min_value:
            return ValidationResult(
                rule_type=ValidationRule.RANGE_CHECK,
                level=ValidationLevel.ERROR,
                message=f"Valeur sous la limite minimale: {value:.3f} < {self.config.min_value:.3f}",
                channel=self.config.channel,
                timestamp=timestamp,
                value=value,
                expected_range=(self.config.min_value, self.config.max_value)
            )
        
        if self.config.max_value is not None and value > self.config.max_value:
            return ValidationResult(
                rule_type=ValidationRule.RANGE_CHECK,
                level=ValidationLevel.ERROR,
                message=f"Valeur au-dessus de la limite maximale: {value:.3f} > {self.config.max_value:.3f}",
                channel=self.config.channel,
                timestamp=timestamp,
                value=value,
                expected_range=(self.config.min_value, self.config.max_value)
            )
        
        return None
    
    def _check_rate_of_change(self, value: float, timestamp: datetime) -> Optional[ValidationResult]:
        """Vérifie le taux de changement"""
        if (self.config.max_rate_of_change is None or 
            self.last_value is None or 
            self.last_timestamp is None):
            return None
        
        dt = (timestamp - self.last_timestamp).total_seconds()
        if dt <= 0:
            return None
        
        rate = abs(value - self.last_value) / dt
        
        if rate > self.config.max_rate_of_change:
            return ValidationResult(
                rule_type=ValidationRule.RATE_OF_CHANGE,
                level=ValidationLevel.WARNING,
                message=f"Taux de changement élevé: {rate:.3f} > {self.config.max_rate_of_change:.3f} unités/s",
                channel=self.config.channel,
                timestamp=timestamp,
                value=value,
                metadata={'rate': rate, 'max_rate': self.config.max_rate_of_change}
            )
        
        return None
    
    def _check_statistical_outlier(self, value: float, timestamp: datetime) -> Optional[ValidationResult]:
        """Détecte les outliers statistiques"""
        if len(self.data_history) < self.config.outlier_window_size:
            return None
        
        # Utiliser une fenêtre glissante
        window_data = list(self.data_history)[-self.config.outlier_window_size:]
        mean = np.mean(window_data[:-1])  # Exclure la valeur actuelle
        std = np.std(window_data[:-1])
        
        if std == 0:
            return None
        
        z_score = abs(value - mean) / std
        
        if z_score > self.config.outlier_threshold:
            level = ValidationLevel.WARNING if z_score < self.config.outlier_threshold * 1.5 else ValidationLevel.ERROR
            return ValidationResult(
                rule_type=ValidationRule.STATISTICAL_OUTLIER,
                level=level,
                message=f"Outlier statistique détecté: z-score = {z_score:.2f}",
                channel=self.config.channel,
                timestamp=timestamp,
                value=value,
                metadata={'z_score': z_score, 'threshold': self.config.outlier_threshold}
            )
        
        return None
    
    def _check_saturation(self, value: float, timestamp: datetime) -> Optional[ValidationResult]:
        """Détecte la saturation du signal"""
        if self.config.min_value is None or self.config.max_value is None:
            return None
        
        full_scale = self.config.max_value - self.config.min_value
        threshold_high = self.config.max_value - (1 - self.config.saturation_threshold) * full_scale
        threshold_low = self.config.min_value + (1 - self.config.saturation_threshold) * full_scale
        
        is_saturated = value >= threshold_high or value <= threshold_low
        
        if is_saturated:
            if self.saturation_start is None:
                self.saturation_start = timestamp
            else:
                duration = (timestamp - self.saturation_start).total_seconds()
                if duration > self.config.saturation_duration:
                    return ValidationResult(
                        rule_type=ValidationRule.SATURATION_CHECK,
                        level=ValidationLevel.ERROR,
                        message=f"Saturation détectée pendant {duration:.2f}s",
                        channel=self.config.channel,
                        timestamp=timestamp,
                        value=value,
                        metadata={'duration': duration, 'threshold': self.config.saturation_threshold}
                    )
        else:
            self.saturation_start = None
        
        return None
    
    def _check_connectivity(self, timestamp: datetime) -> Optional[ValidationResult]:
        """Vérifie la connectivité (pas de données manquantes)"""
        if self.last_timestamp is None:
            return None
        
        dt = (timestamp - self.last_timestamp).total_seconds()
        expected_dt = 1.0 / self.sampling_rate
        
        if dt > expected_dt * 2 + self.config.connectivity_timeout:
            return ValidationResult(
                rule_type=ValidationRule.CONNECTIVITY_CHECK,
                level=ValidationLevel.ERROR,
                message=f"Perte de connectivité détectée: {dt:.2f}s sans données",
                channel=self.config.channel,
                timestamp=timestamp,
                metadata={'gap_duration': dt, 'expected_interval': expected_dt}
            )
        
        return None
    
    def _check_drift(self, timestamp: datetime) -> Optional[ValidationResult]:
        """Détecte la dérive du signal"""
        if (self.config.max_drift_rate is None or 
            len(self.data_history) < self.config.drift_window_size):
            return None
        
        # Calculer la tendance sur la fenêtre
        window_data = np.array(list(self.data_history)[-self.config.drift_window_size:])
        window_times = np.array([(t - self.timestamp_history[0]).total_seconds() 
                                for t in list(self.timestamp_history)[-self.config.drift_window_size:]])
        
        if len(window_times) < 2:
            return None
        
        # Régression linéaire pour détecter la tendance
        slope, _, r_value, _, _ = stats.linregress(window_times, window_data) if SCIPY_AVAILABLE else (0, 0, 0, 0, 0)
        
        if abs(slope) > self.config.max_drift_rate and abs(r_value) > 0.7:
            return ValidationResult(
                rule_type=ValidationRule.DRIFT_DETECTION,
                level=ValidationLevel.WARNING,
                message=f"Dérive détectée: {slope:.4f} unités/s (R² = {r_value**2:.3f})",
                channel=self.config.channel,
                timestamp=timestamp,
                metadata={'drift_rate': slope, 'correlation': r_value}
            )
        
        return None
    
    def _check_spectral_quality(self, timestamp: datetime) -> Optional[ValidationResult]:
        """Analyse la qualité spectrale du signal"""
        if (not SCIPY_AVAILABLE or 
            not self.config.spectral_analysis_enabled or 
            len(self.data_history) < 256):
            return None
        
        # FFT sur une fenêtre récente
        window_size = min(512, len(self.data_history))
        data = np.array(list(self.data_history)[-window_size:])
        
        # Appliquer une fenêtre pour réduire les fuites spectrales
        windowed_data = data * signal.windows.hann(len(data))
        
        # Calculer la FFT
        fft_data = fft(windowed_data)
        freqs = fftfreq(len(windowed_data), 1/self.sampling_rate)
        
        # Analyser le contenu spectral
        power_spectrum = np.abs(fft_data)**2
        positive_freqs = freqs[:len(freqs)//2]
        positive_power = power_spectrum[:len(power_spectrum)//2]
        
        # Vérifier si l'énergie est dans la plage attendue
        if self.config.expected_frequency_range:
            freq_min, freq_max = self.config.expected_frequency_range
            freq_mask = (positive_freqs >= freq_min) & (positive_freqs <= freq_max)
            
            if np.any(freq_mask):
                energy_in_band = np.sum(positive_power[freq_mask])
                total_energy = np.sum(positive_power)
                
                energy_ratio = energy_in_band / total_energy if total_energy > 0 else 0
                
                if energy_ratio < 0.1:  # Moins de 10% de l'énergie dans la bande attendue
                    return ValidationResult(
                        rule_type=ValidationRule.SPECTRAL_ANALYSIS,
                        level=ValidationLevel.WARNING,
                        message=f"Énergie spectrale faible dans la bande attendue: {energy_ratio:.1%}",
                        channel=self.config.channel,
                        timestamp=timestamp,
                        metadata={
                            'energy_ratio': energy_ratio,
                            'frequency_range': self.config.expected_frequency_range
                        }
                    )
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques de validation"""
        return {
            'total_samples': self.total_samples,
            'error_count': self.error_count,
            'warning_count': self.warning_count,
            'error_rate': self.error_count / max(1, self.total_samples),
            'warning_rate': self.warning_count / max(1, self.total_samples),
            'current_mean': self.baseline_stats['mean'],
            'current_std': self.baseline_stats['std'],
            'data_points': len(self.data_history)
        }

class DataValidator:
    """Validateur de données multi-canaux en temps réel"""
    
    def __init__(self, sampling_rate: float):
        self.sampling_rate = sampling_rate
        self.channel_validators: Dict[int, ChannelValidator] = {}
        self.global_results: List[ValidationResult] = []
        self.result_callbacks: List[Callable[[ValidationResult], None]] = []
        
        # Configuration globale
        self.max_results_history = 1000
        self.auto_cleanup_interval = 100  # échantillons
        self.sample_count = 0
    
    def add_channel(self, config: ValidationConfig):
        """Ajoute un canal à valider"""
        validator = ChannelValidator(config, self.sampling_rate)
        self.channel_validators[config.channel] = validator
        print(f"Canal {config.channel} ajouté à la validation ({config.sensor_type})")
    
    def remove_channel(self, channel: int):
        """Supprime un canal de la validation"""
        if channel in self.channel_validators:
            del self.channel_validators[channel]
            print(f"Canal {channel} supprimé de la validation")
    
    def validate_samples(self, samples: Dict[int, float], timestamp: Optional[datetime] = None) -> List[ValidationResult]:
        """Valide un ensemble d'échantillons multi-canaux"""
        if timestamp is None:
            timestamp = datetime.now()
        
        all_results = []
        
        # Valider chaque canal
        for channel, value in samples.items():
            if channel in self.channel_validators:
                results = self.channel_validators[channel].validate_sample(value, timestamp)
                all_results.extend(results)
        
        # Ajouter à l'historique global
        self.global_results.extend(all_results)
        
        # Nettoyer l'historique si nécessaire
        if len(self.global_results) > self.max_results_history:
            self.global_results = self.global_results[-self.max_results_history:]
        
        # Appeler les callbacks
        for result in all_results:
            for callback in self.result_callbacks:
                try:
                    callback(result)
                except Exception as e:
                    print(f"Erreur callback validation: {e}")
        
        self.sample_count += 1
        
        return all_results
    
    def add_result_callback(self, callback: Callable[[ValidationResult], None]):
        """Ajoute un callback pour les résultats de validation"""
        self.result_callbacks.append(callback)
    
    def get_channel_statistics(self, channel: int) -> Optional[Dict[str, Any]]:
        """Retourne les statistiques pour un canal"""
        if channel in self.channel_validators:
            return self.channel_validators[channel].get_statistics()
        return None
    
    def get_global_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques globales"""
        total_errors = sum(1 for r in self.global_results if r.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL])
        total_warnings = sum(1 for r in self.global_results if r.level == ValidationLevel.WARNING)
        
        channel_stats = {}
        for channel, validator in self.channel_validators.items():
            channel_stats[channel] = validator.get_statistics()
        
        return {
            'total_samples_processed': self.sample_count,
            'total_validation_results': len(self.global_results),
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'active_channels': list(self.channel_validators.keys()),
            'channel_statistics': channel_stats
        }
    
    def get_recent_results(self, level: Optional[ValidationLevel] = None, 
                          channel: Optional[int] = None, 
                          limit: int = 50) -> List[ValidationResult]:
        """Retourne les résultats récents avec filtrage optionnel"""
        filtered_results = self.global_results
        
        if level:
            filtered_results = [r for r in filtered_results if r.level == level]
        
        if channel is not None:
            filtered_results = [r for r in filtered_results if r.channel == channel]
        
        return filtered_results[-limit:]
    
    def clear_history(self):
        """Efface l'historique de validation"""
        self.global_results.clear()
        for validator in self.channel_validators.values():
            validator.data_history.clear()
            validator.timestamp_history.clear()
            validator.total_samples = 0
            validator.error_count = 0
            validator.warning_count = 0
        self.sample_count = 0
        print("Historique de validation effacé")

# Factory functions
def create_data_validator(sampling_rate: float) -> DataValidator:
    """Crée un validateur de données"""
    return DataValidator(sampling_rate)

def create_wave_probe_config(channel: int, measurement_range: Tuple[float, float] = (-300, 300)) -> ValidationConfig:
    """Crée une configuration pour sonde de houle"""
    return ValidationConfig(
        channel=channel,
        sensor_type="wave_probe",
        min_value=measurement_range[0],
        max_value=measurement_range[1],
        max_rate_of_change=1000.0,  # mm/s
        outlier_threshold=3.0,
        saturation_threshold=0.95,
        saturation_duration=0.1,
        max_drift_rate=10.0,  # mm/s
        spectral_analysis_enabled=True,
        expected_frequency_range=(0.1, 5.0)  # Hz pour houle
    )

def create_pressure_sensor_config(channel: int, measurement_range: Tuple[float, float] = (0, 1000)) -> ValidationConfig:
    """Crée une configuration pour capteur de pression"""
    return ValidationConfig(
        channel=channel,
        sensor_type="pressure",
        min_value=measurement_range[0],
        max_value=measurement_range[1],
        max_rate_of_change=500.0,  # Pa/s
        outlier_threshold=2.5,
        saturation_threshold=0.98,
        saturation_duration=0.05,
        max_drift_rate=1.0  # Pa/s
    )