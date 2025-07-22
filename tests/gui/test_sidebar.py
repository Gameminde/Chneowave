#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour le composant Sidebar
CHNeoWave v1.1.0 - Sprint 1
"""

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtTest import QTest
from PySide6.QtGui import QKeyEvent

import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from hrneowave.gui.components.sidebar import Sidebar


class TestSidebar:
    """Tests pour le composant Sidebar"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, qtbot):
        """Configuration pour chaque test"""
        self.sidebar = Sidebar()
        qtbot.addWidget(self.sidebar)
        self.sidebar.show()
    
    def test_sidebar_creation(self):
        """Test la création de la sidebar"""
        assert self.sidebar is not None
        assert self.sidebar.isVisible()
        assert self.sidebar.expanded == True  # Démarrage en mode étendu
    
    def test_sidebar_toggle(self, qtbot):
        """Test le basculement expand/collapse"""
        # État initial : étendue
        assert self.sidebar.expanded == True
        
        # Réduction
        self.sidebar.toggle_expanded()
        assert self.sidebar.expanded == False
        
        # Expansion
        self.sidebar.toggle_expanded()
        assert self.sidebar.expanded == True
    
    def test_sidebar_navigation_items(self):
        """Test la présence des éléments de navigation"""
        # Vérifier que tous les éléments de navigation sont présents
        expected_items = [
            'dashboard', 'welcome', 'calibration', 
            'acquisition', 'analysis', 'export'
        ]
        
        for item_name in expected_items:
            assert item_name in self.sidebar.nav_items
            nav_item = self.sidebar.nav_items[item_name]
            assert nav_item is not None
    
    def test_sidebar_item_selection(self, qtbot):
        """Test la sélection d'éléments de navigation"""
        # Sélectionner un élément
        self.sidebar.set_current_step('calibration')
        
        # Vérifier que l'élément est actif
        assert self.sidebar.get_current_step() == 'calibration'
        
        # Sélectionner un autre élément
        self.sidebar.set_current_step('acquisition')
        
        # Vérifier que le nouvel élément est actif
        assert self.sidebar.get_current_step() == 'acquisition'
    
    def test_sidebar_keyboard_navigation(self, qtbot):
        """Test la navigation au clavier"""
        # Donner le focus à la sidebar
        self.sidebar.setFocus()
        
        # Simuler les touches fléchées
        qtbot.keyPress(self.sidebar, Qt.Key_Down)
        qtbot.keyPress(self.sidebar, Qt.Key_Up)
        qtbot.keyPress(self.sidebar, Qt.Key_Return)
        
        # Le test passe si aucune exception n'est levée
        assert True
    
    def test_sidebar_signals(self, qtbot):
        """Test l'émission des signaux"""
        signal_received = []
        
        def on_navigation_requested(view_name):
            signal_received.append(view_name)
        
        # Connecter le signal
        self.sidebar.navigationRequested.connect(on_navigation_requested)
        
        # Simuler une navigation
        self.sidebar.navigate_to('dashboard')
        
        # Vérifier que le signal a été émis
        assert len(signal_received) > 0
        assert 'dashboard' in signal_received
    
    def test_sidebar_expansion_animation(self, qtbot):
        """Test l'animation d'expansion"""
        # Vérifier que l'animation existe
        assert hasattr(self.sidebar, 'width_animation')
        assert self.sidebar.width_animation is not None
        
        # Vérifier l'état initial
        initial_expanded = self.sidebar.expanded
        
        # Déclencher le basculement
        self.sidebar.toggle_expanded()
        
        # Vérifier que l'état a changé
        assert self.sidebar.expanded != initial_expanded
    
    def test_sidebar_step_completion(self):
        """Test le marquage des étapes comme complétées"""
        # Marquer une étape comme complétée
        self.sidebar.mark_step_completed('calibration')
        assert 'calibration' in self.sidebar.get_completed_steps()
        
        # Marquer une étape comme en attente
        self.sidebar.mark_step_pending('calibration')
        assert 'calibration' not in self.sidebar.get_completed_steps()
    
    def test_sidebar_accessibility(self):
        """Test les fonctionnalités d'accessibilité"""
        # Vérifier que la sidebar peut recevoir le focus
        assert self.sidebar.focusPolicy() != Qt.NoFocus
        
        # Vérifier les propriétés d'accessibilité
        assert self.sidebar.accessibleName() is not None


class TestSidebarIntegration:
    """Tests d'intégration pour la Sidebar"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, qtbot):
        """Configuration pour chaque test d'intégration"""
        self.sidebar = Sidebar()
        qtbot.addWidget(self.sidebar)
        self.sidebar.show()
    
    def test_sidebar_with_view_manager_simulation(self, qtbot):
        """Test l'intégration avec un ViewManager simulé"""
        view_changes = []
        
        def mock_view_manager(view_name):
            view_changes.append(view_name)
        
        # Connecter la sidebar au mock
        self.sidebar.navigationRequested.connect(mock_view_manager)
        
        # Simuler plusieurs changements de vue
        test_views = ['dashboard', 'calibration', 'acquisition']
        
        for view_name in test_views:
            # Simuler une navigation
            self.sidebar.navigate_to(view_name)
            
            # Vérifier que la vue active a changé
            assert self.sidebar.get_current_step() == view_name
        
        # Vérifier que tous les signaux ont été émis
        assert len(view_changes) == len(test_views)
        for view_name in test_views:
            assert view_name in view_changes
    
    def test_sidebar_responsive_behavior(self, qtbot):
        """Test le comportement responsive de la sidebar"""
        # Tester différentes tailles de fenêtre
        test_sizes = [(800, 600), (1200, 800), (1920, 1080)]
        
        for width, height in test_sizes:
            self.sidebar.resize(width, height)
            qtbot.wait(50)  # Attendre le redimensionnement
            
            # Vérifier que la sidebar reste fonctionnelle
            assert self.sidebar.isVisible()
            assert len(self.sidebar.nav_items) > 0


if __name__ == '__main__':
    # Permettre l'exécution directe du fichier de test
    app = QApplication([])
    pytest.main([__file__, '-v'])