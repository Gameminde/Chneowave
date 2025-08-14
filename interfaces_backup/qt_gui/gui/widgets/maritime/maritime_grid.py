#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MaritimeGrid - Composant de grille responsive pour CHNeoWave

Composant de grille flexible basé sur le Design System Maritime 2025,
avec support du responsive design et des proportions du Nombre d'Or.

Auteur: Architecte Logiciel en Chef
Date: 2025-01-27
Version: 2.0.0
"""

import logging
from typing import Optional, List, Tuple

try:
    from PySide6.QtWidgets import (
        QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
        QSizePolicy, QFrame
    )
    from PySide6.QtCore import Qt, QSize, Signal
    from PySide6.QtGui import QPaintEvent, QPainter, QColor
except ImportError:
    from PyQt5.QtWidgets import (
        QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
        QSizePolicy, QFrame
    )
    from PyQt5.QtCore import Qt, QSize, pyqtSignal as Signal
    from PyQt5.QtGui import QPaintEvent, QPainter, QColor

# Design System Maritime 2025
class MaritimeGridConstants:
    """Constantes pour la grille maritime"""
    
    # Nombre d'Or et Fibonacci
    GOLDEN_RATIO = 1.618
    FIBONACCI_SPACES = [8, 13, 21, 34, 55, 89, 144]
    
    # Espacements
    SPACE_XS = 8
    SPACE_SM = 13
    SPACE_MD = 21
    SPACE_LG = 34
    SPACE_XL = 55
    
    # Couleurs maritimes
    OCEAN_DEEP = "#0A1929"
    HARBOR_BLUE = "#1565C0"
    STEEL_BLUE = "#1976D2"
    TIDAL_CYAN = "#00BCD4"
    FOAM_WHITE = "#FAFBFC"
    FROST_LIGHT = "#F5F7FA"
    STORM_GRAY = "#37474F"
    
    # Breakpoints responsive
    BREAKPOINT_MOBILE = 768
    BREAKPOINT_TABLET = 1024
    BREAKPOINT_DESKTOP = 1440
    
    # Colonnes par breakpoint
    COLUMNS_MOBILE = 1
    COLUMNS_TABLET = 2
    COLUMNS_DESKTOP = 3
    COLUMNS_WIDE = 4


class MaritimeGrid(QFrame):
    """
    Grille responsive maritime avec support du Nombre d'Or
    
    Fonctionnalités:
    - Layout responsive automatique
    - Proportions basées sur le Nombre d'Or
    - Espacement Fibonacci
    - Adaptation automatique au contenu
    - Support des breakpoints
    """
    
    # Signaux
    layout_changed = Signal(int, int)  # colonnes, lignes
    item_added = Signal(QWidget)
    item_removed = Signal(QWidget)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Configuration de base
        self.setObjectName("MaritimeGrid")
        
        # État interne (initialiser avant _setup_properties)
        self._items: List[QWidget] = []
        self._columns = MaritimeGridConstants.COLUMNS_DESKTOP
        self._min_item_width = 280  # Largeur minimale basée sur φ
        self._auto_resize = True
        
        # Configuration des composants
        self._setup_properties()
        self._setup_layout()
        self._setup_styling()
        
        logging.debug("MaritimeGrid initialisé")
    
    def _setup_properties(self):
        """Configuration des propriétés du widget"""
        self.setFrameStyle(QFrame.NoFrame)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )
        
        # Taille minimale basée sur φ
        min_width = int(self._min_item_width * MaritimeGridConstants.GOLDEN_RATIO)
        self.setMinimumSize(QSize(min_width, 200))
    
    def _setup_layout(self):
        """Configuration du layout de grille"""
        self._grid_layout = QGridLayout(self)
        self._grid_layout.setSpacing(MaritimeGridConstants.SPACE_MD)
        self._grid_layout.setContentsMargins(
            MaritimeGridConstants.SPACE_SM,
            MaritimeGridConstants.SPACE_SM,
            MaritimeGridConstants.SPACE_SM,
            MaritimeGridConstants.SPACE_SM
        )
        
        # Alignement et distribution
        self._grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    
    def _setup_styling(self):
        """Application du style maritime"""
        self.setStyleSheet(f"""
            MaritimeGrid {{
                background-color: transparent;
                border: none;
                border-radius: 8px;
            }}
            
            MaritimeGrid:hover {{
                background-color: rgba(21, 101, 192, 0.02);
            }}
        """)
    
    def add_widget(self, widget: QWidget, row: Optional[int] = None, 
                   column: Optional[int] = None) -> Tuple[int, int]:
        """
        Ajoute un widget à la grille
        
        Args:
            widget: Widget à ajouter
            row: Ligne spécifique (optionnel)
            column: Colonne spécifique (optionnel)
            
        Returns:
            Tuple (row, column) de la position finale
        """
        if widget in self._items:
            logging.warning(f"Widget {widget} déjà présent dans la grille")
            return self._get_widget_position(widget)
        
        # Calcul automatique de la position si non spécifiée
        if row is None or column is None:
            row, column = self._calculate_next_position()
        
        # Ajout du widget
        self._grid_layout.addWidget(widget, row, column)
        self._items.append(widget)
        
        # Configuration du widget
        self._configure_grid_item(widget)
        
        # Mise à jour du layout si nécessaire
        if self._auto_resize:
            self._update_layout()
        
        # Émission du signal
        self.item_added.emit(widget)
        
        logging.debug(f"Widget ajouté à la position ({row}, {column})")
        return (row, column)
    
    def remove_widget(self, widget: QWidget) -> bool:
        """
        Supprime un widget de la grille
        
        Args:
            widget: Widget à supprimer
            
        Returns:
            True si supprimé avec succès
        """
        if widget not in self._items:
            logging.warning(f"Widget {widget} non trouvé dans la grille")
            return False
        
        # Suppression du layout et de la liste
        self._grid_layout.removeWidget(widget)
        self._items.remove(widget)
        
        # Mise à jour du layout
        if self._auto_resize:
            self._reorganize_grid()
        
        # Émission du signal
        self.item_removed.emit(widget)
        
        logging.debug(f"Widget supprimé de la grille")
        return True
    
    def set_columns(self, columns: int):
        """
        Définit le nombre de colonnes
        
        Args:
            columns: Nombre de colonnes (1-6)
        """
        columns = max(1, min(6, columns))
        if columns != self._columns:
            self._columns = columns
            self._reorganize_grid()
            logging.debug(f"Nombre de colonnes mis à jour: {columns}")
    
    def set_auto_resize(self, enabled: bool):
        """
        Active/désactive le redimensionnement automatique
        
        Args:
            enabled: True pour activer
        """
        self._auto_resize = enabled
        if enabled:
            self._update_layout()
    
    def set_min_item_width(self, width: int):
        """
        Définit la largeur minimale des éléments
        
        Args:
            width: Largeur minimale en pixels
        """
        self._min_item_width = max(200, width)
        if self._auto_resize:
            self._update_layout()
    
    def clear(self):
        """Supprime tous les widgets de la grille"""
        for widget in self._items.copy():
            self.remove_widget(widget)
    
    def get_grid_info(self) -> dict:
        """
        Retourne les informations de la grille
        
        Returns:
            Dictionnaire avec les informations
        """
        rows = self._grid_layout.rowCount()
        cols = self._grid_layout.columnCount()
        
        return {
            'items_count': len(self._items),
            'columns': self._columns,
            'rows': rows,
            'actual_columns': cols,
            'min_item_width': self._min_item_width,
            'auto_resize': self._auto_resize
        }
    
    def _calculate_next_position(self) -> Tuple[int, int]:
        """Calcule la prochaine position disponible"""
        item_count = len(self._items)
        row = item_count // self._columns
        column = item_count % self._columns
        return (row, column)
    
    def _get_widget_position(self, widget: QWidget) -> Tuple[int, int]:
        """Retourne la position d'un widget dans la grille"""
        index = self._grid_layout.indexOf(widget)
        if index >= 0:
            row, column, _, _ = self._grid_layout.getItemPosition(index)
            return (row, column)
        return (-1, -1)
    
    def _configure_grid_item(self, widget: QWidget):
        """Configure un élément de la grille"""
        # Politique de taille
        widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )
        
        # Taille minimale basée sur φ
        min_height = int(self._min_item_width / MaritimeGridConstants.GOLDEN_RATIO)
        widget.setMinimumSize(QSize(self._min_item_width, min_height))
    
    def _update_layout(self):
        """Met à jour le layout en fonction de la taille"""
        if not self._auto_resize:
            return
        
        # Calcul du nombre optimal de colonnes
        available_width = self.width() - 2 * MaritimeGridConstants.SPACE_SM
        spacing = MaritimeGridConstants.SPACE_MD
        
        # Nombre de colonnes possibles
        possible_columns = max(1, 
            (available_width + spacing) // (self._min_item_width + spacing)
        )
        
        # Limitation selon les breakpoints
        optimal_columns = min(possible_columns, self._columns)
        
        # Réorganisation si nécessaire
        current_columns = self._grid_layout.columnCount()
        if optimal_columns != current_columns and len(self._items) > 0:
            self._reorganize_grid(optimal_columns)
    
    def _reorganize_grid(self, target_columns: Optional[int] = None):
        """Réorganise la grille avec un nouveau nombre de colonnes"""
        if not self._items:
            return
        
        columns = target_columns or self._columns
        
        # Sauvegarde des widgets
        widgets = self._items.copy()
        
        # Nettoyage du layout
        for widget in widgets:
            self._grid_layout.removeWidget(widget)
        
        # Réajout avec nouvelle organisation
        for i, widget in enumerate(widgets):
            row = i // columns
            col = i % columns
            self._grid_layout.addWidget(widget, row, col)
        
        # Émission du signal de changement
        rows = len(widgets) // columns + (1 if len(widgets) % columns else 0)
        self.layout_changed.emit(columns, rows)
    
    def resizeEvent(self, event):
        """Gestion du redimensionnement"""
        super().resizeEvent(event)
        if self._auto_resize:
            self._update_layout()
    
    def sizeHint(self) -> QSize:
        """Taille suggérée basée sur le contenu"""
        if not self._items:
            return QSize(400, 200)
        
        # Calcul basé sur le nombre d'éléments et les colonnes
        rows = len(self._items) // self._columns + (1 if len(self._items) % self._columns else 0)
        
        width = (self._min_item_width * self._columns + 
                MaritimeGridConstants.SPACE_MD * (self._columns - 1) +
                2 * MaritimeGridConstants.SPACE_SM)
        
        height = (int(self._min_item_width / MaritimeGridConstants.GOLDEN_RATIO) * rows +
                 MaritimeGridConstants.SPACE_MD * (rows - 1) +
                 2 * MaritimeGridConstants.SPACE_SM)
        
        return QSize(width, height)


# Alias pour compatibilité
MaritimeGridLayout = MaritimeGrid