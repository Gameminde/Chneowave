#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test minimal de MainWindow pour identifier le problème CSS
CHNeoWave - Diagnostic MainWindow
"""

import sys
import logging
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

def test_minimal_mainwindow():
    """Test minimal reproduisant la structure MainWindow"""
    
    # Configuration logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger('chneowave')
    logger.info("Test MainWindow minimal - Système de logging configuré")
    
    app = QApplication(sys.argv)
    
    # Test 1: Importer ThemeManager
    try:
        from hrneowave.gui.styles.theme_manager import ThemeManager
        logger.info("✅ ThemeManager importé avec succès")
        
        # Test 2: Créer ThemeManager avec app
        theme_manager = ThemeManager(app)
        logger.info("✅ ThemeManager créé avec succès")
        
        # Test 3: Appliquer le thème
        theme_manager.apply_theme('maritime_modern')
        logger.info("✅ Thème maritime_modern appliqué")
        
    except Exception as e:
        logger.error(f"❌ Erreur ThemeManager: {e}")
        return 1
    
    # Test 4: Créer MainWindow basique
    try:
        window = QMainWindow()
        window.setWindowTitle("CHNeoWave - Test Minimal")
        window.setMinimumSize(1200, 800)
        logger.info("✅ MainWindow créée")
        
        # Test 5: Créer widget central simple
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Test 6: Ajouter QLabel simple
        test_label = QLabel("Test MainWindow Minimal")
        test_label.setAlignment(Qt.AlignCenter)
        test_label.setStyleSheet("color: #1565C0; font-size: 24px; padding: 20px;")
        layout.addWidget(test_label)
        
        window.setCentralWidget(central_widget)
        logger.info("✅ Widget central configuré")
        
    except Exception as e:
        logger.error(f"❌ Erreur création MainWindow: {e}")
        return 1
    
    # Test 7: Afficher la fenêtre
    try:
        window.show()
        window.raise_()
        window.activateWindow()
        
        logger.info("✅ MainWindow affichée")
        logger.info(f"✅ Géométrie : {window.geometry()}")
        logger.info(f"✅ Visible : {window.isVisible()}")
        
    except Exception as e:
        logger.error(f"❌ Erreur affichage: {e}")
        return 1
    
    # Test 8: Fermer automatiquement après 3 secondes
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(3000)
    
    logger.info("🚀 Démarrage de la boucle d'événements Qt")
    
    try:
        exit_code = app.exec()
        logger.info(f"✅ Application fermée avec code: {exit_code}")
        return exit_code
    except Exception as e:
        logger.error(f"❌ Erreur dans la boucle d'événements: {e}")
        return 1

if __name__ == "__main__":
    print("🧪 Test MainWindow Minimal")
    print("=" * 50)
    
    try:
        exit_code = test_minimal_mainwindow()
        print(f"\n✅ Test terminé avec code: {exit_code}")
        
        if exit_code == 0:
            print("🎉 MainWindow fonctionne correctement!")
        else:
            print("❌ Problème détecté dans MainWindow")
            
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        sys.exit(1)