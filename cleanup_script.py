#!/usr/bin/env python3
"""
Script de nettoyage CHNeoWave - Version simplifiée
Supprime les fichiers et dossiers non utilisés identifiés manuellement
"""

import os
import shutil
from pathlib import Path

def cleanup_chneowave_project():
    """Nettoie le projet CHNeoWave en supprimant les fichiers non utilisés"""
    project_root = Path.cwd()
    print(f"🌊 Nettoyage du projet CHNeoWave dans: {project_root}")
    print("=" * 60)
    
    # Fichiers à supprimer (doublons et fichiers non utilisés)
    files_to_delete = [
        # Doublons dans HRNeoWave/gui (versions obsolètes)
        "HRNeoWave/gui/theme.py",
        "HRNeoWave/gui/welcome.py", 
        "HRNeoWave/gui/calibration.py",
        "HRNeoWave/gui/acquisition.py",
        "HRNeoWave/gui/Traitementdonneé.py",
        "HRNeoWave/gui/main.py",  # Version obsolète
        
        # Doublons à la racine
        "hardware_adapter.py",  # Doublon de logiciel hrneowave/hardware_adapter.py
        "test_acquisition.py",  # Doublon de logiciel hrneowave/test_acquisition.py
        "acquisition.py",       # Doublon de logiciel hrneowave/acquisition.py
        
        # Archive des fixes
        "__fixes__.zip",
        
        # Fichiers HTML temporaires
        "logiciel hrneowave/documentation.html",
        "logiciel hrneowave/guide_utilisateur.html",
        "logiciel hrneowave/rapport_technique.html"
    ]
    
    # Dossiers à supprimer (modules non utilisés)
    dirs_to_delete = [
        "HRNeoWave/advanced_visualization",
        "HRNeoWave/advanced_wave_analysis", 
        "HRNeoWave/hardware_improvements",
        "HRNeoWave/numerical_model_interface",
        "HRNeoWave/probe_positioning",
        "HRNeoWave/reflection_analysis",
        "HRNeoWave/uncertainty_analysis",
        "HRNeoWave/wave_generation",
        "HRNeoWave/gui/gamemind",  # Dossier vide
        "HRNeoWave/gui"  # Après suppression des fichiers, le dossier sera vide
    ]
    
    deleted_files = []
    deleted_dirs = []
    errors = []
    
    # Supprimer les fichiers
    print("\n🗑️ Suppression des fichiers dupliqués et non utilisés...")
    for file_path in files_to_delete:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                full_path.unlink()
                deleted_files.append(file_path)
                print(f"  ✅ Supprimé: {file_path}")
            except Exception as e:
                errors.append(f"Erreur suppression {file_path}: {e}")
                print(f"  ❌ Erreur: {file_path} - {e}")
        else:
            print(f"  ⚠️ Fichier non trouvé: {file_path}")
    
    # Supprimer les dossiers
    print("\n📁 Suppression des dossiers non utilisés...")
    for dir_path in dirs_to_delete:
        full_path = project_root / dir_path
        if full_path.exists() and full_path.is_dir():
            try:
                # Vérifier si le dossier est vide ou ne contient que des __init__.py
                contents = list(full_path.rglob('*'))
                if not contents or all(f.name == '__init__.py' for f in contents if f.is_file()):
                    shutil.rmtree(full_path)
                    deleted_dirs.append(dir_path)
                    print(f"  ✅ Supprimé: {dir_path}")
                else:
                    print(f"  ⚠️ Dossier non vide ignoré: {dir_path}")
            except Exception as e:
                errors.append(f"Erreur suppression dossier {dir_path}: {e}")
                print(f"  ❌ Erreur: {dir_path} - {e}")
        else:
            print(f"  ⚠️ Dossier non trouvé: {dir_path}")
    
    # Nettoyer les dossiers __pycache__
    print("\n🧹 Nettoyage des caches Python...")
    pycache_dirs = list(project_root.rglob('__pycache__'))
    for cache_dir in pycache_dirs:
        try:
            shutil.rmtree(cache_dir)
            deleted_dirs.append(str(cache_dir.relative_to(project_root)))
            print(f"  ✅ Cache supprimé: {cache_dir.relative_to(project_root)}")
        except Exception as e:
            errors.append(f"Erreur suppression cache {cache_dir}: {e}")
            print(f"  ❌ Erreur cache: {cache_dir.relative_to(project_root)} - {e}")
    
    # Résumé
    print("\n" + "=" * 60)
    print("✨ NETTOYAGE TERMINÉ!")
    print(f"📊 Fichiers supprimés: {len(deleted_files)}")
    print(f"📊 Dossiers supprimés: {len(deleted_dirs)}")
    if errors:
        print(f"⚠️ Erreurs rencontrées: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    
    # Fichiers et dossiers conservés (essentiels)
    print("\n📋 STRUCTURE FINALE CONSERVÉE:")
    essential_structure = [
        "📁 logiciel hrneowave/",
        "  📄 main.py (point d'entrée principal)",
        "  📄 acquisition.py (interface d'acquisition)", 
        "  📄 calibration.py (module de calibration)",
        "  📄 theme.py (gestion des thèmes)",
        "  📄 welcome.py (écran d'accueil)",
        "  📄 Traitementdonneé.py (traitement des données)",
        "  📄 hardware_adapter.py (interface matérielle)",
        "  📄 hardware_interface.py (interface matérielle avancée)",
        "  📄 test_acquisition.py (tests d'acquisition)",
        "  📄 generate_test_signal.py (génération de signaux test)",
        "  📄 patch_nidaq.py (patch pour NI-DAQ)",
        "  📄 test_hardware.py (tests matériels)",
        "📁 __fixes__/ (scripts d'amélioration)",
        "📁 mcp_jobs/ (configurations MCP)",
        "📁 venv/ (environnement virtuel)",
        "📄 pyproject.toml (configuration du projet)",
        "📄 requirements.txt (dépendances)",
        "📄 AUDIT_CHNEOWAVE_2025.md (documentation)"
    ]
    
    for item in essential_structure:
        print(f"  {item}")
    
    print("\n💡 Le projet est maintenant nettoyé et optimisé pour les laboratoires maritimes!")
    print("🌊 CHNeoWave est prêt pour l'acquisition de données de houle en modèle réduit.")
    
    return {
        'deleted_files': deleted_files,
        'deleted_dirs': deleted_dirs,
        'errors': errors
    }

if __name__ == "__main__":
    cleanup_chneowave_project()