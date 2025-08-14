# -*- coding: utf-8 -*-
"""
Interface graphique pour la détection RÉELLE des cartes MCC DAQ
Version modifiée pour utiliser les vraies DLLs MCC
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

# Assure l'accès aux DLLs MCC sur Windows (InstaCal/UL)
if os.name == 'nt':
    _mcc_dir_candidates = [
        r"C:\\Program Files (x86)\\Measurement Computing\\DAQ",
        r"C:\\Program Files\\Measurement Computing\\DAQ",
    ]
    for _p in _mcc_dir_candidates:
        if os.path.isdir(_p):
            try:
                # Python 3.8+: ajoute le répertoire aux chemins de recherche des DLLs
                os.add_dll_directory(_p)
                logging.getLogger(__name__).info(f"Ajout DLL dir MCC: {_p}")
            except Exception as _e:
                logging.getLogger(__name__).debug(f"Impossible d'ajouter {_p}: {_e}")

# Import MCC ULDAQ (API officielle pour détection/accès matériel)
ULDAQ_AVAILABLE = False
ULDAQ_IMPORT_ERROR = None
try:
    from uldaq import get_daq_device_inventory, InterfaceType, DaqDevice, __version__ as ULDAQ_VERSION
    ULDAQ_AVAILABLE = True
except Exception as e:
    ULDAQ_IMPORT_ERROR = e

# Fallback: MCC Universal Library (mcculw) via InstaCal (cbw32/cbw64)
MCCULW_AVAILABLE = False
MCCULW_IMPORT_ERROR = None
try:
    from mcculw import ul as MCC_UL
    from mcculw.enums import InfoType, BoardInfo
    MCCULW_AVAILABLE = True
except Exception as e:
    MCCULW_IMPORT_ERROR = e

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcc_gui_detector_real.log', encoding='utf-8')
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

class RealMCCDetectorThread(QThread):
    """Thread pour la détection RÉELLE des cartes MCC"""
    
    # Signaux pour communiquer avec l'interface
    card_detected = pyqtSignal(dict)
    card_updated = pyqtSignal(dict)
    detection_complete = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.running = False
        # ULDAQ ne nécessite pas de gestion manuelle des DLLs ici
        self.uldaq_available = ULDAQ_AVAILABLE
        self.udp_ports = [8000, 8001, 8002, 8003, 8004, 8005]
        self.udp_timeout = 2.0
        self.network_scan_range = "192.168.1.0/24"
        # Pas de chargement DLL manuel pour ULDAQ

    def _load_dlls(self):
        """Conservé pour compatibilité; ULDAQ ne requiert pas de chargement manuel."""
        if not self.uldaq_available:
            msg = "Le module 'uldaq' n'est pas disponible. Assurez-vous que: \n" \
                  "1) pip install uldaq (fait) \n" \
                  "2) Measurement Computing Universal Library (UL) et InstaCal sont installés sur Windows. \n" \
                  "   Téléchargez depuis: https://www.mccdaq.com/Software-Downloads \n" \
                  f"Détail import: {ULDAQ_IMPORT_ERROR}"
            logger.error(msg)
            self.error_occurred.emit(msg)
            
    def detect_real_usb_cards(self) -> List[Dict[str, Any]]:
        """Détecte les vraies cartes MCC.
        Stratégie:
          1) ULDAQ (USB/Ethernet) si disponible
          2) mcculw (InstaCal) sinon
        """
        cards: List[Dict[str, Any]] = []
        try:
            if self.uldaq_available:
                # Inventaire via ULDAQ
                inventory = get_daq_device_inventory(InterfaceType.ANY)
                logger.info(f"Périphériques MCC détectés (ULDAQ): {len(inventory)}")
                for dev in inventory:
                    try:
                        card = {
                            "name": getattr(dev, "product_name", "MCC Device"),
                            "type": str(getattr(dev, "dev_interface", "USB")),
                            "serial": getattr(dev, "unique_id", ""),
                            "connected": True,
                            "detection_time": datetime.now().isoformat(),
                        }
                        cards.append(card)
                        self.card_detected.emit(card)
                    except Exception as inner_e:
                        logger.warning(f"Erreur lecture device ULDAQ: {inner_e}")
                return cards

            # Fallback: InstaCal via mcculw
            if MCCULW_AVAILABLE:
                logger.info("ULDAQ indisponible, bascule sur mcculw/Instacal")
                # Parcourir des numéros de cartes InstaCal raisonnables (0..31)
                for board_num in range(0, 32):
                    try:
                        name = MCC_UL.get_board_name(board_num)
                        if name:
                            try:
                                # Lire des infos additionnelles si possible
                                serial = ""
                                try:
                                    serial = MCC_UL.get_config(InfoType.BOARDINFO, board_num, 0, BoardInfo.SERIALNO)
                                except Exception:
                                    pass
                                card = {
                                    "name": name,
                                    "type": "USB/PCI (InstaCal)",
                                    "serial": str(serial) if serial is not None else "",
                                    "connected": True,
                                    "detection_time": datetime.now().isoformat(),
                                    "board_num": board_num,
                                }
                                cards.append(card)
                                self.card_detected.emit(card)
                            except Exception as inner_info_e:
                                logger.debug(f"Infos additionnelles indisponibles pour board {board_num}: {inner_info_e}")
                    except Exception:
                        # Aucune carte configurée sous ce numéro
                        continue
                if not cards:
                    logger.info("Aucune carte détectée via mcculw/Instacal")
                return cards

            # Ni ULDAQ ni mcculw
            logger.error("Ni 'uldaq' ni 'mcculw' ne sont disponibles.\n"
                         f"uldaq err: {ULDAQ_IMPORT_ERROR}\n"
                         f"mcculw err: {MCCULW_IMPORT_ERROR}")

        except Exception as e:
            logger.error(f"Erreur lors de la détection ULDAQ: {e}")
            self.error_occurred.emit(f"Erreur détection ULDAQ: {e}")

        return cards
        
    def detect_real_udp_cards(self) -> List[Dict[str, Any]]:
        """Détecte les vraies cartes UDP MCC"""
        cards = []
        
        try:
            logger.info("Tentative de détection des cartes UDP réelles...")
            
            # Scan réseau réel pour les cartes UDP
            for port in self.udp_ports:
                try:
                    # Test de connexion UDP réel
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(self.udp_timeout)
                    
                    # Test sur localhost et réseau local
                    test_addresses = ["127.0.0.1", "192.168.1.100", "192.168.1.101"]
                    
                    for addr in test_addresses:
                        try:
                            test_message = b"MCC_DETECT_REAL"
                            sock.sendto(test_message, (addr, port))
                            
                            try:
                                data, response_addr = sock.recvfrom(1024)
                                logger.info(f"Carte UDP détectée sur {response_addr}: {data}")
                                
                                card = {
                                    "name": f"UDP-Card-{port}",
                                    "type": "UDP",
                                    "ip_address": response_addr[0],
                                    "port": response_addr[1],
                                    "serial": f"UDP{port:04d}",
                                    "connected": True,
                                    "detection_time": datetime.now().isoformat(),
                                    "response_data": data.decode('utf-8', errors='ignore')
                                }
                                cards.append(card)
                                self.card_detected.emit(card)
                                
                            except socket.timeout:
                                logger.debug(f"Timeout pour {addr}:{port}")
                                
                        except Exception as e:
                            logger.debug(f"Erreur de test pour {addr}:{port}: {e}")
                            
                    sock.close()
                    
                except Exception as e:
                    logger.error(f"Erreur lors du scan du port {port}: {e}")
                    
            if not cards:
                logger.info("Aucune carte UDP réelle détectée")
                
        except Exception as e:
            logger.error(f"Erreur lors de la détection UDP: {e}")
            self.error_occurred.emit(f"Erreur détection UDP: {e}")
            
        return cards
        
    def run(self):
        """Exécute la détection réelle"""
        self.running = True
        try:
            logger.info("Début de la détection RÉELLE des cartes MCC")
            self.progress_updated.emit(10)
            
            # Log version uldaq si dispo
            if self.uldaq_available:
                try:
                    logger.info(f"ULDAQ disponible, version: {ULDAQ_VERSION}")
                except Exception:
                    pass
            # Détection des vraies cartes USB
            usb_cards = self.detect_real_usb_cards()
            self.progress_updated.emit(50)
            
            # Détection des vraies cartes UDP
            udp_cards = self.detect_real_udp_cards()
            self.progress_updated.emit(90)
            
            # Résultats finaux
            results = {
                "usb_cards": usb_cards,
                "udp_cards": udp_cards,
                "total_cards": len(usb_cards) + len(udp_cards),
                "connected_cards": len([c for c in usb_cards + udp_cards if c.get("connected", False)]),
                "detection_time": datetime.now().isoformat(),
                "detection_mode": "REAL"
            }
            
            self.progress_updated.emit(100)
            self.detection_complete.emit(results)
            
        except Exception as e:
            logger.error(f"Erreur lors de la détection réelle: {e}")
            self.error_occurred.emit(str(e))
        finally:
            self.running = False

class RealMCCDetectorGUI(QMainWindow):
    """Interface graphique pour la détection RÉELLE des cartes MCC"""
    
    def __init__(self):
        super().__init__()
        self.detector_thread = None
        self.cards_data = {"usb_cards": [], "udp_cards": []}
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Détecteur RÉEL de Cartes MCC DAQ")
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
        header_group = QGroupBox("Détecteur RÉEL de Cartes MCC DAQ")
        header_layout = QHBoxLayout(header_group)
        
        # Titre
        title_label = QLabel("🔍 Détecteur RÉEL de Cartes MCC DAQ")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        # Indicateur global
        self.global_led = LEDIndicator(30, Qt.GlobalColor.yellow)
        header_layout.addWidget(self.global_led)
        
        # Statut global
        self.global_status = QLabel("En attente - Mode RÉEL")
        self.global_status.setStyleSheet("color: gray; font-weight: bold;")
        header_layout.addWidget(self.global_status)
        
        header_layout.addStretch()
        parent_layout.addWidget(header_group)
        
    def create_controls(self, parent_layout):
        """Crée les contrôles de l'interface"""
        controls_group = QGroupBox("Contrôles - Détection RÉELLE")
        controls_layout = QHBoxLayout(controls_group)
        
        # Bouton de détection
        self.detect_button = QPushButton("🔍 Détecter les Vraies Cartes")
        self.detect_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.detect_button.clicked.connect(self.start_detection)
        
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
        
        # Bouton de test rapide
        self.test_button = QPushButton("✅ Tester la Carte")
        self.test_button.setToolTip("Test rapide: inventaire uldaq si dispo, sinon mcculw/Instacal")
        self.test_button.clicked.connect(self.on_test_card)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        controls_layout.addWidget(self.detect_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.test_button)
        controls_layout.addWidget(self.progress_bar)
        
        controls_layout.addStretch()
        parent_layout.addWidget(controls_group)
        
    def create_detection_panel(self, parent_widget):
        """Crée le panneau de détection"""
        detection_group = QGroupBox("Détection RÉELLE des Cartes")
        detection_layout = QVBoxLayout(detection_group)
        
        # Onglets pour USB et UDP
        self.tab_widget = QTabWidget()
        
        # Onglet USB
        self.usb_tab = self.create_card_table("Cartes USB Réelles")
        self.tab_widget.addTab(self.usb_tab, "🔌 Cartes USB Réelles")
        
        # Onglet UDP
        self.udp_tab = self.create_card_table("Cartes UDP Réelles")
        self.tab_widget.addTab(self.udp_tab, "🌐 Cartes UDP Réelles")
        
        detection_layout.addWidget(self.tab_widget)
        parent_widget.addWidget(detection_group)
        
    def create_card_table(self, title):
        """Crée un tableau pour afficher les cartes"""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Nom", "Type", "Statut", "LED", "Série", "Adresse", "Actions"
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
        details_group = QGroupBox("Détails et Logs - Mode RÉEL")
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
        self.card_info_group = QGroupBox("Informations de la Carte Réelle")
        self.card_info_layout = QVBoxLayout(self.card_info_group)
        
        self.card_info_label = QLabel("Sélectionnez une carte pour voir ses détails")
        self.card_info_label.setStyleSheet("color: gray; font-style: italic;")
        self.card_info_layout.addWidget(self.card_info_label)
        
        details_layout.addWidget(self.card_info_group)
        
        # Statistiques
        self.stats_group = QGroupBox("Statistiques - Détection RÉELLE")
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
        self.statusBar().showMessage("Prêt à détecter les vraies cartes MCC")
        
    def start_detection(self):
        """Démarre la détection réelle des cartes"""
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Démarrage de la détection RÉELLE...")
        
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
        self.global_status.setText("Détection RÉELLE en cours...")
        self.global_status.setStyleSheet("color: blue; font-weight: bold;")
        
        # Démarrage du thread de détection réelle
        self.detector_thread = RealMCCDetectorThread()
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
        self.global_status.setText("Arrêté - Mode RÉEL")
        self.global_status.setStyleSheet("color: red; font-weight: bold;")
        
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Détection RÉELLE arrêtée")
        
    def on_test_card(self):
        """Test rapide de détection: ULDAQ si dispo, sinon mcculw/Instacal."""
        try:
            # 1) ULDAQ
            if ULDAQ_AVAILABLE:
                try:
                    inv = get_daq_device_inventory(InterfaceType.ANY)
                    if not inv:
                        QMessageBox.information(self, "Test MCC (ULDAQ)", "Aucune carte MCC détectée. Vérifiez la connexion USB.")
                        return
                    lines = []
                    found_1608 = False
                    for device in inv:
                        pname = getattr(device, 'product_name', 'MCC Device')
                        pid = getattr(device, 'product_id', None)
                        lines.append(f"Carte détectée : {pname} (ID: {pid})")
                        if pid == 125 or '1608' in str(pname):
                            found_1608 = True
                    msg = "\n".join(lines)
                    if found_1608:
                        msg += "\n\nUSB-1608FS détectée et prête !"
                    QMessageBox.information(self, "Test MCC (ULDAQ)", msg)
                    return
                except Exception as e:
                    QMessageBox.warning(self, "Test MCC (ULDAQ)", f"Erreur ULDAQ: {e}")
                    # continue to fallback
            
            # 2) mcculw / InstaCal
            if MCCULW_AVAILABLE:
                try:
                    from mcculw import ul as MCC_UL
                    found = []
                    found_1608 = False
                    for j in range(32):
                        try:
                            name = MCC_UL.get_board_name(j)
                            if name:
                                found.append(f"Board {j}: {name}")
                                if '1608' in name:
                                    found_1608 = True
                        except Exception:
                            pass
                    if not found:
                        QMessageBox.information(self, "Test MCC (mcculw)", "Aucune carte MCC détectée via InstaCal. Ouvrez InstaCal et vérifiez la configuration.")
                        return
                    msg = "\n".join(found)
                    if found_1608:
                        msg += "\n\nUSB-1608FS détectée et prête !"
                    QMessageBox.information(self, "Test MCC (mcculw)", msg)
                    return
                except Exception as e:
                    QMessageBox.warning(self, "Test MCC (mcculw)", f"Erreur mcculw: {e}")
                    return

            # 3) aucun backend
            QMessageBox.warning(self, "Test MCC", "Ni 'uldaq' ni 'mcculw' ne sont disponibles pour le test.")
        except Exception as e:
            QMessageBox.warning(self, "Test MCC", f"Erreur: {e}")
        
    def clear_tables(self):
        """Vide les tableaux"""
        self.usb_tab.setRowCount(0)
        self.udp_tab.setRowCount(0)
        
    def on_card_detected(self, card_data):
        """Appelé quand une vraie carte est détectée"""
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
        
        # Adresse (IP pour UDP, USB pour USB)
        if card_type == "UDP":
            address = f"{card_data.get('ip_address', 'N/A')}:{card_data.get('port', 'N/A')}"
        else:
            address = "USB"
        address_item = QTableWidgetItem(address)
        table.setItem(row, 5, address_item)
        
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
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Carte RÉELLE détectée: {card_data.get('name')} ({status_text})")
        
    def on_detection_complete(self, results):
        """Appelé quand la détection réelle est terminée"""
        total_cards = results.get("total_cards", 0)
        connected_cards = results.get("connected_cards", 0)
        disconnected_cards = total_cards - connected_cards
        detection_mode = results.get("detection_mode", "UNKNOWN")
        
        # Mise à jour des statistiques
        self.total_cards_label.setText(f"Total: {total_cards}")
        self.connected_cards_label.setText(f"Connectées: {connected_cards}")
        self.disconnected_cards_label.setText(f"Déconnectées: {disconnected_cards}")
        
        # Mise à jour du statut global
        if connected_cards > 0:
            self.global_led.set_state(True)
            self.global_status.setText(f"{connected_cards} carte(s) RÉELLE(s) connectée(s)")
            self.global_status.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.global_led.set_state(False)
            self.global_status.setText("Aucune carte RÉELLE connectée")
            self.global_status.setStyleSheet("color: red; font-weight: bold;")
            
        # Réactivation des contrôles
        self.detect_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Log final
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Détection RÉELLE terminée: {total_cards} cartes trouvées ({connected_cards} connectées)")
        
    def on_error(self, error_message):
        """Appelé en cas d'erreur"""
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ERREUR: {error_message}")
        
        # Réactivation des contrôles
        self.detect_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Mise à jour du statut
        self.global_led.set_state(False)
        self.global_status.setText("Erreur - Mode RÉEL")
        self.global_status.setStyleSheet("color: red; font-weight: bold;")
        
    def test_card_connection(self, card_data):
        """Teste la connexion d'une vraie carte"""
        card_name = card_data.get("name", "Unknown")
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Test de connexion RÉELLE pour {card_name}...")
        
        # Test réel de la connexion
        if card_data.get("type") == "UDP":
            # Test UDP réel
            try:
                ip = card_data.get("ip_address", "127.0.0.1")
                port = card_data.get("port", 8000)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2.0)
                test_message = b"MCC_TEST_REAL"
                sock.sendto(test_message, (ip, port))
                
                try:
                    data, addr = sock.recvfrom(1024)
                    self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ {card_name} répond correctement: {data}")
                    QMessageBox.information(self, "Test RÉEL", f"La carte {card_name} répond correctement!")
                except socket.timeout:
                    self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ {card_name} ne répond pas (timeout)")
                    QMessageBox.warning(self, "Test RÉEL", f"La carte {card_name} ne répond pas!")
                finally:
                    sock.close()
            except Exception as e:
                self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Erreur lors du test de {card_name}: {e}")
                QMessageBox.warning(self, "Test RÉEL", f"Erreur lors du test de {card_name}: {e}")
        else:
            # Test USB (simulation pour l'instant)
            self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] Test USB pour {card_name} (simulation)")
            QMessageBox.information(self, "Test RÉEL", f"Test USB pour {card_name} (fonctionnalité en développement)")

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Configuration du style
    app.setStyle('Fusion')
    
    # Création et affichage de la fenêtre principale
    window = RealMCCDetectorGUI()
    window.show()
    
    # Exécution de l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()




