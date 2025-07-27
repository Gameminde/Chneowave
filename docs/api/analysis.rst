Module Analysis
===============

Le module ``analysis`` contient les algorithmes d'analyse avancée pour le traitement des données de houle et de vagues.

.. currentmodule:: hrneowave.analysis

Analyse Spectrale
----------------

.. automodule:: hrneowave.analysis.spectral
   :members:
   :undoc-members:
   :show-inheritance:

Transformée de Fourier
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.spectral.fft_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: FFTAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur FFT optimisé pour les signaux de houle :
   
   * FFT rapide avec fenêtrage adaptatif
   * Correction de fuite spectrale
   * Analyse multi-canaux
   * Détection automatique de pics
   * Estimation de la résolution fréquentielle

   .. automethod:: __init__
   .. automethod:: compute_fft
   .. automethod:: compute_magnitude_spectrum
   .. automethod:: compute_phase_spectrum
   .. automethod:: find_dominant_frequencies
   .. automethod:: estimate_frequency_resolution

Densité Spectrale de Puissance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.spectral.psd_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: PSDAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur de densité spectrale de puissance :
   
   * Méthode de Welch optimisée
   * Estimation de Bartlett
   * Correction de biais
   * Lissage spectral adaptatif
   * Calcul de bandes de confiance

   .. automethod:: __init__
   .. automethod:: welch_method
   .. automethod:: bartlett_method
   .. automethod:: compute_confidence_intervals
   .. automethod:: smooth_spectrum
   .. automethod:: integrate_spectral_bands

Analyse Temps-Fréquence
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.spectral.spectrogram
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SpectrogramAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur spectrogramme pour signaux non-stationnaires :
   
   * STFT (Short-Time Fourier Transform)
   * Transformée en ondelettes
   * Analyse de Wigner-Ville
   * Détection de transitoires
   * Suivi de fréquences instantanées

   .. automethod:: __init__
   .. automethod:: compute_stft
   .. automethod:: compute_wavelet_transform
   .. automethod:: compute_wigner_ville
   .. automethod:: track_instantaneous_frequency
   .. automethod:: detect_transients

Analyse de Houle (Goda)
----------------------

.. automodule:: hrneowave.analysis.wave
   :members:
   :undoc-members:
   :show-inheritance:

Analyseur de Goda
~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.wave.goda_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: GodaWaveAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur de vagues selon la méthode de Goda :
   
   * Détection de crêtes et creux
   * Calcul des hauteurs individuelles
   * Statistiques de hauteurs (H1/3, H1/10, Hrms)
   * Périodes caractéristiques (Tz, Tc, Tp)
   * Distribution de Rayleigh

   .. automethod:: __init__
   .. automethod:: detect_wave_crests
   .. automethod:: detect_wave_troughs
   .. automethod:: calculate_individual_heights
   .. automethod:: calculate_height_statistics
   .. automethod:: calculate_period_statistics
   .. automethod:: fit_rayleigh_distribution

Analyse Directionnelle
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.wave.directional_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DirectionalWaveAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur directionnel des vagues :
   
   * Spectre directionnel 2D
   * Direction moyenne et étalement
   * Fonction de répartition directionnelle
   * Analyse de la propagation
   * Décomposition en modes

   .. automethod:: __init__
   .. automethod:: compute_directional_spectrum
   .. automethod:: calculate_mean_direction
   .. automethod:: calculate_directional_spreading
   .. automethod:: analyze_wave_propagation
   .. automethod:: decompose_directional_modes

Classification d'États de Mer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.wave.sea_state_classifier
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SeaStateClassifier
   :members:
   :undoc-members:
   :show-inheritance:

   Classificateur d'états de mer :
   
   * Échelle de Douglas
   * Classification WMO
   * États de mer significatifs
   * Conditions de navigation
   * Prédiction de conditions

   .. automethod:: __init__
   .. automethod:: classify_douglas_scale
   .. automethod:: classify_wmo_scale
   .. automethod:: assess_navigation_conditions
   .. automethod:: predict_sea_state_evolution
   .. automethod:: generate_sea_state_report

