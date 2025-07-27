# -*- coding: utf-8 -*-
"""
Theme Toggle Widget - Maritime Theme 2025
Widget de bascule entre thème clair et sombre
"""

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtGui import QFont, QPainter, QColor, QBrush, QPen

# Golden Ratio Constants
FIBONACCI_SPACING = [8, 13, 21, 34, 55, 89]

class AnimatedToggle(QWidget):
    """
    Interrupteur animé personnalisé pour la bascule de thème
    """
    
    toggled = Signal(bool)  # Signal émis lors du changement d'état
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_dark = False  # État actuel (False = clair, True = sombre)
        self.is_animating = False
        self._handle_position = 0.0  # Position du curseur (0.0 à 1.0)
        
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Configure l'interface du toggle"""
        self.setObjectName("theme_toggle")
        self.setFixedSize(55, 34)  # Fibonacci
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Couleurs
        self.bg_color_light = QColor("#E0E7FF")  # Fond clair
        self.bg_color_dark = QColor("#00ACC1")   # Fond sombre (tidal-cyan)
        self.handle_color = QColor("#F5FBFF")    # Couleur du curseur
        self.border_color = QColor("#2B79B6")    # Bordure
        
    def setup_animations(self):
        """Configure les animations du toggle"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.on_animation_finished)
        
        # Timer pour l'animation manuelle
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_steps = 0
        self.animation_total_steps = 10
        
    def get_handle_position(self):
        """Getter pour la position du curseur"""
        return self._handle_position
        
    def set_handle_position(self, position):
        """Setter pour la position du curseur"""
        self._handle_position = position
        self.update()  # Redessiner le widget
        
    # Propriété Qt pour l'animation
    handle_position = property(get_handle_position, set_handle_position)
    
    def toggle(self):
        """Bascule l'état du toggle"""
        if self.is_animating:
            return
            
        self.is_dark = not self.is_dark
        self.is_animating = True
        
        # Animation manuelle avec timer
        self.start_pos = 1.0 if not self.is_dark else 0.0
        self.end_pos = 1.0 if self.is_dark else 0.0
        self.animation_steps = 0
        
        self.animation_timer.start(25)  # 25ms par étape
        
        # Émettre le signal
        self.toggled.emit(self.is_dark)
        
    def update_animation(self):
        """Met à jour l'animation manuellement"""
        self.animation_steps += 1
        progress = self.animation_steps / self.animation_total_steps
        
        if progress >= 1.0:
            progress = 1.0
            self.animation_timer.stop()
            self.is_animating = False
            
        # Interpolation linéaire
        self._handle_position = self.start_pos + (self.end_pos - self.start_pos) * progress
        self.update()
        
    def on_animation_finished(self):
        """Appelé quand l'animation se termine"""
        self.is_animating = False
        
    def set_dark_mode(self, is_dark: bool):
        """Définit l'état sans animation"""
        if self.is_dark != is_dark:
            self.is_dark = is_dark
            self._handle_position = 1.0 if is_dark else 0.0
            self.update()
            
    def mousePressEvent(self, event):
        """Gestionnaire de clic"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()
        super().mousePressEvent(event)
        
    def paintEvent(self, event):
        """Dessine le toggle personnalisé"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensions
        width = self.width()
        height = self.height()
        radius = height // 2
        handle_radius = radius - 3
        
        # Couleur de fond interpolée
        if self.is_dark:
            bg_color = self.bg_color_dark
        else:
            bg_color = self.bg_color_light
            
        # Dessiner le fond
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawRoundedRect(0, 0, width, height, radius, radius)
        
        # Position du curseur
        handle_x = int((width - 2 * handle_radius - 6) * (1.0 - self._handle_position) + 3)
        handle_y = 3
        
        # Dessiner le curseur
        painter.setBrush(QBrush(self.handle_color))
        painter.setPen(QPen(QColor("#CCCCCC"), 1))
        painter.drawEllipse(handle_x, handle_y, 2 * handle_radius, 2 * handle_radius)
        
        # Icônes (soleil/lune)
        painter.setPen(QPen(QColor("#666666"), 1))
        font = QFont("Segoe UI Emoji", 12)
        painter.setFont(font)
        
        # Icône soleil (côté gauche)
        sun_rect = QRect(8, 8, 18, 18)
        painter.drawText(sun_rect, Qt.AlignmentFlag.AlignCenter, "☀️")
        
        # Icône lune (côté droit)
        moon_rect = QRect(width - 26, 8, 18, 18)
        painter.drawText(moon_rect, Qt.AlignmentFlag.AlignCenter, "🌙")


