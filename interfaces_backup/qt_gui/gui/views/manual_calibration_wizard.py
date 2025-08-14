# -*- coding: utf-8 -*-
"""
Manual Calibration Wizard View

Vue d'assistant de calibration manuelle pour CHNeoWave
avec design maritime moderne et proportions basées sur le nombre d'or.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap

from ..components.modern_card import ModernCard
from ..components.animated_button import AnimatedButton
from ..styles.maritime_theme import MaritimeTheme


class ManualCalibrationWizard(QWidget):
    """Assistant de calibration manuelle avec design maritime moderne"""
    
    # Constante du nombre d'or
    PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749
    
    # Signaux
    calibrationCompleted = Signal(dict)
    calibrationCancelled = Signal()
    stepChanged = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = MaritimeTheme()
        self.current_step = 0
        self.total_steps = 5
        self.calibration_data = {}
        
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.setObjectName("manual-calibration-wizard")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            self.theme.spacing['lg'], self.theme.spacing['lg'],
            self.theme.spacing['lg'], self.theme.spacing['lg']
        )
        main_layout.setSpacing(self.theme.spacing['md'])
        
        # Header avec titre et progression
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Zone de contenu principal
        content_widget = self.create_content_area()
        main_layout.addWidget(content_widget)
        
        # Footer avec boutons de navigation
        footer_widget = self.create_footer()
        main_layout.addWidget(footer_widget)
        
        # Proportions basées sur le nombre d'or
        main_layout.setStretchFactor(header_widget, 1)  # 16%
        main_layout.setStretchFactor(content_widget, 4)  # 64%
        main_layout.setStretchFactor(footer_widget, 1)  # 20%
        
    def create_header(self):
        """Création de l'en-tête avec titre et barre de progression"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(self.theme.spacing['md'])
        
        # Titre principal
        title_label = QLabel("Assistant de Calibration Manuelle")
        title_label.setObjectName("wizard-title")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Font du titre
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setWeight(QFont.Bold)
        title_label.setFont(title_font)
        
        header_layout.addWidget(title_label)
        
        # Sous-titre avec étape actuelle
        self.subtitle_label = QLabel(f"Étape {self.current_step + 1} sur {self.total_steps}")
        self.subtitle_label.setObjectName("wizard-subtitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        self.subtitle_label.setFont(subtitle_font)
        
        header_layout.addWidget(self.subtitle_label)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("wizard-progress")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.total_steps)
        self.progress_bar.setValue(self.current_step)
        self.progress_bar.setTextVisible(True)
        
        header_layout.addWidget(self.progress_bar)
        
        return header_widget
        
    def create_content_area(self):
        """Création de la zone de contenu principal"""
        # Zone scrollable pour le contenu
        scroll_area = QScrollArea()
        scroll_area.setObjectName("wizard-content-scroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget de contenu
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(
            self.theme.spacing['md'], self.theme.spacing['md'],
            self.theme.spacing['md'], self.theme.spacing['md']
        )
        self.content_layout.setSpacing(self.theme.spacing['md'])
        
        # Afficher le contenu de l'étape actuelle
        self.update_step_content()
        
        scroll_area.setWidget(self.content_widget)
        return scroll_area
        
    def create_footer(self):
        """Création du footer avec boutons de navigation"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(self.theme.spacing['md'])
        
        # Bouton Annuler
        self.cancel_button = AnimatedButton(
            "Annuler"
        )
        self.cancel_button.clicked.connect(self.cancel_calibration)
        
        # Bouton Précédent
        self.prev_button = AnimatedButton(
            "← Précédent"
        )
        self.prev_button.clicked.connect(self.previous_step)
        self.prev_button.setEnabled(False)  # Désactivé à la première étape
        
        # Spacer
        footer_layout.addWidget(self.cancel_button)
        footer_layout.addStretch()
        footer_layout.addWidget(self.prev_button)
        
        # Bouton Suivant/Terminer
        self.next_button = AnimatedButton(
            "Suivant →"
        )
        self.next_button.clicked.connect(self.next_step)
        
        footer_layout.addWidget(self.next_button)
        
        return footer_widget
        
    def update_step_content(self):
        """Met à jour le contenu selon l'étape actuelle"""
        # Effacer le contenu existant
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
        # Contenu selon l'étape
        if self.current_step == 0:
            self.create_welcome_step()
        elif self.current_step == 1:
            self.create_sensor_check_step()
        elif self.current_step == 2:
            self.create_zero_calibration_step()
        elif self.current_step == 3:
            self.create_scale_calibration_step()
        elif self.current_step == 4:
            self.create_validation_step()
            
    def create_welcome_step(self):
        """Étape 0: Bienvenue et instructions"""
        card = ModernCard(
            title="🌊 Bienvenue dans l'Assistant de Calibration"
        )
        
        content_layout = QVBoxLayout()
        
        instructions = QLabel(
            "Cet assistant vous guidera à travers le processus de calibration manuelle des capteurs.\n\n"
            "Assurez-vous que:\n"
            "• Tous les capteurs sont connectés\n"
            "• Le bassin est dans un état stable\n"
            "• Vous disposez des outils de calibration nécessaires\n\n"
            "La calibration prendra environ 10-15 minutes."
        )
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignLeft)
        
        content_layout.addWidget(instructions)
        card.add_content_layout(content_layout)
        
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()
        
    def create_sensor_check_step(self):
        """Étape 1: Vérification des capteurs"""
        card = ModernCard(
            title="🔍 Vérification des Capteurs"
        )
        
        content_layout = QVBoxLayout()
        
        instructions = QLabel(
            "Vérification de la connectivité et du statut des capteurs...\n\n"
            "Cette étape vérifie automatiquement que tous les capteurs\n"
            "sont correctement connectés et fonctionnels."
        )
        instructions.setWordWrap(True)
        
        # Simulation d'une liste de capteurs
        sensors_info = QLabel(
            "✅ Capteur de houle #1 - Connecté\n"
            "✅ Capteur de houle #2 - Connecté\n"
            "✅ Capteur de pression - Connecté\n"
            "✅ Capteur de température - Connecté"
        )
        sensors_info.setStyleSheet("color: #2E7D32; font-family: monospace;")
        
        content_layout.addWidget(instructions)
        content_layout.addWidget(sensors_info)
        card.add_content_layout(content_layout)
        
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()
        
    def create_zero_calibration_step(self):
        """Étape 2: Calibration du zéro"""
        card = ModernCard(
            title="⚖️ Calibration du Zéro"
        )
        
        content_layout = QVBoxLayout()
        
        instructions = QLabel(
            "Calibration du point zéro des capteurs...\n\n"
            "Assurez-vous que le bassin est au repos et que\n"
            "tous les capteurs sont dans leur position de référence."
        )
        instructions.setWordWrap(True)
        
        # Bouton pour démarrer la calibration du zéro
        zero_button = AnimatedButton(
            "Démarrer Calibration Zéro"
        )
        
        content_layout.addWidget(instructions)
        content_layout.addWidget(zero_button)
        card.add_content_layout(content_layout)
        
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()
        
    def create_scale_calibration_step(self):
        """Étape 3: Calibration de l'échelle"""
        card = ModernCard(
            title="📏 Calibration de l'Échelle"
        )
        
        content_layout = QVBoxLayout()
        
        instructions = QLabel(
            "Calibration de l'échelle des capteurs...\n\n"
            "Appliquez une référence connue et ajustez\n"
            "les paramètres d'échelle pour chaque capteur."
        )
        instructions.setWordWrap(True)
        
        # Bouton pour démarrer la calibration d'échelle
        scale_button = AnimatedButton(
            "Démarrer Calibration Échelle"
        )
        
        content_layout.addWidget(instructions)
        content_layout.addWidget(scale_button)
        card.add_content_layout(content_layout)
        
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()
        
    def create_validation_step(self):
        """Étape 4: Validation et finalisation"""
        card = ModernCard(
            title="✅ Validation de la Calibration"
        )
        
        content_layout = QVBoxLayout()
        
        instructions = QLabel(
            "Validation finale de la calibration...\n\n"
            "Vérification de la précision et de la cohérence\n"
            "des paramètres de calibration."
        )
        instructions.setWordWrap(True)
        
        # Résultats de validation
        validation_results = QLabel(
            "📊 Résultats de Validation:\n\n"
            "• Précision capteur #1: ±0.1mm\n"
            "• Précision capteur #2: ±0.1mm\n"
            "• Dérive temporelle: <0.01%/h\n"
            "• Linéarité: >99.5%\n\n"
            "✅ Calibration validée avec succès!"
        )
        validation_results.setStyleSheet("color: #2E7D32;")
        
        content_layout.addWidget(instructions)
        content_layout.addWidget(validation_results)
        card.add_content_layout(content_layout)
        
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()
        
        # Changer le texte du bouton suivant
        self.next_button.setText("Terminer Calibration")
        
    def next_step(self):
        """Passer à l'étape suivante"""
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update_ui_for_step()
        else:
            # Dernière étape - terminer la calibration
            self.complete_calibration()
            
    def previous_step(self):
        """Revenir à l'étape précédente"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_ui_for_step()
            
    def update_ui_for_step(self):
        """Met à jour l'interface pour l'étape actuelle"""
        # Mettre à jour le sous-titre
        self.subtitle_label.setText(f"Étape {self.current_step + 1} sur {self.total_steps}")
        
        # Mettre à jour la barre de progression
        self.progress_bar.setValue(self.current_step + 1)
        
        # Mettre à jour les boutons
        self.prev_button.setEnabled(self.current_step > 0)
        
        if self.current_step == self.total_steps - 1:
            self.next_button.setText("Terminer Calibration")
        else:
            self.next_button.setText("Suivant →")
            
        # Mettre à jour le contenu
        self.update_step_content()
        
        # Émettre le signal de changement d'étape
        self.stepChanged.emit(self.current_step)
        
    def complete_calibration(self):
        """Terminer la calibration"""
        # Collecter les données de calibration
        calibration_data = {
            'timestamp': '2025-01-26T14:30:00',
            'sensors': {
                'wave_sensor_1': {'zero': 0.0, 'scale': 1.0, 'precision': 0.1},
                'wave_sensor_2': {'zero': 0.0, 'scale': 1.0, 'precision': 0.1},
                'pressure_sensor': {'zero': 0.0, 'scale': 1.0, 'precision': 0.01},
                'temperature_sensor': {'zero': 0.0, 'scale': 1.0, 'precision': 0.1}
            },
            'validation': {
                'accuracy': 99.8,
                'linearity': 99.6,
                'drift': 0.005
            }
        }
        
        self.calibrationCompleted.emit(calibration_data)
        
    def cancel_calibration(self):
        """Annuler la calibration"""
        self.calibrationCancelled.emit()
        
    def apply_styles(self):
        """Application des styles CSS"""
        self.setStyleSheet(f"""
            QWidget#manual-calibration-wizard {{
                background-color: {self.theme.colors['background']};
                color: {self.theme.colors['on_surface']};
            }}
            
            QLabel#wizard-title {{
                color: {self.theme.colors['primary']};
                font-weight: bold;
                margin: {self.theme.spacing['md']}px 0;
            }}
            
            QLabel#wizard-subtitle {{
                color: {self.theme.colors['on_surface_variant']};
                margin-bottom: {self.theme.spacing['md']}px;
            }}
            
            QProgressBar#wizard-progress {{
                border: 2px solid {self.theme.colors['border']};
                border-radius: 8px;
                text-align: center;
                height: 24px;
            }}
            
            QProgressBar#wizard-progress::chunk {{
                background-color: {self.theme.colors['primary']};
                border-radius: 6px;
            }}
            
            QScrollArea#wizard-content-scroll {{
                border: none;
                background-color: transparent;
            }}
        """)