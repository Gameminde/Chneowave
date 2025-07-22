#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fonctions de validation génériques pour CHNeoWave.

Ce module fournit des validateurs de données qui peuvent être utilisés
à travers l'application, indépendamment de l'interface utilisateur.
"""

import re
from typing import Any, Dict, Optional

def validate_value(value: Any, rules: Dict[str, Any]) -> Optional[str]:
    """Valide une valeur en fonction d'un ensemble de règles.

    Args:
        value: La valeur à valider.
        rules: Un dictionnaire de règles de validation.

    Returns:
        Un message d'erreur si la validation échoue, sinon None.
    """
    # Règle: longueur minimale
    if 'min_length' in rules and isinstance(value, str):
        if len(value) < rules['min_length']:
            return f"Minimum {rules['min_length']} caractères requis"

    # Règle: longueur maximale
    if 'max_length' in rules and isinstance(value, str):
        if len(value) > rules['max_length']:
            return f"Maximum {rules['max_length']} caractères autorisés"

    # Règle: valeur minimale
    if 'min_value' in rules and isinstance(value, (int, float)):
        if value < rules['min_value']:
            return f"Valeur minimale: {rules['min_value']}"

    # Règle: valeur maximale
    if 'max_value' in rules and isinstance(value, (int, float)):
        if value > rules['max_value']:
            return f"Valeur maximale: {rules['max_value']}"

    # Règle: expression régulière
    if 'regex' in rules and isinstance(value, str):
        if not re.match(rules['regex'], value):
            return rules.get('regex_error', "Format invalide")

    # Règle: valeurs autorisées
    if 'allowed_values' in rules:
        if value not in rules['allowed_values']:
            return f"Valeur autorisée: {', '.join(map(str, rules['allowed_values']))}"

    # Règle: validation personnalisée
    if 'custom_validator' in rules:
        validator_func = rules['custom_validator']
        try:
            result = validator_func(value)
            if result is not True:
                return str(result) if result else "Valeur invalide"
        except Exception as e:
            return f"Erreur de validation: {str(e)}"

    return None