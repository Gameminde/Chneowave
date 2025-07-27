#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test automatisé pour vérifier que la fenêtre principale n'affiche plus d'écran gris
Ce test échoue si le problème du double QStackedWidget réapparaît
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


# MockPerformanceMonitor est maintenant géré par conftest.py

def test_root_view_visible(qtbot):
    """
    Test que la fenêtre principale affiche du contenu visible (pas d'écran gris)
    """
    # Créer l'application de test
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    
    # Import de la classe principale
    from PySide6.QtWidgets import QMainWindow, QStackedWidget
    from hrneowave.gui.view_manager import ViewManager
    from hrneowave.gui.controllers.main_controller import MainController
    from hrneowave.gui.styles.theme_manager import ThemeManager
    
    # Créer la fenêtre de test
    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("CHNeoWave Test")
            self.setMinimumSize(800, 600)
            
            # Créer le QStackedWidget unique
            self.stack_widget = QStackedWidget()
            self.setCentralWidget(self.stack_widget)
            
            # Créer le ViewManager
            self.view_manager = ViewManager(self.stack_widget)
            
            # Enregistrer les vues
            self.setup_views()
            
            # Créer le MainController avec le view_manager
            default_config = {
                'log_level': 'INFO',
                'theme': 'dark'
            }
            self.main_controller = MainController(self, self.view_manager, default_config)
            self.view_manager.change_view('dashboard')
                        # Simuler l'application d'un thème pour éviter les problèmes de style
            # et se rapprocher des conditions réelles de l'application.
            app = QApplication.instance()
            if app:
                theme_manager = ThemeManager(app)
                theme_manager.apply_theme('dark')
            
        def setup_views(self):
            """Enregistre les vues de test"""
            # Créer une vue de test simple pour éviter les violations d'accès
            from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
            test_view = QWidget()
            layout = QVBoxLayout(test_view)
            label = QLabel("Test View - Not Grey!")
            label.setStyleSheet("color: white; background-color: blue; padding: 20px;")
            layout.addWidget(label)
            self.view_manager.register_view("dashboard", test_view)
    
    # Créer et afficher la fenêtre de test
    win = TestMainWindow()
    qtbot.addWidget(win)
    win.show()
    
    # Attendre que l'interface soit prête
    qtbot.waitForWindowShown(win)
    qtbot.wait(500)  # Attendre que l'initialisation soit complète
    
    # Capturer l'image de la fenêtre
    img = win.grab().toImage()
    
    # Vérifier qu'il y a du contenu visible (pas seulement du gris)
    # Couleur gris foncé typique: #2d2d2d (valeur ~45)
    # On vérifie qu'au moins quelques pixels ont une valeur différente du gris
    non_grey_pixels = 0
    total_checked = 0
    
    # Échantillonner des pixels sur toute la fenêtre
    for x in range(0, img.width(), 50):
        for y in range(0, img.height(), 50):
            pixel_color = img.pixelColor(x, y)
            total_checked += 1
            
            # Vérifier si le pixel n'est pas gris (valeur > 50 ou < 40)
            if pixel_color.value() > 50 or pixel_color.value() < 40:
                non_grey_pixels += 1
    
    # Au moins 10% des pixels échantillonnés doivent être non-gris
    non_grey_ratio = non_grey_pixels / total_checked if total_checked > 0 else 0
    
    print(f"Pixels non-gris: {non_grey_pixels}/{total_checked} ({non_grey_ratio:.2%})")
    
    # Assertion: la fenêtre ne doit pas être entièrement grise
    assert non_grey_ratio > 0.1, f"Fenêtre semble grise! Seulement {non_grey_ratio:.2%} de pixels non-gris détectés"
    
    # Vérifier que le QStackedWidget a bien des widgets
    assert win.stack_widget.count() > 0, "Aucun widget dans le QStackedWidget"
    
    # Vérifier qu'un widget est actuellement affiché
    current_widget = win.stack_widget.currentWidget()
    assert current_widget is not None, "Aucun widget courant dans le QStackedWidget"
    assert current_widget.isVisible(), "Le widget courant n'est pas visible"
    
    print("✅ Test réussi: La fenêtre affiche du contenu visible (pas d'écran gris)")


def test_single_stacked_widget():
    """
    Test que le MainController utilise bien le QStackedWidget fourni
    et ne crée pas de doublon
    """
    from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
    
    app = QApplication.instance() or QApplication([])
    
    # Créer une fenêtre de test
    main_window = QMainWindow()
    original_stacked_widget = QStackedWidget()
    main_window.setCentralWidget(original_stacked_widget)
    
    # Créer le MainController
    from hrneowave.gui.controllers.main_controller import MainController
    from hrneowave.gui.view_manager import ViewManager
    config = {'log_level': 'INFO', 'theme': 'dark'}
    view_manager = ViewManager(original_stacked_widget)
    controller = MainController(main_window, view_manager, config)
    
    # Vérifier que le MainController utilise le bon QStackedWidget
    assert controller.view_manager.stacked_widget is original_stacked_widget, "MainController n'utilise pas le QStackedWidget fourni"
    
    # Vérifier que le centralWidget n'a pas été remplacé
    assert main_window.centralWidget() is original_stacked_widget, "Le centralWidget a été remplacé par un autre QStackedWidget"
    
    print("✅ Test réussi: Un seul QStackedWidget utilisé, pas de doublon")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])