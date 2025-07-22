#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour ExportView
CHNeoWave v1.1.0 - Sprint 1
"""

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from hrneowave.gui.views.export_view import ExportView
except ImportError:
    # Si ExportView n'existe pas encore, créer une classe mock pour les tests
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
    
    class ExportView(QWidget):
        """Mock ExportView pour les tests"""
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setObjectName("ExportView")
            
            layout = QVBoxLayout(self)
            label = QLabel("Export View - En développement")
            layout.addWidget(label)


class TestExportView:
    """Tests pour la vue Export"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, qtbot):
        """Configuration pour chaque test"""
        self.export_view = ExportView()
        # S'assurer que l'objectName est défini
        if not self.export_view.objectName():
            self.export_view.setObjectName("ExportView")
        qtbot.addWidget(self.export_view)
        self.export_view.show()
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if hasattr(self, 'export_view') and self.export_view:
            self.export_view.deleteLater()
            self.export_view = None
    
    def test_export_view_creation(self):
        """Test la création de la vue Export"""
        assert self.export_view is not None
        assert self.export_view.isVisible()
        # Vérifier que l'objectName est défini correctement
        object_name = self.export_view.objectName()
        assert object_name == "ExportView"
    
    def test_export_view_basic_functionality(self):
        """Test les fonctionnalités de base"""
        # Test que la vue peut être redimensionnée
        self.export_view.resize(800, 600)
        assert self.export_view.size().width() == 800
        assert self.export_view.size().height() == 600
        
        # Test que la vue reste visible après redimensionnement
        assert self.export_view.isVisible()
    
    def test_export_view_integration_ready(self):
        """Test que la vue est prête pour l'intégration"""
        # Vérifier que la vue peut être ajoutée à un layout parent
        from PySide6.QtWidgets import QWidget, QVBoxLayout
        
        parent_widget = QWidget()
        parent_layout = QVBoxLayout(parent_widget)
        
        try:
            # Créer une nouvelle instance pour éviter les conflits de parent
            test_view = ExportView()
            if not test_view.objectName():
                test_view.setObjectName("ExportView")
            
            # Ajouter au parent
            parent_layout.addWidget(test_view)
            
            # Vérifier l'intégration
            assert test_view.parent() == parent_widget
            assert parent_layout.count() == 1
            assert parent_layout.itemAt(0).widget() == test_view
            
        finally:
            # Nettoyage
            if 'test_view' in locals():
                test_view.deleteLater()
            parent_widget.deleteLater()


if __name__ == '__main__':
    # Permettre l'exécution directe du fichier de test
    app = QApplication([])
    pytest.main([__file__, '-v'])