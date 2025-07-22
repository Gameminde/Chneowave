#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Project Manager v2.0
Gestionnaire de projets et sessions

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2024
Version: 2.0.0
"""

import os
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class ProjectStatus(Enum):
    """États d'un projet"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"

class SessionType(Enum):
    """Types de session"""
    ACQUISITION = "acquisition"
    ANALYSIS = "analysis"
    CALIBRATION = "calibration"
    EXPORT = "export"
    MIXED = "mixed"

@dataclass
class ProjectMetadata:
    """Métadonnées d'un projet"""
    id: str
    name: str
    description: str
    created_at: str
    modified_at: str
    status: str
    version: str = "2.0.0"
    author: str = ""
    tags: List[str] = None
    location: str = ""
    basin_type: str = ""  # "canal", "bassin", "mer"
    water_depth: float = 0.0
    wave_conditions: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.wave_conditions is None:
            self.wave_conditions = {
                "significant_height": 0.0,
                "peak_period": 0.0,
                "direction": 0.0,
                "spectrum_type": "JONSWAP"
            }

@dataclass
class SessionMetadata:
    """Métadonnées d'une session"""
    id: str
    name: str
    project_id: str
    session_type: str
    created_at: str
    duration: float = 0.0
    data_files: List[str] = None
    notes: str = ""
    parameters: Dict[str, Any] = None
    results: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data_files is None:
            self.data_files = []
        if self.parameters is None:
            self.parameters = {}
        if self.results is None:
            self.results = {}

