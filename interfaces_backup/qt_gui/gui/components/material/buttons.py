#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Buttons
Composants de boutons Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from enum import Enum
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect, Property
from PySide6.QtGui import QColor

from .theme import MaterialTheme, MaterialAnimations, MaterialShape


class MaterialButton(QPushButton):
    """Bouton Material Design 3"""
    
    class Style(Enum):
        """Styles de bouton Material Design 3"""
        FILLED = "filled"
        OUTLINED = "outlined"
        TEXT = "text"
        ELEVATED = "elevated"
        FILLED_TONAL = "filled_tonal"
    
    def __init__(self, text: str = "", style: Style = Style.FILLED, parent=None):
        super().__init__(text, parent)
        self.button_style = style
        self.theme = MaterialTheme()
        self._elevation = 0
        
        # Configuration de base
        self.setMinimumHeight(40)
        self.setMinimumWidth(64)
        
        # Animation d'élévation
        self.elevation_animation = QPropertyAnimation(self, b"elevation")
        self.elevation_animation.setDuration(MaterialAnimations.get_scale_duration())
        self.elevation_animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
        
        self.apply_style()
        
        # Connexions pour les animations
        self.pressed.connect(self._on_pressed)
        self.released.connect(self._on_released)
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
        """Applique le style selon le type de bouton"""
        if self.button_style == self.Style.FILLED:
            self._apply_filled_style()
        elif self.button_style == self.Style.OUTLINED:
            self._apply_outlined_style()
        elif self.button_style == self.Style.TEXT:
            self._apply_text_style()
        elif self.button_style == self.Style.ELEVATED:
            self._apply_elevated_style()
        elif self.button_style == self.Style.FILLED_TONAL:
            self._apply_filled_tonal_style()
    
    def _apply_filled_style(self):
        """Style bouton rempli"""
        style = f"""
        QPushButton {{
            background-color: {self.theme.primary};
            color: {self.theme.on_primary};
            border: none;
            border-radius: {MaterialShape.FULL.value}px;
            padding: 10px 24px;
            font-weight: 500;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.primary, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.primary, 0.12)};
        }}
        QPushButton:disabled {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.12)};
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_outlined_style(self):
        """Style bouton contouré"""
        style = f"""
        QPushButton {{
            background-color: transparent;
            color: {self.theme.primary};
            border: 1px solid {self.theme.outline};
            border-radius: {MaterialShape.FULL.value}px;
            padding: 10px 24px;
            font-weight: 500;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.primary, 0.08)};
            border-color: {self.theme.primary};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.primary, 0.12)};
        }}
        QPushButton:disabled {{
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
            border-color: {self._adjust_color(self.theme.on_surface, 0.12)};
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_text_style(self):
        """Style bouton texte"""
        style = f"""
        QPushButton {{
            background-color: transparent;
            color: {self.theme.primary};
            border: none;
            border-radius: {MaterialShape.FULL.value}px;
            padding: 10px 12px;
            font-weight: 500;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.primary, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.primary, 0.12)};
        }}
        QPushButton:disabled {{
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_elevated_style(self):
        """Style bouton élevé"""
        shadow_blur = max(1, self._elevation * 2)
        style = f"""
        QPushButton {{
            background-color: {self.theme.surface};
            color: {self.theme.primary};
            border: none;
            border-radius: {MaterialShape.FULL.value}px;
            padding: 10px 24px;
            font-weight: 500;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.primary, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.primary, 0.12)};
        }}
        QPushButton:disabled {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.12)};
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_filled_tonal_style(self):
        """Style bouton rempli tonal"""
        style = f"""
        QPushButton {{
            background-color: {self.theme.secondary_container};
            color: {self.theme.on_secondary_container};
            border: none;
            border-radius: {MaterialShape.FULL.value}px;
            padding: 10px 24px;
            font-weight: 500;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.secondary_container, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.secondary_container, 0.12)};
        }}
        QPushButton:disabled {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.12)};
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
        }}
        """
        self.setStyleSheet(style)
    
    def _adjust_color(self, color: str, opacity: float) -> str:
        """Ajuste la couleur avec une opacité"""
        qcolor = QColor(color)
        qcolor.setAlphaF(opacity)
        return qcolor.name(QColor.NameFormat.HexArgb)
    
    def _on_pressed(self):
        """Animation lors du clic"""
        if self.button_style == self.Style.ELEVATED:
            self.elevation_animation.setStartValue(self._elevation)
            self.elevation_animation.setEndValue(1)
            self.elevation_animation.start()
    
    def _on_released(self):
        """Animation lors du relâchement"""
        if self.button_style == self.Style.ELEVATED:
            self.elevation_animation.setStartValue(self._elevation)
            self.elevation_animation.setEndValue(3)
            self.elevation_animation.start()
    
    def _on_enter(self, event):
        """Animation lors de l'entrée de la souris"""
        if self.button_style == self.Style.ELEVATED:
            self.elevation_animation.setStartValue(self._elevation)
            self.elevation_animation.setEndValue(3)
            self.elevation_animation.start()
        super().enterEvent(event)
    
    def _on_leave(self, event):
        """Animation lors de la sortie de la souris"""
        if self.button_style == self.Style.ELEVATED:
            self.elevation_animation.setStartValue(self._elevation)
            self.elevation_animation.setEndValue(1)
            self.elevation_animation.start()
        super().leaveEvent(event)
    
    def set_style(self, style: Style):
        """Change le style du bouton"""
        self.button_style = style
        self.apply_style()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_style()