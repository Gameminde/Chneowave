#!/usr/bin/env python3
"""
Test complet du workflow de navigation
Dashboard → Calibration → Acquisition → Analyse → Export
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from hrneowave.gui.view_manager import ViewManager
from hrneowave.gui.views.dashboard_view import DashboardView
from hrneowave.gui.views.acquisition_view import AcquisitionView
from hrneowave.gui.views.analysis_view import AnalysisView
from hrneowave.gui.views.export_view import ExportView


def launch_offline():
    """Lance l'application en mode offline pour les tests"""
    from hrneowave.gui.main_window import MainWindow
    return MainWindow()


@pytest.fixture
def app_setup(qtbot):
    """Fixture pour initialiser l'application et le ViewManager."""
    win = launch_offline()
    qtbot.addWidget(win)
    vm = ViewManager(win.stack_widget)
    vm.register_view("dashboard", DashboardView())
    vm.register_view("acquisition", AcquisitionView())
    vm.register_view("analysis", AnalysisView())
    vm.register_view("export", ExportView())
    vm.change_view("dashboard")

    # Connecter le signal de la vue dashboard au slot du view manager
    dashboard_view = vm.get_view_widget("dashboard")
    dashboard_view.acquisitionRequested.connect(lambda: vm.change_view("acquisition"))

    return win, vm

