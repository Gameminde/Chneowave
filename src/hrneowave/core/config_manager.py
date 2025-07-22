#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Configuration Manager v2.0
Gestionnaire de configuration centralisé

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

import os
import json
import yaml
import toml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class ConfigFormat(Enum):
    """Formats de configuration supportés"""
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"

@dataclass
class AcquisitionConfig:
    """Configuration d'acquisition"""
    sample_rate: float = 1000.0
    buffer_size: int = 8192
    channels: int = 4
    voltage_range: float = 10.0
    coupling: str = "DC"
    trigger_mode: str = "AUTO"
    trigger_level: float = 0.0
    pre_trigger: float = 0.1
    post_trigger: float = 0.9
    
@dataclass
class AnalysisConfig:
    """Configuration d'analyse"""
    fft_size: int = 8192
    window_type: str = "hann"
    overlap: float = 0.5
    frequency_range: tuple = (0.1, 50.0)
    spectral_smoothing: bool = True
    zero_crossing_analysis: bool = True
    wave_height_method: str = "zero_crossing"
    
@dataclass
class CalibrationConfig:
    """Configuration de calibration"""
    auto_calibration: bool = True
    calibration_interval: int = 3600  # secondes
    reference_frequency: float = 1.0
    reference_amplitude: float = 1.0
    sensor_sensitivity: Dict[str, float] = None
    
    def __post_init__(self):
        if self.sensor_sensitivity is None:
            self.sensor_sensitivity = {
                "channel_1": 1.0,
                "channel_2": 1.0,
                "channel_3": 1.0,
                "channel_4": 1.0
            }

@dataclass
class ExportConfig:
    """Configuration d'export"""
    default_format: str = "hdf5"
    compression: bool = True
    compression_level: int = 6
    include_metadata: bool = True
    export_path: str = "./exports"
    filename_template: str = "chneowave_{timestamp}_{session}"
    
@dataclass
class UIConfig:
    """Configuration de l'interface utilisateur"""
    theme: str = "chneowave"
    language: str = "fr"
    auto_save: bool = True
    auto_save_interval: int = 300  # secondes
    plot_update_rate: int = 30  # Hz
    max_plot_points: int = 10000
    show_grid: bool = True
    show_legend: bool = True
    
@dataclass
class SystemConfig:
    """Configuration système"""
    log_level: str = "INFO"
    log_file: str = "chneowave.log"
    max_log_size: int = 10485760  # 10 MB
    backup_count: int = 5
    temp_dir: str = "./temp"
    cache_size: int = 100
    thread_pool_size: int = 4
    
