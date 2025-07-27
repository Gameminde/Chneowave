#!/usr/bin/env python3
"""
Script de correction de la migration PyQt5 vers PySide6
Corrige les erreurs de migration et assure la compatibilité
"""

import os
import re
from pathlib import Path

def fix_migration_errors():
    """Corrige les erreurs de migration détectées"""
    root_path = Path(os.getcwd())
    
    # Corrections spécifiques
    corrections = {
        'from PyQt6.QtCore import': 'from PySide6.QtCore import',
        'from PyQt6.QtWidgets import': 'from PySide6.QtWidgets import', 
        'from PyQt6.QtGui import': 'from PySide6.QtGui import',
        'from PyQt6.QtTest import': 'from PySide6.QtTest import',
        'from PyQt6 import': 'from PySide6 import',
        'import PyQt6': 'import PySide6',
        'pyqtSignal': 'Signal',
        'pyqtSlot': 'Slot'
    }
    
    # Fichiers à corriger spécifiquement
    files_to_fix = [
        'src/hrneowave/gui/theme/material_theme.py',
        'venv/Lib/site-packages/pytestqt/qt_compat.py'
    ]
    
    fixed_count = 0
    
    for file_rel_path in files_to_fix:
        file_path = root_path / file_rel_path
        if not file_path.exists():
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Application des corrections
            for old, new in corrections.items():
                content = content.replace(old, new)
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                print(f"✅ Corrigé: {file_rel_path}")
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ Erreur sur {file_rel_path}: {e}")
    
    # Correction globale pour tous les fichiers Python du projet
    for py_file in root_path.rglob('*.py'):
        if 'venv' in str(py_file) or '.git' in str(py_file):
            continue
            
        try:
            content = py_file.read_text(encoding='utf-8')
            original_content = content
            
            # Corrections spécifiques PyQt6 -> PySide6
            if 'PyQt6' in content:
                for old, new in corrections.items():
                    content = content.replace(old, new)
                
                if content != original_content:
                    py_file.write_text(content, encoding='utf-8')
                    print(f"✅ Corrigé PyQt6->PySide6: {py_file.relative_to(root_path)}")
                    fixed_count += 1
                    
        except Exception as e:
            print(f"❌ Erreur sur {py_file}: {e}")
    
    print(f"\n📊 {fixed_count} fichiers corrigés")
    return fixed_count

if __name__ == '__main__':
    print("🔧 Correction des erreurs de migration...")
    fix_migration_errors()
    print("✅ Correction terminée")