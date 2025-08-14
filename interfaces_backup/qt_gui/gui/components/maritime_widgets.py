# -*- coding: utf-8 -*-
"""
CHNeoWave Maritime Design System - Widgets Standardisés
Composants UI industriels pour laboratoires océaniques
Certifiés normes maritimes internationales
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal, QRect
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QPen

# Alias pour compatibilité
pyqtSignal = Signal
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)

# MaritimeCard supprimée - utiliser celle de maritime_card.py
# Import depuis le module maritime_widgets
try:
    from ..widgets.maritime import MaritimeCard
except ImportError:
    # Fallback si le module maritime n'est pas disponible
    MaritimeCard = QFrame


class KPIIndicator(MaritimeCard):
    """
    Indicateur KPI maritime avec valeur numérique et label.
    Optimisé pour l'affichage de métriques temps réel.
    """
    
    def __init__(self, 
                 label: str,
                 value: Union[str, int, float] = "--",
                 unit: str = "",
                 status: str = "normal",
                 parent: Optional[QWidget] = None):
        
        self.label_text = label
        self.value_text = str(value)
        self.unit_text = unit
        self.status = status  # normal, warning, error, success
        
        # Initialisation des attributs avant l'appel au constructeur parent
        self.title = ""
        self.content = ""
        # Appel du constructeur parent avec seulement le parent
        super().__init__(parent)
        
    def _setup_ui(self):
        """Configuration spécifique pour KPI."""
        self.setObjectName("KPIIndicator")
        self.setFixedSize(323, 200)  # Golden Ratio
        
        # Layout principal centré
        layout = QVBoxLayout(self)
        layout.setContentsMargins(21, 21, 21, 21)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Valeur principale
        self.value_label = QLabel(self.value_text)
        self.value_label.setObjectName("kpi-value")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setFont(self._get_value_font())
        layout.addWidget(self.value_label)
        
        # Unité (si présente)
        if self.unit_text:
            self.unit_label = QLabel(self.unit_text)
            self.unit_label.setObjectName("kpi-unit")
            self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.unit_label.setFont(self._get_unit_font())
            layout.addWidget(self.unit_label)
        
        # Label descriptif
        self.desc_label = QLabel(self.label_text)
        self.desc_label.setObjectName("kpi-label")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setFont(self._get_label_font())
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        self._apply_kpi_style()
        
    def _apply_kpi_style(self):
        """Application du style KPI avec couleurs de statut."""
        # Utilisation des classes CSS du design system maritime
        self.setProperty("class", "KPIIndicator")
        
        # Configuration des classes CSS pour les labels
        self.value_label.setProperty("class", "kpi-value")
        if hasattr(self, 'unit_label'):
            self.unit_label.setProperty("class", "kpi-unit")
        self.desc_label.setProperty("class", "kpi-label")
        
        # Application du statut via propriété CSS
        self.setProperty("status", self.status)
        
    def _get_value_font(self) -> QFont:
        """Police pour la valeur principale."""
        font = QFont("Inter", 32)
        font.setWeight(QFont.Weight.Bold)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 98)  # -2%
        return font
        
    def _get_unit_font(self) -> QFont:
        """Police pour l'unité."""
        font = QFont("Inter", 16)
        font.setWeight(QFont.Weight.Normal)
        return font
        
    def _get_label_font(self) -> QFont:
        """Police pour le label."""
        font = QFont("Inter", 14)
        font.setWeight(QFont.Weight.Normal)
        return font
        
    def update_value(self, value: Union[str, int, float], unit: str = None):
        """Mise à jour de la valeur avec animation."""
        self.value_text = str(value)
        self.value_label.setText(self.value_text)
        
        if unit is not None:
            self.unit_text = unit
            if hasattr(self, 'unit_label'):
                self.unit_label.setText(unit)
                
    def update_status(self, status: str):
        """Mise à jour du statut avec changement de couleur."""
        self.status = status
        self._apply_kpi_style()


