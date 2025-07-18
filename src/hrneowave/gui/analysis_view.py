# analysis_view.py - Vue d'analyse post-acquisition
import sys
import os
import time
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QGroupBox, QFormLayout, QSplitter, QSizePolicy,
    QTabWidget, QTextEdit, QProgressBar, QComboBox, QCheckBox, QFileDialog,
    QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont, QPixmap

import pyqtgraph as pg
from pyqtgraph import PlotWidget, mkPen

try:
    from .post_processor import PostProcessor
except ImportError:
    print("⚠️ PostProcessor non disponible")
    PostProcessor = None

class AnalysisWorker(QObject):
    """Worker thread pour analyses lourdes"""
    
    analysisProgress = pyqtSignal(int)  # Progression 0-100
    analysisComplete = pyqtSignal(dict)  # Résultats
    analysisError = pyqtSignal(str)  # Erreur
    
    def __init__(self, filepath: str, post_processor: Optional[PostProcessor] = None):
        super().__init__()
        self.filepath = filepath
        self.post_processor = post_processor
        
    def run_analysis(self):
        """Lance l'analyse complète"""
        try:
            self.analysisProgress.emit(10)
            
            # Chargement données
            data = self._load_data()
            self.analysisProgress.emit(30)
            
            # Analyse spectrale
            spectrum_results = self._compute_spectrum(data)
            self.analysisProgress.emit(60)
            
            # Analyse Goda
            goda_results = self._compute_goda_metrics(data)
            self.analysisProgress.emit(90)
            
            # Compilation résultats
            results = {
                'data': data,
                'spectrum': spectrum_results,
                'goda': goda_results,
                'timestamp': datetime.now().isoformat()
            }
            
            self.analysisProgress.emit(100)
            self.analysisComplete.emit(results)
            
        except Exception as e:
            self.analysisError.emit(str(e))
            
    def _load_data(self) -> Dict[str, np.ndarray]:
        """Charge les données depuis le fichier"""
        if self.filepath.endswith('.csv'):
            df = pd.read_csv(self.filepath)
            return {
                'time': df['Time'].values,
                'channels': [df[col].values for col in df.columns if col.startswith('Sonde_')]
            }
        else:
            raise ValueError(f"Format non supporté: {self.filepath}")
            
    def _compute_spectrum(self, data: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """Calcule les spectres FFT"""
        results = {}
        
        for i, channel_data in enumerate(data['channels']):
            # FFT
            fft = np.fft.fft(channel_data)
            freqs = np.fft.fftfreq(len(channel_data), d=1/32.0)  # 32 Hz par défaut
            
            # Spectre de puissance
            power_spectrum = np.abs(fft)**2
            
            # Garder seulement fréquences positives
            positive_freqs = freqs[:len(freqs)//2]
            positive_spectrum = power_spectrum[:len(power_spectrum)//2]
            
            results[f'channel_{i+1}'] = {
                'frequencies': positive_freqs,
                'spectrum': positive_spectrum,
                'peak_freq': positive_freqs[np.argmax(positive_spectrum)],
                'total_energy': np.sum(positive_spectrum)
            }
            
        return results
        
    def _compute_goda_metrics(self, data: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """Calcule les métriques Goda (analyse statistique des vagues)"""
        results = {}
        
        for i, channel_data in enumerate(data['channels']):
            # Détection des vagues (zéro-crossing)
            zero_crossings = np.where(np.diff(np.signbit(channel_data)))[0]
            
            if len(zero_crossings) < 4:
                # Pas assez de données
                results[f'channel_{i+1}'] = self._empty_goda_metrics()
                continue
                
            # Hauteurs des vagues
            wave_heights = []
            wave_periods = []
            
            for j in range(0, len(zero_crossings)-2, 2):
                start_idx = zero_crossings[j]
                end_idx = zero_crossings[j+2]
                
                if end_idx < len(channel_data):
                    wave_segment = channel_data[start_idx:end_idx]
                    height = np.max(wave_segment) - np.min(wave_segment)
                    period = (end_idx - start_idx) / 32.0  # 32 Hz
                    
                    wave_heights.append(height)
                    wave_periods.append(period)
                    
            if not wave_heights:
                results[f'channel_{i+1}'] = self._empty_goda_metrics()
                continue
                
            wave_heights = np.array(wave_heights)
            wave_periods = np.array(wave_periods)
            
            # Tri par hauteur décroissante
            sorted_heights = np.sort(wave_heights)[::-1]
            
            # Métriques Goda
            n_waves = len(wave_heights)
            
            # Hs (hauteur significative) = moyenne du tiers supérieur
            n_third = max(1, n_waves // 3)
            hs = np.mean(sorted_heights[:n_third])
            
            # H1/3 (identique à Hs)
            h13 = hs
            
            # Tp (période de pic)
            tp = np.mean(wave_periods)
            
            # Cr (Crest factor)
            cr = np.max(wave_heights) / np.mean(wave_heights) if np.mean(wave_heights) > 0 else 0
            
            # Sk (Skewness)
            sk = self._compute_skewness(channel_data)
            
            # Ku (Kurtosis)
            ku = self._compute_kurtosis(channel_data)
            
            results[f'channel_{i+1}'] = {
                'Hs': hs,
                'H13': h13,
                'Tp': tp,
                'Cr': cr,
                'Sk': sk,
                'Ku': ku,
                'n_waves': n_waves,
                'mean_height': np.mean(wave_heights),
                'max_height': np.max(wave_heights),
                'mean_period': np.mean(wave_periods)
            }
            
        return results
        
    def _empty_goda_metrics(self) -> Dict[str, float]:
        """Métriques vides en cas d'erreur"""
        return {
            'Hs': 0.0, 'H13': 0.0, 'Tp': 0.0, 'Cr': 0.0, 'Sk': 0.0, 'Ku': 0.0,
            'n_waves': 0, 'mean_height': 0.0, 'max_height': 0.0, 'mean_period': 0.0
        }
        
    def _compute_skewness(self, data: np.ndarray) -> float:
        """Calcule l'asymétrie (skewness)"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std) ** 3)
        
    def _compute_kurtosis(self, data: np.ndarray) -> float:
        """Calcule l'aplatissement (kurtosis)"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std) ** 4) - 3.0

class AnalysisView(QWidget):
    """Vue d'analyse post-acquisition
    
    Fonctionnalités:
    - S'ouvre automatiquement après Stop
    - Spectres FFT, analyse Goda (plots)
    - Tableau complet Hs, H1/3, Tp, Cr, Sk, Ku
    - Export CSV/PDF/HDF5, log détaillé
    - Interface responsive sans scroll
    """
    
    # Signaux
    analysisCompleted = pyqtSignal(dict)
    exportCompleted = pyqtSignal(str)
    
    def __init__(self, filepath: str, config: Dict[str, Any], post_processor: Optional[PostProcessor] = None):
        super().__init__()
        self.filepath = filepath
        self.config = config
        self.post_processor = post_processor
        
        # Résultats analyse
        self.analysis_results = None
        
        # Worker thread
        self.analysis_worker = None
        self.analysis_thread = None
        
        self._init_ui()
        self._start_analysis()
        
    def _init_ui(self):
        """Initialise l'interface d'analyse"""
        self.setWindowTitle(f"HRNeoWave - Analyse: {os.path.basename(self.filepath)}")
        
        # Taille optimale pour analyse
        self.setMinimumSize(1024, 640)
        self.resize(1400, 800)
        
        self._create_layout()
        self._apply_analysis_theme()
        
    def _create_layout(self):
        """Layout principal avec onglets"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(True)
        main_layout.addWidget(self.progress_bar)
        
        # Onglets principaux
        self.tab_widget = QTabWidget()
        
        # Onglet Spectres
        self.spectrum_tab = self._create_spectrum_tab()
        self.tab_widget.addTab(self.spectrum_tab, "📊 Spectres FFT")
        
        # Onglet Goda
        self.goda_tab = self._create_goda_tab()
        self.tab_widget.addTab(self.goda_tab, "🌊 Analyse Goda")
        
        # Onglet Export
        self.export_tab = self._create_export_tab()
        self.tab_widget.addTab(self.export_tab, "💾 Export")
        
        main_layout.addWidget(self.tab_widget)
        
        # Initialement désactivé
        self.tab_widget.setEnabled(False)
        
    def _create_spectrum_tab(self) -> QWidget:
        """Onglet spectres FFT"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Contrôles
        controls_layout = QHBoxLayout()
        
        self.channel_selector = QComboBox()
        self.channel_selector.addItems([f"Sonde {i+1}" for i in range(4)])
        self.channel_selector.currentTextChanged.connect(self._update_spectrum_plot)
        
        self.log_scale_cb = QCheckBox("Échelle log")
        self.log_scale_cb.toggled.connect(self._update_spectrum_plot)
        
        controls_layout.addWidget(QLabel("Canal:"))
        controls_layout.addWidget(self.channel_selector)
        controls_layout.addWidget(self.log_scale_cb)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Graphique spectre
        self.spectrum_plot = PlotWidget()
        self.spectrum_plot.setLabel('left', 'Densité spectrale', units='m²/Hz')
        self.spectrum_plot.setLabel('bottom', 'Fréquence', units='Hz')
        self.spectrum_plot.showGrid(x=True, y=True)
        
        layout.addWidget(self.spectrum_plot)
        
        # Stats spectrales
        stats_group = QGroupBox("Statistiques spectrales")
        stats_layout = QFormLayout(stats_group)
        
        self.peak_freq_label = QLabel("--")
        self.total_energy_label = QLabel("--")
        self.bandwidth_label = QLabel("--")
        
        stats_layout.addRow("Fréquence de pic:", self.peak_freq_label)
        stats_layout.addRow("Énergie totale:", self.total_energy_label)
        stats_layout.addRow("Largeur de bande:", self.bandwidth_label)
        
        layout.addWidget(stats_group)
        
        return tab
        
    def _create_goda_tab(self) -> QWidget:
        """Onglet analyse Goda"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Splitter vertical
        splitter = QSplitter(Qt.Vertical)
        
        # Tableau métriques
        self.goda_table = QTableWidget()
        self.goda_table.setColumnCount(7)
        self.goda_table.setHorizontalHeaderLabels(['Canal', 'Hs (m)', 'H1/3 (m)', 'Tp (s)', 'Cr', 'Sk', 'Ku'])
        
        # Ajuster colonnes
        header = self.goda_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        splitter.addWidget(self.goda_table)
        
        # Graphique distribution hauteurs
        self.height_dist_plot = PlotWidget()
        self.height_dist_plot.setLabel('left', 'Fréquence')
        self.height_dist_plot.setLabel('bottom', 'Hauteur de vague', units='m')
        self.height_dist_plot.showGrid(x=True, y=True)
        
        splitter.addWidget(self.height_dist_plot)
        
        # Proportions 60% tableau / 40% graphique
        splitter.setStretchFactor(0, 60)
        splitter.setStretchFactor(1, 40)
        
        layout.addWidget(splitter)
        
        return tab
        
    def _create_export_tab(self) -> QWidget:
        """Onglet export et log"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Contrôles export
        export_group = QGroupBox("Export des résultats")
        export_layout = QVBoxLayout(export_group)
        
        # Boutons export
        buttons_layout = QHBoxLayout()
        
        self.export_csv_btn = QPushButton("📄 Export CSV")
        self.export_csv_btn.clicked.connect(lambda: self._export_results('csv'))
        
        self.export_pdf_btn = QPushButton("📋 Export PDF")
        self.export_pdf_btn.clicked.connect(lambda: self._export_results('pdf'))
        
        self.export_hdf5_btn = QPushButton("🗃️ Export HDF5")
        self.export_hdf5_btn.clicked.connect(lambda: self._export_results('hdf5'))
        
        buttons_layout.addWidget(self.export_csv_btn)
        buttons_layout.addWidget(self.export_pdf_btn)
        buttons_layout.addWidget(self.export_hdf5_btn)
        buttons_layout.addStretch()
        
        export_layout.addLayout(buttons_layout)
        
        # Options export
        options_layout = QHBoxLayout()
        
        self.include_raw_data_cb = QCheckBox("Inclure données brutes")
        self.include_raw_data_cb.setChecked(True)
        
        self.include_plots_cb = QCheckBox("Inclure graphiques")
        self.include_plots_cb.setChecked(True)
        
        options_layout.addWidget(self.include_raw_data_cb)
        options_layout.addWidget(self.include_plots_cb)
        options_layout.addStretch()
        
        export_layout.addLayout(options_layout)
        layout.addWidget(export_group)
        
        # Log détaillé
        log_group = QGroupBox("Log d'analyse")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group)
        
        # Désactiver initialement
        export_group.setEnabled(False)
        self.export_group = export_group
        
        return tab
        
    def _apply_analysis_theme(self):
        """Thème pour l'analyse"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #3d3d3d;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #2196F3;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 4px;
            }
            QTableWidget {
                gridline-color: #444;
                selection-background-color: #2196F3;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: #ffffff;
                padding: 4px;
                border: 1px solid #444;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2196F3;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        
    def _start_analysis(self):
        """Lance l'analyse en arrière-plan"""
        self._log("🚀 Démarrage de l'analyse...")
        
        # Créer worker et thread
        self.analysis_worker = AnalysisWorker(self.filepath, self.post_processor)
        self.analysis_thread = QThread()
        
        # Connecter signaux
        self.analysis_worker.moveToThread(self.analysis_thread)
        self.analysis_worker.analysisProgress.connect(self.progress_bar.setValue)
        self.analysis_worker.analysisComplete.connect(self._on_analysis_complete)
        self.analysis_worker.analysisError.connect(self._on_analysis_error)
        
        self.analysis_thread.started.connect(self.analysis_worker.run_analysis)
        
        # Démarrer
        self.analysis_thread.start()
        
    def _on_analysis_complete(self, results: Dict[str, Any]):
        """Analyse terminée avec succès"""
        self.analysis_results = results
        
        self._log("✅ Analyse terminée avec succès")
        
        # Masquer barre de progression
        self.progress_bar.setVisible(False)
        
        # Activer interface
        self.tab_widget.setEnabled(True)
        self.export_group.setEnabled(True)
        
        # Mettre à jour affichages
        self._update_spectrum_plot()
        self._update_goda_table()
        
        # Nettoyer thread
        self.analysis_thread.quit()
        self.analysis_thread.wait()
        
        # Signal
        self.analysisCompleted.emit(results)
        
    def _on_analysis_error(self, error: str):
        """Erreur d'analyse"""
        self._log(f"❌ Erreur d'analyse: {error}")
        
        # Masquer barre de progression
        self.progress_bar.setVisible(False)
        
        # Message d'erreur
        QMessageBox.critical(self, "Erreur d'analyse", f"Erreur lors de l'analyse:\n{error}")
        
        # Nettoyer thread
        if self.analysis_thread:
            self.analysis_thread.quit()
            self.analysis_thread.wait()
            
    def _update_spectrum_plot(self):
        """Met à jour le graphique de spectre"""
        if not self.analysis_results:
            return
            
        # Canal sélectionné
        channel_idx = self.channel_selector.currentIndex()
        channel_key = f'channel_{channel_idx + 1}'
        
        spectrum_data = self.analysis_results['spectrum'].get(channel_key)
        if not spectrum_data:
            return
            
        # Données
        freqs = spectrum_data['frequencies']
        spectrum = spectrum_data['spectrum']
        
        # Échelle log si demandée
        if self.log_scale_cb.isChecked():
            spectrum = np.log10(spectrum + 1e-10)  # Éviter log(0)
            
        # Tracer
        self.spectrum_plot.clear()
        self.spectrum_plot.plot(freqs, spectrum, pen=mkPen('#2196F3', width=2))
        
        # Marquer pic
        peak_freq = spectrum_data['peak_freq']
        peak_idx = np.argmin(np.abs(freqs - peak_freq))
        if peak_idx < len(spectrum):
            peak_value = spectrum[peak_idx]
            self.spectrum_plot.plot([peak_freq], [peak_value], 
                                  symbol='o', symbolBrush='red', symbolSize=8)
                                  
        # Mettre à jour stats
        self.peak_freq_label.setText(f"{peak_freq:.3f} Hz")
        self.total_energy_label.setText(f"{spectrum_data['total_energy']:.2e}")
        
        # Largeur de bande (approximative)
        bandwidth = freqs[-1] - freqs[0]
        self.bandwidth_label.setText(f"{bandwidth:.3f} Hz")
        
    def _update_goda_table(self):
        """Met à jour le tableau Goda"""
        if not self.analysis_results:
            return
            
        goda_data = self.analysis_results['goda']
        
        # Configurer tableau
        n_channels = len(goda_data)
        self.goda_table.setRowCount(n_channels)
        
        # Remplir données
        for i, (channel_key, metrics) in enumerate(goda_data.items()):
            channel_name = f"Sonde {i+1}"
            
            self.goda_table.setItem(i, 0, QTableWidgetItem(channel_name))
            self.goda_table.setItem(i, 1, QTableWidgetItem(f"{metrics['Hs']:.3f}"))
            self.goda_table.setItem(i, 2, QTableWidgetItem(f"{metrics['H13']:.3f}"))
            self.goda_table.setItem(i, 3, QTableWidgetItem(f"{metrics['Tp']:.2f}"))
            self.goda_table.setItem(i, 4, QTableWidgetItem(f"{metrics['Cr']:.2f}"))
            self.goda_table.setItem(i, 5, QTableWidgetItem(f"{metrics['Sk']:.3f}"))
            self.goda_table.setItem(i, 6, QTableWidgetItem(f"{metrics['Ku']:.3f}"))
            
        # Ajuster taille
        self.goda_table.resizeColumnsToContents()
        
    def _export_results(self, format_type: str):
        """Exporte les résultats dans le format demandé"""
        if not self.analysis_results:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"analysis_HRNeoWave_{timestamp}"
        
        try:
            if format_type == 'csv':
                filepath = self._export_csv(base_name)
            elif format_type == 'pdf':
                filepath = self._export_pdf(base_name)
            elif format_type == 'hdf5':
                filepath = self._export_hdf5(base_name)
            else:
                raise ValueError(f"Format non supporté: {format_type}")
                
            self._log(f"✅ Export {format_type.upper()} réussi: {filepath}")
            self.exportCompleted.emit(filepath)
            
            # Message de confirmation
            QMessageBox.information(self, "Export réussi", 
                                  f"Fichier exporté:\n{filepath}")
                                  
        except Exception as e:
            error_msg = f"Erreur export {format_type.upper()}: {e}"
            self._log(f"❌ {error_msg}")
            QMessageBox.critical(self, "Erreur d'export", error_msg)
            
    def _export_csv(self, base_name: str) -> str:
        """Export CSV des métriques Goda"""
        filepath = f"{base_name}.csv"
        
        # Créer DataFrame
        rows = []
        for channel_key, metrics in self.analysis_results['goda'].items():
            row = {'Canal': channel_key}
            row.update(metrics)
            rows.append(row)
            
        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False)
        
        return filepath
        
    def _export_pdf(self, base_name: str) -> str:
        """Export PDF (placeholder - nécessite reportlab)"""
        filepath = f"{base_name}.pdf"
        
        # Pour l'instant, export texte simple
        with open(filepath.replace('.pdf', '.txt'), 'w') as f:
            f.write("=== RAPPORT D'ANALYSE HRNEOWAVE ===\n\n")
            f.write(f"Fichier source: {self.filepath}\n")
            f.write(f"Date d'analyse: {self.analysis_results['timestamp']}\n\n")
            
            f.write("=== MÉTRIQUES GODA ===\n")
            for channel_key, metrics in self.analysis_results['goda'].items():
                f.write(f"\n{channel_key}:\n")
                for key, value in metrics.items():
                    f.write(f"  {key}: {value}\n")
                    
        return filepath.replace('.pdf', '.txt')
        
    def _export_hdf5(self, base_name: str) -> str:
        """Export HDF5 (placeholder - nécessite h5py)"""
        filepath = f"{base_name}.h5"
        
        # Pour l'instant, export JSON
        import json
        json_filepath = filepath.replace('.h5', '.json')
        
        with open(json_filepath, 'w') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
            
        return json_filepath
        
    def _log(self, message: str):
        """Ajoute un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        self.log_text.append(log_entry)
        
        # Auto-scroll
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        self.log_text.setTextCursor(cursor)

# Test standalone
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Fichier test (créer si nécessaire)
    test_file = "test_data.csv"
    if not os.path.exists(test_file):
        # Créer données test
        t = np.linspace(0, 100, 3200)  # 100s à 32Hz
        data = {
            'Time': t,
            'Sonde_1': 0.5 * np.sin(2*np.pi*0.1*t) + 0.1*np.random.randn(len(t)),
            'Sonde_2': 0.3 * np.sin(2*np.pi*0.15*t) + 0.1*np.random.randn(len(t)),
            'Sonde_3': 0.4 * np.sin(2*np.pi*0.12*t) + 0.1*np.random.randn(len(t)),
            'Sonde_4': 0.6 * np.sin(2*np.pi*0.08*t) + 0.1*np.random.randn(len(t))
        }
        pd.DataFrame(data).to_csv(test_file, index=False)
        
    config = {'sample_rate': 32.0}
    
    view = AnalysisView(test_file, config)
    view.show()
    
    sys.exit(app.exec_())