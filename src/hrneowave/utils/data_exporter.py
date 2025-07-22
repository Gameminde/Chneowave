# -*- coding: utf-8 -*-
"""
Module pour l'exportation des données.
"""

import h5py
import numpy as np
import hashlib
import json
import os

def export_to_hdf5(file_path: str, data: np.ndarray, metadata: dict):
    """Exporte les données et les métadonnées vers un fichier HDF5.

    Args:
        file_path (str): Le chemin du fichier HDF5 à créer.
        data (np.ndarray): Les données à sauvegarder.
        metadata (dict): Les métadonnées à sauvegarder.
    """
    with h5py.File(file_path, 'w') as f:
        f.create_dataset('data', data=data)
        for key, value in metadata.items():
            f.attrs[key] = json.dumps(value)

def calculate_sha256(file_path: str) -> str:
    """Calcule le checksum SHA-256 d'un fichier.

    Args:
        file_path (str): Le chemin du fichier.

    Returns:
        str: Le checksum SHA-256 en hexadécimal.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_metadata_file(hdf5_file_path: str, metadata: dict):
    """Crée un fichier de métadonnées JSON avec le checksum du fichier HDF5.

    Args:
        hdf5_file_path (str): Le chemin du fichier HDF5.
        metadata (dict): Les métadonnées à inclure.
    """
    checksum = calculate_sha256(hdf5_file_path)
    metadata_with_checksum = {
        'checksum_sha256': checksum,
        'original_metadata': metadata
    }
    
    metadata_file_path = os.path.splitext(hdf5_file_path)[0] + '.json'
    with open(metadata_file_path, 'w') as f:
        json.dump(metadata_with_checksum, f, indent=4)