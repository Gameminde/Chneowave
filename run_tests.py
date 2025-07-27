#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'exécution des tests CHNeoWave

Ce script permet d'exécuter les tests avec différentes configurations :
- Tests unitaires rapides
- Tests d'intégration
- Tests de performance
- Tests complets avec couverture
- Tests spécifiques par module

Usage:
    python run_tests.py [options]
    
Exemples:
    python run_tests.py --quick          # Tests rapides seulement
    python run_tests.py --integration    # Tests d'intégration
    python run_tests.py --performance    # Tests de performance
    python run_tests.py --coverage       # Tests avec couverture complète
    python run_tests.py --module validators  # Tests d'un module spécifique
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def run_command(cmd, description=""):
    """Exécuter une commande et afficher le résultat"""
    if description:
        print(f"\n{'='*60}")
        print(f"🔄 {description}")
        print(f"{'='*60}")
    
    print(f"Commande: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.stdout:
            print("\n📋 Sortie:")
            print(result.stdout)
            
        if result.stderr:
            print("\n⚠️ Erreurs/Avertissements:")
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"\n✅ {description or 'Commande'} terminée avec succès")
        else:
            print(f"\n❌ {description or 'Commande'} échouée (code: {result.returncode})")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n💥 Erreur lors de l'exécution: {e}")
        return False

def check_dependencies():
    """Vérifier que les dépendances nécessaires sont installées"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = ['pytest', 'pytest-cov', 'pytest-timeout']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Packages manquants: {', '.join(missing_packages)}")
        print("\n📦 Installation des dépendances...")
        
        install_cmd = [sys.executable, '-m', 'pip', 'install'] + missing_packages
        if not run_command(install_cmd, "Installation des dépendances"):
            print("\n💥 Échec de l'installation des dépendances")
            return False
    
    print("✅ Toutes les dépendances sont disponibles")
    return True

def run_quick_tests():
    """Exécuter les tests rapides (unitaires seulement)"""
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-m', 'not slow and not integration and not performance',
        '-v',
        '--tb=short',
        '--disable-warnings'
    ]
    
    return run_command(cmd, "Tests rapides (unitaires)")

def run_integration_tests():
    """Exécuter les tests d'intégration"""
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-m', 'integration',
        '-v',
        '--tb=short'
    ]
    
    return run_command(cmd, "Tests d'intégration")

def run_performance_tests():
    """Exécuter les tests de performance"""
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-m', 'performance',
        '-v',
        '--tb=short',
        '--timeout=60'
    ]
    
    return run_command(cmd, "Tests de performance")

def run_coverage_tests():
    """Exécuter tous les tests avec couverture de code"""
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '--cov=src/hrneowave',
        '--cov-report=html:htmlcov',
        '--cov-report=term-missing',
        '--cov-report=xml',
        '--cov-fail-under=80',
        '-v'
    ]
    
    success = run_command(cmd, "Tests complets avec couverture")
    
    if success:
        coverage_html = project_root / "htmlcov" / "index.html"
        if coverage_html.exists():
            print(f"\n📊 Rapport de couverture HTML généré: {coverage_html}")
            print("   Ouvrez ce fichier dans votre navigateur pour voir le détail")
    
    return success

def run_module_tests(module_name):
    """Exécuter les tests d'un module spécifique"""
    test_file = project_root / "tests" / f"test_{module_name}.py"
    
    if not test_file.exists():
        print(f"❌ Fichier de test non trouvé: {test_file}")
        return False
    
    cmd = [
        sys.executable, '-m', 'pytest',
        str(test_file),
        '-v',
        '--tb=short'
    ]
    
    return run_command(cmd, f"Tests du module {module_name}")

def run_all_tests():
    """Exécuter tous les tests"""
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short'
    ]
    
    return run_command(cmd, "Tous les tests")

def run_specific_test(test_path):
    """Exécuter un test spécifique"""
    cmd = [
        sys.executable, '-m', 'pytest',
        test_path,
        '-v',
        '--tb=long'
    ]
    
    return run_command(cmd, f"Test spécifique: {test_path}")

def lint_code():
    """Exécuter les vérifications de qualité de code"""
    print("\n🔍 Vérification de la qualité du code...")
    
    # Vérifier si flake8 est disponible
    try:
        import flake8
        cmd = ['flake8', 'src/', 'tests/', '--max-line-length=100', '--ignore=E203,W503']
        run_command(cmd, "Vérification flake8")
    except ImportError:
        print("⚠️ flake8 non installé, vérification ignorée")
    
    # Vérifier si black est disponible
    try:
        import black
        cmd = ['black', '--check', '--diff', 'src/', 'tests/']
        run_command(cmd, "Vérification formatage Black")
    except ImportError:
        print("⚠️ black non installé, vérification ignorée")

def generate_test_report():
    """Générer un rapport de test complet"""
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '--html=test_report.html',
        '--self-contained-html',
        '--cov=src/hrneowave',
        '--cov-report=html:htmlcov',
        '-v'
    ]
    
    success = run_command(cmd, "Génération du rapport de test")
    
    if success:
        report_file = project_root / "test_report.html"
        if report_file.exists():
            print(f"\n📋 Rapport de test généré: {report_file}")
    
    return success

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Script d'exécution des tests CHNeoWave",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python run_tests.py --quick              # Tests rapides
  python run_tests.py --integration        # Tests d'intégration
  python run_tests.py --performance        # Tests de performance
  python run_tests.py --coverage           # Tests avec couverture
  python run_tests.py --module validators  # Tests d'un module
  python run_tests.py --test tests/test_validators.py::TestProjectValidator::test_validate_project_name_valid
  python run_tests.py --all                # Tous les tests
  python run_tests.py --report             # Rapport complet
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--quick', action='store_true', help='Tests rapides (unitaires seulement)')
    group.add_argument('--integration', action='store_true', help='Tests d\'intégration')
    group.add_argument('--performance', action='store_true', help='Tests de performance')
    group.add_argument('--coverage', action='store_true', help='Tests avec couverture de code')
    group.add_argument('--module', type=str, help='Tests d\'un module spécifique')
    group.add_argument('--test', type=str, help='Test spécifique à exécuter')
    group.add_argument('--all', action='store_true', help='Tous les tests')
    group.add_argument('--report', action='store_true', help='Générer un rapport complet')
    
    parser.add_argument('--lint', action='store_true', help='Vérifier la qualité du code')
    parser.add_argument('--no-deps-check', action='store_true', help='Ignorer la vérification des dépendances')
    
    args = parser.parse_args()
    
    print("🧪 CHNeoWave - Exécution des Tests")
    print("=" * 40)
    
    # Vérifier les dépendances
    if not args.no_deps_check:
        if not check_dependencies():
            sys.exit(1)
    
    # Vérifier la qualité du code si demandé
    if args.lint:
        lint_code()
    
    # Exécuter les tests selon l'option choisie
    success = True
    
    if args.quick:
        success = run_quick_tests()
    elif args.integration:
        success = run_integration_tests()
    elif args.performance:
        success = run_performance_tests()
    elif args.coverage:
        success = run_coverage_tests()
    elif args.module:
        success = run_module_tests(args.module)
    elif args.test:
        success = run_specific_test(args.test)
    elif args.all:
        success = run_all_tests()
    elif args.report:
        success = generate_test_report()
    
    # Résumé final
    print("\n" + "=" * 60)
    if success:
        print("🎉 Tests terminés avec succès!")
        sys.exit(0)
    else:
        print("💥 Certains tests ont échoué")
        sys.exit(1)

if __name__ == '__main__':
    main()