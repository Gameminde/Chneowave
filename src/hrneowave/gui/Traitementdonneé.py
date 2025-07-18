import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from scipy import signal
from scipy.signal import welch
from scipy.optimize import fsolve
from datetime import datetime
import os
import json
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QCheckBox, QPushButton, QTabWidget, QScrollArea, QGridLayout,
                            QTableWidget, QTableWidgetItem, QSplitter, QTextEdit, QFrame,
                            QFileDialog, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MultidimensionalWaveAnalyzer:
    """
    Analyseur multidimensionnel pour signaux de houle
    Implémentation FFT + Méthode de Goda + Moindres Carrés
    """

    def __init__(self, probe_positions, water_depth, sampling_freq, duration):
        """
        Initialisation de l'analyseur

        Args:
            probe_positions (list): Positions des sondes en mètres [x1, x2, ..., xn]
            water_depth (float): Profondeur d'eau en mètres
            sampling_freq (float): Fréquence d'échantillonnage en Hz
            duration (float): Durée d'acquisition en secondes
        """
        self.probe_positions = np.array(probe_positions)
        self.n_probes = len(probe_positions)
        self.water_depth = water_depth
        self.fs = sampling_freq
        self.duration = duration
        self.g = 9.81  # Accélération gravitationnelle

        # Résultats de l'analyse
        self.time_domain_results = {}
        self.frequency_domain_results = {}
        self.wave_separation_results = {}
        self.reflection_analysis = {}

        # Configuration de style pour les graphiques
        plt.style.use('dark_background')
        sns.set_palette("husl")

    def dispersion_relation(self, omega, k):
        """Relation de dispersion pour les ondes de gravité"""
        return omega**2 - self.g * k * np.tanh(k * self.water_depth)

    def solve_dispersion(self, omega):
        """Résolution de la relation de dispersion pour obtenir k"""
        k_guess = omega**2 / self.g  # Approximation eau profonde
        k = fsolve(self.dispersion_relation, k_guess, args=(omega,))[0]
        return max(k, 1e-10)  # Éviter k=0

    def preprocess_signals(self, raw_signals):
        """
        Prétraitement des signaux : détrend + centrage + filtrage

        Args:
            raw_signals (dict): {probe_name: signal_array}
        """
        processed_signals = {}
        self.time_array = np.linspace(0, self.duration, int(self.fs * self.duration))

        for probe_name, signal_data in raw_signals.items():
            # Suppression de la tendance
            detrended = signal.detrend(signal_data, type='linear')

            # Centrage par rapport au niveau moyen
            mean_level = np.mean(detrended)
            centered = detrended - mean_level

            # Filtrage passe-bas pour éliminer le bruit haute fréquence
            sos = signal.butter(4, 5, 'low', fs=self.fs, output='sos')
            filtered = signal.sosfilt(sos, centered)

            processed_signals[probe_name] = {
                'raw': signal_data,
                'processed': filtered,
                'mean_level': mean_level,
                'std': np.std(filtered),
                'max': np.max(filtered),
                'min': np.min(filtered)
            }

        return processed_signals

    def time_domain_analysis(self, processed_signals):
        """Analyse temporelle complète des signaux"""
        for probe_name, probe_data in processed_signals.items():
            signal_data = probe_data['processed']

            # Détection des vagues par zero-up-crossing
            zero_crossings = self._detect_zero_crossings(signal_data)
            wave_heights, wave_periods = self._extract_wave_characteristics(
                signal_data, zero_crossings
            )

            # Calcul des paramètres statistiques
            stats = self._calculate_wave_statistics(wave_heights, wave_periods)

            self.time_domain_results[probe_name] = {
                'wave_heights': wave_heights,
                'wave_periods': wave_periods,
                'statistics': stats,
                'zero_crossings': zero_crossings,
                'n_waves': len(wave_heights)
            }

    def _detect_zero_crossings(self, signal_data):
        """Détection des franchissements de zéro montants"""
        crossings = []
        for i in range(len(signal_data) - 1):
            if signal_data[i] <= 0 and signal_data[i + 1] > 0:
                # Interpolation linéaire pour plus de précision
                t_cross = i - signal_data[i] / (signal_data[i + 1] - signal_data[i])
                crossings.append(t_cross / self.fs)
        return np.array(crossings)

    def _extract_wave_characteristics(self, signal_data, zero_crossings):
        """Extraction des hauteurs et périodes des vagues"""
        wave_heights = []
        wave_periods = []

        for i in range(len(zero_crossings) - 1):
            # Indices correspondant à la vague
            start_idx = int(zero_crossings[i] * self.fs)
            end_idx = int(zero_crossings[i + 1] * self.fs)

            if end_idx > start_idx:
                wave_segment = signal_data[start_idx:end_idx]

                # Hauteur de vague (crête à creux)
                H = np.max(wave_segment) - np.min(wave_segment)
                wave_heights.append(H)

                # Période de vague
                T = zero_crossings[i + 1] - zero_crossings[i]
                wave_periods.append(T)

        return np.array(wave_heights), np.array(wave_periods)

    def _calculate_wave_statistics(self, heights, periods):
        """Calcul des statistiques des vagues"""
        if len(heights) == 0:
            return {}

        heights_sorted = np.sort(heights)[::-1]  # Tri décroissant

        # Hauteurs caractéristiques
        H_max = np.max(heights)
        H_min = np.min(heights)
        H_mean = np.mean(heights)
        H_rms = np.sqrt(np.mean(heights**2))

        # Hauteurs significatives
        n_third = max(1, len(heights) // 3)
        n_tenth = max(1, len(heights) // 10)
        H_1_3 = np.mean(heights_sorted[:n_third])  # H_s
        H_1_10 = np.mean(heights_sorted[:n_tenth])

        # Périodes caractéristiques
        T_max = np.max(periods) if len(periods) > 0 else 0
        T_mean = np.mean(periods) if len(periods) > 0 else 0

        return {
            'H_max': H_max, 'H_min': H_min, 'H_mean': H_mean, 'H_rms': H_rms,
            'H_1_3': H_1_3, 'H_1_10': H_1_10, 'H_s': H_1_3,
            'T_max': T_max, 'T_mean': T_mean,
            'n_waves': len(heights)
        }

    # Dans frequency_domain_analysis, remplacer par :
def frequency_domain_analysis(self, processed_signals):
    """Analyse fréquentielle avec la méthode de Welch"""
    for probe_name, probe_data in processed_signals.items():
        signal_data = probe_data['processed']
        N = len(signal_data)

        # Estimation de la densité spectrale de puissance avec Welch
        nperseg = min(N // 8, 1024)  # Limiter la taille du segment
        noverlap = nperseg // 2

        # Calcul de la densité spectrale de puissance
        freqs, power_spectrum = welch(signal_data, fs=self.fs, nperseg=nperseg, noverlap=noverlap)

        # Calcul FFT pour la phase (nécessaire pour Goda)
        fft_result = np.fft.fft(signal_data)
        fft_complex = fft_result[:len(freqs)]  # Garder seulement les fréquences positives

        # Calcul des moments spectraux
        moments = self._calculate_spectral_moments(freqs, power_spectrum)

        # Stockage des résultats
        self.frequency_domain_results[probe_name] = {
            'frequencies': freqs,
            'power_spectrum': power_spectrum,
            'amplitude_spectrum': np.sqrt(power_spectrum),
            'phase_spectrum': np.angle(fft_complex),
            'fft_complex': fft_complex,  # Nécessaire pour Goda
            'spectral_moments': moments
        }


    def _calculate_spectral_moments(self, freqs, power_spectrum):
        """Calcul des moments spectraux"""
        # Filtrer les fréquences valides (éviter f=0)
        valid_idx = freqs > 0.01
        f_valid = freqs[valid_idx]
        S_valid = power_spectrum[valid_idx]

        if len(f_valid) > 1:
            df = f_valid[1] - f_valid[0]
        else:
            df = 1.0

        moments = {}
        for n in [-1, 0, 1, 2, 4]:
            if n >= 0:
                moments[f'm_{n}'] = np.trapz(S_valid * f_valid**n, dx=df)
            else:
                moments[f'm_{n}'] = np.trapz(S_valid / f_valid**abs(n), dx=df)

        # Paramètres spectraux dérivés
        if moments['m_0'] > 0:
            moments['H_m0'] = 4 * np.sqrt(moments['m_0'])  # Hauteur significative spectrale

        if moments['m_0'] > 0 and moments['m_2'] > 0:
            moments['T_m02'] = 2 * np.pi * np.sqrt(moments['m_0'] / moments['m_2'])

        if moments['m_-1'] > 0 and moments['m_0'] > 0:
            moments['T_m-10'] = moments['m_-1'] / moments['m_0']

        # Période pic (fréquence de maximum d'énergie)
        if len(S_valid) > 0:
            peak_idx = np.argmax(S_valid)
            moments['f_peak'] = f_valid[peak_idx]
            moments['T_peak'] = 1.0 / moments['f_peak'] if moments['f_peak'] > 0 else 0

        return moments


    def wave_separation_goda_method(self, processed_signals):
        """
        Séparation des ondes incidentes/réfléchies par méthode de Goda
        avec résolution par moindres carrés
        """
        # Récupérer les signaux dans l'ordre des positions
        probe_names = list(processed_signals.keys())

        # Matrice des amplitudes complexes pour chaque fréquence
        frequencies = self.frequency_domain_results[probe_names[0]]['frequencies']

        # Résultats de séparation
        incident_amplitude = np.zeros(len(frequencies), dtype=complex)
        reflected_amplitude = np.zeros(len(frequencies), dtype=complex)
        reflection_coefficient = np.zeros(len(frequencies), dtype=complex)

        for f_idx, freq in enumerate(frequencies):
            if freq <= 0.01:  # Éviter les très basses fréquences
                continue

            omega = 2 * np.pi * freq
            k = self.solve_dispersion(omega)

            # Vecteur des amplitudes mesurées (complexes) pour cette fréquence
            X = np.array([
                self.frequency_domain_results[probe]['fft_complex'][f_idx] 
                for probe in probe_names
            ])

            # Construction de la matrice de transfert M
            M = np.zeros((self.n_probes, 2), dtype=complex)
            for i, x_pos in enumerate(self.probe_positions):
                M[i, 0] = np.exp(1j * k * x_pos)      # Onde incidente
                M[i, 1] = np.exp(-1j * k * x_pos)     # Onde réfléchie

            # Résolution par moindres carrés : A = (M^H * M)^(-1) * M^H * X
            try:
                MH = M.conj().T
                MHM = np.dot(MH, M)

                # Vérification du conditionnement
                if np.linalg.cond(MHM) < 1e12:  # Matrice bien conditionnée
                    MHM_inv = np.linalg.inv(MHM)
                    A = np.dot(np.dot(MHM_inv, MH), X)

                    incident_amplitude[f_idx] = A[0]
                    reflected_amplitude[f_idx] = A[1]

                    # Coefficient de réflexion
                    if np.abs(A[0]) > 1e-10:
                        reflection_coefficient[f_idx] = A[1] / A[0]

            except (np.linalg.LinAlgError, ValueError):
                # En cas de problème numérique
                pass

        # Stockage des résultats
        self.wave_separation_results = {
            'frequencies': frequencies,
            'incident_amplitude': incident_amplitude,
            'reflected_amplitude': reflected_amplitude,
            'incident_spectrum': np.abs(incident_amplitude)**2,
            'reflected_spectrum': np.abs(reflected_amplitude)**2,
            'reflection_coefficient': reflection_coefficient,
            'reflection_magnitude': np.abs(reflection_coefficient),
            'reflection_phase': np.angle(reflection_coefficient)
        }

        # Analyse statistique de la réflexion
        self._analyze_reflection_statistics()

    def _analyze_reflection_statistics(self):
        """Analyse statistique des coefficients de réflexion"""
        Kr = self.wave_separation_results['reflection_magnitude']
        freqs = self.wave_separation_results['frequencies']

        # Filtrer les valeurs valides
        valid_idx = (freqs > 0.05) & (freqs < 2.0) & (Kr > 0) & (Kr < 2.0)
        Kr_valid = Kr[valid_idx]
        freqs_valid = freqs[valid_idx]

        if len(Kr_valid) > 0:
            self.reflection_analysis = {
                'Kr_mean': np.mean(Kr_valid),
                'Kr_max': np.max(Kr_valid),
                'Kr_min': np.min(Kr_valid),
                'Kr_std': np.std(Kr_valid),
                'freq_range': [np.min(freqs_valid), np.max(freqs_valid)],
                'optimal_freq_bands': self._identify_optimal_frequency_bands(freqs_valid, Kr_valid)
            }
        else:
            self.reflection_analysis = {}

    def _identify_optimal_frequency_bands(self, freqs, Kr):
        """Identification des bandes de fréquences optimales pour l'analyse"""
        bands = {
            'low_freq': (0.05, 0.15),
            'mid_freq': (0.15, 0.4),
            'high_freq': (0.4, 1.0)
        }

        band_analysis = {}
        for band_name, (f_min, f_max) in bands.items():
            band_idx = (freqs >= f_min) & (freqs <= f_max)
            if np.sum(band_idx) > 0:
                band_analysis[band_name] = {
                    'Kr_mean': np.mean(Kr[band_idx]),
                    'Kr_std': np.std(Kr[band_idx]),
                    'freq_range': [f_min, f_max],
                    'n_points': np.sum(band_idx)
                }

        return band_analysis

    def run_complete_analysis(self, raw_signals):
        """Exécution complète de l'analyse multidimensionnelle"""
        print("🌊 Démarrage de l'analyse multidimensionnelle des signaux de houle...")

        # 1. Prétraitement
        print("📊 Phase 1: Prétraitement des signaux...")
        processed_signals = self.preprocess_signals(raw_signals)

        # 2. Analyse temporelle
        print("⏱️ Phase 2: Analyse temporelle (détection des vagues)...")
        self.time_domain_analysis(processed_signals)

        # 3. Analyse fréquentielle
        print("📈 Phase 3: Analyse fréquentielle (FFT)...")
        self.frequency_domain_analysis(processed_signals)

        # 4. Séparation des ondes
        print("🔄 Phase 4: Séparation ondes incidentes/réfléchies (Méthode Goda)...")
        self.wave_separation_goda_method(processed_signals)

        print("✅ Analyse multidimensionnelle terminée avec succès!")

        return {
            'processed_signals': processed_signals,
            'time_domain': self.time_domain_results,
            'frequency_domain': self.frequency_domain_results,
            'wave_separation': self.wave_separation_results,
            'reflection_analysis': self.reflection_analysis
        }

class AutomatedReportGenerator:
    """
    Générateur de rapports automatisés pour l'analyse des signaux de houle
    """

    def __init__(self, analyzer_results, output_dir="reports"):
        self.results = analyzer_results
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Créer le dossier de sortie
        os.makedirs(output_dir, exist_ok=True)

        # Configuration des styles
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9,
            'figure.titlesize': 14
        })

    def generate_complete_report(self, project_name="Analyse Houle"):
        """Génération du rapport complet avec toutes les visualisations"""

        report_filename = os.path.join(
            self.output_dir, 
            f"Rapport_Houle_{project_name}_{self.timestamp}.pdf"
        )

        with PdfPages(report_filename) as pdf:
            print(f"📄 Génération du rapport PDF: {report_filename}")

            # Page de titre
            self._create_title_page(pdf, project_name)

            # Résumé exécutif
            self._create_executive_summary(pdf)

            # Analyse temporelle
            self._create_time_domain_plots(pdf)

            # Analyse fréquentielle
            self._create_frequency_domain_plots(pdf)

            # Analyse de séparation des ondes
            self._create_wave_separation_plots(pdf)

            # Analyse de réflexion
            self._create_reflection_analysis_plots(pdf)

            # Tableaux de données
            self._create_data_tables(pdf)

        # Génération du rapport JSON pour les données
        self._export_data_json()

        print(f"✅ Rapport complet généré: {report_filename}")
        return report_filename

    def _create_title_page(self, pdf, project_name):
        """Création de la page de titre"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')

        # Titre principal
        ax.text(0.5, 0.8, "RAPPORT D'ANALYSE", 
                horizontalalignment='center', fontsize=24, weight='bold',
                transform=ax.transAxes)

        ax.text(0.5, 0.75, "SIGNAUX DE HOULE", 
                horizontalalignment='center', fontsize=20, weight='bold',
                transform=ax.transAxes)

        ax.text(0.5, 0.65, f"📊 {project_name}", 
                horizontalalignment='center', fontsize=16, style='italic',
                transform=ax.transAxes)

        # Informations du projet
        info_text = f"""
        🗓️ Date: {datetime.now().strftime("%d/%m/%Y %H:%M")}

        🔬 Méthodes d'analyse:
        • Analyse temporelle (Zero-crossing)
        • Transformée de Fourier (FFT)
        • Méthode de Goda
        • Moindres carrés

        📈 Paramètres analysés:
        • Caractéristiques des vagues individuelles
        • Spectres d'énergie
        • Séparation incident/réfléchi
        • Coefficients de réflexion
        """

        ax.text(0.1, 0.45, info_text, 
                transform=ax.transAxes, fontsize=12,
                verticalalignment='top')

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_executive_summary(self, pdf):
        """Création du résumé exécutif"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("📋 RÉSUMÉ EXÉCUTIF", fontsize=16, weight='bold')

        # Graphique 1: Hauteurs significatives par sonde
        probe_names = list(self.results['time_domain'].keys())
        H_s_values = [self.results['time_domain'][probe]['statistics'].get('H_s', 0) 
                     for probe in probe_names]

        bars = ax1.bar(range(len(probe_names)), H_s_values, 
                      color='skyblue', alpha=0.8)
        ax1.set_title('Hauteurs Significatives (H_s) par Sonde')
        ax1.set_ylabel('H_s (m)')
        ax1.set_xticks(range(len(probe_names)))
        ax1.set_xticklabels(probe_names, rotation=45)

        # Ajouter les valeurs sur les barres
        for bar, value in zip(bars, H_s_values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}m', ha='center', va='bottom')

        # Graphique 2: Périodes moyennes
        T_mean_values = [self.results['time_domain'][probe]['statistics'].get('T_mean', 0) 
                        for probe in probe_names]

        ax2.bar(range(len(probe_names)), T_mean_values, 
               color='lightcoral', alpha=0.8)
        ax2.set_title('Périodes Moyennes par Sonde')
        ax2.set_ylabel('T_mean (s)')
        ax2.set_xticks(range(len(probe_names)))
        ax2.set_xticklabels(probe_names, rotation=45)

        # Graphique 3: Coefficient de réflexion moyen
        if 'reflection_analysis' in self.results and self.results['reflection_analysis']:
            Kr_data = self.results['reflection_analysis']
            Kr_values = [Kr_data.get('Kr_mean', 0)]
            ax3.bar(['Coefficient Réflexion'], Kr_values, 
                   color='gold', alpha=0.8)
            ax3.set_title('Coefficient de Réflexion Moyen')
            ax3.set_ylabel('Kr')
            ax3.text(0, Kr_values[0] + 0.01, f'{Kr_values[0]:.3f}',
                    ha='center', va='bottom')
        else:
            ax3.text(0.5, 0.5, 'Données de réflexion\nnon disponibles',
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax3.transAxes)
            ax3.set_title('Coefficient de Réflexion')

        # Graphique 4: Nombre de vagues détectées
        n_waves = [self.results['time_domain'][probe]['n_waves'] 
                  for probe in probe_names]

        ax4.bar(range(len(probe_names)), n_waves, 
               color='lightgreen', alpha=0.8)
        ax4.set_title('Nombre de Vagues Détectées')
        ax4.set_ylabel('Nombre de vagues')
        ax4.set_xticks(range(len(probe_names)))
        ax4.set_xticklabels(probe_names, rotation=45)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_time_domain_plots(self, pdf):
        """Création des graphiques d'analyse temporelle"""
        probe_names = list(self.results['time_domain'].keys())

        # Page 1: Signaux temporels bruts et traités
        fig, axes = plt.subplots(len(probe_names), 1, 
                                figsize=(12, 2*len(probe_names)))
        if len(probe_names) == 1:
            axes = [axes]

        fig.suptitle("📊 ANALYSE TEMPORELLE - Signaux Traités", 
                    fontsize=16, weight='bold')

        for i, probe in enumerate(probe_names):
            processed_data = self.results['processed_signals'][probe]['processed']
            time_array = np.linspace(0, len(processed_data)/32, len(processed_data))  # Assumant fs=32Hz

            axes[i].plot(time_array, processed_data, 'b-', alpha=0.8, linewidth=1)
            axes[i].set_title(f'Signal Traité - {probe}')
            axes[i].set_ylabel('Amplitude (m)')
            axes[i].grid(True, alpha=0.3)

            if i == len(probe_names) - 1:
                axes[i].set_xlabel('Temps (s)')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # Page 2: Histogrammes des hauteurs de vagues
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("📏 DISTRIBUTION DES HAUTEURS DE VAGUES", 
                    fontsize=16, weight='bold')
        axes = axes.flatten()

        for i, probe in enumerate(probe_names[:4]):  # Limite à 4 sondes
            if i < len(axes):
                wave_heights = self.results['time_domain'][probe]['wave_heights']

                axes[i].hist(wave_heights, bins=20, alpha=0.7, 
                           color=plt.cm.viridis(i/len(probe_names)))
                axes[i].set_title(f'Distribution H - {probe}')
                axes[i].set_xlabel('Hauteur (m)')
                axes[i].set_ylabel('Fréquence')
                axes[i].grid(True, alpha=0.3)

                # Ajouter statistiques
                stats = self.results['time_domain'][probe]['statistics']
                stats_text = f"H_max: {stats.get('H_max', 0):.3f}m\n"
                stats_text += f"H_s: {stats.get('H_s', 0):.3f}m\n"
                stats_text += f"H_mean: {stats.get('H_mean', 0):.3f}m"

                axes[i].text(0.02, 0.98, stats_text, 
                           transform=axes[i].transAxes,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # Masquer les axes non utilisés
        for i in range(len(probe_names), len(axes)):
            axes[i].axis('off')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_frequency_domain_plots(self, pdf):
        """Création des graphiques d'analyse fréquentielle"""
        probe_names = list(self.results['frequency_domain'].keys())

        # Page 1: Spectres de puissance
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle("🌊 ANALYSE FRÉQUENTIELLE - Spectres de Puissance", 
                    fontsize=16, weight='bold')

        for i, probe in enumerate(probe_names):
            freq_data = self.results['frequency_domain'][probe]
            freqs = freq_data['frequencies']
            power_spec = freq_data['power_spectrum']

            # Filtrer les fréquences d'intérêt
            valid_idx = (freqs > 0.01) & (freqs < 2.0)

            ax.semilogy(freqs[valid_idx], power_spec[valid_idx], 
                       label=probe, linewidth=2, alpha=0.8)

        ax.set_xlabel('Fréquence (Hz)')
        ax.set_ylabel('Densité Spectrale de Puissance')
        ax.set_title('Spectres de Puissance - Toutes Sondes')
        ax.legend()
        ax.grid(True, alpha=0.3)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # Page 2: Moments spectraux
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("📊 PARAMÈTRES SPECTRAUX", fontsize=16, weight='bold')

        # H_m0 (hauteur significative spectrale)
        H_m0_values = [self.results['frequency_domain'][probe]['spectral_moments'].get('H_m0', 0) 
                      for probe in probe_names]
        ax1.bar(range(len(probe_names)), H_m0_values, color='cyan', alpha=0.7)
        ax1.set_title('Hauteur Significative Spectrale (H_m0)')
        ax1.set_ylabel('H_m0 (m)')
        ax1.set_xticks(range(len(probe_names)))
        ax1.set_xticklabels(probe_names, rotation=45)

        # Période pic
        T_peak_values = [self.results['frequency_domain'][probe]['spectral_moments'].get('T_peak', 0) 
                        for probe in probe_names]
        ax2.bar(range(len(probe_names)), T_peak_values, color='orange', alpha=0.7)
        ax2.set_title('Période Pic (T_peak)')
        ax2.set_ylabel('T_peak (s)')
        ax2.set_xticks(range(len(probe_names)))
        ax2.set_xticklabels(probe_names, rotation=45)

        # Énergie totale (m0)
        m0_values = [self.results['frequency_domain'][probe]['spectral_moments'].get('m_0', 0) 
                    for probe in probe_names]
        ax3.bar(range(len(probe_names)), m0_values, color='pink', alpha=0.7)
        ax3.set_title('Moment Spectral m0 (Énergie)')
        ax3.set_ylabel('m0')
        ax3.set_xticks(range(len(probe_names)))
        ax3.set_xticklabels(probe_names, rotation=45)

        # Fréquence pic
        f_peak_values = [self.results['frequency_domain'][probe]['spectral_moments'].get('f_peak', 0) 
                        for probe in probe_names]
        ax4.bar(range(len(probe_names)), f_peak_values, color='lightgreen', alpha=0.7)
        ax4.set_title('Fréquence Pic (f_peak)')
        ax4.set_ylabel('f_peak (Hz)')
        ax4.set_xticks(range(len(probe_names)))
        ax4.set_xticklabels(probe_names, rotation=45)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_wave_separation_plots(self, pdf):
        """Création des graphiques de séparation des ondes"""
        if 'wave_separation' not in self.results:
            return

        sep_data = self.results['wave_separation']

        # Page 1: Spectres incident et réfléchi
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle("🔄 SÉPARATION DES ONDES - Méthode de Goda", 
                    fontsize=16, weight='bold')

        freqs = sep_data['frequencies']
        valid_idx = (freqs > 0.05) & (freqs < 1.5)

        # Spectres d'énergie
        ax1.semilogy(freqs[valid_idx], sep_data['incident_spectrum'][valid_idx], 
                    'b-', label='Spectre Incident', linewidth=2)
        ax1.semilogy(freqs[valid_idx], sep_data['reflected_spectrum'][valid_idx], 
                    'r-', label='Spectre Réfléchi', linewidth=2)
        ax1.set_ylabel('Densité Spectrale')
        ax1.set_title('Spectres d\'Énergie Séparés')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Coefficient de réflexion
        Kr = sep_data['reflection_magnitude'][valid_idx]
        ax2.plot(freqs[valid_idx], Kr, 'g-', linewidth=2, alpha=0.8)
        ax2.set_xlabel('Fréquence (Hz)')
        ax2.set_ylabel('|Kr|')
        ax2.set_title('Coefficient de Réflexion en Magnitude')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, min(2.0, np.max(Kr) * 1.1))

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # Page 2: Phase du coefficient de réflexion
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.suptitle("📐 PHASE DU COEFFICIENT DE RÉFLEXION", 
                    fontsize=16, weight='bold')

        phase_rad = sep_data['reflection_phase'][valid_idx]
        phase_deg = np.degrees(phase_rad)

        ax.plot(freqs[valid_idx], phase_deg, 'purple', linewidth=2, alpha=0.8)
        ax.set_xlabel('Fréquence (Hz)')
        ax.set_ylabel('Phase (°)')
        ax.set_title('Phase du Coefficient de Réflexion')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_reflection_analysis_plots(self, pdf):
        """Création des graphiques d'analyse de réflexion"""
        if 'reflection_analysis' not in self.results or not self.results['reflection_analysis']:
            return

        refl_data = self.results['reflection_analysis']

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("🎯 ANALYSE DE RÉFLEXION DÉTAILLÉE", 
                    fontsize=16, weight='bold')

        # Statistiques globales
        stats_names = ['Kr_mean', 'Kr_max', 'Kr_min', 'Kr_std']
        stats_values = [refl_data.get(stat, 0) for stat in stats_names]
        stats_labels = ['Moyenne', 'Maximum', 'Minimum', 'Écart-type']

        bars = ax1.bar(stats_labels, stats_values, 
                      color=['blue', 'red', 'green', 'orange'], alpha=0.7)
        ax1.set_title('Statistiques du Coefficient de Réflexion')
        ax1.set_ylabel('Kr')

        for bar, value in zip(bars, stats_values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')

        # Analyse par bandes de fréquences
        if 'optimal_freq_bands' in refl_data:
            bands_data = refl_data['optimal_freq_bands']
            band_names = list(bands_data.keys())
            band_kr_means = [bands_data[band]['Kr_mean'] for band in band_names]

            ax2.bar(band_names, band_kr_means, 
                   color=['lightblue', 'lightcoral', 'lightgreen'], alpha=0.7)
            ax2.set_title('Kr Moyen par Bande de Fréquence')
            ax2.set_ylabel('Kr Moyen')
            ax2.tick_params(axis='x', rotation=45)

        # Graphique de qualité des données
        freq_range = refl_data.get('freq_range', [0, 1])
        ax3.text(0.5, 0.7, f"Gamme de fréquences analysée:", 
                ha='center', va='center', transform=ax3.transAxes, fontsize=11)
        ax3.text(0.5, 0.5, f"{freq_range[0]:.2f} - {freq_range[1]:.2f} Hz", 
                ha='center', va='center', transform=ax3.transAxes, 
                fontsize=14, weight='bold')
        ax3.text(0.5, 0.3, f"Coefficient moyen: {refl_data['Kr_mean']:.3f}", 
                ha='center', va='center', transform=ax3.transAxes, fontsize=11)
        ax3.set_title('Informations d\'Analyse')
        ax3.axis('off')

        # Performance de la méthode
        if 'optimal_freq_bands' in refl_data:
            n_points_total = sum([band['n_points'] for band in bands_data.values()])
            ax4.text(0.5, 0.7, "Points de données valides:", 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=11)
            ax4.text(0.5, 0.5, f"{n_points_total}", 
                    ha='center', va='center', transform=ax4.transAxes, 
                    fontsize=16, weight='bold', color='green')
            ax4.text(0.5, 0.3, "Qualité de l'analyse: Excellente" if n_points_total > 100 else "Qualité: Bonne", 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=11)
        ax4.set_title('Qualité des Données')
        ax4.axis('off')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _create_data_tables(self, pdf):
        """Création des tableaux de données"""
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle("📋 TABLEAUX DE DONNÉES SYNTHÉTIQUES", 
                    fontsize=16, weight='bold')
        ax.axis('off')

        # Construction du tableau de résumé
        probe_names = list(self.results['time_domain'].keys())

        # Données pour le tableau
        table_data = []
        headers = ['Sonde', 'H_max (m)', 'H_s (m)', 'T_mean (s)', 'N_vagues', 'H_m0 (m)', 'T_peak (s)']

        for probe in probe_names:
            time_stats = self.results['time_domain'][probe]['statistics']
            freq_stats = self.results['frequency_domain'][probe]['spectral_moments']

            row = [
                probe,
                f"{time_stats.get('H_max', 0):.3f}",
                f"{time_stats.get('H_s', 0):.3f}",
                f"{time_stats.get('T_mean', 0):.2f}",
                f"{self.results['time_domain'][probe]['n_waves']}",
                f"{freq_stats.get('H_m0', 0):.3f}",
                f"{freq_stats.get('T_peak', 0):.2f}"
            ]
            table_data.append(row)

        # Créer le tableau
        table = ax.table(cellText=table_data,
                        colLabels=headers,
                        cellLoc='center',
                        loc='center',
                        bbox=[0, 0.5, 1, 0.4])

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)

        # Style du tableau
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Informations supplémentaires
        if 'reflection_analysis' in self.results and self.results['reflection_analysis']:
            refl_info = f"""
            ANALYSE DE RÉFLEXION:
            • Coefficient moyen: {self.results['reflection_analysis']['Kr_mean']:.3f}
            • Coefficient maximum: {self.results['reflection_analysis']['Kr_max']:.3f}
            • Écart-type: {self.results['reflection_analysis']['Kr_std']:.3f}
            """
            ax.text(0.05, 0.3, refl_info, transform=ax.transAxes, 
                   fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    def _export_data_json(self):
        """Export des données en format JSON"""
        json_filename = os.path.join(
            self.output_dir, 
            f"donnees_houle_{self.timestamp}.json"
        )

        # Préparer les données pour JSON (conversion des arrays numpy)
        json_data = {
            'metadata': {
                'timestamp': self.timestamp,
                'analysis_date': datetime.now().isoformat(),
                'n_probes': len(self.results['time_domain'])
            },
            'time_domain_summary': {},
            'frequency_domain_summary': {},
            'reflection_summary': self.results.get('reflection_analysis', {})
        }

        # Résumé temporel
        for probe, data in self.results['time_domain'].items():
            json_data['time_domain_summary'][probe] = data['statistics']
            json_data['time_domain_summary'][probe]['n_waves'] = data['n_waves']

        # Résumé fréquentiel
        for probe, data in self.results['frequency_domain'].items():
            json_data['frequency_domain_summary'][probe] = data['spectral_moments']

        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)

        print(f"📊 Données exportées en JSON: {json_filename}")

# Fonction d'intégration avec le système d'acquisition existant
def integrate_with_acquisition_system():
    """
    Fonction d'intégration pour connecter l'analyse multidimensionnelle 
    au système d'acquisition existant
    """

    def enhanced_finalize_acquisition(self):
        """Version améliorée de finalize_acquisition avec analyse complète"""
        if self.running:
            self.running = False
            if self.acquisition_timer.isActive(): 
                self.acquisition_timer.stop()
            if self.plot_update_timer.isActive(): 
                self.plot_update_timer.stop()

            print("Timers arrêtés.")
            self.refresh_all_plots_and_info()

            # === NOUVELLE PARTIE: ANALYSE MULTIDIMENSIONNELLE ===
            print("\n🚀 Démarrage de l'analyse multidimensionnelle...")

            try:
                # Préparer les données pour l'analyseur
                raw_signals = {}
                for i, sonde_name in enumerate(self.sonde_names_calib):
                    if i < len(self.data_storage_full):
                        raw_signals[sonde_name] = np.array(self.data_storage_full[i])

                # Configuration de l'analyseur (adapter selon votre setup)
                probe_positions = np.linspace(0, 2.0, self.n_sondes_total_calib)  # Positions par défaut
                water_depth = 0.5  # Profondeur par défaut - À ADAPTER

                # Création de l'analyseur
                analyzer = MultidimensionalWaveAnalyzer(
                    probe_positions=probe_positions,
                    water_depth=water_depth,
                    sampling_freq=self.freq,
                    duration=self.duree_s
                )

                # Exécution de l'analyse complète
                results = analyzer.run_complete_analysis(raw_signals)

                # Génération du rapport automatisé
                report_generator = AutomatedReportGenerator(
                    results, 
                    output_dir=self.save_folder
                )

                report_filename = report_generator.generate_complete_report(
                    project_name="HRNeoWave_Analysis"
                )

                # Message de succès
                message = f"""
                ✅ Acquisition et analyse terminées avec succès !

                📊 Durée: {self.duree_s}s
                📈 Sondes analysées: {self.n_sondes_total_calib}
                📄 Rapport généré: {os.path.basename(report_filename)}
                """

                QMessageBox.information(self, "Analyse Complète Terminée", message)

            except Exception as e:
                print(f"❌ Erreur lors de l'analyse multidimensionnelle: {e}")
                QMessageBox.warning(self, "Erreur d'Analyse", 
                                  f"L'acquisition est terminée mais l'analyse avancée a échoué:\n{e}")

            # Sauvegarde CSV standard
            self.save_all_data_to_csv()

            QTimer.singleShot(0, self.close)

        return enhanced_finalize_acquisition

class ResultsDisplayWindow(QWidget):
    """Interface d'affichage des résultats d'analyse multidimensionnelle"""
    
    def __init__(self, analysis_results=None, parent=None):
        super().__init__(parent)
        self.analysis_results = analysis_results
        self.setWindowTitle("Résultats d'Analyse - HRNeoWave")
        self.setGeometry(100, 100, 1400, 900)
        
        # Configuration du style sombre
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #3c3c3c;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
            QTableWidget {
                background-color: #3c3c3c;
                alternate-background-color: #484848;
                gridline-color: #555555;
                selection-background-color: #0078d4;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QTextEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px;
            }
            QScrollArea {
                border: none;
                background-color: #2b2b2b;
            }
        """)
        
        self.setup_ui()
        if self.analysis_results:
            self.populate_results()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # En-tête
        header_layout = QHBoxLayout()
        title_label = QLabel("📊 RÉSULTATS D'ANALYSE MULTIDIMENSIONNELLE")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #0078d4; margin: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Boutons d'action
        self.export_btn = QPushButton("📄 Exporter Rapport")
        self.export_btn.clicked.connect(self.export_report)
        header_layout.addWidget(self.export_btn)
        
        self.refresh_btn = QPushButton("🔄 Actualiser")
        self.refresh_btn.clicked.connect(self.refresh_display)
        header_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(header_layout)
        
        # Onglets principaux
        self.tab_widget = QTabWidget()
        
        # Onglet Résumé
        self.summary_tab = self.create_summary_tab()
        self.tab_widget.addTab(self.summary_tab, "📋 Résumé")
        
        # Onglet Analyse Temporelle
        self.time_tab = self.create_time_analysis_tab()
        self.tab_widget.addTab(self.time_tab, "⏱️ Analyse Temporelle")
        
        # Onglet Analyse Fréquentielle
        self.freq_tab = self.create_frequency_analysis_tab()
        self.tab_widget.addTab(self.freq_tab, "📈 Analyse Fréquentielle")
        
        # Onglet Séparation des Ondes
        self.wave_sep_tab = self.create_wave_separation_tab()
        self.tab_widget.addTab(self.wave_sep_tab, "🌊 Séparation des Ondes")
        
        # Onglet Graphiques
        self.plots_tab = self.create_plots_tab()
        self.tab_widget.addTab(self.plots_tab, "📊 Graphiques")
        
        main_layout.addWidget(self.tab_widget)
        
        # Barre de statut
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Prêt")
        self.status_label.setStyleSheet("color: #888888; font-size: 12px;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        timestamp_label = QLabel(f"Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}")
        timestamp_label.setStyleSheet("color: #888888; font-size: 12px;")
        status_layout.addWidget(timestamp_label)
        
        main_layout.addLayout(status_layout)
        
        self.setLayout(main_layout)
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def create_summary_tab(self):
        """Création de l'onglet résumé"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Informations générales
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_frame.setStyleSheet("QFrame { border: 2px solid #555555; border-radius: 8px; padding: 10px; }")
        info_layout = QGridLayout()
        
        # Labels d'information
        self.info_labels = {}
        info_items = [
            ("Nombre de sondes:", "n_probes"),
            ("Durée d'acquisition:", "duration"),
            ("Fréquence d'échantillonnage:", "sampling_freq"),
            ("Profondeur d'eau:", "water_depth"),
            ("Nombre total de vagues:", "total_waves"),
            ("Coefficient de réflexion moyen:", "avg_reflection")
        ]
        
        for i, (label_text, key) in enumerate(info_items):
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            value_label = QLabel("N/A")
            value_label.setStyleSheet("color: #0078d4;")
            
            info_layout.addWidget(label, i // 2, (i % 2) * 2)
            info_layout.addWidget(value_label, i // 2, (i % 2) * 2 + 1)
            
            self.info_labels[key] = value_label
        
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)
        
        # Tableau de résumé par sonde
        summary_label = QLabel("📊 Résumé par Sonde")
        summary_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(summary_label)
        
        self.summary_table = QTableWidget()
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.summary_table)
        
        layout.addStretch()
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return widget
    
    def create_time_analysis_tab(self):
        """Création de l'onglet d'analyse temporelle"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tableau des statistiques temporelles
        time_label = QLabel("⏱️ Statistiques Temporelles")
        time_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(time_label)
        
        self.time_stats_table = QTableWidget()
        self.time_stats_table.setAlternatingRowColors(True)
        self.time_stats_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.time_stats_table)
        
        # Zone de détails
        details_label = QLabel("📋 Détails de l'Analyse")
        details_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(details_label)
        
        self.time_details_text = QTextEdit()
        self.time_details_text.setMaximumHeight(200)
        self.time_details_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.time_details_text)
        
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return widget
    
    def create_frequency_analysis_tab(self):
        """Création de l'onglet d'analyse fréquentielle"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tableau des moments spectraux
        freq_label = QLabel("📈 Moments Spectraux")
        freq_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(freq_label)
        
        self.freq_table = QTableWidget()
        self.freq_table.setAlternatingRowColors(True)
        self.freq_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.freq_table)
        
        # Informations spectrales
        spectral_info_label = QLabel("🔍 Informations Spectrales")
        spectral_info_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(spectral_info_label)
        
        self.spectral_info_text = QTextEdit()
        self.spectral_info_text.setMaximumHeight(200)
        self.spectral_info_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.spectral_info_text)
        
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return widget
    
    def create_wave_separation_tab(self):
        """Création de l'onglet de séparation des ondes"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Informations de réflexion
        reflection_label = QLabel("🌊 Analyse de Réflexion")
        reflection_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(reflection_label)
        
        # Tableau des coefficients de réflexion
        self.reflection_table = QTableWidget()
        self.reflection_table.setAlternatingRowColors(True)
        self.reflection_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.reflection_table)
        
        # Analyse par bandes de fréquences
        bands_label = QLabel("📊 Analyse par Bandes de Fréquences")
        bands_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(bands_label)
        
        self.bands_table = QTableWidget()
        self.bands_table.setAlternatingRowColors(True)
        self.bands_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.bands_table)
        
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return widget
    
    def create_plots_tab(self):
        """Création de l'onglet des graphiques"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Zone de contrôle des graphiques
        control_layout = QHBoxLayout()
        
        plot_type_label = QLabel("Type de graphique:")
        control_layout.addWidget(plot_type_label)
        
        self.plot_selector = QPushButton("Sélectionner...")
        self.plot_selector.clicked.connect(self.show_plot_options)
        control_layout.addWidget(self.plot_selector)
        
        control_layout.addStretch()
        
        self.generate_plot_btn = QPushButton("📊 Générer Graphique")
        self.generate_plot_btn.clicked.connect(self.generate_selected_plot)
        control_layout.addWidget(self.generate_plot_btn)
        
        layout.addLayout(control_layout)
        
        # Zone d'affichage des graphiques
        self.plot_scroll = QScrollArea()
        self.plot_scroll.setWidgetResizable(True)
        self.plot_scroll.setMinimumHeight(600)
        self.plot_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.plot_container = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_container.setLayout(self.plot_layout)
        self.plot_scroll.setWidget(self.plot_container)
        self.plot_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.plot_scroll)
        
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return widget
    
    def populate_results(self):
        """Remplissage des résultats dans l'interface"""
        if not self.analysis_results:
            return
        
        self.populate_summary()
        self.populate_time_analysis()
        self.populate_frequency_analysis()
        self.populate_wave_separation()
        
        self.status_label.setText("Résultats chargés avec succès")
    
    def populate_summary(self):
      """Remplissage de l'onglet résumé"""
      results = self.analysis_results
    
    # Informations générales
      if 'time_domain' in results:
        n_probes = len(results['time_domain'])
        self.info_labels['n_probes'].setText(str(n_probes))
        
        total_waves = sum(results['time_domain'][probe]['n_waves'] 
                        for probe in results['time_domain'])
        self.info_labels['total_waves'].setText(str(total_waves))
    
      if 'reflection_analysis' in results and results['reflection_analysis']:
        avg_kr = results['reflection_analysis'].get('Kr_mean', 0)
        self.info_labels['avg_reflection'].setText(f"{avg_kr:.3f}")
    
    # Tableau de résumé
      if 'time_domain' in results:
        probe_names = list(results['time_domain'].keys())
        
        headers = ['Sonde', 'H_max (m)', 'H_s (m)', 'T_mean (s)', 'N_vagues', 'H_m0 (m)', 'T_peak (s)', 'T_m02 (s)', 'T_m-10 (s)']
        self.summary_table.setColumnCount(len(headers))
        self.summary_table.setHorizontalHeaderLabels(headers)
        self.summary_table.setRowCount(len(probe_names))
        
        for i, probe in enumerate(probe_names):
            time_stats = results['time_domain'][probe]['statistics']
            freq_stats = results['frequency_domain'][probe]['spectral_moments']
            
            data = [
                probe,
                f"{time_stats.get('H_max', 0):.3f}",
                f"{time_stats.get('H_s', 0):.3f}",
                f"{time_stats.get('T_mean', 0):.2f}",
                str(results['time_domain'][probe]['n_waves']),
                f"{freq_stats.get('H_m0', 0):.3f}",
                f"{freq_stats.get('T_peak', 0):.2f}",
                f"{freq_stats.get('T_m02', 0):.2f}",  # Nouvelle colonne pour T_m02
                f"{freq_stats.get('T_m-10', 0):.2f}"  # Nouvelle colonne pour T_m-10
            ]
            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.summary_table.setItem(i, j, item)
        
        self.summary_table.resizeColumnsToContents()
    def populate_time_analysis(self):
        """Remplissage de l'analyse temporelle"""
        if 'time_domain' not in self.analysis_results:
            return
        
        results = self.analysis_results['time_domain']
        probe_names = list(results.keys())
        
        # Tableau des statistiques
        headers = ['Sonde', 'H_max', 'H_min', 'H_mean', 'H_rms', 'H_s', 'T_max', 'T_mean', 'N_vagues']
        self.time_stats_table.setColumnCount(len(headers))
        self.time_stats_table.setHorizontalHeaderLabels(headers)
        self.time_stats_table.setRowCount(len(probe_names))
        
        details_text = "DÉTAILS DE L'ANALYSE TEMPORELLE\n\n"
        
        for i, probe in enumerate(probe_names):
            stats = results[probe]['statistics']
            
            data = [
                probe,
                f"{stats.get('H_max', 0):.3f}",
                f"{stats.get('H_min', 0):.3f}",
                f"{stats.get('H_mean', 0):.3f}",
                f"{stats.get('H_rms', 0):.3f}",
                f"{stats.get('H_s', 0):.3f}",
                f"{stats.get('T_max', 0):.2f}",
                f"{stats.get('T_mean', 0):.2f}",
                str(results[probe]['n_waves'])
            ]
            
            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.time_stats_table.setItem(i, j, item)
            
            # Détails textuels
            details_text += f"🔹 {probe}:\n"
            details_text += f"   • Vagues détectées: {results[probe]['n_waves']}\n"
            details_text += f"   • Hauteur significative: {stats.get('H_s', 0):.3f} m\n"
            details_text += f"   • Période moyenne: {stats.get('T_mean', 0):.2f} s\n\n"
        
        self.time_stats_table.resizeColumnsToContents()
        self.time_details_text.setPlainText(details_text)
    
    def populate_frequency_analysis(self):
        """Remplissage de l'analyse fréquentielle"""
        if 'frequency_domain' not in self.analysis_results:
            return
        
        results = self.analysis_results['frequency_domain']
        probe_names = list(results.keys())
        
        # Tableau des moments spectraux
        headers = ['Sonde', 'H_m0 (m)', 'T_peak (s)', 'f_peak (Hz)', 'm_0', 'm_1', 'm_2']
        self.freq_table.setColumnCount(len(headers))
        self.freq_table.setHorizontalHeaderLabels(headers)
        self.freq_table.setRowCount(len(probe_names))
        
        spectral_info = "INFORMATIONS SPECTRALES\n\n"
        
        for i, probe in enumerate(probe_names):
            moments = results[probe]['spectral_moments']
            
            data = [
                probe,
                f"{moments.get('H_m0', 0):.3f}",
                f"{moments.get('T_peak', 0):.2f}",
                f"{moments.get('f_peak', 0):.3f}",
                f"{moments.get('m_0', 0):.2e}",
                f"{moments.get('m_1', 0):.2e}",
                f"{moments.get('m_2', 0):.2e}"
            ]
            
            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.freq_table.setItem(i, j, item)
            
            # Informations spectrales
            spectral_info += f"🔹 {probe}:\n"
            spectral_info += f"   • Fréquence pic: {moments.get('f_peak', 0):.3f} Hz\n"
            spectral_info += f"   • Période pic: {moments.get('T_peak', 0):.2f} s\n"
            spectral_info += f"   • Hauteur spectrale: {moments.get('H_m0', 0):.3f} m\n\n"
        
        self.freq_table.resizeColumnsToContents()
        self.spectral_info_text.setPlainText(spectral_info)
    
    def populate_wave_separation(self):
        """Remplissage de l'analyse de séparation des ondes"""
        if 'reflection_analysis' not in self.analysis_results:
            return
        
        refl_data = self.analysis_results['reflection_analysis']
        
        # Tableau des coefficients de réflexion
        headers = ['Paramètre', 'Valeur']
        self.reflection_table.setColumnCount(2)
        self.reflection_table.setHorizontalHeaderLabels(headers)
        
        refl_params = [
            ('Coefficient moyen', f"{refl_data.get('Kr_mean', 0):.3f}"),
            ('Coefficient maximum', f"{refl_data.get('Kr_max', 0):.3f}"),
            ('Coefficient minimum', f"{refl_data.get('Kr_min', 0):.3f}"),
            ('Écart-type', f"{refl_data.get('Kr_std', 0):.3f}"),
            ('Gamme de fréquences', f"{refl_data.get('freq_range', [0, 0])[0]:.2f} - {refl_data.get('freq_range', [0, 0])[1]:.2f} Hz")
        ]
        
        self.reflection_table.setRowCount(len(refl_params))
        
        for i, (param, value) in enumerate(refl_params):
            param_item = QTableWidgetItem(param)
            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignCenter)
            
            self.reflection_table.setItem(i, 0, param_item)
            self.reflection_table.setItem(i, 1, value_item)
        
        self.reflection_table.resizeColumnsToContents()
        
        # Tableau des bandes de fréquences
        if 'optimal_freq_bands' in refl_data:
            bands_data = refl_data['optimal_freq_bands']
            
            headers = ['Bande', 'Gamme (Hz)', 'Kr moyen', 'Écart-type', 'N points']
            self.bands_table.setColumnCount(len(headers))
            self.bands_table.setHorizontalHeaderLabels(headers)
            self.bands_table.setRowCount(len(bands_data))
            
            for i, (band_name, band_info) in enumerate(bands_data.items()):
                data = [
                    band_name.replace('_', ' ').title(),
                    f"{band_info['freq_range'][0]:.2f} - {band_info['freq_range'][1]:.2f}",
                    f"{band_info['Kr_mean']:.3f}",
                    f"{band_info['Kr_std']:.3f}",
                    str(band_info['n_points'])
                ]
                
                for j, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.bands_table.setItem(i, j, item)
            
            self.bands_table.resizeColumnsToContents()
    
    def show_plot_options(self):
        """Affichage des options de graphiques"""
        # Ici on pourrait ajouter un menu de sélection des types de graphiques
        self.status_label.setText("Sélection de graphiques disponible prochainement")
    
    def generate_selected_plot(self):
        """Génération du graphique sélectionné"""
        if not self.analysis_results:
            return
        
        # Exemple de génération d'un graphique simple
        try:
            # Nettoyer la zone de graphiques
            for i in reversed(range(self.plot_layout.count())): 
                self.plot_layout.itemAt(i).widget().setParent(None)
            
            # Créer un graphique matplotlib
            fig = Figure(figsize=(12, 8), facecolor='#2b2b2b')
            canvas = FigureCanvas(fig)
            
            # Exemple: graphique des hauteurs significatives
            if 'time_domain' in self.analysis_results:
                ax = fig.add_subplot(111, facecolor='#3c3c3c')
                
                probe_names = list(self.analysis_results['time_domain'].keys())
                h_s_values = [self.analysis_results['time_domain'][probe]['statistics'].get('H_s', 0) 
                             for probe in probe_names]
                
                bars = ax.bar(range(len(probe_names)), h_s_values, 
                             color='#0078d4', alpha=0.8)
                
                ax.set_title('Hauteurs Significatives par Sonde', 
                           color='white', fontsize=14, fontweight='bold')
                ax.set_ylabel('H_s (m)', color='white')
                ax.set_xticks(range(len(probe_names)))
                ax.set_xticklabels(probe_names, color='white')
                ax.tick_params(colors='white')
                ax.grid(True, alpha=0.3, color='white')
                
                # Ajouter les valeurs sur les barres
                for bar, value in zip(bars, h_s_values):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{value:.3f}m', ha='center', va='bottom', color='white')
                
                # Configurer les couleurs des axes
                ax.spines['bottom'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.spines['left'].set_color('white')
            
            fig.tight_layout()
            self.plot_layout.addWidget(canvas)
            
            self.status_label.setText("Graphique généré avec succès")
            
        except Exception as e:
            self.status_label.setText(f"Erreur lors de la génération: {str(e)}")
    
    def export_report(self):
        """Export du rapport complet"""
        if not self.analysis_results:
            QMessageBox.warning(self, "Erreur", "Aucun résultat à exporter")
            return
        
        try:
            # Générer le rapport automatisé
            report_generator = AutomatedReportGenerator(
                self.analysis_results, 
                output_dir="reports"
            )
            
            report_filename = report_generator.generate_complete_report(
                project_name="HRNeoWave_Interface"
            )
            
            QMessageBox.information(self, "Export Réussi", 
                                  f"Rapport exporté avec succès:\n{report_filename}")
            
            self.status_label.setText(f"Rapport exporté: {os.path.basename(report_filename)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'Export", 
                               f"Erreur lors de l'export:\n{str(e)}")
    
    def refresh_display(self):
        """Actualisation de l'affichage"""
        if self.analysis_results:
            self.populate_results()
            self.status_label.setText("Affichage actualisé")
        else:
            self.status_label.setText("Aucun résultat à actualiser")

class DataProcessingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Traitement des Données - HRNeoWave")
        self.setGeometry(100, 100, 1200, 800)
        
        # Données d'exemple pour les tests
        self.sample_results = None
        
        layout = QVBoxLayout()
        
        # En-tête
        header_label = QLabel("🔬 MODULE DE TRAITEMENT DES DONNÉES")
        header_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #0078d4; margin: 20px;")
        layout.addWidget(header_label)
        
        # Zone de contrôle
        control_frame = QFrame()
        control_frame.setFrameStyle(QFrame.Box)
        control_frame.setStyleSheet("QFrame { border: 2px solid #555555; border-radius: 8px; padding: 15px; }")
        control_layout = QVBoxLayout()
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        self.restart = QPushButton("🔄 Recommencer")
        self.restart.setMinimumHeight(40)
        self.restart.clicked.connect(self.restart_processing)
        buttons_layout.addWidget(self.restart)
        
        self.load_data_btn = QPushButton("📂 Charger Données")
        self.load_data_btn.setMinimumHeight(40)
        self.load_data_btn.clicked.connect(self.load_data)
        buttons_layout.addWidget(self.load_data_btn)
        
        self.analyze_btn = QPushButton("🔍 Analyser")
        self.analyze_btn.setMinimumHeight(40)
        self.analyze_btn.clicked.connect(self.run_analysis)
        buttons_layout.addWidget(self.analyze_btn)
        
        self.view_results_btn = QPushButton("📊 Voir Résultats")
        self.view_results_btn.setMinimumHeight(40)
        self.view_results_btn.clicked.connect(self.show_results)
        buttons_layout.addWidget(self.view_results_btn)
        
        self.theme_switch = QCheckBox("🌙 Mode sombre")
        self.theme_switch.setChecked(True)
        buttons_layout.addWidget(self.theme_switch)
        
        control_layout.addLayout(buttons_layout)
        control_frame.setLayout(control_layout)
        layout.addWidget(control_frame)
        
        # Zone de statut
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Prêt")
        self.status_label.setStyleSheet("color: #888888; font-size: 12px;")
        status_layout.addWidget(self.status_label)
        layout.addLayout(status_layout)
        
        self.setLayout(layout)
        
        # Initialiser les boutons
        self.analyze_btn.setEnabled(False)
        self.view_results_btn.clicked.connect(self.show_results)
        
        # Ouvrir la fenêtre en plein écran
        self.showMaximized()
    
    def sync_theme_switch(self, theme):
        """Synchronisation du thème"""
        if theme == "dark":
            self.theme_switch.setChecked(True)
        else:
            self.theme_switch.setChecked(False)
    
    def load_data(self, file_path=None):
        """Chargement des données depuis un fichier CSV"""
        if isinstance(file_path, bool) or not file_path:
            # If no valid file path provided, open file dialog
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Charger données", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)"
            )
            if not file_path:
                return

        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Le fichier n'existe pas: {file_path}")

            # Load data from CSV
            self.data = pd.read_csv(file_path)
            self.file_path = file_path
            
            # Enable analysis button
            self.analyze_btn.setEnabled(True)
            self.status_label.setText(f"Données chargées: {os.path.basename(file_path)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement:\n{str(e)}")
            self.status_label.setText("Erreur de chargement")
                
    
    def restart_processing(self):
        """Reset the processing window state"""
        self.sample_results = None
        self.analyze_btn.setEnabled(False)
        self.view_results_btn.setEnabled(False)
        self.status_label.setText("Prêt")
        self.load_data_btn.setEnabled(True)
    def show_results(self):
        """Affichage des résultats"""
        if not self.sample_results:
            QMessageBox.warning(self, "Erreur", "Aucun résultat disponible")
            return
        self.results_window = ResultsDisplayWindow(self.sample_results)
        self.results_window.showMaximized()
    def run_analysis(self):
        """Exécution de l'analyse des données"""
        if not hasattr(self, 'data') or self.data is None:
            QMessageBox.warning(self, "Erreur", "Aucune donnée à analyser")
            return

        try:
            # Configuration de l'analyseur (à adapter selon vos besoins)
            probe_positions = np.linspace(0, 2.0, len(self.data.columns))  # Positions par défaut
            water_depth = 0.5  # Profondeur par défaut
            sampling_freq = 32  # Fréquence d'échantillonnage par défaut
            duration = len(self.data) / sampling_freq

            # Création de l'analyseur
            analyzer = MultidimensionalWaveAnalyzer(
                probe_positions=probe_positions,
                water_depth=water_depth,
                sampling_freq=sampling_freq,
                duration=duration
            )

            # Préparation des données pour l'analyse
            raw_signals = {}
            for i, column in enumerate(self.data.columns):
                raw_signals[f"Sonde_{i+1}"] = self.data[column].values

            # Exécution de l'analyse
            self.status_label.setText("Analyse en cours...")
            self.sample_results = analyzer.run_complete_analysis(raw_signals)
            
            # Activation du bouton de visualisation
            self.view_results_btn.setEnabled(True)
            self.status_label.setText("Analyse terminée avec succès")

            # Affichage automatique des résultats
            self.show_results()

        except Exception as e:
            QMessageBox.critical(self, "Erreur d'Analyse", 
                               f"Une erreur est survenue lors de l'analyse:\n{str(e)}")
            self.status_label.setText("Erreur lors de l'analyse")
                
