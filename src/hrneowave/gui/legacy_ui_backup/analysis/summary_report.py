# -*- coding: utf-8 -*-
"""
Widget de rapport de synthèse CHNeoWave
Extrait de analysis_view.py pour une meilleure modularité
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QFormLayout, QComboBox, QCheckBox,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

from datetime import datetime
import json
import os


class SummaryReportWidget(QWidget):
    """
    Widget spécialisé pour la génération de rapports de synthèse
    Responsabilité unique : compilation et export des résultats d'analyse
    """
    
    reportGenerated = Signal(dict)  # Signal émis quand le rapport est généré
    exportRequested = Signal(str)   # Signal émis pour demander l'export
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session_data = None
        self.analysis_results = {
            'spectral': {},
            'goda': {},
            'statistics': {}
        }
        self.report_content = ""
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur pour le rapport
        """
        layout = QVBoxLayout(self)
        
        # Paramètres du rapport
        params_group = self._createParametersWidget()
        layout.addWidget(params_group)
        
        # Zone du rapport
        report_group = self._createReportWidget()
        layout.addWidget(report_group)
        
        # Boutons d'action
        buttons_layout = self._createButtonsWidget()
        layout.addLayout(buttons_layout)
    
    def _createParametersWidget(self):
        """
        Création de la zone des paramètres du rapport
        """
        params_group = QGroupBox("Paramètres du Rapport")
        params_layout = QFormLayout(params_group)
        
        # Format du rapport
        self.report_format_combo = QComboBox()
        self.report_format_combo.addItems(["Rapport complet", "Résumé exécutif", "Données techniques"])
        params_layout.addRow("Format:", self.report_format_combo)
        
        # Sections à inclure
        self.include_spectral_check = QCheckBox("Analyse spectrale")
        self.include_spectral_check.setChecked(True)
        params_layout.addRow("Inclure:", self.include_spectral_check)
        
        self.include_goda_check = QCheckBox("Analyse de Goda")
        self.include_goda_check.setChecked(True)
        params_layout.addRow("", self.include_goda_check)
        
        self.include_statistics_check = QCheckBox("Statistiques")
        self.include_statistics_check.setChecked(True)
        params_layout.addRow("", self.include_statistics_check)
        
        self.include_graphs_check = QCheckBox("Graphiques")
        self.include_graphs_check.setChecked(True)
        params_layout.addRow("", self.include_graphs_check)
        
        # Langue du rapport
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Français", "English"])
        params_layout.addRow("Langue:", self.language_combo)
        
        return params_group
    
    def _createReportWidget(self):
        """
        Création de la zone d'affichage du rapport
        """
        report_group = QGroupBox("Rapport de Synthèse")
        report_layout = QVBoxLayout(report_group)
        
        self.report_text = QTextEdit()
        self.report_text.setMinimumHeight(400)
        self.report_text.setReadOnly(True)
        self.report_text.setPlainText("Cliquez sur 'Générer Rapport' pour créer le rapport de synthèse.")
        
        report_layout.addWidget(self.report_text)
        
        return report_group
    
    def _createButtonsWidget(self):
        """
        Création des boutons d'action
        """
        buttons_layout = QHBoxLayout()
        
        self.generate_report_btn = QPushButton("Générer Rapport")
        self.generate_report_btn.setMinimumHeight(35)
        buttons_layout.addWidget(self.generate_report_btn)
        
        self.export_pdf_btn = QPushButton("Exporter en PDF")
        self.export_pdf_btn.setMinimumHeight(35)
        self.export_pdf_btn.setEnabled(False)
        buttons_layout.addWidget(self.export_pdf_btn)
        
        self.export_json_btn = QPushButton("Exporter JSON")
        self.export_json_btn.setMinimumHeight(35)
        self.export_json_btn.setEnabled(False)
        buttons_layout.addWidget(self.export_json_btn)
        
        buttons_layout.addStretch()
        
        return buttons_layout
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        self.generate_report_btn.clicked.connect(self.generateSummaryReport)
        self.export_pdf_btn.clicked.connect(self.exportToPDF)
        self.export_json_btn.clicked.connect(self.exportToJSON)
        self.report_format_combo.currentTextChanged.connect(self.onFormatChanged)
    
    def setSessionData(self, session_data):
        """
        Configuration des données de session
        """
        self.session_data = session_data
    
    def setAnalysisResults(self, analysis_type, results):
        """
        Configuration des résultats d'analyse
        """
        if analysis_type in self.analysis_results:
            self.analysis_results[analysis_type] = results
            
            # Vérifier si toutes les analyses sont disponibles
            if self._allAnalysesComplete():
                self.generate_report_btn.setEnabled(True)
    
    def _allAnalysesComplete(self):
        """
        Vérifie si toutes les analyses sont complètes
        """
        return (bool(self.analysis_results.get('spectral')) and 
                bool(self.analysis_results.get('goda')) and 
                bool(self.analysis_results.get('statistics')))
    
    def onFormatChanged(self):
        """
        Gestion du changement de format de rapport
        """
        if self.report_content:
            self.generateSummaryReport()
    
    def generateSummaryReport(self):
        """
        Génération du rapport de synthèse
        """
        if not self.session_data:
            QMessageBox.warning(self, "Erreur", "Aucune donnée de session disponible.")
            return
        
        try:
            report_format = self.report_format_combo.currentText()
            language = self.language_combo.currentText()
            
            if report_format == "Rapport complet":
                self.report_content = self._createFullReport(language)
            elif report_format == "Résumé exécutif":
                self.report_content = self._createExecutiveSummary(language)
            else:  # Données techniques
                self.report_content = self._createTechnicalReport(language)
            
            self.report_text.setPlainText(self.report_content)
            
            # Activer les boutons d'export
            self.export_pdf_btn.setEnabled(True)
            self.export_json_btn.setEnabled(True)
            
            # Émettre le signal
            report_data = {
                'content': self.report_content,
                'format': report_format,
                'language': language,
                'timestamp': datetime.now().isoformat()
            }
            self.reportGenerated.emit(report_data)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du rapport: {str(e)}")
    
    def _createFullReport(self, language="Français"):
        """
        Création du rapport complet
        """
        if language == "English":
            return self._createFullReportEN()
        else:
            return self._createFullReportFR()
    
    def _createFullReportFR(self):
        """
        Rapport complet en français
        """
        report = f"""RAPPORT D'ANALYSE CHNeoWave
{'='*50}

Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Projet: {self.session_data.get('project_name', 'Projet Test')}
Durée d'acquisition: {self.session_data.get('duration', 0):.1f} s
Fréquence d'échantillonnage: {self.session_data.get('sample_rate', 100)} Hz

"""
        
        # Informations générales
        report += self._addGeneralInfoFR()
        
        # Résultats spectraux
        if self.include_spectral_check.isChecked() and self.analysis_results.get('spectral'):
            report += self._addSpectralResultsFR()
        
        # Résultats de Goda
        if self.include_goda_check.isChecked() and self.analysis_results.get('goda'):
            report += self._addGodaResultsFR()
        
        # Statistiques
        if self.include_statistics_check.isChecked() and self.analysis_results.get('statistics'):
            report += self._addStatisticsResultsFR()
        
        # Conclusions
        report += self._addConclusionsFR()
        
        return report
    
    def _createFullReportEN(self):
        """
        Rapport complet en anglais
        """
        report = f"""CHNeoWave ANALYSIS REPORT
{'='*50}

Generation date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Project: {self.session_data.get('project_name', 'Test Project')}
Acquisition duration: {self.session_data.get('duration', 0):.1f} s
Sampling frequency: {self.session_data.get('sample_rate', 100)} Hz

"""
        
        # Informations générales
        report += self._addGeneralInfoEN()
        
        # Résultats spectraux
        if self.include_spectral_check.isChecked() and self.analysis_results.get('spectral'):
            report += self._addSpectralResultsEN()
        
        # Résultats de Goda
        if self.include_goda_check.isChecked() and self.analysis_results.get('goda'):
            report += self._addGodaResultsEN()
        
        # Statistiques
        if self.include_statistics_check.isChecked() and self.analysis_results.get('statistics'):
            report += self._addStatisticsResultsEN()
        
        # Conclusions
        report += self._addConclusionsEN()
        
        return report
    
    def _createExecutiveSummary(self, language="Français"):
        """
        Création du résumé exécutif
        """
        if language == "English":
            title = "EXECUTIVE SUMMARY"
            intro = "Key findings from the CHNeoWave analysis:"
        else:
            title = "RÉSUMÉ EXÉCUTIF"
            intro = "Principales conclusions de l'analyse CHNeoWave:"
        
        summary = f"""{title}
{'='*30}

{intro}

"""
        
        # Résultats clés
        if self.analysis_results.get('goda'):
            goda = self.analysis_results['goda']
            if language == "English":
                summary += f"Wave Analysis:\n"
                summary += f"- Number of waves: {goda.get('n_waves', 0)}\n"
                summary += f"- Maximum height: {goda.get('h_max', 0):.3f} m\n"
                summary += f"- Significant height (H1/3): {goda.get('h_13', 0):.3f} m\n\n"
            else:
                summary += f"Analyse des vagues:\n"
                summary += f"- Nombre de vagues: {goda.get('n_waves', 0)}\n"
                summary += f"- Hauteur maximale: {goda.get('h_max', 0):.3f} m\n"
                summary += f"- Hauteur significative (H1/3): {goda.get('h_13', 0):.3f} m\n\n"
        
        if self.analysis_results.get('statistics'):
            stats = self.analysis_results['statistics'].get('descriptive_stats', {})
            if language == "English":
                summary += f"Statistical Analysis:\n"
                summary += f"- Mean amplitude: {stats.get('mean', 0):.3f}\n"
                summary += f"- Standard deviation: {stats.get('std', 0):.3f}\n\n"
            else:
                summary += f"Analyse statistique:\n"
                summary += f"- Amplitude moyenne: {stats.get('mean', 0):.3f}\n"
                summary += f"- Écart-type: {stats.get('std', 0):.3f}\n\n"
        
        return summary
    
    def _createTechnicalReport(self, language="Français"):
        """
        Création du rapport technique
        """
        if language == "English":
            title = "TECHNICAL DATA REPORT"
        else:
            title = "RAPPORT TECHNIQUE DÉTAILLÉ"
        
        report = f"""{title}
{'='*40}

"""
        
        # Données brutes des analyses
        for analysis_type, results in self.analysis_results.items():
            if results:
                report += f"\n{analysis_type.upper()} ANALYSIS:\n"
                report += f"{'-'*20}\n"
                report += json.dumps(results, indent=2, ensure_ascii=False)
                report += "\n\n"
        
        return report
    
    def _addGeneralInfoFR(self):
        """
        Ajout des informations générales en français
        """
        sensor_data = self.session_data.get('sensor_data', [])
        
        info = f"""1. INFORMATIONS GÉNÉRALES
{'-'*30}

Configuration d'acquisition:
- Nombre de capteurs: {len(sensor_data)}
- Nombre d'échantillons par capteur: {len(sensor_data[0]) if sensor_data else 0}
- Résolution temporelle: {1/self.session_data.get('sample_rate', 100):.4f} s

Conditions d'essai:
- Type d'essai: {self.session_data.get('test_type', 'Non spécifié')}
- Commentaires: {self.session_data.get('comments', 'Aucun')}

"""
        
        return info
    
    def _addGeneralInfoEN(self):
        """
        Ajout des informations générales en anglais
        """
        sensor_data = self.session_data.get('sensor_data', [])
        
        info = f"""1. GENERAL INFORMATION
{'-'*25}

Acquisition setup:
- Number of sensors: {len(sensor_data)}
- Samples per sensor: {len(sensor_data[0]) if sensor_data else 0}
- Time resolution: {1/self.session_data.get('sample_rate', 100):.4f} s

Test conditions:
- Test type: {self.session_data.get('test_type', 'Not specified')}
- Comments: {self.session_data.get('comments', 'None')}

"""
        
        return info
    
    def _addSpectralResultsFR(self):
        """
        Ajout des résultats spectraux en français
        """
        spectral = self.analysis_results['spectral']
        params = spectral.get('parameters', {})
        
        results = f"""2. ANALYSE SPECTRALE
{'-'*20}

Paramètres d'analyse:
- Taille de fenêtre: {params.get('window_size', 'N/A')}
- Recouvrement: {params.get('overlap', 'N/A')*100:.0f}%
- Type de fenêtre: {params.get('window_type', 'N/A')}

Résultats:
- Nombre de spectres calculés: {len(spectral.get('spectra', []))}
- Résolution fréquentielle: {len(spectral.get('frequencies', []))} points

"""
        
        return results
    
    def _addSpectralResultsEN(self):
        """
        Ajout des résultats spectraux en anglais
        """
        spectral = self.analysis_results['spectral']
        params = spectral.get('parameters', {})
        
        results = f"""2. SPECTRAL ANALYSIS
{'-'*18}

Analysis parameters:
- Window size: {params.get('window_size', 'N/A')}
- Overlap: {params.get('overlap', 'N/A')*100:.0f}%
- Window type: {params.get('window_type', 'N/A')}

Results:
- Number of computed spectra: {len(spectral.get('spectra', []))}
- Frequency resolution: {len(spectral.get('frequencies', []))} points

"""
        
        return results
    
    def _addGodaResultsFR(self):
        """
        Ajout des résultats de Goda en français
        """
        goda = self.analysis_results['goda']
        
        results = f"""3. ANALYSE DE GODA
{'-'*17}

Statistiques des vagues:
- Nombre de vagues détectées: {goda.get('n_waves', 0)}
- Hauteur maximale (Hmax): {goda.get('h_max', 0):.3f} m
- Hauteur moyenne (Hmean): {goda.get('h_mean', 0):.3f} m
- Hauteur significative (H1/3): {goda.get('h_13', 0):.3f} m
- Hauteur 1/10 (H1/10): {goda.get('h_110', 0):.3f} m

Ratios caractéristiques:
- H1/3/Hmean: {goda.get('ratios', {}).get('h13_hmean', 0):.2f}
- Hmax/H1/3: {goda.get('ratios', {}).get('hmax_h13', 0):.2f}

"""
        
        return results
    
    def _addGodaResultsEN(self):
        """
        Ajout des résultats de Goda en anglais
        """
        goda = self.analysis_results['goda']
        
        results = f"""3. GODA ANALYSIS
{'-'*14}

Wave statistics:
- Number of detected waves: {goda.get('n_waves', 0)}
- Maximum height (Hmax): {goda.get('h_max', 0):.3f} m
- Mean height (Hmean): {goda.get('h_mean', 0):.3f} m
- Significant height (H1/3): {goda.get('h_13', 0):.3f} m
- 1/10 height (H1/10): {goda.get('h_110', 0):.3f} m

Characteristic ratios:
- H1/3/Hmean: {goda.get('ratios', {}).get('h13_hmean', 0):.2f}
- Hmax/H1/3: {goda.get('ratios', {}).get('hmax_h13', 0):.2f}

"""
        
        return results
    
    def _addStatisticsResultsFR(self):
        """
        Ajout des résultats statistiques en français
        """
        stats = self.analysis_results['statistics']
        desc_stats = stats.get('descriptive_stats', {})
        
        results = f"""4. ANALYSE STATISTIQUE
{'-'*21}

Statistiques descriptives:
- Moyenne: {desc_stats.get('mean', 0):.3f}
- Écart-type: {desc_stats.get('std', 0):.3f}
- Médiane: {desc_stats.get('median', 0):.3f}
- Asymétrie: {desc_stats.get('skewness', 0):.3f}
- Aplatissement: {desc_stats.get('kurtosis', 0):.3f}

Tests de normalité:
"""
        
        # Tests de normalité
        tests = stats.get('statistical_tests', {})
        if 'shapiro' in tests:
            shapiro = tests['shapiro']
            results += f"- Shapiro-Wilk: p = {shapiro['p_value']:.4f} ({'Normal' if shapiro['is_normal'] else 'Non normal'})\n"
        
        if 'kolmogorov_smirnov' in tests:
            ks = tests['kolmogorov_smirnov']
            results += f"- Kolmogorov-Smirnov: p = {ks['p_value']:.4f} ({'Normal' if ks['is_normal'] else 'Non normal'})\n"
        
        results += "\n"
        
        return results
    
    def _addStatisticsResultsEN(self):
        """
        Ajout des résultats statistiques en anglais
        """
        stats = self.analysis_results['statistics']
        desc_stats = stats.get('descriptive_stats', {})
        
        results = f"""4. STATISTICAL ANALYSIS
{'-'*21}

Descriptive statistics:
- Mean: {desc_stats.get('mean', 0):.3f}
- Standard deviation: {desc_stats.get('std', 0):.3f}
- Median: {desc_stats.get('median', 0):.3f}
- Skewness: {desc_stats.get('skewness', 0):.3f}
- Kurtosis: {desc_stats.get('kurtosis', 0):.3f}

Normality tests:
"""
        
        # Tests de normalité
        tests = stats.get('statistical_tests', {})
        if 'shapiro' in tests:
            shapiro = tests['shapiro']
            results += f"- Shapiro-Wilk: p = {shapiro['p_value']:.4f} ({'Normal' if shapiro['is_normal'] else 'Non-normal'})\n"
        
        if 'kolmogorov_smirnov' in tests:
            ks = tests['kolmogorov_smirnov']
            results += f"- Kolmogorov-Smirnov: p = {ks['p_value']:.4f} ({'Normal' if ks['is_normal'] else 'Non-normal'})\n"
        
        results += "\n"
        
        return results
    
    def _addConclusionsFR(self):
        """
        Ajout des conclusions en français
        """
        conclusions = f"""5. CONCLUSIONS
{'-'*12}

L'analyse CHNeoWave a permis de caractériser les données acquises selon trois approches complémentaires:

- L'analyse spectrale révèle les caractéristiques fréquentielles du signal
- L'analyse de Goda fournit les paramètres statistiques des vagues
- L'analyse statistique évalue la distribution et la normalité des données

Ces résultats constituent une base solide pour l'interprétation physique des phénomènes observés.

Rapport généré automatiquement par CHNeoWave v2.0.0
"""
        
        return conclusions
    
    def _addConclusionsEN(self):
        """
        Ajout des conclusions en anglais
        """
        conclusions = f"""5. CONCLUSIONS
{'-'*12}

The CHNeoWave analysis has characterized the acquired data using three complementary approaches:

- Spectral analysis reveals the frequency characteristics of the signal
- Goda analysis provides statistical parameters of waves
- Statistical analysis evaluates data distribution and normality

These results provide a solid foundation for physical interpretation of observed phenomena.

Report automatically generated by CHNeoWave v2.0.0
"""
        
        return conclusions
    
    def exportToPDF(self):
        """
        Export du rapport en PDF
        """
        if not self.report_content:
            QMessageBox.warning(self, "Erreur", "Aucun rapport à exporter. Générez d'abord un rapport.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter le rapport en PDF", 
            f"rapport_chneowave_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "Fichiers PDF (*.pdf)"
        )
        
        if file_path:
            self.exportRequested.emit(file_path)
    
    def exportToJSON(self):
        """
        Export des données en JSON
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter les données en JSON", 
            f"donnees_chneowave_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "Fichiers JSON (*.json)"
        )
        
        if file_path:
            try:
                export_data = {
                    'session_data': self.session_data,
                    'analysis_results': self.analysis_results,
                    'report_content': self.report_content,
                    'export_timestamp': datetime.now().isoformat()
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                QMessageBox.information(self, "Export réussi", f"Données exportées vers:\n{file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur d'export", f"Erreur lors de l'export JSON:\n{str(e)}")
    
    def getReportContent(self):
        """
        Retourne le contenu du rapport
        """
        return self.report_content
    
    def resetReport(self):
        """
        Réinitialise le rapport
        """
        self.report_text.clear()
        self.report_content = ""
        self.export_pdf_btn.setEnabled(False)
        self.export_json_btn.setEnabled(False)