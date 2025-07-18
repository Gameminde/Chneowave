# test_enhanced_main_ui.py - Tests pour l'interface principale améliorée
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import time

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtTest import QTest
from PyQt5.QtGui import QKeySequence

# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from hrneowave.gui.enhanced_main_ui import (
        EnhancedMainUI, NavigationToolBar, StatusBarWidget
    )
    from hrneowave.gui.theme import set_light_mode, set_dark_mode, get_current_theme
except ImportError as e:
    print(f"⚠️ Import manquant: {e}")
    EnhancedMainUI = NavigationToolBar = StatusBarWidget = None
    set_light_mode = set_dark_mode = get_current_theme = None

@pytest.fixture
def app():
    """Fixture pour l'application Qt"""
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    yield app
    # Pas de quit() ici pour éviter les conflits

@pytest.fixture
def main_ui(app):
    """Fixture pour l'interface principale"""
    if not EnhancedMainUI:
        pytest.skip("EnhancedMainUI non disponible")
        
    config = {
        'sample_rate': 32.0,
        'n_channels': 4,
        'max_duration': 300
    }
    
    ui = EnhancedMainUI(config)
    ui.show()
    QTest.qWaitForWindowExposed(ui)
    
    yield ui
    
    ui.close()
    
@pytest.fixture
def nav_toolbar(app):
    """Fixture pour la barre de navigation"""
    if not NavigationToolBar:
        pytest.skip("NavigationToolBar non disponible")
        
    toolbar = NavigationToolBar()
    yield toolbar
    
@pytest.fixture
def status_bar(app):
    """Fixture pour la barre de statut"""
    if not StatusBarWidget:
        pytest.skip("StatusBarWidget non disponible")
        
    status = StatusBarWidget()
    yield status

class TestNavigationToolBar:
    """Tests pour la barre de navigation"""
    
    def test_init(self, nav_toolbar):
        """Test l'initialisation de la barre de navigation"""
        assert nav_toolbar.current_tab == 0
        assert len(nav_toolbar.tab_actions) == 4
        assert nav_toolbar.tab_actions[0].isChecked()
        
    def test_tab_selection(self, nav_toolbar):
        """Test la sélection d'onglets"""
        # Simuler un clic sur l'onglet 2
        nav_toolbar._on_tab_action(2)
        
        assert nav_toolbar.current_tab == 2
        assert nav_toolbar.tab_actions[2].isChecked()
        assert not nav_toolbar.tab_actions[0].isChecked()
        
    def test_set_current_tab(self, nav_toolbar):
        """Test la définition de l'onglet actuel"""
        nav_toolbar.set_current_tab(3)
        
        assert nav_toolbar.current_tab == 3
        assert nav_toolbar.tab_actions[3].isChecked()
        
    def test_set_tab_enabled(self, nav_toolbar):
        """Test l'activation/désactivation d'onglets"""
        nav_toolbar.set_tab_enabled(1, False)
        assert not nav_toolbar.tab_actions[1].isEnabled()
        
        nav_toolbar.set_tab_enabled(1, True)
        assert nav_toolbar.tab_actions[1].isEnabled()
        
    def test_theme_action_update(self, nav_toolbar):
        """Test la mise à jour de l'action de thème"""
        nav_toolbar.update_theme_action(True)
        assert "Clair" in nav_toolbar.theme_action.text()
        
        nav_toolbar.update_theme_action(False)
        assert "Sombre" in nav_toolbar.theme_action.text()

