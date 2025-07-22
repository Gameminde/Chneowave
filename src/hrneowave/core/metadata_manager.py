#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de métadonnées pour CHNeoWave v1.1.0-RC
Pour laboratoires d'études maritimes en modèle réduit
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import hashlib

# Import conditionnel pour la validation de schéma
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("jsonschema non disponible - validation de schéma désactivée")

class ExperimentType(Enum):
    """Types d'expériences maritimes"""
    WAVE_GENERATION = "wave_generation"
    WAVE_PROPAGATION = "wave_propagation"
    WAVE_BREAKING = "wave_breaking"
    SHIP_RESISTANCE = "ship_resistance"
    SHIP_SEAKEEPING = "ship_seakeeping"
    OFFSHORE_STRUCTURE = "offshore_structure"
    COASTAL_ENGINEERING = "coastal_engineering"
    FREE_SURFACE_FLOW = "free_surface_flow"
    OTHER = "other"

class WaveType(Enum):
    """Types de houle"""
    REGULAR = "regular"
    IRREGULAR = "irregular"
    FOCUSED = "focused"
    BREAKING = "breaking"
    SOLITARY = "solitary"
    TSUNAMI = "tsunami"

@dataclass
class SensorMetadata:
    """Métadonnées d'un capteur"""
    sensor_id: str
    sensor_type: str  # 'wave_probe', 'pressure', 'force', 'acceleration'
    channel: int
    location: Dict[str, float]  # x, y, z coordinates
    calibration_date: Optional[datetime] = None
    calibration_coefficients: Optional[Dict[str, float]] = None
    measurement_range: Optional[Dict[str, float]] = None  # min, max
    units: str = "V"  # Unités de mesure
    sampling_rate: float = 100.0  # Hz
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire sérialisable"""
        data = asdict(self)
        if self.calibration_date:
            data['calibration_date'] = self.calibration_date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SensorMetadata':
        """Crée depuis un dictionnaire"""
        if 'calibration_date' in data and data['calibration_date']:
            data['calibration_date'] = datetime.fromisoformat(data['calibration_date'])
        return cls(**data)

@dataclass
class WaveConditions:
    """Conditions de houle"""
    wave_type: WaveType
    significant_height: Optional[float] = None  # Hs en m
    peak_period: Optional[float] = None  # Tp en s
    wave_direction: Optional[float] = None  # degrés
    spectrum_type: Optional[str] = None  # JONSWAP, Pierson-Moskowitz, etc.
    gamma: Optional[float] = None  # Paramètre de forme JONSWAP
    water_depth: Optional[float] = None  # Profondeur d'eau en m
    current_velocity: Optional[float] = None  # Vitesse du courant en m/s
    current_direction: Optional[float] = None  # Direction du courant en degrés
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire sérialisable"""
        data = asdict(self)
        data['wave_type'] = self.wave_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WaveConditions':
        """Crée depuis un dictionnaire"""
        if 'wave_type' in data:
            data['wave_type'] = WaveType(data['wave_type'])
        return cls(**data)

@dataclass
class EnvironmentalConditions:
    """Conditions environnementales"""
    temperature: Optional[float] = None  # °C
    humidity: Optional[float] = None  # %
    atmospheric_pressure: Optional[float] = None  # hPa
    wind_speed: Optional[float] = None  # m/s
    wind_direction: Optional[float] = None  # degrés
    water_temperature: Optional[float] = None  # °C
    salinity: Optional[float] = None  # ppt
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire sérialisable"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnvironmentalConditions':
        """Crée depuis un dictionnaire"""
        return cls(**data)

@dataclass
class ModelGeometry:
    """Géométrie du modèle testé"""
    model_name: str
    model_type: str  # 'ship', 'platform', 'breakwater', etc.
    scale_factor: Optional[float] = None
    length: Optional[float] = None  # m
    beam: Optional[float] = None  # m
    draft: Optional[float] = None  # m
    displacement: Optional[float] = None  # kg
    center_of_gravity: Optional[Dict[str, float]] = None  # x, y, z
    moment_of_inertia: Optional[Dict[str, float]] = None  # Ixx, Iyy, Izz
    description: str = ""
    cad_file_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire sérialisable"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelGeometry':
        """Crée depuis un dictionnaire"""
        return cls(**data)

