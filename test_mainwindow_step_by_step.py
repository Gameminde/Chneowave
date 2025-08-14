#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow étape par étape pour identifier le point de crash
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_mainwindow_step_by_step(app=None):
    """Test MainWindow étape par étape"""
    print("=== TEST MAINWINDOW ÉTAPE PAR ÉTAPE ===")
    
    try:
        print("Étape 1: Import PySide6...")
        from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
        from PySide6.QtCore import QTimer
        print("✅ PySide6 importé")
        
        print("Étape 2: Configuration logging...")
        from hrneowave.core.logging_config import setup_logging
        setup_logging()
        print("✅ Logging configuré")
        
        print("Étape 3: Vérification QApplication...")
        if app is None:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
                print("✅ Nouvelle QApplication créée")
            else:
                print("✅ QApplication existante réutilisée")
        else:
            print("✅ QApplication fournie en paramètre")
        app.setApplicationName("CHNeoWave Step Test")
        
        print("Étape 4: Test QMainWindow basique...")
        test_window = QMainWindow()
        test_window.setWindowTitle("Test Window")
        test_window.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        label = QLabel("Test QMainWindow basique")
        layout.addWidget(label)
        test_window.setCentralWidget(central_widget)
        
        test_window.show()
        print(f"✅ QMainWindow basique visible: {test_window.isVisible()}")
        test_window.close()
        print("✅ QMainWindow basique fermé")
        
        print("Étape 5: Import modules CHNeoWave...")
        try:
            print("  5a: Import ThemeManager...")
            from hrneowave.gui.styles.theme_manager import ThemeManager
            print("  ✅ ThemeManager importé")
            
            print("  5b: Import ViewManager...")
            from hrneowave.gui.view_manager import ViewManager
            print("  ✅ ViewManager importé")
            
            print("  5c: Import WelcomeView...")
            from hrneowave.gui.views.welcome_view import WelcomeView
            print("  ✅ WelcomeView importé")
            
            print("  5d: Import DashboardViewMaritime...")
            from hrneowave.gui.views.dashboard_view import DashboardViewMaritime
            print("  ✅ DashboardViewMaritime importé")
            
        except Exception as e:
            print(f"  ❌ Erreur import modules: {e}")
            import traceback
            traceback.print_exc()
            return (False, None)
        
        print("Étape 6: Création ThemeManager...")
        try:
            theme_manager = ThemeManager(app)
            print("✅ ThemeManager créé")
            
            print("  6a: Application thème maritime...")
            theme_manager.apply_theme('maritime_professional')
            print("  ✅ Thème maritime appliqué")
            
        except Exception as e:
            print(f"❌ Erreur ThemeManager: {e}")
            import traceback
            traceback.print_exc()
            return (False, None)
        
        print("Étape 7: Import MainWindow...")
        try:
            from hrneowave.gui.main_window import MainWindow
            print("✅ MainWindow importé")
        except Exception as e:
            print(f"❌ Erreur import MainWindow: {e}")
            import traceback
            traceback.print_exc()
            return (False, None)
        
        print("Étape 8: Création MainWindow...")
        try:
            print("  8a: Appel constructeur MainWindow()...")
            main_window = MainWindow()
            print("  ✅ Constructeur MainWindow terminé")
            
            print("  8b: Configuration fenêtre...")
            main_window.setWindowTitle("CHNeoWave - Test Step by Step")
            main_window.setGeometry(200, 200, 1200, 800)
            print("  ✅ Configuration fenêtre terminée")
            
            print("  8c: Affichage fenêtre...")
            main_window.show()
            main_window.raise_()
            main_window.activateWindow()
            print("  ✅ Affichage demandé")
            
            print(f"  8d: Vérification visibilité: {main_window.isVisible()}")
            print(f"  8e: Taille: {main_window.size()}")
            print(f"  8f: Position: {main_window.pos()}")
            
            if main_window.isVisible():
                print("\n🎉 SUCCÈS! MainWindow créé et affiché")
                return (True, main_window)
            else:
                print("\n⚠️ MainWindow créé mais pas visible")
                return (False, None)
                
        except Exception as e:
            print(f"❌ Erreur création MainWindow: {e}")
            import traceback
            traceback.print_exc()
            return (False, None)
        
    except Exception as e:
        print(f"❌ ERREUR générale: {e}")
        import traceback
        traceback.print_exc()
        return (False, None)

