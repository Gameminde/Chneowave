# -*- coding: utf-8 -*-
"""
Vue d'accueil CHNeoWave - Gestion de Projet
Étape 1 : Créer ou ouvrir un projet
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
    QPushButton, QDateEdit, QTextEdit
)
from PySide6.QtCore import Signal, QDate
from PySide6.QtGui import QFont

class WelcomeView(QWidget):
    """
    Vue d'accueil pour la création/ouverture de projet
    Respecte le principe d'isolation : UNIQUEMENT la gestion de projet
    """
    
    # Signal émis lors de la sélection du projet
    projectSelected = Signal(str)  # Chemin du projet (vide pour nouveau projet)
    
    def __init__(self, parent=None):
        super().__init__(parent)
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
        
        # Champs obligatoires
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Nom du projet d'essai")
        self.project_name.setMinimumHeight(35)
        form_layout.addRow("Nom du Projet *:", self.project_name)
        
        self.project_manager = QLineEdit()
        self.project_manager.setPlaceholderText("Nom du chef de projet")
        self.project_manager.setMinimumHeight(35)
        form_layout.addRow("Chef de Projet *:", self.project_manager)
        
        self.laboratory = QLineEdit()
        self.laboratory.setPlaceholderText("Nom du laboratoire")
        self.laboratory.setMinimumHeight(35)
        form_layout.addRow("Laboratoire *:", self.laboratory)
        
        # Champs optionnels
        self.project_date = QDateEdit()
        self.project_date.setDate(QDate.currentDate())
        self.project_date.setMinimumHeight(35)
        form_layout.addRow("Date de l'Essai:", self.project_date)
        
        self.description = QTextEdit()
        self.description.setPlaceholderText("Description de l'essai (optionnel)")
        self.description.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description)
        
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
        # Validation en temps réel
        self.project_name.textChanged.connect(self.validateForm)
        self.project_manager.textChanged.connect(self.validateForm)
        self.laboratory.textChanged.connect(self.validateForm)
        
        # Debug pour tracer le clic
        self.validate_button.clicked.connect(lambda: print("[DEBUG] Bouton Valider cliqué"))
        
        # Validation du projet
        self.validate_button.clicked.connect(self.validateProject)
    
    def validateForm(self):
        """
        Validation en temps réel du formulaire
        Active le bouton uniquement si tous les champs obligatoires sont remplis
        """
        required_fields = [
            self.project_name.text().strip(),
            self.project_manager.text().strip(),
            self.laboratory.text().strip()
        ]
        
        all_filled = all(field for field in required_fields)
        self.validate_button.setEnabled(all_filled)
    
    def validateProject(self):
        """
        Validation finale et émission du signal
        Pour un nouveau projet, on émet un chemin vide
        """
        # 🔍 TRAÇAGE FIN - Ajouté pour diagnostic navigation
        print("[DEBUG] slot validate called")
        print(f"[DEBUG] Début validateProject - Données du projet:")
        
        # Stocker les métadonnées dans l'instance pour récupération ultérieure
        self.project_metadata = {
            'name': self.project_name.text().strip(),
            'manager': self.project_manager.text().strip(),
            'laboratory': self.laboratory.text().strip(),
            'date': self.project_date.date().toString('yyyy-MM-dd'),
            'description': self.description.toPlainText().strip()
        }
        
        print(f"[DEBUG] Métadonnées projet: {self.project_metadata}")
        print(f"[DEBUG] Émission du signal projectSelected...")
        
        # Émission du signal vers le ViewManager (chemin vide = nouveau projet)
        self.projectSelected.emit('')
        
        print(f"[DEBUG] Signal projectSelected émis avec succès")
        print(f"[DEBUG] Fin validateProject")
    
    def resetForm(self):
        """
        Réinitialisation du formulaire
        """
        self.project_name.clear()
        self.project_manager.clear()
        self.laboratory.clear()
        self.project_date.setDate(QDate.currentDate())
        self.description.clear()
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