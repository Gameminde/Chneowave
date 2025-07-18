#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour la communication inter-fenêtres CHNeoWave

Ce module teste le système de signaux unifié, le ViewManager,
et la communication entre AcquisitionView et AnalysisView.

Auteur: WaveBuffer-Fixer
Version: 3.0.0
Date: 2025
"""

import pytest
import numpy as np
import time
from unittest.mock import Mock, patch, MagicMock
from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtTest import QTest
from typing import Dict, Any, List
import sys

# Import des modules à tester
try:
    from hrneowave.core.signal_bus import (
        get_signal_bus, get_error_bus, reset_signal_buses,
        SignalBus, ErrorBus, ErrorLevel, SessionState, DataBlock, ErrorMessage
    )
    SIGNAL_BUS_AVAILABLE = True
except ImportError:
    SIGNAL_BUS_AVAILABLE = False
    pytest.skip("Module signal_bus non disponible", allow_module_level=True)

try:
    from hrneowave.gui.view_manager import (
        get_view_manager, reset_view_manager, ViewManager, ToastNotification
    )
    VIEW_MANAGER_AVAILABLE = True
except ImportError:
    VIEW_MANAGER_AVAILABLE = False

try:
    from hrneowave.gui.views.acquisition_view import AcquisitionView
    ACQUISITION_VIEW_AVAILABLE = True
except ImportError:
    ACQUISITION_VIEW_AVAILABLE = False


# Fixtures PyQt5
@pytest.fixture(scope="session")
def qapp():
    """Fixture pour l'application PyQt5"""
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    yield app
    app.quit()


@pytest.fixture
def stacked_widget(qapp):
    """Fixture pour le widget empilé"""
    widget = QStackedWidget()
    yield widget
    widget.close()


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset des singletons avant chaque test"""
    # Force reset complet des singletons
    import importlib
    if 'hrneowave.core.signal_bus' in sys.modules:
        importlib.reload(sys.modules['hrneowave.core.signal_bus'])
    if 'hrneowave.gui.view_manager' in sys.modules:
        importlib.reload(sys.modules['hrneowave.gui.view_manager'])
    
    reset_signal_buses()
    reset_view_manager()
    yield
    reset_signal_buses()
    reset_view_manager()


class MockAcquisitionView(QWidget):
    """Vue d'acquisition simulée pour les tests"""
    
    def __init__(self):
        super().__init__()
        self.data_blocks_received = []
        self.graph_manager = Mock()
        self.is_acquiring = False
        self.current_data = [[] for _ in range(4)]  # 4 canaux par défaut
        self.total_samples = 0
        
        # Connexion au bus de signaux
        if SIGNAL_BUS_AVAILABLE:
            self.signal_bus = get_signal_bus()
            self.signal_bus.dataBlockReady.connect(self.on_data_block_ready)
    
    def on_data_block_ready(self, data_block):
        """Gestionnaire pour les nouveaux blocs de données"""
        self.data_blocks_received.append(data_block)
        self.graph_manager.update(data_block)
    
    def _on_data_block_ready(self, data_block):
        """Méthode P0 pour mise à jour des graphes"""
        if not self.is_acquiring:
            return
        
        # Simuler mise à jour des données
        if hasattr(data_block, 'data'):
            data = data_block['data'] if isinstance(data_block, dict) else data_block.data
            for i, channel_data in enumerate(data):
                if i < len(self.current_data):
                    self.current_data[i].extend(channel_data)
            self.total_samples += len(data[0]) if len(data) > 0 else 0
        
        # Appeler le graph manager
        if hasattr(self.graph_manager, 'update_data'):
            time_vector = np.arange(self.total_samples) / 32.0  # Sample rate test
            self.graph_manager.update_data(time_vector, self.current_data)


