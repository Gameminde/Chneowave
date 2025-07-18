#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de débogage spécifique pour la CLI CHNeoWave
Reprodu exactement la logique de run_gui avec --simulate
"""

import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

def test_cli_logic():
    """Test reproduisant exactement la logique CLI"""
    try:
        print("🔍 Test CLI CHNeoWave - Mode simulation")
        print("="*50)
        
        # Simuler les arguments CLI
        class Args:
            simulate = True
            fs = 32
            channels = 8
            config = None
            
        args = Args()
        
        # Configurer les variables d'environnement (comme dans run_gui)
        if args.simulate:
            os.environ['CHNW_MODE'] = 'simulate'
        if args.fs:
            os.environ['CHNW_FS'] = str(args.fs)
        if args.channels:
            os.environ['CHNW_CHANNELS'] = str(args.channels)
        if args.config:
            os.environ['CHNW_CONFIG'] = args.config
            
        print("✅ Variables d'environnement configurées")
        print(f"   CHNW_MODE: {os.environ.get('CHNW_MODE')}")
        print(f"   CHNW_FS: {os.environ.get('CHNW_FS')}")
        print(f"   CHNW_CHANNELS: {os.environ.get('CHNW_CHANNELS')}")
        
        # Créer l'application Qt (comme dans run_gui)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave")
            app.setApplicationVersion("3.0")
            app.setOrganizationName("Laboratoire Maritime")
            
        print("✅ QApplication créée")
        
        # Importer et créer l'application (comme dans run_gui)
        from hrneowave.gui.main import HRNeoWaveApp
        print("✅ Import HRNeoWaveApp réussi")
        
        main_app = HRNeoWaveApp(use_new_interface=True)
        print("✅ HRNeoWaveApp créée")
        
        main_app.show()
        print("✅ Interface affichée")
        
        print("🚀 CHNeoWave - Interface complète lancée")
        
        # Timer pour vérifier si l'interface reste ouverte
        def check_status():
            print("⏰ Interface toujours ouverte après 3 secondes")
            
        timer = QTimer()
        timer.timeout.connect(check_status)
        timer.setSingleShot(True)
        timer.start(3000)  # 3 secondes
        
        # Timer pour fermer automatiquement après 8 secondes
        def auto_close():
            print("🔚 Fermeture automatique après 8 secondes")
            app.quit()
            
        close_timer = QTimer()
        close_timer.timeout.connect(auto_close)
        close_timer.setSingleShot(True)
        close_timer.start(8000)  # 8 secondes
        
        print("🚀 Lancement de la boucle d'événements...")
        
        # Lancer la boucle d'événements (comme dans run_gui)
        result = app.exec_()
        
        print(f"✅ Boucle d'événements terminée avec code: {result}")
        return result
        
    except ImportError as e:
        print(f"❌ Erreur: Modules GUI non disponibles - {e}")
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface: {e}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(test_cli_logic())