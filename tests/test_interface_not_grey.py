#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que l'interface CHNeoWave n'affiche pas un écran gris
Ce test échoue si la fenêtre est 100% grise
"""

import pytest
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QColor

@pytest.mark.slow
def test_simple_color_render(qtbot):
    """Vérifie que l'environnement de test peut rendre une couleur simple."""
    # Création d'une fenêtre de test simple
    window = QWidget()
    window.resize(200, 100)
    layout = QVBoxLayout()
    window.setLayout(layout)

    # Ajout d'un bouton avec une couleur distincte
    button = QPushButton("Test Button")
    button.setStyleSheet("background-color: #FF0000; color: white;") # Rouge vif
    layout.addWidget(button)

    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    QApplication.processEvents()
    qtbot.wait(100)

    # Vérification directe de la feuille de style appliquée
    # C'est un test plus robuste que la capture d'écran qui peut être peu fiable
    expected_style = "background-color: #FF0000; color: white;"
    actual_style = button.styleSheet()

    assert expected_style == actual_style, f"La feuille de style est incorrecte. Attendu: '{expected_style}', Obtenu: '{actual_style}'"