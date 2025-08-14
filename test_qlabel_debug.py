#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de débogage pour identifier les QLabel problématiques
CHNeoWave - Diagnostic CSS
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

def test_qlabel_styles():
    """Test des différents styles QLabel pour identifier le problème"""
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Test QLabel CSS Debug")
    window.setGeometry(100, 100, 600, 400)
    
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    # Test 1: QLabel simple sans style
    label1 = QLabel("Test 1: QLabel sans style")
    layout.addWidget(label1)
    print("✅ QLabel 1 créé sans style")
    
    # Test 2: QLabel avec couleur simple
    label2 = QLabel("Test 2: QLabel avec couleur")
    label2.setStyleSheet("color: #0A1929;")
    layout.addWidget(label2)
    print("✅ QLabel 2 créé avec couleur")
    
    # Test 3: QLabel avec font-weight (potentiellement problématique)
    label3 = QLabel("Test 3: QLabel avec font-weight")
    try:
        label3.setStyleSheet("color: #0A1929; font-weight: bold;")
        layout.addWidget(label3)
        print("✅ QLabel 3 créé avec font-weight")
    except Exception as e:
        print(f"❌ Erreur QLabel 3: {e}")
    
    # Test 4: QLabel avec propriétés complexes
    label4 = QLabel("Test 4: QLabel avec propriétés complexes")
    try:
        label4.setStyleSheet("""
            color: #0A1929;
            font-weight: 500;
            padding: 8px;
            margin: 4px;
        """)
        layout.addWidget(label4)
        print("✅ QLabel 4 créé avec propriétés complexes")
    except Exception as e:
        print(f"❌ Erreur QLabel 4: {e}")
    
    # Test 5: QLabel avec propriétés potentiellement problématiques
    label5 = QLabel("Test 5: QLabel avec propriétés avancées")
    try:
        label5.setStyleSheet("""
            QLabel {
                color: #0A1929;
                font-weight: 500;
                background-color: transparent;
                border: none;
            }
        """)
        layout.addWidget(label5)
        print("✅ QLabel 5 créé avec sélecteur QLabel")
    except Exception as e:
        print(f"❌ Erreur QLabel 5: {e}")
    
    # Test 6: Reproduire le style de CHNeoWave
    label6 = QLabel("Test 6: Style CHNeoWave")
    try:
        label6.setStyleSheet("""
            color: #0A1929;
            font-family: "Inter", "Segoe UI", "Roboto", sans-serif;
            font-size: 13px;
            font-weight: normal;
        """)
        layout.addWidget(label6)
        print("✅ QLabel 6 créé avec style CHNeoWave")
    except Exception as e:
        print(f"❌ Erreur QLabel 6: {e}")
    
    window.setCentralWidget(central_widget)
    window.show()
    window.raise_()
    window.activateWindow()
    
    print("\n🔍 Fenêtre de test affichée")
    print("Si vous voyez cette fenêtre, les QLabel fonctionnent")
    print("Vérifiez la console pour les erreurs CSS")
    
    # Fermer automatiquement après 5 secondes
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(5000)
    
    return app.exec()

if __name__ == "__main__":
    print("🧪 Test de débogage QLabel CSS")
    print("=" * 40)
    
    try:
        exit_code = test_qlabel_styles()
        print(f"\n✅ Test terminé avec code: {exit_code}")
    except Exception as e:
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)