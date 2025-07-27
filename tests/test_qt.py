#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Qt installation hors projet CHNeoWave
Pour diagnostic écran gris
"""

import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import QLibraryInfo, Qt
from PySide6.QtGui import QGuiApplication

def test_qt_installation(qtbot):
    """Test basique de l'installation Qt"""
    print("=== TEST QT INSTALLATION ===")
    

    
    # Informations sur la plateforme
    print(f"Platform name: {QGuiApplication.platformName()}")
    print(f"Qt version: {QLibraryInfo.version().toString()}")
    print(f"Qt library path: {QLibraryInfo.path(QLibraryInfo.LibraryPath.LibrariesPath)}")
    print(f"Qt plugins path: {QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)}")
    
    # Variables d'environnement Qt
    import os
    qt_qpa_platform = os.environ.get('QT_QPA_PLATFORM', 'Non définie')
    print(f"QT_QPA_PLATFORM: {qt_qpa_platform}")
    
    # Créer une fenêtre simple
    window = QWidget()
    window.setWindowTitle("Test Qt - CHNeoWave Diagnostic")
    window.resize(400, 200)
    
    layout = QVBoxLayout()
    
    # Label de test
    label = QLabel("Qt OK - Interface visible")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("""
        QLabel {
            background-color: #2d2d2d;
            color: white;
            font-size: 16px;
            padding: 20px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        }
    """)
    
    layout.addWidget(label)
    window.setLayout(layout)
    
    # Afficher la fenêtre
    qtbot.addWidget(window)
    window.show()
    
    print("\n=== INFORMATIONS FENETRE ===")
    print(f"Window visible: {window.isVisible()}")
    print(f"Window size: {window.size()}")
    print(f"Window geometry: {window.geometry()}")
    print(f"Label visible: {label.isVisible()}")
    print(f"Label size: {label.size()}")
    
    qtbot.waitExposed(window, timeout=3000)
    assert window.isVisible()

def check_environment():
    """Vérifier l'environnement système"""
    print("\n=== ENVIRONNEMENT SYSTÈME ===")
    
    import os
    
    # Variables d'environnement Qt importantes
    qt_vars = [
        'QT_QPA_PLATFORM',
        'QT_QPA_PLATFORM_PLUGIN_PATH',
        'QT_PLUGIN_PATH',
        'QT_DEBUG_PLUGINS'
    ]
    
    for var in qt_vars:
        value = os.environ.get(var, 'Non définie')
        print(f"{var}: {value}")
    
    # Vérifier PATH pour autres installations Qt
    print("\n=== CHEMINS DANS PATH ===")
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    qt_paths = [p for p in path_dirs if 'qt' in p.lower() or 'pyside' in p.lower() or 'pyqt' in p.lower()]
    
    if qt_paths:
        print("Chemins Qt trouvés dans PATH:")
        for path in qt_paths:
            print(f"  - {path}")
    else:
        print("Aucun chemin Qt trouvé dans PATH")
    
    # Informations Python
    print(f"\n=== PYTHON ===")
    print(f"Version Python: {sys.version}")
    print(f"Exécutable Python: {sys.executable}")
    
    # Modules Qt installés
    print(f"\n=== MODULES QT ===")
    try:
        import PySide6
        print(f"PySide6 version: {PySide6.__version__}")
        print(f"PySide6 path: {PySide6.__file__}")
    except ImportError:
        print("PySide6 non installé")
    
    try:
        import PyQt5
        print(f"PyQt5 installé: {PyQt5.__file__}")
    except ImportError:
        print("PyQt5 non installé")
    
    try:
        import PyQt6
        print(f"PyQt6 installé: {PyQt6.__file__}")
    except ImportError:
        print("PyQt6 non installé")

def check_gpu_drivers():
    """Vérifier les pilotes GPU"""
    print("\n=== PILOTES GPU ===")
    
    try:
        import subprocess
        
        # Commande pour obtenir les infos GPU sur Windows
        result = subprocess.run(
            ['wmic', 'path', 'win32_VideoController', 'get', 'name,driverversion,driverdate'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("Informations GPU:")
            print(result.stdout)
        else:
            print("Impossible d'obtenir les informations GPU")
            
    except Exception as e:
        print(f"Erreur lors de la vérification GPU: {e}")

if __name__ == "__main__":
    print("ÉCRAN GRIS – DIAGNOSTIC GEMINI")
    print("Test Qt installation hors projet CHNeoWave")
    print("=" * 50)
    
    # Vérifier l'environnement d'abord
    check_environment()
    check_gpu_drivers()
    
    # Tester Qt
    try:
        exit_code = test_qt_installation()
        print(f"\n=== RÉSULTAT ===")
        print(f"Test Qt terminé avec code: {exit_code}")
        if exit_code == 0:
            print("✅ Qt fonctionne correctement")
        else:
            print("❌ Problème détecté avec Qt")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()