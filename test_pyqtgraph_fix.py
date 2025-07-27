#!/usr/bin/env python3
"""
Test pour reproduire et corriger le problème pyqtgraph dans DashboardView.
"""

import sys
import traceback
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest
import pyqtgraph as pg

def test_pyqtgraph_scenarios():
    """Test différents scénarios d'utilisation de pyqtgraph."""
    print("=== Test PyQtGraph Scenarios ===\n")
    
    try:
        # Créer l'application Qt
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✓ QApplication créée")
        
        # Test 1: PlotWidget simple
        print("\n1. Test PlotWidget simple...")
        try:
            plot1 = pg.PlotWidget()
            plot1.show()
            QTest.qWait(500)
            plot1.close()
            plot1.deleteLater()
            print("✓ PlotWidget simple OK")
        except Exception as e:
            print(f"✗ PlotWidget simple échoué: {e}")
            return False
        
        # Test 2: PlotWidget avec parent
        print("\n2. Test PlotWidget avec parent...")
        try:
            parent_widget = QWidget()
            parent_widget.show()
            
            plot2 = pg.PlotWidget(parent=parent_widget)
            layout = QVBoxLayout(parent_widget)
            layout.addWidget(plot2)
            
            QTest.qWait(500)
            parent_widget.close()
            parent_widget.deleteLater()
            print("✓ PlotWidget avec parent OK")
        except Exception as e:
            print(f"✗ PlotWidget avec parent échoué: {e}")
            return False
        
        # Test 3: PlotWidget dans showEvent (simulation DashboardView)
        print("\n3. Test PlotWidget dans showEvent...")
        try:
            class TestWidget(QWidget):
                def __init__(self):
                    super().__init__()
                    self.plot_widget = None
                    self.layout = QVBoxLayout(self)
                
                def showEvent(self, event):
                    super().showEvent(event)
                    if self.plot_widget is None:
                        # Configuration pyqtgraph pour éviter les conflits
                        pg.setConfigOptions(antialias=True, useOpenGL=False)
                        
                        self.plot_widget = pg.PlotWidget(parent=self)
                        self.plot_widget.setBackground('transparent')
                        self.layout.addWidget(self.plot_widget)
                        print("   PlotWidget créé dans showEvent")
                
                def closeEvent(self, event):
                    if self.plot_widget:
                        self.plot_widget.close()
                        self.plot_widget.deleteLater()
                        self.plot_widget = None
                    super().closeEvent(event)
            
            test_widget = TestWidget()
            test_widget.show()
            QTest.qWait(1000)
            test_widget.close()
            test_widget.deleteLater()
            print("✓ PlotWidget dans showEvent OK")
        except Exception as e:
            print(f"✗ PlotWidget dans showEvent échoué: {e}")
            return False
        
        # Test 4: Configuration pyqtgraph optimisée
        print("\n4. Test configuration pyqtgraph optimisée...")
        try:
            # Configuration recommandée pour éviter les crashes
            pg.setConfigOptions(
                antialias=True,
                useOpenGL=False,  # Désactiver OpenGL pour éviter les conflits
                enableExperimental=False,
                crashWarning=True
            )
            
            plot4 = pg.PlotWidget()
            plot4.setBackground('transparent')
            plot_item = plot4.getPlotItem()
            plot_item.setTitle("Test Optimisé")
            plot_item.setLabel('left', 'Y')
            plot_item.setLabel('bottom', 'X')
            
            plot4.show()
            QTest.qWait(500)
            plot4.close()
            plot4.deleteLater()
            print("✓ Configuration optimisée OK")
        except Exception as e:
            print(f"✗ Configuration optimisée échouée: {e}")
            return False
        
        # Test 5: DashboardView corrigée
        print("\n5. Test DashboardView avec correction...")
        try:
            from hrneowave.gui.views.dashboard_view import DashboardView
            
            # Configuration pyqtgraph avant création
            pg.setConfigOptions(
                antialias=True,
                useOpenGL=False,
                enableExperimental=False,
                crashWarning=True
            )
            
            dashboard = DashboardView()
            dashboard.show()
            QTest.qWait(2000)
            dashboard.close()
            dashboard.deleteLater()
            print("✓ DashboardView corrigée OK")
        except Exception as e:
            print(f"✗ DashboardView corrigée échouée: {e}")
            traceback.print_exc()
            return False
        
        print("\n=== Tous les tests pyqtgraph réussis ===\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Erreur générale: {e}")
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer
        if app:
            app.quit()

if __name__ == "__main__":
    success = test_pyqtgraph_scenarios()
    print(f"\nRésultat final: {'SUCCÈS' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)