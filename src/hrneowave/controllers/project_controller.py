#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôleur pour la gestion des projets.

Ce module gère la création, le chargement, la sauvegarde et la configuration des projets.
"""

import os

from PySide6.QtCore import QObject, Signal, Slot

class ProjectController(QObject):
    """Gère la logique métier liée aux projets."""

    project_created = Signal(dict)
    project_loaded = Signal(dict)
    project_saved = Signal(str)
    project_closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project_path = None
        self.project_metadata = {}

    @Slot(dict)
    def create_project(self, metadata):
        """Crée un nouveau projet."""
        project_name = metadata.get('project_name')
        base_path = metadata.get('base_path')

        if not project_name or not base_path:
            # Gérer l'erreur, peut-être avec un signal
            return

        self.current_project_path = os.path.join(base_path, project_name)
        self.project_metadata = metadata

        try:
            os.makedirs(self.current_project_path, exist_ok=True)
            # Créer des sous-dossiers (data, results, etc.) si nécessaire
            os.makedirs(os.path.join(self.current_project_path, 'data'), exist_ok=True)
            os.makedirs(os.path.join(self.current_project_path, 'results'), exist_ok=True)

            # Sauvegarder les métadonnées
            self.save_project_metadata()

            self.project_created.emit(self.project_metadata)

        except OSError as e:
            # Gérer l'erreur de création de dossier
            print(f"Erreur lors de la création du projet : {e}")

    def save_project_metadata(self):
        """Sauvegarde les métadonnées du projet dans un fichier."""
        if not self.current_project_path:
            return

        metadata_path = os.path.join(self.current_project_path, 'project.conf')
        # Utiliser un format plus robuste comme JSON ou YAML à l'avenir
        with open(metadata_path, 'w') as f:
            for key, value in self.project_metadata.items():
                f.write(f"{key}={value}\n")
        
        self.project_saved.emit(metadata_path)

    def close_project(self):
        """Ferme le projet en cours."""
        self.current_project_path = None
        self.project_metadata = {}
        self.project_closed.emit()