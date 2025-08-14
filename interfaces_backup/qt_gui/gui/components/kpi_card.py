# -*- coding: utf-8 -*-
"""
KPI Card Component

Composant carte pour afficher des indicateurs de performance clés (KPI)
avec proportions basées sur le nombre d'or φ ≈ 1.618.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QFont, QColor


class KPICard(QWidget):
    """Carte KPI avec proportions basées sur le nombre d'or φ ≈ 1.618
    
    Affiche un indicateur de performance avec:
    - Valeur principale
    - Unité de mesure
    - Tendance (optionnelle)
    - Statut coloré
    """
    
    # Constante du nombre d'or
    PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749
    
    # Tailles basées sur Fibonacci avec ratio φ exact
    SIZES = {
        "sm": (233, 144),    # 233/144 ≈ 1.618 (φ)
        "md": (377, 233),    # 377/233 ≈ 1.618 (φ)
        "lg": (610, 377)     # 610/377 ≈ 1.618 (φ)
    }
    
    # Espacements Fibonacci
    SPACING_XS = 5
    SPACING_SM = 8
    SPACING_MD = 13
    SPACING_LG = 21
    
    # Statuts KPI
    STATUS_COLORS = {
        "success": "#2E7D32",    # Vert maritime
        "warning": "#F57C00",    # Orange
        "error": "#C62828",      # Rouge
        "info": "#1565C0",       # Bleu océan
        "neutral": "#546E7A"     # Gris maritime
    }
    
    # Signaux
    clicked = Signal()
    
    def __init__(self, title="", value="", unit="", status="neutral", 
                 trend=None, size="sm", clickable=False, parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.unit = unit
        self.status = status
        self.trend = trend  # "+5%", "-2%", etc.
        self.size = size
        self.clickable = clickable
        self._hovered = False
        
        # Validation et application des dimensions φ
        self.validate_phi_ratio()
        self.setup_ui()
        self.setup_animations()
        self.setup_shadow_effect()
        self.apply_styles()
        
    def validate_phi_ratio(self):
        """Validation mathématique du ratio φ"""
        if self.size not in self.SIZES:
            raise ValueError(f"Taille '{self.size}' non supportée. Utilisez: {list(self.SIZES.keys())}")
            
        width, height = self.SIZES[self.size]
        ratio = width / height
        
        # Vérification avec tolérance de 0.01
        if abs(ratio - self.PHI) > 0.01:
            raise ValueError(f"Ratio φ incorrect pour taille '{self.size}': {ratio:.3f} (attendu: {self.PHI:.3f})")
            
        # Application des dimensions
        self.setFixedSize(width, height)
        
    def setup_ui(self):
        """Configuration de l'interface avec proportions φ internes"""
        self.setObjectName("kpi-card")
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(self.SPACING_MD, self.SPACING_MD, self.SPACING_MD, self.SPACING_MD)
        layout.setSpacing(self.SPACING_SM)
        
        # Header avec titre
        if self.title:
            title_label = QLabel(self.title)
            title_label.setObjectName("kpi-card-title")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setWordWrap(True)
            
            # Font du titre
            title_font = QFont()
            title_font.setWeight(QFont.Bold)
            title_font.setPointSize(10 if self.size == "sm" else 12)
            title_label.setFont(title_font)
            
            layout.addWidget(title_label)
            
        # Section valeur principale
        value_widget = self.create_value_section()
        layout.addWidget(value_widget)
        
        # Section tendance (si fournie)
        if self.trend:
            trend_widget = self.create_trend_section()
            layout.addWidget(trend_widget)
            
        # Spacer pour centrer verticalement
        layout.addStretch()
        
        # Rendre cliquable si demandé
        if self.clickable:
            self.setCursor(Qt.PointingHandCursor)
            
    def create_value_section(self):
        """Création de la section valeur principale"""
        value_widget = QWidget()
        value_layout = QVBoxLayout(value_widget)
        value_layout.setContentsMargins(0, 0, 0, 0)
        value_layout.setSpacing(self.SPACING_XS)
        
        # Valeur principale
        value_label = QLabel(str(self.value))
        value_label.setObjectName("kpi-card-value")
        value_label.setAlignment(Qt.AlignCenter)
        
        # Font de la valeur (grande et en gras)
        value_font = QFont()
        value_font.setWeight(QFont.Bold)
        if self.size == "sm":
            value_font.setPointSize(18)
        elif self.size == "md":
            value_font.setPointSize(24)
        else:  # lg
            value_font.setPointSize(32)
        value_label.setFont(value_font)
        
        value_layout.addWidget(value_label)
        
        # Unité (si fournie)
        if self.unit:
            unit_label = QLabel(self.unit)
            unit_label.setObjectName("kpi-card-unit")
            unit_label.setAlignment(Qt.AlignCenter)
            
            # Font de l'unité
            unit_font = QFont()
            unit_font.setPointSize(9 if self.size == "sm" else 11)
            unit_label.setFont(unit_font)
            
            value_layout.addWidget(unit_label)
            
        return value_widget
        
    def create_trend_section(self):
        """Création de la section tendance"""
        trend_widget = QWidget()
        trend_layout = QHBoxLayout(trend_widget)
        trend_layout.setContentsMargins(0, 0, 0, 0)
        trend_layout.setSpacing(self.SPACING_XS)
        
        # Icône de tendance
        if self.trend.startswith("+"):
            trend_icon = "↗"
            trend_color = self.STATUS_COLORS["success"]
        elif self.trend.startswith("-"):
            trend_icon = "↘"
            trend_color = self.STATUS_COLORS["error"]
        else:
            trend_icon = "→"
            trend_color = self.STATUS_COLORS["neutral"]
            
        # Label icône
        icon_label = QLabel(trend_icon)
        icon_label.setObjectName("kpi-card-trend-icon")
        icon_label.setStyleSheet(f"color: {trend_color};")
        
        # Label tendance
        trend_label = QLabel(self.trend)
        trend_label.setObjectName("kpi-card-trend")
        trend_label.setStyleSheet(f"color: {trend_color};")
        
        # Font de la tendance
        trend_font = QFont()
        trend_font.setPointSize(8 if self.size == "sm" else 10)
        trend_font.setWeight(QFont.Bold)
        icon_label.setFont(trend_font)
        trend_label.setFont(trend_font)
        
        # Centrer horizontalement
        trend_layout.addStretch()
        trend_layout.addWidget(icon_label)
        trend_layout.addWidget(trend_label)
        trend_layout.addStretch()
        
        return trend_widget
        
    def setup_animations(self):
        """Configuration des animations hover"""
        # Animation d'élévation (translation Y)
        self.elevation_animation = QPropertyAnimation(self, b"geometry")
        self.elevation_animation.setDuration(200)  # Transition rapide
        self.elevation_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def setup_shadow_effect(self):
        """Configuration de l'effet d'ombre"""
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(8)
        self.shadow_effect.setXOffset(0)
        self.shadow_effect.setYOffset(2)
        self.shadow_effect.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(self.shadow_effect)
        
    def apply_styles(self):
        """Application des styles CSS"""
        status_color = self.STATUS_COLORS.get(self.status, self.STATUS_COLORS["neutral"])
        
        self.setStyleSheet(f"""
            QWidget#kpi-card {{
                background-color: white;
                border: 2px solid {status_color};
                border-radius: 12px;
                padding: 8px;
            }}
            
            QWidget#kpi-card:hover {{
                border-color: {status_color};
                background-color: #f8f9fa;
            }}
            
            QLabel#kpi-card-title {{
                color: #37474f;
                font-weight: bold;
            }}
            
            QLabel#kpi-card-value {{
                color: {status_color};
                font-weight: bold;
            }}
            
            QLabel#kpi-card-unit {{
                color: #78909c;
            }}
        """)
        
    def enterEvent(self, event):
        """Animation d'entrée de la souris"""
        if not self._hovered:
            self._hovered = True
            # Légère élévation
            current_rect = self.geometry()
            target_rect = current_rect.adjusted(0, -2, 0, -2)
            
            self.elevation_animation.setStartValue(current_rect)
            self.elevation_animation.setEndValue(target_rect)
            self.elevation_animation.start()
            
            # Ombre plus prononcée
            self.shadow_effect.setBlurRadius(12)
            self.shadow_effect.setYOffset(4)
            
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Animation de sortie de la souris"""
        if self._hovered:
            self._hovered = False
            # Retour à la position normale
            current_rect = self.geometry()
            target_rect = current_rect.adjusted(0, 2, 0, 2)
            
            self.elevation_animation.setStartValue(current_rect)
            self.elevation_animation.setEndValue(target_rect)
            self.elevation_animation.start()
            
            # Ombre normale
            self.shadow_effect.setBlurRadius(8)
            self.shadow_effect.setYOffset(2)
            
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        """Gestion du clic"""
        if self.clickable and event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
        
    def update_value(self, value, unit=None, trend=None, status=None):
        """Mise à jour des valeurs du KPI"""
        self.value = value
        if unit is not None:
            self.unit = unit
        if trend is not None:
            self.trend = trend
        if status is not None:
            self.status = status
            
        # Reconstruire l'interface
        self.setup_ui()
        self.apply_styles()