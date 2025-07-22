#!/usr/bin/env python3
"""
Validation visuelle du correctif pour l'écran gris de CHNeoWave
Ce script lance l'application et reste ouvert pour permettre la validation visuelle
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

def main():
    """
    Lance CHNeoWave pour validation visuelle du correctif écran gris
    """
    print("=== VALIDATION VISUELLE CORRECTIF ÉCRAN GRIS ===")
    print("Ce script lance CHNeoWave pour validation visuelle.")
    print("L'application devrait s'ouvrir avec l'interface visible (pas d'écran gris).")
    print("Fermez la fenêtre pour terminer la validation.\n")
    
    # Import conditionnel de QApplication
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        try:
            from PyQt5.QtWidgets import QApplication
        except ImportError:
            print("❌ Erreur : Ni PySide6 ni PyQt5 ne sont disponibles")
            return 1
    
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave - Validation Visuelle")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Laboratoire Maritime")
    
    try:
        # Import des modules GUI
        from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStackedWidget
        from PySide6.QtCore import Qt
        
        from hrneowave.gui.view_manager import get_view_manager
        from hrneowave.gui.controllers.main_controller import MainController
        from hrneowave.gui.theme import get_stylesheet
        
        # Définition de la classe de validation
        class ValidationWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("CHNeoWave v1.0.0 - VALIDATION VISUELLE CORRECTIF ÉCRAN GRIS")
                self.setMinimumSize(1200, 800)
                self.resize(1366, 768)
                
                # Application du thème
                self.setStyleSheet(get_stylesheet())
                
                # Configuration du widget central
                central_widget = QWidget()
                self.setCentralWidget(central_widget)
                
                # Layout principal
                layout = QVBoxLayout(central_widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                
                # Création du QStackedWidget
                self.stacked_widget = QStackedWidget()
                layout.addWidget(self.stacked_widget)
                
                # Création du ViewManager
                self.view_manager = get_view_manager(self.stacked_widget)
                
                # Enregistrement des vues
                self.setup_views()
                
                # APPLICATION DU CORRECTIF ÉCRAN GRIS
                self.apply_hotfix()
                
                # Création du MainController
                default_config = {'log_level': 'INFO', 'theme': 'dark'}
                self.main_controller = MainController(self, default_config)
                
                # Centrage de la fenêtre
                self._center_window()
                
                print("✅ VALIDATION VISUELLE: Application lancée avec correctif appliqué")
                print("📋 VÉRIFICATIONS À EFFECTUER:")
                print("   1. La fenêtre s'ouvre sans écran gris")
                print("   2. L'interface Welcome est visible")
                print("   3. Les éléments de l'interface sont correctement affichés")
                print("   4. Le thème sombre est appliqué")
                print("\n🔍 Fermez la fenêtre quand la validation est terminée.")
            
            def setup_views(self):
                """Enregistre les vues dans le ViewManager"""
                from hrneowave.gui.views.welcome_view import WelcomeView
                from hrneowave.gui.views.calibration_view import CalibrationView
                from hrneowave.gui.views.acquisition_view import AcquisitionView
                from hrneowave.gui.views.analysis_view import AnalysisView
                
                # Enregistrement des vues
                self.welcome_view = WelcomeView()
                self.view_manager.register_view("welcome", self.welcome_view)
                
                self.calibration_view = CalibrationView()
                self.view_manager.register_view("calibration", self.calibration_view)
                
                self.acquisition_view = AcquisitionView()
                self.view_manager.register_view("acquisition", self.acquisition_view)
                
                self.analysis_view = AnalysisView()
                self.view_manager.register_view("analysis", self.analysis_view)
                
                print(f"✓ {self.stacked_widget.count()} vues enregistrées")
            
            def apply_hotfix(self):
                """Applique le correctif pour l'écran gris"""
                if self.stacked_widget.count() > 0:
                    # Forcer la visibilité du QStackedWidget
                    self.stacked_widget.setVisible(True)
                    self.stacked_widget.show()
                    self.stacked_widget.setAutoFillBackground(True)
                    
                    # Forcer l'index à 0 et la visibilité du widget courant
                    self.stacked_widget.setCurrentIndex(0)
                    current_widget = self.stacked_widget.currentWidget()
                    if current_widget:
                        current_widget.setVisible(True)
                        current_widget.show()
                        current_widget.setAutoFillBackground(True)
                    
                    print(f"✅ CORRECTIF APPLIQUÉ: count={self.stacked_widget.count()}, visible={self.stacked_widget.isVisible()}")
                    
                    # Diagnostic détaillé
                    print(f"📊 DIAGNOSTIC POST-CORRECTIF:")
                    print(f"   - QStackedWidget visible: {self.stacked_widget.isVisible()}")
                    print(f"   - QStackedWidget autoFillBackground: {self.stacked_widget.autoFillBackground()}")
                    print(f"   - Index courant: {self.stacked_widget.currentIndex()}")
                    if current_widget:
                        print(f"   - Widget courant visible: {current_widget.isVisible()}")
                        print(f"   - Widget courant autoFillBackground: {current_widget.autoFillBackground()}")
                        print(f"   - Type widget courant: {type(current_widget).__name__}")
            
            def _center_window(self):
                """Centre la fenêtre sur l'écran"""
                screen = QApplication.primaryScreen().geometry()
                window = self.geometry()
                x = (screen.width() - window.width()) // 2
                y = (screen.height() - window.height()) // 2
                self.move(x, y)
        
        # Création et affichage de la fenêtre de validation
        validation_window = ValidationWindow()
        validation_window.show()
        
        # Lancement de la boucle d'événements
        result = app.exec()
        
        print("\n✅ VALIDATION VISUELLE TERMINÉE")
        if result == 0:
            print("🎉 L'application s'est fermée normalement")
        else:
            print(f"⚠️  L'application s'est fermée avec le code: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la validation visuelle: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())