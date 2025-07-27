#!/usr/bin/env python3
"""
Test de débogage pour le workflow de navigation
Reproche le bug où l'application navigue vers 'acquisition' puis revient à 'welcome'
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

def test_navigation_workflow():
    """Test de navigation avec logs détaillés"""
    print("\n=== TEST NAVIGATION WORKFLOW ===")
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Importer et créer la fenêtre principale
        from hrneowave.gui.main_window import MainWindow
        
        
        print("[DEBUG] Création de MainWindow...")
        main_window = MainWindow()
        
        print("[DEBUG] Récupération du ViewManager...")
        view_manager = main_window.view_manager
        
        print(f"[DEBUG] Vue actuelle: {view_manager.current_view}")
        print(f"[DEBUG] Vues enregistrées: {list(view_manager.views.keys())}")
        
        # Afficher la fenêtre
        main_window.show()
        
        # Attendre que l'interface soit prête
        QTest.qWait(500)
        
        print(f"[DEBUG] Vue après affichage: {view_manager.current_view}")
        
        # Récupérer la vue welcome
        welcome_view = view_manager.views.get('welcome')
        if not welcome_view:
            print("[ERROR] Vue welcome non trouvée!")
            return False
            
        print("[DEBUG] Vue welcome trouvée")
        
        # Remplir le formulaire
        print("[DEBUG] Remplissage du formulaire...")
        welcome_view.project_name.setText("Test Navigation")
        welcome_view.project_manager.setText("Test Manager")
        welcome_view.laboratory.setText("Test Lab")
        
        # Attendre que la validation soit activée
        QTest.qWait(100)
        
        print(f"[DEBUG] Bouton activé: {welcome_view.validate_button.isEnabled()}")
        
        if not welcome_view.validate_button.isEnabled():
            print("[ERROR] Bouton de validation non activé!")
            return False
            
        print("[DEBUG] Clic sur le bouton Valider...")
        
        # Simuler le clic sur le bouton
        QTest.mouseClick(welcome_view.validate_button, Qt.LeftButton)
        
        # Attendre le traitement
        QTest.qWait(1000)
        
        print(f"[DEBUG] Vue après clic: {view_manager.current_view}")
        
        # Attendre encore un peu pour voir si ça change
        QTest.qWait(2000)
        
        print(f"[DEBUG] Vue finale: {view_manager.current_view}")
        
        # Vérifier le résultat
        if view_manager.current_view == 'acquisition':
            print("[SUCCESS] Navigation vers acquisition réussie!")
            return True
        else:
            print(f"[FAIL] Navigation échouée - Vue actuelle: {view_manager.current_view}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Nettoyer
        if main_window:
            main_window.close()
        app.quit()

if __name__ == '__main__':
    success = test_navigation_workflow()
    sys.exit(0 if success else 1)