class ProjectManager:
    """Gestionnaire de projets et sessions"""
    
    def __init__(self, workspace_dir: Optional[Union[str, Path]] = None):
        """
        Initialise le gestionnaire de projets
        
        Args:
            workspace_dir: Répertoire de travail (par défaut: ~/CHNeoWave_Projects)
        """
        if workspace_dir is None:
            self.workspace_dir = Path.home() / "CHNeoWave_Projects"
        else:
            self.workspace_dir = Path(workspace_dir)
            
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Fichier d'index des projets
        self.projects_index_file = self.workspace_dir / "projects_index.json"
        
        # Projet et session actuels
        self._current_project: Optional[ProjectMetadata] = None
        self._current_session: Optional[SessionMetadata] = None
        
        # Index des projets
        self._projects_index: Dict[str, Dict[str, Any]] = {}
        
        # Charger l'index
        self._load_projects_index()
        
    def _load_projects_index(self):
        """Charge l'index des projets"""
        if self.projects_index_file.exists():
            try:
                with open(self.projects_index_file, 'r', encoding='utf-8') as f:
                    self._projects_index = json.load(f)
                logger.info(f"Index des projets chargé: {len(self._projects_index)} projets")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de l'index des projets: {e}")
                self._projects_index = {}
        else:
            self._projects_index = {}
            
    def _save_projects_index(self):
        """Sauvegarde l'index des projets"""
        try:
            with open(self.projects_index_file, 'w', encoding='utf-8') as f:
                json.dump(self._projects_index, f, indent=2, ensure_ascii=False)
            logger.info("Index des projets sauvegardé")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'index des projets: {e}")
            
    def create_project(self, name: str, description: str = "", **kwargs) -> str:
        """Crée un nouveau projet
        
        Args:
            name: Nom du projet
            description: Description du projet
            **kwargs: Métadonnées supplémentaires
            
        Returns:
            ID du projet créé
        """
        project_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Créer les métadonnées
        metadata = ProjectMetadata(
            id=project_id,
            name=name,
            description=description,
            created_at=timestamp,
            modified_at=timestamp,
            status=ProjectStatus.ACTIVE.value,
            **kwargs
        )
        
        # Créer le répertoire du projet
        project_dir = self.workspace_dir / f"project_{project_id}"
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer la structure du projet
        (project_dir / "data").mkdir(exist_ok=True)
        (project_dir / "sessions").mkdir(exist_ok=True)
        (project_dir / "exports").mkdir(exist_ok=True)
        (project_dir / "analysis").mkdir(exist_ok=True)
        (project_dir / "calibration").mkdir(exist_ok=True)
        
        # Sauvegarder les métadonnées
        metadata_file = project_dir / "project_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(metadata), f, indent=2, ensure_ascii=False)
            
        # Mettre à jour l'index
        self._projects_index[project_id] = {
            "name": name,
            "description": description,
            "created_at": timestamp,
            "modified_at": timestamp,
            "status": ProjectStatus.ACTIVE.value,
            "path": str(project_dir)
        }
        
        self._save_projects_index()
        
        logger.info(f"Projet créé: {name} (ID: {project_id})")
        return project_id
        
    def load_project(self, project_id: str) -> bool:
        """Charge un projet
        
        Args:
            project_id: ID du projet
            
        Returns:
            True si le projet a été chargé avec succès
        """
        if project_id not in self._projects_index:
            logger.error(f"Projet introuvable: {project_id}")
            return False
            
        project_dir = Path(self._projects_index[project_id]["path"])
        metadata_file = project_dir / "project_metadata.json"
        
        if not metadata_file.exists():
            logger.error(f"Fichier de métadonnées introuvable: {metadata_file}")
            return False
            
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata_dict = json.load(f)
                
            self._current_project = ProjectMetadata(**metadata_dict)
            logger.info(f"Projet chargé: {self._current_project.name}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du projet: {e}")
            return False
            
    def get_current_project(self) -> Optional[ProjectMetadata]:
        """Retourne le projet actuel"""
        return self._current_project
        
    def update_project(self, **kwargs) -> bool:
        """Met à jour le projet actuel
        
        Args:
            **kwargs: Champs à mettre à jour
            
        Returns:
            True si la mise à jour a réussi
        """
        if self._current_project is None:
            logger.error("Aucun projet chargé")
            return False
            
        # Mettre à jour les métadonnées
        for key, value in kwargs.items():
            if hasattr(self._current_project, key):
                setattr(self._current_project, key, value)
                
        self._current_project.modified_at = datetime.now(timezone.utc).isoformat()
        
        # Sauvegarder
        return self._save_project_metadata()
        
    def _save_project_metadata(self) -> bool:
        """Sauvegarde les métadonnées du projet actuel"""
        if self._current_project is None:
            return False
            
        try:
            project_dir = self.get_project_directory(self._current_project.id)
            metadata_file = project_dir / "project_metadata.json"
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._current_project), f, indent=2, ensure_ascii=False)
                
            # Mettre à jour l'index
            self._projects_index[self._current_project.id].update({
                "name": self._current_project.name,
                "description": self._current_project.description,
                "modified_at": self._current_project.modified_at,
                "status": self._current_project.status
            })
            
            self._save_projects_index()
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des métadonnées: {e}")
            return False
            
    def create_session(self, name: str, session_type: SessionType, **kwargs) -> str:
        """Crée une nouvelle session
        
        Args:
            name: Nom de la session
            session_type: Type de session
            **kwargs: Paramètres supplémentaires
            
        Returns:
            ID de la session créée
        """
        if self._current_project is None:
            raise ValueError("Aucun projet chargé")
            
        session_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Créer les métadonnées
        metadata = SessionMetadata(
            id=session_id,
            name=name,
            project_id=self._current_project.id,
            session_type=session_type.value,
            created_at=timestamp,
            **kwargs
        )
        
        # Créer le répertoire de la session
        project_dir = self.get_project_directory(self._current_project.id)
        session_dir = project_dir / "sessions" / f"session_{session_id}"
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder les métadonnées
        metadata_file = session_dir / "session_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(metadata), f, indent=2, ensure_ascii=False)
            
        self._current_session = metadata
        
        logger.info(f"Session créée: {name} (ID: {session_id})")
        return session_id
        
    def load_session(self, session_id: str) -> bool:
        """Charge une session
        
        Args:
            session_id: ID de la session
            
        Returns:
            True si la session a été chargée avec succès
        """
        if self._current_project is None:
            logger.error("Aucun projet chargé")
            return False
            
        project_dir = self.get_project_directory(self._current_project.id)
        session_dir = project_dir / "sessions" / f"session_{session_id}"
        metadata_file = session_dir / "session_metadata.json"
        
        if not metadata_file.exists():
            logger.error(f"Session introuvable: {session_id}")
            return False
            
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata_dict = json.load(f)
                
            self._current_session = SessionMetadata(**metadata_dict)
            logger.info(f"Session chargée: {self._current_session.name}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la session: {e}")
            return False
            
    def get_current_session(self) -> Optional[SessionMetadata]:
        """Retourne la session actuelle"""
        return self._current_session
        
    def list_projects(self) -> List[Dict[str, Any]]:
        """Liste tous les projets
        
        Returns:
            Liste des projets avec leurs métadonnées
        """
        projects = []
        for project_id, project_info in self._projects_index.items():
            projects.append({
                "id": project_id,
                **project_info
            })
        return projects
        
    def list_sessions(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Liste les sessions d'un projet
        
        Args:
            project_id: ID du projet (par défaut: projet actuel)
            
        Returns:
            Liste des sessions
        """
        if project_id is None:
            if self._current_project is None:
                return []
            project_id = self._current_project.id
            
        project_dir = self.get_project_directory(project_id)
        sessions_dir = project_dir / "sessions"
        
        if not sessions_dir.exists():
            return []
            
        sessions = []
        for session_dir in sessions_dir.iterdir():
            if session_dir.is_dir() and session_dir.name.startswith("session_"):
                metadata_file = session_dir / "session_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            session_data = json.load(f)
                        sessions.append(session_data)
                    except Exception as e:
                        logger.warning(f"Erreur lors de la lecture de la session {session_dir.name}: {e}")
                        
        return sessions
        
    def get_project_directory(self, project_id: str) -> Path:
        """Retourne le répertoire d'un projet
        
        Args:
            project_id: ID du projet
            
        Returns:
            Chemin du répertoire du projet
        """
        if project_id in self._projects_index:
            return Path(self._projects_index[project_id]["path"])
        else:
            return self.workspace_dir / f"project_{project_id}"
            
    def get_session_directory(self, session_id: str, project_id: Optional[str] = None) -> Path:
        """Retourne le répertoire d'une session
        
        Args:
            session_id: ID de la session
            project_id: ID du projet (par défaut: projet actuel)
            
        Returns:
            Chemin du répertoire de la session
        """
        if project_id is None:
            if self._current_project is None:
                raise ValueError("Aucun projet spécifié")
            project_id = self._current_project.id
            
        project_dir = self.get_project_directory(project_id)
        return project_dir / "sessions" / f"session_{session_id}"
        
    def delete_project(self, project_id: str, confirm: bool = False) -> bool:
        """Supprime un projet
        
        Args:
            project_id: ID du projet
            confirm: Confirmation de suppression
            
        Returns:
            True si la suppression a réussi
        """
        if not confirm:
            logger.warning("Suppression annulée: confirmation requise")
            return False
            
        if project_id not in self._projects_index:
            logger.error(f"Projet introuvable: {project_id}")
            return False
            
        try:
            # Supprimer le répertoire
            project_dir = Path(self._projects_index[project_id]["path"])
            if project_dir.exists():
                shutil.rmtree(project_dir)
                
            # Supprimer de l'index
            del self._projects_index[project_id]
            self._save_projects_index()
            
            # Décharger si c'est le projet actuel
            if self._current_project and self._current_project.id == project_id:
                self._current_project = None
                self._current_session = None
                
            logger.info(f"Projet supprimé: {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du projet: {e}")
            return False
            
    def export_project(self, project_id: str, export_path: Union[str, Path]) -> bool:
        """Exporte un projet
        
        Args:
            project_id: ID du projet
            export_path: Chemin d'export
            
        Returns:
            True si l'export a réussi
        """
        if project_id not in self._projects_index:
            logger.error(f"Projet introuvable: {project_id}")
            return False
            
        try:
            project_dir = Path(self._projects_index[project_id]["path"])
            export_path = Path(export_path)
            
            # Créer l'archive
            shutil.make_archive(str(export_path), 'zip', str(project_dir))
            
            logger.info(f"Projet exporté: {export_path}.zip")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export du projet: {e}")
            return False
            
    def get_workspace_info(self) -> Dict[str, Any]:
        """Retourne les informations sur l'espace de travail
        
        Returns:
            Informations sur l'espace de travail
        """
        total_size = 0
        project_count = len(self._projects_index)
        session_count = 0
        
        for project_id in self._projects_index:
            project_dir = self.get_project_directory(project_id)
            if project_dir.exists():
                # Calculer la taille
                for file_path in project_dir.rglob('*'):
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
                        
                # Compter les sessions
                sessions = self.list_sessions(project_id)
                session_count += len(sessions)
                
        return {
            "workspace_dir": str(self.workspace_dir),
            "project_count": project_count,
            "session_count": session_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }

# Instance globale du gestionnaire de projets
_project_manager = None

def get_project_manager() -> ProjectManager:
    """Retourne l'instance globale du gestionnaire de projets"""
    global _project_manager
    if _project_manager is None:
        _project_manager = ProjectManager()
    return _project_manager