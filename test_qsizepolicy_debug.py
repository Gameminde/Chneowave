#!/usr/bin/env python3
"""
Script de debug approfondi pour QSizePolicy
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide6.QtCore import Qt

def debug_qsizepolicy():
    app = QApplication(sys.argv)
    widget = QWidget()
    
    print(f"=== DEBUG QSizePolicy PySide6 ===")
    print(f"QSizePolicy.Policy.Expanding: {QSizePolicy.Policy.Expanding}")
    print(f"QSizePolicy.Policy.Expanding.value: {QSizePolicy.Policy.Expanding.value}")
    print(f"Type: {type(QSizePolicy.Policy.Expanding)}")
    
    # Test avec les valeurs entières directes
    try:
        widget.setSizePolicy(7, 5)  # Expanding=7, Preferred=5
        print("✓ setSizePolicy(7, 5) réussi")
    except Exception as e:
        print(f"✗ setSizePolicy(7, 5) échoué: {e}")
    
    # Test avec les valeurs .value
    try:
        widget.setSizePolicy(QSizePolicy.Policy.Expanding.value, QSizePolicy.Policy.Preferred.value)
        print("✓ setSizePolicy(.value, .value) réussi")
    except Exception as e:
        print(f"✗ setSizePolicy(.value, .value) échoué: {e}")
    
    # Test création d'un QSizePolicy avec valeurs entières
    try:
        policy = QSizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        policy.setVerticalPolicy(QSizePolicy.Policy.Preferred)
        widget.setSizePolicy(policy)
        print("✓ QSizePolicy() + setHorizontalPolicy/setVerticalPolicy réussi")
    except Exception as e:
        print(f"✗ QSizePolicy() + setHorizontalPolicy/setVerticalPolicy échoué: {e}")
    
    app.quit()

if __name__ == "__main__":
    debug_qsizepolicy()