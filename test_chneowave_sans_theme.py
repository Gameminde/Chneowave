#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test CHNeoWave Sans Thème - Phase 3 Diagnostic
Test de l'application CHNeoWave sans ThemeManager
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

def test_chneowave_sans_theme():
    """Test CHNeoWave sans ThemeManager"""
    print("🔍 PHASE 3: Test CHNeoWave Sans Thème")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave Sans Thème")
    app.setApplicationVersion("1.1.0")
    
    print("✅ QApplication créée")
    
    # IMPORTANT: NE PAS APPLIQUER DE THÈME
    print("⚠️ THÈME DÉSACTIVÉ pour ce test")
    
    try:
        # Import de MainWindow
        print("🔄 Import MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importée avec succès")
        
        # Création de MainWindow
        print("🔄 Création MainWindow...")
        window = MainWindow()
        print("✅ MainWindow créée avec succès")
        
        # Configuration basique
        window.setWindowTitle("CHNeoWave - Test Sans Thème")
        window.resize(1000, 700)
        
        # FORCER AFFICHAGE
        print("🔄 Affichage de la fenêtre...")
        window.show()
        window.raise_()
        window.activateWindow()
        
        print("✅ Commandes d'affichage exécutées")
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ État fenêtre: {window.windowState()}")
        
        # Vérifications détaillées
        if window.isVisible():
            print("🎯 SUCCESS: Interface CHNeoWave visible SANS thème")
            print("✅ Le problème vient probablement du ThemeManager")
        else:
            print("❌ PROBLEM: Interface CHNeoWave invisible même SANS thème")
            print("❌ Le problème est plus profond que le ThemeManager")
            
        # Vérifier les composants internes
        if hasattr(window, 'view_manager'):
            print(f"✅ ViewManager: {window.view_manager}")
            if hasattr(window.view_manager, 'current_view'):
                print(f"✅ Vue actuelle: {window.view_manager.current_view}")
        
        if hasattr(window, 'stack_widget'):
            print(f"✅ StackWidget: {window.stack_widget}")
            print(f"✅ Nombre de vues: {window.stack_widget.count()}")
            print(f"✅ Vue actuelle index: {window.stack_widget.currentIndex()}")
            
        print("⏰ Fermeture automatique dans 10 secondes...")
        
        # Timer pour fermeture automatique
        from PySide6.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(10000)  # 10 secondes
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ ERREUR lors du test: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_chneowave_sans_theme()
    print(f"Code de sortie: {exit_code}")
    sys.exit(exit_code)