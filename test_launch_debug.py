#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic pour le lancement de CHNeoWave
"""

import sys
import traceback
import logging

# Configuration du logging pour capturer toutes les erreurs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug_launch.log')
    ]
)

logger = logging.getLogger(__name__)

def test_imports():
    """Test des imports critiques"""
    logger.info("=== Test des imports ===")
    
    try:
        logger.info("Import PySide6...")
        from PySide6.QtWidgets import QApplication
        logger.info("✓ PySide6.QtWidgets OK")
        
        from PySide6.QtCore import Qt, QObject, Signal
        logger.info("✓ PySide6.QtCore OK")
        
        logger.info("Import hrneowave.core.logging_config...")
        from hrneowave.core.logging_config import setup_logging
        logger.info("✓ hrneowave.core.logging_config OK")
        
        logger.info("Import hrneowave.gui.main_window...")
        from hrneowave.gui.main_window import MainWindow
        logger.info("✓ hrneowave.gui.main_window OK")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur d'import: {e}")
        logger.error(traceback.format_exc())
        return False

def test_app_creation():
    """Test de création de l'application Qt"""
    logger.info("=== Test création QApplication ===")
    
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("CHNeoWave")
        app.setApplicationVersion("1.1.0")
        logger.info("✓ QApplication créée avec succès")
        return app
        
    except Exception as e:
        logger.error(f"Erreur création QApplication: {e}")
        logger.error(traceback.format_exc())
        return None

def test_main_window_creation(app):
    """Test de création de la fenêtre principale"""
    logger.info("=== Test création MainWindow ===")
    
    try:
        from hrneowave.gui.main_window import MainWindow
        main_window = MainWindow()
        logger.info("✓ MainWindow créée avec succès")
        
        main_window.show()
        logger.info("✓ MainWindow affichée")
        
        return main_window
        
    except Exception as e:
        logger.error(f"Erreur création MainWindow: {e}")
        logger.error(traceback.format_exc())
        return None

def main():
    """Fonction principale de diagnostic"""
    logger.info("=== DÉBUT DIAGNOSTIC CHNeoWave ===")
    
    # Test des imports
    if not test_imports():
        logger.error("Échec des imports - arrêt du diagnostic")
        return 1
    
    # Test création application
    app = test_app_creation()
    if app is None:
        logger.error("Échec création QApplication - arrêt du diagnostic")
        return 1
    
    # Test création fenêtre principale
    main_window = test_main_window_creation(app)
    if main_window is None:
        logger.error("Échec création MainWindow - arrêt du diagnostic")
        return 1
    
    logger.info("=== DIAGNOSTIC RÉUSSI ===")
    logger.info("Lancement de l'application...")
    
    try:
        exit_code = app.exec()
        logger.info(f"Application terminée avec code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.critical(f"Erreur critique: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)