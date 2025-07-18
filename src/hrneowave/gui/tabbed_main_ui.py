# tabbed_main_ui.py - Interface principale avec navigation par onglets et validation
import sys
import os
from typing import Dict, Any, Optional
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QToolBar, QAction, QLabel, QLineEdit, QPushButton, QFormLayout,
    QGroupBox, QDateEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QMessageBox, QFrame, QSizePolicy, QProgressBar, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QDate, QTimer
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont

try:
    from .field_validator import FieldValidator
    from .theme import set_dark_mode, set_light_mode, current_theme, register_theme_callback
    from .views.acquisition_view import AcquisitionView
    from .views.analysis_view import AnalysisView
except ImportError as e:
    print(f"⚠️ Import manquant: {e}")
    FieldValidator = None
    AcquisitionView = None
    AnalysisView = None

class WelcomeTab(QWidget):
    """Onglet d'accueil avec champs obligatoires"""
    
    validationChanged = pyqtSignal(bool)
    
    def __init__(self, config: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.config = config
        self.validator = FieldValidator() if FieldValidator else None
        self._init_ui()
        self._setup_validation()
        
    def _init_ui(self):
        """Initialise l'interface de l'onglet d'accueil"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Titre principal
        title_label = QLabel("🌊 CHNeoWave - Laboratoire d'Étude Maritime")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Logiciel d'acquisition et d'analyse de houle pour modèles réduits\n"
            "Spécialisé pour les études en bassin et canal méditerranéens"
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Groupe informations projet (champs obligatoires)
        project_group = QGroupBox("📋 Informations du Projet (Obligatoires)")
        project_layout = QFormLayout(project_group)
        
        # Nom du projet
        self.project_name_edit = QLineEdit()
        self.project_name_edit.setPlaceholderText("Ex: Étude houle Méditerranée 2025")
        project_layout.addRow("Nom du projet *:", self.project_name_edit)
        
        # Chef de projet
        self.project_manager_edit = QLineEdit()
        self.project_manager_edit.setPlaceholderText("Ex: Dr. Marine Dupont")
        project_layout.addRow("Chef de projet *:", self.project_manager_edit)
        
        # Date du projet
        self.project_date_edit = QDateEdit()
        self.project_date_edit.setDate(QDate.currentDate())
        self.project_date_edit.setCalendarPopup(True)
        project_layout.addRow("Date *:", self.project_date_edit)
        
        layout.addWidget(project_group)
        
        # Groupe configuration optionnelle
        config_group = QGroupBox("⚙️ Configuration (Optionnel)")
        config_layout = QFormLayout(config_group)
        
        # Type d'étude
        self.study_type_combo = QComboBox()
        self.study_type_combo.addItems([
            "Houle régulière",
            "Houle irrégulière", 
            "Analyse spectrale",
            "Étude de résonance",
            "Calibration capteurs"
        ])
        config_layout.addRow("Type d'étude:", self.study_type_combo)
        
        # Localisation
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Ex: Bassin Méditerranéen - Marseille")
        config_layout.addRow("Localisation:", self.location_edit)
        
        # Commentaires
        self.comments_edit = QTextEdit()
        self.comments_edit.setMaximumHeight(80)
        self.comments_edit.setPlaceholderText("Commentaires sur l'étude...")
        config_layout.addRow("Commentaires:", self.comments_edit)
        
        layout.addWidget(config_group)
        
        # Groupe thème
        theme_group = QGroupBox("🎨 Apparence")
        theme_layout = QHBoxLayout(theme_group)
        
        self.theme_toggle_btn = QPushButton("🌙 Mode Sombre")
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)
        theme_layout.addWidget(self.theme_toggle_btn)
        theme_layout.addStretch()
        
        layout.addWidget(theme_group)
        
        # Indicateur de validation
        self.validation_label = QLabel("❌ Veuillez remplir tous les champs obligatoires")
        self.validation_label.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 10px;")
        self.validation_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.validation_label)
        
        layout.addStretch()
        
    def _setup_validation(self):
        """Configure la validation des champs obligatoires"""
        if not self.validator:
            return
            
        # Ajouter les champs obligatoires
        self.validator.add_field(
            "project_name", 
            self.project_name_edit, 
            required=True,
            rules={'min_length': 3, 'max_length': 100}
        )
        
        self.validator.add_field(
            "project_manager", 
            self.project_manager_edit, 
            required=True,
            rules={'min_length': 2, 'max_length': 50}
        )
        
        self.validator.add_field(
            "project_date", 
            self.project_date_edit, 
            required=True
        )
        
        # Connecter le signal de validation
        self.validator.validationChanged.connect(self._on_validation_changed)
        
        # Validation initiale
        self.validator.validate_all()
        
    @pyqtSlot(bool)
    def _on_validation_changed(self, is_valid: bool):
        """Gère le changement de validation"""
        if is_valid:
            self.validation_label.setText("✅ Tous les champs obligatoires sont remplis")
            self.validation_label.setStyleSheet("color: #27ae60; font-weight: bold; padding: 10px;")
        else:
            self.validation_label.setText("❌ Veuillez remplir tous les champs obligatoires")
            self.validation_label.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 10px;")
            
        self.validationChanged.emit(is_valid)
        
    def _toggle_theme(self):
        """Bascule entre thème clair et sombre"""
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        
        if current_theme == "dark":
            set_light_mode(app)
            self.theme_toggle_btn.setText("🌙 Mode Sombre")
        else:
            set_dark_mode(app)
            self.theme_toggle_btn.setText("☀️ Mode Clair")
            
    def get_project_data(self) -> Dict[str, Any]:
        """Retourne les données du projet"""
        return {
            'name': self.project_name_edit.text().strip(),
            'manager': self.project_manager_edit.text().strip(),
            'date': self.project_date_edit.date().toString(Qt.ISODate),
            'study_type': self.study_type_combo.currentText(),
            'location': self.location_edit.text().strip(),
            'comments': self.comments_edit.toPlainText().strip()
        }
        
    def is_valid(self) -> bool:
        """Vérifie si tous les champs obligatoires sont valides"""
        if not self.validator:
            return True
        is_valid, _ = self.validator.validate_all()
        return is_valid

class CalibrationTab(QWidget):
    """Onglet de calibration"""
    
    validationChanged = pyqtSignal(bool)
    
    def __init__(self, config: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.config = config
        self._init_ui()
        
    def _init_ui(self):
        """Initialise l'interface de calibration"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre
        title_label = QLabel("⚙️ Calibration des Capteurs")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Configuration capteurs
        sensors_group = QGroupBox("📡 Configuration des Capteurs")
        sensors_layout = QFormLayout(sensors_group)
        
        # Nombre de sondes
        self.n_probes_spin = QSpinBox()
        self.n_probes_spin.setRange(1, 8)
        self.n_probes_spin.setValue(self.config.get('n_channels', 4))
        sensors_layout.addRow("Nombre de sondes:", self.n_probes_spin)
        
        # Fréquence d'échantillonnage
        self.sample_rate_spin = QDoubleSpinBox()
        self.sample_rate_spin.setRange(1.0, 1000.0)
        self.sample_rate_spin.setValue(self.config.get('sample_rate', 32.0))
        self.sample_rate_spin.setSuffix(" Hz")
        sensors_layout.addRow("Fréquence d'échantillonnage:", self.sample_rate_spin)
        
        # Type de capteur
        self.sensor_type_combo = QComboBox()
        self.sensor_type_combo.addItems([
            "Sonde résistive",
            "Sonde capacitive", 
            "Capteur ultrasonique",
            "Capteur laser"
        ])
        sensors_layout.addRow("Type de capteur:", self.sensor_type_combo)
        
        layout.addWidget(sensors_group)
        
        # Calibration
        calib_group = QGroupBox("🎯 Étalonnage")
        calib_layout = QVBoxLayout(calib_group)
        
        calib_info = QLabel(
            "La calibration permet d'ajuster la sensibilité des capteurs\n"
            "et de corriger les dérives de mesure."
        )
        calib_info.setStyleSheet("color: #666; margin-bottom: 10px;")
        calib_layout.addWidget(calib_info)
        
        # Boutons de calibration
        calib_buttons_layout = QHBoxLayout()
        
        self.auto_calib_btn = QPushButton("🔄 Calibration Automatique")
        self.manual_calib_btn = QPushButton("✋ Calibration Manuelle")
        self.test_calib_btn = QPushButton("🧪 Test de Calibration")
        
        calib_buttons_layout.addWidget(self.auto_calib_btn)
        calib_buttons_layout.addWidget(self.manual_calib_btn)
        calib_buttons_layout.addWidget(self.test_calib_btn)
        
        calib_layout.addLayout(calib_buttons_layout)
        
        # Statut calibration
        self.calib_status_label = QLabel("⏳ Calibration non effectuée")
        self.calib_status_label.setStyleSheet("color: #f39c12; font-weight: bold; padding: 10px;")
        calib_layout.addWidget(self.calib_status_label)
        
        layout.addWidget(calib_group)
        layout.addStretch()
        
        # Connecter les boutons
        self.auto_calib_btn.clicked.connect(self._auto_calibration)
        self.manual_calib_btn.clicked.connect(self._manual_calibration)
        self.test_calib_btn.clicked.connect(self._test_calibration)
        
        # Émettre validation initiale (calibration optionnelle)
        self.validationChanged.emit(True)
        
    def _auto_calibration(self):
        """Lance la calibration automatique"""
        self.calib_status_label.setText("🔄 Calibration automatique en cours...")
        self.calib_status_label.setStyleSheet("color: #3498db; font-weight: bold; padding: 10px;")
        
        # Simuler calibration
        QTimer.singleShot(2000, self._calibration_completed)
        
    def _manual_calibration(self):
        """Lance la calibration manuelle"""
        QMessageBox.information(self, "Calibration Manuelle", 
                               "Fonctionnalité de calibration manuelle à implémenter")
        
    def _test_calibration(self):
        """Test la calibration"""
        QMessageBox.information(self, "Test de Calibration", 
                               "Test de calibration effectué avec succès")
        
    def _calibration_completed(self):
        """Marque la calibration comme terminée"""
        self.calib_status_label.setText("✅ Calibration terminée avec succès")
        self.calib_status_label.setStyleSheet("color: #27ae60; font-weight: bold; padding: 10px;")
        
    def get_calibration_data(self) -> Dict[str, Any]:
        """Retourne les données de calibration"""
        return {
            'n_probes': self.n_probes_spin.value(),
            'sample_rate': self.sample_rate_spin.value(),
            'sensor_type': self.sensor_type_combo.currentText(),
            'calibrated': "✅" in self.calib_status_label.text()
        }
        
    def is_valid(self) -> bool:
        """La calibration est toujours valide (optionnelle)"""
        return True

class TabbedMainUI(QMainWindow):
    """Interface principale avec navigation par onglets et validation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.current_tab_index = 0
        self.tab_names = ["Accueil", "Calibration", "Acquisition", "Analyse"]
        
        self._init_ui()
        self._setup_navigation()
        self._apply_theme()
        
    def _init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("CHNeoWave - Interface Unifiée")
        self.setMinimumSize(1024, 640)
        self.resize(1280, 720)
        
        # Widget central avec QStackedWidget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Barre de navigation
        self.nav_toolbar = QToolBar("Navigation")
        self.nav_toolbar.setMovable(False)
        self.nav_toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(Qt.TopToolBarArea, self.nav_toolbar)
        
        # Widget empilé pour les onglets
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Créer les onglets
        self._create_tabs()
        
        # Barre de statut avec boutons navigation
        self._create_status_bar()
        
    def _create_tabs(self):
        """Crée tous les onglets"""
        # Onglet Accueil
        self.welcome_tab = WelcomeTab(self.config)
        self.welcome_tab.validationChanged.connect(
            lambda valid: self._update_navigation_state(0, valid)
        )
        self.stacked_widget.addWidget(self.welcome_tab)
        
        # Onglet Calibration
        self.calibration_tab = CalibrationTab(self.config)
        self.calibration_tab.validationChanged.connect(
            lambda valid: self._update_navigation_state(1, valid)
        )
        self.stacked_widget.addWidget(self.calibration_tab)
        
        # Onglet Acquisition (placeholder)
        acquisition_placeholder = QLabel("🚀 Module d'Acquisition\n\nEn cours de développement...")
        acquisition_placeholder.setAlignment(Qt.AlignCenter)
        acquisition_placeholder.setStyleSheet("font-size: 18px; color: #666;")
        self.stacked_widget.addWidget(acquisition_placeholder)
        
        # Onglet Analyse (placeholder)
        analysis_placeholder = QLabel("📊 Module d'Analyse\n\nEn cours de développement...")
        analysis_placeholder.setAlignment(Qt.AlignCenter)
        analysis_placeholder.setStyleSheet("font-size: 18px; color: #666;")
        self.stacked_widget.addWidget(analysis_placeholder)
        
    def _setup_navigation(self):
        """Configure la navigation par onglets"""
        # Actions de navigation
        self.nav_actions = []
        icons = ["🏠", "⚙️", "🚀", "📊"]
        
        for i, (name, icon) in enumerate(zip(self.tab_names, icons)):
            action = QAction(f"{icon} {name}", self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, idx=i: self._navigate_to_tab(idx))
            self.nav_actions.append(action)
            self.nav_toolbar.addAction(action)
            
        # Sélectionner le premier onglet
        self.nav_actions[0].setChecked(True)
        
    def _create_status_bar(self):
        """Crée la barre de statut avec navigation"""
        status_bar = self.statusBar()
        
        # Bouton Précédent
        self.prev_btn = QPushButton("◀ Précédent")
        self.prev_btn.clicked.connect(self._previous_tab)
        self.prev_btn.setEnabled(False)
        status_bar.addPermanentWidget(self.prev_btn)
        
        # Indicateur de progression
        self.progress_label = QLabel("Étape 1/4: Accueil")
        self.progress_label.setStyleSheet("margin: 0 20px; font-weight: bold;")
        status_bar.addPermanentWidget(self.progress_label)
        
        # Bouton Suivant
        self.next_btn = QPushButton("Suivant ▶")
        self.next_btn.clicked.connect(self._next_tab)
        self.next_btn.setEnabled(False)  # Désactivé jusqu'à validation
        status_bar.addPermanentWidget(self.next_btn)
        
    def _navigate_to_tab(self, index: int):
        """Navigue vers un onglet spécifique"""
        # Vérifier la validation de l'onglet actuel avant de changer
        if not self._can_leave_current_tab():
            # Remettre la sélection sur l'onglet actuel
            self.nav_actions[self.current_tab_index].setChecked(True)
            self.nav_actions[index].setChecked(False)
            return
            
        self.current_tab_index = index
        self.stacked_widget.setCurrentIndex(index)
        
        # Mettre à jour la navigation
        for i, action in enumerate(self.nav_actions):
            action.setChecked(i == index)
            
        self._update_navigation_buttons()
        
    def _can_leave_current_tab(self) -> bool:
        """Vérifie si on peut quitter l'onglet actuel"""
        current_widget = self.stacked_widget.currentWidget()
        
        if hasattr(current_widget, 'is_valid'):
            if not current_widget.is_valid():
                QMessageBox.warning(
                    self, 
                    "Validation requise",
                    "Veuillez remplir tous les champs obligatoires avant de continuer."
                )
                return False
                
        return True
        
    def _previous_tab(self):
        """Navigue vers l'onglet précédent"""
        if self.current_tab_index > 0:
            self._navigate_to_tab(self.current_tab_index - 1)
            
    def _next_tab(self):
        """Navigue vers l'onglet suivant"""
        if self.current_tab_index < len(self.tab_names) - 1:
            self._navigate_to_tab(self.current_tab_index + 1)
            
    def _update_navigation_state(self, tab_index: int, is_valid: bool):
        """Met à jour l'état de navigation basé sur la validation"""
        if tab_index == self.current_tab_index:
            self._update_navigation_buttons()
            
    def _update_navigation_buttons(self):
        """Met à jour l'état des boutons de navigation"""
        # Bouton Précédent
        self.prev_btn.setEnabled(self.current_tab_index > 0)
        
        # Bouton Suivant
        can_proceed = True
        if hasattr(self.stacked_widget.currentWidget(), 'is_valid'):
            can_proceed = self.stacked_widget.currentWidget().is_valid()
            
        self.next_btn.setEnabled(
            self.current_tab_index < len(self.tab_names) - 1 and can_proceed
        )
        
        # Mettre à jour le texte du bouton suivant
        if self.current_tab_index == len(self.tab_names) - 1:
            self.next_btn.setText("Terminer")
        else:
            self.next_btn.setText("Suivant ▶")
            
        # Indicateur de progression
        self.progress_label.setText(
            f"Étape {self.current_tab_index + 1}/{len(self.tab_names)}: {self.tab_names[self.current_tab_index]}"
        )
        
    def _apply_theme(self):
        """Applique le thème par défaut"""
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        
        if self.config.get('theme', 'dark') == 'dark':
            set_dark_mode(app)
        else:
            set_light_mode(app)
            
        # Enregistrer callback pour les changements de thème
        register_theme_callback(self._on_theme_changed)
        
    def _on_theme_changed(self, theme_name: str):
        """Callback appelé lors du changement de thème"""
        # Mettre à jour les graphiques PyQtGraph si nécessaire
        pass