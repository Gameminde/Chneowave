Module Utils
============

Le module ``utils`` contient les utilitaires, helpers et fonctions communes utilisées dans CHNeoWave.

.. currentmodule:: hrneowave.utils

Gestion de Configuration
-----------------------

.. automodule:: hrneowave.utils.config
   :members:
   :undoc-members:
   :show-inheritance:

Gestionnaire de Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.utils.config.config_manager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ConfigManager
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire centralisé de configuration :
   
   * Chargement de fichiers de configuration
   * Validation des paramètres
   * Gestion des profils utilisateur
   * Sauvegarde automatique
   * Configuration par défaut

   .. automethod:: __init__
   .. automethod:: load_config
   .. automethod:: save_config
   .. automethod:: get_setting
   .. automethod:: set_setting
   .. automethod:: validate_config
   .. automethod:: reset_to_defaults

Validateur de Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.utils.config.config_validator
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ConfigValidator
   :members:
   :undoc-members:
   :show-inheritance:

   Validateur de paramètres de configuration :
   
   * Schémas de validation
   * Types de données
   * Plages de valeurs
   * Dépendances entre paramètres
   * Messages d'erreur détaillés

   .. automethod:: __init__
   .. automethod:: validate_schema
   .. automethod:: validate_types
   .. automethod:: validate_ranges
   .. automethod:: validate_dependencies
   .. automethod:: get_validation_errors

Gestion des Fichiers
-------------------

.. automodule:: hrneowave.utils.file_utils
   :members:
   :undoc-members:
   :show-inheritance:

Opérations sur Fichiers
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: ensure_directory_exists
.. autofunction:: get_file_size
.. autofunction:: get_file_extension
.. autofunction:: is_file_readable
.. autofunction:: is_file_writable
.. autofunction:: backup_file
.. autofunction:: cleanup_temp_files

Gestion des Chemins
~~~~~~~~~~~~~~~~~~

.. autofunction:: normalize_path
.. autofunction:: get_relative_path
.. autofunction:: find_files_by_pattern
.. autofunction:: get_project_root
.. autofunction:: create_unique_filename

Archivage et Compression
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: compress_file
.. autofunction:: decompress_file
.. autofunction:: create_archive
.. autofunction:: extract_archive
.. autofunction:: get_compression_ratio

Gestion des Logs
---------------

.. automodule:: hrneowave.utils.logging
   :members:
   :undoc-members:
   :show-inheritance:

Configuration des Logs
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.utils.logging.logger_config
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: LoggerConfig
   :members:
   :undoc-members:
   :show-inheritance:

   Configuration avancée du système de logs :
   
   * Niveaux de log configurables
   * Formatage personnalisé
   * Rotation automatique
   * Handlers multiples
   * Filtrage par module

   .. automethod:: __init__
   .. automethod:: setup_logger
   .. automethod:: add_file_handler
   .. automethod:: add_console_handler
   .. automethod:: set_log_level
   .. automethod:: configure_rotation

Utilitaires de Log
~~~~~~~~~~~~~~~~~

.. autofunction:: get_logger
.. autofunction:: log_function_call
.. autofunction:: log_performance
.. autofunction:: log_memory_usage
.. autofunction:: create_log_decorator

Gestion des Erreurs
------------------

.. automodule:: hrneowave.utils.error_handling
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions Personnalisées
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.utils.error_handling.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoexception:: CHNeoWaveError
   :members:
   :show-inheritance:

   Exception de base pour CHNeoWave.

.. autoexception:: ConfigurationError
   :members:
   :show-inheritance:

   Erreur de configuration.

.. autoexception:: DataValidationError
   :members:
   :show-inheritance:

   Erreur de validation des données.

.. autoexception:: AcquisitionError
   :members:
   :show-inheritance:

   Erreur d'acquisition de données.

.. autoexception:: AnalysisError
   :members:
   :show-inheritance:

   Erreur d'analyse.

.. autoexception:: ExportError
   :members:
   :show-inheritance:

   Erreur d'exportation.

Gestionnaire d'Erreurs
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.utils.error_handling.error_handler
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ErrorHandler
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire centralisé des erreurs :
   
   * Capture et traitement des exceptions
   * Logging automatique
   * Notifications utilisateur
   * Récupération d'erreurs
   * Rapports d'erreurs

   .. automethod:: __init__
   .. automethod:: handle_exception
   .. automethod:: register_error_callback
   .. automethod:: set_error_policy
   .. automethod:: generate_error_report
   .. automethod:: clear_error_history

