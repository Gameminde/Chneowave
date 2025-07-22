#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de diagnostic pour le bouton Valider - Navigation
Reproduction du bug décrit par l'utilisateur
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from PySide6.QtCore import QTimer, Qt
    from PySide6.QtTest import QTest
except ImportError:
    print("❌ PySide6 non disponible")
    sys.exit(1)

try:
    from hrneowave.gui.views.welcome_view import WelcomeView
    from hrneowave.gui.controllers.main_controller import MainController
    from hrneowave.gui.view_manager import ViewManager
except ImportError as e:
    print(f"❌ Import CHNeoWave échoué: {e}")
    sys.exit(1)

class TestWindow(QMainWindow):
    """Fenêtre de test pour reproduire le problème"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Bouton Valider - CHNeoWave")
        self.setMinimumSize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Créer la vue Welcome
        self.welcome_view = WelcomeView()
        layout.addWidget(self.welcome_view)
        
        # Connecter le signal pour observer
        self.welcome_view.projectSelected.connect(self.on_project_selected)
        
        print("✅ TestWindow initialisée")
        print("📝 Instructions:")
        print("   1. Remplissez les champs obligatoires")
        print("   2. Cliquez sur 'Valider et Continuer'")
        print("   3. Observez les messages de debug")
        
    def on_project_selected(self, project_path):
        """Gestionnaire pour le signal projectSelected"""
        print(f"🎯 [DEBUG] Signal projectSelected reçu: '{project_path}'")
        print(f"📊 [DEBUG] Métadonnées du projet: {self.welcome_view.get_project_metadata()}")
        
        # Simuler ce que fait MainController
        if not project_path:  # Nouveau projet
            print("🆕 [DEBUG] Nouveau projet détecté")
            print("🔄 [DEBUG] Navigation vers vue 'acquisition' devrait se faire ici")
            
            # Dans un vrai scénario, on appellerait:
            # self.view_manager.switch_to_view("acquisition")
            print("✅ [DEBUG] Test réussi - Signal émis correctement")
        else:
            print(f"📂 [DEBUG] Projet existant: {project_path}")

def test_bouton_valider():
    """Test principal du bouton Valider"""
    print("🚀 VALIDER – DIAGNOSTIC")
    print("=" * 50)
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Créer la fenêtre de test
    window = TestWindow()
    window.show()
    
    print("\n📋 Étapes de test:")
    print("1️⃣ Remplir automatiquement les champs...")
    
    # Remplir automatiquement les champs
    window.welcome_view.project_name.setText("Test Project Debug")
    window.welcome_view.project_manager.setText("Test Manager")
    window.welcome_view.laboratory.setText("Test Laboratory")
    
    print("✅ Champs remplis")
    print(f"✅ Bouton activé: {window.welcome_view.validate_button.isEnabled()}")
    
    print("\n2️⃣ Simulation du clic sur Valider...")
    
    # Simuler le clic sur le bouton
    QTest.mouseClick(window.welcome_view.validate_button, Qt.LeftButton)
    
    print("\n3️⃣ Résultats du test:")
    
    # Laisser l'application tourner un peu pour voir les résultats
    QTimer.singleShot(2000, app.quit)  # Fermer après 2 secondes
    
    return app.exec()

if __name__ == "__main__":
    exit_code = test_bouton_valider()
    print(f"\n🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)