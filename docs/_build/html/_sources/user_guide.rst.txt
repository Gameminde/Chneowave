Guide Utilisateur CHNeoWave
============================

Bienvenue dans CHNeoWave, le logiciel d'acquisition et d'analyse de données de houle pour laboratoires d'études maritimes en modèle réduit.

.. note::
   Ce guide couvre l'utilisation complète de CHNeoWave v1.0.0. Pour les aspects techniques et de développement, consultez la :doc:`technical_guide`.

Présentation Générale
--------------------

CHNeoWave est un logiciel spécialisé conçu pour :

* **Acquisition de données** : Capture en temps réel depuis des capteurs de houle
* **Analyse spectrale** : Analyse fréquentielle avancée des signaux
* **Analyse de houle** : Méthodes Goda et analyse directionnelle
* **Visualisation** : Graphiques interactifs et rapports détaillés
* **Export** : Formats multiples pour intégration avec d'autres outils

Caractéristiques Principales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Interface utilisateur moderne et intuitive
* Architecture modulaire et extensible
* Performance optimisée pour les gros volumes de données
* Validation automatique des données
* Système de monitoring intégré
* Documentation complète et exemples

Configuration Système Requise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Minimum :**

* Windows 10 ou supérieur
* Python 3.8+
* 4 GB RAM
* 1 GB espace disque libre
* Port série disponible (pour acquisition)

**Recommandé :**

* Windows 11
* Python 3.10+
* 8 GB RAM ou plus
* SSD avec 5 GB espace libre
* Processeur multi-cœurs
* Écran haute résolution (1920x1080 minimum)

Installation
-----------

Installation Standard
~~~~~~~~~~~~~~~~~~~~

1. **Téléchargement**

   Téléchargez la dernière version depuis le dépôt officiel :
   
   .. code-block:: bash
   
      git clone https://github.com/your-org/chneowave.git
      cd chneowave

2. **Installation des dépendances**

   .. code-block:: bash
   
      pip install -r requirements.txt

3. **Configuration initiale**

   .. code-block:: bash
   
      python -m hrneowave.setup --init

4. **Vérification de l'installation**

   .. code-block:: bash
   
      python -m hrneowave.tests.smoke_test

Installation pour Développeurs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour contribuer au développement :

.. code-block:: bash

   # Installation en mode développement
   pip install -e .
   pip install -r requirements-dev.txt
   
   # Configuration des hooks pre-commit
   pre-commit install
   
   # Exécution des tests complets
   pytest tests/ --cov=hrneowave

Installation Portable
~~~~~~~~~~~~~~~~~~~~

Pour une installation sans Python :

1. Téléchargez l'exécutable portable depuis les releases
2. Décompressez l'archive dans le répertoire de votre choix
3. Lancez ``CHNeoWave.exe``

Premier Démarrage
----------------

Lancement de l'Application
~~~~~~~~~~~~~~~~~~~~~~~~~

**Depuis le code source :**

.. code-block:: bash

   python -m hrneowave

**Depuis l'installation :**

.. code-block:: bash

   chneowave

**Mode développement :**

.. code-block:: bash

   python -m hrneowave --debug --verbose

Configuration Initiale
~~~~~~~~~~~~~~~~~~~~~

Au premier démarrage, l'assistant de configuration vous guidera :

1. **Sélection du répertoire de travail**
   
   Choisissez un répertoire pour stocker vos projets et données.

2. **Configuration des capteurs**
   
   * Type de capteur (résistif, capacitif, ultrason)
   * Port série et paramètres de communication
   * Calibration et facteurs de conversion

3. **Paramètres d'acquisition**
   
   * Fréquence d'échantillonnage par défaut
   * Durée d'acquisition standard
   * Filtres et pré-traitements

4. **Préférences d'affichage**
   
   * Thème de l'interface
   * Unités de mesure
   * Format des graphiques

Interface Utilisateur
--------------------

Vue d'Ensemble
~~~~~~~~~~~~~

L'interface de CHNeoWave est organisée en plusieurs zones principales :

