#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide des corrections CHNeoWave
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_qt_imports():
    """Test des imports Qt"""
    print("🧪 TEST 1: Imports Qt")
    print("-" * 30)
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
        from PySide6.QtCore import Qt, QTimer
        print("✅ Imports Qt réussis")
        return True
    except Exception as e:
        print(f"❌ Erreur imports Qt: {e}")
        return False

def test_theme_manager():
    """Test du ThemeManager corrigé"""
    print("\n🧪 TEST 2: ThemeManager")
    print("-" * 30)
    
    try:
        from PySide6.QtWidgets import QApplication
        from hrneowave.gui.styles.theme_manager import ThemeManager
        
        # Vérifier si QApplication existe déjà
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        theme_manager = ThemeManager(app)
        
        # Test de l'attribut available_themes
        if hasattr(theme_manager, 'available_themes'):
            print(f"✅ available_themes: {theme_manager.available_themes}")
        else:
            print("❌ available_themes manquant")
            return False
        
        # Test d'application de thème
        theme_manager.apply_theme('maritime_modern')
        print("✅ Thème appliqué avec succès")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur ThemeManager: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_window():
    """Test de création MainWindow"""
    print("\n🧪 TEST 3: MainWindow")
    print("-" * 30)
    
    try:
        from PySide6.QtWidgets import QApplication
        from hrneowave.gui.main_window import MainWindow
        
        # Vérifier si QApplication existe déjà
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test création MainWindow
        main_window = MainWindow()
        print("✅ MainWindow créée")
        
        # Test affichage
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        visible = main_window.isVisible()
        print(f"✅ MainWindow visible: {visible}")
        
        if visible:
            print("🎉 SUCCÈS: Interface visible!")
            
            # Fermer après 2 secondes
            from PySide6.QtCore import QTimer
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(2000)
            
            print("🔄 Test boucle d'événements...")
            exit_code = app.exec()
            print(f"✅ Test terminé (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: Interface non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_application():
    """Test de l'application complète"""
    print("\n🧪 TEST 4: Application Complète")
    print("-" * 30)
    
    try:
        from PySide6.QtWidgets import QApplication
        from hrneowave.gui.main_window import MainWindow
        from hrneowave.gui.styles.theme_manager import ThemeManager
        
        # Créer une seule instance QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Appliquer le thème
        theme_manager = ThemeManager(app)
        theme_manager.apply_theme('maritime_modern')
        print("✅ Thème appliqué")
        
        # Créer MainWindow
        main_window = MainWindow()
        print("✅ MainWindow créée")
        
        # Afficher
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        visible = main_window.isVisible()
        print(f"✅ Interface visible: {visible}")
        
        if visible:
            print("🎉 SUCCÈS: Application complète fonctionnelle!")
            
            # Fermer après 3 secondes
            from PySide6.QtCore import QTimer
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(3000)
            
            print("🔄 Lancement application...")
            exit_code = app.exec()
            print(f"✅ Application fermée (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: Interface non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur application complète: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entrée principal"""
    print("🚀 TEST RAPIDE DES CORRECTIONS CHNEOWAVE")
    print("=" * 50)
    
    tests = [
        test_qt_imports,
        test_theme_manager,
        test_main_window,
        test_complete_application
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            failed += 1
    
    print(f"\n📊 RÉSULTATS:")
    print(f"✅ Tests réussis: {passed}")
    print(f"❌ Tests échoués: {failed}")
    
    if failed == 0:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ CHNeoWave est prêt à être utilisé")
        return 0
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Des problèmes persistent")
        return 1

if __name__ == "__main__":
    exit(main()) 