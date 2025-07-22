#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phi Layout - Gestionnaire de layouts basés sur le nombre d'or (φ)
CHNeoWave v1.1.0 - Sprint 1

Ce module fournit des layouts et des utilitaires pour créer des interfaces
basées sur les proportions du nombre d'or (φ ≈ 1.618) et la suite de Fibonacci.
"""

import math
from typing import Tuple, List, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QResizeEvent


class PhiConstants:
    """Constantes mathématiques pour les proportions φ"""
    PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749
    PHI_INVERSE = 1 / PHI  # ≈ 0.618033988749
    
    # Suite de Fibonacci
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    
    @classmethod
    def get_phi_dimensions(cls, width: int) -> Tuple[int, int]:
        """Calcule les dimensions φ à partir d'une largeur donnée"""
        height = int(width / cls.PHI)
        return width, height
    
    @classmethod
    def get_phi_dimensions_from_height(cls, height: int) -> Tuple[int, int]:
        """Calcule les dimensions φ à partir d'une hauteur donnée"""
        width = int(height * cls.PHI)
        return width, height
    
    @classmethod
    def get_fibonacci_spacing(cls, index: int) -> int:
        """Retourne l'espacement Fibonacci à l'index donné"""
        if 0 <= index < len(cls.FIBONACCI):
            return cls.FIBONACCI[index]
        return cls.FIBONACCI[-1]  # Retourne le plus grand si index trop grand


