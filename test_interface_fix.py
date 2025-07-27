#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de validation de l'interface corrigée CHNeoWave
Vérifie que les corrections apportées résolvent les problèmes signalés
"""

import sys
import os
import logging
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Signal
from PySide6.QtTest import QTest

class InterfaceTestRunner:
    """Testeur pour valider les corrections de l'interface"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.errors = []
        
    def setup_logging(self):
        """Configure le logging pour capturer les erreurs"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Capturer les erreurs dans une liste
        class ErrorCapture(logging.Handler):
            def __init__(self, error_list):
                super().__init__()
                self.error_list = error_list
                
            def emit(self, record):
                if record.levelno >= logging.ERROR:
                    self.error_list.append(record.getMessage())
        
        error_handler = ErrorCapture(self.errors)
        logging.getLogger().addHandler(error_handler)
    
    def test_main_window_creation(self):
        """Test de création de la fenêtre principale"""
        print("\n=== Test 1: Création de la fenêtre principale ===")
        
        try:
            from hrneowave.gui.main_window import MainWindow
            
            self.main_window = MainWindow()
            print("✓ MainWindow créée avec succès")
            
            # Vérifier que les vues sont enregistrées
            if hasattr(self.main_window, 'view_manager'):
                views = ['welcome', 'dashboard', 'manual_calibration', 'acquisition', 'analysis']
                for view_name in views:
                    if self.main_window.view_manager.has_view(view_name):
                        print(f"✓ Vue '{view_name}' enregistrée")
                    else:
                        print(f"✗ Vue '{view_name}' manquante")
                        self.errors.append(f"Vue {view_name} non enregistrée")
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors de la création: {e}")
            self.errors.append(f"Création MainWindow: {e}")
            return False
    
    def test_navigation_workflow(self):
        """Test du workflow de navigation"""
        print("\n=== Test 2: Workflow de navigation ===")
        
        if not self.main_window:
            print("✗ MainWindow non disponible")
            return False
        
        try:
            # Test navigation vers welcome
            self.main_window.view_manager.switch_to_view('welcome')
            current_view = self.main_window.view_manager.current_view
            if current_view == 'welcome':
                print("✓ Navigation vers 'welcome' réussie")
            else:
                print(f"✗ Navigation vers 'welcome' échouée: vue actuelle = {current_view}")
                self.errors.append("Navigation welcome échouée")
            
            # Test navigation vers dashboard
            self.main_window.view_manager.switch_to_view('dashboard')
            current_view = self.main_window.view_manager.current_view
            if current_view == 'dashboard':
                print("✓ Navigation vers 'dashboard' réussie")
            else:
                print(f"✗ Navigation vers 'dashboard' échouée: vue actuelle = {current_view}")
                self.errors.append("Navigation dashboard échouée")
            
            # Test navigation vers calibration
            self.main_window.view_manager.switch_to_view('manual_calibration')
            current_view = self.main_window.view_manager.current_view
            if current_view == 'manual_calibration':
                print("✓ Navigation vers 'manual_calibration' réussie")
            else:
                print(f"✗ Navigation vers 'manual_calibration' échouée: vue actuelle = {current_view}")
                self.errors.append("Navigation calibration échouée")
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors des tests de navigation: {e}")
            self.errors.append(f"Navigation: {e}")
            return False
    
    def test_project_creation_workflow(self):
        """Test du workflow de création de projet"""
        print("\n=== Test 3: Workflow de création de projet ===")
        
        if not self.main_window:
            print("✗ MainWindow non disponible")
            return False
        
        try:
            # Aller à la vue welcome
            self.main_window.view_manager.switch_to_view('welcome')
            welcome_view = self.main_window.view_manager.get_view_widget('welcome')
            
            if welcome_view:
                print("✓ Vue welcome accessible")
                
                # Simuler la saisie de données de projet
                welcome_view.project_name.setText("Test Project")
                welcome_view.project_manager.setText("Test Manager")
                welcome_view.laboratory.setText("Test Lab")
                welcome_view.description.setPlainText("Test Description")
                
                print("✓ Données de projet saisies")
                
                # Vérifier que le bouton est activé
                if welcome_view.validate_button.isEnabled():
                    print("✓ Bouton de validation activé")
                    
                    # Simuler la validation (sans émettre le signal pour éviter la navigation)
                    project_data = {
                        'name': welcome_view.project_name.text(),
                        'manager': welcome_view.project_manager.text(),
                        'laboratory': welcome_view.laboratory.text(),
                        'description': welcome_view.description.toPlainText()
                    }
                    print(f"✓ Données de projet validées: {project_data}")
                    
                else:
                    print("✗ Bouton de validation non activé")
                    self.errors.append("Bouton validation non activé")
            else:
                print("✗ Vue welcome non accessible")
                self.errors.append("Vue welcome inaccessible")
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors du test de création de projet: {e}")
            self.errors.append(f"Création projet: {e}")
            return False
    
    def test_sidebar_navigation(self):
        """Test de la navigation via la sidebar"""
        print("\n=== Test 4: Navigation via sidebar ===")
        
        if not self.main_window:
            print("✗ MainWindow non disponible")
            return False
        
        try:
            sidebar = self.main_window.sidebar
            if sidebar:
                print("✓ Sidebar accessible")
                
                # Vérifier que les boutons de navigation existent
                nav_buttons = {
                    'welcome': 'Accueil',
                    'dashboard': 'Tableau de bord',
                    'manual_calibration': 'Calibration',
                    'acquisition': 'Acquisition'
                }
                
                for view_name, button_text in nav_buttons.items():
                    # Simuler le clic sur le bouton (via signal)
                    try:
                        sidebar.navigation_requested.emit(view_name)
                        current_view = self.main_window.view_manager.current_view
                        if current_view == view_name:
                            print(f"✓ Navigation sidebar vers '{view_name}' réussie")
                        else:
                            print(f"✗ Navigation sidebar vers '{view_name}' échouée")
                            self.errors.append(f"Navigation sidebar {view_name} échouée")
                    except Exception as e:
                        print(f"✗ Erreur navigation sidebar {view_name}: {e}")
                        self.errors.append(f"Navigation sidebar {view_name}: {e}")
                
            else:
                print("✗ Sidebar non accessible")
                self.errors.append("Sidebar inaccessible")
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors du test de sidebar: {e}")
            self.errors.append(f"Sidebar: {e}")
            return False
    
    def test_performance_widget(self):
        """Test du widget de performance (pour vérifier l'erreur AttributeError)"""
        print("\n=== Test 5: Widget de performance ===")
        
        try:
            from hrneowave.gui.components.performance_widget import PerformanceWidget
            
            perf_widget = PerformanceWidget()
            print("✓ PerformanceWidget créé avec succès")
            
            # Démarrer la surveillance brièvement
            perf_widget.start_monitoring()
            print("✓ Surveillance démarrée")
            
            # Attendre un peu pour collecter des métriques
            QTest.qWait(1000)
            
            # Arrêter la surveillance
            perf_widget.stop_monitoring()
            print("✓ Surveillance arrêtée")
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors du test de performance: {e}")
            self.errors.append(f"Performance widget: {e}")
            return False
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("CHNeoWave - Test de validation de l'interface corrigée")
        print("=" * 60)
        
        self.setup_logging()
        
        # Créer l'application Qt
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        tests = [
            self.test_main_window_creation,
            self.test_navigation_workflow,
            self.test_project_creation_workflow,
            self.test_sidebar_navigation,
            self.test_performance_widget
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"✗ Test échoué avec exception: {e}")
                self.errors.append(f"Exception test: {e}")
        
        # Résultats finaux
        print("\n" + "=" * 60)
        print(f"RÉSULTATS: {passed}/{total} tests réussis")
        
        if self.errors:
            print(f"\nERREURS DÉTECTÉES ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        else:
            print("\n✓ AUCUNE ERREUR DÉTECTÉE")
        
        # Nettoyer
        if self.main_window:
            self.main_window.close()
        
        return len(self.errors) == 0

if __name__ == "__main__":
    tester = InterfaceTestRunner()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS - Interface corrigée avec succès!")
        sys.exit(0)
    else:
        print("\n❌ DES ERREURS PERSISTENT - Corrections supplémentaires nécessaires")
        sys.exit(1)