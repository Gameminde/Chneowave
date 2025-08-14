#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Direct Interface CHNeoWave
Test simple pour vérifier l'affichage visuel
"""

import sys
import os
import time

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class TestInterface(QMainWindow):
    """Interface de test simple"""
    
    def __init__(self):
        super().__init__()
        self.chneowave_window = None
        self.setup_ui()
        
        # Lancer CHNeoWave après 2 secondes
        QTimer.singleShot(2000, self.lancer_chneowave)
        
    def setup_ui(self):
        """Configuration de l'interface de test"""
        self.setWindowTitle("🔍 Test Interface CHNeoWave - REGARDEZ L'ÉCRAN")
        self.setGeometry(50, 50, 500, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Titre
        titre = QLabel("🎯 TEST INTERFACE CHNEOWAVE")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont("Arial", 16, QFont.Bold))
        titre.setStyleSheet("""
            QLabel {
                background: #FF6B6B;
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(titre)
        
        # Instructions
        self.instructions = QLabel("⏳ Lancement de CHNeoWave dans 2 secondes...")
        self.instructions.setWordWrap(True)
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setFont(QFont("Arial", 12))
        self.instructions.setStyleSheet("""
            QLabel {
                background: #e3f2fd;
                border: 2px solid #2196F3;
                border-radius: 8px;
                padding: 20px;
                margin: 10px;
                color: #1976D2;
            }
        """)
        layout.addWidget(self.instructions)
        
        # Statut
        self.statut = QLabel("📊 Statut: En attente...")
        self.statut.setAlignment(Qt.AlignCenter)
        self.statut.setFont(QFont("Arial", 11))
        self.statut.setStyleSheet("""
            QLabel {
                background: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
                color: #856404;
            }
        """)
        layout.addWidget(self.statut)
        
        # Bouton relancer
        self.btn_relancer = QPushButton("🔄 Relancer CHNeoWave")
        self.btn_relancer.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_relancer.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                margin: 10px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        self.btn_relancer.clicked.connect(self.relancer_chneowave)
        layout.addWidget(self.btn_relancer)
        
        # Bouton fermer
        self.btn_fermer = QPushButton("❌ Fermer Test")
        self.btn_fermer.setFont(QFont("Arial", 11))
        self.btn_fermer.setStyleSheet("""
            QPushButton {
                background: #f44336;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                margin: 10px;
            }
            QPushButton:hover {
                background: #d32f2f;
            }
        """)
        self.btn_fermer.clicked.connect(self.fermer_test)
        layout.addWidget(self.btn_fermer)
        
    def lancer_chneowave(self):
        """Lancer CHNeoWave"""
        try:
            self.instructions.setText("🚀 Lancement de CHNeoWave en cours...")
            self.statut.setText("📊 Statut: Import des modules...")
            
            # Import CHNeoWave
            from hrneowave.gui.main_window import MainWindow
            
            self.statut.setText("📊 Statut: Création de la fenêtre...")
            
            # Créer la fenêtre
            self.chneowave_window = MainWindow()
            
            self.statut.setText("📊 Statut: Affichage de la fenêtre...")
            
            # Afficher la fenêtre
            self.chneowave_window.show()
            self.chneowave_window.raise_()
            self.chneowave_window.activateWindow()
            
            # Positionner les fenêtres
            self.move(50, 50)
            self.chneowave_window.move(600, 50)
            
            # Vérifier l'affichage
            if self.chneowave_window.isVisible():
                self.instructions.setText("""
✅ CHNeoWave lancé avec succès!

🔍 VÉRIFIEZ:
• Une fenêtre CHNeoWave doit être visible à droite
• Si vous la voyez, l'interface fonctionne!
• Si non, cliquez sur "Relancer CHNeoWave"
                """)
                self.statut.setText("📊 Statut: ✅ Interface affichée")
                self.statut.setStyleSheet("""
                    QLabel {
                        background: #d4edda;
                        border: 2px solid #28a745;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 10px;
                        color: #155724;
                    }
                """)
            else:
                self.instructions.setText("⚠️ CHNeoWave créé mais non visible")
                self.statut.setText("📊 Statut: ⚠️ Problème d'affichage")
                
        except Exception as e:
            self.instructions.setText(f"❌ Erreur lors du lancement:\n{str(e)}")
            self.statut.setText("📊 Statut: ❌ Échec du lancement")
            self.statut.setStyleSheet("""
                QLabel {
                    background: #f8d7da;
                    border: 2px solid #dc3545;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px;
                    color: #721c24;
                }
            """)
            print(f"Erreur détaillée: {e}")
            import traceback
            traceback.print_exc()
    
    def relancer_chneowave(self):
        """Relancer CHNeoWave"""
        if self.chneowave_window:
            self.chneowave_window.close()
            self.chneowave_window = None
        
        self.instructions.setText("⏳ Relancement dans 1 seconde...")
        self.statut.setText("📊 Statut: Préparation...")
        QTimer.singleShot(1000, self.lancer_chneowave)
    
    def fermer_test(self):
        """Fermer le test"""
        if self.chneowave_window:
            self.chneowave_window.close()
        self.close()

def main():
    """Fonction principale"""
    print("🔍 === TEST INTERFACE DIRECTE CHNEOWAVE ===")
    print("🎯 Objectif: Vérifier si l'interface s'affiche visuellement")
    print("👀 REGARDEZ VOTRE ÉCRAN pour voir si une fenêtre CHNeoWave apparaît")
    print("")
    
    app = QApplication(sys.argv)
    
    # Créer la fenêtre de test
    test_window = TestInterface()
    test_window.show()
    
    print("✅ Fenêtre de test affichée")
    print("⏳ CHNeoWave va se lancer automatiquement")
    print("🔍 Surveillez l'apparition d'une nouvelle fenêtre")
    print("")
    
    # Lancer l'application
    return app.exec()

if __name__ == "__main__":
    exit_code = main()
    print(f"🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)