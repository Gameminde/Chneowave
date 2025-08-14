#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Chips
Composants de chips Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from enum import Enum
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor

from .theme import MaterialTheme, MaterialShape


class MaterialChip(QPushButton):
    """Chip Material Design 3"""
    
    class Type(Enum):
        """Types de chip Material Design 3"""
        ASSIST = "assist"
        FILTER = "filter"
        INPUT = "input"
        SUGGESTION = "suggestion"
    
    # Signaux personnalisés
    closeRequested = Signal()  # Pour les chips input
    
    def __init__(self, text: str = "", chip_type: Type = Type.ASSIST, 
                 icon: QIcon = None, closable: bool = False, parent=None):
        super().__init__(text, parent)
        self.chip_type = chip_type
        self.theme = MaterialTheme()
        self._selected = False
        self._closable = closable
        self._icon = icon
        
        # Configuration de base
        self.setCheckable(chip_type == self.Type.FILTER)
        self.setMinimumHeight(32)
        
        self.apply_style()
        
        # Connexions
        if self.isCheckable():
            self.toggled.connect(self._on_toggled)
        
        if closable:
            self.clicked.connect(self._on_close_clicked)
    
    def apply_style(self):
        """Applique le style selon le type de chip"""
        if self.chip_type == self.Type.ASSIST:
            self._apply_assist_style()
        elif self.chip_type == self.Type.FILTER:
            self._apply_filter_style()
        elif self.chip_type == self.Type.INPUT:
            self._apply_input_style()
        elif self.chip_type == self.Type.SUGGESTION:
            self._apply_suggestion_style()
    
    def _apply_assist_style(self):
        """Style chip d'assistance"""
        style = f"""
        QPushButton {{
            background-color: {self.theme.surface};
            color: {self.theme.on_surface};
            border: 1px solid {self.theme.outline};
            border-radius: {MaterialShape.SMALL.value}px;
            padding: 6px 16px;
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.12)};
        }}
        QPushButton:disabled {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.12)};
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
            border-color: {self._adjust_color(self.theme.on_surface, 0.12)};
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_filter_style(self):
        """Style chip de filtre"""
        if self._selected or self.isChecked():
            bg_color = self.theme.secondary_container
            text_color = self.theme.on_secondary_container
            border_color = self.theme.secondary_container
        else:
            bg_color = "transparent"
            text_color = self.theme.on_surface_variant
            border_color = self.theme.outline
        
        style = f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border: 1px solid {border_color};
            border-radius: {MaterialShape.SMALL.value}px;
            padding: 6px 16px;
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(text_color, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(text_color, 0.12)};
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_input_style(self):
        """Style chip d'entrée"""
        style = f"""
        QPushButton {{
            background-color: {self.theme.surface_variant};
            color: {self.theme.on_surface_variant};
            border: none;
            border-radius: {MaterialShape.SMALL.value}px;
            padding: 6px 16px;
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.on_surface_variant, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.on_surface_variant, 0.12)};
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_suggestion_style(self):
        """Style chip de suggestion"""
        style = f"""
        QPushButton {{
            background-color: {self.theme.surface};
            color: {self.theme.on_surface_variant};
            border: 1px solid {self.theme.outline};
            border-radius: {MaterialShape.SMALL.value}px;
            padding: 6px 16px;
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.on_surface_variant, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.on_surface_variant, 0.12)};
        }}
        """
        self.setStyleSheet(style)
    
    def _adjust_color(self, color: str, opacity: float) -> str:
        """Ajuste la couleur avec une opacité"""
        qcolor = QColor(color)
        qcolor.setAlphaF(opacity)
        return qcolor.name(QColor.NameFormat.HexArgb)
    
    def _on_toggled(self, checked: bool):
        """Gère le changement d'état pour les chips filtre"""
        self._selected = checked
        self.apply_style()
    
    def _on_close_clicked(self):
        """Gère le clic de fermeture pour les chips input"""
        if self._closable:
            self.closeRequested.emit()
    
    def set_selected(self, selected: bool):
        """Définit l'état sélectionné"""
        self._selected = selected
        if self.isCheckable():
            self.setChecked(selected)
        self.apply_style()
    
    def is_selected(self) -> bool:
        """Retourne l'état sélectionné"""
        if self.isCheckable():
            return self.isChecked()
        return self._selected
    
    def set_icon(self, icon: QIcon):
        """Définit l'icône du chip"""
        self._icon = icon
        self.setIcon(icon)
    
    def set_closable(self, closable: bool):
        """Définit si le chip peut être fermé"""
        self._closable = closable
        # Ajouter une icône de fermeture si nécessaire
        if closable and self.chip_type == self.Type.INPUT:
            # Créer une icône de fermeture simple
            close_icon = self._create_close_icon()
            self.setIcon(close_icon)
    
    def _create_close_icon(self) -> QIcon:
        """Crée une icône de fermeture simple"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dessiner une croix
        pen = painter.pen()
        pen.setColor(QColor(self.theme.on_surface_variant))
        pen.setWidth(2)
        painter.setPen(pen)
        
        painter.drawLine(4, 4, 12, 12)
        painter.drawLine(12, 4, 4, 12)
        
        painter.end()
        
        return QIcon(pixmap)
    
    def set_type(self, chip_type: Type):
        """Change le type de chip"""
        self.chip_type = chip_type
        self.setCheckable(chip_type == self.Type.FILTER)
        self.apply_style()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_style()
        
        # Recréer l'icône de fermeture si nécessaire
        if self._closable and self.chip_type == self.Type.INPUT:
            close_icon = self._create_close_icon()
            self.setIcon(close_icon)