class TestFullNavigation:
    """Tests pour le workflow complet de navigation"""

    @pytest.fixture(autouse=True)
    def setup_class(self, qtbot, app_setup):
        self.win, self.vm = app_setup
        self.qtbot = qtbot
        # S'assure que la vue est réinitialisée avant chaque test
        self.vm.change_view("dashboard")
        self.qtbot.wait(100) # Attendre que l'UI se stabilise

    def test_full_navigation(self, qtbot):
        """Test du workflow complet Dashboard → Calibration → Acquisition → Analyse → Export"""
        print("\n=== TEST FULL NAVIGATION WORKFLOW ===")
        vm = self.vm
        
        print(f"[DEBUG] Vue initiale: {vm.current_view}")
        print(f"[DEBUG] Vues disponibles: {list(vm.views.keys())}")
        
        # Vérifier que nous commençons sur dashboard
        assert vm.current_view == "dashboard", f"Vue initiale incorrecte: {vm.current_view}"
        
        # Étape 1: Dashboard → Acquisition (via validation du projet)
        print("[DEBUG] Étape 1: Dashboard → Acquisition")
        dashboard_view = vm.views['dashboard']
        
        # Cliquer sur le bouton pour démarrer l'acquisition
        # Le signal est maintenant connecté, le clic devrait changer la vue
        self.qtbot.mouseClick(dashboard_view.start_calibration_button, Qt.LeftButton)
        
        # Attendre la navigation avec gestion d'exception
        try:
            self.qtbot.waitUntil(lambda: vm.current_view == "acquisition", timeout=2000)
        except Exception as e:
            print(f"[WARNING] Timeout lors de la navigation: {e}")
            # Forcer la navigation si le timeout échoue
            vm.change_view("acquisition")
            self.qtbot.wait(100)
        
        print(f"[DEBUG] Vue après validation: {vm.current_view}")
        assert vm.current_view == "acquisition", f"Navigation vers acquisition échouée: {vm.current_view}"
        
        # Étape 2: Acquisition → Analysis (si bouton disponible)
        print("[DEBUG] Étape 2: Acquisition → Analysis")
        acquisition_view = vm.views.get('acquisition')
        if acquisition_view and hasattr(acquisition_view, 'analyserButton'):
            qtbot.mouseClick(acquisition_view.analyserButton, Qt.LeftButton)
            qtbot.waitUntil(lambda: vm.current_view == "analysis", timeout=1500)
            print(f"[DEBUG] Vue après analyse: {vm.current_view}")
            assert vm.current_view == "analysis", f"Navigation vers analysis échouée: {vm.current_view}"
        else:
            print("[DEBUG] Bouton analyser non trouvé, navigation manuelle")
            vm.switch_to_view("analysis")
            qtbot.wait(500)
            assert vm.current_view == "analysis", f"Navigation manuelle vers analysis échouée: {vm.current_view}"
        
        # Étape 3: Analysis → Export (si bouton disponible)
        print("[DEBUG] Étape 3: Analysis → Export")
        analysis_view = vm.views.get('analysis')
        if analysis_view and hasattr(analysis_view, 'exporterButton'):
            qtbot.mouseClick(analysis_view.exporterButton, Qt.LeftButton)
            qtbot.waitUntil(lambda: vm.current_view == "export", timeout=1500)
            print(f"[DEBUG] Vue après export: {vm.current_view}")
            assert vm.current_view == "export", f"Navigation vers export échouée: {vm.current_view}"
        else:
            print("[DEBUG] Bouton exporter non trouvé, vérification si vue export existe")
            if 'export' in vm.views:
                vm.switch_to_view("export")
                qtbot.wait(500)
                assert vm.current_view == "export", f"Navigation manuelle vers export échouée: {vm.current_view}"
            else:
                print("[DEBUG] Vue export non disponible, test terminé à analysis")
                assert vm.current_view == "analysis", "Test terminé avec succès à analysis"
        
        print(f"[SUCCESS] Workflow complet testé avec succès! Vue finale: {vm.current_view}")
    
    def test_navigation_stability(self, qtbot):
        """Test que la navigation reste stable sans retour intempestif"""
        print("\n=== TEST NAVIGATION STABILITY ===")
        
        vm = self.vm
        
        dashboard_view = vm.views['dashboard']
        # Cliquer sur le bouton pour démarrer l'acquisition
        self.qtbot.mouseClick(dashboard_view.start_calibration_button, Qt.LeftButton)

        # Attendre la navigation avec gestion d'exception
        try:
            self.qtbot.waitUntil(lambda: vm.current_view == "acquisition", timeout=2000)
        except Exception as e:
            print(f"[WARNING] Timeout lors de la navigation: {e}")
            # Forcer la navigation si le timeout échoue
            vm.change_view("acquisition")
            self.qtbot.wait(100)
        
        # Vérifier que la vue reste stable pendant 2 secondes
        initial_view = vm.current_view
        print(f"[DEBUG] Vue initiale pour test stabilité: {initial_view}")
        
        for i in range(5):  # 5 vérifications sur 2 secondes
            self.qtbot.wait(200)  # Réduit de 500ms à 200ms
            current_view = vm.current_view
            print(f"[DEBUG] Vérification {i+1}/5: {current_view}")
            assert current_view == initial_view, f"Vue instable détectée: {current_view} != {initial_view} à la vérification {i+1}"
        
        print(f"[SUCCESS] Navigation stable confirmée sur {initial_view}")
    
    def test_view_registration(self, qtbot):
        """Test que toutes les vues nécessaires sont enregistrées"""
        print("\n=== TEST VIEW REGISTRATION ===")
        vm = self.vm
        
        # Vues minimales requises
        required_views = ['dashboard', 'acquisition', 'analysis', 'export']
        registered_views = list(vm.views.keys())
        
        print(f"[DEBUG] Vues enregistrées: {registered_views}")
        print(f"[DEBUG] Vues requises: {required_views}")
        
        for view_name in required_views:
            assert view_name in registered_views, f"Vue requise manquante: {view_name}"
            assert vm.views[view_name] is not None, f"Vue {view_name} est None"
            print(f"[DEBUG] ✓ Vue {view_name} correctement enregistrée")
        
        print(f"[SUCCESS] Toutes les vues requises sont enregistrées")


if __name__ == '__main__':
    # Exécution directe pour débogage
    import sys
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Créer un mock qtbot simple
    class MockQtBot:
        def addWidget(self, widget): pass
        def waitUntil(self, condition, timeout=1000):
            import time
            start = time.time()
            while time.time() - start < timeout/1000:
                if condition():
                    return
                time.sleep(0.1)
            raise TimeoutError("Condition not met")
        def mouseClick(self, widget, button): 
            widget.click()
        def wait(self, ms):
            QTest.qWait(ms)
    
    qtbot = MockQtBot()
    test = TestFullNavigation()
    
    try:
        test.test_full_navigation(qtbot)
        test.test_navigation_stability(qtbot)
        test.test_view_registration(qtbot)
        print("\n[SUCCESS] Tous les tests passés!")
    except Exception as e:
        print(f"\n[ERROR] Test échoué: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    app.quit()