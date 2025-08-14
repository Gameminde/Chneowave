#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow CHNeoWave en désactivant le système d'aide
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

def test_mainwindow_chneowave_sans_help():
    """Test MainWindow CHNeoWave sans système d'aide"""
    print("🔍 DÉBUT: Test MainWindow CHNeoWave sans système d'aide")
    
    # Créer QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    print(f"✅ QApplication créée: {app.platformName()}")
    
    # Importer et créer MainWindow CHNeoWave
    try:
        from src.hrneowave.gui.main_window import MainWindow
        print("✅ MainWindow CHNeoWave importée")
        
        # Créer l'instance
        window = MainWindow()
        print("✅ MainWindow CHNeoWave créée")
        
        # DÉSACTIVER temporairement le système d'aide
        # en remplaçant la méthode par un pass
        def dummy_install_help(self):
            print("🚫 Système d'aide désactivé pour ce test")
            pass
        
        # Remplacer la méthode
        window._install_contextual_help = dummy_install_help.__get__(window, MainWindow)
        print("✅ Système d'aide désactivé")
        
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
                msg.setText("✅ MainWindow CHNeoWave s'affiche correctement sans système d'aide !\n\nLe problème vient du système d'aide.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            else:
                print("❌ MainWindow toujours invisible - problème plus profond")
            
            # Fermer l'application
            window.close()
            app.quit()
        
        timer = QTimer()
        timer.timeout.connect(check_visibility)
        timer.start(1000)  # 1 seconde
        
        print("🚀 Lancement de l'application CHNeoWave sans aide")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de MainWindow: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_mainwindow_chneowave_sans_help()
    print(f"🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)