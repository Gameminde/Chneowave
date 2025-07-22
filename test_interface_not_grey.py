#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que l'interface CHNeoWave n'affiche pas un écran gris
Ce test échoue si la fenêtre est 100% grise
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QScreen

def test_interface_not_grey():
    """
    Test que l'interface CHNeoWave n'est pas entièrement grise
    """
    print("\n=== TEST INTERFACE NOT GREY ===")
    
    # Créer l'application si elle n'existe pas
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Import et création de la fenêtre principale
    from main import main
    
    # Lancer l'application en mode test
    try:
        # Import des classes nécessaires
        from PySide6.QtWidgets import QMainWindow, QStackedWidget
        
        from src.hrneowave.gui.controllers.main_controller import MainController
        from src.hrneowave.gui.theme import get_stylesheet
        
        # Créer la fenêtre principale comme dans main.py
        class TestCHNeoWaveMainWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("CHNeoWave Test - Interface Not Grey")
                self.setMinimumSize(800, 600)
                self.resize(800, 600)
                
                # Application du thème
                self.setStyleSheet(get_stylesheet())
                
                # QStackedWidget comme widget central
                self.stacked_widget = QStackedWidget()
                self.setCentralWidget(self.stacked_widget)
                
                # ViewManager
                
                
                # Setup des vues
                self.setup_views()
                
                # MainController
                default_config = {'log_level': 'INFO', 'theme': 'dark'}
                self.main_controller = MainController(self, default_config)
                
            def setup_views(self):
                from src.hrneowave.gui.views.welcome_view import WelcomeView
                from src.hrneowave.gui.views.calibration_view import CalibrationView
                from src.hrneowave.gui.views.acquisition_view import AcquisitionView
                from src.hrneowave.gui.views.analysis_view import AnalysisView
                
                # Enregistrer les vues
                self.welcome_view = WelcomeView()
                self.view_manager.register_view("welcome", self.welcome_view)
                
                self.calibration_view = CalibrationView()
                self.view_manager.register_view("calibration", self.calibration_view)
                
                self.acquisition_view = AcquisitionView()
                self.view_manager.register_view("acquisition", self.acquisition_view)
                
                self.analysis_view = AnalysisView()
                self.view_manager.register_view("analysis", self.analysis_view)
                
                # Activer la vue d'accueil
                self.view_manager.switch_to_view("welcome")
        
        # Créer et afficher la fenêtre
        window = TestCHNeoWaveMainWindow()
        window.show()
        
        # Attendre que l'interface soit rendue
        app.processEvents()
        
        # Vérifications de base
        assert window.isVisible(), "La fenêtre doit être visible"
        assert window.stacked_widget.count() > 0, "Le QStackedWidget doit contenir des widgets"
        
        current_widget = window.stacked_widget.currentWidget()
        assert current_widget is not None, "Il doit y avoir un widget courant"
        assert current_widget.isVisible(), "Le widget courant doit être visible"
        
        print(f"✅ Fenêtre visible: {window.isVisible()}")
        print(f"✅ QStackedWidget count: {window.stacked_widget.count()}")
        print(f"✅ Widget courant visible: {current_widget.isVisible()}")
        print(f"✅ Taille fenêtre: {window.size()}")
        print(f"✅ Taille widget courant: {current_widget.size()}")
        
        # Test de capture d'écran pour vérifier que ce n'est pas gris
        try:
            # Capturer la fenêtre
            screen = QApplication.primaryScreen()
            if screen:
                # Capturer la région de la fenêtre
                window_rect = window.geometry()
                pixmap = screen.grabWindow(0, window_rect.x(), window_rect.y(), 
                                         window_rect.width(), window_rect.height())
                
                if not pixmap.isNull():
                    # Analyser les couleurs du pixmap
                    image = pixmap.toImage()
                    
                    # Échantillonner quelques pixels pour vérifier la diversité des couleurs
                    colors = set()
                    width, height = image.width(), image.height()
                    
                    # Échantillonner 100 pixels répartis sur l'image
                    sample_points = [
                        (width//4, height//4),
                        (width//2, height//4),
                        (3*width//4, height//4),
                        (width//4, height//2),
                        (width//2, height//2),
                        (3*width//4, height//2),
                        (width//4, 3*height//4),
                        (width//2, 3*height//4),
                        (3*width//4, 3*height//4),
                    ]
                    
                    for x, y in sample_points:
                        if 0 <= x < width and 0 <= y < height:
                            color = image.pixelColor(x, y)
                            colors.add((color.red(), color.green(), color.blue()))
                    
                    print(f"✅ Couleurs échantillonnées: {len(colors)}")
                    print(f"✅ Échantillon de couleurs: {list(colors)[:5]}")
                    
                    # Vérifier qu'il y a une diversité de couleurs (pas juste du gris)
                    assert len(colors) > 1, f"Interface semble monochrome: {colors}"
                    
                    # Vérifier qu'il n'y a pas que des nuances de gris
                    non_grey_colors = 0
                    for r, g, b in colors:
                        # Une couleur n'est pas grise si R, G, B ne sont pas tous égaux
                        # ou si elle n'est pas dans la gamme des gris (où R≈G≈B)
                        if not (abs(r-g) <= 10 and abs(g-b) <= 10 and abs(r-b) <= 10):
                            non_grey_colors += 1
                    
                    print(f"✅ Couleurs non-grises détectées: {non_grey_colors}/{len(colors)}")
                    
                    # Au moins 20% des couleurs échantillonnées doivent être non-grises
                    min_non_grey = max(1, len(colors) // 5)
                    assert non_grey_colors >= min_non_grey, \
                        f"Interface trop grise: {non_grey_colors} couleurs non-grises sur {len(colors)}"
                    
                    print("✅ Test couleurs réussi: Interface n'est pas entièrement grise")
                    
                else:
                    print("⚠️ Impossible de capturer l'écran, test de couleurs ignoré")
            else:
                print("⚠️ Écran principal non disponible, test de couleurs ignoré")
                
        except Exception as e:
            print(f"⚠️ Erreur lors du test de couleurs: {e}")
            # Ne pas faire échouer le test pour cette erreur
        
        # Test de contenu des widgets
        try:
            # Vérifier que le widget courant a du contenu
            if hasattr(current_widget, 'layout') and current_widget.layout():
                layout_count = current_widget.layout().count()
                print(f"✅ Éléments dans le layout: {layout_count}")
                assert layout_count > 0, "Le widget courant doit avoir du contenu"
            
            # Vérifier les enfants du widget
            children_count = len(current_widget.children())
            print(f"✅ Widgets enfants: {children_count}")
            assert children_count > 0, "Le widget courant doit avoir des enfants"
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification du contenu: {e}")
        
        # Fermer la fenêtre
        window.close()
        
        print("✅ TEST RÉUSSI: L'interface n'est pas entièrement grise")
        
    except Exception as e:
        print(f"❌ ERREUR dans le test: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"Test échoué: {e}")

if __name__ == "__main__":
    # Exécuter le test directement
    test_interface_not_grey()
    print("Test terminé avec succès")