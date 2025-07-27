# -*- coding: utf-8 -*-
"""
Report View - Maritime Theme 2025
Vue de génération et visualisation de rapports avec design maritime et Golden Ratio
"""

from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QTextEdit, QSplitter, QProgressBar, QSlider,
    QTabWidget, QScrollArea, QSpacerItem, QSizePolicy, QListWidget,
    QListWidgetItem, QTableWidget, QTableWidgetItem, QHeaderView,
    QDateEdit, QLineEdit, QFormLayout, QFileDialog, QMessageBox
)
from PySide6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPixmap, QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

# Golden Ratio Constants
FIBONACCI_SPACING = [8, 13, 21, 34, 55, 89]
GOLDEN_RATIO = 1.618

class ReportConfigPanel(QFrame):
    """
    Panneau de configuration des rapports
    """
    
    # Signaux
    report_generated = Signal(str, dict)  # type de rapport, configuration
    template_selected = Signal(str)       # template sélectionné
    export_requested = Signal(str, str)   # format, chemin
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configure l'interface du panneau de configuration"""
        self.setObjectName("report_config_panel")
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
        self.setup_template_section(content_layout)
        self.setup_content_section(content_layout)
        self.setup_metadata_section(content_layout)
        self.setup_export_section(content_layout)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Style du panneau
        self.setStyleSheet("""
            QFrame#report_config_panel {
                background-color: #F5FBFF;
                border-right: 2px solid #E0E7FF;
            }
        """)
        
    def setup_header(self, parent_layout):
        """Configure l'en-tête du panneau"""
        header_frame = QFrame()
        header_frame.setObjectName("config_panel_header")
        header_frame.setFixedHeight(89)  # Fibonacci
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                        FIBONACCI_SPACING[2], FIBONACCI_SPACING[1])
        header_layout.setSpacing(FIBONACCI_SPACING[0])
        
        # Titre
        title_label = QLabel("Configuration")
        title_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #0A1929;")
        
        # Sous-titre
        subtitle_label = QLabel("Génération de rapports")
        subtitle_label.setFont(QFont("Inter", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #445868;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        # Style du header
        header_frame.setStyleSheet("""
            QFrame#config_panel_header {
                background-color: #F5FBFF;
                border-bottom: 2px solid #E0E7FF;
            }
        """)
        
        parent_layout.addWidget(header_frame)
        
    def setup_template_section(self, parent_layout):
        """Configure la section de sélection de template"""
        template_group = QGroupBox("Template de Rapport")
        template_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        template_layout = QVBoxLayout(template_group)
        template_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Sélection du template
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "📊 Rapport Standard",
            "🔬 Rapport Technique",
            "📈 Rapport Exécutif",
            "🌊 Rapport Maritime",
            "📋 Rapport Personnalisé"
        ])
        self.template_combo.setFont(QFont("Inter", 12))
        self.template_combo.currentTextChanged.connect(self.on_template_changed)
        
        # Aperçu du template
        preview_frame = QFrame()
        preview_frame.setFixedHeight(120)
        preview_frame.setObjectName("template_preview")
        
        preview_layout = QVBoxLayout(preview_frame)
        self.template_preview_label = QLabel("📊 Template Standard\n\n• En-tête avec logo\n• Résumé exécutif\n• Données et graphiques\n• Conclusions")
        self.template_preview_label.setFont(QFont("Inter", 10))
        self.template_preview_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.template_preview_label.setWordWrap(True)
        self.template_preview_label.setStyleSheet("color: #445868; padding: 8px;")
        
        preview_layout.addWidget(self.template_preview_label)
        
        # Style du preview
        preview_frame.setStyleSheet("""
            QFrame#template_preview {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
            }
        """)
        
        # Style du combo
        self.template_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
                padding: 8px 13px;
                font-size: 12px;
            }
            
            QComboBox:hover {
                border-color: #00ACC1;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #445868;
                border-top: none;
                border-left: none;
                width: 6px;
                height: 6px;
                margin-right: 8px;
            }
        """)
        
        template_layout.addWidget(self.template_combo)
        template_layout.addWidget(preview_frame)
        
        parent_layout.addWidget(template_group)
        
    def setup_content_section(self, parent_layout):
        """Configure la section de contenu"""
        content_group = QGroupBox("Contenu du Rapport")
        content_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        content_layout = QVBoxLayout(content_group)
        content_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Sections à inclure
        sections_label = QLabel("Sections à inclure:")
        sections_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        sections_label.setStyleSheet("color: #0A1929;")
        
        # Checkboxes pour les sections
        self.section_checkboxes = {}
        sections = [
            ("summary", "📋 Résumé Exécutif"),
            ("data_overview", "📊 Aperçu des Données"),
            ("statistics", "📈 Analyses Statistiques"),
            ("graphs", "📉 Graphiques"),
            ("spectral", "🌊 Analyse Spectrale"),
            ("conclusions", "✅ Conclusions"),
            ("recommendations", "💡 Recommandations"),
            ("appendix", "📎 Annexes")
        ]
        
        for section_id, section_name in sections:
            checkbox = QCheckBox(section_name)
            checkbox.setFont(QFont("Inter", 11))
            checkbox.setChecked(True)  # Toutes cochées par défaut
            
            # Style des checkboxes
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #0A1929;
                    spacing: 8px;
                    padding: 3px;
                }
                
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 2px solid #E0E7FF;
                    border-radius: 3px;
                    background-color: white;
                }
                
                QCheckBox::indicator:checked {
                    background-color: #00ACC1;
                    border-color: #00ACC1;
                    image: none;
                }
                
                QCheckBox::indicator:checked:after {
                    content: "✓";
                    color: white;
                    font-weight: bold;
                }
                
                QCheckBox:hover {
                    color: #00ACC1;
                }
            """)
            
            self.section_checkboxes[section_id] = checkbox
            content_layout.addWidget(checkbox)
            
        content_layout.addWidget(sections_label)
        for checkbox in self.section_checkboxes.values():
            content_layout.addWidget(checkbox)
            
        parent_layout.addWidget(content_group)
        
    def setup_metadata_section(self, parent_layout):
        """Configure la section des métadonnées"""
        metadata_group = QGroupBox("Métadonnées")
        metadata_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        metadata_layout = QFormLayout(metadata_group)
        metadata_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Titre du rapport
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Titre du rapport...")
        self.title_edit.setText("Rapport d'Analyse Maritime")
        self.title_edit.setFont(QFont("Inter", 11))
        
        # Auteur
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Nom de l'auteur...")
        self.author_edit.setText("CHNeoWave System")
        self.author_edit.setFont(QFont("Inter", 11))
        
        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setFont(QFont("Inter", 11))
        self.date_edit.setCalendarPopup(True)
        
        # Version
        self.version_edit = QLineEdit()
        self.version_edit.setPlaceholderText("Version...")
        self.version_edit.setText("1.0")
        self.version_edit.setFont(QFont("Inter", 11))
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Description du rapport...")
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setFont(QFont("Inter", 11))
        self.description_edit.setPlainText("Analyse complète des données d'acquisition maritime.")
        
        # Style des champs
        field_style = """
            QLineEdit, QDateEdit, QTextEdit {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 5px;
                padding: 8px;
                font-size: 11px;
            }
            
            QLineEdit:focus, QDateEdit:focus, QTextEdit:focus {
                border-color: #00ACC1;
                outline: none;
            }
        """
        
        self.title_edit.setStyleSheet(field_style)
        self.author_edit.setStyleSheet(field_style)
        self.date_edit.setStyleSheet(field_style)
        self.version_edit.setStyleSheet(field_style)
        self.description_edit.setStyleSheet(field_style)
        
        # Labels avec style
        label_style = "color: #0A1929; font-weight: 500; font-size: 12px;"
        
        title_label = QLabel("Titre:")
        title_label.setStyleSheet(label_style)
        
        author_label = QLabel("Auteur:")
        author_label.setStyleSheet(label_style)
        
        date_label = QLabel("Date:")
        date_label.setStyleSheet(label_style)
        
        version_label = QLabel("Version:")
        version_label.setStyleSheet(label_style)
        
        description_label = QLabel("Description:")
        description_label.setStyleSheet(label_style)
        
        # Assemblage
        metadata_layout.addRow(title_label, self.title_edit)
        metadata_layout.addRow(author_label, self.author_edit)
        metadata_layout.addRow(date_label, self.date_edit)
        metadata_layout.addRow(version_label, self.version_edit)
        metadata_layout.addRow(description_label, self.description_edit)
        
        parent_layout.addWidget(metadata_group)
        
    def setup_export_section(self, parent_layout):
        """Configure la section d'export"""
        export_group = QGroupBox("Génération et Export")
        export_group.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        export_layout = QVBoxLayout(export_group)
        export_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Bouton de génération
        self.generate_button = QPushButton("🔄 Générer le Rapport")
        self.generate_button.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.generate_button.setFixedHeight(FIBONACCI_SPACING[4])  # 55px
        self.generate_button.clicked.connect(self.generate_report)
        
        # Boutons d'export
        export_buttons_layout = QGridLayout()
        export_buttons_layout.setSpacing(FIBONACCI_SPACING[0])
        
        export_buttons = [
            ("📄 PDF", "pdf", 0, 0),
            ("📊 HTML", "html", 0, 1),
            ("📝 Word", "docx", 1, 0),
            ("📋 Texte", "txt", 1, 1)
        ]
        
        for button_text, export_type, row, col in export_buttons:
            button = QPushButton(button_text)
            button.setFont(QFont("Inter", 10, QFont.Weight.Medium))
            button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
            button.clicked.connect(lambda checked, t=export_type: self.export_report(t))
            
            # Style des boutons d'export
            button.setStyleSheet("""
                QPushButton {
                    background-color: #055080;
                    color: #F5FBFF;
                    border: none;
                    border-radius: 17px;
                    padding: 5px 8px;
                    font-weight: 500;
                }
                
                QPushButton:hover {
                    background-color: #044A73;
                }
                
                QPushButton:pressed {
                    background-color: #033D66;
                }
            """)
            
            export_buttons_layout.addWidget(button, row, col)
            
        # Style du bouton principal
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #00ACC1;
                color: #F5FBFF;
                border: none;
                border-radius: 27px;
                padding: 13px 21px;
                font-weight: 700;
                font-size: 12px;
            }
            
            QPushButton:hover {
                background-color: #0097A7;
            }
            
            QPushButton:pressed {
                background-color: #00838F;
            }
        """)
        
        export_layout.addWidget(self.generate_button)
        export_layout.addLayout(export_buttons_layout)
        
        parent_layout.addWidget(export_group)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        pass  # Les connexions sont faites dans les méthodes setup
        
    def on_template_changed(self, template_name: str):
        """Gestionnaire de changement de template"""
        template_descriptions = {
            "📊 Rapport Standard": "📊 Template Standard\n\n• En-tête avec logo\n• Résumé exécutif\n• Données et graphiques\n• Conclusions",
            "🔬 Rapport Technique": "🔬 Template Technique\n\n• Spécifications détaillées\n• Analyses approfondies\n• Méthodologie\n• Résultats techniques",
            "📈 Rapport Exécutif": "📈 Template Exécutif\n\n• Résumé condensé\n• KPIs principaux\n• Recommandations\n• Plan d'action",
            "🌊 Rapport Maritime": "🌊 Template Maritime\n\n• Contexte maritime\n• Conditions de mer\n• Analyses spécialisées\n• Conformité réglementaire",
            "📋 Rapport Personnalisé": "📋 Template Personnalisé\n\n• Structure flexible\n• Sections modulaires\n• Contenu adaptatif\n• Format sur mesure"
        }
        
        description = template_descriptions.get(template_name, "Template non défini")
        self.template_preview_label.setText(description)
        
        self.template_selected.emit(template_name)
        
    def generate_report(self):
        """Génère le rapport avec la configuration actuelle"""
        config = self.get_report_config()
        self.report_generated.emit("standard", config)
        
    def export_report(self, export_type: str):
        """Exporte le rapport dans le format spécifié"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            f"Exporter en {export_type.upper()}",
            f"rapport.{export_type}",
            f"Fichiers {export_type.upper()} (*.{export_type})"
        )
        
        if filename:
            self.export_requested.emit(export_type, filename)
            
    def get_report_config(self) -> dict:
        """Retourne la configuration actuelle du rapport"""
        selected_sections = []
        for section_id, checkbox in self.section_checkboxes.items():
            if checkbox.isChecked():
                selected_sections.append(section_id)
                
        return {
            "template": self.template_combo.currentText(),
            "title": self.title_edit.text(),
            "author": self.author_edit.text(),
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "version": self.version_edit.text(),
            "description": self.description_edit.toPlainText(),
            "sections": selected_sections
        }


