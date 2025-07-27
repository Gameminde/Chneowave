#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de validation de la nouvelle interface Maritime Theme 2025
CHNeoWave - Laboratoires d'étude maritime
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QFont, QFontDatabase
except ImportError:
    print("❌ PySide6 non disponible. Installation requise: pip install PySide6")
    sys.exit(1)

try:
    from hrneowave.gui.views import DashboardView, CalibrationView, AcquisitionView, AnalysisView, ReportView
    from hrneowave.gui.widgets import MainSidebar, ThemeToggle, KPICard
except ImportError as e:
    print(f"❌ Erreur d'import des modules CHNeoWave: {e}")
    sys.exit(1)

class MaritimeTestWindow(QMainWindow):
    """
    Fenêtre de test pour valider l'interface Maritime Theme 2025
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHNeoWave - Test Interface Maritime 2025")
        self.setGeometry(100, 100, 1400, 900)
        
        # Configuration de la police Inter
        self.setup_fonts()
        
        # Application du thème maritime
        self.apply_maritime_theme()
        
        # Configuration de l'interface
        self.setup_ui()
        
        # Test des composants
        self.test_components()
        
    def setup_fonts(self):
        """Configuration de la police Inter"""
        font_db = QFontDatabase()
        
        # Tentative de chargement de la police Inter
        inter_font = QFont("Inter", 13)
        if not inter_font.exactMatch():
            # Fallback vers des polices système
            inter_font = QFont("Segoe UI", 13)  # Windows
            if not inter_font.exactMatch():
                inter_font = QFont("Arial", 13)  # Fallback universel
        
        self.setFont(inter_font)
        QApplication.instance().setFont(inter_font)
        
    def apply_maritime_theme(self):
        """Application du thème maritime"""
        # Chargement du fichier QSS
        qss_path = Path(__file__).parent / "src" / "hrneowave" / "gui" / "styles" / "maritime_theme.qss"
        
        if qss_path.exists():
            try:
                with open(qss_path, 'r', encoding='utf-8') as f:
                    qss_content = f.read()
                self.setStyleSheet(qss_content)
                print("✅ Thème maritime appliqué avec succès")
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement du thème: {e}")
                self.apply_fallback_theme()
        else:
            print("⚠️ Fichier maritime_theme.qss non trouvé, application du thème de base")
            self.apply_fallback_theme()
    
    def apply_fallback_theme(self):
        """Thème de base si le fichier QSS n'est pas disponible"""
        fallback_qss = """
        QMainWindow {
            background-color: #F5FBFF;
            color: #0A1929;
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        }
        
        QWidget {
            background-color: #F5FBFF;
            color: #0A1929;
        }
        
        QPushButton {
            background-color: #055080;
            color: white;
            border: none;
            padding: 8px 21px;
            border-radius: 8px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #2B79B6;
        }
        """
        self.setStyleSheet(fallback_qss)
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar de navigation
        try:
            self.sidebar = MainSidebar()
            main_layout.addWidget(self.sidebar)
            print("✅ Sidebar créée avec succès")
        except Exception as e:
            print(f"❌ Erreur création sidebar: {e}")
            return
        
        # Zone de contenu principal
        content_layout = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget, 1)
        
        # Test des vues
        self.test_views(content_layout)
        
    def test_views(self, layout):
        """Test de création des vues"""
        views_to_test = [
            ("Dashboard", DashboardView),
            ("Calibration", CalibrationView),
            ("Acquisition", AcquisitionView),
            ("Analysis", AnalysisView),
            ("Report", ReportView)
        ]
        
        for view_name, view_class in views_to_test:
            try:
                view = view_class()
                print(f"✅ {view_name}View créée avec succès")
                
                # Test d'ajout temporaire pour validation
                layout.addWidget(view)
                
                # Timer pour retirer la vue après test
                QTimer.singleShot(1000, lambda v=view: self.remove_test_view(v))
                
            except Exception as e:
                print(f"❌ Erreur création {view_name}View: {e}")
    
    def remove_test_view(self, view):
        """Retire une vue de test"""
        try:
            view.setParent(None)
        except:
            pass
    
    def test_components(self):
        """Test des composants individuels"""
        # Test KPICard
        try:
            kpi_card = KPICard("Test KPI", "42", "unité")
            print("✅ KPICard créée avec succès")
        except Exception as e:
            print(f"❌ Erreur création KPICard: {e}")
        
        # Test ThemeToggle
        try:
            theme_toggle = ThemeToggle()
            print("✅ ThemeToggle créé avec succès")
        except Exception as e:
            print(f"❌ Erreur création ThemeToggle: {e}")

def main():
    """Fonction principale de test"""
    print("🌊 CHNeoWave - Test Interface Maritime 2025")
    print("=" * 50)
    
    # Création de l'application Qt
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave Maritime Test")
    app.setApplicationVersion("1.0.0")
    
    # Création et affichage de la fenêtre de test
    try:
        window = MaritimeTestWindow()
        window.show()
        
        print("\n🎯 Interface de test lancée avec succès!")
        print("📋 Vérifications à effectuer:")
        print("   • Design maritime avec palette de couleurs")
        print("   • Typographie Inter (ou fallback)")
        print("   • Espacements Golden Ratio")
        print("   • Navigation latérale fonctionnelle")
        print("   • Transitions et animations fluides")
        print("   • Thème clair/sombre")
        print("\n🔍 Fermez la fenêtre pour terminer le test.")
        
        # Lancement de la boucle d'événements
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur fatale lors du lancement: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()