#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale pour CHNeoWave
Gestion des signaux de projet et coordination des vues
"""

from PyQt5.QtWidgets import (
    QMainWindow, QStackedWidget, QVBoxLayout, QWidget,
    QMenuBar, QStatusBar, QAction, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

# Import des vues
try:
    from .views.welcome_view import WelcomeView
    from .views.acquisition_view import AcquisitionView
    from .views.analysis_view import AnalysisView
except ImportError:
    # Fallback si les vues ne sont pas disponibles
    WelcomeView = None
    AcquisitionView = None
    AnalysisView = None

# Import des widgets
try:
    from .widgets.infos_essai_dock import InfosEssaiDock
except ImportError:
    InfosEssaiDock = None

try:
    from .widgets.etat_capteurs_dock import EtatCapteursDock
except ImportError:
    EtatCapteursDock = None


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application CHNeoWave"""
    
    projectCreated = pyqtSignal()          # nouveau signal
    
    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CHNeoWave")
        self.setMinimumSize(1024, 768)
        
        # Configuration
        self.config = config or {}
        
        # Métadonnées du projet
        self.project_meta = {}             # renseigné par WelcomeView
        
        # État de l'application
        self.is_acquiring = False
        
        # Construction de l'interface
        self._build_stack()
        self._setup_docks()
        self._setup_menu()
        self._setup_status_bar()
        self._setup_connections()
    
    def _build_stack(self):
        """Construit le widget empilé avec les différentes vues"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Stack widget pour les vues
        self.stack_widget = QStackedWidget()
        layout.addWidget(self.stack_widget)
        
        # Création des vues
        self._create_views()
    
    def _create_views(self):
        """Crée et ajoute les vues au stack widget"""
        # Vue d'accueil
        if WelcomeView:
            self.welcome_view = WelcomeView()
            self.stack_widget.addWidget(self.welcome_view)
        else:
            self.welcome_view = None
        
        # Vue d'acquisition
        if AcquisitionView:
            try:
                self.acquisition_view = AcquisitionView(
                    config=self.config,
                    acquisition_controller=None  # À initialiser plus tard
                )
                self.stack_widget.addWidget(self.acquisition_view)
            except Exception as e:
                print(f"Erreur création AcquisitionView: {e}")
                self.acquisition_view = None
        else:
            self.acquisition_view = None
        
        # Vue d'analyse
        if AnalysisView:
            try:
                # Essayer de créer AnalysisView avec gestion d'erreur pour les arguments
                self.analysis_view = AnalysisView()
                self.stack_widget.addWidget(self.analysis_view)
            except Exception as e:
                print(f"Erreur création AnalysisView: {e}")
                # Créer une vue de substitution
                from PyQt5.QtWidgets import QLabel
                self.analysis_view = QLabel("Vue d'analyse indisponible (arguments manquants)")
                self.stack_widget.addWidget(self.analysis_view)
        else:
            self.analysis_view = None
        
        # Démarrer sur la vue d'accueil
        if self.welcome_view:
            self.stack_widget.setCurrentWidget(self.welcome_view)
    
    def _setup_docks(self):
        """Configure les docks widgets"""
        # Dock Infos Essai
        if InfosEssaiDock:
            self.infos_essai_dock = InfosEssaiDock(self)
            self.addDockWidget(Qt.RightDockWidgetArea, self.infos_essai_dock)
            
            # Connecter les signaux du dock
            self.infos_essai_dock.essai_updated.connect(self._on_essai_updated)
        else:
            self.infos_essai_dock = None
        
        # Dock État Capteurs
        if EtatCapteursDock:
            self.etat_capteurs_dock = EtatCapteursDock(self)
            self.addDockWidget(Qt.LeftDockWidgetArea, self.etat_capteurs_dock)
            
            # Connecter les signaux du dock
            self.etat_capteurs_dock.capteur_selected.connect(self._on_capteur_selected)
            self.etat_capteurs_dock.capteurs_updated.connect(self._on_capteurs_updated)
        else:
            self.etat_capteurs_dock = None
    
    def _setup_menu(self):
        """Configure la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu('Fichier')
        
        new_action = QAction('Nouveau projet', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction('Quitter', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Vues
        view_menu = menubar.addMenu('Vues')
        
        welcome_action = QAction('Accueil', self)
        welcome_action.triggered.connect(lambda: self._switch_to_view('welcome'))
        view_menu.addAction(welcome_action)
        
        acquisition_action = QAction('Acquisition', self)
        acquisition_action.triggered.connect(lambda: self._switch_to_view('acquisition'))
        view_menu.addAction(acquisition_action)
        
        analysis_action = QAction('Analyse', self)
        analysis_action.triggered.connect(lambda: self._switch_to_view('analysis'))
        view_menu.addAction(analysis_action)
    
    def _setup_status_bar(self):
        """Configure la barre de statut"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
    
    def _setup_connections(self):
        """Configure les connexions de signaux"""
        # Signal de création de projet
        self.projectCreated.connect(self._unlock_acquisition)
        
        # Connexions avec les vues
        if self.welcome_view:
            self.welcome_view.projectCreated.connect(self._on_project_created)
        
        if self.acquisition_view:
            # Désactiver les boutons d'acquisition au démarrage
            if hasattr(self.acquisition_view, 'btn_start'):
                self.acquisition_view.btn_start.setEnabled(False)
            if hasattr(self.acquisition_view, 'btn_export'):
                self.acquisition_view.btn_export.setEnabled(False)
            
            # Connecter les signaux d'acquisition au dock infos essai
            if self.infos_essai_dock:
                # Simuler des connexions pour les signaux d'acquisition
                # Ces connexions seront complétées quand les contrôleurs seront disponibles
                pass
    
    @pyqtSlot()
    def _unlock_acquisition(self):
        """Déverrouille les fonctionnalités d'acquisition après création du projet"""
        if self.acquisition_view:
            # Activer les boutons d'acquisition
            if hasattr(self.acquisition_view, 'btn_start'):
                self.acquisition_view.btn_start.setEnabled(True)
            if hasattr(self.acquisition_view, 'btn_export'):
                self.acquisition_view.btn_export.setEnabled(True)
        
        # Mettre à jour la barre de titre avec les métadonnées du projet
        meta = self.project_meta
        if meta:
            title = f"CHNeoWave – {meta.get('name', 'Projet')} ({meta.get('owner', 'Inconnu')}, {meta.get('date', 'Date inconnue')})"
            self.setWindowTitle(title)
        
        # Mettre à jour la barre de statut
        self.status_bar.showMessage(f"Projet '{meta.get('name', 'Inconnu')}' créé - Acquisition disponible")
    
    @pyqtSlot(dict)
    def _on_project_created(self, project_data):
        """Gère la réception des données de projet depuis WelcomeView"""
        self.project_meta = project_data
        
        # Mettre à jour le dock infos essai avec les données du projet
        if self.infos_essai_dock:
            self.infos_essai_dock.set_essai_info(
                nom=project_data.get('name', 'Nouveau projet'),
                operateur=project_data.get('owner', 'Utilisateur'),
                configuration=project_data.get('type', 'Standard')
            )
        
        self.projectCreated.emit()
    
    @pyqtSlot(dict)
    def _on_essai_updated(self, essai_data):
        """Gère les mises à jour des informations d'essai"""
        # Mettre à jour la barre de statut avec les infos essai
        statut = essai_data.get('statut', 'Inconnu')
        nom = essai_data.get('nom', 'Essai')
        
        if statut == 'En cours':
            duree = essai_data.get('duree', '00:00:00')
            nb_echantillons = essai_data.get('nb_echantillons', 0)
            self.status_bar.showMessage(f"Acquisition en cours - {nom} - Durée: {duree} - Échantillons: {nb_echantillons:,}")
        elif statut == 'Pause':
            self.status_bar.showMessage(f"Acquisition en pause - {nom}")
        elif statut == 'Arrêté':
            self.status_bar.showMessage(f"Acquisition arrêtée - {nom}")
        else:
            self.status_bar.showMessage(f"Statut: {statut} - {nom}")
    
    def start_acquisition(self, config=None):
        """Démarre une acquisition (méthode publique pour les contrôleurs)"""
        if self.infos_essai_dock and self.project_meta:
            # Configurer les paramètres d'acquisition
            if config:
                self.infos_essai_dock.set_acquisition_config(
                    nb_sondes=config.get('nb_sondes', 4),
                    freq_echantillonnage=config.get('freq_echantillonnage', 1000),
                    taille_buffer=config.get('taille_buffer', 10000)
                )
            
            # Démarrer l'essai
            self.infos_essai_dock.start_essai(
                nom=self.project_meta.get('name', 'Acquisition'),
                operateur=self.project_meta.get('owner', 'Utilisateur'),
                configuration=self.project_meta.get('type', 'Standard')
            )
            
            self.is_acquiring = True
    
    def stop_acquisition(self):
        """Arrête l'acquisition en cours"""
        if self.infos_essai_dock:
            self.infos_essai_dock.stop_essai()
        self.is_acquiring = False
    
    def pause_acquisition(self):
        """Met en pause l'acquisition"""
        if self.infos_essai_dock:
            self.infos_essai_dock.pause_essai()
    
    def resume_acquisition(self):
        """Reprend l'acquisition"""
        if self.infos_essai_dock:
            self.infos_essai_dock.resume_essai()
    
    def update_acquisition_progress(self, nb_echantillons):
        """Met à jour le progrès de l'acquisition"""
        if self.infos_essai_dock:
            self.infos_essai_dock.update_echantillons(nb_echantillons)
    
    @pyqtSlot(int)
    def _on_capteur_selected(self, capteur_id):
        """Gère la sélection d'un capteur"""
        # Mettre à jour la barre de statut
        self.status_bar.showMessage(f"Capteur {capteur_id} sélectionné")
        
        # Émettre un signal pour les autres composants
        # TODO: Connecter aux vues qui ont besoin de cette information
        print(f"Capteur {capteur_id} sélectionné")
    
    @pyqtSlot(dict)
    def _on_capteurs_updated(self, capteurs_data):
        """Gère les mises à jour des capteurs"""
        # Calculer des statistiques pour la barre de statut
        capteurs = capteurs_data.get('capteurs', {})
        nb_connectes = sum(1 for c in capteurs.values() if c['etat'] in ['Connecté', 'Acquisition'])
        nb_acquisition = sum(1 for c in capteurs.values() if c['etat'] == 'Acquisition')
        nb_erreurs = sum(1 for c in capteurs.values() if c['etat'] == 'Erreur')
        
        # Mettre à jour la barre de statut si pas d'acquisition en cours
        if not self.is_acquiring:
            status_msg = f"Capteurs: {nb_connectes}/{len(capteurs)} connectés"
            if nb_acquisition > 0:
                status_msg += f" | {nb_acquisition} en acquisition"
            if nb_erreurs > 0:
                status_msg += f" | {nb_erreurs} erreurs"
            
            self.status_bar.showMessage(status_msg)
    
    def set_capteurs_config(self, nb_capteurs: int):
        """Configure le nombre de capteurs"""
        if self.etat_capteurs_dock:
            self.etat_capteurs_dock.spin_nb_capteurs.setValue(nb_capteurs)
    
    def start_capteurs_simulation(self):
        """Démarre la simulation des capteurs"""
        if self.etat_capteurs_dock:
            self.etat_capteurs_dock.start_simulation()
    
    def stop_capteurs_simulation(self):
        """Arrête la simulation des capteurs"""
        if self.etat_capteurs_dock:
            self.etat_capteurs_dock.stop_simulation()
    
    def update_capteur_data(self, capteur_id: int, **kwargs):
        """Met à jour les données d'un capteur spécifique"""
        if self.etat_capteurs_dock:
            self.etat_capteurs_dock.set_capteur_data(capteur_id, **kwargs)
    
    def _switch_to_view(self, view_name):
        """Change la vue active"""
        if view_name == 'welcome' and self.welcome_view:
            self.stack_widget.setCurrentWidget(self.welcome_view)
        elif view_name == 'acquisition' and self.acquisition_view:
            self.stack_widget.setCurrentWidget(self.acquisition_view)
        elif view_name == 'analysis' and self.analysis_view:
            self.stack_widget.setCurrentWidget(self.analysis_view)
    
    def _new_project(self):
        """Crée un nouveau projet"""
        if self.is_acquiring:
            QMessageBox.warning(
                self, 
                "Nouveau Projet", 
                "Impossible de créer un nouveau projet pendant l'acquisition."
            )
            return
        
        # Réinitialiser les données
        self.project_meta = {}
        
        # Désactiver l'acquisition
        if self.acquisition_view:
            if hasattr(self.acquisition_view, 'btn_start'):
                self.acquisition_view.btn_start.setEnabled(False)
            if hasattr(self.acquisition_view, 'btn_export'):
                self.acquisition_view.btn_export.setEnabled(False)
        
        # Réinitialiser la vue d'accueil
        if self.welcome_view and hasattr(self.welcome_view, 'reset_form'):
            self.welcome_view.reset_form()
        
        # Retourner à la vue d'accueil
        self._switch_to_view('welcome')
        
        # Réinitialiser le titre
        self.setWindowTitle("CHNeoWave")
        self.status_bar.showMessage("Nouveau projet - Veuillez renseigner les informations")
    
    def get_current_view(self):
        """Retourne la vue actuellement active"""
        current = self.stack_widget.currentWidget()
        
        if current == self.welcome_view:
            return 'welcome'
        elif current == self.acquisition_view:
            return 'acquisition'
        elif current == self.analysis_view:
            return 'analysis'
        else:
            return 'unknown'
    
    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        if self.is_acquiring:
            reply = QMessageBox.question(
                self,
                'Fermeture',
                'Une acquisition est en cours. Voulez-vous vraiment quitter ?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
        
        event.accept()