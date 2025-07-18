"""Interface graphique CHNeoWave

Module GUI pour le logiciel d'acquisition et d'analyse de houle
CHNeoWave destiné aux laboratoires d'études maritimes.
"""

__version__ = "3.0.0"
__author__ = "Laboratoire Maritime"

# Imports principaux pour l'interface
try:
    from .main import main
    from .main_controller import MainController
    from .modern_acquisition_ui import ModernAcquisitionUI
    from .theme import apply_theme, current_theme
    
    __all__ = [
        'main',
        'MainController', 
        'ModernAcquisitionUI',
        'apply_theme',
        'current_theme'
    ]
except ImportError as e:
    print(f"⚠️ Certains modules GUI non disponibles: {e}")
    __all__ = []