Analyse Statistique
------------------

.. automodule:: hrneowave.analysis.statistics
   :members:
   :undoc-members:
   :show-inheritance:

Statistiques Descriptives
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.statistics.descriptive
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DescriptiveStatistics
   :members:
   :undoc-members:
   :show-inheritance:

   Calculateur de statistiques descriptives :
   
   * Moments statistiques (moyenne, variance, skewness, kurtosis)
   * Quantiles et percentiles
   * Statistiques robustes
   * Mesures de dispersion
   * Tests de normalité

   .. automethod:: __init__
   .. automethod:: calculate_moments
   .. automethod:: calculate_quantiles
   .. automethod:: calculate_robust_statistics
   .. automethod:: test_normality
   .. automethod:: generate_summary_statistics

Distributions de Probabilité
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.statistics.distributions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ProbabilityDistributionFitter
   :members:
   :undoc-members:
   :show-inheritance:

   Ajustement de distributions de probabilité :
   
   * Distribution de Rayleigh (hauteurs de vagues)
   * Distribution de Weibull (vitesses de vent)
   * Distribution log-normale (périodes)
   * Distribution gamma généralisée
   * Tests de qualité d'ajustement

   .. automethod:: __init__
   .. automethod:: fit_rayleigh
   .. automethod:: fit_weibull
   .. automethod:: fit_lognormal
   .. automethod:: fit_generalized_gamma
   .. automethod:: goodness_of_fit_test
   .. automethod:: compare_distributions

Analyse de Corrélation
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.statistics.correlation
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: CorrelationAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur de corrélations :
   
   * Corrélation de Pearson
   * Corrélation de Spearman
   * Corrélation croisée temporelle
   * Cohérence spectrale
   * Analyse de causalité

   .. automethod:: __init__
   .. automethod:: pearson_correlation
   .. automethod:: spearman_correlation
   .. automethod:: cross_correlation
   .. automethod:: spectral_coherence
   .. automethod:: granger_causality

Analyse de Tendances
-------------------

.. automodule:: hrneowave.analysis.trends
   :members:
   :undoc-members:
   :show-inheritance:

Détection de Tendances
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.trends.trend_detector
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: TrendDetector
   :members:
   :undoc-members:
   :show-inheritance:

   Détecteur de tendances temporelles :
   
   * Test de Mann-Kendall
   * Régression linéaire robuste
   * Détection de points de rupture
   * Analyse de saisonnalité
   * Filtrage de tendances

   .. automethod:: __init__
   .. automethod:: mann_kendall_test
   .. automethod:: robust_linear_regression
   .. automethod:: detect_change_points
   .. automethod:: seasonal_decomposition
   .. automethod:: detrend_signal

Analyse de Cycles
~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.trends.cycle_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: CycleAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur de cycles temporels :
   
   * Détection de périodicités
   * Analyse harmonique
   * Cycles de marée
   * Variations saisonnières
   * Modulation d'amplitude

   .. automethod:: __init__
   .. automethod:: detect_periodicities
   .. automethod:: harmonic_analysis
   .. automethod:: tidal_analysis
   .. automethod:: seasonal_analysis
   .. automethod:: amplitude_modulation_analysis

Analyse de Qualité
-----------------

.. automodule:: hrneowave.analysis.quality
   :members:
   :undoc-members:
   :show-inheritance:

Évaluateur de Qualité
~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.quality.quality_assessor
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DataQualityAssessor
   :members:
   :undoc-members:
   :show-inheritance:

   Évaluateur de qualité des données :
   
   * Détection de valeurs aberrantes
   * Évaluation de la continuité
   * Analyse du rapport signal/bruit
   * Détection de dérives
   * Score de qualité global

   .. automethod:: __init__
   .. automethod:: detect_outliers
   .. automethod:: assess_continuity
   .. automethod:: calculate_snr
   .. automethod:: detect_drift
   .. automethod:: compute_quality_score

