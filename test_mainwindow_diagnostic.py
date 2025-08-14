#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic ciblé MainWindow - Identification du problème exact
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_mainwindow_creation():
    """Test de création MainWindow avec diagnostic détaillé"""
    print("=== DIAGNOSTIC MAINWINDOW CRÉATION ===")
    
    try:
        # Import PySide6
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        print("✅ QApplication prête")
        
        # Configuration logging
        from hrneowave.core.logging_config import setup_logging
        setup_logging()
        print("✅ Logging configuré")
        
        # Test avec thème maritime_modern (valide)
        print("\n--- Test avec thème maritime_modern ---")
        try:
            from hrneowave.gui.styles.theme_manager import ThemeManager
            theme_manager = ThemeManager(app)
            theme_manager.apply_theme('maritime_modern')  # Thème valide
            print("✅ Thème maritime_modern appliqué")
        except Exception as e:
            print(f"❌ Erreur thème: {e}")
        
        # Import MainWindow
        print("\n--- Import MainWindow ---")
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importé")
        
        # Création MainWindow avec gestion d'erreurs détaillée
        print("\n--- Création MainWindow ---")
        try:
            print("Appel constructeur MainWindow()...")
            main_window = MainWindow()
            print("✅ Constructeur MainWindow terminé")
            
            print("Configuration fenêtre...")
            main_window.setWindowTitle("CHNeoWave - Diagnostic")
            main_window.setGeometry(100, 100, 1000, 700)
            print("✅ Configuration terminée")
            
            print("Affichage fenêtre...")
            main_window.show()
            main_window.raise_()
            main_window.activateWindow()
            print("✅ Affichage demandé")
            
            # Vérifications
            print(f"\nVérifications:")
            print(f"  - Visible: {main_window.isVisible()}")
            print(f"  - Taille: {main_window.size()}")
            print(f"  - Position: {main_window.pos()}")
            
            if main_window.isVisible():
                print("\n🎉 SUCCÈS! MainWindow créé et visible")
                
                # Afficher pendant 5 secondes
                timer = QTimer()
                timer.timeout.connect(app.quit)
                timer.start(5000)
                
                print("Interface affichée pendant 5 secondes...")
                exit_code = app.exec()
                print(f"Application fermée avec code: {exit_code}")
                return True
            else:
                print("\n❌ MainWindow créé mais pas visible")
                return False
                
        except Exception as e:
            print(f"❌ Erreur création MainWindow: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("DIAGNOSTIC MAINWINDOW - VERSION CIBLÉE")
    print("======================================")
    
    success = test_mainwindow_creation()
    
    if success:
        print("\n✅ DIAGNOSTIC RÉUSSI - MainWindow fonctionne")
        return 0
    else:
        print("\n❌ DIAGNOSTIC ÉCHOUÉ - Problème avec MainWindow")
        return 1

if __name__ == "__main__":
    sys.exit(main())