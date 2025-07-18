#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de vues unifié pour CHNeoWave

Ce module gère la navigation automatique entre les vues (AcquisitionView, AnalysisView)
et l'affichage des notifications d'erreur via des toasts.

Auteur: WaveBuffer-Fixer
Version: 3.0.0
Date: 2025
"""

from PyQt5.QtWidgets import (
    QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QGraphicsOpacityEffect,
    QApplication, QDesktopWidget
)
from PyQt5.QtCore import (
    QObject, pyqtSignal, QTimer, QPropertyAnimation, 
    QEasingCurve, QRect, Qt
)
from PyQt5.QtGui import QFont, QPalette, QColor
from typing import Dict, Any, Optional, Callable
import time
import logging

# Import du système de signaux unifié
try:
    from hrneowave.core.signal_bus import (
        get_signal_bus, get_error_bus, ErrorLevel, ErrorMessage
    )
    UNIFIED_SIGNALS_AVAILABLE = True
except ImportError:
    UNIFIED_SIGNALS_AVAILABLE = False
    logging.warning("Système de signaux unifié non disponible")


class ToastNotification(QWidget):
    """Widget de notification toast pour les erreurs"""
    
    def __init__(self, message: str, level: ErrorLevel, parent=None):
        super().__init__(parent)
        self.message = message
        self.level = level
        self.setup_ui()
        self.setup_animation()
    
    def setup_ui(self):
        """Configure l'interface du toast"""
        self.setFixedSize(400, 80)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Frame principal avec style
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Box)
        self.frame.setLineWidth(2)
        
        # Couleurs selon le niveau d'erreur
        colors = {
            ErrorLevel.INFO: ("#2196F3", "#E3F2FD", "#0D47A1"),
            ErrorLevel.WARNING: ("#FF9800", "#FFF3E0", "#E65100"),
            ErrorLevel.ERROR: ("#F44336", "#FFEBEE", "#B71C1C"),
            ErrorLevel.CRITICAL: ("#9C27B0", "#F3E5F5", "#4A148C")
        }
        
        border_color, bg_color, text_color = colors.get(
            self.level, colors[ErrorLevel.INFO]
        )
        
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
        """)
        
        # Layout du frame
        frame_layout = QHBoxLayout(self.frame)
        frame_layout.setContentsMargins(15, 10, 15, 10)
        
        # Icône selon le niveau
        icons = {
            ErrorLevel.INFO: "ℹ️",
            ErrorLevel.WARNING: "⚠️",
            ErrorLevel.ERROR: "❌",
            ErrorLevel.CRITICAL: "🚨"
        }
        
        icon_label = QLabel(icons.get(self.level, "ℹ️"))
        icon_label.setFont(QFont("Arial", 16))
        frame_layout.addWidget(icon_label)
        
        # Message
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet(f"color: {text_color}; font-weight: bold;")
        frame_layout.addWidget(message_label, 1)
        
        # Bouton fermer
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {border_color};
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {text_color};
            }}
        """)
        close_btn.clicked.connect(self.hide_toast)
        frame_layout.addWidget(close_btn)
        
        layout.addWidget(self.frame)
    
    def setup_animation(self):
        """Configure les animations d'apparition/disparition"""
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_out_animation.finished.connect(self.close)
    
    def show_toast(self, duration: int = 5000):
        """Affiche le toast avec une durée spécifiée"""
        # Positionner en haut à droite de l'écran
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        
        x = screen_rect.width() - self.width() - 20
        y = 20
        self.move(x, y)
        
        # Afficher et animer
        self.show()
        self.fade_in_animation.start()
        
        # Timer pour masquer automatiquement
        if duration > 0:
            QTimer.singleShot(duration, self.hide_toast)
    
    def hide_toast(self):
        """Masque le toast avec animation"""
        self.fade_out_animation.start()