Utilitaires de Validation
-------------------------

.. automodule:: hrneowave.utils.validation
   :members:
   :undoc-members:
   :show-inheritance:

Validation de Données
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: validate_numeric_range
.. autofunction:: validate_array_shape
.. autofunction:: validate_sampling_rate
.. autofunction:: validate_file_format
.. autofunction:: validate_project_structure

Validation de Types
~~~~~~~~~~~~~~~~~~

.. autofunction:: is_numeric
.. autofunction:: is_array_like
.. autofunction:: is_valid_path
.. autofunction:: is_valid_filename
.. autofunction:: check_required_fields

Décorateurs de Validation
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: validate_input
.. autofunction:: validate_output
.. autofunction:: require_positive
.. autofunction:: require_non_empty
.. autofunction:: validate_shape

Utilitaires Mathématiques
-------------------------

.. automodule:: hrneowave.utils.math_utils
   :members:
   :undoc-members:
   :show-inheritance:

Fonctions Mathématiques
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: safe_divide
.. autofunction:: safe_log
.. autofunction:: safe_sqrt
.. autofunction:: clamp
.. autofunction:: normalize_range
.. autofunction:: interpolate_linear

Statistiques Robustes
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: robust_mean
.. autofunction:: robust_std
.. autofunction:: median_absolute_deviation
.. autofunction:: trimmed_mean
.. autofunction:: winsorized_mean

Traitement de Signaux
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: next_power_of_2
.. autofunction:: zero_pad
.. autofunction:: apply_window
.. autofunction:: remove_dc_component
.. autofunction:: detect_peaks

Utilitaires de Performance
--------------------------

.. automodule:: hrneowave.utils.performance
   :members:
   :undoc-members:
   :show-inheritance:

Monitoring de Performance
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.utils.performance.profiler
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: PerformanceProfiler
   :members:
   :undoc-members:
   :show-inheritance:

   Profileur de performance :
   
   * Mesure de temps d'exécution
   * Monitoring mémoire
   * Analyse de goulots d'étranglement
   * Rapports de performance
   * Optimisation automatique

   .. automethod:: __init__
   .. automethod:: start_profiling
   .. automethod:: stop_profiling
   .. automethod:: get_performance_report
   .. automethod:: analyze_bottlenecks
   .. automethod:: suggest_optimizations

Décorateurs de Performance
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: time_it
.. autofunction:: memory_profile
.. autofunction:: cache_result
.. autofunction:: retry_on_failure
.. autofunction:: rate_limit

Optimisation
~~~~~~~~~~~

.. autofunction:: optimize_numpy_operations
.. autofunction:: parallel_map
.. autofunction:: batch_process
.. autofunction:: lazy_evaluation
.. autofunction:: memory_efficient_iterator

Utilitaires de Conversion
-------------------------

.. automodule:: hrneowave.utils.converters
   :members:
   :undoc-members:
   :show-inheritance:

Conversion d'Unités
~~~~~~~~~~~~~~~~~~

.. autofunction:: convert_frequency
.. autofunction:: convert_amplitude
.. autofunction:: convert_time
.. autofunction:: convert_angle
.. autofunction:: convert_pressure

Conversion de Formats
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: dict_to_yaml
.. autofunction:: yaml_to_dict
.. autofunction:: dict_to_json
.. autofunction:: json_to_dict
.. autofunction:: array_to_csv
.. autofunction:: csv_to_array

Conversion de Types
~~~~~~~~~~~~~~~~~~

.. autofunction:: to_numeric
.. autofunction:: to_string
.. autofunction:: to_boolean
.. autofunction:: to_datetime
.. autofunction:: to_array

Utilitaires de Système
----------------------

.. automodule:: hrneowave.utils.system
   :members:
   :undoc-members:
   :show-inheritance:

Informations Système
~~~~~~~~~~~~~~~~~~~

.. autofunction:: get_system_info
.. autofunction:: get_memory_usage
.. autofunction:: get_cpu_usage
.. autofunction:: get_disk_usage
.. autofunction:: get_python_version
.. autofunction:: get_dependencies_info

