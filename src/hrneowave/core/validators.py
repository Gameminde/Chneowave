# -*- coding: utf-8 -*-
"""
Module de validation centralisé pour CHNeoWave

Ce module fournit des validateurs robustes pour toutes les entrées utilisateur,
avec des messages d'erreur clairs en français et une gestion cohérente des niveaux de validation.

Auteur: Architecte Logiciel en Chef (ALC)
Date: Janvier 2025
Version: 1.0.0
"""

import re
import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    """Niveaux de validation"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    """Résultat d'une validation"""
    is_valid: bool
    level: ValidationLevel
    message: str
    field: Optional[str] = None
    suggestions: Optional[List[str]] = None
    
    def __str__(self) -> str:
        return f"[{self.level.value.upper()}] {self.message}"

class BaseValidator:
    """Classe de base pour tous les validateurs"""
    
    @staticmethod
    def _clean_string(value: str) -> str:
        """Nettoie une chaîne de caractères"""
        if not isinstance(value, str):
            return ""
        return value.strip()
    
    @staticmethod
    def _is_empty(value: Any) -> bool:
        """Vérifie si une valeur est vide"""
        if value is None:
            return True
        if isinstance(value, str):
            return len(value.strip()) == 0
        if isinstance(value, (list, dict, tuple)):
            return len(value) == 0
        return False

