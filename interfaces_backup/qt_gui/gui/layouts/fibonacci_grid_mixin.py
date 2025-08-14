#!/usr/bin/env python3
"""
Mixin pour la création de grilles basées sur Fibonacci/Golden Ratio pour CHNeoWave.

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024-12-20
Version: 1.0.0
"""

from PySide6.QtWidgets import QGridLayout, QWidget
from typing import List

class FibonacciGridMixin:
    """Classe utilitaire fournissant des méthodes pour créer des layouts basés sur Fibonacci."""

    FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    @staticmethod
    def create_grid(base_px: int = 55, parent: QWidget = None) -> QGridLayout:
        """
        Crée un QGridLayout dont les espacements et les marges respectent la suite de Fibonacci.

        Args:
            base_px (int): La valeur de base correspondant à l'index 9 de la suite (55).
            parent (QWidget): Le widget parent pour le layout.

        Returns:
            QGridLayout: Un layout configuré avec des proportions harmonieuses.
        """
        grid = QGridLayout(parent)

        # Calculer les espacements basés sur le ratio de la suite
        # Marge principale (plus grande) - index 8 (34)
        main_margin = int(base_px * (FibonacciGridMixin.FIBONACCI_SEQUENCE[8] / FibonacciGridMixin.FIBONACCI_SEQUENCE[9]))
        # Espacement horizontal - index 7 (21)
        h_spacing = int(base_px * (FibonacciGridMixin.FIBONACCI_SEQUENCE[7] / FibonacciGridMixin.FIBONACCI_SEQUENCE[9]))
        # Espacement vertical - index 6 (13)
        v_spacing = int(base_px * (FibonacciGridMixin.FIBONACCI_SEQUENCE[6] / FibonacciGridMixin.FIBONACCI_SEQUENCE[9]))

        grid.setContentsMargins(main_margin, main_margin, main_margin, main_margin)
        grid.setHorizontalSpacing(h_spacing)
        grid.setVerticalSpacing(v_spacing)

        return grid

    @staticmethod
    def get_fibonacci_stretch_factors(count: int) -> List[int]:
        """Retourne les facteurs de stretch de la suite de Fibonacci pour un nombre donné d'éléments."""
        if count > len(FibonacciGridMixin.FIBONACCI_SEQUENCE):
            # Si plus d'éléments que dans notre suite, on boucle
            return FibonacciGridMixin.FIBONACCI_SEQUENCE * (count // len(FibonacciGridMixin.FIBONACCI_SEQUENCE)) + FibonacciGridMixin.FIBONACCI_SEQUENCE[:count % len(FibonacciGridMixin.FIBONACCI_SEQUENCE)]
        return FibonacciGridMixin.FIBONACCI_SEQUENCE[:count]