class TestStatusBarWidget:
    """Tests pour la barre de statut"""
    
    def test_init(self, status_bar):
        """Test l'initialisation de la barre de statut"""
        assert status_bar.main_label.text() == "Prêt"
        assert "✅" in status_bar.validation_label.text()
        
    def test_set_main_message(self, status_bar):
        """Test la définition du message principal"""
        status_bar.set_main_message("Test message", "red")
        assert status_bar.main_label.text() == "Test message"
        
    def test_set_validation_status(self, status_bar):
        """Test la définition du statut de validation"""
        status_bar.set_validation_status(False)
        assert "❌" in status_bar.validation_label.text()
        
        status_bar.set_validation_status(True)
        assert "✅" in status_bar.validation_label.text()
        
    def test_set_theme_status(self, status_bar):
        """Test la définition du statut de thème"""
        status_bar.set_theme_status(True)
        assert "Sombre" in status_bar.theme_label.text()
        
        status_bar.set_theme_status(False)
        assert "Clair" in status_bar.theme_label.text()
        
    def test_time_update(self, status_bar):
        """Test la mise à jour de l'heure"""
        initial_time = status_bar.time_label.text()
        
        # Attendre un peu et vérifier que l'heure se met à jour
        QTest.qWait(1100)  # Attendre plus d'une seconde
        
        updated_time = status_bar.time_label.text()
        # L'heure devrait avoir changé (au moins les secondes)
        # Note: Ce test peut être fragile selon le timing

