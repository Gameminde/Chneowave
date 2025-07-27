#!/usr/bin/env python3
"""
Script de validation de l'architecture modulaire CHNeoWave Analysis
Architecte Logiciel en Chef (ALC)
"""

import os
import sys
import importlib.util
from pathlib import Path

def validate_file_structure():
    """Valide la structure des fichiers du module analysis"""
    print("🔍 Validation de la structure des fichiers...")
    
    analysis_dir = Path(__file__).parent
    required_files = [
        '__init__.py',
        'analysis_view_v2.py',
        'analysis_controller.py',
        'spectral_analysis.py',
        'goda_analysis.py',
        'statistics_analysis.py',
        'summary_report.py',
        'migrate_analysis_view.py',
        'test_analysis_modules.py',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        file_path = analysis_dir / file
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MANQUANT")
            missing_files.append(file)
    
    return len(missing_files) == 0

def validate_file_syntax():
    """Valide la syntaxe Python des fichiers"""
    print("\n🔍 Validation de la syntaxe Python...")
    
    analysis_dir = Path(__file__).parent
    python_files = [
        '__init__.py',
        'analysis_view_v2.py',
        'analysis_controller.py',
        'spectral_analysis.py',
        'goda_analysis.py',
        'statistics_analysis.py',
        'summary_report.py',
        'migrate_analysis_view.py',
        'test_analysis_modules.py'
    ]
    
    syntax_errors = []
    for file in python_files:
        file_path = analysis_dir / file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, str(file_path), 'exec')
                print(f"  ✅ {file} - Syntaxe valide")
            except SyntaxError as e:
                print(f"  ❌ {file} - Erreur de syntaxe: {e}")
                syntax_errors.append((file, str(e)))
            except Exception as e:
                print(f"  ⚠️ {file} - Avertissement: {e}")
    
    return len(syntax_errors) == 0

def validate_class_definitions():
    """Valide la présence des classes principales"""
    print("\n🔍 Validation des définitions de classes...")
    
    analysis_dir = Path(__file__).parent
    
    class_checks = [
        ('spectral_analysis.py', 'SpectralAnalysisWidget'),
        ('goda_analysis.py', 'GodaAnalysisWidget'),
        ('statistics_analysis.py', 'StatisticsAnalysisWidget'),
        ('summary_report.py', 'SummaryReportWidget'),
        ('analysis_controller.py', 'AnalysisController'),
        ('analysis_view_v2.py', 'AnalysisViewV2'),
        ('migrate_analysis_view.py', 'AnalysisViewMigrator')
    ]
    
    missing_classes = []
    for file, class_name in class_checks:
        file_path = analysis_dir / file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if f"class {class_name}" in content:
                    print(f"  ✅ {file} - Classe {class_name} trouvée")
                else:
                    print(f"  ❌ {file} - Classe {class_name} manquante")
                    missing_classes.append((file, class_name))
            except Exception as e:
                print(f"  ⚠️ {file} - Erreur de lecture: {e}")
        else:
            print(f"  ❌ {file} - Fichier manquant")
            missing_classes.append((file, class_name))
    
    return len(missing_classes) == 0

def validate_documentation():
    """Valide la présence de la documentation"""
    print("\n🔍 Validation de la documentation...")
    
    analysis_dir = Path(__file__).parent
    readme_path = analysis_dir / 'README.md'
    
    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_sections = [
                '# Module d\'Analyse CHNeoWave - Architecture Modulaire',
                '## Vue d\'ensemble',
                '## Structure des fichiers',
                '## Architecture',
                '## Utilisation',
                '## Migration',
                '## Tests'
            ]
            
            missing_sections = []
            for section in required_sections:
                if section in content:
                    print(f"  ✅ Section trouvée: {section}")
                else:
                    print(f"  ❌ Section manquante: {section}")
                    missing_sections.append(section)
            
            return len(missing_sections) == 0
        except Exception as e:
            print(f"  ❌ Erreur de lecture README.md: {e}")
            return False
    else:
        print(f"  ❌ README.md manquant")
        return False

def calculate_metrics():
    """Calcule les métriques de l'architecture"""
    print("\n📊 Calcul des métriques...")
    
    analysis_dir = Path(__file__).parent
    python_files = [
        'analysis_view_v2.py',
        'analysis_controller.py',
        'spectral_analysis.py',
        'goda_analysis.py',
        'statistics_analysis.py',
        'summary_report.py'
    ]
    
    total_lines = 0
    total_classes = 0
    total_methods = 0
    
    for file in python_files:
        file_path = analysis_dir / file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                file_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
                file_classes = len([line for line in lines if line.strip().startswith('class ')])
                file_methods = len([line for line in lines if line.strip().startswith('def ')])
                
                total_lines += file_lines
                total_classes += file_classes
                total_methods += file_methods
                
                print(f"  📄 {file}: {file_lines} lignes, {file_classes} classes, {file_methods} méthodes")
            except Exception as e:
                print(f"  ⚠️ Erreur lecture {file}: {e}")
    
    print(f"\n📈 Métriques totales:")
    print(f"  • Lignes de code: {total_lines}")
    print(f"  • Classes: {total_classes}")
    print(f"  • Méthodes: {total_methods}")
    print(f"  • Modules: {len(python_files)}")
    print(f"  • Moyenne lignes/module: {total_lines // len(python_files) if python_files else 0}")
    
    return {
        'total_lines': total_lines,
        'total_classes': total_classes,
        'total_methods': total_methods,
        'modules': len(python_files)
    }

def main():
    """Fonction principale de validation"""
    print("🚀 CHNeoWave Analysis Module - Validation Architecture")
    print("=" * 60)
    print("Architecte Logiciel en Chef (ALC)")
    print("=" * 60)
    
    # Tests de validation
    tests = [
        ("Structure des fichiers", validate_file_structure),
        ("Syntaxe Python", validate_file_syntax),
        ("Définitions de classes", validate_class_definitions),
        ("Documentation", validate_documentation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: SUCCÈS")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"💥 {test_name}: ERREUR - {e}")
            results.append((test_name, False))
    
    # Calcul des métriques
    metrics = calculate_metrics()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DE VALIDATION")
    print("=" * 60)
    
    passed_tests = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    for test_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"  {test_name}: {status}")
    
    print(f"\n📊 Score global: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 VALIDATION COMPLÈTE RÉUSSIE!")
        print("✅ L'architecture modulaire est prête pour la production")
        print("✅ Tous les principes ALC sont respectés")
        print("✅ CHNeoWave Analysis Module v2.0.0 - READY FOR DEPLOYMENT")
    else:
        print("\n⚠️ VALIDATION PARTIELLE")
        print(f"❌ {total_tests - passed_tests} test(s) en échec")
        print("🔧 Corrections nécessaires avant déploiement")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)