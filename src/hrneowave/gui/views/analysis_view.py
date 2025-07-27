# -*- coding: utf-8 -*-
"""
Analysis View - Maritime Theme 2025
Vue d'analyse des données avec design maritime et Golden Ratio
"""

from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QTextEdit, QSplitter, QProgressBar, QSlider,
    QTabWidget, QScrollArea, QSpacerItem, QSizePolicy, QListWidget,
    QListWidgetItem, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPixmap

# Golden Ratio Constants
FIBONACCI_SPACING = [8, 13, 21, 34, 55, 89]
GOLDEN_RATIO = 1.618

class AnalysisToolsPanel(QFrame):
    """
    Panneau d'outils d'analyse
    """
    
    # Signaux
    analysis_requested = Signal(str, dict)  # type d'analyse, paramètres
    filter_applied = Signal(str, dict)      # type de filtre, paramètres
    export_requested = Signal(str)          # format d'export
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configure l'interface du panneau d'outils"""
        self.setObjectName("analysis_tools_panel")
        self.setFixedWidth(int(280 * GOLDEN_RATIO))  # ~453px
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # En-tête
        self.setup_header(main_layout)
        
        # Zone de défilement
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Widget conteneur
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(FIBONACCI_SPACING[2])
        content_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[1], 
                                         FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        
        # Sections du panneau
        self.setup_data_selection(content_layout)
        self.setup_filters_section(content_layout)
        self.setup_analysis_section(content_layout)
        self.setup_export_section(content_layout)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Style du panneau
        self.setStyleSheet("""
            QFrame#analysis_tools_panel {
                background-color: #F5FBFF;
                border-right: 2px solid #E0E7FF;
            }
        """)
        
    def setup_header(self, parent_layout):
        """Configure l'en-tête du panneau"""
        header_frame = QFrame()
        header_frame.setObjectName("tools_panel_header")
        header_frame.setFixedHeight(89)  # Fibonacci
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                        FIBONACCI_SPACING[2], FIBONACCI_SPACING[1])
        header_layout.setSpacing(FIBONACCI_SPACING[0])
        
        # Titre
        title_label = QLabel("Outils d'Analyse")
        title_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #0A1929;")
        
        # Sous-titre
        subtitle_label = QLabel("Traitement et analyse")
        subtitle_label.setFont(QFont("Inter", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #445868;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        # Style du header
        header_frame.setStyleSheet("""
            QFrame#tools_panel_header {
                background-color: #F5FBFF;
                border-bottom: 2px solid #E0E7FF;
            }
        """)
        
        parent_layout.addWidget(header_frame)
        
    def setup_data_selection(self, parent_layout):
        """Configure la section de sélection des données"""
        data_group = QGroupBox("Sélection des Données")
        data_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        data_layout = QVBoxLayout(data_group)
        data_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Liste des fichiers de données
        self.data_list = QListWidget()
        self.data_list.setMaximumHeight(120)
        self.data_list.setFont(QFont("Inter", 11))
        
        # Ajouter des éléments d'exemple
        sample_files = [
            "📊 acquisition_2025_01_15_10h30.csv",
            "📊 test_calibration_2025_01_14.csv",
            "📊 mesure_houle_2025_01_13.csv"
        ]
        
        for file_name in sample_files:
            item = QListWidgetItem(file_name)
            item.setFont(QFont("Inter", 11))
            self.data_list.addItem(item)
            
        # Sélectionner le premier élément
        if self.data_list.count() > 0:
            self.data_list.setCurrentRow(0)
            
        # Boutons de gestion des fichiers
        file_buttons_layout = QHBoxLayout()
        file_buttons_layout.setSpacing(FIBONACCI_SPACING[0])
        
        load_button = QPushButton("📁 Charger")
        load_button.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        load_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        refresh_button = QPushButton("🔄 Actualiser")
        refresh_button.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        refresh_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        file_buttons_layout.addWidget(load_button)
        file_buttons_layout.addWidget(refresh_button)
        
        # Style des boutons
        button_style = """
            QPushButton {
                background-color: #2B79B6;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 5px 8px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """
        
        load_button.setStyleSheet(button_style)
        refresh_button.setStyleSheet(button_style)
        
        # Style de la liste
        self.data_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
                padding: 5px;
            }
            
            QListWidget::item {
                padding: 5px;
                border-radius: 5px;
                margin: 1px;
            }
            
            QListWidget::item:selected {
                background-color: rgba(0, 172, 193, 0.2);
                color: #0A1929;
            }
            
            QListWidget::item:hover {
                background-color: rgba(0, 172, 193, 0.1);
            }
        """)
        
        # Assemblage
        data_layout.addWidget(self.data_list)
        data_layout.addLayout(file_buttons_layout)
        
        parent_layout.addWidget(data_group)
        
    def setup_filters_section(self, parent_layout):
        """Configure la section des filtres"""
        filters_group = QGroupBox("Filtres")
        filters_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        filters_layout = QVBoxLayout(filters_group)
        filters_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Type de filtre
        filter_type_layout = QHBoxLayout()
        filter_type_layout.setSpacing(FIBONACCI_SPACING[1])
        
        filter_label = QLabel("Type:")
        filter_label.setFont(QFont("Inter", 12))
        filter_label.setFixedWidth(50)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "Passe-bas", "Passe-haut", "Passe-bande", 
            "Coupe-bande", "Moyennage", "Médian"
        ])
        self.filter_combo.setFont(QFont("Inter", 11))
        
        filter_type_layout.addWidget(filter_label)
        filter_type_layout.addWidget(self.filter_combo)
        
        # Fréquence de coupure
        freq_layout = QHBoxLayout()
        freq_layout.setSpacing(FIBONACCI_SPACING[1])
        
        freq_label = QLabel("Freq:")
        freq_label.setFont(QFont("Inter", 12))
        freq_label.setFixedWidth(50)
        
        self.freq_spinbox = QDoubleSpinBox()
        self.freq_spinbox.setRange(0.1, 1000.0)
        self.freq_spinbox.setValue(10.0)
        self.freq_spinbox.setSuffix(" Hz")
        self.freq_spinbox.setFont(QFont("Inter", 11))
        
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.freq_spinbox)
        
        # Ordre du filtre
        order_layout = QHBoxLayout()
        order_layout.setSpacing(FIBONACCI_SPACING[1])
        
        order_label = QLabel("Ordre:")
        order_label.setFont(QFont("Inter", 12))
        order_label.setFixedWidth(50)
        
        self.order_spinbox = QSpinBox()
        self.order_spinbox.setRange(1, 10)
        self.order_spinbox.setValue(4)
        self.order_spinbox.setFont(QFont("Inter", 11))
        
        order_layout.addWidget(order_label)
        order_layout.addWidget(self.order_spinbox)
        
        # Bouton d'application
        self.apply_filter_button = QPushButton("🔧 Appliquer le Filtre")
        self.apply_filter_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.apply_filter_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        self.apply_filter_button.clicked.connect(self.apply_filter)
        
        # Style du bouton
        self.apply_filter_button.setStyleSheet("""
            QPushButton {
                background-color: #00ACC1;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 8px 13px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #0097A7;
            }
            
            QPushButton:pressed {
                background-color: #00838F;
            }
        """)
        
        # Assemblage
        filters_layout.addLayout(filter_type_layout)
        filters_layout.addLayout(freq_layout)
        filters_layout.addLayout(order_layout)
        filters_layout.addWidget(self.apply_filter_button)
        
        parent_layout.addWidget(filters_group)
        
    def setup_analysis_section(self, parent_layout):
        """Configure la section d'analyse"""
        analysis_group = QGroupBox("Analyses")
        analysis_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        analysis_layout = QVBoxLayout(analysis_group)
        analysis_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Boutons d'analyse
        analysis_buttons = [
            ("📊 Analyse Statistique", "statistics"),
            ("🌊 Analyse Spectrale", "spectral"),
            ("📈 Analyse Temporelle", "temporal"),
            ("🔍 Détection de Pics", "peaks"),
            ("📉 Analyse de Tendance", "trend"),
            ("🎯 Corrélation", "correlation")
        ]
        
        for button_text, analysis_type in analysis_buttons:
            button = QPushButton(button_text)
            button.setFont(QFont("Inter", 11, QFont.Weight.Medium))
            button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
            button.clicked.connect(lambda checked, t=analysis_type: self.request_analysis(t))
            
            # Style du bouton
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2B79B6;
                    color: #F5FBFF;
                    border: none;
                    border-radius: 17px;
                    padding: 8px 13px;
                    font-weight: 500;
                    text-align: left;
                }
                
                QPushButton:hover {
                    background-color: #1976D2;
                }
                
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
            
            analysis_layout.addWidget(button)
            
        parent_layout.addWidget(analysis_group)
        
    def setup_export_section(self, parent_layout):
        """Configure la section d'export"""
        export_group = QGroupBox("Export")
        export_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        export_layout = QVBoxLayout(export_group)
        export_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Boutons d'export
        export_buttons = [
            ("💾 Export CSV", "csv"),
            ("📊 Export Excel", "excel"),
            ("📈 Export Graphique", "image"),
            ("📋 Rapport PDF", "pdf")
        ]
        
        for button_text, export_type in export_buttons:
            button = QPushButton(button_text)
            button.setFont(QFont("Inter", 11, QFont.Weight.Medium))
            button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
            button.clicked.connect(lambda checked, t=export_type: self.request_export(t))
            
            # Style du bouton
            button.setStyleSheet("""
                QPushButton {
                    background-color: #055080;
                    color: #F5FBFF;
                    border: none;
                    border-radius: 17px;
                    padding: 8px 13px;
                    font-weight: 500;
                    text-align: left;
                }
                
                QPushButton:hover {
                    background-color: #044A73;
                }
                
                QPushButton:pressed {
                    background-color: #033D66;
                }
            """)
            
            export_layout.addWidget(button)
            
        parent_layout.addWidget(export_group)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        pass  # Les connexions sont faites dans les méthodes setup
        
    def apply_filter(self):
        """Applique le filtre sélectionné"""
        filter_type = self.filter_combo.currentText()
        params = {
            'frequency': self.freq_spinbox.value(),
            'order': self.order_spinbox.value()
        }
        
        self.filter_applied.emit(filter_type, params)
        
    def request_analysis(self, analysis_type: str):
        """Demande une analyse"""
        params = {}  # Paramètres par défaut
        self.analysis_requested.emit(analysis_type, params)
        
    def request_export(self, export_type: str):
        """Demande un export"""
        self.export_requested.emit(export_type)


