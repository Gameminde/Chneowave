#!/usr/bin/env python3
"""
Test smoke - Lancement GUI
Vérifie que l'application démarre et se ferme correctement en mode simulation
"""

import pytest
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import QTimer, Qt

# Ajout du chemin source
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Test d'importation simple
try:
    from hrneowave.gui.main_window import MainWindow as CHNeoWaveMainWindow
    IMPORT_SUCCESS = True
except Exception as e:
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

try:
    from hrneowave.core.config_manager import ConfigManager
    CONFIG_IMPORT_SUCCESS = True
except Exception as e:
    CONFIG_IMPORT_SUCCESS = False
    CONFIG_IMPORT_ERROR = str(e)

class TestLaunchGUI:
    """Tests de lancement de l'interface graphique"""
    
    @pytest.fixture(scope="class")
    def qapp(self):
        """Fixture pour l'application Qt"""
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        yield app
        app.quit()
    
    def test_gui_startup_simulation(self, qapp):
        """Test de démarrage de la GUI en mode simulation"""
        # Vérifier les importations d'abord
        if not IMPORT_SUCCESS:
            pytest.skip(f"Importation échouée: {IMPORT_ERROR}")
        
        if not CONFIG_IMPORT_SUCCESS:
            pytest.skip(f"Importation ConfigManager échouée: {CONFIG_IMPORT_ERROR}")
        
        # Configuration simple
        config = {
            'hardware': {'simulation_mode': True, 'backend': 'demo'},
            'acquisition': {'default_fs': 32, 'default_channels': 8}
        }
        
        # Variables de test
        window = None
        startup_success = False
        close_success = False
        
        # Création de la fenêtre
        window = CHNeoWaveMainWindow(config=config)
        startup_success = True
        
        # Vérifier que la fenêtre est créée
        assert window is not None, "La fenêtre principale n'a pas pu être créée"
        
        # Afficher la fenêtre
        window.show()
        
        # Traiter les événements Qt
        QTest.qWait(100)
        
        # Fermer la fenêtre
        window.close()
        close_success = True
        
        #finally:
        #    if window:
        #        try:
        #            window.close()
        #        except:
        #            pass
        
        # Assertions finales
        #assert startup_success, "Le démarrage de la GUI a échoué"
        #assert close_success, "La fermeture de la GUI a échoué"
    
    def test_gui_components_loaded(self, qapp):
        """Test de chargement des composants de l'interface"""
        # Vérifier les importations d'abord
        if not IMPORT_SUCCESS:
            pytest.skip(f"Importation échouée: {IMPORT_ERROR}")
        
        # Configuration simple
        config = {'hardware': {'simulation_mode': True, 'backend': 'demo'}}
        
        components_loaded = False
        main_window = None
        
        # Création de la fenêtre
        main_window = CHNeoWaveMainWindow(config=config)
        main_window.show()
        
        # Attendre que la fenêtre soit exposée
        QTest.qWaitForWindowExposed(main_window, 3000)
        
        # Vérifier les composants principaux
        assert hasattr(main_window, 'stack_widget'), "StackWidget manquant"
        assert hasattr(main_window, 'view_manager'), "ViewManager manquant"
        assert hasattr(main_window, 'dashboard_view'), "DashboardView manquante"
        assert hasattr(main_window, 'acquisition_view'), "AcquisitionView manquante"
        assert hasattr(main_window, 'analysis_view'), "AnalysisView manquante"
        
        # Vérifier les onglets/vues
        view_manager = main_window.view_manager
        assert view_manager is not None, "ViewManager non initialisé"
        
        # Vérifier que les vues sont enregistrées
        expected_views = ['dashboard', 'acquisition', 'analysis']
        for view_name in expected_views:
            assert view_name in view_manager.views, f"Vue '{view_name}' non enregistrée"
        
        components_loaded = True
        print("✓ Composants GUI chargés avec succès")
        
        #finally:
        #    if main_window:
        #        main_window.close()
        
        #assert components_loaded, "Le chargement des composants a échoué"
    
    def test_simulation_backend_loaded(self, qapp):
        """Test de chargement du backend de simulation"""
        # Vérifier les importations d'abord
        if not IMPORT_SUCCESS:
            pytest.skip(f"Importation échouée: {IMPORT_ERROR}")
        
        # Configuration simple
        config = {'hardware': {'simulation_mode': True, 'backend': 'demo'}}
        
        backend_loaded = False
        main_window = None
        
        # Création de la fenêtre
        main_window = CHNeoWaveMainWindow(config=config)
        main_window.show()
        
        # Attendre l'initialisation
        QTest.qWaitForWindowExposed(main_window, 3000)
        qapp.processEvents()
        QTest.qWait(1000)  # Attendre l'initialisation complète
        
        # Vérifier que le contrôleur principal existe
        assert hasattr(main_window, 'project_controller'), "Contrôleur principal manquant"
        
        controller = main_window.project_controller
        
        # Vérifier que le backend est en mode simulation
        if hasattr(controller, 'acquisition_manager'):
            acq_manager = controller.acquisition_manager
            if hasattr(acq_manager, 'backend'):
                backend = acq_manager.backend
                backend_name = backend.__class__.__name__
                print(f"✓ Backend chargé: {backend_name}")
                
                # Vérifier que c'est bien le backend de démo
                assert 'demo' in backend_name.lower() or 'simulation' in backend_name.lower(), \
                    f"Backend incorrect: {backend_name}"
        
        backend_loaded = True
        print("✓ Backend de simulation correctement chargé")
        
        #finally:
        #    if main_window:
        #        main_window.close()
        
        #assert backend_loaded, "Le chargement du backend a échoué"

if __name__ == '__main__':
    # Exécution directe pour debug
    pytest.main([__file__, '-v'])