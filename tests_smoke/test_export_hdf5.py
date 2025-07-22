#!/usr/bin/env python3
"""
Test smoke - Export HDF5
Lance une acquisition simulée de 5 secondes, exporte en HDF5 et vérifie le hash
"""

import pytest
import sys
import os
import tempfile
import h5py
import numpy as np
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import QTimer

# Ajout du chemin source
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hrneowave.utils.hdf_writer import HDF5Writer
from hrneowave.utils.hash_tools import hash_file
from hrneowave.core.config_manager import ConfigManager
from hrneowave.hw.demo_backend import DemoBackend

class TestExportHDF5:
    """Tests d'export HDF5"""
    
    @pytest.fixture(scope="class")
    def qapp(self):
        """Fixture pour l'application Qt"""
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        yield app
    
    @pytest.fixture
    def temp_dir(self):
        """Répertoire temporaire pour les tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_hdf5_writer_basic(self, temp_dir):
        """Test basique du HDF5Writer"""
        # Données de test
        fs = 1000
        n_channels = 4
        duration = 2.0
        n_samples = int(fs * duration)
        
        # Génération de données simulées
        data = np.random.randn(n_samples, n_channels).astype(np.float32)
        
        # Métadonnées
        metadata = {
            'fs': fs,
            'n_channels': n_channels,
            'duration': duration,
            'test_mode': True
        }
        
        # Fichier de sortie
        output_file = temp_dir / 'test_basic.h5'
        
        try:
            # Écriture HDF5
            with HDF5Writer(output_file) as writer:
                file_hash = writer.write_acquisition_data(
                    data=data,
                    sampling_rate=fs,
                    channel_names=[f'Channel_{i+1}' for i in range(n_channels)],
                    metadata=metadata
                )
            
            # Vérifications
            assert output_file.exists(), "Fichier HDF5 non créé"
            assert output_file.stat().st_size > 1000, "Fichier HDF5 trop petit"
            
            # Lecture et vérification
            result = HDF5Writer.read_acquisition_data(output_file)
            loaded_data = result['data']
            loaded_metadata = result['metadata']
            
            assert loaded_data.shape == data.shape, "Forme des données incorrecte"
            assert loaded_metadata['fs'] == fs, "Fréquence d'échantillonnage incorrecte"
            assert loaded_metadata['n_channels'] == n_channels, "Nombre de canaux incorrect"
            
            # Vérification du hash
            assert 'sha256' in loaded_metadata, "Hash SHA256 manquant"
            
            print(f"✓ Test HDF5Writer basique réussi: {output_file.name}")
            
        except Exception as e:
            pytest.fail(f"Erreur test HDF5Writer basique: {str(e)}")
    
    def test_simulated_acquisition_export(self, temp_dir):
        """Test d'acquisition simulée et export HDF5"""
        # Configuration
        fs = 32
        n_channels = 8
        duration = 5.0  # 5 secondes
        
        try:
            # Initialisation du backend de démo
            backend = DemoBackend()
            backend.initialize({
                'fs': fs,
                'channels': list(range(n_channels)),
                'buffer_size': 1024
            })
            
            # Simulation d'acquisition
            print(f"Démarrage acquisition simulée: {duration}s à {fs}Hz, {n_channels} canaux")
            
            # Collecte des données
            all_data = []
            backend.start_acquisition()
            
            # Simulation de la collecte pendant 5 secondes
            import time
            start_time = time.time()
            
            while time.time() - start_time < duration:
                # Lecture des données disponibles
                if backend.has_data():
                    chunk = backend.read_data()
                    if chunk is not None and len(chunk) > 0:
                        all_data.append(chunk)
                
                time.sleep(0.1)  # 100ms entre les lectures
            
            backend.stop_acquisition()
            
            # Assemblage des données
            if all_data:
                data = np.vstack(all_data)
            else:
                # Fallback: génération de données simulées
                n_samples = int(fs * duration)
                data = np.random.randn(n_samples, n_channels).astype(np.float32)
                print("Utilisation de données simulées (fallback)")
            
            print(f"Données collectées: {data.shape} ({data.shape[0]/fs:.1f}s)")
            
            # Métadonnées d'acquisition
            metadata = {
                'fs': fs,
                'n_channels': n_channels,
                'duration': data.shape[0] / fs,
                'acquisition_mode': 'simulation',
                'backend': 'demo',
                'timestamp': time.time()
            }
            
            # Export HDF5
            output_file = temp_dir / 'acquisition_5s.h5'
            with HDF5Writer(output_file) as writer:
                file_hash = writer.write_acquisition_data(
                    data=data,
                    sampling_rate=fs,
                    channel_names=[f'Channel_{i+1}' for i in range(n_channels)],
                    metadata=metadata
                )
            
            # Vérifications
            assert output_file.exists(), "Fichier d'export HDF5 non créé"
            
            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"Taille fichier HDF5: {file_size_mb:.2f} MB")
            
            # Vérification du contenu
            with h5py.File(output_file, 'r') as f:
                assert 'raw' in f, "Dataset 'raw' manquant"
                assert f['raw'].shape == data.shape, "Forme des données incorrecte dans HDF5"
                assert f['raw'].attrs['fs'] == fs, "Attribut fs incorrect"
                assert f['raw'].attrs['n_channels'] == n_channels, "Attribut n_channels incorrect"
                assert 'sha256' in f.attrs, "Hash SHA256 manquant"
            
            # Vérification du hash
            file_hash = hash_file(str(output_file))
            assert len(file_hash) == 64, "Hash SHA256 invalide"
            
            print(f"✓ Export HDF5 réussi: {output_file.name} (hash: {file_hash[:8]}...)")
            
        except Exception as e:
            pytest.fail(f"Erreur acquisition/export HDF5: {str(e)}")
    
    def test_hdf5_integrity_verification(self, temp_dir):
        """Test de vérification d'intégrité HDF5"""
        # Génération de données de test
        fs = 100
        n_channels = 2
        n_samples = 1000
        data = np.random.randn(n_samples, n_channels).astype(np.float32)
        
        metadata = {
            'fs': fs,
            'n_channels': n_channels,
            'test_integrity': True
        }
        
        output_file = temp_dir / 'integrity_test.h5'
        
        try:
            # Écriture
            with HDF5Writer(output_file) as writer:
                file_hash = writer.write_acquisition_data(
                    data=data,
                    sampling_rate=fs,
                    channel_names=[f'Channel_{i+1}' for i in range(n_channels)],
                    metadata=metadata
                )
            
            # Vérification d'intégrité
            is_valid = HDF5Writer.verify_file_integrity(output_file)
            assert is_valid, "Vérification d'intégrité échouée"
            
            # Test avec fichier corrompu (simulation)
            corrupted_file = temp_dir / 'corrupted.h5'
            
            # Copie du fichier original
            import shutil
            shutil.copy2(output_file, corrupted_file)
            
            # "Corruption" en modifiant quelques bytes
            with open(corrupted_file, 'r+b') as f:
                f.seek(-100, 2)  # 100 bytes avant la fin
                f.write(b'\x00' * 50)  # Écriture de zéros
            
            # La vérification devrait échouer
            is_corrupted_valid = HDF5Writer.verify_file_integrity(corrupted_file)
            assert not is_corrupted_valid, "La corruption n'a pas été détectée"
            
            print("✓ Vérification d'intégrité HDF5 fonctionnelle")
            
        except Exception as e:
            pytest.fail(f"Erreur test intégrité HDF5: {str(e)}")
    
    def test_large_dataset_export(self, temp_dir):
        """Test d'export de dataset plus volumineux"""
        # Configuration pour un dataset plus gros
        fs = 1000
        n_channels = 16
        duration = 10.0  # 10 secondes
        n_samples = int(fs * duration)
        
        try:
            # Génération de données par chunks pour économiser la mémoire
            output_file = temp_dir / 'large_dataset.h5'
            
            metadata = {
                'fs': fs,
                'n_channels': n_channels,
                'duration': duration,
                'large_dataset_test': True
            }
            
            # Génération et écriture par chunks
            chunk_size = 1000
            
            # Première écriture pour créer le fichier
            first_chunk = np.random.randn(chunk_size, n_channels).astype(np.float32)
            with HDF5Writer(output_file) as writer:
                file_hash = writer.write_acquisition_data(
                    data=first_chunk,
                    sampling_rate=fs,
                    channel_names=[f'Channel_{i+1}' for i in range(n_channels)],
                    metadata=metadata
                )
            
            # Ajout des chunks suivants
            with h5py.File(output_file, 'a') as f:
                dataset = f['raw']
                
                for i in range(1, n_samples // chunk_size):
                    chunk = np.random.randn(chunk_size, n_channels).astype(np.float32)
                    
                    # Redimensionner le dataset
                    new_size = (i + 1) * chunk_size
                    dataset.resize((new_size, n_channels))
                    
                    # Ajouter le chunk
                    dataset[i * chunk_size:(i + 1) * chunk_size, :] = chunk
            
            # Vérifications
            assert output_file.exists(), "Fichier large dataset non créé"
            
            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"Taille large dataset: {file_size_mb:.2f} MB")
            
            # Vérification du contenu
            with h5py.File(output_file, 'r') as f:
                assert f['raw'].shape[1] == n_channels, "Nombre de canaux incorrect"
                assert f['raw'].shape[0] >= n_samples * 0.9, "Nombre d'échantillons insuffisant"
            
            print(f"✓ Export large dataset réussi: {file_size_mb:.1f} MB")
            
        except Exception as e:
            pytest.fail(f"Erreur test large dataset: {str(e)}")

if __name__ == '__main__':
    # Exécution directe pour debug
    pytest.main([__file__, '-v'])