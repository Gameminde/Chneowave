#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composants de barre de progression améliorée pour CHNeoWave
Fournit des barres de progression avec animations fluides et feedback détaillé
"""

import logging
from enum import Enum
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QFrame, QPushButton
)
from PySide6.QtCore import (
    Signal, QTimer, QPropertyAnimation, QEasingCurve, 
    pyqtProperty, Qt, QRect
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, 
    QLinearGradient, QPainterPath
)
from ..material_components import MaterialTheme, MaterialColor

logger = logging.getLogger(__name__)

class ProgressState(Enum):
    """États possibles pour une barre de progression"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"

class MaterialProgressBar(QProgressBar):
    """Barre de progression avec style Material Design et animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = ProgressState.IDLE
        self._animated_value = 0.0
        self._setup_style()
        self._setup_animation()
    
    def _setup_style(self):
        """Configure le style Material Design"""
        self.setTextVisible(False)
        self.setFixedHeight(6)
        
        # Style CSS Material Design
        self.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 3px;
                background-color: {MaterialColor.SURFACE_VARIANT};
                text-align: center;
            }}
            QProgressBar::chunk {{
                border-radius: 3px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 {MaterialColor.PRIMARY},
                    stop: 1 {MaterialColor.PRIMARY_CONTAINER}
                );
            }}
        """)
    
    def _setup_animation(self):
        """Configure l'animation de la barre de progression"""
        self._animation = QPropertyAnimation(self, b"animated_value")
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
    
    @pyqtProperty(float)
    def animated_value(self):
        return self._animated_value
    
    @animated_value.setter
    def animated_value(self, value):
        self._animated_value = value
        super().setValue(int(value))
    
    def setValue(self, value: int):
        """Définit la valeur avec animation"""
        if self._state == ProgressState.RUNNING:
            self._animation.setStartValue(self._animated_value)
            self._animation.setEndValue(value)
            self._animation.start()
        else:
            self._animated_value = value
            super().setValue(value)
    
    def set_state(self, state: ProgressState):
        """Définit l'état de la barre de progression"""
        self._state = state
        
        # Adapter le style selon l'état
        if state == ProgressState.ERROR:
            self.setStyleSheet(self.styleSheet().replace(
                MaterialColor.PRIMARY, MaterialColor.ERROR
            ))
        elif state == ProgressState.COMPLETED:
            self.setStyleSheet(self.styleSheet().replace(
                MaterialColor.PRIMARY, MaterialColor.TERTIARY
            ))
        elif state == ProgressState.PAUSED:
            self.setStyleSheet(self.styleSheet().replace(
                MaterialColor.PRIMARY, MaterialColor.SECONDARY
            ))
        else:
            self._setup_style()  # Restaurer le style par défaut
    
    def get_state(self) -> ProgressState:
        """Retourne l'état actuel"""
        return self._state

class ProgressCard(QFrame):
    """Carte de progression avec titre, barre de progression et contrôles"""
    
    # Signaux
    pause_requested = Signal()
    resume_requested = Signal()
    cancel_requested = Signal()
    
    def __init__(self, title: str, show_controls: bool = True, parent=None):
        super().__init__(parent)
        self.title = title
        self.show_controls = show_controls
        self._current_step = ""
        self._total_steps = 0
        self._current_step_index = 0
        self._setup_ui()
        self._apply_material_style()
    
    def _setup_ui(self):
        """Configure l'interface de la carte de progression"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # En-tête avec titre et pourcentage
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel(self.title)
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f"color: {MaterialColor.ON_SURFACE};")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.percentage_label = QLabel("0%")
        self.percentage_label.setFont(QFont("Segoe UI", 9))
        self.percentage_label.setStyleSheet(f"color: {MaterialColor.ON_SURFACE_VARIANT};")
        header_layout.addWidget(self.percentage_label)
        
        layout.addLayout(header_layout)
        
        # Barre de progression
        self.progress_bar = MaterialProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Étape actuelle
        self.step_label = QLabel()
        self.step_label.setFont(QFont("Segoe UI", 8))
        self.step_label.setStyleSheet(f"color: {MaterialColor.ON_SURFACE_VARIANT};")
        self.step_label.setVisible(False)
        layout.addWidget(self.step_label)
        
        # Contrôles (pause, reprendre, annuler)
        if self.show_controls:
            self._setup_controls(layout)
    
    def _setup_controls(self, layout):
        """Configure les boutons de contrôle"""
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 8, 0, 0)
        
        # Bouton Pause/Reprendre
        self.pause_resume_btn = QPushButton("Pause")
        self.pause_resume_btn.setFixedSize(80, 28)
        self.pause_resume_btn.clicked.connect(self._on_pause_resume_clicked)
        self._style_button(self.pause_resume_btn, MaterialColor.SECONDARY)
        controls_layout.addWidget(self.pause_resume_btn)
        
        controls_layout.addStretch()
        
        # Bouton Annuler
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setFixedSize(80, 28)
        self.cancel_btn.clicked.connect(self.cancel_requested.emit)
        self._style_button(self.cancel_btn, MaterialColor.ERROR)
        controls_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(controls_layout)
    
    def _style_button(self, button: QPushButton, color: str):
        """Applique le style Material Design aux boutons"""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 9px;
                font-weight: bold;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: {color};
                opacity: 0.8;
            }}
            QPushButton:pressed {{
                background-color: {color};
                opacity: 0.6;
            }}
            QPushButton:disabled {{
                background-color: {MaterialColor.SURFACE_VARIANT};
                color: {MaterialColor.ON_SURFACE_VARIANT};
            }}
        """)
    
    def _apply_material_style(self):
        """Applique le style Material Design à la carte"""
        self.setStyleSheet(f"""
            ProgressCard {{
                background-color: {MaterialColor.SURFACE};
                border: 1px solid {MaterialColor.OUTLINE_VARIANT};
                border-radius: 12px;
            }}
        """)
    
    def _on_pause_resume_clicked(self):
        """Gère le clic sur le bouton pause/reprendre"""
        current_state = self.progress_bar.get_state()
        
        if current_state == ProgressState.RUNNING:
            self.pause_requested.emit()
            self.pause_resume_btn.setText("Reprendre")
        elif current_state == ProgressState.PAUSED:
            self.resume_requested.emit()
            self.pause_resume_btn.setText("Pause")
    
    def set_progress(self, value: int, total: int = 100):
        """Met à jour la progression"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(value)
        
        percentage = int((value / total) * 100) if total > 0 else 0
        self.percentage_label.setText(f"{percentage}%")
    
    def set_current_step(self, step: str, step_index: int = 0, total_steps: int = 0):
        """Définit l'étape actuelle"""
        self._current_step = step
        self._current_step_index = step_index
        self._total_steps = total_steps
        
        if step:
            if total_steps > 0:
                step_text = f"Étape {step_index + 1}/{total_steps}: {step}"
            else:
                step_text = step
            
            self.step_label.setText(step_text)
            self.step_label.setVisible(True)
        else:
            self.step_label.setVisible(False)
    
    def set_state(self, state: ProgressState):
        """Définit l'état de la progression"""
        self.progress_bar.set_state(state)
        
        # Adapter les contrôles selon l'état
        if self.show_controls:
            if state in [ProgressState.COMPLETED, ProgressState.ERROR, ProgressState.CANCELLED]:
                self.pause_resume_btn.setEnabled(False)
                self.cancel_btn.setEnabled(False)
            elif state == ProgressState.PAUSED:
                self.pause_resume_btn.setText("Reprendre")
                self.pause_resume_btn.setEnabled(True)
                self.cancel_btn.setEnabled(True)
            elif state == ProgressState.RUNNING:
                self.pause_resume_btn.setText("Pause")
                self.pause_resume_btn.setEnabled(True)
                self.cancel_btn.setEnabled(True)
            else:
                self.pause_resume_btn.setEnabled(False)
                self.cancel_btn.setEnabled(False)
    
    def get_state(self) -> ProgressState:
        """Retourne l'état actuel"""
        return self.progress_bar.get_state()