class ProjectValidator(BaseValidator):
    """Validateur pour les données de projet"""
    
    # Caractères interdits dans les noms de fichiers Windows
    FORBIDDEN_CHARS = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
    
    # Noms réservés Windows
    RESERVED_NAMES = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    ]
    
    @classmethod
    def validate_project_name(cls, name: str) -> ValidationResult:
        """Valide le nom d'un projet"""
        name = cls._clean_string(name)
        
        # Vérification vide
        if cls._is_empty(name):
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "Le nom du projet est obligatoire",
                "project_name",
                ["Saisissez un nom descriptif pour votre projet"]
            )
        
        # Longueur minimale
        if len(name) < 3:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "Le nom du projet doit contenir au moins 3 caractères",
                "project_name",
                ["Exemple: 'Étude Vagues Port Marseille'"]
            )
        
        # Longueur maximale
        if len(name) > 100:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Le nom du projet ne peut pas dépasser 100 caractères (actuellement: {len(name)})",
                "project_name",
                ["Raccourcissez le nom en gardant l'essentiel"]
            )
        
        # Caractères interdits
        forbidden_found = [char for char in cls.FORBIDDEN_CHARS if char in name]
        if forbidden_found:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Le nom du projet contient des caractères interdits: {', '.join(forbidden_found)}",
                "project_name",
                ["Remplacez les caractères interdits par des espaces ou des tirets"]
            )
        
        # Noms réservés Windows
        if name.upper() in cls.RESERVED_NAMES:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"'{name}' est un nom réservé par le système",
                "project_name",
                ["Choisissez un autre nom pour votre projet"]
            )
        
        # Espaces en début/fin
        if name != name.strip():
            return ValidationResult(
                False, ValidationLevel.WARNING,
                "Le nom du projet ne doit pas commencer ou finir par des espaces",
                "project_name",
                ["Les espaces en début et fin seront supprimés automatiquement"]
            )
        
        # Validation réussie
        return ValidationResult(
            True, ValidationLevel.INFO,
            "Nom de projet valide",
            "project_name"
        )
    
    @classmethod
    def validate_chief_name(cls, chief: str) -> ValidationResult:
        """Valide le nom du chef de projet"""
        chief = cls._clean_string(chief)
        
        if cls._is_empty(chief):
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "Le nom du chef de projet est obligatoire",
                "chief_name",
                ["Saisissez le nom du responsable du projet"]
            )
        
        if len(chief) < 2:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "Le nom du chef de projet doit contenir au moins 2 caractères",
                "chief_name"
            )
        
        if len(chief) > 100:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Le nom du chef de projet ne peut pas dépasser 100 caractères (actuellement: {len(chief)})",
                "chief_name"
            )
        
        # Vérification format nom (lettres, espaces, tirets, apostrophes)
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", chief):
            return ValidationResult(
                False, ValidationLevel.WARNING,
                "Le nom du chef de projet contient des caractères inhabituels",
                "chief_name",
                ["Utilisez uniquement des lettres, espaces, tirets et apostrophes"]
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            "Nom du chef de projet valide",
            "chief_name"
        )
    
    @classmethod
    def validate_manager_name(cls, manager: str) -> ValidationResult:
        """Alias pour validate_chief_name pour compatibilité avec l'interface"""
        return cls.validate_chief_name(manager)
    
    @classmethod
    def validate_laboratory(cls, laboratory: str) -> ValidationResult:
        """Valide le nom du laboratoire"""
        laboratory = cls._clean_string(laboratory)
        
        if cls._is_empty(laboratory):
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "Le nom du laboratoire est obligatoire",
                "laboratory",
                ["Exemple: 'LHSV - Laboratoire d'Hydraulique Saint-Venant'"]
            )
        
        if len(laboratory) < 2:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "Le nom du laboratoire doit contenir au moins 2 caractères",
                "laboratory"
            )
        
        if len(laboratory) > 200:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Le nom du laboratoire ne peut pas dépasser 200 caractères (actuellement: {len(laboratory)})",
                "laboratory"
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            "Nom du laboratoire valide",
            "laboratory"
        )
    
    @classmethod
    def validate_description(cls, description: str) -> ValidationResult:
        """Valide la description du projet"""
        description = cls._clean_string(description)
        
        # Description optionnelle
        if cls._is_empty(description):
            return ValidationResult(
                True, ValidationLevel.WARNING,
                "Aucune description fournie",
                "description",
                ["Une description aide à identifier le projet"]
            )
        
        if len(description) > 1000:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"La description ne peut pas dépasser 1000 caractères (actuellement: {len(description)})",
                "description"
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            "Description valide",
            "description"
        )
    
    @classmethod
    def validate_all(cls, project_data: Dict[str, Any]) -> ValidationResult:
        """Valide toutes les données d'un projet"""
        errors = []
        warnings = []
        
        # Validation de chaque champ
        validations = [
            cls.validate_project_name(project_data.get('name', '')),
            cls.validate_chief_name(project_data.get('chief', '')),
            cls.validate_laboratory(project_data.get('laboratory', '')),
            cls.validate_description(project_data.get('description', ''))
        ]
        
        for result in validations:
            if not result.is_valid:
                if result.level == ValidationLevel.ERROR:
                    errors.append(result.message)
                elif result.level == ValidationLevel.WARNING:
                    warnings.append(result.message)
        
        # Résultat global
        if errors:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Erreurs de validation: {'; '.join(errors)}",
                "project_data"
            )
        
        if warnings:
            return ValidationResult(
                True, ValidationLevel.WARNING,
                f"Avertissements: {'; '.join(warnings)}",
                "project_data"
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            "Toutes les validations sont réussies",
            "project_data"
        )
    
    @classmethod
    def validate_project_data(cls, project_data: Dict[str, Any]) -> ValidationResult:
        """Valide toutes les données d'un projet (interface compatible avec welcome_view)"""
        errors = []
        warnings = []
        
        # Validation de chaque champ avec les noms utilisés dans l'interface
        validations = [
            cls.validate_project_name(project_data.get('name', '')),
            cls.validate_manager_name(project_data.get('manager', '')),
            cls.validate_laboratory(project_data.get('laboratory', '')),
            cls.validate_description(project_data.get('description', ''))
        ]
        
        for result in validations:
            if not result.is_valid:
                if result.level == ValidationLevel.ERROR:
                    errors.append(result.message)
                elif result.level == ValidationLevel.WARNING:
                    warnings.append(result.message)
        
        # Résultat global
        if errors:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Erreurs de validation: {'; '.join(errors)}",
                "project_data"
            )
        
        if warnings:
            return ValidationResult(
                True, ValidationLevel.WARNING,
                f"Avertissements: {'; '.join(warnings)}",
                "project_data"
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            "Toutes les données du projet sont valides",
            "project_data"
        )

