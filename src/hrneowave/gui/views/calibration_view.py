# -*- coding: utf-8 -*-
"""
Vue de calibration CHNeoWave
Étape 2 : Calibration des capteurs
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QSpinBox,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QDialog,
    QDialogButtonBox, QSplitter, QTextEdit, QProgressBar, QComboBox,
    QMessageBox
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont, QColor

import numpy as np
import json
import os
from datetime import datetime

class CalibrationView(QWidget):
    """
    Vue de calibration des capteurs
    Respecte le principe d'isolation : UNIQUEMENT la calibration
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Signal émis lorsque la calibration est terminée
        self.calibrationFinished = Signal(dict)
        self.sensor_count = 4  # Valeur par défaut
        self.calibration_data = {}  # Données de calibration
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur
        """
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # Titre principal
        title_label = QLabel("Étape 2 : Calibration des Capteurs")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2980b9; margin-bottom: 15px;")
        main_layout.addWidget(title_label)
        
        # Configuration du nombre de capteurs
        config_layout = QFormLayout()
        self.sensor_count_spinbox = QSpinBox()
        self.sensor_count_spinbox.setRange(1, 16)
        self.sensor_count_spinbox.setValue(4)
        self.sensor_count_spinbox.setMinimumHeight(35)
        config_layout.addRow("Nombre de Capteurs:", self.sensor_count_spinbox)
        main_layout.addLayout(config_layout)
        
        # Tableau des capteurs
        self.sensor_table = QTableWidget()
        self.sensor_table.setColumnCount(3)
        self.sensor_table.setHorizontalHeaderLabels(["Capteur", "Statut", "Action"])
        
        # Configuration du tableau
        header = self.sensor_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.sensor_table.setMinimumHeight(200)
        self.sensor_table.setAlternatingRowColors(True)
        main_layout.addWidget(self.sensor_table)
        
        # Initialisation du tableau
        self.updateSensorTable()
        
        # Espacement flexible
        main_layout.addStretch()
        
        # Bouton de navigation
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Bouton d'export PDF
        self.export_pdf_button = QPushButton("Exporter PDF")
        self.export_pdf_button.setMinimumHeight(45)
        self.export_pdf_button.setMinimumWidth(150)
        self.export_pdf_button.setEnabled(False)  # Désactivé par défaut
        self.export_pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12pt;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #34495e;
            }
        """)
        
        self.next_button = QPushButton("Suivant : Acquisition")
        self.next_button.setMinimumHeight(45)
        self.next_button.setMinimumWidth(200)
        self.next_button.setEnabled(False)  # Désactivé par défaut
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #1e3a5f;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #34495e;
            }
        """)
        
        button_layout.addWidget(self.export_pdf_button)
        button_layout.addWidget(self.next_button)
        main_layout.addLayout(button_layout)
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.sensor_count_spinbox.valueChanged.connect(self.onSensorCountChanged)
        self.next_button.clicked.connect(self.finishCalibration)
        self.export_pdf_button.clicked.connect(self.exportCalibrationPDF)
    
    def onSensorCountChanged(self, value):
        """
        Mise à jour du tableau lors du changement du nombre de capteurs
        """
        self.sensor_count = value
        self.calibration_data.clear()  # Reset des données
        self.updateSensorTable()
        self.checkCalibrationComplete()
    
    def updateSensorTable(self):
        """
        Mise à jour du tableau des capteurs
        """
        self.sensor_table.setRowCount(self.sensor_count)
        
        for i in range(self.sensor_count):
            # Nom du capteur
            sensor_item = QTableWidgetItem(f"Capteur {i+1}")
            sensor_item.setFlags(Qt.ItemIsEnabled)
            self.sensor_table.setItem(i, 0, sensor_item)
            
            # Statut de calibration
            status = "OK" if i in self.calibration_data else "Non calibré"
            status_item = QTableWidgetItem(status)
            status_item.setFlags(Qt.ItemIsEnabled)
            
            if status == "OK":
                status_item.setBackground(QColor(39, 174, 96, 50))  # Vert léger
            else:
                status_item.setBackground(QColor(231, 76, 60, 50))  # Rouge léger
            
            self.sensor_table.setItem(i, 1, status_item)
            
            # Bouton de calibration
            calibrate_button = QPushButton("Calibrer")
            calibrate_button.setMinimumHeight(30)
            calibrate_button.clicked.connect(lambda checked, idx=i: self.openCalibrationDialog(idx))
            calibrate_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            
            self.sensor_table.setCellWidget(i, 2, calibrate_button)
    
    def openCalibrationDialog(self, sensor_index):
        """
        Ouverture de la boîte de dialogue de calibration
        """
        dialog = LinearityCalibrationDialog(sensor_index, self)
        if dialog.exec_() == QDialog.Accepted:
            # Récupération des données de calibration
            self.calibration_data[sensor_index] = dialog.getCalibrationData()
            self.updateSensorTable()
            self.checkCalibrationComplete()
    
    def checkCalibrationComplete(self):
        """
        Vérification si tous les capteurs sont calibrés
        """
        all_calibrated = len(self.calibration_data) == self.sensor_count
        self.next_button.setEnabled(all_calibrated)
        
        # Vérifier si on peut exporter le PDF (R² ≥ 0.998 pour tous les capteurs)
        can_export_pdf = all_calibrated and all(
            data.get('r_squared', 0) >= 0.998 
            for data in self.calibration_data.values()
        )
        self.export_pdf_button.setEnabled(can_export_pdf)
    
    def finishCalibration(self):
        """
        Finalisation de la calibration et émission du signal
        """
        calibration_summary = {
            'sensor_count': self.sensor_count,
            'calibration_data': self.calibration_data,
            'status': 'completed'
        }
        
        # Émission du signal vers le MainController
        self.calibrationFinished.emit(calibration_summary)
    
    def resetCalibration(self):
        """
        Réinitialisation de la calibration
        """
        self.calibration_data.clear()
        self.updateSensorTable()
        self.checkCalibrationComplete()
    
    def reset_view(self):
        """
        Réinitialise la vue pour un nouveau projet
        """
        self.sensor_count_spinbox.setValue(1)
        self.calibration_data.clear()
        self.updateSensorTable()
        self.checkCalibrationComplete()
    
    def set_project_info(self, project_data):
        """
        Configure la vue avec les informations du projet
        """
        # Ici on pourrait utiliser les données du projet si nécessaire
        # Pour l'instant, on garde la configuration par défaut
        pass
    
    def get_calibration_data(self):
        """
        Retourne les données de calibration pour le workflow
        """
        return {
            'sensor_count': self.sensor_count,
            'calibration_data': self.calibration_data,
            'status': 'completed' if len(self.calibration_data) == self.sensor_count else 'incomplete'
        }
    
    def exportCalibrationPDF(self):
        """
        Exporte un certificat PDF de calibration
        """
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        from ...utils.calib_pdf import CalibrationPDFGenerator
        import os
        
        try:
            # Sélection du fichier de sortie
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Exporter certificat de calibration",
                f"certificat_calibration_{self.sensor_count}_capteurs.pdf",
                "Fichiers PDF (*.pdf)"
            )
            
            if not filename:
                return
            
            # Préparation des données de calibration
            calib_data = {
                'sensor_count': self.sensor_count,
                'sensors': []
            }
            
            for sensor_id, data in self.calibration_data.items():
                sensor_info = {
                    'id': sensor_id + 1,
                    'name': f"Capteur {sensor_id + 1}",
                    'gain': data.get('gain', 1.0),
                    'offset': data.get('offset', 0.0),
                    'r_squared': data.get('r_squared', 0.0),
                    'points': data.get('points', [])
                }
                calib_data['sensors'].append(sensor_info)
            
            # Génération du PDF
            generator = CalibrationPDFGenerator()
            generator.generate_certificate(calib_data, filename)
            
            # Message de succès
            QMessageBox.information(
                self,
                "Export réussi",
                f"Certificat de calibration exporté avec succès :\n{filename}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur d'export",
                f"Erreur lors de l'export du certificat PDF :\n{str(e)}"
            )


class LinearityCalibrationDialog(QDialog):
    """
    Boîte de dialogue pour la calibration de linéarité d'un capteur
    LOT A - Calibration manuelle avec linéarité
    """
    
    def __init__(self, sensor_index, parent=None):
        super().__init__(parent)
        self.sensor_index = sensor_index
        self.calibration_data = None
        self.n_points = 3
        self.up_measurements = []
        self.down_measurements = []
        self.current_measurement_type = None
        self.current_point_index = 0
        self.setupUI()
    
    def setupUI(self):
        """
        Configuration de l'interface de calibration - LOT A
        """
        # import pyqtgraph as pg
        # Utilisation de l'adaptateur matplotlib pour compatibilité PySide6
        from ..components.matplotlib_adapter import pg
        self.setWindowTitle(f"Calibration Linéarité - Capteur {self.sensor_index + 1}")
        self.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel(f"Calibration de Linéarité - Capteur {self.sensor_index + 1}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Configuration n_points
        config_layout = QFormLayout()
        self.n_points_combo = QComboBox()
        self.n_points_combo.addItems(["2", "3", "4", "5", "6", "7"])
        self.n_points_combo.setCurrentText("3")
        self.n_points_combo.currentTextChanged.connect(self.onNPointsChanged)
        config_layout.addRow("Nombre de points:", self.n_points_combo)
        layout.addLayout(config_layout)
        
        # Splitter pour diviser l'interface
        splitter = QSplitter(Qt.Horizontal)
        
        # Zone de graphique
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Tension (V)')
        self.plot_widget.setLabel('bottom', 'Hauteur eau (mm)')
        self.plot_widget.setTitle('Courbe de Calibration')
        self.plot_widget.setMinimumWidth(450)
        splitter.addWidget(self.plot_widget)
        
        # Zone de contrôle
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Instructions
        instructions = QTextEdit()
        instructions.setMaximumHeight(100)
        instructions.setPlainText(
            "1. Sélectionnez le nombre de points\n"
            "2. Mesure montée: 0% → 100%\n"
            "3. Mesure descente: 100% → 0%\n"
            "4. Vérifiez la linéarité (R²)"
        )
        instructions.setReadOnly(True)
        control_layout.addWidget(instructions)
        
        # Boutons de mesure
        self.up_btn = QPushButton("Mesure montée")
        self.up_btn.clicked.connect(self.startUpMeasurement)
        self.up_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; padding: 8px; border-radius: 4px; }")
        control_layout.addWidget(self.up_btn)
        
        self.down_btn = QPushButton("Mesure descente")
        self.down_btn.clicked.connect(self.startDownMeasurement)
        self.down_btn.setEnabled(False)
        self.down_btn.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; padding: 8px; border-radius: 4px; }")
        control_layout.addWidget(self.down_btn)
        
        # Status et progression
        self.status_label = QLabel("Prêt pour calibration")
        self.status_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        control_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        control_layout.addWidget(self.progress_bar)
        
        # Résultats
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(180)
        self.results_text.setReadOnly(True)
        control_layout.addWidget(self.results_text)
        
        # Bouton sauvegarde
        self.save_btn = QPushButton("Sauver calibration")
        self.save_btn.clicked.connect(self.saveCalibration)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; padding: 8px; border-radius: 4px; }")
        control_layout.addWidget(self.save_btn)
        
        splitter.addWidget(control_widget)
        splitter.setSizes([550, 350])
        layout.addWidget(splitter)
        
        # Boutons de dialogue
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.button_box = button_box
    
    def onNPointsChanged(self, value):
        """
        Changement du nombre de points de calibration
        """
        self.n_points = int(value)
        self.resetMeasurements()
    
    def resetMeasurements(self):
        """
        Réinitialise les mesures
        """
        self.up_measurements = []
        self.down_measurements = []
        self.plot_widget.clear()
        self.results_text.clear()
        self.up_btn.setEnabled(True)
        self.down_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.status_label.setText("Prêt pour calibration")
    
    def startUpMeasurement(self):
        """
        Démarre la mesure montée (0% → 100%)
        """
        self.current_measurement_type = "up"
        self.current_point_index = 0
        self.up_measurements = []
        self.status_label.setText(f"Mesure montée: point 1/{self.n_points}")
        self.up_btn.setEnabled(False)
        self.simulateMeasurement()
    
    def startDownMeasurement(self):
        """
        Démarre la mesure descente (100% → 0%)
        """
        self.current_measurement_type = "down"
        self.current_point_index = 0
        self.down_measurements = []
        self.status_label.setText(f"Mesure descente: point 1/{self.n_points}")
        self.down_btn.setEnabled(False)
        self.simulateMeasurement()
    
    def simulateMeasurement(self):
        """
        Simule l'acquisition d'un point de mesure
        """
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Timer pour simuler l'acquisition
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(50)  # 50ms
        self.progress_value = 0
    
    def updateProgress(self):
        """
        Met à jour la progression de la mesure
        """
        self.progress_value += 5
        self.progress_bar.setValue(self.progress_value)
        
        if self.progress_value >= 100:
            self.timer.stop()
            self.completeMeasurement()
    
    def completeMeasurement(self):
        """
        Complète une mesure et génère un point de données
        """
        # Calcul de la position (0% à 100% ou 100% à 0%)
        if self.current_measurement_type == "up":
            position_percent = (self.current_point_index / (self.n_points - 1)) * 100
        else:
            position_percent = ((self.n_points - 1 - self.current_point_index) / (self.n_points - 1)) * 100
        
        # Simulation d'une mesure réaliste
        height = position_percent * 5  # 0-500mm
        voltage = 0.01 * height + 0.5 + np.random.normal(0, 0.01)  # Relation linéaire + bruit
        
        # Stockage de la mesure
        measurement = {'height': height, 'voltage': voltage}
        if self.current_measurement_type == "up":
            self.up_measurements.append(measurement)
        else:
            self.down_measurements.append(measurement)
        
        self.current_point_index += 1
        
        # Vérification si toutes les mesures sont terminées
        if self.current_point_index < self.n_points:
            self.status_label.setText(f"Mesure {self.current_measurement_type}: point {self.current_point_index + 1}/{self.n_points}")
            self.simulateMeasurement()
        else:
            self.finishMeasurementSequence()
    
    def finishMeasurementSequence(self):
        """
        Termine une séquence de mesure
        """
        self.progress_bar.setVisible(False)
        
        if self.current_measurement_type == "up":
            self.status_label.setText("Mesure montée terminée")
            self.down_btn.setEnabled(True)
            self.plotMeasurements()
        else:
            self.status_label.setText("Mesure descente terminée")
            self.calculateLinearity()
    
    def plotMeasurements(self):
        """
        Affiche les mesures sur le graphique
        """
        self.plot_widget.clear()
        
        if self.up_measurements:
            heights_up = [m['height'] for m in self.up_measurements]
            voltages_up = [m['voltage'] for m in self.up_measurements]
            self.plot_widget.plot(heights_up, voltages_up, pen=None, symbol='o', 
                                symbolBrush='g', symbolSize=8, name='Montée')
        
        if self.down_measurements:
            heights_down = [m['height'] for m in self.down_measurements]
            voltages_down = [m['voltage'] for m in self.down_measurements]
            self.plot_widget.plot(heights_down, voltages_down, pen=None, symbol='s', 
                                symbolBrush='r', symbolSize=8, name='Descente')
    
    def calculateLinearity(self):
        """
        Calcule la linéarité et affiche les résultats
        """
        # Combinaison des mesures montée et descente
        all_heights = [m['height'] for m in self.up_measurements + self.down_measurements]
        all_voltages = [m['voltage'] for m in self.up_measurements + self.down_measurements]
        
        # Calcul de la régression linéaire
        coeffs = np.polyfit(all_heights, all_voltages, 1)
        slope, intercept = coeffs[0], coeffs[1]
        
        # Calcul du R²
        fit_voltages = np.polyval(coeffs, all_heights)
        ss_res = np.sum((all_voltages - fit_voltages) ** 2)
        ss_tot = np.sum((all_voltages - np.mean(all_voltages)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Affichage de la droite de régression
        height_range = np.linspace(0, 500, 100)
        fit_line = np.polyval(coeffs, height_range)
        self.plot_widget.plot(height_range, fit_line, pen='b', linewidth=2, name='Fit linéaire')
        
        # Affichage des résultats
        results = f"""Résultats calibration:

