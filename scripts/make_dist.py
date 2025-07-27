#!/usr/bin/env python3
"""
Script de création de l'exécutable CHNeoWave avec PyInstaller
CHNeoWave v1.0.0 - Distribution Builder Stable
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """Nettoie les répertoires de build précédents"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Nettoyage de {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Nettoie aussi les fichiers .spec
    for spec_file in Path('.').glob('*.spec'):
        print(f"Suppression de {spec_file}")
        spec_file.unlink()

def check_dependencies():
    """Vérifie que PyInstaller est installé"""
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("ERREUR: PyInstaller n'est pas installé.")
        print("Installez-le avec: pip install pyinstaller")
        return False

def get_hidden_imports():
    """Retourne la liste des imports cachés nécessaires"""
    return [
        'h5py',
        'h5py.defs',
        'h5py.utils',
        'h5py._proxy',
        'numpy',
        'scipy',
        'scipy.signal',
        'scipy.fft',
        'pyqtgraph',
        'pyqtgraph.graphicsItems',
        'pyqtgraph.widgets',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib',
        'reportlab.platypus',
        'matplotlib',
        'matplotlib.backends',
        'matplotlib.backends.backend_qt5agg',
        'pkg_resources.py2_warn'
    ]

def get_data_files():
    """Retourne la liste des fichiers de données à inclure"""
    data_files = []
    
    # Inclure les fichiers de configuration s'ils existent
    config_files = [
        'config.json',
        'settings.ini'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            data_files.append((config_file, '.'))
    
    # Inclure les ressources GUI si elles existent
    if os.path.exists('src/hrneowave/gui/resources'):
        data_files.append(('src/hrneowave/gui/resources', 'hrneowave/gui/resources'))
    
    return data_files

def build_executable():
    """Construit l'exécutable avec PyInstaller"""
    print("Construction de l'exécutable CHNeoWave...")
    
    # Paramètres PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # Un seul fichier exécutable
        '--windowed',                   # Mode fenêtré (pas de console)
        '--name=chneowave',             # Nom de l'exécutable
        '--icon=icon.ico',              # Icône (si elle existe)
        '--clean',                      # Nettoie le cache
        '--noconfirm',                  # Pas de confirmation
    ]
    
    # Ajout des imports cachés
    for hidden_import in get_hidden_imports():
        cmd.extend(['--hidden-import', hidden_import])
    
    # Ajout des fichiers de données
    for src, dst in get_data_files():
        cmd.extend(['--add-data', f'{src};{dst}'])
    
    # Exclusions pour réduire la taille
    excludes = [
        'tkinter',
        'unittest',
        'test',
        'distutils',
        'setuptools',
        'pip'
    ]
    
    for exclude in excludes:
        cmd.extend(['--exclude-module', exclude])
    
    # Point d'entrée
    cmd.append('src/hrneowave/cli.py')
    
    print(f"Commande PyInstaller: {' '.join(cmd)}")
    
    # Exécution
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Construction réussie!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERREUR lors de la construction:")
        print(f"Code de retour: {e.returncode}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def verify_executable():
    """Vérifie que l'exécutable a été créé et fonctionne"""
    exe_path = Path('dist/chneowave.exe')
    
    if not exe_path.exists():
        print("ERREUR: L'exécutable n'a pas été créé.")
        return False
    
    # Vérification de la taille (doit être > 50MB pour inclure toutes les dépendances)
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"Taille de l'exécutable: {size_mb:.1f} MB")
    
    if size_mb < 50:
        print("ATTENTION: L'exécutable semble trop petit, des dépendances pourraient manquer.")
    
    print(f"Exécutable créé avec succès: {exe_path.absolute()}")
    return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print("CHNeoWave Distribution Builder v1.0.0")
    print("=" * 60)
    
    # Vérifications préliminaires
    if not check_dependencies():
        sys.exit(1)
    
    # Nettoyage
    clean_build_dirs()
    
    # Construction
    if not build_executable():
        sys.exit(1)
    
    # Vérification
    if not verify_executable():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SUCCÈS: Distribution créée avec succès!")
    print("Fichier: dist/chneowave.exe")
    print("=" * 60)
    
    # Instructions d'utilisation
    print("\nPour tester l'exécutable:")
    print("  dist\\chneowave.exe --simulate --fs 32 --channels 8")
    print("\nPour distribution:")
    print("  Copiez dist/chneowave.exe vers le système cible")
    print("\nDocumentation complète:")
    print("  Voir docs/_build/html/index.html pour le guide utilisateur")
    print("  Voir docs/_build/html/technical_guide.html pour la documentation technique")

if __name__ == '__main__':
    main()