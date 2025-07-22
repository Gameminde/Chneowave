# -*- coding: utf-8 -*-
"""
Vue d'acquisition CHNeoWave
Étape 3 : Acquisition des données
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QSplitter, QDockWidget, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QProgressBar, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont, QColor
import numpy as np
from datetime import datetime

# Utilisation de l'adaptateur matplotlib pour compatibilité PySide6
from ..components.matplotlib_adapter import pg

class AcquisitionView(QWidget):
    """
    Vue d'acquisition des données
    Respecte le principe d'isolation : UNIQUEMENT l'acquisition
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Signal émis lorsque la session d'acquisition est terminée
        self.acquisitionFinished = Signal(dict)
        self.is_acquiring = False
        self.is_paused = False
        self.acquisition_data = []
        self.start_time = None
        self.setupUI()
        self.setupTimers()
        self.connectSignals()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur
        """
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Titre principal
        title_label = QLabel("Étape 3 : Acquisition des Données")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2980b9; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Splitter principal pour les graphiques
        self.main_splitter = QSplitter(Qt.Horizontal)
        
        # Zone des graphiques (côté gauche)
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        graphs_layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter vertical pour les 3 graphiques
        graphs_splitter = QSplitter(Qt.Vertical)
        
        # Graphique 1 : Séries temporelles
        self.time_series_plot = pg.PlotWidget()
        self.time_series_plot.setLabel('left', 'Amplitude (mm)')
        self.time_series_plot.setLabel('bottom', 'Temps (s)')
        self.time_series_plot.setTitle('Séries Temporelles')
        self.time_series_plot.setMinimumHeight(200)
        graphs_splitter.addWidget(self.time_series_plot)
        
        # Graphique 2 : Spectres de fréquence
        self.frequency_plot = pg.PlotWidget()
        self.frequency_plot.setLabel('left', 'Amplitude')
        self.frequency_plot.setLabel('bottom', 'Fréquence (Hz)')
        self.frequency_plot.setTitle('Spectres de Fréquence')
        self.frequency_plot.setMinimumHeight(200)
        graphs_splitter.addWidget(self.frequency_plot)
        
        # Graphique 3 : Analyse en temps réel
        self.realtime_plot = pg.PlotWidget()
        self.realtime_plot.setLabel('left', 'Hauteur (mm)')
        self.realtime_plot.setLabel('bottom', 'Temps (s)')
        self.realtime_plot.setTitle('Acquisition en Temps Réel')
        self.realtime_plot.setMinimumHeight(200)
        graphs_splitter.addWidget(self.realtime_plot)
        
        graphs_layout.addWidget(graphs_splitter)
        self.main_splitter.addWidget(graphs_widget)
        
        # Zone des docks (côté droit)
        docks_widget = QWidget()
        docks_layout = QVBoxLayout(docks_widget)
        docks_layout.setContentsMargins(10, 0, 0, 0)
        
        # Dock 1 : Infos Essai
        self.createTrialInfoDock(docks_layout)
        
        # Dock 2 : État Capteurs
        self.createSensorStatusDock(docks_layout)
        
        # Panneau de contrôle
        self.createControlPanel(docks_layout)
        
        docks_widget.setMaximumWidth(350)
        self.main_splitter.addWidget(docks_widget)
        
        # Configuration du splitter
        self.main_splitter.setSizes([800, 350])
        main_layout.addWidget(self.main_splitter)
    
    def createTrialInfoDock(self, parent_layout):
        """
        Création du dock d'informations d'essai
        """
        info_group = QGroupBox("Informations Essai")
        info_layout = QVBoxLayout(info_group)
        
        # Informations de base
        self.trial_info_text = QTextEdit()
        self.trial_info_text.setMaximumHeight(120)
        self.trial_info_text.setReadOnly(True)
        self.trial_info_text.setPlainText(
            "Projet: Projet Test\n"
            "Date: " + datetime.now().strftime("%d/%m/%Y %H:%M") + "\n"
            "Capteurs: 4 actifs\n"
            "Fréquence: 100 Hz\n"
            "Durée prévue: 300 s"
        )
        info_layout.addWidget(self.trial_info_text)
        
        # Barre de progression
        progress_label = QLabel("Progression:")
        info_layout.addWidget(progress_label)
        
        self.acquisition_progress = QProgressBar()
        self.acquisition_progress.setRange(0, 100)
        self.acquisition_progress.setValue(0)
        info_layout.addWidget(self.acquisition_progress)
        
        # Temps écoulé
        self.elapsed_time_label = QLabel("Temps écoulé: 00:00:00")
        info_layout.addWidget(self.elapsed_time_label)
        
        parent_layout.addWidget(info_group)
    
    def createSensorStatusDock(self, parent_layout):
        """
        Création du dock d'état des capteurs
        """
        sensor_group = QGroupBox("État des Capteurs")
        sensor_layout = QVBoxLayout(sensor_group)
        
        # Tableau des capteurs
        self.sensor_status_table = QTableWidget(4, 2)
        self.sensor_status_table.setHorizontalHeaderLabels(["Capteur", "État"])
        self.sensor_status_table.setMaximumHeight(150)
        
        # Remplissage du tableau
        for i in range(4):
            # Nom du capteur
            sensor_item = QTableWidgetItem(f"Capteur {i+1}")
            sensor_item.setFlags(Qt.ItemIsEnabled)
            self.sensor_status_table.setItem(i, 0, sensor_item)
            
            # État du capteur
            status_item = QTableWidgetItem("Prêt")
            status_item.setFlags(Qt.ItemIsEnabled)
            status_item.setBackground(QColor(39, 174, 96, 50))  # Vert léger
            self.sensor_status_table.setItem(i, 1, status_item)
        
        # Ajustement des colonnes
        self.sensor_status_table.resizeColumnsToContents()
        sensor_layout.addWidget(self.sensor_status_table)
        
        # Statistiques en temps réel
        stats_label = QLabel("Statistiques:")
        sensor_layout.addWidget(stats_label)
        
        self.stats_text = QTextEdit()
        self.stats_text.setMaximumHeight(80)
        self.stats_text.setReadOnly(True)
        self.stats_text.setPlainText(
            "Points acquis: 0\n"
            "Fréquence réelle: 0.0 Hz\n"
            "Amplitude max: 0.0 mm"
        )
    
    def reset_view(self):
        """
        Réinitialise la vue pour un nouveau projet
        """
        self.resetAcquisition()
    
    def set_calibration_data(self, calibration_data):
        """
        Configure la vue avec les données de calibration
        """
        # Mise à jour des informations d'essai avec les données de calibration
        sensor_count = calibration_data.get('sensor_count', 4)
        info_text = (
            f"Projet: {calibration_data.get('project_name', 'Projet Test')}\n"
            f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"Capteurs: {sensor_count} actifs\n"
            f"Fréquence: 100 Hz\n"
            f"Durée prévue: 300 s"
        )
        self.trial_info_text.setPlainText(info_text)
        
        # Mise à jour du tableau des capteurs
        self.sensor_status_table.setRowCount(sensor_count)
        for i in range(sensor_count):
            # Nom du capteur
            sensor_item = QTableWidgetItem(f"Capteur {i+1}")
            sensor_item.setFlags(Qt.ItemIsEnabled)
            self.sensor_status_table.setItem(i, 0, sensor_item)
            
            # État du capteur
            status_item = QTableWidgetItem("Prêt")
            status_item.setFlags(Qt.ItemIsEnabled)
            status_item.setBackground(QColor(39, 174, 96, 50))  # Vert léger
            self.sensor_status_table.setItem(i, 1, status_item)
        
        # Ajustement des colonnes
        self.sensor_status_table.resizeColumnsToContents()
        
        # Mise à jour des données de simulation
        self.sensor_data = [[] for _ in range(sensor_count)]
    
    def get_acquisition_data(self):
        """
        Retourne les données d'acquisition pour le workflow
        """
        return {
            'duration': self.current_time,
            'sample_rate': 100.0,
            'sensor_count': len(self.sensor_data),
            'time_data': self.time_data.copy(),
            'sensor_data': [data.copy() for data in self.sensor_data],
            'start_time': self.start_time,
            'end_time': datetime.now() if not self.is_acquiring else None,
            'status': 'acquiring' if self.is_acquiring else 'completed'
        }
        sensor_layout.addWidget(self.stats_text)
        
        parent_layout.addWidget(sensor_group)
    
    def createControlPanel(self, parent_layout):
        """
        Création du panneau de contrôle minimaliste
        """
        control_group = QGroupBox("Contrôle d'Acquisition")
        control_layout = QVBoxLayout(control_group)
        
        # Boutons de contrôle
        button_layout = QVBoxLayout()
        
        # Bouton Démarrer/Arrêter
        self.start_stop_button = QPushButton("Démarrer Acquisition")
        self.start_stop_button.setMinimumHeight(40)
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        button_layout.addWidget(self.start_stop_button)
        
        # Bouton Pause Affichage
        self.pause_display_button = QPushButton("Pause Affichage")
        self.pause_display_button.setMinimumHeight(35)
        self.pause_display_button.setEnabled(False)
        self.pause_display_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #34495e;
            }
        """)
        button_layout.addWidget(self.pause_display_button)
        
        control_layout.addLayout(button_layout)
        
        # Espacement
        control_layout.addStretch()
        
        parent_layout.addWidget(control_group)
        parent_layout.addStretch()
    
    def setupTimers(self):
        """
        Configuration des timers pour la simulation
        """
        # Timer pour la mise à jour des données
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.updateData)
        
        # Timer pour la mise à jour de l'interface
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.updateUI)
        
        # Données de simulation
        self.time_data = []
        self.sensor_data = [[] for _ in range(4)]
        self.current_time = 0.0
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.start_stop_button.clicked.connect(self.toggleAcquisition)
        self.pause_display_button.clicked.connect(self.toggleDisplayPause)
    
    def toggleAcquisition(self):
        """
        Basculement entre démarrage et arrêt de l'acquisition
        """
        if not self.is_acquiring:
            self.startAcquisition()
        else:
            self.stopAcquisition()
    
    def startAcquisition(self):
        """
        Démarrage de l'acquisition
        """
        self.is_acquiring = True
        self.start_time = datetime.now()
        
        # Mise à jour de l'interface
        self.start_stop_button.setText("Arrêter Acquisition")
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        self.pause_display_button.setEnabled(True)
        
        # Mise à jour du statut des capteurs
        for i in range(4):
            status_item = QTableWidgetItem("Acquisition")
            status_item.setFlags(Qt.ItemIsEnabled)
            status_item.setBackground(QColor(52, 152, 219, 50))  # Bleu léger
            self.sensor_status_table.setItem(i, 1, status_item)
        
        # Démarrage des timers
        self.data_timer.start(10)  # 100 Hz
        self.ui_timer.start(100)   # 10 Hz pour l'interface
        
        # Réinitialisation des données
        self.time_data.clear()
        for sensor_list in self.sensor_data:
            sensor_list.clear()
        self.current_time = 0.0
    
    def stopAcquisition(self):
        """
        Arrêt de l'acquisition
        """
        self.is_acquiring = False
        
        # Arrêt des timers
        self.data_timer.stop()
        self.ui_timer.stop()
        
        # Mise à jour de l'interface
        self.start_stop_button.setText("Démarrer Acquisition")
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        self.pause_display_button.setEnabled(False)
        self.pause_display_button.setText("Pause Affichage")
        
        # Mise à jour du statut des capteurs
        for i in range(4):
            status_item = QTableWidgetItem("Arrêté")
            status_item.setFlags(Qt.ItemIsEnabled)
            status_item.setBackground(QColor(149, 165, 166, 50))  # Gris léger
            self.sensor_status_table.setItem(i, 1, status_item)
        
        # Préparation des données pour l'émission du signal
        session_data = {
            'duration': self.current_time,
            'sample_rate': 100.0,
            'sensor_count': 4,
            'time_data': self.time_data.copy(),
            'sensor_data': [data.copy() for data in self.sensor_data],
            'start_time': self.start_time,
            'end_time': datetime.now()
        }
        
        # Émission du signal vers le MainController
        self.acquisitionFinished.emit(session_data)
    
    def toggleDisplayPause(self):
        """
        Basculement de la pause d'affichage
        """
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_display_button.setText("Reprendre Affichage")
            self.ui_timer.stop()
        else:
            self.pause_display_button.setText("Pause Affichage")
            if self.is_acquiring:
                self.ui_timer.start(100)
    
    def updateData(self):
        """
        Mise à jour des données (simulation)
        """
        if not self.is_acquiring:
            return
        
        # Génération de données simulées
        dt = 0.01  # 100 Hz
        self.current_time += dt
        self.time_data.append(self.current_time)
        
        # Simulation de vagues avec différentes fréquences pour chaque capteur
        for i in range(4):
            # Mélange de plusieurs fréquences pour simuler des vagues réalistes
            amplitude = (50 + 20 * np.sin(0.1 * self.current_time) *  # Variation lente
                        np.sin(2 * np.pi * (0.5 + 0.1 * i) * self.current_time) +  # Fréquence principale
                        10 * np.sin(2 * np.pi * (1.2 + 0.05 * i) * self.current_time) +  # Harmonique
                        5 * np.random.normal())  # Bruit
            
            self.sensor_data[i].append(amplitude)
        
        # Limitation de la taille des buffers (garder seulement les 1000 derniers points)
        max_points = 1000
        if len(self.time_data) > max_points:
            self.time_data = self.time_data[-max_points:]
            for sensor_list in self.sensor_data:
                sensor_list[:] = sensor_list[-max_points:]
    
    def updateUI(self):
        """
        Mise à jour de l'interface utilisateur
        """
        if not self.is_acquiring or self.is_paused:
            return
        
        # Mise à jour des graphiques
        self.updateGraphs()
        
        # Mise à jour des statistiques
        self.updateStatistics()
        
        # Mise à jour du temps écoulé
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            elapsed_str = str(elapsed).split('.')[0]  # Suppression des microsecondes
            self.elapsed_time_label.setText(f"Temps écoulé: {elapsed_str}")
        
        # Mise à jour de la barre de progression (simulation sur 300s)
        progress = min(100, (self.current_time / 300.0) * 100)
        self.acquisition_progress.setValue(int(progress))
    
    def updateGraphs(self):
        """
        Mise à jour des graphiques
        """
        if not self.time_data or not self.sensor_data[0]:
            return
        
        # Graphique temps réel (dernier capteur)
        self.realtime_plot.clear()
        self.realtime_plot.plot(self.time_data, self.sensor_data[0], pen='b')
        
        # Graphique séries temporelles (tous les capteurs)
        self.time_series_plot.clear()
        colors = ['r', 'g', 'b', 'y']
        for i, (data, color) in enumerate(zip(self.sensor_data, colors)):
            if data:
                self.time_series_plot.plot(self.time_data, data, pen=color, name=f'Capteur {i+1}')
        
        # Graphique fréquentiel (FFT du premier capteur)
        if len(self.sensor_data[0]) > 64:  # Minimum pour une FFT significative
            self.updateFrequencyPlot()
    
    def updateFrequencyPlot(self):
        """
        Mise à jour du graphique fréquentiel
        """
        try:
            # FFT des données du premier capteur
            data = np.array(self.sensor_data[0][-512:])  # Derniers 512 points
            fft = np.fft.fft(data)
            freqs = np.fft.fftfreq(len(data), 0.01)  # dt = 0.01s
            
            # Garder seulement les fréquences positives
            positive_freqs = freqs[:len(freqs)//2]
            positive_fft = np.abs(fft[:len(fft)//2])
            
            self.frequency_plot.clear()
            self.frequency_plot.plot(positive_freqs, positive_fft, pen='r')
        except Exception:
            pass  # Ignorer les erreurs de FFT
    
    def updateStatistics(self):
        """
        Mise à jour des statistiques
        """
        if not self.sensor_data[0]:
            return
        
        # Calcul des statistiques
        points_count = len(self.time_data)
        real_frequency = points_count / max(self.current_time, 0.01)
        max_amplitude = max(max(data) if data else [0] for data in self.sensor_data)
        
        stats_text = (
            f"Points acquis: {points_count}\n"
            f"Fréquence réelle: {real_frequency:.1f} Hz\n"
            f"Amplitude max: {max_amplitude:.1f} mm"
        )
        
        self.stats_text.setPlainText(stats_text)
    
    def resetAcquisition(self):
        """
        Réinitialisation de l'acquisition
        """
        if self.is_acquiring:
            self.stopAcquisition()
        
        # Nettoyage des données
        self.time_data.clear()
        for sensor_list in self.sensor_data:
            sensor_list.clear()
        self.current_time = 0.0
        
        # Nettoyage des graphiques
        self.time_series_plot.clear()
        self.frequency_plot.clear()
        self.realtime_plot.clear()
        
        # Réinitialisation de l'interface
        self.acquisition_progress.setValue(0)
        self.elapsed_time_label.setText("Temps écoulé: 00:00:00")
        self.stats_text.setPlainText(
            "Points acquis: 0\n"
            "Fréquence réelle: 0.0 Hz\n"
            "Amplitude max: 0.0 mm"
        )
    
    def set_controller(self, controller):
        """
        Définit le contrôleur d'acquisition pour cette vue
        """
        self.controller = controller
        print(f"[DEBUG] Contrôleur d'acquisition défini: {controller}")
        
        # Connecter les signaux du contrôleur si nécessaire
        if hasattr(controller, 'acquisition_started'):
            controller.acquisition_started.connect(self._on_controller_acquisition_started)
        if hasattr(controller, 'acquisition_stopped'):
            controller.acquisition_stopped.connect(self._on_controller_acquisition_stopped)
    
    def _on_controller_acquisition_started(self):
        """Gestionnaire pour le démarrage d'acquisition depuis le contrôleur"""
        print("[DEBUG] Acquisition démarrée depuis le contrôleur")
    
    def _on_controller_acquisition_stopped(self):
        """Gestionnaire pour l'arrêt d'acquisition depuis le contrôleur"""
        print("[DEBUG] Acquisition arrêtée depuis le contrôleur")