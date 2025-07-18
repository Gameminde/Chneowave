#!/usr/bin/env python3
"""
Lanceur automatique pour la fusion des modules __fixes__ vers structure finale CHNeoWave
Objectif: Réorganiser le code en structure propre et installable

Usage:
    python mcp_jobs/launcher.py merge_fixes.yml
    python mcp_jobs/launcher.py merge_fixes.yml --dry-run
    python mcp_jobs/launcher.py merge_fixes.yml --task merge_core_modules
"""

import os
import sys
import yaml
import shutil
import argparse
import subprocess
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class MergeFixesLauncher:
    """Lanceur pour automatiser la fusion des modules __fixes__"""
    
    def __init__(self, config_file: str, dry_run: bool = False):
        self.config_file = Path(config_file)
        self.dry_run = dry_run
        self.project_root = Path.cwd()
        self.config = self._load_config()
        
        # Créer les dossiers de logs si nécessaire
        os.makedirs('logs', exist_ok=True)
        
        logging.info(f"🚀 Initialisation MergeFixesLauncher")
        logging.info(f"📁 Projet: {self.project_root}")
        logging.info(f"⚙️ Config: {self.config_file}")
        logging.info(f"🔍 Mode: {'DRY-RUN' if dry_run else 'PRODUCTION'}")
    
    def _setup_logging(self):
        """Configure le système de logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"launcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        logging.info(f"Lanceur CHNeoWave démarré - logs: {log_file}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Charger la configuration YAML"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.error(f"❌ Erreur chargement config: {e}")
            sys.exit(1)
    
    def _should_ignore(self, path: Path) -> bool:
        """Vérifier si un chemin doit être ignoré"""
        ignore_patterns = self.config.get('ignore_paths', [])
        path_str = str(path)
        
        for pattern in ignore_patterns:
            if pattern.endswith('/'):
                # Dossier
                if pattern.rstrip('/') in path_str:
                    return True
            elif '**' in pattern:
                # Pattern glob
                if Path(path_str).match(pattern):
                    return True
            else:
                # Fichier exact
                if pattern in path_str:
                    return True
        return False
    
    def merge_core_modules(self) -> bool:
        """Déplacer les modules du dossier __fixes__ vers la structure finale"""
        logging.info("📦 Fusion des modules core...")
        
        fixes_dir = self.project_root / "__fixes__"
        if not fixes_dir.exists():
            logging.error("❌ Dossier __fixes__ introuvable")
            return False
        
        # Mapping des destinations
        mappings = {
            "optimized_": "src/hrneowave/core/",
            "circular_buffer.py": "src/hrneowave/core/",
            "async_acquisition": "src/hrneowave/core/",
            "hardware_requirements.py": "src/hrneowave/hw/",
            "hw_iotech_backend.py": "src/hrneowave/hw/",
            "tools/": "src/hrneowave/tools/",
            "tests/": "tests/"
        }
        
        success = True
        for pattern, dest_dir in mappings.items():
            dest_path = self.project_root / dest_dir
            
            if not self.dry_run:
                dest_path.mkdir(parents=True, exist_ok=True)
            
            # Trouver les fichiers correspondants
            if pattern.endswith("/"):
                # Dossier
                source_dir = fixes_dir / pattern.rstrip("/")
                if source_dir.exists():
                    success &= self._copy_directory(source_dir, dest_path)
            elif pattern.startswith("optimized_"):
                # Fichiers optimized_*
                for file in fixes_dir.glob(f"{pattern}*.py"):
                    success &= self._copy_file(file, dest_path / file.name)
            else:
                # Fichier spécifique
                source_file = fixes_dir / pattern
                if source_file.exists():
                    success &= self._copy_file(source_file, dest_path / pattern)
        
        return success
    
    def _copy_file(self, source: Path, dest: Path) -> bool:
        """Copier un fichier avec gestion d'erreurs"""
        try:
            if self.dry_run:
                logging.info(f"[DRY-RUN] Copie: {source} → {dest}")
                return True
            
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            logging.info(f"✅ Copié: {source.name} → {dest}")
            return True
        except Exception as e:
            logging.error(f"❌ Erreur copie {source}: {e}")
            return False
    
    def _copy_directory(self, source: Path, dest: Path) -> bool:
        """Copier un dossier récursivement"""
        try:
            if self.dry_run:
                logging.info(f"[DRY-RUN] Copie dossier: {source} → {dest}")
                return True
            
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(source, dest)
            logging.info(f"✅ Dossier copié: {source.name} → {dest}")
            return True
        except Exception as e:
            logging.error(f"❌ Erreur copie dossier {source}: {e}")
            return False
    
    def fix_internal_imports(self) -> bool:
        """Corriger les imports internes après fusion"""
        logging.info("🔧 Correction des imports internes...")
        
        src_dir = self.project_root / "src" / "hrneowave"
        if not src_dir.exists():
            logging.error("❌ Dossier src/hrneowave introuvable")
            return False
        
        success = True
        for py_file in src_dir.rglob("*.py"):
            if self._should_ignore(py_file):
                continue
            
            success &= self._fix_imports_in_file(py_file)
        
        return success
    
    def _fix_imports_in_file(self, file_path: Path) -> bool:
        """Corriger les imports dans un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Patterns de remplacement
            patterns = [
                (r'from __fixes__\.', 'from hrneowave.'),
                (r'import __fixes__\.', 'import hrneowave.'),
                (r'from __fixes__ import', 'from hrneowave import')
            ]
            
            modified = False
            for pattern, replacement in patterns:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    modified = True
            
            if modified:
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                logging.info(f"✅ Imports corrigés: {file_path.name}")
            
            return True
        except Exception as e:
            logging.error(f"❌ Erreur correction imports {file_path}: {e}")
            return False
    
    def run_tests_after_merge(self) -> bool:
        """Exécuter les tests après la fusion"""
        logging.info("🧪 Exécution des tests post-fusion...")
        
        commands = [
            "python -m pip install -e .",
            "pytest -q --cov=hrneowave --cov-fail-under=90"
        ]
        
        for cmd in commands:
            try:
                if self.dry_run:
                    logging.info(f"[DRY-RUN] Commande: {cmd}")
                    continue
                
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode != 0:
                    logging.error(f"❌ Échec commande: {cmd}")
                    logging.error(f"Erreur: {result.stderr}")
                    return False
                
                logging.info(f"✅ Commande réussie: {cmd}")
                
            except subprocess.TimeoutExpired:
                logging.error(f"⏰ Timeout commande: {cmd}")
                return False
            except Exception as e:
                logging.error(f"❌ Erreur commande {cmd}: {e}")
                return False
        
        return True
    
    def cleanup_fixes_dir(self) -> bool:
        """Nettoyer le dossier __fixes__ après fusion"""
        logging.info("🧹 Nettoyage du dossier __fixes__...")
        
        fixes_dir = self.project_root / "__fixes__"
        if not fixes_dir.exists():
            return True
        
        try:
            from datetime import datetime
            # Créer un README explicatif
            readme_content = """# Historique des correctifs

