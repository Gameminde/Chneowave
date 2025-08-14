#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow Simple - Diagnostic Critique
Test ultra-simplifié pour identifier le problème exact
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer

def test_mainwindow_ultra_simple():
    """Test MainWindow ultra-simplifié"""
    print("🔍 TEST MAINWINDOW ULTRA-SIMPLE")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    
    try:
        # Test 1: QMainWindow basique
        print("\n📋 TEST 1: QMainWindow basique")
        window = QMainWindow()
        window.setWindowTitle("Test QMainWindow Basique")
        window.resize(800, 600)
        
        # Widget central simple
        central = QWidget()
        layout = QVBoxLayout(central)
        label = QLabel("Test QMainWindow - Si vous voyez ceci, Qt fonctionne")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        window.setCentralWidget(central)
        
        window.show()
        print(f"✅ QMainWindow basique - Visible: {window.isVisible()}")
        
        # Test 2: Import MainWindow CHNeoWave
        print("\n📋 TEST 2: Import MainWindow CHNeoWave")
        try:
            from hrneowave.gui.main_window import MainWindow as CHMainWindow
            print("✅ Import MainWindow CHNeoWave réussi")
            
            # Test 3: Création MainWindow CHNeoWave SANS appel de méthodes
            print("\n📋 TEST 3: Création MainWindow CHNeoWave (constructeur seulement)")
            try:
                # Créer une instance mais ne pas appeler show() encore
                ch_window = CHMainWindow()
                print("✅ Constructeur MainWindow CHNeoWave réussi")
                print(f"   Type: {type(ch_window)}")
                print(f"   Titre: {ch_window.windowTitle()}")
                print(f"   Taille: {ch_window.size()}")
                
                # Test 4: Affichage MainWindow CHNeoWave
                print("\n📋 TEST 4: Affichage MainWindow CHNeoWave")
                ch_window.setWindowTitle("CHNeoWave - Test Simple")
                ch_window.resize(1000, 700)
                ch_window.show()
                ch_window.raise_()
                ch_window.activateWindow()
                
                # Forcer le traitement des événements
                app.processEvents()
                
                print(f"✅ MainWindow CHNeoWave - Visible: {ch_window.isVisible()}")
                print(f"✅ MainWindow CHNeoWave - Géométrie: {ch_window.geometry()}")
                print(f"✅ MainWindow CHNeoWave - Actif: {ch_window.isActiveWindow()}")
                
                # Vérifier le widget central
                central_widget = ch_window.centralWidget()
                if central_widget:
                    print(f"✅ Widget central: {type(central_widget).__name__}")
                    print(f"✅ Widget central visible: {central_widget.isVisible()}")
                    print(f"✅ Widget central taille: {central_widget.size()}")
                else:
                    print("❌ Aucun widget central défini")
                
                # Test de capture pour vérifier le rendu
                try:
                    pixmap = ch_window.grab()
                    if not pixmap.isNull():
                        print("✅ Capture d'écran réussie - Interface rendue")
                        # Sauvegarder la capture pour vérification
                        pixmap.save("test_mainwindow_capture.png")
                        print("✅ Capture sauvegardée: test_mainwindow_capture.png")
                    else:
                        print("⚠️ Capture d'écran vide")
                except Exception as e:
                    print(f"⚠️ Erreur capture: {e}")
                
            except Exception as e:
                print(f"❌ Erreur création MainWindow CHNeoWave: {e}")
                import traceback
                traceback.print_exc()
                
        except Exception as e:
            print(f"❌ Erreur import MainWindow CHNeoWave: {e}")
            import traceback
            traceback.print_exc()
        
        # Maintenir les fenêtres ouvertes
        print("\n⏰ Maintien des fenêtres pendant 10 secondes...")
        print("   Vérifiez visuellement si les fenêtres apparaissent à l'écran")
        
        # Timer pour fermeture
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(10000)  # 10 secondes
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_mainwindow_ultra_simple()
    print(f"\nCode de sortie: {exit_code}")
    sys.exit(exit_code)