#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dock État Capteurs - HRNeoWave v3.0
Affichage en temps réel de l'état des capteurs de houle

Auteur: Équipe HRNeoWave
Date: 2025
"""

import sys
from datetime import datetime
from typing import Dict, List, Optional, Any

try:
    from PyQt5.QtWidgets import (
        QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
        QLabel, QPushButton, QFrame, QScrollArea, QGroupBox,
        QProgressBar, QSpinBox, QDoubleSpinBox, QCheckBox
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
    from PyQt5.QtGui import QFont, QPalette, QPixmap, QPainter, QBrush, QColor
except ImportError:
    print("⚠️ PyQt5 non disponible pour EtatCapteursDock")
    sys.exit(1)

try:
    from ..theme import get_color, apply_widget_class, CLASS_ACCENT
except ImportError:
    # Fallback si le thème n'est pas disponible
    def get_color(color_name):
        return "#2196F3"
    def apply_widget_class(widget, class_name):
        pass
    CLASS_ACCENT = "accent"


class CapteurWidget(QFrame):
    """Widget représentant un capteur individuel"""
    
    # Signaux
    capteur_clicked = pyqtSignal(int)  # ID du capteur
    
    def __init__(self, capteur_id: int, nom: str = "", parent=None):
        super().__init__(parent)
        self.capteur_id = capteur_id
        self.nom = nom or f"Capteur {capteur_id}"
        
        # État du capteur
        self.etat = "Déconnecté"  # Déconnecté, Connecté, Acquisition, Erreur
        self.signal_quality = 0.0  # 0-100%
        self.last_value = 0.0
        self.sample_rate = 0
        self.total_samples = 0
        
        self._setup_ui()
        self._apply_style()
    
    def _setup_ui(self):
        """Configure l'interface du widget capteur"""
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setMinimumHeight(120)
        self.setMaximumHeight(150)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)
        
        # En-tête avec nom et ID
        header_layout = QHBoxLayout()
        
        self.label_nom = QLabel(self.nom)
        self.label_nom.setFont(QFont("Arial", 9, QFont.Bold))
        header_layout.addWidget(self.label_nom)
        
        header_layout.addStretch()
        
        self.label_id = QLabel(f"#{self.capteur_id}")
        self.label_id.setFont(QFont("Arial", 8))
        header_layout.addWidget(self.label_id)
        
        layout.addLayout(header_layout)
        
        # Indicateur d'état
        self.label_etat = QLabel(self.etat)
        self.label_etat.setAlignment(Qt.AlignCenter)
        self.label_etat.setFont(QFont("Arial", 8, QFont.Bold))
        self.label_etat.setMinimumHeight(20)
        layout.addWidget(self.label_etat)
        
        # Barre de qualité du signal
        signal_layout = QHBoxLayout()
        signal_layout.addWidget(QLabel("Signal:"))
        
        self.progress_signal = QProgressBar()
        self.progress_signal.setRange(0, 100)
        self.progress_signal.setValue(0)
        self.progress_signal.setMaximumHeight(12)
        signal_layout.addWidget(self.progress_signal)
        
        self.label_signal_pct = QLabel("0%")
        self.label_signal_pct.setMinimumWidth(30)
        signal_layout.addWidget(self.label_signal_pct)
        
        layout.addLayout(signal_layout)
        
        # Informations techniques
        info_layout = QGridLayout()
        info_layout.setSpacing(2)
        
        info_layout.addWidget(QLabel("Valeur:"), 0, 0)
        self.label_valeur = QLabel("0.000")
        self.label_valeur.setFont(QFont("Courier", 8))
        info_layout.addWidget(self.label_valeur, 0, 1)
        
        info_layout.addWidget(QLabel("Freq:"), 1, 0)
        self.label_freq = QLabel("0 Hz")
        self.label_freq.setFont(QFont("Courier", 8))
        info_layout.addWidget(self.label_freq, 1, 1)
        
        info_layout.addWidget(QLabel("Échant:"), 2, 0)
        self.label_samples = QLabel("0")
        self.label_samples.setFont(QFont("Courier", 8))
        info_layout.addWidget(self.label_samples, 2, 1)
        
        layout.addLayout(info_layout)
        
        # Rendre le widget cliquable
        self.mousePressEvent = self._on_click
    
    def _apply_style(self):
        """Applique le style HRNeoWave au widget"""
        self._update_etat_style()
    
    def _update_etat_style(self):
        """Met à jour le style selon l'état du capteur"""
        if self.etat == "Connecté":
            color = get_color("success")
            bg_color = get_color("success_bg")
        elif self.etat == "Acquisition":
            color = get_color("accent")
            bg_color = get_color("accent_bg")
        elif self.etat == "Erreur":
            color = get_color("error")
            bg_color = get_color("error_bg")
        else:  # Déconnecté
            color = get_color("text_secondary")
            bg_color = get_color("surface")
        
        # Style de l'indicateur d'état
        self.label_etat.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {color};
                border: 1px solid {color};
                border-radius: 4px;
                padding: 2px;
            }}
        """)
        
        # Style de la barre de progression
        if self.signal_quality >= 80:
            progress_color = get_color("success")
        elif self.signal_quality >= 50:
            progress_color = get_color("warning")
        else:
            progress_color = get_color("error")
        
        self.progress_signal.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {get_color("border")};
                border-radius: 2px;
                text-align: center;
                background-color: {get_color("surface")};
            }}
            QProgressBar::chunk {{
                background-color: {progress_color};
                border-radius: 1px;
            }}
        """)
    
    def set_etat(self, etat: str):
        """Définit l'état du capteur"""
        self.etat = etat
        self.label_etat.setText(etat)
        self._update_etat_style()
    
    def set_signal_quality(self, quality: float):
        """Définit la qualité du signal (0-100)"""
        self.signal_quality = max(0, min(100, quality))
        self.progress_signal.setValue(int(self.signal_quality))
        self.label_signal_pct.setText(f"{self.signal_quality:.0f}%")
        self._update_etat_style()
    
    def set_valeur(self, valeur: float):
        """Définit la dernière valeur mesurée"""
        self.last_value = valeur
        self.label_valeur.setText(f"{valeur:.3f}")
    
    def set_sample_rate(self, rate: int):
        """Définit la fréquence d'échantillonnage"""
        self.sample_rate = rate
        self.label_freq.setText(f"{rate} Hz")
    
    def set_total_samples(self, samples: int):
        """Définit le nombre total d'échantillons"""
        self.total_samples = samples
        if samples >= 1000000:
            self.label_samples.setText(f"{samples/1000000:.1f}M")
        elif samples >= 1000:
            self.label_samples.setText(f"{samples/1000:.1f}K")
        else:
            self.label_samples.setText(str(samples))
    
    def _on_click(self, event):
        """Gère le clic sur le widget"""
        self.capteur_clicked.emit(self.capteur_id)


