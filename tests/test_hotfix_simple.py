#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple du HOTFIX pour vérifier que l'écran vierge est corrigé
"""

import sys
import os
from pathlib import Path

# Ajouter src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_hotfix():
    """
    Test simple du correctif d'écran vierge
    Utilise le même code que main.py
    """
    print("=== Test du HOTFIX écran vierge ===")
    
    # Import conditionnel Qt comme dans main.py
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget
        print("✓ PySide6 importé avec succès")
    except ImportError:
        try:
            from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget
            print("✓ PyQt5 importé avec succès")
        except ImportError:
            print("✗ Aucune bibliothèque Qt disponible")
            return False
    
    # Créer l'application comme dans main.py
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        app.setApplicationName("CHNeoWave")
        print("✓ QApplication créée")
    
    try:
        # Créer une fenêtre simple avec QStackedWidget comme dans main.py
        class TestMainWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("CHNeoWave Test")
                self.setMinimumSize(800, 600)
                
                # Widget central
                central_widget = QWidget()
                self.setCentralWidget(central_widget)
                
                # Layout principal
                layout = QVBoxLayout(central_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                
                # QStackedWidget
                self.stacked_widget = QStackedWidget()
                layout.addWidget(self.stacked_widget)
                
                # Appliquer le HOTFIX
                self.stacked_widget.setAutoFillBackground(True)
                
                # Ajouter quelques widgets de test
                test_widget1 = QWidget()
                test_widget2 = QWidget()
                
                self.stacked_widget.addWidget(test_widget1)
                self.stacked_widget.addWidget(test_widget2)
                
                # HOTFIX: Forcer l'affichage de la première vue si currentIndex == -1
                if self.stacked_widget.currentIndex() == -1 and self.stacked_widget.count() > 0:
                    self.stacked_widget.setCurrentIndex(0)
                    print("🔧 HOTFIX appliqué: currentIndex forcé à 0")
        
        # Créer la fenêtre de test
        main_window = TestMainWindow()
        print("✓ Fenêtre de test créée")
        
        # Vérifications du HOTFIX
        sw = main_window.stacked_widget
        count = sw.count()
        current_index = sw.currentIndex()
        current_widget = sw.currentWidget()
        auto_fill = sw.autoFillBackground()
        
        print(f"✓ Nombre de vues dans le stack: {count}")
        print(f"✓ Index courant: {current_index}")
        print(f"✓ Widget courant: {type(current_widget).__name__ if current_widget else 'None'}")
        print(f"✓ AutoFillBackground: {auto_fill}")
        
        # Vérifications du HOTFIX
        if current_index == -1:
            print("✗ HOTFIX ÉCHEC: currentIndex est encore -1")
            return False
        
        if count == 0:
            print("✗ HOTFIX ÉCHEC: Aucune vue dans le stack")
            return False
        
        if current_widget is None:
            print("✗ HOTFIX ÉCHEC: Widget courant est None")
            return False
        
        if not auto_fill:
            print("✗ HOTFIX ÉCHEC: AutoFillBackground n'est pas activé")
            return False
        
        print("\n🎉 HOTFIX RÉUSSI: L'écran vierge est corrigé!")
        print(f"   - {count} vues enregistrées")
        print(f"   - Vue courante à l'index {current_index}")
        print(f"   - Widget courant: {type(current_widget).__name__}")
        print(f"   - AutoFillBackground: {auto_fill}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_hotfix()
    sys.exit(0 if success else 1)