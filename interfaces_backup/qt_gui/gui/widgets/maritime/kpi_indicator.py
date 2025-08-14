# -*- coding: utf-8 -*-
"""
KPIIndicator - Indicateur de métriques avec icône
Design System Maritime 2025 - CHNeoWave

Indicateur KPI standardisé avec :
- Valeur numérique proéminente
- Label descriptif
- Icône optionnelle
- Animations de mise à jour
- Proportions Golden Ratio
"""

import sys
from typing import Optional, Union

try:
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
    from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal, QTimer
    from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QPen
except ImportError:
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
    from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal as Signal, QTimer
    from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen

from .maritime_card import MaritimeCard


class KPIIndicator(MaritimeCard):
    """
    Indicateur KPI maritime avec valeur, label et icône.
    
    Caractéristiques :
    - Valeur numérique animée
    - Label descriptif
    - Icône optionnelle
    - Couleurs d'état (normal, warning, error, success)
    - Animations fluides
    """
    
    # Signaux
    value_changed = Signal(float)  # Nouvelle valeur
    threshold_exceeded = Signal(str, float)  # Type seuil, valeur
    
    # Types d'état
    STATE_NORMAL = "normal"
    STATE_WARNING = "warning"
    STATE_ERROR = "error"
    STATE_SUCCESS = "success"
    
    def __init__(self, parent: Optional[QWidget] = None,
                 label: str = "Métrique",
                 value: Union[int, float] = 0,
                 unit: str = "",
                 icon_path: Optional[str] = None,
                 precision: int = 1,
                 state: str = STATE_NORMAL):
        # Initialisation des attributs avant l'appel au constructeur parent
        self.title = ""
        self.content = ""
        # Appel du constructeur parent avec seulement le parent
        super().__init__(parent)
        
        self.label_text = label
        self._current_value = float(value)
        self._target_value = float(value)
        self.unit = unit
        self.icon_path = icon_path
        self.precision = precision
        self.state = state
        
        # Seuils d'alerte
        self.warning_threshold = None
        self.error_threshold = None
        
        # Animation de valeur
        self._setup_value_animation()
        
        # Interface
        self._setup_ui()
        
        # Styles
        self._apply_kpi_style()
    
    def _setup_value_animation(self):
        """Configure l'animation de changement de valeur."""
        # Animation simplifiée sans propriété Qt personnalisée
        self.value_animation = QTimer()
        self.value_animation.timeout.connect(self._animate_step)
        self.animation_steps = 0
        self.animation_total_steps = 20
        self.animation_start_value = 0.0
        self.animation_end_value = 0.0
    
    def _setup_ui(self):
        """Configure l'interface du KPI."""
        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(self.FIBONACCI_SPACES[0])  # 8px
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icône (optionnelle)
        if self.icon_path:
            self.icon_label = QLabel()
            self.icon_label.setObjectName("kpi_icon")
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._load_icon()
            main_layout.addWidget(self.icon_label)
        
        # Valeur principale
        self.value_label = QLabel()
        self.value_label.setObjectName("kpi_value")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_display_value()
        main_layout.addWidget(self.value_label)
        
        # Label descriptif
        self.label_widget = QLabel(self.label_text)
        self.label_widget.setObjectName("kpi_label")
        self.label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_widget.setWordWrap(True)
        main_layout.addWidget(self.label_widget)
        
        # Ajouter le layout au contenu de la card
        content_widget = QWidget()
        content_widget.setLayout(main_layout)
        self.add_widget(content_widget)
    
    def _load_icon(self):
        """Charge l'icône si fournie."""
        if self.icon_path and hasattr(self, 'icon_label'):
            try:
                pixmap = QPixmap(self.icon_path)
                if not pixmap.isNull():
                    # Redimensionner l'icône dynamiquement
                    icon_size = self.FIBONACCI_SPACES[2]  # 21px base
                    scaled_pixmap = pixmap.scaled(
                        icon_size, icon_size, 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.icon_label.setPixmap(scaled_pixmap)
            except Exception as e:
                print(f"Erreur chargement icône KPI: {e}")
    
    def _apply_kpi_style(self):
        """Applique le style maritime au KPI."""
        # Couleurs selon l'état
        value_color = self.MARITIME_COLORS['harbor_blue']
        if self.state == self.STATE_SUCCESS:
            value_color = self.MARITIME_COLORS['emerald_success']
        elif self.state == self.STATE_WARNING:
            value_color = '#FF8F00'
        elif self.state == self.STATE_ERROR:
            value_color = self.MARITIME_COLORS['coral_alert']
        
        style = f"""
        QLabel#kpi_value {{
            font-size: 32px;
            font-weight: 600;
            color: {value_color};

            margin: {self.FIBONACCI_SPACES[0]}px 0;
        }}
        
        QLabel#kpi_label {{
            font-size: 12px;
            font-weight: 400;
            color: {self.MARITIME_COLORS['slate_gray']};
            /* text-transform not supported in Qt */

        }}
        
        QLabel#kpi_icon {{

        }}
        """
        
        self.setStyleSheet(style)
    
    def _update_display_value(self, animated_value: Optional[float] = None):
        """Met à jour l'affichage de la valeur."""
        if animated_value is not None:
            display_value = animated_value
        else:
            display_value = self._current_value
        
        # Formatage selon la précision
        if self.precision == 0:
            formatted_value = f"{int(display_value)}"
        else:
            formatted_value = f"{display_value:.{self.precision}f}"
        
        # Ajout de l'unité
        if self.unit:
            text = f"{formatted_value} {self.unit}"
        else:
            text = formatted_value
        
        if hasattr(self, 'value_label'):
            self.value_label.setText(text)
    
    def _animate_step(self):
        """Étape d'animation pour la transition de valeur."""
        if self.animation_steps >= self.animation_total_steps:
            self.value_animation.stop()
            self._current_value = self.animation_end_value
            self._update_display_value()
            return
        
        # Calcul de la valeur interpolée avec easing
        progress = self.animation_steps / self.animation_total_steps
        # Easing out cubic
        eased_progress = 1 - pow(1 - progress, 3)
        
        interpolated_value = self.animation_start_value + (self.animation_end_value - self.animation_start_value) * eased_progress
        self._update_display_value(interpolated_value)
        
        self.animation_steps += 1
    
    def set_value(self, value: Union[int, float], animate: bool = True):
        """Définit une nouvelle valeur avec animation optionnelle."""
        new_value = float(value)
        
        if animate and abs(new_value - self._current_value) > 0.001:
            # Animation de la valeur
            self._target_value = new_value
            self.animation_start_value = self._current_value
            self.animation_end_value = new_value
            self.animation_steps = 0
            self.value_animation.start(40)  # 40ms interval = 800ms total
        else:
            # Mise à jour directe
            self._current_value = new_value
            self._target_value = new_value
            self._update_display_value()
        
        # Vérification des seuils
        self._check_thresholds(new_value)
        
        # Mise à jour de l'état selon les seuils
        self._update_state_from_value(new_value)
        
        # Émission du signal
        self.value_changed.emit(new_value)
    
    def _check_thresholds(self, value: float):
        """Vérifie si la valeur dépasse les seuils."""
        if self.error_threshold is not None and value >= self.error_threshold:
            self.threshold_exceeded.emit("error", value)
        elif self.warning_threshold is not None and value >= self.warning_threshold:
            self.threshold_exceeded.emit("warning", value)
    
    def _update_state_from_value(self, value: float):
        """Met à jour l'état selon la valeur et les seuils."""
        old_state = self.state
        
        if self.error_threshold is not None and value >= self.error_threshold:
            self.state = self.STATE_ERROR
        elif self.warning_threshold is not None and value >= self.warning_threshold:
            self.state = self.STATE_WARNING
        else:
            self.state = self.STATE_NORMAL
        
        # Réapplication du style si l'état a changé
        if old_state != self.state:
            self._apply_kpi_style()
    
    def set_label(self, label: str):
        """Définit le label descriptif."""
        self.label_text = label
        if hasattr(self, 'label_widget'):
            self.label_widget.setText(label)
    
    def set_unit(self, unit: str):
        """Définit l'unité de mesure."""
        self.unit = unit
        self._update_display_value()
    
    def set_precision(self, precision: int):
        """Définit la précision d'affichage."""
        self.precision = max(0, precision)
        self._update_display_value()
    
    def set_state(self, state: str):
        """Définit l'état du KPI manuellement."""
        if state in [self.STATE_NORMAL, self.STATE_WARNING, self.STATE_ERROR, self.STATE_SUCCESS]:
            self.state = state
            self._apply_kpi_style()
    
    def set_thresholds(self, warning: Optional[float] = None, error: Optional[float] = None):
        """Définit les seuils d'alerte."""
        self.warning_threshold = warning
        self.error_threshold = error
        
        # Réévaluation de l'état actuel
        self._update_state_from_value(self._current_value)
    
    def set_icon(self, icon_path: Optional[str]):
        """Définit ou change l'icône."""
        self.icon_path = icon_path
        if hasattr(self, 'icon_label'):
            if icon_path:
                self._load_icon()
            else:
                self.icon_label.clear()
    
    def get_value(self) -> float:
        """Retourne la valeur actuelle."""
        return self._current_value
    
    def get_state(self) -> str:
        """Retourne l'état actuel."""
        return self.state
    
    def reset(self):
        """Remet le KPI à zéro."""
        self.set_value(0, animate=True)
        self.set_state(self.STATE_NORMAL)
    
    # Propriété pour l'animation
    def get_animated_value(self):
        return self._current_value
    
    def set_animated_value(self, value):
        self._current_value = value
        self._update_display_value(value)
    
    animated_value = property(get_animated_value, set_animated_value)
    
    def sizeHint(self):
        """Taille suggérée pour le KPI (Golden Ratio)."""
        # Largeur basée sur le contenu, hauteur selon Golden Ratio
        base_width = 200
        base_height = int(base_width / self.GOLDEN_RATIO)
        return super().sizeHint().expandedTo(
            self.size().expandedTo(
                self.minimumSize().expandedTo(
                    self.sizeHint().expandedTo(
                        self.size().expandedTo(
                            self.minimumSizeHint()
                        )
                    )
                )
            )
        )