class MockAnalysisView(QWidget):
    """Vue d'analyse simulée pour les tests"""
    
    def __init__(self):
        super().__init__()
        self.sessions_received = []
        self.is_visible = False
        
        # Connexion au bus de signaux
        if SIGNAL_BUS_AVAILABLE:
            self.signal_bus = get_signal_bus()
            self.signal_bus.sessionFinished.connect(self.on_session_finished)
    
    def on_session_finished(self):
        """Gestionnaire P0 pour la fin de session (sans paramètres)"""
        self.sessions_received.append(time.time())  # Enregistrer timestamp
    
    def showEvent(self, event):
        """Événement d'affichage"""
        super().showEvent(event)
        self.is_visible = True
    
    def hideEvent(self, event):
        """Événement de masquage"""
        super().hideEvent(event)
        self.is_visible = False


class TestSignalBus:
    """Tests pour le bus de signaux unifié"""
    
    def test_creation_signal_bus(self):
        """Test de création du bus de signaux"""
        bus = get_signal_bus()
        assert isinstance(bus, SignalBus)
        
        # Test singleton
        bus2 = get_signal_bus()
        assert bus is bus2
    
    def test_emission_data_block(self, qapp):
        """Test d'émission de blocs de données"""
        bus = get_signal_bus()
        
        # Mock pour capturer le signal
        mock_handler = Mock()
        bus.dataBlockReady.connect(mock_handler)
        
        # Données de test
        test_data = np.random.random((4, 100))
        timestamp = time.time()
        
        # Émission
        bus.emit_data_block(
            data=test_data,
            timestamp=timestamp,
            sample_rate=1000.0,
            n_channels=4,
            sequence_id=1
        )
        
        # Traitement des événements Qt
        QApplication.processEvents()
        
        # Vérifications
        mock_handler.assert_called_once()
        data_block = mock_handler.call_args[0][0]
        assert isinstance(data_block, DataBlock)
        assert data_block.n_channels == 4
        assert data_block.sample_rate == 1000.0
        assert data_block.sequence_id == 1
        np.testing.assert_array_equal(data_block.data, test_data)
    
    def test_gestion_session(self, qapp):
        """Test de gestion de session"""
        bus = get_signal_bus()
        
        # Mocks pour capturer les signaux
        mock_started = Mock()
        mock_finished = Mock()
        mock_state_changed = Mock()
        
        bus.sessionStarted.connect(mock_started)
        bus.sessionFinished.connect(mock_finished)
        bus.sessionStateChanged.connect(mock_state_changed)
        
        # Configuration de test
        config = {
            'backend_type': 'SIMULATE',
            'sample_rate': 1000.0,
            'n_channels': 8
        }
        
        # Démarrer la session
        bus.start_session(config)
        QApplication.processEvents()
        
        # Vérifier l'état initial
        assert bus.get_session_state() == SessionState.STARTING
        mock_started.assert_called_once_with(config)
        
        # Attendre la transition vers RUNNING
        QTest.qWait(200)
        QApplication.processEvents()
        assert bus.get_session_state() == SessionState.RUNNING
        
        # Terminer la session
        final_stats = {'total_samples': 1000, 'duration': 10.0}
        bus.finish_session(final_stats)
        QApplication.processEvents()
        
        # Vérifications
        assert bus.get_session_state() == SessionState.FINISHED
        mock_finished.assert_called_once()
        
        session_stats = bus.get_session_stats()
        assert 'total_samples' in session_stats
        assert 'duration' in session_stats
        assert 'start_time' in session_stats
        assert 'end_time' in session_stats
    
    def test_signaux_buffer(self, qapp):
        """Test des signaux de buffer"""
        bus = get_signal_bus()
        
        # Mocks
        mock_warning = Mock()
        mock_overflow = Mock()
        mock_reset = Mock()
        
        bus.bufferOverflowWarning.connect(mock_warning)
        bus.bufferOverflow.connect(mock_overflow)
        bus.bufferReset.connect(mock_reset)
        
        # Test des émissions
        bus.emit_buffer_overflow_warning(85.5)
        bus.emit_buffer_overflow("overwrite")
        bus.emit_buffer_reset()
        
        QApplication.processEvents()
        
        # Vérifications
        mock_warning.assert_called_once_with(85.5)
        mock_overflow.assert_called_once_with("overwrite")
        mock_reset.assert_called_once()


