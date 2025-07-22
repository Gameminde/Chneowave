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
                             metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Écrit les données d'acquisition en format HDF5 standardisé
        
        Args:
            data: Données d'acquisition (samples x channels)
            sampling_rate: Fréquence d'échantillonnage en Hz
            channel_names: Noms des canaux
            metadata: Métadonnées additionnelles
            
        Returns:
            Hash SHA-256 du fichier créé
        """
        if self.file_handle is None:
            raise RuntimeError("Fichier HDF5 non ouvert")
            
        # Dataset principal des données brutes
        # Permettre le redimensionnement pour les gros datasets
        raw_dataset = self.file_handle.create_dataset(
            '/raw', 
            data=data,
            compression='gzip',
            compression_opts=6,
            shuffle=True,
            maxshape=(None, data.shape[1])  # Permettre l'extension en nombre d'échantillons
        )
        
        # Attributs obligatoires
        raw_dataset.attrs['fs'] = sampling_rate
        raw_dataset.attrs['n_channels'] = data.shape[1]
        raw_dataset.attrs['n_samples'] = data.shape[0]
        raw_dataset.attrs['duration'] = data.shape[0] / sampling_rate
        raw_dataset.attrs['created_at'] = datetime.now().isoformat()
        raw_dataset.attrs['software'] = 'CHNeoWave v1.1.0-beta'
        
        # Noms des canaux
        channel_names_encoded = [name.encode('utf-8') for name in channel_names]
        raw_dataset.attrs['channel_names'] = channel_names_encoded
        
        # Métadonnées additionnelles
        if metadata:
            for key, value in metadata.items():
                if isinstance(value, str):
                    raw_dataset.attrs[key] = value.encode('utf-8')
                else:
                    raw_dataset.attrs[key] = value
                    
        # Forcer l'écriture
        self.file_handle.flush()
        
        # Calculer le hash SHA-256 et l'ajouter aux attributs du fichier principal
        file_hash = self._calculate_file_hash()
        
        # Ajouter le hash aux attributs du fichier principal (pas du dataset)
        try:
            self.file_handle.attrs['sha256'] = file_hash
            self.file_handle.flush()
        except Exception:
            # Si l'ajout échoue, continuer sans le hash
            pass
        
        return file_hash
        
    def _calculate_file_hash(self) -> str:
        """
        Calcule le hash SHA-256 du fichier HDF5
        
        Returns:
            Hash SHA-256 en hexadécimal
        """
        # Fermer temporairement pour calculer le hash
        if self.file_handle:
            self.file_handle.close()
            
        # Calculer le hash
        sha256_hash = hashlib.sha256()
        with open(self.filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
                
        file_hash = sha256_hash.hexdigest()
        
        # Rouvrir le fichier
        self.file_handle = h5py.File(self.filepath, 'a')
        
        return file_hash
        
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
        """
        Vérifie l'intégrité d'un fichier HDF5 via son hash SHA-256
        
        Args:
            filepath: Chemin du fichier HDF5
            
        Returns:
            True si l'intégrité est vérifiée
        """
        try:
            with h5py.File(filepath, 'r') as f:
                # Le hash est maintenant stocké dans les attributs du fichier principal
                stored_hash = f.attrs.get('sha256')
                if stored_hash is None:
                    return False
                    
                if isinstance(stored_hash, bytes):
                    stored_hash = stored_hash.decode('utf-8')
                    
            # Calculer le hash actuel (sans l'attribut sha256)
            temp_file = filepath.with_suffix('.tmp')
            
            # Copier sans l'attribut sha256 du fichier principal
            with h5py.File(filepath, 'r') as src, h5py.File(temp_file, 'w') as dst:
                raw_src = src['/raw']
                raw_dst = dst.create_dataset('/raw', data=raw_src[:])
                
                # Copier tous les attributs du dataset
                for key, value in raw_src.attrs.items():
                    raw_dst.attrs[key] = value
                
                # Copier les attributs du fichier principal sauf sha256
                for key, value in src.attrs.items():
                    if key != 'sha256':
                        dst.attrs[key] = value
                        
            # Calculer le hash du fichier temporaire
            sha256_hash = hashlib.sha256()
            with open(temp_file, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
                    
            calculated_hash = sha256_hash.hexdigest()
            
            # Nettoyer
            temp_file.unlink()
            
            return stored_hash == calculated_hash
            
        except Exception:
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
        return writer.write_acquisition_data(
            data=data,
            sampling_rate=sampling_rate,
            channel_names=channel_names,
            metadata=metadata
        )