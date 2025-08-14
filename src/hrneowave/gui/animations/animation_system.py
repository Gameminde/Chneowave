# -*- coding: utf-8 -*-
"""
Système d'animations modernes pour CHNeoWave
Phase 6 : Animations et micro-interactions fluides
"""

import logging
from typing import Dict, Any, Optional, Callable
from enum import Enum

try:
    from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, QTimer, Signal, QRect, QPoint, QSize
    from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
    from PySide6.QtGui import QColor
except ImportError:
    try:
        from PyQt6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, QTimer, pyqtSignal as Signal, QRect, QPoint, QSize
        from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
        from PyQt6.QtGui import QColor
    except ImportError:
        from PyQt5.QtCore import QObject, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, QTimer, pyqtSignal as Signal, QRect, QPoint, QSize
        from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
        from PyQt5.QtGui import QColor

logger = logging.getLogger(__name__)

class AnimationType(Enum):
    """Types d'animations disponibles"""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    SLIDE_IN_LEFT = "slide_in_left"
    SLIDE_IN_RIGHT = "slide_in_right"
    SLIDE_IN_UP = "slide_in_up"
    SLIDE_IN_DOWN = "slide_in_down"
    SCALE_IN = "scale_in"
    SCALE_OUT = "scale_out"
    BOUNCE_IN = "bounce_in"
    ELASTIC_IN = "elastic_in"
    HOVER_LIFT = "hover_lift"
    BUTTON_PRESS = "button_press"
    CARD_FLIP = "card_flip"
    LOADING_PULSE = "loading_pulse"
    SUCCESS_GLOW = "success_glow"
    ERROR_SHAKE = "error_shake"

class AnimationPreset:
    """Préréglages d'animations maritimes"""
    
    # Durées en millisecondes
    DURATION_FAST = 150
    DURATION_NORMAL = 300
    DURATION_SLOW = 500
    DURATION_VERY_SLOW = 800
    
    # Courbes d'accélération Material Design
    EASE_STANDARD = QEasingCurve.Type.OutCubic
    EASE_DECELERATE = QEasingCurve.Type.OutQuart
    EASE_ACCELERATE = QEasingCurve.Type.InQuart
    EASE_SHARP = QEasingCurve.Type.InOutQuart
    EASE_BOUNCE = QEasingCurve.Type.OutBounce
    EASE_ELASTIC = QEasingCurve.Type.OutElastic
    
    # Animations de navigation
    PAGE_TRANSITION = {
        'duration': DURATION_NORMAL,
        'easing': EASE_STANDARD
    }
    
    # Animations de boutons
    BUTTON_HOVER = {
        'duration': DURATION_FAST,
        'easing': EASE_DECELERATE,
        'scale': 1.02
    }
    
    BUTTON_PRESS = {
        'duration': 100,
        'easing': EASE_SHARP,
        'scale': 0.98
    }
    
    # Animations de cartes
    CARD_HOVER = {
        'duration': DURATION_NORMAL,
        'easing': EASE_DECELERATE,
        'lift': 8
    }
    
    # Animations de feedback
    SUCCESS_FEEDBACK = {
        'duration': DURATION_SLOW,
        'easing': EASE_BOUNCE,
        'color': '#10b981'
    }
    
    ERROR_FEEDBACK = {
        'duration': DURATION_NORMAL,
        'easing': EASE_SHARP,
        'color': '#ef4444'
    }

