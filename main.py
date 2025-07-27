#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Point d'entrée principal
Logiciel d'acquisition et d'analyse de houle pour laboratoires maritimes

Version 1.0.0 - Interface refactorisée avec flux séquentiel
Flux : Accueil -> Calibration -> Acquisition -> Analyse
"""

import sys
import logging
from pathlib import Path

# Configuration du logging centralisée
# Le setup est maintenant géré via le module de logging de hrneowave
from hrneowave.core.logging_config import setup_logging
setup_logging() # Initialise le logging pour toute l'application

log = logging.getLogger(__name__)

# --- Importations Centralisées PySide6 ---
# Importer tous les composants Qt nécessaires ici pour garantir qu'une seule version
# de chaque classe est chargée dans toute l'application.

from PySide6.QtWidgets import QApplication
from hrneowave.gui.main_window import MainWindow
from PySide6.QtCore import Qt, QObject, Signal

# --- Fin des Importations Centralisées ---



from hrneowave.gui.view_manager import ViewManager
from hrneowave.gui.controllers.main_controller import MainController
from hrneowave.gui.styles.theme_manager import ThemeManager

def main():
    """
    Point d'entrée principal de l'application CHNeoWave.
    Initialise et lance l'interface graphique.
    """
    log.info(f"Lancement de CHNeoWave v1.1.0")
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave")
    app.setApplicationVersion("1.1.0")
    app.setOrganizationName("Laboratoire d'Hydrodynamique Maritime")

    try:
        log.info("Initialisation du gestionnaire de thèmes...")
        theme_manager = ThemeManager(app)
        # Application du nouveau thème maritime moderne par défaut
        theme_manager.apply_theme('maritime_modern')

        log.info("Création de la fenêtre principale...")
        try:
            main_window = MainWindow()
            log.info("MainWindow créée avec succès")
        except Exception as e:
            log.error(f"Erreur lors de la création de MainWindow: {e}", exc_info=True)
            raise
        
        log.info("Affichage de la fenêtre principale.")
        
        # Forcer l'affichage de la fenêtre
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        # S'assurer que la fenêtre est visible
        if not main_window.isVisible():
            log.warning("La fenêtre n'est pas visible, tentative de maximisation...")
            main_window.showMaximized()
        
        log.info(f"Fenêtre visible: {main_window.isVisible()}, Taille: {main_window.size()}")
        log.info(f"Position de la fenêtre: {main_window.pos()}")
        log.info(f"État de la fenêtre: Normal={main_window.isActiveWindow()}, Minimized={main_window.isMinimized()}")
        
        log.info("Démarrage de la boucle d'événements de l'application.")
        exit_code = app.exec()
        log.info(f"Application terminée avec le code de sortie: {exit_code}")
        return exit_code
        
    except Exception as e:
        log.critical(f"Une erreur critique a empêché le lancement de l'application: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())