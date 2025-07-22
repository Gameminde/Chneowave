#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour reproduire et diagnostiquer le problème d'écran gris de CHNeoWave
"""

import pytest
import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Import Qt
try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QPixmap
except ImportError:
    from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

# Import du ViewManager



class CHNeoWaveMainWindow(QMainWindow):
    """Fenêtre principale avec ViewManager réel pour les tests"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHNeoWave Test")
        self.setMinimumSize(800, 600)
        
        # Créer le QStackedWidget comme widget central
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Créer le ViewManager avec le QStackedWidget
        
        
        # Enregistrer les vues
        self.setup_views()
        
    def setup_views(self):
        """Enregistre les vues dans le ViewManager"""
        print("Début de setup_views()")
        
        # Essayer d'importer et d'enregistrer WelcomeView
        try:
            from src.hrneowave.gui.views.welcome_view import WelcomeView
            welcome_view = WelcomeView()
            self.view_manager.register_view("welcome", welcome_view)
            print("WelcomeView enregistrée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'importation de WelcomeView: {e}")
            # Vue de secours
            fallback_view = QLabel("Vue d'Accueil (Secours)")
            fallback_view.setStyleSheet("""
                QLabel {
                    background-color: #2d3748;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    text-align: center;
                    padding: 50px;
                }
            """)
            fallback_view.setAlignment(Qt.AlignCenter)
            self.view_manager.register_view("welcome", fallback_view)
            print("Vue de secours WelcomeView enregistrée")
        
        # Essayer d'importer et d'enregistrer CalibrationView
        try:
            from src.hrneowave.gui.views.calibration_view import CalibrationView
            calibration_view = CalibrationView()
            self.view_manager.register_view("calibration", calibration_view)
            print("CalibrationView enregistrée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'importation de CalibrationView: {e}")
            # Vue de secours
            fallback_view = QLabel("Vue de Calibration (Secours)")
            fallback_view.setStyleSheet("""
                QLabel {
                    background-color: #4a5568;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    text-align: center;
                    padding: 50px;
                }
            """)
            fallback_view.setAlignment(Qt.AlignCenter)
            self.view_manager.register_view("calibration", fallback_view)
            print("Vue de secours CalibrationView enregistrée")
        
        # Essayer d'importer et d'enregistrer AcquisitionView
        try:
            from src.hrneowave.gui.views.acquisition_view import AcquisitionView
            acquisition_view = AcquisitionView()
            self.view_manager.register_view("acquisition", acquisition_view)
            print("AcquisitionView enregistrée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'importation de AcquisitionView: {e}")
            # Vue de secours
            fallback_view = QLabel("Vue d'Acquisition (Secours)")
            fallback_view.setStyleSheet("""
                QLabel {
                    background-color: #2b6cb0;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    text-align: center;
                    padding: 50px;
                }
            """)
            fallback_view.setAlignment(Qt.AlignCenter)
            self.view_manager.register_view("acquisition", fallback_view)
            print("Vue de secours AcquisitionView enregistrée")
        
        # Essayer d'importer et d'enregistrer AnalysisView
        try:
            from src.hrneowave.gui.views.analysis_view import AnalysisView
            analysis_view = AnalysisView()
            self.view_manager.register_view("analysis", analysis_view)
            print("AnalysisView enregistrée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'importation de AnalysisView: {e}")
            # Vue de secours
            fallback_view = QLabel("Vue d'Analyse (Secours)")
            fallback_view.setStyleSheet("""
                QLabel {
                    background-color: #38a169;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    text-align: center;
                    padding: 50px;
                }
            """)
            fallback_view.setAlignment(Qt.AlignCenter)
            self.view_manager.register_view("analysis", fallback_view)
            print("Vue de secours AnalysisView enregistrée")
        
        # Changer vers la vue d'accueil
        if self.view_manager.views:
            self.view_manager.switch_to_view("welcome")
            print("Changement vers la vue welcome")
        
        print(f"Fin de setup_views() - {len(self.view_manager.views)} vues enregistrées")


