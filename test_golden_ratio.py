#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Golden Ratio Interface - CHNeoWave
Démonstration de l'application du Nombre d'Or dans l'interface
Phase 4: Validation des proportions φ et espacements Fibonacci
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit,
    QGroupBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QProgressBar, QSlider, QComboBox, QListWidget, QFrame,
    QSplitter, QDockWidget, QMenuBar, QMenu, QToolBar, QToolButton
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor

# Ajouter le chemin vers les modules CHNeoWave
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from hrneowave.gui.layouts.phi_layout import (
        PhiConstants, PhiGridLayout, PhiVBoxLayout, PhiHBoxLayout,
        PhiWidget, DashboardPhiLayout
    )
except ImportError:
    print("Modules phi_layout non trouvés, utilisation des layouts standards")
    PhiGridLayout = QGridLayout
    PhiVBoxLayout = QVBoxLayout
    PhiHBoxLayout = QHBoxLayout
    PhiWidget = QWidget
    DashboardPhiLayout = QGridLayout
    
    class PhiConstants:
        PHI = 1.618
        FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
        
        @classmethod
        def get_fibonacci_spacing(cls, index):
            return cls.FIBONACCI[min(index, len(cls.FIBONACCI)-1)]


class GoldenRatioTestWindow(QMainWindow):
    """Fenêtre de test pour les proportions Golden Ratio"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHNeoWave - Test Golden Ratio Interface")
        self.setGeometry(100, 100, 1200, 800)
        
        # Charger les styles
        self.load_styles()
        
        # Créer l'interface
        self.setup_ui()
        
        # Démarrer les animations de test
        self.setup_test_animations()
    
    def load_styles(self):
        """Charge les feuilles de style Golden Ratio"""
        styles_dir = Path(__file__).parent / "src" / "hrneowave" / "gui" / "styles"
        
        style_files = [
            "maritime_palette.qss",
            "golden_ratio.qss",
            "maritime_modern.qss"
        ]
        
        combined_style = ""
        
        for style_file in style_files:
            style_path = styles_dir / style_file
            if style_path.exists():
                with open(style_path, 'r', encoding='utf-8') as f:
                    combined_style += f.read() + "\n"
                print(f"✓ Style chargé: {style_file}")
            else:
                print(f"⚠ Style non trouvé: {style_file}")
        
        if combined_style:
            self.setStyleSheet(combined_style)
            print("✓ Styles Golden Ratio appliqués")
        else:
            print("⚠ Aucun style chargé")
    
    def setup_ui(self):
        """Configure l'interface utilisateur avec proportions φ"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal avec proportions φ (1:1.618)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(PhiConstants.get_fibonacci_spacing(7))  # 21px
        main_layout.setContentsMargins(34, 34, 34, 34)  # F9
        
        # Sidebar (38.2% - φ⁻¹)
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 382)  # φ⁻¹ * 1000
        
        # Zone principale (61.8% - φ)
        main_content = self.create_main_content()
        main_layout.addWidget(main_content, 618)  # φ⁻¹ * 1000
        
        # Menu et barre d'outils
        self.setup_menu_toolbar()
    
    def create_sidebar(self):
        """Crée la sidebar avec proportions φ"""
        sidebar = QFrame()
        sidebar.setProperty("class", "sidebar")
        sidebar.setMinimumWidth(233)  # F13
        sidebar.setMaximumWidth(377)  # F14
        
        layout = PhiVBoxLayout(sidebar)
        
        # Titre de la sidebar
        title = QLabel("Navigation")
        title.setProperty("class", "h2")
        layout.addWidget(title)
        
        # Boutons de navigation avec proportions φ
        nav_buttons = [
            "Dashboard", "Analyse FFT", "Calibration", 
            "Paramètres", "Aide", "À propos"
        ]
        
        for btn_text in nav_buttons:
            btn = QPushButton(btn_text)
            btn.setProperty("class", "phi-button")
            layout.addWidget(btn)
        
        # Spacer flexible
        layout.addStretch()
        
        # Informations système
        info_group = QGroupBox("Système")
        info_layout = QVBoxLayout(info_group)
        
        status_label = QLabel("Status: Connecté")
        status_label.setProperty("class", "caption")
        info_layout.addWidget(status_label)
        
        memory_label = QLabel("Mémoire: 45.2%")
        memory_label.setProperty("class", "caption")
        info_layout.addWidget(memory_label)
        
        layout.addWidget(info_group)
        
        return sidebar
    
    def create_main_content(self):
        """Crée la zone principale avec dashboard φ"""
        main_widget = QWidget()
        main_widget.setProperty("class", "main-content")
        
        layout = PhiVBoxLayout(main_widget)
        
        # Titre principal
        title = QLabel("Dashboard Maritime - Proportions Golden Ratio")
        title.setProperty("class", "h1")
        layout.addWidget(title)
        
        # Tabs avec contenu φ
        tabs = QTabWidget()
        
        # Tab 1: Dashboard KPI
        dashboard_tab = self.create_dashboard_tab()
        tabs.addTab(dashboard_tab, "Dashboard")
        
        # Tab 2: Formulaires φ
        forms_tab = self.create_forms_tab()
        tabs.addTab(forms_tab, "Formulaires")
        
        # Tab 3: Tableaux φ
        tables_tab = self.create_tables_tab()
        tabs.addTab(tables_tab, "Données")
        
        layout.addWidget(tabs)
        
        return main_widget
    
    def create_dashboard_tab(self):
        """Crée l'onglet dashboard avec cartes φ"""
        widget = QWidget()
        layout = DashboardPhiLayout(widget)
        
        # Cartes KPI avec proportions φ
        kpi_data = [
            ("Température", "23.5°C", "#00ACC1"),
            ("Pression", "1013 hPa", "#0478b9"),
            ("Humidité", "65%", "#00558c"),
            ("Vent", "12 km/h", "#37474F")
        ]
        
        for i, (title, value, color) in enumerate(kpi_data):
            card = self.create_kpi_card(title, value, color)
            row = i // 2
            col = i % 2
            layout.addWidget(card, row, col)
        
        # Graphique principal (ratio φ)
        chart_card = self.create_chart_card()
        layout.addWidget(chart_card, 2, 0, 1, 2)  # Span 2 colonnes
        
        return widget
    
    def create_kpi_card(self, title, value, color):
        """Crée une carte KPI avec proportions φ"""
        card = QFrame()
        card.setProperty("class", "kpi-card")
        
        layout = QVBoxLayout(card)
        layout.setSpacing(PhiConstants.get_fibonacci_spacing(5))  # 8px
        
        # Titre
        title_label = QLabel(title)
        title_label.setProperty("class", "caption")
        layout.addWidget(title_label)
        
        # Valeur
        value_label = QLabel(value)
        value_label.setProperty("class", "h2")
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # Barre de progression
        progress = QProgressBar()
        progress.setValue(75)
        layout.addWidget(progress)
        
        return card
    
    def create_chart_card(self):
        """Crée une carte graphique avec proportions φ"""
        card = QFrame()
        card.setProperty("class", "card-phi")
        
        layout = QVBoxLayout(card)
        
        # Titre
        title = QLabel("Analyse Spectrale FFT")
        title.setProperty("class", "h2")
        layout.addWidget(title)
        
        # Zone graphique simulée
        chart_area = QFrame()
        chart_area.setMinimumHeight(233)  # F13
        chart_area.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 #E1F5FE, stop:1 #d3edf9); "
            "border: 1px solid #0478b9; "
            "border-radius: 8px;"
        )
        
        chart_layout = QVBoxLayout(chart_area)
        chart_label = QLabel("Graphique FFT - Zone φ")
        chart_label.setAlignment(Qt.AlignCenter)
        chart_label.setProperty("class", "body")
        chart_layout.addWidget(chart_label)
        
        layout.addWidget(chart_area)
        
        return card
    
    def create_forms_tab(self):
        """Crée l'onglet formulaires avec espacements φ"""
        widget = QWidget()
        layout = PhiVBoxLayout(widget)
        
        # Groupe de formulaire
        form_group = QGroupBox("Configuration Maritime")
        form_layout = PhiGridLayout(form_group)
        
        # Champs avec proportions φ
        fields = [
            ("Nom du projet:", QLineEdit()),
            ("Localisation:", QComboBox()),
            ("Profondeur (m):", QLineEdit()),
            ("Température (°C):", QLineEdit())
        ]
        
        for i, (label_text, widget_input) in enumerate(fields):
            label = QLabel(label_text)
            label.setProperty("class", "body")
            
            if isinstance(widget_input, QComboBox):
                widget_input.addItems(["Méditerranée", "Atlantique", "Bassin test"])
            
            widget_input.setProperty("class", "phi-input")
            
            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(widget_input, i, 1)
        
        layout.addWidget(form_group)
        
        # Zone de texte avec proportions φ
        text_group = QGroupBox("Notes")
        text_layout = QVBoxLayout(text_group)
        
        text_edit = QTextEdit()
        text_edit.setProperty("class", "phi-input")
        text_edit.setPlainText(
            "Zone de texte avec proportions Golden Ratio.\n"
            "Hauteur/Largeur ≈ 1:φ (1:1.618)\n"
            "Espacements basés sur la suite de Fibonacci."
        )
        text_layout.addWidget(text_edit)
        
        layout.addWidget(text_group)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(PhiConstants.get_fibonacci_spacing(6))  # 13px
        
        save_btn = QPushButton("Sauvegarder")
        save_btn.setProperty("class", "phi-button")
        buttons_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setProperty("class", "phi-button")
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        return widget
    
    def create_tables_tab(self):
        """Crée l'onglet tableaux avec espacements φ"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(PhiConstants.get_fibonacci_spacing(7))  # 21px
        
        # Titre
        title = QLabel("Données Expérimentales")
        title.setProperty("class", "h2")
        layout.addWidget(title)
        
        # Tableau avec proportions φ
        table = QTableWidget(8, 5)  # F6 x F5
        table.setProperty("class", "phi-table")
        
        headers = ["Temps (s)", "Amplitude (m)", "Fréquence (Hz)", "Phase (°)", "Énergie (J)"]
        table.setHorizontalHeaderLabels(headers)
        
        # Données de test
        for row in range(8):
            for col in range(5):
                value = f"{(row + 1) * (col + 1) * 1.618:.2f}"
                item = QTableWidgetItem(value)
                table.setItem(row, col, item)
        
        layout.addWidget(table)
        
        # Contrôles avec espacements φ
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(PhiConstants.get_fibonacci_spacing(6))  # 13px
        
        # Slider avec proportions φ
        slider_label = QLabel("Échelle:")
        slider_label.setProperty("class", "body")
        controls_layout.addWidget(slider_label)
        
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(100)
        slider.setValue(62)  # ≈ φ * 38.2
        controls_layout.addWidget(slider)
        
        # Liste avec proportions φ
        list_widget = QListWidget()
        list_widget.setMaximumWidth(144)  # F12
        list_items = ["Mesure 1", "Mesure 2", "Mesure 3", "Mesure 5", "Mesure 8"]
        for item_text in list_items:
            list_widget.addItem(item_text)
        
        controls_layout.addWidget(list_widget)
        layout.addLayout(controls_layout)
        
        return widget
    
    def setup_menu_toolbar(self):
        """Configure le menu et la barre d'outils"""
        # Menu bar
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        file_menu.addAction("Nouveau projet")
        file_menu.addAction("Ouvrir")
        file_menu.addAction("Sauvegarder")
        file_menu.addSeparator()
        file_menu.addAction("Quitter")
        
        # Menu Analyse
        analysis_menu = menubar.addMenu("Analyse")
        analysis_menu.addAction("FFT")
        analysis_menu.addAction("Calibration")
        analysis_menu.addAction("Export")
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        help_menu.addAction("Documentation")
        help_menu.addAction("À propos")
        
        # Barre d'outils
        toolbar = self.addToolBar("Principal")
        toolbar.addAction("Nouveau")
        toolbar.addAction("Ouvrir")
        toolbar.addAction("Sauvegarder")
        toolbar.addSeparator()
        toolbar.addAction("Analyser")
        toolbar.addAction("Calibrer")
    
    def setup_test_animations(self):
        """Configure les animations de test"""
        # Timer pour animer les valeurs
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_test_values)
        self.timer.start(2000)  # Toutes les 2 secondes
        
        print("✓ Interface Golden Ratio initialisée")
        print(f"✓ Proportions φ = {PhiConstants.PHI:.3f}")
        print(f"✓ Espacements Fibonacci: {PhiConstants.FIBONACCI[:8]}")
    
    def update_test_values(self):
        """Met à jour les valeurs de test"""
        # Animation des barres de progression
        for progress in self.findChildren(QProgressBar):
            current = progress.value()
            new_value = (current + 5) % 100
            progress.setValue(new_value)


def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("CHNeoWave Golden Ratio Test")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Laboratoire Maritime")
    
    # Police par défaut
    font = QFont("Inter", 13)  # F7 - Body text
    app.setFont(font)
    
    # Fenêtre principale
    window = GoldenRatioTestWindow()
    window.show()
    
    print("\n" + "="*60)
    print("CHNeoWave - Test Golden Ratio Interface")
    print("Phase 4: Application du Nombre d'Or")
    print("="*60)
    print("\n📐 PROPORTIONS TESTÉES:")
    print(f"   • Sidebar : Zone principale = 1 : {PhiConstants.PHI:.3f}")
    print(f"   • Cartes : Hauteur/Largeur ≈ 1 : {PhiConstants.PHI:.3f}")
    print("\n📏 ESPACEMENTS FIBONACCI:")
    print(f"   • Micro (8px), Petit (13px), Moyen (21px)")
    print(f"   • Large (34px), XL (55px)")
    print("\n🔤 HIÉRARCHIE TYPOGRAPHIQUE:")
    print(f"   • H1: 34px, H2: 21px, Body: 13px, Caption: 8px")
    print("\n✨ Interface prête pour validation!")
    print("="*60)
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())