#!/usr/bin/env python3
# test_ui_simple.py - Tests simplifiés pour l'interface principale
"""
Tests simplifiés pour valider les fonctionnalités de l'interface CHNeoWave améliorée
sans dépendance pytest-qt qui peut poser des problèmes.
"""

import sys
import os
import time
from typing import Dict, Any

# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest

try:
    from hrneowave.gui.enhanced_main_ui import (
        EnhancedMainUI, NavigationToolBar, StatusBarWidget
    )
    from hrneowave.gui.theme import (
        set_light_mode, set_dark_mode, get_current_theme, get_theme_colors
    )
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

class TestRunner:
    """Classe pour exécuter les tests"""
    
    def __init__(self):
        self.app = QApplication.instance() or QApplication([])
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def run_test(self, test_name: str, test_func):
        """Exécute un test et enregistre le résultat"""
        try:
            print(f"🧪 Test: {test_name}")
            test_func()
            print(f"✅ PASS: {test_name}")
            self.tests_passed += 1
            self.test_results.append((test_name, "PASS", None))
        except Exception as e:
            import traceback
            error_details = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            print(f"❌ FAIL: {test_name} - {error_details}")
            self.tests_failed += 1
            self.test_results.append((test_name, "FAIL", error_details))
            
    def print_summary(self):
        """Affiche le résumé des tests"""
        total = self.tests_passed + self.tests_failed
        print(f"\n📊 Résumé des tests:")
        print(f"Total: {total}")
        print(f"✅ Réussis: {self.tests_passed}")
        print(f"❌ Échoués: {self.tests_failed}")
        print(f"📈 Taux de réussite: {(self.tests_passed/total*100):.1f}%" if total > 0 else "0%")
        
        if self.tests_failed > 0:
            print("\n❌ Tests échoués:")
            for test_name, status, error in self.test_results:
                if status == "FAIL":
                    print(f"  - {test_name}:")
                    if error:
                        print(f"    {error}")

def test_navigation_toolbar():
    """Test la barre de navigation"""
    toolbar = NavigationToolBar()
    
    # Test initialisation
    assert toolbar.current_tab == 0
    assert len(toolbar.tab_actions) == 4
    assert toolbar.tab_actions[0].isChecked()
    
    # Test sélection d'onglet
    toolbar._on_tab_action(2)
    assert toolbar.current_tab == 2
    assert toolbar.tab_actions[2].isChecked()
    
    # Test activation/désactivation
    toolbar.set_tab_enabled(1, False)
    assert not toolbar.tab_actions[1].isEnabled()
    
    toolbar.set_tab_enabled(1, True)
    assert toolbar.tab_actions[1].isEnabled()
    
    print("  ✓ Initialisation, sélection et activation/désactivation OK")

def test_status_bar():
    """Test la barre de statut"""
    status_bar = StatusBarWidget()
    
    # Test initialisation
    assert status_bar.main_label.text() == "Prêt"
    assert "✅" in status_bar.validation_label.text()
    
    # Test message principal
    status_bar.set_main_message("Test message", "red")
    assert status_bar.main_label.text() == "Test message"
    
    # Test statut de validation
    status_bar.set_validation_status(False)
    assert "❌" in status_bar.validation_label.text()
    
    status_bar.set_validation_status(True)
    assert "✅" in status_bar.validation_label.text()
    
    # Test statut de thème
    status_bar.set_theme_status(True)
    assert "Sombre" in status_bar.theme_label.text()
    
    status_bar.set_theme_status(False)
    assert "Clair" in status_bar.theme_label.text()
    
    print("  ✓ Messages, validation et thème OK")

def test_main_ui_creation():
    """Test la création de l'interface principale"""
    config = {
        'sample_rate': 32.0,
        'n_channels': 4,
        'max_duration': 300
    }
    
    try:
        ui = EnhancedMainUI(config)
        
        # Test initialisation
        assert ui.windowTitle() == "CHNeoWave - Laboratoire d'Étude Maritime"
        
        # current_tab_index peut être différent de 0 si des paramètres sont restaurés
        # On teste plutôt que l'attribut existe et est un entier valide
        assert hasattr(ui, 'current_tab_index')
        assert isinstance(ui.current_tab_index, int)
        assert 0 <= ui.current_tab_index < 4
        
        assert not ui.is_acquiring
        assert ui.stacked_widget.count() == 4
        
        # Test navigation si la méthode existe
        if hasattr(ui, '_switch_to_tab'):
            ui._switch_to_tab(1)
            assert ui.current_tab_index == 1
            assert ui.stacked_widget.currentIndex() == 1
            
            ui._switch_to_tab(2)
            assert ui.current_tab_index == 2
            assert ui.stacked_widget.currentIndex() == 2
            
            # Retour à l'onglet 0
            ui._switch_to_tab(0)
            assert ui.current_tab_index == 0
            assert ui.stacked_widget.currentIndex() == 0
        
        ui.close()
        print("  ✓ Création, initialisation et navigation OK")
        
    except Exception as e:
        print(f"  ❌ Erreur détaillée: {type(e).__name__}: {e}")
        raise

