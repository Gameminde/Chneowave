#!/usr/bin/env python3
"""
Module d'export HDF5 pour CHNeoWave
Export scientifique traçable avec métadonnées et hash SHA-256
"""

import h5py
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
from datetime import datetime
import json
import tempfile
import os
import shutil

class HDF5Writer:
    """
    Écrivain HDF5 pour données d'acquisition CHNeoWave
    Format standardisé avec métadonnées traçables
    """
    
    def __init__(self, filepath: Path):
        """
        Initialise l'écrivain HDF5
        
        Args:
            filepath: Chemin du fichier HDF5 à créer
        """
        self.filepath = Path(filepath)
        self.file_handle: Optional[h5py.File] = None
        
    def __enter__(self):
        """Context manager entry"""
        self.file_handle = h5py.File(self.filepath, 'w')
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.file_handle:
            self.file_handle.close()
            
    def write_acquisition_data(self, 
                             data: np.ndarray,
                             sampling_rate: float,
                             channel_names: list,
                             metadata: Optional[Dict[str, Any]] = None):
        """
        Écrit les données d'acquisition en format HDF5 standardisé
        
        Args:
            data: Données d'acquisition (samples x channels)
            sampling_rate: Fréquence d'échantillonnage en Hz
            channel_names: Noms des canaux
            metadata: Métadonnées additionnelles
        """
        if self.file_handle is None:
            raise RuntimeError("Fichier HDF5 non ouvert")
            
        # Dataset principal des données brutes
        raw_dataset = self.file_handle.create_dataset(
            '/raw', 
            data=data,
            compression='gzip',
            compression_opts=6,
            shuffle=True
        )
        
        # Attributs et métadonnées
        attrs = {
            'fs': sampling_rate,
            'n_channels': data.shape[1],
            'n_samples': data.shape[0],
            'duration': data.shape[0] / sampling_rate,
            'created_at': datetime.now().isoformat(),
            'software': 'CHNeoWave v1.1.0-beta',
            'channel_names': [name.encode('utf-8') for name in channel_names]
        }
        if metadata:
            attrs.update(metadata)

        for key, value in attrs.items():
            if isinstance(value, dict):
                # Sérialiser les dictionnaires (comme metadata) en JSON
                self.file_handle.attrs[key] = json.dumps(value)
            else:
                self.file_handle.attrs[key] = value

        # Calcul et écriture du hash
        self.file_handle.flush()
        file_hash = self._calculate_internal_hash(self.file_handle)
        self.file_handle.attrs['sha256'] = file_hash
                    


    @staticmethod
    def _calculate_internal_hash(h5_file: h5py.File) -> str:
        """Calcule un hash SHA-256 basé sur le contenu interne du fichier HDF5."""
        sha256_hash = hashlib.sha256()

        def hash_attrs(attrs):
            for key, value in sorted(attrs.items()):
                if key == 'sha256': continue # Exclure l'ancien hash
                sha256_hash.update(str(key).encode('utf-8'))
                sha256_hash.update(str(value).encode('utf-8'))

        # Hasher les attributs du fichier racine
        hash_attrs(h5_file.attrs)

        # Hasher les datasets et leurs attributs
        def hash_dataset(name):
            dataset = h5_file[name]
            dataset_array = dataset[:]
            sha256_hash.update(name.encode('utf-8'))
            sha256_hash.update(dataset_array.tobytes())
            hash_attrs(dataset.attrs)

        h5_file.visit(hash_dataset)

        return sha256_hash.hexdigest()
        
    @staticmethod
    def read_acquisition_data(filepath: Path) -> Dict[str, Any]:
        """
        Lit les données d'acquisition depuis un fichier HDF5
        
        Args:
            filepath: Chemin du fichier HDF5
            
        Returns:
            Dictionnaire contenant les données et métadonnées
        """
        result = {}
        
        with h5py.File(filepath, 'r') as f:
            # Données brutes
            raw_dataset = f['/raw']
            result['data'] = raw_dataset[:]
            
            # Métadonnées du dataset
            result['metadata'] = {}
            for key, value in raw_dataset.attrs.items():
                if isinstance(value, bytes):
                    result['metadata'][key] = value.decode('utf-8')
                else:
                    result['metadata'][key] = value
                    
            # Métadonnées du fichier principal (incluant le hash SHA256)
            for key, value in f.attrs.items():
                if isinstance(value, bytes):
                    result['metadata'][key] = value.decode('utf-8')
                else:
                    result['metadata'][key] = value
                    
            # Noms des canaux
            if 'channel_names' in raw_dataset.attrs:
                channel_names = raw_dataset.attrs['channel_names']
                if isinstance(channel_names[0], bytes):
                    result['metadata']['channel_names'] = [name.decode('utf-8') for name in channel_names]
                    
        return result
        


    @staticmethod
    def verify_file_integrity(filepath: Path) -> bool:
        """Vérifie l'intégrité d'un fichier HDF5 via son hash interne SHA256."""
        if not filepath.exists():
            return False
        
        try:
            with h5py.File(filepath, 'r') as f:
                if 'sha256' not in f.attrs:
                    return False
                stored_hash = f.attrs['sha256']
                
                # Calculer le hash à partir du contenu actuel
                calculated_hash = HDF5Writer._calculate_internal_hash(f)
                
            return stored_hash == calculated_hash
        except (IOError, KeyError, h5py.Error):
            # h5py.Error pour les fichiers corrompus
            return False

def export_to_hdf5(data: np.ndarray,
                  sampling_rate: float,
                  channel_names: list,
                  output_path: Path,
                  metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Fonction utilitaire pour export HDF5 simple
    
    Args:
        data: Données d'acquisition (samples x channels)
        sampling_rate: Fréquence d'échantillonnage
        channel_names: Noms des canaux
        output_path: Chemin de sortie
        metadata: Métadonnées optionnelles
        
    Returns:
        Hash SHA-256 du fichier créé
    """
    with HDF5Writer(output_path) as writer:
        hash_val = writer.write_acquisition_data(
            data=data,
            sampling_rate=sampling_rate,
            channel_names=channel_names,
            metadata=metadata
        )
        writer.create_metadata_file(metadata)
        return hash_val

    def create_metadata_file(self, metadata: Dict[str, Any]):
        """Crée un fichier de métadonnées JSON avec le checksum du fichier HDF5.

        Args:
            metadata (dict): Les métadonnées à inclure.
        """
        checksum = self.file_handle.attrs.get('sha256')
        if not checksum:
            return

        metadata_with_checksum = {
            'checksum_sha256': checksum,
            'original_metadata': metadata
        }
        
        metadata_file_path = self.filepath.with_suffix('.json')
        with open(metadata_file_path, 'w') as f:
            json.dump(metadata_with_checksum, f, indent=4)