#!/usr/bin/env python3
"""
Assistant (Wizard) pour la calibration manuelle des capteurs.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-20
Version: 1.0.0
"""

from PySide6.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QLabel, QComboBox, QSpinBox, QTableWidget, QHeaderView, QPushButton, QGridLayout
from PySide6.QtCore import Signal
import pyqtgraph as pg
import numpy as np

class ManualCalibrationWizard(QWizard):
    """Un assistant guidant l'utilisateur à travers la calibration manuelle d'un capteur."""
    calibrationCompleted = Signal(int, float, float, float)

    def __init__(self, num_probes=16, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Assistant de Calibration Manuelle")

        self.setPage(0, IntroductionPage(num_probes))
        self.setPage(1, DataAcquisitionPage())
        self.setPage(2, ResultsPage())

        self.currentIdChanged.connect(self._on_page_changed)

    def _on_page_changed(self, page_id: int):
        if page_id == 2: # Page de résultats
            self.page(2).calculate_and_display_results(self.page(1).get_data())

    def accept(self):
        slope, offset, r2 = self.page(2).get_results()
        sensor_id = self.page(0).sensor_combo.currentIndex()
        self.calibrationCompleted.emit(sensor_id, slope, offset, r2)
        super().accept()

class IntroductionPage(QWizardPage):
    def __init__(self, num_probes, parent=None):
        super().__init__(parent)
        self.setTitle("Étape 1: Sélection du Capteur")
        self.setSubTitle("Choisissez le capteur à calibrer et le nombre de points de mesure.")

        layout = QVBoxLayout(self)
        self.sensor_combo = QComboBox()
        self.sensor_combo.addItems([f"Sonde {i+1}" for i in range(num_probes)])
        self.num_points_spin = QSpinBox()
        self.num_points_spin.setRange(3, 20)
        self.num_points_spin.setValue(5)

        layout.addWidget(QLabel("Capteur à calibrer:"))
        layout.addWidget(self.sensor_combo)
        layout.addWidget(QLabel("Nombre de points de calibration:"))
        layout.addWidget(self.num_points_spin)

        self.registerField("sensor_id", self.sensor_combo)
        self.registerField("num_points", self.num_points_spin)

class DataAcquisitionPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Étape 2: Enregistrement des Points")
        self.setSubTitle("Pour chaque point, entrez la valeur physique connue et enregistrez la mesure du capteur.")

        layout = QGridLayout(self)
        self.table = QTableWidget()
        self.plot = None # Initialisation différée

        self.record_button = QPushButton("Enregistrer le Point")
        self.record_button.clicked.connect(self._record_point)

        layout.addWidget(self.table, 0, 0, 1, 2)
        # Le plot sera ajouté dans initializePage
        layout.addWidget(self.record_button, 2, 0, 1, 2)

    def initializePage(self):
        num_points = self.field("num_points")
        self.table.setRowCount(num_points)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Valeur Physique (m)", "Mesure (V)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if self.plot is None:
            self.plot = pg.PlotWidget(parent=self)
            self.plot.setTitle("Linéarité de la Calibration")
            self.plot.setLabel('left', 'Mesure (V)')
            self.plot.setLabel('bottom', 'Valeur Physique (m)')
            self.scatter_plot = self.plot.plot([], [], pen=None, symbol='o')
            self.line_plot = self.plot.plot([], [], pen='r')
            # Insérer le plot dans le layout
            layout = self.layout()
            if isinstance(layout, QGridLayout):
                layout.addWidget(self.plot, 1, 0, 1, 2)

    def _record_point(self):
        # Simule une lecture de capteur. Dans une vraie application, on lirait le matériel.
        current_row = self.table.currentRow()
        if current_row == -1: current_row = 0
        # Pour la démo, on met une valeur aléatoire
        measured_value = np.random.rand() 
        self.table.setItem(current_row, 1, pg.QtWidgets.QTableWidgetItem(f"{measured_value:.4f}"))
        self._update_plot()

    def _update_plot(self):
        data = self.get_data()
        if data[0].size > 1:
            self.scatter_plot.setData(data[0], data[1])
            # Simple régression linéaire pour la ligne
            p = np.polyfit(data[0], data[1], 1)
            self.line_plot.setData(data[0], np.polyval(p, data[0]))

    def get_data(self):
        known_values = []
        measured_values = []
        for i in range(self.table.rowCount()):
            try:
                known = float(self.table.item(i, 0).text())
                measured = float(self.table.item(i, 1).text())
                known_values.append(known)
                measured_values.append(measured)
            except (ValueError, AttributeError):
                continue
        return np.array(known_values), np.array(measured_values)

class ResultsPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Étape 3: Résultats et Validation")
        self.setSubTitle("Voici les résultats de la calibration. Validez pour sauvegarder.")
        self.slope = 0
        self.offset = 0
        self.r2 = 0

        layout = QVBoxLayout(self)
        self.summary_label = QLabel("Calcul en cours...")
        layout.addWidget(self.summary_label)

    def calculate_and_display_results(self, data):
        known, measured = data
        if known.size < 2:
            self.summary_label.setText("Pas assez de données pour calculer la calibration.")
            return

        # Régression linéaire
        p, res, _, _, _ = np.polyfit(known, measured, 1, full=True)
        self.slope, self.offset = p
        # Calcul du R²
        ss_res = np.sum((measured - np.polyval(p, known)) ** 2)
        ss_tot = np.sum((measured - np.mean(measured)) ** 2)
        self.r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 1

        summary = f"Pente (Slope): {self.slope:.4f}\n"
        summary += f"Ordonnée à l'origine (Offset): {self.offset:.4f}\n"
        summary += f"Coefficient de détermination (R²): {self.r2:.4f}"
        self.summary_label.setText(summary)

    def get_results(self):
        return self.slope, self.offset, self.r2