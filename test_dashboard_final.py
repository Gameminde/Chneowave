#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test DashboardViewMaritime final
"""

import sys
import traceback
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_dashboard_final():
    """Test DashboardViewMaritime final"""
    print("🚀 TEST DASHBOARDVIEW FINAL")
    print("=" * 50)
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Dashboard Final Test")
        
        print("✅ QApplication créé")
        
        # Test import DashboardViewMaritime
        print("🔄 Import DashboardViewMaritime...")
        from hrneowave.gui.views.dashboard_view import DashboardViewMaritime
        print("✅ DashboardViewMaritime importé")
        
        # Test création DashboardViewMaritime
        print("🔄 Création DashboardViewMaritime...")
        dashboard_view = DashboardViewMaritime(parent=None)
        print("✅ DashboardViewMaritime créée")
        
        # Test affichage
        print("🔄 Affichage DashboardViewMaritime...")
        dashboard_view.show()
        
        visible = dashboard_view.isVisible()
        print(f"✅ DashboardViewMaritime visible: {visible}")
        
        if visible:
            print("🎉 SUCCÈS: DashboardViewMaritime visible!")
            
            # Maintenir ouvert 5 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(5000)
            
            print("🔄 Maintien ouvert 5 secondes...")
            exit_code = app.exec()
            print(f"✅ Test terminé (code: {exit_code})")
            return True
        else:
            print("❌ PROBLÈME: DashboardViewMaritime non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_dashboard_final() else 1)
