#!/usr/bin/env python3
"""
Script de test pour comprendre QSizePolicy dans PySide6 6.9.1
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy

def test_qsizepolicy():
    app = QApplication(sys.argv)
    widget = QWidget()
    
    print(f"PySide6 version: {app.applicationVersion()}")
    print(f"QSizePolicy.Policy.Expanding: {QSizePolicy.Policy.Expanding}")
    print(f"QSizePolicy.Policy.Preferred: {QSizePolicy.Policy.Preferred}")
    print(f"Type of QSizePolicy.Policy.Expanding: {type(QSizePolicy.Policy.Expanding)}")
    
    # Test différentes méthodes
    try:
        # Méthode 1: Deux arguments Policy
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        print("✓ Méthode 1 réussie: setSizePolicy(Policy.Expanding, Policy.Preferred)")
    except Exception as e:
        print(f"✗ Méthode 1 échouée: {e}")
    
    try:
        # Méthode 2: Un objet QSizePolicy
        policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        widget.setSizePolicy(policy)
        print("✓ Méthode 2 réussie: setSizePolicy(QSizePolicy(Policy.Expanding, Policy.Preferred))")
    except Exception as e:
        print(f"✗ Méthode 2 échouée: {e}")
    
    try:
        # Méthode 3: Ancienne syntaxe
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        print("✓ Méthode 3 réussie: setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)")
    except Exception as e:
        print(f"✗ Méthode 3 échouée: {e}")
    
    app.quit()

if __name__ == "__main__":
    test_qsizepolicy()