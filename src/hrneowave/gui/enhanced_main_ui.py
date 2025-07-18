# enhanced_main_ui.py - Interface principale avec navigation par onglets et transitions
import sys
import os
from typing import Dict, Any, Optional, Callable
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QToolBar, QAction, QLabel, QPushButton, QMessageBox, QApplication,
    QStatusBar, QMenuBar, QMenu, QSizePolicy, QFrame, QSplitter,
    QProgressBar, QSystemTrayIcon
)
from PyQt5.QtCore import (
    Qt, pyqtSignal, pyqtSlot, QTimer, QPropertyAnimation, QEasingCurve,
    QRect, QSize, QSettings, QThread
)
from PyQt5.QtGui import (
    QFont, QPalette, QColor, QPixmap, QPainter, QIcon, QKeySequence
)

try:
    from .tabbed_main_ui import WelcomeTab, CalibrationTab
    from .enhanced_acquisition_tab import EnhancedAcquisitionTab
    from .enhanced_analysis_tab import EnhancedAnalysisTab
    from .field_validator import FieldValidator
    from .theme import (
        set_light_mode, set_dark_mode, get_current_theme, 
        register_theme_callback, get_theme_colors
    )
except ImportError as e:
    print(f"⚠️ Import manquant: {e}")
    WelcomeTab = CalibrationTab = EnhancedAcquisitionTab = None
    EnhancedAnalysisTab = FieldValidator = None
    set_light_mode = set_dark_mode = get_current_theme = None
    register_theme_callback = get_theme_colors = None

class NavigationToolBar(QToolBar):
    """Barre d'outils de navigation personnalisée"""
    
    tabRequested = pyqtSignal(int)  # index de l'onglet
    themeToggleRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("Navigation", parent)
        self.current_tab = 0
        self.tab_actions = []
        self._init_toolbar()
        
    def _init_toolbar(self):
        """Initialise la barre d'outils"""
        self.setMovable(False)
        self.setFloatable(False)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIconSize(QSize(24, 24))
        
        # Actions de navigation
        tab_info = [
            ("🏠", "Accueil", "Informations du projet"),
            ("⚙️", "Calibration", "Configuration des capteurs"),
            ("🚀", "Acquisition", "Acquisition de données"),
            ("📊", "Analyse", "Analyse des résultats")
        ]
        
        for i, (icon, name, tooltip) in enumerate(tab_info):
            action = QAction(f"{icon} {name}", self)
            action.setToolTip(tooltip)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, idx=i: self._on_tab_action(idx))
            
            self.addAction(action)
            self.tab_actions.append(action)
            
        # Séparateur
        self.addSeparator()
        
        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)
        
        # Toggle thème
        self.theme_action = QAction("🌙 Sombre", self)
        self.theme_action.setToolTip("Basculer le thème")
        self.theme_action.triggered.connect(self.themeToggleRequested.emit)
        self.addAction(self.theme_action)
        
        # Sélectionner le premier onglet
        if self.tab_actions:
            self.tab_actions[0].setChecked(True)
            
    def _on_tab_action(self, index: int):
        """Gère le clic sur un onglet"""
        # Décocher tous les autres
        for i, action in enumerate(self.tab_actions):
            action.setChecked(i == index)
            
        self.current_tab = index
        self.tabRequested.emit(index)
        
    def set_current_tab(self, index: int):
        """Définit l'onglet actuel"""
        if 0 <= index < len(self.tab_actions):
            self.current_tab = index
            
            # Mettre à jour les actions
            for i, action in enumerate(self.tab_actions):
                action.setChecked(i == index)
                
    def set_tab_enabled(self, index: int, enabled: bool):
        """Active/désactive un onglet"""
        if 0 <= index < len(self.tab_actions):
            self.tab_actions[index].setEnabled(enabled)
            
    def update_theme_action(self, is_dark: bool):
        """Met à jour l'action de thème"""
        if is_dark:
            self.theme_action.setText("☀️ Clair")
            self.theme_action.setToolTip("Passer au thème clair")
        else:
            self.theme_action.setText("🌙 Sombre")
            self.theme_action.setToolTip("Passer au thème sombre")