Détecteur d'Anomalies
~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.quality.anomaly_detector
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AnomalyDetector
   :members:
   :undoc-members:
   :show-inheritance:

   Détecteur d'anomalies dans les signaux :
   
   * Détection basée sur les seuils
   * Méthodes statistiques (Z-score, IQR)
   * Algorithmes d'apprentissage automatique
   * Détection de nouveautés
   * Classification d'anomalies

   .. automethod:: __init__
   .. automethod:: threshold_based_detection
   .. automethod:: statistical_detection
   .. automethod:: ml_based_detection
   .. automethod:: novelty_detection
   .. automethod:: classify_anomalies

Algorithmes Avancés
------------------

.. automodule:: hrneowave.analysis.advanced
   :members:
   :undoc-members:
   :show-inheritance:

Analyse en Composantes Principales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.advanced.pca_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: PCAAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur en composantes principales :
   
   * Réduction de dimensionnalité
   * Identification des modes principaux
   * Analyse de variance expliquée
   * Reconstruction de signaux
   * Détection de patterns

   .. automethod:: __init__
   .. automethod:: fit_pca
   .. automethod:: transform_data
   .. automethod:: explained_variance_ratio
   .. automethod:: reconstruct_signal
   .. automethod:: detect_patterns

Analyse de Décomposition Modale
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.advanced.modal_decomposition
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ModalDecomposer
   :members:
   :undoc-members:
   :show-inheritance:

   Décomposeur modal empirique :
   
   * Décomposition en modes empiriques (EMD)
   * EMD d'ensemble (EEMD)
   * Décomposition en modes variationnels (VMD)
   * Analyse des fonctions modales intrinsèques
   * Reconstruction sélective

   .. automethod:: __init__
   .. automethod:: empirical_mode_decomposition
   .. automethod:: ensemble_emd
   .. automethod:: variational_mode_decomposition
   .. automethod:: analyze_imfs
   .. automethod:: selective_reconstruction

Analyse de Réseaux
~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.advanced.network_analyzer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: NetworkAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:

   Analyseur de réseaux de capteurs :
   
   * Analyse de connectivité
   * Détection de communautés
   * Centralité des nœuds
   * Propagation d'information
   * Synchronisation de réseaux

   .. automethod:: __init__
   .. automethod:: build_connectivity_matrix
   .. automethod:: detect_communities
   .. automethod:: calculate_centrality
   .. automethod:: analyze_information_flow
   .. automethod:: assess_network_synchronization

Utilitaires d'Analyse
--------------------

.. automodule:: hrneowave.analysis.utils
   :members:
   :undoc-members:
   :show-inheritance:

Préprocessing
~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.utils.preprocessing
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: normalize_signal
.. autofunction:: detrend_signal
.. autofunction:: remove_outliers
.. autofunction:: interpolate_gaps
.. autofunction:: apply_window_function

Post-processing
~~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.utils.postprocessing
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: smooth_results
.. autofunction:: filter_results
.. autofunction:: aggregate_statistics
.. autofunction:: format_output
.. autofunction:: validate_results

Visualisations
~~~~~~~~~~~~~

.. automodule:: hrneowave.analysis.utils.visualization
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: plot_spectrum
.. autofunction:: plot_spectrogram
.. autofunction:: plot_wave_statistics
.. autofunction:: plot_directional_spectrum
.. autofunction:: plot_quality_metrics

Exemples d'Utilisation
---------------------

