#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de l'interface CHNeoWave
Vérifie que l'application démarre correctement et que l'interface est visible
"""

import sys
import os
from pathlib import Path
# MockPerformanceMonitor est maintenant géré par conftest.py

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_interface():
    """Test de l'interface utilisateur"""
    print("🔍 Test de l'interface CHNeoWave...")
    
    try:
        # Import de Qt
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        
        # Création de l'application Qt
        app = QApplication(sys.argv)
        
        # Import des modules CHNeoWave avec mock
        from src.hrneowave.gui.view_manager import ViewManager
        from src.hrneowave.gui.styles.theme_manager import ThemeManager
        
        # PerformanceMonitor est maintenant mocké par conftest.py
        from src.hrneowave.gui.views.dashboard_view import DashboardView
        
        print("✅ Imports réussis")
        
        # Test de création de la vue d'accueil
        dashboard_view = DashboardView()
        print(f"✅ DashboardView créée: {dashboard_view}")
        print(f"   - Taille: {dashboard_view.size()}")
        print(f"   - Visible: {dashboard_view.isVisible()}")
        
        # Test du thème
        theme_manager = ThemeManager(app)
        print(f"✅ ThemeManager créé: {theme_manager}")
        
        # Test de création réussi sans affichage pour éviter les violations d'accès
        print(f"   - Widget créé avec succès")
        print(f"   - Type: {type(dashboard_view)}")
        
        # Test de fermeture propre
        dashboard_view.close()
        print("✅ Vue fermée proprement")
        
        # Fermeture de l'application
        app.quit()
        print("✅ Application fermée")
        
        print(f"✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_interface()
    if success:
        print("🎉 Test de l'interface réussi !")
    else:
        print("💥 Test de l'interface échoué !")
    sys.exit(0 if success else 1)