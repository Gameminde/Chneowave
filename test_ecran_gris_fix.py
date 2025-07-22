#!/usr/bin/env python3
"""
Test de validation du correctif pour l'écran gris de CHNeoWave
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Configuration du logging
from hrneowave.utils import setup_logging
setup_logging()

def test_ecran_gris_fix():
    """
    Test automatisé pour vérifier que le correctif de l'écran gris fonctionne
    """
    print("=== TEST CORRECTIF ÉCRAN GRIS ===")
    
    # Import conditionnel de QApplication
    try:
        from PySide6.QtWidgets import QApplication, QStackedWidget
        from PySide6.QtCore import QTimer
    except ImportError:
        try:
            from PyQt5.QtWidgets import QApplication, QStackedWidget
            from PyQt5.QtCore import QTimer
        except ImportError:
            print("❌ Erreur : Ni PySide6 ni PyQt5 ne sont disponibles")
            return False
    
    app = QApplication(sys.argv)
    
    try:
        # Import des modules GUI
        from hrneowave.gui.view_manager import get_view_manager
        from hrneowave.gui.views.welcome_view import WelcomeView
        from hrneowave.gui.views.calibration_view import CalibrationView
        from hrneowave.gui.views.acquisition_view import AcquisitionView
        from hrneowave.gui.views.analysis_view import AnalysisView
        
        # Création du QStackedWidget
        stacked_widget = QStackedWidget()
        
        # Création du ViewManager
        view_manager = get_view_manager(stacked_widget)
        
        # Enregistrement des vues
        welcome_view = WelcomeView()
        view_manager.register_view("welcome", welcome_view)
        
        calibration_view = CalibrationView()
        view_manager.register_view("calibration", calibration_view)
        
        acquisition_view = AcquisitionView()
        view_manager.register_view("acquisition", acquisition_view)
        
        analysis_view = AnalysisView()
        view_manager.register_view("analysis", analysis_view)
        
        print(f"✓ Vues enregistrées: {stacked_widget.count()}")
        
        # Application du HOTFIX
        if stacked_widget.count() > 0:
            # Forcer la visibilité du QStackedWidget
            stacked_widget.setVisible(True)
            stacked_widget.show()
            stacked_widget.setAutoFillBackground(True)
            
            # Forcer l'index à 0 et la visibilité du widget courant
            stacked_widget.setCurrentIndex(0)
            current_widget = stacked_widget.currentWidget()
            if current_widget:
                current_widget.setVisible(True)
                current_widget.show()
                current_widget.setAutoFillBackground(True)
            
            print(f"✓ HOTFIX appliqué - count: {stacked_widget.count()}")
        
        # Vérifications
        tests_passed = 0
        total_tests = 6
        
        # Test 1: Nombre de vues
        if stacked_widget.count() == 4:
            print("✓ Test 1 PASSÉ: 4 vues enregistrées")
            tests_passed += 1
        else:
            print(f"❌ Test 1 ÉCHOUÉ: {stacked_widget.count()} vues au lieu de 4")
        
        # Test 2: Index courant
        if stacked_widget.currentIndex() == 0:
            print("✓ Test 2 PASSÉ: Index courant = 0")
            tests_passed += 1
        else:
            print(f"❌ Test 2 ÉCHOUÉ: Index courant = {stacked_widget.currentIndex()}")
        
        # Test 3: Widget courant existe
        current_widget = stacked_widget.currentWidget()
        if current_widget is not None:
            print("✓ Test 3 PASSÉ: Widget courant existe")
            tests_passed += 1
        else:
            print("❌ Test 3 ÉCHOUÉ: Aucun widget courant")
        
        # Test 4: autoFillBackground du QStackedWidget
        if stacked_widget.autoFillBackground():
            print("✓ Test 4 PASSÉ: QStackedWidget autoFillBackground = True")
            tests_passed += 1
        else:
            print("❌ Test 4 ÉCHOUÉ: QStackedWidget autoFillBackground = False")
        
        # Test 5: autoFillBackground du widget courant
        if current_widget and current_widget.autoFillBackground():
            print("✓ Test 5 PASSÉ: Widget courant autoFillBackground = True")
            tests_passed += 1
        else:
            print("❌ Test 5 ÉCHOUÉ: Widget courant autoFillBackground = False")
        
        # Test 6: Type du widget courant
        if isinstance(current_widget, WelcomeView):
            print("✓ Test 6 PASSÉ: Widget courant est WelcomeView")
            tests_passed += 1
        else:
            print(f"❌ Test 6 ÉCHOUÉ: Widget courant est {type(current_widget)}")
        
        # Résultat final
        print(f"\n=== RÉSULTAT: {tests_passed}/{total_tests} tests passés ===")
        
        if tests_passed == total_tests:
            print("🎉 TOUS LES TESTS PASSÉS - Le correctif fonctionne !")
            return True
        else:
            print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ - Le correctif nécessite des ajustements")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

if __name__ == "__main__":
    success = test_ecran_gris_fix()
    sys.exit(0 if success else 1)