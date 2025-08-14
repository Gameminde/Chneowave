#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic MainWindow avec log dans fichier
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def log_message(message, log_file):
    """Écrire un message dans le fichier de log et l'afficher"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(full_message + "\n")

def test_mainwindow_with_log():
    """Test MainWindow avec log détaillé"""
    log_file = "mainwindow_diagnostic.log"
    
    # Vider le fichier de log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"=== DIAGNOSTIC MAINWINDOW - {datetime.now()} ===\n")
    
    try:
        log_message("Début du diagnostic MainWindow", log_file)
        
        # Import PySide6
        log_message("Import PySide6...", log_file)
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        log_message("✅ PySide6 importé", log_file)
        
        # Créer QApplication
        log_message("Création QApplication...", log_file)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        log_message("✅ QApplication créée", log_file)
        
        # Configuration logging
        log_message("Configuration logging...", log_file)
        from hrneowave.core.logging_config import setup_logging
        setup_logging()
        log_message("✅ Logging configuré", log_file)
        
        # Import et application thème
        log_message("Import ThemeManager...", log_file)
        from hrneowave.gui.styles.theme_manager import ThemeManager
        log_message("✅ ThemeManager importé", log_file)
        
        log_message("Création ThemeManager...", log_file)
        theme_manager = ThemeManager(app)
        log_message("✅ ThemeManager créé", log_file)
        
        log_message("Application thème maritime_modern...", log_file)
        theme_manager.apply_theme('maritime_modern')
        log_message("✅ Thème appliqué", log_file)
        
        # Import MainWindow
        log_message("Import MainWindow...", log_file)
        from hrneowave.gui.main_window import MainWindow
        log_message("✅ MainWindow importé", log_file)
        
        # Création MainWindow
        log_message("Création MainWindow...", log_file)
        main_window = MainWindow()
        log_message("✅ MainWindow créé", log_file)
        
        # Configuration
        log_message("Configuration MainWindow...", log_file)
        main_window.setWindowTitle("CHNeoWave - Test Diagnostic")
        main_window.setGeometry(100, 100, 1000, 700)
        log_message("✅ MainWindow configuré", log_file)
        
        # Affichage
        log_message("Affichage MainWindow...", log_file)
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        log_message("✅ Affichage demandé", log_file)
        
        # Vérifications
        visible = main_window.isVisible()
        size = main_window.size()
        pos = main_window.pos()
        
        log_message(f"Visible: {visible}", log_file)
        log_message(f"Taille: {size}", log_file)
        log_message(f"Position: {pos}", log_file)
        
        if visible:
            log_message("🎉 SUCCÈS! MainWindow visible", log_file)
            
            # Timer pour fermer après 3 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(3000)
            
            log_message("Interface affichée pendant 3 secondes...", log_file)
            exit_code = app.exec()
            log_message(f"Application fermée avec code: {exit_code}", log_file)
            
            return True
        else:
            log_message("❌ MainWindow créé mais pas visible", log_file)
            return False
            
    except Exception as e:
        log_message(f"❌ ERREUR: {e}", log_file)
        import traceback
        error_details = traceback.format_exc()
        log_message(f"Détails erreur:\n{error_details}", log_file)
        return False

def main():
    """Fonction principale"""
    success = test_mainwindow_with_log()
    
    if success:
        print("\n✅ DIAGNOSTIC RÉUSSI")
        return 0
    else:
        print("\n❌ DIAGNOSTIC ÉCHOUÉ")
        return 1

if __name__ == "__main__":
    sys.exit(main())