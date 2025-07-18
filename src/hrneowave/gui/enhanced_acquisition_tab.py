# enhanced_acquisition_tab.py - Module d'acquisition avec transitions et feedback
import sys
import os
from typing import Dict, Any, Optional
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QPushButton,
    QProgressBar, QTextEdit, QFormLayout, QSpinBox, QDoubleSpinBox,
    QComboBox, QCheckBox, QFrame, QSplitter, QScrollArea, QGridLayout,
    QSizePolicy, QMessageBox, QApplication
)
from PyQt5.QtCore import (
    Qt, pyqtSignal, pyqtSlot, QTimer, QThread, QObject, QPropertyAnimation,
    QEasingCurve, QRect, QSize
)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QPainter

try:
    import pyqtgraph as pg
    from pyqtgraph import PlotWidget, mkPen
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False
    print("⚠️ PyQtGraph non disponible pour l'acquisition")

try:
    from .field_validator import FieldValidator
    from .theme import register_theme_callback
    from hrneowave.gui.theme import get_theme_colors
except ImportError as e:
    print(f"⚠️ Import manquant: {e}")
    FieldValidator = None
    
    # Fonction de fallback si import échoue
    def get_theme_colors(theme=None):
        return {
            'background': '#2c3e50',
            'foreground': '#ecf0f1',
            'accent': '#3498db'
        }

class AcquisitionWorker(QObject):
    """Worker thread pour l'acquisition de données"""
    
    dataReady = pyqtSignal(list, float)  # data, timestamp
    progressUpdated = pyqtSignal(int)  # pourcentage
    statusChanged = pyqtSignal(str)  # statut
    acquisitionFinished = pyqtSignal(dict)  # résultats
    errorOccurred = pyqtSignal(str)  # erreur
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.is_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self._generate_data)
        self.start_time = None
        self.sample_count = 0
        
    def start_acquisition(self):
        """Démarre l'acquisition"""
        if self.is_running:
            return
            
        self.is_running = True
        self.start_time = datetime.now()
        self.sample_count = 0
        
        # Calculer l'intervalle basé sur la fréquence d'échantillonnage
        sample_rate = self.config.get('sample_rate', 32.0)
        interval_ms = int(1000 / sample_rate)
        
        self.statusChanged.emit("Acquisition en cours...")
        self.timer.start(interval_ms)
        
    def stop_acquisition(self):
        """Arrête l'acquisition"""
        if not self.is_running:
            return
            
        self.is_running = False
        self.timer.stop()
        
        # Calculer les statistiques finales
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        results = {
            'duration': duration,
            'samples': self.sample_count,
            'sample_rate': self.sample_count / duration if duration > 0 else 0,
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat()
        }
        
        self.statusChanged.emit("Acquisition terminée")
        self.acquisitionFinished.emit(results)
        
    def _generate_data(self):
        """Génère des données simulées"""
        import random
        import math
        
        try:
            n_channels = self.config.get('n_channels', 4)
            timestamp = datetime.now().timestamp()
            
            # Générer des données simulées (houle)
            data = []
            for i in range(n_channels):
                # Simulation d'une houle avec bruit
                t = self.sample_count * 0.1
                amplitude = 0.5 + 0.3 * math.sin(0.1 * t)
                frequency = 0.2 + 0.1 * i
                noise = random.gauss(0, 0.05)
                
                value = amplitude * math.sin(frequency * t) + noise
                data.append(value)
                
            self.sample_count += 1
            
            # Émettre les données
            self.dataReady.emit(data, timestamp)
            
            # Mettre à jour le progrès (simulation)
            max_duration = self.config.get('max_duration', 60)  # 60 secondes max
            if self.start_time:
                elapsed = (datetime.now() - self.start_time).total_seconds()
                progress = min(int((elapsed / max_duration) * 100), 100)
                self.progressUpdated.emit(progress)
                
                # Arrêt automatique après durée max
                if elapsed >= max_duration:
                    self.stop_acquisition()
                    
        except Exception as e:
            self.errorOccurred.emit(f"Erreur acquisition: {e}")
            self.stop_acquisition()