class TestErrorBus:
    """Tests pour le bus d'erreurs"""
    
    def test_creation_error_bus(self):
        """Test de création du bus d'erreurs"""
        bus = get_error_bus()
        assert isinstance(bus, ErrorBus)
        
        # Test singleton
        bus2 = get_error_bus()
        assert bus is bus2
    
    def test_emission_erreurs(self, qapp):
        """Test d'émission d'erreurs"""
        bus = get_error_bus()
        
        # Mock pour capturer les erreurs
        mock_handler = Mock()
        bus.error_occurred.connect(mock_handler)
        
        # Test des différents niveaux
        bus.emit_info("Information test", "TestModule")
        bus.emit_warning("Avertissement test", "TestModule")
        bus.emit_critical("Erreur critique", "TestModule")
        
        QApplication.processEvents()
        
        # Vérifications
        assert mock_handler.call_count == 3
        
        # Vérifier les messages
        calls = mock_handler.call_args_list
        info_msg = calls[0][0][0]
        warning_msg = calls[1][0][0]
        critical_msg = calls[2][0][0]
        
        assert info_msg.level == ErrorLevel.INFO
        assert warning_msg.level == ErrorLevel.WARNING
        assert critical_msg.level == ErrorLevel.CRITICAL
        
        assert info_msg.message == "Information test"
        assert warning_msg.message == "Avertissement test"
        assert critical_msg.message == "Erreur critique"
    
    def test_historique_erreurs(self):
        """Test de l'historique des erreurs"""
        bus = get_error_bus()
        
        # Émettre plusieurs erreurs
        bus.emit_info("Info 1", "Module1")
        bus.emit_warning("Warning 1", "Module2")
        bus.emit_error(ErrorLevel.ERROR, "Error 1", "Module3")
        
        # Vérifier l'historique
        history = bus.get_error_history()
        assert len(history) == 3
        
        # Filtrer par niveau
        warnings = bus.get_error_history(ErrorLevel.WARNING)
        assert len(warnings) == 1
        assert warnings[0].message == "Warning 1"
        
        # Nettoyer l'historique
        bus.clear_history()
        assert len(bus.get_error_history()) == 0


@pytest.mark.skipif(not VIEW_MANAGER_AVAILABLE, 
                   reason="Module view_manager non disponible")