Nombre de points: {self.n_points}
Slope: {slope:.6f} V/mm
Offset: {intercept:.6f} V
R²: {r_squared:.6f}

Sensibilité: {slope*1000:.3f} mV/mm
Offset: {intercept*1000:.1f} mV"""
        
        # Vérification de la linéarité
        if abs(r_squared - 1) > 0.002:
            results += "\n\nWARNING: Capteur non linéaire"
            self.showLinearityWarning()
        else:
            results += "\n\n✓ Capteur linéaire"
        
        self.results_text.setPlainText(results)
        
        # Sauvegarde des données
        self.calibration_data = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'n_points': self.n_points,
            'up_measurements': self.up_measurements,
            'down_measurements': self.down_measurements,
            'sensor_index': self.sensor_index,
            'timestamp': datetime.now().isoformat()
        }
        
        self.save_btn.setEnabled(True)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        self.status_label.setText("Calibration terminée")
    
    def showLinearityWarning(self):
        """
        Affiche un warning si le capteur n'est pas linéaire
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Capteur non linéaire")
        msg.setText("Le capteur présente une non-linéarité significative.")
        msg.setDetailedText(f"R² = {self.calibration_data['r_squared']:.6f}\n"
                           f"Écart à la linéarité: {abs(self.calibration_data['r_squared'] - 1):.6f}\n"
                           f"Seuil acceptable: 0.002")
        msg.exec_()
    
    def saveCalibration(self):
        """
        Sauvegarde la calibration en JSON
        """
        if not self.calibration_data:
            return
        
        # Nom du fichier avec timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"calib_{timestamp}.json"
        filepath = os.path.join(os.getcwd(), filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.calibration_data, f, indent=2, ensure_ascii=False)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Sauvegarde réussie")
            msg.setText(f"Calibration sauvegardée:\n{filename}")
            msg.exec_()
            
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Erreur sauvegarde")
            msg.setText(f"Erreur lors de la sauvegarde:\n{str(e)}")
            msg.exec_()
    
    def getCalibrationData(self):
        """
        Retourne les données de calibration
        """
        return self.calibration_data

# Import nécessaire pour QApplication
from PySide6.QtWidgets import QApplication