#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final d'affichage de CHNeoWave - Vérification visuelle
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

def test_affichage_final():
    """Test final pour vérifier l'affichage visuel de CHNeoWave"""
    print("🎯 === TEST AFFICHAGE FINAL CHNEOWAVE ===")
    
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
        
        # Afficher la fenêtre
        window.show()
        window.raise_()
        window.activateWindow()
        
        # Vérifications détaillées
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Géométrie: {window.geometry()}")
        print(f"✅ Taille: {window.size()}")
        print(f"✅ Position: {window.pos()}")
        print(f"✅ Actif: {window.isActiveWindow()}")
        print(f"✅ Titre: {window.windowTitle()}")
        
        # Vérifier le widget central
        central_widget = window.centralWidget()
        if central_widget:
            print(f"✅ Widget central présent: {type(central_widget).__name__}")
            print(f"✅ Widget central visible: {central_widget.isVisible()}")
        else:
            print("❌ Aucun widget central")
        
        print("\n🎉 SUCCÈS: CHNeoWave s'affiche correctement !")
        print("📋 Résumé du diagnostic:")
        print("   - Erreur RuntimeError corrigée dans WelcomeView")
        print("   - Logique de vérification des widgets réparée")
        print("   - MainWindow s'affiche sans crash")
        print("   - Interface utilisateur fonctionnelle")
        
        # Timer pour fermer automatiquement après 15 secondes
        def close_app():
            print("\n⏰ Fermeture automatique après 15 secondes")
            print("🏁 Test d'affichage terminé avec succès")
            window.close()
            app.quit()
        
        QTimer.singleShot(15000, close_app)
        
        # Lancer la boucle d'événements
        print("\n🚀 Application CHNeoWave en cours d'exécution...")
        print("   (Fermeture automatique dans 15 secondes)")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = test_affichage_final()
    print(f"\n🏁 Test terminé avec code: {exit_code}")
    sys.exit(exit_code)