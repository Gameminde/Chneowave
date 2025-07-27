#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation complète du système CHNeoWave

Ce script effectue une validation complète du système :
- Vérification de l'environnement
- Tests de tous les modules
- Validation de l'intégration
- Tests de performance
- Génération de rapports

Usage:
    python validate_system.py [--quick] [--no-performance] [--output-dir DIR]
"""

import sys
import os
import argparse
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

class SystemValidator:
    """Validateur système pour CHNeoWave"""
    
    def __init__(self, output_dir=None, quick_mode=False, skip_performance=False):
        self.project_root = project_root
        self.output_dir = Path(output_dir) if output_dir else project_root / "validation_reports"
        self.quick_mode = quick_mode
        self.skip_performance = skip_performance
        
        # Créer le répertoire de sortie
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialiser le rapport de validation
        self.validation_report = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {},
            "environment_check": {},
            "module_tests": {},
            "integration_tests": {},
            "performance_tests": {},
            "overall_status": "UNKNOWN",
            "recommendations": []
        }
        
    def log(self, message, level="INFO"):
        """Logger avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "DEBUG": "🔍"
        }.get(level, "📝")
        
        print(f"[{timestamp}] {prefix} {message}")
        
    def run_command(self, cmd, description="", capture_output=True):
        """Exécuter une commande et retourner le résultat"""
        self.log(f"Exécution: {description or ' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=capture_output, 
                text=True, 
                cwd=self.project_root,
                timeout=300  # 5 minutes max
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout if capture_output else "",
                "stderr": result.stderr if capture_output else "",
                "command": " ".join(cmd)
            }
            
        except subprocess.TimeoutExpired:
            self.log(f"Timeout lors de l'exécution de: {' '.join(cmd)}", "ERROR")
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": "Timeout expired",
                "command": " ".join(cmd)
            }
        except Exception as e:
            self.log(f"Erreur lors de l'exécution: {e}", "ERROR")
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "command": " ".join(cmd)
            }
    
    def check_system_info(self):
        """Collecter les informations système"""
        self.log("Collecte des informations système", "INFO")
        
        try:
            import platform
            import psutil
            
            self.validation_report["system_info"] = {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "architecture": platform.architecture()[0],
                "processor": platform.processor(),
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "disk_free_gb": round(psutil.disk_usage('.').free / (1024**3), 2)
            }
            
            self.log(f"Système: {self.validation_report['system_info']['platform']}", "SUCCESS")
            self.log(f"Python: {self.validation_report['system_info']['python_version']}", "SUCCESS")
            self.log(f"Mémoire: {self.validation_report['system_info']['memory_total_gb']} GB", "SUCCESS")
            
        except Exception as e:
            self.log(f"Erreur collecte système: {e}", "ERROR")
            self.validation_report["system_info"]["error"] = str(e)
    
    def check_environment(self):
        """Vérifier l'environnement de développement"""
        self.log("Vérification de l'environnement", "INFO")
        
        env_check = {
            "python_path": sys.executable,
            "working_directory": str(self.project_root),
            "src_directory_exists": (self.project_root / "src").exists(),
            "tests_directory_exists": (self.project_root / "tests").exists(),
            "required_packages": {},
            "optional_packages": {}
        }
        
        # Vérifier les packages requis
        required_packages = [
            'pytest', 'pytest-cov', 'pytest-timeout', 'psutil', 
            'numpy', 'scipy', 'matplotlib', 'PyQt6'
        ]
        
        for package in required_packages:
            try:
                if package == 'PyQt6':
                    import PyQt6
                    env_check["required_packages"][package] = "OK"
                else:
                    __import__(package.replace('-', '_'))
                    env_check["required_packages"][package] = "OK"
            except ImportError:
                env_check["required_packages"][package] = "MISSING"
                self.log(f"Package manquant: {package}", "WARNING")
        
        # Vérifier les packages optionnels
        optional_packages = ['black', 'flake8', 'mypy', 'sphinx']
        
        for package in optional_packages:
            try:
                __import__(package.replace('-', '_'))
                env_check["optional_packages"][package] = "OK"
            except ImportError:
                env_check["optional_packages"][package] = "MISSING"
        
        self.validation_report["environment_check"] = env_check
        
        # Vérifier si l'environnement est valide
        missing_required = [pkg for pkg, status in env_check["required_packages"].items() if status == "MISSING"]
        
        if missing_required:
            self.log(f"Packages requis manquants: {', '.join(missing_required)}", "ERROR")
            return False
        else:
            self.log("Environnement valide", "SUCCESS")
            return True
    
    def test_module_imports(self):
        """Tester l'importation de tous les modules"""
        self.log("Test d'importation des modules", "INFO")
        
        modules_to_test = [
            'hrneowave.core.validators',
            'hrneowave.core.error_handler',
            'hrneowave.core.performance_monitor',
            'hrneowave.gui.controllers.main_controller',
            'hrneowave.gui.views.welcome_view'
        ]
        
        import_results = {}
        
        for module in modules_to_test:
            try:
                __import__(module)
                import_results[module] = "SUCCESS"
                self.log(f"Import réussi: {module}", "SUCCESS")
            except Exception as e:
                import_results[module] = f"ERROR: {str(e)}"
                self.log(f"Échec import {module}: {e}", "ERROR")
        
        self.validation_report["module_tests"]["imports"] = import_results
        
        failed_imports = [mod for mod, status in import_results.items() if status.startswith("ERROR")]
        return len(failed_imports) == 0
    
    def run_unit_tests(self):
        """Exécuter les tests unitaires"""
        self.log("Exécution des tests unitaires", "INFO")
        
        if self.quick_mode:
            cmd = [
                sys.executable, '-m', 'pytest',
                'tests/',
                '-m', 'not slow and not integration and not performance',
                '--tb=short',
                '--disable-warnings',
                '-q'
            ]
        else:
            cmd = [
                sys.executable, '-m', 'pytest',
                'tests/',
                '-m', 'not integration and not performance',
                '--tb=short',
                '--disable-warnings'
            ]
        
        result = self.run_command(cmd, "Tests unitaires")
        self.validation_report["module_tests"]["unit_tests"] = result
        
        if result["success"]:
            self.log("Tests unitaires réussis", "SUCCESS")
        else:
            self.log("Échec des tests unitaires", "ERROR")
        
        return result["success"]
    
    def run_integration_tests(self):
        """Exécuter les tests d'intégration"""
        self.log("Exécution des tests d'intégration", "INFO")
        
        cmd = [
            sys.executable, '-m', 'pytest',
            'tests/',
            '-m', 'integration',
            '--tb=short',
            '-v'
        ]
        
        result = self.run_command(cmd, "Tests d'intégration")
        self.validation_report["integration_tests"] = result
        
        if result["success"]:
            self.log("Tests d'intégration réussis", "SUCCESS")
        else:
            self.log("Échec des tests d'intégration", "WARNING")
        
        return result["success"]
    
    def run_performance_tests(self):
        """Exécuter les tests de performance"""
        if self.skip_performance:
            self.log("Tests de performance ignorés", "INFO")
            return True
            
        self.log("Exécution des tests de performance", "INFO")
        
        cmd = [
            sys.executable, '-m', 'pytest',
            'tests/',
            '-m', 'performance',
            '--tb=short',
            '--timeout=120'
        ]
        
        result = self.run_command(cmd, "Tests de performance")
        self.validation_report["performance_tests"] = result
        
        if result["success"]:
            self.log("Tests de performance réussis", "SUCCESS")
        else:
            self.log("Échec des tests de performance", "WARNING")
        
        return result["success"]
    
    def test_error_handling(self):
        """Tester le système de gestion d'erreurs"""
        self.log("Test du système de gestion d'erreurs", "INFO")
        
        try:
            from hrneowave.core.error_handler import get_error_handler, ErrorCategory, CHNeoWaveError
            
            # Test basique du gestionnaire d'erreurs
            handler = get_error_handler()
            
            # Créer une erreur de test
            from hrneowave.core.error_handler import ErrorContext
            
            context = ErrorContext(
                component="SystemValidator",
                operation="test_error_handling",
                category=ErrorCategory.SYSTEM
            )
            
            test_error = CHNeoWaveError(
                message="Test de validation système",
                context=context
            )
            
            # Logger l'erreur
            handler.handle_error(test_error)
            
            # Vérifier que l'erreur a été enregistrée
            if len(handler.error_history) > 0:
                self.log("Gestionnaire d'erreurs fonctionnel", "SUCCESS")
                
                # Nettoyer l'erreur de test
                handler.clear_error_history()
                return True
            else:
                self.log("Gestionnaire d'erreurs non fonctionnel", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Erreur lors du test de gestion d'erreurs: {e}", "ERROR")
            return False
    
    def test_performance_monitoring(self):
        """Tester le système de monitoring de performance"""
        if self.skip_performance:
            return True
            
        self.log("Test du système de monitoring", "INFO")
        
        try:
            from hrneowave.core.performance_monitor import get_performance_monitor
            
            # Test basique du moniteur
            monitor = get_performance_monitor()
            
            # Collecter des métriques
            metrics = monitor.get_current_metrics()
            
            if metrics and hasattr(metrics, 'cpu_percent'):
                self.log(f"Monitoring fonctionnel (CPU: {metrics.cpu_percent:.1f}%)", "SUCCESS")
                return True
            else:
                self.log("Monitoring non fonctionnel", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Erreur lors du test de monitoring: {e}", "ERROR")
            return False
    
    def generate_recommendations(self):
        """Générer des recommandations basées sur les résultats"""
        recommendations = []
        
        # Vérifier l'environnement
        env_check = self.validation_report.get("environment_check", {})
        missing_required = [pkg for pkg, status in env_check.get("required_packages", {}).items() if status == "MISSING"]
        
        if missing_required:
            recommendations.append({
                "type": "CRITICAL",
                "message": f"Installer les packages requis: {', '.join(missing_required)}",
                "action": f"pip install {' '.join(missing_required)}"
            })
        
        missing_optional = [pkg for pkg, status in env_check.get("optional_packages", {}).items() if status == "MISSING"]
        if missing_optional:
            recommendations.append({
                "type": "SUGGESTION",
                "message": f"Installer les packages optionnels pour le développement: {', '.join(missing_optional)}",
                "action": f"pip install {' '.join(missing_optional)}"
            })
        
        # Vérifier les tests
        if not self.validation_report.get("module_tests", {}).get("unit_tests", {}).get("success", False):
            recommendations.append({
                "type": "CRITICAL",
                "message": "Corriger les échecs de tests unitaires",
                "action": "Examiner les logs de tests et corriger les erreurs"
            })
        
        if not self.validation_report.get("integration_tests", {}).get("success", False):
            recommendations.append({
                "type": "WARNING",
                "message": "Corriger les échecs de tests d'intégration",
                "action": "Vérifier la compatibilité entre les modules"
            })
        
        # Recommandations de performance
        system_info = self.validation_report.get("system_info", {})
        if system_info.get("memory_total_gb", 0) < 4:
            recommendations.append({
                "type": "WARNING",
                "message": "Mémoire système faible (< 4GB)",
                "action": "Considérer l'ajout de mémoire pour de meilleures performances"
            })
        
        self.validation_report["recommendations"] = recommendations
        return recommendations
    
    def determine_overall_status(self):
        """Déterminer le statut global du système"""
        # Vérifier les composants critiques
        critical_checks = [
            self.validation_report.get("environment_check", {}).get("src_directory_exists", False),
            self.validation_report.get("environment_check", {}).get("tests_directory_exists", False),
            len([pkg for pkg, status in self.validation_report.get("environment_check", {}).get("required_packages", {}).items() if status == "MISSING"]) == 0,
            self.validation_report.get("module_tests", {}).get("unit_tests", {}).get("success", False)
        ]
        
        if all(critical_checks):
            self.validation_report["overall_status"] = "HEALTHY"
        elif any(critical_checks):
            self.validation_report["overall_status"] = "WARNING"
        else:
            self.validation_report["overall_status"] = "CRITICAL"
    
    def save_report(self):
        """Sauvegarder le rapport de validation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"validation_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_report, f, indent=2, ensure_ascii=False)
        
        self.log(f"Rapport sauvegardé: {report_file}", "SUCCESS")
        
        # Créer aussi un rapport texte lisible
        text_report = self.output_dir / f"validation_summary_{timestamp}.txt"
        self.generate_text_report(text_report)
        
        return report_file
    
    def generate_text_report(self, output_file):
        """Générer un rapport texte lisible"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("CHNeoWave - Rapport de Validation Système\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Date: {self.validation_report['timestamp']}\n")
            f.write(f"Statut global: {self.validation_report['overall_status']}\n\n")
            
            # Informations système
            f.write("INFORMATIONS SYSTÈME\n")
            f.write("-" * 20 + "\n")
            system_info = self.validation_report.get('system_info', {})
            for key, value in system_info.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            # Environnement
            f.write("ENVIRONNEMENT\n")
            f.write("-" * 13 + "\n")
            env_check = self.validation_report.get('environment_check', {})
            
            f.write("Packages requis:\n")
            for pkg, status in env_check.get('required_packages', {}).items():
                f.write(f"  {pkg}: {status}\n")
            
            f.write("\nPackages optionnels:\n")
            for pkg, status in env_check.get('optional_packages', {}).items():
                f.write(f"  {pkg}: {status}\n")
            f.write("\n")
            
            # Tests
            f.write("RÉSULTATS DES TESTS\n")
            f.write("-" * 18 + "\n")
            
            unit_tests = self.validation_report.get('module_tests', {}).get('unit_tests', {})
            f.write(f"Tests unitaires: {'RÉUSSI' if unit_tests.get('success') else 'ÉCHEC'}\n")
            
            integration_tests = self.validation_report.get('integration_tests', {})
            f.write(f"Tests d'intégration: {'RÉUSSI' if integration_tests.get('success') else 'ÉCHEC'}\n")
            
            performance_tests = self.validation_report.get('performance_tests', {})
            if performance_tests:
                f.write(f"Tests de performance: {'RÉUSSI' if performance_tests.get('success') else 'ÉCHEC'}\n")
            f.write("\n")
            
            # Recommandations
            f.write("RECOMMANDATIONS\n")
            f.write("-" * 15 + "\n")
            for rec in self.validation_report.get('recommendations', []):
                f.write(f"[{rec['type']}] {rec['message']}\n")
                f.write(f"  Action: {rec['action']}\n\n")
        
        self.log(f"Rapport texte généré: {output_file}", "SUCCESS")
    
    def run_validation(self):
        """Exécuter la validation complète"""
        self.log("Début de la validation système CHNeoWave", "INFO")
        start_time = time.time()
        
        try:
            # 1. Informations système
            self.check_system_info()
            
            # 2. Vérification environnement
            env_ok = self.check_environment()
            if not env_ok:
                self.log("Environnement invalide, arrêt de la validation", "ERROR")
                self.validation_report["overall_status"] = "CRITICAL"
                return False
            
            # 3. Test d'importation des modules
            imports_ok = self.test_module_imports()
            if not imports_ok:
                self.log("Échec d'importation des modules", "ERROR")
            
            # 4. Tests unitaires
            unit_tests_ok = self.run_unit_tests()
            
            # 5. Tests d'intégration
            integration_ok = self.run_integration_tests()
            
            # 6. Tests de performance
            performance_ok = self.run_performance_tests()
            
            # 7. Test des systèmes critiques
            error_handling_ok = self.test_error_handling()
            monitoring_ok = self.test_performance_monitoring()
            
            # 8. Générer recommandations
            self.generate_recommendations()
            
            # 9. Déterminer le statut global
            self.determine_overall_status()
            
            # 10. Sauvegarder le rapport
            report_file = self.save_report()
            
            # Résumé final
            elapsed_time = time.time() - start_time
            self.log(f"Validation terminée en {elapsed_time:.1f}s", "INFO")
            self.log(f"Statut global: {self.validation_report['overall_status']}", 
                    "SUCCESS" if self.validation_report['overall_status'] == "HEALTHY" else "WARNING")
            
            return self.validation_report['overall_status'] in ["HEALTHY", "WARNING"]
            
        except Exception as e:
            self.log(f"Erreur critique lors de la validation: {e}", "ERROR")
            self.validation_report["overall_status"] = "CRITICAL"
            self.validation_report["critical_error"] = str(e)
            return False

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Validation complète du système CHNeoWave",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--quick', action='store_true', 
                       help='Mode rapide (tests unitaires seulement)')
    parser.add_argument('--no-performance', action='store_true',
                       help='Ignorer les tests de performance')
    parser.add_argument('--output-dir', type=str,
                       help='Répertoire de sortie pour les rapports')
    
    args = parser.parse_args()
    
    # Créer le validateur
    validator = SystemValidator(
        output_dir=args.output_dir,
        quick_mode=args.quick,
        skip_performance=args.no_performance
    )
    
    # Exécuter la validation
    success = validator.run_validation()
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()