Gestion des Processus
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: run_command
.. autofunction:: kill_process
.. autofunction:: is_process_running
.. autofunction:: get_process_info
.. autofunction:: monitor_process

Gestion des Ressources
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: check_memory_available
.. autofunction:: cleanup_resources
.. autofunction:: set_process_priority
.. autofunction:: limit_memory_usage
.. autofunction:: monitor_resource_usage

Utilitaires de Sécurité
-----------------------

.. automodule:: hrneowave.utils.security
   :members:
   :undoc-members:
   :show-inheritance:

Chiffrement
~~~~~~~~~~

.. autofunction:: encrypt_data
.. autofunction:: decrypt_data
.. autofunction:: generate_key
.. autofunction:: hash_password
.. autofunction:: verify_password

Validation de Sécurité
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: sanitize_filename
.. autofunction:: validate_file_path
.. autofunction:: check_file_permissions
.. autofunction:: scan_for_malware
.. autofunction:: validate_input_data

Audit et Logs de Sécurité
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: log_security_event
.. autofunction:: audit_file_access
.. autofunction:: monitor_suspicious_activity
.. autofunction:: generate_security_report
.. autofunction:: check_integrity

Utilitaires de Test
------------------

.. automodule:: hrneowave.utils.testing
   :members:
   :undoc-members:
   :show-inheritance:

Fixtures de Test
~~~~~~~~~~~~~~~

.. autofunction:: create_test_data
.. autofunction:: create_mock_session
.. autofunction:: create_test_project
.. autofunction:: generate_synthetic_signal
.. autofunction:: create_test_config

Assertions Personnalisées
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: assert_array_almost_equal
.. autofunction:: assert_signal_properties
.. autofunction:: assert_frequency_content
.. autofunction:: assert_statistical_properties
.. autofunction:: assert_file_exists

Utilitaires de Mock
~~~~~~~~~~~~~~~~~~

.. autofunction:: mock_acquisition_device
.. autofunction:: mock_file_system
.. autofunction:: mock_network_connection
.. autofunction:: mock_database
.. autofunction:: create_test_environment

Utilitaires de Documentation
----------------------------

.. automodule:: hrneowave.utils.documentation
   :members:
   :undoc-members:
   :show-inheritance:

Génération de Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: generate_api_docs
.. autofunction:: extract_docstrings
.. autofunction:: generate_examples
.. autofunction:: create_user_guide
.. autofunction:: validate_documentation

Formatage de Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: format_docstring
.. autofunction:: add_code_examples
.. autofunction:: generate_cross_references
.. autofunction:: create_index
.. autofunction:: export_to_pdf

Exemples d'Utilisation
---------------------

Gestion de Configuration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.utils.config import ConfigManager, ConfigValidator
   import os
   
   # Créer le gestionnaire de configuration
   config_manager = ConfigManager()
   
   # Charger la configuration depuis un fichier
   config_path = "config/chneowave.yaml"
   if os.path.exists(config_path):
       config = config_manager.load_config(config_path)
   else:
       # Utiliser la configuration par défaut
       config = config_manager.get_default_config()
   
   # Accéder aux paramètres
   sampling_rate = config_manager.get_setting("acquisition.sampling_rate")
   buffer_size = config_manager.get_setting("acquisition.buffer_size")
   
   print(f"Fréquence d'échantillonnage: {sampling_rate} Hz")
   print(f"Taille du buffer: {buffer_size} échantillons")
   
   # Modifier un paramètre
   config_manager.set_setting("acquisition.sampling_rate", 2000.0)
   
   # Valider la configuration
   validator = ConfigValidator()
   validation_result = validator.validate_schema(config)
   
   if validation_result.is_valid:
       print("Configuration valide")
       # Sauvegarder les modifications
       config_manager.save_config(config_path)
   else:
       print("Erreurs de configuration:")
       for error in validation_result.errors:
           print(f"  - {error}")
   
   # Réinitialiser aux valeurs par défaut si nécessaire
   if input("Réinitialiser la configuration? (y/n): ").lower() == 'y':
       config_manager.reset_to_defaults()
       print("Configuration réinitialisée")

