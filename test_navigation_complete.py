#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de navigation - Reproduction du bug bouton Valider
Test avec l'application complète pour identifier le problème
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer, Qt
    from PySide6.QtTest import QTest
except ImportError:
    print("❌ PySide6 non disponible")
    sys.exit(1)

def test_navigation_complete():
    """Test complet de la navigation avec l'application réelle"""
    print("🚀 TEST NAVIGATION COMPLETE")
    print("=" * 50)
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        print("📝 Début des imports...")
        # Importer et créer l'application CHNeoWave
        from hrneowave.gui.main_window import MainWindow
        print("📝 MainWindow importé")
        from hrneowave.gui.controllers.main_controller import MainController
        print("📝 MainController importé")
        
        print("✅ Imports réussis")
        
        # Créer la fenêtre principale avec config
        config = {
            'log_level': 'INFO',
            'theme': 'default'
        }
        print("📝 Création de MainWindow...")
        main_window = MainWindow(config)
        print("📝 MainWindow créé")
        
        # Créer le contrôleur principal
        print("📝 Création de MainController...")
        main_controller = MainController(main_window, main_window.stack_widget, config)
        print("📝 MainController créé")
        
        print("✅ Application initialisée")
        
        # Afficher la fenêtre
        main_window.show()
        
        # Vérifier que le ViewManager existe et a les vues enregistrées
        view_manager = main_controller.view_manager
        print(f"✅ ViewManager: {view_manager}")
        print(f"✅ Vues enregistrées: {list(view_manager.views.keys())}")
        
        # Vérifier que la vue welcome est active
        current_view = view_manager.current_view
        print(f"✅ Vue actuelle: {current_view}")
        
        # Obtenir la vue welcome
        welcome_view = view_manager.views.get('welcome')
        if welcome_view:
            print("✅ Vue welcome trouvée")
            
            # Remplir les champs automatiquement
            welcome_view.project_name.setText("Test Navigation Complete")
            welcome_view.project_manager.setText("Test Manager")
            welcome_view.laboratory.setText("Test Laboratory")
            
            print("✅ Champs remplis")
            print(f"✅ Bouton activé: {welcome_view.validate_button.isEnabled()}")
            
            # Connecter un signal pour observer la navigation
            def on_view_changed(view_name):
                print(f"🎯 [NAVIGATION] Vue changée vers: {view_name}")
                if view_name == "acquisition":
                    print("✅ [SUCCESS] Navigation vers acquisition réussie !")
                    QTimer.singleShot(1000, app.quit)
                else:
                    print(f"❌ [ERROR] Navigation inattendue vers: {view_name}")
                    QTimer.singleShot(1000, app.quit)
            
            # Connecter le signal de changement de vue
            if hasattr(view_manager, 'viewChanged'):
                view_manager.viewChanged.connect(on_view_changed)
            
            # Simuler le clic sur le bouton Valider
            print("\n2️⃣ Simulation du clic sur Valider...")
            QTest.mouseClick(welcome_view.validate_button, Qt.LeftButton)
            
            # Attendre un peu pour voir le résultat
            QTimer.singleShot(3000, lambda: (
                print(f"\n📊 État final:"),
                print(f"   Vue actuelle: {view_manager.current_view}"),
                print(f"   Navigation réussie: {view_manager.current_view == 'acquisition'}"),
                app.quit()
            ))
            
        else:
            print("❌ Vue welcome non trouvée")
            QTimer.singleShot(1000, app.quit)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        QTimer.singleShot(1000, app.quit)
    
    return app.exec()

if __name__ == "__main__":
    exit_code = test_navigation_complete()
    print(f"\n🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)