# test_tabbed_ui.py - Tests pour l'interface avec navigation par onglets
import pytest
import sys
import os
from unittest.mock import Mock, patch
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtTest import QTest
from PyQt5.QtGui import QPalette

# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from hrneowave.gui.tabbed_main_ui import TabbedMainUI, WelcomeTab, CalibrationTab
    from hrneowave.gui.field_validator import FieldValidator
except ImportError as e:
    print(f"⚠️ Import manquant pour les tests: {e}")
    TabbedMainUI = None
    WelcomeTab = None
    CalibrationTab = None
    FieldValidator = None

@pytest.fixture
def app():
    """Fixture pour l'application Qt"""
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    yield app
    
@pytest.fixture
def config():
    """Configuration de test"""
    return {
        'n_channels': 4,
        'sample_rate': 32.0,
        'theme': 'light'
    }

@pytest.fixture
def welcome_tab(app, config):
    """Fixture pour l'onglet d'accueil"""
    if WelcomeTab is None:
        pytest.skip("WelcomeTab non disponible")
    return WelcomeTab(config)

@pytest.fixture
def calibration_tab(app, config):
    """Fixture pour l'onglet de calibration"""
    if CalibrationTab is None:
        pytest.skip("CalibrationTab non disponible")
    return CalibrationTab(config)

@pytest.fixture
def main_ui(app, config):
    """Fixture pour l'interface principale"""
    if TabbedMainUI is None:
        pytest.skip("TabbedMainUI non disponible")
    return TabbedMainUI(config)

class TestWelcomeTab:
    """Tests pour l'onglet d'accueil"""
    
    def test_required_fields_validation(self, welcome_tab):
        """Test de validation des champs obligatoires"""
        # Initialement, les champs sont vides donc invalides
        assert not welcome_tab.is_valid()
        
        # Remplir seulement le nom du projet
        welcome_tab.project_name_edit.setText("Test Project")
        QTest.qWait(100)  # Attendre la validation
        assert not welcome_tab.is_valid()  # Encore invalide
        
        # Remplir le chef de projet
        welcome_tab.project_manager_edit.setText("Dr. Test")
        QTest.qWait(100)
        assert not welcome_tab.is_valid()  # Date manquante
        
        # La date est déjà remplie par défaut, donc maintenant valide
        QTest.qWait(100)
        assert welcome_tab.is_valid()
        
    def test_required_fields_minimum_length(self, welcome_tab):
        """Test des longueurs minimales des champs"""
        # Nom trop court
        welcome_tab.project_name_edit.setText("AB")
        welcome_tab.project_manager_edit.setText("Dr. Test")
        QTest.qWait(100)
        assert not welcome_tab.is_valid()
        
        # Chef de projet trop court
        welcome_tab.project_name_edit.setText("Test Project")
        welcome_tab.project_manager_edit.setText("A")
        QTest.qWait(100)
        assert not welcome_tab.is_valid()
        
        # Longueurs correctes
        welcome_tab.project_name_edit.setText("Test Project")
        welcome_tab.project_manager_edit.setText("Dr. Test")
        QTest.qWait(100)
        assert welcome_tab.is_valid()
        
    def test_validation_signal_emission(self, welcome_tab, qtbot):
        """Test de l'émission du signal de validation"""
        with qtbot.waitSignal(welcome_tab.validationChanged, timeout=1000) as blocker:
            welcome_tab.project_name_edit.setText("Test Project")
            welcome_tab.project_manager_edit.setText("Dr. Test")
            
        # Vérifier que le signal a été émis avec True
        assert blocker.args == [True]
        
    def test_get_project_data(self, welcome_tab):
        """Test de récupération des données du projet"""
        # Remplir les champs
        welcome_tab.project_name_edit.setText("Test Project")
        welcome_tab.project_manager_edit.setText("Dr. Test")
        welcome_tab.project_date_edit.setDate(QDate(2025, 1, 15))
        welcome_tab.study_type_combo.setCurrentText("Houle régulière")
        welcome_tab.location_edit.setText("Bassin Test")
        welcome_tab.comments_edit.setPlainText("Commentaire test")
        
        data = welcome_tab.get_project_data()
        
        assert data['name'] == "Test Project"
        assert data['manager'] == "Dr. Test"
        assert data['date'] == "2025-01-15"
        assert data['study_type'] == "Houle régulière"
        assert data['location'] == "Bassin Test"
        assert data['comments'] == "Commentaire test"
        
    @patch('hrneowave.gui.theme.set_dark_mode')
    @patch('hrneowave.gui.theme.set_light_mode')
    @patch('hrneowave.gui.theme.current_theme', 'light')
    def test_theme_toggle(self, mock_light, mock_dark, welcome_tab, qtbot):
        """Test du basculement de thème"""
        # Cliquer sur le bouton de thème
        qtbot.mouseClick(welcome_tab.theme_toggle_btn, Qt.LeftButton)
        
        # Vérifier que set_dark_mode a été appelé
        mock_dark.assert_called_once()
        
        # Vérifier le changement de texte du bouton
        assert "Mode Clair" in welcome_tab.theme_toggle_btn.text()

