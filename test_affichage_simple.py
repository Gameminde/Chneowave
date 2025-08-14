#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Affichage Simple - CHNeoWave
Test minimal pour forcer l'affichage de l'interface
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer, Qt

def test_affichage_simple():
    """Test simple d'affichage CHNeoWave"""
    print("=== TEST AFFICHAGE SIMPLE CHNeoWave ===")
    
    # Créer QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave Test Simple")
    print(f"✅ QApplication créée sur: {app.platformName()}")
    
    try:
        # Import et création MainWindow
        print("🔍 Import MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow importée")
        
        print("🔍 Création MainWindow...")
        window = MainWindow()
        print("✅ MainWindow créée")
        
        # Configuration basique
        window.setWindowTitle("CHNeoWave - Test Affichage Simple")
        window.setGeometry(200, 200, 1000, 700)
        
        # AFFICHAGE FORCÉ
        print("🔍 Affichage forcé...")
        window.show()
        window.raise_()
        window.activateWindow()
        
        # Vérifications
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ Titre: {window.windowTitle()}")
        
        # Forcer le traitement des événements
        app.processEvents()
        
        # Message de confirmation immédiat
        def show_immediate_confirmation():
            print("🔍 Affichage du message de confirmation...")
            
            msg = QMessageBox()
            msg.setWindowTitle("CHNeoWave - Test Réussi")
            msg.setText("🎉 TEST D'AFFICHAGE RÉUSSI !\n\n"
                       f"✅ MainWindow visible: {window.isVisible()}\n"
                       f"✅ Géométrie: {window.geometry()}\n"
                       f"✅ Position: ({window.x()}, {window.y()})\n"
                       f"✅ Taille: {window.width()}x{window.height()}\n\n"
                       "L'interface CHNeoWave devrait être visible !\n\n"
                       "Cliquez OK pour fermer le test.")
            msg.setIcon(QMessageBox.Information)
            
            # Positionner le message près de la fenêtre
            msg.move(window.x() + 50, window.y() + 50)
            
            result = msg.exec()
            print(f"✅ Message fermé avec résultat: {result}")
            
            # Fermer l'application
            app.quit()
        
        # Timer pour affichage immédiat du message
        timer = QTimer()
        timer.timeout.connect(show_immediate_confirmation)
        timer.setSingleShot(True)
        timer.start(1000)  # 1 seconde
        
        print("⏰ Message de confirmation dans 1 seconde...")
        print("🔍 Vérifiez si la fenêtre CHNeoWave est visible")
        
        # Lancer la boucle d'événements
        exit_code = app.exec()
        print(f"✅ Application terminée avec code: {exit_code}")
        
        return exit_code
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        
        # Message d'erreur
        error_msg = QMessageBox()
        error_msg.setWindowTitle("CHNeoWave - Erreur")
        error_msg.setText(f"❌ ERREUR LORS DU TEST:\n\n{e}\n\nConsultez la console pour plus de détails.")
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.exec()
        
        return 1

if __name__ == "__main__":
    result = test_affichage_simple()
    print(f"\n🏁 Test terminé avec code: {result}")
    
    if result == 0:
        print("🎉 TEST RÉUSSI - Interface visible")
    else:
        print("❌ TEST ÉCHOUÉ - Problème détecté")
    
    sys.exit(result)