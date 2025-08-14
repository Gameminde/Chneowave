#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour identifier le QLabel qui cause l'erreur CSS
CHNeoWave - Diagnostic CSS Error
"""

import sys
import logging
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

def test_css_error_debug():
    """Test pour identifier la source de l'erreur CSS"""
    
    # Configuration logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger('chneowave')
    logger.info("Test CSS Error Debug - Système de logging configuré")
    
    app = QApplication(sys.argv)
    
    # Test 1: Importer et appliquer le thème
    try:
        from hrneowave.gui.styles.theme_manager import ThemeManager
        theme_manager = ThemeManager(app)
        theme_manager.apply_theme('maritime_modern')
        logger.info("✅ Thème appliqué avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur thème: {e}")
        return 1
    
    # Test 2: Importer les composants un par un
    components_to_test = [
        ('MainSidebar', 'hrneowave.gui.widgets.main_sidebar'),
        ('BreadcrumbsWidget', 'hrneowave.gui.components.breadcrumbs'),
        ('SystemStatusWidget', 'hrneowave.gui.components.status_indicators'),
        ('HelpPanel', 'hrneowave.gui.components.help_system'),
        ('WelcomeView', 'hrneowave.gui.views'),
        ('DashboardViewMaritime', 'hrneowave.gui.views')
    ]
    
    for component_name, module_name in components_to_test:
        try:
            logger.info(f"🧪 Test import {component_name}...")
            module = __import__(module_name, fromlist=[component_name])
            component_class = getattr(module, component_name)
            
            # Créer une instance du composant
            logger.info(f"🧪 Création instance {component_name}...")
            instance = component_class()
            
            logger.info(f"✅ {component_name} créé avec succès")
            
            # Nettoyer l'instance
            instance.deleteLater()
            
        except Exception as e:
            logger.error(f"❌ Erreur avec {component_name}: {e}")
            logger.error(f"Module: {module_name}")
            import traceback
            traceback.print_exc()
    
    # Test 3: Créer MainWindow étape par étape
    try:
        logger.info("🧪 Test création MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        
        logger.info("🧪 Instanciation MainWindow...")
        window = MainWindow()
        
        logger.info("✅ MainWindow créée avec succès")
        
        # Afficher brièvement
        window.show()
        window.raise_()
        window.activateWindow()
        
        logger.info(f"✅ Géométrie : {window.geometry()}")
        logger.info(f"✅ Visible : {window.isVisible()}")
        
        # Fermer automatiquement après 2 secondes
        from PySide6.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(2000)
        
        exit_code = app.exec()
        logger.info(f"✅ Application fermée avec code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.error(f"❌ Erreur MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("🧪 Test CSS Error Debug")
    print("=" * 50)
    
    try:
        exit_code = test_css_error_debug()
        print(f"\n✅ Test terminé avec code: {exit_code}")
        
        if exit_code == 0:
            print("🎉 Aucune erreur critique détectée!")
        else:
            print("❌ Erreur détectée - voir les logs")
            
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)