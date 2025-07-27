# -*- coding: utf-8 -*-
"""
Contrôleur d'analyse CHNeoWave
Coordonne les différents widgets d'analyse et gère les interactions
"""

from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QMessageBox

import numpy as np
from datetime import datetime
import logging


class AnalysisController(QObject):
    """
    Contrôleur principal pour coordonner les analyses
    Responsabilité : orchestration des analyses et communication entre widgets
    """
    
    # Signaux pour communication avec la vue principale
    analysisStarted = Signal(str)  # Type d'analyse démarrée
    analysisFinished = Signal(dict)  # Résultats complets
    analysisProgress = Signal(int)  # Progression (0-100)
    analysisError = Signal(str)  # Erreur d'analyse
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Widgets d'analyse
        self.spectral_widget = None
        self.goda_widget = None
        self.statistics_widget = None
        self.summary_widget = None
        
        # Données et résultats
        self.session_data = None
        self.analysis_results = {
            'spectral': {},
            'goda': {},
            'statistics': {},
            'metadata': {}
        }
        
        # État des analyses
        self.analysis_status = {
            'spectral': False,
            'goda': False,
            'statistics': False
        }
        
        # Timer pour les analyses asynchrones
        self.analysis_timer = QTimer()
        self.analysis_timer.timeout.connect(self._checkAnalysisProgress)
    
    def setWidgets(self, spectral_widget, goda_widget, statistics_widget, summary_widget):
        """
        Configuration des widgets d'analyse
        """
        self.spectral_widget = spectral_widget
        self.goda_widget = goda_widget
        self.statistics_widget = statistics_widget
        self.summary_widget = summary_widget
        
        # Connexion des signaux des widgets
        self._connectWidgetSignals()
    
    def _connectWidgetSignals(self):
        """
        Connexion des signaux des widgets
        """
        if self.spectral_widget:
            self.spectral_widget.analysisCompleted.connect(self._onSpectralAnalysisCompleted)
            self.spectral_widget.analysisError.connect(self._onAnalysisError)
        
        if self.goda_widget:
            self.goda_widget.analysisCompleted.connect(self._onGodaAnalysisCompleted)
            self.goda_widget.analysisError.connect(self._onAnalysisError)
        
        if self.statistics_widget:
            self.statistics_widget.analysisCompleted.connect(self._onStatisticsAnalysisCompleted)
            self.statistics_widget.analysisError.connect(self._onAnalysisError)
        
        if self.summary_widget:
            self.summary_widget.reportGenerated.connect(self._onReportGenerated)
            self.summary_widget.exportRequested.connect(self._onExportRequested)
    
    def setSessionData(self, session_data):
        """
        Configuration des données de session pour tous les widgets
        """
        self.session_data = session_data
        
        # Propager aux widgets
        if self.spectral_widget:
            self.spectral_widget.setSessionData(session_data)
        
        if self.goda_widget:
            self.goda_widget.setSessionData(session_data)
        
        if self.statistics_widget:
            self.statistics_widget.setSessionData(session_data)
        
        if self.summary_widget:
            self.summary_widget.setSessionData(session_data)
        
        # Réinitialiser l'état des analyses
        self._resetAnalysisStatus()
        
        self.logger.info(f"Données de session configurées: {len(session_data.get('sensor_data', []))} capteurs")
    
    def startSpectralAnalysis(self):
        """
        Démarrage de l'analyse spectrale
        """
        if not self.spectral_widget or not self.session_data:
            self.analysisError.emit("Widget spectral ou données non disponibles")
            return
        
        try:
            self.analysisStarted.emit("spectral")
            self.spectral_widget.performSpectralAnalysis()
            self.logger.info("Analyse spectrale démarrée")
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage de l'analyse spectrale: {e}")
            self.analysisError.emit(f"Erreur analyse spectrale: {str(e)}")
    
    def startGodaAnalysis(self):
        """
        Démarrage de l'analyse de Goda
        """
        if not self.goda_widget or not self.session_data:
            self.analysisError.emit("Widget Goda ou données non disponibles")
            return
        
        try:
            self.analysisStarted.emit("goda")
            self.goda_widget.performGodaAnalysis()
            self.logger.info("Analyse de Goda démarrée")
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage de l'analyse de Goda: {e}")
            self.analysisError.emit(f"Erreur analyse Goda: {str(e)}")
    
    def startStatisticsAnalysis(self):
        """
        Démarrage de l'analyse statistique
        """
        if not self.statistics_widget or not self.session_data:
            self.analysisError.emit("Widget statistiques ou données non disponibles")
            return
        
        try:
            self.analysisStarted.emit("statistics")
            self.statistics_widget.calculateStatistics()
            self.logger.info("Analyse statistique démarrée")
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage de l'analyse statistique: {e}")
            self.analysisError.emit(f"Erreur analyse statistique: {str(e)}")
    
    def startCompleteAnalysis(self):
        """
        Démarrage de l'analyse complète (toutes les analyses)
        """
        if not self.session_data:
            self.analysisError.emit("Aucune donnée de session disponible")
            return
        
        try:
            self.logger.info("Démarrage de l'analyse complète")
            self.analysisStarted.emit("complete")
            
            # Réinitialiser l'état
            self._resetAnalysisStatus()
            
            # Démarrer les analyses en séquence
            self.startSpectralAnalysis()
            
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage de l'analyse complète: {e}")
            self.analysisError.emit(f"Erreur analyse complète: {str(e)}")
    
    def _onSpectralAnalysisCompleted(self, results):
        """
        Gestion de la fin de l'analyse spectrale
        """
        self.analysis_results['spectral'] = results
        self.analysis_status['spectral'] = True
        
        # Propager aux autres widgets
        if self.summary_widget:
            self.summary_widget.setAnalysisResults('spectral', results)
        
        self.logger.info("Analyse spectrale terminée")
        
        # Démarrer l'analyse de Goda si analyse complète
        if self._isCompleteAnalysisRunning():
            self.startGodaAnalysis()
        
        self._checkAnalysisCompletion()
    
    def _onGodaAnalysisCompleted(self, results):
        """
        Gestion de la fin de l'analyse de Goda
        """
        self.analysis_results['goda'] = results
        self.analysis_status['goda'] = True
        
        # Propager aux autres widgets
        if self.summary_widget:
            self.summary_widget.setAnalysisResults('goda', results)
        
        self.logger.info("Analyse de Goda terminée")
        
        # Démarrer l'analyse statistique si analyse complète
        if self._isCompleteAnalysisRunning():
            self.startStatisticsAnalysis()
        
        self._checkAnalysisCompletion()
    
    def _onStatisticsAnalysisCompleted(self, results):
        """
        Gestion de la fin de l'analyse statistique
        """
        self.analysis_results['statistics'] = results
        self.analysis_status['statistics'] = True
        
        # Propager aux autres widgets
        if self.summary_widget:
            self.summary_widget.setAnalysisResults('statistics', results)
        
        self.logger.info("Analyse statistique terminée")
        
        self._checkAnalysisCompletion()
    
    def _onAnalysisError(self, error_message):
        """
        Gestion des erreurs d'analyse
        """
        self.logger.error(f"Erreur d'analyse: {error_message}")
        self.analysisError.emit(error_message)
    
    def _onReportGenerated(self, report_data):
        """
        Gestion de la génération de rapport
        """
        self.logger.info(f"Rapport généré: {report_data.get('format', 'Format inconnu')}")
    
    def _onExportRequested(self, file_path):
        """
        Gestion des demandes d'export
        """
        self.logger.info(f"Export demandé vers: {file_path}")
        # Ici, on pourrait implémenter la logique d'export PDF
    
    def _isCompleteAnalysisRunning(self):
        """
        Vérifie si une analyse complète est en cours
        """
        return not all(self.analysis_status.values())
    
    def _checkAnalysisCompletion(self):
        """
        Vérifie si toutes les analyses sont terminées
        """
        if all(self.analysis_status.values()):
            # Toutes les analyses sont terminées
            self._finalizeAnalysis()
    
    def _finalizeAnalysis(self):
        """
        Finalisation de l'analyse complète
        """
        try:
            # Ajouter les métadonnées
            self.analysis_results['metadata'] = {
                'completion_time': datetime.now().isoformat(),
                'session_info': {
                    'duration': self.session_data.get('duration', 0),
                    'sample_rate': self.session_data.get('sample_rate', 100),
                    'n_sensors': len(self.session_data.get('sensor_data', [])),
                    'n_samples': len(self.session_data.get('sensor_data', [[]])[0]) if self.session_data.get('sensor_data') else 0
                },
                'analysis_status': self.analysis_status.copy()
            }
            
            # Émettre le signal de fin d'analyse
            self.analysisFinished.emit(self.analysis_results)
            
            self.logger.info("Analyse complète terminée avec succès")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la finalisation: {e}")
            self.analysisError.emit(f"Erreur de finalisation: {str(e)}")
    
    def _resetAnalysisStatus(self):
        """
        Réinitialisation de l'état des analyses
        """
        self.analysis_status = {
            'spectral': False,
            'goda': False,
            'statistics': False
        }
        
        self.analysis_results = {
            'spectral': {},
            'goda': {},
            'statistics': {},
            'metadata': {}
        }
    
    def _checkAnalysisProgress(self):
        """
        Vérification du progrès des analyses (pour timer)
        """
        completed = sum(self.analysis_status.values())
        total = len(self.analysis_status)
        progress = int((completed / total) * 100)
        
        self.analysisProgress.emit(progress)
    
    def resetAnalysis(self):
        """
        Réinitialisation complète des analyses
        """
        try:
            # Réinitialiser les widgets
            if self.spectral_widget:
                self.spectral_widget.resetAnalysis()
            
            if self.goda_widget:
                self.goda_widget.resetAnalysis()
            
            if self.statistics_widget:
                self.statistics_widget.resetAnalysis()
            
            if self.summary_widget:
                self.summary_widget.resetReport()
            
            # Réinitialiser l'état
            self._resetAnalysisStatus()
            
            self.logger.info("Analyses réinitialisées")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la réinitialisation: {e}")
            self.analysisError.emit(f"Erreur de réinitialisation: {str(e)}")
    
    def getAnalysisResults(self):
        """
        Retourne les résultats d'analyse
        """
        return self.analysis_results.copy()
    
    def getAnalysisStatus(self):
        """
        Retourne l'état des analyses
        """
        return self.analysis_status.copy()
    
    def isAnalysisComplete(self):
        """
        Vérifie si l'analyse est complète
        """
        return all(self.analysis_status.values())
    
    def validateSessionData(self, session_data):
        """
        Validation des données de session
        """
        if not session_data:
            return False, "Aucune donnée de session"
        
        sensor_data = session_data.get('sensor_data', [])
        if not sensor_data:
            return False, "Aucune donnée de capteur"
        
        if len(sensor_data) == 0:
            return False, "Données de capteur vides"
        
        # Vérifier que tous les capteurs ont la même longueur
        lengths = [len(data) for data in sensor_data]
        if len(set(lengths)) > 1:
            return False, "Longueurs de données incohérentes entre capteurs"
        
        # Vérifier la fréquence d'échantillonnage
        sample_rate = session_data.get('sample_rate', 0)
        if sample_rate <= 0:
            return False, "Fréquence d'échantillonnage invalide"
        
        return True, "Données valides"
    
    def exportResults(self, file_path, format_type="json"):
        """
        Export des résultats d'analyse
        """
        try:
            if format_type.lower() == "json":
                import json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
            
            elif format_type.lower() == "csv":
                # Export CSV des données principales
                import pandas as pd
                
                # Créer un DataFrame avec les résultats principaux
                export_data = []
                
                # Données spectrales
                if self.analysis_results.get('spectral'):
                    spectral = self.analysis_results['spectral']
                    for i, spectrum in enumerate(spectral.get('spectra', [])):
                        export_data.append({
                            'type': 'spectral',
                            'sensor': i,
                            'data': spectrum
                        })
                
                # Données de Goda
                if self.analysis_results.get('goda'):
                    goda = self.analysis_results['goda']
                    export_data.append({
                        'type': 'goda_summary',
                        'h_max': goda.get('h_max', 0),
                        'h_mean': goda.get('h_mean', 0),
                        'h_13': goda.get('h_13', 0),
                        'h_110': goda.get('h_110', 0),
                        'n_waves': goda.get('n_waves', 0)
                    })
                
                df = pd.DataFrame(export_data)
                df.to_csv(file_path, index=False, encoding='utf-8')
            
            self.logger.info(f"Résultats exportés vers: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export: {e}")
            return False