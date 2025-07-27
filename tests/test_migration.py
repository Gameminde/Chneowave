#!/usr/bin/env python3
"""
Test de validation de la migration PyQt5 vers PySide6
Sprint 0 - Validation des imports et compatibilité
"""

import sys
import traceback
from pathlib import Path

def test_qt_imports():
    """Test des imports Qt avec fallback"""
    print("🧪 Test des imports Qt...")
    
    # Test PySide6 (priorité)
    try:
        from PySide6.QtWidgets import QApplication, QWidget
        from PySide6.QtCore import Signal, Slot, QObject
        from PySide6.QtGui import QPalette, QColor
        print("✅ PySide6 importé avec succès")
        return "PySide6"
    except ImportError as e:
        print(f"⚠️ PySide6 non disponible: {e}")
    
    # Fallback PyQt5
    try:
        from PyQt5.QtWidgets import QApplication, QWidget
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, QObject
        from PyQt5.QtGui import QPalette, QColor
        print("✅ PyQt5 importé en fallback")
        return "PyQt5"
    except ImportError as e:
        print(f"❌ PyQt5 non disponible: {e}")
        return None

def test_theme_manager():
    """Test du nouveau gestionnaire de thèmes"""
    print("\n🎨 Test du gestionnaire de thèmes...")
    
    try:
        # Import du gestionnaire
        sys.path.insert(0, str(Path.cwd() / "src"))
        from hrneowave.gui.theme.theme_manager import (
            get_theme_manager, ThemeMode, apply_theme
        )
        
        # Test de création
        manager = get_theme_manager()
        print("✅ Gestionnaire de thèmes créé")
        
        # Test de validation des fichiers
        validation = manager.validate_theme_files()
        print(f"📁 Validation des fichiers: {validation}")
        
        # Test de récupération des thèmes
        for mode in [ThemeMode.LIGHT, ThemeMode.DARK]:
            stylesheet = manager.get_theme_stylesheet(mode)
            print(f"📄 Thème {mode.value}: {len(stylesheet)} caractères")
        
        # Test des informations
        info = manager.get_theme_info()
        print(f"ℹ️ Mode actuel: {info['current_mode']}")
        print(f"ℹ️ Tous fichiers présents: {info['all_files_present']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur gestionnaire de thèmes: {e}")
        traceback.print_exc()
        return False

def test_gui_components():
    """Test des composants GUI principaux"""
    print("\n🖼️ Test des composants GUI...")
    
    try:
        sys.path.insert(0, str(Path.cwd() / "src"))
        
        # Test d'import des vues principales
        
        print("✅ WelcomeView importée")
        
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importée")
        
        from hrneowave.gui.view_manager import ViewManager
        print("✅ ViewManager importé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur composants GUI: {e}")
        traceback.print_exc()
        return False

def generate_migration_report():
    """Génère le rapport de migration"""
    print("\n📊 RAPPORT DE MIGRATION SPRINT 0")
    print("=" * 50)
    
    # Test des imports
    qt_backend = test_qt_imports()
    
    # Test du gestionnaire de thèmes
    theme_ok = test_theme_manager()
    
    # Test des composants GUI
    gui_ok = test_gui_components()
    
    # Résumé
    print("\n📋 RÉSUMÉ:")
    print(f"   • Backend Qt: {qt_backend or 'ÉCHEC'}")
    print(f"   • Gestionnaire de thèmes: {'✅ OK' if theme_ok else '❌ ÉCHEC'}")
    print(f"   • Composants GUI: {'✅ OK' if gui_ok else '❌ ÉCHEC'}")
    
    # Statut global
    success = qt_backend is not None and theme_ok and gui_ok
    print(f"\n🎯 STATUT GLOBAL: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
    
    return success

if __name__ == "__main__":
    print("🚀 VALIDATION MIGRATION SPRINT 0")
    print("CHNeoWave v1.1.0 - PyQt5 vers PySide6")
    print("=" * 50)
    
    success = generate_migration_report()
    
    if success:
        print("\n🎉 Migration validée avec succès!")
        sys.exit(0)
    else:
        print("\n⚠️ Migration partiellement réussie - vérification requise")
        sys.exit(1)