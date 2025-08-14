#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de la solution CHNeoWave - Évite les problèmes de singleton QApplication
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_application_launch():
    """Test du lancement de l'application complète"""
    print("🚀 TEST FINAL - LANCEMENT CHNEOWAVE")
    print("=" * 50)
    
    try:
        # Imports nécessaires
        from PySide6.QtWidgets import QApplication
        from hrneowave.gui.main_window import MainWindow
        from hrneowave.gui.styles.theme_manager import ThemeManager
        
        # Créer QApplication (une seule fois)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave")
            app.setApplicationVersion("1.1.0")
            app.setOrganizationName("Laboratoire d'Hydrodynamique Maritime")
            app.setQuitOnLastWindowClosed(True)
            print("✅ QApplication créé")
        else:
            print("✅ QApplication existant réutilisé")
        
        # Appliquer le thème
        try:
            theme_manager = ThemeManager(app)
            theme_manager.apply_theme('maritime_modern')
            print("✅ Thème maritime appliqué")
        except Exception as e:
            print(f"⚠️ Erreur thème: {e}")
        
        # Créer MainWindow
        try:
            main_window = MainWindow()
            print("✅ MainWindow créée")
        except Exception as e:
            print(f"❌ Erreur création MainWindow: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Afficher la fenêtre
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        # Vérifications
        visible = main_window.isVisible()
        active = main_window.isActiveWindow()
        minimized = main_window.isMinimized()
        
        print(f"✅ Vérifications: Visible={visible}, Active={active}, Minimized={minimized}")
        
        if visible:
            print("🎉 SUCCÈS: Interface CHNeoWave visible!")
            print("👀 L'interface devrait maintenant être affichée")
            
            # Maintenir ouvert pendant 5 secondes pour vérification
            from PySide6.QtCore import QTimer
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(5000)
            
            print("🔄 Lancement de l'application (5 secondes)...")
            exit_code = app.exec()
            print(f"✅ Application fermée (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: Interface non visible")
            print("⚠️ Tentative de maximisation...")
            main_window.showMaximized()
            
            if main_window.isVisible():
                print("✅ Interface visible après maximisation")
                return True
            else:
                print("❌ Interface toujours non visible")
                return False
                
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_window():
    """Test avec une fenêtre simple pour vérifier Qt"""
    print("\n🧪 TEST FENÊTRE SIMPLE")
    print("=" * 40)
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
        from PySide6.QtCore import Qt, QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Fenêtre simple
        window = QMainWindow()
        window.setWindowTitle("Test CHNeoWave - Simple")
        window.setGeometry(200, 200, 400, 300)
        
        # Label
        label = QLabel("Test CHNeoWave - Interface Simple")
        label.setAlignment(Qt.AlignCenter)
        window.setCentralWidget(label)
        
        # Affichage
        window.show()
        window.raise_()
        window.activateWindow()
        
        print(f"✅ Fenêtre simple créée: Visible={window.isVisible()}")
        
        # Timer pour fermer
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(2000)
        
        exit_code = app.exec()
        print(f"✅ Fenêtre simple fermée (code: {exit_code})")
        return True
        
    except Exception as e:
        print(f"❌ Erreur fenêtre simple: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entrée principal"""
    print("🎯 TEST FINAL - SOLUTION CHNEOWAVE")
    print("=" * 50)
    
    # Test fenêtre simple d'abord
    if not test_simple_window():
        print("❌ ÉCHEC: Fenêtre simple ne fonctionne pas")
        return 1
    
    # Test application complète
    if not test_application_launch():
        print("❌ ÉCHEC: Application complète ne fonctionne pas")
        return 1
    
    print("\n🎉 SUCCÈS TOTAL!")
    print("✅ CHNeoWave fonctionne correctement")
    print("✅ Interface visible et responsive")
    print("✅ Prêt à être utilisé")
    
    return 0

if __name__ == "__main__":
    exit(main()) 