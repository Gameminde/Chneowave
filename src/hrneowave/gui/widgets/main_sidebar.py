# -*- coding: utf-8 -*-
"""
Main Sidebar Widget - Maritime Theme 2025
Barre latérale de navigation principale avec design maritime
"""

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFont, QIcon, QPainter, QColor, QLinearGradient

# Golden Ratio Constants
FIBONACCI_SPACING = [8, 13, 21, 34, 55, 89]

class NavigationButton(QPushButton):
    """
    Bouton de navigation personnalisé avec animations
    """
    
    def __init__(self, text: str, icon_text: str = "", is_active: bool = False, parent=None):
        super().__init__(parent)
        
        self.button_text = text
        self.icon_text = icon_text
        self.is_active = is_active
        self.is_hovered = False
        
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Configure l'interface du bouton"""
        self.setObjectName("nav_button")
        self.setFixedHeight(55)  # Fibonacci
        self.setCheckable(True)
        self.setChecked(self.is_active)
        
        # Layout horizontal pour icône + texte
        layout = QHBoxLayout(self)
        layout.setContentsMargins(FIBONACCI_SPACING[1], FIBONACCI_SPACING[1], 
                                 FIBONACCI_SPACING[1], FIBONACCI_SPACING[1])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Icône (emoji ou caractère)
        if self.icon_text:
            self.icon_label = QLabel(self.icon_text)
            self.icon_label.setFont(QFont("Segoe UI Emoji", 16))
            self.icon_label.setFixedWidth(FIBONACCI_SPACING[3])
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.icon_label)
        
        # Texte
        self.text_label = QLabel(self.button_text)
        self.text_label.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        layout.addWidget(self.text_label)
        
        layout.addStretch()
        
        self.apply_style()
        
    def setup_animations(self):
        """Configure les animations du bouton"""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def apply_style(self):
        """Applique le style selon l'état"""
        if self.is_active:
            # État actif
            self.setStyleSheet("""
                QPushButton#nav_button {
                    background-color: #00ACC1;
                    color: #F5FBFF;
                    border: none;
                    border-radius: 13px;
                    padding: 8px 13px;
                    text-align: left;
                }
                
                QPushButton#nav_button:hover {
                    background-color: #0097A7;
                }
                
                QLabel {
                    background-color: transparent;
                    color: #F5FBFF;
                }
            """)
        else:
            # État normal
            self.setStyleSheet("""
                QPushButton#nav_button {
                    background-color: transparent;
                    color: #445868;
                    border: none;
                    border-radius: 13px;
                    padding: 8px 13px;
                    text-align: left;
                }
                
                QPushButton#nav_button:hover {
                    background-color: rgba(0, 172, 193, 0.1);
                    color: #00ACC1;
                }
                
                QLabel {
                    background-color: transparent;
                    color: inherit;
                }
            """)
            
    def set_active(self, active: bool):
        """Définit l'état actif du bouton"""
        self.is_active = active
        self.setChecked(active)
        self.apply_style()
        
    def enterEvent(self, event):
        """Gestionnaire d'entrée de la souris"""
        super().enterEvent(event)
        self.is_hovered = True
        
    def leaveEvent(self, event):
        """Gestionnaire de sortie de la souris"""
        super().leaveEvent(event)
        self.is_hovered = False