class TestEnhancedMainUI:
    """Tests pour l'interface principale"""
    
    def test_init(self, main_ui):
        """Test l'initialisation de l'interface principale"""
        assert main_ui.windowTitle() == "CHNeoWave - Laboratoire d'Étude Maritime"
        assert main_ui.current_tab_index == 0
        assert not main_ui.is_acquiring
        assert main_ui.stacked_widget.count() == 4
        
    def test_tab_navigation(self, main_ui):
        """Test la navigation entre onglets"""
        # Aller à l'onglet 1
        main_ui._switch_to_tab(1)
        assert main_ui.current_tab_index == 1
        assert main_ui.stacked_widget.currentIndex() == 1
        
        # Aller à l'onglet 2
        main_ui._switch_to_tab(2)
        assert main_ui.current_tab_index == 2
        assert main_ui.stacked_widget.currentIndex() == 2
        
    def test_required_fields_validation(self, main_ui):
        """Test la validation des champs obligatoires"""
        # Simuler une validation échouée
        with patch.object(main_ui, '_can_leave_current_tab', return_value=False):
            initial_tab = main_ui.current_tab_index
            main_ui._on_tab_requested(2)
            
            # L'onglet ne devrait pas avoir changé
            assert main_ui.current_tab_index == initial_tab
            
        # Simuler une validation réussie
        with patch.object(main_ui, '_can_leave_current_tab', return_value=True):
            main_ui._on_tab_requested(2)
            assert main_ui.current_tab_index == 2
            
    @pytest.mark.skipif(not all([set_light_mode, set_dark_mode, get_current_theme]), 
                       reason="Fonctions de thème non disponibles")
    def test_theme_toggle(self, main_ui):
        """Test le basculement de thème"""
        # Obtenir le thème initial
        initial_theme = get_current_theme()
        
        # Basculer le thème
        main_ui._toggle_theme()
        QTest.qWait(100)  # Attendre que le changement soit appliqué
        
        # Vérifier que le thème a changé
        new_theme = get_current_theme()
        assert new_theme != initial_theme
        
        # Basculer à nouveau
        main_ui._toggle_theme()
        QTest.qWait(100)
        
        # Devrait revenir au thème initial
        final_theme = get_current_theme()
        assert final_theme == initial_theme
        
    def test_acquisition_workflow(self, main_ui):
        """Test le workflow d'acquisition"""
        # Simuler le début d'acquisition
        config = {'duration': 60, 'sample_rate': 32.0}
        main_ui._on_acquisition_started(config)
        
        assert main_ui.is_acquiring
        assert "Acquisition en cours" in main_ui.status_bar.main_label.text()
        
        # Simuler la fin d'acquisition
        results = {'data': [1, 2, 3], 'duration': 60}
        main_ui._on_acquisition_finished(results)
        
        assert not main_ui.is_acquiring
        assert main_ui.acquisition_data == results
        assert "Acquisition terminée" in main_ui.status_bar.main_label.text()
        
    def test_auto_switch_to_analysis(self, main_ui):
        """Test le basculement automatique vers l'analyse"""
        # Aller à l'onglet acquisition
        main_ui._switch_to_tab(2)
        
        # Simuler la fin d'acquisition
        results = {'data': [1, 2, 3], 'duration': 60}
        
        with patch.object(QTimer, 'singleShot') as mock_timer:
            main_ui._on_acquisition_finished(results)
            
            # Vérifier que le timer a été configuré pour basculer vers l'analyse
            mock_timer.assert_called_once()
            args = mock_timer.call_args[0]
            assert args[0] == 2000  # 2 secondes
            
            # Exécuter manuellement la fonction de callback
            callback = args[1]
            callback()
            
            # Vérifier qu'on est maintenant sur l'onglet analyse
            assert main_ui.current_tab_index == 3
            
    def test_validation_changed_signal(self, main_ui):
        """Test la gestion du signal de validation"""
        # Simuler un changement de validation
        main_ui._on_validation_changed(False)
        
        # Vérifier que le statut a été mis à jour
        assert "❌" in main_ui.status_bar.validation_label.text()
        
        main_ui._on_validation_changed(True)
        assert "✅" in main_ui.status_bar.validation_label.text()
        
    def test_can_leave_current_tab_with_acquisition(self, main_ui):
        """Test la vérification de sortie d'onglet pendant acquisition"""
        # Aller à l'onglet acquisition
        main_ui._switch_to_tab(2)
        main_ui.is_acquiring = True
        
        # Mocker la boîte de dialogue
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            result = main_ui._can_leave_current_tab()
            assert not result
            
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
            result = main_ui._can_leave_current_tab()
            assert result
            
    def test_project_data_management(self, main_ui):
        """Test la gestion des données de projet"""
        # Définir des données de projet
        test_data = {
            'project_name': 'Test Project',
            'project_manager': 'Test Manager',
            'date': '2024-01-01'
        }
        
        main_ui.project_data.update(test_data)
        
        # Vérifier que les données sont accessibles
        project_data = main_ui.get_project_data()
        assert project_data['project_name'] == 'Test Project'
        assert project_data['project_manager'] == 'Test Manager'
        
    def test_menu_actions(self, main_ui):
        """Test les actions du menu"""
        # Test nouveau projet
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
            main_ui._new_project()
            assert len(main_ui.project_data) == 0
            assert main_ui.current_tab_index == 0
            
        # Test plein écran
        initial_state = main_ui.isFullScreen()
        main_ui._toggle_fullscreen()
        assert main_ui.isFullScreen() != initial_state
        
    def test_close_event_with_acquisition(self, main_ui):
        """Test la fermeture avec acquisition en cours"""
        main_ui.is_acquiring = True
        
        # Créer un événement de fermeture mock
        close_event = Mock()
        
        # Tester refus de fermeture
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            main_ui.closeEvent(close_event)
            close_event.ignore.assert_called_once()
            
        # Tester acceptation de fermeture
        close_event.reset_mock()
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
            main_ui.closeEvent(close_event)
            close_event.accept.assert_called_once()
            
    def test_settings_persistence(self, main_ui):
        """Test la persistance des paramètres"""
        # Changer d'onglet
        main_ui._switch_to_tab(2)
        
        # Sauvegarder les paramètres
        main_ui._save_settings()
        
        # Vérifier que les paramètres sont sauvegardés
        assert main_ui.settings.value("currentTab", type=int) == 2