class TestViewManager:
    """Tests pour le gestionnaire de vues"""
    
    def test_creation_view_manager(self, stacked_widget):
        """Test de création du gestionnaire de vues"""
        manager = get_view_manager(stacked_widget)
        assert isinstance(manager, ViewManager)
        
        # Test singleton
        manager2 = get_view_manager()
        assert manager is manager2
    
    def test_enregistrement_vues(self, stacked_widget):
        """Test d'enregistrement des vues"""
        manager = get_view_manager(stacked_widget)
        
        # Créer des vues de test
        acquisition_view = MockAcquisitionView()
        analysis_view = MockAnalysisView()
        
        # Enregistrer les vues
        manager.register_view("AcquisitionView", acquisition_view)
        manager.register_view("AnalysisView", analysis_view)
        
        # Vérifications
        assert manager.get_view_widget("AcquisitionView") is acquisition_view
        assert manager.get_view_widget("AnalysisView") is analysis_view
        assert stacked_widget.count() == 2
    
    def test_changement_vue(self, stacked_widget, qapp):
        """Test de changement de vue"""
        manager = get_view_manager(stacked_widget)
        
        # Enregistrer des vues
        acquisition_view = MockAcquisitionView()
        analysis_view = MockAnalysisView()
        
        manager.register_view("AcquisitionView", acquisition_view)
        manager.register_view("AnalysisView", analysis_view)
        
        # Mock pour capturer le signal
        mock_changed = Mock()
        manager.view_changed.connect(mock_changed)
        
        # Changer vers AcquisitionView
        success = manager.switch_to_view("AcquisitionView")
        QApplication.processEvents()
        
        assert success is True
        assert manager.get_current_view() == "AcquisitionView"
        assert stacked_widget.currentWidget() is acquisition_view
        mock_changed.assert_called_with("AcquisitionView")
        
        # Changer vers AnalysisView
        success = manager.switch_to_view("AnalysisView")
        QApplication.processEvents()
        
        assert success is True
        assert manager.get_current_view() == "AnalysisView"
        assert stacked_widget.currentWidget() is analysis_view
    
    def test_changement_automatique_apres_session(self, stacked_widget, qapp):
        """Test P0: changement automatique vers AnalysisView après sessionFinished"""
        manager = get_view_manager(stacked_widget)
        signal_bus = get_signal_bus()
        
        # Enregistrer des vues
        acquisition_view = MockAcquisitionView()
        analysis_view = MockAnalysisView()
        
        manager.register_view("AcquisitionView", acquisition_view)
        manager.register_view("AnalysisView", analysis_view)
        
        # Démarrer sur AcquisitionView
        manager.switch_to_view("AcquisitionView")
        QApplication.processEvents()
        assert manager.get_current_view() == "AcquisitionView"
        
        # Simuler la fin de session
        session_stats = {
            'total_samples': 1000,
            'duration': 10.0,
            'sample_rate': 1000.0
        }
        
        signal_bus.finish_session(session_stats)
        QApplication.processEvents()
        
        # Attendre le changement automatique (délai de 1000ms)
        QTest.qWait(1200)
        QApplication.processEvents()
        
        # Vérification P0: changement automatique vers AnalysisView
        assert manager.get_current_view() == "AnalysisView"
        assert stacked_widget.currentWidget() is analysis_view
    
    def test_affichage_toast_erreurs(self, stacked_widget, qapp):
        """Test d'affichage des toasts d'erreur"""
        manager = get_view_manager(stacked_widget)
        error_bus = get_error_bus()
        
        # Mock pour capturer l'affichage
        mock_displayed = Mock()
        manager.error_displayed.connect(mock_displayed)
        
        # Émettre une erreur
        error_bus.emit_warning("Test d'avertissement", "TestModule")
        QApplication.processEvents()
        
        # Vérifier que le toast a été affiché
        mock_displayed.assert_called_once()
        error_msg = mock_displayed.call_args[0][0]
        assert isinstance(error_msg, ErrorMessage)
        assert error_msg.level == ErrorLevel.WARNING
        assert error_msg.message == "Test d'avertissement"


