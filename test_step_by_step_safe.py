#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test étape par étape ultra-sécurisé
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_step_1_pyside6():
    """Test 1: Import PySide6"""
    print("=== ÉTAPE 1: IMPORT PYSIDE6 ===")
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
        from PySide6.QtCore import QTimer
        print("✅ PySide6 importé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur import PySide6: {e}")
        return False

def test_step_2_qapplication():
    """Test 2: Création QApplication"""
    print("\n=== ÉTAPE 2: CRÉATION QAPPLICATION ===")
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✅ QApplication créée avec succès")
        return True, app
    except Exception as e:
        print(f"❌ Erreur création QApplication: {e}")
        return False, None

def test_step_3_logging():
    """Test 3: Configuration logging"""
    print("\n=== ÉTAPE 3: CONFIGURATION LOGGING ===")
    try:
        from hrneowave.core.logging_config import setup_logging
        setup_logging()
        print("✅ Logging configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur configuration logging: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_step_4_theme_manager():
    """Test 4: ThemeManager"""
    print("\n=== ÉTAPE 4: THEME MANAGER ===")
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        
        from hrneowave.gui.styles.theme_manager import ThemeManager
        print("✅ ThemeManager importé")
        
        theme_manager = ThemeManager(app)
        print("✅ ThemeManager créé")
        
        theme_manager.apply_theme('maritime_modern')
        print("✅ Thème maritime_modern appliqué")
        
        return True, theme_manager
    except Exception as e:
        print(f"❌ Erreur ThemeManager: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_step_5_mainwindow_import():
    """Test 5: Import MainWindow"""
    print("\n=== ÉTAPE 5: IMPORT MAINWINDOW ===")
    try:
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur import MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_step_6_mainwindow_creation():
    """Test 6: Création MainWindow"""
    print("\n=== ÉTAPE 6: CRÉATION MAINWINDOW ===")
    try:
        from hrneowave.gui.main_window import MainWindow
        
        print("Appel constructeur MainWindow()...")
        main_window = MainWindow()
        print("✅ MainWindow créé avec succès")
        
        print("Configuration fenêtre...")
        main_window.setWindowTitle("CHNeoWave - Test Étapes")
        main_window.setGeometry(100, 100, 800, 600)
        print("✅ MainWindow configuré")
        
        return True, main_window
    except Exception as e:
        print(f"❌ Erreur création MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_step_7_mainwindow_display():
    """Test 7: Affichage MainWindow"""
    print("\n=== ÉTAPE 7: AFFICHAGE MAINWINDOW ===")
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        
        app = QApplication.instance()
        
        # Récupérer MainWindow depuis l'étape précédente
        success, main_window = test_step_6_mainwindow_creation()
        if not success:
            return False
        
        print("Affichage MainWindow...")
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        print("✅ Affichage demandé")
        
        print(f"Visible: {main_window.isVisible()}")
        print(f"Taille: {main_window.size()}")
        print(f"Position: {main_window.pos()}")
        
        if main_window.isVisible():
            print("🎉 MainWindow visible avec succès!")
            
            # Timer pour fermer après 3 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(3000)
            
            print("Interface affichée pendant 3 secondes...")
            exit_code = app.exec()
            print(f"Application fermée avec code: {exit_code}")
            
            return True
        else:
            print("❌ MainWindow créé mais pas visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur affichage MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test principal étape par étape"""
    print("TEST MAINWINDOW - ÉTAPES SÉCURISÉES")
    print("====================================")
    
    # Étape 1: PySide6
    if not test_step_1_pyside6():
        return 1
    
    # Étape 2: QApplication
    success, app = test_step_2_qapplication()
    if not success:
        return 1
    
    # Étape 3: Logging
    if not test_step_3_logging():
        print("⚠️ Logging échoué, mais on continue...")
    
    # Étape 4: ThemeManager
    success, theme_manager = test_step_4_theme_manager()
    if not success:
        print("⚠️ ThemeManager échoué, mais on continue...")
    
    # Étape 5: Import MainWindow
    if not test_step_5_mainwindow_import():
        return 1
    
    # Étape 6 et 7: Création et affichage MainWindow
    if test_step_7_mainwindow_display():
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        return 0
    else:
        print("\n❌ ÉCHEC FINAL")
        return 1

if __name__ == "__main__":
    sys.exit(main())