class MaritimeAnimator(QObject):
    """Gestionnaire d'animations maritimes modernes"""
    
    animation_finished = Signal(str)  # Signal émis quand une animation se termine
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_animations: Dict[str, QPropertyAnimation] = {}
        self.animation_groups: Dict[str, QParallelAnimationGroup] = {}
        
    def fade_in(self, widget: QWidget, duration: int = AnimationPreset.DURATION_NORMAL, 
                callback: Optional[Callable] = None) -> str:
        """Animation de fondu entrant"""
        animation_id = f"fade_in_{id(widget)}"
        
        # Créer l'effet d'opacité si nécessaire
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
        
        effect = widget.graphicsEffect()
        effect.setOpacity(0.0)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(AnimationPreset.EASE_DECELERATE)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.finished.connect(lambda: self.animation_finished.emit(animation_id))
        
        self.active_animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def fade_out(self, widget: QWidget, duration: int = AnimationPreset.DURATION_NORMAL,
                 callback: Optional[Callable] = None) -> str:
        """Animation de fondu sortant"""
        animation_id = f"fade_out_{id(widget)}"
        
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
        
        effect = widget.graphicsEffect()
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(AnimationPreset.EASE_ACCELERATE)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.finished.connect(lambda: self.animation_finished.emit(animation_id))
        
        self.active_animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def slide_in(self, widget: QWidget, direction: str = "left", 
                 duration: int = AnimationPreset.DURATION_NORMAL,
                 callback: Optional[Callable] = None) -> str:
        """Animation de glissement entrant"""
        animation_id = f"slide_in_{direction}_{id(widget)}"
        
        # Calculer les positions de départ et d'arrivée
        final_geometry = widget.geometry()
        
        if direction == "left":
            start_geometry = QRect(-final_geometry.width(), final_geometry.y(), 
                                 final_geometry.width(), final_geometry.height())
        elif direction == "right":
            start_geometry = QRect(widget.parent().width(), final_geometry.y(),
                                 final_geometry.width(), final_geometry.height())
        elif direction == "up":
            start_geometry = QRect(final_geometry.x(), -final_geometry.height(),
                                 final_geometry.width(), final_geometry.height())
        else:  # down
            start_geometry = QRect(final_geometry.x(), widget.parent().height(),
                                 final_geometry.width(), final_geometry.height())
        
        widget.setGeometry(start_geometry)
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_geometry)
        animation.setEndValue(final_geometry)
        animation.setEasingCurve(AnimationPreset.EASE_DECELERATE)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.finished.connect(lambda: self.animation_finished.emit(animation_id))
        
        self.active_animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def scale_animation(self, widget: QWidget, scale_factor: float = 1.02,
                       duration: int = AnimationPreset.DURATION_FAST,
                       callback: Optional[Callable] = None) -> str:
        """Animation de mise à l'échelle (hover effect)"""
        animation_id = f"scale_{id(widget)}"
        
        original_size = widget.size()
        target_size = QSize(int(original_size.width() * scale_factor),
                           int(original_size.height() * scale_factor))
        
        animation = QPropertyAnimation(widget, b"size")
        animation.setDuration(duration)
        animation.setStartValue(original_size)
        animation.setEndValue(target_size)
        animation.setEasingCurve(AnimationPreset.EASE_DECELERATE)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.finished.connect(lambda: self.animation_finished.emit(animation_id))
        
        self.active_animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def bounce_in(self, widget: QWidget, duration: int = AnimationPreset.DURATION_SLOW,
                  callback: Optional[Callable] = None) -> str:
        """Animation d'entrée avec rebond"""
        animation_id = f"bounce_in_{id(widget)}"
        
        # Animation combinée : opacité + échelle
        group = QParallelAnimationGroup()
        
        # Opacité
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
        
        effect = widget.graphicsEffect()
        effect.setOpacity(0.0)
        
        opacity_anim = QPropertyAnimation(effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setStartValue(0.0)
        opacity_anim.setEndValue(1.0)
        opacity_anim.setEasingCurve(AnimationPreset.EASE_BOUNCE)
        
        # Échelle
        original_size = widget.size()
        widget.resize(0, 0)
        
        scale_anim = QPropertyAnimation(widget, b"size")
        scale_anim.setDuration(duration)
        scale_anim.setStartValue(QSize(0, 0))
        scale_anim.setEndValue(original_size)
        scale_anim.setEasingCurve(AnimationPreset.EASE_BOUNCE)
        
        group.addAnimation(opacity_anim)
        group.addAnimation(scale_anim)
        
        if callback:
            group.finished.connect(callback)
        
        group.finished.connect(lambda: self.animation_finished.emit(animation_id))
        
        self.animation_groups[animation_id] = group
        group.start()
        
        return animation_id
    
    def error_shake(self, widget: QWidget, intensity: int = 10,
                    duration: int = AnimationPreset.DURATION_NORMAL,
                    callback: Optional[Callable] = None) -> str:
        """Animation de secousse pour les erreurs"""
        animation_id = f"error_shake_{id(widget)}"
        
        original_pos = widget.pos()
        
        # Séquence d'animations de secousse
        sequence = QSequentialAnimationGroup()
        
        # Créer plusieurs petites animations de va-et-vient
        shake_count = 4
        shake_duration = duration // (shake_count * 2)
        
        for i in range(shake_count):
            # Vers la droite
            anim_right = QPropertyAnimation(widget, b"pos")
            anim_right.setDuration(shake_duration)
            anim_right.setStartValue(original_pos)
            anim_right.setEndValue(QPoint(original_pos.x() + intensity, original_pos.y()))
            anim_right.setEasingCurve(AnimationPreset.EASE_SHARP)
            
            # Vers la gauche
            anim_left = QPropertyAnimation(widget, b"pos")
            anim_left.setDuration(shake_duration)
            anim_left.setStartValue(QPoint(original_pos.x() + intensity, original_pos.y()))
            anim_left.setEndValue(QPoint(original_pos.x() - intensity, original_pos.y()))
            anim_left.setEasingCurve(AnimationPreset.EASE_SHARP)
            
            sequence.addAnimation(anim_right)
            sequence.addAnimation(anim_left)
            
            # Réduire l'intensité progressivement
            intensity = int(intensity * 0.7)
        
        # Retour à la position originale
        anim_return = QPropertyAnimation(widget, b"pos")
        anim_return.setDuration(shake_duration)
        anim_return.setStartValue(QPoint(original_pos.x() - intensity, original_pos.y()))
        anim_return.setEndValue(original_pos)
        anim_return.setEasingCurve(AnimationPreset.EASE_DECELERATE)
        
        sequence.addAnimation(anim_return)
        
        if callback:
            sequence.finished.connect(callback)
        
        sequence.finished.connect(lambda: self.animation_finished.emit(animation_id))
        
        self.animation_groups[animation_id] = sequence
        sequence.start()
        
        return animation_id
    
    def loading_pulse(self, widget: QWidget, callback: Optional[Callable] = None) -> str:
        """Animation de pulsation pour le chargement"""
        animation_id = f"loading_pulse_{id(widget)}"
        
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
        
        effect = widget.graphicsEffect()
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(1000)
        animation.setStartValue(0.3)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        animation.setLoopCount(-1)  # Boucle infinie
        
        if callback:
            animation.finished.connect(callback)
        
        self.active_animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def stop_animation(self, animation_id: str):
        """Arrête une animation spécifique"""
        if animation_id in self.active_animations:
            self.active_animations[animation_id].stop()
            del self.active_animations[animation_id]
        
        if animation_id in self.animation_groups:
            self.animation_groups[animation_id].stop()
            del self.animation_groups[animation_id]
    
    def stop_all_animations(self):
        """Arrête toutes les animations en cours"""
        for animation in self.active_animations.values():
            animation.stop()
        
        for group in self.animation_groups.values():
            group.stop()
        
        self.active_animations.clear()
        self.animation_groups.clear()
    
    def is_animating(self, widget: QWidget) -> bool:
        """Vérifie si un widget est en cours d'animation"""
        widget_id = id(widget)
        
        for animation_id in self.active_animations:
            if str(widget_id) in animation_id:
                return True
        
        for animation_id in self.animation_groups:
            if str(widget_id) in animation_id:
                return True
        
        return False

# Instance globale du gestionnaire d'animations
_global_animator = None

def get_animator() -> MaritimeAnimator:
    """Retourne l'instance globale du gestionnaire d'animations"""
    global _global_animator
    if _global_animator is None:
        _global_animator = MaritimeAnimator()
    return _global_animator

def animate_widget(widget: QWidget, animation_type: AnimationType, 
                  duration: Optional[int] = None, callback: Optional[Callable] = None) -> str:
    """Fonction utilitaire pour animer un widget"""
    animator = get_animator()
    
    if duration is None:
        duration = AnimationPreset.DURATION_NORMAL
    
    if animation_type == AnimationType.FADE_IN:
        return animator.fade_in(widget, duration, callback)
    elif animation_type == AnimationType.FADE_OUT:
        return animator.fade_out(widget, duration, callback)
    elif animation_type == AnimationType.SLIDE_IN_LEFT:
        return animator.slide_in(widget, "left", duration, callback)
    elif animation_type == AnimationType.SLIDE_IN_RIGHT:
        return animator.slide_in(widget, "right", duration, callback)
    elif animation_type == AnimationType.SLIDE_IN_UP:
        return animator.slide_in(widget, "up", duration, callback)
    elif animation_type == AnimationType.SLIDE_IN_DOWN:
        return animator.slide_in(widget, "down", duration, callback)
    elif animation_type == AnimationType.SCALE_IN:
        return animator.scale_animation(widget, 1.05, duration, callback)
    elif animation_type == AnimationType.SCALE_OUT:
        return animator.scale_animation(widget, 0.95, duration, callback)
    elif animation_type == AnimationType.BOUNCE_IN:
        return animator.bounce_in(widget, duration, callback)
    elif animation_type == AnimationType.ERROR_SHAKE:
        return animator.error_shake(widget, 10, duration, callback)
    elif animation_type == AnimationType.LOADING_PULSE:
        return animator.loading_pulse(widget, callback)
    else:
        logger.warning(f"Type d'animation non supporté: {animation_type}")
        return ""