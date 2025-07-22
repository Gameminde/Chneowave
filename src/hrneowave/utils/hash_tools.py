#!/usr/bin/env python3
"""
Outils de hachage pour CHNeoWave
Fonctions de calcul et vérification de hash SHA-256
"""

import hashlib
from pathlib import Path
from typing import Union, Optional
import json

def hash_file(filepath: Union[str, Path]) -> str:
    """
    Calcule le hash SHA-256 d'un fichier
    
    Args:
        filepath: Chemin vers le fichier
        
    Returns:
        Hash SHA-256 en hexadécimal
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        IOError: En cas d'erreur de lecture
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Fichier non trouvé: {filepath}")
        
    sha256_hash = hashlib.sha256()
    
    try:
        with open(filepath, 'rb') as f:
            # Lire par chunks pour les gros fichiers
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
    except IOError as e:
        raise IOError(f"Erreur lecture fichier {filepath}: {e}")
        
    return sha256_hash.hexdigest()

def hash_string(text: str, encoding: str = 'utf-8') -> str:
    """
    Calcule le hash SHA-256 d'une chaîne de caractères
    
    Args:
        text: Texte à hasher
        encoding: Encodage du texte (défaut: utf-8)
        
    Returns:
        Hash SHA-256 en hexadécimal
    """
    return hashlib.sha256(text.encode(encoding)).hexdigest()

def hash_json(data: dict) -> str:
    """
    Calcule le hash SHA-256 d'un objet JSON
    Utilise un tri des clés pour assurer la reproductibilité
    
    Args:
        data: Dictionnaire à hasher
        
    Returns:
        Hash SHA-256 en hexadécimal
    """
    # Sérialiser avec tri des clés pour reproductibilité
    json_string = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hash_string(json_string)

def verify_file_hash(filepath: Union[str, Path], expected_hash: str) -> bool:
    """
    Vérifie l'intégrité d'un fichier via son hash SHA-256
    
    Args:
        filepath: Chemin vers le fichier
        expected_hash: Hash attendu
        
    Returns:
        True si le hash correspond
    """
    try:
        actual_hash = hash_file(filepath)
        return actual_hash.lower() == expected_hash.lower()
    except (FileNotFoundError, IOError):
        return False

def create_checksum_file(filepath: Union[str, Path], 
                        checksum_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Crée un fichier de checksum SHA-256 pour un fichier donné
    
    Args:
        filepath: Chemin vers le fichier source
        checksum_path: Chemin du fichier checksum (optionnel)
        
    Returns:
        Chemin du fichier checksum créé
    """
    filepath = Path(filepath)
    
    if checksum_path is None:
        checksum_path = filepath.with_suffix(filepath.suffix + '.sha256')
    else:
        checksum_path = Path(checksum_path)
        
    file_hash = hash_file(filepath)
    
    # Format standard: hash  filename
    checksum_content = f"{file_hash}  {filepath.name}\n"
    
    with open(checksum_path, 'w', encoding='utf-8') as f:
        f.write(checksum_content)
        
    return checksum_path

def verify_checksum_file(checksum_path: Union[str, Path], 
                        base_dir: Optional[Union[str, Path]] = None) -> bool:
    """
    Vérifie un fichier de checksum SHA-256
    
    Args:
        checksum_path: Chemin vers le fichier checksum
        base_dir: Répertoire de base pour les fichiers (optionnel)
        
    Returns:
        True si tous les checksums sont valides
    """
    checksum_path = Path(checksum_path)
    
    if base_dir is None:
        base_dir = checksum_path.parent
    else:
        base_dir = Path(base_dir)
        
    try:
        with open(checksum_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                # Format: hash  filename
                parts = line.split('  ', 1)
                if len(parts) != 2:
                    continue
                    
                expected_hash, filename = parts
                filepath = base_dir / filename
                
                if not verify_file_hash(filepath, expected_hash):
                    return False
                    
        return True
        
    except (FileNotFoundError, IOError):
        return False

class HashCalculator:
    """
    Calculateur de hash avec support de mise à jour incrémentale
    Utile pour les gros fichiers ou flux de données
    """
    
    def __init__(self):
        """Initialise le calculateur"""
        self.hasher = hashlib.sha256()
        self._finalized = False
        
    def update(self, data: Union[bytes, str]) -> None:
        """
        Met à jour le hash avec de nouvelles données
        
        Args:
            data: Données à ajouter (bytes ou str)
        """
        if self._finalized:
            raise RuntimeError("Hash déjà finalisé")
            
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        self.hasher.update(data)
        
    def finalize(self) -> str:
        """
        Finalise le calcul et retourne le hash
        
        Returns:
            Hash SHA-256 en hexadécimal
        """
        if self._finalized:
            raise RuntimeError("Hash déjà finalisé")
            
        self._finalized = True
        return self.hasher.hexdigest()
        
    def reset(self) -> None:
        """Remet à zéro le calculateur"""
        self.hasher = hashlib.sha256()
        self._finalized = False
        
    @property
    def is_finalized(self) -> bool:
        """Indique si le hash a été finalisé"""
        return self._finalized

def batch_hash_files(filepaths: list, 
                    progress_callback: Optional[callable] = None) -> dict:
    """
    Calcule les hash de plusieurs fichiers en lot
    
    Args:
        filepaths: Liste des chemins de fichiers
        progress_callback: Fonction de callback pour le progrès (optionnel)
        
    Returns:
        Dictionnaire {filepath: hash}
    """
    results = {}
    total = len(filepaths)
    
    for i, filepath in enumerate(filepaths):
        try:
            file_hash = hash_file(filepath)
            results[str(filepath)] = file_hash
        except (FileNotFoundError, IOError) as e:
            results[str(filepath)] = f"ERROR: {e}"
            
        if progress_callback:
            progress_callback(i + 1, total, filepath)
            
    return results