Gestion des Erreurs
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.utils.error_handling import ErrorHandler, CHNeoWaveError
   from hrneowave.utils.logging import get_logger
   import traceback
   
   # Configurer le gestionnaire d'erreurs
   error_handler = ErrorHandler()
   logger = get_logger(__name__)
   
   # Définir une politique d'erreur personnalisée
   def custom_error_policy(exception, context):
       """Politique personnalisée de gestion d'erreurs."""
       if isinstance(exception, CHNeoWaveError):
           # Erreurs métier : log et notification utilisateur
           logger.error(f"Erreur CHNeoWave: {exception}")
           return "notify_user"
       else:
           # Erreurs système : log détaillé et arrêt
           logger.critical(f"Erreur système: {exception}")
           logger.debug(traceback.format_exc())
           return "stop_execution"
   
   error_handler.set_error_policy(custom_error_policy)
   
   # Fonction de callback pour les erreurs
   def on_error_callback(error_info):
       """Callback appelé lors d'une erreur."""
       print(f"Erreur détectée: {error_info['message']}")
       print(f"Type: {error_info['type']}")
       print(f"Contexte: {error_info['context']}")
   
   error_handler.register_error_callback(on_error_callback)
   
   # Exemple d'utilisation avec gestion d'erreurs
   def process_data_safely(data):
       """Traitement de données avec gestion d'erreurs."""
       try:
           # Simulation d'un traitement qui peut échouer
           if len(data) == 0:
               raise CHNeoWaveError("Données vides")
           
           if not isinstance(data, (list, tuple)):
               raise TypeError("Type de données invalide")
           
           # Traitement normal
           result = sum(data) / len(data)
           logger.info(f"Traitement réussi: moyenne = {result}")
           return result
           
       except Exception as e:
           # Déléguer la gestion d'erreur
           action = error_handler.handle_exception(
               e, context={"function": "process_data_safely", "data_size": len(data)}
           )
           
           if action == "notify_user":
               print(f"Attention: {e}")
               return None
           elif action == "stop_execution":
               raise
           else:
               # Action par défaut
               logger.warning(f"Erreur ignorée: {e}")
               return None
   
   # Tests avec différents types de données
   test_cases = [
       [1, 2, 3, 4, 5],  # Cas normal
       [],               # Données vides (CHNeoWaveError)
       "invalid",        # Type invalide (TypeError)
       [10, 20, 30]      # Cas normal
   ]
   
   for i, test_data in enumerate(test_cases):
       print(f"\nTest {i+1}: {test_data}")
       result = process_data_safely(test_data)
       print(f"Résultat: {result}")
   
   # Générer un rapport d'erreurs
   error_report = error_handler.generate_error_report()
   print("\n=== RAPPORT D'ERREURS ===")
   print(f"Nombre total d'erreurs: {error_report['total_errors']}")
   print(f"Erreurs par type:")
   for error_type, count in error_report['errors_by_type'].items():
       print(f"  {error_type}: {count}")