* **Barre de menu** : Accès aux fonctions principales
* **Barre d'outils** : Raccourcis vers les actions courantes
* **Panneau de navigation** : Arborescence des projets et fichiers
* **Zone de travail** : Affichage des données et graphiques
* **Panneau de propriétés** : Paramètres et informations contextuelles
* **Barre de statut** : Informations système et progression

Menu Principal
~~~~~~~~~~~~~

**Fichier**

* Nouveau projet
* Ouvrir projet
* Sauvegarder / Sauvegarder sous
* Importer données
* Exporter résultats
* Préférences
* Quitter

**Acquisition**

* Démarrer acquisition
* Arrêter acquisition
* Configuration capteurs
* Test de connexion
* Calibration

**Analyse**

* Analyse spectrale
* Analyse de houle
* Analyse statistique
* Analyse de tendances
* Comparaison de datasets

**Affichage**

* Graphiques temporels
* Spectres de fréquence
* Diagrammes polaires
* Cartes de densité
* Rapports

**Outils**

* Calculatrice de houle
* Convertisseur d'unités
* Générateur de signaux test
* Diagnostic système
* Mise à jour

**Aide**

* Guide utilisateur
* Tutoriels
* Exemples
* À propos

Barres d'Outils
~~~~~~~~~~~~~~

**Barre principale**

* |new| Nouveau projet
* |open| Ouvrir projet
* |save| Sauvegarder
* |acquire| Démarrer acquisition
* |stop| Arrêter acquisition
* |analyze| Lancer analyse
* |export| Exporter résultats

**Barre d'affichage**

* |zoom_in| Zoom avant
* |zoom_out| Zoom arrière
* |zoom_fit| Ajuster à la fenêtre
* |grid| Afficher/masquer la grille
* |legend| Afficher/masquer la légende
* |fullscreen| Mode plein écran

.. |new| image:: _static/icons/new.png
   :width: 16px
.. |open| image:: _static/icons/open.png
   :width: 16px
.. |save| image:: _static/icons/save.png
   :width: 16px
.. |acquire| image:: _static/icons/acquire.png
   :width: 16px
.. |stop| image:: _static/icons/stop.png
   :width: 16px
.. |analyze| image:: _static/icons/analyze.png
   :width: 16px
.. |export| image:: _static/icons/export.png
   :width: 16px
.. |zoom_in| image:: _static/icons/zoom_in.png
   :width: 16px
.. |zoom_out| image:: _static/icons/zoom_out.png
   :width: 16px
.. |zoom_fit| image:: _static/icons/zoom_fit.png
   :width: 16px
.. |grid| image:: _static/icons/grid.png
   :width: 16px
.. |legend| image:: _static/icons/legend.png
   :width: 16px
.. |fullscreen| image:: _static/icons/fullscreen.png
   :width: 16px

Gestion des Projets
------------------

Création d'un Nouveau Projet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Menu Fichier > Nouveau projet** ou ``Ctrl+N``

2. **Assistant de création :**
   
   * **Nom du projet** : Nom descriptif
   * **Localisation** : Répertoire de stockage
   * **Type d'étude** : Houle régulière, irrégulière, multidirectionnelle
   * **Configuration** : Bassin, canal, mer ouverte
   * **Capteurs** : Sélection et configuration

3. **Structure créée automatiquement :**
   
   .. code-block:: text
   
      MonProjet/
      ├── config/
      │   ├── acquisition.yaml
      │   ├── analysis.yaml
      │   └── sensors.yaml
      ├── data/
      │   ├── raw/
      │   └── processed/
      ├── results/
      │   ├── reports/
      │   └── exports/
      └── logs/

Ouverture d'un Projet Existant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Menu Fichier > Ouvrir projet** ou ``Ctrl+O``
* Sélectionner le fichier ``.chnw`` du projet
* Le projet s'ouvre avec tous ses paramètres et données

Gestion des Fichiers
~~~~~~~~~~~~~~~~~~~

**Types de fichiers supportés :**