class StatusBarWidget(QStatusBar):
    """Barre de statut personnalisée"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_status_bar()
        
    def _init_status_bar(self):
        """Initialise la barre de statut"""
        # Message principal
        self.main_label = QLabel("Prêt")
        self.addWidget(self.main_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        self.addPermanentWidget(separator)
        
        # Statut de validation
        self.validation_label = QLabel("✅ Valide")
        self.addPermanentWidget(self.validation_label)
        
        # Séparateur
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.VLine)
        self.addPermanentWidget(separator2)
        
        # Thème actuel
        self.theme_label = QLabel("🌙 Clair")
        self.addPermanentWidget(self.theme_label)
        
        # Séparateur
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.VLine)
        self.addPermanentWidget(separator3)
        
        # Heure
        self.time_label = QLabel()
        self.addPermanentWidget(self.time_label)
        
        # Timer pour l'heure
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self._update_time)
        self.time_timer.start(1000)  # Chaque seconde
        self._update_time()
        
    def _update_time(self):
        """Met à jour l'affichage de l'heure"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"🕐 {current_time}")
        
    def set_main_message(self, message: str, color: str = None):
        """Définit le message principal"""
        self.main_label.setText(message)
        if color:
            self.main_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        else:
            self.main_label.setStyleSheet("")
            
    def set_validation_status(self, is_valid: bool):
        """Définit le statut de validation"""
        if is_valid:
            self.validation_label.setText("✅ Valide")
            self.validation_label.setStyleSheet("color: #27ae60;")
        else:
            self.validation_label.setText("❌ Invalide")
            self.validation_label.setStyleSheet("color: #e74c3c;")
            
    def set_theme_status(self, is_dark: bool):
        """Définit le statut du thème"""
        if is_dark:
            self.theme_label.setText("🌙 Sombre")
        else:
            self.theme_label.setText("☀️ Clair")