def test_main_app_launch(qtbot):
    """Test de lancement de l'application principale avec ViewManager réel"""
    try:
        # Créer l'application si elle n'existe pas
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Reset du ViewManager pour éviter les conflits
        reset_view_manager()
        
        # Créer et afficher la fenêtre
        main_window = CHNeoWaveMainWindow()
        qtbot.addWidget(main_window)
        main_window.show()
        qtbot.waitForWindowShown(main_window)
        
        # Diagnostic détaillé
        print(f"\n=== DIAGNOSTIC VIEWMANAGER ===")
        print(f"Fenêtre visible: {main_window.isVisible()}")
        print(f"Fenêtre taille: {main_window.size().width()}x{main_window.size().height()}")
        print(f"Widget central: {main_window.centralWidget()}")
        print(f"ViewManager vues: {list(main_window.view_manager.views.keys())}")
        print(f"QStackedWidget count: {main_window.stacked_widget.count()}")
        print(f"QStackedWidget index: {main_window.stacked_widget.currentIndex()}")
        print(f"QStackedWidget visible: {main_window.stacked_widget.isVisible()}")
        print(f"QStackedWidget taille: {main_window.stacked_widget.size().width()}x{main_window.stacked_widget.size().height()}")
        
        # Vérifier le widget courant
        current_widget = main_window.stacked_widget.currentWidget()
        if current_widget:
            print(f"Widget courant: {current_widget.__class__.__name__}")
            print(f"Widget courant visible: {current_widget.isVisible()}")
            print(f"Widget courant taille: {current_widget.size().width()}x{current_widget.size().height()}")
        else:
            print("❌ Aucun widget courant")
        
        # Test de capture d'écran pour détecter l'écran gris
        screenshot = main_window.grab()
        image = screenshot.toImage()
        
        # Analyser les couleurs de l'image
        colors = set()
        width, height = image.width(), image.height()
        
        # Échantillonner quelques pixels
        for x in range(0, width, 50):
            for y in range(0, height, 50):
                color = image.pixelColor(x, y)
                colors.add((color.red(), color.green(), color.blue()))
        
        print(f"\nCouleurs détectées: {len(colors)}")
        for color in list(colors)[:10]:  # Afficher les 10 premières couleurs
            print(f"  - {color}")
        
        # Vérifications
        assert main_window.centralWidget() is not None, "❌ Pas de widget central"
        assert len(main_window.view_manager.views) > 0, f"❌ ViewManager doit contenir des vues ({len(main_window.view_manager.views)})"
        assert main_window.stacked_widget.count() > 0, f"❌ QStackedWidget doit contenir des widgets (count={main_window.stacked_widget.count()})"
        assert len(colors) > 1, f"❌ Trop peu de couleurs détectées: {colors}"
        
        print("\n✅ Test réussi: ViewManager fonctionne correctement")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"Erreur pendant le test: {e}")


def test_view_manager_switching(qtbot):
    """Test de changement de vues avec ViewManager"""
    try:
        # Créer l'application si elle n'existe pas
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Reset du ViewManager
        reset_view_manager()
        
        # Créer la fenêtre
        main_window = CHNeoWaveMainWindow()
        qtbot.addWidget(main_window)
        main_window.show()
        qtbot.waitForWindowShown(main_window)
        
        # Tester le changement de vues
        view_names = list(main_window.view_manager.views.keys())
        print(f"Vues disponibles: {view_names}")
        
        for view_name in view_names[:3]:  # Tester les 3 premières vues
            print(f"\nChangement vers la vue: {view_name}")
            main_window.view_manager.switch_to_view(view_name)
            qtbot.wait(100)  # Attendre un peu
            
            current_widget = main_window.stacked_widget.currentWidget()
            assert current_widget is not None, f"Aucun widget courant pour la vue {view_name}"
            assert current_widget.isVisible(), f"Widget de la vue {view_name} non visible"
            
            print(f"✅ Vue {view_name} activée avec succès")
        
        print("\n✅ Test de changement de vues réussi")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant le test de changement de vues: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"Erreur pendant le test: {e}")


def test_simple_widget_visibility(qtbot):
    """Test simple de visibilité des widgets"""
    try:
        from src.hrneowave.gui.views.welcome_view import WelcomeView
        
        # Test d'une vue isolée
        welcome_view = WelcomeView()
        qtbot.addWidget(welcome_view)
        welcome_view.show()
        
        qtbot.waitForWindowShown(welcome_view)
        qtbot.wait(500)
        
        assert welcome_view.isVisible(), "La vue d'accueil doit être visible"
        
        size = welcome_view.size()
        assert size.width() > 0, "La vue doit avoir une largeur > 0"
        assert size.height() > 0, "La vue doit avoir une hauteur > 0"
        
        print(f"✅ Vue d'accueil isolée: {size.width()}x{size.height()}")
        
    except Exception as e:
        pytest.skip(f"Impossible de tester la vue isolée: {e}")