#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dock "Infos essai" pour HRNeoWave
Affiche les informations de l'essai en cours avec le style HRNeoWave
"""

from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from datetime import datetime
from ..theme import apply_widget_class, get_color, CLASS_TITLE, CLASS_SUBTITLE, CLASS_VALUE

class InfosEssaiDock(QDockWidget):
    """
    Dock widget affichant les informations de l'essai en cours
    Style HRNeoWave avec mise à jour temps réel
    """
    
    # Signaux
    essai_updated = pyqtSignal(dict)  # Émis quand les infos essai changent
    
    def __init__(self, parent=None):
        super().__init__("Infos Essai", parent)
        self.setObjectName("InfosEssaiDock")
        
        # Données de l'essai
        self._essai_data = {
            'nom': 'Aucun essai',
            'date_debut': None,
            'duree': '00:00:00',
            'operateur': 'Non défini',
            'configuration': 'Standard',
            'nb_sondes': 0,
            'freq_echantillonnage': 0,
            'statut': 'Arrêté',
            'nb_echantillons': 0,
            'taille_buffer': 0,
            'fichier_sortie': 'Non défini'
        }
        
        # Timer pour mise à jour temps réel
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_duree)
        self._update_timer.setInterval(1000)  # Mise à jour chaque seconde
        
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # Widget principal avec scroll
        main_widget = QWidget()
        self.setWidget(main_widget)
        
        # Layout principal
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Titre principal
        self.title_label = QLabel("Informations Essai")
        apply_widget_class(self.title_label, CLASS_TITLE)
        layout.addWidget(self.title_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Section Essai
        self._create_section(layout, "Essai", [
            ('nom', 'Nom'),
            ('date_debut', 'Date début'),
            ('duree', 'Durée'),
            ('operateur', 'Opérateur'),
            ('statut', 'Statut')
        ])
        
        # Section Configuration
        self._create_section(layout, "Configuration", [
            ('configuration', 'Type'),
            ('nb_sondes', 'Nb sondes'),
            ('freq_echantillonnage', 'Fréq. (Hz)'),
            ('taille_buffer', 'Buffer')
        ])
        
        # Section Acquisition
        self._create_section(layout, "Acquisition", [
            ('nb_echantillons', 'Échantillons'),
            ('fichier_sortie', 'Fichier')
        ])
        
        # Spacer pour pousser le contenu vers le haut
        layout.addStretch()
        
        # Mise à jour initiale
        self._update_display()
    
    def _create_section(self, parent_layout, title, fields):
        """Crée une section avec titre et champs"""
        # Titre de section
        section_title = QLabel(title)
        apply_widget_class(section_title, CLASS_SUBTITLE)
        parent_layout.addWidget(section_title)
        
        # Container pour les champs
        fields_widget = QWidget()
        fields_layout = QVBoxLayout(fields_widget)
        fields_layout.setContentsMargins(12, 4, 4, 8)
        fields_layout.setSpacing(2)
        
        # Créer les champs
        for field_key, field_label in fields:
            field_container = QWidget()
            field_layout = QHBoxLayout(field_container)
            field_layout.setContentsMargins(0, 0, 0, 0)
            field_layout.setSpacing(8)
            
            # Label du champ
            label = QLabel(f"{field_label}:")
            label.setMinimumWidth(80)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            field_layout.addWidget(label)
            
            # Valeur du champ
            value_label = QLabel("--")
            apply_widget_class(value_label, CLASS_VALUE)
            value_label.setWordWrap(True)
            value_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            field_layout.addWidget(value_label)
            
            # Stocker la référence pour mise à jour
            setattr(self, f"_{field_key}_label", value_label)
            
            fields_layout.addWidget(field_container)
        
        parent_layout.addWidget(fields_widget)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(separator)
    
    def _apply_styles(self):
        """Applique les styles HRNeoWave"""
        # Style du dock
        self.setStyleSheet(f"""
            QDockWidget[objectName="InfosEssaiDock"] {{
                background-color: {get_color('background')};
                border: 1px solid {get_color('border')};
            }}
            
            QDockWidget[objectName="InfosEssaiDock"]::title {{
                background-color: {get_color('surface')};
                color: {get_color('accent')};
                padding: 8px;
                font-weight: bold;
                border-bottom: 1px solid {get_color('border')};
            }}
            
            QLabel {{
                color: {get_color('text')};
                background: transparent;
            }}
            
            QLabel[class="value"] {{
                color: {get_color('accent')};
                font-weight: bold;
            }}
            
            QFrame {{
                color: {get_color('border')};
            }}
        """)
    
    def _update_display(self):
        """Met à jour l'affichage avec les données actuelles"""
        # Mise à jour des champs
        for field_key, value in self._essai_data.items():
            label = getattr(self, f"_{field_key}_label", None)
            if label:
                if field_key == 'date_debut' and value:
                    if isinstance(value, datetime):
                        display_value = value.strftime("%d/%m/%Y %H:%M:%S")
                    else:
                        display_value = str(value)
                elif field_key == 'freq_echantillonnage' and value > 0:
                    display_value = f"{value:,} Hz"
                elif field_key == 'nb_echantillons' and value > 0:
                    display_value = f"{value:,}"
                elif field_key == 'taille_buffer' and value > 0:
                    display_value = f"{value:,} échantillons"
                elif field_key == 'statut':
                    # Couleur selon le statut
                    if value == 'En cours':
                        label.setStyleSheet(f"color: {get_color('success')}; font-weight: bold;")
                    elif value == 'Erreur':
                        label.setStyleSheet(f"color: {get_color('error')}; font-weight: bold;")
                    elif value == 'Pause':
                        label.setStyleSheet(f"color: {get_color('warning')}; font-weight: bold;")
                    else:
                        label.setStyleSheet(f"color: {get_color('text_secondary')}; font-weight: normal;")
                    display_value = value
                else:
                    display_value = str(value) if value is not None else "--"
                
                label.setText(display_value)
    
    def _update_duree(self):
        """Met à jour la durée si un essai est en cours"""
        if (self._essai_data['statut'] == 'En cours' and 
            self._essai_data['date_debut'] and 
            isinstance(self._essai_data['date_debut'], datetime)):
            
            duree = datetime.now() - self._essai_data['date_debut']
            hours, remainder = divmod(int(duree.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            self._essai_data['duree'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self._duree_label.setText(self._essai_data['duree'])
    
    # === API PUBLIQUE ===
    
    def set_essai_info(self, **kwargs):
        """Met à jour les informations de l'essai"""
        for key, value in kwargs.items():
            if key in self._essai_data:
                self._essai_data[key] = value
        
        self._update_display()
        self.essai_updated.emit(self._essai_data.copy())
    
    def start_essai(self, nom, operateur="Utilisateur", configuration="Standard"):
        """Démarre un nouvel essai"""
        self.set_essai_info(
            nom=nom,
            date_debut=datetime.now(),
            duree="00:00:00",
            operateur=operateur,
            configuration=configuration,
            statut="En cours",
            nb_echantillons=0
        )
        
        # Démarrer le timer de mise à jour
        self._update_timer.start()
    
    def stop_essai(self):
        """Arrête l'essai en cours"""
        self.set_essai_info(statut="Arrêté")
        self._update_timer.stop()
    
    def pause_essai(self):
        """Met en pause l'essai en cours"""
        self.set_essai_info(statut="Pause")
        self._update_timer.stop()
    
    def resume_essai(self):
        """Reprend l'essai en pause"""
        self.set_essai_info(statut="En cours")
        self._update_timer.start()
    
    def set_acquisition_config(self, nb_sondes, freq_echantillonnage, taille_buffer):
        """Configure les paramètres d'acquisition"""
        self.set_essai_info(
            nb_sondes=nb_sondes,
            freq_echantillonnage=freq_echantillonnage,
            taille_buffer=taille_buffer
        )
    
    def update_echantillons(self, nb_echantillons):
        """Met à jour le nombre d'échantillons acquis"""
        self.set_essai_info(nb_echantillons=nb_echantillons)
    
    def set_fichier_sortie(self, fichier):
        """Définit le fichier de sortie"""
        self.set_essai_info(fichier_sortie=fichier)
    
    def get_essai_data(self):
        """Retourne une copie des données de l'essai"""
        return self._essai_data.copy()
    
    def clear_essai(self):
        """Remet à zéro les informations d'essai"""
        self._update_timer.stop()
        self._essai_data = {
            'nom': 'Aucun essai',
            'date_debut': None,
            'duree': '00:00:00',
            'operateur': 'Non défini',
            'configuration': 'Standard',
            'nb_sondes': 0,
            'freq_echantillonnage': 0,
            'statut': 'Arrêté',
            'nb_echantillons': 0,
            'taille_buffer': 0,
            'fichier_sortie': 'Non défini'
        }
        self._update_display()