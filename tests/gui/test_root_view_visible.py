#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de visibilité de la vue racine - HOTFIX écran vierge
Garantit qu'un widget est affiché au démarrage de l'application
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH pour les tests
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def test_root_view_visible(qtbot):
    """
    Test que la vue racine est visible au démarrage
    Vérifie que le QStackedWidget a un widget courant non-None
    """
    # Import conditionnel de QApplication
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        try:
            from PySide6.QtWidgets import QApplication
        except ImportError:
            pytest.skip("PySide6 non disponible")
    
    # Créer l'application si elle n'existe pas
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    try:
        # Import des modules nécessaires
        from hrneowave.gui.main_window import MainWindow as CHNeoWaveMainWindow
        from hrneowave.gui.controllers.main_controller import MainController
        
        # Créer la fenêtre principale
        win = CHNeoWaveMainWindow()
        qtbot.addWidget(win)
        
        # Obtenir le ViewManager
        from hrneowave.gui.view_manager import get_view_manager
        view_manager = get_view_manager()

        # Créer une configuration factice pour le test
        config = {'simulation': {'enabled': False}}

        # Initialiser le contrôleur principal
        controller = MainController(win, view_manager, config)
        controller.initialize()
        
        # Vérifier que la fenêtre existe
        assert win is not None, "La fenêtre principale ne doit pas être None"
        
        # Obtenir le ViewManager et son QStackedWidget
        from hrneowave.gui.view_manager import get_view_manager
        view_manager = get_view_manager()
        
        assert view_manager is not None, "Le ViewManager ne doit pas être None"
        
        sw = view_manager.stacked_widget
        assert sw is not None, "Le QStackedWidget ne doit pas être None"
        
        # Vérifier qu'il y a des widgets dans le stack
        assert sw.count() > 0, f"Le QStackedWidget doit contenir au moins 1 widget, trouvé: {sw.count()}"
        
        # Vérifier qu'un widget est actuellement affiché (currentIndex != -1)
        current_index = sw.currentIndex()
        assert current_index != -1, f"Le currentIndex ne doit pas être -1, trouvé: {current_index}"
        
        # Vérifier que le widget courant n'est pas None
        current_widget = sw.currentWidget()
        assert current_widget is not None, "Le widget courant ne doit pas être None"
        
        # Vérifier que le widget courant est visible
        assert current_widget.isVisible(), "Le widget courant doit être visible"
        
        print(f"✓ Test réussi: {sw.count()} vues, index courant: {current_index}")
        
    except ImportError as e:
        pytest.skip(f"Module hrneowave.cli non disponible: {e}")
    except Exception as e:
        pytest.fail(f"Erreur lors du test: {e}")


def test_stacked_widget_autofill_background(qtbot):
    """
    Test que le QStackedWidget a setAutoFillBackground(True)
    pour éviter les fonds transparents
    """
    # Import conditionnel de QApplication
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        try:
            from PyQt5.QtWidgets import QApplication
        except ImportError:
            pytest.skip("Ni PySide6 ni PyQt5 disponibles")
    
    # Créer l'application si elle n'existe pas
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    try:
        # Import des modules nécessaires
        from hrneowave.gui.main_window import CHNeoWaveMainWindow
        from hrneowave.gui.controllers.main_controller import MainController
        
        # Créer la fenêtre principale
        win = CHNeoWaveMainWindow()
        qtbot.addWidget(win)
        
        # Obtenir le ViewManager
        from hrneowave.gui.view_manager import get_view_manager
        view_manager = get_view_manager()

        # Créer une configuration factice pour le test
        config = {'simulation': {'enabled': False}}

        # Initialiser le contrôleur principal
        controller = MainController(win, view_manager, config)
        controller.initialize()
        
        # Obtenir le ViewManager et son QStackedWidget
        from hrneowave.gui.view_manager import get_view_manager
        view_manager = get_view_manager()
        sw = view_manager.stacked_widget
        
        # Vérifier que autoFillBackground est activé
        assert sw.autoFillBackground(), "Le QStackedWidget doit avoir autoFillBackground=True"
        
        print("✓ Test réussi: autoFillBackground activé")
        
    except ImportError as e:
        pytest.skip(f"Module hrneowave.cli non disponible: {e}")
    except Exception as e:
        pytest.fail(f"Erreur lors du test: {e}")


if __name__ == "__main__":
    # Exécution directe pour debug
    import pytest
    pytest.main([__file__, "-v"])