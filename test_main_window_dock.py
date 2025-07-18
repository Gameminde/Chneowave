#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration du dock dans MainWindow
Validation de l'intégration complète du dock "Infos essai" dans l'interface principale
"""

import sys
import os
from datetime import datetime

# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt, QTimer
except ImportError:
    print("Erreur: PyQt5 non disponible")
    sys.exit(1)

try:
    from hrneowave.gui.main_window import MainWindow
    from hrneowave.gui.theme import apply_skin
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)


class TestMainWindowWithDock(MainWindow):
    """Version de test de MainWindow avec dock intégré"""
    
    def __init__(self, config_path=None):
        super().__init__(config_path)
        
        # Configuration de test
        self.setWindowTitle("HRNeoWave - Test MainWindow avec Dock")
        
        # Simuler des données de projet
        self._simulate_project_data()
        
        # Timer pour simuler une acquisition
        self.test_timer = QTimer()
        self.test_timer.timeout.connect(self._simulate_acquisition_data)
        self.test_sample_count = 0
        
        print("\n=== Test MainWindow avec Dock Infos Essai ===")
        print("1. Vérifiez que le dock 'Infos essai' est présent à droite")
        print("2. Créez un nouveau projet via l'interface")
        print("3. Observez la mise à jour automatique du dock")
        print("4. Testez les méthodes d'acquisition publiques")
        print("5. Vérifiez la synchronisation avec la barre de statut")
        
        # Ajouter des boutons de test dans la barre d'outils
        self._add_test_controls()
    
    def _simulate_project_data(self):
        """Simule la création d'un projet"""
        project_data = {
            'name': f'Test_Project_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'owner': 'Ingénieur Test',
            'type': 'Acquisition Maritime',
            'description': 'Projet de test pour validation du dock',
            'created': datetime.now().isoformat()
        }
        
        # Simuler la réception des données de projet
        self._on_project_created(project_data)
        
        print(f"✅ Projet simulé créé: {project_data['name']}")
    
    def _add_test_controls(self):
        """Ajoute des contrôles de test à la barre d'outils"""
        if hasattr(self, 'toolbar'):
            toolbar = self.toolbar
        else:
            toolbar = self.addToolBar("Test")
        
        # Bouton pour tester l'acquisition
        test_acq_action = toolbar.addAction("🚀 Test Acquisition")
        test_acq_action.triggered.connect(self._test_acquisition)
        
        # Bouton pour tester la pause
        test_pause_action = toolbar.addAction("⏸️ Test Pause")
        test_pause_action.triggered.connect(self._test_pause)
        
        # Bouton pour tester l'arrêt
        test_stop_action = toolbar.addAction("⏹️ Test Arrêt")
        test_stop_action.triggered.connect(self._test_stop)
        
        # Bouton pour tester la configuration
        test_config_action = toolbar.addAction("⚙️ Test Config")
        test_config_action.triggered.connect(self._test_configuration)
    
    def _test_acquisition(self):
        """Test de démarrage d'acquisition"""
        config = {
            'nb_sondes': 6,
            'freq_echantillonnage': 2000,
            'taille_buffer': 20000
        }
        
        print("🚀 Test: Démarrage acquisition")
        self.start_acquisition(config)
        
        # Démarrer la simulation de données
        self.test_sample_count = 0
        self.test_timer.start(200)  # Mise à jour toutes les 200ms
    
    def _test_pause(self):
        """Test de pause d'acquisition"""
        print("⏸️ Test: Pause acquisition")
        if self.is_acquiring:
            self.pause_acquisition()
            self.test_timer.stop()
        else:
            self.resume_acquisition()
            self.test_timer.start(200)
    
    def _test_stop(self):
        """Test d'arrêt d'acquisition"""
        print("⏹️ Test: Arrêt acquisition")
        self.stop_acquisition()
        self.test_timer.stop()
    
    def _test_configuration(self):
        """Test de mise à jour de configuration"""
        print("⚙️ Test: Mise à jour configuration")
        
        if hasattr(self, 'infos_essai_dock') and self.infos_essai_dock:
            # Tester différentes configurations
            configs = [
                {'nb_sondes': 4, 'freq_echantillonnage': 1000, 'taille_buffer': 10000},
                {'nb_sondes': 8, 'freq_echantillonnage': 5000, 'taille_buffer': 50000},
                {'nb_sondes': 12, 'freq_echantillonnage': 10000, 'taille_buffer': 100000}
            ]
            
            import random
            config = random.choice(configs)
            
            self.infos_essai_dock.set_acquisition_config(**config)
            print(f"Configuration mise à jour: {config}")
        else:
            print("❌ Dock non disponible pour le test de configuration")
    
    def _simulate_acquisition_data(self):
        """Simule l'arrivée de données d'acquisition"""
        if self.is_acquiring:
            # Simuler l'arrivée d'échantillons
            increment = 1000  # 1000 échantillons par mise à jour
            self.test_sample_count += increment
            
            # Mettre à jour le dock
            self.update_acquisition_progress(self.test_sample_count)
    
    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        # Arrêter les timers
        if hasattr(self, 'test_timer'):
            self.test_timer.stop()
        
        # Appeler la méthode parent
        super().closeEvent(event)
        
        print("\n✅ Test terminé - Application fermée")


def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("HRNeoWave Test MainWindow")
    app.setApplicationVersion("3.0")
    
    try:
        # Créer la fenêtre principale de test
        window = TestMainWindowWithDock()
        
        # Appliquer le thème
        apply_skin(window, 'dark')
        
        # Afficher la fenêtre
        window.show()
        
        # Vérifier que le dock est bien présent
        if hasattr(window, 'infos_essai_dock') and window.infos_essai_dock:
            print("✅ Dock 'Infos essai' détecté et intégré")
            
            # Afficher quelques informations sur le dock
            dock = window.infos_essai_dock
            print(f"   - Titre: {dock.windowTitle()}")
            print(f"   - Visible: {dock.isVisible()}")
            print(f"   - Flottant: {dock.isFloating()}")
            print(f"   - Zone: {window.dockWidgetArea(dock)}")
        else:
            print("❌ Dock 'Infos essai' non détecté")
            QMessageBox.warning(window, "Avertissement", 
                              "Le dock 'Infos essai' n'a pas pu être créé.")
        
        # Lancer l'application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()