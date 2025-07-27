Module GUI
==========

Le module ``gui`` contient l'interface utilisateur de CHNeoWave, basée sur PySide6/PyQt6 avec une architecture MVC moderne.

.. currentmodule:: hrneowave.gui

Architecture GUI
---------------

L'interface utilisateur suit le pattern MVC (Model-View-Controller) avec :

* **Views** : Composants d'interface utilisateur
* **Controllers** : Logique de contrôle et orchestration
* **Widgets** : Composants réutilisables
* **Layouts** : Gestionnaires de mise en page

Contrôleurs
-----------

.. automodule:: hrneowave.gui.controllers
   :members:
   :undoc-members:
   :show-inheritance:

Contrôleur Principal
~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.controllers.main_controller
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: MainController
   :members:
   :undoc-members:
   :show-inheritance:

   Le contrôleur principal orchestre l'ensemble de l'application :
   
   * Gestion du cycle de vie de l'application
   * Coordination entre les vues
   * Gestion des erreurs globales
   * Communication avec les backends

   .. automethod:: __init__
   .. automethod:: initialize_application
   .. automethod:: shutdown_application
   .. automethod:: switch_view
   .. automethod:: handle_error

Gestionnaire de Vues
~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.controllers.view_manager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ViewManager
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire centralisé des vues de l'application :
   
   * Navigation entre les vues
   * Gestion de la pile de vues
   * Transitions animées
   * État des vues

   .. automethod:: __init__
   .. automethod:: add_view
   .. automethod:: switch_to_view
   .. automethod:: get_current_view
   .. automethod:: get_view_history

Gestionnaire de Workflow
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.controllers.workflow_manager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: WorkflowManager
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire des workflows utilisateur :
   
   * Séquences d'actions guidées
   * Validation des étapes
   * Sauvegarde automatique
   * Récupération d'état

Vues Principales
---------------

.. automodule:: hrneowave.gui.views
   :members:
   :undoc-members:
   :show-inheritance:

Vue d'Accueil
~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.views.welcome_view
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: WelcomeView
   :members:
   :undoc-members:
   :show-inheritance:

   Vue d'accueil de l'application :
   
   * Création/ouverture de projets
   * Projets récents
   * Informations système
   * Liens rapides

Vue Tableau de Bord
~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.views.dashboard_view
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DashboardView
   :members:
   :undoc-members:
   :show-inheritance:

   Tableau de bord principal :
   
   * Vue d'ensemble du projet
   * Métriques en temps réel
   * Statut des composants
   * Actions rapides

Vue d'Acquisition
~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.views.acquisition_view
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AcquisitionView
   :members:
   :undoc-members:
   :show-inheritance:

   Interface d'acquisition de données :
   
   * Configuration des paramètres
   * Contrôle de l'acquisition
   * Visualisation temps réel
   * Monitoring des capteurs

Vue d'Analyse
~~~~~~~~~~~~

.. automodule:: hrneowave.gui.views.analysis
   :members:
   :undoc-members:
   :show-inheritance:

Vue d'Analyse V2
~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.views.analysis.analysis_view_v2
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AnalysisViewV2
   :members:
   :undoc-members:
   :show-inheritance:

   Interface d'analyse moderne :
   
   * Architecture modulaire en onglets
   * Analyse spectrale (FFT)
   * Analyse de Goda
   * Statistiques avancées
   * Génération de rapports

Contrôleur d'Analyse
~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.views.analysis.analysis_controller
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AnalysisController
   :members:
   :undoc-members:
   :show-inheritance:

   Orchestrateur des analyses :
   
   * Coordination des widgets d'analyse
   * Gestion des données de session
   * Exécution des analyses
   * Communication inter-widgets

Vue d'Export
~~~~~~~~~~~

.. automodule:: hrneowave.gui.views.export_view
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ExportView
   :members:
   :undoc-members:
   :show-inheritance:

   Interface d'exportation :
   
   * Sélection des formats
   * Configuration des exports
   * Prévisualisation
   * Progression des exports

Widgets Spécialisés
------------------

.. automodule:: hrneowave.gui.widgets
   :members:
   :undoc-members:
   :show-inheritance:

Widgets d'Analyse
~~~~~~~~~~~~~~~~

Widget d'Analyse Spectrale
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: hrneowave.gui.views.analysis.spectral_analysis_widget
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SpectralAnalysisWidget
   :members:
   :undoc-members:
   :show-inheritance:

   Widget d'analyse spectrale FFT :
   
   * Configuration des paramètres FFT
   * Visualisation du spectre
   * Détection des pics
   * Export des résultats

Widget d'Analyse Goda
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: hrneowave.gui.views.analysis.goda_analysis_widget
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: GodaAnalysisWidget
   :members:
   :undoc-members:
   :show-inheritance:

   Widget d'analyse de Goda :
   
   * Analyse des vagues par la méthode de Goda
   * Calcul des hauteurs significatives
   * Périodes caractéristiques
   * Statistiques de houle

Widget de Statistiques
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: hrneowave.gui.views.analysis.statistics_widget
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: StatisticsWidget
   :members:
   :undoc-members:
   :show-inheritance:

   Widget de statistiques avancées :
   
   * Statistiques descriptives
   * Distributions de probabilité
   * Tests statistiques
   * Visualisations graphiques

Widget de Rapport
^^^^^^^^^^^^^^^^

