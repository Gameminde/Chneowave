#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de graphiques modernisés pour CHNeoWave - Phase 6
Palette maritime appliquée à pyqtgraph avec animations fluides
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, QObject
from PySide6.QtGui import QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QWidget

try:
    import pyqtgraph as pg
    import numpy as np
except ImportError:
    pg = None
    np = None

logger = logging.getLogger(__name__)

# Palette maritime pour graphiques
MARITIME_GRAPH_COLORS = {
    'ocean_deep': '#0A1929',
    'harbor_blue': '#1565C0', 
    'steel_blue': '#1976D2',
    'tidal_cyan': '#00BCD4',
    'foam_white': '#FAFBFC',
    'storm_gray': '#37474F',
    'coral_alert': '#FF5722',
    'emerald_success': '#4CAF50',
    'amber_warning': '#FF9800',
    'deep_purple': '#673AB7'
}

# Courbes de données par défaut
DEFAULT_CURVE_COLORS = [
    MARITIME_GRAPH_COLORS['harbor_blue'],
    MARITIME_GRAPH_COLORS['tidal_cyan'],
    MARITIME_GRAPH_COLORS['emerald_success'],
    MARITIME_GRAPH_COLORS['coral_alert'],
    MARITIME_GRAPH_COLORS['amber_warning'],
    MARITIME_GRAPH_COLORS['deep_purple']
]

class MaritimeGraphStyle:
    """Configuration de style maritime pour graphiques pyqtgraph"""
    
    @staticmethod
    def get_background_color() -> str:
        """Couleur de fond des graphiques"""
        return MARITIME_GRAPH_COLORS['foam_white']
    
    @staticmethod
    def get_foreground_color() -> str:
        """Couleur de premier plan (texte, axes)"""
        return MARITIME_GRAPH_COLORS['ocean_deep']
    
    @staticmethod
    def get_grid_color() -> str:
        """Couleur de la grille"""
        return MARITIME_GRAPH_COLORS['storm_gray']
    
    @staticmethod
    def get_axis_pen() -> QPen:
        """Style des axes"""
        pen = QPen(QColor(MARITIME_GRAPH_COLORS['ocean_deep']))
        pen.setWidth(2)
        return pen
    
    @staticmethod
    def get_grid_pen() -> QPen:
        """Style de la grille"""
        pen = QPen(QColor(MARITIME_GRAPH_COLORS['storm_gray']))
        pen.setWidth(1)
        pen.setStyle(2)  # Ligne pointillée
        return pen
    
    @staticmethod
    def get_curve_pen(color_index: int = 0, width: int = 2) -> QPen:
        """Style des courbes de données"""
        color = DEFAULT_CURVE_COLORS[color_index % len(DEFAULT_CURVE_COLORS)]
        pen = QPen(QColor(color))
        pen.setWidth(width)
        return pen
    
    @staticmethod
    def get_font() -> QFont:
        """Police pour les labels"""
        font = QFont("Segoe UI", 10)
        font.setWeight(QFont.Weight.Normal)
        return font

