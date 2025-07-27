#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'analyse de la qualité du code CHNeoWave
Génère des métriques et recommandations automatiques
"""

import os
import sys
import ast
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
import json
from datetime import datetime

class CodeQualityAnalyzer:
    """Analyseur de qualité de code pour CHNeoWave"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.src_path = self.project_root / "src" / "hrneowave"
        self.metrics = {
            'files_analyzed': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'functions': 0,
            'classes': 0,
            'docstring_coverage': 0,
            'complexity_issues': [],
            'import_issues': [],
            'naming_issues': [],
            'files_by_size': [],
            'dependencies': set(),
            'test_coverage_estimate': 0
        }
        
    def analyze_project(self) -> Dict[str, Any]:
        """Analyse complète du projet"""
        print("🔍 Analyse de la qualité du code CHNeoWave...")
        
        # Analyser tous les fichiers Python
        python_files = list(self.src_path.rglob("*.py"))
        self.metrics['files_analyzed'] = len(python_files)
        
        for file_path in python_files:
            self._analyze_file(file_path)
            
        # Analyser les tests
        self._analyze_test_coverage()
        
        # Analyser les dépendances
        self._analyze_dependencies()
        
        # Calculer les métriques finales
        self._calculate_final_metrics()
        
        return self.metrics
    
    def _analyze_file(self, file_path: Path):
        """Analyse un fichier Python individuel"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\n')
            self.metrics['total_lines'] += len(lines)
            
            # Compter les types de lignes
            code_lines = 0
            comment_lines = 0
            blank_lines = 0
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif stripped.startswith('#'):
                    comment_lines += 1
                else:
                    code_lines += 1
                    
            self.metrics['code_lines'] += code_lines
            self.metrics['comment_lines'] += comment_lines
            self.metrics['blank_lines'] += blank_lines
            
            # Analyser l'AST
            try:
                tree = ast.parse(content)
                self._analyze_ast(tree, file_path)
            except SyntaxError as e:
                print(f"⚠️ Erreur de syntaxe dans {file_path}: {e}")
                
            # Analyser la taille du fichier
            self.metrics['files_by_size'].append({
                'file': str(file_path.relative_to(self.project_root)),
                'lines': len(lines),
                'size_category': self._categorize_file_size(len(lines))
            })
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse de {file_path}: {e}")
    
    def _analyze_ast(self, tree: ast.AST, file_path: Path):
        """Analyse l'arbre syntaxique abstrait"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.metrics['functions'] += 1
                self._check_function_complexity(node, file_path)
                self._check_docstring(node, 'function', file_path)
                
            elif isinstance(node, ast.ClassDef):
                self.metrics['classes'] += 1
                self._check_docstring(node, 'class', file_path)
                self._check_naming_convention(node.name, 'class', file_path)
                
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.metrics['dependencies'].add(alias.name)
                    
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.metrics['dependencies'].add(node.module)
    
    def _check_function_complexity(self, node: ast.FunctionDef, file_path: Path):
        """Vérifie la complexité cyclomatique d'une fonction"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
                
        if complexity > 10:  # Seuil de complexité élevée
            self.metrics['complexity_issues'].append({
                'file': str(file_path.relative_to(self.project_root)),
                'function': node.name,
                'complexity': complexity,
                'line': node.lineno
            })
    
    def _check_docstring(self, node, node_type: str, file_path: Path):
        """Vérifie la présence de docstrings"""
        has_docstring = (ast.get_docstring(node) is not None)
        
        if not hasattr(self, '_docstring_stats'):
            self._docstring_stats = {'total': 0, 'with_docstring': 0}
            
        self._docstring_stats['total'] += 1
        if has_docstring:
            self._docstring_stats['with_docstring'] += 1
    
    def _check_naming_convention(self, name: str, name_type: str, file_path: Path):
        """Vérifie les conventions de nommage"""
        if name_type == 'class':
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                self.metrics['naming_issues'].append({
                    'file': str(file_path.relative_to(self.project_root)),
                    'type': 'class',
                    'name': name,
                    'issue': 'Should use PascalCase'
                })
    
    def _categorize_file_size(self, lines: int) -> str:
        """Catégorise la taille d'un fichier"""
        if lines < 50:
            return 'small'
        elif lines < 200:
            return 'medium'
        elif lines < 500:
            return 'large'
        else:
            return 'very_large'
    
    def _analyze_test_coverage(self):
        """Estime la couverture de tests"""
        test_files = list(self.project_root.rglob("test_*.py"))
        test_files.extend(list(self.project_root.rglob("*_test.py")))
        
        tests_dir = self.project_root / "tests"
        if tests_dir.exists():
            test_files.extend(list(tests_dir.rglob("*.py")))
            
        # Estimation simple basée sur le ratio fichiers de test / fichiers source
        source_files = len(list(self.src_path.rglob("*.py")))
        test_file_count = len([f for f in test_files if f.name != "__init__.py"])
        
        if source_files > 0:
            self.metrics['test_coverage_estimate'] = min(100, (test_file_count / source_files) * 100)
    
    def _analyze_dependencies(self):
        """Analyse les dépendances du projet"""
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Extraire le nom du package (avant ==, >=, etc.)
                            package = re.split(r'[><=!]', line)[0].strip()
                            self.metrics['dependencies'].add(package)
            except Exception as e:
                print(f"⚠️ Erreur lecture requirements.txt: {e}")
    
    def _calculate_final_metrics(self):
        """Calcule les métriques finales"""
        # Couverture de docstrings
        if hasattr(self, '_docstring_stats') and self._docstring_stats['total'] > 0:
            self.metrics['docstring_coverage'] = (
                self._docstring_stats['with_docstring'] / self._docstring_stats['total'] * 100
            )
        
        # Convertir les sets en listes pour la sérialisation JSON
        self.metrics['dependencies'] = sorted(list(self.metrics['dependencies']))
        
        # Trier les fichiers par taille
        self.metrics['files_by_size'].sort(key=lambda x: x['lines'], reverse=True)
    
    def generate_report(self) -> str:
        """Génère un rapport de qualité"""
        report = []
        report.append("# 📊 Rapport de Qualité du Code CHNeoWave")
        report.append(f"**Date:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append("")
        
        # Métriques générales
        report.append("## 📈 Métriques Générales")
        report.append(f"- **Fichiers analysés:** {self.metrics['files_analyzed']}")
        report.append(f"- **Lignes totales:** {self.metrics['total_lines']:,}")
        report.append(f"- **Lignes de code:** {self.metrics['code_lines']:,}")
        report.append(f"- **Lignes de commentaires:** {self.metrics['comment_lines']:,}")
        report.append(f"- **Fonctions:** {self.metrics['functions']}")
        report.append(f"- **Classes:** {self.metrics['classes']}")
        report.append("")
        
        # Qualité du code
        report.append("## 🎯 Indicateurs de Qualité")
        
        # Ratio commentaires/code
        if self.metrics['code_lines'] > 0:
            comment_ratio = (self.metrics['comment_lines'] / self.metrics['code_lines']) * 100
            report.append(f"- **Ratio commentaires/code:** {comment_ratio:.1f}%")
        
        report.append(f"- **Couverture docstrings:** {self.metrics['docstring_coverage']:.1f}%")
        report.append(f"- **Estimation couverture tests:** {self.metrics['test_coverage_estimate']:.1f}%")
        report.append("")
        
        # Problèmes de complexité
        if self.metrics['complexity_issues']:
            report.append("## ⚠️ Problèmes de Complexité")
            for issue in self.metrics['complexity_issues'][:5]:  # Top 5
                report.append(f"- **{issue['file']}:{issue['line']}** - Fonction `{issue['function']}` (complexité: {issue['complexity']})")
            if len(self.metrics['complexity_issues']) > 5:
                report.append(f"- ... et {len(self.metrics['complexity_issues']) - 5} autres")
            report.append("")
        
        # Fichiers volumineux
        large_files = [f for f in self.metrics['files_by_size'] if f['size_category'] in ['large', 'very_large']]
        if large_files:
            report.append("## 📄 Fichiers Volumineux")
            for file_info in large_files[:5]:
                report.append(f"- **{file_info['file']}** - {file_info['lines']} lignes ({file_info['size_category']})")
            report.append("")
        
        # Dépendances
        report.append("## 📦 Dépendances Principales")
        main_deps = [dep for dep in self.metrics['dependencies'] if not dep.startswith('hrneowave')]
        for dep in sorted(main_deps)[:10]:
            report.append(f"- {dep}")
        report.append("")
        
        # Recommandations
        report.append("## 💡 Recommandations")
        
        if self.metrics['docstring_coverage'] < 80:
            report.append("- 📝 **Améliorer la documentation** - Ajouter des docstrings aux fonctions et classes")
        
        if self.metrics['test_coverage_estimate'] < 50:
            report.append("- 🧪 **Augmenter la couverture de tests** - Ajouter des tests unitaires")
        
        if self.metrics['complexity_issues']:
            report.append("- 🔧 **Réduire la complexité** - Refactoriser les fonctions complexes")
        
        if large_files:
            report.append("- 📄 **Diviser les gros fichiers** - Séparer les responsabilités")
        
        report.append("")
        report.append("---")
        report.append("*Rapport généré automatiquement par l'Analyseur de Qualité CHNeoWave*")
        
        return "\n".join(report)

def main():
    """Point d'entrée principal"""
    project_root = Path(__file__).parent
    
    print("🚀 Lancement de l'analyse de qualité du code CHNeoWave")
    print(f"📁 Répertoire du projet: {project_root}")
    print()
    
    analyzer = CodeQualityAnalyzer(str(project_root))
    metrics = analyzer.analyze_project()
    
    # Générer le rapport
    report = analyzer.generate_report()
    
    # Sauvegarder le rapport
    report_file = project_root / "RAPPORT_QUALITE_CODE.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Sauvegarder les métriques JSON
    metrics_file = project_root / "metriques_qualite.json"
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ Analyse terminée!")
    print(f"📄 Rapport sauvegardé: {report_file}")
    print(f"📊 Métriques sauvegardées: {metrics_file}")
    print()
    print("📋 Résumé rapide:")
    print(f"   - {metrics['files_analyzed']} fichiers analysés")
    print(f"   - {metrics['total_lines']:,} lignes totales")
    print(f"   - {metrics['functions']} fonctions, {metrics['classes']} classes")
    print(f"   - Couverture docstrings: {metrics['docstring_coverage']:.1f}%")
    print(f"   - Estimation tests: {metrics['test_coverage_estimate']:.1f}%")
    
    if metrics['complexity_issues']:
        print(f"   - ⚠️ {len(metrics['complexity_issues'])} problèmes de complexité")
    else:
        print("   - ✅ Aucun problème de complexité majeur")

if __name__ == "__main__":
    main()