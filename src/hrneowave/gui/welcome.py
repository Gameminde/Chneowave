from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QFileDialog, QMessageBox, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPalette, QColor, QFont
import sys
import os
import csv
import json

def set_light_mode(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(240, 240, 240))
    palette.setColor(QPalette.AlternateBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(220, 220, 220))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    app.setStyleSheet('''
        QWidget {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
        }
        QLabel#titleLabel {
            font-size: 22px;
            font-weight: bold;
            color: #00bfff;
            letter-spacing: 2px;
        }
        QLineEdit, QComboBox, QDateEdit {
            background: #e0e0e0;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 5px 8px;
            color: #000000;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00bfff, stop:1 #005fa3);
            color: white;
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #005fa3, stop:1 #00bfff);
        }
        QComboBox QAbstractItemView {
            background: #e0e0e0;
            color: #000000;
            selection-background-color: #00bfff;
        }
    ''')

def set_dark_mode(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 36))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(24, 24, 28))
    palette.setColor(QPalette.AlternateBase, QColor(36, 36, 42))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(40, 40, 48))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    app.setStyleSheet('''
        QWidget {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
        }
        QLabel#titleLabel {
            font-size: 22px;
            font-weight: bold;
            color: #00bfff;
            letter-spacing: 2px;
        }
        QLineEdit, QComboBox, QDateEdit {
            background: #23232b;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 5px 8px;
            color: #e0e0e0;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00bfff, stop:1 #005fa3);
            color: white;
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #005fa3, stop:1 #00bfff);
        }
        QComboBox QAbstractItemView {
            background: #23232b;
            color: #e0e0e0;
            selection-background-color: #00bfff;
        }
    ''')

class WelcomeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("HRNeoWave - Bienvenue")
        layout = QVBoxLayout()

        self.theme_switch = QCheckBox("Mode sombre")
        self.theme_switch.setChecked(True)
        self.theme_switch.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_switch)

        label = QLabel("HRNeoWave")
        label.setObjectName("titleLabel")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        subtitle = QLabel("<i>Analyse moderne des essais de houle</i>")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        form = QFormLayout()
        self.nom_projet = QLineEdit()
        self.code_projet = QLineEdit()
        self.chef_projet = QLineEdit()
        self.ingenieur = QLineEdit()
        echelle_label = QLabel("Échelle du projet :")
        self.echelle_input = QLineEdit()
        self.echelle_input.setPlaceholderText("Ex : 40 pour 1/40")
        echelle_help = QLabel("<span style='color:#aaa'>Entrez le dénominateur de l'échelle (ex : 40 pour 1/40, 47 pour 1/47)</span>")
        self.type_install = QComboBox()
        self.type_install.addItems(["Bassin", "Canal"])
        self.date_projet = QDateEdit()
        self.date_projet.setDate(QDate.currentDate())
        self.format_enreg = QComboBox()
        self.format_enreg.addItems(["CSV", "JSON"])
        
        # Sélecteur de backend d'acquisition
        self.backend_acquisition = QComboBox()
        self.backend_acquisition.addItems(["Simulate", "NI-DAQ", "IOTech", "Arduino"])
        self.backend_acquisition.setCurrentText("Simulate")  # Par défaut
        self.backend_acquisition.currentTextChanged.connect(self.on_backend_changed)
        
        # Fréquence d'échantillonnage
        self.freq_echantillonnage = QLineEdit()
        self.freq_echantillonnage.setText("32.0")
        self.freq_echantillonnage.setPlaceholderText("Hz")

        form.addRow("Nom du projet :", self.nom_projet)
        form.addRow("Code du projet :", self.code_projet)
        form.addRow("Chef de projet :", self.chef_projet)
        form.addRow("Ingénieur/Technicien :", self.ingenieur)
        form.addRow(echelle_label, self.echelle_input)
        form.addRow("", echelle_help)
        form.addRow("Type d'installation :", self.type_install)
        form.addRow("Date du projet :", self.date_projet)
        form.addRow("Format d'enregistrement :", self.format_enreg)
        form.addRow("Backend d'acquisition :", self.backend_acquisition)
        form.addRow("Fréquence (Hz) :", self.freq_echantillonnage)
        layout.addLayout(form)

        file_layout = QHBoxLayout()
        file_label = QLabel("Fichier de sauvegarde :")
        self.file_path = QLineEdit()
        file_btn = QPushButton("Choisir...")
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(file_btn)
        layout.addLayout(file_layout)

        file_btn.clicked.connect(self.choose_file)

        self.next_step = QPushButton("Continuer")
        layout.addWidget(self.next_step)
        self.setLayout(layout)

    def toggle_theme(self):
        if self.theme_switch.isChecked():
            set_dark_mode(QApplication.instance())
        else:
            set_light_mode(QApplication.instance())
    
    def on_backend_changed(self, backend_text):
        """Gère le changement de backend d'acquisition"""
        # Mapper les noms d'affichage vers les noms internes
        backend_mapping = {
            "Simulate": "simulate",
            "NI-DAQ": "ni",
            "IOTech": "iotech",
            "Arduino": "arduino"
        }
        
        backend_mode = backend_mapping.get(backend_text, "simulate")
        
        # Notifier l'application principale si elle existe
        if hasattr(self, 'parent') and self.parent() and hasattr(self.parent(), 'change_acquisition_backend'):
            try:
                fs = float(self.freq_echantillonnage.text() or "32.0")
                success = self.parent().change_acquisition_backend(backend_mode, fs)
                if not success:
                    # Revenir à simulate en cas d'erreur
                    self.backend_acquisition.setCurrentText("Simulate")
                    QMessageBox.warning(self, "Erreur", f"Impossible d'initialiser le backend {backend_text}. Retour à la simulation.")
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Fréquence d'échantillonnage invalide. Utilisation de 32.0 Hz.")
                self.freq_echantillonnage.setText("32.0")
    
    def get_acquisition_config(self):
        """Retourne la configuration d'acquisition sélectionnée"""
        backend_mapping = {
            "Simulate": "simulate",
            "NI-DAQ": "ni",
            "IOTech": "iotech",
            "Arduino": "arduino"
        }
        
        return {
            'backend': backend_mapping.get(self.backend_acquisition.currentText(), "simulate"),
            'sample_rate': float(self.freq_echantillonnage.text() or "32.0")
        }

    def choose_file(self):
        fmt = self.format_enreg.currentText().lower()
        ext = "json" if fmt == "json" else "csv"
        path, _ = QFileDialog.getSaveFileName(self, "Choisir le fichier de sauvegarde", f"projet.{ext}", f"*.{ext}")
        if path:
            self.file_path.setText(path)

    def sync_theme_switch(self, theme):
        if theme == "dark":
            self.theme_switch.setChecked(True)
        else:
            self.theme_switch.setChecked(False)

from PyQt5.QtCore import Qt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_dark_mode(app)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())