# -*- coding: utf-8 -*-
"""
ProgressStepper - Indicateur de progression par étapes
Design System Maritime 2025 - CHNeoWave

Indicateur avec :
- Étapes numérotées
- États visuels (completed, active, pending)
- Animations de transition
- Labels descriptifs
- Navigation optionnelle
"""

import sys
from typing import Optional, List, Dict, Tuple

try:
    from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
    from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QRect, QTimer
    from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics
except ImportError:
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
    from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QRect, QTimer
    from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics


class ProgressStepper(QWidget):
    """
    Indicateur de progression par étapes maritime.
    
    Caractéristiques :
    - Étapes avec numéros et labels
    - États visuels distincts
    - Animations de transition
    - Navigation optionnelle
    - Responsive design
    """
    
    # Signaux
    step_clicked = pyqtSignal(int)  # Étape cliquée
    step_changed = pyqtSignal(int)  # Étape changée
    completed = pyqtSignal()        # Toutes les étapes terminées
    
    # États des étapes
    STATE_PENDING = "pending"
    STATE_ACTIVE = "active"
    STATE_COMPLETED = "completed"
    STATE_ERROR = "error"
    
    # Orientations
    ORIENTATION_HORIZONTAL = "horizontal"
    ORIENTATION_VERTICAL = "vertical"
    
    # Constantes Design System
    FIBONACCI_SPACES = [8, 13, 21, 34, 55, 89, 144]
    GOLDEN_RATIO = 1.618
    
    # Couleurs Maritime
    MARITIME_COLORS = {
        'ocean_deep': '#0A1929',
        'harbor_blue': '#1565C0',
        'steel_blue': '#1976D2',
        'tidal_cyan': '#00BCD4',
        'foam_white': '#FAFBFC',
        'frost_light': '#F5F7FA',
        'storm_gray': '#37474F',
        'slate_gray': '#546E7A',
        'coral_alert': '#FF5722',
        'emerald_success': '#4CAF50',
        'amber_warning': '#FF8F00'
    }
    
    def __init__(self, parent: Optional[QWidget] = None,
                 steps: List[str] = None,
                 orientation: str = ORIENTATION_HORIZONTAL,
                 clickable: bool = False,
                 show_numbers: bool = True,
                 show_labels: bool = True):
        super().__init__(parent)
        
        # Configuration
        self.steps = steps or ["Étape 1", "Étape 2", "Étape 3"]
        self.orientation = orientation
        self.clickable = clickable
        self.show_numbers = show_numbers
        self.show_labels = show_labels
        
        # État
        self.current_step = 0
        self.step_states = [self.STATE_PENDING] * len(self.steps)
        self.step_states[0] = self.STATE_ACTIVE  # Première étape active
        
        # Dimensions
        self.step_size = 32
        self.connector_width = 2
        
        # Animation
        self._animation_progress = 0.0
        
        # Configuration de base
        self._setup_ui()
        self._setup_animations()
        
        # Style
        self._apply_stepper_style()
    
    def _setup_ui(self):
        """Configure l'interface du stepper."""
        # Layout principal selon l'orientation
        if self.orientation == self.ORIENTATION_HORIZONTAL:
            self.layout = QHBoxLayout(self)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.layout = QVBoxLayout(self)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.layout.setContentsMargins(self.FIBONACCI_SPACES[1], self.FIBONACCI_SPACES[1],
                                     self.FIBONACCI_SPACES[1], self.FIBONACCI_SPACES[1])
        self.layout.setSpacing(0)
        
        # Calcul des dimensions
        self._calculate_dimensions()
        
        # Configuration du curseur si cliquable
        if self.clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def _setup_animations(self):
        """Configure les animations du stepper."""
        # Animation de progression
        self.progress_animation = QPropertyAnimation(self, b"animation_progress")
        self.progress_animation.setDuration(500)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Animation de pulsation pour l'étape active
        self.pulse_animation = QPropertyAnimation(self, b"animation_progress")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_animation.setStartValue(0.0)
        self.pulse_animation.setEndValue(1.0)
        self.pulse_animation.setLoopCount(-1)
    
    def _calculate_dimensions(self):
        """Calcule les dimensions du stepper."""
        if self.orientation == self.ORIENTATION_HORIZONTAL:
            # Largeur : étapes + connecteurs
            step_width = self.step_size
            connector_length = self.FIBONACCI_SPACES[4]  # 55px
            total_width = (len(self.steps) * step_width + 
                          (len(self.steps) - 1) * connector_length)
            
            # Hauteur : étape + label si affiché
            height = self.step_size
            if self.show_labels:
                height += self.FIBONACCI_SPACES[2] + 20  # Espace + hauteur du label
            
            self.setFixedSize(total_width, height)
        else:
            # Largeur : étape + label si affiché
            width = self.step_size
            if self.show_labels:
                # Calcul de la largeur maximale des labels
                font = QFont()
                font.setPointSize(10)
                metrics = QFontMetrics(font)
                max_label_width = max(metrics.horizontalAdvance(step) for step in self.steps)
                width += self.FIBONACCI_SPACES[1] + max_label_width
            
            # Hauteur : étapes + connecteurs
            step_height = self.step_size
            connector_length = self.FIBONACCI_SPACES[3]  # 34px
            total_height = (len(self.steps) * step_height + 
                           (len(self.steps) - 1) * connector_length)
            
            self.setFixedSize(width, total_height)
    
    def _apply_stepper_style(self):
        """Applique le style maritime au stepper."""
        style = f"""
        ProgressStepper {{
            background-color: transparent;
        }}
        """
        self.setStyleSheet(style)
    
    def paintEvent(self, event):
        """Rendu personnalisé du stepper."""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.orientation == self.ORIENTATION_HORIZONTAL:
            self._paint_horizontal(painter)
        else:
            self._paint_vertical(painter)
    
    def _paint_horizontal(self, painter: QPainter):
        """Rendu horizontal du stepper."""
        step_width = self.step_size
        connector_length = self.FIBONACCI_SPACES[4]
        y_center = self.step_size // 2
        
        x_offset = 0
        
        for i, step in enumerate(self.steps):
            # Position de l'étape
            step_x = x_offset
            step_y = 0
            step_rect = QRect(step_x, step_y, step_width, self.step_size)
            
            # Rendu de l'étape
            self._paint_step(painter, step_rect, i)
            
            # Rendu du connecteur (sauf pour la dernière étape)
            if i < len(self.steps) - 1:
                connector_x = step_x + step_width
                connector_y = y_center - self.connector_width // 2
                connector_rect = QRect(connector_x, connector_y, 
                                     connector_length, self.connector_width)
                self._paint_connector(painter, connector_rect, i)
            
            # Rendu du label si activé
            if self.show_labels:
                label_y = self.step_size + self.FIBONACCI_SPACES[0]
                label_rect = QRect(step_x, label_y, step_width, 20)
                self._paint_label(painter, label_rect, step, i)
            
            x_offset += step_width + connector_length
    
    def _paint_vertical(self, painter: QPainter):
        """Rendu vertical du stepper."""
        step_height = self.step_size
        connector_length = self.FIBONACCI_SPACES[3]
        x_center = self.step_size // 2
        
        y_offset = 0
        
        for i, step in enumerate(self.steps):
            # Position de l'étape
            step_x = 0
            step_y = y_offset
            step_rect = QRect(step_x, step_y, self.step_size, step_height)
            
            # Rendu de l'étape
            self._paint_step(painter, step_rect, i)
            
            # Rendu du connecteur (sauf pour la dernière étape)
            if i < len(self.steps) - 1:
                connector_x = x_center - self.connector_width // 2
                connector_y = step_y + step_height
                connector_rect = QRect(connector_x, connector_y, 
                                     self.connector_width, connector_length)
                self._paint_connector(painter, connector_rect, i)
            
            # Rendu du label si activé
            if self.show_labels:
                label_x = self.step_size + self.FIBONACCI_SPACES[0]
                label_y = step_y + (step_height - 20) // 2
                label_rect = QRect(label_x, label_y, 200, 20)
                self._paint_label(painter, label_rect, step, i)
            
            y_offset += step_height + connector_length
    
    def _paint_step(self, painter: QPainter, rect: QRect, step_index: int):
        """Rendu d'une étape individuelle."""
        state = self.step_states[step_index]
        
        # Couleurs selon l'état
        colors = {
            self.STATE_PENDING: {
                'bg': QColor(self.MARITIME_COLORS['frost_light']),
                'border': QColor(self.MARITIME_COLORS['slate_gray']),
                'text': QColor(self.MARITIME_COLORS['slate_gray'])
            },
            self.STATE_ACTIVE: {
                'bg': QColor(self.MARITIME_COLORS['harbor_blue']),
                'border': QColor(self.MARITIME_COLORS['steel_blue']),
                'text': QColor(self.MARITIME_COLORS['foam_white'])
            },
            self.STATE_COMPLETED: {
                'bg': QColor(self.MARITIME_COLORS['emerald_success']),
                'border': QColor(self.MARITIME_COLORS['emerald_success']),
                'text': QColor(self.MARITIME_COLORS['foam_white'])
            },
            self.STATE_ERROR: {
                'bg': QColor(self.MARITIME_COLORS['coral_alert']),
                'border': QColor(self.MARITIME_COLORS['coral_alert']),
                'text': QColor(self.MARITIME_COLORS['foam_white'])
            }
        }
        
        step_colors = colors[state]
        
        # Animation de pulsation pour l'étape active
        if state == self.STATE_ACTIVE:
            pulse_factor = 0.5 + 0.5 * abs(1 - 2 * self._animation_progress)
            step_colors['bg'].setAlphaF(pulse_factor)
        
        # Dessin du cercle de l'étape
        painter.setBrush(QBrush(step_colors['bg']))
        painter.setPen(QPen(step_colors['border'], 2))
        painter.drawEllipse(rect)
        
        # Dessin du contenu (numéro ou icône)
        if self.show_numbers:
            if state == self.STATE_COMPLETED:
                # Icône de validation (✓)
                painter.setPen(QPen(step_colors['text'], 3))
                check_size = rect.width() // 3
                check_x = rect.center().x() - check_size // 2
                check_y = rect.center().y() - check_size // 4
                
                painter.drawLine(check_x, check_y, 
                               check_x + check_size // 2, check_y + check_size // 2)
                painter.drawLine(check_x + check_size // 2, check_y + check_size // 2,
                               check_x + check_size, check_y - check_size // 2)
            elif state == self.STATE_ERROR:
                # Icône d'erreur (✗)
                painter.setPen(QPen(step_colors['text'], 3))
                cross_size = rect.width() // 3
                cross_x = rect.center().x() - cross_size // 2
                cross_y = rect.center().y() - cross_size // 2
                
                painter.drawLine(cross_x, cross_y, 
                               cross_x + cross_size, cross_y + cross_size)
                painter.drawLine(cross_x + cross_size, cross_y,
                               cross_x, cross_y + cross_size)
            else:
                # Numéro de l'étape
                font = QFont()
                font.setPointSize(12)
                font.setWeight(QFont.Weight.Bold)
                painter.setFont(font)
                painter.setPen(QPen(step_colors['text']))
                
                number_text = str(step_index + 1)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, number_text)
    
    def _paint_connector(self, painter: QPainter, rect: QRect, step_index: int):
        """Rendu d'un connecteur entre étapes."""
        # Couleur selon l'état de l'étape suivante
        next_state = self.step_states[step_index + 1] if step_index + 1 < len(self.step_states) else self.STATE_PENDING
        
        if next_state in [self.STATE_COMPLETED, self.STATE_ACTIVE]:
            color = QColor(self.MARITIME_COLORS['harbor_blue'])
        else:
            color = QColor(self.MARITIME_COLORS['slate_gray'])
        
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRect(rect)
    
    def _paint_label(self, painter: QPainter, rect: QRect, text: str, step_index: int):
        """Rendu du label d'une étape."""
        state = self.step_states[step_index]
        
        # Couleur du texte selon l'état
        if state == self.STATE_ACTIVE:
            color = QColor(self.MARITIME_COLORS['harbor_blue'])
        elif state == self.STATE_COMPLETED:
            color = QColor(self.MARITIME_COLORS['emerald_success'])
        elif state == self.STATE_ERROR:
            color = QColor(self.MARITIME_COLORS['coral_alert'])
        else:
            color = QColor(self.MARITIME_COLORS['slate_gray'])
        
        # Configuration de la police
        font = QFont()
        font.setPointSize(10)
        if state in [self.STATE_ACTIVE, self.STATE_COMPLETED]:
            font.setWeight(QFont.Weight.Bold)
        
        painter.setFont(font)
        painter.setPen(QPen(color))
        
        # Alignement selon l'orientation
        if self.orientation == self.ORIENTATION_HORIZONTAL:
            alignment = Qt.AlignmentFlag.AlignCenter
        else:
            alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        
        painter.drawText(rect, alignment, text)
    
    def mousePressEvent(self, event):
        """Gestion du clic sur une étape."""
        super().mousePressEvent(event)
        
        if not self.clickable or event.button() != Qt.MouseButton.LeftButton:
            return
        
        # Détection de l'étape cliquée
        clicked_step = self._get_step_at_position(event.pos())
        if clicked_step >= 0:
            self.step_clicked.emit(clicked_step)
    
    def _get_step_at_position(self, pos) -> int:
        """Retourne l'index de l'étape à la position donnée."""
        if self.orientation == self.ORIENTATION_HORIZONTAL:
            step_width = self.step_size
            connector_length = self.FIBONACCI_SPACES[4]
            
            x_offset = 0
            for i in range(len(self.steps)):
                step_rect = QRect(x_offset, 0, step_width, self.step_size)
                if step_rect.contains(pos):
                    return i
                x_offset += step_width + connector_length
        else:
            step_height = self.step_size
            connector_length = self.FIBONACCI_SPACES[3]
            
            y_offset = 0
            for i in range(len(self.steps)):
                step_rect = QRect(0, y_offset, self.step_size, step_height)
                if step_rect.contains(pos):
                    return i
                y_offset += step_height + connector_length
        
        return -1
    
    def set_current_step(self, step: int, animate: bool = True):
        """Définit l'étape actuelle."""
        if 0 <= step < len(self.steps) and step != self.current_step:
            # Mise à jour des états
            old_step = self.current_step
            self.current_step = step
            
            # Marquer les étapes précédentes comme complétées
            for i in range(step):
                if self.step_states[i] != self.STATE_ERROR:
                    self.step_states[i] = self.STATE_COMPLETED
            
            # Marquer l'étape actuelle comme active
            self.step_states[step] = self.STATE_ACTIVE
            
            # Marquer les étapes suivantes comme en attente
            for i in range(step + 1, len(self.steps)):
                if self.step_states[i] != self.STATE_ERROR:
                    self.step_states[i] = self.STATE_PENDING
            
            # Animation si demandée
            if animate:
                self._animate_step_change(old_step, step)
            
            # Mise à jour de l'affichage
            self.update()
            
            # Émission du signal
            self.step_changed.emit(step)
            
            # Vérification de la completion
            if step == len(self.steps) - 1:
                QTimer.singleShot(500, self._check_completion)
    
    def set_step_state(self, step: int, state: str):
        """Définit l'état d'une étape spécifique."""
        if 0 <= step < len(self.steps) and state in [self.STATE_PENDING, self.STATE_ACTIVE, 
                                                     self.STATE_COMPLETED, self.STATE_ERROR]:
            self.step_states[step] = state
            self.update()
    
    def next_step(self, animate: bool = True):
        """Passe à l'étape suivante."""
        if self.current_step < len(self.steps) - 1:
            self.set_current_step(self.current_step + 1, animate)
    
    def previous_step(self, animate: bool = True):
        """Revient à l'étape précédente."""
        if self.current_step > 0:
            self.set_current_step(self.current_step - 1, animate)
    
    def reset(self):
        """Remet le stepper à l'état initial."""
        self.current_step = 0
        self.step_states = [self.STATE_PENDING] * len(self.steps)
        self.step_states[0] = self.STATE_ACTIVE
        self.update()
    
    def _animate_step_change(self, old_step: int, new_step: int):
        """Animation lors du changement d'étape."""
        self.progress_animation.setStartValue(0.0)
        self.progress_animation.setEndValue(1.0)
        self.progress_animation.start()
    
    def _check_completion(self):
        """Vérifie si toutes les étapes sont terminées."""
        if all(state == self.STATE_COMPLETED for state in self.step_states):
            self.completed.emit()
    
    def start_pulse(self):
        """Démarre l'animation de pulsation."""
        self.pulse_animation.start()
    
    def stop_pulse(self):
        """Arrête l'animation de pulsation."""
        self.pulse_animation.stop()
        self._animation_progress = 0.0
        self.update()
    
    # Propriétés pour les animations
    def get_animation_progress(self):
        return self._animation_progress
    
    def set_animation_progress(self, progress):
        self._animation_progress = progress
        self.update()
    
    animation_progress = property(get_animation_progress, set_animation_progress)
    
    def get_current_step(self) -> int:
        """Retourne l'étape actuelle."""
        return self.current_step
    
    def get_step_count(self) -> int:
        """Retourne le nombre total d'étapes."""
        return len(self.steps)
    
    def get_step_state(self, step: int) -> str:
        """Retourne l'état d'une étape."""
        if 0 <= step < len(self.steps):
            return self.step_states[step]
        return self.STATE_PENDING
    
    def is_completed(self) -> bool:
        """Retourne True si toutes les étapes sont terminées."""
        return all(state == self.STATE_COMPLETED for state in self.step_states)