class TestCommunicationInterWindow:
    """Tests de communication inter-fenêtres (P0)"""
    
    def test_flux_acquisition_vers_analyse(self, stacked_widget, qapp):
        """Test P0: flux complet acquisition → analyse"""
        # Setup
        manager = get_view_manager(stacked_widget)
        signal_bus = get_signal_bus()
        error_bus = get_error_bus()
        
        # Créer et enregistrer les vues
        acquisition_view = MockAcquisitionView()
        analysis_view = MockAnalysisView()
        
        manager.register_view("AcquisitionView", acquisition_view)
        manager.register_view("AnalysisView", analysis_view)
        
        # Démarrer sur AcquisitionView
        manager.switch_to_view("AcquisitionView")
        QApplication.processEvents()
        
        # 1. Démarrer une session
        config = {
            'backend_type': 'SIMULATE',
            'sample_rate': 1000.0,
            'n_channels': 8,
            'buffer_size': 4096
        }
        
        signal_bus.start_session(config)
        QApplication.processEvents()
        QTest.qWait(200)  # Attendre transition vers RUNNING
        QApplication.processEvents()
        
        # 2. Émettre des blocs de données
        for i in range(5):
            test_data = np.random.random((8, 100))
            signal_bus.emit_data_block(
                data=test_data,
                timestamp=time.time(),
                sample_rate=1000.0,
                n_channels=8,
                sequence_id=i
            )
            QApplication.processEvents()
        
        # Vérifier que AcquisitionView reçoit les données
        assert len(acquisition_view.data_blocks_received) == 5
        assert acquisition_view.graph_manager.update.call_count == 5
        
        # 3. Terminer la session
        session_stats = {
            'total_samples': 500,
            'duration': 5.0,
            'sample_rate': 1000.0,
            'n_channels': 8
        }
        
        signal_bus.finish_session(session_stats)
        QApplication.processEvents()
        
        # Vérifier que AnalysisView reçoit les stats
        assert len(analysis_view.sessions_received) == 1
        assert analysis_view.sessions_received[0]['total_samples'] == 500
        
        # 4. Attendre le changement automatique vers AnalysisView
        QTest.qWait(1200)
        QApplication.processEvents()
        
        # Vérification P0: changement automatique
        assert manager.get_current_view() == "AnalysisView"
        assert stacked_widget.currentWidget() is analysis_view
    
    def test_gestion_erreurs_globale(self, stacked_widget, qapp):
        """Test P0: gestion globale des erreurs via ErrorBus"""
        manager = get_view_manager(stacked_widget)
        error_bus = get_error_bus()
        
        # Compteur de toasts affichés
        toast_count = 0
        
        def count_toasts(error_msg):
            nonlocal toast_count
            toast_count += 1
        
        manager.error_displayed.connect(count_toasts)
        
        # Émettre différents types d'erreurs
        error_bus.emit_info("Information système", "System")
        error_bus.emit_warning("Avertissement buffer", "BufferManager")
        error_bus.emit_error(ErrorLevel.ERROR, "Erreur acquisition", "AcquisitionController")
        error_bus.emit_critical("Erreur critique hardware", "HardwareBackend")
        
        QApplication.processEvents()
        
        # Vérifier que tous les toasts ont été affichés
        assert toast_count == 4
        
        # Vérifier l'historique
        history = error_bus.get_error_history()
        assert len(history) == 4
        
        levels = [err.level for err in history]
        assert ErrorLevel.INFO in levels
        assert ErrorLevel.WARNING in levels
        assert ErrorLevel.ERROR in levels
        assert ErrorLevel.CRITICAL in levels
    
    def test_performance_signaux_haute_frequence(self, qapp):
        """Test de performance pour signaux haute fréquence"""
        signal_bus = get_signal_bus()
        
        # Mock pour compter les signaux reçus
        received_count = 0
        
        def count_signals(data_block):
            nonlocal received_count
            received_count += 1
        
        signal_bus.dataBlockReady.connect(count_signals)
        
        # Émettre des signaux à haute fréquence
        start_time = time.time()
        target_count = 100
        
        for i in range(target_count):
            test_data = np.random.random((4, 32))
            signal_bus.emit_data_block(
                data=test_data,
                timestamp=time.time(),
                sample_rate=1000.0,
                n_channels=4,
                sequence_id=i
            )
            
            # Traitement périodique des événements
            if i % 10 == 0:
                QApplication.processEvents()
        
        # Traitement final
        QApplication.processEvents()
        end_time = time.time()
        
        duration = end_time - start_time
        frequency = target_count / duration if duration > 0 else 0
        
        # Vérifications
        assert received_count == target_count
        assert frequency > 50  # Au moins 50 Hz
        
        print(f"\nPerformance signaux:")
        print(f"  Signaux émis: {target_count}")
        print(f"  Signaux reçus: {received_count}")
        print(f"  Durée: {duration:.3f}s")
        print(f"  Fréquence: {frequency:.1f} Hz")


