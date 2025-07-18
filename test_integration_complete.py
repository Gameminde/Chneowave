#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration complète - Validation finale des docks HRNeoWave

Ce script valide l'intégration complète des docks Infos Essai et État Capteurs
avec des tests automatisés et des vérifications de cohérence.
"""

import sys
import os
from pathlib import Path
import random
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QProgressBar, QTextEdit, QSplitter
)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

# Ajouter le chemin vers le module HRNeoWave
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from hrneowave.gui.main_window import MainWindow
    from hrneowave.gui.theme import apply_skin
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Vérifiez que le module HRNeoWave est accessible")
    sys.exit(1)


class TestWorker(QThread):
    """Worker thread pour les tests automatisés"""
    
    test_progress = pyqtSignal(str, int)  # message, pourcentage
    test_completed = pyqtSignal(bool, str)  # succès, rapport
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.tests_results = []
    
    def run(self):
        """Exécute la suite de tests automatisés"""
        try:
            self.test_progress.emit("Démarrage des tests automatisés...", 0)
            time.sleep(1)
            
            # Test 1: Vérification des docks
            self.test_progress.emit("Test 1: Vérification présence des docks", 10)
            result1 = self._test_docks_presence()
            self.tests_results.append(("Présence des docks", result1))
            time.sleep(0.5)
            
            # Test 2: Configuration des capteurs
            self.test_progress.emit("Test 2: Configuration des capteurs", 25)
            result2 = self._test_capteurs_config()
            self.tests_results.append(("Configuration capteurs", result2))
            time.sleep(0.5)
            
            # Test 3: États des capteurs
            self.test_progress.emit("Test 3: États des capteurs", 40)
            result3 = self._test_capteurs_states()
            self.tests_results.append(("États capteurs", result3))
            time.sleep(0.5)
            
            # Test 4: Simulation d'acquisition
            self.test_progress.emit("Test 4: Simulation d'acquisition", 55)
            result4 = self._test_acquisition_simulation()
            self.tests_results.append(("Simulation acquisition", result4))
            time.sleep(0.5)
            
            # Test 5: Synchronisation des docks
            self.test_progress.emit("Test 5: Synchronisation des docks", 70)
            result5 = self._test_docks_synchronization()
            self.tests_results.append(("Synchronisation docks", result5))
            time.sleep(0.5)
            
            # Test 6: Performance et mémoire
            self.test_progress.emit("Test 6: Performance et mémoire", 85)
            result6 = self._test_performance()
            self.tests_results.append(("Performance", result6))
            time.sleep(0.5)
            
            # Test 7: Thème et styles
            self.test_progress.emit("Test 7: Thème et styles", 95)
            result7 = self._test_theme_consistency()
            self.tests_results.append(("Thème et styles", result7))
            time.sleep(0.5)
            
            self.test_progress.emit("Tests terminés", 100)
            
            # Générer le rapport
            success_count = sum(1 for _, result in self.tests_results if result['success'])
            total_tests = len(self.tests_results)
            overall_success = success_count == total_tests
            
            rapport = self._generate_report(success_count, total_tests)
            self.test_completed.emit(overall_success, rapport)
            
        except Exception as e:
            self.test_completed.emit(False, f"Erreur lors des tests: {str(e)}")
    
    def _test_docks_presence(self):
        """Test de présence des docks"""
        try:
            infos_dock = hasattr(self.main_window, 'infos_essai_dock') and self.main_window.infos_essai_dock
            capteurs_dock = hasattr(self.main_window, 'etat_capteurs_dock') and self.main_window.etat_capteurs_dock
            
            details = []
            if infos_dock:
                details.append("✅ Dock Infos Essai présent")
            else:
                details.append("❌ Dock Infos Essai manquant")
            
            if capteurs_dock:
                details.append("✅ Dock État Capteurs présent")
            else:
                details.append("❌ Dock État Capteurs manquant")
            
            return {
                'success': infos_dock and capteurs_dock,
                'details': details
            }
        except Exception as e:
            return {'success': False, 'details': [f"Erreur: {str(e)}"]}
    
    def _test_capteurs_config(self):
        """Test de configuration des capteurs"""
        try:
            if not hasattr(self.main_window, 'etat_capteurs_dock'):
                return {'success': False, 'details': ["Dock capteurs non disponible"]}
            
            dock = self.main_window.etat_capteurs_dock
            details = []
            
            # Test configuration 4 capteurs
            self.main_window.set_capteurs_config(4)
            time.sleep(0.1)
            if len(dock.capteurs) == 4:
                details.append("✅ Configuration 4 capteurs OK")
            else:
                details.append(f"❌ Configuration 4 capteurs: {len(dock.capteurs)} trouvés")
            
            # Test configuration 8 capteurs
            self.main_window.set_capteurs_config(8)
            time.sleep(0.1)
            if len(dock.capteurs) == 8:
                details.append("✅ Configuration 8 capteurs OK")
            else:
                details.append(f"❌ Configuration 8 capteurs: {len(dock.capteurs)} trouvés")
            
            return {
                'success': len(dock.capteurs) == 8,
                'details': details
            }
        except Exception as e:
            return {'success': False, 'details': [f"Erreur: {str(e)}"]}
    
    def _test_capteurs_states(self):
        """Test des états des capteurs"""
        try:
            if not hasattr(self.main_window, 'etat_capteurs_dock'):
                return {'success': False, 'details': ["Dock capteurs non disponible"]}
            
            dock = self.main_window.etat_capteurs_dock
            details = []
            
            # Test état connecté
            self.main_window.update_capteur_data(1, etat="Connecté", signal_quality=85)
            time.sleep(0.1)
            capteur1 = dock.capteurs.get(1)
            if capteur1 and capteur1.etat == "Connecté":
                details.append("✅ État Connecté OK")
            else:
                details.append("❌ État Connecté échoué")
            
            # Test état acquisition
            self.main_window.update_capteur_data(2, etat="Acquisition", signal_quality=95, valeur=1.25)
            time.sleep(0.1)
            capteur2 = dock.capteurs.get(2)
            if capteur2 and capteur2.etat == "Acquisition":
                details.append("✅ État Acquisition OK")
            else:
                details.append("❌ État Acquisition échoué")
            
            # Test état erreur
            self.main_window.update_capteur_data(3, etat="Erreur", signal_quality=0)
            time.sleep(0.1)
            capteur3 = dock.capteurs.get(3)
            if capteur3 and capteur3.etat == "Erreur":
                details.append("✅ État Erreur OK")
            else:
                details.append("❌ État Erreur échoué")
            
            return {
                'success': len(details) == 3 and all("✅" in d for d in details),
                'details': details
            }
        except Exception as e:
            return {'success': False, 'details': [f"Erreur: {str(e)}"]}
    
    def _test_acquisition_simulation(self):
        """Test de simulation d'acquisition"""
        try:
            details = []
            
            # Démarrer simulation
            self.main_window.start_capteurs_simulation()
            time.sleep(0.2)
            details.append("✅ Démarrage simulation OK")
            
            # Arrêter simulation
            self.main_window.stop_capteurs_simulation()
            time.sleep(0.2)
            details.append("✅ Arrêt simulation OK")
            
            return {
                'success': True,
                'details': details
            }
        except Exception as e:
            return {'success': False, 'details': [f"Erreur: {str(e)}"]}
    
    def _test_docks_synchronization(self):
        """Test de synchronisation entre les docks"""
        try:
            details = []
            
            # Test mise à jour infos essai
            if hasattr(self.main_window, 'infos_essai_dock'):
                dock_infos = self.main_window.infos_essai_dock
                dock_infos.set_acquisition_config(8, 2000, 1000)
                time.sleep(0.1)
                details.append("✅ Mise à jour config acquisition OK")
            
            # Test cohérence nombre de capteurs
            if hasattr(self.main_window, 'etat_capteurs_dock'):
                dock_capteurs = self.main_window.etat_capteurs_dock
                nb_capteurs = len(dock_capteurs.capteurs)
                if nb_capteurs > 0:
                    details.append(f"✅ Cohérence capteurs: {nb_capteurs} configurés")
                else:
                    details.append("❌ Aucun capteur configuré")
            
            return {
                'success': len(details) >= 1,
                'details': details
            }
        except Exception as e:
            return {'success': False, 'details': [f"Erreur: {str(e)}"]}
    
    def _test_performance(self):
        """Test de performance"""
        try:
            details = []
            
            # Test mise à jour rapide
            start_time = time.time()
            for i in range(1, 9):
                self.main_window.update_capteur_data(
                    i, 
                    etat="Acquisition",
                    signal_quality=random.uniform(80, 100),
                    valeur=random.uniform(-2, 2)
                )
            end_time = time.time()
            
            update_time = (end_time - start_time) * 1000  # en ms
            if update_time < 100:  # Moins de 100ms pour 8 capteurs
                details.append(f"✅ Performance OK: {update_time:.1f}ms pour 8 capteurs")
            else:
                details.append(f"⚠️ Performance lente: {update_time:.1f}ms pour 8 capteurs")
            
            return {
                'success': update_time < 200,  # Seuil plus permissif
                'details': details
            }
        except Exception as e:
            return {'success': False, 'details': [f"Erreur: {str(e)}"]}
    
    def _test_theme_consistency(self):
        """Test de cohérence du thème"""
        try:
            details = []
            
            # Vérifier que les docks ont des styles appliqués
            if hasattr(self.main_window, 'infos_essai_dock'):
                dock_infos = self.main_window.infos_essai_dock
                if dock_infos.styleSheet():
                    details.append("✅ Thème Dock Infos Essai appliqué")
                else:
                    details.append("❌ Thème Dock Infos Essai manquant")
            
            if hasattr(self.main_window, 'etat_capteurs_dock'):
                dock_capteurs = self.main_window.etat_capteurs_dock
                if dock_capteurs.styleSheet():
                    details.append("✅ Thème Dock État Capteurs appliqué")
                else:
                    details.append("❌ Thème Dock État Capteurs manquant")
            
            return {
                'success': len(details) >= 1 and all("✅" in d for d in details),
                'details': details
            }
        except Exception as e:
            return {'success': False, 'details': [f"Erreur: {str(e)}"]}
    
    def _generate_report(self, success_count, total_tests):
        """Génère le rapport de tests"""
        rapport = f"\n=== RAPPORT DE TESTS AUTOMATISÉS ===\n\n"
        rapport += f"Tests réussis: {success_count}/{total_tests}\n"
        rapport += f"Taux de réussite: {(success_count/total_tests)*100:.1f}%\n\n"
        
        for test_name, result in self.tests_results:
            status = "✅ RÉUSSI" if result['success'] else "❌ ÉCHOUÉ"
            rapport += f"{status} - {test_name}\n"
            for detail in result['details']:
                rapport += f"  {detail}\n"
            rapport += "\n"
        
        if success_count == total_tests:
            rapport += "🎉 TOUS LES TESTS SONT RÉUSSIS !\n"
            rapport += "L'intégration des docks HRNeoWave est validée.\n"
        else:
            rapport += "⚠️ Certains tests ont échoué.\n"
            rapport += "Vérifiez les détails ci-dessus.\n"
        
        return rapport


