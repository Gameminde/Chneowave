#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration des graphiques maritimes modernisés - Phase 6
Exemples d'utilisation des animations et du style maritime
"""

import sys
import logging
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QLabel, QTabWidget
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont

try:
    import numpy as np
    import pyqtgraph as pg
except ImportError:
    np = None
    pg = None
    print("numpy et pyqtgraph requis pour cette démonstration")
    sys.exit(1)

from .maritime_graphs import (
    create_maritime_plot, 
    apply_maritime_theme,
    MaritimeGraphStyle,
    MARITIME_GRAPH_COLORS
)

logger = logging.getLogger(__name__)

class MaritimeGraphDemo(QMainWindow):
    """Démonstration des graphiques maritimes avec animations"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHNeoWave - Démonstration Graphiques Maritimes Phase 6")
        self.setGeometry(100, 100, 1400, 900)
        
        # Données de démonstration
        self.time_data = np.linspace(0, 10, 100)
        self.wave_data = np.sin(self.time_data) * np.exp(-self.time_data/10)
        self.current_point = 0
        
        # Timer pour animation temps réel
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_realtime_data)
        
        self._setup_ui()
        self._setup_demo_data()
        
        logger.info("Démonstration graphiques maritimes initialisée")
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Titre
        title_label = QLabel("Graphiques Maritimes Modernisés - Phase 6")
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {MARITIME_GRAPH_COLORS['ocean_deep']};")
        layout.addWidget(title_label)
        
        # Onglets de démonstration
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Onglet 1: Animations de courbes
        self._create_curve_animation_tab()
        
        # Onglet 2: Graphiques temps réel
        self._create_realtime_tab()
        
        # Onglet 3: Graphiques multiples
        self._create_multiple_plots_tab()
        
        # Contrôles
        controls_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Démarrer Animations")
        self.start_btn.clicked.connect(self._start_animations)
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MARITIME_GRAPH_COLORS['harbor_blue']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {MARITIME_GRAPH_COLORS['steel_blue']};
            }}
        """)
        
        self.stop_btn = QPushButton("Arrêter")
        self.stop_btn.clicked.connect(self._stop_animations)
        self.stop_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MARITIME_GRAPH_COLORS['coral_alert']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #E64A19;
            }}
        """)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self._reset_demos)
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {MARITIME_GRAPH_COLORS['storm_gray']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #455A64;
            }}
        """)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.reset_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
    
    def _create_curve_animation_tab(self):
        """Crée l'onglet de démonstration des animations de courbes"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Description
        desc_label = QLabel("Démonstration des animations d'apparition et de transition des courbes")
        desc_label.setStyleSheet(f"color: {MARITIME_GRAPH_COLORS['storm_gray']}; font-size: 12px;")
        layout.addWidget(desc_label)
        
        # Graphique principal
        self.curve_plot = create_maritime_plot(
            "curve_demo",
            parent=tab_widget,
            title="Animations de Courbes Maritimes",
            x_label="Temps (s)",
            y_label="Amplitude"
        )
        layout.addWidget(self.curve_plot)
        
        self.tab_widget.addTab(tab_widget, "Animations de Courbes")
    
    def _create_realtime_tab(self):
        """Crée l'onglet de démonstration temps réel"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Description
        desc_label = QLabel("Simulation d'acquisition de données en temps réel avec animations fluides")
        desc_label.setStyleSheet(f"color: {MARITIME_GRAPH_COLORS['storm_gray']}; font-size: 12px;")
        layout.addWidget(desc_label)
        
        # Graphique temps réel
        self.realtime_plot = create_maritime_plot(
            "realtime_demo",
            parent=tab_widget,
            title="Acquisition Temps Réel",
            x_label="Temps (s)",
            y_label="Signal"
        )
        layout.addWidget(self.realtime_plot)
        
        self.tab_widget.addTab(tab_widget, "Temps Réel")
    
    def _create_multiple_plots_tab(self):
        """Crée l'onglet avec plusieurs graphiques"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Description
        desc_label = QLabel("Plusieurs graphiques avec palette maritime cohérente")
        desc_label.setStyleSheet(f"color: {MARITIME_GRAPH_COLORS['storm_gray']}; font-size: 12px;")
        layout.addWidget(desc_label)
        
        # Layout pour 2x2 graphiques
        plots_layout = QHBoxLayout()
        
        # Colonne gauche
        left_column = QVBoxLayout()
        
        self.plot1 = create_maritime_plot(
            "multi_1",
            parent=tab_widget,
            title="Houle",
            x_label="Temps",
            y_label="Hauteur (m)"
        )
        left_column.addWidget(self.plot1)
        
        self.plot2 = create_maritime_plot(
            "multi_2",
            parent=tab_widget,
            title="Courant",
            x_label="Temps",
            y_label="Vitesse (m/s)"
        )
        left_column.addWidget(self.plot2)
        
        # Colonne droite
        right_column = QVBoxLayout()
        
        self.plot3 = create_maritime_plot(
            "multi_3",
            parent=tab_widget,
            title="Pression",
            x_label="Temps",
            y_label="Pression (Pa)"
        )
        right_column.addWidget(self.plot3)
        
        self.plot4 = create_maritime_plot(
            "multi_4",
            parent=tab_widget,
            title="Température",
            x_label="Temps",
            y_label="Température (°C)"
        )
        right_column.addWidget(self.plot4)
        
        plots_layout.addLayout(left_column)
        plots_layout.addLayout(right_column)
        layout.addLayout(plots_layout)
        
        self.tab_widget.addTab(tab_widget, "Graphiques Multiples")
    
    def _setup_demo_data(self):
        """Configure les données de démonstration"""
        # Données pour animations de courbes
        t = np.linspace(0, 4*np.pi, 200)
        
        # Différentes courbes avec animations
        self.demo_curves = {
            'sine': np.sin(t),
            'cosine': np.cos(t),
            'damped': np.sin(t) * np.exp(-t/10),
            'wave': np.sin(t) + 0.5 * np.sin(3*t)
        }
        
        self.demo_time = t
        
        # Données temps réel
        self.realtime_buffer = np.zeros(100)
        self.realtime_time = np.linspace(0, 10, 100)
    
    def _start_animations(self):
        """Démarre toutes les animations"""
        logger.info("Démarrage des animations de démonstration")
        
        # Animation des courbes
        self._animate_curves()
        
        # Animation temps réel
        self.animation_timer.start(50)  # 20 FPS
        
        # Graphiques multiples
        self._animate_multiple_plots()
    
    def _animate_curves(self):
        """Anime les courbes de démonstration"""
        colors = [0, 1, 2, 3]  # Indices de couleurs
        
        for i, (name, data) in enumerate(self.demo_curves.items()):
            # Délai progressif pour chaque courbe
            QTimer.singleShot(i * 500, lambda d=data, c=colors[i], n=name: 
                             self.curve_plot.add_animated_curve(n, self.demo_time, d, c, 2000))
    
    def _update_realtime_data(self):
        """Met à jour les données temps réel"""
        # Simulation de nouvelles données
        new_value = np.sin(self.current_point * 0.1) + 0.3 * np.random.randn()
        
        # Décaler le buffer
        self.realtime_buffer[:-1] = self.realtime_buffer[1:]
        self.realtime_buffer[-1] = new_value
        
        # Mettre à jour le graphique
        if hasattr(self.realtime_plot, 'curves') and 'realtime' in self.realtime_plot.curves:
            self.realtime_plot.update_curve_data('realtime', self.realtime_time, self.realtime_buffer)
        else:
            self.realtime_plot.add_animated_curve('realtime', self.realtime_time, self.realtime_buffer, 0, 100)
        
        self.current_point += 1
    
    def _animate_multiple_plots(self):
        """Anime les graphiques multiples"""
        t = np.linspace(0, 2*np.pi, 50)
        
        # Données différentes pour chaque graphique
        data_sets = [
            (np.sin(t), "Houle sinusoïdale"),
            (np.cos(t) * 2, "Courant cosinus"),
            (np.sin(2*t) + 1, "Pression oscillante"),
            (np.sin(t/2) * 10 + 20, "Température variable")
        ]
        
        plots = [self.plot1, self.plot2, self.plot3, self.plot4]
        
        for i, (plot, (data, name)) in enumerate(zip(plots, data_sets)):
            QTimer.singleShot(i * 300, lambda p=plot, d=data, t=t, n=name, c=i: 
                             p.add_animated_curve(n, t, d, c, 1500))
    
    def _stop_animations(self):
        """Arrête toutes les animations"""
        logger.info("Arrêt des animations")
        self.animation_timer.stop()
    
    def _reset_demos(self):
        """Remet à zéro toutes les démonstrations"""
        logger.info("Reset des démonstrations")
        
        # Arrêter les animations
        self._stop_animations()
        
        # Vider tous les graphiques
        plots = [self.curve_plot, self.realtime_plot, self.plot1, self.plot2, self.plot3, self.plot4]
        for plot in plots:
            plot.clear_all_curves()
        
        # Reset des données
        self.current_point = 0
        self.realtime_buffer = np.zeros(100)

def main():
    """Fonction principale de démonstration"""
    logging.basicConfig(level=logging.INFO)
    
    app = QApplication(sys.argv)
    
    # Style global maritime
    app.setStyleSheet(f"""
        QMainWindow {{
            background-color: {MARITIME_GRAPH_COLORS['foam_white']};
        }}
        QTabWidget::pane {{
            border: 2px solid {MARITIME_GRAPH_COLORS['storm_gray']};
            background-color: {MARITIME_GRAPH_COLORS['foam_white']};
        }}
        QTabBar::tab {{
            background-color: {MARITIME_GRAPH_COLORS['storm_gray']};
            color: white;
            padding: 8px 16px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {MARITIME_GRAPH_COLORS['harbor_blue']};
        }}
    """)
    
    demo = MaritimeGraphDemo()
    demo.show()
    
    return app.exec()

if __name__ == "__main__":
    main()