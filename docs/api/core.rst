Module Core
===========

Le module ``core`` contient les composants fondamentaux de CHNeoWave, incluant la gestion des erreurs, le monitoring des performances, et les validateurs.

.. currentmodule:: hrneowave.core

Gestion des Erreurs
-------------------

.. automodule:: hrneowave.core.error_handler
   :members:
   :undoc-members:
   :show-inheritance:

Classes d'Exceptions
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CHNeoWaveError
   :members:
   :show-inheritance:

.. autoclass:: SystemError
   :members:
   :show-inheritance:

.. autoclass:: DataError
   :members:
   :show-inheritance:

.. autoclass:: HardwareError
   :members:
   :show-inheritance:

.. autoclass:: UserError
   :members:
   :show-inheritance:

Gestionnaire d'Erreurs
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ErrorHandler
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__
   .. automethod:: log_error
   .. automethod:: handle_critical_error
   .. automethod:: get_error_history
   .. automethod:: clear_history

Monitoring des Performances
---------------------------

.. automodule:: hrneowave.core.performance_monitor
   :members:
   :undoc-members:
   :show-inheritance:

Métriques de Performance
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PerformanceMetrics
   :members:
   :show-inheritance:

   Classe de données contenant les métriques système :
   
   * ``cpu_percent`` : Utilisation CPU (0-100%)
   * ``memory_percent`` : Utilisation mémoire (0-100%)
   * ``disk_usage`` : Espace disque utilisé (bytes)
   * ``thread_count`` : Nombre de threads actifs
   * ``response_time`` : Temps de réponse moyen (ms)

Moniteur de Performance
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PerformanceMonitor
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__
   .. automethod:: get_current_metrics
   .. automethod:: check_thresholds
   .. automethod:: start_monitoring
   .. automethod:: stop_monitoring
   .. automethod:: get_history

Validation des Données
----------------------

.. automodule:: hrneowave.core.validators
   :members:
   :undoc-members:
   :show-inheritance:

Validateurs de Projet
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ProjectValidator
   :members:
   :show-inheritance:

   .. automethod:: validate_project_name
   .. automethod:: validate_project_path
   .. automethod:: validate_project_settings

Validateurs d'Acquisition
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: AcquisitionValidator
   :members:
   :show-inheritance:

   .. automethod:: validate_sampling_frequency
   .. automethod:: validate_duration
   .. automethod:: validate_channels
   .. automethod:: validate_hardware_config

Validateurs de Données
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: DataValidator
   :members:
   :show-inheritance:

   .. automethod:: validate_signal_data
   .. automethod:: validate_file_format
   .. automethod:: validate_metadata

Gestion de Configuration
------------------------

.. automodule:: hrneowave.core.config_manager
   :members:
   :undoc-members:
   :show-inheritance:

Gestionnaire de Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ConfigManager
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__
   .. automethod:: load_config
   .. automethod:: save_config
   .. automethod:: get_setting
   .. automethod:: set_setting
   .. automethod:: reset_to_defaults

Utilitaires Core
---------------

.. automodule:: hrneowave.core.utils
   :members:
   :undoc-members:
   :show-inheritance:

Fonctions Utilitaires
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: get_error_handler

   Retourne l'instance singleton du gestionnaire d'erreurs.
   
   :return: Instance ErrorHandler
   :rtype: ErrorHandler

.. autofunction:: get_performance_monitor

   Retourne l'instance singleton du moniteur de performance.
   
   :return: Instance PerformanceMonitor
   :rtype: PerformanceMonitor

.. autofunction:: setup_logging

   Configure le système de logging pour CHNeoWave.
   
   :param level: Niveau de logging (DEBUG, INFO, WARNING, ERROR)
   :type level: str
   :param log_file: Chemin du fichier de log (optionnel)
   :type log_file: str or None

Décorateurs
~~~~~~~~~~~

.. autofunction:: handle_errors

   Décorateur pour la gestion automatique des erreurs.
   
   :param category: Catégorie d'erreur (SYSTEM, DATA, HARDWARE, USER)
   :type category: ErrorCategory
   :param reraise: Re-lever l'exception après logging
   :type reraise: bool
   
   Exemple d'utilisation :
   
   .. code-block:: python
   
      @handle_errors(category=ErrorCategory.SYSTEM)
      def ma_fonction_critique():
          # Code pouvant lever des exceptions
          pass

.. autofunction:: performance_monitor

   Décorateur pour le monitoring automatique des performances.
   
   :param track_memory: Surveiller l'utilisation mémoire
   :type track_memory: bool
   :param track_time: Surveiller le temps d'exécution
   :type track_time: bool
   
   Exemple d'utilisation :
   
   .. code-block:: python
   
      @performance_monitor(track_memory=True, track_time=True)
      def fonction_intensive():
          # Code nécessitant un monitoring
          pass

Exemples d'Utilisation
---------------------

Gestion d'Erreurs Basique
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.core import get_error_handler, CHNeoWaveError, ErrorCategory
   
   # Obtenir le gestionnaire d'erreurs
   error_handler = get_error_handler()
   
   try:
       # Code pouvant échouer
       result = operation_critique()
   except Exception as e:
       # Créer une erreur CHNeoWave
       error = CHNeoWaveError(
           message="Échec de l'opération critique",
           category=ErrorCategory.SYSTEM,
           context={"operation": "test", "user_id": 123}
       )
       
       # Logger l'erreur
       error_handler.log_error(error)
       
       # Gérer l'erreur critique si nécessaire
       if error.is_critical():
           error_handler.handle_critical_error(error)

Monitoring des Performances
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.core import get_performance_monitor
   
   # Obtenir le moniteur
   monitor = get_performance_monitor()
   
   # Démarrer le monitoring
   monitor.start_monitoring(interval=5.0)
   
   # Obtenir les métriques actuelles
   metrics = monitor.get_current_metrics()
   print(f"CPU: {metrics.cpu_percent}%")
   print(f"Mémoire: {metrics.memory_percent}%")
   
   # Vérifier les seuils
   alerts = monitor.check_thresholds(metrics)
   if alerts:
       print(f"Alertes: {alerts}")
   
   # Arrêter le monitoring
   monitor.stop_monitoring()

Validation de Données
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.core.validators import AcquisitionValidator, DataValidator
   
   # Validation des paramètres d'acquisition
   acq_validator = AcquisitionValidator()
   
   try:
       acq_validator.validate_sampling_frequency(1000.0)
       acq_validator.validate_duration(60.0)
       acq_validator.validate_channels([0, 1, 2, 3])
       print("Paramètres d'acquisition valides")
   except ValueError as e:
       print(f"Erreur de validation: {e}")
   
   # Validation des données
   data_validator = DataValidator()
   
   import numpy as np
   signal_data = np.random.randn(1000, 4)  # 1000 échantillons, 4 canaux
   
   try:
       data_validator.validate_signal_data(signal_data)
       print("Données de signal valides")
   except ValueError as e:
       print(f"Données invalides: {e}")