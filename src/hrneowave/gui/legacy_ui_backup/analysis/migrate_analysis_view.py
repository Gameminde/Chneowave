#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migration pour analysis_view.py
Facilite la transition vers l'architecture modulaire
"""

import os
import shutil
import logging
from datetime import datetime
from pathlib import Path


class AnalysisViewMigrator:
    """
    Gestionnaire de migration pour analysis_view.py
    """
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.views_dir = self.project_root / "src" / "hrneowave" / "gui" / "views"
        self.analysis_dir = self.views_dir / "analysis"
        self.backup_dir = self.views_dir / "backup" / f"analysis_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.logger = logging.getLogger(__name__)
        
        # Fichiers concernés par la migration
        self.files_to_backup = [
            "analysis_view.py",
            "analysis_view_v2.py"  # Si elle existe déjà
        ]
    
    def create_backup(self):
        """
        Création d'une sauvegarde de l'ancienne version
        """
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            for filename in self.files_to_backup:
                source_file = self.views_dir / filename
                if source_file.exists():
                    backup_file = self.backup_dir / filename
                    shutil.copy2(source_file, backup_file)
                    self.logger.info(f"Sauvegarde créée: {backup_file}")
            
            # Créer un fichier de métadonnées
            metadata_file = self.backup_dir / "migration_info.txt"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                f.write(f"Migration analysis_view.py\n")
                f.write(f"Date: {datetime.now().isoformat()}\n")
                f.write(f"Version: CHNeoWave v2.0.0\n")
                f.write(f"Type: Refactoring vers architecture modulaire\n\n")
                f.write(f"Fichiers sauvegardés:\n")
                for filename in self.files_to_backup:
                    if (self.views_dir / filename).exists():
                        f.write(f"- {filename}\n")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def verify_new_structure(self):
        """
        Vérification de la nouvelle structure modulaire
        """
        required_files = [
            "__init__.py",
            "spectral_analysis.py",
            "goda_analysis.py",
            "statistics_analysis.py",
            "summary_report.py",
            "analysis_controller.py",
            "analysis_view_v2.py"
        ]
        
        missing_files = []
        for filename in required_files:
            file_path = self.analysis_dir / filename
            if not file_path.exists():
                missing_files.append(filename)
        
        if missing_files:
            self.logger.error(f"Fichiers manquants: {missing_files}")
            return False
        
        self.logger.info("Structure modulaire vérifiée avec succès")
        return True
    
    def update_imports(self):
        """
        Mise à jour des imports dans les fichiers qui utilisent analysis_view
        """
        files_to_update = [
            self.project_root / "src" / "hrneowave" / "gui" / "main_window.py",
            self.project_root / "src" / "hrneowave" / "gui" / "controllers" / "main_controller.py",
            self.project_root / "src" / "hrneowave" / "gui" / "controllers" / "view_manager.py"
        ]
        
        import_replacements = {
            "from ..views.analysis_view import AnalysisView": "from ..views.analysis.analysis_view_v2 import AnalysisViewV2 as AnalysisView",
            "from .views.analysis_view import AnalysisView": "from .views.analysis.analysis_view_v2 import AnalysisViewV2 as AnalysisView",
            "from hrneowave.gui.views.analysis_view import AnalysisView": "from hrneowave.gui.views.analysis.analysis_view_v2 import AnalysisViewV2 as AnalysisView"
        }
        
        updated_files = []
        
        for file_path in files_to_update:
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for old_import, new_import in import_replacements.items():
                    if old_import in content:
                        content = content.replace(old_import, new_import)
                        self.logger.info(f"Import mis à jour dans {file_path.name}: {old_import} -> {new_import}")
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_files.append(file_path.name)
                
            except Exception as e:
                self.logger.error(f"Erreur lors de la mise à jour de {file_path}: {e}")
        
        return updated_files
    
    def create_compatibility_layer(self):
        """
        Création d'une couche de compatibilité pour l'ancienne interface
        """
        compatibility_file = self.views_dir / "analysis_view_compat.py"
        
        compatibility_code = '''# -*- coding: utf-8 -*-
"""
Couche de compatibilité pour analysis_view.py
Permet l'utilisation de l'ancienne interface avec la nouvelle architecture
"""

import warnings
from .analysis.analysis_view_v2 import AnalysisViewV2


class AnalysisView(AnalysisViewV2):
    """
    Couche de compatibilité pour l'ancienne AnalysisView
    Hérite de AnalysisViewV2 et maintient l'interface legacy
    """
    
    def __init__(self, parent=None):
        warnings.warn(
            "AnalysisView est deprecated. Utilisez AnalysisViewV2 directement.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(parent)
    
    # Méthodes de compatibilité avec l'ancienne interface
    def setupUI(self):
        """Compatibilité: setupUI -> déjà appelé dans __init__"""
        pass  # Déjà fait dans le parent
    
    def connectSignals(self):
        """Compatibilité: connectSignals -> déjà appelé dans __init__"""
        pass  # Déjà fait dans le parent
    
    def setSessionData(self, session_data):
        """Compatibilité: interface identique"""
        super().setSessionData(session_data)
    
    def updateDataInfo(self):
        """Compatibilité: updateDataInfo -> _updateDataInfo"""
        self._updateDataInfo()
    
    def performSpectralAnalysis(self):
        """Compatibilité: délégation vers le widget spectral"""
        if self.spectral_widget:
            self.spectral_widget.performSpectralAnalysis()
    
    def performGodaAnalysis(self):
        """Compatibilité: délégation vers le widget Goda"""
        if self.goda_widget:
            self.goda_widget.performGodaAnalysis()
    
    def calculateStatistics(self):
        """Compatibilité: délégation vers le widget statistiques"""
        if self.statistics_widget:
            self.statistics_widget.calculateStatistics()
    
    def generateSummaryReport(self):
        """Compatibilité: délégation vers le widget rapport"""
        if self.summary_widget:
            self.summary_widget.generateSummaryReport()
    
    def completeAnalysis(self):
        """Compatibilité: completeAnalysis -> startCompleteAnalysis"""
        self.startCompleteAnalysis()
    
    def resetAnalysis(self):
        """Compatibilité: interface identique"""
        super().resetAnalysis()
    
    def get_analysis_results(self):
        """Compatibilité: get_analysis_results -> getAnalysisResults"""
        return self.getAnalysisResults()
'''
        
        try:
            with open(compatibility_file, 'w', encoding='utf-8') as f:
                f.write(compatibility_code)
            
            self.logger.info(f"Couche de compatibilité créée: {compatibility_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de la couche de compatibilité: {e}")
            return False
    
    def run_migration(self):
        """
        Exécution complète de la migration
        """
        self.logger.info("Début de la migration analysis_view.py")
        
        # 1. Créer une sauvegarde
        if not self.create_backup():
            self.logger.error("Échec de la sauvegarde - Migration annulée")
            return False
        
        # 2. Vérifier la nouvelle structure
        if not self.verify_new_structure():
            self.logger.error("Structure modulaire incomplète - Migration annulée")
            return False
        
        # 3. Mettre à jour les imports
        updated_files = self.update_imports()
        if updated_files:
            self.logger.info(f"Imports mis à jour dans: {', '.join(updated_files)}")
        
        # 4. Créer la couche de compatibilité
        if not self.create_compatibility_layer():
            self.logger.warning("Échec de la création de la couche de compatibilité")
        
        self.logger.info("Migration terminée avec succès")
        return True
    
    def rollback_migration(self):
        """
        Annulation de la migration (restauration depuis la sauvegarde)
        """
        if not self.backup_dir.exists():
            self.logger.error("Aucune sauvegarde trouvée pour le rollback")
            return False
        
        try:
            for filename in self.files_to_backup:
                backup_file = self.backup_dir / filename
                if backup_file.exists():
                    target_file = self.views_dir / filename
                    shutil.copy2(backup_file, target_file)
                    self.logger.info(f"Fichier restauré: {filename}")
            
            # Supprimer la couche de compatibilité
            compat_file = self.views_dir / "analysis_view_compat.py"
            if compat_file.exists():
                compat_file.unlink()
                self.logger.info("Couche de compatibilité supprimée")
            
            self.logger.info("Rollback terminé avec succès")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors du rollback: {e}")
            return False


def main():
    """
    Point d'entrée principal pour la migration
    """
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration analysis_view.py vers architecture modulaire")
    parser.add_argument("--project-root", default=".", help="Racine du projet CHNeoWave")
    parser.add_argument("--rollback", action="store_true", help="Annuler la migration")
    parser.add_argument("--verify-only", action="store_true", help="Vérifier seulement la structure")
    
    args = parser.parse_args()
    
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    migrator = AnalysisViewMigrator(args.project_root)
    
    if args.verify_only:
        success = migrator.verify_new_structure()
        sys.exit(0 if success else 1)
    
    if args.rollback:
        success = migrator.rollback_migration()
    else:
        success = migrator.run_migration()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()