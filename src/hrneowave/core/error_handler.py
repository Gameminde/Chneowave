# -*- coding: utf-8 -*-
"""
Gestionnaire d'erreurs centralisé pour CHNeoWave

Ce module fournit une gestion d'erreurs robuste et cohérente avec:
- Contexte d'erreur enrichi pour le débogage
- Messages utilisateur appropriés en français
- Logging structuré avec ID d'erreur unique
- Sauvegarde des erreurs pour analyse

Auteur: Architecte Logiciel en Chef (ALC)
Date: Janvier 2025
Version: 1.0.0
"""

import json
import logging
import traceback
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from functools import wraps

class ErrorSeverity(Enum):
    """Niveaux de sévérité des erreurs"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    def __lt__(self, other):
        if not isinstance(other, ErrorSeverity):
            return NotImplemented
        order = [ErrorSeverity.LOW, ErrorSeverity.MEDIUM, ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
        return order.index(self) < order.index(other)
    
    def __le__(self, other):
        return self == other or self < other
    
    def __gt__(self, other):
        if not isinstance(other, ErrorSeverity):
            return NotImplemented
        return not self <= other
    
    def __ge__(self, other):
        return self == other or self > other

class ErrorCategory(Enum):
    """Catégories d'erreurs"""
    USER_INPUT = "user_input"
    HARDWARE = "hardware"
    FILE_IO = "file_io"
    NETWORK = "network"
    PROCESSING = "processing"
    GUI = "gui"
    SYSTEM = "system"
    UNKNOWN = "unknown"

