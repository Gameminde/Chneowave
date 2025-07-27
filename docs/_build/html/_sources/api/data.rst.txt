Module Data
===========

Le module ``data`` gère l'acquisition, le traitement et la persistance des données dans CHNeoWave.

.. currentmodule:: hrneowave.data

Acquisition de Données
---------------------

.. automodule:: hrneowave.data.acquisition
   :members:
   :undoc-members:
   :show-inheritance:

Gestionnaire d'Acquisition
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.acquisition.acquisition_manager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AcquisitionManager
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire principal de l'acquisition de données :
   
   * Configuration des paramètres d'acquisition
   * Contrôle des sessions d'acquisition
   * Gestion des buffers de données
   * Synchronisation multi-capteurs
   * Monitoring en temps réel

   .. automethod:: __init__
   .. automethod:: configure_acquisition
   .. automethod:: start_acquisition
   .. automethod:: stop_acquisition
   .. automethod:: pause_acquisition
   .. automethod:: resume_acquisition
   .. automethod:: get_acquisition_status
   .. automethod:: get_real_time_data

Configuration d'Acquisition
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.acquisition.acquisition_config
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AcquisitionConfig
   :members:
   :undoc-members:
   :show-inheritance:

   Configuration des paramètres d'acquisition :
   
   * Fréquence d'échantillonnage
   * Nombre de canaux
   * Durée d'acquisition
   * Filtres analogiques
   * Calibration des capteurs

   .. automethod:: __init__
   .. automethod:: validate_config
   .. automethod:: to_dict
   .. automethod:: from_dict
   .. automethod:: save_to_file
   .. automethod:: load_from_file

Session d'Acquisition
~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.acquisition.acquisition_session
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AcquisitionSession
   :members:
   :undoc-members:
   :show-inheritance:

   Représentation d'une session d'acquisition :
   
   * Métadonnées de session
   * Données temporelles
   * État de l'acquisition
   * Informations de qualité
   * Historique des événements

   .. automethod:: __init__
   .. automethod:: add_data_chunk
   .. automethod:: get_data_range
   .. automethod:: get_statistics
   .. automethod:: export_data
   .. automethod:: validate_data_integrity

Traitement de Données
--------------------

.. automodule:: hrneowave.data.processing
   :members:
   :undoc-members:
   :show-inheritance:

Processeur de Données
~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.processing.data_processor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DataProcessor
   :members:
   :undoc-members:
   :show-inheritance:

   Processeur principal des données :
   
   * Filtrage numérique
   * Décimation et interpolation
   * Correction de dérive
   * Détection d'anomalies
   * Préparation pour analyse

   .. automethod:: __init__
   .. automethod:: apply_filter
   .. automethod:: remove_drift
   .. automethod:: detect_outliers
   .. automethod:: resample_data
   .. automethod:: calibrate_data

Filtres Numériques
~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.processing.filters
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DigitalFilter
   :members:
   :undoc-members:
   :show-inheritance:

   Filtres numériques pour le traitement du signal :
   
   * Filtres passe-bas, passe-haut, passe-bande
   * Filtres de Butterworth, Chebyshev, Elliptique
   * Filtres adaptatifs
   * Filtres de Kalman

   .. automethod:: __init__
   .. automethod:: design_filter
   .. automethod:: apply_filter
   .. automethod:: get_frequency_response
   .. automethod:: plot_response

Validation de Données
~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.processing.validation
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DataValidator
   :members:
   :undoc-members:
   :show-inheritance:

   Validation et contrôle qualité des données :
   
   * Vérification de l'intégrité
   * Détection de valeurs aberrantes
   * Contrôle de cohérence temporelle
   * Évaluation de la qualité du signal
   * Génération de rapports de qualité

   .. automethod:: __init__
   .. automethod:: validate_data_integrity
   .. automethod:: check_temporal_consistency
   .. automethod:: assess_signal_quality
   .. automethod:: generate_quality_report

Analyse de Données
-----------------

.. automodule:: hrneowave.data.analysis
   :members:
   :undoc-members:
   :show-inheritance:

Analyse Spectrale
~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.analysis.spectral_analysis
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SpectralAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur spectral avancé :
   
   * Transformée de Fourier (FFT)
   * Analyse temps-fréquence (spectrogramme)
   * Densité spectrale de puissance (PSD)
   * Cohérence et phase
   * Détection de pics spectraux

   .. automethod:: __init__
   .. automethod:: compute_fft
   .. automethod:: compute_psd
   .. automethod:: compute_spectrogram
   .. automethod:: find_spectral_peaks
   .. automethod:: compute_coherence

Analyse de Goda
~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.analysis.goda_analysis
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: GodaAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur de vagues selon la méthode de Goda :
   
   * Analyse des hauteurs de vagues
   * Calcul des périodes caractéristiques
   * Statistiques de houle
   * Paramètres directionnels
   * Conditions de mer

   .. automethod:: __init__
   .. automethod:: analyze_wave_heights
   .. automethod:: compute_wave_periods
   .. automethod:: calculate_wave_statistics
   .. automethod:: estimate_directional_spectrum
   .. automethod:: classify_sea_state