class MainSidebar(QFrame):
    """
    Barre latérale principale de navigation
    Design maritime avec Golden Ratio
    """
    
    # Signaux
    navigation_requested = Signal(str)  # Nom de la vue demandée
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_view = "dashboard"  # Vue active
        self.navigation_buttons = {}
        self.is_collapsed = False
        
        self.setup_ui()
        self.setup_navigation()
        
    def setup_ui(self):
        """Configure l'interface de la sidebar"""
        self.setObjectName("main_sidebar")
        self.setFixedWidth(250)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === HEADER avec logo ===
        self.setup_header(main_layout)
        
        # === NAVIGATION PRINCIPALE ===
        self.setup_navigation_area(main_layout)
        
        # === FOOTER avec informations ===
        self.setup_footer(main_layout)
        
        # Style de base
        self.setStyleSheet("""
            QFrame#main_sidebar {
                background-color: #F5FBFF;
                border-right: 2px solid #E0E7FF;
            }
        """)
        
    def setup_header(self, parent_layout):
        """Configure l'en-tête avec logo et titre"""
        header_frame = QFrame()
        header_frame.setObjectName("sidebar_header")
        header_frame.setFixedHeight(89)  # Fibonacci
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                        FIBONACCI_SPACING[2], FIBONACCI_SPACING[1])
        header_layout.setSpacing(FIBONACCI_SPACING[0])
        
        # Logo/Icône
        logo_label = QLabel("🌊")
        logo_label.setFont(QFont("Segoe UI Emoji", 32))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Titre
        title_label = QLabel("CHNeoWave")
        title_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #0A1929;")
        
        # Version
        version_label = QLabel("v2025.1")
        version_label.setFont(QFont("Inter", 10))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #445868;")
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addWidget(version_label)
        
        # Style du header
        header_frame.setStyleSheet("""
            QFrame#sidebar_header {
                background-color: #F5FBFF;
                border-bottom: 1px solid #E0E7FF;
            }
        """)
        
        parent_layout.addWidget(header_frame)
        
    def setup_navigation_area(self, parent_layout):
        """Configure la zone de navigation"""
        # Scroll area pour la navigation
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Widget conteneur
        nav_widget = QWidget()
        self.nav_layout = QVBoxLayout(nav_widget)
        self.nav_layout.setContentsMargins(FIBONACCI_SPACING[1], FIBONACCI_SPACING[2], 
                                          FIBONACCI_SPACING[1], FIBONACCI_SPACING[1])
        self.nav_layout.setSpacing(FIBONACCI_SPACING[0])
        
        scroll_area.setWidget(nav_widget)
        parent_layout.addWidget(scroll_area)
        
    def setup_navigation(self):
        """Configure les boutons de navigation"""
        # Définition des vues
        navigation_items = [
            {"name": "dashboard", "text": "Tableau de Bord", "icon": "📊", "active": True},
            {"name": "calibration", "text": "Calibration", "icon": "⚙️", "active": False},
            {"name": "acquisition", "text": "Acquisition", "icon": "📡", "active": False},
            {"name": "analysis", "text": "Analyse", "icon": "📈", "active": False},
            {"name": "report", "text": "Rapport", "icon": "📋", "active": False},
        ]
        
        # Séparateur - Navigation principale
        main_section = QLabel("NAVIGATION")
        main_section.setFont(QFont("Inter", 10, QFont.Weight.Bold))
        main_section.setStyleSheet("color: #445868; margin: 13px 0 8px 0;")
        self.nav_layout.addWidget(main_section)
        
        # Création des boutons
        for item in navigation_items:
            button = NavigationButton(
                text=item["text"],
                icon_text=item["icon"],
                is_active=item["active"]
            )
            
            # Connexion du signal
            button.clicked.connect(lambda checked, name=item["name"]: self.navigate_to(name))
            
            self.navigation_buttons[item["name"]] = button
            self.nav_layout.addWidget(button)
            
        # Spacer
        self.nav_layout.addSpacerItem(
            QSpacerItem(20, FIBONACCI_SPACING[2], QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        
        # Séparateur - Outils
        tools_section = QLabel("OUTILS")
        tools_section.setFont(QFont("Inter", 10, QFont.Weight.Bold))
        tools_section.setStyleSheet("color: #445868; margin: 13px 0 8px 0;")
        self.nav_layout.addWidget(tools_section)
        
        # Boutons d'outils
        tool_items = [
            {"name": "preferences", "text": "Préférences", "icon": "⚙️"},
            {"name": "help", "text": "Aide", "icon": "❓"},
            {"name": "about", "text": "À propos", "icon": "ℹ️"}
        ]
        
        for item in tool_items:
            button = NavigationButton(
                text=item["text"],
                icon_text=item["icon"],
                is_active=False
            )
            
            button.clicked.connect(lambda checked, name=item["name"]: self.navigate_to(name))
            self.navigation_buttons[item["name"]] = button
            self.nav_layout.addWidget(button)
            
    def setup_footer(self, parent_layout):
        """Configure le pied de page"""
        footer_frame = QFrame()
        footer_frame.setObjectName("sidebar_footer")
        footer_frame.setFixedHeight(55)  # Fibonacci
        
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(FIBONACCI_SPACING[1], FIBONACCI_SPACING[1], 
                                        FIBONACCI_SPACING[1], FIBONACCI_SPACING[1])
        footer_layout.setSpacing(FIBONACCI_SPACING[0])
        
        # Statut de connexion
        status_layout = QHBoxLayout()
        
        status_indicator = QLabel("●")
        status_indicator.setFont(QFont("Arial", 12))
        status_indicator.setStyleSheet("color: #4CAF50;")  # Vert pour connecté
        
        status_text = QLabel("Système connecté")
        status_text.setFont(QFont("Inter", 10))
        status_text.setStyleSheet("color: #445868;")
        
        status_layout.addWidget(status_indicator)
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        
        footer_layout.addLayout(status_layout)
        
        # Style du footer
        footer_frame.setStyleSheet("""
            QFrame#sidebar_footer {
                background-color: #F5FBFF;
                border-top: 1px solid #E0E7FF;
            }
        """)
        
        parent_layout.addWidget(footer_frame)
        
    def navigate_to(self, view_name: str):
        """Navigue vers une vue spécifique"""
        # Désactiver l'ancien bouton
        if self.current_view in self.navigation_buttons:
            self.navigation_buttons[self.current_view].set_active(False)
            
        # Activer le nouveau bouton
        if view_name in self.navigation_buttons:
            self.navigation_buttons[view_name].set_active(True)
            
        # Mettre à jour la vue actuelle
        self.current_view = view_name
        
        # Émettre le signal de navigation
        self.navigation_requested.emit(view_name)
        
    def set_active_view(self, view_name: str):
        """Définit la vue active depuis l'extérieur"""
        if view_name != self.current_view:
            self.navigate_to(view_name)
            
    def get_active_view(self) -> str:
        """Retourne la vue actuellement active"""
        return self.current_view
        
    def set_theme(self, is_dark: bool):
        """Applique le thème sombre ou clair"""
        if is_dark:
            # Thème sombre
            self.setStyleSheet("""
                QFrame#main_sidebar {
                    background-color: #0A1929;
                    border-right: 2px solid #2B79B6;
                }
                
                QFrame#sidebar_header {
                    background-color: #0A1929;
                    border-bottom: 1px solid #2B79B6;
                }
                
                QFrame#sidebar_footer {
                    background-color: #0A1929;
                    border-top: 1px solid #2B79B6;
                }
                
                QLabel {
                    color: #F5FBFF;
                }
            """)
        else:
            # Thème clair (défaut)
            self.setStyleSheet("""
                QFrame#main_sidebar {
                    background-color: #F5FBFF;
                    border-right: 2px solid #E0E7FF;
                }
                
                QFrame#sidebar_header {
                    background-color: #F5FBFF;
                    border-bottom: 1px solid #E0E7FF;
                }
                
                QFrame#sidebar_footer {
                    background-color: #F5FBFF;
                    border-top: 1px solid #E0E7FF;
                }
            """)
            
        # Mettre à jour les boutons
        for button in self.navigation_buttons.values():
            button.apply_style()
            
    def collapse_sidebar(self, collapsed: bool):
        """Réduit ou étend la sidebar"""
        self.is_collapsed = collapsed
        
        if collapsed:
            self.setFixedWidth(55)  # Largeur réduite
            # Cacher les textes, garder seulement les icônes
            for button in self.navigation_buttons.values():
                if hasattr(button, 'text_label'):
                    button.text_label.hide()
        else:
            self.setFixedWidth(250)  # Largeur normale
            # Montrer les textes
            for button in self.navigation_buttons.values():
                if hasattr(button, 'text_label'):
                    button.text_label.show()
                    
    def update_connection_status(self, connected: bool, message: str = ""):
        """Met à jour le statut de connexion"""
        # Cette méthode peut être étendue pour mettre à jour le footer
        pass