* ``.chnw`` : Fichier projet CHNeoWave
* ``.h5`` : Données HDF5 (format principal)
* ``.csv`` : Données tabulaires
* ``.txt`` : Données texte
* ``.mat`` : Fichiers MATLAB
* ``.yaml`` : Fichiers de configuration

**Opérations sur fichiers :**

* Glisser-déposer pour importer
* Clic droit pour menu contextuel
* Prévisualisation dans le panneau de propriétés
* Recherche et filtrage

Acquisition de Données
---------------------

Configuration des Capteurs
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Types de capteurs supportés :**

* **Capteurs résistifs** : Mesure par variation de résistance
* **Capteurs capacitifs** : Mesure par variation de capacité
* **Capteurs ultrasoniques** : Mesure par temps de vol
* **Capteurs optiques** : Mesure par réflexion laser

**Configuration série :**

.. code-block:: yaml

   # config/sensors.yaml
   sensors:
     primary:
       type: "resistive"
       port: "COM3"
       baudrate: 115200
       data_bits: 8
       parity: "none"
       stop_bits: 1
       timeout: 1.0
       
     calibration:
       offset: 0.0
       scale: 1.0
       units: "mm"
       range: [-100, 100]

Paramètres d'Acquisition
~~~~~~~~~~~~~~~~~~~~~~~

**Configuration de base :**

* **Fréquence d'échantillonnage** : 100 Hz à 10 kHz
* **Durée d'acquisition** : 10 secondes à plusieurs heures
* **Nombre de canaux** : 1 à 16 capteurs simultanés
* **Format de stockage** : HDF5 avec compression

**Paramètres avancés :**

* **Filtrage temps réel** : Passe-bas, passe-haut, passe-bande
* **Déclenchement** : Manuel, automatique, conditionnel
* **Buffer circulaire** : Acquisition continue avec sauvegarde
* **Validation** : Contrôle de plausibilité en temps réel

Procédure d'Acquisition
~~~~~~~~~~~~~~~~~~~~~~

1. **Préparation**
   
   * Vérifier la connexion des capteurs
   * Tester la communication série
   * Calibrer si nécessaire
   * Configurer les paramètres

2. **Démarrage**
   
   * Cliquer sur |acquire| ou ``F5``
   * Surveiller l'affichage temps réel
   * Vérifier la qualité du signal
   * Ajuster si nécessaire

3. **Surveillance**
   
   * **Indicateurs de qualité** : SNR, dérive, saturation
   * **Statistiques temps réel** : Min, max, moyenne, écart-type
   * **Spectrogramme** : Évolution fréquentielle
   * **Alertes** : Dépassements de seuils

4. **Arrêt et sauvegarde**
   
   * Arrêt manuel ou automatique
   * Sauvegarde automatique en HDF5
   * Génération de métadonnées
   * Validation post-acquisition

Acquisition Programmée
~~~~~~~~~~~~~~~~~~~~~

**Planification d'acquisitions :**

.. code-block:: python

   # Exemple de script d'acquisition programmée
   from hrneowave.data.acquisition import AcquisitionManager
   from datetime import datetime, timedelta
   
   # Configuration
   config = {
       'duration': 300,  # 5 minutes
       'sampling_rate': 1000,  # 1 kHz
       'channels': ['wave_1', 'wave_2'],
       'trigger': 'time',
       'schedule': {
           'start_time': '08:00',
           'interval': timedelta(hours=1),
           'repeat': 24  # 24 acquisitions
       }
   }
   
   # Démarrage
   manager = AcquisitionManager()
   manager.schedule_acquisition(config)

Analyse des Données
------------------

Analyse Spectrale
~~~~~~~~~~~~~~~~

**Transformée de Fourier (FFT) :**

* **Paramètres** :
  
  * Taille de fenêtre : 512 à 8192 points
  * Recouvrement : 0% à 75%
  * Fenêtrage : Hanning, Hamming, Blackman
  * Moyennage : Linéaire ou logarithmique

* **Résultats** :
  
  * Spectre d'amplitude
  * Densité spectrale de puissance (PSD)
  * Cohérence entre canaux
  * Phase relative

**Spectrogramme :**

