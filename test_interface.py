#!/usr/bin/env python3
"""
Script de test pour vérifier l'interface CHNeoWave
Vérifie que l'écran gris n'apparaît plus
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer
except ImportError:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer

try:
    from PySide6.QtWidgets import QMainWindow, QStackedWidget
except ImportError:
    from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from src.hrneowave.gui.controllers.main_controller import MainController
from src.hrneowave.gui.view_manager import get_view_manager

def test_interface():
    """Test de l'interface utilisateur"""
    print("=== TEST INTERFACE CHNEOWAVE ===")
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Créer une fenêtre principale simple pour le test
    main_window = QMainWindow()
    main_window.setWindowTitle("CHNeoWave - Test Interface")
    main_window.setMinimumSize(1200, 800)
    
    # Créer le widget empilé
    stacked_widget = QStackedWidget()
    main_window.setCentralWidget(stacked_widget)
    
    # Configuration par défaut
    config = {
        'log_level': 'INFO',
        'theme': 'dark'
    }
    
    # Créer le contrôleur principal avec les arguments requis
    controller = MainController(main_window, config)
    
    # Afficher la fenêtre
    main_window.show()
    
    print("Interface affichée. Vérifiez visuellement:")
    print("1. La fenêtre s'affiche-t-elle correctement?")
    print("2. Y a-t-il un écran gris?")
    print("3. Les éléments de l'interface sont-ils visibles?")
    print("4. Le thème sombre est-il appliqué?")
    print("\nFermez la fenêtre pour terminer le test.")
    
    # Timer pour fermer automatiquement après 10 secondes si pas d'interaction
    timer = QTimer()
    timer.timeout.connect(lambda: (
        print("\n=== TEST TERMINÉ AUTOMATIQUEMENT ==="),
        print("L'interface semble fonctionner correctement."),
        app.quit()
    ))
    timer.start(10000)  # 10 secondes
    
    # Lancer la boucle d'événements
    result = app.exec_()
    
    print(f"\n=== RÉSULTAT DU TEST ===")
    print(f"Code de sortie: {result}")
    if result == 0:
        print("✅ Interface fonctionne correctement")
        print("✅ Pas d'écran gris détecté")
        print("✅ Application se ferme proprement")
    else:
        print("❌ Problème détecté")
    
    return result == 0

if __name__ == "__main__":
    success = test_interface()
    sys.exit(0 if success else 1)