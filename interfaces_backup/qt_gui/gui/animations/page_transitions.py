# -*- coding: utf-8 -*-
"""
Système de transitions de pages pour CHNeoWave
Phase 6 : Transitions fluides entre les vues
"""

import logging
from typing import Dict, Any, Optional, Callable
from enum import Enum

try:
    from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, Signal, QRect, QTimer
    from PySide6.QtWidgets import QWidget, QStackedWidget, QGraphicsOpacityEffect
    from PySide6.QtGui import QPixmap, QPainter
except ImportError:
    try:
        from PyQt6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, pyqtSignal as Signal, QRect, QTimer
        from PyQt6.QtWidgets import QWidget, QStackedWidget, QGraphicsOpacityEffect
        from PyQt6.QtGui import QPixmap, QPainter
    except ImportError:
        from PyQt5.QtCore import QObject, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, pyqtSignal as Signal, QRect, QTimer
        from PyQt5.QtWidgets import QWidget, QStackedWidget, QGraphicsOpacityEffect
        from PyQt5.QtGui import QPixmap, QPainter

from .animation_system import AnimationPreset

logger = logging.getLogger(__name__)

class TransitionType(Enum):
    """Types de transitions disponibles"""
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    PUSH_LEFT = "push_left"
    PUSH_RIGHT = "push_right"
    PUSH_UP = "push_up"
    PUSH_DOWN = "push_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    FLIP_HORIZONTAL = "flip_horizontal"
    FLIP_VERTICAL = "flip_vertical"
    CUBE_LEFT = "cube_left"
    CUBE_RIGHT = "cube_right"

class TransitionDirection(Enum):
    """Directions de transition"""
    FORWARD = "forward"
    BACKWARD = "backward"
    UP = "up"
    DOWN = "down"

