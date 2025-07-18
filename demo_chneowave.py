#!/usr/bin/env python3
"""
Démonstration du logiciel CHNeoWave
Logiciel d'acquisition et d'analyse de données pour laboratoire d'étude maritime
Modèles réduits en Méditerranée - Bassins et canaux
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from hrneowave.core.optimized_fft_processor import OptimizedFFTProcessor
    from hrneowave.core.circular_buffer import CircularBuffer, BufferConfig
    from hrneowave.offline_guard import check_offline_mode
    print("✓ Modules CHNeoWave importés avec succès")
except ImportError as e:
    print(f"✗ Erreur d'importation: {e}")
    sys.exit(1)

def demo_acquisition_simulation():
    """Simulation d'acquisition de données de vagues"""
    print("\n=== Simulation d'acquisition de données de vagues ===")
    
    # Paramètres de simulation
    fs = 100  # Fréquence d'échantillonnage (Hz)
    duration = 10  # Durée (secondes)
    t = np.linspace(0, duration, int(fs * duration))
    
    # Simulation de vagues avec plusieurs composantes
    wave1 = 0.5 * np.sin(2 * np.pi * 0.5 * t)  # Vague principale 0.5 Hz
    wave2 = 0.3 * np.sin(2 * np.pi * 1.2 * t)  # Vague secondaire 1.2 Hz
    wave3 = 0.1 * np.sin(2 * np.pi * 2.5 * t)  # Vague haute fréquence 2.5 Hz
    noise = 0.05 * np.random.randn(len(t))     # Bruit
    
    signal = wave1 + wave2 + wave3 + noise
    
    print(f"Signal généré: {len(signal)} échantillons à {fs} Hz")
    print(f"Durée: {duration} secondes")
    
    return t, signal, fs

def demo_circular_buffer(signal):
    """Démonstration du buffer circulaire"""
    print("\n=== Test du buffer circulaire ===")
    
    buffer_size = 500
    config = BufferConfig(
        n_channels=1,
        buffer_size=buffer_size,
        sample_rate=100.0,
        dtype=np.float32
    )
    buffer = CircularBuffer(config)
    
    # Remplissage progressif par chunks
    chunk_size = 50
    for i in range(0, min(len(signal), buffer_size + 100), chunk_size):
        chunk = signal[i:i+chunk_size]
        if len(chunk) > 0:
            success = buffer.write(chunk.reshape(1, -1))
            if i % 100 == 0:
                print(f"Buffer: {buffer.available_samples()} échantillons")
            if not success:
                print("Buffer plein - arrêt du remplissage")
                break
    
    # Lecture des données
    available = buffer.available_samples()
    data = buffer.read(available)
    if data is not None:
        data = data.flatten()  # Convertir de (1, N) à (N,)
    else:
        data = np.array([])
    
    print(f"Buffer final: {len(data)} échantillons (max: {buffer_size})")
    
    return data

def demo_fft_analysis(signal, fs):
    """Démonstration de l'analyse FFT optimisée"""
    print("\n=== Analyse FFT optimisée ===")
    
    processor = OptimizedFFTProcessor()
    
    # Calcul de la FFT
    fft_result = processor.compute_fft(signal)
    freqs, power_spectrum = processor.compute_power_spectrum(signal, fs)
    
    print(f"FFT calculée: {len(fft_result)} points")
    print(f"Spectre de puissance: {len(power_spectrum)} points")
    
    # Informations sur le cache
    cache_info = processor.get_cache_info()
    print(f"Cache FFT: {cache_info}")
    
    return freqs, power_spectrum

def demo_visualization(t, signal, freqs, power_spectrum):
    """Visualisation des résultats"""
    print("\n=== Génération des graphiques ===")
    
    plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Signal temporel
    ax1.plot(t, signal, 'b-', linewidth=0.8, alpha=0.8)
    ax1.set_xlabel('Temps (s)')
    ax1.set_ylabel('Amplitude (m)')
    ax1.set_title('Signal de vagues simulé - CHNeoWave')
    ax1.grid(True, alpha=0.3)
    
    # Spectre de puissance
    ax2.semilogy(freqs, power_spectrum, 'r-', linewidth=1.2)
    ax2.set_xlabel('Fréquence (Hz)')
    ax2.set_ylabel('Densité spectrale de puissance')
    ax2.set_title('Analyse spectrale - Laboratoire maritime')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 5)  # Limiter à 5 Hz pour la clarté
    
    plt.tight_layout()
    
    # Sauvegarde
    output_file = 'demo_chneowave_results.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Graphiques sauvegardés: {output_file}")
    
    plt.show()

def demo_offline_mode():
    """Test du mode offline"""
    print("\n=== Test du mode offline ===")
    
    # Test du mode offline
    offline_status = check_offline_mode()
    print(f"Mode offline: {'Activé' if offline_status else 'Désactivé'}")
    
    if offline_status:
        print("✓ Fonctionnement en mode laboratoire sécurisé")
    else:
        print("ℹ Mode en ligne - Connexions réseau autorisées")

def main():
    """Fonction principale de démonstration"""
    print("="*60)
    print("    CHNeoWave - Logiciel d'étude maritime")
    print("    Laboratoire de modèles réduits")
    print("    Méditerranée - Bassins et canaux")
    print("="*60)
    
    try:
        # Test du mode offline
        demo_offline_mode()
        
        # Simulation d'acquisition
        t, signal, fs = demo_acquisition_simulation()
        
        # Test du buffer circulaire
        buffered_data = demo_circular_buffer(signal)
        
        # Analyse FFT
        freqs, power_spectrum = demo_fft_analysis(signal, fs)
        
        # Visualisation
        demo_visualization(t, signal, freqs, power_spectrum)
        
        print("\n" + "="*60)
        print("✓ Démonstration CHNeoWave terminée avec succès")
        print("✓ Tous les modules fonctionnent correctement")
        print("✓ Prêt pour l'acquisition de données réelles")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Erreur durant la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())