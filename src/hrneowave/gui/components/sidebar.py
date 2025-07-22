# -*- coding: utf-8 -*-
"""
Sidebar Navigation Component

Composant de navigation sidebar verticale avec états visuels et navigation clavier.
Basé sur les proportions Fibonacci et le système de design CHNeoWave.

Auteur: CHNeoWave Team
Version: 1.1.0-RC
Date: 2024-12-19
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QKeyEvent, QFont


class Sidebar(QWidget):
    """Sidebar verticale avec navigation et états visuels
    
    Fonctionnalités:
    - Navigation entre les vues principales
    - États visuels: active, done, pending
    - Support navigation clavier (← →)
    - Animation collapse/expand
    - Proportions basées sur Fibonacci
    """
    
    # Signaux
    navigationRequested = Signal(str)  # Nom de la vue demandée
    
    # Constantes Fibonacci pour dimensions
    WIDTH_COLLAPSED = 55   # Fibonacci 55
    WIDTH_EXPANDED = 233   # Fibonacci 233
    ITEM_HEIGHT = 55       # Fibonacci 55
    ICON_SIZE = 21         # Fibonacci 21
    SPACING = 8            # Fibonacci 8
    MARGIN = 13            # Fibonacci 13
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.expanded = True
        self.current_step = "dashboard"
        self.completed_steps = set()
        self.nav_buttons = {}
        
        self.setup_ui()
        self.setup_keyboard_navigation()
        self.setup_animations()
        
    def setup_ui(self):
        """Configuration de l'interface sidebar"""
        self.setObjectName("sidebar")
        self.setFixedWidth(self.WIDTH_EXPANDED)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Layout principal vertical
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header avec logo
        self.create_header(layout)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("sidebar-separator")
        layout.addWidget(separator)
        
        # Navigation items
        self.create_navigation_items(layout)
        
        # Spacer pour pousser le footer en bas
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        # Footer avec paramètres
        self.create_footer(layout)
        
    def create_header(self, layout):
        """Création de l'en-tête avec logo"""
        header_widget = QWidget()
        header_widget.setFixedHeight(self.ITEM_HEIGHT + self.MARGIN)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        
        # Logo/Icône
        logo_label = QLabel("🌊")
        logo_label.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # Titre (masqué si collapsed)
        self.title_label = QLabel("CHNeoWave")
        self.title_label.setObjectName("sidebar-title")
        font = QFont()
        font.setWeight(QFont.Bold)
        self.title_label.setFont(font)
        header_layout.addWidget(self.title_label)
        
        layout.addWidget(header_widget)
        
    def create_navigation_items(self, layout):
        """Création des éléments de navigation"""
        self.nav_items = {
            "dashboard": {"icon": "🏠", "label": "Dashboard", "order": 0},
            "welcome": {"icon": "👋", "label": "Projet", "order": 1},
            "calibration": {"icon": "⚙️", "label": "Calibration", "order": 2},
            "acquisition": {"icon": "📊", "label": "Acquisition", "order": 3},
            "analysis": {"icon": "📈", "label": "Analyse", "order": 4},
            "export": {"icon": "💾", "label": "Export", "order": 5}
        }
        
        # Conteneur pour les boutons de navigation
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, self.SPACING, 0, 0)
        nav_layout.setSpacing(self.SPACING // 2)
        
        # Création des boutons dans l'ordre
        sorted_items = sorted(self.nav_items.items(), key=lambda x: x[1]["order"])
        for step_name, item_data in sorted_items:
            nav_button = self.create_nav_button(step_name, item_data)
            self.nav_buttons[step_name] = nav_button
            nav_layout.addWidget(nav_button)
            
        layout.addWidget(nav_container)
        
    def create_nav_button(self, step_name, item_data):
        """Création d'un bouton de navigation avec états visuels"""
        button = QPushButton()
        button.setObjectName("sidebar-nav-button")
        button.setFixedHeight(self.ITEM_HEIGHT)
        button.setFocusPolicy(Qt.StrongFocus)
        
        # Layout horizontal pour icône + texte
        layout = QHBoxLayout(button)
        layout.setContentsMargins(self.MARGIN, self.SPACING, self.MARGIN, self.SPACING)
        layout.setSpacing(self.SPACING)
        
        # Icône
        icon_label = QLabel(item_data["icon"])
        icon_label.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Texte (masqué si sidebar collapsed)
        text_label = QLabel(item_data["label"])
        text_label.setVisible(self.expanded)
        layout.addWidget(text_label)
        
        # Spacer pour aligner à gauche
        layout.addStretch()
        
        # États visuels selon progression
        self.update_button_state(button, step_name)
        
        # Connexion signal
        button.clicked.connect(lambda: self.navigate_to(step_name))
        
        return button
        
    def create_footer(self, layout):
        """Création du footer avec bouton paramètres"""
        footer_widget = QWidget()
        footer_widget.setFixedHeight(self.ITEM_HEIGHT)
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(self.MARGIN, self.SPACING, self.MARGIN, self.SPACING)
        
        # Bouton paramètres
        settings_button = QPushButton()
        settings_button.setObjectName("sidebar-settings-button")
        settings_button.setFixedHeight(self.ITEM_HEIGHT - self.SPACING)
        
        settings_layout = QHBoxLayout(settings_button)
        settings_layout.setContentsMargins(self.SPACING, 0, self.SPACING, 0)
        
        # Icône paramètres
        settings_icon = QLabel("⚙️")
        settings_icon.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        settings_icon.setAlignment(Qt.AlignCenter)
        settings_layout.addWidget(settings_icon)
        
        # Texte paramètres
        self.settings_label = QLabel("Paramètres")
        self.settings_label.setVisible(self.expanded)
        settings_layout.addWidget(self.settings_label)
        
        footer_layout.addWidget(settings_button)
        layout.addWidget(footer_widget)
        
    def setup_keyboard_navigation(self):
        """Configuration de la navigation clavier"""
        self.setFocusPolicy(Qt.StrongFocus)
        
    def setup_animations(self):
        """Configuration des animations"""
        self.width_animation = QPropertyAnimation(self, b"maximumWidth")
        self.width_animation.setDuration(233)  # Fibonacci 233ms
        self.width_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def keyPressEvent(self, event: QKeyEvent):
        """Gestion des événements clavier pour navigation"""
        if event.key() == Qt.Key_Left:
            self.navigate_previous()
        elif event.key() == Qt.Key_Right:
            self.navigate_next()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Activer l'élément sélectionné
            self.navigate_to(self.current_step)
        else:
            super().keyPressEvent(event)
            
    def navigate_previous(self):
        """Navigation vers l'élément précédent"""
        current_order = self.nav_items[self.current_step]["order"]
        if current_order > 0:
            # Trouver l'élément précédent
            for step_name, item_data in self.nav_items.items():
                if item_data["order"] == current_order - 1:
                    self.set_current_step(step_name)
                    break
                    
    def navigate_next(self):
        """Navigation vers l'élément suivant"""
        current_order = self.nav_items[self.current_step]["order"]
        max_order = max(item["order"] for item in self.nav_items.values())
        if current_order < max_order:
            # Trouver l'élément suivant
            for step_name, item_data in self.nav_items.items():
                if item_data["order"] == current_order + 1:
                    self.set_current_step(step_name)
                    break
                    
    def navigate_to(self, step_name):
        """Navigation vers une vue spécifique"""
        if step_name in self.nav_items:
            self.set_current_step(step_name)
            self.navigationRequested.emit(step_name)
            
    def set_current_step(self, step_name):
        """Définir l'étape actuelle"""
        if step_name in self.nav_items:
            self.current_step = step_name
            self.update_all_button_states()
            
    def mark_step_completed(self, step_name):
        """Marquer une étape comme complétée"""
        if step_name in self.nav_items:
            self.completed_steps.add(step_name)
            self.update_button_state(self.nav_buttons[step_name], step_name)
            
    def mark_step_pending(self, step_name):
        """Marquer une étape comme en attente"""
        if step_name in self.nav_items:
            self.completed_steps.discard(step_name)
            self.update_button_state(self.nav_buttons[step_name], step_name)
            
    def update_button_state(self, button, step_name):
        """Mise à jour de l'état visuel du bouton"""
        if step_name == self.current_step:
            button.setProperty("state", "active")
        elif step_name in self.completed_steps:
            button.setProperty("state", "done")
        else:
            button.setProperty("state", "pending")
            
        # Forcer la mise à jour du style
        button.style().unpolish(button)
        button.style().polish(button)
        
    def update_all_button_states(self):
        """Mise à jour de tous les états des boutons"""
        for step_name, button in self.nav_buttons.items():
            self.update_button_state(button, step_name)
            
    def toggle_expanded(self):
        """Basculer entre état étendu/réduit"""
        self.expanded = not self.expanded
        
        # Animation de la largeur
        target_width = self.WIDTH_EXPANDED if self.expanded else self.WIDTH_COLLAPSED
        self.width_animation.setStartValue(self.width())
        self.width_animation.setEndValue(target_width)
        self.width_animation.start()
        
        # Masquer/afficher les textes
        self.title_label.setVisible(self.expanded)
        self.settings_label.setVisible(self.expanded)
        
        for button in self.nav_buttons.values():
            # Trouver le label de texte dans le bouton
            for child in button.findChildren(QLabel):
                if child.text() != "":
                    # C'est probablement le label de texte (pas l'icône)
                    if not any(emoji in child.text() for emoji in ["🏠", "👋", "⚙️", "📊", "📈", "💾"]):
                        child.setVisible(self.expanded)
                        
    def get_current_step(self):
        """Obtenir l'étape actuelle"""
        return self.current_step
        
    def get_completed_steps(self):
        """Obtenir la liste des étapes complétées"""
        return self.completed_steps.copy()
        
    def is_expanded(self):
        """Vérifier si la sidebar est étendue"""
        return self.expanded