class ViewManager(QObject):
    """Gestionnaire de vues principal pour CHNeoWave"""
    
    # Signaux pour la communication
    view_changed = pyqtSignal(str)  # nom de la nouvelle vue
    error_displayed = pyqtSignal(object)  # ErrorMessage affiché
    
    def __init__(self, stacked_widget: QStackedWidget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.views: Dict[str, QWidget] = {}
        self.current_view = None
        self.active_toasts = []
        self.max_toasts = 3
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
        # Connexion au système de signaux unifié
        if UNIFIED_SIGNALS_AVAILABLE:
            self.signal_bus = get_signal_bus()
            self.error_bus = get_error_bus()
            self._connect_unified_signals()
        else:
            self.signal_bus = None
            self.error_bus = None
            self.logger.warning("Système de signaux unifié non disponible")
    
    def register_view(self, name: str, widget: QWidget) -> None:
        """Enregistre une vue dans le gestionnaire"""
        self.views[name] = widget
        self.stacked_widget.addWidget(widget)
        self.logger.info(f"Vue '{name}' enregistrée")
    
    def switch_to_view(self, view_name: str) -> bool:
        """Change vers la vue spécifiée"""
        if view_name not in self.views:
            self.logger.error(f"Vue '{view_name}' non trouvée")
            if self.error_bus:
                self.error_bus.emit_error(
                    ErrorLevel.ERROR,
                    f"Vue '{view_name}' non trouvée",
                    "ViewManager"
                )
            return False
        
        try:
            widget = self.views[view_name]
            self.stacked_widget.setCurrentWidget(widget)
            self.current_view = view_name
            
            self.view_changed.emit(view_name)
            self.logger.info(f"Changement vers la vue '{view_name}'")
            
            if self.error_bus:
                self.error_bus.emit_info(
                    f"Changement vers la vue '{view_name}'",
                    "ViewManager",
                    {'previous_view': self.current_view}
                )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors du changement de vue: {e}")
            if self.error_bus:
                self.error_bus.emit_error(
                    ErrorLevel.ERROR,
                    f"Erreur lors du changement de vue: {e}",
                    "ViewManager",
                    exception=e
                )
            return False
    
    def get_current_view(self) -> Optional[str]:
        """Retourne le nom de la vue actuelle"""
        return self.current_view
    
    def get_view_widget(self, view_name: str) -> Optional[QWidget]:
        """Retourne le widget d'une vue"""
        return self.views.get(view_name)
    
    def show_error_toast(self, error_msg: ErrorMessage) -> None:
        """Affiche un toast d'erreur"""
        # Limiter le nombre de toasts actifs
        if len(self.active_toasts) >= self.max_toasts:
            # Fermer le plus ancien
            oldest_toast = self.active_toasts.pop(0)
            oldest_toast.hide_toast()
        
        # Créer et afficher le nouveau toast
        toast = ToastNotification(
            message=error_msg.message,
            level=error_msg.level,
            parent=self.stacked_widget
        )
        
        # Positionner les toasts en cascade
        toast_index = len(self.active_toasts)
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        
        x = screen_rect.width() - toast.width() - 20
        y = 20 + (toast_index * (toast.height() + 10))
        toast.move(x, y)
        
        # Durée selon le niveau d'erreur
        durations = {
            ErrorLevel.INFO: 3000,
            ErrorLevel.WARNING: 5000,
            ErrorLevel.ERROR: 7000,
            ErrorLevel.CRITICAL: 10000
        }
        duration = durations.get(error_msg.level, 5000)
        
        self.active_toasts.append(toast)
        toast.show_toast(duration)
        
        # Nettoyer la liste quand le toast se ferme
        def cleanup_toast():
            if toast in self.active_toasts:
                self.active_toasts.remove(toast)
        
        toast.fade_out_animation.finished.connect(cleanup_toast)
        
        self.error_displayed.emit(error_msg)
        self.logger.info(f"Toast affiché: {error_msg.level.value} - {error_msg.message}")
    
    def _connect_unified_signals(self) -> None:
        """Connecte les signaux du système unifié"""
        if not self.signal_bus or not self.error_bus:
            return
        
        # Changement automatique vers AnalysisView après sessionFinished
        self.signal_bus.sessionFinished.connect(self._on_session_finished)
        
        # Demandes de changement de vue
        self.signal_bus.viewChangeRequested.connect(self.switch_to_view)
        
        # Affichage des erreurs via toasts
        self.error_bus.error_occurred.connect(self.show_error_toast)
        
        self.logger.info("Signaux unifiés connectés au ViewManager")
    
    def _on_session_finished(self) -> None:
        """P0: Gestionnaire pour sessionFinished() - change automatiquement vers AnalysisView"""
        self.logger.info("Session terminée, changement automatique vers AnalysisView")
        
        # P0: AnalysisView apparaît quand sessionFinished est reçu
        QTimer.singleShot(1000, lambda: self.switch_to_view("AnalysisView"))
        
        # Afficher une notification de succès
        if self.error_bus:
            self.error_bus.emit_info(
                "Session d'acquisition terminée",
                "ViewManager"
            )
    
    def cleanup_toasts(self) -> None:
        """Nettoie tous les toasts actifs"""
        for toast in self.active_toasts:
            toast.hide_toast()
        self.active_toasts.clear()
        self.logger.info("Tous les toasts ont été nettoyés")


# Instance globale du gestionnaire de vues
_view_manager_instance = None


def get_view_manager(stacked_widget: QStackedWidget = None) -> ViewManager:
    """Retourne l'instance globale du gestionnaire de vues"""
    global _view_manager_instance
    if _view_manager_instance is None and stacked_widget is not None:
        _view_manager_instance = ViewManager(stacked_widget)
    return _view_manager_instance


def reset_view_manager() -> None:
    """Remet à zéro le gestionnaire de vues (pour les tests)"""
    global _view_manager_instance
    if _view_manager_instance:
        _view_manager_instance.cleanup_toasts()
    _view_manager_instance = None