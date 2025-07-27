# post_processor.py - Module de post-traitement pour l'analyse des données de houle
import os
import json
import numpy as np
from typing import Dict, List, Optional, Tuple

# Variables globales pour les imports Qt conditionnels
QObject = None
Signal = None

def _ensure_qt_imports():
    """Importe les modules Qt de manière conditionnelle"""
    global QObject, Signal
    
    if QObject is None:
        try:
            from PySide6.QtCore import QObject, Signal
        except ImportError:
            # Mode non-GUI, on utilise des mocks
            QObject = object
            class MockSignal:
                def emit(self, *args, **kwargs):
                    pass
            Signal = MockSignal

_ensure_qt_imports()

class PostProcessor(QObject):
    """Contrôleur pour le post-traitement et l'analyse des données de houle
    
    Ce module gère :
    - Chargement des données exportées
    - Calculs statistiques avancés
    - Analyse spectrale (FFT)
    - Métriques Goda
    - Export des résultats
    """
    
    # Signaux pour communication avec l'interface
    dataLoaded = Signal(dict)  # Données chargées
    analysisCompleted = Signal(dict)  # Analyse terminée
    exportCompleted = Signal(str)  # Export terminé
    errorOccurred = Signal(str)  # Erreur
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__()
        
        # Configuration
        self.config = self._load_config(config_path)
        
        # État
        self.current_data = None
        self.current_analysis = None
        self.sample_rate = 32.0  # Hz par défaut
        
        print("PostProcessor initialisé")
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Charge la configuration"""
        default_config = {
            'analysis': {
                'window_size': 1024,
                'overlap': 0.5,
                'detrend': True,
                'apply_window': True
            },
            'goda': {
                'significant_wave_height': True,
                'peak_period': True,
                'mean_period': True,
                'spectral_moments': True
            },
            'export': {
                'formats': ['csv', 'json', 'hdf5'],
                'precision': 6
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Erreur chargement config: {e}")
                
        return default_config
        
    def load_data_file(self, file_path: str) -> bool:
        """Charge un fichier de données
        
        Args:
            file_path: Chemin vers le fichier de données
            
        Returns:
            True si succès, False sinon
        """
        try:
            if not os.path.exists(file_path):
                self.errorOccurred.emit(f"Fichier introuvable: {file_path}")
                return False
                
            # Déterminer le format du fichier
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.csv':
                data = self._load_csv(file_path)
            elif ext == '.json':
                data = self._load_json(file_path)
            elif ext in ['.h5', '.hdf5']:
                data = self._load_hdf5(file_path)
            else:
                self.errorOccurred.emit(f"Format non supporté: {ext}")
                return False
                
            self.current_data = data
            self.dataLoaded.emit(data)
            
            print(f"Données chargées: {file_path}")
            return True
            
        except Exception as e:
            error_msg = f"Erreur chargement données: {e}"
            print(f"❌ {error_msg}")
            self.errorOccurred.emit(error_msg)
            return False
            
    def _load_csv(self, file_path: str) -> Dict:
        """Charge un fichier CSV"""
        import pandas as pd
        
        df = pd.read_csv(file_path)
        
        # Extraire les métadonnées du header si présentes
        metadata = {}
        if 'sample_rate' in df.columns:
            self.sample_rate = float(df['sample_rate'].iloc[0])
            metadata['sample_rate'] = self.sample_rate
            
        # Extraire les données temporelles
        time_cols = [col for col in df.columns if 'time' in col.lower()]
        data_cols = [col for col in df.columns if col.startswith('channel_') or col.startswith('probe_')]
        
        data = {
            'metadata': metadata,
            'time': df[time_cols[0]].values if time_cols else np.arange(len(df)) / self.sample_rate,
            'channels': {}
        }
        
        for col in data_cols:
            data['channels'][col] = df[col].values
            
        return data
        
    def _load_json(self, file_path: str) -> Dict:
        """Charge un fichier JSON"""
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Convertir les listes en arrays numpy
        if 'channels' in data:
            for channel, values in data['channels'].items():
                data['channels'][channel] = np.array(values)
                
        if 'time' in data:
            data['time'] = np.array(data['time'])
            
        if 'metadata' in data and 'sample_rate' in data['metadata']:
            self.sample_rate = float(data['metadata']['sample_rate'])
            
        return data
        
    def _load_hdf5(self, file_path: str) -> Dict:
        """Charge un fichier HDF5"""
        try:
            import h5py
        except ImportError:
            raise ImportError("h5py requis pour les fichiers HDF5")
            
        data = {'channels': {}, 'metadata': {}}
        
        with h5py.File(file_path, 'r') as f:
            # Charger les métadonnées
            if 'metadata' in f.attrs:
                data['metadata'] = dict(f.attrs)
                
            # Charger les données temporelles
            if 'time' in f:
                data['time'] = f['time'][:]
                
            # Charger les canaux
            for key in f.keys():
                if key.startswith('channel_') or key.startswith('probe_'):
                    data['channels'][key] = f[key][:]
                    
        if 'sample_rate' in data['metadata']:
            self.sample_rate = float(data['metadata']['sample_rate'])
            
        return data
        
    def run_analysis(self) -> bool:
        """Lance l'analyse complète des données
        
        Returns:
            True si succès, False sinon
        """
        if self.current_data is None:
            self.errorOccurred.emit("Aucune donnée chargée")
            return False
            
        try:
            analysis_results = {
                'basic_stats': self._compute_basic_stats(),
                'spectral_analysis': self._compute_spectral_analysis(),
                'goda_metrics': self._compute_goda_metrics(),
                'timestamp': np.datetime64('now').astype(str)
            }
            
            self.current_analysis = analysis_results
            self.analysisCompleted.emit(analysis_results)
            
            print("Analyse terminée")
            return True
            
        except Exception as e:
            error_msg = f"Erreur analyse: {e}"
            print(f"❌ {error_msg}")
            self.errorOccurred.emit(error_msg)
            return False
            
    def _compute_basic_stats(self) -> Dict:
        """Calcule les statistiques de base"""
        stats = {}
        
        for channel, data in self.current_data['channels'].items():
            stats[channel] = {
                'mean': float(np.mean(data)),
                'std': float(np.std(data)),
                'min': float(np.min(data)),
                'max': float(np.max(data)),
                'rms': float(np.sqrt(np.mean(data**2))),
                'skewness': float(self._compute_skewness(data)),
                'kurtosis': float(self._compute_kurtosis(data))
            }
            
        return stats
        
    def _compute_spectral_analysis(self) -> Dict:
        """Calcule l'analyse spectrale (FFT)"""
        spectral_results = {}
        
        for channel, data in self.current_data['channels'].items():
            # Calcul FFT
            n_fft = self.config['analysis']['window_size']
            freqs = np.fft.fftfreq(n_fft, 1/self.sample_rate)[:n_fft//2]
            
            # Appliquer fenêtrage si configuré
            if self.config['analysis']['apply_window']:
                window = np.hanning(len(data))
                windowed_data = data * window
            else:
                windowed_data = data
                
            # Calcul du spectre de puissance
            fft_data = np.fft.fft(windowed_data, n_fft)
            power_spectrum = np.abs(fft_data[:n_fft//2])**2
            
            spectral_results[channel] = {
                'frequencies': freqs.tolist(),
                'power_spectrum': power_spectrum.tolist(),
                'peak_frequency': float(freqs[np.argmax(power_spectrum)]),
                'total_energy': float(np.sum(power_spectrum))
            }
            
        return spectral_results
        
    def _compute_goda_metrics(self) -> Dict:
        """Calcule les métriques Goda pour l'analyse de houle"""
        goda_results = {}
        
        for channel, data in self.current_data['channels'].items():
            # Calcul des hauteurs de vagues (méthode zero-crossing)
            wave_heights = self._extract_wave_heights(data)
            
            if len(wave_heights) > 0:
                # Trier par ordre décroissant
                sorted_heights = np.sort(wave_heights)[::-1]
                n_waves = len(sorted_heights)
                
                # Métriques Goda
                goda_results[channel] = {
                    'Hs': float(np.mean(sorted_heights[:max(1, n_waves//3)])),  # H1/3
                    'H_max': float(np.max(sorted_heights)),
                    'H_mean': float(np.mean(sorted_heights)),
                    'H_rms': float(np.sqrt(np.mean(sorted_heights**2))),
                    'n_waves': int(n_waves),
                    'Tp': self._compute_peak_period(data),
                    'Tm': self._compute_mean_period(data)
                }
            else:
                goda_results[channel] = {
                    'Hs': 0.0, 'H_max': 0.0, 'H_mean': 0.0,
                    'H_rms': 0.0, 'n_waves': 0, 'Tp': 0.0, 'Tm': 0.0
                }
                
        return goda_results
        
    def _extract_wave_heights(self, data: np.ndarray) -> np.ndarray:
        """Extrait les hauteurs de vagues par méthode zero-crossing"""
        # Détecter les passages par zéro
        zero_crossings = np.where(np.diff(np.sign(data)))[0]
        
        wave_heights = []
        for i in range(0, len(zero_crossings)-1, 2):
            if i+1 < len(zero_crossings):
                start_idx = zero_crossings[i]
                end_idx = zero_crossings[i+1]
                wave_segment = data[start_idx:end_idx]
                
                if len(wave_segment) > 0:
                    height = np.max(wave_segment) - np.min(wave_segment)
                    wave_heights.append(height)
                    
        return np.array(wave_heights)
        
    def _compute_peak_period(self, data: np.ndarray) -> float:
        """Calcule la période de pic"""
        # Analyse spectrale pour trouver la fréquence de pic
        freqs = np.fft.fftfreq(len(data), 1/self.sample_rate)
        fft_data = np.fft.fft(data)
        power_spectrum = np.abs(fft_data)**2
        
        # Trouver la fréquence de pic (en excluant DC)
        valid_indices = freqs > 0
        if np.any(valid_indices):
            peak_freq = freqs[valid_indices][np.argmax(power_spectrum[valid_indices])]
            return 1.0 / peak_freq if peak_freq > 0 else 0.0
        return 0.0
        
    def _compute_mean_period(self, data: np.ndarray) -> float:
        """Calcule la période moyenne"""
        # Détecter les passages par zéro pour estimer la période
        zero_crossings = np.where(np.diff(np.sign(data)))[0]
        
        if len(zero_crossings) > 1:
            periods = np.diff(zero_crossings) / self.sample_rate * 2  # *2 car demi-période
            return float(np.mean(periods))
        return 0.0
        
    def _compute_skewness(self, data: np.ndarray) -> float:
        """Calcule l'asymétrie (skewness)"""
        mean = np.mean(data)
        std = np.std(data)
        if std > 0:
            return np.mean(((data - mean) / std) ** 3)
        return 0.0
        
    def _compute_kurtosis(self, data: np.ndarray) -> float:
        """Calcule l'aplatissement (kurtosis)"""
        mean = np.mean(data)
        std = np.std(data)
        if std > 0:
            return np.mean(((data - mean) / std) ** 4) - 3.0  # Excès de kurtosis
        return 0.0
        
    def export_results(self, output_path: str, format_type: str = 'csv') -> bool:
        """Exporte les résultats d'analyse
        
        Args:
            output_path: Chemin de sortie
            format_type: Format d'export ('csv', 'json', 'hdf5')
            
        Returns:
            True si succès, False sinon
        """
        if self.current_analysis is None:
            self.errorOccurred.emit("Aucune analyse à exporter")
            return False
            
        try:
            if format_type == 'csv':
                self._export_csv(output_path)
            elif format_type == 'json':
                self._export_json(output_path)
            elif format_type == 'hdf5':
                self._export_hdf5(output_path)
            else:
                raise ValueError(f"Format non supporté: {format_type}")
                
            self.exportCompleted.emit(output_path)
            print(f"Export terminé: {output_path}")
            return True
            
        except Exception as e:
            error_msg = f"Erreur export: {e}"
            print(f"❌ {error_msg}")
            self.errorOccurred.emit(error_msg)
            return False
            
    def _export_csv(self, output_path: str):
        """Exporte en format CSV"""
        import pandas as pd
        
        # Préparer les données pour DataFrame
        export_data = []
        
        # Ajouter les statistiques de base
        for channel, stats in self.current_analysis['basic_stats'].items():
            for metric, value in stats.items():
                export_data.append({
                    'channel': channel,
                    'category': 'basic_stats',
                    'metric': metric,
                    'value': value
                })
                
        # Ajouter les métriques Goda
        for channel, goda in self.current_analysis['goda_metrics'].items():
            for metric, value in goda.items():
                export_data.append({
                    'channel': channel,
                    'category': 'goda_metrics',
                    'metric': metric,
                    'value': value
                })
                
        df = pd.DataFrame(export_data)
        df.to_csv(output_path, index=False)
        
    def _export_json(self, output_path: str):
        """Exporte en format JSON"""
        # Convertir les arrays numpy en listes pour la sérialisation JSON
        export_data = self._prepare_json_data(self.current_analysis)
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
            
    def _export_hdf5(self, output_path: str):
        """Exporte en format HDF5"""
        try:
            import h5py
        except ImportError:
            raise ImportError("h5py requis pour l'export HDF5")
            
        with h5py.File(output_path, 'w') as f:
            # Sauvegarder les métadonnées
            f.attrs['timestamp'] = self.current_analysis['timestamp']
            f.attrs['sample_rate'] = self.sample_rate
            
            # Sauvegarder les statistiques de base
            stats_group = f.create_group('basic_stats')
            for channel, stats in self.current_analysis['basic_stats'].items():
                channel_group = stats_group.create_group(channel)
                for metric, value in stats.items():
                    channel_group.attrs[metric] = value
                    
            # Sauvegarder les métriques Goda
            goda_group = f.create_group('goda_metrics')
            for channel, goda in self.current_analysis['goda_metrics'].items():
                channel_group = goda_group.create_group(channel)
                for metric, value in goda.items():
                    channel_group.attrs[metric] = value
                    
    def _prepare_json_data(self, data):
        """Prépare les données pour la sérialisation JSON"""
        if isinstance(data, dict):
            return {k: self._prepare_json_data(v) for k, v in data.items()}
        elif isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, (np.integer, np.floating)):
            return float(data)
        else:
            return data
            
    def get_analysis_summary(self) -> Optional[Dict]:
        """Retourne un résumé de l'analyse actuelle"""
        if self.current_analysis is None:
            return None
            
        summary = {
            'timestamp': self.current_analysis['timestamp'],
            'channels_analyzed': list(self.current_analysis['basic_stats'].keys()),
            'sample_rate': self.sample_rate
        }
        
        # Ajouter les métriques principales
        if 'goda_metrics' in self.current_analysis:
            summary['goda_summary'] = {}
            for channel, goda in self.current_analysis['goda_metrics'].items():
                summary['goda_summary'][channel] = {
                    'Hs': goda.get('Hs', 0),
                    'H_max': goda.get('H_max', 0),
                    'Tp': goda.get('Tp', 0),
                    'n_waves': goda.get('n_waves', 0)
                }
                
        return summary