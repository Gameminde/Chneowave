#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic automatisé pour CHNeoWave
Identifie rapidement les problèmes critiques et génère un rapport détaillé

Auteur: Assistant IA
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import json
import importlib
import subprocess
import platform
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CHNeoWaveDiagnostic:
    """Diagnostic automatisé pour CHNeoWave"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {},
            'environment_check': {},
            'module_analysis': {},
            'critical_issues': [],
            'warnings': [],
            'recommendations': [],
            'overall_status': 'UNKNOWN'
        }
        
        self.critical_issues = []
        self.warnings = []
        
    def run_full_diagnostic(self) -> Dict[str, Any]:
        """Exécute le diagnostic complet"""
        logger.info("🚀 Démarrage du diagnostic CHNeoWave")
        
        try:
            # Collecte des informations système
            self._collect_system_info()
            
            # Vérification de l'environnement
            self._check_environment()
            
            # Analyse des modules
            self._analyze_modules()
            
            # Vérification des tests
            self._check_tests()
            
            # Analyse des dépendances
            self._analyze_dependencies()
            
            # Génération du rapport
            self._generate_report()
            
        except Exception as e:
            logger.error(f"Erreur lors du diagnostic: {e}")
            self.critical_issues.append(f"Erreur de diagnostic: {e}")
        
        return self.results
    
    def _collect_system_info(self):
        """Collecte les informations système"""
        logger.info("📊 Collecte des informations système")
        
        self.results['system_info'] = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'cpu_count': os.cpu_count(),
            'working_directory': os.getcwd(),
            'python_path': sys.executable
        }
        
        # Informations mémoire (si disponible)
        try:
            import psutil
            memory = psutil.virtual_memory()
            self.results['system_info']['memory_total_gb'] = round(memory.total / (1024**3), 2)
            self.results['system_info']['memory_available_gb'] = round(memory.available / (1024**3), 2)
        except ImportError:
            self.results['system_info']['memory_info'] = 'psutil non disponible'
    
    def _check_environment(self):
        """Vérifie l'environnement de développement"""
        logger.info("🔍 Vérification de l'environnement")
        
        env_check = {
            'src_directory_exists': False,
            'tests_directory_exists': False,
            'required_packages': {},
            'optional_packages': {},
            'qt_libraries': {},
            'python_path': os.environ.get('PYTHONPATH', 'Non défini')
        }
        
        # Vérification des répertoires
        src_path = Path('src')
        tests_path = Path('tests')
        
        if src_path.exists():
            env_check['src_directory_exists'] = True
            logger.info("✅ Répertoire src trouvé")
        else:
            self.warnings.append("Répertoire src manquant")
            
        if tests_path.exists():
            env_check['tests_directory_exists'] = True
            logger.info("✅ Répertoire tests trouvé")
        else:
            self.warnings.append("Répertoire tests manquant")
        
        # Vérification des packages requis
        required_packages = [
            'numpy', 'scipy', 'PyQt6', 'PySide6', 'h5py', 
            'pyqtgraph', 'pytest', 'pytest-qt'
        ]
        
        for package in required_packages:
            try:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'Version inconnue')
                env_check['required_packages'][package] = f"OK ({version})"
                logger.info(f"✅ {package}: {version}")
            except ImportError:
                env_check['required_packages'][package] = "MISSING"
                self.warnings.append(f"Package requis manquant: {package}")
        
        # Vérification des bibliothèques Qt
        qt_libs = ['PyQt6', 'PySide6']
        for qt_lib in qt_libs:
            try:
                if qt_lib == 'PyQt6':
                    import PyQt6.QtCore
                    version = PyQt6.QtCore.QT_VERSION_STR
                elif qt_lib == 'PySide6':
                    import PySide6.QtCore
                    version = PySide6.QtCore.__version__
                
                env_check['qt_libraries'][qt_lib] = f"OK ({version})"
                
                # Vérifier les conflits Qt
                if len(env_check['qt_libraries']) > 1:
                    self.critical_issues.append(f"CONFLIT: Plusieurs bibliothèques Qt détectées: {list(env_check['qt_libraries'].keys())}")
                    
            except ImportError:
                env_check['qt_libraries'][qt_lib] = "MISSING"
        
        self.results['environment_check'] = env_check
    
    def _analyze_modules(self):
        """Analyse les modules principaux"""
        logger.info("🔍 Analyse des modules")
        
        modules_to_check = [
            'hrneowave.core.config_manager',
            'hrneowave.core.error_handler',
            'hrneowave.core.performance_monitor',
            'hrneowave.gui.main_window',
            'hrneowave.acquisition.acquisition_controller'
        ]
        
        module_analysis = {}
        
        for module_name in modules_to_check:
            try:
                module = importlib.import_module(module_name)
                module_analysis[module_name] = "SUCCESS"
                
                # Vérification des attributs critiques
                if hasattr(module, '__file__'):
                    file_path = Path(module.__file__)
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        if file_size > 10000:  # Plus de 10KB
                            self.warnings.append(f"Module {module_name} très volumineux ({file_size} bytes)")
                
            except ImportError as e:
                module_analysis[module_name] = f"FAILED: {e}"
                self.critical_issues.append(f"Impossible d'importer {module_name}: {e}")
            except Exception as e:
                module_analysis[module_name] = f"ERROR: {e}"
                self.warnings.append(f"Erreur lors de l'import de {module_name}: {e}")
        
        self.results['module_analysis'] = module_analysis
    
    def _check_tests(self):
        """Vérifie l'état des tests"""
        logger.info("🧪 Vérification des tests")
        
        test_check = {
            'pytest_available': False,
            'test_files_count': 0,
            'test_execution': 'NOT_RUN'
        }
        
        # Vérifier pytest
        try:
            import pytest
            test_check['pytest_available'] = True
            test_check['pytest_version'] = pytest.__version__
        except ImportError:
            self.critical_issues.append("pytest non disponible")
            return
        
        # Compter les fichiers de test
        tests_dir = Path('tests')
        if tests_dir.exists():
            test_files = list(tests_dir.rglob('test_*.py'))
            test_check['test_files_count'] = len(test_files)
            logger.info(f"📁 {len(test_files)} fichiers de test trouvés")
        
        # Exécuter un test simple
        try:
            logger.info("🧪 Exécution d'un test simple...")
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', 'tests/', '--collect-only', '-q'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                test_check['test_execution'] = 'COLLECTION_OK'
                logger.info("✅ Collection des tests réussie")
            else:
                test_check['test_execution'] = f'COLLECTION_FAILED: {result.stderr}'
                self.warnings.append(f"Échec de la collection des tests: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            test_check['test_execution'] = 'TIMEOUT'
            self.critical_issues.append("Timeout lors de la collection des tests")
        except Exception as e:
            test_check['test_execution'] = f'ERROR: {e}'
            self.critical_issues.append(f"Erreur lors de l'exécution des tests: {e}")
        
        self.results['test_check'] = test_check
    
    def _analyze_dependencies(self):
        """Analyse les dépendances et conflits"""
        logger.info("🔧 Analyse des dépendances")
        
        deps_analysis = {
            'conflicts': [],
            'version_issues': [],
            'security_issues': []
        }
        
        # Vérifier les conflits Qt
        qt_imports = []
        try:
            import PyQt6
            qt_imports.append('PyQt6')
        except ImportError:
            pass
            
        try:
            import PySide6
            qt_imports.append('PySide6')
        except ImportError:
            pass
        
        if len(qt_imports) > 1:
            deps_analysis['conflicts'].append(f"Conflit Qt: {qt_imports}")
            self.critical_issues.append(f"Conflit entre bibliothèques Qt: {qt_imports}")
        
        # Vérifier pytest-qt
        try:
            import pytest_qt
            qt_version = getattr(pytest_qt, '__version__', 'Version inconnue')
            deps_analysis['pytest_qt'] = f"OK ({qt_version})"
        except ImportError:
            deps_analysis['pytest_qt'] = "MISSING"
            self.warnings.append("pytest-qt non disponible")
        
        # Vérifier pyqtgraph
        try:
            import pyqtgraph
            pg_version = getattr(pyqtgraph, '__version__', 'Version inconnue')
            deps_analysis['pyqtgraph'] = f"OK ({pg_version})"
        except ImportError:
            deps_analysis['pyqtgraph'] = "MISSING"
            self.warnings.append("pyqtgraph non disponible")
        
        self.results['dependencies_analysis'] = deps_analysis
    
    def _generate_report(self):
        """Génère le rapport final"""
        logger.info("📋 Génération du rapport")
        
        # Déterminer le statut global
        if self.critical_issues:
            self.results['overall_status'] = 'CRITICAL'
        elif self.warnings:
            self.results['overall_status'] = 'WARNING'
        else:
            self.results['overall_status'] = 'OK'
        
        # Ajouter les problèmes et recommandations
        self.results['critical_issues'] = self.critical_issues
        self.results['warnings'] = self.warnings
        
        # Générer les recommandations
        self._generate_recommendations()
        
        # Sauvegarder le rapport
        self._save_report()
    
    def _generate_recommendations(self):
        """Génère les recommandations basées sur l'analyse"""
        logger.info("💡 Génération des recommandations")
        
        recommendations = []
        
        # Recommandations basées sur les problèmes critiques
        if self.critical_issues:
            recommendations.append({
                'type': 'CRITICAL',
                'message': 'Résoudre les problèmes critiques avant tout déploiement',
                'priority': 'IMMEDIATE'
            })
        
        # Recommandations basées sur les conflits Qt
        if any('CONFLIT' in issue for issue in self.critical_issues):
            recommendations.append({
                'type': 'CONFLICT',
                'message': 'Standardiser sur une seule bibliothèque Qt (PyQt6 recommandé)',
                'priority': 'HIGH'
            })
        
        # Recommandations basées sur les tests
        test_check = self.results.get('test_check', {})
        if test_check.get('test_execution') != 'COLLECTION_OK':
            recommendations.append({
                'type': 'TESTING',
                'message': 'Corriger la configuration pytest et les tests',
                'priority': 'HIGH'
            })
        
        # Recommandations générales
        if not self.results['environment_check'].get('src_directory_exists'):
            recommendations.append({
                'type': 'STRUCTURE',
                'message': 'Vérifier la structure du projet',
                'priority': 'MEDIUM'
            })
        
        self.results['recommendations'] = recommendations
    
    def _save_report(self):
        """Sauvegarde le rapport"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Rapport JSON
        json_file = f'diagnostic_report_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Rapport texte
        txt_file = f'diagnostic_summary_{timestamp}.txt'
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_text_report())
        
        logger.info(f"📁 Rapports sauvegardés: {json_file}, {txt_file}")
    
    def _generate_text_report(self) -> str:
        """Génère un rapport texte lisible"""
        report = []
        report.append("CHNeoWave - Rapport de Diagnostic")
        report.append("=" * 50)
        report.append(f"Date: {self.results['timestamp']}")
        report.append(f"Statut global: {self.results['overall_status']}")
        report.append("")
        
        # Informations système
        report.append("INFORMATIONS SYSTÈME")
        report.append("-" * 20)
        for key, value in self.results['system_info'].items():
            report.append(f"{key}: {value}")
        report.append("")
        
        # Problèmes critiques
        if self.critical_issues:
            report.append("PROBLÈMES CRITIQUES")
            report.append("-" * 20)
            for issue in self.critical_issues:
                report.append(f"❌ {issue}")
            report.append("")
        
        # Avertissements
        if self.warnings:
            report.append("AVERTISSEMENTS")
            report.append("-" * 15)
            for warning in self.warnings:
                report.append(f"⚠️ {warning}")
            report.append("")
        
        # Recommandations
        if self.results['recommendations']:
            report.append("RECOMMANDATIONS")
            report.append("-" * 15)
            for rec in self.results['recommendations']:
                report.append(f"[{rec['priority']}] {rec['message']}")
            report.append("")
        
        return "\n".join(report)

def main():
    """Point d'entrée principal"""
    print("🔍 Diagnostic CHNeoWave - Démarrage...")
    
    try:
        diagnostic = CHNeoWaveDiagnostic()
        results = diagnostic.run_full_diagnostic()
        
        print(f"\n📊 Diagnostic terminé - Statut: {results['overall_status']}")
        
        if results['critical_issues']:
            print(f"\n🚨 {len(results['critical_issues'])} problème(s) critique(s) détecté(s)")
            for issue in results['critical_issues']:
                print(f"   ❌ {issue}")
        
        if results['warnings']:
            print(f"\n⚠️ {len(results['warnings'])} avertissement(s) détecté(s)")
            for warning in results['warnings']:
                print(f"   ⚠️ {warning}")
        
        print(f"\n📁 Rapports sauvegardés dans le répertoire courant")
        print("💡 Consultez les fichiers JSON et TXT pour plus de détails")
        
    except KeyboardInterrupt:
        print("\n⏹️ Diagnostic interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur fatale lors du diagnostic: {e}")
        logger.error(f"Erreur fatale: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()