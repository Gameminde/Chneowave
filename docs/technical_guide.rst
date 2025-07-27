Guide Technique CHNeoWave
==========================

Ce guide technique s'adresse aux développeurs, intégrateurs et administrateurs système travaillant avec CHNeoWave.

.. note::
   Pour l'utilisation standard du logiciel, consultez le :doc:`user_guide`.

Architecture Système
--------------------

Vue d'Ensemble
~~~~~~~~~~~~~

CHNeoWave suit une architecture MVC (Model-View-Controller) modulaire :

.. code-block:: text

   CHNeoWave/
   ├── src/hrneowave/
   │   ├── core/           # Noyau système
   │   ├── data/           # Gestion des données
   │   ├── analysis/       # Moteurs d'analyse
   │   ├── gui/            # Interface utilisateur
   │   └── utils/          # Utilitaires
   ├── tests/              # Tests automatisés
   ├── docs/               # Documentation
   ├── config/             # Configuration
   └── scripts/            # Scripts utilitaires

Composants Principaux
~~~~~~~~~~~~~~~~~~~~

**Core (Noyau)**

* **ErrorHandler** : Gestion centralisée des erreurs
* **PerformanceMonitor** : Monitoring des performances
* **ConfigManager** : Gestion de la configuration
* **ValidationEngine** : Validation des données

**Data (Données)**

* **AcquisitionManager** : Acquisition temps réel
* **DataProcessor** : Traitement des données
* **StorageManager** : Persistance HDF5
* **ExportEngine** : Export multi-formats

**Analysis (Analyse)**

* **SpectralAnalyzer** : Analyse fréquentielle
* **WaveAnalyzer** : Analyse de houle
* **StatisticalAnalyzer** : Analyse statistique
* **QualityAnalyzer** : Contrôle qualité

**GUI (Interface)**

* **MainController** : Contrôleur principal
* **ViewManager** : Gestion des vues
* **WorkflowManager** : Orchestration des workflows
* **ThemeManager** : Gestion des thèmes

Patterns de Conception
~~~~~~~~~~~~~~~~~~~~~

**Singleton**

.. code-block:: python

   class ConfigManager:
       """Gestionnaire de configuration (Singleton)."""
       _instance = None
       _initialized = False
       
       def __new__(cls):
           if cls._instance is None:
               cls._instance = super().__new__(cls)
           return cls._instance
       
       def __init__(self):
           if not self._initialized:
               self._config = {}
               self._initialized = True

**Observer**

.. code-block:: python

   class SignalBus(QObject):
       """Bus de signaux pour communication inter-composants."""
       
       # Signaux d'acquisition
       acquisition_started = Signal()
       acquisition_stopped = Signal()
       data_received = Signal(object)
       
       # Signaux d'analyse
       analysis_completed = Signal(str, object)
       analysis_failed = Signal(str, str)
       
       # Signaux d'interface
       view_changed = Signal(str)
       theme_changed = Signal(str)

**Factory**

.. code-block:: python

   class AnalyzerFactory:
       """Factory pour créer les analyseurs."""
       
       _analyzers = {
           'spectral': SpectralAnalyzer,
           'wave': WaveAnalyzer,
           'statistical': StatisticalAnalyzer,
           'quality': QualityAnalyzer
       }
       
       @classmethod
       def create_analyzer(cls, analyzer_type, **kwargs):
           if analyzer_type not in cls._analyzers:
               raise ValueError(f"Analyseur inconnu: {analyzer_type}")
           
           analyzer_class = cls._analyzers[analyzer_type]
           return analyzer_class(**kwargs)

**Strategy**

.. code-block:: python

   class DataProcessor:
       """Processeur de données avec stratégies configurables."""
       
       def __init__(self):
           self._strategies = {
               'filtering': None,
               'detrending': None,
               'windowing': None
           }
       
       def set_strategy(self, strategy_type, strategy):
           self._strategies[strategy_type] = strategy
       
       def process(self, data):
           for strategy in self._strategies.values():
               if strategy:
                   data = strategy.apply(data)
           return data

Gestion des Données
------------------

Format HDF5
~~~~~~~~~~

**Structure des fichiers :**

.. code-block:: text

   acquisition_001.h5
   ├── /metadata
   │   ├── acquisition_info
   │   ├── sensor_config
   │   └── processing_history
   ├── /raw_data
   │   ├── channel_1
   │   ├── channel_2
   │   └── timestamps
   ├── /processed_data
   │   ├── filtered
   │   ├── calibrated
   │   └── quality_flags
   └── /analysis_results
       ├── spectral
       ├── wave_statistics
       └── quality_metrics

**Implémentation :**

.. code-block:: python

   import h5py
   import numpy as np
   from datetime import datetime
   
   class HDF5Manager:
       """Gestionnaire de fichiers HDF5."""
       
       def __init__(self, filename, mode='r'):
           self.filename = filename
           self.mode = mode
           self._file = None
       
       def __enter__(self):
           self._file = h5py.File(self.filename, self.mode)
           return self
       
       def __exit__(self, exc_type, exc_val, exc_tb):
           if self._file:
               self._file.close()
       
       def save_acquisition_data(self, data, metadata):
           """Sauvegarde des données d'acquisition."""
           
           # Métadonnées
           meta_group = self._file.create_group('metadata')
           meta_group.attrs['acquisition_date'] = datetime.now().isoformat()
           meta_group.attrs['sampling_rate'] = metadata['sampling_rate']
           meta_group.attrs['duration'] = metadata['duration']
           meta_group.attrs['channels'] = metadata['channels']
           
           # Données brutes
           raw_group = self._file.create_group('raw_data')
           
           for i, channel_data in enumerate(data):
               dataset = raw_group.create_dataset(
                   f'channel_{i+1}',
                   data=channel_data,
                   compression='gzip',
                   compression_opts=9,
                   shuffle=True,
                   fletcher32=True
               )
               dataset.attrs['units'] = metadata.get('units', 'mm')
               dataset.attrs['calibration_factor'] = metadata.get('cal_factor', 1.0)
           
           # Timestamps
           timestamps = np.arange(len(data[0])) / metadata['sampling_rate']
           raw_group.create_dataset(
               'timestamps',
               data=timestamps,
               compression='gzip'
           )
       
       def load_acquisition_data(self):
           """Chargement des données d'acquisition."""
           
           # Métadonnées
           metadata = dict(self._file['metadata'].attrs)
           
           # Données
           raw_group = self._file['raw_data']
           channels = []
           
           for key in sorted(raw_group.keys()):
               if key.startswith('channel_'):
                   channels.append(raw_group[key][:])
           
           timestamps = raw_group['timestamps'][:]
           
           return {
               'data': np.array(channels),
               'timestamps': timestamps,
               'metadata': metadata
           }

Validation des Données
~~~~~~~~~~~~~~~~~~~~~

**Système de validation :**

.. code-block:: python

   from abc import ABC, abstractmethod
   from typing import List, Dict, Any
   
   class ValidationRule(ABC):
       """Règle de validation abstraite."""
       
       @abstractmethod
       def validate(self, data: np.ndarray) -> Dict[str, Any]:
           pass
   
   class RangeValidationRule(ValidationRule):
       """Validation de plage de valeurs."""
       
       def __init__(self, min_val: float, max_val: float):
           self.min_val = min_val
           self.max_val = max_val
       
       def validate(self, data: np.ndarray) -> Dict[str, Any]:
           out_of_range = (data < self.min_val) | (data > self.max_val)
           
           return {
               'is_valid': not np.any(out_of_range),
               'error_count': np.sum(out_of_range),
               'error_percentage': np.mean(out_of_range) * 100,
               'error_indices': np.where(out_of_range)[0].tolist()
           }
   
   class SpikeDetectionRule(ValidationRule):
       """Détection de pics aberrants."""
       
       def __init__(self, threshold: float = 3.0):
           self.threshold = threshold
       
       def validate(self, data: np.ndarray) -> Dict[str, Any]:
           # Détection par écart-type
           mean_val = np.mean(data)
           std_val = np.std(data)
           
           spikes = np.abs(data - mean_val) > (self.threshold * std_val)
           
           return {
               'is_valid': not np.any(spikes),
               'spike_count': np.sum(spikes),
               'spike_percentage': np.mean(spikes) * 100,
               'spike_indices': np.where(spikes)[0].tolist(),
               'threshold_used': self.threshold * std_val
           }
   
   class DataValidator:
       """Validateur de données principal."""
       
       def __init__(self):
           self.rules: List[ValidationRule] = []
       
       def add_rule(self, rule: ValidationRule):
           self.rules.append(rule)
       
       def validate(self, data: np.ndarray) -> Dict[str, Any]:
           results = {
               'overall_valid': True,
               'rule_results': {},
               'summary': {
                   'total_errors': 0,
                   'error_types': []
               }
           }
           
           for i, rule in enumerate(self.rules):
               rule_name = rule.__class__.__name__
               rule_result = rule.validate(data)
               
               results['rule_results'][rule_name] = rule_result
               
               if not rule_result['is_valid']:
                   results['overall_valid'] = False
                   results['summary']['total_errors'] += rule_result.get('error_count', 0)
                   results['summary']['error_types'].append(rule_name)
           
           return results

