#!/usr/bin/env python3
"""
Script pour obtenir uniquement le rapport de couverture
"""

import subprocess
import sys
import re

def get_coverage_report():
    """Exécute les tests et extrait le rapport de couverture"""
    try:
        # Exécuter pytest avec couverture
        result = subprocess.run([
            'venv\\Scripts\\python.exe', '-m', 'pytest', 'tests\\',
            '--cov=src', '--cov-report=term', '--tb=no', '-q'
        ], capture_output=True, text=True, cwd='.')
        
        # Extraire les lignes de couverture
        lines = result.stdout.split('\n')
        coverage_started = False
        coverage_lines = []
        
        for line in lines:
            if 'coverage:' in line.lower() or 'Name' in line and 'Stmts' in line:
                coverage_started = True
            
            if coverage_started:
                coverage_lines.append(line)
                
            # Arrêter après la ligne TOTAL
            if line.strip().startswith('TOTAL'):
                break
        
        # Afficher le rapport de couverture
        print("\n=== RAPPORT DE COUVERTURE ===")
        for line in coverage_lines:
            if line.strip():
                print(line)
        
        # Extraire le pourcentage total
        total_match = re.search(r'TOTAL.*?(\d+)%', result.stdout)
        if total_match:
            total_coverage = total_match.group(1)
            print(f"\n🎯 COUVERTURE TOTALE: {total_coverage}%")
        
        # Compter les tests
        test_summary = re.search(r'(\d+) failed, (\d+) passed, (\d+) skipped', result.stdout)
        if test_summary:
            failed, passed, skipped = test_summary.groups()
            total_tests = int(failed) + int(passed) + int(skipped)
            print(f"📊 TESTS: {passed}/{total_tests} réussis ({int(passed)/total_tests*100:.1f}%)")
            print(f"   - Réussis: {passed}")
            print(f"   - Échoués: {failed}")
            print(f"   - Ignorés: {skipped}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        return False

if __name__ == "__main__":
    success = get_coverage_report()
    sys.exit(0 if success else 1)