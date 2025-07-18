"""Module d'optimisation FFT avec pyFFTW pour CHNeoWave

Ce module remplace les appels numpy.fft basiques par une implémentation
optimisée utilisant pyFFTW avec planification et cache.

Gains de performance attendus: +80% sur signaux longs (>1024 points)
"""

import numpy as np
import logging
import os
import threading
from typing import Optional, Tuple, Dict, Any, Union
from functools import lru_cache
import time

try:
    import pyfftw
    PYFFTW_AVAILABLE = True
except ImportError:
    PYFFTW_AVAILABLE = False
    pyfftw = None

# Configuration par défaut
FS = int(os.getenv("CHNW_FS", 500))  # défaut 500 Hz, override via env


class OptimizedFFTProcessor:
    """Processeur FFT optimisé avec cache et planification FFTW"""
    
    def __init__(self, enable_wisdom: bool = True, threads: Optional[int] = None):
        """
        Initialise le processeur FFT optimisé
        
        Args:
            enable_wisdom: Active la sauvegarde/chargement des plans FFTW
            threads: Nombre de threads (None = auto-détection)
        """
        if not PYFFTW_AVAILABLE:
            logging.warning("pyFFTW non disponible, utilisation de numpy.fft")
            self.use_numpy_fallback = True
            return
            
        self.use_numpy_fallback = False
        self.enable_wisdom = enable_wisdom
        self.threads = threads or pyfftw.config.NUM_THREADS
        self._plans_cache: Dict[Tuple[int, str], Any] = {}
        self._lock = threading.Lock()
        
        # Configuration globale pyFFTW
        pyfftw.config.NUM_THREADS = self.threads
        pyfftw.config.PLANNER_EFFORT = 'FFTW_MEASURE'
        
        if self.enable_wisdom:
            self._load_wisdom()
    
    def _load_wisdom(self) -> None:
        """Charge la sagesse FFTW depuis le disque si disponible"""
        if self.use_numpy_fallback:
            return
        try:
            with open('.fftw_wisdom', 'rb') as f:
                wisdom = f.read()
                pyfftw.import_wisdom(wisdom)
        except (FileNotFoundError, Exception):
            # Pas de fichier de sagesse ou erreur de lecture
            pass
    
    def _save_wisdom(self) -> None:
        """Sauvegarde la sagesse FFTW sur disque"""
        if self.use_numpy_fallback or not self.enable_wisdom:
            return
        try:
            wisdom = pyfftw.export_wisdom()
            with open('.fftw_wisdom', 'wb') as f:
                f.write(wisdom)
        except Exception:
            # Erreur de sauvegarde, continuer silencieusement
            pass
    
    @lru_cache(maxsize=32)
    def _get_plan_key(self, length: int, transform_type: str) -> Tuple[int, str]:
        """Génère une clé de cache pour les plans FFT"""
        return (length, transform_type)
    
    def _get_or_create_plan(self, signal_length: int, transform_type: str = 'fft') -> Any:
        """Récupère ou crée un plan FFT avec cache thread-safe"""
        if self.use_numpy_fallback:
            return None  # Pas de plan nécessaire pour numpy
            
        plan_key = self._get_plan_key(signal_length, transform_type)
        
        with self._lock:
            if plan_key not in self._plans_cache:
                # Créer les arrays alignés pour de meilleures performances
                input_array = pyfftw.empty_aligned(signal_length, dtype='complex128')
                output_array = pyfftw.empty_aligned(signal_length, dtype='complex128')
                
                if transform_type == 'fft':
                    plan = pyfftw.FFTW(
                        input_array, output_array,
                        direction='FFTW_FORWARD',
                        flags=('FFTW_MEASURE',),
                        threads=self.threads
                    )
                elif transform_type == 'ifft':
                    plan = pyfftw.FFTW(
                        input_array, output_array,
                        direction='FFTW_BACKWARD',
                        flags=('FFTW_MEASURE',),
                        threads=self.threads
                    )
                else:
                    raise ValueError(f"Type de transformation non supporté: {transform_type}")
                
                self._plans_cache[plan_key] = plan
                
                # Sauvegarder la sagesse après création d'un nouveau plan
                self._save_wisdom()
            
            return self._plans_cache[plan_key]
    
    def compute_fft(self, signal: np.ndarray, normalize: bool = False) -> np.ndarray:
        """
        Calcule la FFT optimisée d'un signal
        
        Args:
            signal: Signal d'entrée (réel ou complexe)
            normalize: Normalise le résultat par la longueur
            
        Returns:
            Transformée de Fourier du signal
        """
        signal = np.asarray(signal, dtype=np.complex128)
        
        if self.use_numpy_fallback:
            result = np.fft.fft(signal)
            if normalize:
                result /= len(signal)
            return result
            
        plan = self._get_or_create_plan(len(signal), 'fft')
        
        # Copier le signal dans l'array d'entrée du plan
        plan.input_array[:] = signal
        
        # Exécuter la FFT
        plan.execute()
        
        result = plan.output_array.copy()
        
        if normalize:
            result /= len(signal)
            
        return result
    
    def compute_ifft(self, spectrum: np.ndarray, normalize: bool = True) -> np.ndarray:
        """
        Calcule la FFT inverse optimisée
        
        Args:
            spectrum: Spectre d'entrée
            normalize: Normalise le résultat par la longueur
            
        Returns:
            Signal temporel reconstruit
        """
        spectrum = np.asarray(spectrum, dtype=np.complex128)
        
        if self.use_numpy_fallback:
            result = np.fft.ifft(spectrum)
            if not normalize:
                result *= len(spectrum)
            return result
            
        plan = self._get_or_create_plan(len(spectrum), 'ifft')
        
        plan.input_array[:] = spectrum
        plan.execute()
        
        result = plan.output_array.copy()
        
        if normalize:
            result /= len(spectrum)
            
        return result
    
    def compute_power_spectrum(self, signal: np.ndarray, 
                             sampling_freq: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcule le spectre de puissance optimisé
        
        Args:
            signal: Signal temporel
            sampling_freq: Fréquence d'échantillonnage
            
        Returns:
            Tuple (fréquences, densité spectrale de puissance)
        """
        N = len(signal)
        fft_result = self.compute_fft(signal)
        
        # Calcul des fréquences
        freqs = np.fft.fftfreq(N, 1/sampling_freq)[:N//2]
        
        # Densité spectrale de puissance (unilatérale)
        power_spectrum = np.abs(fft_result[:N//2])**2
        power_spectrum[1:-1] *= 2  # Facteur 2 pour spectre unilatéral
        power_spectrum /= (sampling_freq * N)  # Normalisation
        
        return freqs, power_spectrum
    
    def clear_cache(self) -> None:
        """Vide le cache des plans FFT"""
        if self.use_numpy_fallback:
            return
        with self._lock:
            self._plans_cache.clear()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Retourne des informations sur le cache"""
        if self.use_numpy_fallback:
            return {
                'cached_plans': 0,
                'threads': 1,
                'wisdom_enabled': False,
                'using_numpy_fallback': True
            }
        with self._lock:
            return {
                'cached_plans': len(self._plans_cache),
                'threads': self.threads,
                'wisdom_enabled': self.enable_wisdom,
                'using_numpy_fallback': False
            }
    
    def __del__(self):
        """Sauvegarde la sagesse à la destruction de l'objet"""
        if hasattr(self, 'use_numpy_fallback') and not self.use_numpy_fallback:
            self._save_wisdom()


# Fonction de compatibilité pour remplacer np.fft.fft
_global_processor = None

def get_global_processor() -> OptimizedFFTProcessor:
    """Retourne l'instance globale du processeur FFT"""
    global _global_processor
    if _global_processor is None:
        _global_processor = OptimizedFFTProcessor()
    return _global_processor


def optimized_fft(signal: np.ndarray, **kwargs) -> np.ndarray:
    """Fonction de remplacement drop-in pour np.fft.fft"""
    processor = get_global_processor()
    return processor.compute_fft(signal, **kwargs)


def optimized_ifft(spectrum: np.ndarray, **kwargs) -> np.ndarray:
    """Fonction de remplacement drop-in pour np.fft.ifft"""
    processor = get_global_processor()
    return processor.compute_ifft(spectrum, **kwargs)


# Exemple d'utilisation pour migration
if __name__ == "__main__":
    import time
    
    # Test de performance
    signal_length = 8192
    test_signal = np.random.randn(signal_length) + 1j * np.random.randn(signal_length)
    
    # Test numpy standard
    start_time = time.time()
    for _ in range(100):
        result_numpy = np.fft.fft(test_signal)
    numpy_time = time.time() - start_time
    
    # Test optimisé
    processor = OptimizedFFTProcessor()
    start_time = time.time()
    for _ in range(100):
        result_optimized = processor.compute_fft(test_signal)
    optimized_time = time.time() - start_time
    
    print(f"Temps numpy: {numpy_time:.4f}s")
    print(f"Temps optimisé: {optimized_time:.4f}s")
    print(f"Accélération: {numpy_time/optimized_time:.2f}x")
    print(f"Erreur max: {np.max(np.abs(result_numpy - result_optimized)):.2e}")
    
    print(f"\nInfo cache: {processor.get_cache_info()}")