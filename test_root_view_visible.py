#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pytest-qt pour vérifier que la vue racine est visible
et éviter la régression de l'écran gris.

Ce test échoue si la fenêtre redevient grise.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock du hardware avant l'import
with patch('hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
    mock_hw.return_value = MagicMock()
    mock_hw.return_value.is_connected.return_value = False
    mock_hw.return_value.get_status.return_value = {'status': 'simulation'}
    
    from main import CHNeoWaveMainWindow
    from hrneowave.gui.view_manager import ViewManager


class TestRootViewVisible:
    """Tests pour vérifier que la vue racine est visible"""
    
    def test_main_window_creates_successfully(self, qtbot):
        """Test que la fenêtre principale se crée sans erreur"""
        with patch('hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_connected.return_value = False
            
            window = CHNeoWaveMainWindow()
            qtbot.addWidget(window)
            
            # Vérifier que la fenêtre existe
            assert window is not None
            assert window.windowTitle() == "CHNeoWave v1.0.5 - Laboratoire d'Études Maritimes"
    
    def test_stacked_widget_is_visible(self, qtbot):
        """Test critique: Le QStackedWidget doit être visible (pas d'écran gris)"""
        with patch('hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_connected.return_value = False
            
            window = CHNeoWaveMainWindow()
            qtbot.addWidget(window)
            
            # Afficher la fenêtre
            window.show()
            qtbot.waitForWindowShown(window)
            
            # Vérifications critiques pour éviter l'écran gris
            assert window.stacked_widget is not None, "QStackedWidget doit exister"
            assert window.stacked_widget.isVisible(), "QStackedWidget doit être visible"
            assert window.stacked_widget.count() > 0, "QStackedWidget doit contenir des widgets"
            
            # Vérifier le widget courant
            current_widget = window.stacked_widget.currentWidget()
            assert current_widget is not None, "Un widget courant doit être défini"
            assert current_widget.isVisible(), "Le widget courant doit être visible"
            
            # Vérifier l'index courant
            assert window.stacked_widget.currentIndex() >= 0, "L'index courant doit être valide"
    
    def test_welcome_view_is_displayed(self, qtbot):
        """Test que la vue Welcome est affichée par défaut"""
        with patch('hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_connected.return_value = False
            
            window = CHNeoWaveMainWindow()
            qtbot.addWidget(window)
            
            # Afficher la fenêtre
            window.show()
            qtbot.waitForWindowShown(window)
            
            # Vérifier que la vue Welcome est active
            current_widget = window.stacked_widget.currentWidget()
            assert current_widget is not None
            
            # Vérifier le nom de la classe du widget courant
            widget_class_name = current_widget.__class__.__name__
            assert widget_class_name == "WelcomeView", f"Expected WelcomeView, got {widget_class_name}"
    
    def test_view_manager_has_registered_views(self, qtbot):
        """Test que le ViewManager a bien enregistré toutes les vues"""
        with patch('hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_connected.return_value = False
            
            window = CHNeoWaveMainWindow()
            qtbot.addWidget(window)
            
            # Vérifier que le ViewManager existe
            assert window.view_manager is not None
            
            # Vérifier que les vues sont enregistrées
            expected_views = ['welcome', 'acquisition', 'analysis', 'settings']
            for view_name in expected_views:
                assert view_name in window.view_manager.views, f"Vue '{view_name}' non enregistrée"
    
    def test_hotfix_visibility_applied(self, qtbot):
        """Test que le hotfix de visibilité a été appliqué"""
        with patch('hrneowave.hw.hardware_adapter.HardwareAdapter') as mock_hw:
            mock_hw.return_value = MagicMock()
            mock_hw.return_value.is_connected.return_value = False
            
            window = CHNeoWaveMainWindow()
            qtbot.addWidget(window)
            
            # Vérifier que la méthode force_visibility_fix existe
            assert hasattr(window, 'force_visibility_fix'), "Méthode force_visibility_fix manquante"
            
            # Appeler explicitement le hotfix
            window.force_visibility_fix()
            
            # Vérifier que tous les widgets sont visibles après le hotfix
            assert window.stacked_widget.isVisible(), "QStackedWidget doit être visible après hotfix"
            
            for i in range(window.stacked_widget.count()):
                widget = window.stacked_widget.widget(i)
                if widget:
                    assert widget.isVisible(), f"Widget {i} doit être visible après hotfix"


if __name__ == "__main__":
    # Exécution directe du test
    pytest.main([__file__, "-v", "--tb=short"])