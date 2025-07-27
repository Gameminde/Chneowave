#!/usr/bin/env python3
"""
Nouvelle vue d'acquisition en temps réel (V2) avec plusieurs graphes.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-20
Version: 1.0.0
"""

from PySide6.QtWidgets import QWidget, QGridLayout, QComboBox, QVBoxLayout, QLabel
from PySide6.QtCore import Slot, Qt, QObject, Signal, QRunnable, QThreadPool
import pyqtgraph as pg
import numpy as np


class WorkerSignals(QObject):
    '''Signaux pour le worker FFT.'''
    result_ready = Signal(np.ndarray, np.ndarray)


class FFTCalculator(QRunnable):
    '''Worker pour calculer la FFT dans un thread séparé.'''
    def __init__(self, time_array, data_slice):
        super().__init__()
        self.signals = WorkerSignals()
        self.time_array = time_array
        self.data_slice = data_slice

    @Slot()
    def run(self):
        if self.data_slice.size > 1:
            sample_spacing = self.time_array[1] - self.time_array[0] if len(self.time_array) > 1 else 1
            fft_freq = np.fft.rfftfreq(self.data_slice.size, d=sample_spacing)
            fft_vals = np.abs(np.fft.rfft(self.data_slice))
            self.signals.result_ready.emit(fft_freq, fft_vals)


class GraphPane(QWidget):
    """Un panneau contenant un graphe et des contrôles pour sélectionner les sondes."""
    def __init__(self, title: str, num_probes: int, multi_trace: bool = False, parent: QWidget = None):
        super().__init__(parent)
        self.multi_trace = multi_trace
        self.num_probes = num_probes
        self.curves = {}

        self.title = title
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = None # Initialisation différée

        self.probe_selector = QComboBox()
        self.probe_selector.addItems([f"Sonde {i+1}" for i in range(num_probes)])
        if multi_trace:
            # Pour le multi-trace, on pourrait utiliser un autre type de sélecteur
            # ou simplement afficher toutes les sondes sélectionnées.
            # Pour l'instant, on le laisse simple.
            pass
        else:
            self.probe_selector.currentIndexChanged.connect(self._on_probe_changed)

        # Le widget sera ajouté dans showEvent
        layout.addWidget(self.probe_selector)

    def showEvent(self, event):
        super().showEvent(event)
        if self.plot_widget is None:
            self.plot_widget = pg.PlotWidget(parent=self)
            self.plot_widget.setBackground('transparent')
            self.plot_item = self.plot_widget.getPlotItem()
            self.plot_item.setTitle(self.title)
            self.plot_item.setLabel('left', 'Amplitude (V)')
            self.plot_item.setLabel('bottom', 'Temps (s)')
            self.plot_item.showGrid(x=True, y=True, alpha=0.3)
            self.plot_item.setDownsampling(mode='peak')
            self.plot_item.setClipToView(True)
            self.layout().insertWidget(0, self.plot_widget)
            self._create_curves()

    def _create_curves(self):
        if self.plot_item is None: return
        if self.multi_trace:
            for i in range(self.num_probes):
                pen = pg.mkPen(color=pg.intColor(i, hues=self.num_probes))
                self.curves[i] = self.plot_item.plot(pen=pen, name=f"Sonde {i+1}")
        else:
            self.curves[0] = self.plot_item.plot(pen='c')

    def _on_probe_changed(self, index: int):
        # Logique pour changer la sonde affichée
        pass

    @Slot(np.ndarray, np.ndarray)
    def update_data(self, time_array: np.ndarray, data_array: np.ndarray):
        """Met à jour les données du graphe. data_array est (samples, probes)."""
        if self.multi_trace:
            for i in range(self.num_probes):
                if i in self.curves:
                    self.curves[i].setData(time_array, data_array[:, i])
        else:
            selected_probe = self.probe_selector.currentIndex()
            self.curves[0].setData(time_array, data_array[:, selected_probe])

class LiveAcquisitionViewV2(QWidget):
    """Vue d'acquisition V2 avec trois panneaux de graphes indépendants."""
    def __init__(self, num_probes: int = 16, parent: QWidget = None):
        super().__init__(parent)
        self.setObjectName("LiveAcquisitionViewV2")
        self.num_probes = num_probes
        self.thread_pool = QThreadPool()
        print(f"Max threads in pool: {self.thread_pool.maxThreadCount()}")

        self._setup_ui()

    def _setup_ui(self):
        """Initialise les trois panneaux de graphes."""
        main_layout = QGridLayout(self)

        self.graph_pane1 = GraphPane("Signal Brut - Sonde Unique", self.num_probes, multi_trace=False, parent=self)
        self.graph_pane2 = GraphPane("Analyse Fréquentielle (FFT)", self.num_probes, multi_trace=False, parent=self)
        self.graph_pane3 = GraphPane("Toutes les Sondes", self.num_probes, multi_trace=True, parent=self)

        main_layout.addWidget(self.graph_pane1, 0, 0)
        main_layout.addWidget(self.graph_pane2, 0, 1)
        main_layout.addWidget(self.graph_pane3, 1, 0, 1, 2)

    @Slot(np.ndarray, np.ndarray)
    def on_data_ready(self, time_array: np.ndarray, data_array: np.ndarray):
        """Slot pour recevoir les données du SignalBus et les dispatcher.
        
        Ici, on applique un downsampling simple pour l'affichage.
        """
        self.graph_pane1.update_data(time_array, data_array)
        self.graph_pane3.update_data(time_array, data_array)

        # Lancer le calcul de la FFT dans un thread séparé
        selected_probe = self.graph_pane2.probe_selector.currentIndex()
        calculator = FFTCalculator(time_array, data_array[:, selected_probe])
        calculator.signals.result_ready.connect(self.on_fft_ready)
        self.thread_pool.start(calculator)

    @Slot(np.ndarray, np.ndarray)
    def on_fft_ready(self, fft_freq: np.ndarray, fft_vals: np.ndarray):
        """Met à jour le graphe FFT avec les résultats du worker."""
        self.graph_pane2.curves[0].setData(fft_freq, fft_vals)