Monitoring de Performance
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.utils.performance import (
       PerformanceProfiler, time_it, memory_profile
   )
   import numpy as np
   import time
   
   # Créer le profileur
   profiler = PerformanceProfiler()
   
   # Décorateur de mesure de temps
   @time_it
   def compute_fft(signal):
       """Calcul FFT avec mesure de performance."""
       return np.fft.fft(signal)
   
   # Décorateur de monitoring mémoire
   @memory_profile
   def generate_large_array(size):
       """Génération d'un grand tableau avec monitoring mémoire."""
       return np.random.randn(size)
   
   # Fonction à profiler
   def complex_computation(n_samples, n_iterations):
       """Calcul complexe pour test de performance."""
       results = []
       
       for i in range(n_iterations):
           # Génération de données
           data = np.random.randn(n_samples)
           
           # Traitement (FFT + filtrage)
           fft_result = np.fft.fft(data)
           filtered = np.fft.ifft(fft_result * np.exp(-np.arange(n_samples)/1000))
           
           # Statistiques
           stats = {
               'mean': np.mean(np.real(filtered)),
               'std': np.std(np.real(filtered)),
               'max': np.max(np.real(filtered))
           }
           results.append(stats)
           
           # Simulation d'une pause
           time.sleep(0.001)
       
       return results
   
   # Profiling avec contexte
   print("=== PROFILING DE PERFORMANCE ===")
   
   # Test 1: Calcul FFT simple
   print("\n1. Test FFT simple:")
   test_signal = np.random.randn(1024)
   fft_result = compute_fft(test_signal)
   
   # Test 2: Génération de grand tableau
   print("\n2. Test génération mémoire:")
   large_array = generate_large_array(1000000)
   
   # Test 3: Calcul complexe avec profiling complet
   print("\n3. Test calcul complexe:")
   
   profiler.start_profiling("complex_computation")
   
   # Exécution avec différentes tailles
   test_sizes = [1024, 2048, 4096]
   test_iterations = [10, 20, 30]
   
   performance_results = {}
   
   for size in test_sizes:
       for iterations in test_iterations:
           test_name = f"size_{size}_iter_{iterations}"
           
           print(f"  Exécution: {test_name}")
           
           start_time = time.time()
           results = complex_computation(size, iterations)
           end_time = time.time()
           
           performance_results[test_name] = {
               'execution_time': end_time - start_time,
               'samples_per_second': (size * iterations) / (end_time - start_time),
               'results_count': len(results)
           }
   
   profiler.stop_profiling("complex_computation")
   
   # Analyse des résultats
   print("\n=== RÉSULTATS DE PERFORMANCE ===")
   
   # Rapport du profileur
   performance_report = profiler.get_performance_report()
   print(f"\nRapport du profileur:")
   print(f"Temps total de profiling: {performance_report['total_time']:.3f}s")
   print(f"Pic d'utilisation mémoire: {performance_report['peak_memory']:.1f} MB")
   
   # Analyse des goulots d'étranglement
   bottlenecks = profiler.analyze_bottlenecks()
   if bottlenecks:
       print(f"\nGoulots d'étranglement détectés:")
       for bottleneck in bottlenecks:
           print(f"  - {bottleneck['function']}: {bottleneck['time_percent']:.1f}% du temps")
   
   # Suggestions d'optimisation
   optimizations = profiler.suggest_optimizations()
   if optimizations:
       print(f"\nSuggestions d'optimisation:")
       for suggestion in optimizations:
           print(f"  - {suggestion}")
   
   # Résultats détaillés par test
   print(f"\nRésultats détaillés:")
   for test_name, metrics in performance_results.items():
       print(f"  {test_name}:")
       print(f"    Temps d'exécution: {metrics['execution_time']:.3f}s")
       print(f"    Échantillons/sec: {metrics['samples_per_second']:.0f}")
       print(f"    Résultats générés: {metrics['results_count']}")
   
   # Analyse comparative
   print(f"\n=== ANALYSE COMPARATIVE ===")
   
   # Trouver le test le plus rapide et le plus lent
   fastest_test = min(performance_results.items(), 
                     key=lambda x: x[1]['execution_time'])
   slowest_test = max(performance_results.items(), 
                     key=lambda x: x[1]['execution_time'])
   
   print(f"Test le plus rapide: {fastest_test[0]} ({fastest_test[1]['execution_time']:.3f}s)")
   print(f"Test le plus lent: {slowest_test[0]} ({slowest_test[1]['execution_time']:.3f}s)")
   
   speedup_ratio = slowest_test[1]['execution_time'] / fastest_test[1]['execution_time']
   print(f"Ratio de performance: {speedup_ratio:.1f}x")
   
   # Efficacité par échantillon
   efficiency_analysis = {}
   for test_name, metrics in performance_results.items():
       size = int(test_name.split('_')[1])
       iterations = int(test_name.split('_')[3])
       total_samples = size * iterations
       
       efficiency = metrics['samples_per_second'] / total_samples
       efficiency_analysis[test_name] = efficiency
   
   most_efficient = max(efficiency_analysis.items(), key=lambda x: x[1])
   print(f"\nConfiguration la plus efficace: {most_efficient[0]}")
   print(f"Efficacité: {most_efficient[1]:.6f} (échantillons/sec)/échantillon")

