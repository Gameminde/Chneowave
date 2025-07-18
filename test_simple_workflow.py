#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple du workflow de création de projet
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import pyqtSlot

def main():
    """Test simple du workflow"""
    app = QApplication(sys.argv)
    
    try:
        # Import direct des vues
        from hrneowave.gui.views.welcome_view import WelcomeView
        from hrneowave.gui.views.acquisition_view import AcquisitionView
        
        # Créer une fenêtre de test simple
        window = QMainWindow()
        window.setWindowTitle("Test Workflow CHNeoWave")
        window.resize(800, 600)
        
        # Stack widget pour les vues
        stack = QStackedWidget()
        window.setCentralWidget(stack)
        
        # Créer les vues
        welcome_view = WelcomeView()
        
        # Configuration par défaut pour AcquisitionView
        default_config = {
            'n_sondes': 4,
            'sampling_rate': 1000,
            'buffer_size': 10000,
            'acquisition': {
                'duration': 60,
                'auto_save': True
            }
        }
        acquisition_view = AcquisitionView(default_config)
        
        # Ajouter au stack
        stack.addWidget(welcome_view)
        stack.addWidget(acquisition_view)
        
        # Simuler le signal projectCreated
        @pyqtSlot()
        def on_project_created():
            print("✅ Projet créé! Activation des boutons d'acquisition...")
            if hasattr(acquisition_view, 'btn_start'):
                acquisition_view.btn_start.setEnabled(True)
                print("✅ Bouton Start activé")
            if hasattr(acquisition_view, 'btn_export'):
                acquisition_view.btn_export.setEnabled(True)
                print("✅ Bouton Export activé")
            
            # Passer à la vue d'acquisition
            stack.setCurrentIndex(1)
            print("✅ Navigation vers l'onglet Acquisition")
        
        # Connecter le signal
        welcome_view.projectCreated.connect(on_project_created)
        
        # Afficher la fenêtre
        window.show()
        
        print("=" * 50)
        print("Test Workflow CHNeoWave")
        print("=" * 50)
        print("1. Remplissez le formulaire")
        print("2. Cliquez sur 'Créer le projet'")
        print("3. Observez l'activation des boutons")
        print("=" * 50)
        
        # Lancer l'application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()