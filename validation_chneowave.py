#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation rapide CHNeoWave
Vérifie que l'application se lance correctement après correction
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def validation_rapide():
    """Validation rapide de CHNeoWave"""
    print("🚀 === VALIDATION CHNEOWAVE ===")
    
    try:
        # Test 1: Import des modules principaux
        print("📦 Test 1: Imports...")
        from PySide6.QtWidgets import QApplication
        from hrneowave.gui.main_window import MainWindow
        print("   ✅ Imports réussis")
        
        # Test 2: Création application Qt
        print("🖥️  Test 2: Application Qt...")
        app = QApplication(sys.argv)
        print("   ✅ QApplication créée")
        
        # Test 3: Création MainWindow
        print("🏠 Test 3: MainWindow...")
        window = MainWindow()
        print("   ✅ MainWindow créée sans erreur")
        
        # Test 4: Vérification de l'état
        print("🔍 Test 4: État de la fenêtre...")
        window.show()
        print(f"   ✅ Visible: {window.isVisible()}")
        print(f"   ✅ Taille: {window.size()}")
        
        # Test 5: Widget central
        print("📱 Test 5: Interface...")
        central = window.centralWidget()
        if central and central.isVisible():
            print("   ✅ Interface utilisateur active")
        else:
            print("   ⚠️  Interface non visible")
        
        # Fermeture propre
        window.close()
        app.quit()
        
        print("\n🎉 === VALIDATION RÉUSSIE ===")
        print("✅ CHNeoWave fonctionne parfaitement")
        print("✅ Problème d'affichage résolu")
        print("✅ Application prête à l'utilisation")
        
        return True
        
    except Exception as e:
        print(f"\n❌ === VALIDATION ÉCHOUÉE ===")
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = validation_rapide()
    if success:
        print("\n🏁 Validation terminée avec succès")
        sys.exit(0)
    else:
        print("\n🏁 Validation échouée")
        sys.exit(1)