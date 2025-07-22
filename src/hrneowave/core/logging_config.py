#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Logging Configuration v2.0
Configuration centralisée du système de logging

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json

# Configuration par défaut
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
DEFAULT_BACKUP_COUNT = 5

class ColoredFormatter(logging.Formatter):
    """Formateur avec couleurs pour la console"""
    
    # Codes de couleur ANSI
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Vert
        'WARNING': '\033[33m',   # Jaune
        'ERROR': '\033[31m',     # Rouge
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        # Ajouter la couleur selon le niveau
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

class JSONFormatter(logging.Formatter):
    """Formateur JSON pour les logs structurés"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Ajouter les informations d'exception si présentes
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
            
        # Ajouter les attributs personnalisés
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'lineno', 'funcName', 'created',
                          'msecs', 'relativeCreated', 'thread', 'threadName',
                          'processName', 'process', 'getMessage', 'exc_info',
                          'exc_text', 'stack_info']:
                log_entry[key] = value
                
        return json.dumps(log_entry, ensure_ascii=False)

class CHNeoWaveLogger:
    """Gestionnaire de logging pour CHNeoWave"""
    
    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialise le système de logging
        
        Args:
            log_dir: Répertoire des logs (par défaut: ~/.chneowave/logs)
        """
        if log_dir is None:
            self.log_dir = Path.home() / ".chneowave" / "logs"
        else:
            self.log_dir = Path(log_dir)
            
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Fichiers de log
        self.main_log_file = self.log_dir / "chneowave.log"
        self.error_log_file = self.log_dir / "chneowave_errors.log"
        self.debug_log_file = self.log_dir / "chneowave_debug.log"
        self.json_log_file = self.log_dir / "chneowave.json"
        
        # Configuration actuelle
        self._config = {
            'level': DEFAULT_LOG_LEVEL,
            'format': DEFAULT_LOG_FORMAT,
            'date_format': DEFAULT_DATE_FORMAT,
            'max_bytes': DEFAULT_MAX_BYTES,
            'backup_count': DEFAULT_BACKUP_COUNT,
            'console_enabled': True,
            'file_enabled': True,
            'json_enabled': False,
            'colored_console': True
        }
        
        # Logger principal
        self.logger = logging.getLogger('chneowave')
        self._configured = False
        
    def configure(self, **kwargs):
        """Configure le système de logging
        
        Args:
            **kwargs: Options de configuration
        """
        # Mettre à jour la configuration
        self._config.update(kwargs)
        
        # Nettoyer les handlers existants
        self.logger.handlers.clear()
        
        # Définir le niveau de log
        if isinstance(self._config['level'], str):
            level = getattr(logging, self._config['level'].upper())
        else:
            level = self._config['level']
            
        self.logger.setLevel(level)
        
        # Créer les formateurs
        standard_formatter = logging.Formatter(
            self._config['format'],
            self._config['date_format']
        )
        
        colored_formatter = ColoredFormatter(
            self._config['format'],
            self._config['date_format']
        )
        
        json_formatter = JSONFormatter()
        
        # Handler console
        if self._config['console_enabled']:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            
            if self._config['colored_console'] and sys.stdout.isatty():
                console_handler.setFormatter(colored_formatter)
            else:
                console_handler.setFormatter(standard_formatter)
                
            self.logger.addHandler(console_handler)
            
        # Handler fichier principal
        if self._config['file_enabled']:
            file_handler = logging.handlers.RotatingFileHandler(
                self.main_log_file,
                maxBytes=self._config['max_bytes'],
                backupCount=self._config['backup_count'],
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(standard_formatter)
            self.logger.addHandler(file_handler)
            
            # Handler fichier erreurs
            error_handler = logging.handlers.RotatingFileHandler(
                self.error_log_file,
                maxBytes=self._config['max_bytes'],
                backupCount=self._config['backup_count'],
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(standard_formatter)
            self.logger.addHandler(error_handler)
            
            # Handler fichier debug (si niveau DEBUG)
            if level <= logging.DEBUG:
                debug_handler = logging.handlers.RotatingFileHandler(
                    self.debug_log_file,
                    maxBytes=self._config['max_bytes'],
                    backupCount=self._config['backup_count'],
                    encoding='utf-8'
                )
                debug_handler.setLevel(logging.DEBUG)
                debug_handler.setFormatter(standard_formatter)
                self.logger.addHandler(debug_handler)
                
        # Handler JSON
        if self._config['json_enabled']:
            json_handler = logging.handlers.RotatingFileHandler(
                self.json_log_file,
                maxBytes=self._config['max_bytes'],
                backupCount=self._config['backup_count'],
                encoding='utf-8'
            )
            json_handler.setLevel(level)
            json_handler.setFormatter(json_formatter)
            self.logger.addHandler(json_handler)
            
        self._configured = True
        self.logger.info("Système de logging configuré")
        
    def get_logger(self, name: str = None) -> logging.Logger:
        """Retourne un logger
        
        Args:
            name: Nom du logger (par défaut: logger principal)
            
        Returns:
            Instance de logger
        """
        if not self._configured:
            self.configure()
            
        if name is None:
            return self.logger
        else:
            return logging.getLogger(f'chneowave.{name}')
            
    def set_level(self, level):
        """Définit le niveau de log
        
        Args:
            level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
            
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            if not isinstance(handler, logging.handlers.RotatingFileHandler) or \
               handler.baseFilename != str(self.error_log_file):
                handler.setLevel(level)
                
    def enable_debug(self):
        """Active le mode debug"""
        self.set_level(logging.DEBUG)
        self.logger.debug("Mode debug activé")
        
    def disable_console(self):
        """Désactive la sortie console"""
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                self.logger.removeHandler(handler)
                
    def enable_json_logging(self):
        """Active le logging JSON"""
        if not self._config['json_enabled']:
            self._config['json_enabled'] = True
            self.configure(**self._config)
            
    def get_log_files(self) -> Dict[str, Path]:
        """Retourne la liste des fichiers de log
        
        Returns:
            Dictionnaire des fichiers de log
        """
        return {
            'main': self.main_log_file,
            'error': self.error_log_file,
            'debug': self.debug_log_file,
            'json': self.json_log_file
        }
        
    def get_log_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques des logs
        
        Returns:
            Statistiques des fichiers de log
        """
        stats = {}
        
        for name, file_path in self.get_log_files().items():
            if file_path.exists():
                stat = file_path.stat()
                stats[name] = {
                    'size_bytes': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'exists': True
                }
            else:
                stats[name] = {'exists': False}
                
        return stats
        
    def cleanup_old_logs(self, days: int = 30):
        """Nettoie les anciens fichiers de log
        
        Args:
            days: Nombre de jours à conserver
        """
        import time
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        for log_file in self.log_dir.glob('*.log*'):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    self.logger.info(f"Fichier de log supprimé: {log_file}")
                except Exception as e:
                    self.logger.error(f"Erreur lors de la suppression de {log_file}: {e}")
                    
    def archive_logs(self, archive_path: Optional[Path] = None):
        """Archive les fichiers de log
        
        Args:
            archive_path: Chemin de l'archive (par défaut: logs/archives)
        """
        import shutil
        from datetime import datetime
        
        if archive_path is None:
            archive_path = self.log_dir / "archives"
            
        archive_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = archive_path / f"chneowave_logs_{timestamp}"
        
        try:
            shutil.make_archive(str(archive_file), 'zip', str(self.log_dir), '*.log*')
            self.logger.info(f"Logs archivés: {archive_file}.zip")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'archivage des logs: {e}")

# Instance globale du logger
_chneowave_logger = None

def get_logger(name: str = None) -> logging.Logger:
    """Retourne un logger CHNeoWave
    
    Args:
        name: Nom du logger
        
    Returns:
        Instance de logger
    """
    global _chneowave_logger
    if _chneowave_logger is None:
        _chneowave_logger = CHNeoWaveLogger()
        
    return _chneowave_logger.get_logger(name)

def configure_logging(**kwargs):
    """Configure le système de logging
    
    Args:
        **kwargs: Options de configuration
    """
    global _chneowave_logger
    if _chneowave_logger is None:
        _chneowave_logger = CHNeoWaveLogger()
        
    _chneowave_logger.configure(**kwargs)

def setup_basic_logging(level=logging.INFO, enable_debug=False):
    """Configuration de base du logging
    
    Args:
        level: Niveau de log
        enable_debug: Activer le mode debug
    """
    config = {
        'level': logging.DEBUG if enable_debug else level,
        'console_enabled': True,
        'file_enabled': True,
        'colored_console': True
    }
    
    configure_logging(**config)

def setup_production_logging():
    """Configuration pour la production"""
    config = {
        'level': logging.INFO,
        'console_enabled': False,
        'file_enabled': True,
        'json_enabled': True,
        'colored_console': False
    }
    
    configure_logging(**config)

def setup_development_logging():
    """Configuration pour le développement"""
    config = {
        'level': logging.DEBUG,
        'console_enabled': True,
        'file_enabled': True,
        'json_enabled': False,
        'colored_console': True
    }
    
    configure_logging(**config)

def setup_logging(level=logging.INFO, enable_debug=False, enable_file=True, enable_console=True):
    """Configuration générale du logging
    
    Args:
        level: Niveau de log
        enable_debug: Activer le mode debug
        enable_file: Activer l'écriture dans les fichiers
        enable_console: Activer la sortie console
    """
    config = {
        'level': logging.DEBUG if enable_debug else level,
        'console_enabled': enable_console,
        'file_enabled': enable_file,
        'colored_console': True
    }
    
    configure_logging(**config)

# Configuration automatique selon l'environnement
if __name__ == "__main__":
    # Test du système de logging
    setup_development_logging()
    
    logger = get_logger("test")
    logger.debug("Message de debug")
    logger.info("Message d'information")
    logger.warning("Message d'avertissement")
    logger.error("Message d'erreur")
    logger.critical("Message critique")