#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface en ligne de commande pour CHNeoWave
"""



# Import conditionnel des modules Qt
def _ensure_qt_imports():
    """Assure que les modules Qt sont importés correctement"""
    global QApplication, Qt
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        return True
    except ImportError:
        try:
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtCore import Qt
            return True
        except ImportError:
            return False

def run_gui():
    """
    Lance l'interface graphique CHNeoWave
    """
    import sys
    import os
    import logging
    logger = logging.getLogger(__name__)
    logger.info("run_gui() started")
    
    # Ajouter le répertoire parent au path pour les imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    try:
        # Assurer les imports Qt
        if not _ensure_qt_imports():
            logger.critical("Aucune bibliothèque Qt trouvée (PyQt5, PyQt6, ou PySide6)")
            sys.exit(1)
            
        # Configuration de l'application Qt
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        app = QApplication(sys.argv)
        app.setApplicationName("CHNeoWave")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Laboratoire Maritime")
        
        # Gestionnaire de thèmes
        from hrneowave.gui.styles.theme_manager import ThemeManager
        theme_manager = ThemeManager(app)
        theme_manager.apply_theme('light')

        # Import et lancement de la fenêtre principale
        from hrneowave.gui.main_window import MainWindow
        
        logger.info("Creating MainWindow...")
        window = MainWindow()
        logger.info("Showing MainWindow...")
        window.show()
        
        # Démarrage de la boucle d'événements
        logger.info("Starting event loop...")
        exit_code = app.exec_()
        logger.info(f"Event loop finished with exit code {exit_code}")
        sys.exit(exit_code)
        
    except ImportError as e:
        logger.critical(f"Erreur d'import: {e}", exc_info=True)
        
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Erreur lors du lancement: {e}", exc_info=True)
        sys.exit(1)

def run_cli():
    """
    Point d'entrée principal de l'interface en ligne de commande
    """


    import argparse
    import logging

    # Configuration initiale pour capturer les erreurs de démarrage
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='chneowave_debug.log',
            filemode='w'
        )
        logger = logging.getLogger(__name__)
        logger.info("run_cli() started and logging configured.")
    except Exception as e:
        print(f"CRITICAL: Failed to configure logging: {e}")
        # Pas de sys.exit ici, car sys n'est pas encore importé

    parser = argparse.ArgumentParser(
        description="CHNeoWave - Logiciel d'acquisition et d'analyse de données maritimes",
        prog="chneowave"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="CHNeoWave 1.0.0"
    )
    
    parser.add_argument(
        "--gui", 
        action="store_true", 
        default=False,
        help="Lance l'interface graphique"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Active le mode debug"
    )
    
    args = parser.parse_args()

    # La configuration du logging est maintenant faite au début de la fonction.
    if args.debug:
        logger.info("Mode debug activé")
    else:
        # Si le mode debug n'est pas activé, on remet le niveau à INFO
        logging.getLogger().setLevel(logging.INFO)

    if args.gui:
        logger.info("--gui flag is set, calling run_gui()")
        run_gui()
    else:
        logger.info("Aucun argument spécifié, fin du programme.")
        # Comportement par défaut si --gui n'est pas spécifié
        # Peut être étendu pour d'autres commandes CLI
        pass

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="CHNeoWave - Logiciel d'acquisition et d'analyse de données maritimes",
        prog="chneowave"
    )
    
    parser.add_argument(
        "--gui", 
        action="store_true", 
        default=False,
        help="Lance l'interface graphique"
    )
    
    args = parser.parse_args()

    if args.gui:
        # Assurer les imports Qt
        if not _ensure_qt_imports():
            print("CRITICAL: Aucune bibliothèque Qt trouvée (PyQt5, PyQt6, ou PySide6)")
            sys.exit(1)
            
        # Configuration de l'application Qt
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        app = QApplication(sys.argv)
        app.setApplicationName("CHNeoWave")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Laboratoire Maritime")
        
        # Import et lancement de la fenêtre principale
        from hrneowave.gui.main_window import MainWindow
        
        window = MainWindow()
        window.show()
        
        # Démarrage de la boucle d'événements
        sys.exit(app.exec_())
    else:
        run_cli()