Utilitaires de Validation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.utils.validation import (
       validate_numeric_range, validate_array_shape, validate_input,
       is_numeric, is_array_like, require_positive
   )
   import numpy as np
   
   # Décorateur de validation d'entrée
   @validate_input
   @require_positive('sampling_rate')
   def process_signal(signal, sampling_rate, window_size=1024):
       """
       Traitement de signal avec validation automatique.
       
       Parameters:
       -----------
       signal : array_like
           Signal à traiter
       sampling_rate : float
           Fréquence d'échantillonnage (doit être positive)
       window_size : int, optional
           Taille de fenêtre (défaut: 1024)
       """
       # Validation manuelle supplémentaire
       if not is_array_like(signal):
           raise ValueError("Le signal doit être un tableau")
       
       signal = np.asarray(signal)
       
       if not validate_array_shape(signal, min_length=window_size):
           raise ValueError(f"Signal trop court (minimum {window_size} échantillons)")
       
       if not validate_numeric_range(sampling_rate, min_val=1.0, max_val=100000.0):
           raise ValueError("Fréquence d'échantillonnage invalide (1-100000 Hz)")
       
       # Traitement du signal
       print(f"Traitement signal: {len(signal)} échantillons à {sampling_rate} Hz")
       
       # Exemple de traitement
       windowed_signal = signal[:len(signal)//window_size * window_size]
       windowed_signal = windowed_signal.reshape(-1, window_size)
       
       # Calcul de statistiques par fenêtre
       window_stats = {
           'mean': np.mean(windowed_signal, axis=1),
           'std': np.std(windowed_signal, axis=1),
           'max': np.max(windowed_signal, axis=1),
           'min': np.min(windowed_signal, axis=1)
       }
       
       return window_stats
   
   # Tests de validation
   print("=== TESTS DE VALIDATION ===")
   
   # Test 1: Données valides
   print("\n1. Test avec données valides:")
   try:
       valid_signal = np.random.randn(5000)
       valid_fs = 1000.0
       result = process_signal(valid_signal, valid_fs, window_size=512)
       print(f"   Succès: {len(result['mean'])} fenêtres traitées")
   except Exception as e:
       print(f"   Erreur: {e}")
   
   # Test 2: Fréquence d'échantillonnage négative
   print("\n2. Test avec fréquence négative:")
   try:
       result = process_signal(valid_signal, -1000.0)
   except Exception as e:
       print(f"   Erreur attendue: {e}")
   
   # Test 3: Signal trop court
   print("\n3. Test avec signal trop court:")
   try:
       short_signal = np.random.randn(100)
       result = process_signal(short_signal, 1000.0, window_size=512)
   except Exception as e:
       print(f"   Erreur attendue: {e}")
   
   # Test 4: Type de signal invalide
   print("\n4. Test avec type invalide:")
   try:
       invalid_signal = "not_a_signal"
       result = process_signal(invalid_signal, 1000.0)
   except Exception as e:
       print(f"   Erreur attendue: {e}")
   
   # Validation de structure de projet
   print("\n=== VALIDATION DE STRUCTURE ===")
   
   from hrneowave.utils.validation import validate_project_structure
   
   # Structure de projet attendue
   expected_structure = {
       'config': ['acquisition.yaml', 'analysis.yaml'],
       'data': ['raw', 'processed'],
       'results': ['reports', 'exports'],
       'logs': []
   }
   
   # Validation d'un répertoire de projet
   project_path = "./test_project"
   
   try:
       validation_result = validate_project_structure(project_path, expected_structure)
       
       if validation_result['is_valid']:
           print(f"Structure de projet valide: {project_path}")
       else:
           print(f"Structure de projet invalide:")
           for error in validation_result['errors']:
               print(f"  - {error}")
           
           print(f"Éléments manquants:")
           for missing in validation_result['missing_elements']:
               print(f"  - {missing}")
   
   except Exception as e:
       print(f"Erreur de validation: {e}")
   
   # Fonctions utilitaires de validation
   print("\n=== TESTS UTILITAIRES ===")
   
   test_values = [42, 3.14, "123", "abc", [1, 2, 3], np.array([1, 2, 3]), None]
   
   print("Validation de types:")
   for value in test_values:
       numeric = is_numeric(value)
       array_like = is_array_like(value)
       print(f"  {str(value):15s} -> numérique: {numeric:5s}, array: {array_like}")
   
   # Validation de plages
   print("\nValidation de plages:")
   test_ranges = [
       (50, 0, 100),    # Valide
       (-10, 0, 100),   # Trop petit
       (150, 0, 100),   # Trop grand
       (0, 0, 100),     # Limite inférieure
       (100, 0, 100),   # Limite supérieure
   ]
   
   for value, min_val, max_val in test_ranges:
       valid = validate_numeric_range(value, min_val, max_val)
       print(f"  {value:3d} dans [{min_val}, {max_val}] -> {valid}")