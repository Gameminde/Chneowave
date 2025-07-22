"""CHNeoWave - Logiciel d'acquisition houle laboratoire maritime"""

__version__ = "0.3.0"


from .hw import *
from .tools import *

# Import du module GUI pour l'interface moderne
try:
    from . import gui
except ImportError as e:
    print(f"Module GUI non disponible: {e}")
