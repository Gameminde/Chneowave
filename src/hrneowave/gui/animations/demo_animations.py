# -*- coding: utf-8 -*-
"""
Démonstration des Animations Phase 6
CHNeoWave Maritime Design System

Démonstration interactive des animations et micro-interactions :
- Boutons avec feedback
- Cartes avec élévation
- Transitions de pages
- États de chargement
"""

import sys
from typing import Optional

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QFrame, QScrollArea, QGroupBox, QGridLayout
    )
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QFont
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QPushButton, QFrame, QScrollArea, QGroupBox, QGridLayout
        )
        from PyQt6.QtCore import Qt, QTimer
        from PyQt6.QtGui import QFont
    except ImportError:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QPushButton, QFrame, QScrollArea, QGroupBox, QGridLayout
        )
        from PyQt5.QtCore import Qt, QTimer
        from PyQt5.QtGui import QFont

# Import des composants maritimes avec animations
try:
    from ..widgets.maritime.maritime_button import MaritimeButton, PrimaryButton, SecondaryButton
    from ..widgets.maritime.maritime_card import MaritimeCard
    from .animation_system import MaritimeAnimator, AnimationType
    from .micro_interactions import MaritimeMicroInteractions
except ImportError:
    # Fallback pour test standalone
    MaritimeButton = QPushButton
    PrimaryButton = QPushButton
    SecondaryButton = QPushButton
    MaritimeCard = QFrame
    MaritimeAnimator = None
    MaritimeMicroInteractions = None