.. automodule:: hrneowave.gui.views.analysis.summary_report
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SummaryReportWidget
   :members:
   :undoc-members:
   :show-inheritance:

   Widget de génération de rapports :
   
   * Rapports techniques détaillés
   * Support multilingue
   * Export PDF et JSON
   * Templates personnalisables

Widgets Material Design
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.widgets.material_components
   :members:
   :undoc-members:
   :show-inheritance:

Composants Material
^^^^^^^^^^^^^^^^^^

.. autoclass:: MaterialButton
   :members:
   :show-inheritance:

   Bouton Material Design avec animations et états.

.. autoclass:: MaterialCard
   :members:
   :show-inheritance:

   Carte Material Design avec ombres et élévation.

.. autoclass:: MaterialInput
   :members:
   :show-inheritance:

   Champ de saisie Material Design avec labels flottants.

.. autoclass:: MaterialDialog
   :members:
   :show-inheritance:

   Dialogue Material Design avec animations.

Layouts et Mise en Page
----------------------

.. automodule:: hrneowave.gui.layouts
   :members:
   :undoc-members:
   :show-inheritance:

Layout Fibonacci
~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.layouts.fibonacci_grid_mixin
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: FibonacciGridMixin
   :members:
   :show-inheritance:

   Mixin pour layouts basés sur la suite de Fibonacci :
   
   * Proportions harmonieuses
   * Grille adaptative
   * Responsive design
   * Esthétique mathématique

Layout Phi
~~~~~~~~~

.. automodule:: hrneowave.gui.layouts.phi_layout
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: PhiLayout
   :members:
   :show-inheritance:

   Layout basé sur le nombre d'or (φ = 1.618) :
   
   * Proportions dorées
   * Équilibre visuel optimal
   * Adaptation automatique
   * Design harmonieux

Thèmes et Styles
---------------

.. automodule:: hrneowave.gui.themes
   :members:
   :undoc-members:
   :show-inheritance:

Gestionnaire de Thèmes
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.themes.theme_manager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ThemeManager
   :members:
   :undoc-members:
   :show-inheritance:

   Gestionnaire des thèmes visuels :
   
   * Thèmes prédéfinis (clair, sombre, maritime)
   * Personnalisation des couleurs
   * Application dynamique
   * Sauvegarde des préférences

Utilitaires GUI
--------------

.. automodule:: hrneowave.gui.utils
   :members:
   :undoc-members:
   :show-inheritance:

Bus de Signaux
~~~~~~~~~~~~~

.. automodule:: hrneowave.gui.utils.signal_bus
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: SignalBus
   :members:
   :undoc-members:
   :show-inheritance:

   Bus de communication centralisé :
   
   * Communication inter-composants
   * Découplage des modules
   * Événements globaux
   * Pattern Observer

Exemples d'Utilisation
---------------------

Création d'une Vue Personnalisée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
   from hrneowave.gui.layouts import FibonacciGridMixin
   from hrneowave.gui.widgets import MaterialButton, MaterialCard
   
   class MaVuePersonnalisee(QWidget, FibonacciGridMixin):
       def __init__(self, parent=None):
           super().__init__(parent)
           self.setup_ui()
       
       def setup_ui(self):
           layout = QVBoxLayout(self)
           
           # Carte Material Design
           card = MaterialCard("Ma Carte")
           card.setContent(QLabel("Contenu de la carte"))
           
           # Bouton Material Design
           button = MaterialButton("Action")
           button.clicked.connect(self.on_action)
           
           # Layout Fibonacci
           self.add_fibonacci_widget(card, 0, 0, 3, 2)
           self.add_fibonacci_widget(button, 3, 0, 2, 1)
       
       def on_action(self):
           print("Action déclenchée")

Intégration avec le Contrôleur Principal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.gui.controllers import MainController
   from hrneowave.gui.utils import get_signal_bus
   
   # Obtenir le contrôleur principal
   controller = MainController()
   
   # Obtenir le bus de signaux
   signal_bus = get_signal_bus()
   
   # Connecter aux événements globaux
   signal_bus.project_opened.connect(self.on_project_opened)
   signal_bus.acquisition_started.connect(self.on_acquisition_started)
   
   # Initialiser l'application
   controller.initialize_application()
   
   def on_project_opened(self, project_path):
       print(f"Projet ouvert: {project_path}")
   
   def on_acquisition_started(self, session_id):
       print(f"Acquisition démarrée: {session_id}")

Utilisation des Widgets d'Analyse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from hrneowave.gui.views.analysis import (
       AnalysisController,
       SpectralAnalysisWidget,
       GodaAnalysisWidget
   )
   import numpy as np
   
   # Créer le contrôleur d'analyse
   controller = AnalysisController()
   
   # Configurer les données de session
   session_data = {
       'raw_data': np.random.randn(1000, 4),
       'sampling_frequency': 1000.0,
       'duration': 1.0,
       'channels': [0, 1, 2, 3]
   }
   controller.set_session_data(session_data)
   
   # Créer les widgets d'analyse
   spectral_widget = SpectralAnalysisWidget()
   goda_widget = GodaAnalysisWidget()
   
   # Connecter au contrôleur
   controller.add_analysis_widget("spectral", spectral_widget)
   controller.add_analysis_widget("goda", goda_widget)
   
   # Lancer l'analyse spectrale
   controller.run_analysis("spectral", {
       'window_size': 1024,
       'window_type': 'hann',
       'overlap': 0.5
   })