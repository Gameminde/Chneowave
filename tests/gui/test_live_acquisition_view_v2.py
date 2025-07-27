#!/usr/bin/env python3
"""
Tests pour la vue LiveAcquisitionViewV2.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-21
Version: 1.0.0
"""

import pytest
import numpy as np

from hrneowave.gui.views.live_acquisition_view_v2 import LiveAcquisitionViewV2

@pytest.fixture
def app(qapp):
    """Fixture pour l'application Qt."""
    return qapp

def test_live_acquisition_v2_initialization(qtbot):
    """Teste l'initialisation correcte de LiveAcquisitionViewV2."""
    widget = LiveAcquisitionViewV2(num_probes=8)
    qtbot.addWidget(widget)
    widget.show()

    assert widget.objectName() == "LiveAcquisitionViewV2"
    assert widget.num_probes == 8
    assert widget.graph_pane1 is not None
    assert widget.graph_pane2 is not None
    assert widget.graph_pane3 is not None
    assert widget.graph_pane1.probe_selector.count() == 8
    assert widget.graph_pane3.multi_trace is True

def test_live_acquisition_v2_data_update(qtbot):
    """Teste la mise à jour des données sur les graphes."""
    widget = LiveAcquisitionViewV2(num_probes=4)
    qtbot.addWidget(widget)

    # Créer des données de test
    time_array = np.linspace(0, 1, 1000)
    data_array = np.random.randn(1000, 4)

    # Mettre à jour les données
    widget.on_data_ready(time_array, data_array)

    # Attendre que le thread FFT se termine
    widget.thread_pool.waitForDone(1000)

    # Activer l'auto-range pour s'assurer que les vues sont prêtes
    widget.graph_pane1.plot_item.enableAutoRange(True)
    widget.graph_pane2.plot_item.enableAutoRange(True)
    widget.graph_pane3.plot_item.enableAutoRange(True)

    # Vérifier que les données ont été mises à jour (vérification simple)
    # Graphe 1 (sonde unique)
    assert widget.graph_pane1.curves[0].xData is not None
    assert len(widget.graph_pane1.curves[0].xData) > 0

    # Graphe 2 (FFT)
    assert widget.graph_pane2.curves[0].xData is not None
    assert len(widget.graph_pane2.curves[0].xData) > 0

    # Graphe 3 (multi-trace)
    assert widget.graph_pane3.curves[0].xData is not None
    assert len(widget.graph_pane3.curves[0].xData) > 0
    assert widget.graph_pane3.curves[3].xData is not None # Vérifier la dernière sonde