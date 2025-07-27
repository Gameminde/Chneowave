#!/usr/bin/env python3
"""
Vue pour la configuration des paramètres du projet.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-20
Version: 1.0.0
"""

from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton, QVBoxLayout
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtCore import Signal

from hrneowave.gui.layouts.fibonacci_grid_mixin import FibonacciGridMixin

class ProjectSettingsView(QWidget, FibonacciGridMixin):
    """Vue permettant de définir les paramètres essentiels d'un projet.

    Utilise un QFormLayout intégré dans une grille Fibonacci pour une présentation claire.
    """
    settings_saved = Signal(dict)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setObjectName("ProjectSettingsView")
        self._setup_ui()

    def _setup_ui(self):
        """Initialise l'interface de configuration."""
        main_layout = self.create_grid(base_px=55, parent=self)
        self.setLayout(main_layout)

        form_layout = QFormLayout()

        # --- Champs de configuration ---
        self.project_name_input = QLineEdit("Nouveau Projet")
        self.num_probes_spinbox = QSpinBox()

        self.num_probes_spinbox.setRange(1, 16)
        self.num_probes_spinbox.setValue(8)

        self.test_duration_spinbox = QDoubleSpinBox()

        self.test_duration_spinbox.setRange(1.0, 3600.0)
        self.test_duration_spinbox.setValue(60.0)
        self.test_duration_spinbox.setSuffix(" s")

        self.sampling_freq_spinbox = QDoubleSpinBox()

        self.sampling_freq_spinbox.setRange(1.0, 10000.0)
        self.sampling_freq_spinbox.setValue(1000.0)
        self.sampling_freq_spinbox.setSuffix(" Hz")

        # --- Ajout au formulaire ---
        form_layout.addRow("Nom du Projet:", self.project_name_input)
        form_layout.addRow("Nombre de Sondes:", self.num_probes_spinbox)
        form_layout.addRow("Durée du Test:", self.test_duration_spinbox)
        form_layout.addRow("Fréquence d'Échantillonnage:", self.sampling_freq_spinbox)

        # --- Bouton de sauvegarde ---
        self.save_button = QPushButton("Sauvegarder les Paramètres")
        self.save_button.setObjectName("PrimaryButton")
        self.save_button.clicked.connect(self._on_save)

        # --- Assemblage final ---
        main_layout.addLayout(form_layout, 0, 0)
        main_layout.addWidget(self.save_button, 1, 0)

    def _on_save(self):
        """Récupère les données et émet le signal settings_saved."""
        settings = {
            "project_name": self.project_name_input.text(),
            "num_probes": self.num_probes_spinbox.value(),
            "test_duration": self.test_duration_spinbox.value(),
            "sampling_frequency": self.sampling_freq_spinbox.value(),
        }
        self.settings_saved.emit(settings)

    def load_settings(self, settings: dict):
        """Charge des paramètres existants dans la vue."""
        self.project_name_input.setText(settings.get("project_name", ""))
        self.num_probes_spinbox.setValue(settings.get("num_probes", 8))
        self.test_duration_spinbox.setValue(settings.get("test_duration", 60.0))
        self.sampling_freq_spinbox.setValue(settings.get("sampling_frequency", 1000.0))