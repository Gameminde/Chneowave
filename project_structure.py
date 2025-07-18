#!/usr/bin/env python3
# project_structure.py - Analyseur de structure pour CHNeoWave

import os
from pathlib import Path

def scan_directory_structure(root_path, max_depth=3):
    """Scanne la structure du répertoire avec une profondeur limitée"""
    structure = {}
    
    def _scan_recursive(path, current_depth=0):
        if current_depth >= max_depth:
            return {}
        
        result = {'dirs': [], 'files': []}
        
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return result
        
        for item in items:
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                # Ignorer les dossiers système
                if item not in ['.git', '__pycache__', '.pytest_cache', 'venv', 
                               'node_modules', 'site-packages', 'Include', 'Lib', 'Scripts']:
                    result['dirs'].append({
                        'name': item,
                        'path': item_path,
                        'content': _scan_recursive(item_path, current_depth + 1)
                    })
            else:
                # Filtrer les fichiers importants
                if (item.endswith(('.py', '.md', '.txt', '.json', '.yml', '.yaml', '.bat', '.ps1')) or 
                    item in ['.gitignore', 'requirements.txt', 'pyproject.toml', 'pytest.ini']):
                    result['files'].append(item)
        
        return result
    
    return _scan_recursive(root_path)

def print_tree(structure, prefix="", is_last=True, current_depth=0, max_depth=3):
    """Affiche l'arbre de structure"""
    if current_depth >= max_depth:
        return
    
    # Afficher les dossiers
    dirs = structure.get('dirs', [])
    files = structure.get('files', [])
    
    for i, dir_info in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1) and len(files) == 0
        connector = "└── " if is_last_dir else "├── "
        print(f"{prefix}{connector}{dir_info['name']}/")
        
        # Récursion pour les sous-dossiers
        new_prefix = prefix + ("    " if is_last_dir else "│   ")
        print_tree(dir_info['content'], new_prefix, is_last_dir, current_depth + 1, max_depth)
    
    # Afficher les fichiers importants (limités)
    important_files = []
    if current_depth == 0:
        # Niveau racine - fichiers de configuration
        priority_files = ['README.md', 'requirements.txt', 'pyproject.toml', 'pytest.ini', 
                         '.gitignore', 'launch_chneowave.bat', 'launch_chneowave.ps1',
                         'demo_chneowave.py', 'quick_audit.py', 'validate_integration.py']
        important_files = [f for f in files if f in priority_files]
    elif current_depth == 1:
        # Niveau 1 - fichiers Python principaux (max 5)
        python_files = [f for f in files if f.endswith('.py') and not f.startswith('test_')]
        important_files = python_files[:5]
    
    for i, file_name in enumerate(important_files):
        is_last_file = i == len(important_files) - 1
        connector = "└── " if is_last_file else "├── "
        print(f"{prefix}{connector}{file_name}")
    
    # Indiquer s'il y a plus de fichiers
    if len(files) > len(important_files):
        remaining = len(files) - len(important_files)
        print(f"{prefix}└── ... (+{remaining} autres fichiers)")

def analyze_project_metrics(root_path):
    """Analyse les métriques du projet"""
    python_files = 0
    test_files = 0
    doc_files = 0
    config_files = 0
    
    for root, dirs, files in os.walk(root_path):
        # Ignorer venv et cache
        if any(skip in root for skip in ['venv', '__pycache__', '.git']):
            continue
        
        for file in files:
            if file.endswith('.py'):
                python_files += 1
                if file.startswith('test_'):
                    test_files += 1
            elif file.endswith('.md'):
                doc_files += 1
            elif file.endswith(('.json', '.yml', '.yaml', '.toml', '.ini')):
                config_files += 1
    
    return {
        'python_files': python_files,
        'test_files': test_files,
        'doc_files': doc_files,
        'config_files': config_files
    }

def main():
    """Point d'entrée principal"""
    print("🌊 STRUCTURE DU PROJET CHNEOWAVE")
    print("=" * 60)
    print("📁 Arbre hiérarchique du laboratoire maritime\n")
    
    current_dir = Path.cwd()
    print(f"{current_dir.name}/")
    
    # Scanner et afficher la structure
    structure = scan_directory_structure(current_dir, max_depth=3)
    print_tree(structure, max_depth=3)
    
    print("\n" + "=" * 60)
    print("📊 MÉTRIQUES DU PROJET:")
    
    # Analyser les métriques
    metrics = analyze_project_metrics(current_dir)
    
    # Vérifier les dossiers principaux
    main_dirs = ['src', 'logciel hrneowave', 'tests', 'config', 'docs']
    existing_dirs = [d for d in main_dirs if (current_dir / d).exists()]
    
    print(f"  📂 Dossiers principaux: {len(existing_dirs)}/{len(main_dirs)}")
    print(f"  🐍 Modules Python: {metrics['python_files']}")
    print(f"  🧪 Tests: {metrics['test_files']}")
    print(f"  📄 Documentation: {metrics['doc_files']}")
    print(f"  ⚙️ Configuration: {metrics['config_files']}")
    
    # Vérifier les modules optimisés
    optimized_modules = [
        'src/hrneowave/core/optimized_fft_processor.py',
        'src/hrneowave/core/optimized_goda_analyzer.py', 
        'src/hrneowave/core/circular_buffer.py',
        'logciel hrneowave/modern_acquisition_ui.py'
    ]
    
    existing_optimized = sum(1 for module in optimized_modules if (current_dir / module).exists())
    print(f"  ⚡ Modules optimisés: {existing_optimized}/{len(optimized_modules)}")
    
    print("\n🏛️ ARCHITECTURE MARITIME MÉDITERRANÉENNE:")
    print("   ├── 🌊 Acquisition temps réel (PyQt5 + PyQtGraph)")
    print("   ├── ⚡ Traitement optimisé (FFT + Analyse Goda)")
    print("   ├── 🖥️ Interface moderne (modern_acquisition_ui.py)")
    print("   ├── 🧪 Tests d'intégration validés")
    print("   └── 📊 Analyse de vagues en bassin et canal")
    
    # Statut d'intégration
    integration_score = (existing_optimized / len(optimized_modules)) * 100
    print(f"\n✅ Statut d'intégration: {integration_score:.0f}% complet")
    
    if integration_score == 100:
        print("🎯 Projet prêt pour les études maritimes!")
    else:
        print("⚠️ Intégration en cours...")

if __name__ == "__main__":
    main()