class AnalysisResultsArea(QFrame):
    """
    Zone d'affichage des résultats d'analyse
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface des résultats"""
        self.setObjectName("analysis_results_area")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                      FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        main_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # En-tête
        self.setup_header(main_layout)
        
        # Onglets de résultats
        self.setup_results_tabs(main_layout)
        
        # Style de base
        self.setStyleSheet("""
            QFrame#analysis_results_area {
                background-color: #F5FBFF;
            }
        """)
        
    def setup_header(self, parent_layout):
        """Configure l'en-tête des résultats"""
        header_frame = QFrame()
        header_frame.setFixedHeight(55)  # Fibonacci
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, FIBONACCI_SPACING[1], 0, FIBONACCI_SPACING[1])
        header_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title_label = QLabel("Résultats d'Analyse")
        title_label.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0A1929;")
        
        # Indicateurs de statut
        status_layout = QHBoxLayout()
        status_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Statut de l'analyse
        self.analysis_status_label = QLabel("📊 Prêt")
        self.analysis_status_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.analysis_status_label.setStyleSheet("""
            background-color: rgba(76, 175, 80, 0.1);
            color: #4CAF50;
            padding: 5px 10px;
            border-radius: 10px;
        """)
        
        # Nombre d'analyses
        self.analysis_count_label = QLabel("0 Analyses")
        self.analysis_count_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.analysis_count_label.setStyleSheet("""
            background-color: rgba(43, 121, 182, 0.1);
            color: #2B79B6;
            padding: 5px 10px;
            border-radius: 10px;
        """)
        
        status_layout.addWidget(self.analysis_status_label)
        status_layout.addWidget(self.analysis_count_label)
        
        # Assemblage
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addLayout(status_layout)
        
        parent_layout.addWidget(header_frame)
        
    def setup_results_tabs(self, parent_layout):
        """Configure les onglets de résultats"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Inter", 12))
        
        # Onglet Graphiques
        graphs_tab = self.create_graphs_tab()
        self.tab_widget.addTab(graphs_tab, "📈 Graphiques")
        
        # Onglet Statistiques
        stats_tab = self.create_statistics_tab()
        self.tab_widget.addTab(stats_tab, "📊 Statistiques")
        
        # Onglet Spectral
        spectral_tab = self.create_spectral_tab()
        self.tab_widget.addTab(spectral_tab, "🌊 Spectral")
        
        # Onglet Rapport
        report_tab = self.create_report_tab()
        self.tab_widget.addTab(report_tab, "📋 Rapport")
        
        # Style des onglets
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #E0E7FF;
                border-radius: 13px;
                background-color: white;
            }
            
            QTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background-color: #F5FBFF;
                color: #445868;
                padding: 8px 21px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
            }
            
            QTabBar::tab:selected {
                background-color: #00ACC1;
                color: #F5FBFF;
                font-weight: 600;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: rgba(0, 172, 193, 0.1);
                color: #00ACC1;
            }
        """)
        
        parent_layout.addWidget(self.tab_widget)
        
    def create_graphs_tab(self) -> QWidget:
        """Crée l'onglet des graphiques"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                 FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Zone de graphique principal
        main_graph_frame = QFrame()
        main_graph_frame.setObjectName("analysis_main_graph")
        main_graph_frame.setMinimumHeight(400)
        main_graph_frame.setStyleSheet("""
            QFrame#analysis_main_graph {
                background-color: #F5FBFF;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
            }
        """)
        
        main_graph_layout = QVBoxLayout(main_graph_frame)
        main_graph_placeholder = QLabel("📈 Graphique d'Analyse Principal")
        main_graph_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_graph_placeholder.setFont(QFont("Inter", 16))
        main_graph_placeholder.setStyleSheet("color: #445868;")
        main_graph_layout.addWidget(main_graph_placeholder)
        
        # Contrôles du graphique
        controls_frame = QFrame()
        controls_frame.setFixedHeight(55)  # Fibonacci
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Type de graphique
        graph_type_label = QLabel("Type:")
        graph_type_label.setFont(QFont("Inter", 12))
        
        graph_type_combo = QComboBox()
        graph_type_combo.addItems(["Ligne", "Points", "Barres", "Histogramme"])
        graph_type_combo.setFont(QFont("Inter", 12))
        
        # Échelle
        scale_label = QLabel("Échelle:")
        scale_label.setFont(QFont("Inter", 12))
        
        scale_combo = QComboBox()
        scale_combo.addItems(["Linéaire", "Logarithmique"])
        scale_combo.setFont(QFont("Inter", 12))
        
        # Boutons d'action
        zoom_button = QPushButton("🔍 Zoom")
        zoom_button.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        zoom_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        reset_button = QPushButton("🔄 Reset")
        reset_button.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        reset_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        # Style des boutons
        button_style = """
            QPushButton {
                background-color: #2B79B6;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 8px 13px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """
        
        zoom_button.setStyleSheet(button_style)
        reset_button.setStyleSheet(button_style)
        
        controls_layout.addWidget(graph_type_label)
        controls_layout.addWidget(graph_type_combo)
        controls_layout.addWidget(scale_label)
        controls_layout.addWidget(scale_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(zoom_button)
        controls_layout.addWidget(reset_button)
        
        layout.addWidget(main_graph_frame)
        layout.addWidget(controls_frame)
        
        return tab
        
    def create_statistics_tab(self) -> QWidget:
        """Crée l'onglet des statistiques"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                 FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Tableau des statistiques
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(4)
        self.stats_table.setHorizontalHeaderLabels(["Paramètre", "Canal 1", "Canal 2", "Canal 3"])
        self.stats_table.setFont(QFont("Inter", 11))
        
        # Données d'exemple
        stats_data = [
            ["Moyenne", "1.234", "2.567", "3.890"],
            ["Médiane", "1.235", "2.568", "3.891"],
            ["Écart-type", "0.123", "0.256", "0.389"],
            ["Variance", "0.015", "0.066", "0.151"],
            ["Min", "0.890", "1.234", "2.567"],
            ["Max", "1.678", "3.456", "4.789"],
            ["RMS", "1.240", "2.570", "3.895"],
            ["Kurtosis", "2.98", "3.12", "2.87"],
            ["Skewness", "0.12", "-0.05", "0.23"]
        ]
        
        self.stats_table.setRowCount(len(stats_data))
        
        for row, data in enumerate(stats_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setFont(QFont("Inter", 11))
                if col == 0:  # Première colonne (paramètre)
                    item.setFont(QFont("Inter", 11, QFont.Weight.Medium))
                self.stats_table.setItem(row, col, item)
                
        # Configuration du tableau
        header = self.stats_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stats_table.verticalHeader().setVisible(False)
        
        # Style du tableau
        self.stats_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
                gridline-color: #E0E7FF;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }
            
            QTableWidget::item:selected {
                background-color: rgba(0, 172, 193, 0.2);
            }
            
            QHeaderView::section {
                background-color: #F5FBFF;
                color: #0A1929;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #E0E7FF;
                font-weight: 600;
            }
        """)
        
        layout.addWidget(self.stats_table)
        
        return tab
        
    def create_spectral_tab(self) -> QWidget:
        """Crée l'onglet spectral"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                 FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Contrôles spectraux
        controls_frame = QFrame()
        controls_frame.setFixedHeight(55)  # Fibonacci
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Type d'analyse
        analysis_label = QLabel("Analyse:")
        analysis_label.setFont(QFont("Inter", 12))
        
        analysis_combo = QComboBox()
        analysis_combo.addItems(["FFT", "PSD", "Spectrogramme", "Cohérence"])
        analysis_combo.setFont(QFont("Inter", 12))
        
        # Fenêtrage
        window_label = QLabel("Fenêtre:")
        window_label.setFont(QFont("Inter", 12))
        
        window_combo = QComboBox()
        window_combo.addItems(["Hanning", "Hamming", "Blackman", "Kaiser"])
        window_combo.setFont(QFont("Inter", 12))
        
        # Bouton de calcul
        compute_button = QPushButton("🔬 Calculer")
        compute_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        compute_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        compute_button.setStyleSheet("""
            QPushButton {
                background-color: #00ACC1;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 8px 13px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #0097A7;
            }
            
            QPushButton:pressed {
                background-color: #00838F;
            }
        """)
        
        controls_layout.addWidget(analysis_label)
        controls_layout.addWidget(analysis_combo)
        controls_layout.addWidget(window_label)
        controls_layout.addWidget(window_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(compute_button)
        
        # Zone de graphique spectral
        spectral_frame = QFrame()
        spectral_frame.setObjectName("spectral_graph")
        spectral_frame.setStyleSheet("""
            QFrame#spectral_graph {
                background-color: #F5FBFF;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
            }
        """)
        
        spectral_layout = QVBoxLayout(spectral_frame)
        spectral_placeholder = QLabel("🌊 Analyse Spectrale")
        spectral_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spectral_placeholder.setFont(QFont("Inter", 16))
        spectral_placeholder.setStyleSheet("color: #445868;")
        spectral_layout.addWidget(spectral_placeholder)
        
        layout.addWidget(controls_frame)
        layout.addWidget(spectral_frame)
        
        return tab
        
    def create_report_tab(self) -> QWidget:
        """Crée l'onglet de rapport"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                 FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # En-tête du rapport
        report_header = QFrame()
        report_header.setFixedHeight(89)  # Fibonacci
        report_header_layout = QVBoxLayout(report_header)
        report_header_layout.setSpacing(FIBONACCI_SPACING[0])
        
        report_title = QLabel("Rapport d'Analyse")
        report_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        report_title.setStyleSheet("color: #0A1929;")
        
        report_date = QLabel("Généré le: 2025-01-XX à 10:30")
        report_date.setFont(QFont("Inter", 12))
        report_date.setStyleSheet("color: #445868;")
        
        report_header_layout.addWidget(report_title)
        report_header_layout.addWidget(report_date)
        
        # Contenu du rapport
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Inter", 11))
        
        # Contenu d'exemple
        report_content = """
# Rapport d'Analyse des Données

## Résumé Exécutif
Analyse complète des données d'acquisition maritime effectuée le 2025-01-XX.

## Données Analysées
- Fichier: acquisition_2025_01_15_10h30.csv
- Durée: 60 secondes
- Fréquence d'échantillonnage: 1000 Hz
- Nombre de canaux: 4

## Résultats Statistiques
### Canal 1 - Pression
- Moyenne: 1.234 bar
- Écart-type: 0.123 bar
- Plage: 0.890 - 1.678 bar

### Canal 2 - Température
- Moyenne: 20.5°C
- Écart-type: 0.8°C
- Plage: 19.2 - 22.1°C

## Analyse Spectrale
- Fréquence dominante: 2.5 Hz
- Harmoniques détectées: 5.0 Hz, 7.5 Hz
- Bruit de fond: -40 dB

## Conclusions
1. Les données présentent une bonne qualité signal/bruit
2. Aucune anomalie détectée
3. Les mesures sont conformes aux spécifications

## Recommandations
- Maintenir les paramètres d'acquisition actuels
- Surveiller l'évolution de la fréquence dominante
- Effectuer une calibration mensuelle
        """
        
        self.report_text.setPlainText(report_content)
        
        # Style du rapport
        self.report_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
                padding: 13px;
                line-height: 1.5;
            }
        """)
        
        # Boutons d'action
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(FIBONACCI_SPACING[1])
        
        generate_button = QPushButton("🔄 Régénérer")
        generate_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        generate_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        export_pdf_button = QPushButton("📄 Export PDF")
        export_pdf_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        export_pdf_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        
        # Style des boutons
        button_style = """
            QPushButton {
                background-color: #055080;
                color: #F5FBFF;
                border: none;
                border-radius: 17px;
                padding: 8px 13px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #044A73;
            }
            
            QPushButton:pressed {
                background-color: #033D66;
            }
        """
        
        generate_button.setStyleSheet(button_style)
        export_pdf_button.setStyleSheet(button_style)
        
        actions_layout.addStretch()
        actions_layout.addWidget(generate_button)
        actions_layout.addWidget(export_pdf_button)
        
        layout.addWidget(report_header)
        layout.addWidget(self.report_text)
        layout.addLayout(actions_layout)
        
        return tab
        
    def update_analysis_status(self, status: str, count: int = 0):
        """Met à jour le statut d'analyse"""
        self.analysis_status_label.setText(status)
        self.analysis_count_label.setText(f"{count} Analyses")


