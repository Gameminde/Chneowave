#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Feedback
Composants de feedback Material Design 3 (Toast, Switch)

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from enum import Enum
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import QTimer, Signal, Qt, QPropertyAnimation, QEasingCurve, QRect, Property
from PySide6.QtGui import QPainter, QColor, QBrush

from .theme import MaterialTheme, MaterialShape, MaterialAnimations


class MaterialToast(QWidget):
    """Toast notification Material Design 3"""
    
    class Type(Enum):
        """Types de toast"""
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"
    
    def __init__(self, message: str, toast_type: Type = Type.INFO, 
                 duration: int = 3000, parent=None):
        super().__init__(parent)
        self.message = message
        self.toast_type = toast_type
        self.duration = duration
        self.theme = MaterialTheme()
        
        self._setup_ui()
        self._setup_timer()
        self.apply_theme()
        
        # Positionnement
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Animation d'apparition
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(MaterialAnimations.get_fade_duration())
        self.fade_animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(16, 12, 16, 12)
        self.layout.setSpacing(8)
        
        # Message
        self.label = QLabel(self.message)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)
        
        # Bouton de fermeture optionnel
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(24, 24)
        self.close_button.clicked.connect(self.hide)
        self.layout.addWidget(self.close_button)
        
        # Taille minimale
        self.setMinimumWidth(288)
        self.setMaximumWidth(568)
    
    def _setup_timer(self):
        """Configure le timer pour la fermeture automatique"""
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._fade_out)
    
    def apply_theme(self):
        """Applique le thème selon le type de toast"""
        if self.toast_type == self.Type.INFO:
            bg_color = self.theme.surface_variant
            text_color = self.theme.on_surface_variant
        elif self.toast_type == self.Type.SUCCESS:
            bg_color = "#4CAF50"  # Vert
            text_color = "#FFFFFF"
        elif self.toast_type == self.Type.WARNING:
            bg_color = "#FF9800"  # Orange
            text_color = "#FFFFFF"
        elif self.toast_type == self.Type.ERROR:
            bg_color = self.theme.error
            text_color = self.theme.on_error
        else:
            bg_color = self.theme.surface
            text_color = self.theme.on_surface
        
        style = f"""
        QWidget {{
            background-color: {bg_color};
            border-radius: {MaterialShape.SMALL.value}px;
        }}
        QLabel {{
            color: {text_color};
            font-size: 14px;
            background-color: transparent;
        }}
        QPushButton {{
            background-color: transparent;
            color: {text_color};
            border: none;
            font-weight: bold;
        }}
        """
        self.setStyleSheet(style)
    
    def show_toast(self):
        """Affiche le toast avec animation"""
        self.setWindowOpacity(0.0)
        self.show()
        
        # Animation d'apparition
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
        
        # Démarrer le timer si une durée est définie
        if self.duration > 0:
            self.timer.start(self.duration)
    
    def _fade_out(self):
        """Animation de disparition"""
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()


class MaterialSwitch(QWidget):
    """Switch Material Design 3"""
    
    toggled = Signal(bool)
    
    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self.theme = MaterialTheme()
        self._thumb_position = 0.0
        
        self.setFixedSize(52, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Animation du thumb
        self.thumb_animation = QPropertyAnimation(self, b"thumbPosition")
        self.thumb_animation.setDuration(MaterialAnimations.get_slide_duration())
        self.thumb_animation.setEasingCurve(MaterialAnimations.EASING_STANDARD)
        
        self.apply_theme()
        self._update_thumb_position()
    
    def get_thumb_position(self) -> float:
        """Getter pour la position du thumb"""
        return self._thumb_position
    
    def set_thumb_position(self, position: float):
        """Setter pour la position du thumb"""
        self._thumb_position = position
        self.update()
    
    thumbPosition = Property(float, get_thumb_position, set_thumb_position)
    
    def is_checked(self) -> bool:
        """Retourne l'état du switch"""
        return self._checked
    
    def set_checked(self, checked: bool, animate: bool = True):
        """Définit l'état du switch"""
        if self._checked != checked:
            self._checked = checked
            self.toggled.emit(checked)
            
            if animate:
                self._animate_thumb()
            else:
                self._update_thumb_position()
            
            self.update()
    
    def _update_thumb_position(self):
        """Met à jour la position du thumb sans animation"""
        self._thumb_position = 1.0 if self._checked else 0.0
        self.update()
    
    def _animate_thumb(self):
        """Anime le mouvement du thumb"""
        start_pos = self._thumb_position
        end_pos = 1.0 if self._checked else 0.0
        
        self.thumb_animation.setStartValue(start_pos)
        self.thumb_animation.setEndValue(end_pos)
        self.thumb_animation.start()
    
    def mousePressEvent(self, event):
        """Gère le clic"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_checked(not self._checked)
    
    def paintEvent(self, event):
        """Dessine le switch"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Couleurs selon l'état
        if self._checked:
            track_color = QColor(self.theme.primary)
            thumb_color = QColor(self.theme.on_primary)
        else:
            track_color = QColor(self.theme.outline)
            thumb_color = QColor(self.theme.outline_variant)
        
        # Track (rail)
        track_rect = QRect(6, 12, 40, 8)
        painter.setBrush(QBrush(track_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(track_rect, 4, 4)
        
        # Thumb (bouton) - position animée
        thumb_x = int(6 + (26 * self._thumb_position))  # 6 à 32
        thumb_rect = QRect(thumb_x, 6, 20, 20)
        painter.setBrush(QBrush(thumb_color))
        painter.drawEllipse(thumb_rect)
    
    def apply_theme(self):
        """Applique le thème"""
        self.update()
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_theme()
    
    def toggle(self):
        """Inverse l'état du switch"""
        self.set_checked(not self._checked)


# Classe de compatibilité pour l'ancien nom
class ToastNotification(MaterialToast):
    """Alias pour compatibilité avec l'ancien code"""
    pass