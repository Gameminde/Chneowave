# -*- coding: utf-8 -*-
"""
Composant ModernCard - Carte moderne avec design maritime
Utilise le nombre d'or pour les proportions

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPainter, QLinearGradient, QColor, QPalette


class ModernCard(QFrame):
    """
    Carte moderne avec design maritime et proportions dorées
    """
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        
        self.title = title
        self.content_widget = None
        
        # Configuration de base
        self.setObjectName("modernCard")
        self.setFrameShape(QFrame.NoFrame)
        
        # Configuration de l'interface
        self._setup_ui()
        self._apply_style()
    
    def _setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # En-tête avec titre (si fourni)
        if self.title:
            self._create_header(main_layout)
        
        # Zone de contenu
        self.content_widget = QWidget()
        self.content_widget.setObjectName("cardContent")
        main_layout.addWidget(self.content_widget)
    
    def _create_header(self, layout):
        """Crée l'en-tête de la carte"""
        header_frame = QFrame()
        header_frame.setObjectName("cardHeader")
        header_frame.setFixedHeight(50)  # Proportion dorée
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Titre
        title_label = QLabel(self.title)
        title_label.setObjectName("cardTitle")
        title_font = QFont("Segoe UI", 14, QFont.Bold)
        title_label.setFont(title_font)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def _apply_style(self):
        """Applique le style maritime moderne"""
        self.setStyleSheet("""
            #modernCard {
                background-color: #ffffff;
                border: 1px solid #e0e6ed;
                border-radius: 12px;
                margin: 5px;
            }
            
            #modernCard:hover {
                border-color: #2c5aa0;
            }
            
            #cardHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c5aa0,
                    stop:1 #1e3d72);
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom: 1px solid #e0e6ed;
            }
            
            #cardTitle {
                color: white;
                font-weight: bold;
            }
            
            #cardContent {
                background-color: #ffffff;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
                padding: 20px;
            }
        """)
    
    def set_title(self, title):
        """Définit le titre de la carte"""
        self.title = title
        # Recréer l'interface si nécessaire
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)
    
    def get_content_widget(self):
        """Retourne le widget de contenu"""
        return self.content_widget
    
    def add_content_layout(self, layout):
        """Ajoute un layout au contenu"""
        if self.content_widget.layout():
            # Supprimer l'ancien layout
            old_layout = self.content_widget.layout()
            while old_layout.count():
                old_layout.takeAt(0)
        
        self.content_widget.setLayout(layout)
    
    def set_content_widget(self, widget):
        """Définit le widget de contenu"""
        if self.content_widget:
            # Remplacer le widget de contenu
            layout = self.layout()
            layout.removeWidget(self.content_widget)
            self.content_widget.deleteLater()
        
        self.content_widget = widget
        self.content_widget.setObjectName("cardContent")
        self.layout().addWidget(self.content_widget)
    
    def animate_entrance(self):
        """Animation d'entrée de la carte"""
        self.setProperty("opacity", 0.0)
        
        self.fade_animation = QPropertyAnimation(self, b"opacity")
        self.fade_animation.setDuration(400)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.start()
    
    def animate_hover_in(self):
        """Animation au survol"""
        # Animation de survol simplifiée (propriétés CSS non supportées supprimées)
        pass
    
    def animate_hover_out(self):
        """Animation de sortie du survol"""
        self._apply_style()
    
    def enterEvent(self, event):
        """Événement d'entrée de la souris"""
        self.animate_hover_in()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Événement de sortie de la souris"""
        self.animate_hover_out()
        super().leaveEvent(event)