#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Imports Diagnostic - Phase 4
Diagnostic détaillé des imports CHNeoWave
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports_step_by_step():
    """Test des imports un par un"""
    print("🔍 PHASE 4: Diagnostic Imports CHNeoWave")
    print("=" * 50)
    
    imports_success = True
    
    # Test 1: PySide6
    print("\n📋 TEST 1: PySide6")
    print("-" * 20)
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
        from PySide6.QtCore import Qt, Signal, QTimer
        from PySide6.QtGui import QFont
        print("✅ PySide6 import OK")
    except Exception as e:
        print(f"❌ PySide6 import FAILED: {e}")
        imports_success = False
    
    # Test 2: MainWindow
    print("\n📋 TEST 2: MainWindow")
    print("-" * 20)
    try:
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow import OK")
    except Exception as e:
        print(f"❌ MainWindow import FAILED: {e}")
        imports_success = False
    
    # Test 3: ViewManager
    print("\n📋 TEST 3: ViewManager")
    print("-" * 20)
    try:
        from hrneowave.gui.view_manager import ViewManager
        print("✅ ViewManager import OK")
    except Exception as e:
        print(f"❌ ViewManager import FAILED: {e}")
        imports_success = False
    
    # Test 4: ThemeManager
    print("\n📋 TEST 4: ThemeManager")
    print("-" * 20)
    try:
        from hrneowave.gui.styles.theme_manager import ThemeManager
        print("✅ ThemeManager import OK")
    except Exception as e:
        print(f"❌ ThemeManager import FAILED: {e}")
        imports_success = False
    
    # Test 5: Vues principales
    print("\n📋 TEST 5: Vues Principales")
    print("-" * 20)
    try:
        from hrneowave.gui.views import WelcomeView, DashboardViewMaritime
        print("✅ Vues principales import OK")
    except Exception as e:
        print(f"❌ Vues principales import FAILED: {e}")
        imports_success = False
    
    # Test 6: Composants UI
    print("\n📋 TEST 6: Composants UI")
    print("-" * 20)
    try:
        from hrneowave.gui.widgets.main_sidebar import MainSidebar
        print("✅ MainSidebar import OK")
    except Exception as e:
        print(f"❌ MainSidebar import FAILED: {e}")
        imports_success = False
    
    try:
        from hrneowave.gui.components.breadcrumbs import BreadcrumbsWidget
        print("✅ BreadcrumbsWidget import OK")
    except Exception as e:
        print(f"❌ BreadcrumbsWidget import FAILED: {e}")
        imports_success = False
    
    # Test 7: Système d'animations
    print("\n📋 TEST 7: Système d'Animations")
    print("-" * 20)
    try:
        from hrneowave.gui.animations import PageTransitionManager, MaritimeAnimator
        print("✅ Animations import OK")
    except Exception as e:
        print(f"⚠️ Animations import FAILED (attendu): {e}")
        # Ce n'est pas critique
    
    # Test 8: Core modules
    print("\n📋 TEST 8: Modules Core")
    print("-" * 20)
    try:
        from hrneowave.core.signal_bus import get_error_bus
        print("✅ Signal bus import OK")
    except Exception as e:
        print(f"❌ Signal bus import FAILED: {e}")
        imports_success = False
    
    # Test 9: Préférences
    print("\n📋 TEST 9: Préférences")
    print("-" * 20)
    try:
        from hrneowave.gui.preferences import get_user_preferences
        print("✅ Préférences import OK")
    except Exception as e:
        print(f"❌ Préférences import FAILED: {e}")
        imports_success = False
    
    # Résumé
    print("\n" + "=" * 50)
    if imports_success:
        print("🎯 RÉSULTAT: Tous les imports critiques réussis")
        print("✅ Le problème n'est PAS dans les imports")
    else:
        print("❌ RÉSULTAT: Certains imports ont échoué")
        print("❌ Le problème pourrait venir des dépendances manquantes")
    
    return imports_success

def test_qt_environment():
    """Test de l'environnement Qt"""
    print("\n🔍 DIAGNOSTIC ENVIRONNEMENT QT")
    print("=" * 40)
    
    # Variables d'environnement
    print("📋 Variables d'environnement:")
    env_vars = ['QT_QPA_PLATFORM', 'DISPLAY', 'QT_SCALE_FACTOR', 'QT_AUTO_SCREEN_SCALE_FACTOR']
    for var in env_vars:
        value = os.getenv(var, 'Non défini')
        print(f"   {var}: {value}")
    
    # Test QApplication
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        print(f"\n📋 Informations QApplication:")
        print(f"   Plateforme: {app.platformName()}")
        print(f"   Nombre d'écrans: {len(app.screens())}")
        
        for i, screen in enumerate(app.screens()):
            print(f"   Écran {i}: {screen.geometry()} - DPI: {screen.logicalDotsPerInch()}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test QApplication: {e}")

if __name__ == "__main__":
    success = test_imports_step_by_step()
    test_qt_environment()
    
    if success:
        print("\n🎯 CONCLUSION: Imports OK - Problème ailleurs")
        sys.exit(0)
    else:
        print("\n❌ CONCLUSION: Problème dans les imports")
        sys.exit(1)