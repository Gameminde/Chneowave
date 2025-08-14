#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de fenêtre Qt
"""

import sys
import traceback
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_simple_window():
    """Test simple de fenêtre Qt"""
    print("🚀 TEST FENÊTRE SIMPLE")
    print("=" * 50)
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
        from PySide6.QtCore import Qt, QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("Test Simple Fenêtre")
        
        print("✅ QApplication créé")
        
        # Créer une fenêtre simple
        print("🔄 Création fenêtre simple...")
        window = QMainWindow()
        window.setWindowTitle("Test Simple - CHNeoWave")
        window.resize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Label de test
        label = QLabel("🎉 Test de visibilité réussi !")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: blue;")
        layout.addWidget(label)
        
        window.setCentralWidget(central_widget)
        
        print("✅ Fenêtre simple créée")
        
        # Centrer la fenêtre
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = window.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        window.move(x, y)
        
        print("✅ Fenêtre centrée")
        
        # Afficher la fenêtre
        print("🔄 Affichage fenêtre...")
        window.show()
        window.raise_()
        window.activateWindow()
        
        visible = window.isVisible()
        print(f"✅ Fenêtre visible: {visible}")
        
        if visible:
            print("🎉 SUCCÈS: Fenêtre simple visible!")
            
            # Maintenir ouvert 10 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(10000)
            
            print("🔄 Maintien ouvert 10 secondes...")
            print("🔍 Vérifiez que la fenêtre est visible sur votre écran")
            
            exit_code = app.exec()
            print(f"✅ Test terminé (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: Fenêtre simple non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_simple_window() else 1)
