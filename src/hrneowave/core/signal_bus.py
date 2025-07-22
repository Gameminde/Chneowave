#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bus de signaux unifié pour CHNeoWave

Ce module implémente un système de signaux centralisé pour la communication
entre les différents composants de l'application (acquisition, traitement, GUI).

Auteur: WaveBuffer-Fixer
Version: 3.0.0
Date: 2025
"""

import numpy as np
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import time
import threading

# Variables globales pour les imports Qt conditionnels
QObject = None
Signal = None
QTimer = None
QApplication = None

def _ensure_qt_imports():
    """Importe les modules Qt de manière conditionnelle"""
    global QObject, Signal, QTimer, QApplication
    
    if QObject is None:
        from PySide6.QtCore import QObject, Signal, QTimer
        from PySide6.QtWidgets import QApplication


class ErrorLevel(Enum):
    """Niveaux de sévérité des erreurs"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class SessionState(Enum):
    """États de session d'acquisition"""
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FINISHED = "finished"
    ERROR = "error"


@dataclass
class DataBlock:
    """Bloc de données avec métadonnées"""
    data: np.ndarray
    timestamp: float
    sample_rate: float
    n_channels: int
    sequence_id: int = 0
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        
        # Validation des données
        if self.data.ndim not in [1, 2]:
            raise ValueError("Les données doivent être 1D ou 2D")
        
        if self.data.ndim == 2 and self.data.shape[0] != self.n_channels:
            raise ValueError(f"Nombre de canaux incorrect: {self.data.shape[0]} vs {self.n_channels}")
    
    @property
    def n_samples(self) -> int:
        """Nombre d'échantillons dans le bloc"""
        return self.data.shape[-1] if self.data.ndim == 2 else len(self.data)
    
    @property
    def duration(self) -> float:
        """Durée du bloc en secondes"""
        return self.n_samples / self.sample_rate if self.sample_rate > 0 else 0.0