class EtatCapteursDock(QDockWidget):
    """Dock widget pour afficher l'état des capteurs"""
    
    # Signaux
    capteur_selected = pyqtSignal(int)  # ID du capteur sélectionné
    capteurs_updated = pyqtSignal(dict)  # Données des capteurs
    
    def __init__(self, parent=None):
        super().__init__("État Capteurs", parent)
        
        # Configuration
        self.nb_capteurs = 4
        self.capteurs: Dict[int, CapteurWidget] = {}
        self.auto_update = True
        self.update_interval = 500  # ms
        
        # Timer pour mise à jour automatique
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._auto_update)
        
        # Configuration de l'interface
        self._setup_ui()
        self._apply_style()
        
        # Démarrer la mise à jour automatique
        if self.auto_update:
            self.update_timer.start(self.update_interval)
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # Widget principal
        main_widget = QWidget()
        self.setWidget(main_widget)
        
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        
        # En-tête avec contrôles
        self._setup_header(layout)
        
        # Zone de défilement pour les capteurs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget conteneur pour les capteurs
        self.capteurs_widget = QWidget()
        self.capteurs_layout = QVBoxLayout(self.capteurs_widget)
        self.capteurs_layout.setContentsMargins(2, 2, 2, 2)
        self.capteurs_layout.setSpacing(4)
        
        scroll_area.setWidget(self.capteurs_widget)
        layout.addWidget(scroll_area)
        
        # Pied avec statistiques globales
        self._setup_footer(layout)
        
        # Créer les widgets capteurs initiaux
        self._create_capteurs()
    
    def _setup_header(self, layout):
        """Configure l'en-tête du dock"""
        header_group = QGroupBox("Configuration")
        header_layout = QVBoxLayout(header_group)
        
        # Contrôles de configuration
        config_layout = QHBoxLayout()
        
        config_layout.addWidget(QLabel("Capteurs:"))
        self.spin_nb_capteurs = QSpinBox()
        self.spin_nb_capteurs.setRange(1, 16)
        self.spin_nb_capteurs.setValue(self.nb_capteurs)
        self.spin_nb_capteurs.valueChanged.connect(self._on_nb_capteurs_changed)
        config_layout.addWidget(self.spin_nb_capteurs)
        
        config_layout.addWidget(QLabel("MAJ (ms):"))
        self.spin_update_interval = QSpinBox()
        self.spin_update_interval.setRange(100, 5000)
        self.spin_update_interval.setValue(self.update_interval)
        self.spin_update_interval.valueChanged.connect(self._on_update_interval_changed)
        config_layout.addWidget(self.spin_update_interval)
        
        self.check_auto_update = QCheckBox("Auto")
        self.check_auto_update.setChecked(self.auto_update)
        self.check_auto_update.toggled.connect(self._on_auto_update_toggled)
        config_layout.addWidget(self.check_auto_update)
        
        config_layout.addStretch()
        
        header_layout.addLayout(config_layout)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        self.btn_refresh = QPushButton("🔄 Actualiser")
        self.btn_refresh.clicked.connect(self._refresh_capteurs)
        buttons_layout.addWidget(self.btn_refresh)
        
        self.btn_reset = QPushButton("🔄 Reset")
        self.btn_reset.clicked.connect(self._reset_capteurs)
        buttons_layout.addWidget(self.btn_reset)
        
        buttons_layout.addStretch()
        
        header_layout.addLayout(buttons_layout)
        
        layout.addWidget(header_group)
    
    def _setup_footer(self, layout):
        """Configure le pied du dock avec statistiques"""
        footer_group = QGroupBox("Statistiques Globales")
        footer_layout = QGridLayout(footer_group)
        footer_layout.setSpacing(4)
        
        # Statistiques
        footer_layout.addWidget(QLabel("Connectés:"), 0, 0)
        self.label_connectes = QLabel("0")
        self.label_connectes.setFont(QFont("Arial", 9, QFont.Bold))
        footer_layout.addWidget(self.label_connectes, 0, 1)
        
        footer_layout.addWidget(QLabel("En acquisition:"), 0, 2)
        self.label_acquisition = QLabel("0")
        self.label_acquisition.setFont(QFont("Arial", 9, QFont.Bold))
        footer_layout.addWidget(self.label_acquisition, 0, 3)
        
        footer_layout.addWidget(QLabel("Erreurs:"), 1, 0)
        self.label_erreurs = QLabel("0")
        self.label_erreurs.setFont(QFont("Arial", 9, QFont.Bold))
        footer_layout.addWidget(self.label_erreurs, 1, 1)
        
        footer_layout.addWidget(QLabel("Qualité moy.:"), 1, 2)
        self.label_qualite_moy = QLabel("0%")
        self.label_qualite_moy.setFont(QFont("Arial", 9, QFont.Bold))
        footer_layout.addWidget(self.label_qualite_moy, 1, 3)
        
        layout.addWidget(footer_group)
    
    def _create_capteurs(self):
        """Crée les widgets capteurs"""
        # Supprimer les capteurs existants
        for capteur in self.capteurs.values():
            capteur.setParent(None)
        self.capteurs.clear()
        
        # Créer les nouveaux capteurs
        for i in range(1, self.nb_capteurs + 1):
            capteur = CapteurWidget(i, f"Capteur Houle {i}")
            capteur.capteur_clicked.connect(self._on_capteur_clicked)
            
            self.capteurs[i] = capteur
            self.capteurs_layout.addWidget(capteur)
        
        # Ajouter un stretch à la fin
        self.capteurs_layout.addStretch()
        
        # Mettre à jour les statistiques
        self._update_statistics()
    
    def _apply_style(self):
        """Applique le style HRNeoWave"""
        # Style du dock
        self.setStyleSheet(f"""
            QDockWidget {{
                background-color: {get_color("background")};
                color: {get_color("text")};
                border: 1px solid {get_color("border")};
            }}
            QDockWidget::title {{
                background-color: {get_color("surface")};
                color: {get_color("text")};
                padding: 4px;
                border-bottom: 1px solid {get_color("border")};
            }}
        """)
        
        # Appliquer la classe accent aux boutons principaux
        apply_widget_class(self.btn_refresh, CLASS_ACCENT)
    
    def _on_nb_capteurs_changed(self, value):
        """Gère le changement du nombre de capteurs"""
        self.nb_capteurs = value
        self._create_capteurs()
    
    def _on_update_interval_changed(self, value):
        """Gère le changement de l'intervalle de mise à jour"""
        self.update_interval = value
        if self.auto_update:
            self.update_timer.start(self.update_interval)
    
    def _on_auto_update_toggled(self, checked):
        """Gère l'activation/désactivation de la mise à jour automatique"""
        self.auto_update = checked
        if checked:
            self.update_timer.start(self.update_interval)
        else:
            self.update_timer.stop()
    
    def _on_capteur_clicked(self, capteur_id):
        """Gère le clic sur un capteur"""
        self.capteur_selected.emit(capteur_id)
    
    def _refresh_capteurs(self):
        """Actualise manuellement l'état des capteurs"""
        self._auto_update()
    
    def _reset_capteurs(self):
        """Remet à zéro tous les capteurs"""
        for capteur in self.capteurs.values():
            capteur.set_etat("Déconnecté")
            capteur.set_signal_quality(0)
            capteur.set_valeur(0.0)
            capteur.set_sample_rate(0)
            capteur.set_total_samples(0)
        
        self._update_statistics()
    
    def _auto_update(self):
        """Mise à jour automatique des capteurs (simulation)"""
        import random
        
        for capteur_id, capteur in self.capteurs.items():
            # Simuler des états aléatoires pour la démonstration
            etats = ["Déconnecté", "Connecté", "Acquisition", "Erreur"]
            weights = [0.1, 0.3, 0.5, 0.1]  # Probabilités
            
            etat = random.choices(etats, weights=weights)[0]
            capteur.set_etat(etat)
            
            if etat in ["Connecté", "Acquisition"]:
                # Simuler une qualité de signal variable
                quality = random.uniform(60, 100)
                capteur.set_signal_quality(quality)
                
                # Simuler des valeurs de houle
                valeur = random.uniform(-2.0, 2.0)
                capteur.set_valeur(valeur)
                
                # Simuler une fréquence d'échantillonnage
                rate = random.choice([1000, 2000, 5000])
                capteur.set_sample_rate(rate)
                
                # Incrémenter les échantillons
                if etat == "Acquisition":
                    capteur.set_total_samples(capteur.total_samples + rate // 2)
            else:
                capteur.set_signal_quality(0)
                capteur.set_sample_rate(0)
        
        self._update_statistics()
        
        # Émettre le signal de mise à jour
        data = self._get_capteurs_data()
        self.capteurs_updated.emit(data)
    
    def _update_statistics(self):
        """Met à jour les statistiques globales"""
        connectes = 0
        acquisition = 0
        erreurs = 0
        qualites = []
        
        for capteur in self.capteurs.values():
            if capteur.etat == "Connecté":
                connectes += 1
            elif capteur.etat == "Acquisition":
                acquisition += 1
                connectes += 1  # En acquisition = connecté
            elif capteur.etat == "Erreur":
                erreurs += 1
            
            if capteur.signal_quality > 0:
                qualites.append(capteur.signal_quality)
        
        # Vérifier que les labels existent avant de les mettre à jour
        if hasattr(self, 'label_connectes'):
            self.label_connectes.setText(str(connectes))
        if hasattr(self, 'label_acquisition'):
            self.label_acquisition.setText(str(acquisition))
        if hasattr(self, 'label_erreurs'):
            self.label_erreurs.setText(str(erreurs))
        
        if hasattr(self, 'label_qualite_moy'):
            if qualites:
                qualite_moy = sum(qualites) / len(qualites)
                self.label_qualite_moy.setText(f"{qualite_moy:.0f}%")
            else:
                self.label_qualite_moy.setText("0%")
    
    def _get_capteurs_data(self) -> Dict[str, Any]:
        """Retourne les données de tous les capteurs"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'nb_capteurs': self.nb_capteurs,
            'capteurs': {}
        }
        
        for capteur_id, capteur in self.capteurs.items():
            data['capteurs'][capteur_id] = {
                'nom': capteur.nom,
                'etat': capteur.etat,
                'signal_quality': capteur.signal_quality,
                'last_value': capteur.last_value,
                'sample_rate': capteur.sample_rate,
                'total_samples': capteur.total_samples
            }
        
        return data
    
    # API publique
    def set_capteur_etat(self, capteur_id: int, etat: str):
        """Définit l'état d'un capteur spécifique"""
        if capteur_id in self.capteurs:
            self.capteurs[capteur_id].set_etat(etat)
            self._update_statistics()
    
    def set_capteur_data(self, capteur_id: int, **kwargs):
        """Met à jour les données d'un capteur"""
        if capteur_id in self.capteurs:
            capteur = self.capteurs[capteur_id]
            
            if 'etat' in kwargs:
                capteur.set_etat(kwargs['etat'])
            if 'signal_quality' in kwargs:
                capteur.set_signal_quality(kwargs['signal_quality'])
            if 'valeur' in kwargs:
                capteur.set_valeur(kwargs['valeur'])
            if 'sample_rate' in kwargs:
                capteur.set_sample_rate(kwargs['sample_rate'])
            if 'total_samples' in kwargs:
                capteur.set_total_samples(kwargs['total_samples'])
            
            self._update_statistics()
    
    def get_capteurs_status(self) -> Dict[str, Any]:
        """Retourne le statut de tous les capteurs"""
        return self._get_capteurs_data()
    
    def start_simulation(self):
        """Démarre la simulation de capteurs"""
        self.auto_update = True
        self.check_auto_update.setChecked(True)
        self.update_timer.start(self.update_interval)
    
    def stop_simulation(self):
        """Arrête la simulation de capteurs"""
        self.auto_update = False
        self.check_auto_update.setChecked(False)
        self.update_timer.stop()