class EnhancedMainUI(QMainWindow):
    """Interface principale améliorée avec navigation par onglets"""
    
    # Signaux
    acquisitionStarted = pyqtSignal(dict)
    acquisitionFinished = pyqtSignal(dict)
    analysisCompleted = pyqtSignal(dict)
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__()
        self.config = config or {}
        self.settings = QSettings('CHNeoWave', 'MainUI')
        
        # État de l'application
        self.current_tab_index = 0
        self.is_acquiring = False
        self.project_data = {}
        self.acquisition_data = None
        self.analysis_results = None
        
        # Onglets
        self.welcome_tab = None
        self.calibration_tab = None
        self.acquisition_tab = None
        self.analysis_tab = None
        
        # Validation globale
        self.global_validator = FieldValidator() if FieldValidator else None
        
        self._init_ui()
        self._setup_connections()
        self._setup_animations()
        self._restore_settings()
        
        # Enregistrer callback thème
        if register_theme_callback:
            register_theme_callback(self._on_theme_changed)
            
    def _init_ui(self):
        """Initialise l'interface utilisateur"""
        # Configuration de la fenêtre principale
        self.setWindowTitle("CHNeoWave - Laboratoire d'Étude Maritime")
        self.setMinimumSize(1024, 640)
        self.resize(1280, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barre d'outils de navigation
        self.nav_toolbar = NavigationToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.nav_toolbar)
        
        # Widget empilé pour les onglets
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Créer les onglets
        self._create_tabs()
        
        # Barre de statut
        self.status_bar = StatusBarWidget()
        self.setStatusBar(self.status_bar)
        
        # Menu
        self._create_menu()
        
    def _create_tabs(self):
        """Crée tous les onglets"""
        # Onglet Accueil
        if WelcomeTab:
            self.welcome_tab = WelcomeTab(self.config)
            self.stacked_widget.addWidget(self.welcome_tab)
        else:
            placeholder = QLabel("Onglet Accueil non disponible")
            placeholder.setAlignment(Qt.AlignCenter)
            self.stacked_widget.addWidget(placeholder)
            
        # Onglet Calibration
        if CalibrationTab:
            self.calibration_tab = CalibrationTab(self.config)
            self.stacked_widget.addWidget(self.calibration_tab)
        else:
            placeholder = QLabel("Onglet Calibration non disponible")
            placeholder.setAlignment(Qt.AlignCenter)
            self.stacked_widget.addWidget(placeholder)
            
        # Onglet Acquisition
        if EnhancedAcquisitionTab:
            self.acquisition_tab = EnhancedAcquisitionTab(self.config)
            self.stacked_widget.addWidget(self.acquisition_tab)
        else:
            placeholder = QLabel("Onglet Acquisition non disponible")
            placeholder.setAlignment(Qt.AlignCenter)
            self.stacked_widget.addWidget(placeholder)
            
        # Onglet Analyse
        if EnhancedAnalysisTab:
            self.analysis_tab = EnhancedAnalysisTab()
            self.stacked_widget.addWidget(self.analysis_tab)
        else:
            placeholder = QLabel("Onglet Analyse non disponible")
            placeholder.setAlignment(Qt.AlignCenter)
            self.stacked_widget.addWidget(placeholder)
            
    def _create_menu(self):
        """Crée le menu principal"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("&Fichier")
        
        new_action = QAction("&Nouveau Projet", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Ouvrir Projet", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Sauvegarder", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Quitter", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Affichage
        view_menu = menubar.addMenu("&Affichage")
        
        theme_action = QAction("Basculer &Thème", self)
        theme_action.setShortcut("Ctrl+T")
        theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(theme_action)
        
        fullscreen_action = QAction("&Plein Écran", self)
        fullscreen_action.setShortcut(QKeySequence.FullScreen)
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("&Aide")
        
        about_action = QAction("À &Propos", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _setup_connections(self):
        """Configure les connexions de signaux"""
        # Navigation
        self.nav_toolbar.tabRequested.connect(self._on_tab_requested)
        self.nav_toolbar.themeToggleRequested.connect(self._toggle_theme)
        
        # Validation des onglets
        if self.welcome_tab and hasattr(self.welcome_tab, 'validationChanged'):
            self.welcome_tab.validationChanged.connect(self._on_validation_changed)
            
        if self.calibration_tab and hasattr(self.calibration_tab, 'validationChanged'):
            self.calibration_tab.validationChanged.connect(self._on_validation_changed)
            
        if self.acquisition_tab and hasattr(self.acquisition_tab, 'validationChanged'):
            self.acquisition_tab.validationChanged.connect(self._on_validation_changed)
            
        # Acquisition
        if self.acquisition_tab:
            self.acquisition_tab.acquisitionStarted.connect(self._on_acquisition_started)
            self.acquisition_tab.acquisitionFinished.connect(self._on_acquisition_finished)
            
        # Analyse
        if self.analysis_tab:
            self.analysis_tab.analysisCompleted.connect(self._on_analysis_completed)
            
        # ÉTAPE 1: Configuration initiale - tous les onglets activés
        self.nav_toolbar.set_tab_enabled(0, True)   # Accueil
        self.nav_toolbar.set_tab_enabled(1, True)   # Calibration
        self.nav_toolbar.set_tab_enabled(2, True)   # Acquisition
        self.nav_toolbar.set_tab_enabled(3, True)   # Analyse
            
    def _setup_animations(self):
        """Configure les animations"""
        # Animation de transition entre onglets
        self.tab_animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        self.tab_animation.setDuration(300)
        self.tab_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def _restore_settings(self):
        """Restaure les paramètres sauvegardés"""
        # Géométrie de la fenêtre
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
            
        # État de la fenêtre
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)
            
        # Thème
        theme = self.settings.value("theme", "light")
        if theme == "dark" and set_dark_mode:
            set_dark_mode()
        elif set_light_mode:
            set_light_mode()
            
        # Onglet actuel
        current_tab = self.settings.value("currentTab", 0, type=int)
        self._switch_to_tab(current_tab)
        
    def _save_settings(self):
        """Sauvegarde les paramètres"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue("currentTab", self.current_tab_index)
        
        if get_current_theme:
            self.settings.setValue("theme", get_current_theme())
            
    @pyqtSlot(int)
    def _on_tab_requested(self, index: int):
        """Gère la demande de changement d'onglet"""
        # Vérifier si on peut quitter l'onglet actuel
        if not self._can_leave_current_tab():
            # Remettre la sélection sur l'onglet actuel
            self.nav_toolbar.set_current_tab(self.current_tab_index)
            return
            
        # Effectuer la transition
        self._switch_to_tab(index)
        
    def _can_leave_current_tab(self) -> bool:
        """Vérifie si on peut quitter l'onglet actuel"""
        # ÉTAPE 1: Navigation libre - Supprimer la validation obligatoire pour la navigation
        # La validation ne sera requise que pour le bouton "Créer projet"
        
        # Vérifier seulement si une acquisition est en cours
        if self.is_acquiring and self.current_tab_index == 2:
            reply = QMessageBox.question(
                self, "Acquisition en cours", 
                "Une acquisition est en cours. Voulez-vous vraiment changer d'onglet?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            return reply == QMessageBox.Yes
            
        return True
        
    def _switch_to_tab(self, index: int):
        """Effectue le changement d'onglet"""
        if 0 <= index < self.stacked_widget.count():
            # Sauvegarder les données de l'onglet actuel
            self._save_current_tab_data()
            
            # Changer d'onglet
            self.current_tab_index = index
            self.stacked_widget.setCurrentIndex(index)
            self.nav_toolbar.set_current_tab(index)
            
            # Charger les données dans le nouvel onglet
            self._load_tab_data(index)
            
            # Mettre à jour le statut
            self._update_status_for_tab(index)
            
    def _save_current_tab_data(self):
        """Sauvegarde les données de l'onglet actuel"""
        if self.current_tab_index == 0 and self.welcome_tab:
            # Sauvegarder les données du projet
            if hasattr(self.welcome_tab, 'get_project_data'):
                self.project_data.update(self.welcome_tab.get_project_data())
                
        elif self.current_tab_index == 1 and self.calibration_tab:
            # Sauvegarder la configuration de calibration
            if hasattr(self.calibration_tab, 'get_calibration_config'):
                self.project_data['calibration'] = self.calibration_tab.get_calibration_config()
                
        elif self.current_tab_index == 2 and self.acquisition_tab:
            # Sauvegarder la configuration d'acquisition
            if hasattr(self.acquisition_tab, 'get_acquisition_config'):
                self.project_data['acquisition'] = self.acquisition_tab.get_acquisition_config()
                
    def _load_tab_data(self, index: int):
        """Charge les données dans l'onglet"""
        if index == 0 and self.welcome_tab:
            # Charger les données du projet
            if hasattr(self.welcome_tab, 'load_project_data'):
                self.welcome_tab.load_project_data(self.project_data)
                
        elif index == 1 and self.calibration_tab:
            # Charger la configuration de calibration
            if hasattr(self.calibration_tab, 'load_calibration_config'):
                calib_config = self.project_data.get('calibration', {})
                self.calibration_tab.load_calibration_config(calib_config)
                
        elif index == 3 and self.analysis_tab:
            # Charger les données d'acquisition pour analyse
            if self.acquisition_data and hasattr(self.analysis_tab, 'load_acquisition_data'):
                self.analysis_tab.load_acquisition_data(self.acquisition_data)
                
    def _update_status_for_tab(self, index: int):
        """Met à jour le statut pour l'onglet"""
        tab_names = ["Accueil", "Calibration", "Acquisition", "Analyse"]
        if 0 <= index < len(tab_names):
            self.status_bar.set_main_message(f"Onglet: {tab_names[index]}")
            
    @pyqtSlot(bool)
    def _on_validation_changed(self, is_valid: bool):
        """Gère le changement de validation"""
        self.status_bar.set_validation_status(is_valid)
        
        # ÉTAPE 1: Navigation libre - Les onglets restent toujours activés
        # La validation n'affecte plus l'accès aux onglets
        pass
            
    @pyqtSlot(dict)
    def _on_acquisition_started(self, config: dict):
        """Gère le début d'acquisition"""
        self.is_acquiring = True
        self.status_bar.set_main_message("Acquisition en cours...", "#3498db")
        
        # Désactiver les champs de l'onglet Accueil
        if self.welcome_tab and hasattr(self.welcome_tab, 'set_enabled'):
            self.welcome_tab.set_enabled(False)
            
        # Émettre le signal
        self.acquisitionStarted.emit(config)
        
    @pyqtSlot(dict)
    def _on_acquisition_finished(self, results: dict):
        """Gère la fin d'acquisition"""
        self.is_acquiring = False
        self.acquisition_data = results
        
        self.status_bar.set_main_message("Acquisition terminée", "#27ae60")
        
        # Réactiver les champs de l'onglet Accueil
        if self.welcome_tab and hasattr(self.welcome_tab, 'set_enabled'):
            self.welcome_tab.set_enabled(True)
            
        # Basculer automatiquement vers l'analyse
        QTimer.singleShot(2000, lambda: self._switch_to_tab(3))
        
        # Émettre le signal
        self.acquisitionFinished.emit(results)
        
    @pyqtSlot(dict)
    def _on_analysis_completed(self, results: dict):
        """Gère la fin d'analyse"""
        self.analysis_results = results
        self.status_bar.set_main_message("Analyse terminée", "#27ae60")
        
        # Émettre le signal
        self.analysisCompleted.emit(results)
        
    def _toggle_theme(self):
        """Bascule le thème"""
        if get_current_theme and set_light_mode and set_dark_mode:
            current = get_current_theme()
            if current == "light":
                set_dark_mode()
            else:
                set_light_mode()
                
    def _on_theme_changed(self, theme_name: str):
        """Callback pour changement de thème"""
        is_dark = theme_name == "dark"
        self.nav_toolbar.update_theme_action(is_dark)
        self.status_bar.set_theme_status(is_dark)
        
    def _new_project(self):
        """Crée un nouveau projet"""
        if self.is_acquiring:
            QMessageBox.warning(self, "Nouveau Projet", "Impossible de créer un nouveau projet pendant l'acquisition.")
            return
            
        reply = QMessageBox.question(
            self, "Nouveau Projet", 
            "Créer un nouveau projet? Les données non sauvegardées seront perdues.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.project_data.clear()
            self.acquisition_data = None
            self.analysis_results = None
            
            # Réinitialiser tous les onglets
            # TODO: Implémenter la réinitialisation
            
            self._switch_to_tab(0)
            self.status_bar.set_main_message("Nouveau projet créé")
            
    def _open_project(self):
        """Ouvre un projet existant"""
        # TODO: Implémenter l'ouverture de projet
        QMessageBox.information(self, "Ouvrir Projet", "Fonction à implémenter")
        
    def _save_project(self):
        """Sauvegarde le projet"""
        # TODO: Implémenter la sauvegarde de projet
        QMessageBox.information(self, "Sauvegarder", "Fonction à implémenter")
        
    def _toggle_fullscreen(self):
        """Bascule le mode plein écran"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def _show_about(self):
        """Affiche la boîte À Propos"""
        QMessageBox.about(
            self, "À Propos de CHNeoWave",
            "<h3>CHNeoWave</h3>"
            "<p>Logiciel d'acquisition et d'analyse de données maritimes</p>"
            "<p>Laboratoire d'Étude Maritime - Modèles Réduits</p>"
            "<p>Méditerranée - Bassin et Canal</p>"
            "<p><b>Version:</b> 2.0.0</p>"
            "<p><b>Développé avec:</b> PyQt5, PyQtGraph, NumPy</p>"
        )
        
    def get_current_tab_index(self) -> int:
        """Retourne l'index de l'onglet actuel"""
        return self.current_tab_index
        
    def is_acquisition_running(self) -> bool:
        """Vérifie si une acquisition est en cours"""
        return self.is_acquiring
        
    def get_project_data(self) -> Dict[str, Any]:
        """Retourne les données du projet"""
        return self.project_data.copy()
        
    def get_acquisition_data(self) -> Optional[Dict[str, Any]]:
        """Retourne les données d'acquisition"""
        return self.acquisition_data
        
    def get_analysis_results(self) -> Optional[Dict[str, Any]]:
        """Retourne les résultats d'analyse"""
        return self.analysis_results
        
    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        if self.is_acquiring:
            reply = QMessageBox.question(
                self, "Fermeture", 
                "Une acquisition est en cours. Voulez-vous vraiment quitter?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        # Sauvegarder les paramètres
        self._save_settings()
        
        # Nettoyer les ressources
        if self.acquisition_tab and hasattr(self.acquisition_tab, 'cleanup'):
            self.acquisition_tab.cleanup()
            
        if self.analysis_tab and hasattr(self.analysis_tab, 'cleanup'):
            self.analysis_tab.cleanup()
            
        event.accept()

def main():
    """Fonction principale pour tester l'interface"""
    app = QApplication(sys.argv)
    
    # Configuration par défaut
    config = {
        'sample_rate': 32.0,
        'n_channels': 4,
        'max_duration': 300
    }
    
    # Créer et afficher l'interface
    window = EnhancedMainUI(config)
    window.show()
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())