class MultiStepProgressWidget(QWidget):
    """Widget de progression multi-étapes pour les workflows complexes"""
    
    step_completed = Signal(int, str)  # (step_index, step_name)
    all_steps_completed = Signal()
    
    def __init__(self, steps: list = None, parent=None):
        super().__init__(parent)
        self.steps = steps or []
        self.current_step_index = -1
        self.step_cards: Dict[int, ProgressCard] = {}
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface du widget multi-étapes"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
        
        # Titre principal
        self.main_title = QLabel("Progression du Workflow")
        self.main_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.main_title.setStyleSheet(f"color: {MaterialColor.ON_SURFACE};")
        self.layout.addWidget(self.main_title)
        
        # Créer les cartes pour chaque étape
        self._create_step_cards()
    
    def _create_step_cards(self):
        """Crée les cartes de progression pour chaque étape"""
        for i, step_name in enumerate(self.steps):
            card = ProgressCard(f"Étape {i + 1}: {step_name}", show_controls=False)
            card.set_state(ProgressState.IDLE)
            card.set_progress(0)
            
            self.step_cards[i] = card
            self.layout.addWidget(card)
    
    def start_step(self, step_index: int):
        """Démarre une étape spécifique"""
        if step_index < len(self.steps):
            self.current_step_index = step_index
            
            # Marquer les étapes précédentes comme complétées
            for i in range(step_index):
                if i in self.step_cards:
                    self.step_cards[i].set_state(ProgressState.COMPLETED)
                    self.step_cards[i].set_progress(100)
            
            # Démarrer l'étape actuelle
            if step_index in self.step_cards:
                self.step_cards[step_index].set_state(ProgressState.RUNNING)
                self.step_cards[step_index].set_progress(0)
            
            logger.info(f"Étape {step_index + 1} démarrée: {self.steps[step_index]}")
    
    def update_step_progress(self, step_index: int, progress: int):
        """Met à jour la progression d'une étape"""
        if step_index in self.step_cards:
            self.step_cards[step_index].set_progress(progress)
    
    def complete_step(self, step_index: int):
        """Marque une étape comme complétée"""
        if step_index in self.step_cards:
            self.step_cards[step_index].set_state(ProgressState.COMPLETED)
            self.step_cards[step_index].set_progress(100)
            
            self.step_completed.emit(step_index, self.steps[step_index])
            logger.info(f"Étape {step_index + 1} complétée: {self.steps[step_index]}")
            
            # Vérifier si toutes les étapes sont complétées
            if step_index == len(self.steps) - 1:
                self.all_steps_completed.emit()
                logger.info("Toutes les étapes du workflow sont complétées")
    
    def set_step_error(self, step_index: int, error_message: str = ""):
        """Marque une étape en erreur"""
        if step_index in self.step_cards:
            self.step_cards[step_index].set_state(ProgressState.ERROR)
            if error_message:
                self.step_cards[step_index].set_current_step(f"Erreur: {error_message}")
            
            logger.error(f"Erreur à l'étape {step_index + 1}: {error_message}")
    
    def reset_workflow(self):
        """Remet à zéro le workflow"""
        self.current_step_index = -1
        for card in self.step_cards.values():
            card.set_state(ProgressState.IDLE)
            card.set_progress(0)
            card.set_current_step("")
        
        logger.info("Workflow remis à zéro")