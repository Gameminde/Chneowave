# -*- coding: utf-8 -*-
"""
Script de lancement pour l'interface graphique MCC DAQ Detector
"""
import sys
import os
import subprocess
import importlib.util

def check_pyqt6():
    """Vérifie si PyQt6 est installé"""
    try:
        import PyQt6
        return True
    except ImportError:
        return False

def install_pyqt6():
    """Installe PyQt6 si nécessaire"""
    print("PyQt6 n'est pas installé. Installation en cours...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6>=6.4.0"])
        print("PyQt6 installé avec succès!")
        return True
    except subprocess.CalledProcessError:
        print("Erreur lors de l'installation de PyQt6")
        return False

def main():
    """Fonction principale du launcher"""
    print("=" * 60)
    print("🔍 Détecteur de Cartes MCC DAQ - Interface Graphique")
    print("=" * 60)
    
    # Vérification de PyQt6
    if not check_pyqt6():
        print("❌ PyQt6 n'est pas installé")
        response = input("Voulez-vous l'installer maintenant? (o/n): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            if not install_pyqt6():
                print("❌ Impossible d'installer PyQt6. Arrêt.")
                return
        else:
            print("❌ PyQt6 est requis pour lancer l'interface graphique.")
            return
    
    # Vérification du fichier principal
    gui_file = "mcc_detector_gui.py"
    if not os.path.exists(gui_file):
        print(f"❌ Fichier {gui_file} non trouvé")
        print("Assurez-vous d'être dans le bon répertoire.")
        return
    
    print("✅ Toutes les vérifications sont passées")
    print("🚀 Lancement de l'interface graphique...")
    print("-" * 60)
    
    try:
        # Import et lancement de l'interface
        spec = importlib.util.spec_from_file_location("mcc_detector_gui", gui_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Lancement de l'application
        if hasattr(module, 'main'):
            module.main()
        else:
            print("❌ Fonction main() non trouvée dans le module")
            
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        print("Vérifiez que tous les fichiers sont présents et que PyQt6 est correctement installé.")

if __name__ == "__main__":
    main()