class AnalysisView(QWidget):
    """
    Vue principale d'analyse avec design maritime
    """
    
    # Signaux
    analysis_completed = Signal(str, dict)  # type d'analyse, résultats
    filter_applied = Signal(str, dict)      # type de filtre, paramètres
    data_exported = Signal(str)             # chemin du fichier exporté
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_dark_mode = False
        self.analysis_count = 0
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configure l'interface principale"""
        self.setObjectName("analysis_view")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter horizontal (outils + résultats)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panneau d'outils
        self.tools_panel = AnalysisToolsPanel()
        splitter.addWidget(self.tools_panel)
        
        # Zone de résultats
        self.results_area = AnalysisResultsArea()
        splitter.addWidget(self.results_area)
        
        # Proportions du splitter (Golden Ratio)
        tools_width = int(280 * GOLDEN_RATIO)  # ~453px
        results_width = int(tools_width * GOLDEN_RATIO)  # ~733px
        splitter.setSizes([tools_width, results_width])
        splitter.setCollapsible(0, False)  # Outils non collapsible
        splitter.setCollapsible(1, False)  # Résultats non collapsible
        
        main_layout.addWidget(splitter)
        
        # Style de base
        self.setStyleSheet("""
            QWidget#analysis_view {
                background-color: #F5FBFF;
            }
        """)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        # Connexions du panneau d'outils
        self.tools_panel.analysis_requested.connect(self.on_analysis_requested)
        self.tools_panel.filter_applied.connect(self.on_filter_applied)
        self.tools_panel.export_requested.connect(self.on_export_requested)
        
    def on_analysis_requested(self, analysis_type: str, params: dict):
        """Gestionnaire de demande d'analyse"""
        print(f"Analyse demandée: {analysis_type} avec paramètres: {params}")
        
        # Simuler l'analyse
        self.analysis_count += 1
        self.results_area.update_analysis_status(f"🔬 Analyse en cours...", self.analysis_count)
        
        # Émettre le signal
        results = {"status": "completed", "data": "sample_results"}
        self.analysis_completed.emit(analysis_type, results)
        
        # Mettre à jour le statut
        self.results_area.update_analysis_status(f"✅ Analyse terminée", self.analysis_count)
        
    def on_filter_applied(self, filter_type: str, params: dict):
        """Gestionnaire d'application de filtre"""
        print(f"Filtre appliqué: {filter_type} avec paramètres: {params}")
        
        # Émettre le signal
        self.filter_applied.emit(filter_type, params)
        
    def on_export_requested(self, export_type: str):
        """Gestionnaire de demande d'export"""
        print(f"Export demandé: {export_type}")
        
        # Simuler l'export
        filename = f"analysis_export.{export_type}"
        self.data_exported.emit(filename)
        
    def set_theme(self, is_dark: bool):
        """Applique le thème sombre ou clair"""
        self.is_dark_mode = is_dark
        
        if is_dark:
            # Thème sombre
            self.setStyleSheet("""
                QWidget#analysis_view {
                    background-color: #0A1929;
                    color: #F5FBFF;
                }
            """)
        else:
            # Thème clair
            self.setStyleSheet("""
                QWidget#analysis_view {
                    background-color: #F5FBFF;
                    color: #0A1929;
                }
            """)
            
    def load_data_file(self, file_path: str):
        """Charge un fichier de données pour analyse"""
        print(f"Chargement du fichier: {file_path}")
        # Logique de chargement des données
        
    def get_analysis_results(self) -> dict:
        """Retourne les résultats d'analyse actuels"""
        return {
            "analysis_count": self.analysis_count,
            "current_data": "sample_data",
            "last_analysis": "spectral"
        }
        
    def clear_results(self):
        """Efface tous les résultats d'analyse"""
        self.analysis_count = 0
        self.results_area.update_analysis_status("📊 Prêt", 0)