class PhiGridLayout(QGridLayout):
    """Layout en grille basé sur les proportions φ"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_phi_spacing()
    
    def _setup_phi_spacing(self):
        """Configure les espacements basés sur Fibonacci"""
        spacing = PhiConstants.get_fibonacci_spacing(5)  # 8px
        self.setSpacing(spacing)
        
        # Marges basées sur Fibonacci
        margin = PhiConstants.get_fibonacci_spacing(6)  # 13px
        self.setContentsMargins(margin, margin, margin, margin)
    
    def add_phi_widget(self, widget: QWidget, row: int, col: int, 
                      width_ratio: float = 1.0, height_ratio: float = 1.0):
        """Ajoute un widget avec des proportions φ"""
        self.addWidget(widget, row, col)
        
        # Configure la politique de taille pour respecter φ
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Définit les ratios de colonnes/lignes
        self.setColumnStretch(col, int(width_ratio * 100))
        self.setRowStretch(row, int(height_ratio * 100))


class PhiVBoxLayout(QVBoxLayout):
    """Layout vertical basé sur les proportions φ"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_phi_spacing()
    
    def _setup_phi_spacing(self):
        """Configure les espacements basés sur Fibonacci"""
        spacing = PhiConstants.get_fibonacci_spacing(6)  # 13px
        self.setSpacing(spacing)
        
        # Marges basées sur Fibonacci
        margin = PhiConstants.get_fibonacci_spacing(7)  # 21px
        self.setContentsMargins(margin, margin, margin, margin)
    
    def add_phi_section(self, widget: QWidget, stretch_factor: int = 1):
        """Ajoute une section avec un facteur d'étirement basé sur φ"""
        self.addWidget(widget, stretch_factor)
    
    def add_phi_spacer(self, fibonacci_index: int = 5):
        """Ajoute un espaceur basé sur Fibonacci"""
        size = PhiConstants.get_fibonacci_spacing(fibonacci_index)
        spacer = QSpacerItem(0, size, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.addItem(spacer)


class PhiHBoxLayout(QHBoxLayout):
    """Layout horizontal basé sur les proportions φ"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_phi_spacing()
    
    def _setup_phi_spacing(self):
        """Configure les espacements basés sur Fibonacci"""
        spacing = PhiConstants.get_fibonacci_spacing(6)  # 13px
        self.setSpacing(spacing)
        
        # Marges basées sur Fibonacci
        margin = PhiConstants.get_fibonacci_spacing(7)  # 21px
        self.setContentsMargins(margin, margin, margin, margin)
    
    def add_phi_section(self, widget: QWidget, stretch_factor: int = 1):
        """Ajoute une section avec un facteur d'étirement basé sur φ"""
        self.addWidget(widget, stretch_factor)
    
    def add_golden_ratio_sections(self, widget1: QWidget, widget2: QWidget):
        """Ajoute deux widgets dans un ratio φ (1:φ)"""
        self.addWidget(widget1, 100)  # Section plus petite
        self.addWidget(widget2, 162)  # Section plus grande (φ * 100)
    
    def add_phi_spacer(self, fibonacci_index: int = 5):
        """Ajoute un espaceur basé sur Fibonacci"""
        size = PhiConstants.get_fibonacci_spacing(fibonacci_index)
        spacer = QSpacerItem(size, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.addItem(spacer)


class PhiWidget(QWidget):
    """Widget de base qui maintient automatiquement les proportions φ"""
    
    def __init__(self, parent: Optional[QWidget] = None, 
                 maintain_ratio: bool = True):
        super().__init__(parent)
        self.maintain_ratio = maintain_ratio
        self._setup_phi_properties()
    
    def _setup_phi_properties(self):
        """Configure les propriétés φ du widget"""
        if self.maintain_ratio:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def resizeEvent(self, event: QResizeEvent):
        """Maintient les proportions φ lors du redimensionnement"""
        if self.maintain_ratio:
            new_size = event.size()
            width = new_size.width()
            
            # Calcule la hauteur φ
            phi_height = int(width / PhiConstants.PHI)
            
            # Redimensionne si nécessaire
            if abs(new_size.height() - phi_height) > 5:  # Tolérance de 5px
                self.resize(width, phi_height)
                return
        
        super().resizeEvent(event)
    
    def sizeHint(self) -> QSize:
        """Retourne une taille suggérée basée sur φ"""
        if self.maintain_ratio:
            # Taille par défaut basée sur Fibonacci
            width = PhiConstants.get_fibonacci_spacing(12)  # 233px
            height = int(width / PhiConstants.PHI)  # ≈ 144px
            return QSize(width, height)
        return super().sizeHint()


class DashboardPhiLayout(PhiGridLayout):
    """Layout spécialisé pour le dashboard avec proportions φ"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_dashboard_grid()
    
    def _setup_dashboard_grid(self):
        """Configure la grille du dashboard"""
        # Espacement spécial pour le dashboard
        dashboard_spacing = PhiConstants.get_fibonacci_spacing(7)  # 21px
        self.setSpacing(dashboard_spacing)
        
        # Marges du dashboard
        dashboard_margin = PhiConstants.get_fibonacci_spacing(8)  # 34px
        self.setContentsMargins(
            dashboard_margin, dashboard_margin, 
            dashboard_margin, dashboard_margin
        )
    
    def add_dashboard_card(self, card_widget: QWidget, row: int, col: int,
                          row_span: int = 1, col_span: int = 1):
        """Ajoute une carte au dashboard avec proportions φ"""
        self.addWidget(card_widget, row, col, row_span, col_span)
        
        # Configure les proportions φ pour la carte
        card_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Définit les ratios basés sur φ
        phi_ratio = int(PhiConstants.PHI * 100)
        self.setColumnStretch(col, phi_ratio)
        self.setRowStretch(row, 100)
    
    def setup_three_column_layout(self):
        """Configure un layout à 3 colonnes avec proportions φ"""
        # Colonne 1: ratio 1
        self.setColumnStretch(0, 100)
        # Colonne 2: ratio φ
        self.setColumnStretch(1, int(PhiConstants.PHI * 100))
        # Colonne 3: ratio 1
        self.setColumnStretch(2, 100)


def create_phi_layout(layout_type: str = "grid", **kwargs) -> QGridLayout:
    """Factory function pour créer des layouts φ"""
    layout_map = {
        "grid": PhiGridLayout,
        "vbox": PhiVBoxLayout,
        "hbox": PhiHBoxLayout,
        "dashboard": DashboardPhiLayout
    }
    
    layout_class = layout_map.get(layout_type, PhiGridLayout)
    return layout_class(**kwargs)


def calculate_phi_grid_positions(total_items: int) -> List[Tuple[int, int]]:
    """Calcule les positions optimales dans une grille φ"""
    positions = []
    
    # Calcule le nombre de colonnes basé sur φ
    cols = max(1, int(math.sqrt(total_items * PhiConstants.PHI)))
    
    for i in range(total_items):
        row = i // cols
        col = i % cols
        positions.append((row, col))
    
    return positions