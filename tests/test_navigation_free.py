# test_navigation_free.py - Tests pour la navigation libre entre onglets
import pytest
import sys
from unittest.mock import Mock, patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

sys.path.insert(0, '../src')

try:
    from hrneowave.gui.enhanced_main_ui import EnhancedMainUI
except ImportError:
    EnhancedMainUI = None

@pytest.fixture
def app():
    """Fixture pour l'application Qt"""
    if not QApplication.instance():
        return QApplication([])
    return QApplication.instance()

@pytest.fixture
def main_ui(app):
    """Fixture pour l'interface principale"""
    if not EnhancedMainUI:
        pytest.skip("EnhancedMainUI non disponible")
    
    config = {
        'acquisition': {'sample_rate': 1000, 'duration': 10},
        'calibration': {'auto_detect': True}
    }
    ui = EnhancedMainUI(config)
    yield ui
    ui.close()

class TestNavigationFree:
    """Tests pour la navigation libre entre onglets"""
    
    def test_navigation_free(self, main_ui):
        """Test que tous les onglets sont accessibles sans validation préalable"""
        # Vérifier que tous les onglets sont activés dès le départ
        for i in range(4):
            assert main_ui.nav_toolbar.tab_actions[i].isEnabled(), f"L'onglet {i} devrait être activé"
        
        # Tester la navigation vers chaque onglet
        for target_tab in range(4):
            # Naviguer vers l'onglet
            main_ui._switch_to_tab(target_tab)
            
            # Vérifier que la navigation a réussi
            assert main_ui.current_tab_index == target_tab, f"Devrait être sur l'onglet {target_tab}"
            assert main_ui.stacked_widget.currentIndex() == target_tab, f"StackedWidget devrait afficher l'onglet {target_tab}"
            assert main_ui.nav_toolbar.current_tab == target_tab, f"NavigationToolBar devrait indiquer l'onglet {target_tab}"
    
    def test_can_leave_current_tab_always_true(self, main_ui):
        """Test que _can_leave_current_tab retourne toujours True (sauf acquisition en cours)"""
        # Tester depuis chaque onglet
        for tab_index in range(4):
            main_ui.current_tab_index = tab_index
            main_ui.is_acquiring = False
            
            # Devrait toujours pouvoir quitter l'onglet
            assert main_ui._can_leave_current_tab() == True, f"Devrait pouvoir quitter l'onglet {tab_index}"
    
    def test_can_leave_during_acquisition(self, main_ui):
        """Test que _can_leave_current_tab gère correctement l'acquisition en cours"""
        main_ui.current_tab_index = 2  # Onglet Acquisition
        main_ui.is_acquiring = True
        
        # Mock QMessageBox pour simuler la réponse utilisateur
        with patch('hrneowave.gui.enhanced_main_ui.QMessageBox') as mock_msgbox:
            # Simuler "Non" - ne pas quitter
            mock_msgbox.question.return_value = mock_msgbox.No
            assert main_ui._can_leave_current_tab() == False
            
            # Simuler "Oui" - quitter
            mock_msgbox.question.return_value = mock_msgbox.Yes
            assert main_ui._can_leave_current_tab() == True
    
    def test_validation_does_not_block_navigation(self, main_ui):
        """Test que la validation ne bloque plus la navigation"""
        # Simuler une validation échouée
        main_ui._on_validation_changed(False)
        
        # Tous les onglets devraient rester activés
        for i in range(4):
            assert main_ui.nav_toolbar.tab_actions[i].isEnabled(), f"L'onglet {i} devrait rester activé même avec validation échouée"
        
        # La navigation devrait fonctionner
        for target_tab in range(4):
            main_ui._switch_to_tab(target_tab)
            assert main_ui.current_tab_index == target_tab, f"Navigation vers onglet {target_tab} devrait réussir"
    
    def test_tab_request_navigation(self, main_ui):
        """Test la navigation via _on_tab_requested"""
        # Tester la navigation via le signal de la toolbar
        for target_tab in range(4):
            main_ui._on_tab_requested(target_tab)
            
            # Vérifier que la navigation a réussi
            assert main_ui.current_tab_index == target_tab, f"Navigation via signal vers onglet {target_tab} devrait réussir"
    
    def test_initial_tab_configuration(self, main_ui):
        """Test que la configuration initiale active tous les onglets"""
        # Vérifier que tous les onglets sont activés dès l'initialisation
        for i in range(4):
            assert main_ui.nav_toolbar.tab_actions[i].isEnabled(), f"L'onglet {i} devrait être activé à l'initialisation"
        
        # Vérifier que l'onglet 0 est sélectionné par défaut
        assert main_ui.current_tab_index == 0, "L'onglet Accueil devrait être sélectionné par défaut"
        assert main_ui.nav_toolbar.current_tab == 0, "NavigationToolBar devrait indiquer l'onglet Accueil"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])