def test_minimal_mainwindow():
    """Test avec une version minimale de MainWindow"""
    print("\n=== TEST MAINWINDOW MINIMAL ===")
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
        from PySide6.QtCore import QTimer
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Création d'une MainWindow minimale
        class MinimalMainWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("CHNeoWave - Minimal")
                self.setGeometry(300, 300, 800, 600)
                
                # Widget central simple
                central_widget = QWidget()
                layout = QVBoxLayout(central_widget)
                
                title = QLabel("CHNeoWave - Interface Minimale")
                title.setStyleSheet("font-size: 24px; color: #1565C0; margin: 20px;")
                
                status = QLabel("✅ Interface fonctionnelle sans modules complexes")
                status.setStyleSheet("font-size: 16px; color: #4CAF50; margin: 10px;")
                
                info = QLabel("Cette version minimale prouve que Qt fonctionne.\nLe problème vient des modules CHNeoWave.")
                info.setStyleSheet("font-size: 14px; color: #666; margin: 10px;")
                
                layout.addWidget(title)
                layout.addWidget(status)
                layout.addWidget(info)
                
                self.setCentralWidget(central_widget)
        
        print("Création MainWindow minimal...")
        minimal_window = MinimalMainWindow()
        
        print("Affichage MainWindow minimal...")
        minimal_window.show()
        minimal_window.raise_()
        minimal_window.activateWindow()
        
        print(f"✅ MainWindow minimal visible: {minimal_window.isVisible()}")
        
        if minimal_window.isVisible():
            print("\n🎉 SUCCÈS! MainWindow minimal fonctionne")
            print("Le problème vient des modules CHNeoWave complexes")
            return (True, app, minimal_window)
        else:
            print("\n❌ Même MainWindow minimal ne s'affiche pas")
            return (False, app, None)
            
    except Exception as e:
        print(f"❌ Erreur MainWindow minimal: {e}")
        import traceback
        traceback.print_exc()
        return (False, None, None)

def main():
    """Fonction principale"""
    print("DIAGNOSTIC MAINWINDOW - ÉTAPE PAR ÉTAPE")
    print("=======================================")
    
    # Test 1: MainWindow minimal
    print("\n--- Test 1: MainWindow minimal ---")
    minimal_success, app, minimal_window = test_minimal_mainwindow()
    
    if minimal_success and app:
        print("\n--- Test 2: MainWindow CHNeoWave complet ---")
        full_success, chneowave_window = test_mainwindow_step_by_step(app)
        
        if full_success and chneowave_window:
            print("\n🎉 TOUS LES TESTS RÉUSSIS!")
            print("L'interface CHNeoWave fonctionne correctement.")
            
            # Afficher l'interface CHNeoWave pendant 8 secondes
            from PySide6.QtCore import QTimer
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(8000)
            
            print("Interface CHNeoWave affichée pendant 8 secondes...")
            exit_code = app.exec()
            print(f"Application fermée avec code: {exit_code}")
            return 0
        else:
            print("\n⚠️ MainWindow CHNeoWave pose problème")
            print("Le problème vient des modules complexes CHNeoWave")
            
            # Afficher l'interface minimale pendant 5 secondes
            if minimal_window:
                from PySide6.QtCore import QTimer
                timer = QTimer()
                timer.timeout.connect(app.quit)
                timer.start(5000)
                
                print("Interface minimale affichée pendant 5 secondes...")
                exit_code = app.exec()
                print(f"Application fermée avec code: {exit_code}")
            
            return 1
    else:
        print("\n❌ Problème fondamental avec Qt/PySide6")
        return 1

if __name__ == "__main__":
    sys.exit(main())