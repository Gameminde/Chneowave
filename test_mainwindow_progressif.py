#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MainWindow CHNeoWave PROGRESSIF
Ajouter les composants un par un pour identifier le problème
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
    QPushButton, QHBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class TestProgressifWindow(QMainWindow):
    """Test progressif des composants CHNeoWave"""
    
    def __init__(self):
        super().__init__()
        print("🔍 Début construction TestProgressifWindow")
        
        # Configuration de base
        self.setWindowTitle("CHNeoWave - Test Progressif")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("CHNeoWave - Test Progressif des Composants")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(title)
        
        # Zone de logs
        self.log_area = QTextEdit()
        self.log_area.setMaximumHeight(200)
        self.log_area.setFont(QFont("Courier", 10))
        main_layout.addWidget(self.log_area)
        
        # Boutons de test
        buttons_layout = QHBoxLayout()
        
        self.btn_test1 = QPushButton("Test 1: Import ViewManager")
        self.btn_test1.clicked.connect(self.test_import_viewmanager)
        buttons_layout.addWidget(self.btn_test1)
        
        self.btn_test2 = QPushButton("Test 2: Import WelcomeView")
        self.btn_test2.clicked.connect(self.test_import_welcomeview)
        buttons_layout.addWidget(self.btn_test2)
        
        self.btn_test3 = QPushButton("Test 3: Créer ViewManager")
        self.btn_test3.clicked.connect(self.test_create_viewmanager)
        buttons_layout.addWidget(self.btn_test3)
        
        self.btn_test4 = QPushButton("Test 4: Créer WelcomeView")
        self.btn_test4.clicked.connect(self.test_create_welcomeview)
        buttons_layout.addWidget(self.btn_test4)
        
        main_layout.addLayout(buttons_layout)
        
        # Boutons de test avancés
        buttons_layout2 = QHBoxLayout()
        
        self.btn_test5 = QPushButton("Test 5: Import ThemeManager")
        self.btn_test5.clicked.connect(self.test_import_thememanager)
        buttons_layout2.addWidget(self.btn_test5)
        
        self.btn_test6 = QPushButton("Test 6: Appliquer Thème")
        self.btn_test6.clicked.connect(self.test_apply_theme)
        buttons_layout2.addWidget(self.btn_test6)
        
        self.btn_test7 = QPushButton("Test 7: MainWindow Complète")
        self.btn_test7.clicked.connect(self.test_mainwindow_complete)
        buttons_layout2.addWidget(self.btn_test7)
        
        main_layout.addLayout(buttons_layout2)
        
        # Zone de contenu pour les tests
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        main_layout.addWidget(self.content_area)
        
        self.log("✅ TestProgressifWindow initialisée")
        print("✅ TestProgressifWindow construite")
        
    def log(self, message):
        """Ajouter un message au log"""
        self.log_area.append(message)
        print(message)
        
    def test_import_viewmanager(self):
        """Test 1: Import ViewManager"""
        try:
            from hrneowave.gui.view_manager import ViewManager
            self.log("✅ Test 1: ViewManager importé avec succès")
        except Exception as e:
            self.log(f"❌ Test 1: Erreur import ViewManager: {e}")
            
    def test_import_welcomeview(self):
        """Test 2: Import WelcomeView"""
        try:
            from hrneowave.gui.views.welcome_view import WelcomeView
            self.log("✅ Test 2: WelcomeView importé avec succès")
        except Exception as e:
            self.log(f"❌ Test 2: Erreur import WelcomeView: {e}")
            
    def test_create_viewmanager(self):
        """Test 3: Créer ViewManager"""
        try:
            from hrneowave.gui.view_manager import ViewManager
            self.view_manager = ViewManager(parent=self)
            self.log("✅ Test 3: ViewManager créé avec succès")
        except Exception as e:
            self.log(f"❌ Test 3: Erreur création ViewManager: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            
    def test_create_welcomeview(self):
        """Test 4: Créer WelcomeView"""
        try:
            from hrneowave.gui.views.welcome_view import WelcomeView
            welcome_view = WelcomeView(parent=self)
            self.content_layout.addWidget(welcome_view)
            self.log("✅ Test 4: WelcomeView créée et ajoutée")
        except Exception as e:
            self.log(f"❌ Test 4: Erreur création WelcomeView: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            
    def test_import_thememanager(self):
        """Test 5: Import ThemeManager"""
        try:
            from hrneowave.gui.styles.theme_manager import ThemeManager
            self.log("✅ Test 5: ThemeManager importé avec succès")
        except Exception as e:
            self.log(f"❌ Test 5: Erreur import ThemeManager: {e}")
            
    def test_apply_theme(self):
        """Test 6: Appliquer thème"""
        try:
            from hrneowave.gui.styles.theme_manager import ThemeManager
            app = QApplication.instance()
            theme_manager = ThemeManager(app=app)
            theme_manager.apply_theme('maritime_modern')
            self.log("✅ Test 6: Thème maritime appliqué avec succès")
        except Exception as e:
            self.log(f"❌ Test 6: Erreur application thème: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            
    def test_mainwindow_complete(self):
        """Test 7: MainWindow complète"""
        try:
            from hrneowave.gui.main_window import MainWindow
            self.main_window_complete = MainWindow()
            self.main_window_complete.show()
            self.log("✅ Test 7: MainWindow complète créée et affichée")
            self.log(f"Visible: {self.main_window_complete.isVisible()}")
        except Exception as e:
            self.log(f"❌ Test 7: Erreur MainWindow complète: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")

def main():
    """Test principal"""
    print("🚀 Test Progressif CHNeoWave")
    print("=" * 50)
    
    try:
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Test Progressif")
        
        print("✅ QApplication créée")
        
        # Créer fenêtre de test
        window = TestProgressifWindow()
        print("✅ TestProgressifWindow créée")
        
        # Afficher la fenêtre
        window.show()
        window.raise_()
        window.activateWindow()
        
        print(f"✅ Fenêtre affichée")
        print(f"✅ Visible: {window.isVisible()}")
        print("👀 Cliquez sur les boutons pour tester chaque composant")
        
        # Pas de timer automatique pour permettre les tests manuels
        print("🔄 Application lancée (fermez manuellement)")
        
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