* Évolution temporelle du spectre
* Résolution temps-fréquence ajustable
* Détection d'événements transitoires
* Analyse de stationnarité

**Exemple d'utilisation :**

.. code-block:: python

   from hrneowave.analysis.spectral import SpectralAnalyzer
   
   # Chargement des données
   analyzer = SpectralAnalyzer()
   data = analyzer.load_data('data/raw/acquisition_001.h5')
   
   # Configuration de l'analyse
   config = {
       'window_size': 2048,
       'overlap': 0.5,
       'window_type': 'hanning',
       'detrend': True
   }
   
   # Calcul du spectre
   spectrum = analyzer.compute_spectrum(data, **config)
   
   # Affichage
   analyzer.plot_spectrum(spectrum, log_scale=True)

Analyse de Houle
~~~~~~~~~~~~~~~

**Méthode de Goda :**

Analyse statistique des vagues individuelles :

* **Détection des vagues** : Algorithme de passage par zéro
* **Paramètres calculés** :
  
  * Hauteur significative (H₁/₃, Hs)
  * Hauteur moyenne (H̄)
  * Hauteur maximale (Hmax)
  * Période moyenne (T̄)
  * Période de pic (Tp)
  * Période significative (T₁/₃)

* **Distributions statistiques** :
  
  * Distribution de Rayleigh
  * Distribution de Weibull
  * Ajustement et tests de conformité

**Analyse directionnelle :**

Pour les mesures multi-capteurs :

* **Méthodes** :
  
  * Maximum de vraisemblance (MLM)
  * Maximum d'entropie (MEM)
  * Transformée de Fourier directionnelle

* **Paramètres directionnels** :
  
  * Direction moyenne
  * Étalement directionnel
  * Fonction de répartition directionnelle

**Exemple d'analyse Goda :**

.. code-block:: python

   from hrneowave.analysis.wave import GodaAnalyzer
   
   # Initialisation
   goda = GodaAnalyzer()
   
   # Chargement des données
   wave_data = goda.load_wave_data('data/processed/waves_001.h5')
   
   # Analyse
   results = goda.analyze(wave_data, method='zero_crossing')
   
   # Résultats
   print(f"Hauteur significative: {results['Hs']:.2f} m")
   print(f"Période de pic: {results['Tp']:.2f} s")
   print(f"Nombre de vagues: {results['N_waves']}")
   
   # Distributions
   goda.plot_height_distribution(results)
   goda.plot_period_distribution(results)

Analyse Statistique
~~~~~~~~~~~~~~~~~~

**Statistiques descriptives :**

* Moments statistiques (moyenne, variance, asymétrie, aplatissement)
* Quantiles et percentiles
* Valeurs extrêmes
* Tests de normalité

**Analyse de corrélation :**

* Corrélation croisée
* Cohérence spectrale
* Analyse de phase
* Délais de propagation

**Détection d'anomalies :**

* Détection de valeurs aberrantes
* Analyse de dérive
* Contrôle de qualité automatique
* Signalement d'événements

Visualisation
------------

Graphiques Temporels
~~~~~~~~~~~~~~~~~~~

**Types de graphiques :**

* **Série temporelle simple** : Un signal vs temps
* **Séries multiples** : Plusieurs signaux synchronisés
* **Graphique empilé** : Signaux superposés avec décalage
* **Vue panoramique** : Navigation dans de longues séries

**Fonctionnalités interactives :**

* Zoom et panoramique
* Curseurs de mesure
* Sélection de régions
* Annotations
* Export haute résolution

**Personnalisation :**

* Couleurs et styles de ligne
* Échelles linéaires/logarithmiques
* Grilles et axes
* Légendes et titres
* Thèmes prédéfinis

Graphiques Fréquentiels
~~~~~~~~~~~~~~~~~~~~~~

**Spectres de puissance :**

* Affichage linéaire ou logarithmique
* Échelles dB ou linéaires
* Lissage et moyennage
* Bandes de fréquence
* Pics automatiques

**Spectrogrammes :**

