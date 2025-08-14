# -*- coding: utf-8 -*-
"""
Breadcrumb Navigation Component

Composant fil d'Ariane avec états visuels pour la navigation CHNeoWave.
Affiche la progression dans le workflow avec états done/pending/active.

Auteur: CHNeoWave Team
Version: 1.1.0-RC
Date: 2024-12-19
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class Breadcrumb(QWidget):
    """Fil d'Ariane avec états visuels pour navigation
    
    Fonctionnalités:
    - Affichage de la progression dans le workflow
    - États visuels: active, done, pending
    - Navigation cliquable vers les étapes précédentes
    - Séparateurs visuels entre étapes
    - Responsive selon la largeur disponible
    """
    
    # Signal émis lors du clic sur une étape
    stepClicked = Signal(str)  # Nom de l'étape
    
    # Hauteur Fibonacci
    HEIGHT = 34  # Fibonacci 34
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = "dashboard"
        self.completed_steps = set()
        self.step_buttons = {}
        self.separators = []
        
        # Définition des étapes du workflow
        self.steps = {
            "dashboard": {"label": "Dashboard", "icon": "🏠", "order": 0},
            "welcome": {"label": "Projet", "icon": "👋", "order": 1},
            "calibration": {"label": "Calibration", "icon": "⚙️", "order": 2},
            "acquisition": {"label": "Acquisition", "icon": "📊", "order": 3},
            "analysis": {"label": "Analyse", "icon": "📈", "order": 4},
            "export": {"label": "Export", "icon": "💾", "order": 5}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface breadcrumb"""
        self.setObjectName("breadcrumb")
        self.setFixedHeight(self.HEIGHT)
        
        # Layout horizontal principal
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(13, 5, 13, 5)  # Fibonacci 13, 5
        self.layout.setSpacing(8)  # Fibonacci 8
        
        # Création des éléments de navigation
        self.create_breadcrumb_items()
        
        # Spacer pour aligner à gauche
        self.layout.addStretch()
        
    def create_breadcrumb_items(self):
        """Création des éléments du breadcrumb"""
        # Trier les étapes par ordre
        sorted_steps = sorted(self.steps.items(), key=lambda x: x[1]["order"])
        
        for i, (step_name, step_data) in enumerate(sorted_steps):
            # Créer le bouton d'étape
            step_button = self.create_step_button(step_name, step_data)
            self.step_buttons[step_name] = step_button
            self.layout.addWidget(step_button)
            
            # Ajouter un séparateur (sauf pour le dernier élément)
            if i < len(sorted_steps) - 1:
                separator = self.create_separator()
                self.separators.append(separator)
                self.layout.addWidget(separator)
                
        # Mise à jour initiale des états
        self.update_all_states()
        
    def create_step_button(self, step_name, step_data):
        """Création d'un bouton d'étape"""
        button = QPushButton()
        button.setObjectName("breadcrumb-step")
        button.setFlat(True)
        button.setCursor(Qt.PointingHandCursor)
        
        # Texte du bouton avec icône
        button_text = f"{step_data['icon']} {step_data['label']}"
        button.setText(button_text)
        
        # Font du bouton
        font = QFont()
        font.setPointSize(10)
        button.setFont(font)
        
        # Connexion du signal
        button.clicked.connect(lambda: self.step_clicked(step_name))
        
        return button
        
    def create_separator(self):
        """Création d'un séparateur entre étapes"""
        separator = QLabel("›")
        separator.setObjectName("breadcrumb-separator")
        separator.setAlignment(Qt.AlignCenter)
        
        # Font du séparateur
        font = QFont()
        font.setPointSize(12)
        font.setWeight(QFont.Bold)
        separator.setFont(font)
        
        return separator
        
    def step_clicked(self, step_name):
        """Gestion du clic sur une étape"""
        # Permettre la navigation uniquement vers les étapes précédentes ou complétées
        current_order = self.steps[self.current_step]["order"]
        target_order = self.steps[step_name]["order"]
        
        if (target_order <= current_order or 
            step_name in self.completed_steps or 
            step_name == "dashboard"):  # Dashboard toujours accessible
            self.stepClicked.emit(step_name)
            
    def set_current_step(self, step_name):
        """Définir l'étape actuelle"""
        if step_name in self.steps:
            self.current_step = step_name
            self.update_all_states()
            
    def mark_step_completed(self, step_name):
        """Marquer une étape comme complétée"""
        if step_name in self.steps:
            self.completed_steps.add(step_name)
            self.update_step_state(step_name)
            
    def mark_step_pending(self, step_name):
        """Marquer une étape comme en attente"""
        if step_name in self.steps:
            self.completed_steps.discard(step_name)
            self.update_step_state(step_name)
            
    def update_step_state(self, step_name):
        """Mise à jour de l'état visuel d'une étape"""
        if step_name not in self.step_buttons:
            return
            
        button = self.step_buttons[step_name]
        
        # Déterminer l'état
        if step_name == self.current_step:
            state = "active"
            button.setEnabled(True)
        elif step_name in self.completed_steps:
            state = "done"
            button.setEnabled(True)
        else:
            # Vérifier si l'étape est accessible (précédente ou dashboard)
            current_order = self.steps[self.current_step]["order"]
            step_order = self.steps[step_name]["order"]
            
            if step_order < current_order or step_name == "dashboard":
                state = "accessible"
                button.setEnabled(True)
            else:
                state = "pending"
                button.setEnabled(False)
                
        # Appliquer l'état
        button.setProperty("state", state)
        
        # Forcer la mise à jour du style
        button.style().unpolish(button)
        button.style().polish(button)
        
    def update_all_states(self):
        """Mise à jour de tous les états des étapes"""
        for step_name in self.steps.keys():
            self.update_step_state(step_name)
            
        # Mise à jour des séparateurs
        self.update_separators()
        
    def update_separators(self):
        """Mise à jour de l'état des séparateurs"""
        sorted_steps = sorted(self.steps.items(), key=lambda x: x[1]["order"])
        
        for i, separator in enumerate(self.separators):
            if i < len(sorted_steps) - 1:
                # Étape actuelle et suivante
                current_step_name = sorted_steps[i][0]
                next_step_name = sorted_steps[i + 1][0]
                
                # État du séparateur basé sur les étapes qu'il relie
                if (current_step_name in self.completed_steps and 
                    next_step_name in self.completed_steps):
                    separator.setProperty("state", "done")
                elif current_step_name == self.current_step:
                    separator.setProperty("state", "active")
                else:
                    separator.setProperty("state", "pending")
                    
                # Forcer la mise à jour du style
                separator.style().unpolish(separator)
                separator.style().polish(separator)
                
    def get_current_step(self):
        """Obtenir l'étape actuelle"""
        return self.current_step
        
    def get_completed_steps(self):
        """Obtenir la liste des étapes complétées"""
        return self.completed_steps.copy()
        
    def get_progress_percentage(self):
        """Obtenir le pourcentage de progression"""
        total_steps = len(self.steps)
        completed_count = len(self.completed_steps)
        
        # Ajouter l'étape actuelle si elle n'est pas déjà complétée
        if self.current_step not in self.completed_steps:
            completed_count += 0.5  # Étape en cours = 50%
            
        return min(100, (completed_count / total_steps) * 100)
        
    def reset_progress(self):
        """Réinitialiser la progression"""
        self.current_step = "dashboard"
        self.completed_steps.clear()
        self.update_all_states()
        
    def set_workflow_mode(self, linear=True):
        """Configurer le mode de workflow
        
        Args:
            linear: Si True, navigation séquentielle uniquement.
                   Si False, navigation libre vers toutes les étapes.
        """
        self.linear_mode = linear
        self.update_all_states()
        
    def get_next_step(self):
        """Obtenir la prochaine étape dans le workflow"""
        current_order = self.steps[self.current_step]["order"]
        max_order = max(step["order"] for step in self.steps.values())
        
        if current_order < max_order:
            # Trouver l'étape suivante
            for step_name, step_data in self.steps.items():
                if step_data["order"] == current_order + 1:
                    return step_name
                    
        return None
        
    def get_previous_step(self):
        """Obtenir l'étape précédente dans le workflow"""
        current_order = self.steps[self.current_step]["order"]
        
        if current_order > 0:
            # Trouver l'étape précédente
            for step_name, step_data in self.steps.items():
                if step_data["order"] == current_order - 1:
                    return step_name
                    
        return None