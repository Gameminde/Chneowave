# -*- coding: utf-8 -*-
"""
Test pour vérifier que le bouton Valider navigue correctement
vers la vue suivante après création d'un projet.
"""

import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

# Import des modules CHNeoWave
from src.hrneowave.gui.views.welcome_view import WelcomeView
from src.hrneowave.gui.controllers.main_controller import MainController
from src.hrneowave.gui.view_manager import ViewManager


class TestValidateNavigates:
    """Tests pour la navigation après validation du projet"""
    
    def test_validate_button_click_emits_signal(self, qtbot):
        """Test que le clic sur Valider émet le signal projectSelected"""
        # Créer la vue Welcome
        welcome_view = WelcomeView()
        qtbot.addWidget(welcome_view)
        
        # Remplir les champs obligatoires
        welcome_view.project_name.setText("Test Project")
        welcome_view.project_manager.setText("Test Manager")
        welcome_view.laboratory.setText("Test Lab")
        
        # Vérifier que le bouton est activé
        assert welcome_view.validate_button.isEnabled()
        
        # Connecter un spy au signal
        signal_emitted = False
        signal_path = None
        
        def signal_handler(path):
            nonlocal signal_emitted, signal_path
            signal_emitted = True
            signal_path = path
            
        welcome_view.projectSelected.connect(signal_handler)
        
        # Cliquer sur le bouton
        qtbot.mouseClick(welcome_view.validate_button, Qt.LeftButton)
        
        # Vérifier que le signal a été émis avec un chemin vide (nouveau projet)
        assert signal_emitted, "Le signal projectSelected n'a pas été émis"
        assert signal_path == "", f"Le signal devrait être émis avec un chemin vide, reçu: '{signal_path}'"
        
    def test_main_controller_handles_project_selected(self, qtbot):
        """Test que MainController gère correctement le signal projectSelected"""
        with patch('src.hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_connected.return_value = False
            
            # Créer un ViewManager mock
            view_manager = MagicMock()
            view_manager.switch_to_view.return_value = True
            
            # Créer le contrôleur avec des mocks
            controller = MainController()
            controller.view_manager = view_manager
            
            # Simuler la réception du signal projectSelected avec chemin vide
            controller._on_project_selected("")
            
            # Vérifier que switch_to_view a été appelé avec "acquisition"
            view_manager.switch_to_view.assert_called_with("acquisition")
                
    def test_integration_validate_navigates(self, qtbot):
        """Test d'intégration: validation du projet navigue vers acquisition"""
        with patch('src.hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_connected.return_value = False
            
            # Créer les composants
            welcome_view = WelcomeView()
            qtbot.addWidget(welcome_view)
            
            # Créer un ViewManager réel mais avec des vues mockées
            from PySide6.QtWidgets import QStackedWidget, QWidget
            stacked_widget = QStackedWidget()
            qtbot.addWidget(stacked_widget)
            
            view_manager = ViewManager(stacked_widget)
            
            # Enregistrer les vues
            acquisition_view = QWidget()  # Vue mock
            view_manager.register_view("welcome", welcome_view)
            view_manager.register_view("acquisition", acquisition_view)
            
            # Créer le contrôleur
            controller = MainController()
            controller.view_manager = view_manager
            
            # Connecter le signal
            welcome_view.projectSelected.connect(controller._on_project_selected)
            
            # Remplir le formulaire
            welcome_view.project_name.setText("Test Project")
            welcome_view.project_manager.setText("Test Manager")
            welcome_view.laboratory.setText("Test Lab")
            
            # Vérifier l'état initial
            view_manager.switch_to_view("welcome")
            assert view_manager.current_view == "welcome"
            
            # Cliquer sur Valider
            qtbot.mouseClick(welcome_view.validate_button, Qt.LeftButton)
            
            # Vérifier que la navigation a eu lieu
            assert view_manager.current_view == "acquisition", f"Vue actuelle: {view_manager.current_view}, attendue: acquisition"
            
    def test_validate_button_disabled_when_fields_empty(self, qtbot):
        """Test que le bouton Valider est désactivé quand les champs sont vides"""
        welcome_view = WelcomeView()
        qtbot.addWidget(welcome_view)
        
        # Vérifier que le bouton est désactivé par défaut
        assert not welcome_view.validate_button.isEnabled()
        
        # Remplir partiellement
        welcome_view.project_name.setText("Test")
        assert not welcome_view.validate_button.isEnabled()
        
        welcome_view.project_manager.setText("Manager")
        assert not welcome_view.validate_button.isEnabled()
        
        # Remplir complètement
        welcome_view.laboratory.setText("Lab")
        assert welcome_view.validate_button.isEnabled()
        
        # Vider un champ
        welcome_view.project_name.clear()
        assert not welcome_view.validate_button.isEnabled()