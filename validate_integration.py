#!/usr/bin/env python3
# validate_integration.py - Validation finale de l'intégration CHNeoWave

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def validate_integration():
    """Validation finale de l'intégration des modules optimisés"""
    
    print("🔍 VALIDATION FINALE DE L'INTÉGRATION CHNEOWAVE")
    print("=" * 50)
    
    project_root = Path.cwd()
    validation_results = {
        "timestamp": datetime.now().isoformat(),
        "project_root": str(project_root),
        "validation_status": "UNKNOWN",
        "checks": {},
        "summary": {},
        "recommendations": []
    }
    
    # 1. Vérification des modules optimisés
    print("\n📦 Vérification des modules optimisés...")
    optimized_modules = [
        "src/hrneowave/core/optimized_fft_processor.py",
        "src/hrneowave/core/optimized_goda_analyzer.py", 
        "src/hrneowave/core/circular_buffer.py",
        "logciel hrneowave/modern_acquisition_ui.py"
    ]
    
    modules_found = 0
    for module in optimized_modules:
        module_path = project_root / module
        exists = module_path.exists()
        print(f"  {'✅' if exists else '❌'} {module}")
        if exists:
            modules_found += 1
            
    validation_results["checks"]["optimized_modules"] = {
        "found": modules_found,
        "total": len(optimized_modules),
        "status": "PASS" if modules_found >= 3 else "FAIL"
    }
    
    # 2. Vérification de l'intégration GUI
    print("\n🖥️ Vérification de l'intégration GUI...")
    acquisition_file = project_root / "logciel hrneowave" / "acquisition.py"
    
    gui_integration_score = 0
    if acquisition_file.exists():
        with open(acquisition_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier les imports optimisés
        imports_to_check = [
            "OptimizedProcessingWorker",
            "OptimizedFFTProcessor", 
            "OptimizedGodaAnalyzer"
        ]
        
        for import_name in imports_to_check:
            if import_name in content:
                print(f"  ✅ Import {import_name} trouvé")
                gui_integration_score += 1
            else:
                print(f"  ❌ Import {import_name} manquant")
                
    validation_results["checks"]["gui_integration"] = {
        "score": gui_integration_score,
        "total": 3,
        "status": "PASS" if gui_integration_score == 3 else "FAIL"
    }
    
    # 3. Vérification de l'absence de fichiers orphelins critiques
    print("\n🗑️ Vérification des fichiers orphelins...")
    orphan_files = [
        "logciel hrneowave/processing_worker.py",
        "logciel hrneowave/optimized_processing_worker.py",
        "HRNeoWave/gui/Traitementdonneé.py"
    ]
    
    orphans_found = 0
    for orphan in orphan_files:
        orphan_path = project_root / orphan
        exists = orphan_path.exists()
        if exists:
            print(f"  ⚠️ Orphelin trouvé: {orphan}")
            orphans_found += 1
        else:
            print(f"  ✅ Orphelin supprimé: {orphan}")
            
    validation_results["checks"]["orphan_cleanup"] = {
        "orphans_found": orphans_found,
        "status": "PASS" if orphans_found == 0 else "PARTIAL"
    }
    
    # 4. Vérification de la structure du projet
    print("\n📁 Vérification de la structure du projet...")
    essential_dirs = [
        "src/hrneowave/core",
        "logciel hrneowave", 
        "tests",
        "config"
    ]
    
    structure_score = 0
    for dir_path in essential_dirs:
        full_path = project_root / dir_path
        exists = full_path.exists()
        print(f"  {'✅' if exists else '❌'} {dir_path}")
        if exists:
            structure_score += 1
            
    validation_results["checks"]["project_structure"] = {
        "score": structure_score,
        "total": len(essential_dirs),
        "status": "PASS" if structure_score >= 3 else "FAIL"
    }
    
    # 5. Test de syntaxe des fichiers critiques
    print("\n🔍 Vérification de la syntaxe...")
    critical_files = [
        "logciel hrneowave/acquisition.py",
        "logciel hrneowave/modern_acquisition_ui.py"
    ]
    
    syntax_score = 0
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                import ast
                ast.parse(content)
                print(f"  ✅ Syntaxe OK: {file_path}")
                syntax_score += 1
            except SyntaxError as e:
                print(f"  ❌ Erreur syntaxe {file_path}: {e}")
            except Exception as e:
                print(f"  ⚠️ Erreur lecture {file_path}: {e}")
        else:
            print(f"  ❌ Fichier manquant: {file_path}")
            
    validation_results["checks"]["syntax_validation"] = {
        "score": syntax_score,
        "total": len(critical_files),
        "status": "PASS" if syntax_score == len(critical_files) else "FAIL"
    }
    
    # 6. Calcul du score global
    print("\n📊 RÉSULTATS DE LA VALIDATION")
    print("=" * 50)
    
    total_checks = len(validation_results["checks"])
    passed_checks = sum(1 for check in validation_results["checks"].values() 
                       if check["status"] == "PASS")
    
    validation_results["summary"] = {
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "success_rate": round((passed_checks / total_checks) * 100, 1)
    }
    
    success_rate = validation_results["summary"]["success_rate"]
    
    print(f"  📈 Modules optimisés: {modules_found}/{len(optimized_modules)}")
    print(f"  🖥️ Intégration GUI: {gui_integration_score}/3")
    print(f"  🗑️ Fichiers orphelins: {orphans_found}")
    print(f"  📁 Structure projet: {structure_score}/{len(essential_dirs)}")
    print(f"  🔍 Syntaxe: {syntax_score}/{len(critical_files)}")
    print(f"  \n🎯 Score global: {passed_checks}/{total_checks} ({success_rate}%)")
    
    # Déterminer le statut final
    if success_rate >= 80:
        validation_results["validation_status"] = "SUCCESS"
        print("\n🎉 VALIDATION RÉUSSIE !")
        print("✅ L'intégration des modules optimisés est complète et fonctionnelle.")
    elif success_rate >= 60:
        validation_results["validation_status"] = "PARTIAL"
        print("\n⚠️ VALIDATION PARTIELLE")
        print("🔧 L'intégration est fonctionnelle mais nécessite des améliorations.")
    else:
        validation_results["validation_status"] = "FAILED"
        print("\n❌ VALIDATION ÉCHOUÉE")
        print("🚨 L'intégration nécessite des corrections importantes.")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS:")
    if orphans_found > 0:
        validation_results["recommendations"].append("Supprimer les fichiers orphelins restants")
        print("  1. Supprimer les fichiers orphelins restants")
        
    if gui_integration_score < 3:
        validation_results["recommendations"].append("Compléter l'intégration GUI")
        print("  2. Compléter l'intégration GUI")
        
    if syntax_score < len(critical_files):
        validation_results["recommendations"].append("Corriger les erreurs de syntaxe")
        print("  3. Corriger les erreurs de syntaxe")
        
    if structure_score < len(essential_dirs):
        validation_results["recommendations"].append("Compléter la structure du projet")
        print("  4. Compléter la structure du projet")
        
    if not validation_results["recommendations"]:
        validation_results["recommendations"].append("Aucune action requise - intégration optimale")
        print("  ✅ Aucune action requise - intégration optimale")
    
    # Sauvegarder le rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"validation_report_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport sauvegardé: {report_file}")
    print("=" * 50)
    
    return validation_results["validation_status"] == "SUCCESS"

if __name__ == "__main__":
    try:
        success = validate_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur lors de la validation: {e}")
        sys.exit(1)