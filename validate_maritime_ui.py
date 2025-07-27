#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation finale pour l'interface Maritime Theme 2025
CHNeoWave - Validation complète de la reconstruction UI
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Ajouter le chemin src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

class MaritimeUIValidator:
    """
    Validateur pour l'interface Maritime Theme 2025
    """
    
    def __init__(self):
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'theme': 'Maritime PRO 2025',
            'tests': {},
            'summary': {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
        
        self.base_path = Path(__file__).parent
        self.src_path = self.base_path / "src" / "hrneowave" / "gui"
        
    def log_test(self, test_name: str, status: str, message: str, details: Any = None):
        """Enregistre un résultat de test"""
        self.validation_results['tests'][test_name] = {
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        self.validation_results['summary']['total_tests'] += 1
        if status == 'PASS':
            self.validation_results['summary']['passed'] += 1
        elif status == 'FAIL':
            self.validation_results['summary']['failed'] += 1
        elif status == 'WARN':
            self.validation_results['summary']['warnings'] += 1
    
    def validate_file_structure(self) -> bool:
        """Validation de la structure des fichiers"""
        print("🔍 Validation de la structure des fichiers...")
        
        required_files = {
            'styles/maritime_theme.qss': 'Thème maritime principal',
            'views/dashboard_view.py': 'Vue tableau de bord',
            'views/calibration_view.py': 'Vue calibration',
            'views/acquisition_view.py': 'Vue acquisition',
            'views/analysis_view.py': 'Vue analyse',
            'views/report_view.py': 'Vue rapport',
            'widgets/kpi_card.py': 'Widget carte KPI',
            'widgets/main_sidebar.py': 'Sidebar principale',
            'widgets/theme_toggle.py': 'Basculeur de thème',
            'views/__init__.py': 'Module views',
            'widgets/__init__.py': 'Module widgets'
        }
        
        all_files_exist = True
        missing_files = []
        
        for file_path, description in required_files.items():
            full_path = self.src_path / file_path
            if full_path.exists():
                self.log_test(f"file_exists_{file_path.replace('/', '_')}", 'PASS', 
                            f"{description} existe", str(full_path))
            else:
                self.log_test(f"file_exists_{file_path.replace('/', '_')}", 'FAIL', 
                            f"{description} manquant", str(full_path))
                missing_files.append(file_path)
                all_files_exist = False
        
        if missing_files:
            self.log_test('file_structure', 'FAIL', 
                        f"Fichiers manquants: {', '.join(missing_files)}")
        else:
            self.log_test('file_structure', 'PASS', 
                        "Tous les fichiers requis sont présents")
        
        return all_files_exist
    
    def validate_qss_theme(self) -> bool:
        """Validation du fichier de thème QSS"""
        print("🎨 Validation du thème maritime...")
        
        qss_path = self.src_path / "styles" / "maritime_theme.qss"
        
        if not qss_path.exists():
            self.log_test('qss_theme', 'FAIL', "Fichier maritime_theme.qss manquant")
            return False
        
        try:
            with open(qss_path, 'r', encoding='utf-8') as f:
                qss_content = f.read()
            
            # Vérifications du contenu QSS
            required_elements = {
                'palette_colors': ['#0A1929', '#055080', '#2B79B6', '#00ACC1', '#F5FBFF'],
                'golden_ratio_spacing': ['8px', '13px', '21px', '34px', '55px'],
                'typography': ['Inter', 'font-family'],
                'components': ['QMainWindow', 'QPushButton', 'QScrollBar', 'QTabWidget'],
                'animations': ['transition', 'ease-in-out'],
                'themes': ['[data-theme="light"]', '[data-theme="dark"]']
            }
            
            validation_details = {}
            all_valid = True
            
            for category, elements in required_elements.items():
                found_elements = []
                missing_elements = []
                
                for element in elements:
                    if element in qss_content:
                        found_elements.append(element)
                    else:
                        missing_elements.append(element)
                        all_valid = False
                
                validation_details[category] = {
                    'found': found_elements,
                    'missing': missing_elements
                }
            
            # Vérification de la taille du fichier
            file_size = len(qss_content)
            if file_size < 1000:
                self.log_test('qss_size', 'WARN', 
                            f"Fichier QSS petit ({file_size} caractères)")
            else:
                self.log_test('qss_size', 'PASS', 
                            f"Taille QSS appropriée ({file_size} caractères)")
            
            if all_valid:
                self.log_test('qss_theme', 'PASS', 
                            "Thème maritime valide", validation_details)
            else:
                self.log_test('qss_theme', 'WARN', 
                            "Thème maritime partiellement valide", validation_details)
            
            return True
            
        except Exception as e:
            self.log_test('qss_theme', 'FAIL', f"Erreur lecture QSS: {e}")
            return False
    
    def validate_python_imports(self) -> bool:
        """Validation des imports Python"""
        print("🐍 Validation des imports Python...")
        
        modules_to_test = {
            'views': ['DashboardView', 'CalibrationView', 'AcquisitionView', 'AnalysisView', 'ReportView'],
            'widgets': ['KPICard', 'MainSidebar', 'ThemeToggle']
        }
        
        all_imports_valid = True
        
        for module_name, classes in modules_to_test.items():
            try:
                if module_name == 'views':
                    from hrneowave.gui.views import (
                        DashboardView, CalibrationView, AcquisitionView, 
                        AnalysisView, ReportView
                    )
                    imported_classes = {
                        'DashboardView': DashboardView,
                        'CalibrationView': CalibrationView,
                        'AcquisitionView': AcquisitionView,
                        'AnalysisView': AnalysisView,
                        'ReportView': ReportView
                    }
                elif module_name == 'widgets':
                    from hrneowave.gui.widgets import KPICard, MainSidebar, ThemeToggle
                    imported_classes = {
                        'KPICard': KPICard,
                        'MainSidebar': MainSidebar,
                        'ThemeToggle': ThemeToggle
                    }
                
                for class_name in classes:
                    if class_name in imported_classes:
                        self.log_test(f"import_{module_name}_{class_name}", 'PASS', 
                                    f"Import {class_name} réussi")
                    else:
                        self.log_test(f"import_{module_name}_{class_name}", 'FAIL', 
                                    f"Import {class_name} échoué")
                        all_imports_valid = False
                        
            except ImportError as e:
                self.log_test(f"import_{module_name}", 'FAIL', 
                            f"Erreur import module {module_name}: {e}")
                all_imports_valid = False
            except Exception as e:
                self.log_test(f"import_{module_name}", 'FAIL', 
                            f"Erreur inattendue {module_name}: {e}")
                all_imports_valid = False
        
        return all_imports_valid
    
    def validate_design_guide(self) -> bool:
        """Validation du guide de design"""
        print("📖 Validation du guide de design...")
        
        guide_path = self.base_path / "docs" / "DESIGN_GUIDE_2025.md"
        
        if not guide_path.exists():
            self.log_test('design_guide', 'FAIL', "Guide de design manquant")
            return False
        
        try:
            with open(guide_path, 'r', encoding='utf-8') as f:
                guide_content = f.read()
            
            required_sections = [
                '# CHNeoWave Design Guide 2025',
                '## Palette de Couleurs Maritime PRO',
                '## Typographie Inter',
                '## Golden Ratio',
                '## Composants UI',
                '## Animations et Transitions',
                '## Accessibilité WCAG 2.1 AA'
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in guide_content:
                    missing_sections.append(section)
            
            if missing_sections:
                self.log_test('design_guide', 'WARN', 
                            f"Sections manquantes: {', '.join(missing_sections)}")
            else:
                self.log_test('design_guide', 'PASS', 
                            "Guide de design complet")
            
            return True
            
        except Exception as e:
            self.log_test('design_guide', 'FAIL', f"Erreur lecture guide: {e}")
            return False
    
    def validate_legacy_backup(self) -> bool:
        """Validation de la sauvegarde legacy"""
        print("💾 Validation de la sauvegarde legacy...")
        
        backup_path = self.src_path / "legacy_ui_backup"
        
        if not backup_path.exists():
            self.log_test('legacy_backup', 'FAIL', "Dossier de sauvegarde manquant")
            return False
        
        # Compter les fichiers sauvegardés
        backup_files = list(backup_path.rglob("*"))
        backup_count = len([f for f in backup_files if f.is_file()])
        
        if backup_count == 0:
            self.log_test('legacy_backup', 'WARN', "Aucun fichier dans la sauvegarde")
        else:
            self.log_test('legacy_backup', 'PASS', 
                        f"{backup_count} fichiers sauvegardés")
        
        return True
    
    def run_validation(self) -> Dict[str, Any]:
        """Exécute toutes les validations"""
        print("🌊 CHNeoWave - Validation Interface Maritime 2025")
        print("=" * 60)
        
        # Exécution des tests
        tests = [
            ('Structure des fichiers', self.validate_file_structure),
            ('Thème QSS maritime', self.validate_qss_theme),
            ('Imports Python', self.validate_python_imports),
            ('Guide de design', self.validate_design_guide),
            ('Sauvegarde legacy', self.validate_legacy_backup)
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.log_test(f"error_{test_name.lower().replace(' ', '_')}", 'FAIL', 
                            f"Erreur lors du test '{test_name}': {e}")
        
        # Génération du rapport
        self.generate_report()
        
        return self.validation_results
    
    def generate_report(self):
        """Génère le rapport de validation"""
        print("\n📋 Génération du rapport de validation...")
        
        # Sauvegarde JSON
        report_path = self.base_path / "validation_maritime_ui_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        
        # Affichage du résumé
        summary = self.validation_results['summary']
        print(f"\n✅ Tests réussis: {summary['passed']}")
        print(f"⚠️  Avertissements: {summary['warnings']}")
        print(f"❌ Tests échoués: {summary['failed']}")
        print(f"📊 Total: {summary['total_tests']}")
        
        # Calcul du score
        if summary['total_tests'] > 0:
            score = (summary['passed'] / summary['total_tests']) * 100
            print(f"🎯 Score de validation: {score:.1f}%")
            
            if score >= 90:
                print("🏆 Interface Maritime 2025 - EXCELLENTE qualité!")
            elif score >= 75:
                print("✅ Interface Maritime 2025 - BONNE qualité")
            elif score >= 50:
                print("⚠️ Interface Maritime 2025 - Qualité ACCEPTABLE")
            else:
                print("❌ Interface Maritime 2025 - Qualité INSUFFISANTE")
        
        print(f"\n📄 Rapport détaillé sauvegardé: {report_path}")

def main():
    """Fonction principale"""
    validator = MaritimeUIValidator()
    results = validator.run_validation()
    
    # Code de sortie basé sur les résultats
    if results['summary']['failed'] > 0:
        sys.exit(1)
    elif results['summary']['warnings'] > 0:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()