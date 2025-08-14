#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Validation Visuelle CHNeoWave - Version Simplifiée
Fenêtre persistante pour validation manuelle
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QWidget, QTextEdit, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class TestValidationCHNeoWave(QMainWindow):
    """Test de validation visuelle simple"""
    
    def __init__(self):
        super().__init__()
        self.clics_validation = 0
        self.chneowave_window = None
        self.setup_ui()
        
        # Timer pour initialiser CHNeoWave après l'affichage
        QTimer.singleShot(1000, self.initialiser_chneowave)
        
    def setup_ui(self):
        """Configuration de l'interface de validation"""
        self.setWindowTitle("🔍 Test Validation CHNeoWave - Cliquez 5 fois pour valider")
        self.setGeometry(100, 100, 600, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Titre
        titre = QLabel("🎯 VALIDATION VISUELLE CHNEOWAVE")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont("Arial", 16, QFont.Bold))
        titre.setStyleSheet("""
            QLabel {
                background: #4CAF50;
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(titre)
        
        # Instructions
        self.instructions = QLabel()
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
        
        # Bouton de validation principal
        self.btn_valider = QPushButton("✅ JE VOIS L'INTERFACE CHNEOWAVE!")
        self.btn_valider.setFont(QFont("Arial", 14, QFont.Bold))
        self.btn_valider.setMinimumHeight(80)
        self.btn_valider.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 20px;
                border-radius: 12px;
                margin: 15px;
            }
            QPushButton:hover {
                background: #45a049;
            }
            QPushButton:pressed {
                background: #3d8b40;
            }
        """)
        self.btn_valider.clicked.connect(self.valider_affichage)
        layout.addWidget(self.btn_valider)
        
        # Compteur
        self.compteur = QLabel("Validations: 0/5")
        self.compteur.setAlignment(Qt.AlignCenter)
        self.compteur.setFont(QFont("Arial", 14, QFont.Bold))
        self.compteur.setStyleSheet("""
            QLabel {
                background: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
                color: #856404;
            }
        """)
        layout.addWidget(self.compteur)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        self.btn_relancer = QPushButton("🔄 Relancer CHNeoWave")
        self.btn_relancer.clicked.connect(self.relancer_chneowave)
        btn_layout.addWidget(self.btn_relancer)
        
        self.btn_fermer = QPushButton("❌ Fermer Test")
        self.btn_fermer.clicked.connect(self.fermer_test)
        btn_layout.addWidget(self.btn_fermer)
        
        # Style pour boutons d'action
        for btn in [self.btn_relancer, self.btn_fermer]:
            btn.setFont(QFont("Arial", 11))
            btn.setStyleSheet("""
                QPushButton {
                    background: #2196F3;
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 6px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background: #1976D2;
                }
            """)
        
        layout.addLayout(btn_layout)
        
        # Log des actions
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(250)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background: #1e1e1e;
                color: #00ff41;
                border: 2px solid #333;
                border-radius: 5px;
                font-family: 'Consolas', 'Courier New';
                font-size: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.log_text)
        
        self.mettre_a_jour_instructions()
        
    def initialiser_chneowave(self):
        """Initialiser CHNeoWave"""
        try:
            self.log("🚀 Initialisation de CHNeoWave...")
            
            # Importer et créer CHNeoWave
            from hrneowave.gui.main_window import MainWindow
            self.chneowave_window = MainWindow()
            
            self.log("✅ CHNeoWave MainWindow créée")
            
            # Afficher CHNeoWave
            self.chneowave_window.show()
            self.chneowave_window.raise_()
            self.chneowave_window.activateWindow()
            
            self.log("✅ CHNeoWave affichée")
            self.log(f"📊 Visible: {self.chneowave_window.isVisible()}")
            self.log(f"📊 Géométrie: {self.chneowave_window.geometry()}")
            self.log(f"📊 Titre: {self.chneowave_window.windowTitle()}")
            
            # Positionner les fenêtres côte à côte
            self.move(50, 50)
            if self.chneowave_window:
                self.chneowave_window.move(700, 50)
            
        except Exception as e:
            self.log(f"❌ Erreur CHNeoWave: {e}")
            import traceback
            self.log(f"📋 Traceback: {traceback.format_exc()}")
    
    def log(self, message):
        """Ajouter un message au log"""
        self.log_text.append(f"[{self.clics_validation:02d}] {message}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def mettre_a_jour_instructions(self):
        """Mettre à jour les instructions"""
        if self.clics_validation < 5:
            instructions = f"""
🎯 OBJECTIF: Valider que CHNeoWave s'affiche visuellement

📋 INSTRUCTIONS:
1. Une fenêtre CHNeoWave doit s'ouvrir automatiquement
2. Si vous voyez l'interface CHNeoWave, cliquez sur le bouton vert
3. Répétez 5 fois pour valider complètement
4. Si aucune fenêtre n'apparaît, cliquez sur "Relancer CHNeoWave"

📊 Progression: {self.clics_validation}/5 validations
            """
        else:
            instructions = """
🎉 VALIDATION TERMINÉE AVEC SUCCÈS!

✅ CHNeoWave s'affiche correctement
✅ Interface utilisateur fonctionnelle  
✅ Test de validation visuelle réussi

Vous pouvez maintenant fermer cette fenêtre.
            """
        
        self.instructions.setText(instructions)
        self.compteur.setText(f"Validations: {self.clics_validation}/5")
    
    def valider_affichage(self):
        """Valider l'affichage de CHNeoWave"""
        self.clics_validation += 1
        
        self.log(f"✅ VALIDATION #{self.clics_validation} - Interface visible confirmée")
        
        if self.clics_validation >= 5:
            self.log("🎉 TEST VALIDÉ AVEC SUCCÈS!")
            self.log("✅ CHNeoWave s'affiche correctement")
            self.log("✅ Interface utilisateur fonctionnelle")
            self.log("✅ Validation visuelle complète")
            
            self.btn_valider.setText("🎉 TEST RÉUSSI!")
            self.btn_valider.setEnabled(False)
            
            # Changer la couleur en succès
            self.btn_valider.setStyleSheet("""
                QPushButton {
                    background: #2E7D32;
                    color: white;
                    border: 3px solid #1B5E20;
                    padding: 20px;
                    border-radius: 12px;
                    margin: 15px;
                }
            """)
        
        self.mettre_a_jour_instructions()
    
    def relancer_chneowave(self):
        """Relancer CHNeoWave"""
        self.log("🔄 Relancement de CHNeoWave...")
        if self.chneowave_window:
            self.chneowave_window.close()
        QTimer.singleShot(500, self.initialiser_chneowave)
    
    def fermer_test(self):
        """Fermer le test"""
        self.log("🔚 Fermeture du test de validation")
        if self.chneowave_window:
            self.chneowave_window.close()
        self.close()

def main():
    """Fonction principale"""
    print("🔍 === TEST VALIDATION VISUELLE CHNEOWAVE ===")
    
    app = QApplication(sys.argv)
    
    # Créer la fenêtre de validation
    validation_window = TestValidationCHNeoWave()
    validation_window.show()
    
    print("✅ Fenêtre de validation affichée")
    print("👆 Cliquez 5 fois sur le bouton vert pour valider")
    print("🔍 Vérifiez qu'une fenêtre CHNeoWave s'ouvre")
    
    # Lancer l'application
    return app.exec()

if __name__ == "__main__":
    exit_code = main()
    print(f"🏁 Test de validation terminé avec code: {exit_code}")
    sys.exit(exit_code)