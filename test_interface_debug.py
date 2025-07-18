#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de débogage pour l'interface CHNeoWave
Vérifie pourquoi l'interface se ferme immédiatement
"""

import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

def test_interface_debug():
    """Test de débogage de l'interface"""
    try:
        print("🔍 Test de débogage interface CHNeoWave")
        print("="*50)
        
        # Créer application Qt
        app = QApplication(sys.argv)
        app.setApplicationName("CHNeoWave Debug")
        
        print("✅ QApplication créée")
        
        # Importer et créer l'interface
        print("📦 Tentative d'import HRNeoWaveApp...")
        try:
            from hrneowave.gui.main import HRNeoWaveApp
            print("✅ Import HRNeoWaveApp réussi")
        except Exception as e:
            print(f"❌ Erreur import HRNeoWaveApp: {e}")
            traceback.print_exc()
            return 1
        
        # Créer l'application
        print("🏗️ Création de HRNeoWaveApp...")
        try:
            main_app = HRNeoWaveApp(use_new_interface=True)
            print("✅ HRNeoWaveApp créée")
        except Exception as e:
            print(f"❌ Erreur création HRNeoWaveApp: {e}")
            traceback.print_exc()
            return 1
        
        # Afficher l'interface
        main_app.show()
        print("✅ Interface affichée")
        
        # Timer pour vérifier si l'interface reste ouverte
        def check_status():
            print("⏰ Interface toujours ouverte après 2 secondes")
            
        timer = QTimer()
        timer.timeout.connect(check_status)
        timer.setSingleShot(True)
        timer.start(2000)  # 2 secondes
        
        # Timer pour fermer automatiquement après 10 secondes
        def auto_close():
            print("🔚 Fermeture automatique après 10 secondes")
            app.quit()
            
        close_timer = QTimer()
        close_timer.timeout.connect(auto_close)
        close_timer.setSingleShot(True)
        close_timer.start(10000)  # 10 secondes
        
        print("🚀 Lancement de la boucle d'événements...")
        
        # Lancer la boucle d'événements
        result = app.exec_()
        
        print(f"✅ Boucle d'événements terminée avec code: {result}")
        return result
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"❌ Erreur: {e}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(test_interface_debug())