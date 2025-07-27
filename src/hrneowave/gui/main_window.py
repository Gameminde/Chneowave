#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale pour CHNeoWave
Gestion des signaux de projet et coordination des vues
"""

import logging
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal, Slot, QTimer

logger = logging.getLogger(__name__)
from hrneowave.core.signal_bus import get_error_bus, ErrorLevel
from .view_manager import ViewManager
from .widgets.main_sidebar import MainSidebar
from .components.breadcrumbs import BreadcrumbsWidget, WorkflowStep
from .preferences import PreferencesDialog, get_user_preferences
from .components.help_system import HelpPanel, get_help_system, install_help_on_widget
from .components.status_indicators import SystemStatusWidget, StatusLevel
from .components.notification_system import get_notification_center, show_success, show_error, show_info

# Import des vues v2 et configurations
from .views import (
    DashboardViewMaritime,
    WelcomeView,
    get_calibration_view,
    get_acquisition_view,
    get_analysis_view,
    get_export_view,
    get_settings_view,
    VIEWS_CONFIG,
    NAVIGATION_ORDER
)

class MainWindow(QMainWindow):
    """Fenêtre principale de l'application CHNeoWave"""
    
    projectCreated = Signal()          # nouveau signal
    
    def __init__(self, config=None, parent=None):
        # Import des classes Qt seulement quand nécessaire
        from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget
        from PySide6.QtCore import Qt
        
        super().__init__(parent)
        self.setWindowTitle("CHNeoWave")
        self.setMinimumSize(1024, 768)
        
        # Configuration
        self.config = config or {}
        
        # Préférences utilisateur
        self.user_preferences = get_user_preferences()
        
        # Métadonnées du projet
        self.project_meta = {}
        
        # État de l'application
        self.is_acquiring = False
        self.acquisition_controller = None
        self.analysis_controller = None
        self.project_controller = None
        
        # Construction de l'interface
        logger.info("Début de la construction de l'interface...")
        self._build_ui()
        logger.info("Interface construite avec succès")
        
        logger.info("Configuration des connexions...")
        self._setup_connections()
        logger.info("Connexions configurées avec succès")
        
        # Configurer les nouveaux composants UX
        logger.info("Configuration des indicateurs de statut...")
        self._setup_status_indicators()
        logger.info("Indicateurs de statut configurés avec succès")
        
        logger.info("Installation de l'aide contextuelle...")
        self._install_contextual_help()
        logger.info("Aide contextuelle installée avec succès")
        
        logger.info("Interface utilisateur v2 chargée avec succès")

        # Connecter la barre de navigation
        self.sidebar.navigation_requested.connect(self._on_navigation_requested)
    
    @Slot(str)
    def _on_navigation_requested(self, view_name):
        """Change la vue affichée en réponse à la barre de navigation latérale."""
        if view_name in VIEWS_CONFIG:
            self.view_manager.switch_to_view(view_name)
            logger.info(f"Navigation vers la vue: '{view_name}'")
            self._update_breadcrumbs_for_view(view_name)
        else:
            logger.warning(f"Tentative de naviguer vers une vue inconnue: '{view_name}'")
    
    def _build_ui(self):
        """Construit l'interface utilisateur principale avec une barre latérale et breadcrumbs."""
        from PySide6.QtWidgets import QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget, QSplitter
        from PySide6.QtCore import Qt

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Zone principale avec splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Barre latérale
        self.sidebar = MainSidebar()
        self.sidebar.setFixedWidth(280)
        main_splitter.addWidget(self.sidebar)

        # Zone de contenu principal avec breadcrumbs
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Breadcrumbs
        self.breadcrumbs = BreadcrumbsWidget()
        self.breadcrumbs.setFixedHeight(48)
        self.breadcrumbs.step_selected.connect(self._on_breadcrumb_step_selected)
        content_layout.addWidget(self.breadcrumbs)

        # Contenu principal (Stack)
        self.stack_widget = QStackedWidget()
        self.stack_widget.setObjectName("mainContent")
        content_layout.addWidget(self.stack_widget)
        
        main_splitter.addWidget(content_widget)
        main_splitter.setSizes([280, 1200])
        
        main_layout.addWidget(main_splitter)

        # Composants d'aide et de statut
        self.help_panel = HelpPanel()
        self.status_widget = SystemStatusWidget()
        self.status_widget.status_updated.connect(self._on_system_status_updated)

        # Initialiser le gestionnaire de vues
        self.view_manager = ViewManager(self.stack_widget)
        self._create_and_register_views()
    
    def _create_and_register_views(self):
        """Crée et enregistre les vues v2 auprès du ViewManager"""
        logger.info("Création et enregistrement des vues v2")

        # Vue d'accueil
        welcome_view = WelcomeView(parent=None)
        self.view_manager.register_view('welcome', welcome_view)
        welcome_view.projectCreationRequested.connect(self._handle_project_creation)

        # Dashboard maritime
        dashboard_view = DashboardViewMaritime(parent=None)
        self.view_manager.register_view('dashboard', dashboard_view)

        # Vues avec lazy loading
        for view_name, config in VIEWS_CONFIG.items():
            if 'loader' in config:
                view_instance = config['loader'](parent=None)
                self.view_manager.register_view(view_name, view_instance)
                logger.info(f"[VIEW REGISTRATION] '{view_name}' view registered with object ID: {id(view_instance)}")

        # Navigation initiale
        self.view_manager.switch_to_view('welcome')
        self._update_breadcrumbs_for_view('welcome')

    def _update_breadcrumbs_for_view(self, view_name):
        """Met à jour les breadcrumbs en fonction de la vue actuelle"""
        # Mapping des noms de vues vers les WorkflowStep
        view_to_step = {
            'welcome': WorkflowStep.WELCOME,
            'dashboard': WorkflowStep.PROJECT,
            'calibration': WorkflowStep.CALIBRATION,
            'acquisition': WorkflowStep.ACQUISITION,
            'analysis': WorkflowStep.ANALYSIS,
            'export': WorkflowStep.EXPORT
        }
        
        if view_name in view_to_step:
            workflow_step = view_to_step[view_name]
            self.breadcrumbs.set_current_step(workflow_step)

    @Slot(object, str)
    def _on_breadcrumb_step_selected(self, workflow_step, view_name):
        """Gère la sélection d'une étape dans les breadcrumbs"""
        # Mapping des WorkflowStep vers les noms de vues
        step_to_view = {
            WorkflowStep.WELCOME: 'welcome',
            WorkflowStep.PROJECT: 'dashboard',
            WorkflowStep.CALIBRATION: 'calibration',
            WorkflowStep.ACQUISITION: 'acquisition',
            WorkflowStep.ANALYSIS: 'analysis',
            WorkflowStep.EXPORT: 'export'
        }
        
        if workflow_step in step_to_view:
            target_view = step_to_view[workflow_step]
            self.view_manager.switch_to_view(target_view)
        else:
            logger.warning(f"Étape de breadcrumb inconnue: {workflow_step}")

    def _setup_connections(self):
        """Configure les connexions entre les composants"""
        pass

    def _setup_status_indicators(self):
        """Configure les indicateurs de statut système"""
        pass

    def _install_contextual_help(self):
        """Installe le système d'aide contextuelle"""
        pass

    def _handle_project_creation(self):
        """Gère la création d'un nouveau projet"""
        self.projectCreated.emit()
        self.view_manager.switch_to_view('dashboard')

    @Slot(StatusLevel)
    def _on_system_status_updated(self, status_level):
        """Met à jour l'interface en fonction du statut système"""
        logger.debug(f"Mise à jour du statut système: {status_level}")
        if status_level == StatusLevel.ERROR:
            show_error("Une erreur système est survenue")
        elif status_level == StatusLevel.WARNING:
            show_info("Attention: Le système nécessite votre attention")
        elif status_level == StatusLevel.OK:
            show_success("Le système fonctionne normalement")