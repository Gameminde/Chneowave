# -*- coding: utf-8 -*-
"""
Vue d'accueil CHNeoWave - Gestion de Projet
Étape 1 : Créer ou ouvrir un projet
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
    QPushButton, QDateEdit, QTextEdit, QFrame
)
from PySide6.QtCore import Signal, QDate
from PySide6.QtGui import QFont

# Import des modules de validation et gestion d'erreurs
from ...core.validators import ProjectValidator, ValidationLevel
from ...core.error_handler import get_error_handler, ErrorCategory, ErrorContext

class WelcomeView(QWidget):
    """
    Vue d'accueil pour la création/ouverture de projet
    Respecte le principe d'isolation : UNIQUEMENT la gestion de projet
    """
    
    # Signal émis lors de la sélection du projet
    projectSelected = Signal(str)  # Chemin du projet (vide pour nouveau projet)
    projectCreationRequested = Signal(dict) # Dictionnaire avec les métadonnées du projet
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialisation des validateurs et gestionnaire d'erreurs
        self.validator = ProjectValidator()
        self.error_handler = get_error_handler()
        
        # Dictionnaire pour stocker les labels d'erreur
        self.error_labels = {}
        
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur
        """

        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Titre principal
        title_label = QLabel("CHNeoWave : Gestion de Projet")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2980b9; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Formulaire de métadonnées du projet
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Champs obligatoires avec validation
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Nom du projet d'essai")
        self.project_name.setMinimumHeight(35)
        form_layout.addRow("Nom du Projet *:", self.project_name)
        
        # Label d'erreur pour le nom du projet
        self.error_labels['project_name'] = self._create_error_label()
        form_layout.addRow("", self.error_labels['project_name'])
        
        self.project_manager = QLineEdit()
        self.project_manager.setPlaceholderText("Nom du chef de projet")
        self.project_manager.setMinimumHeight(35)
        form_layout.addRow("Chef de Projet *:", self.project_manager)
        
        # Label d'erreur pour le chef de projet
        self.error_labels['project_manager'] = self._create_error_label()
        form_layout.addRow("", self.error_labels['project_manager'])
        
        self.laboratory = QLineEdit()
        self.laboratory.setPlaceholderText("Nom du laboratoire")
        self.laboratory.setMinimumHeight(35)
        form_layout.addRow("Laboratoire *:", self.laboratory)
        
        # Label d'erreur pour le laboratoire
        self.error_labels['laboratory'] = self._create_error_label()
        form_layout.addRow("", self.error_labels['laboratory'])
        
        # Champs optionnels
        self.project_date = QDateEdit()
        self.project_date.setDate(QDate.currentDate())
        self.project_date.setMinimumHeight(35)
        form_layout.addRow("Date de l'Essai:", self.project_date)
        
        self.description = QTextEdit()
        self.description.setPlaceholderText("Description de l'essai (optionnel)")
        self.description.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description)
        
        # Label d'erreur pour la description
        self.error_labels['description'] = self._create_error_label()
        form_layout.addRow("", self.error_labels['description'])
        
        main_layout.addLayout(form_layout)
        
        # Espacement flexible
        main_layout.addStretch()
        
        # Bouton de validation
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.validate_button = QPushButton("Valider et Continuer")
        self.validate_button.setMinimumHeight(45)
        self.validate_button.setMinimumWidth(200)
        self.validate_button.setEnabled(False)  # Désactivé par défaut
        self.validate_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #1e3a5f;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #34495e;
            }
        """)
        
        button_layout.addWidget(self.validate_button)
        main_layout.addLayout(button_layout)
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        # Validation en temps réel avec messages d'erreur
        self.project_name.textChanged.connect(lambda: self._validate_field('project_name'))
        self.project_manager.textChanged.connect(lambda: self._validate_field('project_manager'))
        self.laboratory.textChanged.connect(lambda: self._validate_field('laboratory'))
        self.description.textChanged.connect(lambda: self._validate_field('description'))
        
        # Validation du projet
        self.validate_button.clicked.connect(self.validateProject)
    
    def _create_error_label(self):
        """Crée un label d'erreur stylisé"""
        label = QLabel()
        label.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                font-size: 10pt;
                font-style: italic;
                margin-top: 2px;
                margin-bottom: 5px;
            }
        """)
        label.setWordWrap(True)
        label.hide()  # Caché par défaut
        return label
    
    def _validate_field(self, field_name):
        """Valide un champ spécifique et affiche les erreurs"""
        try:
            # Récupérer la valeur du champ
            if field_name == 'project_name':
                value = self.project_name.text().strip()
                result = self.validator.validate_project_name(value)
            elif field_name == 'project_manager':
                value = self.project_manager.text().strip()
                result = self.validator.validate_manager_name(value)
            elif field_name == 'laboratory':
                value = self.laboratory.text().strip()
                result = self.validator.validate_laboratory(value)
            elif field_name == 'description':
                value = self.description.toPlainText().strip()
                result = self.validator.validate_description(value)
            else:
                return
            
            # Afficher ou masquer le message d'erreur
            error_label = self.error_labels[field_name]
            
            if not result.is_valid:
                error_label.setText(result.message)
                error_label.show()
                
                # Changer la couleur du champ selon le niveau
                field_widget = getattr(self, field_name)
                if result.level == ValidationLevel.ERROR:
                    field_widget.setStyleSheet("border: 2px solid #e74c3c; border-radius: 4px;")
                elif result.level == ValidationLevel.WARNING:
                    field_widget.setStyleSheet("border: 2px solid #f39c12; border-radius: 4px;")
            else:
                error_label.hide()
                # Réinitialiser le style du champ
                field_widget = getattr(self, field_name)
                field_widget.setStyleSheet("")
            
            # Mettre à jour l'état du bouton
            self._update_button_state()
            
        except Exception as e:
            # Gestion d'erreur avec le gestionnaire centralisé
            context = ErrorContext(
                operation="field_validation",
                component="welcome_view",
                category=ErrorCategory.GUI,
                user_data={'field': field_name, 'value': value if 'value' in locals() else ''}
            )
            self.error_handler.handle_error(e, context, 
                f"Erreur lors de la validation du champ {field_name}")
    
    def _update_button_state(self):
        """Met à jour l'état du bouton de validation"""
        try:
            # Vérifier que tous les champs obligatoires sont valides
            required_fields = ['project_name', 'project_manager', 'laboratory']
            all_valid = True
            
            for field_name in required_fields:
                if field_name == 'project_name':
                    value = self.project_name.text().strip()
                    result = self.validator.validate_project_name(value)
                elif field_name == 'project_manager':
                    value = self.project_manager.text().strip()
                    result = self.validator.validate_manager_name(value)
                elif field_name == 'laboratory':
                    value = self.laboratory.text().strip()
                    result = self.validator.validate_laboratory(value)
                
                if not result.is_valid or result.level == ValidationLevel.ERROR:
                    all_valid = False
                    break
            
            self.validate_button.setEnabled(all_valid)
            
        except Exception as e:
            # En cas d'erreur, désactiver le bouton par sécurité
            self.validate_button.setEnabled(False)
            context = ErrorContext(
                operation="button_state_update",
                component="welcome_view",
                category=ErrorCategory.GUI
            )
            self.error_handler.handle_error(e, context, 
                "Erreur lors de la mise à jour du bouton de validation")
    
    def validateProject(self):
        """
        Validation finale et émission du signal
        Pour un nouveau projet, on émet un chemin vide
        """
        try:
            # Validation finale de tous les champs
            project_data = {
                'name': self.project_name.text().strip(),
                'manager': self.project_manager.text().strip(),
                'laboratory': self.laboratory.text().strip(),
                'date': self.project_date.date().toString('yyyy-MM-dd'),
                'description': self.description.toPlainText().strip()
            }
            
            # Validation complète du projet
            validation_result = self.validator.validate_project_data(project_data)
            
            if not validation_result.is_valid:
                # Afficher l'erreur de validation globale
                context = ErrorContext(
                    operation="project_validation",
                    component="welcome_view",
                    category=ErrorCategory.USER_INPUT,
                    user_data=project_data
                )
                error_msg = self.error_handler.handle_error(
                    ValueError(validation_result.message), 
                    context, 
                    f"Validation du projet échouée: {validation_result.message}"
                )
                return
            
            # Stocker les métadonnées validées
            self.project_metadata = project_data
            
            # Émission des signaux
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"[SIGNAL EMISSION] Emitting 'projectCreationRequested' from WelcomeView with object ID: {id(self)}")
            self.projectCreationRequested.emit(self.project_metadata)
            self.projectSelected.emit('')  # Pour compatibilité
            
        except Exception as e:
            # Gestion d'erreur avec le gestionnaire centralisé
            context = ErrorContext(
                operation="project_validation",
                component="welcome_view",
                category=ErrorCategory.GUI
            )
            error_msg = self.error_handler.handle_error(e, context, 
                "Erreur lors de la validation du projet")
            
            # Optionnel: afficher un message à l'utilisateur
            # Ici on pourrait ajouter une QMessageBox si nécessaire
    
    def resetForm(self):
        """
        Réinitialisation du formulaire
        """
        self.project_name.clear()
        self.project_manager.clear()
        self.laboratory.clear()
        self.project_date.setDate(QDate.currentDate())
        self.description.clear()
        
        # Masquer tous les messages d'erreur
        for error_label in self.error_labels.values():
            error_label.hide()
        
        # Réinitialiser les styles des champs
        for field_name in ['project_name', 'project_manager', 'laboratory', 'description']:
            field_widget = getattr(self, field_name)
            field_widget.setStyleSheet("")
        
        self.validate_button.setEnabled(False)
        
    def reset_view(self):
        """
        Méthode requise par le ViewManager pour réinitialiser la vue
        """
        self.resetForm()
        
    def get_project_metadata(self):
        """
        Retourne les métadonnées du projet actuel
        """
        return getattr(self, 'project_metadata', {})