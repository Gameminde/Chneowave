#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration complète - MainWindow avec Dock État Capteurs

Ce script teste l'intégration du dock État Capteurs dans la MainWindow complète.
"""

import sys
import os
from pathlib import Path
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QSpinBox, QLabel, QGroupBox, QCheckBox, QSlider,
    QComboBox, QTextEdit, QSplitter, QToolBar, QAction
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon

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


class TestMainWindowCapteurs(MainWindow):
    """MainWindow de test avec contrôles pour les capteurs"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test HRNeoWave - MainWindow avec État Capteurs")
        self.setGeometry(100, 100, 1400, 900)
        
        # Ajouter des contrôles de test
        self._setup_test_controls()
        
        # Simuler un projet
        self._simulate_project()
        
        print("MainWindow avec État Capteurs initialisée")
    
    def _setup_test_controls(self):
        """Ajoute des contrôles de test à la barre d'outils"""
        # Barre d'outils pour les tests
        test_toolbar = self.addToolBar("Tests Capteurs")
        test_toolbar.setObjectName("TestCapteursToolBar")
        
        # Actions de test pour les capteurs
        action_config_capteurs = QAction("⚙️ Config Capteurs", self)
        action_config_capteurs.setToolTip("Configurer le nombre de capteurs")
        action_config_capteurs.triggered.connect(self._test_config_capteurs)
        test_toolbar.addAction(action_config_capteurs)
        
        action_start_sim = QAction("▶️ Démarrer Simulation", self)
        action_start_sim.setToolTip("Démarrer la simulation des capteurs")
        action_start_sim.triggered.connect(self._test_start_simulation)
        test_toolbar.addAction(action_start_sim)
        
        action_stop_sim = QAction("⏹️ Arrêter Simulation", self)
        action_stop_sim.setToolTip("Arrêter la simulation des capteurs")
        action_stop_sim.triggered.connect(self._test_stop_simulation)
        test_toolbar.addAction(action_stop_sim)
        
        test_toolbar.addSeparator()
        
        action_all_connected = QAction("🔗 Tous Connectés", self)
        action_all_connected.setToolTip("Mettre tous les capteurs en état connecté")
        action_all_connected.triggered.connect(self._test_all_connected)
        test_toolbar.addAction(action_all_connected)
        
        action_some_acquiring = QAction("📊 Quelques en Acquisition", self)
        action_some_acquiring.setToolTip("Mettre quelques capteurs en acquisition")
        action_some_acquiring.triggered.connect(self._test_some_acquiring)
        test_toolbar.addAction(action_some_acquiring)
        
        action_some_errors = QAction("⚠️ Quelques Erreurs", self)
        action_some_errors.setToolTip("Simuler des erreurs sur quelques capteurs")
        action_some_errors.triggered.connect(self._test_some_errors)
        test_toolbar.addAction(action_some_errors)
        
        action_reset_capteurs = QAction("🔄 Reset Capteurs", self)
        action_reset_capteurs.setToolTip("Remettre à zéro tous les capteurs")
        action_reset_capteurs.triggered.connect(self._test_reset_capteurs)
        test_toolbar.addAction(action_reset_capteurs)
        
        test_toolbar.addSeparator()
        
        # Timer pour simulation de données
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self._simulate_capteur_data)
        
        action_data_sim = QAction("📈 Simulation Données", self)
        action_data_sim.setToolTip("Démarrer/arrêter la simulation de données")
        action_data_sim.setCheckable(True)
        action_data_sim.toggled.connect(self._toggle_data_simulation)
        test_toolbar.addAction(action_data_sim)
    
    def _simulate_project(self):
        """Simule la création d'un projet"""
        # Simuler les informations de projet
        project_info = {
            'nom': 'Test Capteurs Houle',
            'description': 'Test d\'intégration du dock État Capteurs',
            'operateur': 'Utilisateur Test',
            'laboratoire': 'Laboratoire Maritime Méditerranée',
            'date_creation': '2025-01-16'
        }
        
        # Mettre à jour le dock infos essai si disponible
        if hasattr(self, 'infos_essai_dock') and self.infos_essai_dock:
            self.infos_essai_dock.start_essai(
                nom=project_info['nom'],
                operateur=project_info['operateur'],
                configuration="Test Capteurs Houle"
            )
        
        print(f"✅ Projet simulé créé: {project_info['nom']}")
    
    def _test_config_capteurs(self):
        """Test de configuration du nombre de capteurs"""
        if hasattr(self, 'etat_capteurs_dock') and self.etat_capteurs_dock:
            # Alterner entre 4, 8, 12 capteurs
            current = self.etat_capteurs_dock.spin_nb_capteurs.value()
            new_value = 4 if current >= 12 else current + 4
            self.set_capteurs_config(new_value)
            print(f"🔧 Configuration capteurs: {new_value} capteurs")
        else:
            print("❌ Dock État Capteurs non disponible")
    
    def _test_start_simulation(self):
        """Test de démarrage de simulation"""
        self.start_capteurs_simulation()
        print("▶️ Simulation capteurs démarrée")
    
    def _test_stop_simulation(self):
        """Test d'arrêt de simulation"""
        self.stop_capteurs_simulation()
        print("⏹️ Simulation capteurs arrêtée")
    
    def _test_all_connected(self):
        """Test: tous les capteurs connectés"""
        if hasattr(self, 'etat_capteurs_dock') and self.etat_capteurs_dock:
            nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
            for i in range(1, nb_capteurs + 1):
                self.update_capteur_data(i, etat="Connecté", signal_quality=random.uniform(70, 95))
            print(f"🔗 Tous les {nb_capteurs} capteurs connectés")
    
    def _test_some_acquiring(self):
        """Test: quelques capteurs en acquisition"""
        if hasattr(self, 'etat_capteurs_dock') and self.etat_capteurs_dock:
            nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
            
            # Mettre la moitié en acquisition
            acquiring_count = nb_capteurs // 2
            acquiring_ids = random.sample(range(1, nb_capteurs + 1), acquiring_count)
            
            for i in range(1, nb_capteurs + 1):
                if i in acquiring_ids:
                    self.update_capteur_data(
                        i, 
                        etat="Acquisition",
                        signal_quality=random.uniform(80, 100),
                        sample_rate=random.choice([1000, 2000, 5000]),
                        valeur=random.uniform(-1.5, 1.5)
                    )
                else:
                    self.update_capteur_data(i, etat="Connecté", signal_quality=random.uniform(60, 85))
            
            print(f"📊 {acquiring_count} capteurs en acquisition sur {nb_capteurs}")
    
    def _test_some_errors(self):
        """Test: quelques capteurs en erreur"""
        if hasattr(self, 'etat_capteurs_dock') and self.etat_capteurs_dock:
            nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
            
            # Mettre 2-3 capteurs en erreur
            error_count = min(3, max(1, nb_capteurs // 4))
            error_ids = random.sample(range(1, nb_capteurs + 1), error_count)
            
            for i in range(1, nb_capteurs + 1):
                if i in error_ids:
                    self.update_capteur_data(i, etat="Erreur", signal_quality=0)
                else:
                    self.update_capteur_data(i, etat="Connecté", signal_quality=random.uniform(70, 90))
            
            print(f"⚠️ {error_count} capteurs en erreur: {error_ids}")
    
    def _test_reset_capteurs(self):
        """Test: reset de tous les capteurs"""
        if hasattr(self, 'etat_capteurs_dock') and self.etat_capteurs_dock:
            nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
            for i in range(1, nb_capteurs + 1):
                self.update_capteur_data(
                    i, 
                    etat="Déconnecté",
                    signal_quality=0,
                    valeur=0.0,
                    sample_rate=0,
                    total_samples=0
                )
            print(f"🔄 {nb_capteurs} capteurs remis à zéro")
    
    def _toggle_data_simulation(self, enabled):
        """Active/désactive la simulation de données"""
        if enabled:
            self.data_timer.start(1000)  # Mise à jour chaque seconde
            print("📈 Simulation de données activée")
        else:
            self.data_timer.stop()
            print("📈 Simulation de données désactivée")
    
    def _simulate_capteur_data(self):
        """Simule des données de capteurs en temps réel"""
        if hasattr(self, 'etat_capteurs_dock') and self.etat_capteurs_dock:
            nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
            
            for i in range(1, nb_capteurs + 1):
                capteur = self.etat_capteurs_dock.capteurs.get(i)
                if capteur and capteur.etat == "Acquisition":
                    # Simuler des données de houle
                    amplitude = random.uniform(0.5, 2.5)
                    frequence = random.uniform(0.8, 1.2)
                    phase = random.uniform(-180, 180)
                    
                    # Incrémenter les échantillons
                    new_samples = capteur.total_samples + capteur.sample_rate
                    
                    self.update_capteur_data(
                        i,
                        valeur=amplitude * random.uniform(-1, 1),
                        total_samples=new_samples,
                        signal_quality=random.uniform(85, 100)
                    )
    
    def _on_capteur_selected(self, capteur_id):
        """Override pour ajouter des logs de test"""
        super()._on_capteur_selected(capteur_id)
        print(f"🎯 Test: Capteur {capteur_id} sélectionné")
    
    def _on_capteurs_updated(self, capteurs_data):
        """Override pour ajouter des logs de test"""
        super()._on_capteurs_updated(capteurs_data)
        
        # Log des statistiques
        capteurs = capteurs_data.get('capteurs', {})
        nb_connectes = sum(1 for c in capteurs.values() if c['etat'] in ['Connecté', 'Acquisition'])
        nb_acquisition = sum(1 for c in capteurs.values() if c['etat'] == 'Acquisition')
        nb_erreurs = sum(1 for c in capteurs.values() if c['etat'] == 'Erreur')
        
        print(f"📊 Stats capteurs: {nb_connectes}/{len(capteurs)} connectés, {nb_acquisition} acquisition, {nb_erreurs} erreurs")


def main():
    """Fonction principale"""
    print("=== Test HRNeoWave - MainWindow avec État Capteurs ===")
    print("Démarrage de l'interface complète...")
    
    app = QApplication(sys.argv)
    
    # Créer et afficher la MainWindow de test
    window = TestMainWindowCapteurs()
    window.show()
    
    print("\n=== Instructions de Test ===")
    print("1. Vérifiez que les deux docks sont visibles (Infos Essai à droite, État Capteurs à gauche)")
    print("2. Utilisez la barre d'outils 'Tests Capteurs' pour tester les fonctionnalités")
    print("3. Testez la configuration du nombre de capteurs")
    print("4. Démarrez/arrêtez la simulation des capteurs")
    print("5. Testez les différents états des capteurs")
    print("6. Activez la simulation de données pour voir les mises à jour en temps réel")
    print("7. Cliquez sur les capteurs pour les sélectionner")
    print("8. Observez les mises à jour de la barre de statut")
    print("9. Testez le redimensionnement et déplacement des docks")
    print("10. Vérifiez l'application cohérente du thème HRNeoWave")
    
    # Lancer l'application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()