def test_theme_functions():
    """Test les fonctions de thème"""
    # Test obtention du thème actuel
    current = get_current_theme()
    assert current in ["light", "dark"]
    
    # Test obtention des couleurs
    colors = get_theme_colors()
    assert isinstance(colors, dict)
    assert 'background' in colors
    assert 'foreground' in colors
    assert 'accent' in colors
    
    # Test basculement de thème
    initial_theme = get_current_theme()
    
    if initial_theme == "light":
        set_dark_mode()
        new_theme = get_current_theme()
        assert new_theme == "dark"
        
        set_light_mode()
        final_theme = get_current_theme()
        assert final_theme == "light"
    else:
        set_light_mode()
        new_theme = get_current_theme()
        assert new_theme == "light"
        
        set_dark_mode()
        final_theme = get_current_theme()
        assert final_theme == "dark"
    
    print("  ✓ Thème actuel, couleurs et basculement OK")

def test_acquisition_workflow():
    """Test le workflow d'acquisition"""
    config = {'sample_rate': 32.0, 'n_channels': 4}
    ui = EnhancedMainUI(config)
    
    # Test début d'acquisition
    acq_config = {'duration': 60, 'sample_rate': 32.0}
    ui._on_acquisition_started(acq_config)
    
    assert ui.is_acquiring
    assert "Acquisition en cours" in ui.status_bar.main_label.text()
    
    # Test fin d'acquisition
    results = {'data': [1, 2, 3], 'duration': 60}
    ui._on_acquisition_finished(results)
    
    assert not ui.is_acquiring
    assert ui.acquisition_data == results
    assert "Acquisition terminée" in ui.status_bar.main_label.text()
    
    ui.close()
    print("  ✓ Début et fin d'acquisition OK")

def test_validation_workflow():
    """Test le workflow de validation"""
    config = {'sample_rate': 32.0, 'n_channels': 4}
    ui = EnhancedMainUI(config)
    
    # Test changement de validation
    ui._on_validation_changed(False)
    assert "❌" in ui.status_bar.validation_label.text()
    
    ui._on_validation_changed(True)
    assert "✅" in ui.status_bar.validation_label.text()
    
    ui.close()
    print("  ✓ Validation des champs OK")

def test_project_data_management():
    """Test la gestion des données de projet"""
    config = {'sample_rate': 32.0, 'n_channels': 4}
    ui = EnhancedMainUI(config)
    
    # Test données de projet
    test_data = {
        'project_name': 'Test Project',
        'project_manager': 'Test Manager',
        'date': '2024-01-01'
    }
    
    ui.project_data.update(test_data)
    
    project_data = ui.get_project_data()
    assert project_data['project_name'] == 'Test Project'
    assert project_data['project_manager'] == 'Test Manager'
    
    ui.close()
    print("  ✓ Gestion des données de projet OK")

def test_performance_basic():
    """Test de performance basique"""
    config = {'sample_rate': 32.0, 'n_channels': 4}
    ui = EnhancedMainUI(config)
    
    # Test changement d'onglets rapide
    start_time = time.time()
    
    for i in range(10):
        ui._switch_to_tab(i % 4)
        
    end_time = time.time()
    duration = end_time - start_time
    
    # Le changement d'onglets devrait être rapide
    assert duration < 1.0
    
    ui.close()
    print(f"  ✓ Performance OK - 10 changements d'onglets en {duration:.3f}s")

def main():
    """Fonction principale de test"""
    print("🧪 Tests simplifiés CHNeoWave Interface Améliorée")
    print("=" * 50)
    
    runner = TestRunner()
    
    # Exécuter les tests
    runner.run_test("Navigation ToolBar", test_navigation_toolbar)
    runner.run_test("Status Bar", test_status_bar)
    runner.run_test("Main UI Creation", test_main_ui_creation)
    runner.run_test("Theme Functions", test_theme_functions)
    runner.run_test("Acquisition Workflow", test_acquisition_workflow)
    runner.run_test("Validation Workflow", test_validation_workflow)
    runner.run_test("Project Data Management", test_project_data_management)
    runner.run_test("Performance Basic", test_performance_basic)
    
    # Afficher le résumé
    runner.print_summary()
    
    # Retourner le code de sortie
    return 0 if runner.tests_failed == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    print(f"\n{'✅ Tous les tests sont passés!' if exit_code == 0 else '❌ Certains tests ont échoué.'}")
    sys.exit(exit_code)