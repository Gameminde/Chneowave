# -*- coding: utf-8 -*-
"""
Contrôleur principal moderne pour CHNeoWave
Orchestre le workflow en 5 étapes avec le ViewManager
"""

import sys
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from PySide6.QtCore import QObject, Signal, QTimer
from ..view_manager import ViewManager
from hrneowave.core.signal_bus import get_signal_bus
from hrneowave.hardware.manager import HardwareManager
from hrneowave.core.post_processor import PostProcessor
from .optimized_processing_worker import OptimizedProcessingWorker
from hrneowave.core.error_handler import get_error_handler, ErrorCategory, ErrorContext, handle_errors
from hrneowave.core.performance_monitor import get_performance_monitor, Alert, AlertLevel

class MainController(QObject):
    """
    Contrôleur principal moderne pour CHNeoWave
    
    Responsabilités:
    - Orchestration du workflow en 5 étapes
    - Gestion des données entre les étapes
    - Interface avec les modules core et hardware
    - Gestion des erreurs et de la configuration
    """
    
    # Signaux pour la communication externe
    applicationReady = Signal()
    workflowCompleted = Signal(str)  # Chemin du rapport final
    errorOccurred = Signal(str, str)  # Titre, message

    def __init__(self, main_window, view_manager: ViewManager, config: Dict[str, Any]):
        # Initialisation QObject
        super().__init__()
        
        self.main_window = main_window
        self.view_manager = view_manager
        self.stacked_widget = self.view_manager.stacked_widget
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Gestionnaire d'erreurs centralisé
        self.error_handler = get_error_handler()
        
        # Moniteur de performance
        self.performance_monitor = get_performance_monitor()
        self._setup_performance_monitoring()
        
        # État du workflow
        self.current_project_path: Optional[str] = None
        self.workflow_data: Dict[str, Any] = {}
        
        # Modules backend
        self.hardware_adapter: Optional[HardwareManager] = None
        self.post_processor: Optional[PostProcessor] = None
        self.processing_worker: Optional[OptimizedProcessingWorker] = None
        
        # Initialisation
        self._setup_logging()
        self._initialize_backend_modules()
        self._connect_signals()
        
        # Démarrage
        # QTimer.singleShot(100, self._finalize_initialization)
        self._finalize_initialization()
        
        # Démarrer le monitoring de performance
        self.performance_monitor.start_monitoring()
        
        self.logger.info("MainController initialisé")
        
    def _setup_logging(self):
        """
        Configure le système de logging
        """
        log_level = self.config.get('log_level', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    @handle_errors(operation="initialize_backend", component="MainController", category=ErrorCategory.SYSTEM)
    def _initialize_backend_modules(self):
        """
        Initialise les modules backend
        """
        try:
            # Initialiser le post-processor
            if PostProcessor:
                self.post_processor = PostProcessor()
                self.logger.info("PostProcessor initialisé")
                
            # Initialiser l'adaptateur matériel
            if HardwareManager:
                self.hardware_adapter = HardwareManager(self.config)
                self.logger.info("Hardware adapter initialisé")
                
        except Exception as e:
            self.logger.error(f"Erreur initialisation backend: {e}")
            raise
            

        try:
            # Créer le view manager avec le widget empilé existant
            
            
            self.logger.info("ViewManager créé et configuré")
            
        except Exception as e:
            self.logger.error(f"Erreur création ViewManager: {e}")
            self._show_error("Erreur d'initialisation", f"Impossible de créer l'interface: {e}")
            
    def _connect_signals(self):
        """
        Connecte tous les signaux du workflow
        """
        if not self.view_manager:
            return
            
        # Signaux du ViewManager
        self.view_manager.projectSelected.connect(self._on_project_selected)
        self.view_manager.calibrationFinished.connect(self._on_calibration_finished)
        self.view_manager.acquisitionFinished.connect(self._on_acquisition_finished)
        self.view_manager.analysisFinished.connect(self._on_analysis_finished)
        self.view_manager.exportFinished.connect(self._on_export_finished)
        
        # Signal bus global (si disponible)
        if get_signal_bus:
            try:
                bus = get_signal_bus()
                bus.sessionStarted.connect(self._on_session_started)
                bus.errorOccurred.connect(self._on_bus_error)
                self.logger.info("Signal bus connecté")
            except Exception as e:
                self.logger.warning(f"Signal bus non disponible: {e}")
                
        self.logger.info("Signaux connectés")
        
    def _setup_performance_monitoring(self):
        """
        Configure le monitoring de performance
        """
        # Ajouter un callback pour les alertes de performance
        self.performance_monitor.add_alert_callback(self._on_performance_alert)
        
        self.logger.info("Monitoring de performance configuré")
        
    def _on_performance_alert(self, alert: Alert):
        """
        Gestionnaire pour les alertes de performance
        """
        # Créer le contexte d'erreur
        context = ErrorContext(
            component="PerformanceMonitor",
            operation="monitoring",
            user_data={
                "metric": alert.metric,
                "value": alert.value,
                "threshold": alert.threshold,
                "current_step": self.get_current_step()
            }
        )
        
        # Traiter selon le niveau d'alerte
        if alert.level == AlertLevel.CRITICAL:
            self.error_handler.handle_error(
                Exception(alert.message),
                category=ErrorCategory.SYSTEM,
                context=context
            )
            # Afficher une alerte critique à l'utilisateur
            self._show_error("Alerte Performance Critique", alert.message, ErrorCategory.SYSTEM)
            
        elif alert.level == AlertLevel.WARNING:
            self.error_handler.log_warning(alert.message, context)
            # Pour les avertissements, on log seulement sans déranger l'utilisateur
            
        self.logger.info(f"Alerte performance traitée: {alert.level.value} - {alert.message}")

    def navigate_to_acquisition(self):
        """Navigue vers la vue d'acquisition."""
        self.logger.info("Navigation vers la vue d'acquisition demandée.")
        self.view_manager.change_view('acquisition')

    def _finalize_initialization(self):
        """
        Finalise l'initialisation et émet le signal de prêt
        """
        try:
            # Appliquer le thème
            self._apply_theme()
            
            # Mettre à jour le titre de la fenêtre
            self._update_window_title()
            
            # Afficher la vue initiale
            self._show_initial_view()
            
            # Émettre le signal de prêt
            self.applicationReady.emit()
            
            self.logger.info("Initialisation finalisée - Application prête")
            
        except Exception as e:
            self.logger.error(f"Erreur finalisation: {e}")
            
    def _show_initial_view(self, view_name: str = "dashboard"):
        """
        Affiche la vue initiale de l'application (Dashboard moderne)
        """
        try:
            if self.view_manager:
                self.view_manager.switch_to_view(view_name)
                self.logger.info(f"[INTERFACE UNIFIÉE] Vue initiale '{view_name}' affichée")
                print(f"[NAV] Application démarrée → {view_name}")
            else:
                self.logger.warning("ViewManager non disponible pour afficher la vue initiale")
        except Exception as e:
            self.logger.error(f"Erreur affichage vue initiale: {e}")
            
    def _apply_theme(self):
        """
        Applique le thème configuré
        """
        try:
            from ..theme import get_dark_stylesheet, CHNeoWaveTheme
            
            theme_name = self.config.get('theme', 'dark')
            
            if theme_name == 'dark':
                # Utiliser la nouvelle fonction get_dark_stylesheet
                stylesheet = get_dark_stylesheet()
            else:
                # Fallback vers le thème principal
                theme = CHNeoWaveTheme()
                stylesheet = theme.get_stylesheet()
                
            # Appliquer le thème seulement si on a une stylesheet valide
            if stylesheet and self.main_window:
                self.main_window.setStyleSheet(stylesheet)
                self.logger.info(f"Thème '{theme_name}' appliqué")
            else:
                self.logger.info("Thème par défaut conservé")
            
        except Exception as e:
            self.logger.warning(f"Erreur application thème: {e}")
            # Ne pas bloquer l'application si le thème échoue
            
    def _update_window_title(self, subtitle: str = ""):
        """
        Met à jour le titre de la fenêtre
        """
        base_title = "CHNeoWave v3.0.0 - Laboratoire d'Études Maritimes"
        
        if subtitle:
            title = f"{base_title} - {subtitle}"
        else:
            title = base_title
            
        self.main_window.setWindowTitle(title)
        
    # Gestionnaires d'événements du workflow
    
    def _on_project_selected(self, project_path: str):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_project_selected = Slot(str)(self._on_project_selected)
        """
        Gestionnaire pour sélection de projet - Navigation: dashboard → calibration
        """
        print(f"[DEBUG] _on_project_selected appelée avec project_path='{project_path}'")
        
        self.current_project_path = project_path
        
        if project_path:
            # Projet existant
            self.logger.info(f"Projet sélectionné: {project_path}")
            self._update_window_title(f"Projet: {Path(project_path).name}")
            
            # Charger les données du projet si nécessaire
            self._load_project_data(project_path)
        else:
            # Nouveau projet
            print("[DEBUG] Nouveau projet détecté")
            self.logger.info("Nouveau projet créé")
            self._update_window_title("Nouveau Projet")
            
            # Initialiser les données pour un nouveau projet
            self._initialize_new_project()
            
        # Navigation stricte: dashboard → calibration
        self._navigate_to_view("calibration", "Valider projet")
            
    @handle_errors(operation="load_project_data", component="MainController")
    def _load_project_data(self, project_path: str):
        """
        Charge les données d'un projet existant
        """
        try:
            # Ici, on chargerait les données du projet depuis le fichier
            # Pour l'instant, on simule
            self.workflow_data['project_info'] = {
                'path': project_path,
                'name': Path(project_path).stem,
                'loaded_at': self._get_current_timestamp()
            }
            
            self.logger.info(f"Données du projet chargées: {project_path}")
            
        except Exception as e:
            self.logger.error(f"Erreur chargement projet: {e}")
            self._show_error("Erreur de chargement", f"Impossible de charger le projet: {e}", ErrorCategory.DATA)
            raise
            
    def _initialize_new_project(self):
        """
        Initialise un nouveau projet
        """
        self.workflow_data = {
            'project_info': {
                'name': 'Nouveau Projet CHNeoWave',
                'created_at': self._get_current_timestamp(),
                'version': '3.0.0'
            }
        }
        
        self.logger.info("Nouveau projet initialisé")
        
    def _navigate_to_view(self, target_view: str, event_name: str):
        """
        Navigation stricte avec logs détaillés
        """
        from datetime import datetime
        
        current_view = self.view_manager.current_view if self.view_manager else "unknown"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[NAV] {timestamp} [{event_name}] {current_view} → {target_view}")
        self.logger.info(f"[INTERFACE UNIFIÉE] Navigation: {current_view} → {target_view} (événement: {event_name})")
        
        if self.view_manager:
            success = self.view_manager.switch_to_view(target_view)
            if success:
                print(f"[NAV] ✓ Navigation réussie vers {target_view}")
            else:
                print(f"[NAV] ✗ Échec navigation vers {target_view}")
                self.logger.error(f"Échec navigation vers {target_view}")
        else:
            print("[NAV] ✗ ViewManager non disponible")
            self.logger.error("ViewManager non disponible pour navigation")
    
    def _on_calibration_finished(self, calibration_config: Dict[str, Any]):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_calibration_finished = Slot(dict)(self._on_calibration_finished)
        """
        Gestionnaire pour fin de calibration - Navigation: calibration → acquisition
        """
        self.workflow_data['calibration_config'] = calibration_config
        
        self.logger.info("Calibration terminée")
        self.logger.debug(f"Configuration: {calibration_config}")
        
        # Initialiser le matériel avec la configuration
        self._initialize_hardware(calibration_config)
        
        # Navigation stricte: calibration → acquisition
        self._navigate_to_view("acquisition", "Continuer calibration")
        
    @handle_errors(operation="initialize_hardware", component="MainController")
    def _initialize_hardware(self, calibration_config: Dict[str, Any]):
        """
        Initialise le matériel avec la configuration de calibration
        """
        try:
            if self.hardware_adapter:
                self.hardware_adapter.initialize(calibration_config)
                self.logger.info("Matériel initialisé avec la configuration")
            else:
                self.logger.warning("Hardware adapter non disponible")
                
        except Exception as e:
            self.logger.error(f"Erreur initialisation matériel: {e}")
            self._show_error("Erreur matériel", f"Impossible d'initialiser le matériel: {e}", ErrorCategory.HARDWARE)
            raise
            
    def _on_acquisition_finished(self, acquisition_data: Dict[str, Any]):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_acquisition_finished = Slot(dict)(self._on_acquisition_finished)
        """
        Gestionnaire pour fin d'acquisition - Navigation: acquisition → analysis
        """
        self.workflow_data['acquisition_data'] = acquisition_data
        
        self.logger.info("Acquisition terminée")
        self.logger.debug(f"Données acquises: {len(acquisition_data)} éléments")
        
        # Démarrer le traitement automatique
        self._start_data_processing(acquisition_data)
        
        # Navigation stricte: acquisition → analysis
        self._navigate_to_view("analysis", "Analyser acquisition OK")
        
    def _start_data_processing(self, acquisition_data: Dict[str, Any]):
        """
        Démarre le traitement des données d'acquisition
        """
        try:
            if OptimizedProcessingWorker and not self.processing_worker:
                self.processing_worker = OptimizedProcessingWorker(self, acquisition_data)
                self.processing_worker.processingFinished.connect(self._on_processing_finished)
                self.processing_worker.start()
                
                self.logger.info("Traitement des données démarré")
            else:
                self.logger.warning("Worker de traitement non disponible")
                
        except Exception as e:
            self.logger.error(f"Erreur démarrage traitement: {e}")
            
    def _on_processing_finished(self, processed_data: Dict[str, Any]):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_processing_finished = Slot(dict)(self._on_processing_finished)
        """
        Gestionnaire pour fin de traitement des données
        """
        # Ajouter les données traitées au workflow
        self.workflow_data['processed_data'] = processed_data
        
        self.logger.info("Traitement des données terminé")
        
    def _on_analysis_finished(self, analysis_results: Dict[str, Any]):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_analysis_finished = Slot(dict)(self._on_analysis_finished)
        """
        Gestionnaire pour fin d'analyse - Navigation: analysis → export
        """
        self.workflow_data['analysis_results'] = analysis_results
        
        self.logger.info("Analyse terminée")
        self.logger.debug(f"Résultats: {len(analysis_results)} sections")
        
        # Navigation stricte: analysis → export
        self._navigate_to_view("export", "Exporter PDF/HDF5")
        
    def _on_export_finished(self, report_path: str):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_export_finished = Slot(str)(self._on_export_finished)
        """
        Gestionnaire pour fin d'export
        """
        self.workflow_data['report_path'] = report_path
        
        self.logger.info(f"Export terminé: {report_path}")
        
        # Émettre le signal de workflow terminé
        self.workflowCompleted.emit(report_path)
        
        # Mettre à jour le titre
        self._update_window_title(f"Rapport généré: {Path(report_path).name}")
        
    # Gestionnaires d'événements du signal bus
    
    def _on_session_started(self, session_config: Dict[str, Any]):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_session_started = Slot(dict)(self._on_session_started)
        """
        Gestionnaire pour démarrage de session depuis le signal bus
        """
        self.logger.info("Session démarrée via signal bus")
        
        # Intégrer la configuration de session
        if 'session_config' not in self.workflow_data:
            self.workflow_data['session_config'] = {}
            
        self.workflow_data['session_config'].update(session_config)
        
    def _on_bus_error(self, error_type: str, error_message: str):
        from PySide6.QtCore import Slot
        # Décorateur appliqué dynamiquement
        self._on_bus_error = Slot(str, str)(self._on_bus_error)
        """
        Gestionnaire pour erreurs du signal bus
        """
        self.logger.error(f"Erreur signal bus [{error_type}]: {error_message}")
        self.errorOccurred.emit(error_type, error_message)
        
    # Méthodes utilitaires
    
    def _show_error(self, title: str, message: str, category: ErrorCategory = ErrorCategory.GUI):
        """
        Affiche une boîte de dialogue d'erreur avec gestion centralisée
        """
        from PySide6.QtWidgets import QMessageBox
        
        # Créer le contexte d'erreur
        context = ErrorContext(
            component="MainController",
            operation=title,
            user_data={"current_step": self.get_current_step()}
        )
        
        # Enregistrer l'erreur
        self.error_handler.handle_error(
            Exception(message),
            category=category,
            context=context
        )
        
        # Afficher la boîte de dialogue
        QMessageBox.critical(self.main_window, title, message)
        self.errorOccurred.emit(title, message)
        
    def _show_warning(self, title: str, message: str):
        """
        Affiche une boîte de dialogue d'avertissement
        """
        from PySide6.QtWidgets import QMessageBox
        
        # Enregistrer l'avertissement
        context = ErrorContext(
            component="MainController",
            operation=title,
            user_data={"current_step": self.get_current_step()}
        )
        
        self.error_handler.log_warning(message, context)
        QMessageBox.warning(self.main_window, title, message)
        
    def _show_info(self, title: str, message: str):
        """
        Affiche une boîte de dialogue d'information
        """
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self.main_window, title, message)
        
    def _get_current_timestamp(self):
        """
        Retourne un timestamp ISO formaté
        """
        from datetime import datetime
        return datetime.now().isoformat()
        
    # Méthodes publiques pour contrôle externe
    
    def get_current_step(self) -> str:
        """
        Retourne l'étape actuelle du workflow
        """
        if self.view_manager:
            return self.view_manager.get_current_step()
        return "WELCOME"
        
    def get_workflow_data(self) -> Dict[str, Any]:
        """
        Retourne les données du workflow
        """
        return self.workflow_data.copy()
        
    def reset_workflow(self):
        """
        Remet le workflow à zéro
        """
        self.workflow_data = {}
        self.current_project_path = None
        
        if self.view_manager:
            self.view_manager.reset_workflow()
            
        self._update_window_title()
        
        self.logger.info("Workflow réinitialisé")
        
    def navigate_to_step(self, step: str) -> bool:
        """
        Navigue vers une étape spécifique
        """
        if self.view_manager:
            return self.view_manager.navigate_to_step(step)
        return False
        
    def get_config(self) -> Dict[str, Any]:
        """
        Retourne la configuration actuelle
        """
        return self.config.copy()
        
    def update_config(self, new_config: Dict[str, Any]):
        """
        Met à jour la configuration
        """
        self.config.update(new_config)
        
        # Réappliquer le thème si nécessaire
        if 'theme' in new_config:
            self._apply_theme()
            
        self.logger.info("Configuration mise à jour")
        
    def shutdown(self):
        """
        Arrêt propre du contrôleur
        """
        self.logger.info("Arrêt du MainController")
        
        # Arrêter le monitoring de performance
        if self.performance_monitor:
            try:
                self.performance_monitor.stop_monitoring()
                self.logger.info("Monitoring de performance arrêté")
            except Exception as e:
                self.logger.error(f"Erreur arrêt monitoring: {e}")
        
        # Arrêter le worker de traitement
        if self.processing_worker and self.processing_worker.isRunning():
            self.processing_worker.terminate()
            self.processing_worker.wait(3000)  # Attendre 3 secondes max
            
        # Fermer l'adaptateur matériel
        if self.hardware_adapter:
            try:
                self.hardware_adapter.cleanup()
            except Exception as e:
                self.logger.error(f"Erreur fermeture hardware: {e}")
                
        self.logger.info("MainController arrêté")
        
    def get_status_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé de l'état actuel
        """
        summary = {
            'current_step': self.get_current_step(),
            'project_path': self.current_project_path,
            'workflow_data_keys': list(self.workflow_data.keys()),
            'hardware_initialized': self.hardware_adapter is not None,
            'processing_active': self.processing_worker is not None and self.processing_worker.isRunning(),
            'timestamp': self._get_current_timestamp()
        }
        
        if self.view_manager:
            summary.update(self.view_manager.get_workflow_summary())
            
        return summary