@dataclass
class AcquisitionSettings:
    """Paramètres d'acquisition"""
    sampling_rate: float  # Hz
    duration: float  # secondes
    pre_trigger: float = 0.0  # secondes
    post_trigger: float = 0.0  # secondes
    trigger_type: str = "manual"  # manual, threshold, external
    trigger_level: Optional[float] = None
    trigger_channel: Optional[int] = None
    anti_aliasing_filter: bool = True
    filter_cutoff: Optional[float] = None  # Hz
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire sérialisable"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AcquisitionSettings':
        """Crée depuis un dictionnaire"""
        return cls(**data)

@dataclass
class SessionMetadata:
    """Métadonnées complètes d'une session d'acquisition"""
    # Identifiants
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_name: str = ""
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Expérience
    experiment_type: ExperimentType = ExperimentType.OTHER
    experiment_description: str = ""
    test_number: Optional[str] = None
    operator: str = ""
    laboratory: str = ""
    project_name: str = ""
    
    # Configuration technique
    sensors: List[SensorMetadata] = field(default_factory=list)
    acquisition_settings: Optional[AcquisitionSettings] = None
    
    # Conditions expérimentales
    wave_conditions: Optional[WaveConditions] = None
    environmental_conditions: Optional[EnvironmentalConditions] = None
    model_geometry: Optional[ModelGeometry] = None
    
    # Données de session
    data_files: List[str] = field(default_factory=list)
    total_samples: int = 0
    file_size_bytes: int = 0
    
    # Qualité et validation
    data_quality_score: Optional[float] = None  # 0-100
    validation_status: str = "pending"  # pending, validated, rejected
    validation_notes: str = ""
    
    # Métadonnées étendues
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    # Versioning et intégrité
    metadata_version: str = "1.0.0"
    checksum: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire sérialisable"""
        data = {
            'session_id': self.session_id,
            'session_name': self.session_name,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'experiment_type': self.experiment_type.value,
            'experiment_description': self.experiment_description,
            'test_number': self.test_number,
            'operator': self.operator,
            'laboratory': self.laboratory,
            'project_name': self.project_name,
            'sensors': [sensor.to_dict() for sensor in self.sensors],
            'acquisition_settings': self.acquisition_settings.to_dict() if self.acquisition_settings else None,
            'wave_conditions': self.wave_conditions.to_dict() if self.wave_conditions else None,
            'environmental_conditions': self.environmental_conditions.to_dict() if self.environmental_conditions else None,
            'model_geometry': self.model_geometry.to_dict() if self.model_geometry else None,
            'data_files': self.data_files,
            'total_samples': self.total_samples,
            'file_size_bytes': self.file_size_bytes,
            'data_quality_score': self.data_quality_score,
            'validation_status': self.validation_status,
            'validation_notes': self.validation_notes,
            'tags': self.tags,
            'custom_fields': self.custom_fields,
            'metadata_version': self.metadata_version,
            'checksum': self.checksum
        }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionMetadata':
        """Crée depuis un dictionnaire"""
        # Conversion des timestamps
        if 'created_at' in data:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'started_at' in data and data['started_at']:
            data['started_at'] = datetime.fromisoformat(data['started_at'])
        if 'completed_at' in data and data['completed_at']:
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        
        # Conversion des enums
        if 'experiment_type' in data:
            data['experiment_type'] = ExperimentType(data['experiment_type'])
        
        # Conversion des objets complexes
        if 'sensors' in data:
            data['sensors'] = [SensorMetadata.from_dict(s) for s in data['sensors']]
        
        if 'acquisition_settings' in data and data['acquisition_settings']:
            data['acquisition_settings'] = AcquisitionSettings.from_dict(data['acquisition_settings'])
        
        if 'wave_conditions' in data and data['wave_conditions']:
            data['wave_conditions'] = WaveConditions.from_dict(data['wave_conditions'])
        
        if 'environmental_conditions' in data and data['environmental_conditions']:
            data['environmental_conditions'] = EnvironmentalConditions.from_dict(data['environmental_conditions'])
        
        if 'model_geometry' in data and data['model_geometry']:
            data['model_geometry'] = ModelGeometry.from_dict(data['model_geometry'])
        
        return cls(**data)
    
    def calculate_checksum(self) -> str:
        """Calcule le checksum des métadonnées"""
        # Exclure le checksum lui-même du calcul
        data = self.to_dict()
        data.pop('checksum', None)
        
        # Sérialiser de manière déterministe
        json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def update_checksum(self):
        """Met à jour le checksum"""
        self.checksum = self.calculate_checksum()
    
    def verify_integrity(self) -> bool:
        """Vérifie l'intégrité des métadonnées"""
        if not self.checksum:
            return False
        return self.checksum == self.calculate_checksum()