Analyse Spectrale Complète
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.analysis.spectral import FFTAnalyzer, PSDAnalyzer
   from hrneowave.analysis.utils import normalize_signal
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Données simulées de houle
   fs = 10.0  # Hz
   t = np.arange(0, 600, 1/fs)  # 10 minutes
   
   # Signal composite : houle + vent + bruit
   signal = (0.5 * np.sin(2*np.pi*0.1*t) +  # Houle longue
            0.3 * np.sin(2*np.pi*0.3*t) +   # Houle courte
            0.1 * np.random.randn(len(t)))   # Bruit
   
   # Normalisation
   signal_norm = normalize_signal(signal)
   
   # Analyse FFT
   fft_analyzer = FFTAnalyzer(sampling_rate=fs)
   frequencies, spectrum = fft_analyzer.compute_fft(
       signal_norm,
       window='hann',
       zero_padding=2
   )
   
   # Détection des fréquences dominantes
   dominant_freqs = fft_analyzer.find_dominant_frequencies(
       frequencies, spectrum,
       num_peaks=5,
       min_prominence=0.1
   )
   
   # Analyse PSD
   psd_analyzer = PSDAnalyzer(sampling_rate=fs)
   freq_psd, psd = psd_analyzer.welch_method(
       signal_norm,
       nperseg=1024,
       overlap=0.5,
       window='hann'
   )
   
   # Intégration par bandes spectrales
   energy_bands = psd_analyzer.integrate_spectral_bands(
       freq_psd, psd,
       bands=[(0.05, 0.15), (0.15, 0.35), (0.35, 0.5)]
   )
   
   # Visualisation
   fig, axes = plt.subplots(3, 1, figsize=(12, 10))
   
   # Signal temporel
   axes[0].plot(t[:1000], signal_norm[:1000])
   axes[0].set_title('Signal Temporel (premiers 100s)')
   axes[0].set_xlabel('Temps (s)')
   axes[0].set_ylabel('Amplitude normalisée')
   
   # Spectre FFT
   axes[1].plot(frequencies, np.abs(spectrum))
   axes[1].scatter([frequencies[i] for i in dominant_freqs],
                  [np.abs(spectrum[i]) for i in dominant_freqs],
                  color='red', s=50, zorder=5)
   axes[1].set_title('Spectre FFT avec Pics Dominants')
   axes[1].set_xlabel('Fréquence (Hz)')
   axes[1].set_ylabel('Amplitude')
   axes[1].set_xlim(0, 1)
   
   # Densité spectrale de puissance
   axes[2].semilogy(freq_psd, psd)
   axes[2].set_title('Densité Spectrale de Puissance')
   axes[2].set_xlabel('Fréquence (Hz)')
   axes[2].set_ylabel('PSD')
   axes[2].set_xlim(0, 1)
   
   plt.tight_layout()
   plt.show()
   
   # Affichage des résultats
   print("Fréquences dominantes (Hz):")
   for i, freq_idx in enumerate(dominant_freqs):
       print(f"  {i+1}: {frequencies[freq_idx]:.3f} Hz")
   
   print("\nÉnergie par bandes spectrales:")
   band_names = ['Houle longue', 'Houle courte', 'Vagues de vent']
   for i, (band, energy) in enumerate(zip(band_names, energy_bands)):
       print(f"  {band}: {energy:.4f}")