Analyse Statistique
~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.analysis.statistical_analysis
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: StatisticalAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur statistique des données :
   
   * Statistiques descriptives
   * Distributions de probabilité
   * Tests d'hypothèses
   * Analyse de corrélation
   * Modélisation stochastique

   .. automethod:: __init__
   .. automethod:: compute_descriptive_stats
   .. automethod:: fit_probability_distribution
   .. automethod:: perform_hypothesis_test
   .. automethod:: compute_correlation_matrix
   .. automethod:: generate_statistical_report

Persistance de Données
---------------------

.. automodule:: hrneowave.data.storage
   :members:
   :undoc-members:
   :show-inheritance:

Gestionnaire de Stockage
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.storage.storage_manager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: StorageManager
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire de stockage des données :
   
   * Sauvegarde automatique
   * Compression des données
   * Indexation pour recherche rapide
   * Sauvegarde incrémentale
   * Récupération après panne

   .. automethod:: __init__
   .. automethod:: save_session
   .. automethod:: load_session
   .. automethod:: export_data
   .. automethod:: import_data
   .. automethod:: cleanup_old_data

Formats de Données
~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.storage.formats
   :members:
   :undoc-members:
   :show-inheritance:

Format HDF5
^^^^^^^^^^^

.. autoclass:: HDF5Handler
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire de fichiers HDF5 :
   
   * Stockage hiérarchique
   * Compression efficace
   * Métadonnées intégrées
   * Accès partiel aux données
   * Compatibilité multi-plateforme

Format CSV
^^^^^^^^^^

.. autoclass:: CSVHandler
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire de fichiers CSV :
   
   * Export pour analyse externe
   * Format lisible par l'humain
   * Compatibilité universelle
   * Configuration flexible
   * Gestion des gros volumes

Format MAT
^^^^^^^^^^

.. autoclass:: MATHandler
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire de fichiers MATLAB :
   
   * Compatibilité MATLAB/Octave
   * Structures de données complexes
   * Métadonnées préservées
   * Import/export bidirectionnel
   * Optimisation mémoire

Modèles de Données
-----------------

.. automodule:: hrneowave.data.models
   :members:
   :undoc-members:
   :show-inheritance:

Modèle de Projet
~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.models.project
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Project
   :members:
   :undoc-members:
   :show-inheritance:

   Modèle de données pour un projet :
   
   * Métadonnées du projet
   * Configuration globale
   * Sessions d'acquisition
   * Résultats d'analyse
   * Historique des modifications

   .. automethod:: __init__
   .. automethod:: add_session
   .. automethod:: get_session
   .. automethod:: remove_session
   .. automethod:: save_project
   .. automethod:: load_project

Modèle de Session
~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.models.session
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Session
   :members:
   :undoc-members:
   :show-inheritance:

   Modèle de données pour une session :
   
   * Données temporelles
   * Configuration d'acquisition
   * Métadonnées de session
   * Résultats d'analyse
   * Annotations utilisateur

   .. automethod:: __init__
   .. automethod:: add_data
   .. automethod:: get_data_slice
   .. automethod:: add_annotation
   .. automethod:: export_session

Modèle de Capteur
~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.models.sensor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: Sensor
   :members:
   :undoc-members:
   :show-inheritance:

   Modèle de données pour un capteur :
   
   * Caractéristiques techniques
   * Paramètres de calibration
   * Historique de maintenance
   * Données de performance
   * Configuration d'acquisition

   .. automethod:: __init__
   .. automethod:: calibrate
   .. automethod:: get_transfer_function
   .. automethod:: validate_configuration
   .. automethod:: update_maintenance_log

Utilitaires de Données
---------------------

.. automodule:: hrneowave.data.utils
   :members:
   :undoc-members:
   :show-inheritance:

Conversion de Données
~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.utils.converters
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: convert_units
.. autofunction:: resample_data
.. autofunction:: interpolate_missing_data
.. autofunction:: normalize_data
.. autofunction:: denormalize_data

Validation de Données
~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.data.utils.validators
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: validate_sampling_rate
.. autofunction:: validate_data_range
.. autofunction:: validate_temporal_consistency
.. autofunction:: validate_channel_count
.. autofunction:: validate_data_format

Exemples d'Utilisation
---------------------

