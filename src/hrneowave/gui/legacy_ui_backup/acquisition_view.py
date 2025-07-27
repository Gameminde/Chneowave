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
from PySide6.QtCore import Signal, Slot, Qt, QTimer
from PySide6.QtGui import QFont, QColor
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Utilisation de l'adaptateur matplotlib pour compatibilité PySide6
from ..components.matplotlib_adapter import pg

class AcquisitionView(QWidget):
    """
    Vue d'acquisition des données
    Respecte le principe d'isolation : UNIQUEMENT l'acquisition
    """
    # Signal émis lorsque la session d'acquisition est terminée
    acquisitionFinished = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_acquiring = False
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
        
        # Zone des graphiques (côté gauche) - optimisée pour plus d'espace
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        graphs_layout.setContentsMargins(5, 5, 5, 5)  # Marges réduites
        graphs_layout.setSpacing(8)  # Espacement réduit
        
        # Titre de la section graphiques - plus compact
        graphs_title = QLabel("Visualisation des Données")
        graphs_title.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #2c3e50;
                padding: 6px 10px;
                background-color: #ecf0f1;
                border-radius: 4px;
                margin-bottom: 5px;
            }
        """)
        graphs_layout.addWidget(graphs_title)
        
        # Splitter vertical pour les 3 graphiques avec proportions optimisées
        graphs_splitter = QSplitter(Qt.Vertical)
        graphs_splitter.setChildrenCollapsible(False)  # Empêche la réduction complète
        
        # Graphique 1 : Séries temporelles - hauteur optimisée
        self.time_series_plot = pg.PlotWidget()
        self.time_series_plot.setLabel('left', 'Amplitude (mm)')
        self.time_series_plot.setLabel('bottom', 'Temps (s)')
        self.time_series_plot.setTitle('Séries Temporelles')
        self.time_series_plot.setMinimumHeight(400)  # Augmenté pour plus d'espace
        graphs_splitter.addWidget(self.time_series_plot)
        
        # Graphique 2 : Spectres de fréquence - hauteur optimisée
        self.frequency_plot = pg.PlotWidget()
        self.frequency_plot.setLabel('left', 'Amplitude')
        self.frequency_plot.setLabel('bottom', 'Fréquence (Hz)')
        self.frequency_plot.setTitle('Spectres de Fréquence')
        self.frequency_plot.setMinimumHeight(380)  # Augmenté pour plus d'espace
        graphs_splitter.addWidget(self.frequency_plot)
        
        # Graphique 3 : Analyse en temps réel - hauteur optimisée
        self.realtime_plot = pg.PlotWidget()
        self.realtime_plot.setLabel('left', 'Hauteur (mm)')
        self.realtime_plot.setLabel('bottom', 'Temps (s)')
        self.realtime_plot.setTitle('Acquisition en Temps Réel')
        self.realtime_plot.setMinimumHeight(380)  # Augmenté pour plus d'espace
        graphs_splitter.addWidget(self.realtime_plot)
        
        # Configuration des proportions optimisées pour les graphiques
        graphs_splitter.setSizes([450, 400, 400])  # Plus d'espace pour le graphique principal
        graphs_layout.addWidget(graphs_splitter)
        
        # Ajout d'une barre de contrôle minimaliste en bas
        control_bar = QWidget()
        control_bar_layout = QHBoxLayout(control_bar)
        control_bar_layout.setContentsMargins(10, 5, 10, 5)
        control_bar.setMaximumHeight(60)  # Barre compacte
        control_bar.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
        """)
        
        # Boutons de contrôle essentiels dans la barre
        self.start_stop_button = QPushButton("Démarrer Acquisition")
        self.start_stop_button.setMinimumHeight(40)
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        control_bar_layout.addWidget(self.start_stop_button)
        
        # Indicateur de statut compact
        self.status_label = QLabel("Prêt")
        self.status_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #495057;
                padding: 8px 12px;
                background-color: #e9ecef;
                border-radius: 4px;
            }
        """)
        control_bar_layout.addWidget(self.status_label)
        
        # Temps écoulé compact
        self.elapsed_time_label = QLabel("Temps: 00:00:00")
        self.elapsed_time_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #495057;
                padding: 8px 12px;
                background-color: #e9ecef;
                border-radius: 4px;
            }
        """)
        control_bar_layout.addWidget(self.elapsed_time_label)
        
        # Barre de progression compacte
        self.acquisition_progress = QProgressBar()
        self.acquisition_progress.setRange(0, 100)
        self.acquisition_progress.setValue(0)
        self.acquisition_progress.setMaximumWidth(200)
        self.acquisition_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                text-align: center;
                font-size: 11px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 3px;
            }
        """)
        control_bar_layout.addWidget(self.acquisition_progress)
        
        control_bar_layout.addStretch()  # Pousse les éléments vers la gauche
        
        # Ajout des widgets au layout principal
        main_layout.addWidget(graphs_widget)
        main_layout.addWidget(control_bar)
        
        # Flag pour savoir si les grilles ont été configurées
        self._grids_configured = False
    
    # Méthode supprimée - les informations sont maintenant dans la barre de contrôle
    
    # Méthode supprimée - les informations des capteurs sont maintenant intégrées dans l'interface principale
    
    def showEvent(self, event):
        """Configure les grilles des graphiques lors de l'affichage."""
        super().showEvent(event)
        if not self._grids_configured:
            try:
                # Configuration des grilles pour chaque graphique
                time_plot_item = self.time_series_plot.getPlotItem()
                time_plot_item.showGrid(x=True, y=True, alpha=0.3)
                
                freq_plot_item = self.frequency_plot.getPlotItem()
                freq_plot_item.showGrid(x=True, y=True, alpha=0.3)
                
                realtime_plot_item = self.realtime_plot.getPlotItem()
                realtime_plot_item.showGrid(x=True, y=True, alpha=0.3)
                
                self._grids_configured = True
            except Exception as e:
                print(f"Erreur lors de la configuration des grilles: {e}")
    
    def reset_view(self):
        """
        Réinitialise la vue pour un nouveau projet
        """
        self.resetAcquisition()
    
    def set_calibration_data(self, calibration_data):
        """
        Configure la vue avec les données de calibration
        """
        # Configuration simplifiée - les informations sont maintenant dans la barre de statut
        sensor_count = calibration_data.get('sensor_count', 4)
        project_name = calibration_data.get('project_name', 'Projet Test')
        
        # Mise à jour du statut avec les informations du projet
        self.status_label.setText(f"Prêt - {project_name} ({sensor_count} capteurs)")
        
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
    
    # Méthode supprimée - les contrôles sont maintenant dans la barre de contrôle en bas
    
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
    
    def toggleAcquisition(self):
        """
        Basculement entre démarrage et arrêt de l'acquisition
        """
        logger.debug(f"toggleAcquisition called. is_acquiring: {self.is_acquiring}")
        if not self.is_acquiring:
            self.startAcquisition()
        else:
            self.stopAcquisition()
    
    def startAcquisition(self):
        """
        Démarrage de l'acquisition
        """
        logger.info("Démarrage de l'acquisition")
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
        
        # Mise à jour du statut
        self.status_label.setText("Acquisition en cours")
        
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
        logger.info("Arrêt de l'acquisition")
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
        
        # Mise à jour du statut
        self.status_label.setText("Prêt")
        

    
    def finishAcquisition(self):
        """
        Termine la session d'acquisition et émet les données.
        """
        logger.debug("finishAcquisition called.")
        if self.is_acquiring:
            self.stopAcquisition()

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
        logger.info("Émission du signal acquisitionFinished")
        self.acquisitionFinished.emit(session_data)
        self.status_label.setText("Acquisition terminée")

    # Méthode supprimée - la pause d'affichage n'est plus disponible dans l'interface simplifiée
    
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
        if not self.is_acquiring:
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
        Mise à jour des statistiques - simplifiée
        """
        if not self.sensor_data[0]:
            return
        
        # Les statistiques sont maintenant affichées dans la barre de statut
        # Cette méthode est conservée pour d'éventuelles extensions futures
        pass
    
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
        self.elapsed_time_label.setText("Temps: 00:00:00")
        self.status_label.setText("Prêt")
    
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