* Cartes temps-fréquence
* Échelles de couleur ajustables
* Résolution configurable
* Animation temporelle
* Export vidéo

**Diagrammes polaires :**

* Représentation directionnelle
* Rose des vents
* Densité de probabilité
* Superposition de données
* Statistiques sectorielles

Rapports et Export
-----------------

Génération de Rapports
~~~~~~~~~~~~~~~~~~~~~

**Types de rapports :**

* **Rapport d'acquisition** : Paramètres et qualité des données
* **Rapport d'analyse** : Résultats statistiques et spectraux
* **Rapport de synthèse** : Vue d'ensemble multi-sessions
* **Rapport personnalisé** : Template utilisateur

**Contenu automatique :**

* Métadonnées de session
* Graphiques et tableaux
* Statistiques principales
* Conclusions et recommandations
* Annexes techniques

**Formats de sortie :**

* PDF haute qualité
* HTML interactif
* Word/OpenDocument
* LaTeX pour publication

Export de Données
~~~~~~~~~~~~~~~~

**Formats supportés :**

* **HDF5** : Format natif avec métadonnées
* **CSV** : Données tabulaires
* **MATLAB** : Fichiers .mat
* **NumPy** : Arrays binaires
* **JSON** : Métadonnées et configuration

**Options d'export :**

* Sélection de canaux
* Plages temporelles
* Résolution et filtrage
* Compression
* Validation d'intégrité

**Export graphiques :**

* PNG, JPEG : Images bitmap
* SVG, PDF : Graphiques vectoriels
* EPS : Publication scientifique
* Résolutions configurables
* Transparence et qualité

**Exemple d'export :**

.. code-block:: python

   from hrneowave.data.export import DataExporter
   
   # Configuration d'export
   exporter = DataExporter()
   
   # Export CSV
   exporter.to_csv(
       data='results/analysis_001.h5',
       output='exports/data_001.csv',
       channels=['wave_1', 'wave_2'],
       time_range=(0, 300),
       decimation=10
   )
   
   # Export MATLAB
   exporter.to_matlab(
       data='results/analysis_001.h5',
       output='exports/data_001.mat',
       include_metadata=True
   )
   
   # Export graphique
   exporter.export_plot(
       figure=current_figure,
       filename='exports/spectrum_001.pdf',
       dpi=300,
       format='pdf'
   )

Configuration Avancée
--------------------

Fichiers de Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

**Structure des fichiers YAML :**

.. code-block:: yaml

   # config/acquisition.yaml
   acquisition:
     sampling_rate: 1000.0
     duration: 300.0
     buffer_size: 8192
     
     filters:
       enable: true
       lowpass:
         cutoff: 100.0
         order: 4
       highpass:
         cutoff: 0.1
         order: 2
     
     validation:
       enable: true
       range_check: true
       drift_detection: true
       spike_removal: true
   
   # config/analysis.yaml
   analysis:
     spectral:
       window_size: 2048
       overlap: 0.5
       window_type: "hanning"
       detrend: "linear"
       
     wave:
       method: "zero_crossing"
       min_height: 0.01
       min_period: 0.5
       max_period: 20.0
   
   # config/display.yaml
   display:
     theme: "dark"
     font_size: 12
     line_width: 1.5
     colors:
       primary: "#2E86AB"
       secondary: "#A23B72"
       background: "#F18F01"

Personnalisation de l'Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Thèmes disponibles :**

* **Clair** : Interface claire pour environnements lumineux
* **Sombre** : Interface sombre pour réduire la fatigue oculaire
* **Contraste élevé** : Accessibilité pour malvoyants
* **Personnalisé** : Couleurs et polices configurables

**Configuration des raccourcis :**

.. code-block:: yaml

   # config/shortcuts.yaml
   shortcuts:
     file:
       new_project: "Ctrl+N"
       open_project: "Ctrl+O"
       save_project: "Ctrl+S"
       export_data: "Ctrl+E"
     
     acquisition:
       start: "F5"
       stop: "F6"
       pause: "F7"
       calibrate: "F8"
     
     analysis:
       spectral: "Ctrl+1"
       wave: "Ctrl+2"
       statistics: "Ctrl+3"
       export_results: "Ctrl+Shift+E"

