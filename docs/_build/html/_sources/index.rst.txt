CHNeoWave Documentation
=======================

.. image:: https://img.shields.io/badge/version-1.0.0-blue.svg
   :target: https://github.com/laboratoire-maritime/chneowave
   :alt: Version

.. image:: https://img.shields.io/badge/python-3.8+-green.svg
   :target: https://python.org
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE
   :alt: License

Bienvenue dans la documentation de **CHNeoWave**, le logiciel d'acquisition et d'analyse de données pour les laboratoires d'études maritimes en modèle réduit.

CHNeoWave est spécialement conçu pour les études en bassins et canaux méditerranéens, offrant des outils avancés d'acquisition, d'analyse spectrale et de génération de rapports scientifiques.

🎯 Fonctionnalités Principales
------------------------------

* **Acquisition de données** en temps réel avec support multi-capteurs
* **Analyse spectrale avancée** (FFT, Goda, statistiques)
* **Export scientifique HDF5** avec signature cryptographique
* **Génération de certificats PDF** de calibration
* **Interface utilisateur moderne** avec Material Design
* **Architecture modulaire** et extensible

📋 Table des Matières
---------------------

.. toctree::
   :maxdepth: 2
   :caption: Guide Utilisateur

   user_guide/installation
   user_guide/quickstart
   user_guide/workflows
   user_guide/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Documentation Technique

   technical/architecture
   technical/api_reference
   technical/data_formats
   technical/performance

.. toctree::
   :maxdepth: 2
   :caption: Développement

   development/contributing
   development/testing
   development/packaging
   development/changelog

.. toctree::
   :maxdepth: 3
   :caption: Référence API

   api/core
   api/gui
   api/hardware
   api/data
   api/utils

🚀 Démarrage Rapide
-------------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # Installation depuis PyPI (recommandé)
   pip install hrneowave

   # Ou installation depuis les sources
   git clone https://github.com/laboratoire-maritime/chneowave.git
   cd chneowave
   pip install -e .

Lancement
~~~~~~~~~

.. code-block:: bash

   # Lancement de l'interface graphique
   chneowave

   # Ou depuis Python
   python -m hrneowave.gui.main

Premier Projet
~~~~~~~~~~~~~~

1. **Créer un nouveau projet** depuis l'interface d'accueil
2. **Configurer l'acquisition** (fréquence, durée, capteurs)
3. **Lancer l'acquisition** et visualiser en temps réel
4. **Analyser les données** avec les outils intégrés
5. **Exporter les résultats** en HDF5, PDF, Excel

📊 Exemples d'Utilisation
-------------------------

Acquisition Programmée
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.core import AcquisitionManager
   from hrneowave.hardware import SimulatedAdapter

   # Configuration de l'acquisition
   manager = AcquisitionManager()
   adapter = SimulatedAdapter(channels=8, fs=1000)
   
   # Lancement de l'acquisition
   session = manager.start_acquisition(
       adapter=adapter,
       duration=60.0,
       project_path="./mon_projet"
   )
   
   # Attendre la fin
   session.wait_completion()
   print(f"Données sauvegardées: {session.output_file}")

Analyse Spectrale
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.analysis import SpectralAnalyzer
   import h5py

   # Charger les données
   with h5py.File("session_data.h5", "r") as f:
       data = f["data/raw_data"][:]
       fs = f["metadata"].attrs["sampling_frequency"]
   
   # Analyse spectrale
   analyzer = SpectralAnalyzer(window_size=1024)
   results = analyzer.analyze(data, fs)
   
   print(f"Fréquence de pic: {results.peak_frequency:.2f} Hz")
   print(f"Hauteur significative: {results.significant_height:.3f} m")

🔧 Configuration
----------------

CHNeoWave utilise un système de configuration flexible basé sur YAML :

.. code-block:: yaml

   # config.yaml
   acquisition:
     default_fs: 1000
     default_duration: 60.0
     buffer_size: 8192
   
   analysis:
     fft_window: "hann"
     overlap_ratio: 0.5
     frequency_bands: [0.05, 0.5, 2.0]
   
   export:
     default_formats: ["hdf5", "pdf", "excel"]
     compression: "gzip"

📈 Performance
--------------

* **Acquisition temps réel** : Jusqu'à 32 canaux à 10 kHz
* **Traitement parallèle** : Utilisation optimale des cœurs CPU
* **Mémoire optimisée** : Buffers circulaires pour les longues acquisitions
* **Export rapide** : Compression HDF5 avec threads dédiés

🆘 Support
----------

* **Documentation** : Cette documentation complète
* **Exemples** : Dossier ``examples/`` avec cas d'usage
* **Tests** : Suite de tests complète avec ``pytest``
* **Issues** : `GitHub Issues <https://github.com/laboratoire-maritime/chneowave/issues>`_

📄 Licence
----------

CHNeoWave est distribué sous licence MIT. Voir le fichier ``LICENSE`` pour plus de détails.

🏛️ À Propos
------------

CHNeoWave est développé par le **Laboratoire d'Études Maritimes** pour les besoins spécifiques des études en modèle réduit en Méditerranée.

**Version** : 1.0.0  
**Auteurs** : Équipe LEM  
**Contact** : lem@maritime.fr  

Indices et Tables
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`