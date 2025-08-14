#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow en désactivant temporairement tout CSS embedded
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def patch_setStyleSheet():
    """Patch temporaire pour désactiver setStyleSheet"""
    from PySide6.QtWidgets import QWidget
    
    # Sauvegarder la méthode originale
    original_setStyleSheet = QWidget.setStyleSheet
    
    def dummy_setStyleSheet(self, stylesheet):
        """Version dummy qui ne fait rien"""
        # Ne fait rien - ignore tous les CSS
        pass
    
    # Remplacer temporairement
    QWidget.setStyleSheet = dummy_setStyleSheet
    
    return original_setStyleSheet

def restore_setStyleSheet(original_method):
    """Restaure la méthode setStyleSheet originale"""
    from PySide6.QtWidgets import QWidget
    QWidget.setStyleSheet = original_method

def test_mainwindow_without_css():
    """Test MainWindow sans aucun CSS embedded"""
    print("=== TEST MAINWINDOW SANS CSS EMBEDDED ===")
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        from hrneowave.core.logging_config import setup_logging
        
        # Configuration logging
        setup_logging()
        print("✅ Logging configuré")
        
        # Création QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("CHNeoWave Sans CSS Embedded")
        print("✅ QApplication créée")
        
        # PATCH: Désactiver temporairement setStyleSheet
        print("🔧 Désactivation temporaire de setStyleSheet...")
        original_setStyleSheet = patch_setStyleSheet()
        
        try:
            # Import MainWindow
            from hrneowave.gui.main_window import MainWindow
            print("✅ MainWindow importée")
            
            # Création MainWindow
            print("Création de MainWindow sans CSS...")
            main_window = MainWindow()
            print("✅ MainWindow créée avec succès!")
            
            # Configuration basique
            main_window.setWindowTitle("CHNeoWave - Test Sans CSS Embedded")
            main_window.setGeometry(200, 200, 1200, 800)
            
            # Restaurer setStyleSheet avant affichage
            print("🔧 Restauration de setStyleSheet...")
            restore_setStyleSheet(original_setStyleSheet)
            
            # Affichage
            print("Affichage de MainWindow...")
            main_window.show()
            main_window.raise_()
            main_window.activateWindow()
            
            # Vérifications
            print(f"✅ MainWindow visible: {main_window.isVisible()}")
            print(f"✅ Taille: {main_window.size()}")
            print(f"✅ Position: {main_window.pos()}")
            print(f"✅ Titre: {main_window.windowTitle()}")
            
            if main_window.isVisible():
                print("\n🎉 SUCCÈS! MainWindow s'affiche sans CSS embedded")
                print("Le problème vient du CSS embedded malformé")
            else:
                print("\n⚠️ MainWindow créée mais pas visible")
            
            # Timer pour fermer après 10 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(10000)
            
            print("\nInterface affichée pendant 10 secondes...")
            print("(L'interface sera basique sans styles, c'est normal)")
            
            exit_code = app.exec()
            print(f"\n✅ Application fermée avec code: {exit_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ ERREUR pendant création MainWindow: {e}")
            import traceback
            traceback.print_exc()
            
            # Restaurer setStyleSheet en cas d'erreur
            restore_setStyleSheet(original_setStyleSheet)
            return False
        
    except Exception as e:
        print(f"❌ ERREUR générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_identify_problematic_css():
    """Test pour identifier le CSS problématique"""
    print("\n=== IDENTIFICATION CSS PROBLÉMATIQUE ===")
    
    try:
        from PySide6.QtWidgets import QApplication, QLabel
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test de différents CSS problématiques connus
        problematic_css_tests = [
            {
                "name": "CSS avec accolade manquante",
                "css": """
                QPushButton#nav_button {
                    background-color: #00ACC1;
                    color: #F5FBFF;
                    border: none;
                    border-radius: 13px;
                    padding: 8px 13px;
    
                }
                """
            },
            {
                "name": "CSS avec propriété invalide",
                "css": """
                QLabel {
                    invalid-property: value;
                    color: #445868;
                }
                """
            },
            {
                "name": "CSS avec sélecteur invalide",
                "css": """
                QLabel[invalid-selector] {
                    color: #445868;
                }
                """
            }
        ]
        
        for test in problematic_css_tests:
            print(f"\nTest: {test['name']}")
            try:
                test_label = QLabel("Test")
                test_label.setStyleSheet(test['css'])
                print(f"✅ CSS accepté: {test['name']}")
                test_label.deleteLater()
            except Exception as e:
                print(f"❌ CSS rejeté: {test['name']} - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR test CSS: {e}")
        return False

def main():
    """Fonction principale"""
    print("DIAGNOSTIC MAINWINDOW - CSS EMBEDDED")
    print("====================================")
    
    # Test 1: MainWindow sans CSS embedded
    success = test_mainwindow_without_css()
    
    if success:
        print("\n✅ MainWindow fonctionne sans CSS embedded")
        print("Le problème vient du CSS embedded malformé")
        
        # Test 2: Identifier CSS problématique
        test_identify_problematic_css()
        
        print("\n🔧 SOLUTION:")
        print("1. Corriger le CSS malformé dans main_sidebar.py")
        print("2. Externaliser tout le CSS embedded vers des fichiers .qss")
        print("3. Valider la syntaxe CSS avant application")
        
        return 0
    else:
        print("\n❌ MainWindow ne peut pas se créer même sans CSS")
        print("Le problème est plus profond que le CSS")
        return 1

if __name__ == "__main__":
    sys.exit(main())