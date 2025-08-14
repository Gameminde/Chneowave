#!/usr/bin/env python3
"""
Test simple pour vérifier les erreurs CSS de parsing QLabel
"""

import sys
import os
from io import StringIO
from contextlib import redirect_stderr

# Ajouter le chemin du projet
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer
    
    # Capturer stderr pour les erreurs CSS
    stderr_capture = StringIO()
    
    with redirect_stderr(stderr_capture):
        app = QApplication(sys.argv)
        
        # Importer et créer la fenêtre principale
        from hrneowave.gui.main_window import MainWindow
        
        window = MainWindow()
        window.show()
        
        # Fermer automatiquement après 2 secondes
        QTimer.singleShot(2000, app.quit)
        
        # Lancer l'application
        app.exec()
    
    # Analyser les erreurs capturées
    errors = stderr_capture.getvalue()
    
    if "Could not parse stylesheet" in errors:
        print("❌ ERREURS CSS DÉTECTÉES:")
        print(errors)
        sys.exit(1)
    else:
        print("✅ AUCUNE ERREUR CSS DÉTECTÉE")
        print("Application lancée avec succès")
        sys.exit(0)
        
except Exception as e:
    print(f"❌ ERREUR LORS DU LANCEMENT: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)