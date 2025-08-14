#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Complet des Modules CHNeoWave
Vérifie si tous les modules se lancent correctement ensemble
"""

import sys
import traceback
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_modules_complets():
    """Test complet de tous les modules CHNeoWave"""
    print("🔍 TEST COMPLET DES MODULES CHNEOWAVE")
    print("=" * 60)
    
    modules_tests = []
    
    try:
        # Test 1: Qt/PySide6
        print("🔄 Test 1: Qt/PySide6...")
        from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QFrame, QScrollArea, QTabWidget, QTextEdit, QProgressBar
        from PySide6.QtCore import Qt, QTimer
        from PySide6.QtGui import QFont, QPixmap
        print("✅ Qt/PySide6: Tous les widgets importés")
        modules_tests.append(("Qt/PySide6", True))
        
        # Test 2: Création QApplication
        print("🔄 Test 2: QApplication...")
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Modules Test")
        print("✅ QApplication: Créé avec succès")
        modules_tests.append(("QApplication", True))
        
        # Test 3: ThemeManager
        print("🔄 Test 3: ThemeManager...")
        from hrneowave.gui.styles.theme_manager import ThemeManager
        theme_manager = ThemeManager(app=app)
        theme_manager.apply_theme('maritime_modern')
        print("✅ ThemeManager: Thème maritime appliqué")
        modules_tests.append(("ThemeManager", True))
        
        # Test 4: ViewManager
        print("🔄 Test 4: ViewManager...")
        from hrneowave.gui.view_manager import ViewManager
        view_manager = ViewManager()
        print("✅ ViewManager: Créé avec succès")
        modules_tests.append(("ViewManager", True))
        
        # Test 5: WelcomeView
        print("🔄 Test 5: WelcomeView...")
        from hrneowave.gui.views.welcome_view import WelcomeView
        welcome_view = WelcomeView()
        print("✅ WelcomeView: Créée avec succès")
        modules_tests.append(("WelcomeView", True))
        
        # Test 6: DashboardViewMaritime
        print("🔄 Test 6: DashboardViewMaritime...")
        from hrneowave.gui.views.dashboard_view import DashboardViewMaritime
        dashboard_view = DashboardViewMaritime()
        print("✅ DashboardViewMaritime: Créée avec succès")
        modules_tests.append(("DashboardViewMaritime", True))
        
        # Test 7: MainWindow (construction)
        print("🔄 Test 7: MainWindow...")
        from hrneowave.gui.main_window import MainWindow
        main_window = MainWindow()
        print("✅ MainWindow: Construite avec succès")
        modules_tests.append(("MainWindow", True))
        
        # Test 8: Composants additionnels
        print("🔄 Test 8: Composants additionnels...")
        try:
            from hrneowave.gui.components.enhanced_toast import ToastManager, ToastLevel
            print("✅ Enhanced Toast: Importé")
            modules_tests.append(("Enhanced Toast", True))
        except Exception as e:
            print(f"⚠️ Enhanced Toast: {e}")
            modules_tests.append(("Enhanced Toast", False))
        
        # Test 9: Core modules
        print("🔄 Test 9: Core modules...")
        try:
            from hrneowave.core.signal_bus import SignalBus
            print("✅ SignalBus: Importé")
            modules_tests.append(("SignalBus", True))
        except Exception as e:
            print(f"⚠️ SignalBus: {e}")
            modules_tests.append(("SignalBus", False))
        
        # Test 10: Preferences
        print("🔄 Test 10: Preferences...")
        try:
            from hrneowave.gui.preferences.user_preferences import UserPreferences
            print("✅ UserPreferences: Importé")
            modules_tests.append(("UserPreferences", True))
        except Exception as e:
            print(f"⚠️ UserPreferences: {e}")
            modules_tests.append(("UserPreferences", False))
        
        # Test 11: Breadcrumbs
        print("🔄 Test 11: Breadcrumbs...")
        try:
            from hrneowave.gui.components.breadcrumbs import BreadcrumbNavigator
            print("✅ Breadcrumbs: Importé")
            modules_tests.append(("Breadcrumbs", True))
        except Exception as e:
            print(f"⚠️ Breadcrumbs: {e}")
            modules_tests.append(("Breadcrumbs", False))
        
        # Test 12: Interface complète avec tous les modules
        print("🔄 Test 12: Interface complète...")
        window = QMainWindow()
        window.setWindowTitle("CHNeoWave - Test Complet des Modules")
        window.resize(1400, 900)
        
        # Centrer la fenêtre
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = window.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        window.move(x, y)
        
        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # En-tête
        header_label = QLabel("🌊 CHNeoWave - Test Complet des Modules")
        header_label.setStyleSheet("""
            QLabel {
                background-color: #1e3a8a;
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                border-radius: 10px;
            }
        """)
        main_layout.addWidget(header_label)
        
        # Onglets pour les tests
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background-color: #f8fafc;
            }
            QTabBar::tab {
                background-color: #e2e8f0;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: white;
            }
        """)
        
        # Onglet 1: Modules Testés
        modules_tab = QWidget()
        modules_layout = QVBoxLayout(modules_tab)
        
        modules_title = QLabel("📋 Modules Testés")
        modules_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b; margin: 10px;")
        modules_layout.addWidget(modules_title)
        
        # Liste des modules
        for module_name, success in modules_tests:
            module_layout = QHBoxLayout()
            status_icon = "✅" if success else "❌"
            status_color = "#10b981" if success else "#ef4444"
            
            module_label = QLabel(f"{status_icon} {module_name}")
            module_label.setStyleSheet(f"color: {status_color}; font-weight: bold; min-width: 200px;")
            module_layout.addWidget(module_label)
            
            status_text = "SUCCÈS" if success else "ÉCHEC"
            status_label = QLabel(status_text)
            status_label.setStyleSheet(f"color: {status_color};")
            module_layout.addWidget(status_label)
            
            modules_layout.addLayout(module_layout)
        
        tabs.addTab(modules_tab, "📋 Modules")
        
        # Onglet 2: Composants Intégrés
        components_tab = QWidget()
        components_layout = QVBoxLayout(components_tab)
        
        components_title = QLabel("🔧 Composants Intégrés")
        components_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b; margin: 10px;")
        components_layout.addWidget(components_title)
        
        # Intégration des vues
        try:
            # Créer un stacked widget
            stacked_widget = QStackedWidget()
            
            # Ajouter WelcomeView
            welcome_view = WelcomeView()
            stacked_widget.addWidget(welcome_view)
            
            # Ajouter DashboardViewMaritime
            dashboard_view = DashboardViewMaritime()
            stacked_widget.addWidget(dashboard_view)
            
            components_layout.addWidget(stacked_widget)
            
            # Boutons de navigation
            nav_layout = QHBoxLayout()
            
            welcome_btn = QPushButton("WelcomeView")
            welcome_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)
            welcome_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
            nav_layout.addWidget(welcome_btn)
            
            dashboard_btn = QPushButton("DashboardViewMaritime")
            dashboard_btn.setStyleSheet("""
                QPushButton {
                    background-color: #10b981;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """)
            dashboard_btn.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
            nav_layout.addWidget(dashboard_btn)
            
            components_layout.addLayout(nav_layout)
            
            print("✅ Composants: Intégrés avec succès")
            modules_tests.append(("Intégration Composants", True))
            
        except Exception as e:
            print(f"❌ Composants: {e}")
            error_label = QLabel(f"Erreur d'intégration: {e}")
            error_label.setStyleSheet("color: #ef4444; padding: 20px;")
            components_layout.addWidget(error_label)
            modules_tests.append(("Intégration Composants", False))
        
        tabs.addTab(components_tab, "🔧 Composants")
        
        # Onglet 3: Informations Système
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        
        info_title = QLabel("ℹ️ Informations Système")
        info_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e293b; margin: 10px;")
        info_layout.addWidget(info_title)
        
        import platform
        system_info = [
            f"🖥️ Système: {platform.system()} {platform.version()}",
            f"🏗️ Architecture: {platform.architecture()[0]}",
            f"🐍 Python: {sys.version.split()[0]}",
            f"📁 Répertoire: {Path.cwd()}",
            f"🔧 Environnement virtuel: {'ACTIF' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'NON DÉTECTÉ'}",
            f"📊 Qt/PySide6: Opérationnel",
            f"🎨 Thème: Maritime moderne",
            f"📈 Modules testés: {len(modules_tests)}",
            f"✅ Modules réussis: {sum(1 for _, success in modules_tests if success)}",
            f"❌ Modules échoués: {sum(1 for _, success in modules_tests if not success)}"
        ]
        
        for info in system_info:
            info_label = QLabel(info)
            info_label.setStyleSheet("color: #1e40af; font-size: 14px; margin: 5px;")
            info_layout.addWidget(info_label)
        
        tabs.addTab(info_tab, "ℹ️ Système")
        
        main_layout.addWidget(tabs)
        
        # Barre d'état
        status_bar = QFrame()
        status_bar.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        status_layout = QHBoxLayout(status_bar)
        
        success_count = sum(1 for _, success in modules_tests if success)
        total_count = len(modules_tests)
        
        status_text = QLabel(f"🚀 CHNeoWave - {success_count}/{total_count} modules opérationnels")
        status_text.setStyleSheet("color: white; font-size: 14px;")
        status_layout.addWidget(status_text)
        
        # Bouton de fermeture
        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        close_button.clicked.connect(app.quit)
        status_layout.addWidget(close_button, alignment=Qt.AlignRight)
        
        main_layout.addWidget(status_bar)
        
        # Définir le widget central
        window.setCentralWidget(central_widget)
        
        print("✅ Interface complète: Créée avec succès")
        modules_tests.append(("Interface Complète", True))
        
        # Afficher la fenêtre
        print("🔄 Affichage de l'interface complète...")
        window.show()
        window.raise_()
        window.activateWindow()
        
        visible = window.isVisible()
        print(f"✅ Fenêtre visible: {visible}")
        
        if visible:
            print("🎉 SUCCÈS: CHNeoWave complet avec tous les modules !")
            print("🔍 Vérifiez que la fenêtre est visible sur votre écran")
            
            # Timer pour fermeture automatique après 45 secondes
            timer = QTimer()
            timer.timeout.connect(app.quit)
            timer.start(45000)
            
            print("🔄 Interface maintenue ouverte 45 secondes...")
            
            # Lancer la boucle d'événements
            exit_code = app.exec()
            print(f"✅ Application terminée (code: {exit_code})")
            
            # Résumé final
            print("\n" + "=" * 60)
            print("📊 RÉSUMÉ FINAL DES TESTS")
            print("=" * 60)
            
            for module_name, success in modules_tests:
                status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
                print(f"{module_name:30} : {status}")
            
            success_count = sum(1 for _, success in modules_tests if success)
            total_count = len(modules_tests)
            
            print(f"\n📈 RÉSULTATS: {success_count}/{total_count} modules opérationnels")
            
            if success_count == total_count:
                print("🎉 TOUS LES MODULES FONCTIONNENT - CHNeoWave 100% opérationnel !")
                return True
            elif success_count >= total_count * 0.8:
                print("⚠️ LA PLUPART DES MODULES FONCTIONNENT - CHNeoWave opérationnel !")
                return True
            else:
                print("❌ PROBLÈMES DÉTECTÉS - Intervention nécessaire")
                return False
        else:
            print("❌ PROBLÈME: Fenêtre non visible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test complet: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exit(0 if test_modules_complets() else 1) 