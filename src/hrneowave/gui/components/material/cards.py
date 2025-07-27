#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Cards
Composants de cartes Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from enum import Enum
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor

from .theme import MaterialTheme, MaterialAnimations, MaterialShape, MaterialElevation


class MaterialCard(QFrame):
    """Carte Material Design 3"""
    
    class Type(Enum):
        """Types de carte Material Design 3"""
        ELEVATED = "elevated"
        FILLED = "filled"
        OUTLINED = "outlined"
    
    def __init__(self, card_type: Type = Type.ELEVATED, parent=None):
        super().__init__(parent)
        self.card_type = card_type
        self.theme = MaterialTheme()
        self._elevation = MaterialElevation.LEVEL_1.value
        self._is_hovered = False
        
        # Configuration de base
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Animation d'élévation
        self.elevation_animation = QPropertyAnimation(self, b"elevation")
        self.elevation_animation.setDuration(MaterialAnimations.get_scale_duration())
        self.elevation_animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
        
        self.apply_style()
        
        # Événements de souris pour l'animation
        self.enterEvent = self._on_enter
        self.leaveEvent = self._on_leave
    
    def get_elevation(self) -> int:
        """Getter pour l'élévation"""
        return self._elevation
    
    def set_elevation(self, value: int):
        """Setter pour l'élévation"""
        self._elevation = value
        self.apply_style()
    
    elevation = Property(int, get_elevation, set_elevation)
    
    def apply_style(self):
        """Applique le style selon le type de carte"""
        if self.card_type == self.Type.ELEVATED:
            self._apply_elevated_style()
        elif self.card_type == self.Type.FILLED:
            self._apply_filled_style()
        elif self.card_type == self.Type.OUTLINED:
            self._apply_outlined_style()
    
    def _apply_elevated_style(self):
        """Style carte élevée"""
        # Calcul de l'ombre basé sur l'élévation
        shadow_blur = max(1, self._elevation * 2)
        shadow_offset = max(1, self._elevation)
        
        style = f"""
        QFrame {{
            background-color: {self.theme.surface};
            border: none;
            border-radius: {MaterialShape.MEDIUM.value}px;
            padding: 16px;
        }}
        """
        
        # Note: Qt ne supporte pas les box-shadow CSS, 
        # l'effet d'ombre devrait être implémenté via paintEvent
        self.setStyleSheet(style)
    
    def _apply_filled_style(self):
        """Style carte remplie"""
        style = f"""
        QFrame {{
            background-color: {self.theme.surface_variant};
            border: none;
            border-radius: {MaterialShape.MEDIUM.value}px;
            padding: 16px;
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_outlined_style(self):
        """Style carte contourée"""
        style = f"""
        QFrame {{
            background-color: {self.theme.surface};
            border: 1px solid {self.theme.outline_variant};
            border-radius: {MaterialShape.MEDIUM.value}px;
            padding: 16px;
        }}
        """
        self.setStyleSheet(style)
    
    def _on_enter(self, event):
        """Animation lors de l'entrée de la souris"""
        self._is_hovered = True
        if self.card_type == self.Type.ELEVATED:
            # Augmente l'élévation au survol
            target_elevation = min(MaterialElevation.LEVEL_3.value, self._elevation + 2)
            self.elevation_animation.setStartValue(self._elevation)
            self.elevation_animation.setEndValue(target_elevation)
            self.elevation_animation.start()
        super().enterEvent(event)
    
    def _on_leave(self, event):
        """Animation lors de la sortie de la souris"""
        self._is_hovered = False
        if self.card_type == self.Type.ELEVATED:
            # Restaure l'élévation originale
            original_elevation = MaterialElevation.LEVEL_1.value
            self.elevation_animation.setStartValue(self._elevation)
            self.elevation_animation.setEndValue(original_elevation)
            self.elevation_animation.start()
        super().leaveEvent(event)
    
    def set_type(self, card_type: Type):
        """Change le type de carte"""
        self.card_type = card_type
        self.apply_style()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_style()
    
    def set_clickable(self, clickable: bool = True):
        """Rend la carte cliquable avec des effets visuels"""
        if clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            # Ajouter des effets de clic si nécessaire
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)