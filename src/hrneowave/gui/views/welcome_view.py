#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vue d'accueil pour CHNeoWave
Gestion de la création de projet avec validation
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QDateEdit
)
from PyQt5.QtCore import Qt, QDate, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QFont

# Import du système d'erreurs unifié
try:
    from ...core.signal_bus import get_error_bus
    ErrorBus = get_error_bus
except ImportError:
    # Fallback si le système d'erreurs n'est pas disponible
    class ErrorBus:
        @staticmethod
        def instance():
            return ErrorBus()
        
        def error(self):
            return ErrorBus()
        
        def emit(self, module, message, level):
            print(f"[{module}] {message}")


class WelcomeView(QWidget):
    """Vue d'accueil avec création de projet"""
    
    # Signal émis lors de la création d'un projet
    projectCreated = pyqtSignal(dict)  # Émet les métadonnées du projet
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_connections()
        self.project_created = False     # flag global
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Titre
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        
        # Formulaire de projet
        form_group = QWidget()
        form_group.setMaximumWidth(400)
        form_layout = QFormLayout(form_group)
        
        # Champs du projet
        self.le_name = QLineEdit()
        self.le_name.setPlaceholderText("Entrez le nom du projet")
        
        self.le_owner = QLineEdit()
        self.le_owner.setPlaceholderText("Entrez le nom du chef de projet")
        
        self.de_date = QDateEdit(calendarPopup=True)
        self.de_date.setDate(QDate.currentDate())
        self.de_date.setDisplayFormat("dd/MM/yyyy")
        
        form_layout.addRow("Nom du projet *", self.le_name)
        form_layout.addRow("Chef de projet *", self.le_owner)
        form_layout.addRow("Date *", self.de_date)
        
        # Centrer le formulaire
        form_container = QHBoxLayout()
        form_container.addStretch(1)
        form_container.addWidget(form_group)
        form_container.addStretch(1)
        
        # Boutons
        buttons = QHBoxLayout()
        self.btn_create = QPushButton("Créer le projet")
        self.btn_create.setEnabled(True)               # toujours visible
        self.btn_create.setMinimumHeight(40)
        self.btn_create.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        
        buttons.addStretch(1)
        buttons.addWidget(self.btn_create)
        
        # Assemblage final
        layout.addStretch(1)
        layout.addLayout(title_layout)
        layout.addLayout(form_container)
        layout.addLayout(buttons)
        layout.addStretch(2)
    
    def _setup_connections(self):
        """Configure les connexions de signaux"""
        self.btn_create.clicked.connect(self._on_create_project)
    
    @pyqtSlot()
    def _on_create_project(self):
        """Gère la création du projet avec validation"""
        # Validation des champs obligatoires
        if not all([self.le_name.text().strip(), 
                    self.le_owner.text().strip()]):
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Champs manquants",
                "Veuillez renseigner Nom et Chef de projet avant de créer."
            )
            return
        
        # Marquer le projet comme créé
        self.project_created = True
        
        # Préparer les métadonnées du projet
        project_meta = {
            "name": self.le_name.text().strip(),
            "owner": self.le_owner.text().strip(),
            "date": self.de_date.date().toString("yyyy-MM-dd")
        }
        
        # Propager dans le MainController via le parent window
        try:
            main_window = self.parent().window()
            if hasattr(main_window, 'project_meta'):
                main_window.project_meta = project_meta
            if hasattr(main_window, 'projectCreated'):
                main_window.projectCreated.emit()
        except Exception as e:
            print(f"Erreur lors de la propagation du projet: {e}")
        
        # Émettre le signal local
        self.projectCreated.emit(project_meta)
        
        # Message de confirmation
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Projet créé",
            f"Projet « {self.le_name.text()} » créé avec succès."
        )
    
    def get_project_data(self):
        """Retourne les données du projet actuel"""
        if not self.project_created:
            return None
        
        return {
            "name": self.le_name.text().strip(),
            "owner": self.le_owner.text().strip(),
            "date": self.de_date.date().toString("yyyy-MM-dd")
        }
    
    def reset_form(self):
        """Remet à zéro le formulaire"""
        self.le_name.clear()
        self.le_owner.clear()
        self.de_date.setDate(QDate.currentDate())
        self.project_created = False