class RealTimePlotWidget(QWidget):
    """Widget de graphique temps réel optimisé"""
    
    def __init__(self, n_channels: int = 4, parent=None):
        super().__init__(parent)
        self.n_channels = n_channels
        self.max_points = 1000  # Limiter pour performance
        self.data_buffers = [[] for _ in range(n_channels)]
        self.time_buffer = []
        
        self._init_ui()
        self._setup_plots()
        
    def _init_ui(self):
        """Initialise l'interface du graphique"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        if not PYQTGRAPH_AVAILABLE:
            error_label = QLabel("PyQtGraph non disponible")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)
            return
            
        # Widget de graphique
        self.plot_widget = PlotWidget()
        self.plot_widget.setLabel('left', 'Amplitude (m)')
        self.plot_widget.setLabel('bottom', 'Temps (s)')
        self.plot_widget.setTitle('Acquisition Temps Réel - Houle')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setMenuEnabled(False)
        
        layout.addWidget(self.plot_widget)
        
    def _setup_plots(self):
        """Configure les courbes de données"""
        if not PYQTGRAPH_AVAILABLE:
            return
            
        self.curves = []
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
        
        for i in range(self.n_channels):
            color = colors[i % len(colors)]
            pen = mkPen(color=color, width=2)
            curve = self.plot_widget.plot(pen=pen, name=f'Sonde {i+1}')
            self.curves.append(curve)
            
        # Légende
        self.plot_widget.addLegend()
        
    @pyqtSlot(list, float)
    def update_data(self, data: list, timestamp: float):
        """Met à jour les données du graphique"""
        if not PYQTGRAPH_AVAILABLE or len(data) != self.n_channels:
            return
            
        try:
            # Ajouter les nouvelles données
            self.time_buffer.append(timestamp)
            
            for i, value in enumerate(data):
                self.data_buffers[i].append(value)
                
            # Limiter la taille des buffers pour la performance
            if len(self.time_buffer) > self.max_points:
                self.time_buffer = self.time_buffer[-self.max_points:]
                for buffer in self.data_buffers:
                    buffer[:] = buffer[-self.max_points:]
                    
            # Mettre à jour les courbes
            for i, curve in enumerate(self.curves):
                if i < len(self.data_buffers):
                    curve.setData(self.time_buffer, self.data_buffers[i])
                    
        except Exception as e:
            print(f"⚠️ Erreur mise à jour graphique: {e}")
            
    def clear_data(self):
        """Efface toutes les données"""
        self.time_buffer.clear()
        for buffer in self.data_buffers:
            buffer.clear()
            
        if PYQTGRAPH_AVAILABLE:
            for curve in self.curves:
                curve.clear()

class EnhancedAcquisitionTab(QWidget):
    """Onglet d'acquisition amélioré avec transitions et feedback"""
    
    validationChanged = pyqtSignal(bool)
    acquisitionStarted = pyqtSignal(dict)  # config
    acquisitionFinished = pyqtSignal(dict)  # résultats
    
    def __init__(self, config: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.config = config
        self.validator = FieldValidator() if FieldValidator else None
        self.acquisition_worker = None
        self.worker_thread = None
        self.is_acquiring = False
        
        self._init_ui()
        self._setup_validation()
        self._setup_animations()
        
        # Enregistrer callback thème
        register_theme_callback(self._on_theme_changed)
        
    def _init_ui(self):
        """Initialise l'interface d'acquisition"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Titre avec animation
        self.title_label = QLabel("🚀 Acquisition de Données")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_splitter)
        
        # Panneau de contrôle (gauche)
        control_panel = self._create_control_panel()
        main_splitter.addWidget(control_panel)
        
        # Panneau graphique (droite)
        plot_panel = self._create_plot_panel()
        main_splitter.addWidget(plot_panel)
        
        # Ratio golden pour le splitter
        main_splitter.setSizes([int(self.width() * 0.382), int(self.width() * 0.618)])
        
        # Barre de statut
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Prêt pour l'acquisition")
        self.status_label.setStyleSheet("color: #27ae60; font-weight: bold; padding: 5px;")
        status_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        status_layout.addWidget(self.progress_bar)
        
        layout.addLayout(status_layout)
        
    def _create_control_panel(self) -> QWidget:
        """Crée le panneau de contrôle"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Configuration acquisition
        config_group = QGroupBox("⚙️ Configuration")
        config_layout = QFormLayout(config_group)
        
        # Durée d'acquisition
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 3600)  # 1 sec à 1 heure
        self.duration_spin.setValue(60)
        self.duration_spin.setSuffix(" sec")
        config_layout.addRow("Durée:", self.duration_spin)
        
        # Fréquence d'échantillonnage
        self.sample_rate_spin = QDoubleSpinBox()
        self.sample_rate_spin.setRange(0.1, 1000.0)
        self.sample_rate_spin.setValue(self.config.get('sample_rate', 32.0))
        self.sample_rate_spin.setSuffix(" Hz")
        config_layout.addRow("Fréquence:", self.sample_rate_spin)
        
        # Nombre de canaux
        self.channels_spin = QSpinBox()
        self.channels_spin.setRange(1, 8)
        self.channels_spin.setValue(self.config.get('n_channels', 4))
        config_layout.addRow("Canaux:", self.channels_spin)
        
        # Mode d'acquisition
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Continu",
            "Déclenché",
            "Burst",
            "Calibration"
        ])
        config_layout.addRow("Mode:", self.mode_combo)
        
        # Sauvegarde automatique
        self.auto_save_check = QCheckBox("Sauvegarde automatique")
        self.auto_save_check.setChecked(True)
        config_layout.addRow(self.auto_save_check)
        
        layout.addWidget(config_group)
        
        # Contrôles d'acquisition
        controls_group = QGroupBox("🎮 Contrôles")
        controls_layout = QVBoxLayout(controls_group)
        
        # Boutons principaux
        buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Démarrer")
        self.start_btn.setObjectName("startButton")
        self.start_btn.clicked.connect(self._start_acquisition)
        buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Arrêter")
        self.stop_btn.setObjectName("stopButton")
        self.stop_btn.clicked.connect(self._stop_acquisition)
        self.stop_btn.setEnabled(False)
        buttons_layout.addWidget(self.stop_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.clicked.connect(self._pause_acquisition)
        self.pause_btn.setEnabled(False)
        buttons_layout.addWidget(self.pause_btn)
        
        controls_layout.addLayout(buttons_layout)
        
        # Boutons secondaires
        secondary_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("🗑 Effacer")
        self.clear_btn.clicked.connect(self._clear_data)
        secondary_layout.addWidget(self.clear_btn)
        
        self.export_btn = QPushButton("💾 Exporter")
        self.export_btn.clicked.connect(self._export_data)
        self.export_btn.setEnabled(False)
        secondary_layout.addWidget(self.export_btn)
        
        controls_layout.addLayout(secondary_layout)
        
        layout.addWidget(controls_group)
        
        # Statistiques temps réel
        stats_group = QGroupBox("📊 Statistiques")
        stats_layout = QFormLayout(stats_group)
        
        self.samples_label = QLabel("0")
        stats_layout.addRow("Échantillons:", self.samples_label)
        
        self.rate_label = QLabel("0.0 Hz")
        stats_layout.addRow("Taux réel:", self.rate_label)
        
        self.duration_label = QLabel("00:00")
        stats_layout.addRow("Durée:", self.duration_label)
        
        layout.addWidget(stats_group)
        
        # Log des événements
        log_group = QGroupBox("📝 Journal")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        layout.addStretch()
        return panel
        
    def _create_plot_panel(self) -> QWidget:
        """Crée le panneau de graphiques"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Graphique temps réel
        self.plot_widget = RealTimePlotWidget(
            n_channels=self.config.get('n_channels', 4)
        )
        layout.addWidget(self.plot_widget)
        
        return panel
        
    def _setup_validation(self):
        """Configure la validation des champs"""
        if not self.validator:
            self.validationChanged.emit(True)
            return
            
        # Ajouter les champs à valider
        self.validator.add_field(
            "duration", 
            self.duration_spin, 
            required=True,
            rules={'min_value': 1, 'max_value': 3600}
        )
        
        self.validator.add_field(
            "sample_rate", 
            self.sample_rate_spin, 
            required=True,
            rules={'min_value': 0.1, 'max_value': 1000.0}
        )
        
        # Connecter le signal de validation
        self.validator.validationChanged.connect(self.validationChanged.emit)
        
        # Validation initiale
        self.validator.validate_all()
        
    def _setup_animations(self):
        """Configure les animations d'interface"""
        # Animation du titre
        self.title_animation = QPropertyAnimation(self.title_label, b"geometry")
        self.title_animation.setDuration(500)
        self.title_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def _start_acquisition(self):
        """Démarre l'acquisition"""
        if self.is_acquiring:
            return
            
        try:
            # Valider la configuration
            if self.validator and not self.validator.validate_all()[0]:
                QMessageBox.warning(self, "Validation", "Veuillez corriger les erreurs de configuration.")
                return
                
            # Préparer la configuration
            acquisition_config = {
                'duration': self.duration_spin.value(),
                'sample_rate': self.sample_rate_spin.value(),
                'n_channels': self.channels_spin.value(),
                'mode': self.mode_combo.currentText(),
                'auto_save': self.auto_save_check.isChecked(),
                'max_duration': self.duration_spin.value()
            }
            
            # Créer le worker
            self.acquisition_worker = AcquisitionWorker(acquisition_config)
            self.worker_thread = QThread()
            self.acquisition_worker.moveToThread(self.worker_thread)
            
            # Connecter les signaux
            self.acquisition_worker.dataReady.connect(self.plot_widget.update_data)
            self.acquisition_worker.dataReady.connect(self._update_stats)
            self.acquisition_worker.progressUpdated.connect(self.progress_bar.setValue)
            self.acquisition_worker.statusChanged.connect(self._update_status)
            self.acquisition_worker.acquisitionFinished.connect(self._on_acquisition_finished)
            self.acquisition_worker.errorOccurred.connect(self._on_error)
            
            # Démarrer le thread
            self.worker_thread.started.connect(self.acquisition_worker.start_acquisition)
            self.worker_thread.start()
            
            # Mettre à jour l'interface
            self.is_acquiring = True
            self._update_ui_state()
            
            # Effacer les données précédentes
            self.plot_widget.clear_data()
            
            # Afficher la barre de progression
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Log
            self._log_message(f"Acquisition démarrée - {acquisition_config['sample_rate']} Hz, {acquisition_config['n_channels']} canaux")
            
            # Émettre le signal
            self.acquisitionStarted.emit(acquisition_config)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de démarrer l'acquisition: {e}")
            self._log_message(f"Erreur: {e}")
            
    def _stop_acquisition(self):
        """Arrête l'acquisition"""
        if not self.is_acquiring or not self.acquisition_worker:
            return
            
        try:
            # Arrêter le worker
            self.acquisition_worker.stop_acquisition()
            
            # Arrêter le thread
            if self.worker_thread and self.worker_thread.isRunning():
                self.worker_thread.quit()
                self.worker_thread.wait(2000)  # Attendre 2 secondes max
                
            self.is_acquiring = False
            self._update_ui_state()
            
            # Masquer la barre de progression
            self.progress_bar.setVisible(False)
            
            self._log_message("Acquisition arrêtée manuellement")
            
        except Exception as e:
            self._log_message(f"Erreur arrêt: {e}")
            
    def _pause_acquisition(self):
        """Met en pause/reprend l'acquisition"""
        # TODO: Implémenter la pause
        self._log_message("Fonction pause à implémenter")
        
    def _clear_data(self):
        """Efface toutes les données"""
        self.plot_widget.clear_data()
        self.samples_label.setText("0")
        self.rate_label.setText("0.0 Hz")
        self.duration_label.setText("00:00")
        self.log_text.clear()
        self._log_message("Données effacées")
        
    def _export_data(self):
        """Exporte les données"""
        # TODO: Implémenter l'export
        self._log_message("Fonction export à implémenter")
        
    def _update_ui_state(self):
        """Met à jour l'état de l'interface"""
        # Boutons
        self.start_btn.setEnabled(not self.is_acquiring)
        self.stop_btn.setEnabled(self.is_acquiring)
        self.pause_btn.setEnabled(self.is_acquiring)
        
        # Champs de configuration
        self.duration_spin.setEnabled(not self.is_acquiring)
        self.sample_rate_spin.setEnabled(not self.is_acquiring)
        self.channels_spin.setEnabled(not self.is_acquiring)
        self.mode_combo.setEnabled(not self.is_acquiring)
        
        # Export
        self.export_btn.setEnabled(not self.is_acquiring and len(self.plot_widget.time_buffer) > 0)
        
    @pyqtSlot(list, float)
    def _update_stats(self, data: list, timestamp: float):
        """Met à jour les statistiques"""
        try:
            # Nombre d'échantillons
            sample_count = len(self.plot_widget.time_buffer)
            self.samples_label.setText(str(sample_count))
            
            # Taux d'échantillonnage réel
            if sample_count > 1:
                time_span = self.plot_widget.time_buffer[-1] - self.plot_widget.time_buffer[0]
                if time_span > 0:
                    real_rate = (sample_count - 1) / time_span
                    self.rate_label.setText(f"{real_rate:.1f} Hz")
                    
            # Durée
            if sample_count > 0 and self.acquisition_worker and self.acquisition_worker.start_time:
                elapsed = (datetime.now() - self.acquisition_worker.start_time).total_seconds()
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                self.duration_label.setText(f"{minutes:02d}:{seconds:02d}")
                
        except Exception as e:
            print(f"⚠️ Erreur mise à jour stats: {e}")
            
    @pyqtSlot(str)
    def _update_status(self, status: str):
        """Met à jour le statut"""
        self.status_label.setText(status)
        
        # Couleur selon le statut
        if "erreur" in status.lower():
            color = "#e74c3c"
        elif "en cours" in status.lower():
            color = "#3498db"
        elif "terminée" in status.lower():
            color = "#27ae60"
        else:
            color = "#f39c12"
            
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold; padding: 5px;")
        
    @pyqtSlot(dict)
    def _on_acquisition_finished(self, results: dict):
        """Gère la fin d'acquisition"""
        self.is_acquiring = False
        self._update_ui_state()
        
        # Masquer la barre de progression
        self.progress_bar.setVisible(False)
        
        # Log des résultats
        duration = results.get('duration', 0)
        samples = results.get('samples', 0)
        rate = results.get('sample_rate', 0)
        
        self._log_message(f"Acquisition terminée: {duration:.1f}s, {samples} échantillons, {rate:.1f} Hz")
        
        # Émettre le signal
        self.acquisitionFinished.emit(results)
        
    @pyqtSlot(str)
    def _on_error(self, error_msg: str):
        """Gère les erreurs d'acquisition"""
        self._log_message(f"ERREUR: {error_msg}")
        QMessageBox.critical(self, "Erreur d'acquisition", error_msg)
        
        if self.is_acquiring:
            self._stop_acquisition()
            
    def _log_message(self, message: str):
        """Ajoute un message au journal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # Faire défiler vers le bas
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def _on_theme_changed(self, theme_name: str):
        """Callback pour changement de thème"""
        # Mettre à jour les couleurs du graphique
        if hasattr(self.plot_widget, 'plot_widget') and self.plot_widget.plot_widget:
            colors = get_theme_colors(theme_name)
            # Appliquer les couleurs au graphique
            pass
            
    def get_acquisition_config(self) -> Dict[str, Any]:
        """Retourne la configuration d'acquisition"""
        return {
            'duration': self.duration_spin.value(),
            'sample_rate': self.sample_rate_spin.value(),
            'n_channels': self.channels_spin.value(),
            'mode': self.mode_combo.currentText(),
            'auto_save': self.auto_save_check.isChecked()
        }
        
    def is_valid(self) -> bool:
        """Vérifie si la configuration est valide"""
        if not self.validator:
            return True
        is_valid, _ = self.validator.validate_all()
        return is_valid
        
    def cleanup(self):
        """Nettoie les ressources"""
        if self.is_acquiring:
            self._stop_acquisition()
            
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()