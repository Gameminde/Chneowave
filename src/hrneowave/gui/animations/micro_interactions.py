# -*- coding: utf-8 -*-
"""
Système de micro-interactions pour les composants maritimes CHNeoWave
Phase 6 : Micro-interactions et feedback utilisateur
"""

import logging
from typing import Dict, Any, Optional, Callable
from enum import Enum

try:
    from PySide6.QtCore import QObject, QTimer, Signal, QPropertyAnimation, QEasingCurve, QRect, QPoint
    from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect
    from PySide6.QtGui import QColor, QPalette, QFont
except ImportError:
    try:
        from PyQt6.QtCore import QObject, QTimer, pyqtSignal as Signal, QPropertyAnimation, QEasingCurve, QRect, QPoint
        from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor, QPalette, QFont
    except ImportError:
        from PyQt5.QtCore import QObject, QTimer, pyqtSignal as Signal, QPropertyAnimation, QEasingCurve, QRect, QPoint
        from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor, QPalette, QFont

from .animation_system import MaritimeAnimator, AnimationPreset

logger = logging.getLogger(__name__)

class InteractionState(Enum):
    """États d'interaction des composants"""
    IDLE = "idle"
    HOVER = "hover"
    PRESSED = "pressed"
    FOCUSED = "focused"
    DISABLED = "disabled"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"

