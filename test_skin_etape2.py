#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'étape 2 : Dock "Infos essai"
Validation de l'intégration du dock dans l'interface principale
"""

import sys
import os
from datetime import datetime

# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
        QWidget, QPushButton, QLabel, QGroupBox, QSpinBox,
        QDoubleSpinBox, QLineEdit, QTextEdit, QMessageBox
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal
    from PyQt5.QtGui import QFont
except ImportError:
    print("Erreur: PyQt5 non disponible")
    sys.exit(1)

try:
    from hrneowave.gui.theme import apply_skin
    from hrneowave.gui.widgets.infos_essai_dock import InfosEssaiDock
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)


class TestMainWindow(QMainWindow):
    """Fenêtre de test pour le dock Infos essai"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test HRNeoWave - Dock Infos Essai")
        self.setGeometry(100, 100, 1200, 800)
        
        # Variables de test
        self.is_acquiring = False
        self.sample_count = 0
        self.acquisition_timer = QTimer()
        self.acquisition_timer.timeout.connect(self._simulate_acquisition)
        
        # Configuration de l'interface
        self._setup_ui()
        self._setup_dock()
        
        # Appliquer le thème HRNeoWave
        apply_skin(self, 'dark')
        
        print("\n=== Test du Dock Infos Essai ===")
        print("1. Vérifiez que le dock 'Infos essai' apparaît à droite")
        print("2. Testez les boutons de contrôle d'acquisition")
        print("3. Observez la mise à jour en temps réel des informations")
        print("4. Vérifiez l'application du thème HRNeoWave")
        print("5. Testez le redimensionnement et le déplacement du dock")
    
    def _setup_ui(self):
        """Configure l'interface utilisateur principale"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("Test du Dock Infos Essai - HRNeoWave")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Groupe de contrôles de test
        controls_group = QGroupBox("Contrôles de Test")
        controls_layout = QVBoxLayout(controls_group)
        
        # Configuration d'essai
        config_layout = QHBoxLayout()
        
        config_layout.addWidget(QLabel("Nom essai:"))
        self.essai_name = QLineEdit("Test_Acquisition_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        config_layout.addWidget(self.essai_name)
        
        config_layout.addWidget(QLabel("Opérateur:"))
        self.operateur = QLineEdit("Ingénieur Test")
        config_layout.addWidget(self.operateur)
        
        controls_layout.addLayout(config_layout)
        
        # Configuration technique
        tech_layout = QHBoxLayout()
        
        tech_layout.addWidget(QLabel("Nb sondes:"))
        self.nb_sondes = QSpinBox()
        self.nb_sondes.setRange(1, 16)
        self.nb_sondes.setValue(4)
        tech_layout.addWidget(self.nb_sondes)
        
        tech_layout.addWidget(QLabel("Fréq. (Hz):"))
        self.freq_ech = QSpinBox()
        self.freq_ech.setRange(100, 10000)
        self.freq_ech.setValue(1000)
        tech_layout.addWidget(self.freq_ech)
        
        tech_layout.addWidget(QLabel("Buffer:"))
        self.buffer_size = QSpinBox()
        self.buffer_size.setRange(1000, 100000)
        self.buffer_size.setValue(10000)
        tech_layout.addWidget(self.buffer_size)
        
        controls_layout.addLayout(tech_layout)
        
        # Boutons de contrôle
        buttons_layout = QHBoxLayout()
        
        self.btn_configure = QPushButton("Configurer Essai")
        self.btn_configure.clicked.connect(self._configure_essai)
        buttons_layout.addWidget(self.btn_configure)
        
        self.btn_start = QPushButton("Démarrer Acquisition")
        self.btn_start.clicked.connect(self._start_acquisition)
        buttons_layout.addWidget(self.btn_start)
        
        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self._pause_acquisition)
        self.btn_pause.setEnabled(False)
        buttons_layout.addWidget(self.btn_pause)
        
        self.btn_stop = QPushButton("Arrêter")
        self.btn_stop.clicked.connect(self._stop_acquisition)
        self.btn_stop.setEnabled(False)
        buttons_layout.addWidget(self.btn_stop)
        
        controls_layout.addLayout(buttons_layout)
        
        layout.addWidget(controls_group)
        
        # Zone de log
        log_group = QGroupBox("Log des événements")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        layout.addStretch()
    
    def _setup_dock(self):
        """Configure le dock Infos essai"""
        try:
            self.infos_dock = InfosEssaiDock(self)
            self.addDockWidget(Qt.RightDockWidgetArea, self.infos_dock)
            
            # Connecter les signaux
            self.infos_dock.essai_updated.connect(self._on_essai_updated)
            
            self._log("Dock 'Infos essai' créé et configuré avec succès")
            
        except Exception as e:
            self._log(f"Erreur lors de la création du dock: {e}")
            QMessageBox.critical(self, "Erreur", f"Impossible de créer le dock: {e}")
    
    def _configure_essai(self):
        """Configure les informations d'essai"""
        if hasattr(self, 'infos_dock'):
            self.infos_dock.set_essai_info(
                nom=self.essai_name.text(),
                operateur=self.operateur.text(),
                configuration=f"Sondes: {self.nb_sondes.value()}, Freq: {self.freq_ech.value()}Hz"
            )
            
            self.infos_dock.set_acquisition_config(
                nb_sondes=self.nb_sondes.value(),
                freq_echantillonnage=self.freq_ech.value(),
                taille_buffer=self.buffer_size.value()
            )
            
            self._log(f"Essai configuré: {self.essai_name.text()}")
    
    def _start_acquisition(self):
        """Démarre l'acquisition de test"""
        if hasattr(self, 'infos_dock'):
            self.infos_dock.start_essai(
                nom=self.essai_name.text(),
                operateur=self.operateur.text(),
                configuration=f"Sondes: {self.nb_sondes.value()}, Freq: {self.freq_ech.value()}Hz"
            )
            
            self.is_acquiring = True
            self.sample_count = 0
            self.acquisition_timer.start(100)  # Mise à jour toutes les 100ms
            
            # Mise à jour des boutons
            self.btn_start.setEnabled(False)
            self.btn_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)
            
            self._log("Acquisition démarrée")
    
    def _pause_acquisition(self):
        """Met en pause l'acquisition"""
        if hasattr(self, 'infos_dock'):
            if self.is_acquiring:
                self.infos_dock.pause_essai()
                self.acquisition_timer.stop()
                self.is_acquiring = False
                self.btn_pause.setText("Reprendre")
                self._log("Acquisition mise en pause")
            else:
                self.infos_dock.resume_essai()
                self.acquisition_timer.start(100)
                self.is_acquiring = True
                self.btn_pause.setText("Pause")
                self._log("Acquisition reprise")
    
    def _stop_acquisition(self):
        """Arrête l'acquisition"""
        if hasattr(self, 'infos_dock'):
            self.infos_dock.stop_essai()
            self.acquisition_timer.stop()
            self.is_acquiring = False
            
            # Mise à jour des boutons
            self.btn_start.setEnabled(True)
            self.btn_pause.setEnabled(False)
            self.btn_pause.setText("Pause")
            self.btn_stop.setEnabled(False)
            
            self._log(f"Acquisition arrêtée - Total: {self.sample_count:,} échantillons")
    
    def _simulate_acquisition(self):
        """Simule l'acquisition de données"""
        if self.is_acquiring and hasattr(self, 'infos_dock'):
            # Simuler l'arrivée d'échantillons
            increment = self.freq_ech.value() // 10  # 100ms d'échantillons
            self.sample_count += increment
            
            self.infos_dock.update_echantillons(self.sample_count)
    
    def _on_essai_updated(self, essai_data):
        """Gère les mises à jour du dock"""
        statut = essai_data.get('statut', 'Inconnu')
        nom = essai_data.get('nom', 'Essai')
        duree = essai_data.get('duree', '00:00:00')
        nb_echantillons = essai_data.get('nb_echantillons', 0)
        
        # Mettre à jour la barre de statut
        if statut == 'En cours':
            self.statusBar().showMessage(
                f"Acquisition en cours - {nom} - Durée: {duree} - Échantillons: {nb_echantillons:,}"
            )
        elif statut == 'Pause':
            self.statusBar().showMessage(f"Acquisition en pause - {nom} - Échantillons: {nb_echantillons:,}")
        elif statut == 'Arrêté':
            self.statusBar().showMessage(f"Acquisition arrêtée - {nom} - Total: {nb_echantillons:,} échantillons")
        else:
            self.statusBar().showMessage(f"Statut: {statut} - {nom}")
    
    def _log(self, message):
        """Ajoute un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")


def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("HRNeoWave Test")
    app.setApplicationVersion("2.0")
    
    try:
        # Créer et afficher la fenêtre de test
        window = TestMainWindow()
        window.show()
        
        # Lancer l'application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()