Acquisition de Données
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.data.acquisition import AcquisitionManager, AcquisitionConfig
   import numpy as np
   
   # Configuration de l'acquisition
   config = AcquisitionConfig(
       sampling_rate=1000.0,  # Hz
       channels=[0, 1, 2, 3],
       duration=60.0,  # secondes
       buffer_size=1024
   )
   
   # Gestionnaire d'acquisition
   manager = AcquisitionManager()
   manager.configure_acquisition(config)
   
   # Démarrer l'acquisition
   session = manager.start_acquisition()
   
   # Monitoring en temps réel
   while manager.is_acquiring():
       real_time_data = manager.get_real_time_data()
       print(f"Données reçues: {real_time_data.shape}")
       time.sleep(0.1)
   
   # Arrêter l'acquisition
   manager.stop_acquisition()
   
   # Sauvegarder la session
   session.save_to_file("ma_session.h5")

Analyse Spectrale
~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.data.analysis import SpectralAnalyzer
   from hrneowave.data.storage import HDF5Handler
   import matplotlib.pyplot as plt
   
   # Charger les données
   handler = HDF5Handler()
   data = handler.load_data("ma_session.h5")
   
   # Créer l'analyseur spectral
   analyzer = SpectralAnalyzer(sampling_rate=1000.0)
   
   # Calculer la FFT
   frequencies, spectrum = analyzer.compute_fft(
       data[:, 0],  # Premier canal
       window='hann',
       nperseg=1024
   )
   
   # Calculer la densité spectrale de puissance
   freq_psd, psd = analyzer.compute_psd(
       data[:, 0],
       method='welch',
       nperseg=1024,
       overlap=0.5
   )
   
   # Détecter les pics spectraux
   peaks = analyzer.find_spectral_peaks(
       freq_psd, psd,
       height_threshold=0.1,
       prominence=0.05
   )
   
   # Visualisation
   plt.figure(figsize=(12, 8))
   
   plt.subplot(2, 1, 1)
   plt.plot(frequencies, np.abs(spectrum))
   plt.title('Spectre FFT')
   plt.xlabel('Fréquence (Hz)')
   plt.ylabel('Amplitude')
   
   plt.subplot(2, 1, 2)
   plt.semilogy(freq_psd, psd)
   plt.scatter(freq_psd[peaks], psd[peaks], color='red', s=50)
   plt.title('Densité Spectrale de Puissance')
   plt.xlabel('Fréquence (Hz)')
   plt.ylabel('PSD')
   
   plt.tight_layout()
   plt.show()

Analyse de Goda
~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.data.analysis import GodaAnalyzer
   import numpy as np
   
   # Données de vagues (élévation de surface)
   wave_data = np.random.randn(10000) * 0.5  # Simulation
   sampling_rate = 10.0  # Hz
   
   # Créer l'analyseur de Goda
   analyzer = GodaAnalyzer(sampling_rate=sampling_rate)
   
   # Analyser les hauteurs de vagues
   wave_heights = analyzer.analyze_wave_heights(
       wave_data,
       method='zero_crossing'
   )
   
   # Calculer les périodes caractéristiques
   wave_periods = analyzer.compute_wave_periods(
       wave_data,
       wave_heights
   )
   
   # Statistiques de houle
   wave_stats = analyzer.calculate_wave_statistics(
       wave_heights,
       wave_periods
   )
   
   print(f"Hauteur significative (Hs): {wave_stats['Hs']:.2f} m")
   print(f"Période moyenne (Tm): {wave_stats['Tm']:.2f} s")
   print(f"Période de pic (Tp): {wave_stats['Tp']:.2f} s")
   print(f"Hauteur maximale (Hmax): {wave_stats['Hmax']:.2f} m")
   
   # Classification de l'état de mer
   sea_state = analyzer.classify_sea_state(wave_stats['Hs'])
   print(f"État de mer: {sea_state}")

Gestion de Projet
~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.data.models import Project, Session
   from hrneowave.data.storage import StorageManager
   from datetime import datetime
   
   # Créer un nouveau projet
   project = Project(
       name="Étude Houle Méditerranée",
       description="Analyse des conditions de houle en bassin",
       location="Laboratoire Maritime",
       created_date=datetime.now()
   )
   
   # Ajouter des sessions
   session1 = Session(
       name="Session_001",
       description="Conditions calmes",
       acquisition_config={
           'sampling_rate': 1000.0,
           'duration': 300.0,
           'channels': [0, 1, 2, 3]
       }
   )
   
   session2 = Session(
       name="Session_002",
       description="Conditions agitées",
       acquisition_config={
           'sampling_rate': 1000.0,
           'duration': 600.0,
           'channels': [0, 1, 2, 3]
       }
   )
   
   project.add_session(session1)
   project.add_session(session2)
   
   # Gestionnaire de stockage
   storage = StorageManager()
   
   # Sauvegarder le projet
   storage.save_project(project, "mon_projet.chw")
   
   # Charger le projet
   loaded_project = storage.load_project("mon_projet.chw")
   
   print(f"Projet chargé: {loaded_project.name}")
   print(f"Nombre de sessions: {len(loaded_project.sessions)}")
   
   # Exporter les données
   for session in loaded_project.sessions:
       storage.export_session_data(
           session,
           format='csv',
           output_path=f"{session.name}.csv"
       )