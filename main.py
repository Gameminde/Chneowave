#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Point d'entrée principal
Logiciel d'acquisition et d'analyse de houle pour laboratoires maritimes

Version 1.0.0 - Interface refactorisée avec flux séquentiel
Flux : Accueil -> Calibration -> Acquisition -> Analyse
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Configuration du logging AVANT tout import GUI
from hrneowave.utils import setup_logging
setup_logging()

# --- Importations Centralisées PySide6 ---
# Importer tous les composants Qt nécessaires ici pour garantir qu'une seule version
# de chaque classe est chargée dans toute l'application.

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget
)
from PySide6.QtCore import Qt, QObject, Signal

# --- Fin des Importations Centralisées ---



from hrneowave.gui.view_manager import ViewManager
from hrneowave.gui.controllers.main_controller import MainController
from hrneowave.gui.theme import get_stylesheet
from hrneowave.gui.views.dashboard_view import DashboardView
from hrneowave.gui.views.calibration_view import CalibrationView
from hrneowave.gui.views.acquisition_view import AcquisitionView
from hrneowave.gui.views.analysis_view import AnalysisView
from hrneowave.gui.views.export_view import ExportView

class CHNeoWaveMainWindow(QMainWindow):
    """
    Fenêtre principale CHNeoWave avec nouveau flux séquentiel
    """
    
    def __init__(self):
        super().__init__()
        print("==> CHNeoWaveMainWindow.__init__() START")
        self.setWindowTitle("CHNeoWave v1.0.0 - Laboratoire Maritime")
        self.setMinimumSize(1200, 800)
        self.resize(1366, 768)  # Optimisé pour 1366x768
        
        # Application du thème professionnel
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
        
        # Création du ViewManager avec le QStackedWidget
        self.view_manager = ViewManager(self.stacked_widget)
        
        # Enregistrement des vues
        self.setup_views()

        # Afficher la vue initiale
        self.view_manager.change_view("dashboard")
        
        # Création du MainController avec le ViewManager et une config par défaut
        default_config = {
            'log_level': 'INFO',
            'theme': 'dark'
        }
        self.main_controller = MainController(self, self.view_manager, default_config)
        
        # Centrage de la fenêtre
        self._center_window()
        print("==> CHNeoWaveMainWindow.__init__() END")
        
    def setup_views(self):
        """
        Enregistre les vues modernes dans le ViewManager
        Interface unifiée avec workflow complet : Dashboard → Calibration → Acquisition → Analysis → Export
        """
        # Vue dashboard (remplace welcome)
        self.dashboard_view = DashboardView()
        self.view_manager.register_view("dashboard", self.dashboard_view)
        
        # Vue de calibration
        self.calibration_view = CalibrationView()
        self.view_manager.register_view("calibration", self.calibration_view)
        
        # Vue d'acquisition
        self.acquisition_view = AcquisitionView()
        self.view_manager.register_view("acquisition", self.acquisition_view)
        
        # Vue d'analyse
        self.analysis_view = AnalysisView()
        self.view_manager.register_view("analysis", self.analysis_view)
        
        # Vue d'export
        self.export_view = ExportView()
        self.view_manager.register_view("export", self.export_view)
        
        print("[INTERFACE UNIFIÉE] Toutes les vues modernes enregistrées : dashboard, calibration, acquisition, analysis, export")
        print("[NAV] Workflow complet activé : Dashboard → Calibration → Acquisition → Analysis → Export")
    
    def _center_window(self):
        """
        Centre la fenêtre sur l'écran
        """
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

def main():
    """
    Point d'entrée principal de CHNeoWave.
    Lance l'application avec le nouveau flux séquentiel.
    """
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("CHNeoWave")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Laboratoire Maritime")
    
    print("CHNeoWave v1.0.0 - Initialisation...")
    print("Flux séquentiel : Accueil -> Calibration -> Acquisition -> Analyse")
    print("Interface professionnelle pour laboratoire maritime")
    
    try:
        print("==> main(): Avant création CHNeoWaveMainWindow")
        main_window = CHNeoWaveMainWindow()
        print("==> main(): Après création CHNeoWaveMainWindow")

        # Affichage de la fenêtre principale
        print("==> main(): Avant main_window.show()")
        main_window.show()
        print("==> main(): Après main_window.show()")
        
        print(f"Fenêtre visible: {main_window.isVisible()}")
        
        # Lancement de la boucle d'événements
        print("==> main(): Avant app.exec()")
        exit_code = app.exec()
        print(f"==> main(): Après app.exec(), code de sortie: {exit_code}")
        return exit_code
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Erreur non interceptée dans main: {e}")
        import traceback
        traceback.print_exc()