class MetadataManager:
    """Gestionnaire de métadonnées pour les sessions d'acquisition"""
    
    def __init__(self, base_path: Optional[Union[str, Path]] = None):
        self.base_path = Path(base_path) if base_path else Path.cwd() / "metadata"
        self.base_path.mkdir(exist_ok=True)
        
        # Schéma JSON pour validation (si disponible)
        self.schema = self._create_json_schema() if JSONSCHEMA_AVAILABLE else None
    
    def create_session(self, session_name: str = "", 
                      experiment_type: ExperimentType = ExperimentType.OTHER) -> SessionMetadata:
        """Crée une nouvelle session de métadonnées"""
        session = SessionMetadata(
            session_name=session_name,
            experiment_type=experiment_type
        )
        session.update_checksum()
        return session
    
    def save_metadata(self, metadata: SessionMetadata, 
                     file_path: Optional[Union[str, Path]] = None) -> Path:
        """Sauvegarde les métadonnées dans un fichier JSON"""
        if file_path is None:
            filename = f"session_{metadata.session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = self.base_path / filename
        else:
            file_path = Path(file_path)
        
        # Mettre à jour le checksum avant sauvegarde
        metadata.update_checksum()
        
        # Sauvegarder
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata.to_dict(), f, indent=2, ensure_ascii=False)
        
        print(f"Métadonnées sauvegardées: {file_path}")
        return file_path
    
    def load_metadata(self, file_path: Union[str, Path]) -> SessionMetadata:
        """Charge les métadonnées depuis un fichier JSON"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier de métadonnées non trouvé: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validation du schéma si disponible
        if self.schema and JSONSCHEMA_AVAILABLE:
            try:
                jsonschema.validate(data, self.schema)
            except jsonschema.ValidationError as e:
                print(f"Avertissement: Validation schéma échouée: {e}")
        
        metadata = SessionMetadata.from_dict(data)
        
        # Vérification de l'intégrité
        if not metadata.verify_integrity():
            print("Avertissement: Intégrité des métadonnées compromise")
        
        return metadata
    
    def list_sessions(self, pattern: str = "*.json") -> List[Path]:
        """Liste les fichiers de métadonnées"""
        return list(self.base_path.glob(pattern))
    
    def search_sessions(self, **criteria) -> List[SessionMetadata]:
        """Recherche des sessions selon des critères"""
        sessions = []
        
        for file_path in self.list_sessions():
            try:
                metadata = self.load_metadata(file_path)
                
                # Vérifier les critères
                match = True
                for key, value in criteria.items():
                    if hasattr(metadata, key):
                        attr_value = getattr(metadata, key)
                        
                        # Gérer les comparaisons d'enum
                        if isinstance(attr_value, Enum) and isinstance(value, Enum):
                            # Comparer les enums directement
                            if attr_value != value:
                                match = False
                                break
                        elif isinstance(attr_value, Enum):
                            # Comparer enum avec valeur
                            if attr_value.value != value:
                                match = False
                                break
                        elif isinstance(value, Enum):
                            # Comparer valeur avec enum
                            if attr_value != value.value:
                                match = False
                                break
                        else:
                            # Comparaison normale
                            if attr_value != value:
                                match = False
                                break
                
                if match:
                    sessions.append(metadata)
                    
            except Exception as e:
                print(f"Erreur lecture métadonnées {file_path}: {e}")
        
        return sessions
    
    def export_metadata_summary(self, output_path: Union[str, Path]) -> bool:
        """Exporte un résumé de toutes les sessions"""
        try:
            sessions = []
            
            for file_path in self.list_sessions():
                try:
                    metadata = self.load_metadata(file_path)
                    summary = {
                        'session_id': metadata.session_id,
                        'session_name': metadata.session_name,
                        'created_at': metadata.created_at.isoformat(),
                        'experiment_type': metadata.experiment_type.value,
                        'operator': metadata.operator,
                        'total_samples': metadata.total_samples,
                        'validation_status': metadata.validation_status
                    }
                    sessions.append(summary)
                except Exception as e:
                    print(f"Erreur lecture {file_path}: {e}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, indent=2, ensure_ascii=False)
            
            print(f"Résumé exporté: {output_path}")
            return True
            
        except Exception as e:
            print(f"Erreur export résumé: {e}")
            return False
    
    def _create_json_schema(self) -> Dict[str, Any]:
        """Crée le schéma JSON pour validation"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["session_id", "created_at", "experiment_type", "metadata_version"],
            "properties": {
                "session_id": {"type": "string"},
                "session_name": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "experiment_type": {
                    "type": "string",
                    "enum": [e.value for e in ExperimentType]
                },
                "metadata_version": {"type": "string"},
                "sensors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["sensor_id", "sensor_type", "channel"],
                        "properties": {
                            "sensor_id": {"type": "string"},
                            "sensor_type": {"type": "string"},
                            "channel": {"type": "integer"}
                        }
                    }
                }
            }
        }