class MaritimePageTransitions(QObject):
    """Gestionnaire de transitions de pages maritimes"""
    
    transition_started = Signal(str, str)  # from_page, to_page
    transition_finished = Signal(str, str)  # from_page, to_page
    
    def __init__(self, stacked_widget: QStackedWidget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.current_animation = None
        self.animation_group = None
        self.is_animating = False
        
        # Configuration par défaut
        self.default_duration = AnimationPreset.DURATION_NORMAL
        self.default_easing = AnimationPreset.EASE_STANDARD
        
        # Mapping des vues pour les transitions contextuelles
        self.view_hierarchy = {
            'welcome': 0,
            'dashboard': 1,
            'calibration': 2,
            'acquisition': 3,
            'analysis': 4,
            'report': 5,
            'settings': 6
        }
        
        # Transitions recommandées selon le contexte
        self.contextual_transitions = {
            ('welcome', 'dashboard'): TransitionType.FADE,
            ('dashboard', 'calibration'): TransitionType.SLIDE_RIGHT,
            ('calibration', 'acquisition'): TransitionType.SLIDE_RIGHT,
            ('acquisition', 'analysis'): TransitionType.SLIDE_RIGHT,
            ('analysis', 'report'): TransitionType.SLIDE_RIGHT,
            ('dashboard', 'settings'): TransitionType.SLIDE_UP,
        }
    
    def transition_to_page(self, target_index: int, 
                          transition_type: Optional[TransitionType] = None,
                          duration: Optional[int] = None,
                          direction: Optional[TransitionDirection] = None,
                          callback: Optional[Callable] = None) -> bool:
        """Effectue une transition vers une page spécifique"""
        
        if self.is_animating:
            logger.warning("Transition déjà en cours, ignorée")
            return False
        
        current_index = self.stacked_widget.currentIndex()
        if current_index == target_index:
            logger.debug("Déjà sur la page cible")
            return True
        
        # Déterminer la transition automatiquement si non spécifiée
        if transition_type is None:
            transition_type = self._get_contextual_transition(current_index, target_index)
        
        # Déterminer la direction automatiquement si non spécifiée
        if direction is None:
            direction = self._get_transition_direction(current_index, target_index)
        
        # Utiliser la durée par défaut si non spécifiée
        if duration is None:
            duration = self.default_duration
        
        # Obtenir les widgets source et cible
        current_widget = self.stacked_widget.widget(current_index)
        target_widget = self.stacked_widget.widget(target_index)
        
        if not current_widget or not target_widget:
            logger.error("Widget source ou cible introuvable")
            return False
        
        # Émettre le signal de début de transition
        current_name = self._get_page_name(current_index)
        target_name = self._get_page_name(target_index)
        self.transition_started.emit(current_name, target_name)
        
        # Marquer comme en cours d'animation
        self.is_animating = True
        
        # Exécuter la transition selon le type
        success = self._execute_transition(
            current_widget, target_widget, current_index, target_index,
            transition_type, direction, duration, callback
        )
        
        if not success:
            self.is_animating = False
            logger.error(f"Échec de la transition {transition_type}")
            return False
        
        return True
    
    def _execute_transition(self, current_widget: QWidget, target_widget: QWidget,
                           current_index: int, target_index: int,
                           transition_type: TransitionType, direction: TransitionDirection,
                           duration: int, callback: Optional[Callable]) -> bool:
        """Exécute la transition spécifiée"""
        
        try:
            if transition_type == TransitionType.FADE:
                return self._fade_transition(current_widget, target_widget, current_index, target_index, duration, callback)
            
            elif transition_type in [TransitionType.SLIDE_LEFT, TransitionType.SLIDE_RIGHT, 
                                   TransitionType.SLIDE_UP, TransitionType.SLIDE_DOWN]:
                return self._slide_transition(current_widget, target_widget, current_index, target_index, 
                                            transition_type, duration, callback)
            
            elif transition_type in [TransitionType.PUSH_LEFT, TransitionType.PUSH_RIGHT,
                                   TransitionType.PUSH_UP, TransitionType.PUSH_DOWN]:
                return self._push_transition(current_widget, target_widget, current_index, target_index,
                                           transition_type, duration, callback)
            
            elif transition_type in [TransitionType.ZOOM_IN, TransitionType.ZOOM_OUT]:
                return self._zoom_transition(current_widget, target_widget, current_index, target_index,
                                           transition_type, duration, callback)
            
            else:
                # Fallback vers fade
                return self._fade_transition(current_widget, target_widget, current_index, target_index, duration, callback)
        
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la transition: {e}")
            return False
    
    def _fade_transition(self, current_widget: QWidget, target_widget: QWidget,
                        current_index: int, target_index: int,
                        duration: int, callback: Optional[Callable]) -> bool:
        """Transition de fondu croisé"""
        
        # Préparer les effets d'opacité
        current_effect = QGraphicsOpacityEffect()
        target_effect = QGraphicsOpacityEffect()
        
        current_widget.setGraphicsEffect(current_effect)
        target_widget.setGraphicsEffect(target_effect)
        
        # Configurer les opacités initiales
        current_effect.setOpacity(1.0)
        target_effect.setOpacity(0.0)
        
        # Afficher le widget cible
        self.stacked_widget.setCurrentIndex(target_index)
        
        # Créer les animations
        fade_out = QPropertyAnimation(current_effect, b"opacity")
        fade_out.setDuration(duration)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(self.default_easing)
        
        fade_in = QPropertyAnimation(target_effect, b"opacity")
        fade_in.setDuration(duration)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(self.default_easing)
        
        # Grouper les animations
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(fade_out)
        self.animation_group.addAnimation(fade_in)
        
        # Connecter la fin d'animation
        self.animation_group.finished.connect(
            lambda: self._on_transition_finished(current_index, target_index, callback)
        )
        
        # Démarrer l'animation
        self.animation_group.start()
        
        return True
    
    def _slide_transition(self, current_widget: QWidget, target_widget: QWidget,
                         current_index: int, target_index: int,
                         transition_type: TransitionType, duration: int,
                         callback: Optional[Callable]) -> bool:
        """Transition de glissement"""
        
        # Obtenir les dimensions du conteneur
        container_rect = self.stacked_widget.geometry()
        width = container_rect.width()
        height = container_rect.height()
        
        # Déterminer les positions selon le type de glissement
        if transition_type == TransitionType.SLIDE_LEFT:
            current_start = QRect(0, 0, width, height)
            current_end = QRect(-width, 0, width, height)
            target_start = QRect(width, 0, width, height)
            target_end = QRect(0, 0, width, height)
        
        elif transition_type == TransitionType.SLIDE_RIGHT:
            current_start = QRect(0, 0, width, height)
            current_end = QRect(width, 0, width, height)
            target_start = QRect(-width, 0, width, height)
            target_end = QRect(0, 0, width, height)
        
        elif transition_type == TransitionType.SLIDE_UP:
            current_start = QRect(0, 0, width, height)
            current_end = QRect(0, -height, width, height)
            target_start = QRect(0, height, width, height)
            target_end = QRect(0, 0, width, height)
        
        else:  # SLIDE_DOWN
            current_start = QRect(0, 0, width, height)
            current_end = QRect(0, height, width, height)
            target_start = QRect(0, -height, width, height)
            target_end = QRect(0, 0, width, height)
        
        # Positionner les widgets
        current_widget.setGeometry(current_start)
        target_widget.setGeometry(target_start)
        
        # Afficher le widget cible
        self.stacked_widget.setCurrentIndex(target_index)
        
        # Créer les animations
        current_anim = QPropertyAnimation(current_widget, b"geometry")
        current_anim.setDuration(duration)
        current_anim.setStartValue(current_start)
        current_anim.setEndValue(current_end)
        current_anim.setEasingCurve(self.default_easing)
        
        target_anim = QPropertyAnimation(target_widget, b"geometry")
        target_anim.setDuration(duration)
        target_anim.setStartValue(target_start)
        target_anim.setEndValue(target_end)
        target_anim.setEasingCurve(self.default_easing)
        
        # Grouper les animations
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(current_anim)
        self.animation_group.addAnimation(target_anim)
        
        # Connecter la fin d'animation
        self.animation_group.finished.connect(
            lambda: self._on_transition_finished(current_index, target_index, callback)
        )
        
        # Démarrer l'animation
        self.animation_group.start()
        
        return True
    
    def _push_transition(self, current_widget: QWidget, target_widget: QWidget,
                        current_index: int, target_index: int,
                        transition_type: TransitionType, duration: int,
                        callback: Optional[Callable]) -> bool:
        """Transition de poussée (push)"""
        
        # Similar to slide but with different timing
        container_rect = self.stacked_widget.geometry()
        width = container_rect.width()
        height = container_rect.height()
        
        # Séquence d'animations : d'abord sortir l'ancien, puis entrer le nouveau
        sequence = QSequentialAnimationGroup()
        
        # Phase 1 : Sortie de l'ancien widget
        if transition_type == TransitionType.PUSH_LEFT:
            current_end = QRect(-width, 0, width, height)
        elif transition_type == TransitionType.PUSH_RIGHT:
            current_end = QRect(width, 0, width, height)
        elif transition_type == TransitionType.PUSH_UP:
            current_end = QRect(0, -height, width, height)
        else:  # PUSH_DOWN
            current_end = QRect(0, height, width, height)
        
        current_anim = QPropertyAnimation(current_widget, b"geometry")
        current_anim.setDuration(duration // 2)
        current_anim.setStartValue(QRect(0, 0, width, height))
        current_anim.setEndValue(current_end)
        current_anim.setEasingCurve(AnimationPreset.EASE_ACCELERATE)
        
        # Phase 2 : Entrée du nouveau widget
        if transition_type == TransitionType.PUSH_LEFT:
            target_start = QRect(width, 0, width, height)
        elif transition_type == TransitionType.PUSH_RIGHT:
            target_start = QRect(-width, 0, width, height)
        elif transition_type == TransitionType.PUSH_UP:
            target_start = QRect(0, height, width, height)
        else:  # PUSH_DOWN
            target_start = QRect(0, -height, width, height)
        
        target_anim = QPropertyAnimation(target_widget, b"geometry")
        target_anim.setDuration(duration // 2)
        target_anim.setStartValue(target_start)
        target_anim.setEndValue(QRect(0, 0, width, height))
        target_anim.setEasingCurve(AnimationPreset.EASE_DECELERATE)
        
        # Ajouter à la séquence
        sequence.addAnimation(current_anim)
        
        # Changer de page entre les deux animations
        current_anim.finished.connect(lambda: self.stacked_widget.setCurrentIndex(target_index))
        current_anim.finished.connect(lambda: target_widget.setGeometry(target_start))
        
        sequence.addAnimation(target_anim)
        
        # Connecter la fin d'animation
        sequence.finished.connect(
            lambda: self._on_transition_finished(current_index, target_index, callback)
        )
        
        self.animation_group = sequence
        sequence.start()
        
        return True
    
    def _zoom_transition(self, current_widget: QWidget, target_widget: QWidget,
                        current_index: int, target_index: int,
                        transition_type: TransitionType, duration: int,
                        callback: Optional[Callable]) -> bool:
        """Transition de zoom"""
        
        # Préparer les effets d'opacité
        current_effect = QGraphicsOpacityEffect()
        target_effect = QGraphicsOpacityEffect()
        
        current_widget.setGraphicsEffect(current_effect)
        target_widget.setGraphicsEffect(target_effect)
        
        # Configurer les opacités initiales
        current_effect.setOpacity(1.0)
        target_effect.setOpacity(0.0)
        
        # Obtenir les tailles
        original_size = current_widget.size()
        
        if transition_type == TransitionType.ZOOM_IN:
            # Zoom out de l'ancien, zoom in du nouveau
            current_end_size = original_size * 1.2
            target_start_size = original_size * 0.8
        else:  # ZOOM_OUT
            # Zoom in de l'ancien, zoom out du nouveau
            current_end_size = original_size * 0.8
            target_start_size = original_size * 1.2
        
        # Positionner le widget cible
        target_widget.resize(target_start_size)
        
        # Afficher le widget cible
        self.stacked_widget.setCurrentIndex(target_index)
        
        # Créer les animations
        group = QParallelAnimationGroup()
        
        # Animation de l'ancien widget
        current_fade = QPropertyAnimation(current_effect, b"opacity")
        current_fade.setDuration(duration)
        current_fade.setStartValue(1.0)
        current_fade.setEndValue(0.0)
        current_fade.setEasingCurve(self.default_easing)
        
        current_scale = QPropertyAnimation(current_widget, b"size")
        current_scale.setDuration(duration)
        current_scale.setStartValue(original_size)
        current_scale.setEndValue(current_end_size)
        current_scale.setEasingCurve(self.default_easing)
        
        # Animation du nouveau widget
        target_fade = QPropertyAnimation(target_effect, b"opacity")
        target_fade.setDuration(duration)
        target_fade.setStartValue(0.0)
        target_fade.setEndValue(1.0)
        target_fade.setEasingCurve(self.default_easing)
        
        target_scale = QPropertyAnimation(target_widget, b"size")
        target_scale.setDuration(duration)
        target_scale.setStartValue(target_start_size)
        target_scale.setEndValue(original_size)
        target_scale.setEasingCurve(self.default_easing)
        
        # Ajouter au groupe
        group.addAnimation(current_fade)
        group.addAnimation(current_scale)
        group.addAnimation(target_fade)
        group.addAnimation(target_scale)
        
        # Connecter la fin d'animation
        group.finished.connect(
            lambda: self._on_transition_finished(current_index, target_index, callback)
        )
        
        self.animation_group = group
        group.start()
        
        return True
    
    def _get_contextual_transition(self, current_index: int, target_index: int) -> TransitionType:
        """Détermine la transition contextuelle appropriée"""
        current_name = self._get_page_name(current_index)
        target_name = self._get_page_name(target_index)
        
        # Vérifier les transitions prédéfinies
        key = (current_name, target_name)
        if key in self.contextual_transitions:
            return self.contextual_transitions[key]
        
        # Vérifier les transitions inverses
        reverse_key = (target_name, current_name)
        if reverse_key in self.contextual_transitions:
            transition = self.contextual_transitions[reverse_key]
            # Inverser la direction pour les transitions de glissement
            if transition == TransitionType.SLIDE_RIGHT:
                return TransitionType.SLIDE_LEFT
            elif transition == TransitionType.SLIDE_LEFT:
                return TransitionType.SLIDE_RIGHT
            elif transition == TransitionType.SLIDE_UP:
                return TransitionType.SLIDE_DOWN
            elif transition == TransitionType.SLIDE_DOWN:
                return TransitionType.SLIDE_UP
            else:
                return transition
        
        # Transition par défaut selon la hiérarchie
        if current_index < target_index:
            return TransitionType.SLIDE_RIGHT
        else:
            return TransitionType.SLIDE_LEFT
    
    def _get_transition_direction(self, current_index: int, target_index: int) -> TransitionDirection:
        """Détermine la direction de transition"""
        if current_index < target_index:
            return TransitionDirection.FORWARD
        else:
            return TransitionDirection.BACKWARD
    
    def _get_page_name(self, index: int) -> str:
        """Obtient le nom de la page à partir de son index"""
        for name, idx in self.view_hierarchy.items():
            if idx == index:
                return name
        return f"page_{index}"
    
    def _on_transition_finished(self, current_index: int, target_index: int, callback: Optional[Callable]):
        """Appelé à la fin d'une transition"""
        # Nettoyer les effets graphiques
        current_widget = self.stacked_widget.widget(current_index)
        target_widget = self.stacked_widget.widget(target_index)
        
        if current_widget and current_widget.graphicsEffect():
            current_widget.setGraphicsEffect(None)
        
        if target_widget and target_widget.graphicsEffect():
            target_widget.setGraphicsEffect(None)
        
        # Réinitialiser les géométries
        container_rect = self.stacked_widget.geometry()
        if target_widget:
            target_widget.setGeometry(0, 0, container_rect.width(), container_rect.height())
        
        # Marquer comme terminé
        self.is_animating = False
        
        # Nettoyer les animations
        if self.animation_group:
            self.animation_group.deleteLater()
            self.animation_group = None
        
        # Émettre le signal de fin
        current_name = self._get_page_name(current_index)
        target_name = self._get_page_name(target_index)
        self.transition_finished.emit(current_name, target_name)
        
        # Appeler le callback si fourni
        if callback:
            try:
                callback()
            except Exception as e:
                logger.error(f"Erreur dans le callback de transition: {e}")
    
    def set_transition_duration(self, duration: int):
        """Définit la durée par défaut des transitions"""
        self.default_duration = max(100, min(2000, duration))  # Entre 100ms et 2s
    
    def set_transition_easing(self, easing: QEasingCurve.Type):
        """Définit la courbe d'accélération par défaut"""
        self.default_easing = easing
    
    def is_transition_active(self) -> bool:
        """Vérifie si une transition est en cours"""
        return self.is_animating
    
    def stop_current_transition(self):
        """Arrête la transition en cours"""
        if self.animation_group and self.is_animating:
            self.animation_group.stop()
            self.is_animating = False
            
            # Nettoyer
            if self.animation_group:
                self.animation_group.deleteLater()
                self.animation_group = None
    
    def add_contextual_transition(self, from_page: str, to_page: str, transition: TransitionType):
        """Ajoute une transition contextuelle personnalisée"""
        self.contextual_transitions[(from_page, to_page)] = transition
    
    def remove_contextual_transition(self, from_page: str, to_page: str):
        """Supprime une transition contextuelle"""
        key = (from_page, to_page)
        if key in self.contextual_transitions:
            del self.contextual_transitions[key]