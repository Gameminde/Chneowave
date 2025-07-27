# -*- coding: utf-8 -*-
"""
Vue de calibration CHNeoWave
Étape 2 : Calibration des capteurs
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QSpinBox,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QDialog,
    QDialogButtonBox, QSplitter, QTextEdit, QProgressBar, QComboBox,
    QMessageBox, QFileDialog
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont, QColor

import numpy as np
import json
import os
from datetime import datetime

class CalibrationView(QWidget):
    """
    Vue de calibration unifiée des capteurs
    Interface moderne avec navigation par étapes selon standards UI/UX 2025
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Signal émis lorsque la calibration est terminée
        self.calibrationFinished = Signal(dict)
        self.sensor_count = 4  # Valeur par défaut
        self.calibration_data = {}  # Données de calibration
        self.current_step = 0  # Étape actuelle (0-4)
        self.steps = [
            "Capteur", "Points", "Mesure", "Analyse", "Rapport"
        ]
        
        # Données de mesure
        self.current_sensor_data = []
        self.measurement_points = 5
        self.setupUI()
        self.connectSignals()
        # Initialisation de l'affichage
        self.updateStepDisplay()
        self.updateNavigationButtons()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur unifiée
        Structure : Header + Sidebar (20%) + Zone principale (80%) + Footer
        """
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header avec barre de progression
        self.setupHeader(main_layout)
        
        # Zone principale horizontale : Sidebar + Contenu
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
                width: 2px;
            }
        """)
        
        # Sidebar navigation (20%)
        self.setupSidebar(content_splitter)
        
        # Zone de contenu principal (80%)
        self.setupMainContent(content_splitter)
        
        # Proportions : 20% sidebar, 80% contenu
        content_splitter.setSizes([200, 800])
        main_layout.addWidget(content_splitter)
        
        # Footer avec boutons de navigation
        self.setupFooter(main_layout)
        
    def setupHeader(self, main_layout):
        """
        Configuration du header avec titre et barre de progression
        """
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 2px solid #e2e8f0;
            }
        """)
        
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 15, 30, 15)
        
        # Titre
        title_label = QLabel("CHNeoWave - Calibration Unifiée")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1e40af; margin-bottom: 8px;")
        header_layout.addWidget(title_label)
        
        # Barre de progression avec pourcentage
        progress_layout = QHBoxLayout()
        
        self.progress_label = QLabel("●●●○○ Progression: Étape 1/5")
        self.progress_label.setStyleSheet("color: #475569; font-weight: normal;")
        progress_layout.addWidget(self.progress_label)
        
        progress_layout.addStretch()
        
        self.progress_percent = QLabel("20%")
        self.progress_percent.setStyleSheet("color: #1e40af; font-weight: bold; font-size: 16px;")
        progress_layout.addWidget(self.progress_percent)
        
        header_layout.addLayout(progress_layout)
        main_layout.addWidget(header_widget)
        
    def setupSidebar(self, parent_splitter):
        """
        Configuration de la sidebar avec navigation par étapes
        """
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(250)
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border-right: 2px solid #e2e8f0;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(15)
        
        # Titre sidebar
        steps_title = QLabel("ÉTAPES")
        steps_title.setStyleSheet("""
            color: #64748b;
            font-weight: 600;
            font-size: 12px;
            letter-spacing: 1px;
            margin-bottom: 10px;
        """)
        sidebar_layout.addWidget(steps_title)
        
        # Boutons d'étapes
        self.step_buttons = []
        for i, step_name in enumerate(self.steps):
            step_button = QPushButton(f"{step_name}")
            step_button.setFixedHeight(50)
            step_button.clicked.connect(lambda checked, idx=i: self.goToStep(idx))
            
            # Style selon l'état
            if i == self.current_step:
                step_button.setStyleSheet(self.getActiveStepStyle())
            elif i < self.current_step:
                step_button.setStyleSheet(self.getCompletedStepStyle())
            else:
                step_button.setStyleSheet(self.getInactiveStepStyle())
            
            self.step_buttons.append(step_button)
            sidebar_layout.addWidget(step_button)
        
        sidebar_layout.addStretch()
        parent_splitter.addWidget(sidebar_widget)
        
    def setupMainContent(self, parent_splitter):
        """
        Configuration de la zone de contenu principal
        """
        self.main_content_widget = QWidget()
        self.main_content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        
        self.content_layout = QVBoxLayout(self.main_content_widget)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.content_layout.setSpacing(30)
        
        # Zone de contenu dynamique selon l'étape
        self.setupStepContent()
        
        parent_splitter.addWidget(self.main_content_widget)
    
    def setupFooter(self, main_layout):
        """
        Configuration du footer avec boutons de navigation
        """
        footer_widget = QWidget()
        footer_widget.setFixedHeight(80)
        footer_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-top: 2px solid #e2e8f0;
            }
        """)
        
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(30, 20, 30, 20)
        
        # Bouton Précédent
        self.prev_button = QPushButton("Précédent")
        self.prev_button.setFixedHeight(45)
        self.prev_button.setFixedWidth(120)
        self.prev_button.setEnabled(False)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #475569;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                border-color: #cbd5e1;
                background-color: #f8fafc;
            }
            QPushButton:disabled {
                color: #94a3b8;
                border-color: #f1f5f9;
            }
        """)
        
        footer_layout.addWidget(self.prev_button)
        footer_layout.addStretch()
        
        # Boutons droite
        self.continue_button = QPushButton("Continuer")
        self.continue_button.setFixedHeight(45)
        self.continue_button.setFixedWidth(120)
        self.continue_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #3b82f6, stop:1 #1e40af);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #60a5fa, stop:1 #2563eb);
            }
        """)
        
        self.finish_button = QPushButton("Terminer")
        self.finish_button.setFixedHeight(45)
        self.finish_button.setFixedWidth(120)
        self.finish_button.setVisible(False)
        self.finish_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #34d399, stop:1 #10b981);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #4ade80, stop:1 #059669);
            }
        """)
        
        footer_layout.addWidget(self.continue_button)
        footer_layout.addWidget(self.finish_button)
        main_layout.addWidget(footer_widget)
    
    def setupStepContent(self):
        """
        Configuration du contenu selon l'étape actuelle
        """
        # Nettoyer le contenu existant
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        if self.current_step == 0:  # Étape Capteur
            self.setupSensorStep()
        elif self.current_step == 1:  # Étape Points
            self.setupPointsStep()
        elif self.current_step == 2:  # Étape Mesure
            self.setupMeasureStep()
            self.updateSensorCombo()
            self.updateMeasurementTable()
        elif self.current_step == 3:  # Étape Analyse
            self.setupAnalysisStep()
        elif self.current_step == 4:  # Étape Rapport
            self.setupReportStep()
    
    def setupSensorStep(self):
        """
        Configuration de l'étape de sélection des capteurs
        """
        # Titre de l'étape
        step_title = QLabel("Configuration des Capteurs")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        # Description
        description = QLabel("Sélectionnez le nombre de capteurs à calibrer et configurez leurs paramètres.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.5;
        """)
        self.content_layout.addWidget(description)
        
        # Configuration du nombre de capteurs
        config_widget = QWidget()
        config_widget.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        
        config_layout = QFormLayout(config_widget)
        config_layout.setSpacing(20)
        
        self.sensor_count_spinbox = QSpinBox()
        self.sensor_count_spinbox.setRange(1, 16)
        self.sensor_count_spinbox.setValue(4)
        self.sensor_count_spinbox.setMinimumHeight(45)
        self.sensor_count_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 16px;
                font-weight: 500;
            }
            QSpinBox:focus {
                border-color: #3b82f6;
                outline: none;
            }
        """)
        
        label = QLabel("Nombre de Capteurs:")
        label.setStyleSheet("""
            color: #374151;
            font-size: 16px;
            font-weight: 600;
        """)
        
        config_layout.addRow(label, self.sensor_count_spinbox)
        self.content_layout.addWidget(config_widget)
        
        # Tableau des capteurs
        self.sensor_table = QTableWidget()
        self.sensor_table.setColumnCount(3)
        self.sensor_table.setHorizontalHeaderLabels(["Capteur", "Statut", "Action"])
        
        # Configuration du tableau avec style moderne
        header = self.sensor_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.sensor_table.setMinimumHeight(300)
        self.sensor_table.setAlternatingRowColors(True)
        self.sensor_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                gridline-color: #f1f5f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                color: #374151;
                font-weight: 600;
                padding: 15px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
            }
        """)
        
        self.content_layout.addWidget(self.sensor_table)
        
        # Initialisation du tableau
        self.updateSensorTable()
        
        self.content_layout.addStretch()
    
    def setupPointsStep(self):
        """
        Configuration de l'étape de définition des points de mesure
        """
        step_title = QLabel("Points de Mesure")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        description = QLabel("Définissez les points de mesure pour la calibration des capteurs.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
        """)
        self.content_layout.addWidget(description)
        
        # Contenu temporaire pour cette étape
        placeholder = QLabel("Configuration des points de mesure - En développement")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("""
            color: #9ca3af;
            font-size: 18px;
            font-style: italic;
            padding: 60px;
            background-color: #f9fafb;
            border: 2px dashed #d1d5db;
            border-radius: 12px;
        """)
        self.content_layout.addWidget(placeholder)
        self.content_layout.addStretch()
    
    def setupPointsStep(self):
        """
        Configuration de l'étape de sélection des points de calibration
        """
        # Titre de l'étape
        step_title = QLabel("Points de Calibration")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        # Description
        description = QLabel("Configurez le nombre de points de mesure pour chaque capteur.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.5;
        """)
        self.content_layout.addWidget(description)
        
        # Configuration des points
        points_widget = QWidget()
        points_widget.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        
        points_layout = QFormLayout(points_widget)
        points_layout.setSpacing(20)
        
        self.points_count_spinbox = QSpinBox()
        self.points_count_spinbox.setRange(3, 20)
        self.points_count_spinbox.setValue(5)
        self.points_count_spinbox.setMinimumHeight(45)
        self.points_count_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 16px;
                font-weight: 500;
            }
            QSpinBox:focus {
                border-color: #3b82f6;
                outline: none;
            }
        """)
        
        points_label = QLabel("Nombre de Points:")
        points_label.setStyleSheet("""
            color: #374151;
            font-size: 16px;
            font-weight: 600;
        """)
        
        points_layout.addRow(points_label, self.points_count_spinbox)
        self.content_layout.addWidget(points_widget)
        
        # Slider pour visualisation
        slider_widget = QWidget()
        slider_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 30px;
                margin-top: 20px;
            }
        """)
        
        slider_layout = QVBoxLayout(slider_widget)
        
        slider_title = QLabel("Répartition des Points")
        slider_title.setStyleSheet("""
            color: #374151;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
        """)
        slider_layout.addWidget(slider_title)
        
        # Visualisation graphique des points
        from PySide6.QtWidgets import QSlider
        self.points_slider = QSlider(Qt.Horizontal)
        self.points_slider.setRange(3, 20)
        self.points_slider.setValue(5)
        self.points_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #e2e8f0;
                height: 8px;
                background: #f1f5f9;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3b82f6;
                border: 2px solid #1e40af;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #60a5fa;
            }
        """)
        
        slider_layout.addWidget(self.points_slider)
        
        # Synchroniser spinbox et slider
        self.points_count_spinbox.valueChanged.connect(self.points_slider.setValue)
        self.points_slider.valueChanged.connect(self.points_count_spinbox.setValue)
        
        # Connecter aux changements pour mettre à jour measurement_points
        self.points_count_spinbox.valueChanged.connect(self.updateMeasurementPoints)
        
        self.content_layout.addWidget(slider_widget)
        self.content_layout.addStretch()
    
    def setupMeasureStep(self):
        """
        Configuration de l'étape de mesure - Intégration du wizard de calibration
        """
        # Titre de l'étape
        step_title = QLabel("Acquisition des Mesures")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        # Description
        description = QLabel("Enregistrez les points de calibration pour chaque capteur sélectionné.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.5;
        """)
        self.content_layout.addWidget(description)
        
        # Splitter horizontal pour tableau et graphique
        measure_splitter = QSplitter(Qt.Horizontal)
        
        # Zone de saisie des données
        data_widget = QWidget()
        data_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        data_layout = QVBoxLayout(data_widget)
        
        # Sélecteur de capteur
        sensor_selector_layout = QHBoxLayout()
        sensor_label = QLabel("Capteur:")
        sensor_label.setStyleSheet("""
            color: #374151;
            font-size: 16px;
            font-weight: 600;
        """)
        
        self.current_sensor_combo = QComboBox()
        self.current_sensor_combo.setMinimumHeight(40)
        self.current_sensor_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: 500;
                min-width: 150px;
            }
            QComboBox:focus {
                border-color: #3b82f6;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzY0NzQ4YiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
                width: 12px;
                height: 8px;
            }
        """)
        
        sensor_selector_layout.addWidget(sensor_label)
        sensor_selector_layout.addWidget(self.current_sensor_combo)
        sensor_selector_layout.addStretch()
        data_layout.addLayout(sensor_selector_layout)
        
        # Tableau de saisie des points
        self.measurement_table = QTableWidget()
        self.measurement_table.setColumnCount(3)
        self.measurement_table.setHorizontalHeaderLabels(["Point", "Valeur Physique (m)", "Mesure (V)"])
        
        # Configuration du tableau
        header = self.measurement_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.measurement_table.setMinimumHeight(300)
        self.measurement_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #f1f5f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                color: #374151;
                font-weight: 600;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        
        data_layout.addWidget(self.measurement_table)
        
        # Bouton d'enregistrement
        record_button = QPushButton("📊 Enregistrer le Point")
        record_button.setFixedHeight(45)
        record_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #34d399, stop:1 #10b981);
            }
        """)
        record_button.clicked.connect(self.recordMeasurementPoint)
        data_layout.addWidget(record_button)
        
        measure_splitter.addWidget(data_widget)
        
        # Zone graphique
        self.setupMeasurementPlot(measure_splitter)
        
        # Proportions 50/50
        measure_splitter.setSizes([400, 400])
        self.content_layout.addWidget(measure_splitter)
    
    def setupMeasurementPlot(self, parent_splitter):
        """
        Configuration du graphique de mesure en temps réel
        """
        try:
            import pyqtgraph as pg
            
            # Configuration moderne de pyqtgraph
            pg.setConfigOptions(
                antialias=True,
                useOpenGL=True,
                background='#f8fafc',
                foreground='#1e293b'
            )
            
            plot_widget = QWidget()
            plot_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 20px;
                }
            """)
            
            plot_layout = QVBoxLayout(plot_widget)
            
            plot_title = QLabel("Courbe de Calibration en Temps Réel")
            plot_title.setStyleSheet("""
                color: #374151;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 15px;
            """)
            plot_layout.addWidget(plot_title)
            
            # Graphique pyqtgraph moderne
            self.calibration_plot = pg.PlotWidget()
            self.calibration_plot.setTitle('Linéarité de la Calibration', color='#1e293b', size='14pt')
            self.calibration_plot.setLabel('left', 'Mesure (V)', color='#1e293b', size='12pt')
            self.calibration_plot.setLabel('bottom', 'Valeur Physique (m)', color='#1e293b', size='12pt')
            
            # Style moderne du graphique
            self.calibration_plot.getAxis('left').setPen(color='#64748b', width=1)
            self.calibration_plot.getAxis('bottom').setPen(color='#64748b', width=1)
            self.calibration_plot.getAxis('left').setTextPen(color='#374151')
            self.calibration_plot.getAxis('bottom').setTextPen(color='#374151')
            
            # Grille subtile
            self.calibration_plot.showGrid(x=True, y=True, alpha=0.3)
            
            # Courbes de données
            self.scatter_plot = self.calibration_plot.plot(
                [], [], 
                pen=None, 
                symbol='o', 
                symbolBrush='#3b82f6', 
                symbolSize=8,
                name='Points mesurés'
            )
            
            self.line_plot = self.calibration_plot.plot(
                [], [], 
                pen=pg.mkPen(color='#ef4444', width=2, style=Qt.SolidLine),
                name='Régression linéaire'
            )
            
            # Légende moderne
            legend = self.calibration_plot.addLegend()
            legend.setParentItem(self.calibration_plot.getPlotItem())
            
            plot_layout.addWidget(self.calibration_plot)
            parent_splitter.addWidget(plot_widget)
            
        except ImportError:
            # Fallback si pyqtgraph n'est pas disponible
            fallback_widget = QLabel("Graphique non disponible\n(pyqtgraph requis)")
            fallback_widget.setAlignment(Qt.AlignCenter)
            fallback_widget.setStyleSheet("""
                QLabel {
                    background-color: #f8fafc;
                    border: 2px dashed #e2e8f0;
                    border-radius: 12px;
                    color: #64748b;
                    font-size: 16px;
                    padding: 40px;
                }
            """)
            parent_splitter.addWidget(fallback_widget)
        step_title = QLabel("Acquisition des Mesures")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        description = QLabel("Lancez l'acquisition des données de calibration.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
        """)
        self.content_layout.addWidget(description)
        
        # Contenu temporaire
        placeholder = QLabel("Interface d'acquisition - En développement")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("""
            color: #9ca3af;
            font-size: 18px;
            font-style: italic;
            padding: 60px;
            background-color: #f9fafb;
            border: 2px dashed #d1d5db;
            border-radius: 12px;
        """)
        self.content_layout.addWidget(placeholder)
        self.content_layout.addStretch()
    
    def setupAnalysisStep(self):
        """
        Configuration de l'étape d'analyse
        """
        step_title = QLabel("Analyse des Données")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        description = QLabel("Analysez les résultats de calibration et validez les paramètres.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
        """)
        self.content_layout.addWidget(description)
        
        # Contenu temporaire
        placeholder = QLabel("Outils d'analyse - En développement")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("""
            color: #9ca3af;
            font-size: 18px;
            font-style: italic;
            padding: 60px;
            background-color: #f9fafb;
            border: 2px dashed #d1d5db;
            border-radius: 12px;
        """)
        self.content_layout.addWidget(placeholder)
        self.content_layout.addStretch()
    
    def setupReportStep(self):
        """
        Configuration de l'étape de rapport
        """
        step_title = QLabel("Rapport de Calibration")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        description = QLabel("Générez et exportez le rapport de calibration.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
        """)
        self.content_layout.addWidget(description)
        
        # Bouton d'export PDF
        self.export_pdf_button = QPushButton("📄 Exporter le Rapport PDF")
        self.export_pdf_button.setFixedHeight(50)
        self.export_pdf_button.setFixedWidth(250)
        self.export_pdf_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #ef4444, stop:1 #dc2626);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f87171, stop:1 #ef4444);
            }
        """)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.export_pdf_button)
        button_layout.addStretch()
        
        self.content_layout.addLayout(button_layout)
        self.content_layout.addStretch()
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        # Navigation
        self.prev_button.clicked.connect(self.goToPreviousStep)
        self.continue_button.clicked.connect(self.goToNextStep)
        self.finish_button.clicked.connect(self.onFinishClicked)
        
        # Étape capteur
        if hasattr(self, 'sensor_count_spinbox'):
            self.sensor_count_spinbox.valueChanged.connect(self.onSensorCountChanged)
        
        # Export PDF (sera connecté dans setupReportStep)
        if hasattr(self, 'export_pdf_button'):
            self.export_pdf_button.clicked.connect(self.onExportPDFClicked)
    
    def goToStep(self, step_index):
        """
        Navigation vers une étape spécifique
        """
        if 0 <= step_index < len(self.steps):
            self.current_step = step_index
            self.updateStepDisplay()
            self.setupStepContent()
            self.updateNavigationButtons()
    
    def goToNextStep(self):
        """
        Navigation vers l'étape suivante
        """
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.updateStepDisplay()
            self.setupStepContent()
            self.updateNavigationButtons()
    
    def goToPreviousStep(self):
        """
        Navigation vers l'étape précédente
        """
        if self.current_step > 0:
            self.current_step -= 1
            self.updateStepDisplay()
            self.setupStepContent()
            self.updateNavigationButtons()
    
    def updateStepDisplay(self):
        """
        Mise à jour de l'affichage de la progression
        """
        # Mise à jour de la barre de progression
        progress_dots = ""
        for i in range(len(self.steps)):
            if i <= self.current_step:
                progress_dots += "●"
            else:
                progress_dots += "○"
        
        self.progress_label.setText(f"{progress_dots} Progression: Étape {self.current_step + 1}/{len(self.steps)}")
        self.progress_percent.setText(f"{int((self.current_step + 1) / len(self.steps) * 100)}%")
        
        # Mise à jour des boutons de la sidebar
        for i, button in enumerate(self.step_buttons):
            if i == self.current_step:
                button.setStyleSheet(self.getActiveStepStyle())
            elif i < self.current_step:
                button.setStyleSheet(self.getCompletedStepStyle())
            else:
                button.setStyleSheet(self.getInactiveStepStyle())
    
    def updateNavigationButtons(self):
        """
        Mise à jour de l'état des boutons de navigation
        """
        # Bouton Précédent
        self.prev_button.setEnabled(self.current_step > 0)
        
        # Boutons Continuer/Terminer
        if self.current_step == len(self.steps) - 1:  # Dernière étape
            self.continue_button.setVisible(False)
            self.finish_button.setVisible(True)
        else:
            self.continue_button.setVisible(True)
            self.finish_button.setVisible(False)
    
    def getActiveStepStyle(self):
        """
        Style pour l'étape active
        """
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #3b82f6, stop:1 #1e40af);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: 700;
                font-size: 14px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #60a5fa, stop:1 #2563eb);
            }
        """
    
    def getCompletedStepStyle(self):
        """
        Style pour les étapes complétées
        """
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #34d399, stop:1 #10b981);
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 14px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #4ade80, stop:1 #059669);
            }
        """
    
    def getInactiveStepStyle(self):
        """
        Style pour les étapes inactives
        """
        return """
            QPushButton {
                background-color: white;
                color: #64748b;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                font-weight: 500;
                font-size: 14px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background-color: #f8fafc;
                border-color: #cbd5e1;
                color: #475569;
            }
        """
    
    def onFinishClicked(self):
        """
        Gestionnaire pour le bouton Terminer
        """
        # Vérifier que tous les capteurs sont calibrés
        all_calibrated = len(self.calibration_data) == self.sensor_count
        
        if all_calibrated:
            self.calibrationFinished.emit(self.calibration_data)
        else:
            QMessageBox.warning(
                self,
                "Calibration incomplète",
                "Veuillez calibrer tous les capteurs avant de terminer."
            )
    
    def onExportPDFClicked(self):
        """
        Gestionnaire pour l'export PDF
        """
        self.exportCalibrationPDF()
    
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
        
        # Vérifier si on peut exporter le PDF (R² ≥ 0.998 pour tous les capteurs)
        can_export_pdf = all_calibrated and all(
            data.get('r_squared', 0) >= 0.998 
            for data in self.calibration_data.values()
        )
        
        # Mise à jour des boutons si ils existent
        if hasattr(self, 'export_pdf_button'):
            self.export_pdf_button.setEnabled(can_export_pdf)
    
    def finishCalibration(self):
        """
        Finalisation de la calibration et émission du signal (méthode legacy)
        """
        self.onFinishClicked()
    
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
    
    # Méthodes d'intégration pour la vue unifiée
    def updateSensorCombo(self):
        """
        Met à jour la liste des capteurs dans le combo
        """
        if hasattr(self, 'current_sensor_combo'):
            self.current_sensor_combo.clear()
            for i in range(self.sensor_count):
                self.current_sensor_combo.addItem(f"Capteur {i+1}")
    
    def updateMeasurementTable(self):
        """
        Met à jour le tableau de mesure avec le nombre de points configuré
        """
        if hasattr(self, 'measurement_table'):
            points_count = getattr(self, 'measurement_points', 5)
            self.measurement_table.setRowCount(points_count)
            
            for row in range(points_count):
                # Numéro du point
                point_item = QTableWidgetItem(f"Point {row + 1}")
                point_item.setFlags(point_item.flags() & ~Qt.ItemIsEditable)
                self.measurement_table.setItem(row, 0, point_item)
                
                # Valeur physique (éditable)
                physical_item = QTableWidgetItem(f"{row * 100:.1f}")
                self.measurement_table.setItem(row, 1, physical_item)
                
                # Mesure (éditable)
                measure_item = QTableWidgetItem("")
                self.measurement_table.setItem(row, 2, measure_item)
    
    def recordMeasurementPoint(self):
        """
        Enregistre un point de mesure depuis le tableau
        """
        if not hasattr(self, 'measurement_table'):
            return
            
        current_sensor = self.current_sensor_combo.currentText()
        
        # Collecte des données du tableau
        points_data = []
        for row in range(self.measurement_table.rowCount()):
            physical_item = self.measurement_table.item(row, 1)
            measure_item = self.measurement_table.item(row, 2)
            
            if physical_item and measure_item and measure_item.text():
                try:
                    physical_value = float(physical_item.text())
                    measure_value = float(measure_item.text())
                    points_data.append({
                        'physical': physical_value,
                        'measure': measure_value
                    })
                except ValueError:
                    continue
        
        # Stockage des données
        if current_sensor not in self.calibration_data:
            self.calibration_data[current_sensor] = []
        
        self.calibration_data[current_sensor] = points_data
        
        # Mise à jour du graphique
        self.updateCalibrationPlot(points_data)
        
        # Message de confirmation
        QMessageBox.information(self, "Point enregistré", 
                               f"Données enregistrées pour {current_sensor}\n"
                               f"{len(points_data)} points de mesure")
    
    def updateCalibrationPlot(self, points_data):
        """
        Met à jour le graphique de calibration
        """
        if not hasattr(self, 'calibration_plot') or not points_data:
            return
            
        try:
            # Extraction des données
            physical_values = [p['physical'] for p in points_data]
            measure_values = [p['measure'] for p in points_data]
            
            # Mise à jour des points
            self.scatter_plot.setData(physical_values, measure_values)
            
            # Calcul et affichage de la régression linéaire
            if len(points_data) >= 2:
                coeffs = np.polyfit(physical_values, measure_values, 1)
                x_range = np.linspace(min(physical_values), max(physical_values), 100)
                y_fit = np.polyval(coeffs, x_range)
                self.line_plot.setData(x_range, y_fit)
                
        except Exception as e:
             print(f"Erreur mise à jour graphique: {e}")
    
    def updateMeasurementPoints(self, value):
        """
        Met à jour le nombre de points de mesure
        """
        self.measurement_points = value
        
        # Si on est à l'étape de mesure, mettre à jour le tableau
        if self.current_step == 2 and hasattr(self, 'measurement_table'):
            self.updateMeasurementTable()
    
    def setupAnalysisStep(self):
        """
        Configuration de l'étape d'analyse des résultats
        """
        # Titre de l'étape
        step_title = QLabel("Analyse des Résultats")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        # Description
        description = QLabel("Analysez la qualité de la calibration et validez les résultats.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.5;
        """)
        self.content_layout.addWidget(description)
        
        # Zone d'analyse
        analysis_widget = QWidget()
        analysis_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        
        analysis_layout = QVBoxLayout(analysis_widget)
        
        # Résumé des données
        summary_label = QLabel("Résumé de la Calibration")
        summary_label.setStyleSheet("""
            color: #374151;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
        """)
        analysis_layout.addWidget(summary_label)
        
        # Affichage des résultats
        self.analysis_text = QTextEdit()
        self.analysis_text.setMinimumHeight(200)
        self.analysis_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        
        # Générer le résumé d'analyse
        self.generateAnalysisSummary()
        
        analysis_layout.addWidget(self.analysis_text)
        self.content_layout.addWidget(analysis_widget)
        self.content_layout.addStretch()
    
    def setupReportStep(self):
        """
        Configuration de l'étape de génération du rapport
        """
        # Titre de l'étape
        step_title = QLabel("Rapport de Calibration")
        step_title.setStyleSheet("""
            color: #1e40af;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        """)
        self.content_layout.addWidget(step_title)
        
        # Description
        description = QLabel("Générez et exportez le rapport final de calibration.")
        description.setStyleSheet("""
            color: #64748b;
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.5;
        """)
        self.content_layout.addWidget(description)
        
        # Zone de rapport
        report_widget = QWidget()
        report_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        
        report_layout = QVBoxLayout(report_widget)
        
        # Boutons d'export
        export_layout = QHBoxLayout()
        
        self.export_pdf_button = QPushButton("📄 Exporter PDF")
        self.export_pdf_button.setFixedHeight(45)
        self.export_pdf_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #ef4444, stop:1 #dc2626);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f87171, stop:1 #ef4444);
            }
        """)
        self.export_pdf_button.clicked.connect(self.onExportPDFClicked)
        
        export_json_button = QPushButton("💾 Exporter JSON")
        export_json_button.setFixedHeight(45)
        export_json_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #8b5cf6, stop:1 #7c3aed);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #a78bfa, stop:1 #8b5cf6);
            }
        """)
        export_json_button.clicked.connect(self.exportCalibrationJSON)
        
        export_layout.addWidget(self.export_pdf_button)
        export_layout.addWidget(export_json_button)
        export_layout.addStretch()
        
        report_layout.addLayout(export_layout)
        self.content_layout.addWidget(report_widget)
        self.content_layout.addStretch()
    
    def generateAnalysisSummary(self):
        """
        Génère un résumé de l'analyse de calibration
        """
        summary = "=== RÉSUMÉ DE CALIBRATION CHNeoWave ===\n\n"
        summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += f"Nombre de capteurs: {self.sensor_count}\n"
        summary += f"Points de mesure: {self.measurement_points}\n\n"
        
        if self.calibration_data:
            summary += "DONNÉES DE CALIBRATION:\n"
            for sensor, data in self.calibration_data.items():
                summary += f"\n{sensor}:\n"
                summary += f"  - Points enregistrés: {len(data)}\n"
                if len(data) >= 2:
                    # Calcul de la régression
                    physical_values = [p['physical'] for p in data]
                    measure_values = [p['measure'] for p in data]
                    coeffs = np.polyfit(physical_values, measure_values, 1)
                    slope, intercept = coeffs[0], coeffs[1]
                    
                    # Calcul du R²
                    fit_values = np.polyval(coeffs, physical_values)
                    ss_res = np.sum((measure_values - fit_values) ** 2)
                    ss_tot = np.sum((measure_values - np.mean(measure_values)) ** 2)
                    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                    
                    summary += f"  - Pente: {slope:.6f} V/mm\n"
                    summary += f"  - Offset: {intercept:.6f} V\n"
                    summary += f"  - R²: {r_squared:.6f}\n"
                    summary += f"  - Linéarité: {'✓ Acceptable' if r_squared > 0.998 else '⚠ Non-linéaire'}\n"
        else:
            summary += "Aucune donnée de calibration disponible.\n"
        
        summary += "\n=== FIN DU RÉSUMÉ ===\n"
        
        if hasattr(self, 'analysis_text'):
            self.analysis_text.setPlainText(summary)
    
    def exportCalibrationJSON(self):
        """
        Exporte les données de calibration en JSON
        """
        if not self.calibration_data:
            QMessageBox.warning(self, "Aucune donnée", "Aucune donnée de calibration à exporter.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter Calibration JSON", 
            f"calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "Fichiers JSON (*.json)"
        )
        
        if filename:
            try:
                export_data = {
                    'metadata': {
                        'timestamp': datetime.now().isoformat(),
                        'sensor_count': self.sensor_count,
                        'measurement_points': self.measurement_points,
                        'software': 'CHNeoWave',
                        'version': '1.0.0'
                    },
                    'calibration_data': self.calibration_data
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                QMessageBox.information(self, "Export réussi", 
                                       f"Données exportées vers:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur d'export", 
                                   f"Erreur lors de l'export:\n{str(e)}")

# Import nécessaire pour QApplication
from PySide6.QtWidgets import QApplication