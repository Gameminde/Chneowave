#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour vérifier la navigation du workflow
"""

import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ajouter le répertoire racine au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_simple_navigation():
    """Test simple de navigation"""
    print("🚀 TEST SIMPLE NAVIGATION")
    print("=" * 50)
    
    try:
        # Mock du hardware avant l'import
        with patch('hrneowave.hardware.manager.HardwareManager') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_initialized = True
            
            from hrneowave.gui.main_window import MainWindow
            from PySide6.QtWidgets import QApplication
            
            # Créer l'application Qt
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            print("✅ QApplication créée")
            
            # Créer la fenêtre principale
            window = MainWindow()
            print("✅ CHNeoWaveMainWindow créée")
            
            # Vérifier le ViewManager
            assert window.view_manager is not None, "ViewManager doit exister"
            print("✅ ViewManager existe")
            
            # Vérifier les vues enregistrées
            expected_views = ["dashboard", "calibration", "acquisition", "analysis", "export"]
            for view_name in expected_views:
                if window.view_manager.has_view(view_name):
                    print(f"✅ Vue '{view_name}' enregistrée")
                else:
                    print(f"❌ Vue '{view_name}' manquante")
                    return False
            
            # Tester la navigation vers dashboard
            success = window.view_manager.switch_to_view("dashboard")
            if success:
                print("✅ Navigation vers dashboard réussie")
                current = window.view_manager.current_view
                print(f"✅ Vue actuelle: {current}")
                return current == "dashboard"
            else:
                print("❌ Navigation vers dashboard échouée")
                return False
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_simple_navigation()
    if result:
        print("\n🎉 TEST RÉUSSI")
        sys.exit(0)
    else:
        print("\n💥 TEST ÉCHOUÉ")
        sys.exit(1)