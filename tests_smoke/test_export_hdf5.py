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
import shutil
from pathlib import Path
from PySide6.QtWidgets import QApplication

# Ajout du chemin source
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hrneowave.utils.hdf_writer import HDF5Writer
from hrneowave.hardware.backends.demo import DemoBackend

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

    @pytest.fixture
    def setup_test_data(self):
        """Données de test communes"""
        fs = 1000
        n_channels = 4
        duration = 2.0
        n_samples = int(fs * duration)
        data = np.random.randn(n_samples, n_channels).astype(np.float32)
        channels = [f'Channel_{i+1}' for i in range(n_channels)]
        metadata = {'test_project': 'CHNeoWave'}
        return data, fs, channels, metadata

    def test_hdf5_writer_basic(self, temp_dir, setup_test_data):
        """Test basique du HDF5Writer"""
        data, fs, channels, metadata = setup_test_data
        output_file = temp_dir / 'test_basic.h5'

        with HDF5Writer(output_file) as writer:
            writer.write_acquisition_data(data, fs, channels, metadata)

        assert output_file.exists(), "Fichier HDF5 non créé"
        assert HDF5Writer.verify_file_integrity(output_file)

        result = HDF5Writer.read_acquisition_data(output_file)
        assert np.array_equal(result['data'], data)
        assert result['metadata']['fs'] == fs

    def test_simulated_acquisition_export(self, temp_dir):
        """Test d'acquisition simulée et export HDF5"""
        fs = 32
        n_channels = 8
        duration = 1.0
        backend = DemoBackend({'sample_rate': fs, 'channels': n_channels, 'num_samples': int(fs*duration)})
        backend.start()
        import time
        time.sleep(duration)
        data = backend.read()
        backend.stop()

        output_file = temp_dir / 'acquisition_sim.h5'
        channels = [f'Sim_{i+1}' for i in range(n_channels)]
        metadata = {'source': 'simulation'}

        with HDF5Writer(output_file) as writer:
            writer.write_acquisition_data(data, fs, channels, metadata)

        assert output_file.exists()
        assert HDF5Writer.verify_file_integrity(output_file)

    def test_hdf5_integrity_verification(self, temp_dir, setup_test_data):
        """Teste la logique de vérification d'intégrité."""
        data, fs, channels, metadata = setup_test_data
        valid_file = temp_dir / "valid.h5"

        with HDF5Writer(valid_file) as writer:
            writer.write_acquisition_data(data, fs, channels, metadata)

        # 1. Vérifier un fichier valide
        assert HDF5Writer.verify_file_integrity(valid_file)

        # 2. Vérifier un fichier corrompu (modifier une donnée)
        corrupted_file = temp_dir / "corrupted.h5"
        shutil.copy(valid_file, corrupted_file)
        with h5py.File(corrupted_file, 'a') as f:
            data = f['/raw']
            data[0, 0] = 9999.99 # Corrompre une valeur
        assert not HDF5Writer.verify_file_integrity(corrupted_file)

        # 3. Vérifier un fichier sans hash
        no_hash_file = temp_dir / "no_hash.h5"
        with h5py.File(valid_file, 'r') as src, h5py.File(no_hash_file, 'w') as dst:
            src.copy('/raw', dst)
            for attr_key, attr_val in src.attrs.items():
                if attr_key != 'sha256':
                    dst.attrs[attr_key] = attr_val
        assert not HDF5Writer.verify_file_integrity(no_hash_file)

    def test_large_dataset_export(self, temp_dir):
        """Test d'export de dataset volumineux."""
        fs = 1000
        n_channels = 16
        duration = 5.0
        n_samples = int(fs * duration)
        data = np.random.randn(n_samples, n_channels).astype(np.float32)
        output_file = temp_dir / 'large_dataset.h5'
        channels = [f'Lrg_{i+1}' for i in range(n_channels)]

        with HDF5Writer(output_file) as writer:
            writer.write_acquisition_data(data, fs, channels)

        assert output_file.exists()
        assert HDF5Writer.verify_file_integrity(output_file)
        file_size_mb = output_file.stat().st_size / (1024 * 1024)
        assert file_size_mb > 0.1 # Ajustement pour la compression

if __name__ == '__main__':
    pytest.main([__file__, '-v'])