@dataclass
class ErrorContext:
    """Contexte d'erreur enrichi"""
    operation: str
    component: str
    category: ErrorCategory = ErrorCategory.UNKNOWN
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    user_data: Optional[Dict[str, Any]] = None
    system_info: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    thread_id: Optional[int] = None
    stack_trace: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.thread_id is None:
            self.thread_id = threading.get_ident()
        if self.stack_trace is None:
            self.stack_trace = traceback.format_stack()[:-1]  # Exclure cette ligne
        if self.user_data is None:
            self.user_data = {}
        if self.system_info is None:
            self.system_info = self._collect_system_info()
    
    def _collect_system_info(self) -> Dict[str, Any]:
        """Collecte des informations système de base"""
        try:
            import psutil
            import platform
            
            return {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'available_memory_mb': psutil.virtual_memory().available / 1024 / 1024
            }
        except ImportError:
            return {
                'platform': 'unknown',
                'python_version': 'unknown'
            }
        except Exception:
            return {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le contexte en dictionnaire"""
        data = asdict(self)
        # Convertir les enums en strings
        data['category'] = self.category.value
        data['severity'] = self.severity.value
        # Convertir datetime en string
        if self.timestamp:
            data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorContext':
        """Crée un ErrorContext depuis un dictionnaire"""
        # Convertir les strings en enums
        if 'category' in data and isinstance(data['category'], str):
            data['category'] = ErrorCategory(data['category'])
        if 'severity' in data and isinstance(data['severity'], str):
            data['severity'] = ErrorSeverity(data['severity'])
        # Convertir timestamp string en datetime
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        
        return cls(**data)

class CHNeoWaveError(Exception):
    """Exception de base pour CHNeoWave avec contexte enrichi"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None, 
                 user_message: Optional[str] = None):
        super().__init__(message)
        self.context = context
        self.user_message = user_message
        self.error_id = self._generate_error_id()
    
    def _generate_error_id(self) -> str:
        """Génère un ID d'erreur unique"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"CHN_{timestamp}_{id(self) % 10000:04d}"
    
    def get_user_message(self) -> str:
        """Retourne le message utilisateur approprié"""
        if self.user_message:
            return f"{self.user_message} (ID: {self.error_id})"
        return f"Une erreur inattendue s'est produite. ID: {self.error_id}"

class ErrorHandler:
    """Gestionnaire d'erreurs centralisé pour CHNeoWave"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_file: Optional[Path] = None, 
                 max_error_history: int = 1000):
        if hasattr(self, '_initialized'):
            return
        
        self.logger = logging.getLogger('CHNeoWave.ErrorHandler')
        self.error_log_file = log_file or Path('logs/errors.jsonl')
        self.max_error_history = max_error_history
        self.error_history: List[Dict[str, Any]] = []
        self._error_callbacks: List[Callable] = []
        
        # Créer le répertoire de logs si nécessaire
        self.error_log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Charger l'historique existant
        self._load_error_history()
        
        self._initialized = True
    
    def add_error_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Ajoute un callback appelé lors d'une erreur"""
        self._error_callbacks.append(callback)
    
    def handle_error(self, exception: Exception, context: Optional[ErrorContext] = None,
                    user_message: Optional[str] = None, 
                    notify_user: bool = True) -> str:
        """Gère une erreur avec contexte enrichi"""
        
        # Créer un contexte par défaut si non fourni
        if context is None:
            context = ErrorContext(
                operation="unknown",
                component="unknown",
                category=self._categorize_exception(exception)
            )
        
        # Générer un ID d'erreur unique
        error_id = self._generate_error_id(exception)
        
        # Préparer les données d'erreur
        error_data = {
            'error_id': error_id,
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'context': context.to_dict(),
            'user_message': user_message,
            'traceback': traceback.format_exc(),
            'notify_user': notify_user
        }
        
        # Logger l'erreur
        self._log_error(error_data)
        
        # Sauvegarder dans l'historique
        self._save_error_to_history(error_data)
        
        # Sauvegarder dans le fichier
        self._save_error_to_file(error_data)
        
        # Notifier les callbacks
        self._notify_callbacks(error_data)
        
        # Retourner le message utilisateur
        return self._format_user_message(error_data)
    
    def _categorize_exception(self, exception: Exception) -> ErrorCategory:
        """Catégorise automatiquement une exception"""
        exception_type = type(exception).__name__
        
        if exception_type in ['ValueError', 'TypeError', 'AttributeError']:
            return ErrorCategory.USER_INPUT
        elif exception_type in ['FileNotFoundError', 'PermissionError', 'IOError']:
            return ErrorCategory.FILE_IO
        elif exception_type in ['ConnectionError', 'TimeoutError', 'URLError']:
            return ErrorCategory.NETWORK
        elif 'Hardware' in exception_type or 'DAQ' in exception_type:
            return ErrorCategory.HARDWARE
        elif 'Qt' in exception_type or 'GUI' in exception_type:
            return ErrorCategory.GUI
        else:
            return ErrorCategory.UNKNOWN
    
    def _generate_error_id(self, exception: Exception) -> str:
        """Génère un ID d'erreur unique"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        return f"ERR_{timestamp}_{id(exception) % 10000:04d}"
    
    def _log_error(self, error_data: Dict[str, Any]):
        """Log l'erreur avec le niveau approprié"""
        severity = error_data['context'].get('severity', 'medium')
        
        log_message = (
            f"[{error_data['error_id']}] {error_data['exception_type']}: "
            f"{error_data['exception_message']} "
            f"(Opération: {error_data['context']['operation']}, "
            f"Composant: {error_data['context']['component']})"
        )
        
        if severity == 'critical':
            self.logger.critical(log_message, extra=error_data)
        elif severity == 'high':
            self.logger.error(log_message, extra=error_data)
        elif severity == 'medium':
            self.logger.warning(log_message, extra=error_data)
        else:
            self.logger.info(log_message, extra=error_data)
    
    def _save_error_to_history(self, error_data: Dict[str, Any]):
        """Sauvegarde l'erreur dans l'historique en mémoire"""
        self.error_history.append(error_data)
        
        # Limiter la taille de l'historique
        if len(self.error_history) > self.max_error_history:
            self.error_history.pop(0)
    
    def _save_error_to_file(self, error_data: Dict[str, Any]):
        """Sauvegarde l'erreur dans le fichier JSON Lines"""
        try:
            with open(self.error_log_file, 'a', encoding='utf-8') as f:
                json.dump(error_data, f, ensure_ascii=False, default=str)
                f.write('\n')
        except Exception as e:
            self.logger.critical(f"Impossible de sauvegarder l'erreur dans le fichier: {e}")
    
    def _load_error_history(self):
        """Charge l'historique des erreurs depuis le fichier"""
        if not self.error_log_file.exists():
            return
        
        try:
            with open(self.error_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-self.max_error_history:]  # Dernières erreurs
                
            for line in lines:
                try:
                    error_data = json.loads(line.strip())
                    self.error_history.append(error_data)
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            self.logger.warning(f"Impossible de charger l'historique des erreurs: {e}")
    
    def _notify_callbacks(self, error_data: Dict[str, Any]):
        """Notifie tous les callbacks enregistrés"""
        for callback in self._error_callbacks:
            try:
                callback(error_data)
            except Exception as e:
                self.logger.error(f"Erreur dans le callback d'erreur: {e}")
    
    def _format_user_message(self, error_data: Dict[str, Any]) -> str:
        """Formate le message utilisateur selon la catégorie d'erreur"""
        category = error_data['context'].get('category', 'unknown')
        error_id = error_data['error_id']
        user_message = error_data.get('user_message')
        
        if user_message:
            return f"{user_message} (Référence: {error_id})"
        
        # Messages par défaut selon la catégorie
        default_messages = {
            'user_input': "Données saisies incorrectes. Vérifiez vos entrées.",
            'file_io': "Problème d'accès aux fichiers. Vérifiez les permissions.",
            'hardware': "Problème de communication avec le matériel d'acquisition.",
            'network': "Problème de connexion réseau.",
            'processing': "Erreur lors du traitement des données.",
            'gui': "Problème d'interface utilisateur.",
            'system': "Erreur système.",
            'unknown': "Une erreur inattendue s'est produite."
        }
        
        base_message = default_messages.get(category, default_messages['unknown'])
        return f"{base_message} (Référence: {error_id})"
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Retourne des statistiques sur les erreurs"""
        if not self.error_history:
            return {}
        
        # Compter par catégorie
        categories = {}
        severities = {}
        components = {}
        
        for error in self.error_history:
            context = error.get('context', {})
            
            category = context.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
            
            severity = context.get('severity', 'unknown')
            severities[severity] = severities.get(severity, 0) + 1
            
            component = context.get('component', 'unknown')
            components[component] = components.get(component, 0) + 1
        
        return {
            'total_errors': len(self.error_history),
            'by_category': categories,
            'by_severity': severities,
            'by_component': components,
            'most_recent': self.error_history[-1] if self.error_history else None
        }
    
    def clear_error_history(self):
        """Efface l'historique des erreurs"""
        self.error_history.clear()
        self.logger.info("Historique des erreurs effacé")
    
    def get_errors_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Retourne les erreurs filtrées par catégorie"""
        return [error for error in self.error_history 
                if error.get('context', {}).get('category') == category]
    
    def get_errors_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Retourne les erreurs filtrées par sévérité"""
        return [error for error in self.error_history 
                if error.get('context', {}).get('severity') == severity]
    
    def get_recent_errors(self, count: int = 10) -> List[Dict[str, Any]]:
        """Retourne les erreurs les plus récentes"""
        return self.error_history[-count:] if count <= len(self.error_history) else self.error_history
    
    def save_errors_to_file(self, file_path):
        """Sauvegarde toutes les erreurs dans un fichier"""
        # Convertir en Path si c'est une chaîne
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for error in self.error_history:
                    json.dump(error, f, ensure_ascii=False, default=str)
                    f.write('\n')
        except Exception as e:
            self.logger.error(f"Impossible de sauvegarder les erreurs: {e}")
    
    def load_errors_from_file(self, file_path):
        """Charge les erreurs depuis un fichier"""
        # Convertir en Path si c'est une chaîne
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        if not file_path.exists():
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        error_data = json.loads(line.strip())
                        self.error_history.append(error_data)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            self.logger.error(f"Impossible de charger les erreurs: {e}")