class AcquisitionValidator(BaseValidator):
    """Validateur pour les paramètres d'acquisition"""
    
    @classmethod
    def validate_sampling_rate(cls, rate: Union[int, float, str]) -> ValidationResult:
        """Valide la fréquence d'échantillonnage"""
        try:
            rate_float = float(rate)
        except (ValueError, TypeError):
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "La fréquence d'échantillonnage doit être un nombre",
                "sampling_rate",
                ["Exemple: 1000 pour 1000 Hz"]
            )
        
        if rate_float <= 0:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "La fréquence d'échantillonnage doit être positive",
                "sampling_rate"
            )
        
        if rate_float < 10:
            return ValidationResult(
                False, ValidationLevel.WARNING,
                f"Fréquence très faible: {rate_float} Hz",
                "sampling_rate",
                ["Vérifiez que cette fréquence est appropriée pour votre étude"]
            )
        
        if rate_float > 50000:
            return ValidationResult(
                False, ValidationLevel.WARNING,
                f"Fréquence très élevée: {rate_float} Hz",
                "sampling_rate",
                ["Une fréquence élevée peut impacter les performances"]
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            f"Fréquence d'échantillonnage valide: {rate_float} Hz",
            "sampling_rate"
        )
    
    @classmethod
    def validate_duration(cls, duration: Union[int, float, str]) -> ValidationResult:
        """Valide la durée d'acquisition"""
        try:
            duration_float = float(duration)
        except (ValueError, TypeError):
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "La durée d'acquisition doit être un nombre",
                "duration",
                ["Exemple: 60 pour 60 secondes"]
            )
        
        if duration_float <= 0:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "La durée d'acquisition doit être positive",
                "duration"
            )
        
        if duration_float < 1:
            return ValidationResult(
                False, ValidationLevel.WARNING,
                f"Durée très courte: {duration_float} secondes",
                "duration",
                ["Une durée courte peut limiter la qualité de l'analyse"]
            )
        
        if duration_float > 3600:  # 1 heure
            return ValidationResult(
                False, ValidationLevel.WARNING,
                f"Durée très longue: {duration_float} secondes",
                "duration",
                ["Une longue durée peut générer des fichiers volumineux"]
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            f"Durée d'acquisition valide: {duration_float} secondes",
            "duration"
        )

class FileValidator(BaseValidator):
    """Validateur pour les chemins et noms de fichiers"""
    
    @classmethod
    def validate_file_path(cls, path: Union[str, Path]) -> ValidationResult:
        """Valide un chemin de fichier"""
        if cls._is_empty(path):
            return ValidationResult(
                False, ValidationLevel.ERROR,
                "Le chemin de fichier est obligatoire",
                "file_path"
            )
        
        try:
            path_obj = Path(path)
        except Exception as e:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Chemin de fichier invalide: {e}",
                "file_path"
            )
        
        # Vérifier que le répertoire parent existe
        if not path_obj.parent.exists():
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Le répertoire parent n'existe pas: {path_obj.parent}",
                "file_path",
                ["Créez le répertoire ou choisissez un autre emplacement"]
            )
        
        # Vérifier les permissions d'écriture
        try:
            if path_obj.exists():
                # Fichier existant - vérifier les permissions
                if not path_obj.is_file():
                    return ValidationResult(
                        False, ValidationLevel.ERROR,
                        f"Le chemin pointe vers un répertoire, pas un fichier: {path_obj}",
                        "file_path"
                    )
            else:
                # Nouveau fichier - vérifier les permissions du répertoire
                test_file = path_obj.parent / "test_write_permission.tmp"
                test_file.touch()
                test_file.unlink()
        except PermissionError:
            return ValidationResult(
                False, ValidationLevel.ERROR,
                f"Permissions insuffisantes pour écrire dans: {path_obj.parent}",
                "file_path",
                ["Choisissez un répertoire avec des permissions d'écriture"]
            )
        except Exception as e:
            return ValidationResult(
                False, ValidationLevel.WARNING,
                f"Impossible de vérifier les permissions: {e}",
                "file_path"
            )
        
        return ValidationResult(
            True, ValidationLevel.INFO,
            f"Chemin de fichier valide: {path_obj}",
            "file_path"
        )

# Fonction utilitaire pour validation rapide
def validate_project_quick(name: str, chief: str, laboratory: str) -> bool:
    """Validation rapide des données essentielles d'un projet"""
    validators = [
        ProjectValidator.validate_project_name(name),
        ProjectValidator.validate_chief_name(chief),
        ProjectValidator.validate_laboratory(laboratory)
    ]
    
    return all(result.is_valid for result in validators)

# Export des classes principales
__all__ = [
    'ValidationLevel',
    'ValidationResult', 
    'ProjectValidator',
    'AcquisitionValidator',
    'FileValidator',
    'validate_project_quick'
]