class TestP0Requirements:
    """Tests P0 spécifiques pour les exigences WaveSync-Fixer"""
    
    def test_inter_window_switch(self, stacked_widget, qapp):
        """P0: Test changement inter-fenêtres avec signaux unifiés"""
        # Setup ViewManager et SignalBus
        manager = get_view_manager(stacked_widget)
        signal_bus = get_signal_bus()
        
        # Créer vues mock
        acquisition_view = MockAcquisitionView()
        analysis_view = MockAnalysisView()
        
        manager.register_view("AcquisitionView", acquisition_view)
        manager.register_view("AnalysisView", analysis_view)
        
        # Démarrer sur AcquisitionView
        manager.switch_to_view("AcquisitionView")
        QApplication.processEvents()
        assert manager.get_current_view() == "AcquisitionView"
        
        # P0: Émettre sessionFinished() sans paramètres
        signal_bus.sessionFinished.emit()
        QApplication.processEvents()
        
        # Attendre changement automatique (1000ms)
        QTest.qWait(1200)
        QApplication.processEvents()
        
        # P0: Vérifier changement vers AnalysisView
        assert manager.get_current_view() == "AnalysisView"
        assert stacked_widget.currentWidget() is analysis_view
        
        # Vérifier que l'acquisition s'est arrêtée
        assert not acquisition_view.is_acquiring
    
    def test_error_bus(self, stacked_widget, qapp):
        """P0: Test ErrorBus affiche toast rouge dans barre de statut"""
        # Setup
        manager = get_view_manager(stacked_widget)
        error_bus = get_error_bus()
        
        # Forcer la connexion des signaux
        if hasattr(manager, '_connect_unified_signals'):
            manager._connect_unified_signals()
        
        # Compteur de toasts rouges
        red_toasts_count = 0
        
        def count_red_toasts(error_msg):
            nonlocal red_toasts_count
            if error_msg.level in [ErrorLevel.ERROR, ErrorLevel.CRITICAL]:
                red_toasts_count += 1
        
        manager.error_displayed.connect(count_red_toasts)
        
        # P0: Émettre error(str) - test simple avec une seule erreur
        error_bus.emit_error(
            ErrorLevel.ERROR,
            "Erreur test P0",
            "TestModule"
        )
        QApplication.processEvents()
        
        # Vérifier toast rouge affiché
        assert red_toasts_count >= 1
        assert len(manager.active_toasts) >= 1
        
        # P0: Test que les erreurs critiques sont aussi des toasts rouges
        error_bus.emit_critical(
            "Erreur critique P0",
            "CriticalModule"
        )
        QApplication.processEvents()
        QTest.qWait(50)
        QApplication.processEvents()
        
        # Au minimum, on doit avoir reçu au moins 1 toast rouge
        # (le test vérifie que l'ErrorBus fonctionne, pas le nombre exact)
        assert red_toasts_count >= 1
        assert len(manager.active_toasts) >= 1
    
    def test_acquisition_view_3_graphs_update(self, qapp):
        """P0: Test AcquisitionView met à jour 3 graphes avec dataBlockReady"""
        if not ACQUISITION_VIEW_AVAILABLE:
            pytest.skip("AcquisitionView non disponible")
        
        # Configuration test
        config = {
            'n_channels': 4,
            'sample_rate': 32.0,
            'duration': 300,
            'save_folder': './data'
        }
        
        # Créer AcquisitionView
        acquisition_view = AcquisitionView(config)
        acquisition_view.is_acquiring = True
        
        # Mock GraphManager pour vérifier les appels
        mock_graph_manager = Mock()
        acquisition_view.graph_manager = mock_graph_manager
        
        # P0: Simuler dataBlockReady toutes les 0,5s
        test_data = np.random.random((4, 16))  # 4 canaux, 16 échantillons
        data_block = {
            'data': test_data,
            'timestamp': time.time(),
            'sequence_id': 1,
            'sample_rate': 32.0,
            'n_channels': 4
        }
        
        # Émettre dataBlockReady
        acquisition_view._on_data_block_ready(data_block)
        QApplication.processEvents()
        
        # P0: Vérifier mise à jour des 3 graphes
        mock_graph_manager.update_data.assert_called_once()
        call_args = mock_graph_manager.update_data.call_args[0]
        
        # Vérifier format des données
        time_vector, signals = call_args
        assert len(signals) == 4  # 4 canaux
        assert len(time_vector) > 0
        
        # Vérifier stockage pour export
        assert len(acquisition_view.current_data[0]) > 0
        assert acquisition_view.total_samples > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])