class StatusBeacon(QWidget):
    """
    Indicateur d'état maritime avec animation de pulsation.
    Utilisé pour les statuts système et équipements.
    """
    
    def __init__(self, 
                 status: str = "inactive",
                 size: int = 12,
                 animated: bool = True,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.status = status  # active, warning, error, inactive
        self.beacon_size = size
        self.animated = animated
        
        self._setup_ui()
        self._setup_animation()
        
    def _setup_ui(self):
        """Configuration de l'interface."""
        self.setObjectName("StatusBeacon")
        self.setFixedSize(self.beacon_size, self.beacon_size)
        self._apply_beacon_style()
        
    def _setup_animation(self):
        """Configuration de l'animation de pulsation."""
        if self.animated and self.status == "active":
            # Animation de pulsation pour les statuts actifs
            self.pulse_animation = QPropertyAnimation(self, b"windowOpacity")
            self.pulse_animation.setDuration(2000)
            self.pulse_animation.setStartValue(1.0)
            self.pulse_animation.setEndValue(0.7)
            self.pulse_animation.setLoopCount(-1)  # Infini
            self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
            self.pulse_animation.start()
            
    def _apply_beacon_style(self):
        """Application du style avec couleurs de statut."""
        # Utilisation des classes CSS du design system maritime
        self.setProperty("class", "StatusBeacon")
        self.setProperty("status", self.status)
        self.setProperty("size", str(self.beacon_size))
        
    def update_status(self, status: str):
        """Mise à jour du statut."""
        self.status = status
        self._apply_beacon_style()
        
        # Redémarrer l'animation si nécessaire
        if hasattr(self, 'pulse_animation'):
            self.pulse_animation.stop()
            
        if self.animated and status == "active":
            self._setup_animation()


class MaritimeButton(QPushButton):
    """
    Bouton maritime standardisé avec animations et états.
    Respecte les normes d'accessibilité et de contraste.
    """
    
    def __init__(self, 
                 text: str,
                 button_type: str = "primary",  # primary, secondary
                 size: str = "normal",  # small, normal, large
                 parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        
        self.button_type = button_type
        self.size = size
        
        self._setup_ui()
        self._setup_animations()
        
    def _setup_ui(self):
        """Configuration de l'interface."""
        self.setObjectName(f"{self.button_type.title()}Button")
        
        # Tailles standardisées
        size_configs = {
            "small": {"height": 36, "padding": "8px 13px", "font_size": 12},
            "normal": {"height": 44, "padding": "13px 21px", "font_size": 14},
            "large": {"height": 52, "padding": "16px 34px", "font_size": 16}
        }
        
        config = size_configs.get(self.size, size_configs["normal"])
        self.setMinimumHeight(config["height"])
        self.setMinimumWidth(120)
        
        # Police
        font = QFont("Inter", config["font_size"])
        font.setWeight(QFont.Weight.Medium)
        self.setFont(font)
        
        self._apply_button_style(config)
        
    def _apply_button_style(self, config):
        """Application du style selon le type."""
        # Utilisation des classes CSS du design system maritime
        self.setProperty("class", f"{self.button_type.title()}Button")
        self.setProperty("size", self.size)
            
    def _setup_animations(self):
        """Configuration des animations de bouton."""
        # Animation de scale au clic
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(100)  # transition-micro
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def mousePressEvent(self, event):
        """Animation au clic."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Légère réduction de taille
            current_rect = self.geometry()
            scaled_rect = QRect(
                current_rect.x() + 1, current_rect.y() + 1,
                current_rect.width() - 2, current_rect.height() - 2
            )
            
            self.scale_animation.setStartValue(current_rect)
            self.scale_animation.setEndValue(scaled_rect)
            self.scale_animation.start()
            
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Retour à la taille normale."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Retour à la taille normale
            current_rect = self.geometry()
            normal_rect = QRect(
                current_rect.x() - 1, current_rect.y() - 1,
                current_rect.width() + 2, current_rect.height() + 2
            )
            
            self.scale_animation.setStartValue(current_rect)
            self.scale_animation.setEndValue(normal_rect)
            self.scale_animation.start()
            
        super().mouseReleaseEvent(event)


class ProgressStepper(QWidget):
    """
    Stepper de progression maritime pour workflows complexes.
    Affichage visuel des étapes avec statuts et animations.
    """
    
    def __init__(self, steps: list, current_step: int = 0, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.steps = steps  # Liste des noms d'étapes
        self.current_step = current_step
        self.step_widgets = []
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configuration de l'interface."""
        self.setObjectName("ProgressStepper")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(21, 21, 21, 21)
        layout.setSpacing(13)
        
        for i, step_name in enumerate(self.steps):
            step_widget = self._create_step_widget(step_name, i)
            self.step_widgets.append(step_widget)
            layout.addWidget(step_widget)
            
        self._apply_stepper_style()
        
    def _create_step_widget(self, step_name: str, index: int) -> QWidget:
        """Création d'un widget d'étape."""
        step_widget = QFrame()
        step_widget.setObjectName("StepItem")
        step_widget.setProperty("class", "StepItem")
        
        layout = QHBoxLayout(step_widget)
        layout.setContentsMargins(13, 13, 13, 13)
        layout.setSpacing(13)
        
        # Indicateur de statut
        status_beacon = StatusBeacon(
            status=self._get_step_status(index),
            size=16,
            animated=index == self.current_step
        )
        layout.addWidget(status_beacon)
        
        # Nom de l'étape
        step_label = QLabel(step_name)
        step_label.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        layout.addWidget(step_label)
        
        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)
        
        return step_widget
        
    def _get_step_status(self, index: int) -> str:
        """Détermination du statut d'une étape."""
        if index < self.current_step:
            return "active"  # Complétée (vert)
        elif index == self.current_step:
            return "warning"  # En cours (orange)
        else:
            return "inactive"  # En attente (gris)
            
    def _apply_stepper_style(self):
        """Application du style stepper."""
        # Utilisation des classes CSS du design system maritime
        self.setProperty("class", "ProgressStepper")
        
    def update_current_step(self, step_index: int):
        """Mise à jour de l'étape courante."""
        if 0 <= step_index < len(self.steps):
            self.current_step = step_index
            
            # Mise à jour des statuts
            for i, step_widget in enumerate(self.step_widgets):
                # Trouver le StatusBeacon dans le widget
                for child in step_widget.findChildren(StatusBeacon):
                    child.update_status(self._get_step_status(i))
                    
    def add_step(self, step_name: str):
        """Ajout d'une nouvelle étape."""
        self.steps.append(step_name)
        step_widget = self._create_step_widget(step_name, len(self.steps) - 1)
        self.step_widgets.append(step_widget)
        self.layout().addWidget(step_widget)
        
    def remove_step(self, index: int):
        """Suppression d'une étape."""
        if 0 <= index < len(self.steps):
            self.steps.pop(index)
            widget = self.step_widgets.pop(index)
            widget.deleteLater()
            
            # Réajustement des indices
            if self.current_step >= index:
                self.current_step = max(0, self.current_step - 1)
                
            self.update_current_step(self.current_step)


# Fonctions utilitaires pour l'application du design system

def apply_maritime_theme(app):
    """
    Application du thème maritime à l'application complète.
    """
    try:
        with open("src/hrneowave/gui/styles/maritime_design_system.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        logger.info("Thème maritime appliqué avec succès")
    except FileNotFoundError:
        logger.error("Fichier maritime_design_system.qss introuvable")
    except Exception as e:
        logger.error(f"Erreur lors de l'application du thème maritime: {e}")


def create_kpi_grid(kpis: list, parent: Optional[QWidget] = None) -> QWidget:
    """
    Création d'une grille de KPIs standardisée.
    
    Args:
        kpis: Liste de dictionnaires avec les clés 'label', 'value', 'unit', 'status'
        parent: Widget parent
        
    Returns:
        Widget contenant la grille de KPIs
    """
    grid_widget = QWidget(parent)
    grid_widget.setObjectName("KPIGrid")
    
    # Layout en grille responsive
    layout = QHBoxLayout(grid_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(21)  # space-md
    
    for kpi_data in kpis:
        kpi_widget = KPIIndicator(
            label=kpi_data.get('label', ''),
            value=kpi_data.get('value', '--'),
            unit=kpi_data.get('unit', ''),
            status=kpi_data.get('status', 'normal')
        )
        layout.addWidget(kpi_widget)
        
    # Spacer pour aligner à gauche si moins de KPIs
    spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    layout.addItem(spacer)
    
    return grid_widget


def create_action_bar(actions: list, parent: Optional[QWidget] = None) -> QWidget:
    """
    Création d'une barre d'actions standardisée.
    
    Args:
        actions: Liste de dictionnaires avec les clés 'text', 'type', 'callback'
        parent: Widget parent
        
    Returns:
        Widget contenant la barre d'actions
    """
    action_bar = QWidget(parent)
    action_bar.setObjectName("ActionBar")
    
    layout = QHBoxLayout(action_bar)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(13)  # space-sm
    
    # Spacer pour aligner les boutons à droite
    spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    layout.addItem(spacer)
    
    for action_data in actions:
        button = MaritimeButton(
            text=action_data.get('text', ''),
            button_type=action_data.get('type', 'secondary'),
            size=action_data.get('size', 'normal')
        )
        
        # Connexion du callback si fourni
        callback = action_data.get('callback')
        if callback and callable(callback):
            button.clicked.connect(callback)
            
        layout.addWidget(button)
        
    return action_bar