**Layouts personnalisés :**

* Disposition des panneaux
* Taille des fenêtres
* Barres d'outils visibles
* Espaces de travail sauvegardés

Plugins et Extensions
~~~~~~~~~~~~~~~~~~~~

**Architecture de plugins :**

.. code-block:: python

   # plugins/custom_analyzer.py
   from hrneowave.core.plugin import AnalysisPlugin
   
   class CustomAnalyzer(AnalysisPlugin):
       """Plugin d'analyse personnalisé."""
       
       name = "Analyse Personnalisée"
       version = "1.0.0"
       description = "Analyse spécialisée pour bassin méditerranéen"
       
       def analyze(self, data, **kwargs):
           """Méthode d'analyse principale."""
           # Implémentation personnalisée
           results = self.custom_processing(data)
           return results
       
       def get_parameters(self):
           """Paramètres configurables."""
           return {
               'threshold': {'type': 'float', 'default': 0.1},
               'method': {'type': 'choice', 'options': ['A', 'B', 'C']}
           }

**Installation de plugins :**

.. code-block:: bash

   # Installation depuis un fichier
   chneowave plugin install custom_analyzer.py
   
   # Installation depuis un dépôt
   chneowave plugin install git+https://github.com/user/plugin.git
   
   # Liste des plugins installés
   chneowave plugin list
   
   # Activation/désactivation
   chneowave plugin enable custom_analyzer
   chneowave plugin disable custom_analyzer

Dépannage
---------

Problèmes Courants
~~~~~~~~~~~~~~~~~

**Problèmes de connexion série :**

* **Symptôme** : "Port série non disponible"
* **Solutions** :
  
  * Vérifier que le port n'est pas utilisé par une autre application
  * Contrôler les permissions d'accès
  * Tester avec un terminal série externe
  * Redémarrer le service série Windows

* **Diagnostic** :
  
  .. code-block:: bash
  
     # Test de connexion
     chneowave diagnostic serial --port COM3
     
     # Liste des ports disponibles
     chneowave diagnostic ports

**Problèmes de performance :**

* **Symptôme** : Interface lente ou blocages
* **Solutions** :
  
  * Réduire la fréquence d'échantillonnage
  * Augmenter la taille du buffer
  * Fermer les applications non nécessaires
  * Vérifier l'espace disque disponible

* **Monitoring** :
  
  .. code-block:: python
  
     from hrneowave.utils.performance import PerformanceMonitor
     
     # Activation du monitoring
     monitor = PerformanceMonitor()
     monitor.start()
     
     # Rapport de performance
     report = monitor.get_report()
     print(f"CPU: {report['cpu_usage']:.1f}%")
     print(f"Mémoire: {report['memory_usage']:.1f} MB")

**Problèmes de données :**

* **Symptôme** : Données corrompues ou incohérentes
* **Solutions** :
  
  * Vérifier la calibration des capteurs
  * Contrôler l'intégrité des fichiers
  * Valider les paramètres d'acquisition
  * Nettoyer les données aberrantes

* **Validation** :
  
  .. code-block:: python
  
     from hrneowave.data.validation import DataValidator
     
     validator = DataValidator()
     result = validator.validate_file('data/raw/acquisition_001.h5')
     
     if not result.is_valid:
         print("Erreurs détectées:")
         for error in result.errors:
             print(f"  - {error}")

Logs et Diagnostic
~~~~~~~~~~~~~~~~~

**Niveaux de log :**

* **DEBUG** : Informations détaillées pour le développement
* **INFO** : Informations générales sur le fonctionnement
* **WARNING** : Avertissements non critiques
* **ERROR** : Erreurs nécessitant une attention
* **CRITICAL** : Erreurs critiques bloquantes

**Configuration des logs :**

.. code-block:: yaml

   # config/logging.yaml
   logging:
     level: "INFO"
     format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
     
     handlers:
       console:
         enable: true
         level: "INFO"
       
       file:
         enable: true
         level: "DEBUG"
         filename: "logs/chneowave.log"
         max_size: "10MB"
         backup_count: 5

