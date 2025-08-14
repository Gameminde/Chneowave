# -*- coding: utf-8 -*-
"""
Interface graphique pour la détection des cartes MCC DAQ
Utilise PyQt6 avec des indicateurs LED et fenêtres de détection
"""
import sys
import os
import time
import logging
import socket
import threading
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from ctypes import *
from ctypes.wintypes import *
import random

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QTextEdit, QGroupBox,
    QProgressBar, QFrame, QSplitter, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QComboBox,
    QSpinBox, QCheckBox, QLineEdit
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QRect, QSize
)
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QPixmap, QPainter, QBrush,
    QPen, QIcon
)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcc_gui_detector.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class LEDIndicator(QWidget):
    """Widget LED personnalisé avec animation"""
    
    def __init__(self, size=20, color=Qt.GlobalColor.green):
        super().__init__()
        self.size = size
        self.color = color
        self.is_on = False
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.setFixedSize(size, size)
        self.setMinimumSize(size, size)
        
    def set_state(self, is_on: bool):
        """Change l'état de la LED"""
        self.is_on = is_on
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Couleur de la LED
        if self.is_on:
            if self.color == Qt.GlobalColor.green:
                color = QColor(0, 255, 0)
            elif self.color == Qt.GlobalColor.red:
                color = QColor(255, 0, 0)
            else:
                color = QColor(255, 255, 0)  # Jaune par défaut
        else:
            color = QColor(100, 100, 100)  # Gris éteint
            
        # Dessiner la LED
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawEllipse(2, 2, self.size - 4, self.size - 4)
        
        # Effet de brillance
        if self.is_on:
            painter.setBrush(QBrush(QColor(255, 255, 255, 100)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(4, 4, (self.size - 8) // 3, (self.size - 8) // 3)

class MCCDetectorThread(QThread):
    """Thread pour la détection des cartes MCC"""
    
    # Signaux pour communiquer avec l'interface
    card_detected = pyqtSignal(dict)
    card_updated = pyqtSignal(dict)
    detection_complete = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.mcc_dll_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Measurement Computing", "DAQami")
        self.hal_dll = None
        self.ul_dll = None
        self.hal_ul_dll = None
        self.udp_ports = [8000, 8001, 8002, 8003, 8004, 8005]
        self.udp_timeout = 2.0
        self.network_scan_range = "192.168.1.0/24"
        self._load_dlls()
        
    def _load_dlls(self):
        """Charge les DLLs MCC"""
        try:
            # Simulation du chargement des DLLs
            logger.info("Chargement des DLLs MCC...")
            time.sleep(0.5)  # Simulation du temps de chargement
            logger.info("DLLs MCC chargées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des DLLs: {e}")
            self.error_occurred.emit(f"Erreur DLL: {e}")
            
    def detect_usb_cards(self) -> List[Dict[str, Any]]:
        """Détecte les cartes USB (simulation)"""
        cards = []
        usb_devices = [
            {
                "name": "USB-1608G",
                "type": "USB",
                "serial": "USB1608G001",
                "channels": 16,
                "resolution": "16-bit",
                "sample_rate": "100kS/s",
                "status": "connected"
            },
            {
                "name": "USB-1208HS",
                "type": "USB",
                "serial": "USB1208HS002",
                "channels": 8,
                "resolution": "12-bit",
                "sample_rate": "50kS/s",
                "status": "connected"
            }
        ]
        
        for device in usb_devices:
            # Simulation de la détection
            time.sleep(0.2)
            device["detection_time"] = datetime.now().isoformat()
            device["connected"] = True
            cards.append(device)
            self.card_detected.emit(device)
            
        return cards
        
    def detect_udp_cards(self) -> List[Dict[str, Any]]:
        """Détecte les cartes UDP (simulation)"""
        cards = []
        udp_devices = [
            {
                "name": "UDP-1208HS",
                "type": "UDP",
                "ip_address": "192.168.1.100",
                "port": 8000,
                "serial": "UDP1208HS003",
                "channels": 8,
                "resolution": "12-bit",
                "sample_rate": "50kS/s",
                "status": "connected"
            },
            {
                "name": "UDP-1608G",
                "type": "UDP",
                "ip_address": "192.168.1.101",
                "port": 8001,
                "serial": "UDP1608G004",
                "channels": 16,
                "resolution": "16-bit",
                "sample_rate": "100kS/s",
                "status": "disconnected"
            }
        ]
        
        for device in udp_devices:
            # Simulation du test de connexion UDP
            time.sleep(0.3)
            device["detection_time"] = datetime.now().isoformat()
            
            # Simulation probabiliste de la connexion
            if device["name"] == "UDP-1208HS":
                device["connected"] = True
                device["response_time"] = random.randint(10, 50)
            else:
                device["connected"] = False
                device["response_time"] = None
                
            cards.append(device)
            self.card_detected.emit(device)
            
        return cards
        
    def run(self):
        """Exécute la détection"""
        self.running = True
        try:
            logger.info("Début de la détection des cartes MCC")
            self.progress_updated.emit(10)
            
            # Détection des cartes USB
            usb_cards = self.detect_usb_cards()
            self.progress_updated.emit(50)
            
            # Détection des cartes UDP
            udp_cards = self.detect_udp_cards()
            self.progress_updated.emit(90)
            
            # Résultats finaux
            results = {
                "usb_cards": usb_cards,
                "udp_cards": udp_cards,
                "total_cards": len(usb_cards) + len(udp_cards),
                "connected_cards": len([c for c in usb_cards + udp_cards if c.get("connected", False)]),
                "detection_time": datetime.now().isoformat()
            }
            
            self.progress_updated.emit(100)
            self.detection_complete.emit(results)
            
        except Exception as e:
            logger.error(f"Erreur lors de la détection: {e}")
            self.error_occurred.emit(str(e))
        finally:
            self.running = False

class MCCDetectorGUI(QMainWindow):
    """Interface graphique principale pour la détection MCC"""
    
    def __init__(self):
        super().__init__()
        self.detector_thread = None
        self.cards_data = {"usb_cards": [], "udp_cards": []}
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Détecteur de Cartes MCC DAQ")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # En-tête
        self.create_header(main_layout)
        
        # Contrôles
        self.create_controls(main_layout)
        
        # Zone de contenu principal
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Panneau de détection
        self.create_detection_panel(content_splitter)
        
        # Panneau de détails
        self.create_details_panel(content_splitter)
        
        # Barre de statut
        self.create_status_bar()
        
        # Configuration des proportions
        content_splitter.setSizes([600, 600])
        
    def create_header(self, parent_layout):
        """Crée l'en-tête de l'interface"""
        header_group = QGroupBox("Détecteur de Cartes MCC DAQ")
        header_layout = QHBoxLayout(header_group)
        
        # Titre
        title_label = QLabel("🔍 Détecteur de Cartes MCC DAQ")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        # Indicateur global
        self.global_led = LEDIndicator(30, Qt.GlobalColor.yellow)
        header_layout.addWidget(self.global_led)
        
        # Statut global
        self.global_status = QLabel("En attente")
        self.global_status.setStyleSheet("color: gray; font-weight: bold;")
        header_layout.addWidget(self.global_status)
        
        header_layout.addStretch()
        parent_layout.addWidget(header_group)
        
    def create_controls(self, parent_layout):
        """Crée les contrôles de l'interface"""
        controls_group = QGroupBox("Contrôles")
        controls_layout = QHBoxLayout(controls_group)
        
        # Bouton de détection
        self.detect_button = QPushButton("🔍 Détecter les Cartes")
        self.detect_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.detect_button.clicked.connect(self.start_detection)
        controls_layout.addWidget(self.detect_button)
        
        # Bouton d'arrêt
        self.stop_button = QPushButton("⏹️ Arrêter")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        self.stop_button.clicked.connect(self.stop_detection)
        self.stop_button.setEnabled(False)
        controls_layout.addWidget(self.stop_button)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        controls_layout.addWidget(self.progress_bar)
        
        controls_layout.addStretch()
        parent_layout.addWidget(controls_group)
        
    def create_detection_panel(self, parent_widget):
        """Crée le panneau de détection"""
        detection_group = QGroupBox("Détection des Cartes")
        detection_layout = QVBoxLayout(detection_group)
        
        # Onglets pour USB et UDP
        self.tab_widget = QTabWidget()
        
        # Onglet USB
        self.usb_tab = self.create_card_table("Cartes USB")
        self.tab_widget.addTab(self.usb_tab, "🔌 Cartes USB")
        
        # Onglet UDP
        self.udp_tab = self.create_card_table("Cartes UDP")
        self.tab_widget.addTab(self.udp_tab, "🌐 Cartes UDP")
        
        detection_layout.addWidget(self.tab_widget)
        parent_widget.addWidget(detection_group)
        
    def create_card_table(self, title):
        """Crée un tableau pour afficher les cartes"""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Nom", "Type", "Statut", "LED", "Série", "Canaux", "Actions"
        ])
        
        # Configuration du tableau
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        
        table.setColumnWidth(3, 50)  # LED
        table.setColumnWidth(6, 100)  # Actions
        
        return table
        
    def create_details_panel(self, parent_widget):
        """Crée le panneau de détails"""
        details_group = QGroupBox("Détails et Logs")
        details_layout = QVBoxLayout(details_group)
        
        # Zone de logs
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        details_layout.addWidget(self.log_text)
        
        # Informations de la carte sélectionnée
        self.card_info_group = QGroupBox("Informations de la Carte")
        self.card_info_layout = QVBoxLayout(self.card_info_group)
        
        self.card_info_label = QLabel("Sélectionnez une carte pour voir ses détails")
        self.card_info_label.setStyleSheet("color: gray; font-style: italic;")
        self.card_info_layout.addWidget(self.card_info_label)
        
        details_layout.addWidget(self.card_info_group)
        
        # Statistiques
        self.stats_group = QGroupBox("Statistiques")
        self.stats_layout = QGridLayout(self.stats_group)
        
        self.total_cards_label = QLabel("Total: 0")
        self.connected_cards_label = QLabel("Connectées: 0")
        self.disconnected_cards_label = QLabel("Déconnectées: 0")
        
        self.stats_layout.addWidget(QLabel("Cartes détectées:"), 0, 0)
        self.stats_layout.addWidget(self.total_cards_label, 0, 1)
        self.stats_layout.addWidget(self.connected_cards_label, 1, 0)
        self.stats_layout.addWidget(self.disconnected_cards_label, 1, 1)
        
        details_layout.addWidget(self.stats_group)
        parent_widget.addWidget(details_group)
        
    def create_status_bar(self):
        """Crée la barre de statut"""
        self.statusBar().showMessage("Prêt à détecter les cartes MCC")
        
    def start_detection(self):
        """Démarre la détection des cartes"""
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Démarrage de la détection...")
        
        # Réinitialisation
        self.cards_data = {"usb_cards": [], "udp_cards": []}
        self.clear_tables()
        
        # Configuration de l'interface
        self.detect_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Mise à jour du statut global
        self.global_led.set_state(True)
        self.global_status.setText("Détection en cours...")
        self.global_status.setStyleSheet("color: orange; font-weight: bold;")
        
        # Démarrage du thread de détection
        self.detector_thread = MCCDetectorThread()
        self.detector_thread.card_detected.connect(self.on_card_detected)
        self.detector_thread.detection_complete.connect(self.on_detection_complete)
        self.detector_thread.error_occurred.connect(self.on_error)
        self.detector_thread.progress_updated.connect(self.progress_bar.setValue)
        
        self.detector_thread.start()
        
    def stop_detection(self):
        """Arrête la détection"""
        if self.detector_thread and self.detector_thread.running:
            self.detector_thread.running = False
            self.detector_thread.wait()
            
        self.detect_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        self.global_led.set_state(False)
        self.global_status.setText("Arrêté")
        self.global_status.setStyleSheet("color: red; font-weight: bold;")
        
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Détection arrêtée")
        
    def clear_tables(self):
        """Vide les tableaux"""
        self.usb_tab.setRowCount(0)
        self.udp_tab.setRowCount(0)
        
    def on_card_detected(self, card_data):
        """Appelé quand une carte est détectée"""
        card_type = card_data.get("type", "Unknown")
        table = self.usb_tab if card_type == "USB" else self.udp_tab
        
        # Ajouter une nouvelle ligne
        row = table.rowCount()
        table.insertRow(row)
        
        # Nom de la carte
        name_item = QTableWidgetItem(card_data.get("name", "Unknown"))
        table.setItem(row, 0, name_item)
        
        # Type
        type_item = QTableWidgetItem(card_type)
        table.setItem(row, 1, type_item)
        
        # Statut
        connected = card_data.get("connected", False)
        status_text = "Connectée" if connected else "Déconnectée"
        status_item = QTableWidgetItem(status_text)
        status_item.setForeground(QColor("green") if connected else QColor("red"))
        table.setItem(row, 2, status_item)
        
        # LED
        led_widget = LEDIndicator(20, Qt.GlobalColor.green if connected else Qt.GlobalColor.red)
        led_widget.set_state(connected)
        table.setCellWidget(row, 3, led_widget)
        
        # Série
        serial_item = QTableWidgetItem(card_data.get("serial", "N/A"))
        table.setItem(row, 4, serial_item)
        
        # Canaux
        channels_item = QTableWidgetItem(str(card_data.get("channels", "N/A")))
        table.setItem(row, 5, channels_item)
        
        # Actions
        test_button = QPushButton("Tester")
        test_button.clicked.connect(lambda: self.test_card_connection(card_data))
        table.setCellWidget(row, 6, test_button)
        
        # Mise à jour des données
        if card_type == "USB":
            self.cards_data["usb_cards"].append(card_data)
        else:
            self.cards_data["udp_cards"].append(card_data)
            
        # Log
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Carte détectée: {card_data.get('name')} ({status_text})")
        
    def on_detection_complete(self, results):
        """Appelé quand la détection est terminée"""
        total_cards = results.get("total_cards", 0)
        connected_cards = results.get("connected_cards", 0)
        disconnected_cards = total_cards - connected_cards
        
        # Mise à jour des statistiques
        self.total_cards_label.setText(f"Total: {total_cards}")
        self.connected_cards_label.setText(f"Connectées: {connected_cards}")
        self.disconnected_cards_label.setText(f"Déconnectées: {disconnected_cards}")
        
        # Mise à jour du statut global
        if connected_cards > 0:
            self.global_led.set_state(True)
            self.global_status.setText(f"{connected_cards} carte(s) connectée(s)")
            self.global_status.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.global_led.set_state(False)
            self.global_status.setText("Aucune carte connectée")
            self.global_status.setStyleSheet("color: red; font-weight: bold;")
            
        # Réactivation des contrôles
        self.detect_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Log final
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Détection terminée: {total_cards} cartes trouvées ({connected_cards} connectées)")
        
    def on_error(self, error_message):
        """Appelé en cas d'erreur"""
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ERREUR: {error_message}")
        
        # Réactivation des contrôles
        self.detect_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Mise à jour du statut
        self.global_led.set_state(False)
        self.global_status.setText("Erreur")
        self.global_status.setStyleSheet("color: red; font-weight: bold;")
        
    def test_card_connection(self, card_data):
        """Teste la connexion d'une carte spécifique"""
        card_name = card_data.get("name", "Unknown")
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Test de connexion pour {card_name}...")
        
        # Simulation du test
        time.sleep(0.5)
        
        if card_data.get("connected", False):
            self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ {card_name} répond correctement")
            QMessageBox.information(self, "Test de Connexion", f"La carte {card_name} répond correctement!")
        else:
            self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ {card_name} ne répond pas")
            QMessageBox.warning(self, "Test de Connexion", f"La carte {card_name} ne répond pas!")

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Configuration du style
    app.setStyle('Fusion')
    
    # Création et affichage de la fenêtre principale
    window = MCCDetectorGUI()
    window.show()
    
    # Exécution de l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()