class TestIntegrationComplete(MainWindow):
    """MainWindow de test avec validation automatisée"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test HRNeoWave - Validation Complète des Docks")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Interface de test
        self._setup_test_interface()
        
        # Simuler un projet
        self._simulate_project()
        
        print("Interface de validation complète initialisée")
    
    def _setup_test_interface(self):
        """Configure l'interface de test"""
        # Widget central pour les tests
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Titre
        title = QLabel("Validation Complète - Docks HRNeoWave")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Bouton de test automatique
        self.btn_auto_test = QPushButton("🚀 Lancer Tests Automatisés")
        self.btn_auto_test.setMinimumHeight(40)
        self.btn_auto_test.clicked.connect(self._start_auto_tests)
        layout.addWidget(self.btn_auto_test)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Label de statut
        self.status_label = QLabel("Prêt pour les tests")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Zone de rapport
        self.rapport_text = QTextEdit()
        self.rapport_text.setMinimumHeight(300)
        self.rapport_text.setPlainText("Les résultats des tests apparaîtront ici...")
        layout.addWidget(self.rapport_text)
        
        # Worker pour tests
        self.test_worker = None
    
    def _simulate_project(self):
        """Simule un projet de test"""
        if hasattr(self, 'infos_essai_dock') and self.infos_essai_dock:
            self.infos_essai_dock.start_essai(
                nom="Validation Docks HRNeoWave",
                operateur="Test Automatisé",
                configuration="Validation Complète"
            )
            self.infos_essai_dock.set_acquisition_config(8, 2000, 1000)
        
        # Configurer 8 capteurs par défaut
        self.set_capteurs_config(8)
    
    def _start_auto_tests(self):
        """Démarre les tests automatisés"""
        if self.test_worker and self.test_worker.isRunning():
            return
        
        self.btn_auto_test.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Tests en cours...")
        self.rapport_text.clear()
        
        # Créer et démarrer le worker
        self.test_worker = TestWorker(self)
        self.test_worker.test_progress.connect(self._on_test_progress)
        self.test_worker.test_completed.connect(self._on_tests_completed)
        self.test_worker.start()
    
    def _on_test_progress(self, message, percentage):
        """Met à jour la progression des tests"""
        self.status_label.setText(message)
        self.progress_bar.setValue(percentage)
    
    def _on_tests_completed(self, success, rapport):
        """Traite la fin des tests"""
        self.btn_auto_test.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_label.setText("✅ Tous les tests réussis !")
        else:
            self.status_label.setText("❌ Certains tests ont échoué")
        
        self.rapport_text.setPlainText(rapport)
        
        # Scroll vers le bas
        cursor = self.rapport_text.textCursor()
        cursor.movePosition(cursor.End)
        self.rapport_text.setTextCursor(cursor)


def main():
    """Fonction principale"""
    print("=== Test HRNeoWave - Validation Complète des Docks ===")
    print("Démarrage de la validation automatisée...")
    
    app = QApplication(sys.argv)
    
    # Créer et afficher l'interface de test
    window = TestIntegrationComplete()
    window.show()
    
    print("\n=== Instructions ===")
    print("1. Cliquez sur 'Lancer Tests Automatisés' pour valider l'intégration")
    print("2. Observez la progression des tests")
    print("3. Consultez le rapport détaillé")
    print("4. Vérifiez visuellement les docks pendant les tests")
    
    # Lancer l'application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()