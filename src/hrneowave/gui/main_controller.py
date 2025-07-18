# main_controller.py - Contrôleur principal pour orchestrer les vues
import sys
import os
from typing import Dict, Any, Optional

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

try:
    from hrneowave.gui.views.acquisition_view import AcquisitionView
    print("✅ AcquisitionView importée")
except ImportError as e:
    print(f"⚠️ Import AcquisitionView manquant: {e}")
    AcquisitionView = None

try:
    from hrneowave.gui.views.analysis_view import AnalysisView
    print("✅ AnalysisView importée")
except ImportError as e:
    print(f"⚠️ Import AnalysisView manquant: {e}")
    AnalysisView = None

try:
    from hrneowave.gui.controllers.acquisition_controller import AcquisitionController
    print("✅ AcquisitionController importé")
except ImportError as e:
    print(f"⚠️ Import AcquisitionController manquant: {e}")
    AcquisitionController = None

try:
    from hrneowave.gui.post_processor import PostProcessor
    print("✅ PostProcessor importé")
except ImportError as e:
    print(f"⚠️ Import PostProcessor manquant: {e}")
    PostProcessor = None

class MainController(QMainWindow):
    """Contrôleur principal HRNeoWave
    
    Gère:
    - Transition automatique Acquisition → Analyse après Stop
    - Découplage AcquisitionView ↔ AcquisitionController
    - Découplage AnalysisView ↔ PostProcessor
    - Configuration globale
    - Gestion des erreurs
    """
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__()
        
        # Configuration
        self.config = self._load_config(config_path)
        
        # Contrôleurs métier
        self.acquisition_controller = None
        self.post_processor = None
        
        # Vues
        self.acquisition_view = None
        self.analysis_view = None
        
        # Interface
        self.stacked_widget = None
        
        self._init_controllers()
        self._init_ui()
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Charge la configuration depuis fichier ou utilise défauts"""
        default_config = {
            # Acquisition
            'n_channels': 4,
            'sample_rate': 32.0,
            'duration': 300,  # 5 minutes
            'buffer_size': 1024,
            
            # Chemins
            'save_folder': './data',
            'export_folder': './exports',
            
            # Performance
            'max_fps': 60,
            'update_interval_ms': 16,  # ~60 FPS
            
            # Interface
            'theme': 'dark',
            'auto_analysis': True,
            'min_window_size': (1024, 640),
            'default_window_size': (1280, 720),
            
            # Analyse
            'fft_window': 'hann',
            'overlap_ratio': 0.5,
            'frequency_bands': [(0.05, 0.5), (0.5, 2.0), (2.0, 10.0)],
            
            # Export
            'default_formats': ['csv', 'hdf5'],
            'include_metadata': True,
            'compress_exports': True
        }
        
        if config_path and os.path.exists(config_path):
            try:
                import json
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"⚠️ Erreur chargement config: {e}")
                
        return default_config
        
    def _init_controllers(self):
        """Initialise les contrôleurs métier"""
        try:
            # Contrôleur acquisition - utiliser la factory function
            if AcquisitionController:
                from hrneowave.gui.controllers.acquisition_controller import create_acquisition_controller
                self.acquisition_controller = create_acquisition_controller(
                    mode_str='simulate',
                    fs=self.config.get('sample_rate', 32.0),
                    sensor_type='wave_probe'
                )
            else:
                print("⚠️ AcquisitionController non disponible - mode simulation")
                self.acquisition_controller = None
                
            # Post-processeur
            if PostProcessor:
                self.post_processor = PostProcessor(config_path=None)  # Utilise config par défaut
            else:
                print("⚠️ PostProcessor non disponible - analyse simplifiée")
                self.post_processor = None
                
        except Exception as e:
            print(f"⚠️ Erreur initialisation contrôleurs: {e}")
            self.acquisition_controller = None
            self.post_processor = None
            
    def _init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("HRNeoWave - Laboratoire d'Étude Maritime")
        
        # Taille fenêtre
        min_size = self.config['min_window_size']
        default_size = self.config['default_window_size']
        
        self.setMinimumSize(*min_size)
        self.resize(*default_size)
        
        # Widget empilé pour basculer entre vues
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Créer vue acquisition
        self._create_acquisition_view()
        
        # Appliquer thème
        self._apply_global_theme()
        
        # Centrer fenêtre
        self._center_window()
        
    def _create_acquisition_view(self):
        """Crée et configure la vue d'acquisition"""
        if not AcquisitionView:
            self._show_error("Vue d'acquisition non disponible")
            return
            
        try:
            # Créer vue
            self.acquisition_view = AcquisitionView(
                config=self.config,
                acquisition_controller=self.acquisition_controller
            )
            
            # Connecter signaux
            self.acquisition_view.acquisitionStarted.connect(self._on_acquisition_started)
            self.acquisition_view.acquisitionStopped.connect(self._on_acquisition_stopped)
            self.acquisition_view.dataExported.connect(self._on_data_exported)
            self.acquisition_view.analysisRequested.connect(self._on_analysis_requested)
            
            # Ajouter au stack
            self.stacked_widget.addWidget(self.acquisition_view)
            self.stacked_widget.setCurrentWidget(self.acquisition_view)
            
        except Exception as e:
            self._show_error(f"Erreur création vue acquisition: {e}")
            
    def _create_analysis_view(self, filepath: str):
        """Crée et configure la vue d'analyse"""
        if not AnalysisView:
            self._show_error("Vue d'analyse non disponible")
            return
            
        try:
            # Créer vue
            self.analysis_view = AnalysisView(
                filepath=filepath,
                config=self.config,
                post_processor=self.post_processor
            )
            
            # Connecter signaux
            self.analysis_view.analysisCompleted.connect(self._on_analysis_completed)
            self.analysis_view.exportCompleted.connect(self._on_export_completed)
            
            # Ajouter au stack et basculer
            self.stacked_widget.addWidget(self.analysis_view)
            self.stacked_widget.setCurrentWidget(self.analysis_view)
            
            # Mettre à jour titre
            filename = os.path.basename(filepath)
            self.setWindowTitle(f"HRNeoWave - Analyse: {filename}")
            
        except Exception as e:
            self._show_error(f"Erreur création vue analyse: {e}")
            
    def _apply_global_theme(self):
        """Applique le thème global"""
        if self.config['theme'] == 'dark':
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QStackedWidget {
                    background-color: #1e1e1e;
                }
            """)
            
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
        
    # === SLOTS ACQUISITION ===
    
    @pyqtSlot()
    def _on_acquisition_started(self):
        """Acquisition démarrée"""
        print("🚀 Acquisition démarrée")
        
        # Mettre à jour titre
        self.setWindowTitle("HRNeoWave - Acquisition en cours...")
        
        # Démarrer contrôleur si disponible
        if self.acquisition_controller:
            try:
                self.acquisition_controller.start_acquisition()
            except Exception as e:
                print(f"⚠️ Erreur démarrage acquisition: {e}")
                
    @pyqtSlot()
    def _on_acquisition_stopped(self):
        """Acquisition arrêtée"""
        print("⏹️ Acquisition arrêtée")
        
        # Mettre à jour titre
        self.setWindowTitle("HRNeoWave - Acquisition terminée")
        
        # Arrêter contrôleur si disponible
        if self.acquisition_controller:
            try:
                self.acquisition_controller.stop_acquisition()
            except Exception as e:
                print(f"⚠️ Erreur arrêt acquisition: {e}")
                
    @pyqtSlot(str)
    def _on_data_exported(self, filepath: str):
        """Données exportées"""
        print(f"💾 Données exportées: {filepath}")
        
    @pyqtSlot(str)
    def _on_analysis_requested(self, filepath: str):
        """Analyse demandée - transition automatique"""
        print(f"📊 Analyse demandée pour: {filepath}")
        
        if self.config.get('auto_analysis', True):
            # Transition automatique vers vue analyse
            self._create_analysis_view(filepath)
        else:
            # Demander confirmation
            reply = QMessageBox.question(
                self, 
                "Analyse",
                f"Ouvrir l'analyse pour:\n{os.path.basename(filepath)}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self._create_analysis_view(filepath)
                
    # === SLOTS ANALYSE ===
    
    @pyqtSlot(dict)
    def _on_analysis_completed(self, results: Dict[str, Any]):
        """Analyse terminée"""
        print("✅ Analyse terminée")
        
        # Optionnel: traitement des résultats
        if self.post_processor:
            try:
                self.post_processor.process_results(results)
            except Exception as e:
                print(f"⚠️ Erreur post-traitement: {e}")
                
    @pyqtSlot(str)
    def _on_export_completed(self, filepath: str):
        """Export terminé"""
        print(f"📁 Export terminé: {filepath}")
        
    # === MÉTHODES PUBLIQUES ===
    
    def switch_to_acquisition(self):
        """Bascule vers la vue d'acquisition"""
        if self.acquisition_view:
            self.stacked_widget.setCurrentWidget(self.acquisition_view)
            self.setWindowTitle("HRNeoWave - Acquisition")
        else:
            self._create_acquisition_view()
            
    def switch_to_analysis(self, filepath: str):
        """Bascule vers la vue d'analyse"""
        if os.path.exists(filepath):
            self._create_analysis_view(filepath)
        else:
            self._show_error(f"Fichier non trouvé: {filepath}")
            
    def get_current_view(self) -> str:
        """Retourne la vue actuelle"""
        current = self.stacked_widget.currentWidget()
        
        if current == self.acquisition_view:
            return "acquisition"
        elif current == self.analysis_view:
            return "analysis"
        else:
            return "unknown"
            
    def cleanup(self):
        """Nettoyage avant fermeture"""
        print("🧹 Nettoyage en cours...")
        
        # Arrêter acquisition si en cours
        if self.acquisition_controller:
            try:
                self.acquisition_controller.stop_acquisition()
            except:
                pass
                
        # Nettoyer vues
        if self.acquisition_view:
            try:
                self.acquisition_view.update_timer.stop()
            except:
                pass
                
        if self.analysis_view:
            try:
                if hasattr(self.analysis_view, 'analysis_thread'):
                    self.analysis_view.analysis_thread.quit()
                    self.analysis_view.analysis_thread.wait()
            except:
                pass
                
        print("✅ Nettoyage terminé")
        
    def _show_error(self, message: str):
        """Affiche un message d'erreur"""
        print(f"❌ {message}")
        QMessageBox.critical(self, "Erreur", message)
        
    # === ÉVÉNEMENTS ===
    
    def closeEvent(self, event):
        """Gestion fermeture application"""
        # Demander confirmation si acquisition en cours
        if (self.acquisition_view and 
            hasattr(self.acquisition_view, 'is_acquiring') and 
            self.acquisition_view.is_acquiring):
            
            reply = QMessageBox.question(
                self,
                "Fermeture",
                "Une acquisition est en cours.\nVoulez-vous vraiment quitter?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        # Nettoyage
        self.cleanup()
        
        # Accepter fermeture
        event.accept()
        
    def keyPressEvent(self, event):
        """Gestion raccourcis clavier"""
        # F11: Plein écran
        if event.key() == 16777274:  # F11
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
                
        # Ctrl+Q: Quitter
        elif event.key() == 81 and event.modifiers() == 67108864:  # Ctrl+Q
            self.close()
            
        # Ctrl+1: Vue acquisition
        elif event.key() == 49 and event.modifiers() == 67108864:  # Ctrl+1
            self.switch_to_acquisition()
            
        else:
            super().keyPressEvent(event)

def main():
    """Point d'entrée principal"""
    app = QApplication(sys.argv)
    
    # Configuration application
    app.setApplicationName("HRNeoWave")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Laboratoire d'Étude Maritime")
    
    # Créer contrôleur principal
    try:
        controller = MainController()
        controller.show()
        
        # Boucle événements
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()