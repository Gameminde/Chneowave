#!/usr/bin/env python3
"""
Configuration pytest pour les tests smoke CHNeoWave
"""

import pytest
import sys
import os
from pathlib import Path

# Ajout du chemin source au début
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

# Configuration des variables d'environnement pour les tests
os.environ['CHNEOWAVE_TEST_MODE'] = '1'
os.environ['CHNEOWAVE_LOG_LEVEL'] = 'WARNING'
os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Pour les tests GUI sans affichage

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configuration globale de l'environnement de test"""
    print("\n=== Configuration environnement de test CHNeoWave ===")
    print(f"Répertoire projet: {project_root}")
    print(f"Répertoire source: {src_path}")
    print(f"Python: {sys.version}")
    
    # Vérification des dépendances critiques
    required_packages = [
        'PySide6',
        'numpy',
        'scipy',
        'h5py',
        'reportlab',
        'pyqtgraph'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} MANQUANT")
    
    if missing_packages:
        pytest.fail(f"Packages manquants: {', '.join(missing_packages)}")
    
    print("=== Environnement de test prêt ===")
    
    yield
    
    print("\n=== Nettoyage environnement de test ===")

@pytest.fixture
def qt_no_exception_capture(qtbot):
    """Désactive la capture d'exceptions Qt pour un meilleur debugging"""
    import sys
    from PySide6.QtCore import qInstallMessageHandler
    
    def qt_message_handler(mode, context, message):
        if 'exception' in message.lower():
            print(f"Qt Exception: {message}")
    
    old_handler = qInstallMessageHandler(qt_message_handler)
    yield
    qInstallMessageHandler(old_handler)

# Configuration des markers pytest
pytest_plugins = ['pytestqt']

def pytest_configure(config):
    """Configuration des markers personnalisés"""
    config.addinivalue_line(
        "markers", "gui: marque les tests qui nécessitent l'interface graphique"
    )
    config.addinivalue_line(
        "markers", "slow: marque les tests lents (> 10s)"
    )
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration"
    )

def pytest_collection_modifyitems(config, items):
    """Modification automatique des items de test"""
    for item in items:
        # Marquer automatiquement les tests GUI
        if 'gui' in item.nodeid.lower() or 'qt' in str(item.function.__code__.co_names):
            item.add_marker(pytest.mark.gui)
        
        # Marquer les tests lents
        if 'large' in item.name or 'slow' in item.name:
            item.add_marker(pytest.mark.slow)

@pytest.fixture(scope="function")
def clean_qt_app():
    """Assure un environnement Qt propre pour chaque test"""
    from PySide6.QtWidgets import QApplication
    
    # Fermer toute application Qt existante
    app = QApplication.instance()
    if app:
        app.closeAllWindows()
        app.processEvents()
    
    yield
    
    # Nettoyage après le test
    app = QApplication.instance()
    if app:
        app.closeAllWindows()
        app.processEvents()

# Configuration des timeouts
DEFAULT_TIMEOUT = 30  # secondes
GUI_TIMEOUT = 10      # secondes pour les tests GUI

@pytest.fixture
def timeout_config():
    """Configuration des timeouts pour les tests"""
    return {
        'default': DEFAULT_TIMEOUT,
        'gui': GUI_TIMEOUT
    }