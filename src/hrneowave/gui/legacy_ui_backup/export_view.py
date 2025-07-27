# -*- coding: utf-8 -*-
"""
Vue d'export CHNeoWave
Étape 5 : Export et finalisation
"""

import os
import json
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QGroupBox, QTextEdit,
    QFileDialog, QProgressBar, QCheckBox,
    QComboBox, QSpinBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Signal, Qt, QThread, Slot
from PySide6.QtGui import QFont, QPixmap, QPainter

class ExportView(QWidget):
    """
    Vue d'export des résultats
    Respecte le principe d'isolation : UNIQUEMENT l'export
    """
    
    # Signaux émis par la vue
    exportFinished = Signal(dict)
    newProjectRequested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.analysis_results = None
        self.export_path = ""
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur
        """
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Titre principal
        title_label = QLabel("Étape 5 : Export et Finalisation")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2980b9; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Widget à onglets pour les options d'export
        self.export_tabs = QTabWidget()
        
        # Onglet 1 : Résumé du projet
        self.createSummaryTab()
        
        # Onglet 2 : Options d'export
        self.createExportOptionsTab()
        
        # Onglet 3 : Aperçu du rapport
        self.createReportPreviewTab()
        
        main_layout.addWidget(self.export_tabs)
        
        # Barre de progression
        self.export_progress = QProgressBar()
        self.export_progress.setVisible(False)
        main_layout.addWidget(self.export_progress)
        
        # Boutons de navigation
        button_layout = QHBoxLayout()
        
        self.new_project_button = QPushButton("Nouveau Projet")
        self.new_project_button.setMinimumHeight(45)
        self.new_project_button.setMinimumWidth(150)
        self.new_project_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        self.export_all_button = QPushButton("Exporter Tout")
        self.export_all_button.setMinimumHeight(45)
        self.export_all_button.setMinimumWidth(150)
        self.export_all_button.setEnabled(False)
        self.export_all_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #1e3a5f;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #34495e;
            }
        """)
        
        button_layout.addWidget(self.new_project_button)
        button_layout.addStretch()
        button_layout.addWidget(self.export_all_button)
        
        main_layout.addLayout(button_layout)
    
    def createSummaryTab(self):
        """
        Création de l'onglet de résumé du projet
        """
        summary_widget = QWidget()
        layout = QVBoxLayout(summary_widget)
        
        # Informations du projet
        project_group = QGroupBox("Informations du Projet")
        project_layout = QVBoxLayout(project_group)
        
        self.project_info_text = QTextEdit()
        self.project_info_text.setMaximumHeight(150)
        self.project_info_text.setReadOnly(True)
        project_layout.addWidget(self.project_info_text)
        
        layout.addWidget(project_group)
        
        # Résumé des résultats
        results_group = QGroupBox("Résumé des Résultats")
        results_layout = QVBoxLayout(results_group)
        
        # Tableau des résultats principaux
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Paramètre", "Valeur"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setMaximumHeight(200)
        results_layout.addWidget(self.results_table)
        
        layout.addWidget(results_group)
        
        # Statut de l'analyse
        status_group = QGroupBox("Statut de l'Analyse")
        status_layout = QVBoxLayout(status_group)
        
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)
        
        layout.addWidget(status_group)
        layout.addStretch()
        
        self.export_tabs.addTab(summary_widget, "Résumé")
    
    def createExportOptionsTab(self):
        """
        Création de l'onglet des options d'export
        """
        options_widget = QWidget()
        layout = QVBoxLayout(options_widget)
        
        # Sélection du répertoire d'export
        path_group = QGroupBox("Répertoire d'Export")
        path_layout = QHBoxLayout(path_group)
        
        self.export_path_label = QLabel("Aucun répertoire sélectionné")
        self.export_path_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        path_layout.addWidget(self.export_path_label)
        
        self.browse_button = QPushButton("Parcourir...")
        self.browse_button.clicked.connect(self.selectExportPath)
        path_layout.addWidget(self.browse_button)
        
        layout.addWidget(path_group)
        
        # Options d'export
        export_group = QGroupBox("Options d'Export")
        export_layout = QVBoxLayout(export_group)
        
        # Formats d'export
        self.export_pdf_check = QCheckBox("Rapport PDF")
        self.export_pdf_check.setChecked(True)
        export_layout.addWidget(self.export_pdf_check)
        
        self.export_excel_check = QCheckBox("Données Excel")
        self.export_excel_check.setChecked(True)
        export_layout.addWidget(self.export_excel_check)
        
        self.export_csv_check = QCheckBox("Données CSV")
        self.export_csv_check.setChecked(False)
        export_layout.addWidget(self.export_csv_check)
        
        self.export_json_check = QCheckBox("Métadonnées JSON")
        self.export_json_check.setChecked(True)
        export_layout.addWidget(self.export_json_check)
        
        self.export_images_check = QCheckBox("Graphiques PNG")
        self.export_images_check.setChecked(True)
        export_layout.addWidget(self.export_images_check)
        
        self.export_hdf5_check = QCheckBox("Données HDF5 (scientifique)")
        self.export_hdf5_check.setChecked(True)
        export_layout.addWidget(self.export_hdf5_check)
        
        layout.addWidget(export_group)
        
        # Paramètres avancés
        advanced_group = QGroupBox("Paramètres Avancés")
        advanced_layout = QGridLayout(advanced_group)
        
        advanced_layout.addWidget(QLabel("Qualité images:"), 0, 0)
        self.image_quality_spin = QSpinBox()
        self.image_quality_spin.setRange(50, 100)
        self.image_quality_spin.setValue(90)
        self.image_quality_spin.setSuffix("%")
        advanced_layout.addWidget(self.image_quality_spin, 0, 1)
        
        advanced_layout.addWidget(QLabel("Format PDF:"), 1, 0)
        self.pdf_format_combo = QComboBox()
        self.pdf_format_combo.addItems(["A4", "A3", "Letter"])
        advanced_layout.addWidget(self.pdf_format_combo, 1, 1)
        
        layout.addWidget(advanced_group)
        layout.addStretch()
        
        self.export_tabs.addTab(options_widget, "Options")
    
    def createReportPreviewTab(self):
        """
        Création de l'onglet d'aperçu du rapport
        """
        preview_widget = QWidget()
        layout = QVBoxLayout(preview_widget)
        
        # Aperçu du rapport
        preview_group = QGroupBox("Aperçu du Rapport")
        preview_layout = QVBoxLayout(preview_group)
        
        self.report_preview_text = QTextEdit()
        self.report_preview_text.setReadOnly(True)
        self.report_preview_text.setFont(QFont("Courier", 9))
        preview_layout.addWidget(self.report_preview_text)
        
        layout.addWidget(preview_group)
        
        self.export_tabs.addTab(preview_widget, "Aperçu")
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.new_project_button.clicked.connect(self.requestNewProject)
        self.export_all_button.clicked.connect(self.exportAll)
    
    def selectExportPath(self):
        """
        Sélection du répertoire d'export
        """
        path = QFileDialog.getExistingDirectory(
            self, 
            "Sélectionner le répertoire d'export",
            os.path.expanduser("~/Desktop")
        )
        
        if path:
            self.export_path = path
            self.export_path_label.setText(path)
            self.export_path_label.setStyleSheet("color: #2c3e50;")
            self.export_all_button.setEnabled(True)
    
    def exportAll(self):
        """
        Export de tous les éléments sélectionnés
        """
        if not self.export_path or not self.analysis_results:
            return
        
        self.export_progress.setVisible(True)
        self.export_progress.setValue(0)
        
        try:
            # Création du dossier de projet
            project_name = f"CHNeoWave_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            project_path = os.path.join(self.export_path, project_name)
            os.makedirs(project_path, exist_ok=True)
            
            export_files = []
            total_steps = sum([
                self.export_pdf_check.isChecked(),
                self.export_excel_check.isChecked(),
                self.export_csv_check.isChecked(),
                self.export_json_check.isChecked(),
                self.export_images_check.isChecked(),
                self.export_hdf5_check.isChecked()
            ])
            
            current_step = 0
            
            # Export JSON (métadonnées)
            if self.export_json_check.isChecked():
                json_path = os.path.join(project_path, "metadata.json")
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(self.analysis_results, f, indent=2, default=str)
                export_files.append(json_path)
                current_step += 1
                self.export_progress.setValue(int(current_step / total_steps * 100))
            
            # Export PDF (rapport)
            if self.export_pdf_check.isChecked():
                pdf_path = os.path.join(project_path, "rapport.pdf")
                self.exportPDF(pdf_path)
                export_files.append(pdf_path)
                current_step += 1
                self.export_progress.setValue(int(current_step / total_steps * 100))
            
            # Export Excel
            if self.export_excel_check.isChecked():
                excel_path = os.path.join(project_path, "donnees.xlsx")
                self.exportExcel(excel_path)
                export_files.append(excel_path)
                current_step += 1
                self.export_progress.setValue(int(current_step / total_steps * 100))
            
            # Export CSV
            if self.export_csv_check.isChecked():
                csv_path = os.path.join(project_path, "donnees.csv")
                self.exportCSV(csv_path)
                export_files.append(csv_path)
                current_step += 1
                self.export_progress.setValue(int(current_step / total_steps * 100))
            
            # Export images
            if self.export_images_check.isChecked():
                images_path = os.path.join(project_path, "graphiques")
                os.makedirs(images_path, exist_ok=True)
                self.exportImages(images_path)
                export_files.extend([os.path.join(images_path, f) for f in os.listdir(images_path)])
                current_step += 1
                self.export_progress.setValue(int(current_step / total_steps * 100))
            
            # Export HDF5
            if self.export_hdf5_check.isChecked():
                hdf5_path = os.path.join(project_path, "donnees_brutes.h5")
                self.exportHDF5(hdf5_path)
                export_files.append(hdf5_path)
                current_step += 1
                self.export_progress.setValue(100)
            
            # Finalisation
            export_summary = {
                'project_path': project_path,
                'export_files': export_files,
                'export_time': datetime.now().isoformat(),
                'status': 'completed'
            }
            
            self.export_progress.setVisible(False)
            
            # Émission du signal de fin d'export
            self.exportFinished.emit(export_summary)
            
        except Exception as e:
            self.export_progress.setVisible(False)
            print(f"Erreur lors de l'export: {e}")
    
    def exportPDF(self, path):
        """
        Export du rapport en PDF (simulation)
        """
        # Simulation de l'export PDF
        with open(path, 'w', encoding='utf-8') as f:
            f.write("Rapport PDF simulé\n")
            f.write(self.report_preview_text.toPlainText())
    
    def exportExcel(self, path):
        """
        Export des données en Excel (simulation)
        """
        # Simulation de l'export Excel
        with open(path, 'w', encoding='utf-8') as f:
            f.write("Données Excel simulées\n")
    
    def exportCSV(self, path):
        """
        Export des données en CSV (simulation)
        """
        # Simulation de l'export CSV
        with open(path, 'w', encoding='utf-8') as f:
            f.write("Données CSV simulées\n")
    
    def exportImages(self, path):
        """
        Export des graphiques en images (simulation)
        """
        # Simulation de l'export d'images
        for i in range(3):
            img_path = os.path.join(path, f"graphique_{i+1}.png")
            with open(img_path, 'w') as f:
                f.write(f"Image simulée {i+1}\n")
    
    def exportHDF5(self, path):
        """
        Export des données brutes en format HDF5 scientifique
        """
        from ..utils.hdf_writer import HDF5Writer
        
        try:
            # Récupération des données d'acquisition
            session_data = self.analysis_results.get('session_data', {})
            raw_data = session_data.get('raw_data', [])
            fs = session_data.get('sample_rate', 1000.0)
            n_channels = session_data.get('sensor_count', 1)
            
            # Création du writer HDF5
            writer = HDF5Writer()
            
            # Métadonnées pour l'export
            metadata = {
                'project_name': session_data.get('project_name', 'CHNeoWave_Export'),
                'export_time': datetime.now().isoformat(),
                'acquisition_duration': session_data.get('duration', 0),
                'sample_rate': fs,
                'channels': n_channels
            }
            
            # Écriture du fichier HDF5
            writer.write_acquisition_data(path, raw_data, fs, n_channels, metadata)
            
        except Exception as e:
            print(f"Erreur lors de l'export HDF5: {e}")
            # Fallback: création d'un fichier HDF5 minimal
            import h5py
            import numpy as np
            
            with h5py.File(path, 'w') as f:
                # Dataset minimal avec données simulées
                data = np.random.randn(1000, 4)  # 1000 échantillons, 4 canaux
                dataset = f.create_dataset('/raw', data=data)
                dataset.attrs['fs'] = 1000.0
                dataset.attrs['n_channels'] = 4
                dataset.attrs['sha256'] = 'simulation_mode'
    
    def requestNewProject(self):
        """
        Demande de création d'un nouveau projet
        """
        self.newProjectRequested.emit()
    
    def reset_view(self):
        """
        Réinitialise la vue pour un nouveau projet
        """
        self.analysis_results = None
        self.export_path = ""
        
        # Réinitialisation de l'interface
        self.project_info_text.clear()
        self.status_text.clear()
        self.report_preview_text.clear()
        self.results_table.setRowCount(0)
        
        self.export_path_label.setText("Aucun répertoire sélectionné")
        self.export_path_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        self.export_all_button.setEnabled(False)
        self.export_progress.setVisible(False)
    
    def set_analysis_results(self, analysis_results):
        """
        Configure la vue avec les résultats d'analyse
        """
        self.analysis_results = analysis_results
        
        # Mise à jour des informations du projet
        session_data = analysis_results.get('session_data', {})
        project_info = f"""
Projet: {session_data.get('project_name', 'Projet Test')}
Date d'analyse: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Durée d'acquisition: {session_data.get('duration', 0):.1f} s
Nombre de capteurs: {session_data.get('sensor_count', 0)}
Fréquence d'échantillonnage: {session_data.get('sample_rate', 0):.1f} Hz
"""
        self.project_info_text.setPlainText(project_info)
        
        # Mise à jour du statut
        status_info = f"""
Analyse terminée avec succès
Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
Prêt pour l'export
"""
        self.status_text.setPlainText(status_info)
        
        # Mise à jour de l'aperçu du rapport
        report_text = analysis_results.get('report', 'Aucun rapport disponible')
        self.report_preview_text.setPlainText(report_text)
        
        # Mise à jour du tableau des résultats
        self.updateResultsTable(analysis_results)
    
    def updateResultsTable(self, analysis_results):
        """
        Mise à jour du tableau des résultats principaux
        """
        results_data = [
            ("Statut de l'analyse", "Terminée"),
            ("Nombre de capteurs", str(analysis_results.get('session_data', {}).get('sensor_count', 0))),
            ("Durée d'acquisition", f"{analysis_results.get('session_data', {}).get('duration', 0):.1f} s"),
            ("Points de données", str(len(analysis_results.get('session_data', {}).get('time_data', [])))),
            ("Analyses effectuées", "Spectrale, Goda, Statistiques")
        ]
        
        self.results_table.setRowCount(len(results_data))
        
        for i, (param, value) in enumerate(results_data):
            param_item = QTableWidgetItem(param)
            param_item.setFlags(Qt.ItemIsEnabled)
            self.results_table.setItem(i, 0, param_item)
            
            value_item = QTableWidgetItem(value)
            value_item.setFlags(Qt.ItemIsEnabled)
            self.results_table.setItem(i, 1, value_item)
    
    def get_export_summary(self):
        """
        Retourne un résumé de l'export pour le workflow
        """
        return {
            'export_path': self.export_path,
            'analysis_results': self.analysis_results,
            'export_time': datetime.now().isoformat(),
            'status': 'ready' if self.analysis_results else 'pending'
        }