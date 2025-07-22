# -*- coding: utf-8 -*-
"""
Phi Card Component

Composant carte avec proportions basées sur le nombre d'or φ ≈ 1.618.
Utilisé pour créer des interfaces harmonieuses selon les principes du design CHNeoWave.

Auteur: CHNeoWave Team
Version: 1.1.0-RC
Date: 2024-12-19
"""

import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QPushButton, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal
from PySide6.QtGui import QFont, QColor


class PhiCard(QWidget):
    """Carte avec proportions basées sur le nombre d'or φ ≈ 1.618
    
    Tailles disponibles basées sur la suite de Fibonacci:
    - sm: 233×144 px (ratio φ)
    - md: 377×233 px (ratio φ)
    - lg: 610×377 px (ratio φ)
    
    Fonctionnalités:
    - Proportions mathématiquement exactes φ
    - Animations hover avec élévation
    - Contenu flexible (titre, texte, icône)
    - Styles Material Design 3
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
    
    # Signaux
    clicked = Signal()
    
    def __init__(self, title="", content="", size="md", icon="", clickable=False, parent=None):
        super().__init__(parent)
        self.title = title
        self.content = content
        self.size = size
        self.icon = icon
        self.clickable = clickable
        self._hovered = False
        
        # Validation et application des dimensions φ
        self.validate_phi_ratio()
        self.setup_ui()
        self.setup_animations()
        self.setup_shadow_effect()
        
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
        self.setObjectName("phi-card")
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(self.SPACING_MD, self.SPACING_MD, self.SPACING_MD, self.SPACING_MD)
        layout.setSpacing(self.SPACING_SM)
        
        # Header (section supérieure - proportion φ⁻¹)
        header_height = int(self.height() * (1 / self.PHI))  # ≈ 0.618
        header_widget = self.create_header(header_height)
        layout.addWidget(header_widget)
        
        # Content (section inférieure - proportion φ⁻²)
        content_widget = self.create_content()
        layout.addWidget(content_widget)
        
        # Répartition selon φ: 62% header, 38% content
        layout.setStretchFactor(header_widget, 62)  # φ⁻¹ * 100
        layout.setStretchFactor(content_widget, 38)  # (1 - φ⁻¹) * 100
        
        # Rendre cliquable si demandé
        if self.clickable:
            self.setCursor(Qt.PointingHandCursor)
            
    def create_header(self, height):
        """Création de la section header avec icône et titre"""
        header_widget = QWidget()
        header_widget.setMaximumHeight(height)
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(self.SPACING_SM)
        
        # Icône (si fournie)
        if self.icon:
            icon_label = QLabel(self.icon)
            icon_label.setObjectName("phi-card-icon")
            icon_label.setAlignment(Qt.AlignCenter)
            
            # Taille de l'icône basée sur Fibonacci
            icon_size = self.SPACING_LG * 2  # 42px (proche de Fibonacci 34)
            icon_label.setFixedSize(icon_size, icon_size)
            
            # Font size pour emoji
            font = QFont()
            font.setPointSize(24)
            icon_label.setFont(font)
            
            header_layout.addWidget(icon_label)
            
        # Titre
        if self.title:
            title_label = QLabel(self.title)
            title_label.setObjectName("phi-card-title")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setWordWrap(True)
            
            # Font du titre
            title_font = QFont()
            title_font.setWeight(QFont.Bold)
            title_font.setPointSize(14 if self.size == "lg" else 12)
            title_label.setFont(title_font)
            
            header_layout.addWidget(title_label)
            
        # Spacer pour centrer verticalement
        header_layout.addStretch()
        
        return header_widget
        
    def create_content(self):
        """Création de la section contenu"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(self.SPACING_SM)
        
        # Séparateur subtil
        if self.title and self.content:
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setObjectName("phi-card-separator")
            content_layout.addWidget(separator)
            
        # Contenu principal
        if self.content:
            content_label = QLabel(self.content)
            content_label.setObjectName("phi-card-content")
            content_label.setAlignment(Qt.AlignCenter)
            content_label.setWordWrap(True)
            
            # Font du contenu
            content_font = QFont()
            content_font.setPointSize(10 if self.size == "sm" else 11)
            content_label.setFont(content_font)
            
            content_layout.addWidget(content_label)
            
        # Spacer pour centrer verticalement
        content_layout.addStretch()
        
        return content_widget
        
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
        self.shadow_effect.setColor(QColor(0, 0, 0, 60))  # Ombre légère
        self.shadow_effect.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
    def enterEvent(self, event):
        """Événement survol - élévation de la carte"""
        super().enterEvent(event)
        if not self._hovered:
            self._hovered = True
            self.animate_elevation(True)
            
    def leaveEvent(self, event):
        """Événement fin survol - retour position normale"""
        super().leaveEvent(event)
        if self._hovered:
            self._hovered = False
            self.animate_elevation(False)
            
    def animate_elevation(self, elevated):
        """Animation d'élévation de la carte"""
        current_rect = self.geometry()
        
        if elevated:
            # Élever la carte de 3px et augmenter l'ombre
            target_rect = QRect(current_rect.x(), current_rect.y() - 3, 
                              current_rect.width(), current_rect.height())
            self.shadow_effect.setBlurRadius(12)
            self.shadow_effect.setOffset(0, 4)
        else:
            # Retour position normale
            target_rect = QRect(current_rect.x(), current_rect.y() + 3, 
                              current_rect.width(), current_rect.height())
            self.shadow_effect.setBlurRadius(8)
            self.shadow_effect.setOffset(0, 2)
            
        self.elevation_animation.setStartValue(current_rect)
        self.elevation_animation.setEndValue(target_rect)
        self.elevation_animation.start()
        
    def mousePressEvent(self, event):
        """Gestion du clic sur la carte"""
        super().mousePressEvent(event)
        if self.clickable and event.button() == Qt.LeftButton:
            self.clicked.emit()
            
    def set_title(self, title):
        """Modifier le titre de la carte"""
        self.title = title
        # Trouver et mettre à jour le label titre
        title_label = self.findChild(QLabel, "phi-card-title")
        if title_label:
            title_label.setText(title)
            
    def set_content(self, content):
        """Modifier le contenu de la carte"""
        self.content = content
        # Trouver et mettre à jour le label contenu
        content_label = self.findChild(QLabel, "phi-card-content")
        if content_label:
            content_label.setText(content)
            
    def set_icon(self, icon):
        """Modifier l'icône de la carte"""
        self.icon = icon
        # Trouver et mettre à jour le label icône
        icon_label = self.findChild(QLabel, "phi-card-icon")
        if icon_label:
            icon_label.setText(icon)
            
    def get_phi_ratio(self):
        """Obtenir le ratio φ actuel de la carte"""
        return self.width() / self.height()
        
    def get_size_info(self):
        """Obtenir les informations de taille"""
        return {
            "size": self.size,
            "width": self.width(),
            "height": self.height(),
            "ratio": self.get_phi_ratio(),
            "phi_exact": self.PHI,
            "ratio_error": abs(self.get_phi_ratio() - self.PHI)
        }
        
    @classmethod
    def create_project_card(cls, project_name="Aucun projet", status="Fermé"):
        """Factory method pour créer une carte projet"""
        return cls(
            title="Projet Actuel",
            content=f"{project_name}\nStatut: {status}",
            size="md",
            icon="📁",
            clickable=True
        )
        
    @classmethod
    def create_acquisition_card(cls, status="Prêt", last_run="Jamais"):
        """Factory method pour créer une carte acquisition"""
        return cls(
            title="Acquisition",
            content=f"Statut: {status}\nDernière: {last_run}",
            size="sm",
            icon="📊",
            clickable=True
        )
        
    @classmethod
    def create_system_card(cls, status="Opérationnel", version="v1.1.0-RC"):
        """Factory method pour créer une carte système"""
        return cls(
            title="Système",
            content=f"Statut: {status}\nVersion: {version}",
            size="sm",
            icon="⚙️",
            clickable=True
        )