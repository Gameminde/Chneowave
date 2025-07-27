# -*- coding: utf-8 -*-
"""
Vue d'analyse CHNeoWave v2.0 - Version refactorisée
Utilise une architecture modulaire avec des widgets spécialisés
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, 
    QPushButton, QProgressBar, QMessageBox, QSplitter,
    QGroupBox, QFormLayout, QTextEdit
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont

import logging
from datetime import datetime

# Import des widgets spécialisés
from .spectral_analysis import SpectralAnalysisWidget
from .goda_analysis import GodaAnalysisWidget
from .statistics_analysis import StatisticsAnalysisWidget
from .summary_report import SummaryReportWidget
from .analysis_controller import AnalysisController


class AnalysisViewV2(QWidget):
    """
    Vue d'analyse refactorisée utilisant une architecture modulaire
    Responsabilité principale : orchestration de l'interface utilisateur
    """
    
    # Signaux pour communication avec le contrôleur principal
    analysisFinished = Signal(dict)  # Résultats d'analyse complets
    analysisStarted = Signal(str)    # Type d'analyse démarrée
    analysisError = Signal(str)      # Erreur d'analyse
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Données de session
        self.session_data = None
        
        # Widgets spécialisés
        self.spectral_widget = None
        self.goda_widget = None
        self.statistics_widget = None
        self.summary_widget = None
        
        # Contrôleur d'analyse
        self.analysis_controller = AnalysisController()
        
        # Interface utilisateur
        self.setupUI()
        self.connectSignals()
        
        self.logger.info("AnalysisViewV2 initialisée")
    
    def setupUI(self):
        """
        Configuration de l'interface utilisateur principale
        """
        layout = QVBoxLayout(self)
        
        # En-tête avec informations et contrôles
        header_widget = self._createHeaderWidget()
        layout.addWidget(header_widget)
        
        # Zone principale avec onglets
        main_widget = self._createMainWidget()
        layout.addWidget(main_widget)
        
        # Barre de statut
        status_widget = self._createStatusWidget()
        layout.addWidget(status_widget)
    
    def _createHeaderWidget(self):
        """
        Création de l'en-tête avec informations et contrôles globaux
        """
        header_group = QGroupBox("Contrôle d'Analyse")
        header_layout = QVBoxLayout(header_group)
        
        # Informations sur les données
        info_layout = QFormLayout()
        
        self.data_info_label = QLabel("Aucune donnée chargée")
        self.data_info_label.setStyleSheet("color: #666; font-style: italic;")
        info_layout.addRow("Données:", self.data_info_label)
        
        self.session_info_label = QLabel("Session non définie")
        self.session_info_label.setStyleSheet("color: #666; font-style: italic;")
        info_layout.addRow("Session:", self.session_info_label)
        
        header_layout.addLayout(info_layout)
        
        # Boutons de contrôle global
        controls_layout = QHBoxLayout()
        
        self.analyze_all_btn = QPushButton("Analyse Complète")
        self.analyze_all_btn.setMinimumHeight(40)
        self.analyze_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        self.analyze_all_btn.setEnabled(False)
        controls_layout.addWidget(self.analyze_all_btn)
        
        self.reset_btn = QPushButton("Réinitialiser")
        self.reset_btn.setMinimumHeight(40)
        controls_layout.addWidget(self.reset_btn)
        
        self.export_btn = QPushButton("Exporter Résultats")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.setEnabled(False)
        controls_layout.addWidget(self.export_btn)
        
        controls_layout.addStretch()
        
        header_layout.addLayout(controls_layout)
        
        return header_group
    
    def _createMainWidget(self):
        """
        Création de la zone principale avec onglets d'analyse
        """
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # Onglet Analyse Spectrale
        self.spectral_widget = SpectralAnalysisWidget()
        self.tab_widget.addTab(self.spectral_widget, "Analyse Spectrale")
        
        # Onglet Analyse de Goda
        self.goda_widget = GodaAnalysisWidget()
        self.tab_widget.addTab(self.goda_widget, "Analyse de Goda")
        
        # Onglet Statistiques
        self.statistics_widget = StatisticsAnalysisWidget()
        self.tab_widget.addTab(self.statistics_widget, "Statistiques")
        
        # Onglet Rapport
        self.summary_widget = SummaryReportWidget()
        self.tab_widget.addTab(self.summary_widget, "Rapport")
        
        # Configuration du contrôleur avec les widgets
        self.analysis_controller.setWidgets(
            self.spectral_widget,
            self.goda_widget,
            self.statistics_widget,
            self.summary_widget
        )
        
        return self.tab_widget
    
    def _createStatusWidget(self):
        """
        Création de la barre de statut
        """
        status_group = QGroupBox("Statut")
        status_layout = QVBoxLayout(status_group)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        # Messages de statut
        self.status_label = QLabel("Prêt pour l'analyse")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        return status_group
    
    def connectSignals(self):
        """
        Connexion des signaux
        """
        # Boutons de contrôle
        self.analyze_all_btn.clicked.connect(self.startCompleteAnalysis)
        self.reset_btn.clicked.connect(self.resetAnalysis)
        self.export_btn.clicked.connect(self.exportResults)
        
        # Signaux du contrôleur
        self.analysis_controller.analysisStarted.connect(self._onAnalysisStarted)
        self.analysis_controller.analysisFinished.connect(self._onAnalysisFinished)
        self.analysis_controller.analysisProgress.connect(self._onAnalysisProgress)
        self.analysis_controller.analysisError.connect(self._onAnalysisError)
        
        # Signaux des widgets individuels
        if self.spectral_widget:
            self.spectral_widget.analysisCompleted.connect(self._onIndividualAnalysisCompleted)
        
        if self.goda_widget:
            self.goda_widget.analysisCompleted.connect(self._onIndividualAnalysisCompleted)
        
        if self.statistics_widget:
            self.statistics_widget.analysisCompleted.connect(self._onIndividualAnalysisCompleted)
    
    def setSessionData(self, session_data):
        """
        Configuration des données de session
        """
        try:
            # Validation des données
            is_valid, message = self.analysis_controller.validateSessionData(session_data)
            if not is_valid:
                QMessageBox.warning(self, "Données invalides", message)
                return
            
            self.session_data = session_data
            
            # Propager aux widgets via le contrôleur
            self.analysis_controller.setSessionData(session_data)
            
            # Mettre à jour l'interface
            self._updateDataInfo()
            
            # Activer les contrôles
            self.analyze_all_btn.setEnabled(True)
            
            self.logger.info(f"Données de session configurées: {len(session_data.get('sensor_data', []))} capteurs")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la configuration des données: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la configuration des données:\n{str(e)}")
    
    def _updateDataInfo(self):
        """
        Mise à jour des informations sur les données
        """
        if not self.session_data:
            self.data_info_label.setText("Aucune donnée chargée")
            self.session_info_label.setText("Session non définie")
            return
        
        sensor_data = self.session_data.get('sensor_data', [])
        sample_rate = self.session_data.get('sample_rate', 100)
        duration = self.session_data.get('duration', 0)
        
        data_info = f"{len(sensor_data)} capteurs, {len(sensor_data[0]) if sensor_data else 0} échantillons"
        self.data_info_label.setText(data_info)
        self.data_info_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        session_info = f"Durée: {duration:.1f}s, Fréq: {sample_rate}Hz"
        if 'project_name' in self.session_data:
            session_info = f"{self.session_data['project_name']} - {session_info}"
        
        self.session_info_label.setText(session_info)
        self.session_info_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
    
    def startCompleteAnalysis(self):
        """
        Démarrage de l'analyse complète
        """
        if not self.session_data:
            QMessageBox.warning(self, "Erreur", "Aucune donnée de session disponible.")
            return
        
        try:
            self.analysis_controller.startCompleteAnalysis()
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage de l'analyse: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors du démarrage de l'analyse:\n{str(e)}")
    
    def startSpectralAnalysis(self):
        """
        Démarrage de l'analyse spectrale uniquement
        """
        self.analysis_controller.startSpectralAnalysis()
    
    def startGodaAnalysis(self):
        """
        Démarrage de l'analyse de Goda uniquement
        """
        self.analysis_controller.startGodaAnalysis()
    
    def startStatisticsAnalysis(self):
        """
        Démarrage de l'analyse statistique uniquement
        """
        self.analysis_controller.startStatisticsAnalysis()
    
    def resetAnalysis(self):
        """
        Réinitialisation de toutes les analyses
        """
        try:
            self.analysis_controller.resetAnalysis()
            
            # Réinitialiser l'interface
            self.progress_bar.setVisible(False)
            self.progress_bar.setValue(0)
            self.status_label.setText("Prêt pour l'analyse")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            
            # Réactiver les contrôles
            self.analyze_all_btn.setEnabled(bool(self.session_data))
            self.export_btn.setEnabled(False)
            
            self.logger.info("Analyses réinitialisées")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la réinitialisation: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la réinitialisation:\n{str(e)}")
    
    def exportResults(self):
        """
        Export des résultats d'analyse
        """
        if not self.analysis_controller.isAnalysisComplete():
            QMessageBox.warning(self, "Export impossible", "Aucune analyse complète disponible pour l'export.")
            return
        
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter les résultats", 
            f"resultats_chneowave_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "Fichiers JSON (*.json);;Fichiers CSV (*.csv)"
        )
        
        if file_path:
            try:
                format_type = "json" if file_path.endswith('.json') else "csv"
                success = self.analysis_controller.exportResults(file_path, format_type)
                
                if success:
                    QMessageBox.information(self, "Export réussi", f"Résultats exportés vers:\n{file_path}")
                else:
                    QMessageBox.warning(self, "Erreur d'export", "Erreur lors de l'export des résultats.")
                    
            except Exception as e:
                self.logger.error(f"Erreur lors de l'export: {e}")
                QMessageBox.critical(self, "Erreur d'export", f"Erreur lors de l'export:\n{str(e)}")
    
    def _onAnalysisStarted(self, analysis_type):
        """
        Gestion du démarrage d'analyse
        """
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        if analysis_type == "complete":
            self.status_label.setText("Analyse complète en cours...")
        else:
            self.status_label.setText(f"Analyse {analysis_type} en cours...")
        
        self.status_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        
        # Désactiver les contrôles pendant l'analyse
        self.analyze_all_btn.setEnabled(False)
        
        # Émettre le signal vers le contrôleur principal
        self.analysisStarted.emit(analysis_type)
    
    def _onAnalysisFinished(self, results):
        """
        Gestion de la fin d'analyse
        """
        self.progress_bar.setValue(100)
        self.status_label.setText("Analyse terminée avec succès")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        # Réactiver les contrôles
        self.analyze_all_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        
        # Masquer la barre de progression après un délai
        QTimer.singleShot(3000, lambda: self.progress_bar.setVisible(False))
        
        # Émettre le signal vers le contrôleur principal
        self.analysisFinished.emit(results)
        
        self.logger.info("Analyse complète terminée")
    
    def _onAnalysisProgress(self, progress):
        """
        Gestion du progrès d'analyse
        """
        self.progress_bar.setValue(progress)
    
    def _onAnalysisError(self, error_message):
        """
        Gestion des erreurs d'analyse
        """
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Erreur: {error_message}")
        self.status_label.setStyleSheet("color: #F44336; font-weight: bold;")
        
        # Réactiver les contrôles
        self.analyze_all_btn.setEnabled(bool(self.session_data))
        
        # Afficher le message d'erreur
        QMessageBox.critical(self, "Erreur d'analyse", error_message)
        
        # Émettre le signal vers le contrôleur principal
        self.analysisError.emit(error_message)
    
    def _onIndividualAnalysisCompleted(self, results):
        """
        Gestion de la fin d'une analyse individuelle
        """
        # Mettre à jour le statut si ce n'est pas une analyse complète
        if self.analysis_controller.isAnalysisComplete():
            self.export_btn.setEnabled(True)
    
    def getAnalysisResults(self):
        """
        Retourne les résultats d'analyse
        """
        return self.analysis_controller.getAnalysisResults()
    
    def getAnalysisStatus(self):
        """
        Retourne l'état des analyses
        """
        return self.analysis_controller.getAnalysisStatus()
    
    def isAnalysisComplete(self):
        """
        Vérifie si l'analyse est complète
        """
        return self.analysis_controller.isAnalysisComplete()
    
    def setCurrentTab(self, tab_index):
        """
        Définit l'onglet actuel
        """
        if 0 <= tab_index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(tab_index)
    
    def getCurrentTab(self):
        """
        Retourne l'index de l'onglet actuel
        """
        return self.tab_widget.currentIndex()
    
    def getSpectralWidget(self):
        """
        Retourne le widget d'analyse spectrale
        """
        return self.spectral_widget
    
    def getGodaWidget(self):
        """
        Retourne le widget d'analyse de Goda
        """
        return self.goda_widget
    
    def getStatisticsWidget(self):
        """
        Retourne le widget d'analyse statistique
        """
        return self.statistics_widget
    
    def getSummaryWidget(self):
        """
        Retourne le widget de rapport
        """
        return self.summary_widget
    
    def reset_view(self):
        """
        Réinitialisation de la vue (compatibilité avec l'ancienne interface)
        """
        self.resetAnalysis()
    
    def set_acquisition_data(self, session_data):
        """
        Configuration des données d'acquisition (compatibilité avec l'ancienne interface)
        """
        self.setSessionData(session_data)
        
        # Démarrer automatiquement l'analyse complète si demandé
        # (comportement de l'ancienne version)
        # self.startCompleteAnalysis()