# Décorateur pour gestion automatique des erreurs
def handle_errors(operation: str, component: str, 
                 category: ErrorCategory = ErrorCategory.UNKNOWN,
                 severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                 user_message: Optional[str] = None):
    """Décorateur pour gestion automatique des erreurs"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = ErrorContext(
                    operation=operation,
                    component=component,
                    category=category,
                    severity=severity
                )
                
                error_handler = get_error_handler()
                error_message = error_handler.handle_error(e, context, user_message)
                
                # Re-lever l'exception avec le message utilisateur
                raise CHNeoWaveError(str(e), context, error_message) from e
        
        return wrapper
    return decorator

# Instance globale du gestionnaire d'erreurs
_global_error_handler = None

def get_error_handler() -> ErrorHandler:
    """Retourne l'instance globale du gestionnaire d'erreurs"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler

# Fonctions utilitaires
def log_error(exception: Exception, operation: str, component: str,
             category: ErrorCategory = ErrorCategory.UNKNOWN,
             user_message: Optional[str] = None) -> str:
    """Fonction utilitaire pour logger une erreur rapidement"""
    context = ErrorContext(
        operation=operation,
        component=component,
        category=category
    )
    
    error_handler = get_error_handler()
    return error_handler.handle_error(exception, context, user_message)

# Export des classes et fonctions principales
__all__ = [
    'ErrorSeverity',
    'ErrorCategory',
    'ErrorContext',
    'CHNeoWaveError',
    'ErrorHandler',
    'handle_errors',
    'get_error_handler',
    'log_error'
]