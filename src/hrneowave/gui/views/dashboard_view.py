# -*- coding: utf-8 -*-
"""
Dashboard View

Vue dashboard principale avec cartes proportionnées selon φ et actions rapides.
Point d'entrée principal de l'application CHNeoWave.

Auteur: CHNeoWave Team
Version: 1.1.0-RC
Date: 2024-12-19
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QFrame, QSpacerItem, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QPixmap

from ..components.phi_card import PhiCard


class DashboardView(QWidget):
    """Vue dashboard avec cartes proportionnées selon φ
    
    Fonctionnalités:
    - Cartes projet, acquisition, système avec ratios φ
    - Grille basée sur les espacements Fibonacci
    - Boutons d'action rapide
    - Informations système en temps réel
    - Navigation vers les autres vues
    """
    
    # Signaux pour navigation
    projectRequested = Signal()
    acquisitionRequested = Signal()
    calibrationRequested = Signal()
    analysisRequested = Signal()
    exportRequested = Signal()
    
    # Espacements Fibonacci
    SPACING_SM = 8
    SPACING_MD = 13
    SPACING_LG = 21
    SPACING_XL = 34
    SPACING_XXL = 55
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration du dashboard avec grille φ"""
        self.setObjectName("dashboard-view")
        
        # Scroll area pour contenu défilant
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget principal du contenu
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        # Layout du contenu avec marges Fibonacci
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(self.SPACING_XL, self.SPACING_XL, self.SPACING_XL, self.SPACING_XL)
        layout.setSpacing(self.SPACING_LG)
        
        # En-tête du dashboard
        self.create_header(layout)

        # Grille de cartes φ
        phi_grid = self.create_phi_grid()
        layout.addLayout(phi_grid)
        
        # Spacer pour pousser le contenu vers le haut
        layout.addStretch()
        
    def create_header(self, layout):
        """Création de l'en-tête du dashboard"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(self.SPACING_SM)
        
        # Titre principal
        title = QLabel("CHNeoWave - Laboratoire Maritime")
        title.setObjectName("dashboard-title")
        title.setAlignment(Qt.AlignCenter)
        
        # Font du titre
        title_font = QFont()
        title_font.setWeight(QFont.Bold)
        title_font.setPointSize(24)
        title.setFont(title_font)
        
        header_layout.addWidget(title)
        
        # Sous-titre
        subtitle = QLabel("Système d'acquisition et d'analyse des vagues en modèle réduit")
        subtitle.setObjectName("dashboard-subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        
        # Font du sous-titre
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_widget)
        
    def create_phi_grid(self):
        """Création de la grille avec proportions φ"""
        grid = QGridLayout()
        grid.setSpacing(self.SPACING_LG)  # Espacement Fibonacci 21
        
        # Carte Projet (377×233 - ratio φ) - Position dominante
        self.project_card = PhiCard.create_project_card()
        self.project_card.clicked.connect(self.projectRequested.emit)
        grid.addWidget(self.project_card, 0, 0, 2, 1)  # Span 2 lignes
        
        # Carte Acquisition (233×144 - ratio φ) - En haut à droite
        self.acquisition_card = PhiCard.create_acquisition_card()
        self.acquisition_card.clicked.connect(self.acquisitionRequested.emit)
        grid.addWidget(self.acquisition_card, 0, 1)
        
        # Carte Système (233×144 - ratio φ) - En bas à droite
        self.system_card = PhiCard.create_system_card()
        self.system_card.clicked.connect(self.show_system_info)
        grid.addWidget(self.system_card, 1, 1)
        
        # Configuration des proportions de colonnes selon φ
        # Colonne 0 (projet): φ parts, Colonne 1 (acquisition/système): 1 part
        grid.setColumnStretch(0, 162)  # φ * 100 ≈ 162
        grid.setColumnStretch(1, 100)  # 1 * 100 = 100
        
        return grid
        
    def create_quick_actions(self):
        """Création des boutons d'action rapide"""
        actions_widget = QWidget()
        actions_layout = QVBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(self.SPACING_MD)
        
        # Titre de la section
        actions_title = QLabel("Actions Rapides")
        actions_title.setObjectName("dashboard-section-title")
        
        # Font du titre de section
        section_font = QFont()
        section_font.setWeight(QFont.Bold)
        section_font.setPointSize(16)
        actions_title.setFont(section_font)
        
        actions_layout.addWidget(actions_title)
        
        # Grille de boutons d'action
        buttons_grid = QGridLayout()
        buttons_grid.setSpacing(self.SPACING_MD)
        
        # Boutons d'action avec icônes
        actions = [
            ("🚀 Démarrer Acquisition", "Lancer une nouvelle session d'acquisition", self.acquisitionRequested.emit),
            ("📁 Ouvrir Projet", "Charger un projet existant", self.projectRequested.emit),
            ("⚙️ Calibrer Sondes", "Calibration des capteurs", self.calibrationRequested.emit),
            ("📊 Derniers Rapports", "Consulter les analyses récentes", self.analysisRequested.emit)
        ]
        
        for i, (text, tooltip, signal) in enumerate(actions):
            button = QPushButton(text)
            button.setObjectName("dashboard-action-button")
            button.setToolTip(tooltip)
            button.setMinimumHeight(self.SPACING_XXL)  # Fibonacci 55
            
            # Font des boutons
            button_font = QFont()
            button_font.setPointSize(11)
            button.setFont(button_font)
            
            # Connexion du signal
            button.clicked.connect(signal)
            
            # Placement en grille 2×2
            row = i // 2
            col = i % 2
            buttons_grid.addWidget(button, row, col)
            
        actions_layout.addLayout(buttons_grid)
        
        return actions_widget
        
    def create_system_info(self):
        """Création de la section informations système"""
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(self.SPACING_SM)
        
        # Titre de la section
        info_title = QLabel("État du Système")
        info_title.setObjectName("dashboard-section-title")
        
        # Font du titre
        section_font = QFont()
        section_font.setWeight(QFont.Bold)
        section_font.setPointSize(16)
        info_title.setFont(section_font)
        
        info_layout.addWidget(info_title)
        
        # Grille d'informations
        info_grid = QGridLayout()
        info_grid.setSpacing(self.SPACING_SM)
        
        # Informations système
        system_infos = [
            ("Version:", "CHNeoWave v1.1.0-RC"),
            ("Statut:", "🟢 Opérationnel"),
            ("Dernière MAJ:", "2024-12-19"),
            ("Capteurs:", "✅ Connectés")
        ]
        
        for i, (label, value) in enumerate(system_infos):
            # Label
            label_widget = QLabel(label)
            label_widget.setObjectName("dashboard-info-label")
            info_grid.addWidget(label_widget, i, 0)
            
            # Valeur
            value_widget = QLabel(value)
            value_widget.setObjectName("dashboard-info-value")
            info_grid.addWidget(value_widget, i, 1)
            
        # Configuration des colonnes
        info_grid.setColumnStretch(0, 30)  # Labels
        info_grid.setColumnStretch(1, 70)  # Valeurs
        
        info_layout.addLayout(info_grid)
        
        return info_widget
        
    def setup_refresh_timer(self):
        """Configuration du timer de rafraîchissement"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_system_info)
        self.refresh_timer.start(5000)  # Rafraîchir toutes les 5 secondes
        
    def refresh_system_info(self):
        """Rafraîchissement des informations système"""
        # Mise à jour des cartes avec informations actuelles
        if self.system_card:
            # Simuler la récupération d'informations système
            import datetime
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.system_card.set_content(f"Statut: Opérationnel\nMAJ: {current_time}")
            
    def update_project_info(self, project_name, status="Ouvert"):
        """Mise à jour des informations du projet"""
        if self.project_card:
            self.project_card.set_content(f"{project_name}\nStatut: {status}")
            
    def update_acquisition_status(self, status, last_run="Maintenant"):
        """Mise à jour du statut d'acquisition"""
        if self.acquisition_card:
            self.acquisition_card.set_content(f"Statut: {status}\nDernière: {last_run}")
            
    def show_system_info(self):
        """Afficher les informations détaillées du système"""
        # Pour l'instant, émettre un signal vers les paramètres
        # Peut être étendu avec une dialog d'informations système
        pass
        
    def get_phi_validation(self):
        """Validation des proportions φ des cartes"""
        validation_results = []
        
        cards = [self.project_card, self.acquisition_card, self.system_card]
        card_names = ["Projet", "Acquisition", "Système"]
        
        for card, name in zip(cards, card_names):
            if card:
                info = card.get_size_info()
                validation_results.append({
                    "name": name,
                    "size": info["size"],
                    "ratio": info["ratio"],
                    "phi_exact": info["phi_exact"],
                    "error": info["ratio_error"],
                    "valid": info["ratio_error"] < 0.01
                })
                
        return validation_results
        
    def get_fibonacci_validation(self):
        """Validation des espacements Fibonacci"""
        layout = self.layout().itemAt(0).widget().widget().layout()  # Accès au layout du contenu
        
        return {
            "margins": layout.contentsMargins().left(),  # Devrait être 34
            "spacing": layout.spacing(),  # Devrait être 21
            "expected_margin": self.SPACING_XL,
            "expected_spacing": self.SPACING_LG,
            "margin_valid": layout.contentsMargins().left() == self.SPACING_XL,
            "spacing_valid": layout.spacing() == self.SPACING_LG
        }