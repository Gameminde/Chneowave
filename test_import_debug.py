#!/usr/bin/env python3
"""
Test d'importation pour identifier le problème de crash.
"""

import sys
import traceback

def test_imports():
    """Test les imports un par un pour identifier le problème."""
    print("=== Test d'importation des modules ===\n")
    
    try:
        print("1. Import PySide6...")
        from PySide6.QtWidgets import QApplication, QWidget
        from PySide6.QtCore import Qt, Signal
        print("   ✓ PySide6 OK")
    except Exception as e:
        print(f"   ✗ Erreur PySide6: {e}")
        return False
    
    try:
        print("2. Import PhiCard...")
        from hrneowave.gui.components.phi_card import PhiCard
        print("   ✓ PhiCard OK")
    except Exception as e:
        print(f"   ✗ Erreur PhiCard: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("3. Import PerformanceMonitor...")
        from hrneowave.core.performance_monitor import PerformanceMonitor
        print("   ✓ PerformanceMonitor OK")
    except Exception as e:
        print(f"   ✗ Erreur PerformanceMonitor: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("4. Import PerformanceWidget...")
        from hrneowave.gui.components.performance_widget import PerformanceWidget
        print("   ✓ PerformanceWidget OK")
    except Exception as e:
        print(f"   ✗ Erreur PerformanceWidget: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("5. Import pyqtgraph...")
        import pyqtgraph as pg
        print("   ✓ pyqtgraph OK")
    except Exception as e:
        print(f"   ✗ Erreur pyqtgraph: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("6. Import DashboardView...")
        from hrneowave.gui.views.dashboard_view import DashboardView
        print("   ✓ DashboardView OK")
    except Exception as e:
        print(f"   ✗ Erreur DashboardView: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("7. Test création QApplication...")
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("   ✓ QApplication OK")
    except Exception as e:
        print(f"   ✗ Erreur QApplication: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("8. Test création DashboardView...")
        dashboard = DashboardView()
        print("   ✓ Création DashboardView OK")
    except Exception as e:
        print(f"   ✗ Erreur création DashboardView: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("9. Test show DashboardView...")
        dashboard.show()
        print("   ✓ Show DashboardView OK")
    except Exception as e:
        print(f"   ✗ Erreur show DashboardView: {e}")
        traceback.print_exc()
        return False
    
    print("\n=== Tous les tests d'importation réussis ===\n")
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("Le problème n'est pas dans les imports.")
    else:
        print("Problème d'importation détecté.")
    
    sys.exit(0 if success else 1)