class ReportPreviewArea(QFrame):
    """
    Zone de prévisualisation du rapport
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface de prévisualisation"""
        self.setObjectName("report_preview_area")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[2], 
                                      FIBONACCI_SPACING[2], FIBONACCI_SPACING[2])
        main_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # En-tête
        self.setup_header(main_layout)
        
        # Zone de prévisualisation
        self.setup_preview_area(main_layout)
        
        # Barre d'outils
        self.setup_toolbar(main_layout)
        
        # Style de base
        self.setStyleSheet("""
            QFrame#report_preview_area {
                background-color: #F5FBFF;
            }
        """)
        
    def setup_header(self, parent_layout):
        """Configure l'en-tête de la prévisualisation"""
        header_frame = QFrame()
        header_frame.setFixedHeight(55)  # Fibonacci
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, FIBONACCI_SPACING[1], 0, FIBONACCI_SPACING[1])
        header_layout.setSpacing(FIBONACCI_SPACING[2])
        
        # Titre
        title_label = QLabel("Prévisualisation du Rapport")
        title_label.setFont(QFont("Inter", 21, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0A1929;")
        
        # Indicateurs de statut
        status_layout = QHBoxLayout()
        status_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Statut de génération
        self.generation_status_label = QLabel("📄 Prêt")
        self.generation_status_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.generation_status_label.setStyleSheet("""
            background-color: rgba(76, 175, 80, 0.1);
            color: #4CAF50;
            padding: 5px 10px;
            border-radius: 10px;
        """)
        
        # Nombre de pages
        self.page_count_label = QLabel("0 Pages")
        self.page_count_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.page_count_label.setStyleSheet("""
            background-color: rgba(43, 121, 182, 0.1);
            color: #2B79B6;
            padding: 5px 10px;
            border-radius: 10px;
        """)
        
        status_layout.addWidget(self.generation_status_label)
        status_layout.addWidget(self.page_count_label)
        
        # Assemblage
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addLayout(status_layout)
        
        parent_layout.addWidget(header_frame)
        
    def setup_preview_area(self, parent_layout):
        """Configure la zone de prévisualisation"""
        # Zone de défilement pour le contenu
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Widget de contenu
        self.content_widget = QWidget()
        self.content_widget.setObjectName("report_content")
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(FIBONACCI_SPACING[4], FIBONACCI_SPACING[4], 
                                         FIBONACCI_SPACING[4], FIBONACCI_SPACING[4])
        content_layout.setSpacing(FIBONACCI_SPACING[3])
        
        # Contenu par défaut
        self.setup_default_content(content_layout)
        
        # Style du contenu
        self.content_widget.setStyleSheet("""
            QWidget#report_content {
                background-color: white;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
                margin: 8px;
            }
        """)
        
        scroll_area.setWidget(self.content_widget)
        parent_layout.addWidget(scroll_area)
        
    def setup_default_content(self, parent_layout):
        """Configure le contenu par défaut du rapport"""
        # En-tête du rapport
        report_header = QFrame()
        report_header.setObjectName("report_header")
        report_header.setFixedHeight(120)
        
        header_layout = QVBoxLayout(report_header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Logo/Titre principal
        main_title = QLabel("🌊 CHNeoWave")
        main_title.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        main_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_title.setStyleSheet("color: #0A1929;")
        
        # Sous-titre
        subtitle = QLabel("Rapport d'Analyse Maritime")
        subtitle.setFont(QFont("Inter", 16))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #445868;")
        
        # Date
        date_label = QLabel(f"Généré le {QDate.currentDate().toString('dd/MM/yyyy')}")
        date_label.setFont(QFont("Inter", 12))
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_label.setStyleSheet("color: #445868;")
        
        header_layout.addWidget(main_title)
        header_layout.addWidget(subtitle)
        header_layout.addWidget(date_label)
        
        # Style de l'en-tête
        report_header.setStyleSheet("""
            QFrame#report_header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F5FBFF, stop:1 rgba(0, 172, 193, 0.1));
                border-radius: 8px;
                border-bottom: 2px solid #E0E7FF;
            }
        """)
        
        # Contenu du rapport
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Inter", 11))
        
        # Contenu d'exemple
        sample_content = """
<h2 style="color: #0A1929; font-family: Inter; font-weight: 600;">📋 Résumé Exécutif</h2>
<p style="font-family: Inter; line-height: 1.6; color: #445868;">
Ce rapport présente une analyse complète des données d'acquisition maritime collectées 
par le système CHNeoWave. L'analyse couvre une période de mesure de 60 minutes avec 
une fréquence d'échantillonnage de 1000 Hz sur 4 canaux de mesure.
</p>

<h2 style="color: #0A1929; font-family: Inter; font-weight: 600;">📊 Aperçu des Données</h2>
<p style="font-family: Inter; line-height: 1.6; color: #445868;">
<strong>Fichier analysé:</strong> acquisition_2025_01_15_10h30.csv<br>
<strong>Durée d'acquisition:</strong> 3600 secondes<br>
<strong>Fréquence d'échantillonnage:</strong> 1000 Hz<br>
<strong>Nombre de canaux:</strong> 4<br>
<strong>Nombre d'échantillons:</strong> 3,600,000
</p>

<h2 style="color: #0A1929; font-family: Inter; font-weight: 600;">📈 Résultats Statistiques</h2>
<table style="width: 100%; border-collapse: collapse; font-family: Inter;">
<tr style="background-color: #F5FBFF;">
    <th style="padding: 8px; border: 1px solid #E0E7FF; color: #0A1929;">Canal</th>
    <th style="padding: 8px; border: 1px solid #E0E7FF; color: #0A1929;">Moyenne</th>
    <th style="padding: 8px; border: 1px solid #E0E7FF; color: #0A1929;">Écart-type</th>
    <th style="padding: 8px; border: 1px solid #E0E7FF; color: #0A1929;">Min/Max</th>
</tr>
<tr>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">Canal 1 - Pression</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">1.234 bar</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">0.123 bar</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">0.890 / 1.678 bar</td>
</tr>
<tr style="background-color: #FAFBFF;">
    <td style="padding: 8px; border: 1px solid #E0E7FF;">Canal 2 - Température</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">20.5°C</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">0.8°C</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">19.2 / 22.1°C</td>
</tr>
<tr>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">Canal 3 - Débit</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">15.7 L/min</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">2.1 L/min</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">12.3 / 19.8 L/min</td>
</tr>
<tr style="background-color: #FAFBFF;">
    <td style="padding: 8px; border: 1px solid #E0E7FF;">Canal 4 - Niveau</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">2.45 m</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">0.15 m</td>
    <td style="padding: 8px; border: 1px solid #E0E7FF;">2.12 / 2.78 m</td>
</tr>
</table>

<h2 style="color: #0A1929; font-family: Inter; font-weight: 600;">🌊 Analyse Spectrale</h2>
<p style="font-family: Inter; line-height: 1.6; color: #445868;">
L'analyse spectrale révèle une fréquence dominante à 2.5 Hz avec des harmoniques 
significatives à 5.0 Hz et 7.5 Hz. Le rapport signal/bruit est excellent avec 
un niveau de bruit de fond à -40 dB.
</p>

<h2 style="color: #0A1929; font-family: Inter; font-weight: 600;">✅ Conclusions</h2>
<ul style="font-family: Inter; line-height: 1.6; color: #445868;">
<li>Les données présentent une excellente qualité avec un rapport signal/bruit optimal</li>
<li>Aucune anomalie ou dérive significative détectée sur la période d'acquisition</li>
<li>Les mesures sont conformes aux spécifications techniques du système</li>
<li>La stabilité thermique du système est satisfaisante</li>
</ul>

<h2 style="color: #0A1929; font-family: Inter; font-weight: 600;">💡 Recommandations</h2>
<ul style="font-family: Inter; line-height: 1.6; color: #445868;">
<li>Maintenir les paramètres d'acquisition actuels pour les prochaines mesures</li>
<li>Effectuer une calibration de contrôle dans 30 jours</li>
<li>Surveiller l'évolution de la fréquence dominante lors des prochaines acquisitions</li>
<li>Archiver les données selon la procédure qualité en vigueur</li>
</ul>
        """
        
        self.report_text.setHtml(sample_content)
        
        # Style du texte
        self.report_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                padding: 21px;
                line-height: 1.6;
            }
        """)
        
        parent_layout.addWidget(report_header)
        parent_layout.addWidget(self.report_text)
        
    def setup_toolbar(self, parent_layout):
        """Configure la barre d'outils"""
        toolbar_frame = QFrame()
        toolbar_frame.setFixedHeight(55)  # Fibonacci
        toolbar_frame.setObjectName("preview_toolbar")
        
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(FIBONACCI_SPACING[2], FIBONACCI_SPACING[1], 
                                         FIBONACCI_SPACING[2], FIBONACCI_SPACING[1])
        toolbar_layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Contrôles de zoom
        zoom_label = QLabel("Zoom:")
        zoom_label.setFont(QFont("Inter", 12))
        zoom_label.setStyleSheet("color: #0A1929;")
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(50, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(120)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        
        self.zoom_value_label = QLabel("100%")
        self.zoom_value_label.setFont(QFont("Inter", 11))
        self.zoom_value_label.setFixedWidth(40)
        self.zoom_value_label.setStyleSheet("color: #445868;")
        
        # Boutons d'action
        refresh_button = QPushButton("🔄 Actualiser")
        refresh_button.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        refresh_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        refresh_button.clicked.connect(self.refresh_preview)
        
        print_button = QPushButton("🖨️ Imprimer")
        print_button.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        print_button.setFixedHeight(FIBONACCI_SPACING[3])  # 34px
        print_button.clicked.connect(self.print_report)
        
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
        
        refresh_button.setStyleSheet(button_style)
        print_button.setStyleSheet(button_style)
        
        # Style du slider
        self.zoom_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #E0E7FF;
                height: 6px;
                background: #F5FBFF;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: #00ACC1;
                border: 2px solid #00ACC1;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -5px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background: #0097A7;
                border-color: #0097A7;
            }
            
            QSlider::sub-page:horizontal {
                background: #00ACC1;
                border-radius: 3px;
            }
        """)
        
        # Style de la toolbar
        toolbar_frame.setStyleSheet("""
            QFrame#preview_toolbar {
                background-color: #F5FBFF;
                border-top: 1px solid #E0E7FF;
            }
        """)
        
        # Assemblage
        toolbar_layout.addWidget(zoom_label)
        toolbar_layout.addWidget(self.zoom_slider)
        toolbar_layout.addWidget(self.zoom_value_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(refresh_button)
        toolbar_layout.addWidget(print_button)
        
        parent_layout.addWidget(toolbar_frame)
        
    def on_zoom_changed(self, value: int):
        """Gestionnaire de changement de zoom"""
        self.zoom_value_label.setText(f"{value}%")
        
        # Appliquer le zoom au contenu
        scale_factor = value / 100.0
        font = self.report_text.font()
        base_size = 11
        font.setPointSize(int(base_size * scale_factor))
        self.report_text.setFont(font)
        
    def refresh_preview(self):
        """Actualise la prévisualisation"""
        print("Actualisation de la prévisualisation...")
        # Logique de rafraîchissement
        
    def print_report(self):
        """Imprime le rapport"""
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.report_text.print(printer)
            
    def update_content(self, content: str):
        """Met à jour le contenu du rapport"""
        self.report_text.setHtml(content)
        
    def update_status(self, status: str, page_count: int = 0):
        """Met à jour le statut de génération"""
        self.generation_status_label.setText(status)
        self.page_count_label.setText(f"{page_count} Pages")


class ReportView(QWidget):
    """
    Vue principale de génération de rapports avec design maritime
    """
    
    # Signaux
    report_generated = Signal(str, dict)    # type de rapport, configuration
    report_exported = Signal(str, str)      # format, chemin
    template_changed = Signal(str)          # template sélectionné
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_dark_mode = False
        self.current_report_config = {}
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Configure l'interface principale"""
        self.setObjectName("report_view")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter horizontal (configuration + prévisualisation)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panneau de configuration
        self.config_panel = ReportConfigPanel()
        splitter.addWidget(self.config_panel)
        
        # Zone de prévisualisation
        self.preview_area = ReportPreviewArea()
        splitter.addWidget(self.preview_area)
        
        # Proportions du splitter (Golden Ratio)
        config_width = int(280 * GOLDEN_RATIO)  # ~453px
        preview_width = int(config_width * GOLDEN_RATIO)  # ~733px
        splitter.setSizes([config_width, preview_width])
        splitter.setCollapsible(0, False)  # Configuration non collapsible
        splitter.setCollapsible(1, False)  # Prévisualisation non collapsible
        
        main_layout.addWidget(splitter)
        
        # Style de base
        self.setStyleSheet("""
            QWidget#report_view {
                background-color: #F5FBFF;
            }
        """)
        
    def setup_connections(self):
        """Configure les connexions de signaux"""
        # Connexions du panneau de configuration
        self.config_panel.report_generated.connect(self.on_report_generated)
        self.config_panel.template_selected.connect(self.on_template_selected)
        self.config_panel.export_requested.connect(self.on_export_requested)
        
    def on_report_generated(self, report_type: str, config: dict):
        """Gestionnaire de génération de rapport"""
        print(f"Génération du rapport: {report_type} avec config: {config}")
        
        self.current_report_config = config
        
        # Mettre à jour le statut
        self.preview_area.update_status("🔄 Génération en cours...", 0)
        
        # Simuler la génération
        QTimer.singleShot(2000, lambda: self.complete_report_generation(config))
        
        # Émettre le signal
        self.report_generated.emit(report_type, config)
        
    def complete_report_generation(self, config: dict):
        """Complète la génération du rapport"""
        # Mettre à jour le statut
        self.preview_area.update_status("✅ Rapport généré", 3)
        
        # Mettre à jour le contenu si nécessaire
        # self.preview_area.update_content(generated_content)
        
    def on_template_selected(self, template: str):
        """Gestionnaire de sélection de template"""
        print(f"Template sélectionné: {template}")
        self.template_changed.emit(template)
        
    def on_export_requested(self, export_type: str, filename: str):
        """Gestionnaire de demande d'export"""
        print(f"Export demandé: {export_type} vers {filename}")
        
        # Simuler l'export
        self.preview_area.update_status(f"📤 Export {export_type.upper()}...", 3)
        
        QTimer.singleShot(1500, lambda: self.complete_export(export_type, filename))
        
        # Émettre le signal
        self.report_exported.emit(export_type, filename)
        
    def complete_export(self, export_type: str, filename: str):
        """Complète l'export du rapport"""
        self.preview_area.update_status("✅ Export terminé", 3)
        
        # Afficher un message de confirmation
        QMessageBox.information(
            self,
            "Export Terminé",
            f"Le rapport a été exporté avec succès:\n{filename}"
        )
        
    def set_theme(self, is_dark: bool):
        """Applique le thème sombre ou clair"""
        self.is_dark_mode = is_dark
        
        if is_dark:
            # Thème sombre
            self.setStyleSheet("""
                QWidget#report_view {
                    background-color: #0A1929;
                    color: #F5FBFF;
                }
            """)
        else:
            # Thème clair
            self.setStyleSheet("""
                QWidget#report_view {
                    background-color: #F5FBFF;
                    color: #0A1929;
                }
            """)
            
    def load_report_data(self, data_source: str):
        """Charge les données pour le rapport"""
        print(f"Chargement des données: {data_source}")
        # Logique de chargement des données
        
    def get_current_config(self) -> dict:
        """Retourne la configuration actuelle du rapport"""
        return self.current_report_config
        
    def set_report_config(self, config: dict):
        """Définit la configuration du rapport"""
        self.current_report_config = config
        # Mettre à jour l'interface si nécessaire
        
    def generate_custom_report(self, template: str, sections: list, metadata: dict):
        """Génère un rapport personnalisé"""
        config = {
            "template": template,
            "sections": sections,
            "metadata": metadata
        }
        
        self.on_report_generated("custom", config)