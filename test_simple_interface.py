#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour vérifier l'affichage de l'interface
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_chneowave_complete():
    """Test complet CHNeoWave avec une seule QApplication"""
    print("=== TEST CHNEOWAVE COMPLET ===")
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        from hrneowave.core.logging_config import setup_logging
        
        # Configuration logging
        setup_logging()
        print("✅ Logging configuré")
        
        # Création unique de QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("CHNeoWave Test Complet")
        print("✅ QApplication créée")
        
        # Test 1: Interface Qt basique d'abord
        print("\n--- Test 1: Interface Qt basique ---")
        try:
            from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
            
            basic_window = QMainWindow()
            basic_window.setWindowTitle("CHNeoWave - Test Qt Basique")
            basic_window.setGeometry(100, 100, 600, 400)
            
            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)
            
            label = QLabel("✅ Interface Qt Basique Fonctionnelle!")
            label.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #1565C0;
                    padding: 20px;
                    text-align: center;
                    background-color: #E3F2FD;
                    border-radius: 10px;
                }
            """)
            
            layout.addWidget(label)
            basic_window.setCentralWidget(central_widget)
            
            basic_window.show()
            basic_window.raise_()
            basic_window.activateWindow()
            
            print(f"✅ Fenêtre basique visible: {basic_window.isVisible()}")
            print(f"✅ Taille: {basic_window.size()}")
            
            # Attendre 3 secondes
            timer1 = QTimer()
            timer1.setSingleShot(True)
            timer1.timeout.connect(lambda: basic_window.close())
            timer1.start(3000)
            
            # Traiter les événements pendant 3 secondes
            from PySide6.QtCore import QEventLoop
            loop = QEventLoop()
            timer1.timeout.connect(loop.quit)
            loop.exec()
            
            print("✅ Test Qt basique terminé")
            
        except Exception as e:
            print(f"❌ Erreur test Qt basique: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test 2: Interface CHNeoWave complète
        print("\n--- Test 2: Interface CHNeoWave complète ---")
        try:
            from hrneowave.gui.main_window import MainWindow
            from hrneowave.gui.styles.theme_manager import ThemeManager
            
            print("✅ Modules CHNeoWave importés")
            
            # Création du gestionnaire de thème
            theme_manager = ThemeManager(app)
            theme_manager.apply_theme('maritime_modern')
            print("✅ Thème maritime appliqué")
            
            # Création de MainWindow
            main_window = MainWindow()
            print("✅ MainWindow créée")
            
            main_window.setWindowTitle("CHNeoWave - Interface Maritime Professionnelle")
            main_window.setGeometry(150, 150, 1200, 800)
            
            main_window.show()
            main_window.raise_()
            main_window.activateWindow()
            
            print(f"✅ MainWindow visible: {main_window.isVisible()}")
            print(f"✅ Taille: {main_window.size()}")
            print(f"✅ Position: {main_window.pos()}")
            
            # Afficher pendant 10 secondes
            timer2 = QTimer()
            timer2.timeout.connect(app.quit)
            timer2.start(10000)  # 10 secondes
            
            print("\n🎉 INTERFACE CHNEOWAVE AFFICHÉE AVEC SUCCÈS!")
            print("Interface visible pendant 10 secondes...")
            
            exit_code = app.exec()
            print(f"✅ Application fermée avec code: {exit_code}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur MainWindow: {e}")
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
    print("DIAGNOSTIC COMPLET INTERFACE CHNEOWAVE")
    print("======================================")
    
    if test_chneowave_complete():
        print("\n🎉 SUCCÈS TOTAL - INTERFACE CHNEOWAVE OPÉRATIONNELLE!")
        return 0
    else:
        print("\n❌ ÉCHEC - Problème avec l'interface CHNeoWave")
        return 1

if __name__ == "__main__":
    sys.exit(main())