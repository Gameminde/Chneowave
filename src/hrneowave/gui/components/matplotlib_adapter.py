#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptateur Matplotlib pour remplacer PyQtGraph
Compatible PySide6 - CHNeoWave v1.0.0

Cet adaptateur fournit une interface compatible avec PyQtGraph
utilisant matplotlib comme backend pour la compatibilité PySide6.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal, QObject


class PlotWidget(QWidget):
    """
    Widget de tracé compatible avec l'interface PyQtGraph
    Utilise matplotlib comme backend
    """
    
    def __init__(self, parent=None, background='default', **kwargs):
        super().__init__(parent)
        
        # Configuration matplotlib
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Axes principal
        self.axes = self.figure.add_subplot(111)
        
        # Configuration du style
        if background == 'w' or background == 'white':
            self.figure.patch.set_facecolor('white')
            self.axes.set_facecolor('white')
        elif background == 'k' or background == 'black':
            self.figure.patch.set_facecolor('black')
            self.axes.set_facecolor('black')
            self.axes.tick_params(colors='white')
            self.axes.xaxis.label.set_color('white')
            self.axes.yaxis.label.set_color('white')
        
        # Stockage des courbes
        self.plot_items = []
        
    def plot(self, x=None, y=None, pen=None, name=None, **kwargs):
        """
        Tracer une courbe - Interface compatible PyQtGraph
        """
        if x is None and y is not None:
            x = np.arange(len(y))
        elif x is not None and y is None:
            y = x
            x = np.arange(len(y))
        
        # Configuration du style
        plot_kwargs = {}
        if pen is not None:
            if isinstance(pen, str):
                plot_kwargs['color'] = pen
            elif hasattr(pen, 'color'):
                plot_kwargs['color'] = pen.color()
        
        if name is not None:
            plot_kwargs['label'] = name
            
        # Tracer
        line, = self.axes.plot(x, y, **plot_kwargs, **kwargs)
        self.plot_items.append(line)
        
        # Rafraîchir
        self.canvas.draw()
        
        return PlotDataItem(line)
    
    def clear(self):
        """
        Effacer tous les tracés
        """
        self.axes.clear()
        self.plot_items.clear()
        self.canvas.draw()
    
    def setLabel(self, axis, text, units=None, **kwargs):
        """
        Définir les labels des axes
        """
        if units:
            label = f"{text} ({units})"
        else:
            label = text
            
        if axis.lower() in ['left', 'y']:
            self.axes.set_ylabel(label)
        elif axis.lower() in ['bottom', 'x']:
            self.axes.set_xlabel(label)
        elif axis.lower() in ['top']:
            self.axes.set_title(label)
            
        self.canvas.draw()
    
    def setTitle(self, title):
        """
        Définir le titre du graphique
        """
        self.axes.set_title(title)
        self.canvas.draw()
    
    def addLegend(self, **kwargs):
        """
        Ajouter une légende
        """
        self.axes.legend()
        self.canvas.draw()
    
    def setXRange(self, min_val, max_val, padding=None):
        """
        Définir la plage X
        """
        self.axes.set_xlim(min_val, max_val)
        self.canvas.draw()
    
    def setYRange(self, min_val, max_val, padding=None):
        """
        Définir la plage Y
        """
        self.axes.set_ylim(min_val, max_val)
        self.canvas.draw()
    
    def autoRange(self):
        """
        Ajustement automatique des plages
        """
        self.axes.relim()
        self.axes.autoscale()
        self.canvas.draw()
    
    def setLogMode(self, x=None, y=None):
        """
        Définir le mode logarithmique pour les axes
        """
        if x:
            self.axes.set_xscale('log')
        if y:
            self.axes.set_yscale('log')
        self.canvas.draw()


class PlotDataItem(QObject):
    """
    Élément de données de tracé - Compatible PyQtGraph
    """
    
    def __init__(self, line):
        super().__init__()
        self.line = line
    
    def setData(self, x=None, y=None, **kwargs):
        """
        Mettre à jour les données
        """
        if x is not None and y is not None:
            self.line.set_data(x, y)
        elif y is not None:
            self.line.set_ydata(y)
        elif x is not None:
            self.line.set_xdata(x)
            
        # Rafraîchir le canvas
        if hasattr(self.line.axes, 'figure'):
            self.line.axes.figure.canvas.draw()
    
    def setPen(self, pen):
        """
        Définir le style de ligne
        """
        if isinstance(pen, str):
            self.line.set_color(pen)
        elif hasattr(pen, 'color'):
            self.line.set_color(pen.color())
            
        if hasattr(self.line.axes, 'figure'):
            self.line.axes.figure.canvas.draw()


class mkPen:
    """
    Créateur de stylo compatible PyQtGraph
    """
    
    def __init__(self, color='b', width=1, style='-'):
        self._color = color
        self._width = width
        self._style = style
    
    def color(self):
        return self._color
    
    def width(self):
        return self._width
    
    def style(self):
        return self._style


# Fonctions utilitaires compatibles
def mkPen(*args, **kwargs):
    """
    Créer un stylo - Interface compatible PyQtGraph
    """
    if args:
        return mkPen(color=args[0], **kwargs)
    return mkPen(**kwargs)


def setConfigOptions(**kwargs):
    """
    Configuration globale - Stub pour compatibilité
    """
    pass


# Alias pour compatibilité
pg = type('pg', (), {
    'PlotWidget': PlotWidget,
    'mkPen': mkPen,
    'setConfigOptions': setConfigOptions,
    'PlotDataItem': PlotDataItem
})()