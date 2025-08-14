# -*- coding: utf-8 -*-
"""
Composant ThemeToggle - Commutateur de thème avec design maritime
Permet de basculer entre les thèmes clair et sombre

Auteur: Architecte Logiciel en Chef (ALC)
Date: 2025-01-26
Version: 1.1.0
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, Property, QRect
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont


class ThemeToggle(QWidget):
    """
    Commutateur de thème animé avec design maritime
    """
    
    # Signal émis lors du changement de thème
    themeChanged = Signal(bool)  # True pour sombre, False pour clair
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # État du thème (False = clair, True = sombre)
        self._is_dark = False
        
        # Propriétés d'animation
        self._toggle_position = 0.0
        
        # Configuration de base
        self.setObjectName("themeToggle")
        self.setFixedSize(60, 30)
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation
        self._setup_animation()
        
        # Style de base
        self._apply_base_style()
    
    def _setup_animation(self):
        """Configuration de l'animation de basculement"""
        self.toggle_animation = QPropertyAnimation(self, b"toggle_position")
        self.toggle_animation.setDuration(200)
        self.toggle_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def _apply_base_style(self):
        """Applique le style de base"""
        self.setStyleSheet("""
            #themeToggle {
                background-color: transparent;
                border: none;
            }
        """)
    
    # Propriété pour l'animation
    def get_toggle_position(self):
        return self._toggle_position
    
    def set_toggle_position(self, position):
        self._toggle_position = position
        self.update()
    
    toggle_position = Property(float, get_toggle_position, set_toggle_position)
    
    @property
    def is_dark(self):
        """Retourne True si le thème sombre est actif"""
        return self._is_dark
    
    def set_dark_theme(self, dark=True, animate=True):
        """Active/désactive le thème sombre"""
        if self._is_dark == dark:
            return
        
        self._is_dark = dark
        
        if animate:
            # Animation de basculement
            start_pos = 0.0 if not dark else 1.0
            end_pos = 1.0 if dark else 0.0
            
            self.toggle_animation.setStartValue(start_pos)
            self.toggle_animation.setEndValue(end_pos)
            self.toggle_animation.start()
        else:
            # Changement immédiat
            self._toggle_position = 1.0 if dark else 0.0
            self.update()
        
        # Émettre le signal
        self.themeChanged.emit(dark)
    
    def toggle_theme(self):
        """Bascule entre les thèmes"""
        self.set_dark_theme(not self._is_dark)
    
    def mousePressEvent(self, event):
        """Gestion du clic"""
        if event.button() == Qt.LeftButton:
            self.toggle_theme()
        super().mousePressEvent(event)
    
    def paintEvent(self, event):
        """Dessin personnalisé du commutateur"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dimensions
        rect = self.rect()
        track_rect = QRect(2, 8, rect.width() - 4, rect.height() - 16)
        thumb_size = 18
        thumb_margin = 6
        
        # Couleurs selon le thème
        if self._is_dark:
            track_color = QColor("#2c5aa0")  # Bleu maritime
            thumb_color = QColor("#ffffff")
            track_border = QColor("#1e3d72")
        else:
            track_color = QColor("#e9ecef")
            thumb_color = QColor("#6c757d")
            track_border = QColor("#ced4da")
        
        # Interpolation des couleurs pendant l'animation
        if 0 < self._toggle_position < 1:
            # Mélange des couleurs
            light_track = QColor("#e9ecef")
            dark_track = QColor("#2c5aa0")
            
            r = int(light_track.red() + (dark_track.red() - light_track.red()) * self._toggle_position)
            g = int(light_track.green() + (dark_track.green() - light_track.green()) * self._toggle_position)
            b = int(light_track.blue() + (dark_track.blue() - light_track.blue()) * self._toggle_position)
            
            track_color = QColor(r, g, b)
        
        # Dessiner la piste
        painter.setPen(QPen(track_border, 1))
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track_rect, track_rect.height() // 2, track_rect.height() // 2)
        
        # Position du curseur
        max_thumb_x = track_rect.width() - thumb_size - thumb_margin
        thumb_x = thumb_margin + (max_thumb_x - thumb_margin) * self._toggle_position
        thumb_y = (rect.height() - thumb_size) // 2
        
        thumb_rect = QRect(int(thumb_x), thumb_y, thumb_size, thumb_size)
        
        # Dessiner le curseur
        painter.setPen(QPen(QColor("#ffffff"), 2))
        painter.setBrush(QBrush(thumb_color))
        painter.drawEllipse(thumb_rect)
        
        # Icônes optionnelles (soleil/lune)
        if self._toggle_position < 0.5:
            # Icône soleil (thème clair)
            self._draw_sun_icon(painter, thumb_rect)
        else:
            # Icône lune (thème sombre)
            self._draw_moon_icon(painter, thumb_rect)
    
    def _draw_sun_icon(self, painter, rect):
        """Dessine l'icône du soleil"""
        painter.setPen(QPen(QColor("#ffc107"), 2))
        
        center = rect.center()
        radius = 4
        
        # Cercle central
        painter.drawEllipse(center, radius, radius)
        
        # Rayons
        ray_length = 3
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            start_x = center.x() + (radius + 1) * math.cos(rad)
            start_y = center.y() + (radius + 1) * math.sin(rad)
            end_x = center.x() + (radius + ray_length + 1) * math.cos(rad)
            end_y = center.y() + (radius + ray_length + 1) * math.sin(rad)
            
            painter.drawLine(int(start_x), int(start_y), int(end_x), int(end_y))
    
    def _draw_moon_icon(self, painter, rect):
        """Dessine l'icône de la lune"""
        painter.setPen(QPen(QColor("#6c757d"), 2))
        painter.setBrush(QBrush(QColor("#6c757d")))
        
        center = rect.center()
        radius = 5
        
        # Croissant de lune
        moon_rect = QRect(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        painter.drawEllipse(moon_rect)
        
        # Masque pour créer le croissant
        mask_offset = 3
        mask_rect = QRect(center.x() - radius + mask_offset, center.y() - radius, radius * 2, radius * 2)
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(mask_rect)
    
    def sizeHint(self):
        """Taille recommandée"""
        return self.size()
    
    def minimumSizeHint(self):
        """Taille minimale"""
        return self.size()


class ThemeToggleWithLabel(QWidget):
    """
    Commutateur de thème avec étiquette
    """
    
    # Signal émis lors du changement de thème
    themeChanged = Signal(bool)
    
    def __init__(self, label_text="Thème sombre", parent=None):
        super().__init__(parent)
        
        # Configuration du layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Étiquette
        self.label = QLabel(label_text)
        self.label.setObjectName("themeLabel")
        
        # Commutateur
        self.toggle = ThemeToggle()
        
        # Connexion du signal
        self.toggle.themeChanged.connect(self.themeChanged.emit)
        self.toggle.themeChanged.connect(self._update_label)
        
        # Ajout au layout
        layout.addWidget(self.label)
        layout.addWidget(self.toggle)
        layout.addStretch()
        
        # Style de base
        self._apply_base_style()
    
    def _apply_base_style(self):
        """Applique le style de base"""
        self.setStyleSheet("""
            #themeLabel {
                color: #495057;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: bold;
            }
        """)
    
    def _update_label(self, is_dark):
        """Met à jour l'étiquette selon le thème"""
        if is_dark:
            self.label.setStyleSheet("""
                #themeLabel {
                    color: #ffffff;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
        else:
            self.label.setStyleSheet("""
                #themeLabel {
                    color: #495057;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
    
    @property
    def is_dark(self):
        """Retourne True si le thème sombre est actif"""
        return self.toggle.is_dark
    
    def set_dark_theme(self, dark=True, animate=True):
        """Active/désactive le thème sombre"""
        self.toggle.set_dark_theme(dark, animate)
    
    def toggle_theme(self):
        """Bascule entre les thèmes"""
        self.toggle.toggle_theme()