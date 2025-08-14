#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale simplifiée pour CHNeoWave
Version de test sans acquisition_controller
"""

import logging
from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Signal, Slot, QTimer, Qt

logger = logging.getLogger(__name__)

# Import conditionnel pour éviter les erreurs
try:
    from hrneowave.gui.controllers.acquisition_controller import AcquisitionController
    ACQUISITION_CONTROLLER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ AcquisitionController non disponible: {e}")
    AcquisitionController = None
    ACQUISITION_CONTROLLER_AVAILABLE = False

try:
    from hrneowave.gui.controllers.main_controller import MainController
    MAIN_CONTROLLER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ MainController non disponible: {e}")
    MainController = None
    MAIN_CONTROLLER_AVAILABLE = False

from hrneowave.gui.styles.theme_manager import ThemeManager

# Import du système d'animations Phase 6
try:
    from hrneowave.gui.animations import PageTransitionManager, TransitionType, MaritimeAnimator
except ImportError:
    PageTransitionManager = None
    TransitionType = None
    MaritimeAnimator = None
    logger.warning("Système d'animations Phase 6 non disponible")

# Import des vues v2 et configurations
try:
    from hrneowave.gui.views import (
        DashboardViewMaritime,
        WelcomeView,
        VIEWS_CONFIG,
        NAVIGATION_ORDER
    )
except ImportError as e:
    print(f"⚠️ Vues non disponibles: {e}")
    DashboardViewMaritime = None
    WelcomeView = None
    VIEWS_CONFIG = {}
    NAVIGATION_ORDER = []

class SimpleMainWindow(QMainWindow):
    """Fenêtre principale simplifiée de l'application CHNeoWave"""
    
    projectCreated = Signal()
    
    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CHNeoWave - Version Simplifiée")
        self.setMinimumSize(1024, 768)
        
        # Configuration
        self.config = config or {}
        
        # État de l'application
        self.is_acquiring = False
        self.acquisition_controller = None
        self.analysis_controller = None
        self.project_controller = None
        
        # Construction de l'interface
        logger.info("Début de la construction de l'interface simplifiée...")
        self._build_simple_ui()
        logger.info("Interface simplifiée construite avec succès")
        
        logger.info("Interface utilisateur simplifiée chargée avec succès")

    def _build_simple_ui(self):
        """Construit une interface utilisateur simplifiée."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Titre
        title_label = QLabel("CHNeoWave - Laboratoire d'Hydrodynamique Maritime")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 20px;
                background-color: #ecf0f1;
                border-radius: 10px;
            }
        """)
        main_layout.addWidget(title_label)

        # Message de statut
        status_label = QLabel("✅ Interface simplifiée chargée avec succès")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #27ae60;
                padding: 15px;
                background-color: #d5f4e6;
                border-radius: 8px;
            }
        """)
        main_layout.addWidget(status_label)

        # Informations système
        info_label = QLabel(f"""
        📊 Informations système:
        • AcquisitionController: {'✅ Disponible' if ACQUISITION_CONTROLLER_AVAILABLE else '❌ Non disponible'}
        • MainController: {'✅ Disponible' if MAIN_CONTROLLER_AVAILABLE else '❌ Non disponible'}
        • Animations Phase 6: {'✅ Disponible' if PageTransitionManager else '❌ Non disponible'}
        • Vues: {'✅ Disponible' if WelcomeView else '❌ Non disponible'}
        """)
        info_label.setAlignment(Qt.AlignLeft)
        info_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #34495e;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        main_layout.addWidget(info_label)

        # Espace flexible
        from PySide6.QtWidgets import QSizePolicy
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)

        # Message de fermeture
        close_label = QLabel("Cette fenêtre se fermera automatiquement dans 10 secondes...")
        close_label.setAlignment(Qt.AlignCenter)
        close_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                padding: 10px;
            }
        """)
        main_layout.addWidget(close_label)

    def showEvent(self, event):
        """Gestionnaire d'événement d'affichage"""
        super().showEvent(event)
        logger.info("Fenêtre simplifiée affichée")

    def closeEvent(self, event):
        """Gestionnaire d'événement de fermeture"""
        logger.info("Fenêtre simplifiée fermée")
        super().closeEvent(event)
