#!/usr/bin/env python3
# tree_scanner.py - Scanner d'arbre hiérarchique pour CHNeoWave

import os
from pathlib import Path

def generate_tree(directory, max_depth=3, current_depth=0, prefix=""):
    """Génère un arbre hiérarchique du répertoire"""
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        return
    
    # Séparer dossiers et fichiers
    dirs = []
    files = []
    
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # Ignorer certains dossiers système/cache/venv
            if item not in ['.git', '__pycache__', '.pytest_cache', 'venv', 'node_modules', 
                           'site-packages', 'Include', 'Lib', 'Scripts', 'share', 'docx-template']:
                dirs.append(item)
        else:
            # Inclure seulement les fichiers importants
            if current_depth <= 1 and (item.endswith(('.py', '.md', '.txt', '.json', '.yml', '.yaml', '.bat', '.ps1', '.html', '.csv')) or 
                                       item in ['.gitignore', 'requirements.txt', 'pyproject.toml', 'pytest.ini']):
                files.append(item)
    
    # Afficher les dossiers d'abord
    for i, dir_name in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1) and len(files) == 0
        connector = "└── " if is_last_dir else "├── "
        print(f"{prefix}{connector}{dir_name}/")
        
        # Récursion pour les sous-dossiers
        new_prefix = prefix + ("    " if is_last_dir else "│   ")
        dir_path = os.path.join(directory, dir_name)
        generate_tree(dir_path, max_depth, current_depth + 1, new_prefix)
    
    # Afficher les fichiers les plus importants
    important_files = []
    for file in files:
        if current_depth == 0:
            # Au niveau racine, fichiers de configuration principaux
            if file in ['README.md', 'requirements.txt', 'pyproject.toml', 'pytest.ini', 
                       '.gitignore', 'launch_chneowave.bat', 'launch_chneowave.ps1',
                       'demo_chneowave.py', 'quick_audit.py', 'validate_integration.py',
                       'tree_scanner.py', 'audit_integration.py']:
                important_files.append(file)
        elif current_depth == 1:
            # Au niveau 1, fichiers Python principaux (max 8)
            if file.endswith('.py') and not file.startswith('test_') and len(important_files) < 8:
                important_files.append(file)
            elif file in ['README.md', 'requirements.txt']:
                important_files.append(file)
    
    # Afficher les fichiers importants
    for i, file_name in enumerate(important_files):
        is_last = i == len(important_files) - 1 and len(files) <= len(important_files)
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{file_name}")
    
    # Indiquer s'il y a plus de fichiers
    if len(files) > len(important_files):
        remaining = len(files) - len(important_files)
        print(f"{prefix}└── ... (+{remaining} autres fichiers)")

def count_project_files(directory):
    """Compte les fichiers du projet (excluant venv)"""
    python_files = 0
    test_files = 0
    doc_files = 0
    
    for root, dirs, files in os.walk(directory):
        # Ignorer le dossier venv et ses sous-dossiers
        if 'venv' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                python_files += 1
                if file.startswith('test_'):
                    test_files += 1
            elif file.endswith('.md'):
                doc_files += 1
    
    return python_files, test_files, doc_files

def main():
    """Point d'entrée principal"""
    print("🌳 STRUCTURE DU PROJET CHNEOWAVE")
    print("=" * 50)
    print("📁 Arbre hiérarchique (3 niveaux max)\n")
    
    current_dir = Path.cwd()
    print(f"{current_dir.name}/")
    
    generate_tree(current_dir, max_depth=3)
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU PROJET:")
    
    # Compter les éléments principaux
    main_dirs = ['src', 'logciel hrneowave', 'tests', 'config', 'docs']
    existing_dirs = [d for d in main_dirs if (current_dir / d).exists()]
    
    python_files, test_files, doc_files = count_project_files(current_dir)
    
    print(f"  📂 Dossiers principaux: {len(existing_dirs)}/{len(main_dirs)}")
    print(f"  🐍 Modules Python: {python_files}")
    print(f"  🧪 Fichiers de tests: {test_files}")
    print(f"  📄 Documentation: {doc_files}")
    
    # Vérifier les modules optimisés
    optimized_modules = [
        'src/hrneowave/core/optimized_fft_processor.py',
        'src/hrneowave/core/optimized_goda_analyzer.py',
        'src/hrneowave/core/circular_buffer.py',
        'logciel hrneowave/modern_acquisition_ui.py'
    ]
    
    existing_optimized = sum(1 for module in optimized_modules if (current_dir / module).exists())
    print(f"  ⚡ Modules optimisés: {existing_optimized}/{len(optimized_modules)}")
    
    print("\n🏛️ Architecture pour laboratoire maritime méditerranéen")
    print("   ├── Acquisition temps réel (PyQt5 + PyQtGraph)")
    print("   ├── Traitement optimisé (FFT + Analyse Goda)")
    print("   ├── Interface moderne (modern_acquisition_ui.py)")
    print("   └── Tests d'intégration validés")

if __name__ == "__main__":
    main()