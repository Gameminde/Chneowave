"""Package des contrôleurs GUI pour CHNeoWave.

Ce package contient les contrôleurs et workers pour l'interface utilisateur.
"""

from .acquisition_controller import AcquisitionController, create_acquisition_controller
from .optimized_processing_worker import OptimizedProcessingWorker, ProcessingStats

__all__ = [
    'AcquisitionController',
    'create_acquisition_controller',
    'OptimizedProcessingWorker',
    'ProcessingStats'
]