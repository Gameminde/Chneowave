#!/usr/bin/env python3
"""
Test de débogage pour reproduire le crash après validation du projet.
"""

import sys
import os
import traceback
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest

def test_navigation_crash():
    """Test la navigation de WelcomeView vers DashboardView."""
    print("=== Test de navigation WelcomeView → DashboardView ===\n")
    
    try:
        # Créer l'application Qt
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✓ QApplication créée")
        
        # Importer MainWindow
        from hrneowave.gui.main_window import MainWindow
        print("✓ MainWindow importée")
        
        # Créer la fenêtre principale
        main_window = MainWindow()
        print("✓ MainWindow créée")
        
        # Afficher la fenêtre
        main_window.show()
        print("✓ MainWindow affichée")
        
        # Attendre que l'interface soit prête
        QTest.qWait(500)
        print("✓ Interface initialisée")
        
        # Vérifier que nous sommes sur welcome
        current_view = main_window.view_manager.get_current_view()
        print(f"Vue actuelle: {current_view}")
        
        if current_view != "welcome":
            print(f"⚠ Vue attendue: welcome, vue actuelle: {current_view}")
            # Naviguer vers welcome si nécessaire
            main_window.view_manager.switch_to_view("welcome")
            QTest.qWait(200)
        
        # Obtenir la welcome view
        welcome_view = main_window.view_manager.get_view_widget("welcome")
        if not welcome_view:
            print("✗ Impossible d'obtenir welcome view")
            return False
        print("✓ Welcome view obtenue")
        
        # Remplir le formulaire
        welcome_view.project_name.setText("TestProject")
        welcome_view.project_manager.setText("TestManager")
        welcome_view.laboratory.setText("TestLab")
        welcome_view.description.setPlainText("Test Description")
        print("✓ Formulaire rempli")
        
        # Attendre un peu
        QTest.qWait(200)
        
        print("\n=== Tentative de navigation vers dashboard ===\n")
        
        # Tenter la navigation directe vers dashboard
        print("Test 1: Navigation directe...")
        success = main_window.view_manager.switch_to_view("dashboard")
        print(f"Résultat navigation directe: {success}")
        
        if success:
            QTest.qWait(1000)  # Attendre 1 seconde
            current_view = main_window.view_manager.get_current_view()
            print(f"Vue après navigation: {current_view}")
            
            # Vérifier si l'application est toujours active
            if app.activeWindow():
                print("✓ Application toujours active")
            else:
                print("✗ Application fermée ou inactive")
                return False
        
        print("\n=== Test de création de DashboardView isolée ===\n")
        
        # Test de création isolée de DashboardView
        try:
            from hrneowave.gui.views.dashboard_view import DashboardView
            dashboard = DashboardView()
            print("✓ DashboardView créée en isolation")
            
            dashboard.show()
            print("✓ DashboardView affichée en isolation")
            
            QTest.qWait(1000)
            
            if dashboard.isVisible():
                print("✓ DashboardView toujours visible")
            else:
                print("✗ DashboardView fermée")
                
            dashboard.close()
            print("✓ DashboardView fermée proprement")
            
        except Exception as e:
            print(f"✗ Erreur lors de la création de DashboardView: {e}")
            traceback.print_exc()
            return False
        
        print("\n=== Test terminé avec succès ===\n")
        return True
        
    except Exception as e:
        print(f"✗ Erreur durant le test: {e}")
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer
        if 'main_window' in locals():
            main_window.close()
        if app:
            app.quit()

if __name__ == "__main__":
    success = test_navigation_crash()
    print(f"\nRésultat final: {'SUCCÈS' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)