class TestCalibrationTab:
    """Tests pour l'onglet de calibration"""
    
    def test_initial_validation(self, calibration_tab):
        """Test que la calibration est valide par défaut"""
        assert calibration_tab.is_valid()
        
    def test_auto_calibration(self, calibration_tab, qtbot):
        """Test de la calibration automatique"""
        # Cliquer sur calibration automatique
        qtbot.mouseClick(calibration_tab.auto_calib_btn, Qt.LeftButton)
        
        # Vérifier le statut en cours
        assert "en cours" in calibration_tab.calib_status_label.text()
        
        # Attendre la fin de la calibration simulée
        QTest.qWait(2500)
        
        # Vérifier le statut terminé
        assert "✅" in calibration_tab.calib_status_label.text()
        
    def test_get_calibration_data(self, calibration_tab):
        """Test de récupération des données de calibration"""
        # Modifier les valeurs
        calibration_tab.n_probes_spin.setValue(6)
        calibration_tab.sample_rate_spin.setValue(64.0)
        calibration_tab.sensor_type_combo.setCurrentText("Sonde capacitive")
        
        data = calibration_tab.get_calibration_data()
        
        assert data['n_probes'] == 6
        assert data['sample_rate'] == 64.0
        assert data['sensor_type'] == "Sonde capacitive"
        assert not data['calibrated']  # Pas encore calibré

class TestTabbedMainUI:
    """Tests pour l'interface principale"""
    
    def test_initial_state(self, main_ui):
        """Test de l'état initial de l'interface"""
        # Vérifier l'onglet initial
        assert main_ui.current_tab_index == 0
        assert main_ui.stacked_widget.currentIndex() == 0
        
        # Vérifier les boutons de navigation
        assert not main_ui.prev_btn.isEnabled()
        assert not main_ui.next_btn.isEnabled()  # Champs non remplis
        
    def test_navigation_validation(self, main_ui, qtbot):
        """Test que la navigation respecte la validation"""
        # Essayer de naviguer sans remplir les champs
        with patch.object(QMessageBox, 'warning') as mock_warning:
            qtbot.mouseClick(main_ui.nav_actions[1], Qt.LeftButton)
            
        # Vérifier qu'un avertissement a été affiché
        mock_warning.assert_called_once()
        
        # Vérifier qu'on est resté sur le premier onglet
        assert main_ui.current_tab_index == 0
        
    def test_successful_navigation(self, main_ui, qtbot):
        """Test de navigation réussie après validation"""
        # Remplir les champs obligatoires
        welcome_tab = main_ui.welcome_tab
        welcome_tab.project_name_edit.setText("Test Project")
        welcome_tab.project_manager_edit.setText("Dr. Test")
        
        # Attendre la validation
        QTest.qWait(200)
        
        # Maintenant la navigation devrait fonctionner
        qtbot.mouseClick(main_ui.next_btn, Qt.LeftButton)
        
        # Vérifier qu'on est passé au deuxième onglet
        assert main_ui.current_tab_index == 1
        assert main_ui.stacked_widget.currentIndex() == 1
        
    def test_navigation_buttons_state(self, main_ui, qtbot):
        """Test de l'état des boutons de navigation"""
        # Remplir les champs et naviguer
        welcome_tab = main_ui.welcome_tab
        welcome_tab.project_name_edit.setText("Test Project")
        welcome_tab.project_manager_edit.setText("Dr. Test")
        QTest.qWait(200)
        
        # Aller au deuxième onglet
        qtbot.mouseClick(main_ui.next_btn, Qt.LeftButton)
        
        # Vérifier l'état des boutons
        assert main_ui.prev_btn.isEnabled()  # Peut revenir en arrière
        assert main_ui.next_btn.isEnabled()  # Peut continuer (calibration optionnelle)
        
    def test_progress_indicator(self, main_ui, qtbot):
        """Test de l'indicateur de progression"""
        # Vérifier l'indicateur initial
        assert "Étape 1/4" in main_ui.progress_label.text()
        assert "Accueil" in main_ui.progress_label.text()
        
        # Naviguer et vérifier la mise à jour
        welcome_tab = main_ui.welcome_tab
        welcome_tab.project_name_edit.setText("Test Project")
        welcome_tab.project_manager_edit.setText("Dr. Test")
        QTest.qWait(200)
        
        qtbot.mouseClick(main_ui.next_btn, Qt.LeftButton)
        
        assert "Étape 2/4" in main_ui.progress_label.text()
        assert "Calibration" in main_ui.progress_label.text()
        
    @patch('hrneowave.gui.theme.set_dark_mode')
    @patch('hrneowave.gui.theme.set_light_mode')
    def test_theme_application(self, mock_light, mock_dark, config):
        """Test de l'application du thème"""
        # Test thème sombre
        config['theme'] = 'dark'
        if TabbedMainUI:
            ui = TabbedMainUI(config)
            mock_dark.assert_called()
            
        # Test thème clair
        config['theme'] = 'light'
        if TabbedMainUI:
            ui = TabbedMainUI(config)
            mock_light.assert_called()

class TestPerformance:
    """Tests de performance"""
    
    def test_ui_responsiveness(self, main_ui, qtbot):
        """Test de la réactivité de l'interface (objectif: ≥50 FPS)"""
        import time
        
        # Mesurer le temps de rendu
        start_time = time.time()
        iterations = 100
        
        for i in range(iterations):
            # Simuler des interactions utilisateur
            main_ui.welcome_tab.project_name_edit.setText(f"Project {i}")
            QTest.qWait(1)  # 1ms entre chaque interaction
            
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculer les FPS équivalents
        fps = iterations / total_time
        
        # Vérifier que les FPS sont ≥ 50
        assert fps >= 50, f"Performance insuffisante: {fps:.1f} FPS < 50 FPS"
        
    def test_memory_usage(self, main_ui):
        """Test de l'utilisation mémoire"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Effectuer des opérations intensives
        for i in range(1000):
            main_ui.welcome_tab.project_name_edit.setText(f"Test {i}")
            
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Vérifier que l'augmentation mémoire reste raisonnable (< 50MB)
        assert memory_increase < 50, f"Fuite mémoire détectée: +{memory_increase:.1f}MB"

if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v", "--tb=short"])