@dataclass
class ErrorMessage:
    """Message d'erreur avec contexte"""
    level: ErrorLevel
    message: str
    source: str
    timestamp: float
    details: Optional[Dict[str, Any]] = None
    exception: Optional[Exception] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}
        
        if self.timestamp <= 0:
            self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le message en dictionnaire"""
        return {
            'level': self.level.value,
            'message': self.message,
            'source': self.source,
            'timestamp': self.timestamp,
            'details': self.details,
            'exception': str(self.exception) if self.exception else None
        }


class ErrorBus(QObject):
    """Bus d'erreurs global pour diffuser les erreurs vers l'interface"""
    
    # Signal pour les erreurs
    error_occurred = pyqtSignal(object)  # ErrorMessage
    
    def __init__(self):
        super().__init__()
        self._error_history: List[ErrorMessage] = []
        self._max_history = 1000
        self._lock = threading.Lock()
    
    def emit_error(self, level: ErrorLevel, message: str, source: str, 
                   details: Optional[Dict[str, Any]] = None, 
                   exception: Optional[Exception] = None) -> None:
        """Émet une erreur sur le bus"""
        error_msg = ErrorMessage(
            level=level,
            message=message,
            source=source,
            timestamp=time.time(),
            details=details,
            exception=exception
        )
        
        with self._lock:
            self._error_history.append(error_msg)
            # Limiter l'historique
            if len(self._error_history) > self._max_history:
                self._error_history.pop(0)
        
        # Émettre le signal
        self.error_occurred.emit(error_msg)
    
    def emit_info(self, message: str, source: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Émet une information"""
        self.emit_error(ErrorLevel.INFO, message, source, details)
    
    def emit_warning(self, message: str, source: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Émet un avertissement"""
        self.emit_error(ErrorLevel.WARNING, message, source, details)
    
    def emit_critical(self, message: str, source: str, details: Optional[Dict[str, Any]] = None, 
                     exception: Optional[Exception] = None) -> None:
        """Émet une erreur critique"""
        self.emit_error(ErrorLevel.CRITICAL, message, source, details, exception)
    
    def get_error_history(self, level: Optional[ErrorLevel] = None) -> List[ErrorMessage]:
        """Retourne l'historique des erreurs"""
        with self._lock:
            if level is None:
                return self._error_history.copy()
            else:
                return [err for err in self._error_history if err.level == level]
    
    def clear_history(self) -> None:
        """Efface l'historique des erreurs"""
        with self._lock:
            self._error_history.clear()


class SignalBus(QObject):
    """Bus de signaux principal pour CHNeoWave"""
    
    # Signaux d'acquisition
    dataBlockReady = pyqtSignal(object)  # DataBlock
    sessionStarted = pyqtSignal(dict)  # config de session
    sessionFinished = pyqtSignal()  # P0: signal sans paramètres
    sessionStateChanged = pyqtSignal(object)  # SessionState
    
    # Signaux de buffer
    bufferOverflowWarning = pyqtSignal(float)  # pourcentage d'utilisation
    bufferOverflow = pyqtSignal(str)  # mode d'overflow
    bufferReset = pyqtSignal()
    bufferStatsUpdated = pyqtSignal(dict)  # statistiques buffer
    
    # Signaux de traitement
    processingStarted = pyqtSignal()
    processingFinished = pyqtSignal(dict)  # résultats
    processingProgress = pyqtSignal(float)  # pourcentage 0-100
    
    # Signaux d'interface
    viewChangeRequested = pyqtSignal(str)  # nom de la vue
    configurationChanged = pyqtSignal(dict)  # nouvelle configuration
    analysisRequested = pyqtSignal(dict)  # Demande d'analyse avec les données
    
    def __init__(self):
        super().__init__()
        self._session_state = SessionState.IDLE
        self._session_stats = {}
        self._lock = threading.Lock()
    
    def emit_data_block(self, data: np.ndarray, timestamp: float, sample_rate: float, 
                       n_channels: int, sequence_id: int = 0, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Émet un bloc de données"""
        data_block = DataBlock(
            data=data,
            timestamp=timestamp,
            sample_rate=sample_rate,
            n_channels=n_channels,
            sequence_id=sequence_id,
            metadata=metadata
        )
        self.dataBlockReady.emit(data_block)
    
    def start_session(self, config: Dict[str, Any]) -> None:
        """Démarre une session d'acquisition"""
        with self._lock:
            self._session_state = SessionState.STARTING
            self._session_stats = {
                'start_time': time.time(),
                'config': config.copy(),
                'blocks_processed': 0,
                'total_samples': 0
            }
        
        self.sessionStateChanged.emit(SessionState.STARTING)
        self.sessionStarted.emit(config)
        
        # Transition vers RUNNING
        QTimer.singleShot(100, lambda: self._set_session_running())
    
    def _set_session_running(self) -> None:
        """Transition vers l'état RUNNING"""
        with self._lock:
            self._session_state = SessionState.RUNNING
        self.sessionStateChanged.emit(SessionState.RUNNING)
    
    def finish_session(self, final_stats: Optional[Dict[str, Any]] = None) -> None:
        """Termine une session d'acquisition"""
        with self._lock:
            self._session_state = SessionState.FINISHED
            if final_stats:
                self._session_stats.update(final_stats)
            
            self._session_stats['end_time'] = time.time()
            self._session_stats['duration'] = (
                self._session_stats['end_time'] - self._session_stats['start_time']
            )
        
        self.sessionStateChanged.emit(SessionState.FINISHED)
        self.sessionFinished.emit()  # P0: émission sans paramètres
    
    def update_session_stats(self, stats: Dict[str, Any]) -> None:
        """Met à jour les statistiques de session"""
        with self._lock:
            self._session_stats.update(stats)
    
    def get_session_state(self) -> SessionState:
        """Retourne l'état actuel de la session"""
        with self._lock:
            return self._session_state
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de session"""
        with self._lock:
            return self._session_stats.copy()
    
    def request_view_change(self, view_name: str) -> None:
        """Demande un changement de vue"""
        self.viewChangeRequested.emit(view_name)
    
    def emit_buffer_overflow_warning(self, usage_percent: float) -> None:
        """Émet un avertissement de débordement de buffer"""
        self.bufferOverflowWarning.emit(usage_percent)
    
    def emit_buffer_overflow(self, overflow_mode: str) -> None:
        """Émet un signal de débordement de buffer"""
        self.bufferOverflow.emit(overflow_mode)
    
    def emit_buffer_reset(self) -> None:
        """Émet un signal de reset du buffer"""
        self.bufferReset.emit()
    
    def emit_processing_progress(self, progress: float) -> None:
        """Émet le progrès du traitement (0-100)"""
        self.processingProgress.emit(max(0.0, min(100.0, progress)))


# Instance globale du bus de signaux
_signal_bus_instance = None
_error_bus_instance = None


def get_signal_bus() -> SignalBus:
    """Retourne l'instance globale du bus de signaux"""
    global _signal_bus_instance
    if _signal_bus_instance is None:
        _signal_bus_instance = SignalBus()
    return _signal_bus_instance


def get_error_bus() -> ErrorBus:
    """Retourne l'instance globale du bus d'erreurs"""
    global _error_bus_instance
    if _error_bus_instance is None:
        _error_bus_instance = ErrorBus()
    return _error_bus_instance


def reset_signal_buses() -> None:
    """Remet à zéro les bus de signaux (pour les tests)"""
    global _signal_bus_instance, _error_bus_instance
    _signal_bus_instance = None
    _error_bus_instance = None