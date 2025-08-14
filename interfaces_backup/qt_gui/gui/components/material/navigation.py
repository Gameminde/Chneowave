#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Material Design Navigation
Composants de navigation Material Design 3

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

from typing import List, Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Signal, Qt, Property
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor

from .theme import MaterialTheme, MaterialShape


class MaterialNavigationRailItem:
    """Élément de navigation rail"""
    
    def __init__(self, icon: QIcon, label: str, identifier: str = None):
        self.icon = icon
        self.label = label
        self.identifier = identifier or label.lower().replace(' ', '_')
        self.selected = False
        self.badge_count = 0


class MaterialNavigationRail(QWidget):
    """Rail de navigation Material Design 3"""
    
    # Signal émis quand un élément est sélectionné
    itemSelected = Signal(str)  # identifier de l'élément
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = MaterialTheme()
        self.items: List[MaterialNavigationRailItem] = []
        self.buttons: List[QPushButton] = []
        self.selected_index = -1
        self._toggle_position = 0  # Position pour les animations de toggle
        
        self._setup_ui()
        self.apply_style()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        self.setFixedWidth(80)
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 12, 0, 12)
        self.layout.setSpacing(12)
        
        # Conteneur pour les boutons
        self.buttons_container = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_container)
        self.buttons_layout.setContentsMargins(8, 0, 8, 0)
        self.buttons_layout.setSpacing(12)
        
        self.layout.addWidget(self.buttons_container)
        self.layout.addStretch()
    
    def apply_style(self):
        """Applique le style Material Design 3"""
        style = f"""
        QWidget {{
            background-color: {self.theme.surface};
            border-right: 1px solid {self.theme.outline_variant};
        }}
        """
        self.setStyleSheet(style)
    
    def add_item(self, item: MaterialNavigationRailItem):
        """Ajoute un élément de navigation"""
        self.items.append(item)
        
        # Créer le bouton
        button = QPushButton()
        button.setCheckable(True)
        button.setFixedSize(64, 56)
        button.setIcon(item.icon)
        button.setToolTip(item.label)
        
        # Style du bouton
        self._apply_button_style(button, len(self.items) - 1)
        
        # Connexion
        button.clicked.connect(lambda checked, idx=len(self.items) - 1: self._on_item_clicked(idx))
        
        self.buttons.append(button)
        self.buttons_layout.addWidget(button)
    
    def _apply_button_style(self, button: QPushButton, index: int):
        """Applique le style à un bouton de navigation"""
        item = self.items[index]
        is_selected = index == self.selected_index
        
        if is_selected:
            bg_color = self.theme.secondary_container
            icon_color = self.theme.on_secondary_container
        else:
            bg_color = "transparent"
            icon_color = self.theme.on_surface_variant
        
        style = f"""
        QPushButton {{
            background-color: {bg_color};
            border: none;
            border-radius: {MaterialShape.LARGE.value}px;
            padding: 8px;
        }}
        QPushButton:hover {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.08)};
        }}
        QPushButton:pressed {{
            background-color: {self._adjust_color(self.theme.on_surface, 0.12)};
        }}
        """
        
        button.setStyleSheet(style)
        
        # Mettre à jour l'icône avec la bonne couleur
        if hasattr(item, 'icon') and item.icon:
            colored_icon = self._colorize_icon(item.icon, icon_color)
            button.setIcon(colored_icon)
    
    def _colorize_icon(self, icon: QIcon, color: str) -> QIcon:
        """Colorie une icône avec la couleur spécifiée"""
        pixmap = icon.pixmap(24, 24)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(colored_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.SourceOver)
        painter.drawPixmap(0, 0, pixmap)
        
        painter.setCompositionMode(QPainter.CompositionMode.SourceIn)
        painter.fillRect(colored_pixmap.rect(), QColor(color))
        painter.end()
        
        return QIcon(colored_pixmap)
    
    def _adjust_color(self, color: str, opacity: float) -> str:
        """Ajuste la couleur avec une opacité"""
        qcolor = QColor(color)
        qcolor.setAlphaF(opacity)
        return qcolor.name(QColor.NameFormat.HexArgb)
    
    def _on_item_clicked(self, index: int):
        """Gère le clic sur un élément"""
        if index != self.selected_index:
            # Désélectionner l'ancien élément
            if self.selected_index >= 0:
                self.items[self.selected_index].selected = False
                self._apply_button_style(self.buttons[self.selected_index], self.selected_index)
            
            # Sélectionner le nouvel élément
            self.selected_index = index
            self.items[index].selected = True
            self._apply_button_style(self.buttons[index], index)
            
            # Émettre le signal
            self.itemSelected.emit(self.items[index].identifier)
    
    def set_selected_item(self, identifier: str):
        """Sélectionne un élément par son identifiant"""
        for i, item in enumerate(self.items):
            if item.identifier == identifier:
                self._on_item_clicked(i)
                break
    
    @Property(int)
    def toggle_position(self):
        """Retourne la position du toggle pour les animations"""
        return self._toggle_position
    
    @toggle_position.setter
    def toggle_position(self, value: int):
        """Définit la position du toggle pour les animations"""
        self._toggle_position = value
        self.update()
    
    def get_selected_item(self) -> Optional[MaterialNavigationRailItem]:
        """Retourne l'élément sélectionné"""
        if self.selected_index >= 0:
            return self.items[self.selected_index]
        return None
    
    def set_badge_count(self, identifier: str, count: int):
        """Définit le nombre de badges pour un élément"""
        for item in self.items:
            if item.identifier == identifier:
                item.badge_count = count
                # TODO: Implémenter l'affichage du badge
                break
    
    def clear_items(self):
        """Supprime tous les éléments"""
        # Supprimer les boutons
        for button in self.buttons:
            self.buttons_layout.removeWidget(button)
            button.deleteLater()
        
        # Réinitialiser les listes
        self.items.clear()
        self.buttons.clear()
        self.selected_index = -1
    
    def set_theme(self, theme: MaterialTheme):
        """Définit le thème"""
        self.theme = theme
        self.apply_style()
        
        # Réappliquer le style à tous les boutons
        for i, button in enumerate(self.buttons):
            self._apply_button_style(button, i)
    
    def add_separator(self):
        """Ajoute un séparateur visuel"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"""
        QFrame {{
            background-color: {self.theme.outline_variant};
            border: none;
        }}
        """)
        self.buttons_layout.addWidget(separator)
    
    def insert_item(self, index: int, item: MaterialNavigationRailItem):
        """Insère un élément à l'index spécifié"""
        self.items.insert(index, item)
        
        # Créer le bouton
        button = QPushButton()
        button.setCheckable(True)
        button.setFixedSize(64, 56)
        button.setIcon(item.icon)
        button.setToolTip(item.label)
        
        # Style du bouton
        self._apply_button_style(button, index)
        
        # Connexion
        button.clicked.connect(lambda checked, idx=index: self._on_item_clicked(idx))
        
        self.buttons.insert(index, button)
        self.buttons_layout.insertWidget(index, button)
        
        # Mettre à jour les connexions des boutons suivants
        for i in range(index + 1, len(self.buttons)):
            self.buttons[i].clicked.disconnect()
            self.buttons[i].clicked.connect(lambda checked, idx=i: self._on_item_clicked(idx))
    
    def remove_item(self, identifier: str):
        """Supprime un élément par son identifiant"""
        for i, item in enumerate(self.items):
            if item.identifier == identifier:
                # Supprimer le bouton
                button = self.buttons[i]
                self.buttons_layout.removeWidget(button)
                button.deleteLater()
                
                # Supprimer des listes
                self.items.pop(i)
                self.buttons.pop(i)
                
                # Ajuster l'index sélectionné
                if self.selected_index == i:
                    self.selected_index = -1
                elif self.selected_index > i:
                    self.selected_index -= 1
                
                # Mettre à jour les connexions des boutons suivants
                for j in range(i, len(self.buttons)):
                    self.buttons[j].clicked.disconnect()
                    self.buttons[j].clicked.connect(lambda checked, idx=j: self._on_item_clicked(idx))
                
                break