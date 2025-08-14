#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour forcer l'affichage de MainWindow
CHNeoWave - Force Display Test
"""

import sys
import logging
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer

def test_mainwindow_force_display():
    """Test pour forcer l'affichage de MainWindow"""
    
    # Configuration logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger('chneowave')
    logger.info("Test MainWindow Force Display - Système de logging configuré")
    
    app = QApplication(sys.argv)
    
    # Test 1: Appliquer le thème
    try:
        from hrneowave.gui.styles.theme_manager import ThemeManager
        theme_manager = ThemeManager(app)
        theme_manager.apply_theme('maritime_modern')
        logger.info("✅ Thème appliqué avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur thème: {e}")
        return 1
    
    # Test 2: Créer MainWindow
    try:
        logger.info("🧪 Création MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        
        window = MainWindow()
        logger.info("✅ MainWindow créée")
        
        # FORCER L'AFFICHAGE EXPLICITEMENT
        window.show()
        window.raise_()
        window.activateWindow()
        window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        
        logger.info(f"✅ Géométrie : {window.geometry()}")
        logger.info(f"✅ Visible : {window.isVisible()}")
        logger.info(f"✅ État fenêtre : {window.windowState()}")
        
        # Vérifier que la fenêtre est bien affichée
        if window.isVisible():
            logger.info("🎉 MainWindow est VISIBLE!")
        else:
            logger.error("❌ MainWindow n'est PAS visible!")
            return 1
        
        # Timer pour garder la fenêtre ouverte 10 secondes
        timer = QTimer()
        timer.timeout.connect(lambda: (
            logger.info("⏰ Timer déclenché - fermeture de l'application"),
            app.quit()
        ))
        timer.start(10000)  # 10 secondes
        
        logger.info("🚀 Démarrage de la boucle d'événements Qt (10 secondes)")
        logger.info("👀 Vérifiez que la fenêtre CHNeoWave est visible à l'écran!")
        
        # Démarrer la boucle d'événements
        exit_code = app.exec()
        logger.info(f"✅ Application fermée avec code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.error(f"❌ Erreur MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("🧪 Test MainWindow Force Display")
    print("=" * 50)
    print("👀 Ce test va afficher CHNeoWave pendant 10 secondes")
    print("🔍 Vérifiez visuellement que la fenêtre apparaît!")
    print("=" * 50)
    
    try:
        exit_code = test_mainwindow_force_display()
        print(f"\n✅ Test terminé avec code: {exit_code}")
        
        if exit_code == 0:
            print("🎉 MainWindow s'est affichée correctement!")
            print("✅ PROBLÈME D'AFFICHAGE RÉSOLU!")
        else:
            print("❌ Problème d'affichage persistant")
            
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)