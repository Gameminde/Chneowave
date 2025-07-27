#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de validation de l'interface CHNeoWave
Se concentre sur les problèmes principaux sans matplotlib
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

def test_interface_fixes():
    """Test simple des corrections d'interface"""
    print("CHNeoWave - Test simple de validation")
    print("=" * 50)
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    errors = []
    
    try:
        print("\n1. Test d'importation des modules...")
        
        # Test d'importation de MainWindow
        from hrneowave.gui.main_window import MainWindow
        print("✓ MainWindow importée")
        
        # Test d'importation de ViewManager
        from hrneowave.gui.view_manager import ViewManager
        print("✓ ViewManager importé")
        
        # Test d'importation de MainSidebar
        from hrneowave.gui.components.main_sidebar import MainSidebar
        print("✓ MainSidebar importée")
        
        print("\n2. Test de création de MainWindow...")
        main_window = MainWindow()
        print("✓ MainWindow créée avec succès")
        
        print("\n3. Test de ViewManager...")
        view_manager = main_window.view_manager
        
        # Vérifier les méthodes du ViewManager
        if hasattr(view_manager, 'switch_to_view'):
            print("✓ Méthode switch_to_view disponible")
        else:
            errors.append("Méthode switch_to_view manquante")
            
        if hasattr(view_manager, 'has_view'):
            print("✓ Méthode has_view disponible")
        else:
            errors.append("Méthode has_view manquante")
            
        if hasattr(view_manager, 'get_view_widget'):
            print("✓ Méthode get_view_widget disponible")
        else:
            errors.append("Méthode get_view_widget manquante")
        
        print("\n4. Test des vues enregistrées...")
        required_views = ['welcome', 'dashboard', 'manual_calibration', 'acquisition']
        for view_name in required_views:
            if view_manager.has_view(view_name):
                print(f"✓ Vue '{view_name}' enregistrée")
            else:
                print(f"✗ Vue '{view_name}' manquante")
                errors.append(f"Vue {view_name} non enregistrée")
        
        print("\n5. Test de navigation...")
        # Test navigation vers welcome
        try:
            success = view_manager.switch_to_view('welcome')
            if success:
                print("✓ Navigation vers 'welcome' réussie")
            else:
                print("✗ Navigation vers 'welcome' échouée")
                errors.append("Navigation welcome échouée")
        except Exception as e:
            print(f"✗ Erreur navigation welcome: {e}")
            errors.append(f"Navigation welcome: {e}")
        
        # Test navigation vers dashboard
        try:
            success = view_manager.switch_to_view('dashboard')
            if success:
                print("✓ Navigation vers 'dashboard' réussie")
            else:
                print("✗ Navigation vers 'dashboard' échouée")
                errors.append("Navigation dashboard échouée")
        except Exception as e:
            print(f"✗ Erreur navigation dashboard: {e}")
            errors.append(f"Navigation dashboard: {e}")
        
        print("\n6. Test de la sidebar...")
        sidebar = main_window.sidebar
        if sidebar:
            print("✓ Sidebar accessible")
            
            # Vérifier le signal de navigation
            if hasattr(sidebar, 'navigation_requested'):
                print("✓ Signal navigation_requested disponible")
            else:
                print("✗ Signal navigation_requested manquant")
                errors.append("Signal navigation_requested manquant")
        else:
            print("✗ Sidebar non accessible")
            errors.append("Sidebar inaccessible")
        
        print("\n7. Test du workflow de création de projet...")
        welcome_view = view_manager.get_view_widget('welcome')
        if welcome_view:
            print("✓ Vue welcome accessible")
            
            # Vérifier les champs de saisie
            required_fields = ['project_name', 'project_manager', 'laboratory', 'description']
            for field_name in required_fields:
                if hasattr(welcome_view, field_name):
                    print(f"✓ Champ '{field_name}' disponible")
                else:
                    print(f"✗ Champ '{field_name}' manquant")
                    errors.append(f"Champ {field_name} manquant")
            
            # Vérifier le bouton de validation
            if hasattr(welcome_view, 'validate_button'):
                print("✓ Bouton de validation disponible")
            else:
                print("✗ Bouton de validation manquant")
                errors.append("Bouton validation manquant")
            
            # Vérifier le signal de création de projet
            if hasattr(welcome_view, 'projectCreationRequested'):
                print("✓ Signal projectCreationRequested disponible")
            else:
                print("✗ Signal projectCreationRequested manquant")
                errors.append("Signal projectCreationRequested manquant")
        else:
            print("✗ Vue welcome non accessible")
            errors.append("Vue welcome inaccessible")
        
        # Nettoyer
        main_window.close()
        
    except Exception as e:
        print(f"\n✗ ERREUR CRITIQUE: {e}")
        errors.append(f"Erreur critique: {e}")
    
    # Résultats
    print("\n" + "=" * 50)
    if errors:
        print(f"❌ ERREURS DÉTECTÉES ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        return False
    else:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✓ Interface corrigée avec succès")
        print("✓ Navigation fonctionnelle")
        print("✓ Workflow de création de projet opérationnel")
        return True

if __name__ == "__main__":
    success = test_interface_fixes()
    sys.exit(0 if success else 1)