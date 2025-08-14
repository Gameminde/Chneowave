#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test ViewManager corrigé
"""

import sys
import traceback
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_viewmanager():
    """Test ViewManager corrigé"""
    print("🚀 TEST VIEWMANAGER CORRIGÉ")
    print("=" * 50)
    
    try:
        from PySide6.QtWidgets import QApplication, QStackedWidget
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        print("✅ QApplication créé")
        
        # Test import ViewManager
        print("🔄 Test import ViewManager...")
        from hrneowave.gui.view_manager import ViewManager
        print("✅ ViewManager importé")
        
        # Test création ViewManager sans paramètre
        print("🔄 Test création ViewManager sans paramètre...")
        view_manager = ViewManager()
        print("✅ ViewManager créé sans paramètre")
        
        # Test création ViewManager avec paramètre
        print("🔄 Test création ViewManager avec paramètre...")
        stacked_widget = QStackedWidget()
        view_manager_with_param = ViewManager(stacked_widget)
        print("✅ ViewManager créé avec paramètre")
        
        print("🎉 SUCCÈS: ViewManager fonctionne dans les deux cas !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_viewmanager() else 1)
