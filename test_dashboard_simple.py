#!/usr/bin/env python3
"""
Test de DashboardView simplifié pour identifier le problème.
"""

import sys
import traceback
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest

def test_dashboard_components():
    """Test les composants de DashboardView un par un."""
    print("=== Test des composants DashboardView ===\n")
    
    try:
        # Créer l'application Qt
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✓ QApplication créée")
        
        # Test 1: Import PhiCard
        print("\n1. Test PhiCard...")
        from hrneowave.gui.components.phi_card import PhiCard
        phi_card = PhiCard("Test", "0%", size="sm")
        phi_card.show()
        QTest.qWait(500)
        phi_card.close()
        print("✓ PhiCard OK")
        
        # Test 2: Import PerformanceMonitor
        print("\n2. Test PerformanceMonitor...")
        from hrneowave.core.performance_monitor import PerformanceMonitor
        perf_monitor = PerformanceMonitor()
        print("✓ PerformanceMonitor créé")
        
        # Test 3: Démarrage du monitoring
        print("\n3. Test démarrage monitoring...")
        perf_monitor.start_monitoring()
        print("✓ Monitoring démarré")
        QTest.qWait(1000)
        
        # Test 4: Arrêt du monitoring
        print("\n4. Test arrêt monitoring...")
        perf_monitor.stop_monitoring()
        print("✓ Monitoring arrêté")
        
        # Test 5: Import PerformanceWidget
        print("\n5. Test PerformanceWidget...")
        from hrneowave.gui.components.performance_widget import PerformanceWidget
        perf_widget = PerformanceWidget()
        print("✓ PerformanceWidget créé")
        
        # Test 6: pyqtgraph
        print("\n6. Test pyqtgraph...")
        import pyqtgraph as pg
        plot_widget = pg.PlotWidget()
        plot_widget.show()
        QTest.qWait(500)
        plot_widget.close()
        print("✓ pyqtgraph OK")
        
        # Test 7: DashboardView sans monitoring
        print("\n7. Test DashboardView modifiée...")
        
        class SimpleDashboardView(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setObjectName("SimpleDashboardView")
                
                # Layout simple
                layout = QVBoxLayout(self)
                label = QLabel("Dashboard Test")
                layout.addWidget(label)
                
                # Créer les cartes sans monitoring
                self.buffer_card = PhiCard("Utilisation Buffer", "0%", size="sm")
                self.cpu_card = PhiCard("Charge CPU", "0%", size="sm")
                layout.addWidget(self.buffer_card)
                layout.addWidget(self.cpu_card)
        
        simple_dashboard = SimpleDashboardView()
        simple_dashboard.show()
        QTest.qWait(1000)
        print("✓ SimpleDashboardView OK")
        
        # Test 8: DashboardView originale
        print("\n8. Test DashboardView originale...")
        from hrneowave.gui.views.dashboard_view import DashboardView
        
        print("   Création...")
        dashboard = DashboardView()
        print("   ✓ Créée")
        
        print("   Affichage...")
        dashboard.show()
        print("   ✓ Affichée")
        
        print("   Attente...")
        QTest.qWait(2000)
        print("   ✓ Stable")
        
        print("   Fermeture...")
        dashboard.close()
        print("   ✓ Fermée")
        
        simple_dashboard.close()
        
        print("\n=== Tous les tests réussis ===\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Erreur durant le test: {e}")
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer
        if app:
            app.quit()

if __name__ == "__main__":
    success = test_dashboard_components()
    print(f"\nRésultat final: {'SUCCÈS' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)