Acquisition Temps Réel
---------------------

Architecture Multi-Thread
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import threading
   import queue
   import serial
   from PySide6.QtCore import QThread, Signal
   
   class AcquisitionThread(QThread):
       """Thread d'acquisition de données."""
       
       data_received = Signal(np.ndarray)
       error_occurred = Signal(str)
       status_changed = Signal(str)
       
       def __init__(self, config):
           super().__init__()
           self.config = config
           self.running = False
           self.paused = False
           
           # Buffer circulaire
           self.buffer_size = config.get('buffer_size', 8192)
           self.data_buffer = queue.Queue(maxsize=self.buffer_size)
           
           # Connexion série
           self.serial_connection = None
       
       def run(self):
           """Boucle principale d'acquisition."""
           try:
               self._setup_serial_connection()
               self.running = True
               self.status_changed.emit("Acquisition démarrée")
               
               while self.running:
                   if not self.paused:
                       data_point = self._read_data_point()
                       if data_point is not None:
                           self._process_data_point(data_point)
                   else:
                       self.msleep(10)  # Pause courte
               
           except Exception as e:
               self.error_occurred.emit(f"Erreur d'acquisition: {str(e)}")
           finally:
               self._cleanup()
               self.status_changed.emit("Acquisition arrêtée")
       
       def _setup_serial_connection(self):
           """Configuration de la connexion série."""
           self.serial_connection = serial.Serial(
               port=self.config['port'],
               baudrate=self.config['baudrate'],
               bytesize=self.config.get('bytesize', 8),
               parity=self.config.get('parity', 'N'),
               stopbits=self.config.get('stopbits', 1),
               timeout=self.config.get('timeout', 1.0)
           )
       
       def _read_data_point(self):
           """Lecture d'un point de données."""
           try:
               if self.serial_connection.in_waiting > 0:
                   line = self.serial_connection.readline().decode('utf-8').strip()
                   return float(line)
           except (ValueError, UnicodeDecodeError) as e:
               # Log de l'erreur sans arrêter l'acquisition
               pass
           return None
       
       def _process_data_point(self, data_point):
           """Traitement d'un point de données."""
           try:
               # Ajout au buffer
               if not self.data_buffer.full():
                   self.data_buffer.put(data_point)
               else:
                   # Buffer plein, supprimer le plus ancien
                   self.data_buffer.get()
                   self.data_buffer.put(data_point)
               
               # Émission du signal si buffer suffisant
               if self.data_buffer.qsize() >= self.config.get('emit_threshold', 100):
                   buffer_data = []
                   temp_queue = queue.Queue()
                   
                   # Extraction des données
                   while not self.data_buffer.empty():
                       data = self.data_buffer.get()
                       buffer_data.append(data)
                       temp_queue.put(data)
                   
                   # Remise en buffer
                   self.data_buffer = temp_queue
                   
                   # Émission
                   self.data_received.emit(np.array(buffer_data))
               
           except Exception as e:
               self.error_occurred.emit(f"Erreur de traitement: {str(e)}")
       
       def stop_acquisition(self):
           """Arrêt de l'acquisition."""
           self.running = False
       
       def pause_acquisition(self):
           """Pause de l'acquisition."""
           self.paused = True
       
       def resume_acquisition(self):
           """Reprise de l'acquisition."""
           self.paused = False
       
       def _cleanup(self):
           """Nettoyage des ressources."""
           if self.serial_connection and self.serial_connection.is_open:
               self.serial_connection.close()

Gestion des Buffers
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from collections import deque
   import threading
   
   class CircularBuffer:
       """Buffer circulaire thread-safe."""
       
       def __init__(self, size: int):
           self.size = size
           self.buffer = deque(maxlen=size)
           self.lock = threading.RLock()
           self._full = False
       
       def append(self, data):
           """Ajout de données au buffer."""
           with self.lock:
               was_full = len(self.buffer) == self.size
               self.buffer.append(data)
               if was_full:
                   self._full = True
       
       def extend(self, data_array):
           """Ajout de plusieurs données."""
           with self.lock:
               for data in data_array:
                   self.append(data)
       
       def get_data(self, n_points=None):
           """Récupération des données."""
           with self.lock:
               if n_points is None:
                   return np.array(list(self.buffer))
               else:
                   return np.array(list(self.buffer)[-n_points:])
       
       def clear(self):
           """Vidage du buffer."""
           with self.lock:
               self.buffer.clear()
               self._full = False
       
       def is_full(self):
           """Vérification si le buffer est plein."""
           with self.lock:
               return self._full
       
       def __len__(self):
           with self.lock:
               return len(self.buffer)

