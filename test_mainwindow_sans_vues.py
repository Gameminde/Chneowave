#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow CHNeoWave en désactivant la création des vues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

def test_mainwindow_sans_vues():
    """Test MainWindow CHNeoWave sans création de vues"""
    print("🔍 DÉBUT: Test MainWindow CHNeoWave sans vues")
    
    # Créer QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    print(f"✅ QApplication créée: {app.platformName()}")
    
    # Importer et modifier MainWindow
    try:
        from src.hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow CHNeoWave importée")
        
        # Créer l'instance
        window = MainWindow()
        print("✅ MainWindow CHNeoWave créée")
        
        # DÉSACTIVER la création des vues en remplaçant la méthode
        def dummy_create_views(self):
            print("🚫 Création des vues désactivée pour ce test")
            print("🔍 DEBUG: _create_and_register_views - DÉSACTIVÉ")
            # Ne rien faire - pas de création de vues
            pass
        
        # Remplacer la méthode
        window._create_and_register_views = dummy_create_views.__get__(window, MainWindow)
        print("✅ Création des vues désactivée")
        
        # FORCER L'AFFICHAGE
        window.show()
        window.raise_()
        window.activateWindow()
        
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Actif: {window.isActiveWindow()}")
        
        # Vérifier après 1 seconde
        def check_visibility():
            print(f"🔍 Vérification après 1s:")
            print(f"   - Visible: {window.isVisible()}")
            print(f"   - Géométrie: {window.geometry()}")
            print(f"   - Actif: {window.isActiveWindow()}")
            
            if window.isVisible():
                # Afficher une boîte de dialogue pour confirmer
                msg = QMessageBox()
                msg.setWindowTitle("Test Réussi")
                msg.setText("✅ MainWindow CHNeoWave s'affiche correctement sans vues !\n\nLe problème vient de la création des vues.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                print("✅ SUCCESS: Le problème vient de la création des vues")
            else:
                print("❌ MainWindow toujours invisible - problème dans _build_ui")
            
            # Fermer l'application
            window.close()
            app.quit()
        
        timer = QTimer()
        timer.timeout.connect(check_visibility)
        timer.start(1000)  # 1 seconde
        
        print("🚀 Lancement MainWindow CHNeoWave sans vues")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_mainwindow_sans_vues()
    print(f"🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)