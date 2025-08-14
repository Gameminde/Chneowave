#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Point d'entrée principal CORRIGÉ
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
    
    # CORRECTION CRITIQUE : Empêcher la fermeture automatique
    app.setQuitOnLastWindowClosed(True)  # S'assurer que l'app se ferme quand la fenêtre se ferme

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
        
        # CORRECTION CRITIQUE : Forcer l'affichage AVANT la boucle d'événements
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        # CORRECTION : Forcer l'état actif
        main_window.setWindowState(main_window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        
        # S'assurer que la fenêtre est visible
        if not main_window.isVisible():
            log.warning("La fenêtre n'est pas visible, tentative de maximisation...")
            main_window.showMaximized()
        
        log.info(f"✅ Fenêtre visible: {main_window.isVisible()}")
        log.info(f"✅ Taille: {main_window.size()}")
        log.info(f"✅ Position: {main_window.pos()}")
        log.info(f"✅ État actif: {main_window.isActiveWindow()}")
        log.info(f"✅ Minimisée: {main_window.isMinimized()}")
        
        # CORRECTION CRITIQUE : Vérification finale
        if main_window.isVisible():
            log.info("🎉 SUCCÈS : MainWindow est VISIBLE à l'écran!")
        else:
            log.error("❌ ÉCHEC : MainWindow n'est PAS visible!")
            return 1
        
        log.info("🚀 Démarrage de la boucle d'événements de l'application.")
        log.info("👀 CHNeoWave devrait maintenant être visible à l'écran!")
        
        # CORRECTION : Démarrer la boucle d'événements
        exit_code = app.exec()
        log.info(f"✅ Application terminée avec le code de sortie: {exit_code}")
        return exit_code
        
    except Exception as e:
        log.critical(f"❌ Une erreur critique a empêché le lancement de l'application: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    print("🚀 Lancement de CHNeoWave - Version Corrigée")
    print("=" * 50)
    print("👀 L'interface devrait s'afficher dans quelques secondes...")
    print("=" * 50)
    
    exit_code = main()
    
    if exit_code == 0:
        print("\n✅ CHNeoWave s'est fermé normalement")
    else:
        print(f"\n❌ CHNeoWave s'est fermé avec une erreur (code: {exit_code})")
    
    sys.exit(exit_code)