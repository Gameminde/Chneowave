#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'Étape 1 : Palette & apply_skin()
Vérifie que le nouveau système de thème HRNeoWave fonctionne
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt

try:
    from hrneowave.gui.theme import (
        apply_skin, get_color, apply_widget_class,
        CLASS_ACCENT, CLASS_LARGE, CLASS_TITLE, CLASS_SUBTITLE
    )
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test HRNeoWave Skin - Étape 1")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Titre principal
        title = QLabel("Test de la Palette HRNeoWave")
        apply_widget_class(title, CLASS_TITLE)
        layout.addWidget(title)
        
        # Sous-titre
        subtitle = QLabel("Vérification des couleurs et styles")
        apply_widget_class(subtitle, CLASS_SUBTITLE)
        layout.addWidget(subtitle)
        
        # Groupe de test des boutons
        button_group = QGroupBox("Test des Boutons")
        button_layout = QHBoxLayout(button_group)
        
        # Bouton normal
        normal_btn = QPushButton("Bouton Normal")
        button_layout.addWidget(normal_btn)
        
        # Bouton accent
        accent_btn = QPushButton("Bouton Accent")
        apply_widget_class(accent_btn, CLASS_ACCENT)
        button_layout.addWidget(accent_btn)
        
        # Bouton large
        large_btn = QPushButton("Bouton Large")
        apply_widget_class(large_btn, CLASS_LARGE)
        button_layout.addWidget(large_btn)
        
        # Bouton large + accent
        large_accent_btn = QPushButton("Large + Accent")
        large_accent_btn.setProperty('class', f'{CLASS_LARGE} {CLASS_ACCENT}')
        large_accent_btn.style().unpolish(large_accent_btn)
        large_accent_btn.style().polish(large_accent_btn)
        button_layout.addWidget(large_accent_btn)
        
        layout.addWidget(button_group)
        
        # Groupe de test des champs
        input_group = QGroupBox("Test des Champs de Saisie")
        input_layout = QVBoxLayout(input_group)
        
        line_edit = QLineEdit("Champ de texte")
        input_layout.addWidget(line_edit)
        
        text_edit = QTextEdit("Zone de texte\nMulti-lignes")
        text_edit.setMaximumHeight(100)
        input_layout.addWidget(text_edit)
        
        layout.addWidget(input_group)
        
        # Boutons de contrôle du thème
        theme_group = QGroupBox("Contrôle du Thème")
        theme_layout = QHBoxLayout(theme_group)
        
        dark_btn = QPushButton("Thème Sombre")
        dark_btn.clicked.connect(lambda: self.apply_dark_theme())
        theme_layout.addWidget(dark_btn)
        
        light_btn = QPushButton("Thème Clair")
        light_btn.clicked.connect(lambda: self.apply_light_theme())
        theme_layout.addWidget(light_btn)
        
        layout.addWidget(theme_group)
        
        # Informations sur les couleurs
        color_info = QLabel(self.get_color_info())
        color_info.setWordWrap(True)
        layout.addWidget(color_info)
        
        # Appliquer le thème sombre par défaut
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Applique le thème sombre HRNeoWave"""
        app = QApplication.instance()
        apply_skin(app, dark=True)
        print("✅ Thème sombre appliqué")
    
    def apply_light_theme(self):
        """Applique le thème clair"""
        app = QApplication.instance()
        apply_skin(app, dark=False)
        print("✅ Thème clair appliqué")
    
    def get_color_info(self):
        """Retourne les informations sur la palette"""
        colors = [
            ('background', 'Arrière-plan'),
            ('surface', 'Surface'),
            ('text', 'Texte'),
            ('accent', 'Accent'),
            ('success', 'Succès'),
            ('warning', 'Avertissement'),
            ('error', 'Erreur')
        ]
        
        info = "Palette HRNeoWave:\n"
        for color_key, description in colors:
            color_value = get_color(color_key)
            info += f"• {description}: {color_value}\n"
        
        return info

def main():
    app = QApplication(sys.argv)
    
    print("🎨 Test de l'Étape 1 : Palette & apply_skin()")
    print("=" * 50)
    
    # Créer la fenêtre de test
    window = TestWindow()
    window.show()
    
    print("\n📋 Instructions de test:")
    print("1. Vérifiez que le thème sombre est appliqué par défaut")
    print("2. Testez les boutons 'Thème Sombre' et 'Thème Clair'")
    print("3. Vérifiez que les styles des boutons sont corrects:")
    print("   - Bouton Normal: style de base")
    print("   - Bouton Accent: couleur d'accent (#00B5AD)")
    print("   - Bouton Large: taille minimale 120x48px")
    print("   - Large + Accent: combinaison des deux")
    print("4. Vérifiez que les champs de saisie ont le bon style")
    print("5. Vérifiez que les couleurs correspondent à la palette")
    print("\n✅ Si tout fonctionne, l'Étape 1 est validée!")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()