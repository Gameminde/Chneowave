#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow CHNeoWave SANS THÈME
Pour diagnostiquer le problème d'affichage
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class MainWindowMinimal(QMainWindow):
    """MainWindow minimale sans aucun thème ni composant complexe"""
    
    def __init__(self):
        super().__init__()
        print("🔍 Début construction MainWindow minimale")
        
        # Configuration de base
        self.setWindowTitle("CHNeoWave - Test Minimal SANS THÈME")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central simple
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout simple
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("CHNeoWave - Interface de Test")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title)
        
        # Message de statut
        self.status_label = QLabel("✅ MainWindow créée avec succès")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.status_label)
        
        # Bouton de test
        test_button = QPushButton("Cliquez pour tester")
        test_button.setFont(QFont("Arial", 12))
        test_button.clicked.connect(self._on_test_click)
        layout.addWidget(test_button)
        
        # Informations de débogage
        debug_info = QLabel(f"""Informations de débogage:
• Géométrie: {self.geometry()}
• Visible: {self.isVisible()}
• Actif: {self.isActiveWindow()}
• Titre: {self.windowTitle()}""")
        debug_info.setFont(QFont("Courier", 10))
        layout.addWidget(debug_info)
        
        print("✅ MainWindow minimale construite")
        
    def _on_test_click(self):
        """Test d'interaction"""
        self.status_label.setText("🎉 Bouton cliqué ! Interface fonctionne !")
        print("✅ Interaction réussie")

def main():
    """Test principal"""
    print("🚀 Test MainWindow CHNeoWave SANS THÈME")
    print("=" * 50)
    
    try:
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Test Minimal")
        
        print("✅ QApplication créée")
        
        # Créer MainWindow minimale
        window = MainWindowMinimal()
        print("✅ MainWindow minimale créée")
        
        # Afficher la fenêtre
        window.show()
        window.raise_()
        window.activateWindow()
        
        print(f"✅ Fenêtre affichée")
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ Actif: {window.isActiveWindow()}")
        
        # Timer pour fermeture automatique
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(15000)  # 15 secondes
        
        print("🔄 Application lancée (15 secondes)")
        print("👀 VÉRIFIEZ QUE LA FENÊTRE EST VISIBLE !")
        
        # Lancer la boucle d'événements
        exit_code = app.exec()
        print(f"✅ Application terminée (code: {exit_code})")
        return exit_code
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())