Analyse en Temps Réel
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class RealTimeAnalyzer(QThread):
       """Analyseur temps réel."""
       
       analysis_ready = Signal(dict)
       
       def __init__(self, buffer, config):
           super().__init__()
           self.buffer = buffer
           self.config = config
           self.running = False
           
           # Paramètres d'analyse
           self.window_size = config.get('window_size', 1024)
           self.overlap = config.get('overlap', 0.5)
           self.update_rate = config.get('update_rate', 10)  # Hz
       
       def run(self):
           """Boucle d'analyse temps réel."""
           self.running = True
           
           while self.running:
               if len(self.buffer) >= self.window_size:
                   # Extraction des données
                   data = self.buffer.get_data(self.window_size)
                   
                   # Analyse rapide
                   analysis_result = self._quick_analysis(data)
                   
                   # Émission du résultat
                   self.analysis_ready.emit(analysis_result)
               
               # Attente selon le taux de mise à jour
               self.msleep(int(1000 / self.update_rate))
       
       def _quick_analysis(self, data):
           """Analyse rapide pour temps réel."""
           result = {
               'timestamp': time.time(),
               'statistics': {
                   'mean': np.mean(data),
                   'std': np.std(data),
                   'min': np.min(data),
                   'max': np.max(data),
                   'rms': np.sqrt(np.mean(data**2))
               }
           }
           
           # FFT rapide
           if len(data) >= 256:  # Minimum pour FFT
               fft_data = np.fft.fft(data)
               freqs = np.fft.fftfreq(len(data), 1/self.config['sampling_rate'])
               
               # Pic de fréquence
               magnitude = np.abs(fft_data)
               peak_idx = np.argmax(magnitude[1:len(magnitude)//2]) + 1
               peak_freq = freqs[peak_idx]
               
               result['spectral'] = {
                   'peak_frequency': peak_freq,
                   'peak_amplitude': magnitude[peak_idx],
                   'total_power': np.sum(magnitude**2)
               }
           
           return result
       
       def stop(self):
           """Arrêt de l'analyseur."""
           self.running = False

Interface Utilisateur
--------------------

Architecture MVC
~~~~~~~~~~~~~~~

**Contrôleur Principal :**

.. code-block:: python

   from PySide6.QtWidgets import QApplication
   from PySide6.QtCore import QObject, Signal
   
   class MainController(QObject):
       """Contrôleur principal de l'application."""
       
       def __init__(self):
           super().__init__()
           
           # Gestionnaires
           self.view_manager = ViewManager()
           self.workflow_manager = WorkflowManager()
           self.data_manager = DataManager()
           
           # Bus de signaux
           self.signal_bus = SignalBus()
           
           # Connexions
           self._setup_connections()
       
       def _setup_connections(self):
           """Configuration des connexions de signaux."""
           
           # Signaux d'acquisition
           self.signal_bus.acquisition_started.connect(
               self.view_manager.on_acquisition_started
           )
           self.signal_bus.data_received.connect(
               self.data_manager.on_data_received
           )
           
           # Signaux d'analyse
           self.signal_bus.analysis_completed.connect(
               self.view_manager.on_analysis_completed
           )
           
           # Signaux d'interface
           self.signal_bus.view_changed.connect(
               self.view_manager.change_view
           )
       
       def start_application(self):
           """Démarrage de l'application."""
           
           # Initialisation des composants
           self.view_manager.initialize()
           self.workflow_manager.initialize()
           self.data_manager.initialize()
           
           # Affichage de la vue principale
           self.view_manager.show_main_window()
       
       def shutdown_application(self):
           """Arrêt propre de l'application."""
           
           # Arrêt des acquisitions en cours
           self.workflow_manager.stop_all_workflows()
           
           # Sauvegarde des données
           self.data_manager.save_pending_data()
           
           # Nettoyage des ressources
           self.view_manager.cleanup()

**Gestionnaire de Vues :**

.. code-block:: python

   from PySide6.QtWidgets import QMainWindow, QStackedWidget
   
   class ViewManager(QObject):
       """Gestionnaire des vues de l'interface."""
       
       def __init__(self):
           super().__init__()
           
           self.main_window = None
           self.stacked_widget = None
           self.views = {}
           
           # Thème
           self.theme_manager = ThemeManager()
       
       def initialize(self):
           """Initialisation du gestionnaire de vues."""
           
           # Fenêtre principale
           self.main_window = MainWindow()
           self.stacked_widget = QStackedWidget()
           self.main_window.setCentralWidget(self.stacked_widget)
           
           # Création des vues
           self._create_views()
           
           # Application du thème
           self.theme_manager.apply_theme('default')
       
       def _create_views(self):
           """Création des vues de l'application."""
           
           # Vue d'accueil
           self.views['welcome'] = WelcomeView()
           self.stacked_widget.addWidget(self.views['welcome'])
           
           # Vue d'acquisition
           self.views['acquisition'] = AcquisitionView()
           self.stacked_widget.addWidget(self.views['acquisition'])
           
           # Vue d'analyse
           self.views['analysis'] = AnalysisViewV2()
           self.stacked_widget.addWidget(self.views['analysis'])
           
           # Vue d'export
           self.views['export'] = ExportView()
           self.stacked_widget.addWidget(self.views['export'])
       
       def change_view(self, view_name):
           """Changement de vue."""
           if view_name in self.views:
               view_widget = self.views[view_name]
               self.stacked_widget.setCurrentWidget(view_widget)
               
               # Notification à la vue
               if hasattr(view_widget, 'on_view_activated'):
                   view_widget.on_view_activated()
       
       def show_main_window(self):
           """Affichage de la fenêtre principale."""
           self.main_window.show()
           self.change_view('welcome')

Composants Material Design
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
   from PySide6.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty
   from PySide6.QtGui import QColor, QPainter, QPainterPath
   
   class MaterialButton(QPushButton):
       """Bouton Material Design."""
       
       def __init__(self, text="", parent=None):
           super().__init__(text, parent)
           
           # Propriétés Material
           self._elevation = 2
           self._ripple_color = QColor(255, 255, 255, 80)
           
           # Animation
           self._animation = QPropertyAnimation(self, b"elevation")
           self._animation.setDuration(150)
           self._animation.setEasingCurve(QEasingCurve.OutCubic)
           
           # Style de base
           self._setup_style()
           self._setup_shadow()
       
       def _setup_style(self):
           """Configuration du style de base."""
           self.setStyleSheet("""
               MaterialButton {
                   background-color: #2196F3;
                   color: white;
                   border: none;
                   border-radius: 4px;
                   padding: 8px 16px;
                   font-weight: 500;
                   text-transform: uppercase;
               }
               MaterialButton:hover {
                   background-color: #1976D2;
               }
               MaterialButton:pressed {
                   background-color: #0D47A1;
               }
           """)
       
       def _setup_shadow(self):
           """Configuration de l'ombre."""
           self.shadow_effect = QGraphicsDropShadowEffect()
           self.shadow_effect.setBlurRadius(self._elevation * 2)
           self.shadow_effect.setOffset(0, self._elevation)
           self.shadow_effect.setColor(QColor(0, 0, 0, 60))
           self.setGraphicsEffect(self.shadow_effect)
       
       @pyqtProperty(int)
       def elevation(self):
           return self._elevation
       
       @elevation.setter
       def elevation(self, value):
           self._elevation = value
           self._update_shadow()
       
       def _update_shadow(self):
           """Mise à jour de l'ombre selon l'élévation."""
           self.shadow_effect.setBlurRadius(self._elevation * 2)
           self.shadow_effect.setOffset(0, self._elevation)
       
       def enterEvent(self, event):
           """Animation d'entrée de souris."""
           self._animation.setStartValue(self._elevation)
           self._animation.setEndValue(self._elevation + 2)
           self._animation.start()
           super().enterEvent(event)
       
       def leaveEvent(self, event):
           """Animation de sortie de souris."""
           self._animation.setStartValue(self._elevation + 2)
           self._animation.setEndValue(self._elevation)
           self._animation.start()
           super().leaveEvent(event)

Gestion des Thèmes
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from pathlib import Path
   
   class ThemeManager:
       """Gestionnaire de thèmes."""
       
       def __init__(self):
           self.themes_dir = Path("config/themes")
           self.current_theme = None
           self.themes = {}
           
           # Chargement des thèmes
           self._load_themes()
       
       def _load_themes(self):
           """Chargement des thèmes disponibles."""
           
           # Thème par défaut
           self.themes['default'] = {
               'name': 'Défaut',
               'colors': {
                   'primary': '#2196F3',
                   'secondary': '#FFC107',
                   'background': '#FAFAFA',
                   'surface': '#FFFFFF',
                   'error': '#F44336',
                   'text_primary': '#212121',
                   'text_secondary': '#757575'
               },
               'fonts': {
                   'family': 'Segoe UI',
                   'size_small': 10,
                   'size_normal': 12,
                   'size_large': 14,
                   'size_title': 18
               }
           }
           
           # Thème sombre
           self.themes['dark'] = {
               'name': 'Sombre',
               'colors': {
                   'primary': '#BB86FC',
                   'secondary': '#03DAC6',
                   'background': '#121212',
                   'surface': '#1E1E1E',
                   'error': '#CF6679',
                   'text_primary': '#FFFFFF',
                   'text_secondary': '#AAAAAA'
               },
               'fonts': {
                   'family': 'Segoe UI',
                   'size_small': 10,
                   'size_normal': 12,
                   'size_large': 14,
                   'size_title': 18
               }
           }
           
           # Chargement des thèmes personnalisés
           if self.themes_dir.exists():
               for theme_file in self.themes_dir.glob('*.json'):
                   try:
                       with open(theme_file, 'r', encoding='utf-8') as f:
                           theme_data = json.load(f)
                           theme_name = theme_file.stem
                           self.themes[theme_name] = theme_data
                   except Exception as e:
                       print(f"Erreur chargement thème {theme_file}: {e}")
       
       def apply_theme(self, theme_name):
           """Application d'un thème."""
           if theme_name not in self.themes:
               theme_name = 'default'
           
           theme = self.themes[theme_name]
           self.current_theme = theme_name
           
           # Génération du stylesheet
           stylesheet = self._generate_stylesheet(theme)
           
           # Application à l'application
           app = QApplication.instance()
           if app:
               app.setStyleSheet(stylesheet)
       
       def _generate_stylesheet(self, theme):
           """Génération du stylesheet à partir du thème."""
           colors = theme['colors']
           fonts = theme['fonts']
           
           return f"""
           QMainWindow {{
               background-color: {colors['background']};
               color: {colors['text_primary']};
               font-family: {fonts['family']};
               font-size: {fonts['size_normal']}px;
           }}
           
           QWidget {{
               background-color: {colors['background']};
               color: {colors['text_primary']};
           }}
           
           QPushButton {{
               background-color: {colors['primary']};
               color: white;
               border: none;
               border-radius: 4px;
               padding: 8px 16px;
               font-weight: 500;
           }}
           
           QPushButton:hover {{
               background-color: {self._darken_color(colors['primary'])};
           }}
           
           QLineEdit {{
               background-color: {colors['surface']};
               border: 1px solid {colors['text_secondary']};
               border-radius: 4px;
               padding: 8px;
           }}
           
           QTextEdit {{
               background-color: {colors['surface']};
               border: 1px solid {colors['text_secondary']};
               border-radius: 4px;
           }}
           
           QLabel {{
               color: {colors['text_primary']};
           }}
           
           QMenuBar {{
               background-color: {colors['surface']};
               color: {colors['text_primary']};
           }}
           
           QMenuBar::item:selected {{
               background-color: {colors['primary']};
           }}
           
           QStatusBar {{
               background-color: {colors['surface']};
               color: {colors['text_secondary']};
           }}
           """
       
       def _darken_color(self, color_hex, factor=0.8):
           """Assombrissement d'une couleur."""
           color = QColor(color_hex)
           return color.darker(int(100/factor)).name()
       
       def get_available_themes(self):
           """Liste des thèmes disponibles."""
           return [(name, theme['name']) for name, theme in self.themes.items()]
       
       def save_custom_theme(self, theme_name, theme_data):
           """Sauvegarde d'un thème personnalisé."""
           self.themes_dir.mkdir(exist_ok=True)
           
           theme_file = self.themes_dir / f"{theme_name}.json"
           with open(theme_file, 'w', encoding='utf-8') as f:
               json.dump(theme_data, f, indent=2, ensure_ascii=False)
           
           self.themes[theme_name] = theme_data

Performance et Optimisation
--------------------------

Monitoring des Performances
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import psutil
   import time
   import threading
   from collections import deque
   
   class PerformanceMonitor:
       """Moniteur de performance système."""
       
       def __init__(self, history_size=1000):
           self.history_size = history_size
           self.metrics_history = {
               'cpu_percent': deque(maxlen=history_size),
               'memory_percent': deque(maxlen=history_size),
               'memory_mb': deque(maxlen=history_size),
               'disk_io_read': deque(maxlen=history_size),
               'disk_io_write': deque(maxlen=history_size),
               'timestamps': deque(maxlen=history_size)
           }
           
           self.monitoring = False
           self.monitor_thread = None
           self.update_interval = 1.0  # secondes
       
       def start_monitoring(self):
           """Démarrage du monitoring."""
           if not self.monitoring:
               self.monitoring = True
               self.monitor_thread = threading.Thread(target=self._monitor_loop)
               self.monitor_thread.daemon = True
               self.monitor_thread.start()
       
       def stop_monitoring(self):
           """Arrêt du monitoring."""
           self.monitoring = False
           if self.monitor_thread:
               self.monitor_thread.join()
       
       def _monitor_loop(self):
           """Boucle de monitoring."""
           process = psutil.Process()
           
           while self.monitoring:
               try:
                   # Métriques CPU
                   cpu_percent = psutil.cpu_percent()
                   
                   # Métriques mémoire
                   memory_info = process.memory_info()
                   memory_mb = memory_info.rss / 1024 / 1024
                   memory_percent = process.memory_percent()
                   
                   # Métriques disque
                   io_counters = process.io_counters()
                   
                   # Stockage
                   timestamp = time.time()
                   self.metrics_history['cpu_percent'].append(cpu_percent)
                   self.metrics_history['memory_percent'].append(memory_percent)
                   self.metrics_history['memory_mb'].append(memory_mb)
                   self.metrics_history['disk_io_read'].append(io_counters.read_bytes)
                   self.metrics_history['disk_io_write'].append(io_counters.write_bytes)
                   self.metrics_history['timestamps'].append(timestamp)
                   
               except Exception as e:
                   print(f"Erreur monitoring: {e}")
               
               time.sleep(self.update_interval)
       
       def get_current_metrics(self):
           """Métriques actuelles."""
           if not self.metrics_history['timestamps']:
               return None
           
           return {
               'cpu_percent': self.metrics_history['cpu_percent'][-1],
               'memory_percent': self.metrics_history['memory_percent'][-1],
               'memory_mb': self.metrics_history['memory_mb'][-1],
               'timestamp': self.metrics_history['timestamps'][-1]
           }
       
       def get_performance_report(self):
           """Rapport de performance."""
           if not self.metrics_history['timestamps']:
               return None
           
           cpu_data = list(self.metrics_history['cpu_percent'])
           memory_data = list(self.metrics_history['memory_mb'])
           
           return {
               'monitoring_duration': len(self.metrics_history['timestamps']) * self.update_interval,
               'cpu_stats': {
                   'mean': np.mean(cpu_data),
                   'max': np.max(cpu_data),
                   'min': np.min(cpu_data),
                   'std': np.std(cpu_data)
               },
               'memory_stats': {
                   'mean_mb': np.mean(memory_data),
                   'max_mb': np.max(memory_data),
                   'min_mb': np.min(memory_data),
                   'current_mb': memory_data[-1] if memory_data else 0
               },
               'recommendations': self._generate_recommendations(cpu_data, memory_data)
           }
       
       def _generate_recommendations(self, cpu_data, memory_data):
           """Génération de recommandations d'optimisation."""
           recommendations = []
           
           # Analyse CPU
           avg_cpu = np.mean(cpu_data)
           if avg_cpu > 80:
               recommendations.append("CPU élevé: Réduire la fréquence d'acquisition ou optimiser les calculs")
           elif avg_cpu > 60:
               recommendations.append("CPU modéré: Surveiller les pics d'utilisation")
           
           # Analyse mémoire
           max_memory = np.max(memory_data)
           if max_memory > 1000:  # > 1GB
               recommendations.append("Mémoire élevée: Optimiser les buffers ou réduire la taille des données")
           
           # Tendances
           if len(memory_data) > 10:
               recent_trend = np.polyfit(range(len(memory_data[-10:])), memory_data[-10:], 1)[0]
               if recent_trend > 1:  # Augmentation > 1MB par mesure
                   recommendations.append("Fuite mémoire potentielle détectée")
           
           return recommendations

Optimisation des Calculs
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from numba import jit, prange
   from concurrent.futures import ThreadPoolExecutor
   import multiprocessing as mp
   
   class OptimizedProcessor:
       """Processeur optimisé pour les calculs intensifs."""
       
       def __init__(self, use_numba=True, n_workers=None):
           self.use_numba = use_numba
           self.n_workers = n_workers or mp.cpu_count()
           self.executor = ThreadPoolExecutor(max_workers=self.n_workers)
       
       @staticmethod
       @jit(nopython=True, parallel=True)
       def _fast_fft_magnitude(data):
           """Calcul rapide de magnitude FFT avec Numba."""
           n = len(data)
           result = np.zeros(n//2)
           
           for i in prange(n//2):
               real_sum = 0.0
               imag_sum = 0.0
               
               for j in range(n):
                   angle = -2.0 * np.pi * i * j / n
                   cos_val = np.cos(angle)
                   sin_val = np.sin(angle)
                   
                   real_sum += data[j] * cos_val
                   imag_sum += data[j] * sin_val
               
               result[i] = np.sqrt(real_sum*real_sum + imag_sum*imag_sum)
           
           return result
       
       def compute_spectrum_batch(self, data_batch, window_size=1024, overlap=0.5):
           """Calcul de spectres par batch."""
           
           def process_single_spectrum(data):
               if self.use_numba:
                   return self._fast_fft_magnitude(data)
               else:
                   return np.abs(np.fft.fft(data)[:len(data)//2])
           
           # Division en chunks
           step = int(window_size * (1 - overlap))
           chunks = []
           
           for data in data_batch:
               for i in range(0, len(data) - window_size + 1, step):
                   chunk = data[i:i + window_size]
                   chunks.append(chunk)
           
           # Traitement parallèle
           futures = []
           for chunk in chunks:
               future = self.executor.submit(process_single_spectrum, chunk)
               futures.append(future)
           
           # Collecte des résultats
           results = []
           for future in futures:
               results.append(future.result())
           
           return np.array(results)
       
       @staticmethod
       @jit(nopython=True)
       def _fast_statistics(data):
           """Calcul rapide de statistiques avec Numba."""
           n = len(data)
           
           # Moyenne
           mean_val = np.sum(data) / n
           
           # Variance
           var_sum = 0.0
           for i in range(n):
               diff = data[i] - mean_val
               var_sum += diff * diff
           variance = var_sum / (n - 1)
           
           # Min/Max
           min_val = data[0]
           max_val = data[0]
           for i in range(1, n):
               if data[i] < min_val:
                   min_val = data[i]
               if data[i] > max_val:
                   max_val = data[i]
           
           return mean_val, np.sqrt(variance), min_val, max_val
       
       def compute_statistics_batch(self, data_batch):
           """Calcul de statistiques par batch."""
           
           futures = []
           for data in data_batch:
               future = self.executor.submit(self._fast_statistics, data)
               futures.append(future)
           
           results = []
           for future in futures:
               mean, std, min_val, max_val = future.result()
               results.append({
                   'mean': mean,
                   'std': std,
                   'min': min_val,
                   'max': max_val
               })
           
           return results
       
       def cleanup(self):
           """Nettoyage des ressources."""
           self.executor.shutdown(wait=True)

Gestion Mémoire
~~~~~~~~~~~~~~

.. code-block:: python

   import gc
   import weakref
   from contextlib import contextmanager
   
   class MemoryManager:
       """Gestionnaire de mémoire optimisé."""
       
       def __init__(self):
           self.tracked_objects = weakref.WeakSet()
           self.memory_pools = {}
       
       @contextmanager
       def memory_context(self, max_memory_mb=500):
           """Contexte de gestion mémoire."""
           initial_memory = self._get_memory_usage()
           
           try:
               yield
           finally:
               current_memory = self._get_memory_usage()
               memory_used = current_memory - initial_memory
               
               if memory_used > max_memory_mb:
                   self._force_cleanup()
       
       def _get_memory_usage(self):
           """Utilisation mémoire actuelle en MB."""
           import psutil
           process = psutil.Process()
           return process.memory_info().rss / 1024 / 1024
       
       def _force_cleanup(self):
           """Nettoyage forcé de la mémoire."""
           # Nettoyage des objets trackés
           for obj in list(self.tracked_objects):
               if hasattr(obj, 'cleanup'):
                   obj.cleanup()
           
           # Garbage collection agressif
           for _ in range(3):
               gc.collect()
       
       def track_object(self, obj):
           """Ajout d'un objet au tracking."""
           self.tracked_objects.add(obj)
       
       def create_array_pool(self, pool_name, shape, dtype=np.float64, pool_size=10):
           """Création d'un pool de tableaux réutilisables."""
           pool = []
           for _ in range(pool_size):
               array = np.zeros(shape, dtype=dtype)
               pool.append(array)
           
           self.memory_pools[pool_name] = {
               'pool': pool,
               'available': list(range(pool_size)),
               'in_use': set()
           }
       
       def get_array_from_pool(self, pool_name):
           """Récupération d'un tableau du pool."""
           if pool_name not in self.memory_pools:
               return None
           
           pool_info = self.memory_pools[pool_name]
           
           if pool_info['available']:
               index = pool_info['available'].pop()
               pool_info['in_use'].add(index)
               return pool_info['pool'][index]
           
           return None
       
       def return_array_to_pool(self, pool_name, array):
           """Retour d'un tableau au pool."""
           if pool_name not in self.memory_pools:
               return
           
           pool_info = self.memory_pools[pool_name]
           
           # Recherche de l'index du tableau
           for i, pool_array in enumerate(pool_info['pool']):
               if pool_array is array:
                   if i in pool_info['in_use']:
                       pool_info['in_use'].remove(i)
                       pool_info['available'].append(i)
                       # Remise à zéro du tableau
                       array.fill(0)
                   break

Tests et Validation
------------------

Architecture de Tests
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   tests/
   ├── unit/               # Tests unitaires
   │   ├── test_core/
   │   ├── test_data/
   │   ├── test_analysis/
   │   └── test_gui/
   ├── integration/        # Tests d'intégration
   │   ├── test_workflows/
   │   └── test_end_to_end/
   ├── performance/        # Tests de performance
   │   ├── test_benchmarks/
   │   └── test_memory/
   ├── fixtures/           # Données de test
   │   ├── sample_data/
   │   └── mock_configs/
   └── conftest.py         # Configuration pytest

Tests Unitaires
~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   import numpy as np
   from unittest.mock import Mock, patch
   from hrneowave.analysis.spectral import SpectralAnalyzer
   
   class TestSpectralAnalyzer:
       """Tests pour l'analyseur spectral."""
       
       @pytest.fixture
       def analyzer(self):
           """Fixture analyseur spectral."""
           return SpectralAnalyzer()
       
       @pytest.fixture
       def sample_data(self):
           """Fixture données d'exemple."""
           # Signal sinusoïdal + bruit
           t = np.linspace(0, 10, 1000)
           signal = np.sin(2 * np.pi * 5 * t) + 0.1 * np.random.randn(1000)
           return {
               'data': signal,
               'sampling_rate': 100.0,
               'timestamps': t
           }
       
       def test_fft_computation(self, analyzer, sample_data):
           """Test calcul FFT."""
           result = analyzer.compute_fft(
               sample_data['data'],
               sampling_rate=sample_data['sampling_rate']
           )
           
           # Vérifications
           assert 'frequencies' in result
           assert 'magnitude' in result
           assert 'phase' in result
           
           # Taille correcte
           expected_size = len(sample_data['data']) // 2
           assert len(result['frequencies']) == expected_size
           assert len(result['magnitude']) == expected_size
           
           # Pic à 5 Hz
           peak_idx = np.argmax(result['magnitude'])
           peak_freq = result['frequencies'][peak_idx]
           assert abs(peak_freq - 5.0) < 0.5  # Tolérance
       
       def test_psd_computation(self, analyzer, sample_data):
           """Test calcul PSD."""
           result = analyzer.compute_psd(
               sample_data['data'],
               sampling_rate=sample_data['sampling_rate'],
               window_size=256,
               overlap=0.5
           )
           
           assert 'frequencies' in result
           assert 'psd' in result
           assert 'confidence_interval' in result
           
           # Valeurs positives
           assert np.all(result['psd'] >= 0)
           
       def test_spectrogram_computation(self, analyzer, sample_data):
           """Test calcul spectrogramme."""
           result = analyzer.compute_spectrogram(
               sample_data['data'],
               sampling_rate=sample_data['sampling_rate'],
               window_size=128,
               overlap=0.75
           )
           
           assert 'time' in result
           assert 'frequencies' in result
           assert 'spectrogram' in result
           
           # Dimensions cohérentes
           n_time, n_freq = result['spectrogram'].shape
           assert len(result['time']) == n_time
           assert len(result['frequencies']) == n_freq
       
       def test_invalid_input_handling(self, analyzer):
           """Test gestion des entrées invalides."""
           
           # Données vides
           with pytest.raises(ValueError):
               analyzer.compute_fft(np.array([]), sampling_rate=100.0)
           
           # Fréquence d'échantillonnage invalide
           with pytest.raises(ValueError):
               analyzer.compute_fft(np.random.randn(100), sampling_rate=0)
           
           # Type de données invalide
           with pytest.raises(TypeError):
               analyzer.compute_fft("invalid_data", sampling_rate=100.0)
       
       @patch('hrneowave.analysis.spectral.np.fft.fft')
       def test_fft_error_handling(self, mock_fft, analyzer, sample_data):
           """Test gestion d'erreurs FFT."""
           
           # Simulation d'erreur FFT
           mock_fft.side_effect = RuntimeError("FFT failed")
           
           with pytest.raises(RuntimeError):
               analyzer.compute_fft(
                   sample_data['data'],
                   sampling_rate=sample_data['sampling_rate']
               )

Tests d'Intégration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   import tempfile
   import shutil
   from pathlib import Path
   from hrneowave.workflows.acquisition_workflow import AcquisitionWorkflow
   from hrneowave.data.acquisition import MockAcquisitionDevice
   
   class TestAcquisitionWorkflow:
       """Tests d'intégration pour le workflow d'acquisition."""
       
       @pytest.fixture
       def temp_project_dir(self):
           """Répertoire de projet temporaire."""
           temp_dir = tempfile.mkdtemp()
           yield Path(temp_dir)
           shutil.rmtree(temp_dir)
       
       @pytest.fixture
       def mock_device(self):
           """Dispositif d'acquisition simulé."""
           device = MockAcquisitionDevice()
           device.configure({
               'sampling_rate': 1000.0,
               'channels': ['channel_1'],
               'noise_level': 0.1
           })
           return device
       
       @pytest.fixture
       def workflow_config(self, temp_project_dir):
           """Configuration du workflow."""
           return {
               'project_dir': temp_project_dir,
               'acquisition': {
                   'duration': 5.0,  # 5 secondes
                   'sampling_rate': 1000.0,
                   'buffer_size': 1024
               },
               'processing': {
                   'enable_filtering': True,
                   'lowpass_cutoff': 100.0
               },
               'storage': {
                   'format': 'hdf5',
                   'compression': True
               }
           }
       
       def test_complete_acquisition_workflow(self, mock_device, workflow_config):
           """Test workflow complet d'acquisition."""
           
           workflow = AcquisitionWorkflow(workflow_config)
           workflow.set_acquisition_device(mock_device)
           
           # Démarrage du workflow
           workflow.start()
           
           # Attente de la fin
           workflow.wait_for_completion(timeout=10.0)
           
           # Vérifications
           assert workflow.is_completed()
           assert not workflow.has_errors()
           
           # Vérification des fichiers générés
           project_dir = Path(workflow_config['project_dir'])
           data_files = list(project_dir.glob('data/raw/*.h5'))
           assert len(data_files) > 0
           
           # Vérification du contenu
           data_file = data_files[0]
           with h5py.File(data_file, 'r') as f:
               assert 'raw_data' in f
               assert 'metadata' in f
               
               # Données cohérentes
               channel_data = f['raw_data/channel_1'][:]
               expected_samples = int(workflow_config['acquisition']['duration'] * 
                                   workflow_config['acquisition']['sampling_rate'])
               
               assert len(channel_data) == expected_samples
       
       def test_workflow_error_recovery(self, mock_device, workflow_config):
           """Test récupération d'erreurs."""
           
           # Configuration d'erreur sur le device
           mock_device.set_error_mode(True, error_after=1000)
           
           workflow = AcquisitionWorkflow(workflow_config)
           workflow.set_acquisition_device(mock_device)
           
           # Démarrage avec erreur attendue
           workflow.start()
           workflow.wait_for_completion(timeout=10.0)
           
           # Vérifications
           assert workflow.has_errors()
           
           # Vérification que les données partielles sont sauvées
           project_dir = Path(workflow_config['project_dir'])
           data_files = list(project_dir.glob('data/raw/*.h5'))
           
           if data_files:  # Des données partielles peuvent être sauvées
               data_file = data_files[0]
               with h5py.File(data_file, 'r') as f:
                   channel_data = f['raw_data/channel_1'][:]
                   assert len(channel_data) > 0

Tests de Performance
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   import time
   import numpy as np
   from memory_profiler import profile
   from hrneowave.analysis.spectral import SpectralAnalyzer
   
   class TestPerformance:
       """Tests de performance."""
       
       @pytest.fixture
       def large_dataset(self):
           """Jeu de données volumineux."""
           # 1 million de points
           return np.random.randn(1000000)
       
       def test_fft_performance(self, large_dataset):
           """Test performance FFT."""
           analyzer = SpectralAnalyzer()
           
           start_time = time.time()
           result = analyzer.compute_fft(large_dataset, sampling_rate=1000.0)
           end_time = time.time()
           
           execution_time = end_time - start_time
           
           # Assertion sur le temps d'exécution (< 5 secondes)
           assert execution_time < 5.0
           
           # Vérification du résultat
           assert len(result['magnitude']) == len(large_dataset) // 2
       
       @profile
       def test_memory_usage(self, large_dataset):
           """Test utilisation mémoire."""
           analyzer = SpectralAnalyzer()
           
           # Traitement par chunks pour économiser la mémoire
           chunk_size = 10000
           results = []
           
           for i in range(0, len(large_dataset), chunk_size):
               chunk = large_dataset[i:i+chunk_size]
               result = analyzer.compute_fft(chunk, sampling_rate=1000.0)
               results.append(result['magnitude'])
           
           # Vérification que tous les chunks ont été traités
           expected_chunks = len(large_dataset) // chunk_size
           assert len(results) == expected_chunks

Configuration et Déploiement
---------------------------

Configuration Système
~~~~~~~~~~~~~~~~~~~~

**Fichier de configuration principal (config/app_config.yaml) :**

.. code-block:: yaml

   # Configuration CHNeoWave
   application:
     name: "CHNeoWave"
     version: "1.0.0"
     debug: false
     log_level: "INFO"
   
   # Interface utilisateur
   gui:
     theme: "default"
     language: "fr"
     window:
       width: 1200
       height: 800
       maximized: false
     
     # Mise à jour de l'interface
     update_rates:
       real_time_display: 30  # Hz
       status_bar: 2          # Hz
       progress_bar: 10       # Hz
   
   # Acquisition de données
   acquisition:
     default_sampling_rate: 1000.0  # Hz
     buffer_size: 8192
     max_channels: 8
     
     # Communication série
     serial:
       timeout: 1.0
       baudrate: 115200
       bytesize: 8
       parity: "N"
       stopbits: 1
     
     # Validation des données
     validation:
       enable_range_check: true
       min_value: -1000.0
       max_value: 1000.0
       enable_spike_detection: true
       spike_threshold: 3.0
   
   # Traitement des données
   processing:
     # Filtrage
     filtering:
       enable_lowpass: true
       lowpass_cutoff: 100.0
       enable_highpass: false
       highpass_cutoff: 0.1
       filter_order: 4
     
     # Fenêtrage
     windowing:
       default_window: "hann"
       window_size: 1024
       overlap: 0.5
   
   # Analyse
   analysis:
     spectral:
       fft_size: 1024
       zero_padding: true
       detrend: "linear"
     
     wave:
       enable_goda_analysis: true
       enable_directional_analysis: false
       significant_wave_height_method: "zero_crossing"
     
     statistics:
       confidence_level: 0.95
       enable_outlier_detection: true
   
   # Stockage
   storage:
     format: "hdf5"
     compression: true
     compression_level: 6
     
     # Répertoires
     directories:
       projects: "./projects"
       data: "./data"
       exports: "./exports"
       logs: "./logs"
       temp: "./temp"
     
     # Rétention des données
     retention:
       raw_data_days: 30
       processed_data_days: 90
       log_files_days: 7
   
   # Performance
   performance:
     enable_monitoring: true
     max_memory_mb: 2048
     enable_multiprocessing: true
     max_workers: 4
     
     # Optimisations
     optimizations:
       use_numba: true
       enable_caching: true
       cache_size_mb: 256
   
   # Sécurité
   security:
     enable_data_validation: true
     enable_input_sanitization: true
     max_file_size_mb: 1024
   
   # Export
   export:
     default_format: "csv"
     include_metadata: true
     
     formats:
       csv:
         delimiter: ","
         encoding: "utf-8"
       
       excel:
         engine: "openpyxl"
         include_charts: true
       
       matlab:
         version: "7.3"
         compression: true

**Configuration des capteurs (config/sensors.yaml) :**

.. code-block:: yaml

   # Configuration des capteurs
   sensors:
     # Capteur de houle résistif
     wave_gauge_resistive:
       type: "resistive_wave_gauge"
       description: "Capteur de houle résistif"
       
       # Paramètres physiques
       physical:
         sensitivity: 1.0      # mm/V
         range_min: -500.0     # mm
         range_max: 500.0      # mm
         accuracy: 0.1         # mm
         resolution: 0.01      # mm
       
       # Calibration
       calibration:
         offset: 0.0
         gain: 1.0
         polynomial_coeffs: [0.0, 1.0]  # Correction polynomiale
       
       # Communication
       communication:
         protocol: "serial"
         port: "COM1"
         baudrate: 115200
         data_format: "ascii"
         terminator: "\r\n"
     
     # Capteur de houle capacitif
     wave_gauge_capacitive:
       type: "capacitive_wave_gauge"
       description: "Capteur de houle capacitif"
       
       physical:
         sensitivity: 2.0
         range_min: -300.0
         range_max: 300.0
         accuracy: 0.05
         resolution: 0.005
       
       calibration:
         offset: 0.0
         gain: 1.0
         temperature_compensation: true
         temp_coeff: -0.001    # %/°C
       
       communication:
         protocol: "serial"
         port: "COM2"
         baudrate: 9600
         data_format: "binary"
   
   # Configurations prédéfinies
   configurations:
     # Configuration bassin simple
     single_basin:
       name: "Bassin simple"
       description: "Configuration pour bassin d'essai simple"
       sensors:
         - sensor_id: "WG01"
           type: "wave_gauge_resistive"
           position: {x: 0.0, y: 0.0, z: 0.0}
           active: true
       
       sampling:
         rate: 1000.0
         duration: 300.0  # 5 minutes
     
     # Configuration canal à houle
     wave_channel:
       name: "Canal à houle"
       description: "Configuration pour canal à houle 2D"
       sensors:
         - sensor_id: "WG01"
           type: "wave_gauge_resistive"
           position: {x: 0.0, y: 0.0, z: 0.0}
           active: true
         
         - sensor_id: "WG02"
           type: "wave_gauge_resistive"
           position: {x: 1.0, y: 0.0, z: 0.0}
           active: true
         
         - sensor_id: "WG03"
           type: "wave_gauge_capacitive"
           position: {x: 2.0, y: 0.0, z: 0.0}
           active: true
       
       sampling:
         rate: 2000.0
         duration: 600.0  # 10 minutes
     
     # Configuration bassin 3D
     basin_3d:
       name: "Bassin 3D"
       description: "Configuration pour bassin d'essai 3D"
       sensors:
         - sensor_id: "WG01"
           type: "wave_gauge_resistive"
           position: {x: -1.0, y: -1.0, z: 0.0}
           active: true
         
         - sensor_id: "WG02"
           type: "wave_gauge_resistive"
           position: {x: 1.0, y: -1.0, z: 0.0}
           active: true
         
         - sensor_id: "WG03"
           type: "wave_gauge_resistive"
           position: {x: -1.0, y: 1.0, z: 0.0}
           active: true
         
         - sensor_id: "WG04"
           type: "wave_gauge_resistive"
           position: {x: 1.0, y: 1.0, z: 0.0}
           active: true
       
       sampling:
         rate: 1000.0
         duration: 1200.0  # 20 minutes

Script de Déploiement
~~~~~~~~~~~~~~~~~~~~

**Script de construction (scripts/build_release.py) :**

.. code-block:: python

   #!/usr/bin/env python3
   """
   Script de construction de release CHNeoWave.
   """
   
   import os
   import sys
   import shutil
   import subprocess
   import zipfile
   from pathlib import Path
   import argparse
   
   class ReleaseBuilder:
       """Constructeur de release."""
       
       def __init__(self, version, target_platform="windows"):
           self.version = version
           self.target_platform = target_platform
           self.project_root = Path(__file__).parent.parent
           self.build_dir = self.project_root / "build"
           self.dist_dir = self.project_root / "dist"
           
       def clean_build_dirs(self):
           """Nettoyage des répertoires de build."""
           print("Nettoyage des répertoires de build...")
           
           for dir_path in [self.build_dir, self.dist_dir]:
               if dir_path.exists():
                   shutil.rmtree(dir_path)
               dir_path.mkdir(exist_ok=True)
       
       def run_tests(self):
           """Exécution des tests."""
           print("Exécution des tests...")
           
           result = subprocess.run([
               sys.executable, "-m", "pytest", 
               "tests/", 
               "-v", 
               "--cov=src/hrneowave",
               "--cov-report=html",
               "--cov-report=term"
           ], cwd=self.project_root)
           
           if result.returncode != 0:
               raise RuntimeError("Les tests ont échoué")
       
       def build_documentation(self):
           """Construction de la documentation."""
           print("Construction de la documentation...")
           
           docs_dir = self.project_root / "docs"
           build_docs_dir = docs_dir / "_build"
           
           # Nettoyage
           if build_docs_dir.exists():
               shutil.rmtree(build_docs_dir)
           
           # Construction Sphinx
           result = subprocess.run([
               "sphinx-build",
               "-b", "html",
               str(docs_dir),
               str(build_docs_dir / "html")
           ])
           
           if result.returncode != 0:
               raise RuntimeError("Construction de la documentation échouée")
       
       def build_executable(self):
           """Construction de l'exécutable."""
           print("Construction de l'exécutable...")
           
           # Utilisation du script make_dist.py existant
           make_dist_script = self.project_root / "scripts" / "make_dist.py"
           
           result = subprocess.run([
               sys.executable, str(make_dist_script)
           ], cwd=self.project_root)
           
           if result.returncode != 0:
               raise RuntimeError("Construction de l'exécutable échouée")
       
       def create_installer_package(self):
           """Création du package d'installation."""
           print("Création du package d'installation...")
           
           package_name = f"CHNeoWave-{self.version}-{self.target_platform}"
           package_dir = self.dist_dir / package_name
           package_dir.mkdir(exist_ok=True)
           
           # Copie de l'exécutable
           exe_file = self.dist_dir / "CHNeoWave.exe"
           if exe_file.exists():
               shutil.copy2(exe_file, package_dir)
           
           # Copie des fichiers de configuration
           config_dir = package_dir / "config"
           shutil.copytree(
               self.project_root / "config",
               config_dir,
               ignore=shutil.ignore_patterns("*.pyc", "__pycache__")
           )
           
           # Copie de la documentation
           docs_build_dir = self.project_root / "docs" / "_build" / "html"
           if docs_build_dir.exists():
               docs_package_dir = package_dir / "documentation"
               shutil.copytree(docs_build_dir, docs_package_dir)
           
           # Fichiers README et LICENSE
           for file_name in ["README.md", "LICENSE", "CHANGELOG.md"]:
               src_file = self.project_root / file_name
               if src_file.exists():
                   shutil.copy2(src_file, package_dir)
           
           # Script d'installation
           self._create_install_script(package_dir)
           
           # Création de l'archive ZIP
           zip_file = self.dist_dir / f"{package_name}.zip"
           with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
               for file_path in package_dir.rglob('*'):
                   if file_path.is_file():
                       arc_name = file_path.relative_to(package_dir)
                       zf.write(file_path, arc_name)
           
           print(f"Package créé: {zip_file}")
           return zip_file
       
       def _create_install_script(self, package_dir):
           """Création du script d'installation."""
           install_script = package_dir / "install.bat"
           
           script_content = f"""
@echo off
echo Installation de CHNeoWave v{self.version}
echo.

REM Création du répertoire d'installation
set INSTALL_DIR=%PROGRAMFILES%\CHNeoWave
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copie des fichiers
echo Copie des fichiers...
copy CHNeoWave.exe "%INSTALL_DIR%\"
xcopy config "%INSTALL_DIR%\config\" /E /I /Y
xcopy documentation "%INSTALL_DIR%\documentation\" /E /I /Y

REM Création du raccourci sur le bureau
echo Création du raccourci...
set DESKTOP=%USERPROFILE%\Desktop
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\CHNeoWave.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\CHNeoWave.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "CHNeoWave - Logiciel d'analyse de houle" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo Installation terminée!
echo CHNeoWave est installé dans: %INSTALL_DIR%
echo Un raccourci a été créé sur le bureau.
echo.
pause
"""
           
           with open(install_script, 'w', encoding='utf-8') as f:
               f.write(script_content)
       
       def build_release(self):
           """Construction complète de la release."""
           print(f"Construction de CHNeoWave v{self.version}")
           print("=" * 50)
           
           try:
               # Étapes de construction
               self.clean_build_dirs()
               self.run_tests()
               self.build_documentation()
               self.build_executable()
               package_file = self.create_installer_package()
               
               print("\n" + "=" * 50)
               print("Construction terminée avec succès!")
               print(f"Package: {package_file}")
               
               return package_file
               
           except Exception as e:
               print(f"\nErreur lors de la construction: {e}")
               sys.exit(1)
   
   def main():
       parser = argparse.ArgumentParser(description="Construction de release CHNeoWave")
       parser.add_argument("version", help="Version de la release (ex: 1.0.0)")
       parser.add_argument("--platform", default="windows", 
                          choices=["windows", "linux", "macos"],
                          help="Plateforme cible")
       
       args = parser.parse_args()
       
       builder = ReleaseBuilder(args.version, args.platform)
       builder.build_release()
   
   if __name__ == "__main__":
       main()

Dépannage et Maintenance
-----------------------

Problèmes Courants
~~~~~~~~~~~~~~~~~

**Problème : Erreur de connexion série**

*Symptômes :*
- Message "Impossible de se connecter au port série"
- Acquisition qui ne démarre pas

*Solutions :*

1. Vérifier que le port série est correct :

.. code-block:: python

   import serial.tools.list_ports
   
   # Lister les ports disponibles
   ports = serial.tools.list_ports.comports()
   for port in ports:
       print(f"Port: {port.device}, Description: {port.description}")

2. Vérifier les paramètres de communication :

.. code-block:: yaml

   # Dans config/sensors.yaml
   communication:
     port: "COM1"        # Vérifier le bon port
     baudrate: 115200    # Vérifier la vitesse
     timeout: 2.0        # Augmenter si nécessaire

3. Tester la connexion manuellement :

.. code-block:: python

   import serial
   
   try:
       ser = serial.Serial('COM1', 115200, timeout=1)
       print("Connexion réussie")
       
       # Test de lecture
       data = ser.readline()
       print(f"Données reçues: {data}")
       
       ser.close()
   except Exception as e:
       print(f"Erreur: {e}")

**Problème : Performance dégradée**

*Symptômes :*
- Interface qui rame
- Acquisition qui saute des échantillons
- Utilisation mémoire élevée

*Solutions :*

1. Réduire la fréquence d'affichage :

.. code-block:: yaml

   # Dans config/app_config.yaml
   gui:
     update_rates:
       real_time_display: 10  # Réduire de 30 à 10 Hz

2. Optimiser les buffers :

.. code-block:: yaml

   acquisition:
     buffer_size: 4096     # Réduire si nécessaire

3. Activer les optimisations :

.. code-block:: yaml

   performance:
     optimizations:
       use_numba: true
       enable_caching: true

**Problème : Fichiers corrompus**

*Symptômes :*
- Erreur lors de l'ouverture de fichiers HDF5
- Données manquantes

*Solutions :*

1. Vérification d'intégrité :

.. code-block:: python

   import h5py
   
   def check_hdf5_integrity(filename):
       try:
           with h5py.File(filename, 'r') as f:
               # Vérification des groupes principaux
               required_groups = ['metadata', 'raw_data']
               for group in required_groups:
                   if group not in f:
                       print(f"Groupe manquant: {group}")
                       return False
               
               # Vérification des données
               for key in f['raw_data'].keys():
                   data = f['raw_data'][key]
                   if len(data) == 0:
                       print(f"Données vides: {key}")
                       return False
               
               print("Fichier intègre")
               return True
               
       except Exception as e:
           print(f"Fichier corrompu: {e}")
           return False

2. Récupération de données :

.. code-block:: python

   def recover_partial_data(corrupted_file, output_file):
       """Récupération de données partielles."""
       try:
           with h5py.File(corrupted_file, 'r') as f_in:
               with h5py.File(output_file, 'w') as f_out:
                   
                   # Copie des métadonnées si disponibles
                   if 'metadata' in f_in:
                       f_in.copy('metadata', f_out)
                   
                   # Copie des données récupérables
                   if 'raw_data' in f_in:
                       raw_group = f_out.create_group('raw_data')
                       
                       for key in f_in['raw_data'].keys():
                           try:
                               data = f_in['raw_data'][key][:]
                               raw_group.create_dataset(key, data=data)
                               print(f"Récupéré: {key} ({len(data)} points)")
                           except Exception as e:
                               print(f"Impossible de récupérer {key}: {e}")
                   
                   print(f"Données récupérées dans: {output_file}")
                   
       except Exception as e:
           print(f"Échec de récupération: {e}")

Logs et Diagnostic
~~~~~~~~~~~~~~~~~

**Configuration des logs :**

.. code-block:: python

   import logging
   import logging.handlers
   from pathlib import Path
   
   def setup_logging(log_level="INFO", log_dir="logs"):
       """Configuration du système de logs."""
       
       # Création du répertoire de logs
       log_path = Path(log_dir)
       log_path.mkdir(exist_ok=True)
       
       # Configuration du logger principal
       logger = logging.getLogger('chneowave')
       logger.setLevel(getattr(logging, log_level.upper()))
       
       # Formatter
       formatter = logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
       )
       
       # Handler pour fichier avec rotation
       file_handler = logging.handlers.RotatingFileHandler(
           log_path / 'chneowave.log',
           maxBytes=10*1024*1024,  # 10MB
           backupCount=5
       )
       file_handler.setFormatter(formatter)
       logger.addHandler(file_handler)
       
       # Handler pour console
       console_handler = logging.StreamHandler()
       console_handler.setFormatter(formatter)
       logger.addHandler(console_handler)
       
       # Loggers spécialisés
       
       # Logger acquisition
       acq_logger = logging.getLogger('chneowave.acquisition')
       acq_handler = logging.handlers.RotatingFileHandler(
           log_path / 'acquisition.log',
           maxBytes=5*1024*1024,
           backupCount=3
       )
       acq_handler.setFormatter(formatter)
       acq_logger.addHandler(acq_handler)
       
       # Logger analyse
       analysis_logger = logging.getLogger('chneowave.analysis')
       analysis_handler = logging.handlers.RotatingFileHandler(
           log_path / 'analysis.log',
           maxBytes=5*1024*1024,
           backupCount=3
       )
       analysis_handler.setFormatter(formatter)
       analysis_logger.addHandler(analysis_handler)
       
       # Logger erreurs
       error_logger = logging.getLogger('chneowave.errors')
       error_handler = logging.handlers.RotatingFileHandler(
           log_path / 'errors.log',
           maxBytes=5*1024*1024,
           backupCount=10
       )
       error_handler.setFormatter(formatter)
       error_handler.setLevel(logging.ERROR)
       error_logger.addHandler(error_handler)
       
       return logger

**Diagnostic automatique :**

.. code-block:: python

   import psutil
   import platform
   import sys
   from pathlib import Path
   
   def generate_diagnostic_report():
       """Génération d'un rapport de diagnostic."""
       
       report = {
           'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
           'system': {},
           'application': {},
           'performance': {},
           'configuration': {},
           'errors': []
       }
       
       try:
           # Informations système
           report['system'] = {
               'platform': platform.platform(),
               'python_version': sys.version,
               'cpu_count': psutil.cpu_count(),
               'memory_total_gb': psutil.virtual_memory().total / (1024**3),
               'disk_free_gb': psutil.disk_usage('.').free / (1024**3)
           }
           
           # Informations application
           from hrneowave import __version__
           report['application'] = {
               'version': __version__,
               'install_path': str(Path(__file__).parent),
               'config_files': {
                   'app_config': Path('config/app_config.yaml').exists(),
                   'sensors_config': Path('config/sensors.yaml').exists()
               }
           }
           
           # Performance actuelle
           process = psutil.Process()
           report['performance'] = {
               'cpu_percent': psutil.cpu_percent(interval=1),
               'memory_mb': process.memory_info().rss / (1024**2),
               'memory_percent': process.memory_percent(),
               'open_files': len(process.open_files()),
               'threads': process.num_threads()
           }
           
           # Vérification de la configuration
           config_issues = []
           
           # Vérification des ports série
           import serial.tools.list_ports
           available_ports = [port.device for port in serial.tools.list_ports.comports()]
           if not available_ports:
               config_issues.append("Aucun port série disponible")
           
           report['configuration'] = {
               'available_serial_ports': available_ports,
               'issues': config_issues
           }
           
           # Analyse des logs d'erreur récents
           error_log = Path('logs/errors.log')
           if error_log.exists():
               with open(error_log, 'r', encoding='utf-8') as f:
                   lines = f.readlines()
                   recent_errors = lines[-50:]  # 50 dernières lignes
                   report['errors'] = recent_errors
           
       except Exception as e:
           report['errors'].append(f"Erreur génération rapport: {str(e)}")
       
       return report
   
   def save_diagnostic_report(report, filename=None):
       """Sauvegarde du rapport de diagnostic."""
       if filename is None:
           timestamp = time.strftime('%Y%m%d_%H%M%S')
           filename = f"diagnostic_report_{timestamp}.json"
       
       with open(filename, 'w', encoding='utf-8') as f:
           json.dump(report, f, indent=2, ensure_ascii=False)
       
       print(f"Rapport de diagnostic sauvegardé: {filename}")
       return filename

Mise à Jour et Migration
~~~~~~~~~~~~~~~~~~~~~~~

**Script de mise à jour :**

.. code-block:: python

   import json
   import shutil
   from pathlib import Path
   from packaging import version
   
   class UpdateManager:
       """Gestionnaire de mises à jour."""
       
       def __init__(self, current_version):
           self.current_version = current_version
           self.backup_dir = Path("backups")
           self.backup_dir.mkdir(exist_ok=True)
       
       def check_for_updates(self, update_server_url):
           """Vérification des mises à jour disponibles."""
           try:
               import requests
               
               response = requests.get(f"{update_server_url}/latest_version")
               latest_info = response.json()
               
               latest_version = latest_info['version']
               
               if version.parse(latest_version) > version.parse(self.current_version):
                   return {
                       'update_available': True,
                       'latest_version': latest_version,
                       'download_url': latest_info['download_url'],
                       'changelog': latest_info.get('changelog', ''),
                       'critical': latest_info.get('critical', False)
                   }
               else:
                   return {'update_available': False}
                   
           except Exception as e:
               print(f"Erreur vérification mise à jour: {e}")
               return {'error': str(e)}
       
       def backup_current_installation(self):
           """Sauvegarde de l'installation actuelle."""
           timestamp = time.strftime('%Y%m%d_%H%M%S')
           backup_name = f"backup_v{self.current_version}_{timestamp}"
           backup_path = self.backup_dir / backup_name
           
           # Sauvegarde des fichiers critiques
           critical_paths = [
               'config/',
               'projects/',
               'data/',
               'src/hrneowave/'
           ]
           
           backup_path.mkdir(exist_ok=True)
           
           for path_str in critical_paths:
               src_path = Path(path_str)
               if src_path.exists():
                   if src_path.is_dir():
                       shutil.copytree(
                           src_path, 
                           backup_path / src_path.name,
                           ignore=shutil.ignore_patterns('*.pyc', '__pycache__')
                       )
                   else:
                       shutil.copy2(src_path, backup_path)
           
           # Métadonnées de sauvegarde
           backup_info = {
               'version': self.current_version,
               'timestamp': timestamp,
               'paths_backed_up': critical_paths
           }
           
           with open(backup_path / 'backup_info.json', 'w') as f:
               json.dump(backup_info, f, indent=2)
           
           print(f"Sauvegarde créée: {backup_path}")
           return backup_path
       
       def migrate_configuration(self, old_version, new_version):
           """Migration de configuration entre versions."""
           
           migration_rules = {
               '0.3.0': {
                   'to': '1.0.0',
                   'config_changes': {
                       'gui.theme': 'default',  # Nouvelle valeur par défaut
                       'performance.enable_monitoring': True,
                       'security.enable_data_validation': True
                   },
                   'removed_keys': [
                       'deprecated_setting'
                   ]
               }
           }
           
           if old_version in migration_rules:
               rules = migration_rules[old_version]
               
               if version.parse(new_version) >= version.parse(rules['to']):
                   self._apply_migration_rules(rules)
       
       def _apply_migration_rules(self, rules):
           """Application des règles de migration."""
           config_file = Path('config/app_config.yaml')
           
           if config_file.exists():
               import yaml
               
               # Chargement de la configuration
               with open(config_file, 'r', encoding='utf-8') as f:
                   config = yaml.safe_load(f)
               
               # Application des changements
               for key, value in rules.get('config_changes', {}).items():
                   self._set_nested_key(config, key, value)
               
               # Suppression des clés obsolètes
               for key in rules.get('removed_keys', []):
                   self._remove_nested_key(config, key)
               
               # Sauvegarde
               with open(config_file, 'w', encoding='utf-8') as f:
                   yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
               
               print("Configuration migrée avec succès")
       
       def _set_nested_key(self, config, key_path, value):
           """Définition d'une clé imbriquée."""
           keys = key_path.split('.')
           current = config
           
           for key in keys[:-1]:
               if key not in current:
                   current[key] = {}
               current = current[key]
           
           current[keys[-1]] = value
       
       def _remove_nested_key(self, config, key_path):
           """Suppression d'une clé imbriquée."""
           keys = key_path.split('.')
           current = config
           
           try:
               for key in keys[:-1]:
                   current = current[key]
               
               if keys[-1] in current:
                   del current[keys[-1]]
           except KeyError:
               pass  # Clé déjà absente

Conclusion
----------

Ce guide technique fournit une vue d'ensemble complète de l'architecture et de l'implémentation de CHNeoWave. Il couvre :

- **Architecture système** : Patterns MVC, composants principaux, patterns de conception
- **Gestion des données** : Format HDF5, validation, acquisition temps réel
- **Interface utilisateur** : Architecture MVC, Material Design, gestion des thèmes
- **Performance** : Monitoring, optimisation, gestion mémoire
- **Tests** : Architecture de tests, tests unitaires, intégration, performance
- **Configuration** : Fichiers YAML, déploiement, scripts de build
- **Maintenance** : Dépannage, logs, diagnostic, mises à jour

Pour toute question technique ou contribution au projet, consultez la documentation de développement et les guides de contribution.

.. note::
   Ce guide est maintenu à jour avec chaque version de CHNeoWave. 
   Version du guide : 1.0.0
   Dernière mise à jour : |today|