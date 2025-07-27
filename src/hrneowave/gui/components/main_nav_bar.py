# -*- coding: utf-8 -*-
"""
Main Navigation Bar Component

Barre de navigation principale horizontale.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal

class MainNavBar(QWidget):
    """Barre de navigation principale horizontale."""
    navigationRequested = Signal(str)  # Nom de la vue demandée

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_buttons = {}
        self.setup_ui()

    def setup_ui(self):
        """Configuration de l'interface de la barre de navigation."""
        self.setObjectName("mainNavBar")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        nav_items = ["Accueil", "Calibration", "Acquisition", "Traitement & Analyse", "Rapport Final"]

        for item_name in nav_items:
            button = QPushButton(item_name)
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.clicked.connect(lambda checked, name=item_name: self.on_button_clicked(name))
            self.nav_buttons[item_name] = button
            layout.addWidget(button)
        
        layout.addStretch()

        # Set Accueil as active by default
        if "Accueil" in self.nav_buttons:
            self.nav_buttons["Accueil"].setChecked(True)

    def on_button_clicked(self, view_name: str):
        """Gère le clic sur un bouton de navigation."""
        for name, button in self.nav_buttons.items():
            if name != view_name:
                button.setChecked(False)
        self.navigationRequested.emit(view_name.lower().replace(' ', '_'))