class MaritimeMicroInteractions(QObject):
    """Gestionnaire de micro-interactions maritimes"""
    
    interaction_triggered = Signal(str, str)  # widget_id, interaction_type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animator = MaritimeAnimator()
        self.active_interactions: Dict[str, Dict[str, Any]] = {}
        self.hover_timers: Dict[str, QTimer] = {}
        
        # Couleurs maritimes pour les interactions
        self.colors = {
            'ocean_deep': '#0A1929',
            'harbor_blue': '#1565C0',
            'steel_blue': '#1976D2',
            'tidal_cyan': '#00BCD4',
            'foam_white': '#FAFBFC',
            'storm_gray': '#37474F',
            'coral_alert': '#FF5722',
            'emerald_success': '#4CAF50',
            'amber_warning': '#FF9800'
        }
    
    def setup_button_interactions(self, button: QPushButton, style: str = "primary") -> str:
        """Configure les micro-interactions pour un bouton maritime"""
        widget_id = f"btn_{id(button)}"
        
        # Stocker les propriétés originales
        original_style = button.styleSheet()
        original_font = button.font()
        
        self.active_interactions[widget_id] = {
            'widget': button,
            'type': 'button',
            'style': style,
            'original_style': original_style,
            'original_font': original_font,
            'state': InteractionState.IDLE
        }
        
        # Connecter les événements
        button.enterEvent = lambda event: self._on_button_hover_enter(widget_id, event)
        button.leaveEvent = lambda event: self._on_button_hover_leave(widget_id, event)
        button.mousePressEvent = lambda event: self._on_button_press(widget_id, event)
        button.mouseReleaseEvent = lambda event: self._on_button_release(widget_id, event)
        
        # Appliquer le style initial
        self._apply_button_style(button, style, InteractionState.IDLE)
        
        return widget_id
    
    def setup_card_interactions(self, card: QFrame, elevation: int = 2) -> str:
        """Configure les micro-interactions pour une carte maritime"""
        widget_id = f"card_{id(card)}"
        
        # Créer l'effet d'ombre
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(elevation * 4)
        shadow_effect.setOffset(0, elevation)
        shadow_effect.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(shadow_effect)
        
        self.active_interactions[widget_id] = {
            'widget': card,
            'type': 'card',
            'elevation': elevation,
            'shadow_effect': shadow_effect,
            'state': InteractionState.IDLE
        }
        
        # Connecter les événements
        card.enterEvent = lambda event: self._on_card_hover_enter(widget_id, event)
        card.leaveEvent = lambda event: self._on_card_hover_leave(widget_id, event)
        
        return widget_id
    
    def setup_input_interactions(self, input_widget: QWidget) -> str:
        """Configure les micro-interactions pour un champ de saisie"""
        widget_id = f"input_{id(input_widget)}"
        
        original_style = input_widget.styleSheet()
        
        self.active_interactions[widget_id] = {
            'widget': input_widget,
            'type': 'input',
            'original_style': original_style,
            'state': InteractionState.IDLE
        }
        
        # Connecter les événements
        input_widget.focusInEvent = lambda event: self._on_input_focus_in(widget_id, event)
        input_widget.focusOutEvent = lambda event: self._on_input_focus_out(widget_id, event)
        
        return widget_id
    
    def setup_status_beacon_interactions(self, beacon: QLabel, status: str = "active") -> str:
        """Configure les micro-interactions pour un beacon de statut"""
        widget_id = f"beacon_{id(beacon)}"
        
        self.active_interactions[widget_id] = {
            'widget': beacon,
            'type': 'beacon',
            'status': status,
            'state': InteractionState.IDLE
        }
        
        # Démarrer l'animation de pulsation si actif
        if status == "active":
            self._start_beacon_pulse(widget_id)
        
        return widget_id
    
    def _on_button_hover_enter(self, widget_id: str, event):
        """Gestion de l'entrée de la souris sur un bouton"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        button = interaction['widget']
        style = interaction['style']
        
        # Changer l'état
        interaction['state'] = InteractionState.HOVER
        
        # Animation de hover avec délai
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._apply_button_hover_effect(widget_id))
        timer.start(50)  # Délai de 50ms pour éviter les survols accidentels
        
        self.hover_timers[widget_id] = timer
        
        self.interaction_triggered.emit(widget_id, "hover_enter")
    
    def _on_button_hover_leave(self, widget_id: str, event):
        """Gestion de la sortie de la souris d'un bouton"""
        if widget_id not in self.active_interactions:
            return
        
        # Annuler le timer de hover si actif
        if widget_id in self.hover_timers:
            self.hover_timers[widget_id].stop()
            del self.hover_timers[widget_id]
        
        interaction = self.active_interactions[widget_id]
        button = interaction['widget']
        style = interaction['style']
        
        # Retour à l'état normal
        interaction['state'] = InteractionState.IDLE
        self._apply_button_style(button, style, InteractionState.IDLE)
        
        self.interaction_triggered.emit(widget_id, "hover_leave")
    
    def _on_button_press(self, widget_id: str, event):
        """Gestion du clic sur un bouton"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        button = interaction['widget']
        style = interaction['style']
        
        # Changer l'état
        interaction['state'] = InteractionState.PRESSED
        
        # Animation de pression
        self.animator.scale_animation(button, 0.98, AnimationPreset.DURATION_FAST)
        self._apply_button_style(button, style, InteractionState.PRESSED)
        
        self.interaction_triggered.emit(widget_id, "press")
    
    def _on_button_release(self, widget_id: str, event):
        """Gestion du relâchement du clic sur un bouton"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        button = interaction['widget']
        style = interaction['style']
        
        # Retour à l'état hover ou idle
        if button.underMouse():
            interaction['state'] = InteractionState.HOVER
            self._apply_button_style(button, style, InteractionState.HOVER)
        else:
            interaction['state'] = InteractionState.IDLE
            self._apply_button_style(button, style, InteractionState.IDLE)
        
        # Animation de retour
        self.animator.scale_animation(button, 1.0, AnimationPreset.DURATION_FAST)
        
        self.interaction_triggered.emit(widget_id, "release")
    
    def _on_card_hover_enter(self, widget_id: str, event):
        """Gestion de l'entrée de la souris sur une carte"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        card = interaction['widget']
        shadow_effect = interaction['shadow_effect']
        
        # Augmenter l'élévation
        new_elevation = interaction['elevation'] + 4
        shadow_effect.setBlurRadius(new_elevation * 4)
        shadow_effect.setOffset(0, new_elevation)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        
        # Animation de lift
        self.animator.scale_animation(card, 1.02, AnimationPreset.DURATION_NORMAL)
        
        interaction['state'] = InteractionState.HOVER
        self.interaction_triggered.emit(widget_id, "card_hover_enter")
    
    def _on_card_hover_leave(self, widget_id: str, event):
        """Gestion de la sortie de la souris d'une carte"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        card = interaction['widget']
        shadow_effect = interaction['shadow_effect']
        
        # Retour à l'élévation normale
        elevation = interaction['elevation']
        shadow_effect.setBlurRadius(elevation * 4)
        shadow_effect.setOffset(0, elevation)
        shadow_effect.setColor(QColor(0, 0, 0, 30))
        
        # Animation de retour
        self.animator.scale_animation(card, 1.0, AnimationPreset.DURATION_NORMAL)
        
        interaction['state'] = InteractionState.IDLE
        self.interaction_triggered.emit(widget_id, "card_hover_leave")
    
    def _on_input_focus_in(self, widget_id: str, event):
        """Gestion du focus sur un champ de saisie"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        input_widget = interaction['widget']
        
        # Appliquer le style de focus
        focus_style = f"""
            border: 2px solid {self.colors['tidal_cyan']};
            background-color: {self.colors['foam_white']};
            border-radius: 6px;
            padding: 8px 12px;
        """
        
        input_widget.setStyleSheet(focus_style)
        
        interaction['state'] = InteractionState.FOCUSED
        self.interaction_triggered.emit(widget_id, "focus_in")
    
    def _on_input_focus_out(self, widget_id: str, event):
        """Gestion de la perte de focus sur un champ de saisie"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        input_widget = interaction['widget']
        
        # Retour au style normal
        normal_style = f"""
            border: 1px solid {self.colors['storm_gray']};
            background-color: {self.colors['foam_white']};
            border-radius: 6px;
            padding: 8px 12px;
        """
        
        input_widget.setStyleSheet(normal_style)
        
        interaction['state'] = InteractionState.IDLE
        self.interaction_triggered.emit(widget_id, "focus_out")
    
    def _apply_button_hover_effect(self, widget_id: str):
        """Applique l'effet de hover sur un bouton"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        if interaction['state'] != InteractionState.HOVER:
            return
        
        button = interaction['widget']
        style = interaction['style']
        
        # Animation de scale
        self.animator.scale_animation(button, 1.02, AnimationPreset.DURATION_FAST)
        
        # Appliquer le style de hover
        self._apply_button_style(button, style, InteractionState.HOVER)
    
    def _apply_button_style(self, button: QPushButton, style: str, state: InteractionState):
        """Applique le style approprié selon l'état du bouton"""
        base_style = f"""
            QPushButton {{
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
                /* transition not supported in Qt */
            }}
        """
        
        if style == "primary":
            if state == InteractionState.IDLE:
                color_style = f"""
                    background-color: {self.colors['harbor_blue']};
                    color: {self.colors['foam_white']};
                """
            elif state == InteractionState.HOVER:
                color_style = f"""
                    background-color: {self.colors['steel_blue']};
                    color: {self.colors['foam_white']};
                """
            elif state == InteractionState.PRESSED:
                color_style = f"""
                    background-color: {self.colors['ocean_deep']};
                    color: {self.colors['foam_white']};
                """
            else:
                color_style = f"""
                    background-color: {self.colors['storm_gray']};
                    color: {self.colors['foam_white']};
                """
        
        elif style == "secondary":
            if state == InteractionState.IDLE:
                color_style = f"""
                    background-color: transparent;
                    color: {self.colors['harbor_blue']};
                    border: 2px solid {self.colors['harbor_blue']};
                """
            elif state == InteractionState.HOVER:
                color_style = f"""
                    background-color: {self.colors['harbor_blue']};
                    color: {self.colors['foam_white']};
                    border: 2px solid {self.colors['harbor_blue']};
                """
            elif state == InteractionState.PRESSED:
                color_style = f"""
                    background-color: {self.colors['ocean_deep']};
                    color: {self.colors['foam_white']};
                    border: 2px solid {self.colors['ocean_deep']};
                """
            else:
                color_style = f"""
                    background-color: transparent;
                    color: {self.colors['storm_gray']};
                    border: 2px solid {self.colors['storm_gray']};
                """
        
        elif style == "success":
            if state == InteractionState.IDLE:
                color_style = f"""
                    background-color: {self.colors['emerald_success']};
                    color: {self.colors['foam_white']};
                """
            elif state == InteractionState.HOVER:
                color_style = f"""
                    background-color: #059669;
                    color: {self.colors['foam_white']};
                """
            else:
                color_style = f"""
                    background-color: {self.colors['emerald_success']};
                    color: {self.colors['foam_white']};
                """
        
        elif style == "danger":
            if state == InteractionState.IDLE:
                color_style = f"""
                    background-color: {self.colors['coral_alert']};
                    color: {self.colors['foam_white']};
                """
            elif state == InteractionState.HOVER:
                color_style = f"""
                    background-color: #dc2626;
                    color: {self.colors['foam_white']};
                """
            else:
                color_style = f"""
                    background-color: {self.colors['coral_alert']};
                    color: {self.colors['foam_white']};
                """
        
        else:  # default
            color_style = f"""
                background-color: {self.colors['storm_gray']};
                color: {self.colors['foam_white']};
            """
        
        button.setStyleSheet(base_style + color_style)
    
    def _start_beacon_pulse(self, widget_id: str):
        """Démarre l'animation de pulsation pour un beacon"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        beacon = interaction['widget']
        
        # Animation de pulsation continue
        self.animator.loading_pulse(beacon)
    
    def trigger_success_feedback(self, widget_id: str):
        """Déclenche un feedback de succès"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        widget = interaction['widget']
        
        # Animation de succès
        self.animator.bounce_in(widget, AnimationPreset.DURATION_SLOW)
        
        # Changer temporairement la couleur
        original_style = widget.styleSheet()
        success_style = f"""
            background-color: {self.colors['emerald_success']};
            color: {self.colors['foam_white']};
            border-radius: 8px;
        """
        
        widget.setStyleSheet(success_style)
        
        # Retour au style original après 2 secondes
        QTimer.singleShot(2000, lambda: widget.setStyleSheet(original_style))
        
        self.interaction_triggered.emit(widget_id, "success_feedback")
    
    def trigger_error_feedback(self, widget_id: str):
        """Déclenche un feedback d'erreur"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        widget = interaction['widget']
        
        # Animation de secousse
        self.animator.error_shake(widget)
        
        # Changer temporairement la couleur
        original_style = widget.styleSheet()
        error_style = f"""
            background-color: {self.colors['coral_alert']};
            color: {self.colors['foam_white']};
            border-radius: 8px;
            border: 2px solid #dc2626;
        """
        
        widget.setStyleSheet(error_style)
        
        # Retour au style original après 3 secondes
        QTimer.singleShot(3000, lambda: widget.setStyleSheet(original_style))
        
        self.interaction_triggered.emit(widget_id, "error_feedback")
    
    def set_loading_state(self, widget_id: str, loading: bool = True):
        """Active/désactive l'état de chargement"""
        if widget_id not in self.active_interactions:
            return
        
        interaction = self.active_interactions[widget_id]
        widget = interaction['widget']
        
        if loading:
            interaction['state'] = InteractionState.LOADING
            widget.setEnabled(False)
            
            # Démarrer l'animation de chargement
            if interaction['type'] == 'button':
                widget.setText("Chargement...")
                self.animator.loading_pulse(widget)
        else:
            interaction['state'] = InteractionState.IDLE
            widget.setEnabled(True)
            
            # Arrêter l'animation de chargement
            self.animator.stop_animation(f"loading_pulse_{id(widget)}")
        
        self.interaction_triggered.emit(widget_id, "loading_state_changed")
    
    def cleanup_interactions(self, widget_id: str):
        """Nettoie les interactions pour un widget"""
        if widget_id in self.active_interactions:
            # Arrêter toutes les animations pour ce widget
            widget = self.active_interactions[widget_id]['widget']
            widget_obj_id = id(widget)
            
            # Arrêter les animations actives
            animations_to_stop = []
            for anim_id in self.animator.active_animations:
                if str(widget_obj_id) in anim_id:
                    animations_to_stop.append(anim_id)
            
            for anim_id in animations_to_stop:
                self.animator.stop_animation(anim_id)
            
            # Nettoyer les timers
            if widget_id in self.hover_timers:
                self.hover_timers[widget_id].stop()
                del self.hover_timers[widget_id]
            
            # Supprimer l'interaction
            del self.active_interactions[widget_id]
    
    def configure_button_interactions(self, config: Dict[str, Any]):
        """Configure les interactions pour un bouton"""
        self.interaction_configs = getattr(self, 'interaction_configs', {})
        self.interaction_configs['button'] = {
            'hover_scale': config.get('hover_scale', 1.02),
            'press_scale': config.get('press_scale', 0.98),
            'hover_duration': config.get('hover_duration', AnimationPreset.DURATION_FAST),
            'press_duration': config.get('press_duration', AnimationPreset.DURATION_FAST),
            'success_color': config.get('success_color', '#4CAF50'),
            'error_color': config.get('error_color', '#FF5722'),
            'loading_color': config.get('loading_color', '#FF9800')
        }
    
    def configure_card_interactions(self, config: Dict[str, Any]):
        """Configure les interactions pour une carte"""
        self.interaction_configs = getattr(self, 'interaction_configs', {})
        self.interaction_configs['card'] = {
            'hover_elevation': config.get('hover_elevation', 8),
            'press_elevation': config.get('press_elevation', 1),
            'rest_elevation': config.get('rest_elevation', 2),
            'hover_duration': config.get('hover_duration', AnimationPreset.DURATION_NORMAL),
            'press_duration': config.get('press_duration', AnimationPreset.DURATION_FAST),
            'hover_scale': config.get('hover_scale', 1.01),
            'press_scale': config.get('press_scale', 0.99)
        }
    
    def cleanup_all_interactions(self):
        """Nettoie toutes les interactions"""
        # Arrêter tous les timers
        for timer in self.hover_timers.values():
            timer.stop()
        self.hover_timers.clear()
        
        # Arrêter toutes les animations
        self.animator.stop_all_animations()
        
        # Nettoyer les interactions
        self.active_interactions.clear()

# Instance globale du gestionnaire de micro-interactions
_global_micro_interactions = None

def get_micro_interactions() -> MaritimeMicroInteractions:
    """Retourne l'instance globale du gestionnaire de micro-interactions"""
    global _global_micro_interactions
    if _global_micro_interactions is None:
        _global_micro_interactions = MaritimeMicroInteractions()
    return _global_micro_interactions