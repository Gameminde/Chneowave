#!/usr/bin/env python3
"""
Tests pour la vue ProjectSettingsView.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-21
Version: 1.0.0
"""

import pytest
from PySide6.QtCore import Qt

from hrneowave.gui.views.project_settings_view import ProjectSettingsView

@pytest.fixture
def app(qapp):
    """Fixture pour l'application Qt."""
    return qapp

def test_project_settings_view_initialization(qtbot):
    """Teste l'initialisation correcte de ProjectSettingsView."""
    widget = ProjectSettingsView()
    qtbot.addWidget(widget)

    assert widget.objectName() == "ProjectSettingsView"
    assert widget.project_name_input is not None
    assert widget.num_probes_spinbox is not None
    assert widget.test_duration_spinbox is not None
    assert widget.sampling_freq_spinbox is not None
    assert widget.save_button is not None

def test_project_settings_view_validators(qtbot):
    """Teste les validateurs sur les champs de saisie."""
    widget = ProjectSettingsView()
    qtbot.addWidget(widget)

    # Test num_probes_spinbox (Int)
    widget.num_probes_spinbox.setValue(17)
    assert widget.num_probes_spinbox.value() <= 16
    widget.num_probes_spinbox.setValue(0)
    assert widget.num_probes_spinbox.value() >= 1

    # Test test_duration_spinbox (Double)
    widget.test_duration_spinbox.setValue(0.5)
    assert widget.test_duration_spinbox.value() > 0

    # Test sampling_freq_spinbox (Double)
    widget.sampling_freq_spinbox.setValue(0)
    assert widget.sampling_freq_spinbox.value() > 0

def test_project_settings_save_signal(qtbot):
    """Teste l'émission du signal de sauvegarde."""
    widget = ProjectSettingsView()
    qtbot.addWidget(widget)

    widget.project_name_input.setText("Test Project")
    widget.num_probes_spinbox.setValue(8)
    widget.test_duration_spinbox.setValue(60.5)
    widget.sampling_freq_spinbox.setValue(1000.0)

    with qtbot.waitSignal(widget.settings_saved, raising=True) as blocker:
        qtbot.mouseClick(widget.save_button, Qt.LeftButton)

        assert blocker.signal_triggered
    assert blocker.args[0]['project_name'] == "Test Project"
    assert blocker.args[0]['num_probes'] == 8
    assert blocker.args[0]['test_duration'] == 60.5
    assert blocker.args[0]['sampling_frequency'] == 1000.0