# Factory functions
def create_metadata_manager(base_path: Optional[Union[str, Path]] = None) -> MetadataManager:
    """Crée un gestionnaire de métadonnées"""
    return MetadataManager(base_path)

def create_sample_session_metadata() -> SessionMetadata:
    """Crée des métadonnées d'exemple pour test"""
    # Capteurs d'exemple
    sensors = [
        SensorMetadata(
            sensor_id="WP01",
            sensor_type="wave_probe",
            channel=0,
            location={"x": 0.0, "y": 0.0, "z": 0.0},
            units="mm",
            description="Sonde de houle principale"
        ),
        SensorMetadata(
            sensor_id="WP02",
            sensor_type="wave_probe",
            channel=1,
            location={"x": 1.0, "y": 0.0, "z": 0.0},
            units="mm",
            description="Sonde de houle secondaire"
        )
    ]
    
    # Paramètres d'acquisition
    acq_settings = AcquisitionSettings(
        sampling_rate=100.0,
        duration=60.0,
        trigger_type="manual"
    )
    
    # Conditions de houle
    wave_conditions = WaveConditions(
        wave_type=WaveType.IRREGULAR,
        significant_height=0.1,  # 10 cm
        peak_period=1.2,  # 1.2 s
        spectrum_type="JONSWAP",
        gamma=3.3,
        water_depth=0.5
    )
    
    # Conditions environnementales
    env_conditions = EnvironmentalConditions(
        temperature=20.5,
        humidity=45.0,
        atmospheric_pressure=1013.2,
        water_temperature=20.0
    )
    
    # Géométrie du modèle
    model = ModelGeometry(
        model_name="Navire Test",
        model_type="ship",
        scale_factor=1/50,
        length=2.0,
        beam=0.3,
        draft=0.1,
        displacement=15.0
    )
    
    # Session complète
    session = SessionMetadata(
        session_name="Test Houle Irrégulière",
        experiment_type=ExperimentType.WAVE_PROPAGATION,
        experiment_description="Test de propagation de houle irrégulière JONSWAP",
        test_number="TEST_001",
        operator="Ingénieur Test",
        laboratory="Laboratoire Méditerranéen",
        project_name="Projet CHNeoWave",
        sensors=sensors,
        acquisition_settings=acq_settings,
        wave_conditions=wave_conditions,
        environmental_conditions=env_conditions,
        model_geometry=model,
        tags=["houle", "irrégulière", "JONSWAP", "test"]
    )
    
    session.update_checksum()
    return session