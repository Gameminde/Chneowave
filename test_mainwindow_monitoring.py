#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow Monitoring - Phase 6
Monitoring détaillé de la construction MainWindow
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

def test_mainwindow_construction_detaillee():
    """Test détaillé de la construction MainWindow"""
    print("🔍 PHASE 6: Monitoring Détaillé MainWindow")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave Monitoring")
    
    print("✅ QApplication créée")
    
    try:
        print("\n🔄 ÉTAPE 1: Import MainWindow")
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importée")
        
        print("\n🔄 ÉTAPE 2: Création instance MainWindow")
        window = MainWindow()
        print("✅ MainWindow instance créée")
        
        print("\n🔄 ÉTAPE 3: Configuration fenêtre")
        window.setWindowTitle("CHNeoWave - Monitoring Test")
        window.resize(1200, 800)
        print("✅ Configuration fenêtre terminée")
        
        print("\n🔄 ÉTAPE 4: Vérifications avant affichage")
        print(f"   📊 Taille: {window.size()}")
        print(f"   📊 Position: {window.pos()}")
        print(f"   📊 Visible: {window.isVisible()}")
        print(f"   📊 Minimisé: {window.isMinimized()}")
        print(f"   📊 Maximisé: {window.isMaximized()}")
        print(f"   📊 État: {window.windowState()}")
        
        # Vérifier les composants internes
        print("\n🔄 ÉTAPE 5: Vérification composants internes")
        if hasattr(window, 'view_manager'):
            print(f"   ✅ ViewManager: {type(window.view_manager).__name__}")
            if hasattr(window.view_manager, 'stack_widget'):
                stack = window.view_manager.stack_widget
                print(f"   ✅ StackWidget: {type(stack).__name__}")
                print(f"   ✅ Nombre de vues: {stack.count()}")
                print(f"   ✅ Index actuel: {stack.currentIndex()}")
                
                # Lister les vues
                for i in range(stack.count()):
                    widget = stack.widget(i)
                    print(f"   📋 Vue {i}: {type(widget).__name__}")
        
        if hasattr(window, 'sidebar'):
            print(f"   ✅ Sidebar: {type(window.sidebar).__name__}")
            
        if hasattr(window, 'breadcrumbs'):
            print(f"   ✅ Breadcrumbs: {type(window.breadcrumbs).__name__}")
        
        print("\n🔄 ÉTAPE 6: Tentative d'affichage")
        print("   🔄 Appel window.show()...")
        window.show()
        print("   ✅ window.show() exécuté")
        
        print("   🔄 Appel window.raise_()...")
        window.raise_()
        print("   ✅ window.raise_() exécuté")
        
        print("   🔄 Appel window.activateWindow()...")
        window.activateWindow()
        print("   ✅ window.activateWindow() exécuté")
        
        # Forcer le traitement des événements
        print("   🔄 Traitement des événements Qt...")
        app.processEvents()
        print("   ✅ Événements Qt traités")
        
        print("\n🔄 ÉTAPE 7: Vérifications après affichage")
        print(f"   📊 Visible: {window.isVisible()}")
        print(f"   📊 Actif: {window.isActiveWindow()}")
        print(f"   📊 Géométrie: {window.geometry()}")
        print(f"   📊 Taille frame: {window.frameGeometry()}")
        print(f"   📊 Widget central: {window.centralWidget()}")
        
        # Test de visibilité du widget central
        if window.centralWidget():
            central = window.centralWidget()
            print(f"   📊 Widget central visible: {central.isVisible()}")
            print(f"   📊 Widget central taille: {central.size()}")
        
        # Diagnostic final
        print("\n" + "=" * 50)
        if window.isVisible():
            print("🎯 SUCCESS: MainWindow est VISIBLE")
            print("✅ L'interface devrait apparaître à l'écran")
            
            # Test de capture d'écran pour vérifier
            try:
                pixmap = window.grab()
                if not pixmap.isNull():
                    print("✅ Capture d'écran réussie - Interface rendue")
                else:
                    print("⚠️ Capture d'écran vide - Problème de rendu")
            except Exception as e:
                print(f"⚠️ Erreur capture d'écran: {e}")
                
        else:
            print("❌ PROBLEM: MainWindow est INVISIBLE")
            print("❌ Problème critique dans l'affichage")
        
        # Maintenir la fenêtre ouverte
        print("\n⏰ Maintien de la fenêtre pendant 15 secondes...")
        print("   (Vérifiez si une fenêtre CHNeoWave apparaît à l'écran)")
        
        # Timer pour fermeture
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(15000)  # 15 secondes
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_mainwindow_construction_detaillee()
    print(f"\nCode de sortie: {exit_code}")
    sys.exit(exit_code)