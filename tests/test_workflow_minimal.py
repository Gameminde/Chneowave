#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test minimal du workflow CHNeoWave
Test simple et robuste pour valider la navigation de base
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Mock du hardware avant les imports
with patch('hrneowave.hardware.manager.HardwareManager') as mock_hw:
    mock_hw.return_value.is_initialized = True
    
    # Ajouter le répertoire src au path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer
    from hrneowave.gui.main_window import MainWindow

def test_workflow_minimal():
    """Test minimal du workflow de navigation"""
    print("🚀 DEBUT TEST WORKFLOW MINIMAL")
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Mock du hardware
        with patch('hrneowave.hardware.manager.HardwareManager') as mock_hw:
            mock_hw.return_value.is_initialized = True
            
            # Créer la fenêtre principale
            window = MainWindow()
            print("✅ Fenêtre principale créée")
            
            # Vérifier que le ViewManager existe
            assert hasattr(window, 'view_manager'), "ViewManager manquant"
            print("✅ ViewManager trouvé")
            
            # Vérifier les vues enregistrées
            expected_views = ['dashboard', 'calibration', 'acquisition', 'analysis', 'export']
            for view_name in expected_views:
                assert view_name in window.view_manager.views, f"Vue {view_name} manquante"
            print(f"✅ Toutes les vues enregistrées: {list(window.view_manager.views.keys())}")
            
            # Test de navigation vers dashboard
            window.view_manager.switch_to_view('dashboard')
            current_view = window.view_manager.current_view
            assert current_view == 'dashboard', f"Navigation échouée: vue actuelle = {current_view}"
            print("✅ Navigation vers dashboard réussie")
            
            # Test de navigation vers calibration
            window.view_manager.switch_to_view('calibration')
            current_view = window.view_manager.current_view
            assert current_view == 'calibration', f"Navigation échouée: vue actuelle = {current_view}"
            print("✅ Navigation vers calibration réussie")
            
            print("🎉 TOUS LES TESTS PASSES")
            return True
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer
        if 'window' in locals():
            window.close()
        app.quit()

if __name__ == '__main__':
    success = test_workflow_minimal()
    sys.exit(0 if success else 1)