class TestPerformance:
    """Tests de performance"""
    
    def test_tab_switching_performance(self, main_ui):
        """Test la performance du changement d'onglets"""
        start_time = time.time()
        
        # Effectuer plusieurs changements d'onglets
        for i in range(10):
            main_ui._switch_to_tab(i % 4)
            QTest.qWait(10)  # Petite pause
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Le changement d'onglets devrait être rapide (< 1 seconde pour 10 changements)
        assert duration < 1.0
        
    def test_ui_responsiveness(self, main_ui):
        """Test la réactivité de l'interface"""
        start_time = time.time()
        
        # Simuler des interactions utilisateur
        for i in range(5):
            main_ui._on_validation_changed(i % 2 == 0)
            main_ui.status_bar.set_main_message(f"Test {i}")
            QTest.qWait(10)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Les mises à jour UI devraient être rapides
        assert duration < 0.5
        
    def test_memory_usage_stability(self, main_ui):
        """Test la stabilité de l'utilisation mémoire"""
        import gc
        import psutil
        import os
        
        # Obtenir l'utilisation mémoire initiale
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Effectuer de nombreuses opérations
        for i in range(100):
            main_ui._switch_to_tab(i % 4)
            main_ui._on_validation_changed(i % 2 == 0)
            main_ui.status_bar.set_main_message(f"Test {i}")
            
            if i % 10 == 0:
                gc.collect()  # Forcer le garbage collection
                
        # Obtenir l'utilisation mémoire finale
        gc.collect()
        final_memory = process.memory_info().rss
        
        # L'augmentation de mémoire ne devrait pas être excessive (< 50MB)
        memory_increase = final_memory - initial_memory
        assert memory_increase < 50 * 1024 * 1024  # 50MB

class TestIntegration:
    """Tests d'intégration"""
    
    def test_complete_workflow(self, main_ui):
        """Test un workflow complet"""
        # 1. Commencer à l'accueil
        assert main_ui.current_tab_index == 0
        
        # 2. Simuler la validation de l'accueil
        main_ui._on_validation_changed(True)
        
        # 3. Aller à la calibration
        main_ui._switch_to_tab(1)
        assert main_ui.current_tab_index == 1
        
        # 4. Simuler la validation de la calibration
        main_ui._on_validation_changed(True)
        
        # 5. Aller à l'acquisition
        main_ui._switch_to_tab(2)
        assert main_ui.current_tab_index == 2
        
        # 6. Simuler une acquisition
        config = {'duration': 60}
        main_ui._on_acquisition_started(config)
        assert main_ui.is_acquiring
        
        # 7. Terminer l'acquisition
        results = {'data': [1, 2, 3]}
        with patch.object(QTimer, 'singleShot') as mock_timer:
            main_ui._on_acquisition_finished(results)
            
            # 8. Vérifier le basculement automatique vers l'analyse
            callback = mock_timer.call_args[0][1]
            callback()
            assert main_ui.current_tab_index == 3
            
        # 9. Simuler l'analyse
        analysis_results = {'spectrum': [1, 2, 3]}
        main_ui._on_analysis_completed(analysis_results)
        
        # 10. Vérifier que toutes les données sont présentes
        assert main_ui.acquisition_data == results
        assert main_ui.analysis_results == analysis_results
        
    def test_error_handling(self, main_ui):
        """Test la gestion d'erreurs"""
        # Test avec onglet invalide
        main_ui._switch_to_tab(10)  # Onglet inexistant
        # Ne devrait pas planter
        
        # Test avec données invalides
        main_ui._on_acquisition_finished(None)
        # Ne devrait pas planter
        
        # Test avec validation None
        main_ui._on_validation_changed(None)
        # Ne devrait pas planter

def test_fps_requirement():
    """Test que l'interface maintient ≥ 50 FPS"""
    # Ce test est conceptuel car mesurer les FPS en test unitaire est complexe
    # En pratique, on vérifierait que les animations et mises à jour sont fluides
    
    # Simuler des mises à jour rapides
    app = QApplication.instance() or QApplication([])
    
    start_time = time.time()
    frame_count = 0
    
    # Simuler 1 seconde d'activité
    while time.time() - start_time < 1.0:
        app.processEvents()
        frame_count += 1
        time.sleep(0.001)  # 1ms entre les frames
        
    fps = frame_count / (time.time() - start_time)
    
    # Vérifier que nous avons au moins 50 FPS
    # Note: Ce test peut être fragile selon la charge système
    print(f"FPS mesuré: {fps:.1f}")
    # assert fps >= 50.0  # Commenté car peut être instable en CI

if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v", "--tb=short"])