#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Progress
Composants de progression Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from enum import Enum
from PySide6.QtWidgets import QProgressBar, QWidget
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, Property
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from .theme import MaterialTheme, MaterialAnimations, MaterialShape


class MaterialProgressBar(QProgressBar):
    """Barre de progression Material Design 3"""
    
    class Type(Enum):
        """Types de barre de progression"""
        LINEAR = "linear"
        CIRCULAR = "circular"
    
    def __init__(self, progress_type: Type = Type.LINEAR, parent=None):
        super().__init__(parent)
        self.progress_type = progress_type
        self.theme = MaterialTheme()
        self._animated_value = 0
        
        # Configuration de base
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        
        if progress_type == self.Type.LINEAR:
            self.setMinimumHeight(4)
            self.setMaximumHeight(4)
        else:
            self.setFixedSize(48, 48)
        
        # Animation de la valeur
        self.value_animation = QPropertyAnimation(self, b"animatedValue")
        self.value_animation.setDuration(MaterialAnimations.get_slide_duration())
        self.value_animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
        
        # Animation indéterminée
        self.indeterminate_animation = QPropertyAnimation(self, b"animatedValue")
        self.indeterminate_animation.setDuration(2000)
        self.indeterminate_animation.setEasingCurve(MaterialAnimations.EASING_LINEAR)
        self.indeterminate_animation.setLoopCount(-1)  # Boucle infinie
        
        self.apply_style()
    
    def get_animated_value(self) -> float:
        """Getter pour la valeur animée"""
        return self._animated_value
    
    def set_animated_value(self, value: float):
        """Setter pour la valeur animée"""
        self._animated_value = value
        self.update()
    
    animatedValue = Property(float, get_animated_value, set_animated_value)
    
    def apply_style(self):
        """Applique le style selon le type de progression"""
        if self.progress_type == self.Type.LINEAR:
            self._apply_linear_style()
        else:
            self._apply_circular_style()
    
    def _apply_linear_style(self):
        """Style barre de progression linéaire"""
        style = f"""
        QProgressBar {{
            background-color: {self.theme.surface_variant};
            border: none;
            border-radius: {MaterialShape.EXTRA_SMALL.value // 2}px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: {self.theme.primary};
            border-radius: {MaterialShape.EXTRA_SMALL.value // 2}px;
        }}
        """
        self.setStyleSheet(style)
        self.setTextVisible(False)
    
    def _apply_circular_style(self):
        """Style barre de progression circulaire"""
        # Pour les barres circulaires, on utilise un paintEvent personnalisé
        self.setStyleSheet("""
        QProgressBar {
            background-color: transparent;
            border: none;
        }
        """)
        self.setTextVisible(False)
    
    def paintEvent(self, event):
        """Dessine la barre de progression"""
        if self.progress_type == self.Type.CIRCULAR:
            self._paint_circular_progress()
        else:
            super().paintEvent(event)
    
    def _paint_circular_progress(self):
        """Dessine une barre de progression circulaire"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensions
        width = self.width()
        height = self.height()
        size = min(width, height) - 8
        x = (width - size) // 2
        y = (height - size) // 2
        
        # Couleurs
        track_color = QColor(self.theme.surface_variant)
        progress_color = QColor(self.theme.primary)
        
        # Épaisseur de la ligne
        line_width = 4
        
        # Dessiner le track (fond)
        painter.setPen(QPen(track_color, line_width))
        painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        painter.drawEllipse(x, y, size, size)
        
        # Dessiner le progrès
        if not self.isIndeterminate():
            # Mode déterminé
            progress_angle = int((self.value() / self.maximum()) * 360 * 16)  # Qt utilise 1/16 de degré
            painter.setPen(QPen(progress_color, line_width))
            painter.drawArc(x, y, size, size, 90 * 16, -progress_angle)  # Commence en haut
        else:
            # Mode indéterminé - arc qui tourne
            arc_length = 90 * 16  # 90 degrés
            start_angle = int(self._animated_value * 360 * 16) % (360 * 16)
            painter.setPen(QPen(progress_color, line_width))
            painter.drawArc(x, y, size, size, start_angle, arc_length)
    
    def setValue(self, value: int):
        """Définit la valeur avec animation"""
        if value != self.value():
            self.value_animation.setStartValue(self.value())
            self.value_animation.setEndValue(value)
            self.value_animation.finished.connect(lambda: super(MaterialProgressBar, self).setValue(value))
            self.value_animation.start()
    
    def setIndeterminate(self, indeterminate: bool):
        """Active/désactive le mode indéterminé"""
        if indeterminate:
            self.indeterminate_animation.setStartValue(0)
            self.indeterminate_animation.setEndValue(1)
            self.indeterminate_animation.start()
        else:
            self.indeterminate_animation.stop()
            self._animated_value = 0
            self.update()
    
    def isIndeterminate(self) -> bool:
        """Retourne si le mode indéterminé est actif"""
        return self.indeterminate_animation.state() == QPropertyAnimation.State.Running
    
    def set_type(self, progress_type: Type):
        """Change le type de progression"""
        self.progress_type = progress_type
        
        if progress_type == self.Type.LINEAR:
            self.setMinimumHeight(4)
            self.setMaximumHeight(4)
            self.setFixedSize(self.parent().width() if self.parent() else 200, 4)
        else:
            self.setFixedSize(48, 48)
        
        self.apply_style()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_style()
    
    def start_indeterminate(self):
        """Démarre l'animation indéterminée"""
        self.setIndeterminate(True)
    
    def stop_indeterminate(self):
        """Arrête l'animation indéterminée"""
        self.setIndeterminate(False)
    
    def set_color(self, color: str):
        """Définit une couleur personnalisée pour la progression"""
        # Temporairement modifier le thème pour cette couleur
        original_primary = self.theme.primary
        self.theme.primary = color
        self.apply_style()
        # Restaurer la couleur originale après un court délai
        QTimer.singleShot(100, lambda: setattr(self.theme, 'primary', original_primary))