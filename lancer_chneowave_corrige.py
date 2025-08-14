#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur CHNeoWave - Version Corrigée et Fonctionnelle
Interface maritime pour laboratoires d'étude sur modèles réduits

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0-fixed
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QMessageBox, QSplashScreen
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QColor

class CHNeoWaveCorrige(QMainWindow):
    """CHNeoWave - Interface Maritime Corrigée et Fonctionnelle"""
    
    def __init__(self):
        super().__init__()
        print("🚀 Initialisation CHNeoWave Corrigé")
        
        # Configuration de base
        self.setWindowTitle("CHNeoWave - Laboratoire Maritime v1.1.0")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        # Initialiser l'interface
        self._init_interface()
        self._init_navigation()
        self._init_views()
        self._load_welcome()
        
        # Appliquer le thème maritime
        self._apply_maritime_theme()
        
        print("✅ CHNeoWave Corrigé initialisé avec succès")
        
    def _init_interface(self):
        """Initialiser l'interface principale"""
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header maritime
        self._create_header()
        
        # Zone de contenu
        self.content_area = QWidget()
        self.content_layout = QHBoxLayout(self.content_area)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar navigation
        self._create_sidebar()
        
        # Zone principale
        self.main_content = QStackedWidget()
        self.content_layout.addWidget(self.main_content, 1)
        
        self.main_layout.addWidget(self.content_area, 1)
        
    def _create_header(self):
        """Créer l'en-tête maritime"""
        header = QWidget()
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        
        # Logo et titre
        title_layout = QVBoxLayout()
        
        app_title = QLabel("CHNeoWave")
        app_title.setFont(QFont("Arial", 24, QFont.Bold))
        app_title.setStyleSheet("color: white; margin: 0;")
        title_layout.addWidget(app_title)
        
        subtitle = QLabel("Laboratoire Maritime - Modèles Réduits Méditerranée")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #b3d9ff; margin: 0;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Indicateurs de statut
        status_label = QLabel("🟢 Système Opérationnel")
        status_label.setFont(QFont("Arial", 12, QFont.Bold))
        status_label.setStyleSheet("color: #90EE90; padding: 10px;")
        header_layout.addWidget(status_label)
        
        self.main_layout.addWidget(header)
        
    def _create_sidebar(self):
        """Créer la barre latérale de navigation"""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(5)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        # Titre navigation
        nav_title = QLabel("Navigation")
        nav_title.setFont(QFont("Arial", 14, QFont.Bold))
        nav_title.setStyleSheet("color: #1e3a5f; margin-bottom: 15px;")
        sidebar_layout.addWidget(nav_title)
        
        # Boutons de navigation
        self.nav_buttons = {}
        nav_items = [
            ("welcome", "🏠 Accueil", "Page d'accueil et création de projets"),
            ("dashboard", "📊 Tableau de Bord", "Vue d'ensemble des données"),
            ("acquisition", "📡 Acquisition", "Collecte de données capteurs"),
            ("calibration", "⚙️ Calibration", "Calibration des instruments"),
            ("analysis", "📈 Analyse", "Analyse des résultats"),
            ("reports", "📋 Rapports", "Génération de rapports")
        ]
        
        for view_id, title, description in nav_items:
            btn = QPushButton(title)
            btn.setFont(QFont("Arial", 11))
            btn.setToolTip(description)
            btn.clicked.connect(lambda checked, v=view_id: self._navigate_to(v))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[view_id] = btn
        
        sidebar_layout.addStretch()
        
        # Informations système
        info_label = QLabel("CHNeoWave v1.1.0\nInterface Corrigée\n✅ Fonctionnelle")
        info_label.setFont(QFont("Arial", 9))
        info_label.setStyleSheet("color: #666; padding: 10px; border-top: 1px solid #ddd;")
        info_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(info_label)
        
        self.content_layout.addWidget(sidebar)
        
    def _init_navigation(self):
        """Initialiser le système de navigation"""
        self.views = {}
        self.current_view = None
        
    def _init_views(self):
        """Initialiser toutes les vues"""
        # Vue d'accueil
        self._create_welcome_view()
        
        # Tableau de bord
        self._create_dashboard_view()
        
        # Acquisition
        self._create_acquisition_view()
        
        # Calibration
        self._create_calibration_view()
        
        # Analyse
        self._create_analysis_view()
        
        # Rapports
        self._create_reports_view()
        
    def _create_welcome_view(self):
        """Vue d'accueil"""
        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Titre principal
        title = QLabel("Bienvenue dans CHNeoWave")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet("color: #1e3a5f; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("""
CHNeoWave est un logiciel avancé destiné aux laboratoires d'étude maritime 
sur modèles réduits en Méditerranée (bassins, canaux).

🌊 Acquisition de données en temps réel
⚙️ Calibration précise des instruments
📊 Analyse avancée des résultats
📋 Génération de rapports professionnels
        """)
        description.setAlignment(Qt.AlignCenter)
        description.setFont(QFont("Arial", 14))
        description.setStyleSheet("color: #333; line-height: 1.6;")
        layout.addWidget(description)
        
        # Boutons d'action
        actions_layout = QHBoxLayout()
        
        new_project_btn = QPushButton("🆕 Nouveau Projet")
        new_project_btn.setFont(QFont("Arial", 14, QFont.Bold))
        new_project_btn.clicked.connect(self._new_project)
        actions_layout.addWidget(new_project_btn)
        
        open_project_btn = QPushButton("📂 Ouvrir Projet")
        open_project_btn.setFont(QFont("Arial", 14))
        open_project_btn.clicked.connect(self._open_project)
        actions_layout.addWidget(open_project_btn)
        
        layout.addLayout(actions_layout)
        layout.addStretch()
        
        self.views['welcome'] = view
        self.main_content.addWidget(view)
        
    def _create_dashboard_view(self):
        """Tableau de bord"""
        view = QWidget()
        layout = QVBoxLayout(view)
        
        title = QLabel("📊 Tableau de Bord Maritime")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #1e3a5f; margin: 20px;")
        layout.addWidget(title)
        
        # KPIs simulés
        kpi_layout = QHBoxLayout()
        kpis = [
            ("Capteurs Actifs", "15/15", "#28a745"),
            ("Température Eau", "22.5°C", "#17a2b8"),
            ("Pression Atm.", "1013 hPa", "#ffc107"),
            ("Houle Moyenne", "0.8m", "#6f42c1")
        ]
        
        for name, value, color in kpis:
            kpi_widget = self._create_kpi_card(name, value, color)
            kpi_layout.addWidget(kpi_widget)
        
        layout.addLayout(kpi_layout)
        
        # Zone graphiques (simulée)
        graph_area = QLabel("📈 Zone Graphiques\n(Graphiques temps réel à implémenter)")
        graph_area.setAlignment(Qt.AlignCenter)
        graph_area.setFont(QFont("Arial", 16))
        graph_area.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px dashed #dee2e6;
                border-radius: 10px;
                padding: 50px;
                margin: 20px;
            }
        """)
        layout.addWidget(graph_area)
        
        self.views['dashboard'] = view
        self.main_content.addWidget(view)
        
    def _create_acquisition_view(self):
        """Vue acquisition"""
        view = QWidget()
        layout = QVBoxLayout(view)
        
        title = QLabel("📡 Acquisition de Données")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #1e3a5f; margin: 20px;")
        layout.addWidget(title)
        
        content = QLabel("Module d'acquisition des données capteurs\n(À implémenter)")
        content.setAlignment(Qt.AlignCenter)
        content.setFont(QFont("Arial", 16))
        layout.addWidget(content)
        
        self.views['acquisition'] = view
        self.main_content.addWidget(view)
        
    def _create_calibration_view(self):
        """Vue calibration"""
        view = QWidget()
        layout = QVBoxLayout(view)
        
        title = QLabel("⚙️ Calibration des Instruments")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #1e3a5f; margin: 20px;")
        layout.addWidget(title)
        
        content = QLabel("Module de calibration des capteurs\n(À implémenter)")
        content.setAlignment(Qt.AlignCenter)
        content.setFont(QFont("Arial", 16))
        layout.addWidget(content)
        
        self.views['calibration'] = view
        self.main_content.addWidget(view)
        
    def _create_analysis_view(self):
        """Vue analyse"""
        view = QWidget()
        layout = QVBoxLayout(view)
        
        title = QLabel("📈 Analyse des Résultats")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #1e3a5f; margin: 20px;")
        layout.addWidget(title)
        
        content = QLabel("Module d'analyse des données\n(À implémenter)")
        content.setAlignment(Qt.AlignCenter)
        content.setFont(QFont("Arial", 16))
        layout.addWidget(content)
        
        self.views['analysis'] = view
        self.main_content.addWidget(view)
        
    def _create_reports_view(self):
        """Vue rapports"""
        view = QWidget()
        layout = QVBoxLayout(view)
        
        title = QLabel("📋 Génération de Rapports")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #1e3a5f; margin: 20px;")
        layout.addWidget(title)
        
        content = QLabel("Module de génération de rapports\n(À implémenter)")
        content.setAlignment(Qt.AlignCenter)
        content.setFont(QFont("Arial", 16))
        layout.addWidget(content)
        
        self.views['reports'] = view
        self.main_content.addWidget(view)
        
    def _create_kpi_card(self, name, value, color):
        """Créer une carte KPI"""
        card = QWidget()
        card.setFixedSize(200, 120)
        layout = QVBoxLayout(card)
        
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(name_label)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Arial", 18, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
                margin: 10px;
            }}
        """)
        
        return card
        
    def _load_welcome(self):
        """Charger la vue d'accueil"""
        self._navigate_to('welcome')
        
    def _navigate_to(self, view_name):
        """Naviguer vers une vue"""
        if view_name in self.views:
            self.main_content.setCurrentWidget(self.views[view_name])
            self.current_view = view_name
            
            # Mettre à jour les boutons
            for btn_name, btn in self.nav_buttons.items():
                if btn_name == view_name:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #1e3a5f;
                            color: white;
                            padding: 12px;
                            border-radius: 6px;
                            font-weight: bold;
                        }
                    """)
                else:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            color: #1e3a5f;
                            padding: 12px;
                            border-radius: 6px;
                            text-align: left;
                        }
                        QPushButton:hover {
                            background-color: #e3f2fd;
                        }
                    """)
            
            print(f"✅ Navigation vers {view_name}")
        else:
            print(f"❌ Vue {view_name} non trouvée")
            
    def _apply_maritime_theme(self):
        """Appliquer le thème maritime"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f8ff;
            }
            QWidget {
                background-color: #f0f8ff;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2c5aa0;
            }
        """)
        
        # Thème header
        header = self.main_layout.itemAt(0).widget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #2c5aa0);
                border-bottom: 3px solid #0d47a1;
            }
        """)
        
    def _new_project(self):
        """Créer un nouveau projet"""
        QMessageBox.information(self, "Nouveau Projet", 
                               "Fonctionnalité de création de projet\n(À implémenter)")
        self._navigate_to('dashboard')
        
    def _open_project(self):
        """Ouvrir un projet existant"""
        QMessageBox.information(self, "Ouvrir Projet", 
                               "Fonctionnalité d'ouverture de projet\n(À implémenter)")

def create_splash_screen():
    """Créer un écran de démarrage"""
    splash_pixmap = QPixmap(400, 300)
    splash_pixmap.fill(QColor(30, 58, 95))
    
    painter = QPainter(splash_pixmap)
    painter.setPen(QColor(255, 255, 255))
    painter.setFont(QFont("Arial", 24, QFont.Bold))
    painter.drawText(splash_pixmap.rect(), Qt.AlignCenter, "CHNeoWave\nChargement...")
    painter.end()
    
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    return splash

def main():
    """Lancer CHNeoWave Corrigé"""
    print("🚀 CHNeoWave - Version Corrigée et Fonctionnelle")
    print("=" * 60)
    
    try:
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Corrigé")
            app.setApplicationVersion("1.1.0-fixed")
            app.setOrganizationName("Laboratoire Maritime")
        
        print("✅ QApplication créée")
        
        # Écran de démarrage
        splash = create_splash_screen()
        
        # Créer l'interface principale
        window = CHNeoWaveCorrige()
        print("✅ Interface CHNeoWave créée")
        
        # Fermer le splash et afficher l'interface
        splash.finish(window)
        
        # Afficher la fenêtre
        window.show()
        window.raise_()
        window.activateWindow()
        
        print(f"✅ Interface affichée")
        print(f"✅ Visible: {window.isVisible()}")
        print(f"✅ Géométrie: {window.geometry()}")
        print("🎉 CHNeoWave Corrigé est opérationnel !")
        print("🌊 Interface maritime fonctionnelle")
        print("👀 L'interface devrait maintenant être visible")
        
        # Lancer la boucle d'événements
        exit_code = app.exec()
        print(f"✅ Application terminée (code: {exit_code})")
        return exit_code
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())