Analyse de Goda Complète
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.analysis.wave import GodaWaveAnalyzer, SeaStateClassifier
   from hrneowave.analysis.statistics import DescriptiveStatistics
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Simulation d'élévation de surface libre
   fs = 10.0  # Hz
   duration = 1200  # 20 minutes
   t = np.arange(0, duration, 1/fs)
   
   # Génération d'un signal de vagues réaliste
   np.random.seed(42)
   Hs = 1.5  # Hauteur significative (m)
   Tp = 8.0  # Période de pic (s)
   
   # Spectre JONSWAP simplifié
   frequencies = np.fft.fftfreq(len(t), 1/fs)[:len(t)//2]
   fp = 1/Tp
   gamma = 3.3
   
   # Génération du signal
   phases = np.random.uniform(0, 2*np.pi, len(frequencies))
   amplitudes = np.sqrt(2 * 0.0081 * (Hs**2) * (frequencies**-5) * 
                       np.exp(-1.25 * (frequencies/fp)**-4))
   amplitudes[0] = 0  # Pas de composante DC
   
   # Signal temporel
   eta = np.zeros(len(t))
   for i, (amp, freq, phase) in enumerate(zip(amplitudes, frequencies, phases)):
       if freq > 0:
           eta += amp * np.cos(2*np.pi*freq*t + phase)
   
   # Analyse de Goda
   goda_analyzer = GodaWaveAnalyzer(sampling_rate=fs)
   
   # Détection des vagues
   crests = goda_analyzer.detect_wave_crests(eta, min_height=0.1)
   troughs = goda_analyzer.detect_wave_troughs(eta, min_depth=0.1)
   
   # Calcul des hauteurs individuelles
   wave_heights = goda_analyzer.calculate_individual_heights(
       eta, crests, troughs
   )
   
   # Statistiques de hauteurs
   height_stats = goda_analyzer.calculate_height_statistics(wave_heights)
   
   # Calcul des périodes
   wave_periods = goda_analyzer.calculate_period_statistics(
       eta, crests, sampling_rate=fs
   )
   
   # Ajustement distribution de Rayleigh
   rayleigh_params = goda_analyzer.fit_rayleigh_distribution(wave_heights)
   
   # Classification état de mer
   classifier = SeaStateClassifier()
   sea_state = classifier.classify_douglas_scale(height_stats['H_s'])
   navigation_conditions = classifier.assess_navigation_conditions(
       height_stats, wave_periods
   )
   
   # Statistiques descriptives
   desc_stats = DescriptiveStatistics()
   height_moments = desc_stats.calculate_moments(wave_heights)
   
   # Visualisation
   fig, axes = plt.subplots(4, 1, figsize=(15, 12))
   
   # Signal temporel avec détection de vagues
   time_window = slice(0, 2000)  # Premiers 200s
   axes[0].plot(t[time_window], eta[time_window], 'b-', alpha=0.7)
   
   # Marquer les crêtes et creux dans la fenêtre
   crests_in_window = [c for c in crests if c < len(time_window)]
   troughs_in_window = [c for c in troughs if c < len(time_window)]
   
   axes[0].scatter(t[crests_in_window], eta[crests_in_window], 
                  color='red', s=30, zorder=5, label='Crêtes')
   axes[0].scatter(t[troughs_in_window], eta[troughs_in_window], 
                  color='blue', s=30, zorder=5, label='Creux')
   axes[0].set_title('Élévation de Surface avec Détection de Vagues')
   axes[0].set_xlabel('Temps (s)')
   axes[0].set_ylabel('Élévation (m)')
   axes[0].legend()
   axes[0].grid(True, alpha=0.3)
   
   # Histogramme des hauteurs
   axes[1].hist(wave_heights, bins=30, density=True, alpha=0.7, 
               color='skyblue', edgecolor='black')
   
   # Distribution de Rayleigh ajustée
   h_range = np.linspace(0, max(wave_heights), 100)
   rayleigh_pdf = (h_range / rayleigh_params['sigma']**2) * \
                  np.exp(-h_range**2 / (2 * rayleigh_params['sigma']**2))
   axes[1].plot(h_range, rayleigh_pdf, 'r-', linewidth=2, 
               label=f'Rayleigh (σ={rayleigh_params["sigma"]:.2f})')
   axes[1].axvline(height_stats['H_s'], color='green', linestyle='--', 
                  linewidth=2, label=f'Hs = {height_stats["H_s"]:.2f} m')
   axes[1].set_title('Distribution des Hauteurs de Vagues')
   axes[1].set_xlabel('Hauteur (m)')
   axes[1].set_ylabel('Densité de probabilité')
   axes[1].legend()
   axes[1].grid(True, alpha=0.3)
   
   # Statistiques de hauteurs
   stats_labels = ['H_s', 'H_max', 'H_mean', 'H_rms', 'H_1/10', 'H_1/3']
   stats_values = [height_stats[key] for key in stats_labels]
   
   bars = axes[2].bar(stats_labels, stats_values, color='lightcoral', 
                     edgecolor='darkred')
   axes[2].set_title('Statistiques des Hauteurs de Vagues')
   axes[2].set_ylabel('Hauteur (m)')
   axes[2].grid(True, alpha=0.3, axis='y')
   
   # Ajouter les valeurs sur les barres
   for bar, value in zip(bars, stats_values):
       axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                   f'{value:.2f}', ha='center', va='bottom')
   
   # Périodes caractéristiques
   period_labels = ['T_z', 'T_c', 'T_s', 'T_mean']
   period_values = [wave_periods[key] for key in period_labels]
   
   bars = axes[3].bar(period_labels, period_values, color='lightgreen', 
                     edgecolor='darkgreen')
   axes[3].set_title('Périodes Caractéristiques')
   axes[3].set_ylabel('Période (s)')
   axes[3].grid(True, alpha=0.3, axis='y')
   
   # Ajouter les valeurs sur les barres
   for bar, value in zip(bars, period_values):
       axes[3].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   f'{value:.1f}', ha='center', va='bottom')
   
   plt.tight_layout()
   plt.show()
   
   # Rapport détaillé
   print("=== RAPPORT D'ANALYSE DE GODA ===")
   print(f"\nDurée d'analyse: {duration/60:.1f} minutes")
   print(f"Nombre de vagues détectées: {len(wave_heights)}")
   
   print("\n--- STATISTIQUES DE HAUTEURS ---")
   for label, value in zip(stats_labels, stats_values):
       print(f"{label:8s}: {value:6.2f} m")
   
   print("\n--- PÉRIODES CARACTÉRISTIQUES ---")
   for label, value in zip(period_labels, period_values):
       print(f"{label:8s}: {value:6.1f} s")
   
   print("\n--- CLASSIFICATION ---")
   print(f"État de mer (Douglas): {sea_state['scale']} - {sea_state['description']}")
   print(f"Conditions de navigation: {navigation_conditions['category']}")
   print(f"Recommandations: {navigation_conditions['recommendations']}")
   
   print("\n--- DISTRIBUTION DE RAYLEIGH ---")
   print(f"Paramètre σ: {rayleigh_params['sigma']:.3f}")
   print(f"Qualité d'ajustement (R²): {rayleigh_params['r_squared']:.3f}")
   
   print("\n--- MOMENTS STATISTIQUES ---")
   print(f"Moyenne: {height_moments['mean']:.3f} m")
   print(f"Écart-type: {height_moments['std']:.3f} m")
   print(f"Asymétrie (skewness): {height_moments['skewness']:.3f}")
   print(f"Aplatissement (kurtosis): {height_moments['kurtosis']:.3f}")

