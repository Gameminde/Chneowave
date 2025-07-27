#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests d'intégration pour les nouveaux composants UX de CHNeoWave.

Ce module teste l'intégration des systèmes de préférences, d'aide contextuelle,
d'indicateurs de statut et de notifications dans l'interface principale.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest

import hrneowave.gui.main_window as main_window_module
from hrneowave.gui.preferences.user_preferences import get_user_preferences, ThemeMode
from hrneowave.gui.components.help_system import get_help_system
from hrneowave.gui.components.notification_system import get_notification_center
from hrneowave.gui.components.status_indicators import StatusLevel


class TestUXIntegration:
    """Tests d'intégration des composants UX."""
    
    @pytest.fixture
    def app(self):
        """Fixture pour l'application Qt."""
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        yield app
        
    @pytest.fixture
    def main_window(self, app):
        """Fixture pour la fenêtre principale."""
        with patch('hrneowave.core.project_manager.ProjectManager'), \
             patch('hrneowave.gui.controllers.acquisition_controller.AcquisitionController'):
            window = main_window_module.MainWindow()
            yield window
            window.close()
    
    def test_preferences_integration(self, main_window):
        """Test l'intégration du système de préférences."""
        # Vérifier que les préférences sont initialisées
        assert hasattr(main_window, 'user_preferences')
        assert main_window.user_preferences is not None
        
        # Vérifier que le menu Outils existe
        menu_bar = main_window.menuBar()
        tools_menu = None
        for action in menu_bar.actions():
            if action.text() == "Outils":
                tools_menu = action.menu()
                break
        
        assert tools_menu is not None, "Le menu Outils doit exister"
        
        # Vérifier que l'action Préférences existe
        preferences_action = None
        for action in tools_menu.actions():
            if "Préférences" in action.text():
                preferences_action = action
                break
        
        assert preferences_action is not None, "L'action Préférences doit exister"
        assert preferences_action.shortcut().toString() == "Ctrl+,"
    
    def test_help_system_integration(self, main_window):
        """Test l'intégration du système d'aide."""
        # Vérifier que le panneau d'aide existe
        assert hasattr(main_window, 'help_panel')
        assert main_window.help_panel is not None
        
        # Vérifier que le système d'aide global est accessible
        help_system = get_help_system()
        assert help_system is not None
        
        # Tester la mise à jour du contexte d'aide
        main_window._update_help_context("test_context")
        assert help_system.current_context == "test_context"
    
    def test_status_indicators_integration(self, main_window):
        """Test l'intégration des indicateurs de statut."""
        # Vérifier que le widget de statut existe
        assert hasattr(main_window, 'status_widget')
        assert main_window.status_widget is not None
        
        # Vérifier que les composants de base sont configurés
        status_widget = main_window.status_widget
        expected_components = ["acquisition", "sensors", "storage", "network"]
        
        for component in expected_components:
            assert component in status_widget.status_cards
        
        # Tester la mise à jour d'un statut
        status_widget.update_component_status("acquisition", StatusLevel.OK)
        assert status_widget.get_component_status("acquisition") == StatusLevel.OK
    
    def test_notification_system_integration(self, main_window):
        """Test l'intégration du système de notifications."""
        # Vérifier que les méthodes de notification existent
        assert hasattr(main_window, 'show_success_notification')
        assert hasattr(main_window, 'show_error_notification')
        assert hasattr(main_window, 'show_info_notification')
        
        # Vérifier que le centre de notifications est accessible
        notification_center = get_notification_center()
        assert notification_center is not None
        
        # Tester l'affichage d'une notification
        initial_count = len(notification_center.notifications)
        main_window.show_success_notification("Test", "Message de test")
        
        # Attendre un peu pour que la notification soit traitée
        QTest.qWait(100)
        
        # Vérifier qu'une notification a été ajoutée
        assert len(notification_center.notifications) > initial_count
    
    def test_theme_application(self, main_window):
        """Test l'application des thèmes."""
        # Tester le changement de thème
        preferences = main_window.user_preferences
        
        # Changer vers le thème sombre
        preferences.set_preference('theme', 'mode', ThemeMode.DARK.value)
        main_window._apply_theme(ThemeMode.DARK.value)
        
        # Vérifier que le thème a été appliqué (test basique)
        assert main_window.styleSheet() != ""
        
        # Changer vers le thème clair
        preferences.set_preference('theme', 'mode', ThemeMode.LIGHT.value)
        main_window._apply_theme(ThemeMode.LIGHT.value)
        
        # Vérifier que le style a changé
        assert main_window.styleSheet() != ""
    
    def test_ui_layout_with_new_components(self, main_window):
        """Test que la mise en page inclut tous les nouveaux composants."""
        # Vérifier que la fenêtre a un splitter principal
        central_widget = main_window.centralWidget()
        assert central_widget is not None
        
        # Vérifier que les composants principaux sont présents
        assert hasattr(main_window, 'sidebar')
        assert hasattr(main_window, 'view_manager')
        assert hasattr(main_window, 'help_panel')
        assert hasattr(main_window, 'status_widget')
        assert hasattr(main_window, 'breadcrumbs')
    
    def test_status_update_handling(self, main_window):
        """Test la gestion des mises à jour de statut."""
        # Simuler une mise à jour de statut
        with patch.object(main_window, 'status_bar') as mock_status_bar:
            mock_status_bar.showMessage = Mock()
            
            # Tester une erreur
            main_window._on_system_status_updated("test_component", "error", "Test error")
            mock_status_bar.showMessage.assert_called_with(
                "Erreur test_component: Test error", 10000
            )
            
            # Tester un avertissement
            main_window._on_system_status_updated("test_component", "warning", "Test warning")
            mock_status_bar.showMessage.assert_called_with(
                "Attention test_component: Test warning", 5000
            )
    
    def test_notification_center_dialog(self, main_window):
        """Test l'ouverture du centre de notifications."""
        # Tester l'ouverture du centre de notifications
        with patch('PySide6.QtWidgets.QDialog') as mock_dialog, \
             patch('PySide6.QtWidgets.QVBoxLayout') as mock_layout:
            mock_dialog_instance = Mock()
            mock_dialog.return_value = mock_dialog_instance
            mock_layout_instance = Mock()
            mock_layout.return_value = mock_layout_instance
            
            main_window._show_notification_center()
            
            # Vérifier que la boîte de dialogue a été créée et configurée
            mock_dialog.assert_called_once_with(main_window)
            mock_dialog_instance.setWindowTitle.assert_called_with("Centre de notifications")
            mock_dialog_instance.setModal.assert_called_with(False)
            mock_dialog_instance.resize.assert_called_with(400, 600)
            mock_dialog_instance.show.assert_called_once()
            
            # Vérifier que le layout a été créé
            mock_layout.assert_called_once_with(mock_dialog_instance)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])