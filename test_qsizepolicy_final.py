#!/usr/bin/env python3
"""
Test final pour comprendre QSizePolicy avec cette version de PySide6
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide6.QtCore import Qt

def test_qsizepolicy_methods():
    """Test toutes les méthodes possibles pour QSizePolicy"""
    app = QApplication(sys.argv)
    widget = QWidget()
    
    print(f"PySide6 version: {app.applicationVersion()}")
    print(f"Qt version: {app.applicationVersion()}")
    
    # Test 1: Méthode directe avec deux arguments Policy
    try:
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        print("✓ Test 1 réussi: setSizePolicy(Policy.Expanding, Policy.Preferred)")
    except Exception as e:
        print(f"✗ Test 1 échoué: {e}")
    
    # Test 2: Création d'un objet QSizePolicy avec arguments
    try:
        policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        widget.setSizePolicy(policy)
        print("✓ Test 2 réussi: QSizePolicy(Policy.Expanding, Policy.Preferred)")
    except Exception as e:
        print(f"✗ Test 2 échoué: {e}")
    
    # Test 3: Objet QSizePolicy vide + setters
    try:
        policy = QSizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        policy.setVerticalPolicy(QSizePolicy.Policy.Preferred)
        widget.setSizePolicy(policy)
        print("✓ Test 3 réussi: QSizePolicy() + setHorizontalPolicy + setVerticalPolicy")
    except Exception as e:
        print(f"✗ Test 3 échoué: {e}")
    
    # Test 4: Valeurs entières directes
    try:
        widget.setSizePolicy(7, 5)  # Expanding=7, Preferred=5
        print("✓ Test 4 réussi: setSizePolicy(7, 5)")
    except Exception as e:
        print(f"✗ Test 4 échoué: {e}")
    
    # Test 5: Constantes QSizePolicy directes
    try:
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        print("✓ Test 5 réussi: setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)")
    except Exception as e:
        print(f"✗ Test 5 échoué: {e}")
    
    # Test 6: Méthode alternative avec sizePolicy()
    try:
        current_policy = widget.sizePolicy()
        current_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        current_policy.setVerticalPolicy(QSizePolicy.Policy.Preferred)
        widget.setSizePolicy(current_policy)
        print("✓ Test 6 réussi: sizePolicy() + modification + setSizePolicy")
    except Exception as e:
        print(f"✗ Test 6 échoué: {e}")
    
    app.quit()

if __name__ == "__main__":
    test_qsizepolicy_methods()