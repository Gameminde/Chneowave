#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module des vues pour HRNeoWave
"""

from .welcome_view import WelcomeView
from .acquisition_view import AcquisitionView
from .analysis_view import AnalysisView

__all__ = ["WelcomeView", "AcquisitionView", "AnalysisView"]