class AnimationDemoWindow(QMainWindow):
    """
    Fenêtre de démonstration des animations Phase 6.
    
    Sections :
    - Boutons avec micro-interactions
    - Cartes avec élévation
    - États de chargement
    - Feedback de succès/erreur
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHNeoWave - Démonstration Animations Phase 6")
        self.setMinimumSize(1200, 800)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Titre
        self._create_header()
        
        # Zone de démonstration avec scroll
        self._create_demo_area()
        
        # Application du style maritime
        self._apply_maritime_style()
    
    def _create_header(self):
        """Crée l'en-tête de la démonstration."""
        header_layout = QVBoxLayout()
        
        # Titre principal
        title = QLabel("Démonstration Animations Phase 6")
        title.setObjectName("demo_title")
        font = QFont()
        font.setPointSize(24)
        font.setWeight(QFont.Weight.Bold)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Sous-titre
        subtitle = QLabel("Micro-interactions et animations fluides du Design System Maritime")
        subtitle.setObjectName("demo_subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        self.main_layout.addLayout(header_layout)
    
    def _create_demo_area(self):
        """Crée la zone de démonstration avec scroll."""
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Widget de contenu
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)
        
        # Sections de démonstration
        self._create_button_demo(content_layout)
        self._create_card_demo(content_layout)
        self._create_interaction_demo(content_layout)
        
        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area)
    
    def _create_button_demo(self, parent_layout):
        """Démonstration des boutons avec animations."""
        group = QGroupBox("Boutons Maritimes avec Micro-interactions")
        layout = QGridLayout(group)
        layout.setSpacing(15)
        
        # Boutons Primary
        primary_label = QLabel("Boutons Primary :")
        layout.addWidget(primary_label, 0, 0)
        
        primary_btn = PrimaryButton(text="Action Principale")
        primary_btn.clicked.connect(lambda: primary_btn.trigger_success_feedback())
        layout.addWidget(primary_btn, 0, 1)
        
        loading_btn = PrimaryButton(text="Chargement")
        loading_btn.clicked.connect(lambda: self._demo_loading(loading_btn))
        layout.addWidget(loading_btn, 0, 2)
        
        error_btn = PrimaryButton(text="Erreur")
        error_btn.clicked.connect(lambda: error_btn.trigger_error_feedback())
        layout.addWidget(error_btn, 0, 3)
        
        # Boutons Secondary
        secondary_label = QLabel("Boutons Secondary :")
        layout.addWidget(secondary_label, 1, 0)
        
        secondary_btn = SecondaryButton(text="Action Secondaire")
        layout.addWidget(secondary_btn, 1, 1)
        
        cancel_btn = SecondaryButton(text="Annuler")
        layout.addWidget(cancel_btn, 1, 2)
        
        parent_layout.addWidget(group)
    
    def _create_card_demo(self, parent_layout):
        """Démonstration des cartes avec élévation."""
        group = QGroupBox("Cartes Maritimes avec Élévation")
        layout = QHBoxLayout(group)
        layout.setSpacing(20)
        
        # Carte simple
        simple_card = MaritimeCard(title="Carte Simple", elevated=True)
        simple_card.add_widget(QLabel("Contenu de la carte simple avec élévation."))
        layout.addWidget(simple_card)
        
        # Carte cliquable
        clickable_card = MaritimeCard(title="Carte Cliquable", elevated=True, clickable=True)
        clickable_card.add_widget(QLabel("Cette carte est cliquable avec animations."))
        clickable_card.clicked.connect(lambda: print("Carte cliquée!"))
        layout.addWidget(clickable_card)
        
        # Carte avec contenu complexe
        complex_card = MaritimeCard(title="Carte Complexe", elevated=True)
        complex_content = QVBoxLayout()
        complex_content.addWidget(QLabel("Titre du contenu"))
        complex_content.addWidget(QLabel("Description détaillée du contenu de la carte."))
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(PrimaryButton(text="Action"))
        btn_layout.addWidget(SecondaryButton(text="Annuler"))
        complex_content.addLayout(btn_layout)
        
        complex_widget = QWidget()
        complex_widget.setLayout(complex_content)
        complex_card.add_widget(complex_widget)
        layout.addWidget(complex_card)
        
        parent_layout.addWidget(group)
    
    def _create_interaction_demo(self, parent_layout):
        """Démonstration des interactions avancées."""
        group = QGroupBox("Interactions Avancées")
        layout = QVBoxLayout(group)
        
        # Description
        desc = QLabel("Testez les différentes interactions :")
        layout.addWidget(desc)
        
        # Boutons de test
        test_layout = QHBoxLayout()
        
        hover_btn = PrimaryButton(text="Survol")
        hover_btn.setToolTip("Survolez ce bouton pour voir l'animation")
        test_layout.addWidget(hover_btn)
        
        press_btn = PrimaryButton(text="Pression")
        press_btn.setToolTip("Cliquez et maintenez pour voir l'effet")
        test_layout.addWidget(press_btn)
        
        focus_btn = PrimaryButton(text="Focus")
        focus_btn.setToolTip("Utilisez Tab pour naviguer et voir le focus")
        test_layout.addWidget(focus_btn)
        
        layout.addLayout(test_layout)
        
        parent_layout.addWidget(group)
    
    def _demo_loading(self, button):
        """Démonstration de l'état de chargement."""
        button.set_loading(True)
        
        # Simuler un processus de 3 secondes
        QTimer.singleShot(3000, lambda: button.set_loading(False))
    
    def _apply_maritime_style(self):
        """Applique le style maritime à la fenêtre."""
        style = """
        QMainWindow {
            background-color: #F5F7FA;
        }
        
        QLabel#demo_title {
            color: #0A1929;
            margin: 20px 0;
        }
        
        QLabel#demo_subtitle {
            color: #37474F;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        QGroupBox {
            font-weight: 600;
            font-size: 16px;
            color: #1565C0;
            border: 2px solid #E3F2FD;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 15px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px 0 10px;
        }
        
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        """
        
        self.setStyleSheet(style)


def main():
    """Point d'entrée de la démonstration."""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("CHNeoWave Animation Demo")
    app.setApplicationVersion("1.0.0")
    
    # Fenêtre principale
    window = AnimationDemoWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())