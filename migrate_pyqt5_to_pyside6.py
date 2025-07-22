#!/usr/bin/env python3
"""
Script de migration PyQt5 vers PySide6 pour CHNeoWave v1.1.0
Sprint 0 - Migration automatisée des imports

Ce script remplace tous les imports PyQt5 par leurs équivalents PySide6
en préservant la compatibilité et la fonctionnalité.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# Mapping des imports PyQt5 vers PySide6
IMPORT_MAPPING = {
    'from PyQt5.QtCore import': 'from PySide6.QtCore import',
    'from PyQt5.QtWidgets import': 'from PySide6.QtWidgets import',
    'from PyQt5.QtGui import': 'from PySide6.QtGui import',
    'from PyQt5.QtTest import': 'from PySide6.QtTest import',
    'from PyQt5.QtSvg import': 'from PySide6.QtSvg import',
    'from PyQt5 import': 'from PySide6 import',
    'import PyQt5': 'import PySide6',
    'pyqtSignal': 'Signal',
    'pyqtSlot': 'Slot',
    'qInstallMessageHandler': 'qInstallMessageHandler',  # Reste identique
}

# Fichiers à exclure de la migration
EXCLUDE_FILES = {
    'migrate_pyqt5_to_pyside6.py',
    '__pycache__',
    '.git',
    '.pytest_cache',
    'build',
    'dist',
    '*.egg-info'
}

class PyQt5ToPySide6Migrator:
    """Migrateur automatisé PyQt5 vers PySide6"""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.modified_files: List[Path] = []
        self.backup_files: List[Path] = []
        self.errors: List[Tuple[Path, str]] = []
        
    def should_exclude_file(self, file_path: Path) -> bool:
        """Vérifie si un fichier doit être exclu de la migration"""
        for exclude in EXCLUDE_FILES:
            if exclude in str(file_path):
                return True
        return False
    
    def find_python_files(self) -> List[Path]:
        """Trouve tous les fichiers Python dans le projet"""
        python_files = []
        for file_path in self.root_path.rglob('*.py'):
            if not self.should_exclude_file(file_path):
                python_files.append(file_path)
        return python_files
    
    def backup_file(self, file_path: Path) -> Path:
        """Crée une sauvegarde du fichier original"""
        backup_path = file_path.with_suffix(f'{file_path.suffix}.bak')
        backup_path.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
        self.backup_files.append(backup_path)
        return backup_path
    
    def migrate_file_content(self, content: str) -> Tuple[str, bool]:
        """Migre le contenu d'un fichier PyQt5 vers PySide6"""
        original_content = content
        modified = False
        
        # Remplacement des imports et signaux
        for old_pattern, new_pattern in IMPORT_MAPPING.items():
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                modified = True
        
        return content, modified
    
    def migrate_file(self, file_path: Path) -> bool:
        """Migre un fichier spécifique"""
        try:
            # Lecture du contenu original
            original_content = file_path.read_text(encoding='utf-8')
            
            # Vérification si le fichier contient des imports PyQt5
            if 'PyQt5' not in original_content:
                return False
            
            # Création de la sauvegarde
            self.backup_file(file_path)
            
            # Migration du contenu
            migrated_content, was_modified = self.migrate_file_content(original_content)
            
            if was_modified:
                # Écriture du contenu migré
                file_path.write_text(migrated_content, encoding='utf-8')
                self.modified_files.append(file_path)
                print(f"✅ Migré: {file_path.relative_to(self.root_path)}")
                return True
            
            return False
            
        except Exception as e:
            error_msg = f"Erreur lors de la migration: {str(e)}"
            self.errors.append((file_path, error_msg))
            print(f"❌ Erreur: {file_path.relative_to(self.root_path)} - {error_msg}")
            return False
    
    def migrate_all(self) -> Dict[str, int]:
        """Migre tous les fichiers Python du projet"""
        print("🚀 Début de la migration PyQt5 vers PySide6...")
        print(f"📁 Répertoire racine: {self.root_path}")
        
        python_files = self.find_python_files()
        print(f"📄 {len(python_files)} fichiers Python trouvés")
        
        migrated_count = 0
        for file_path in python_files:
            if self.migrate_file(file_path):
                migrated_count += 1
        
        # Rapport de migration
        stats = {
            'total_files': len(python_files),
            'migrated_files': migrated_count,
            'backup_files': len(self.backup_files),
            'errors': len(self.errors)
        }
        
        print("\n📊 RAPPORT DE MIGRATION:")
        print(f"   • Fichiers analysés: {stats['total_files']}")
        print(f"   • Fichiers migrés: {stats['migrated_files']}")
        print(f"   • Sauvegardes créées: {stats['backup_files']}")
        print(f"   • Erreurs: {stats['errors']}")
        
        if self.errors:
            print("\n❌ ERREURS DÉTECTÉES:")
            for file_path, error in self.errors:
                print(f"   • {file_path.relative_to(self.root_path)}: {error}")
        
        return stats
    
    def rollback(self) -> bool:
        """Restaure les fichiers depuis les sauvegardes"""
        print("🔄 Rollback en cours...")
        
        success_count = 0
        for backup_path in self.backup_files:
            try:
                original_path = backup_path.with_suffix('')
                original_path.write_text(backup_path.read_text(encoding='utf-8'), encoding='utf-8')
                backup_path.unlink()  # Supprime la sauvegarde
                success_count += 1
                print(f"✅ Restauré: {original_path.relative_to(self.root_path)}")
            except Exception as e:
                print(f"❌ Erreur rollback: {backup_path} - {str(e)}")
        
        print(f"📊 {success_count}/{len(self.backup_files)} fichiers restaurés")
        return success_count == len(self.backup_files)
    
    def cleanup_backups(self) -> None:
        """Supprime les fichiers de sauvegarde après migration réussie"""
        for backup_path in self.backup_files:
            try:
                backup_path.unlink()
            except Exception as e:
                print(f"⚠️ Impossible de supprimer la sauvegarde {backup_path}: {e}")

def main():
    """Point d'entrée principal"""
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        root_path = os.getcwd()
    
    migrator = PyQt5ToPySide6Migrator(root_path)
    
    try:
        stats = migrator.migrate_all()
        
        if stats['errors'] == 0 and stats['migrated_files'] > 0:
            print("\n✅ Migration terminée avec succès!")
            print("💡 Exécutez les tests pour valider la migration.")
            print("💡 Si tout fonctionne, supprimez les fichiers .bak")
            return 0
        elif stats['migrated_files'] == 0:
            print("\nℹ️ Aucun fichier à migrer trouvé.")
            return 0
        else:
            print("\n⚠️ Migration terminée avec des erreurs.")
            print("💡 Vérifiez les erreurs ci-dessus et corrigez manuellement si nécessaire.")
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 Migration interrompue par l'utilisateur.")
        print("🔄 Rollback automatique...")
        migrator.rollback()
        return 1
    except Exception as e:
        print(f"\n💥 Erreur critique: {str(e)}")
        print("🔄 Rollback automatique...")
        migrator.rollback()
        return 1

if __name__ == '__main__':
    sys.exit(main())