**Outils de diagnostic :**

.. code-block:: bash

   # Diagnostic complet du système
   chneowave diagnostic system
   
   # Test des dépendances
   chneowave diagnostic dependencies
   
   # Vérification de la configuration
   chneowave diagnostic config
   
   # Test de performance
   chneowave diagnostic performance

Support et Ressources
--------------------

Documentation
~~~~~~~~~~~~

* **Guide utilisateur** : Ce document
* **Documentation technique** : :doc:`technical_guide`
* **Référence API** : :doc:`api/index`
* **Tutoriels** : :doc:`tutorials/index`
* **FAQ** : :doc:`faq`

Communauté
~~~~~~~~~

* **Forum utilisateurs** : https://forum.chneowave.org
* **Issues GitHub** : https://github.com/your-org/chneowave/issues
* **Discussions** : https://github.com/your-org/chneowave/discussions
* **Wiki** : https://github.com/your-org/chneowave/wiki

Support Technique
~~~~~~~~~~~~~~~~

* **Email** : support@chneowave.org
* **Documentation** : https://docs.chneowave.org
* **Tickets** : https://support.chneowave.org
* **Téléphone** : +33 (0)X XX XX XX XX

Contribution
~~~~~~~~~~~

* **Guide de contribution** : :doc:`contributing`
* **Standards de code** : :doc:`coding_standards`
* **Tests** : :doc:`testing_guide`
* **Roadmap** : :doc:`roadmap`

Licence et Crédits
-----------------

Licence
~~~~~~

CHNeoWave est distribué sous licence MIT. Voir le fichier ``LICENSE`` pour les détails complets.

Crédits
~~~~~~

**Équipe de développement :**

* **Architecte principal** : [Nom]
* **Développeurs** : [Noms]
* **Testeurs** : [Noms]
* **Documentation** : [Noms]

**Remerciements :**

* Laboratoire d'études maritimes
* Communauté scientifique
* Contributeurs open source
* Utilisateurs beta-testeurs

**Bibliothèques utilisées :**

* NumPy, SciPy : Calcul scientifique
* PySide6 : Interface graphique
* PyQtGraph : Visualisation
* HDF5 : Stockage de données
* YAML : Configuration
* Pytest : Tests

Versions et Changelog
~~~~~~~~~~~~~~~~~~~~

**Version 1.0.0** (Date de release)

* Interface utilisateur complète
* Acquisition multi-capteurs
* Analyses spectrale et de houle
* Export multi-formats
* Documentation complète
* Tests de validation

**Versions précédentes :**

* v0.9.x : Versions beta
* v0.8.x : Versions alpha
* v0.7.x : Prototypes

Pour l'historique complet, voir ``CHANGELOG.md``.

Index et Glossaire
-----------------

Glossaire
~~~~~~~~

**Acquisition**
   Processus de capture de données depuis les capteurs

**Analyse spectrale**
   Décomposition d'un signal en ses composantes fréquentielles

**Bassin**
   Installation expérimentale pour études en modèle réduit

**Calibration**
   Ajustement des paramètres de mesure pour assurer la précision

**Canal**
   Installation linéaire pour études de propagation de houle

**Capteur**
   Dispositif de mesure de la hauteur d'eau

**FFT**
   Transformée de Fourier Rapide (Fast Fourier Transform)

**Goda**
   Méthode d'analyse statistique des vagues (Yoshimi Goda)

**HDF5**
   Format de fichier hiérarchique pour données scientifiques

**Houle**
   Ondulation de la surface de l'eau

**Modèle réduit**
   Reproduction à échelle réduite d'un phénomène maritime

**PSD**
   Densité Spectrale de Puissance (Power Spectral Density)

**Spectrogramme**
   Représentation temps-fréquence d'un signal

**YAML**
   Format de sérialisation de données lisible par l'homme

Index
~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. note::
   Ce guide utilisateur est en constante évolution. N'hésitez pas à nous faire part de vos suggestions d'amélioration via les canaux de support.