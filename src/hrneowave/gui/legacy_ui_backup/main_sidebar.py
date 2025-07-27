# -*- coding: utf-8 -*-
"""
main_sidebar.py

Widget de la barre latérale principale pour la navigation.
S'inspire de la structure de `interface.html`.
"""

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon

log = logging.getLogger(__name__)

class MainSidebar(QWidget):
    """Barre latérale de navigation principale de l'application."""
    navigation_requested = Signal(str)  # Émet le nom de la vue demandée

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("mainSidebar")
        self._setup_ui()

    def _setup_ui(self):
        """Construit l'interface de la barre latérale."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Header ---
        header = self._create_header()
        main_layout.addWidget(header)

        # --- Navigation ---
        nav_frame = QFrame()
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 24, 0, 24)
        nav_layout.setSpacing(4)

        # Section: Principal
        nav_layout.addWidget(self._create_section_title("Principal"))
        nav_layout.addWidget(self._create_nav_button("Accueil", "fa.home", "welcome"))
        nav_layout.addWidget(self._create_nav_button("Tableau de bord", "fa.tachometer-alt", "dashboard"))

        # Section: Workflow
        nav_layout.addSpacing(24)
        nav_layout.addWidget(self._create_section_title("Workflow"))
        nav_layout.addWidget(self._create_nav_button("Calibration", "fa.sliders-h", "manual_calibration"))
        nav_layout.addWidget(self._create_nav_button("Acquisition", "fa.wave-square", "acquisition"))
        nav_layout.addWidget(self._create_nav_button("Analyse", "fa.chart-line", "analysis"))
        nav_layout.addWidget(self._create_nav_button("Paramètres", "fa.cog", "project_settings"))

        # Section: Système
        nav_layout.addSpacing(24)
        nav_layout.addWidget(self._create_section_title("Système"))
        nav_layout.addWidget(self._create_nav_button("Réglages", "fa.cog", "settings"))
        nav_layout.addWidget(self._create_nav_button("Aide", "fa.question-circle", "help"))
        
        nav_layout.addStretch()
        main_layout.addWidget(nav_frame)

    def _create_header(self) -> QWidget:
        """Crée l'en-tête avec le logo et le titre."""
        header_widget = QWidget()
        header_widget.setObjectName("sidebarHeader")
        layout = QVBoxLayout(header_widget)
        
        logo_text = QLabel("CHNeoWave")
        logo_text.setObjectName("logoText")
        logo_text.setStyleSheet("font-size: 20px; font-weight: bold; color: white; padding: 24px 20px;")
        
        layout.addWidget(logo_text)
        return header_widget

    def _create_section_title(self, text: str) -> QLabel:
        """Crée un titre de section pour la navigation."""
        label = QLabel(text.upper())
        label.setObjectName("navSectionTitle")
        label.setStyleSheet("font-size: 12px; font-weight: bold; color: #71717a; padding: 0 20px 8px 20px; letter-spacing: 1px;")
        return label

    def _create_nav_button(self, text: str, icon_name: str, view_name: str) -> QPushButton:
        """Crée un bouton de navigation."""
        button = QPushButton(f"  {text}")
        button.setCheckable(True)
        button.setAutoExclusive(True)
        # Note: L'icône FontAwesome n'est pas gérée nativement. 
        # Cela nécessiterait une bibliothèque comme qtawesome.
        # button.setIcon(QIcon(f":/icons/{icon_name}.svg")) 
        button.clicked.connect(lambda: self.navigation_requested.emit(view_name))
        return button

    def set_active_view(self, view_name: str):
        """Met à jour le bouton actif dans la barre latérale."""
        for button in self.findChildren(QPushButton):
            # Ceci est une simplification. Une vraie implémentation mapperait view_name au bouton.
            if button.text().strip().lower() == view_name.lower():
                button.setChecked(True)
                break