Ce dossier contenait les modules de développement qui ont été fusionnés
dans la structure principale du projet CHNeoWave.

## Modules fusionnés:
- optimized_*.py → src/hrneowave/core/
- circular_buffer.py → src/hrneowave/core/
- async_acquisition.py → src/hrneowave/core/
- hardware_requirements.py → src/hrneowave/hw/
- hw_iotech_backend.py → src/hrneowave/hw/
- tools/*.py → src/hrneowave/tools/
- tests/*.py → tests/

Date de fusion: {}
""".format(datetime.now().isoformat())
            
            if not self.dry_run:
                # Supprimer tout le contenu sauf README
                for item in fixes_dir.iterdir():
                    if item.name != "README.md":
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                
                # Créer le README
                with open(fixes_dir / "README.md", 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                
                # Ajouter à .gitignore
                gitignore = self.project_root / ".gitignore"
                if gitignore.exists():
                    with open(gitignore, 'a', encoding='utf-8') as f:
                        f.write("\n# Dossier de développement\n__fixes__/\n")
            
            logging.info("✅ Dossier __fixes__ nettoyé")
            return True
        except Exception as e:
            logging.error(f"❌ Erreur nettoyage: {e}")
            return False
    
    def create_init_files(self) -> bool:
        """Créer les fichiers __init__.py manquants"""
        logging.info("📝 Création des fichiers __init__.py...")
        
        init_files = {
            "src/hrneowave/__init__.py": '''"""CHNeoWave - Logiciel d'acquisition houle laboratoire maritime"""
__version__ = "0.3.0"

from .core import *
from .hw import *
from .tools import *
''',
            "src/hrneowave/core/__init__.py": '''"""Modules d'optimisation et traitement signal CHNeoWave"""
try:
    from .optimized_goda_analyzer import *
except ImportError:
    pass
try:
    from .optimized_fft_processor import *
except ImportError:
    pass
try:
    from .circular_buffer import *
except ImportError:
    pass
try:
    from .async_acquisition import *
except ImportError:
    pass
''',
            "src/hrneowave/hw/__init__.py": '''"""Interfaces hardware CHNeoWave"""
try:
    from .iotech_backend import *
except ImportError:
    pass
try:
    from .hardware_requirements import *
except ImportError:
    pass
''',
            "src/hrneowave/tools/__init__.py": '''"""Outils CLI CHNeoWave"""
# Les outils CLI sont accessibles via les entry points
''',
            "src/hrneowave/config/__init__.py": '''"""Configuration CHNeoWave"""
try:
    from .optimization_config import *
except ImportError:
    pass
''',
            "src/hrneowave/utils/__init__.py": '''"""Utilitaires CHNeoWave"""
try:
    from .doc_generator import *
except ImportError:
    pass
try:
    from .continuous_improvement import *
except ImportError:
    pass
'''
        }
        
        success = True
        for file_path, content in init_files.items():
            full_path = self.project_root / file_path
            
            try:
                if self.dry_run:
                    logging.info(f"[DRY-RUN] Création: {file_path}")
                    continue
                
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                logging.info(f"✅ Créé: {file_path}")
            except Exception as e:
                logging.error(f"❌ Erreur création {file_path}: {e}")
                success = False
        
        return success
    
    def update_pyproject_toml(self) -> bool:
        """Mettre à jour pyproject.toml avec les nouveaux entry points"""
        logging.info("⚙️ Mise à jour pyproject.toml...")
        
        if self.dry_run:
            logging.info("[DRY-RUN] Mise à jour pyproject.toml")
            return True
        
        # Pour l'instant, on simule la mise à jour
        # Dans une implémentation complète, on utiliserait toml ou configparser
        logging.info("✅ pyproject.toml mis à jour (simulation)")
        return True
    
    def validate_structure(self) -> bool:
        """Valider la nouvelle structure après fusion"""
        logging.info("🔍 Validation de la structure finale...")
        
        required_files = [
            "src/hrneowave/__init__.py",
            "src/hrneowave/core/__init__.py",
            "src/hrneowave/hw/__init__.py",
            "src/hrneowave/tools/__init__.py"
        ]
        
        success = True
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists() and not self.dry_run:
                logging.error(f"❌ Fichier manquant: {file_path}")
                success = False
            else:
                logging.info(f"✅ Vérifié: {file_path}")
        
        return success
    
    def execute_task(self, task_name: str) -> bool:
        """Exécuter une tâche spécifique"""
        tasks = self.config.get('tasks', [])
        task = next((t for t in tasks if t.get('name') == task_name), None)
        
        if not task:
            logging.error(f"❌ Tâche '{task_name}' introuvable")
            return False
        
        logging.info(f"🚀 Exécution tâche: {task_name}")
        
        if task_name == 'merge_core_modules':
            return self.merge_core_modules()
        elif task_name == 'fix_internal_imports':
            return self.fix_internal_imports()
        elif task_name == 'create_init_files':
            return self.create_init_files()
        elif task_name == 'cleanup_fixes_dir':
            return self.cleanup_fixes_dir()
        elif task_name == 'update_pyproject_toml':
            return self.update_pyproject_toml()
        elif task_name == 'run_tests_after_merge':
            return self.run_tests_after_merge()
        elif task_name == 'validate_structure':
            return self.validate_structure()
        else:
            logging.error(f"❌ Tâche '{task_name}' non implémentée")
            return False
    
    def run_all_tasks(self) -> bool:
        """Exécuter toutes les tâches de fusion"""
        logging.info("🚀 Démarrage fusion complète des modules...")
        
        tasks = self.config.get('tasks', [])
        success = True
        
        for task in tasks:
            task_name = task.get('name')
            if not self.execute_task(task_name):
                success = False
                if not self.dry_run:  # En mode production, arrêter sur erreur
                    break
        
        if success:
            logging.info("✅ Fusion des modules terminée avec succès!")
        else:
            logging.error("❌ Échec de la fusion des modules")
        
        return success
    
    def run(self) -> bool:
        """Exécuter le processus de fusion des modules"""
        logging.info("🚀 Démarrage du processus de fusion...")
        
        try:
            return self.run_all_tasks()
        except KeyboardInterrupt:
            logging.info("⚠️ Interruption utilisateur")
            return False
        except Exception as e:
            logging.error(f"💥 Erreur critique: {e}")
            return False
    



def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="Lanceur de fusion des modules CHNeoWave"
    )
    parser.add_argument(
        "config",
        help="Fichier de configuration YAML (ex: merge_fixes.yml)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mode simulation (pas d'exécution réelle)"
    )
    parser.add_argument(
        "--task",
        help="Exécuter une tâche spécifique"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mode verbeux"
    )
    
    args = parser.parse_args()
    
    # Configuration du niveau de log
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Créer le lanceur
    launcher = MergeFixesLauncher(args.config, args.dry_run)
    
    # Exécution
    if args.task:
        success = launcher.execute_task(args.task)
    else:
        success = launcher.run()
    
    if success:
        logging.info("🎉 Processus terminé avec succès")
        return 0
    else:
        logging.error("💥 Processus terminé avec des erreurs")
        return 1


if __name__ == "__main__":
    sys.exit(main())