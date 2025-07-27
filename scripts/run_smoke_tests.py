#!/usr/bin/env python3
"""
Script d'exécution des tests smoke CHNeoWave v1.1.0-beta
Validation rapide des fonctionnalités critiques
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import json
from datetime import datetime

def setup_environment():
    """Configuration de l'environnement de test"""
    # Variables d'environnement pour les tests
    os.environ['CHNEOWAVE_TEST_MODE'] = '1'
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    os.environ['CHNEOWAVE_LOG_LEVEL'] = 'WARNING'
    
    print("✓ Environnement de test configuré")

def check_dependencies():
    """Vérification des dépendances critiques"""
    required_packages = {
        'pytest': 'pytest',
        'pytest-qt': 'pytestqt',
        'PyQt5': 'PyQt5',
        'numpy': 'numpy',
        'scipy': 'scipy',
        'h5py': 'h5py',
        'reportlab': 'reportlab',
        'pyqtgraph': 'pyqtgraph'
    }
    
    missing = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print(f"❌ Packages manquants: {', '.join(missing)}")
        print("Installez-les avec: pip install " + ' '.join(missing))
        return False
    
    print("✓ Toutes les dépendances sont présentes")
    return True

def run_test_suite(test_file, timeout=60):
    """Exécute une suite de tests avec timeout"""
    test_path = Path('tests_smoke') / test_file
    
    if not test_path.exists():
        return {
            'status': 'error',
            'message': f'Fichier de test non trouvé: {test_path}',
            'duration': 0
        }
    
    print(f"\n🧪 Exécution: {test_file}")
    start_time = time.time()
    
    try:
        # Commande pytest avec options appropriées
        cmd = [
            sys.executable, '-m', 'pytest',
            str(test_path),
            '-v',                    # Verbose
            '--tb=short',           # Traceback court
            '--no-header',          # Pas d'en-tête
            '--disable-warnings',   # Désactiver les warnings
            f'--timeout={timeout}'  # Timeout par test
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 10  # Timeout global
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {test_file} - RÉUSSI ({duration:.1f}s)")
            return {
                'status': 'success',
                'duration': duration,
                'output': result.stdout
            }
        else:
            print(f"❌ {test_file} - ÉCHEC ({duration:.1f}s)")
            return {
                'status': 'failed',
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            }
    
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        print(f"⏰ {test_file} - TIMEOUT ({duration:.1f}s)")
        return {
            'status': 'timeout',
            'duration': duration,
            'message': f'Test timeout après {timeout}s'
        }
    
    except Exception as e:
        duration = time.time() - start_time
        print(f"💥 {test_file} - ERREUR ({duration:.1f}s): {e}")
        return {
            'status': 'error',
            'duration': duration,
            'message': str(e)
        }

def generate_report(results):
    """Génère un rapport de validation"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'version': 'CHNeoWave v1.1.0-beta',
        'total_tests': len(results),
        'passed': sum(1 for r in results.values() if r['status'] == 'success'),
        'failed': sum(1 for r in results.values() if r['status'] == 'failed'),
        'errors': sum(1 for r in results.values() if r['status'] == 'error'),
        'timeouts': sum(1 for r in results.values() if r['status'] == 'timeout'),
        'total_duration': sum(r['duration'] for r in results.values()),
        'results': results
    }
    
    # Sauvegarde JSON
    report_file = f"smoke_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Rapport texte
    print("\n" + "=" * 60)
    print("📊 RAPPORT DE VALIDATION SMOKE TESTS")
    print("=" * 60)
    print(f"Version: {report['version']}")
    print(f"Date: {report['timestamp']}")
    print(f"Durée totale: {report['total_duration']:.1f}s")
    print()
    print(f"Tests exécutés: {report['total_tests']}")
    print(f"✅ Réussis: {report['passed']}")
    print(f"❌ Échecs: {report['failed']}")
    print(f"💥 Erreurs: {report['errors']}")
    print(f"⏰ Timeouts: {report['timeouts']}")
    
    # Détails par test
    print("\n📋 DÉTAILS PAR TEST:")
    for test_name, result in results.items():
        status_icon = {
            'success': '✅',
            'failed': '❌',
            'error': '💥',
            'timeout': '⏰'
        }.get(result['status'], '❓')
        
        print(f"{status_icon} {test_name}: {result['status'].upper()} ({result['duration']:.1f}s)")
        
        if result['status'] != 'success' and 'message' in result:
            print(f"   └─ {result['message']}")
    
    # Verdict final
    print("\n" + "=" * 60)
    if report['failed'] == 0 and report['errors'] == 0 and report['timeouts'] == 0:
        print("🎉 VALIDATION RÉUSSIE - Tous les tests smoke sont passés!")
        print("CHNeoWave v1.1.0-beta est prêt pour la distribution.")
        success = True
    else:
        print("⚠️  VALIDATION ÉCHOUÉE - Des problèmes ont été détectés.")
        print("Corrigez les erreurs avant la distribution.")
        success = False
    
    print(f"Rapport détaillé: {report_file}")
    print("=" * 60)
    
    return success, report_file

def main():
    """Fonction principale"""
    print("🚀 CHNeoWave v1.1.0-beta - Tests Smoke")
    print("Validation des fonctionnalités critiques\n")
    
    # Vérifications préliminaires
    if not check_dependencies():
        sys.exit(1)
    
    setup_environment()
    
    # Liste des tests smoke
    smoke_tests = [
        'test_launch_gui.py',
        'test_export_hdf5.py',
        'test_calib_pdf.py'
    ]
    
    # Configuration des timeouts par test
    timeouts = {
        'test_launch_gui.py': 30,
        'test_export_hdf5.py': 45,
        'test_calib_pdf.py': 20
    }
    
    # Exécution des tests
    results = {}
    start_time = time.time()
    
    for test_file in smoke_tests:
        timeout = timeouts.get(test_file, 60)
        results[test_file] = run_test_suite(test_file, timeout)
    
    total_duration = time.time() - start_time
    print(f"\n⏱️  Durée totale d'exécution: {total_duration:.1f}s")
    
    # Génération du rapport
    success, report_file = generate_report(results)
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()