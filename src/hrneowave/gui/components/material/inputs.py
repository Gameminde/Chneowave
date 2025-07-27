#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Inputs
Composants d'entrée Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from enum import Enum
from PySide6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal, QRect
from PySide6.QtGui import QColor, QPainter, QPen

from .theme import MaterialTheme, MaterialAnimations, MaterialShape


class MaterialTextField(QWidget):
    """Champ de texte Material Design 3"""
    
    class Style(Enum):
        """Styles de champ de texte"""
        FILLED = "filled"
        OUTLINED = "outlined"
    
    textChanged = Signal(str)
    textEdited = Signal(str)
    returnPressed = Signal()
    
    def __init__(self, label: str = "", style: Style = Style.OUTLINED, parent=None):
        super().__init__(parent)
        self.field_style = style
        self.theme = MaterialTheme()
        self._label_text = label
        self._is_focused = False
        self._has_text = False
        
        self._setup_ui()
        self._setup_animations()
        self.apply_style()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 8, 0, 8)
        self.layout.setSpacing(4)
        
        # Label flottant
        self.label = QLabel(self._label_text)
        self.label.setObjectName("floating_label")
        
        # Champ de texte
        self.line_edit = QLineEdit()
        self.line_edit.setObjectName("text_field")
        
        # Connexions
        self.line_edit.textChanged.connect(self._on_text_changed)
        self.line_edit.textEdited.connect(self.textEdited.emit)
        self.line_edit.returnPressed.connect(self.returnPressed.emit)
        self.line_edit.focusInEvent = self._on_focus_in
        self.line_edit.focusOutEvent = self._on_focus_out
        
        if self.field_style == self.Style.FILLED:
            self.layout.addWidget(self.line_edit)
            self.layout.addWidget(self.label)
        else:  # OUTLINED
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.line_edit)
    
    def _setup_animations(self):
        """Configure les animations"""
        # Animation du label
        self.label_animation = QPropertyAnimation(self.label, b"geometry")
        self.label_animation.setDuration(MaterialAnimations.get_slide_duration())
        self.label_animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
        
        # Animation de la couleur de focus
        self.focus_animation = QPropertyAnimation(self, b"focusColor")
        self.focus_animation.setDuration(MaterialAnimations.get_fade_duration())
        self.focus_animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
    
    def apply_style(self):
        """Applique le style selon le type de champ"""
        if self.field_style == self.Style.FILLED:
            self._apply_filled_style()
        else:  # OUTLINED
            self._apply_outlined_style()
    
    def _apply_filled_style(self):
        """Style champ rempli"""
        style = f"""
        QLineEdit#text_field {{
            background-color: {self.theme.surface_variant};
            color: {self.theme.on_surface};
            border: none;
            border-bottom: 2px solid {self.theme.outline};
            border-radius: {MaterialShape.SMALL.value}px {MaterialShape.SMALL.value}px 0px 0px;
            padding: 16px 12px 8px 12px;
            font-size: 16px;
        }}
        QLineEdit#text_field:focus {{
            border-bottom: 2px solid {self.theme.primary};
            background-color: {self._adjust_color(self.theme.surface_variant, 0.12)};
        }}
        QLineEdit#text_field:disabled {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.04)};
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
            border-bottom: 1px solid {self._adjust_color(self.theme.on_surface, 0.38)};
        }}
        QLabel#floating_label {{
            color: {self.theme.on_surface_variant};
            font-size: 12px;
            padding: 0px 12px;
        }}
        """
        self.setStyleSheet(style)
    
    def _apply_outlined_style(self):
        """Style champ contouré"""
        border_color = self.theme.primary if self._is_focused else self.theme.outline
        border_width = "2px" if self._is_focused else "1px"
        
        style = f"""
        QLineEdit#text_field {{
            background-color: transparent;
            color: {self.theme.on_surface};
            border: {border_width} solid {border_color};
            border-radius: {MaterialShape.SMALL.value}px;
            padding: 16px 12px;
            font-size: 16px;
        }}
        QLineEdit#text_field:disabled {{
            color: {self._adjust_color(self.theme.on_surface, 0.38)};
            border: 1px solid {self._adjust_color(self.theme.on_surface, 0.38)};
        }}
        QLabel#floating_label {{
            color: {self.theme.primary if self._is_focused else self.theme.on_surface_variant};
            font-size: {'12px' if self._is_focused or self._has_text else '16px'};
            background-color: {self.theme.surface};
            padding: 0px 4px;
        }}
        """
        self.setStyleSheet(style)
    
    def _adjust_color(self, color: str, opacity: float) -> str:
        """Ajuste la couleur avec une opacité"""
        qcolor = QColor(color)
        qcolor.setAlphaF(opacity)
        return qcolor.name(QColor.NameFormat.HexArgb)
    
    def _on_text_changed(self, text: str):
        """Gère le changement de texte"""
        self._has_text = bool(text.strip())
        self._animate_label()
        self.textChanged.emit(text)
    
    def _on_focus_in(self, event):
        """Gère l'obtention du focus"""
        self._is_focused = True
        self._animate_label()
        self.apply_style()
        super(QLineEdit, self.line_edit).focusInEvent(event)
    
    def _on_focus_out(self, event):
        """Gère la perte du focus"""
        self._is_focused = False
        self._animate_label()
        self.apply_style()
        super(QLineEdit, self.line_edit).focusOutEvent(event)
    
    def _animate_label(self):
        """Anime le label flottant"""
        if self.field_style == self.Style.OUTLINED:
            current_rect = self.label.geometry()
            
            if self._is_focused or self._has_text:
                # Label en position haute
                new_rect = QRect(
                    12, -8,
                    current_rect.width(),
                    16
                )
            else:
                # Label en position normale
                new_rect = QRect(
                    12, 16,
                    current_rect.width(),
                    20
                )
            
            self.label_animation.setStartValue(current_rect)
            self.label_animation.setEndValue(new_rect)
            self.label_animation.start()
    
    def text(self) -> str:
        """Retourne le texte du champ"""
        return self.line_edit.text()
    
    def setText(self, text: str):
        """Définit le texte du champ"""
        self.line_edit.setText(text)
    
    def setPlaceholderText(self, text: str):
        """Définit le texte d'aide"""
        self.line_edit.setPlaceholderText(text)
    
    def setReadOnly(self, read_only: bool):
        """Définit le mode lecture seule"""
        self.line_edit.setReadOnly(read_only)
    
    def setEnabled(self, enabled: bool):
        """Active/désactive le champ"""
        super().setEnabled(enabled)
        self.line_edit.setEnabled(enabled)
        self.apply_style()
    
    def setLabel(self, label: str):
        """Définit le texte du label"""
        self._label_text = label
        self.label.setText(label)
    
    def setStyle(self, style: Style):
        """Change le style du champ"""
        self.field_style = style
        self.apply_style()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_style()
    
    def clear(self):
        """Efface le contenu du champ"""
        self.line_edit.clear()
    
    def selectAll(self):
        """Sélectionne tout le texte"""
        self.line_edit.selectAll()
    
    def setFocus(self):
        """Donne le focus au champ"""
        self.line_edit.setFocus()