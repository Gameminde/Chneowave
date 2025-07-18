#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'étape 3 du skinning HRNeoWave - Dock État Capteurs

Ce script teste l'intégration du dock État Capteurs dans l'interface principale.
"""

import sys
import os
from pathlib import Path
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QSpinBox, QLabel, QGroupBox, QCheckBox, QSlider,
    QComboBox, QTextEdit, QSplitter
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont

# Ajouter le chemin vers le module HRNeoWave
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from hrneowave.gui.theme import apply_skin
    from hrneowave.gui.widgets.etat_capteurs_dock import EtatCapteursDock
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Vérifiez que le module HRNeoWave est accessible")
    sys.exit(1)


class TestEtatCapteursWindow(QMainWindow):
    """Fenêtre de test pour le dock État Capteurs"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test HRNeoWave - Dock État Capteurs")
        self.setGeometry(100, 100, 1200, 800)
        
        # Créer le dock État Capteurs
        self.etat_capteurs_dock = EtatCapteursDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.etat_capteurs_dock)
        
        # Connecter les signaux
        self.etat_capteurs_dock.capteur_selected.connect(self._on_capteur_selected)
        self.etat_capteurs_dock.capteurs_updated.connect(self._on_capteurs_updated)
        
        # Créer l'interface de contrôle
        self._setup_ui()
        
        # Appliquer le thème
        apply_skin(self)
        
        # Timer pour simulation
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self._simulate_capteur_data)
        
        print("Interface de test État Capteurs initialisée")
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("Test du Dock État Capteurs HRNeoWave")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Contrôles de configuration
        config_group = QGroupBox("Configuration des Capteurs")
        config_layout = QHBoxLayout(config_group)
        
        # Nombre de capteurs
        config_layout.addWidget(QLabel("Nombre de capteurs:"))
        self.spin_capteurs = QSpinBox()
        self.spin_capteurs.setRange(1, 16)
        self.spin_capteurs.setValue(8)
        self.spin_capteurs.valueChanged.connect(self._on_nb_capteurs_changed)
        config_layout.addWidget(self.spin_capteurs)
        
        # Bouton appliquer config
        btn_apply_config = QPushButton("Appliquer Configuration")
        btn_apply_config.clicked.connect(self._apply_config)
        config_layout.addWidget(btn_apply_config)
        
        config_layout.addStretch()
        layout.addWidget(config_group)
        
        # Contrôles de simulation
        sim_group = QGroupBox("Simulation des Capteurs")
        sim_layout = QHBoxLayout(sim_group)
        
        # Boutons de contrôle
        self.btn_start_sim = QPushButton("Démarrer Simulation")
        self.btn_start_sim.clicked.connect(self._start_simulation)
        sim_layout.addWidget(self.btn_start_sim)
        
        self.btn_stop_sim = QPushButton("Arrêter Simulation")
        self.btn_stop_sim.clicked.connect(self._stop_simulation)
        self.btn_stop_sim.setEnabled(False)
        sim_layout.addWidget(self.btn_stop_sim)
        
        # Vitesse de simulation
        sim_layout.addWidget(QLabel("Vitesse (ms):"))
        self.slider_speed = QSlider(Qt.Horizontal)
        self.slider_speed.setRange(100, 2000)
        self.slider_speed.setValue(500)
        self.slider_speed.valueChanged.connect(self._on_speed_changed)
        sim_layout.addWidget(self.slider_speed)
        
        self.label_speed = QLabel("500 ms")
        sim_layout.addWidget(self.label_speed)
        
        sim_layout.addStretch()
        layout.addWidget(sim_group)
        
        # Contrôles manuels
        manual_group = QGroupBox("Contrôles Manuels")
        manual_layout = QVBoxLayout(manual_group)
        
        # Sélection capteur
        capteur_layout = QHBoxLayout()
        capteur_layout.addWidget(QLabel("Capteur:"))
        self.combo_capteur = QComboBox()
        self.combo_capteur.addItems([f"Capteur {i+1}" for i in range(8)])
        capteur_layout.addWidget(self.combo_capteur)
        
        # État
        capteur_layout.addWidget(QLabel("État:"))
        self.combo_etat = QComboBox()
        self.combo_etat.addItems(["Déconnecté", "Connecté", "Acquisition", "Erreur"])
        capteur_layout.addWidget(self.combo_etat)
        
        # Bouton appliquer
        btn_apply_manual = QPushButton("Appliquer")
        btn_apply_manual.clicked.connect(self._apply_manual_state)
        capteur_layout.addWidget(btn_apply_manual)
        
        capteur_layout.addStretch()
        manual_layout.addLayout(capteur_layout)
        
        # Boutons d'actions rapides
        actions_layout = QHBoxLayout()
        
        btn_all_connected = QPushButton("Tous Connectés")
        btn_all_connected.clicked.connect(lambda: self._set_all_capteurs("Connecté"))
        actions_layout.addWidget(btn_all_connected)
        
        btn_all_acquiring = QPushButton("Tous en Acquisition")
        btn_all_acquiring.clicked.connect(lambda: self._set_all_capteurs("Acquisition"))
        actions_layout.addWidget(btn_all_acquiring)
        
        btn_some_errors = QPushButton("Quelques Erreurs")
        btn_some_errors.clicked.connect(self._set_some_errors)
        actions_layout.addWidget(btn_some_errors)
        
        btn_all_disconnected = QPushButton("Tous Déconnectés")
        btn_all_disconnected.clicked.connect(lambda: self._set_all_capteurs("Déconnecté"))
        actions_layout.addWidget(btn_all_disconnected)
        
        actions_layout.addStretch()
        manual_layout.addLayout(actions_layout)
        
        layout.addWidget(manual_group)
        
        # Zone de log
        log_group = QGroupBox("Log des Événements")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        layout.addStretch()
    
    def _on_nb_capteurs_changed(self, value):
        """Met à jour la liste des capteurs dans le combo"""
        self.combo_capteur.clear()
        self.combo_capteur.addItems([f"Capteur {i+1}" for i in range(value)])
    
    def _apply_config(self):
        """Applique la configuration du nombre de capteurs"""
        nb_capteurs = self.spin_capteurs.value()
        self.etat_capteurs_dock.spin_nb_capteurs.setValue(nb_capteurs)
        self._log(f"Configuration appliquée: {nb_capteurs} capteurs")
    
    def _start_simulation(self):
        """Démarre la simulation"""
        self.etat_capteurs_dock.start_simulation()
        self.simulation_timer.start(self.slider_speed.value())
        self.btn_start_sim.setEnabled(False)
        self.btn_stop_sim.setEnabled(True)
        self._log("Simulation démarrée")
    
    def _stop_simulation(self):
        """Arrête la simulation"""
        self.etat_capteurs_dock.stop_simulation()
        self.simulation_timer.stop()
        self.btn_start_sim.setEnabled(True)
        self.btn_stop_sim.setEnabled(False)
        self._log("Simulation arrêtée")
    
    def _on_speed_changed(self, value):
        """Met à jour la vitesse de simulation"""
        self.label_speed.setText(f"{value} ms")
        if self.simulation_timer.isActive():
            self.simulation_timer.setInterval(value)
    
    def _simulate_capteur_data(self):
        """Simule des données de capteurs"""
        nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
        
        for capteur_id in range(1, nb_capteurs + 1):
            # Simuler des données aléatoires
            if random.random() < 0.1:  # 10% de chance de changer l'état
                continue
            
            # Données simulées
            amplitude = random.uniform(0.5, 2.5)
            frequence = random.uniform(0.8, 1.2)
            phase = random.uniform(-180, 180)
            
            self.etat_capteurs_dock.set_capteur_data(
                capteur_id,
                amplitude=amplitude,
                frequence=frequence,
                phase=phase
            )
    
    def _apply_manual_state(self):
        """Applique l'état manuel sélectionné"""
        capteur_text = self.combo_capteur.currentText()
        capteur_id = int(capteur_text.split()[-1])
        etat = self.combo_etat.currentText()
        
        self.etat_capteurs_dock.set_capteur_data(capteur_id, etat=etat)
        self._log(f"État manuel appliqué: {capteur_text} -> {etat}")
    
    def _set_all_capteurs(self, etat):
        """Définit l'état de tous les capteurs"""
        nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
        
        for capteur_id in range(1, nb_capteurs + 1):
            self.etat_capteurs_dock.set_capteur_data(capteur_id, etat=etat)
        
        self._log(f"Tous les capteurs définis à: {etat}")
    
    def _set_some_errors(self):
        """Définit quelques capteurs en erreur"""
        nb_capteurs = self.etat_capteurs_dock.spin_nb_capteurs.value()
        
        # Mettre 2-3 capteurs en erreur
        error_capteurs = random.sample(range(1, nb_capteurs + 1), min(3, nb_capteurs))
        
        for capteur_id in error_capteurs:
            self.etat_capteurs_dock.set_capteur_data(capteur_id, etat="Erreur")
        
        self._log(f"Capteurs en erreur: {error_capteurs}")
    
    def _on_capteur_selected(self, capteur_id):
        """Gère la sélection d'un capteur"""
        self._log(f"Capteur sélectionné: {capteur_id}")
        
        # Mettre à jour le combo
        self.combo_capteur.setCurrentText(f"Capteur {capteur_id}")
    
    def _on_capteurs_updated(self, capteurs_data):
        """Gère les mises à jour des capteurs"""
        capteurs = capteurs_data.get('capteurs', {})
        nb_connectes = sum(1 for c in capteurs.values() if c['etat'] in ['Connecté', 'Acquisition'])
        nb_acquisition = sum(1 for c in capteurs.values() if c['etat'] == 'Acquisition')
        nb_erreurs = sum(1 for c in capteurs.values() if c['etat'] == 'Erreur')
        
        status_msg = f"Capteurs: {nb_connectes}/{len(capteurs)} connectés"
        if nb_acquisition > 0:
            status_msg += f" | {nb_acquisition} en acquisition"
        if nb_erreurs > 0:
            status_msg += f" | {nb_erreurs} erreurs"
        
        self.statusBar().showMessage(status_msg)
    
    def _log(self, message):
        """Ajoute un message au log"""
        self.log_text.append(f"[{QTimer().remainingTime()}] {message}")
        print(f"LOG: {message}")


def main():
    """Fonction principale"""
    print("=== Test HRNeoWave - Dock État Capteurs ===")
    print("Démarrage de l'interface de test...")
    
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre de test
    window = TestEtatCapteursWindow()
    window.show()
    
    print("\n=== Instructions de Test ===")
    print("1. Vérifiez que le dock 'État Capteurs' est visible à gauche")
    print("2. Testez la configuration du nombre de capteurs")
    print("3. Démarrez la simulation et observez les mises à jour")
    print("4. Testez les contrôles manuels d'état")
    print("5. Cliquez sur les capteurs pour les sélectionner")
    print("6. Vérifiez l'application du thème HRNeoWave")
    print("7. Testez le redimensionnement et déplacement du dock")
    print("8. Observez les mises à jour de la barre de statut")
    
    # Lancer l'application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()