class ConfigManager:
    """Gestionnaire de configuration centralisé"""
    
    def __init__(self, config_dir: Optional[Union[str, Path]] = None):
        """
        Initialise le gestionnaire de configuration
        
        Args:
            config_dir: Répertoire de configuration (par défaut: ~/.chneowave)
        """
        if config_dir is None:
            self.config_dir = Path.home() / ".chneowave"
        else:
            self.config_dir = Path(config_dir)
            
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Fichiers de configuration
        self.main_config_file = self.config_dir / "config.yaml"
        self.user_config_file = self.config_dir / "user_config.yaml"
        self.session_config_file = self.config_dir / "session_config.json"
        
        # Configuration par défaut
        self._default_config = {
            "acquisition": AcquisitionConfig(),
            "analysis": AnalysisConfig(),
            "calibration": CalibrationConfig(),
            "export": ExportConfig(),
            "ui": UIConfig(),
            "system": SystemConfig()
        }
        
        # Configuration actuelle
        self._config = {}
        
        # Charger la configuration
        self.load_config()
        
    def load_config(self):
        """Charge la configuration depuis les fichiers"""
        # Commencer avec la configuration par défaut
        self._config = self._serialize_config(self._default_config)
        
        # Charger la configuration principale
        if self.main_config_file.exists():
            try:
                with open(self.main_config_file, 'r', encoding='utf-8') as f:
                    main_config = yaml.safe_load(f)
                    if main_config:
                        self._merge_config(self._config, main_config)
                        logger.info(f"Configuration principale chargée: {self.main_config_file}")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la configuration principale: {e}")
                
        # Charger la configuration utilisateur
        if self.user_config_file.exists():
            try:
                with open(self.user_config_file, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        self._merge_config(self._config, user_config)
                        logger.info(f"Configuration utilisateur chargée: {self.user_config_file}")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la configuration utilisateur: {e}")
                
        # Charger la configuration de session
        if self.session_config_file.exists():
            try:
                with open(self.session_config_file, 'r', encoding='utf-8') as f:
                    session_config = json.load(f)
                    if session_config:
                        self._merge_config(self._config, session_config)
                        logger.info(f"Configuration de session chargée: {self.session_config_file}")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la configuration de session: {e}")
                
    def save_config(self, config_type: str = "user"):
        """Sauvegarde la configuration
        
        Args:
            config_type: Type de configuration à sauvegarder ("main", "user", "session")
        """
        try:
            if config_type == "main":
                with open(self.main_config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                logger.info(f"Configuration principale sauvegardée: {self.main_config_file}")
                
            elif config_type == "user":
                with open(self.user_config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                logger.info(f"Configuration utilisateur sauvegardée: {self.user_config_file}")
                
            elif config_type == "session":
                with open(self.session_config_file, 'w', encoding='utf-8') as f:
                    json.dump(self._config, f, indent=2, ensure_ascii=False)
                logger.info(f"Configuration de session sauvegardée: {self.session_config_file}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration {config_type}: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration
        
        Args:
            key: Clé de configuration (format: "section.subsection.key")
            default: Valeur par défaut si la clé n'existe pas
            
        Returns:
            Valeur de configuration
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key: str, value: Any):
        """Définit une valeur de configuration
        
        Args:
            key: Clé de configuration (format: "section.subsection.key")
            value: Valeur à définir
        """
        keys = key.split('.')
        config = self._config
        
        # Naviguer jusqu'à la dernière clé
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        # Définir la valeur
        config[keys[-1]] = value
        
    def get_section(self, section: str) -> Dict[str, Any]:
        """Récupère une section complète de configuration
        
        Args:
            section: Nom de la section
            
        Returns:
            Dictionnaire de configuration de la section
        """
        return self._config.get(section, {})
        
    def set_section(self, section: str, config: Dict[str, Any]):
        """Définit une section complète de configuration
        
        Args:
            section: Nom de la section
            config: Dictionnaire de configuration
        """
        self._config[section] = config
        
    def reset_to_defaults(self, section: Optional[str] = None):
        """Remet la configuration aux valeurs par défaut
        
        Args:
            section: Section à remettre par défaut (None pour tout)
        """
        if section is None:
            self._config = self._serialize_config(self._default_config)
            logger.info("Configuration remise aux valeurs par défaut")
        else:
            if section in self._default_config:
                self._config[section] = self._serialize_config({section: self._default_config[section]})[section]
                logger.info(f"Section {section} remise aux valeurs par défaut")
                
    def export_config(self, file_path: Union[str, Path], format: ConfigFormat = ConfigFormat.YAML):
        """Exporte la configuration vers un fichier
        
        Args:
            file_path: Chemin du fichier d'export
            format: Format d'export
        """
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if format == ConfigFormat.JSON:
                    json.dump(self._config, f, indent=2, ensure_ascii=False)
                elif format == ConfigFormat.YAML:
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                elif format == ConfigFormat.TOML:
                    toml.dump(self._config, f)
                    
            logger.info(f"Configuration exportée: {file_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export de la configuration: {e}")
            
    def import_config(self, file_path: Union[str, Path], merge: bool = True):
        """Importe la configuration depuis un fichier
        
        Args:
            file_path: Chemin du fichier d'import
            merge: Si True, fusionne avec la configuration existante
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"Fichier de configuration introuvable: {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() == '.json':
                    imported_config = json.load(f)
                elif file_path.suffix.lower() in ['.yaml', '.yml']:
                    imported_config = yaml.safe_load(f)
                elif file_path.suffix.lower() == '.toml':
                    imported_config = toml.load(f)
                else:
                    logger.error(f"Format de fichier non supporté: {file_path.suffix}")
                    return
                    
            if merge:
                self._merge_config(self._config, imported_config)
            else:
                self._config = imported_config
                
            logger.info(f"Configuration importée: {file_path}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'import de la configuration: {e}")
            
    def validate_config(self) -> bool:
        """Valide la configuration actuelle
        
        Returns:
            True si la configuration est valide
        """
        try:
            # Vérifier les sections obligatoires
            required_sections = ["acquisition", "analysis", "calibration", "export", "ui", "system"]
            for section in required_sections:
                if section not in self._config:
                    logger.error(f"Section manquante: {section}")
                    return False
                    
            # Vérifier les valeurs critiques
            if self.get("acquisition.sample_rate", 0) <= 0:
                logger.error("Fréquence d'échantillonnage invalide")
                return False
                
            if self.get("acquisition.buffer_size", 0) <= 0:
                logger.error("Taille de buffer invalide")
                return False
                
            if self.get("analysis.fft_size", 0) <= 0:
                logger.error("Taille FFT invalide")
                return False
                
            logger.info("Configuration validée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la validation de la configuration: {e}")
            return False
            
    def _serialize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Sérialise la configuration (convertit les dataclasses en dict)"""
        serialized = {}
        for key, value in config.items():
            if hasattr(value, '__dict__'):
                serialized[key] = asdict(value)
            else:
                serialized[key] = value
        return serialized
        
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Fusionne deux configurations"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
                
    def get_config_info(self) -> Dict[str, Any]:
        """Retourne les informations sur la configuration"""
        return {
            "config_dir": str(self.config_dir),
            "main_config_exists": self.main_config_file.exists(),
            "user_config_exists": self.user_config_file.exists(),
            "session_config_exists": self.session_config_file.exists(),
            "sections": list(self._config.keys()),
            "is_valid": self.validate_config()
        }

# Instance globale du gestionnaire de configuration
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Retourne l'instance globale du gestionnaire de configuration"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_config(key: str, default: Any = None) -> Any:
    """Raccourci pour récupérer une valeur de configuration"""
    return get_config_manager().get(key, default)

def set_config(key: str, value: Any):
    """Raccourci pour définir une valeur de configuration"""
    get_config_manager().set(key, value)

def save_config(config_type: str = "user"):
    """Raccourci pour sauvegarder la configuration"""
    get_config_manager().save_config(config_type)