# -*- coding: utf-8 -*-
"""
KPI Card Widget - Maritime Theme 2025
Carte d'indicateur de performance avec animations et états visuels
"""

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtGui import QFont, QPainter, QPen, QColor, QLinearGradient

# Golden Ratio Constants
FIBONACCI_SPACING = [8, 13, 21, 34, 55, 89]

class KPICard(QFrame):
    """
    Carte KPI avec design maritime et animations fluides
    États: normal, warning, critical, success
    """
    
    # Signaux
    clicked = Signal(str)  # Nom du KPI cliqué
    value_changed = Signal(str, str)  # title, new_value
    
    def __init__(self, title: str, value: str, unit: str = "", status: str = "normal", parent=None):
        super().__init__(parent)
        
        self.title = title
        self.current_value = value
        self.unit = unit
        self.status = status
        self.is_hovered = False
        
        # Animations
        self.hover_animation = None
        self.value_animation = None
        
        self.setup_ui()
        self.setup_animations()
        self.apply_status_style()
        
    def setup_ui(self):
        """Configure l'interface de la carte KPI"""
        self.setObjectName("kpi_card")
        self.setFixedSize(200, 120)  # Ratio proche du Golden Ratio
        self.setFrameStyle(QFrame.Shape.Box)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(FIBONACCI_SPACING[1], FIBONACCI_SPACING[1], 
                                 FIBONACCI_SPACING[1], FIBONACCI_SPACING[1])
        layout.setSpacing(FIBONACCI_SPACING[0])
        
        # === HEADER avec titre ===
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("kpi_title")
        title_font = QFont("Inter", 11, QFont.Weight.Medium)
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)
        
        # === VALEUR PRINCIPALE ===
        value_layout = QHBoxLayout()
        value_layout.setSpacing(FIBONACCI_SPACING[0])
        
        self.value_label = QLabel(self.current_value)
        self.value_label.setObjectName("kpi_value")
        value_font = QFont("Inter", 24, QFont.Weight.Bold)
        self.value_label.setFont(value_font)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # === UNITÉ ===
        self.unit_label = QLabel(self.unit)
        self.unit_label.setObjectName("kpi_unit")
        unit_font = QFont("Inter", 10)
        self.unit_label.setFont(unit_font)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # === INDICATEUR DE STATUT ===
        self.status_indicator = QFrame()
        self.status_indicator.setObjectName("status_indicator")
        self.status_indicator.setFixedSize(4, 60)
        
        # Assemblage du layout de valeur
        value_layout.addWidget(self.status_indicator)
        value_layout.addWidget(self.value_label, 1)
        value_layout.addWidget(self.unit_label)
        
        # Assemblage final
        layout.addWidget(self.title_label)
        layout.addLayout(value_layout)
        layout.addStretch()
        
        # Style de base
        self.setStyleSheet("""
            QFrame#kpi_card {
                background-color: #F5FBFF;
                border: 1px solid #E0E7FF;
                border-radius: 13px;
                padding: 8px;
            }
            
            QFrame#kpi_card:hover {
                border: 2px solid #00ACC1;
            }
            
            QLabel#kpi_title {
                color: #445868;
                font-weight: bold;
                margin-bottom: 8px;
            }
            
            QLabel#kpi_value {
                color: #0A1929;
                font-weight: bold;
            }
            
            QLabel#kpi_unit {
                color: #445868;
                margin-left: 4px;
            }
        """)
        
    def setup_animations(self):
        """Configure les animations de la carte"""
        # Animation de hover
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Animation de changement de valeur
        self.value_animation = QPropertyAnimation(self.value_label, b"geometry")
        self.value_animation.setDuration(300)
        self.value_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
    def apply_status_style(self):
        """Applique le style selon le statut"""
        status_colors = {
            "normal": "#00ACC1",    # tidal-cyan
            "success": "#4CAF50",   # vert
            "warning": "#FF9800",   # orange
            "critical": "#FF6B47"   # coral-alert
        }
        
        color = status_colors.get(self.status, "#00ACC1")
        
        # Style de l'indicateur de statut
        status_style = f"QFrame#status_indicator {{ background-color: {color}; border-radius: 2px; }}"
        self.status_indicator.setStyleSheet(status_style)
        
        # Couleur de la valeur selon le statut
        if self.status == "critical":
            value_color = "#FF6B47"
        elif self.status == "warning":
            value_color = "#FF9800"
        elif self.status == "success":
            value_color = "#4CAF50"
        else:
            value_color = "#0A1929"
            
        value_style = f"QLabel#kpi_value {{ color: {value_color}; font-weight: bold; }}"
        self.value_label.setStyleSheet(value_style)
        
    def update_value(self, new_value: str, new_status: str = None):
        """Met à jour la valeur avec animation"""
        old_value = self.current_value
        self.current_value = new_value
        
        if new_status:
            self.status = new_status
            self.apply_status_style()
            
        # Animation de changement
        self.animate_value_change(old_value, new_value)
        
        # Émettre le signal
        self.value_changed.emit(self.title, new_value)
        
    def animate_value_change(self, old_value: str, new_value: str):
        """Anime le changement de valeur"""
        # Effet de pulsation
        original_geometry = self.value_label.geometry()
        
        # Agrandir légèrement
        expanded_geometry = QRect(
            original_geometry.x() - 2,
            original_geometry.y() - 2,
            original_geometry.width() + 4,
            original_geometry.height() + 4
        )
        
        # Animation d'expansion puis retour
        self.value_animation.setStartValue(original_geometry)
        self.value_animation.setKeyValueAt(0.5, expanded_geometry)
        self.value_animation.setEndValue(original_geometry)
        
        # Changer la valeur au milieu de l'animation
        def change_text():
            self.value_label.setText(new_value)
            
        QTimer.singleShot(150, change_text)
        self.value_animation.start()
        
    def enterEvent(self, event):
        """Gestionnaire d'entrée de la souris"""
        super().enterEvent(event)
        self.is_hovered = True
        self.animate_hover(True)
        
    def leaveEvent(self, event):
        """Gestionnaire de sortie de la souris"""
        super().leaveEvent(event)
        self.is_hovered = False
        self.animate_hover(False)
        
    def animate_hover(self, entering: bool):
        """Anime l'effet de hover"""
        current_geometry = self.geometry()
        
        if entering:
            # Légère élévation
            new_geometry = QRect(
                current_geometry.x(),
                current_geometry.y() - 2,
                current_geometry.width(),
                current_geometry.height()
            )
        else:
            # Retour à la position normale
            new_geometry = QRect(
                current_geometry.x(),
                current_geometry.y() + 2,
                current_geometry.width(),
                current_geometry.height()
            )
            
        self.hover_animation.setStartValue(current_geometry)
        self.hover_animation.setEndValue(new_geometry)
        self.hover_animation.start()
        
    def mousePressEvent(self, event):
        """Gestionnaire de clic"""
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.title)
            
    def paintEvent(self, event):
        """Gestionnaire de peinture personnalisé pour les ombres"""
        super().paintEvent(event)
        
        if self.is_hovered:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Ombre portée
            shadow_color = QColor(0, 172, 193, 30)  # tidal-cyan avec transparence
            painter.setPen(QPen(shadow_color, 1))
            
            # Dessiner l'ombre
            shadow_rect = self.rect().adjusted(2, 2, 2, 2)
            painter.drawRoundedRect(shadow_rect, 13, 13)
            
    def set_theme(self, is_dark: bool):
        """Applique le thème sombre ou clair"""
        if is_dark:
            # Thème sombre
            self.setStyleSheet("""
                QFrame#kpi_card {
                    background-color: #1A2332;
                    border: 1px solid #2B79B6;
                    border-radius: 13px;
                    padding: 8px;
                }
                
                QFrame#kpi_card:hover {
                    border: 2px solid #00ACC1;
                }
                
                QLabel#kpi_title {
                    color: #F5FBFF;
                    font-weight: bold;
                    margin-bottom: 8px;
                }
                
                QLabel#kpi_value {
                    color: #F5FBFF;
                    font-weight: bold;
                }
                
                QLabel#kpi_unit {
                    color: #F5FBFF;
                    margin-left: 4px;
                }
            """)
        else:
            # Thème clair (défaut)
            self.setStyleSheet("""
                QFrame#kpi_card {
                    background-color: #F5FBFF;
                    border: 1px solid #E0E7FF;
                    border-radius: 13px;
                    padding: 8px;
                }
                
                QFrame#kpi_card:hover {
                    border: 2px solid #00ACC1;
                }
                
                QLabel#kpi_title {
                    color: #445868;
                    font-weight: bold;
                    margin-bottom: 8px;
                }
                
                QLabel#kpi_value {
                    color: #0A1929;
                    font-weight: bold;
                }
                
                QLabel#kpi_unit {
                    color: #445868;
                    margin-left: 4px;
                }
            """)
            
        # Réappliquer le style de statut
        self.apply_status_style()
        
    def get_value(self) -> str:
        """Retourne la valeur actuelle"""
        return self.current_value
        
    def get_status(self) -> str:
        """Retourne le statut actuel"""
        return self.status
        
    def set_clickable(self, clickable: bool):
        """Active/désactive la capacité de clic"""
        if clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            
    def set_status(self, new_status: str):
        """Met à jour le statut de la carte KPI"""
        self.status = new_status
        self.apply_status_style()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    
    # Test des cartes KPI
    window = QWidget()
    layout = QHBoxLayout(window)
    
    # Différents états
    cards = [
        KPICard("CPU Usage", "45", "%", "normal"),
        KPICard("Memory", "78", "%", "warning"),
        KPICard("Disk Space", "92", "%", "critical"),
        KPICard("Sensors", "8", "active", "success")
    ]
    
    for card in cards:
        card.clicked.connect(lambda title: print(f"Clicked: {title}"))
        card.value_changed.connect(lambda title, value: print(f"{title}: {value}"))
        layout.addWidget(card)
        
    window.setWindowTitle("KPI Cards Test - Maritime Theme")
    window.resize(900, 200)
    window.show()
    
    # Test de mise à jour automatique
    import random
    from PySide6.QtCore import QTimer
    
    def update_random_card():
        card = random.choice(cards)
        new_value = str(random.randint(10, 99))
        new_status = random.choice(["normal", "warning", "critical", "success"])
        card.update_value(new_value, new_status)
        
    timer = QTimer()
    timer.timeout.connect(update_random_card)
    timer.start(3000)  # Toutes les 3 secondes
    
    sys.exit(app.exec())