Analyse Multi-Capteurs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.analysis.advanced import PCAAnalyzer, NetworkAnalyzer
   from hrneowave.analysis.statistics import CorrelationAnalyzer
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Simulation de données multi-capteurs
   fs = 20.0  # Hz
   duration = 600  # 10 minutes
   t = np.arange(0, duration, 1/fs)
   n_sensors = 8
   
   # Génération de signaux corrélés spatialement
   np.random.seed(123)
   
   # Signal de référence (mode principal)
   ref_signal = np.sin(2*np.pi*0.15*t) + 0.3*np.sin(2*np.pi*0.4*t)
   
   # Matrice de données multi-capteurs
   data_matrix = np.zeros((len(t), n_sensors))
   
   for i in range(n_sensors):
       # Atténuation spatiale
       attenuation = np.exp(-0.1 * i)
       # Déphasage spatial
       phase_shift = 0.2 * i
       # Bruit local
       local_noise = 0.1 * np.random.randn(len(t))
       
       data_matrix[:, i] = (attenuation * 
                           np.roll(ref_signal, int(phase_shift * fs)) + 
                           local_noise)
   
   # Analyse en composantes principales
   pca_analyzer = PCAAnalyzer()
   pca_result = pca_analyzer.fit_pca(data_matrix, n_components=4)
   
   # Transformation des données
   transformed_data = pca_analyzer.transform_data(data_matrix)
   
   # Variance expliquée
   explained_variance = pca_analyzer.explained_variance_ratio()
   
   # Analyse de corrélation
   corr_analyzer = CorrelationAnalyzer()
   
   # Matrice de corrélation de Pearson
   pearson_matrix = corr_analyzer.pearson_correlation(data_matrix)
   
   # Corrélations croisées temporelles
   cross_corr_results = {}
   for i in range(1, n_sensors):
       cross_corr = corr_analyzer.cross_correlation(
           data_matrix[:, 0], data_matrix[:, i],
           max_lag=int(2*fs)  # ±2 secondes
       )
       cross_corr_results[f'Sensor_{i+1}'] = cross_corr
   
   # Analyse de réseau
   network_analyzer = NetworkAnalyzer()
   
   # Construction de la matrice de connectivité
   connectivity_matrix = network_analyzer.build_connectivity_matrix(
       data_matrix, method='correlation', threshold=0.3
   )
   
   # Détection de communautés
   communities = network_analyzer.detect_communities(connectivity_matrix)
   
   # Centralité des nœuds
   centrality = network_analyzer.calculate_centrality(
       connectivity_matrix, method='betweenness'
   )
   
   # Visualisation
   fig = plt.figure(figsize=(16, 12))
   
   # Signaux temporels (échantillon)
   ax1 = plt.subplot(3, 3, 1)
   time_sample = slice(0, int(60*fs))  # Premier minute
   for i in range(min(4, n_sensors)):
       plt.plot(t[time_sample], data_matrix[time_sample, i], 
               label=f'Capteur {i+1}', alpha=0.8)
   plt.title('Signaux Multi-Capteurs (1ère minute)')
   plt.xlabel('Temps (s)')
   plt.ylabel('Amplitude')
   plt.legend()
   plt.grid(True, alpha=0.3)
   
   # Variance expliquée par les composantes principales
   ax2 = plt.subplot(3, 3, 2)
   plt.bar(range(1, len(explained_variance)+1), explained_variance*100,
          color='skyblue', edgecolor='navy')
   plt.title('Variance Expliquée par Composante')
   plt.xlabel('Composante Principale')
   plt.ylabel('Variance Expliquée (%)')
   plt.grid(True, alpha=0.3, axis='y')
   
   # Premières composantes principales
   ax3 = plt.subplot(3, 3, 3)
   for i in range(min(3, transformed_data.shape[1])):
       plt.plot(t[time_sample], transformed_data[time_sample, i], 
               label=f'PC{i+1}', linewidth=2)
   plt.title('Composantes Principales')
   plt.xlabel('Temps (s)')
   plt.ylabel('Amplitude')
   plt.legend()
   plt.grid(True, alpha=0.3)
   
   # Matrice de corrélation
   ax4 = plt.subplot(3, 3, 4)
   im = plt.imshow(pearson_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
   plt.colorbar(im, shrink=0.8)
   plt.title('Matrice de Corrélation de Pearson')
   plt.xlabel('Capteur')
   plt.ylabel('Capteur')
   
   # Ajouter les valeurs dans la matrice
   for i in range(n_sensors):
       for j in range(n_sensors):
           plt.text(j, i, f'{pearson_matrix[i,j]:.2f}', 
                   ha='center', va='center', 
                   color='white' if abs(pearson_matrix[i,j]) > 0.5 else 'black')
   
   # Corrélations croisées avec le capteur de référence
   ax5 = plt.subplot(3, 3, 5)
   for sensor_name, cross_corr in list(cross_corr_results.items())[:3]:
       lags = np.arange(-len(cross_corr['correlation'])//2, 
                       len(cross_corr['correlation'])//2) / fs
       plt.plot(lags, cross_corr['correlation'], 
               label=sensor_name, linewidth=2)
   plt.title('Corrélations Croisées (vs Capteur 1)')
   plt.xlabel('Délai (s)')
   plt.ylabel('Corrélation')
   plt.legend()
   plt.grid(True, alpha=0.3)
   
   # Matrice de connectivité du réseau
   ax6 = plt.subplot(3, 3, 6)
   im = plt.imshow(connectivity_matrix, cmap='Blues')
   plt.colorbar(im, shrink=0.8)
   plt.title('Matrice de Connectivité')
   plt.xlabel('Capteur')
   plt.ylabel('Capteur')
   
   # Centralité des nœuds
   ax7 = plt.subplot(3, 3, 7)
   plt.bar(range(1, n_sensors+1), centrality, 
          color='lightcoral', edgecolor='darkred')
   plt.title('Centralité des Capteurs')
   plt.xlabel('Capteur')
   plt.ylabel('Centralité')
   plt.grid(True, alpha=0.3, axis='y')
   
   # Communautés détectées
   ax8 = plt.subplot(3, 3, 8)
   colors = plt.cm.Set3(np.linspace(0, 1, len(set(communities))))
   community_colors = [colors[communities[i]] for i in range(n_sensors)]
   
   plt.scatter(range(1, n_sensors+1), [1]*n_sensors, 
              c=community_colors, s=200, alpha=0.8)
   for i, comm in enumerate(communities):
       plt.text(i+1, 1, str(comm), ha='center', va='center', 
               fontweight='bold')
   plt.title('Communautés de Capteurs')
   plt.xlabel('Capteur')
   plt.ylim(0.5, 1.5)
   plt.yticks([])
   
   # Reconstruction du signal principal
   ax9 = plt.subplot(3, 3, 9)
   reconstructed = pca_analyzer.reconstruct_signal(
       transformed_data[:, :2], n_components=2
   )
   
   plt.plot(t[time_sample], data_matrix[time_sample, 0], 
           'b-', label='Signal Original', alpha=0.7)
   plt.plot(t[time_sample], reconstructed[time_sample, 0], 
           'r--', label='Reconstruction (2 PC)', linewidth=2)
   plt.title('Reconstruction par PCA')
   plt.xlabel('Temps (s)')
   plt.ylabel('Amplitude')
   plt.legend()
   plt.grid(True, alpha=0.3)
   
   plt.tight_layout()
   plt.show()
   
   # Rapport d'analyse
   print("=== RAPPORT D'ANALYSE MULTI-CAPTEURS ===")
   print(f"\nNombre de capteurs: {n_sensors}")
   print(f"Durée d'analyse: {duration/60:.1f} minutes")
   print(f"Fréquence d'échantillonnage: {fs} Hz")
   
   print("\n--- ANALYSE EN COMPOSANTES PRINCIPALES ---")
   print("Variance expliquée par composante:")
   for i, var in enumerate(explained_variance):
       print(f"  PC{i+1}: {var*100:5.1f}%")
   
   cumulative_var = np.cumsum(explained_variance)
   print(f"\nVariance cumulée (2 premières PC): {cumulative_var[1]*100:.1f}%")
   print(f"Variance cumulée (3 premières PC): {cumulative_var[2]*100:.1f}%")
   
   print("\n--- ANALYSE DE CORRÉLATION ---")
   print("Corrélations moyennes par capteur:")
   for i in range(n_sensors):
       mean_corr = np.mean([pearson_matrix[i, j] for j in range(n_sensors) if i != j])
       print(f"  Capteur {i+1}: {mean_corr:5.3f}")
   
   print("\n--- ANALYSE DE RÉSEAU ---")
   print(f"Nombre de communautés détectées: {len(set(communities))}")
   print("Composition des communautés:")
   for comm_id in set(communities):
       members = [i+1 for i, c in enumerate(communities) if c == comm_id]
       print(f"  Communauté {comm_id}: Capteurs {members}")
   
   print("\nCapteurs les plus centraux:")
   sorted_centrality = sorted(enumerate(centrality), key=lambda x: x[1], reverse=True)
   for i, (sensor_idx, cent_value) in enumerate(sorted_centrality[:3]):
       print(f"  {i+1}. Capteur {sensor_idx+1}: {cent_value:.3f}")