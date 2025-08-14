#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow CHNeoWave après correction de la logique des widgets
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

def test_mainwindow_corrigee():
    """Test de la MainWindow après correction de la logique des widgets"""
    print("🔍 === TEST MAINWINDOW CORRIGÉE ===")
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    print("✅ QApplication créée")
    
    try:
        # Importer et créer MainWindow
        from hrneowave.gui.main_window import MainWindow
        print("✅ Import MainWindow réussi")
        
        # Créer la fenêtre principale
        window = MainWindow()
        print("✅ MainWindow créée")
        
        # Vérifier l'état de la fenêtre
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ Actif: {window.isActiveWindow()}")
        
        # Forcer l'affichage
        window.show()
        window.raise_()
        window.activateWindow()
        
        print("✅ MainWindow affichée avec succès")
        print(f"✅ Visible après show(): {window.isVisible()}")
        
        # Timer pour fermer automatiquement après 10 secondes
        def close_app():
            print("⏰ Fermeture automatique après 10 secondes")
            window.close()
            app.quit()
        
        QTimer.singleShot(10000, close_app)
        
        # Lancer la boucle d'événements
        print("🚀 Lancement de la boucle d'événements...")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_mainwindow_corrigee()
    print(f"🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)