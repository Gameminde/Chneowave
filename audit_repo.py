#!/usr/bin/env python3
"""
Script d'audit complet du dépôt Chneowave
Basé sur mcp_jobs/audit_repo.yml

Objectif : cartographier le dépôt, détecter doublons/modules orphelins,
vérifier que la GUI importe bien les optimisations, lister ce qui reste
à fusionner et proposer un plan de correction.
"""

import os
import sys
import pathlib
import ast
import importlib.util
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import textwrap

class RepositoryAuditor:
    def __init__(self, repo_root: str):
        self.repo_root = pathlib.Path(repo_root)
        self.build_dir = self.repo_root / "build"
        self.build_dir.mkdir(exist_ok=True)
        
        # Chemins à ignorer
        self.ignore_patterns = [
            "venv*/", "__pycache__/", "logs/**", "exports/**",
            ".git/", ".pytest_cache/", "*.pyc"
        ]
        
    def should_ignore(self, path: pathlib.Path) -> bool:
        """Vérifie si un chemin doit être ignoré"""
        try:
            path_str = str(path.relative_to(self.repo_root))
            for pattern in self.ignore_patterns:
                if pattern.endswith("/**"):
                    if path_str.startswith(pattern[:-3]):
                        return True
                elif pattern.endswith("/"):
                    if pattern[:-1] in path_str.split(os.sep):
                        return True
                elif pattern.startswith("*."):
                    if path_str.endswith(pattern[1:]):
                        return True
            return False
        except ValueError:
            # Si le chemin n'est pas relatif au repo_root
            return True
        
    def scan_tree(self) -> Dict:
        """Tâche 1: Analyse récursive du dépôt"""
        print("🔍 Analyse de l'arborescence du dépôt...")
        
        python_dirs = {}
        processed_dirs = 0
        
        try:
            for root, dirs, files in os.walk(self.repo_root):
                root_path = pathlib.Path(root)
                processed_dirs += 1
                
                if processed_dirs % 10 == 0:
                    print(f"   Traitement dossier {processed_dirs}: {root_path.name}")
                
                # Ignorer les dossiers spécifiés
                if self.should_ignore(root_path):
                    continue
                    
                # Chercher les fichiers Python
                py_files = [f for f in files if f.endswith('.py')]
                
                if py_files:
                    total_lines = 0
                    for py_file in py_files:
                        try:
                            file_path = root_path / py_file
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                total_lines += len(f.readlines())
                        except Exception as e:
                            print(f"   ⚠️ Erreur lecture {py_file}: {e}")
                            
                    # Vérifier si c'est un package importable
                    is_package = (root_path / "__init__.py").exists()
                    
                    try:
                        rel_path = root_path.relative_to(self.repo_root)
                        python_dirs[str(rel_path)] = {
                            'nb_files': len(py_files),
                            'total_lines': total_lines,
                            'is_package': is_package,
                            'files': py_files
                        }
                    except ValueError as e:
                        print(f"   ⚠️ Erreur chemin relatif {root_path}: {e}")
                        
        except Exception as e:
            print(f"❌ Erreur durant scan_tree: {e}")
            raise
                
        # Générer le rapport
        report_path = self.build_dir / "AUDIT_TREE.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Audit de l'arborescence Python\n\n")
            f.write(f"**Dépôt analysé:** {self.repo_root}\n\n")
            f.write(f"**Nombre de dossiers Python:** {len(python_dirs)}\n\n")
            
            f.write("## Détail par dossier\n\n")
            for dir_path, info in sorted(python_dirs.items()):
                f.write(f"### {dir_path}\n")
                f.write(f"- **Fichiers Python:** {info['nb_files']}\n")
                f.write(f"- **Lignes totales:** {info['total_lines']}\n")
                f.write(f"- **Package importable:** {'✅' if info['is_package'] else '❌'}\n")
                f.write(f"- **Fichiers:** {', '.join(info['files'])}\n\n")
                
        print(f"✅ Rapport d'arborescence généré: {report_path}")
        return python_dirs
        
    def detect_duplicates(self) -> Dict:
        """Tâche 2: Détection de doublons & imports cassés"""
        print("🔍 Détection des doublons et imports cassés...")
        
        # Collecter tous les fichiers Python
        all_py_files = []
        for root, dirs, files in os.walk(self.repo_root):
            root_path = pathlib.Path(root)
            if self.should_ignore(root_path):
                continue
                
            for file in files:
                if file.endswith('.py'):
                    all_py_files.append(root_path / file)
                    
        # Détecter les doublons par nom de fichier
        file_names = defaultdict(list)
        for file_path in all_py_files:
            file_names[file_path.name].append(file_path)
            
        duplicates = {name: paths for name, paths in file_names.items() if len(paths) > 1}
        
        # Analyser les imports problématiques
        problematic_imports = []
        fixes_orphans = []
        
        for file_path in all_py_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Chercher les imports problématiques
                if 'from HRNeoWave' in content or 'from logiciel hrneowave' in content:
                    problematic_imports.append(file_path)
                    
                # Vérifier si c'est un fichier dans __fixes__ non intégré
                if '__fixes__' in str(file_path):
                    fixes_orphans.append(file_path)
                    
            except Exception as e:
                print(f"⚠️ Erreur lecture {file_path}: {e}")
                
        # Générer le rapport
        report_path = self.build_dir / "AUDIT_DUPES.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Audit des doublons et imports\n\n")
            
            f.write("## Modules homonymes\n\n")
            if duplicates:
                for name, paths in duplicates.items():
                    f.write(f"### {name}\n")
                    for path in paths:
                        rel_path = path.relative_to(self.repo_root)
                        f.write(f"- {rel_path}\n")
                    f.write("\n")
            else:
                f.write("✅ Aucun doublon détecté\n\n")
                
            f.write("## Imports problématiques\n\n")
            if problematic_imports:
                for file_path in problematic_imports:
                    rel_path = file_path.relative_to(self.repo_root)
                    f.write(f"- {rel_path}\n")
            else:
                f.write("✅ Aucun import problématique détecté\n\n")
                
            f.write("## Fichiers orphelins dans __fixes__\n\n")
            if fixes_orphans:
                for file_path in fixes_orphans:
                    rel_path = file_path.relative_to(self.repo_root)
                    f.write(f"- {rel_path}\n")
            else:
                f.write("✅ Aucun fichier orphelin dans __fixes__\n\n")
                
        print(f"✅ Rapport de doublons généré: {report_path}")
        return {
            'duplicates': duplicates,
            'problematic_imports': problematic_imports,
            'fixes_orphans': fixes_orphans
        }
        
    def check_gui_backend(self) -> Dict:
        """Tâche 3: Vérification d'intégration GUI ↔ optimisations"""
        print("🔍 Vérification de l'intégration GUI...")
        
        results = {
            'acquisition_controller_ok': False,
            'processing_worker_ok': False,
            'import_test_ok': False,
            'issues': []
        }
        
        # Vérifier les fichiers GUI principaux
        gui_files = [
            self.repo_root / "logciel hrneowave" / "acquisition.py",
            self.repo_root / "logciel hrneowave" / "main.py",
            self.repo_root / "src" / "hrneowave" / "core" / "acquisition_controller.py"
        ]
        
        for gui_file in gui_files:
            if gui_file.exists():
                try:
                    with open(gui_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Analyser les imports
                    if 'AcquisitionController' in content:
                        if 'src.hrneowave' in content or 'from hrneowave' in content:
                            results['acquisition_controller_ok'] = True
                        else:
                            results['issues'].append(f"AcquisitionController dans {gui_file.name} n'utilise pas src/hrneowave")
                            
                    if 'ProcessingWorker' in content:
                        if 'optimized_fft' in content or 'optimized_goda' in content:
                            results['processing_worker_ok'] = True
                        else:
                            results['issues'].append(f"ProcessingWorker dans {gui_file.name} n'utilise pas les optimisations")
                            
                except Exception as e:
                    results['issues'].append(f"Erreur lecture {gui_file}: {e}")
                    
        # Test d'import simulé
        try:
            sys.path.insert(0, str(self.repo_root / "src"))
            import hrneowave
            results['import_test_ok'] = True
        except ImportError as e:
            results['issues'].append(f"Échec import hrneowave: {e}")
        except Exception as e:
            results['issues'].append(f"Erreur test import: {e}")
            
        # Générer le rapport
        report_path = self.build_dir / "AUDIT_GUI.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Audit de l'intégration GUI\n\n")
            
            f.write("## Vérifications\n\n")
            f.write(f"- **AcquisitionController depuis src/hrneowave:** {'✅' if results['acquisition_controller_ok'] else '❌'}\n")
            f.write(f"- **ProcessingWorker avec optimisations:** {'✅' if results['processing_worker_ok'] else '❌'}\n")
            f.write(f"- **Test d'import hrneowave:** {'✅' if results['import_test_ok'] else '❌'}\n\n")
            
            if results['issues']:
                f.write("## Problèmes détectés\n\n")
                for issue in results['issues']:
                    f.write(f"- {issue}\n")
            else:
                f.write("✅ Aucun problème détecté\n\n")
                
        print(f"✅ Rapport GUI généré: {report_path}")
        return results
        
    def audit_summary(self):
        """Tâche 4: Synthèse de l'audit"""
        print("📋 Génération de la synthèse d'audit...")
        
        # Concaténer tous les rapports
        report_files = ["AUDIT_TREE.md", "AUDIT_DUPES.md", "AUDIT_GUI.md"]
        complete_report = self.build_dir / "AUDIT_REPO_COMPLETE.md"
        
        with open(complete_report, 'w', encoding='utf-8') as out:
            out.write("# Audit complet du dépôt Chneowave\n\n")
            out.write(f"**Date:** {pathlib.Path().cwd()}\n")
            out.write(f"**Dépôt:** {self.repo_root}\n\n")
            
            for report_file in report_files:
                report_path = self.build_dir / report_file
                if report_path.exists():
                    out.write(f"\n\n---\n\n")
                    content = report_path.read_text(encoding='utf-8')
                    out.write(content)
                    
        # Afficher un résumé
        content = complete_report.read_text(encoding='utf-8')
        summary = textwrap.shorten(content, 4000, placeholder="…")
        
        print("\n" + "="*60)
        print("📋 RÉSUMÉ DE L'AUDIT")
        print("="*60)
        print(summary)
        print("="*60)
        
        print(f"\n✅ Rapport complet généré: {complete_report}")
        
    def run_full_audit(self):
        """Exécute l'audit complet"""
        print("🚀 Démarrage de l'audit complet du dépôt Chneowave\n")
        
        try:
            # Exécuter toutes les tâches
            self.scan_tree()
            self.detect_duplicates()
            self.check_gui_backend()
            self.audit_summary()
            
            print("\n✅ Audit complet terminé avec succès!")
            print(f"📁 Rapports disponibles dans: {self.build_dir}")
            
        except Exception as e:
            print(f"❌ Erreur durant l'audit: {e}")
            raise

def main():
    """Point d'entrée principal"""
    repo_root = pathlib.Path(__file__).parent
    auditor = RepositoryAuditor(repo_root)
    auditor.run_full_audit()

if __name__ == "__main__":
    main()