class AnimatedPlotWidget(pg.PlotWidget):
    """Widget de graphique avec animations maritimes"""
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configuration du style maritime
        self._apply_maritime_style()
        
        # Système d'animations
        self._setup_animations()
        
        # Données et courbes
        self.curves = {}
        self.curve_colors = {}
        
        logger.info("AnimatedPlotWidget initialisé avec style maritime")
    
    def _apply_maritime_style(self):
        """Applique le style maritime au graphique"""
        # Couleurs de fond
        self.setBackground(MaritimeGraphStyle.get_background_color())
        
        # Style des axes
        axis_pen = MaritimeGraphStyle.get_axis_pen()
        grid_pen = MaritimeGraphStyle.get_grid_pen()
        font = MaritimeGraphStyle.get_font()
        
        # Configuration des axes
        for axis_name in ['left', 'bottom', 'right', 'top']:
            axis = self.getAxis(axis_name)
            axis.setPen(axis_pen)
            axis.setTextPen(MaritimeGraphStyle.get_foreground_color())
            axis.setTickFont(font)
        
        # Grille
        self.showGrid(x=True, y=True, alpha=0.3)
        self.getPlotItem().getViewBox().setBackgroundColor(MaritimeGraphStyle.get_background_color())
    
    def _setup_animations(self):
        """Configure les animations pour les courbes"""
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_animations)
        
        # Animations de courbes
        self.curve_animations = {}
        self.animation_progress = {}
    
    def add_animated_curve(self, name: str, x_data: np.ndarray, y_data: np.ndarray, 
                          color_index: int = 0, animation_duration: int = 1000):
        """Ajoute une courbe avec animation d'apparition"""
        if not pg or not np:
            logger.warning("pyqtgraph ou numpy non disponible")
            return
        
        # Créer la courbe
        pen = MaritimeGraphStyle.get_curve_pen(color_index)
        curve = self.plot([], [], pen=pen, name=name)
        
        # Stocker les données
        self.curves[name] = {
            'curve': curve,
            'x_data': x_data,
            'y_data': y_data,
            'pen': pen
        }
        
        # Animation d'apparition progressive
        self._animate_curve_appearance(name, animation_duration)
    
    def _animate_curve_appearance(self, curve_name: str, duration: int):
        """Anime l'apparition progressive d'une courbe"""
        if curve_name not in self.curves:
            return
        
        curve_data = self.curves[curve_name]
        total_points = len(curve_data['x_data'])
        
        # Animation par timer
        animation_steps = 60  # 60 FPS
        step_duration = duration // animation_steps
        points_per_step = max(1, total_points // animation_steps)
        
        current_points = 0
        
        def update_curve():
            nonlocal current_points
            current_points = min(current_points + points_per_step, total_points)
            
            # Mettre à jour la courbe
            x_partial = curve_data['x_data'][:current_points]
            y_partial = curve_data['y_data'][:current_points]
            curve_data['curve'].setData(x_partial, y_partial)
            
            if current_points >= total_points:
                timer.stop()
        
        timer = QTimer()
        timer.timeout.connect(update_curve)
        timer.start(step_duration)
    
    def update_curve_data(self, name: str, x_data: np.ndarray, y_data: np.ndarray, 
                         animate: bool = True):
        """Met à jour les données d'une courbe avec animation optionnelle"""
        if name not in self.curves:
            logger.warning(f"Courbe '{name}' non trouvée")
            return
        
        curve_data = self.curves[name]
        
        if animate:
            # Animation de transition fluide
            self._animate_curve_transition(name, x_data, y_data)
        else:
            # Mise à jour directe
            curve_data['curve'].setData(x_data, y_data)
            curve_data['x_data'] = x_data
            curve_data['y_data'] = y_data
    
    def _animate_curve_transition(self, curve_name: str, new_x: np.ndarray, new_y: np.ndarray):
        """Anime la transition entre anciennes et nouvelles données"""
        if curve_name not in self.curves:
            return
        
        curve_data = self.curves[curve_name]
        old_x = curve_data['x_data']
        old_y = curve_data['y_data']
        
        # Interpolation progressive
        animation_steps = 30
        step_duration = 16  # ~60 FPS
        
        current_step = 0
        
        def interpolate_step():
            nonlocal current_step
            progress = current_step / animation_steps
            
            # Interpolation linéaire
            if len(old_x) == len(new_x):
                interp_x = old_x + (new_x - old_x) * progress
                interp_y = old_y + (new_y - old_y) * progress
                curve_data['curve'].setData(interp_x, interp_y)
            else:
                # Si les tailles diffèrent, transition directe
                curve_data['curve'].setData(new_x, new_y)
            
            current_step += 1
            if current_step >= animation_steps:
                timer.stop()
                curve_data['x_data'] = new_x
                curve_data['y_data'] = new_y
        
        timer = QTimer()
        timer.timeout.connect(interpolate_step)
        timer.start(step_duration)
    
    def clear_all_curves(self):
        """Supprime toutes les courbes"""
        self.clear()
        self.curves.clear()
        self.curve_colors.clear()
    
    def set_maritime_title(self, title: str):
        """Définit un titre avec style maritime"""
        font = MaritimeGraphStyle.get_font()
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Bold)
        
        self.setTitle(title, color=MaritimeGraphStyle.get_foreground_color(), size='12pt')
    
    def set_maritime_labels(self, x_label: str, y_label: str):
        """Définit les labels des axes avec style maritime"""
        font = MaritimeGraphStyle.get_font()
        
        self.setLabel('left', y_label, color=MaritimeGraphStyle.get_foreground_color())
        self.setLabel('bottom', x_label, color=MaritimeGraphStyle.get_foreground_color())

class MaritimeGraphManager:
    """Gestionnaire global pour les graphiques maritimes"""
    
    def __init__(self):
        self.graphs = {}
        logger.info("MaritimeGraphManager initialisé")
    
    def create_plot_widget(self, name: str, parent=None, **kwargs) -> AnimatedPlotWidget:
        """Crée un nouveau widget de graphique maritime"""
        plot_widget = AnimatedPlotWidget(parent, **kwargs)
        self.graphs[name] = plot_widget
        return plot_widget
    
    def get_plot_widget(self, name: str) -> Optional[AnimatedPlotWidget]:
        """Récupère un widget de graphique par nom"""
        return self.graphs.get(name)
    
    def apply_maritime_theme_to_existing(self, plot_widget: pg.PlotWidget):
        """Applique le thème maritime à un graphique existant"""
        if not isinstance(plot_widget, pg.PlotWidget):
            logger.warning("Widget fourni n'est pas un PlotWidget")
            return
        
        # Appliquer le style maritime
        plot_widget.setBackground(MaritimeGraphStyle.get_background_color())
        
        # Style des axes
        axis_pen = MaritimeGraphStyle.get_axis_pen()
        font = MaritimeGraphStyle.get_font()
        
        for axis_name in ['left', 'bottom', 'right', 'top']:
            axis = plot_widget.getAxis(axis_name)
            axis.setPen(axis_pen)
            axis.setTextPen(MaritimeGraphStyle.get_foreground_color())
            axis.setTickFont(font)
        
        # Grille
        plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        logger.info("Thème maritime appliqué au graphique existant")

# Instance globale
_maritime_graph_manager = None

def get_maritime_graph_manager() -> MaritimeGraphManager:
    """Récupère l'instance globale du gestionnaire de graphiques"""
    global _maritime_graph_manager
    if _maritime_graph_manager is None:
        _maritime_graph_manager = MaritimeGraphManager()
    return _maritime_graph_manager

# Fonctions utilitaires
def create_maritime_plot(name: str, parent=None, title: str = "", 
                        x_label: str = "", y_label: str = "") -> AnimatedPlotWidget:
    """Fonction utilitaire pour créer rapidement un graphique maritime"""
    manager = get_maritime_graph_manager()
    plot_widget = manager.create_plot_widget(name, parent)
    
    if title:
        plot_widget.set_maritime_title(title)
    
    if x_label or y_label:
        plot_widget.set_maritime_labels(x_label, y_label)
    
    return plot_widget

def apply_maritime_theme(plot_widget: pg.PlotWidget):
    """Applique le thème maritime à un graphique existant"""
    manager = get_maritime_graph_manager()
    manager.apply_maritime_theme_to_existing(plot_widget)