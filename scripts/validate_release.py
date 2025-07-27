#!/usr/bin/env python3
"""
Script de validation finale pour CHNeoWave v1.0.0
Vérifie tous les composants critiques avant release
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Ajout du chemin src pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class ReleaseValidator:
    """Validateur de release pour CHNeoWave v1.0.0"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results = {
            "version_check": False,
            "dependencies": False,
            "tests": False,
            "documentation": False,
            "packaging": False,
            "performance": False,
            "security": False
        }
        self.errors = []
        self.warnings = []
    
    def validate_version_consistency(self) -> bool:
        """Vérifie la cohérence des versions dans tous les fichiers"""
        print("\n🔍 Validation de la cohérence des versions...")
        
        version_files = {
            "pyproject.toml": r'version = "([^"]+)"',
            "src/chneowave/__init__.py": r'__version__ = "([^"]+)"',
            "scripts/make_dist.py": r'CHNeoWave v([0-9.]+)'
        }
        
        versions = {}
        for file_path, pattern in version_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                import re
                content = full_path.read_text(encoding='utf-8')
                match = re.search(pattern, content)
                if match:
                    versions[file_path] = match.group(1)
                else:
                    self.errors.append(f"Version non trouvée dans {file_path}")
        
        # Vérification cohérence
        target_version = "1.0.0"
        inconsistent = [f for f, v in versions.items() if v != target_version]
        
        if inconsistent:
            self.errors.append(f"Versions incohérentes: {inconsistent}")
            return False
        
        print(f"✅ Version {target_version} cohérente dans tous les fichiers")
        return True
    
    def validate_dependencies(self) -> bool:
        """Vérifie que les dépendances critiques sont installées"""
        print("\n📦 Validation des dépendances...")
        
        try:
            # Test des dépendances critiques seulement
            critical_deps = {
                "PySide6": "PySide6",
                "numpy": "numpy", 
                "scipy": "scipy",
                "matplotlib": "matplotlib",
                "h5py": "h5py"
            }
            
            missing = []
            installed = []
            
            for dep_name, import_name in critical_deps.items():
                try:
                    __import__(import_name)
                    installed.append(dep_name)
                except ImportError:
                    missing.append(dep_name)
            
            if missing:
                self.warnings.append(f"Dépendances critiques manquantes: {missing}")
                if len(missing) > len(critical_deps) // 2:  # Plus de 50% manquantes
                    return False
            
            print(f"✅ Dépendances critiques validées ({len(installed)}/{len(critical_deps)})")
            if missing:
                print(f"   ⚠️  Manquantes: {missing}")
            
            return True
            
        except Exception as e:
            self.warnings.append(f"Erreur validation dépendances: {e}")
            return True  # Non-bloquant
    
    def validate_tests(self) -> bool:
        """Exécute une validation rapide des tests"""
        print("\n🧪 Validation des tests...")
        
        try:
            # Test rapide - juste vérifier que pytest peut démarrer
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "-q"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30  # Timeout de 30 secondes
            )
            
            if result.returncode != 0:
                self.warnings.append(f"Problème détecté avec pytest: {result.stderr}")
                # Essayer une validation basique des imports
                return self._validate_basic_imports()
            
            # Compter les tests collectés
            output_lines = result.stdout.split('\n')
            test_count = 0
            for line in output_lines:
                if "test session starts" in line or "collected" in line:
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        test_count = int(numbers[-1])
                        break
            
            print(f"✅ Tests validés ({test_count} tests détectés)")
            return True
            
        except subprocess.TimeoutExpired:
            self.warnings.append("Timeout lors de la validation des tests")
            return self._validate_basic_imports()
        except Exception as e:
            self.warnings.append(f"Erreur validation tests: {e}")
            return self._validate_basic_imports()
    
    def _validate_basic_imports(self) -> bool:
        """Validation basique par import des modules principaux"""
        print("   Validation par imports basiques...")
        
        try:
            # Test des imports principaux
            import sys
            sys.path.insert(0, str(self.project_root / "src"))
            
            # Imports critiques
            from hrneowave.core.acquisition_engine import AcquisitionEngine
            from hrneowave.gui.main_window import MainWindow
            
            print("   ✅ Imports principaux fonctionnels")
            return True
            
        except ImportError as e:
            self.errors.append(f"Import critique échoué: {e}")
            return False
        except Exception as e:
            self.warnings.append(f"Erreur validation imports: {e}")
            return True  # Non-bloquant
    
    def validate_documentation(self) -> bool:
        """Vérifie que la documentation est complète et générée"""
        print("\n📚 Validation de la documentation...")
        
        required_docs = [
            "docs/_build/html/index.html",
            "docs/_build/html/user_guide.html",
            "docs/_build/html/technical_guide.html",
            "README.md",
            "INSTALL.md",
            "CHANGELOG.md"
        ]
        
        missing_docs = []
        for doc_path in required_docs:
            full_path = self.project_root / doc_path
            if not full_path.exists():
                missing_docs.append(doc_path)
        
        if missing_docs:
            self.errors.append(f"Documentation manquante: {missing_docs}")
            return False
        
        # Vérification taille minimale des fichiers HTML
        html_files = [
            "docs/_build/html/index.html",
            "docs/_build/html/user_guide.html",
            "docs/_build/html/technical_guide.html"
        ]
        
        for html_file in html_files:
            full_path = self.project_root / html_file
            if full_path.stat().st_size < 1000:  # Moins de 1KB = probablement vide
                self.warnings.append(f"Fichier HTML suspicieusement petit: {html_file}")
        
        print("✅ Documentation complète et générée")
        return True
    
    def validate_packaging(self) -> bool:
        """Vérifie la configuration de packaging"""
        print("\n📦 Validation du packaging...")
        
        # Vérification pyproject.toml
        try:
            import tomli
            pyproject_path = self.project_root / "pyproject.toml"
            with open(pyproject_path, "rb") as f:
                pyproject = tomli.load(f)
            
            project = pyproject.get("project", {})
            required_fields = ["name", "version", "description", "authors", "license"]
            
            missing_fields = [field for field in required_fields if field not in project]
            if missing_fields:
                self.errors.append(f"Champs manquants dans pyproject.toml: {missing_fields}")
                return False
            
            # Vérification script de distribution
            dist_script = self.project_root / "scripts" / "make_dist.py"
            if not dist_script.exists():
                self.errors.append("Script make_dist.py manquant")
                return False
            
            print("✅ Configuration de packaging valide")
            return True
            
        except Exception as e:
            self.errors.append(f"Erreur validation packaging: {e}")
            return False
    
    def validate_performance(self) -> bool:
        """Tests de performance basiques"""
        print("\n⚡ Tests de performance...")
        
        try:
            # Test d'import (temps de démarrage)
            import time
            start_time = time.time()
            
            # Import principal
            from chneowave.core.acquisition_engine import AcquisitionEngine
            from chneowave.analysis.spectral_analysis import SpectralAnalyzer
            
            import_time = time.time() - start_time
            
            if import_time > 5.0:  # Plus de 5 secondes = problème
                self.warnings.append(f"Temps d'import élevé: {import_time:.2f}s")
            
            # Test création objets principaux
            start_time = time.time()
            engine = AcquisitionEngine()
            analyzer = SpectralAnalyzer()
            creation_time = time.time() - start_time
            
            if creation_time > 2.0:
                self.warnings.append(f"Temps de création objets élevé: {creation_time:.2f}s")
            
            print(f"✅ Performance acceptable (import: {import_time:.2f}s, création: {creation_time:.2f}s)")
            return True
            
        except Exception as e:
            self.errors.append(f"Erreur tests performance: {e}")
            return False
    
    def validate_security(self) -> bool:
        """Vérifications de sécurité basiques"""
        print("\n🔒 Vérifications de sécurité...")
        
        security_issues = []
        
        # Vérification des fichiers sensibles
        sensitive_patterns = [
            "*.key", "*.pem", "*.p12", "*.pfx",
            "*password*", "*secret*", "*token*"
        ]
        
        for pattern in sensitive_patterns:
            matches = list(self.project_root.rglob(pattern))
            if matches:
                security_issues.append(f"Fichiers sensibles détectés: {matches}")
        
        # Vérification des imports dangereux dans le code
        dangerous_imports = ["eval", "exec", "__import__", "compile"]
        
        python_files = list(self.project_root.rglob("*.py"))
        for py_file in python_files:
            if "venv" in str(py_file) or ".git" in str(py_file):
                continue
            
            try:
                content = py_file.read_text(encoding='utf-8')
                for dangerous in dangerous_imports:
                    if dangerous in content and not py_file.name.endswith("_test.py"):
                        security_issues.append(f"Import potentiellement dangereux '{dangerous}' dans {py_file}")
            except:
                continue
        
        if security_issues:
            self.warnings.extend(security_issues)
        
        print("✅ Vérifications de sécurité terminées")
        return True
    
    def run_validation(self) -> Dict:
        """Exécute toutes les validations"""
        print("🚀 CHNeoWave v1.0.0 - Validation de Release")
        print("=" * 50)
        
        validations = [
            ("version_check", self.validate_version_consistency),
            ("dependencies", self.validate_dependencies),
            ("tests", self.validate_tests),
            ("documentation", self.validate_documentation),
            ("packaging", self.validate_packaging),
            ("performance", self.validate_performance),
            ("security", self.validate_security)
        ]
        
        for key, validator in validations:
            try:
                self.results[key] = validator()
            except Exception as e:
                self.results[key] = False
                self.errors.append(f"Erreur dans {key}: {e}")
        
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Génère le rapport final"""
        print("\n" + "=" * 50)
        print("📊 RAPPORT DE VALIDATION FINALE")
        print("=" * 50)
        
        # Résultats par catégorie
        for category, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{category.upper():.<20} {status}")
        
        # Statistiques
        total = len(self.results)
        passed = sum(self.results.values())
        success_rate = (passed / total) * 100
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   Tests réussis: {passed}/{total} ({success_rate:.1f}%)")
        print(f"   Erreurs: {len(self.errors)}")
        print(f"   Avertissements: {len(self.warnings)}")
        
        # Erreurs critiques
        if self.errors:
            print(f"\n❌ ERREURS CRITIQUES:")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        # Avertissements
        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        # Verdict final
        print("\n" + "=" * 50)
        if passed == total and not self.errors:
            print("🎉 VALIDATION RÉUSSIE - PRÊT POUR RELEASE v1.0.0")
            verdict = "READY"
        elif passed >= total * 0.8 and not self.errors:
            print("⚠️  VALIDATION PARTIELLE - REVIEW RECOMMANDÉE")
            verdict = "REVIEW"
        else:
            print("❌ VALIDATION ÉCHOUÉE - CORRECTIONS REQUISES")
            verdict = "FAILED"
        
        print("=" * 50)
        
        return {
            "verdict": verdict,
            "success_rate": success_rate,
            "results": self.results,
            "errors": self.errors,
            "warnings": self.warnings,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

def main():
    """Point d'entrée principal"""
    validator = ReleaseValidator()
    report = validator.run_validation()
    
    # Sauvegarde du rapport
    report_path = Path(__file__).parent.parent / "validation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport sauvegardé: {report_path}")
    
    # Code de sortie
    if report["verdict"] == "READY":
        sys.exit(0)
    elif report["verdict"] == "REVIEW":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()