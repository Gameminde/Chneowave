#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Qt Minimal - Diagnostic Fondamental
Test pour vérifier si Qt fonctionne correctement sur ce système
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt

def test_qt_basique():
    """Test Qt le plus basique possible"""
    print("=== TEST QT BASIQUE ===")
    
    # Créer QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Test Qt Basique")
    print(f"✅ QApplication créée sur: {app.platformName()}")
    print(f"✅ Nombre d'écrans: {len(app.screens())}")
    
    for i, screen in enumerate(app.screens()):
        print(f"   Écran {i}: {screen.geometry()}")
    
    # Créer fenêtre simple
    window = QWidget()
    window.setWindowTitle("Test Qt Basique - CHNeoWave Diagnostic")
    window.setGeometry(300, 300, 500, 400)
    
    # Layout simple
    layout = QVBoxLayout()
    
    # Label de test
    label = QLabel("🎉 SI VOUS VOYEZ CETTE FENÊTRE, QT FONCTIONNE !")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("""
        QLabel {
            font-size: 16px;
            font-weight: bold;
            color: #2E8B57;
            padding: 20px;
            background-color: #F0F8FF;
            border: 2px solid #2E8B57;
            border-radius: 10px;
        }
    """)
    layout.addWidget(label)
    
    # Informations système
    info_label = QLabel(f"""
📋 INFORMATIONS SYSTÈME:

✅ Plateforme: {app.platformName()}
✅ Écrans disponibles: {len(app.screens())}
✅ Géométrie fenêtre: {window.geometry()}

Si cette fenêtre s'affiche correctement,
le problème vient de CHNeoWave, pas de Qt.
    """)
    info_label.setAlignment(Qt.AlignLeft)
    info_label.setStyleSheet("""
        QLabel {
            font-size: 12px;
            padding: 15px;
            background-color: #FFFACD;
            border: 1px solid #DDD;
            border-radius: 5px;
        }
    """)
    layout.addWidget(info_label)
    
    # Bouton de test
    def show_success_message():
        msg = QMessageBox()
        msg.setWindowTitle("Qt Fonctionne !")
        msg.setText("🎉 EXCELLENT !\n\nQt fonctionne parfaitement sur votre système.\n\nLe problème d'affichage de CHNeoWave vient donc\nde l'architecture de l'application, pas de Qt.")
        msg.setIcon(QMessageBox.Information)
        msg.exec()
    
    button = QPushButton("✅ Cliquez ici pour confirmer que Qt fonctionne")
    button.setStyleSheet("""
        QPushButton {
            font-size: 14px;
            font-weight: bold;
            color: white;
            background-color: #2E8B57;
            border: none;
            border-radius: 8px;
            padding: 12px;
        }
        QPushButton:hover {
            background-color: #228B22;
        }
        QPushButton:pressed {
            background-color: #006400;
        }
    """)
    button.clicked.connect(show_success_message)
    layout.addWidget(button)
    
    # Bouton fermer
    close_button = QPushButton("❌ Fermer le test")
    close_button.setStyleSheet("""
        QPushButton {
            font-size: 12px;
            color: #8B0000;
            background-color: #FFE4E1;
            border: 1px solid #8B0000;
            border-radius: 5px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #FFC0CB;
        }
    """)
    close_button.clicked.connect(app.quit)
    layout.addWidget(close_button)
    
    window.setLayout(layout)
    
    # AFFICHAGE
    print("🔍 Affichage de la fenêtre Qt basique...")
    window.show()
    window.raise_()
    window.activateWindow()
    
    print(f"✅ Fenêtre visible: {window.isVisible()}")
    print(f"✅ Géométrie: {window.geometry()}")
    print(f"✅ Position: ({window.x()}, {window.y()})")
    print(f"✅ Taille: {window.width()}x{window.height()}")
    
    print("\n🔍 Si vous voyez la fenêtre, Qt fonctionne parfaitement !")
    print("🔍 Si vous ne voyez rien, le problème vient de l'environnement Qt.")
    
    # Lancer la boucle d'événements
    exit_code = app.exec()
    print(f"\n✅ Application Qt basique terminée avec code: {exit_code}")
    
    return exit_code

if __name__ == "__main__":
    try:
        result = test_qt_basique()
        print(f"\n🏁 Test Qt basique terminé avec code: {result}")
        
        if result == 0:
            print("🎉 QT FONCTIONNE PARFAITEMENT")
            print("➡️  Le problème d'affichage CHNeoWave vient de l'architecture de l'app")
        else:
            print("❌ PROBLÈME AVEC QT DÉTECTÉ")
            print("➡️  Il faut corriger l'environnement Qt avant CHNeoWave")
        
        sys.exit(result)
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)