# -*- coding: utf-8 -*-
"""
Composant AnimatedButton - Bouton animé avec design maritime
Utilise des animations fluides et le thème maritime

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, Signal, Property
from PySide6.QtGui import QFont, QPainter, QLinearGradient, QColor, QPalette


class AnimatedButton(QPushButton):
    """
    Bouton animé avec design maritime moderne
    """
    
    # Signaux personnalisés
    hoverEntered = Signal()
    hoverLeft = Signal()
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        
        # Configuration de base
        self.setObjectName("animatedButton")
        self.setCursor(Qt.PointingHandCursor)
        
        # Propriétés d'animation
        self._hover_scale = 1.0
        self._press_scale = 1.0
        self._opacity = 1.0
        
        # Animations
        self._setup_animations()
        
        # Style de base
        self._apply_base_style()
    
    def _setup_animations(self):
        """Configuration des animations"""
        # Animation de survol
        self.hover_animation = QPropertyAnimation(self, b"hover_scale")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animation de pression
        self.press_animation = QPropertyAnimation(self, b"press_scale")
        self.press_animation.setDuration(100)
        self.press_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animation d'opacité
        self.opacity_animation = QPropertyAnimation(self, b"opacity")
        self.opacity_animation.setDuration(150)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def _apply_base_style(self):
        """Applique le style de base"""
        self.setStyleSheet("""
            #animatedButton {
                background-color: #2c5aa0;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
                min-height: 36px;
            }
            
            #animatedButton:hover {
                background-color: #1e3d72;
            }
            
            #animatedButton:pressed {
                background-color: #163056;
            }
            
            #animatedButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
    
    # Propriétés pour les animations avec décorateurs Qt
    def get_hover_scale(self):
        return self._hover_scale
    
    def set_hover_scale(self, scale):
        self._hover_scale = scale
        self.update()
    
    hover_scale = Property(float, get_hover_scale, set_hover_scale)
    
    def get_press_scale(self):
        return self._press_scale
    
    def set_press_scale(self, scale):
        self._press_scale = scale
        self.update()
    
    press_scale = Property(float, get_press_scale, set_press_scale)
    
    def get_opacity(self):
        return self._opacity
    
    def set_opacity(self, opacity):
        self._opacity = opacity
        self.update()
    
    opacity = Property(float, get_opacity, set_opacity)
    
    def enterEvent(self, event):
        """Événement d'entrée de la souris"""
        if self.isEnabled():
            self.hover_animation.setStartValue(1.0)
            self.hover_animation.setEndValue(1.05)
            self.hover_animation.start()
            self.hoverEntered.emit()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Événement de sortie de la souris"""
        if self.isEnabled():
            self.hover_animation.setStartValue(1.05)
            self.hover_animation.setEndValue(1.0)
            self.hover_animation.start()
            self.hoverLeft.emit()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Événement de pression de la souris"""
        if self.isEnabled() and event.button() == Qt.LeftButton:
            self.press_animation.setStartValue(1.0)
            self.press_animation.setEndValue(0.95)
            self.press_animation.start()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Événement de relâchement de la souris"""
        if self.isEnabled() and event.button() == Qt.LeftButton:
            self.press_animation.setStartValue(0.95)
            self.press_animation.setEndValue(1.0)
            self.press_animation.start()
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        """Événement de peinture personnalisé"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Appliquer les transformations
        rect = self.rect()
        center = rect.center()
        
        painter.translate(center)
        painter.scale(self._hover_scale * self._press_scale, self._hover_scale * self._press_scale)
        painter.translate(-center)
        
        # Appliquer l'opacité
        painter.setOpacity(self._opacity)
        
        # Dessiner le bouton normal
        super().paintEvent(event)
    
    def animate_click(self):
        """Animation de clic programmé"""
        # Animation de pression puis relâchement
        press_anim = QPropertyAnimation(self, b"press_scale")
        press_anim.setDuration(100)
        press_anim.setStartValue(1.0)
        press_anim.setEndValue(0.95)
        press_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        release_anim = QPropertyAnimation(self, b"press_scale")
        release_anim.setDuration(100)
        release_anim.setStartValue(0.95)
        release_anim.setEndValue(1.0)
        release_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Séquence d'animations
        self.click_sequence = QParallelAnimationGroup()
        press_anim.finished.connect(release_anim.start)
        
        press_anim.start()
    
    def animate_success(self):
        """Animation de succès"""
        # Changement temporaire de couleur
        original_style = self.styleSheet()
        
        success_style = """
            #animatedButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
                min-height: 36px;
            }
        """
        
        self.setStyleSheet(success_style)
        
        # Animation de pulsation
        pulse_anim = QPropertyAnimation(self, b"hover_scale")
        pulse_anim.setDuration(300)
        pulse_anim.setStartValue(1.0)
        pulse_anim.setEndValue(1.1)
        pulse_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Retour au style original après l'animation
        def restore_style():
            self.setStyleSheet(original_style)
            self.hover_scale = 1.0
        
        pulse_anim.finished.connect(restore_style)
        pulse_anim.start()
    
    def animate_error(self):
        """Animation d'erreur"""
        # Changement temporaire de couleur
        original_style = self.styleSheet()
        
        error_style = """
            #animatedButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
                min-height: 36px;
            }
        """
        
        self.setStyleSheet(error_style)
        
        # Animation de secousse
        shake_anim = QPropertyAnimation(self, b"pos")
        shake_anim.setDuration(200)
        original_pos = self.pos()
        
        # Séquence de secousse
        positions = [
            original_pos,
            original_pos + self.rect().topLeft() + self.rect().center() * 0.02,
            original_pos - self.rect().topLeft() - self.rect().center() * 0.02,
            original_pos
        ]
        
        # Retour au style original après l'animation
        def restore_style():
            self.setStyleSheet(original_style)
            self.move(original_pos)
        
        shake_anim.finished.connect(restore_style)
    
    def set_loading(self, loading=True):
        """Active/désactive l'état de chargement"""
        if loading:
            self.setEnabled(False)
            self.setText("Chargement...")
            
            # Animation de pulsation continue
            self.loading_animation = QPropertyAnimation(self, b"opacity")
            self.loading_animation.setDuration(1000)
            self.loading_animation.setStartValue(0.6)
            self.loading_animation.setEndValue(1.0)
            self.loading_animation.setEasingCurve(QEasingCurve.InOutSine)
            self.loading_animation.setLoopCount(-1)  # Infini
            self.loading_animation.start()
        else:
            self.setEnabled(True)
            if hasattr(self, 'loading_animation'):
                self.loading_animation.stop()
            self.opacity = 1.0
    
    def set_primary_style(self):
        """Applique le style primaire"""
        self.setObjectName("primaryButton")
        self.setStyleSheet("""
            #primaryButton {
                background-color: #2c5aa0;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
                min-height: 36px;
            }
            
            #primaryButton:hover {
                background-color: #1e3d72;
            }
            
            #primaryButton:pressed {
                background-color: #163056;
            }
            
            #primaryButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
    
    def set_secondary_style(self):
        """Applique le style secondaire"""
        self.setObjectName("secondaryButton")
        self.setStyleSheet("""
            #secondaryButton {
                background-color: #ffffff;
                color: #2c5aa0;
                border: 2px solid #2c5aa0;
                border-radius: 8px;
                padding: 10px 22px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
                min-height: 36px;
            }
            
            #secondaryButton:hover {
                background-color: #f8f9fa;
                border-color: #1e3d72;
                color: #1e3d72;
            }
            
            #secondaryButton:pressed {
                background-color: #e9ecef;
            }
            
            #secondaryButton:disabled {
                background-color: #f8f9fa;
                border-color: #cccccc;
                color: #666666;
            }
        """)
    
    def set_warning_style(self):
        """Applique le style d'avertissement"""
        self.setObjectName("warningButton")
        self.setStyleSheet("""
            #warningButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
                min-height: 36px;
            }
            
            #warningButton:hover {
                background-color: #e0a800;
            }
            
            #warningButton:pressed {
                background-color: #d39e00;
            }
            
            #warningButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)