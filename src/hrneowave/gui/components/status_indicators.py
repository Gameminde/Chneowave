#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composants d'indicateurs de statut pour CHNeoWave
Fournit des indicateurs visuels pour l'état du système, des capteurs et des processus
"""

import logging
from enum import Enum
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
    QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Signal, QTimer, QPropertyAnimation, QEasingCurve, Property, Qt
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from .material_components import MaterialTheme, MaterialColor

logger = logging.getLogger(__name__)

class StatusLevel(Enum):
    """Niveaux de statut pour les indicateurs"""
    UNKNOWN = "unknown"
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    OFFLINE = "offline"
    CONNECTING = "connecting"
    PROCESSING = "processing"

class StatusIndicator(QWidget):
    """Indicateur de statut circulaire avec animation"""
    
    status_changed = Signal(str, str)  # (indicator_id, new_status)
    
    def __init__(self, indicator_id: str = "", size: int = 16, parent=None):
        super().__init__(parent)
        self.indicator_id = indicator_id
        self._status = StatusLevel.UNKNOWN
        self._size = size
        self._pulse_opacity = 1.0
        
        # Configuration du widget
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Animation de pulsation pour les états actifs
        self._pulse_animation = QPropertyAnimation(self, b"pulse_opacity")
        self._pulse_animation.setDuration(1000)
        self._pulse_animation.setStartValue(0.3)
        self._pulse_animation.setEndValue(1.0)
        self._pulse_animation.setEasingCurve(QEasingCurve.InOutSine)
        self._pulse_animation.setLoopCount(-1)  # Boucle infinie
        
        # Couleurs selon le thème Material Design
        self._colors = {
            StatusLevel.UNKNOWN: MaterialColor.SURFACE_VARIANT,
            StatusLevel.OK: MaterialColor.PRIMARY,
            StatusLevel.WARNING: MaterialColor.TERTIARY,
            StatusLevel.ERROR: MaterialColor.ERROR,
            StatusLevel.CRITICAL: MaterialColor.ERROR,
            StatusLevel.OFFLINE: MaterialColor.OUTLINE,
            StatusLevel.CONNECTING: MaterialColor.SECONDARY,
            StatusLevel.PROCESSING: MaterialColor.PRIMARY
        }
    
    @Property(float)
    def pulse_opacity(self):
        return self._pulse_opacity
    
    @pulse_opacity.setter
    def pulse_opacity(self, value):
        self._pulse_opacity = value
        self.update()
    
    def set_status(self, status: StatusLevel, animate: bool = True):
        """Définit le statut de l'indicateur"""
        if self._status != status:
            old_status = self._status.value if self._status else "unknown"
            self._status = status
            
            # Gérer l'animation selon le statut
            if status in [StatusLevel.CONNECTING, StatusLevel.PROCESSING]:
                if animate:
                    self._pulse_animation.start()
            else:
                self._pulse_animation.stop()
                self._pulse_opacity = 1.0
            
            self.update()
            self.status_changed.emit(self.indicator_id, status.value)
            logger.debug(f"Indicateur {self.indicator_id}: {old_status} -> {status.value}")
    
    def get_status(self) -> StatusLevel:
        """Retourne le statut actuel"""
        return self._status
    
    def paintEvent(self, event):
        """Dessine l'indicateur de statut"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Obtenir la couleur selon le statut
        color = self._colors.get(self._status, MaterialColor.SURFACE_VARIANT)
        
        # Appliquer l'opacité de pulsation
        # Gérer le cas où color pourrait être un QVariant
        if isinstance(color, str):
            color_with_opacity = QColor(color)
        else:
            color_with_opacity = QColor(str(color))
        color_with_opacity.setAlphaF(self._pulse_opacity)
        
        # Dessiner le cercle principal
        painter.setBrush(QBrush(color_with_opacity))
        painter.setPen(QPen(color_with_opacity.darker(120), 1))
        
        margin = 2
        painter.drawEllipse(
            margin, margin, 
            self._size - 2 * margin, 
            self._size - 2 * margin
        )
        
        # Effet de brillance pour les statuts OK
        if self._status == StatusLevel.OK:
            if isinstance(color, str):
                highlight_color = QColor(color)
            else:
                highlight_color = QColor(str(color))
            highlight_color.setAlphaF(0.3 * self._pulse_opacity)
            painter.setBrush(QBrush(highlight_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                margin + 2, margin + 2,
                self._size - 2 * (margin + 2),
                self._size - 2 * (margin + 2)
            )

class StatusCard(QFrame):
    """Carte d'affichage de statut avec indicateur et texte"""
    
    def __init__(self, title: str, status_id: str = "", parent=None):
        super().__init__(parent)
        self.status_id = status_id
        self._setup_ui(title)
        self._apply_material_style()
    
    def _setup_ui(self, title: str):
        """Configure l'interface de la carte de statut"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        
        # Indicateur de statut
        self.status_indicator = StatusIndicator(self.status_id, size=12)
        layout.addWidget(self.status_indicator)
        
        # Texte du titre
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.title_label)
        
        # Texte de détail (optionnel)
        self.detail_label = QLabel()
        self.detail_label.setFont(QFont("Segoe UI", 8))
        self.detail_label.setStyleSheet("color: #999999;")
        layout.addWidget(self.detail_label)
        
        layout.addStretch()
    
    def _apply_material_style(self):
        """Applique le style Material Design à la carte"""
        self.setStyleSheet(f"""
            StatusCard {{
                background-color: {MaterialColor.SURFACE};
                border: 1px solid {MaterialColor.OUTLINE_VARIANT};
                border-radius: 8px;
                padding: 4px;
            }}
            StatusCard:hover {{
                background-color: {MaterialColor.SURFACE_VARIANT};
                border-color: {MaterialColor.OUTLINE};
            }}
        """)
        
        # Effet d'ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 1)
        self.setGraphicsEffect(shadow)
    
    def set_status(self, status: StatusLevel, detail: str = ""):
        """Met à jour le statut de la carte"""
        self.status_indicator.set_status(status)
        if detail:
            self.detail_label.setText(detail)
            self.detail_label.setVisible(True)
        else:
            self.detail_label.setVisible(False)
    
    def get_status(self) -> StatusLevel:
        """Retourne le statut actuel"""
        return self.status_indicator.get_status()

class SystemStatusWidget(QWidget):
    """Widget d'affichage du statut global du système"""
    
    status_updated = Signal(str, str, str)  # (component, status, detail)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_cards: Dict[str, StatusCard] = {}
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface du widget de statut système"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Titre
        title_label = QLabel("État du Système")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {MaterialColor.ON_SURFACE};")
        layout.addWidget(title_label)
        
        # Conteneur pour les cartes de statut
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setSpacing(2)
        layout.addLayout(self.cards_layout)
        
        layout.addStretch()
    
    def add_status_component(self, component_id: str, title: str):
        """Ajoute un composant de statut"""
        if component_id not in self.status_cards:
            card = StatusCard(title, component_id)
            card.status_indicator.status_changed.connect(
                lambda comp_id, status: self.status_updated.emit(comp_id, status, "")
            )
            self.status_cards[component_id] = card
            self.cards_layout.addWidget(card)
            logger.debug(f"Composant de statut ajouté: {component_id}")
    
    def update_component_status(self, component_id: str, status: StatusLevel, detail: str = ""):
        """Met à jour le statut d'un composant"""
        if component_id in self.status_cards:
            self.status_cards[component_id].set_status(status, detail)
            self.status_updated.emit(component_id, status.value, detail)
        else:
            logger.warning(f"Tentative de mise à jour d'un composant inexistant: {component_id}")
    
    def get_component_status(self, component_id: str) -> Optional[StatusLevel]:
        """Retourne le statut d'un composant"""
        if component_id in self.status_cards:
            return self.status_cards[component_id].get_status()
        return None
    
    def remove_component(self, component_id: str):
        """Supprime un composant de statut"""
        if component_id in self.status_cards:
            card = self.status_cards.pop(component_id)
            self.cards_layout.removeWidget(card)
            card.deleteLater()
            logger.debug(f"Composant de statut supprimé: {component_id}")
    
    def get_overall_status(self) -> StatusLevel:
        """Calcule le statut global du système"""
        if not self.status_cards:
            return StatusLevel.UNKNOWN
        
        statuses = [card.get_status() for card in self.status_cards.values()]
        
        # Priorité des statuts (du plus critique au moins critique)
        priority_order = [
            StatusLevel.CRITICAL,
            StatusLevel.ERROR,
            StatusLevel.OFFLINE,
            StatusLevel.WARNING,
            StatusLevel.CONNECTING,
            StatusLevel.PROCESSING,
            StatusLevel.OK,
            StatusLevel.UNKNOWN
        ]
        
        for priority_status in priority_order:
            if priority_status in statuses:
                return priority_status
        
        return StatusLevel.UNKNOWN