class ThemeToggle(QFrame):
    """
    Widget complet de bascule de thème avec label et toggle
    """
    
    theme_changed = Signal(bool)  # Signal émis lors du changement de thème
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_dark_mode = False
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface du widget"""
        self.setObjectName("theme_toggle_widget")
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Layout horizontal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(FIBONACCI_SPACING[1], FIBONACCI_SPACING[1], 
                                 FIBONACCI_SPACING[1], FIBONACCI_SPACING[1])
        layout.setSpacing(FIBONACCI_SPACING[1])
        
        # Label
        self.theme_label = QLabel("Thème sombre")
        self.theme_label.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        self.theme_label.setStyleSheet("color: #445868;")
        
        # Toggle switch
        self.toggle_switch = AnimatedToggle()
        self.toggle_switch.toggled.connect(self.on_theme_toggled)
        
        # Ajouter au layout
        layout.addWidget(self.theme_label)
        layout.addStretch()
        layout.addWidget(self.toggle_switch)
        
        # Style du widget
        self.setStyleSheet("""
            QFrame#theme_toggle_widget {
                background-color: transparent;
                border: 1px solid #E0E7FF;
                border-radius: 13px;
                padding: 8px;
            }
            
            QFrame#theme_toggle_widget:hover {
                background-color: rgba(0, 172, 193, 0.05);
                border-color: #00ACC1;
            }
        """)
        
    def on_theme_toggled(self, is_dark: bool):
        """Gestionnaire de changement de thème"""
        self.is_dark_mode = is_dark
        
        # Mettre à jour le label
        if is_dark:
            self.theme_label.setText("Thème sombre")
            self.theme_label.setStyleSheet("color: #F5FBFF;")
        else:
            self.theme_label.setText("Thème clair")
            self.theme_label.setStyleSheet("color: #445868;")
            
        # Émettre le signal
        self.theme_changed.emit(is_dark)
        
    def set_dark_mode(self, is_dark: bool):
        """Définit le mode sombre depuis l'extérieur"""
        if self.is_dark_mode != is_dark:
            self.toggle_switch.set_dark_mode(is_dark)
            self.on_theme_toggled(is_dark)
            
    def get_dark_mode(self) -> bool:
        """Retourne l'état actuel du thème"""
        return self.is_dark_mode
        
    def apply_theme(self, is_dark: bool):
        """Applique le thème au widget lui-même"""
        if is_dark:
            # Thème sombre
            self.setStyleSheet("""
                QFrame#theme_toggle_widget {
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid #2B79B6;
                    border-radius: 13px;
                    padding: 8px;
                }
                
                QFrame#theme_toggle_widget:hover {
                    background-color: rgba(0, 172, 193, 0.1);
                    border-color: #00ACC1;
                }
            """)
        else:
            # Thème clair
            self.setStyleSheet("""
                QFrame#theme_toggle_widget {
                    background-color: transparent;
                    border: 1px solid #E0E7FF;
                    border-radius: 13px;
                    padding: 8px;
                }
                
                QFrame#theme_toggle_widget:hover {
                    background-color: rgba(0, 172, 193, 0.05);
                    border-color: #00ACC1;
                }
            """)


class CompactThemeToggle(QPushButton):
    """
    Version compacte du toggle de thème (bouton simple)
    """
    
    theme_changed = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.is_dark_mode = False
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface du bouton compact"""
        self.setObjectName("compact_theme_toggle")
        self.setFixedSize(FIBONACCI_SPACING[3], FIBONACCI_SPACING[3])  # 34x34
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        
        # Icône et tooltip
        self.update_appearance()
        
        # Connexion du signal
        self.clicked.connect(self.toggle_theme)
        
    def update_appearance(self):
        """Met à jour l'apparence selon le thème"""
        if self.is_dark_mode:
            self.setText("🌙")
            self.setToolTip("Passer au thème clair")
            self.setStyleSheet("""
                QPushButton#compact_theme_toggle {
                    background-color: #0A1929;
                    color: #F5FBFF;
                    border: 2px solid #2B79B6;
                    border-radius: 17px;
                    font-size: 16px;
                }
                
                QPushButton#compact_theme_toggle:hover {
                    background-color: #2B79B6;
                    border-color: #00ACC1;
                }
                
                QPushButton#compact_theme_toggle:pressed {
                    background-color: #055080;
                }
            """)
        else:
            self.setText("☀️")
            self.setToolTip("Passer au thème sombre")
            self.setStyleSheet("""
                QPushButton#compact_theme_toggle {
                    background-color: #F5FBFF;
                    color: #0A1929;
                    border: 2px solid #E0E7FF;
                    border-radius: 17px;
                    font-size: 16px;
                }
                
                QPushButton#compact_theme_toggle:hover {
                    background-color: #E0E7FF;
                    border-color: #00ACC1;
                }
                
                QPushButton#compact_theme_toggle:pressed {
                    background-color: #D0D7EF;
                }
            """)
            
    def toggle_theme(self):
        """Bascule le thème"""
        self.is_dark_mode = not self.is_dark_mode
        self.setChecked(self.is_dark_mode)
        self.update_appearance()
        self.theme_changed.emit(self.is_dark_mode)
        
    def set_dark_mode(self, is_dark: bool):
        """Définit le mode sombre"""
        if self.is_dark_mode != is_dark:
            self.is_dark_mode = is_dark
            self.setChecked(is_dark)
            self.update_appearance()
            
    def get_dark_mode(self) -> bool:
        """Retourne l'état actuel"""
        return self.is_dark_mode