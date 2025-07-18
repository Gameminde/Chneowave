# main.py - Point d'entrée HRNeoWave avec nouveau contrôleur principal
import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Configuration pour meilleur débogage
def excepthook(exc_type, exc_value, exc_tb):
    traceback.print_exception(exc_type, exc_value, exc_tb)
    
sys.excepthook = excepthook

# Import du nouveau contrôleur principal
try:
    from hrneowave.gui.main_controller import MainController
except ImportError as e:
    print(f"❌ Erreur import MainController: {e}")
    MainController = None

# Imports legacy pour compatibilité (si nécessaire)
try:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
    from hrneowave.gui.theme import set_dark_mode, set_light_mode, current_theme, register_theme_callback
    from hrneowave.gui.welcome import WelcomeWindow
    from hrneowave.gui.calibration import CalibrationMainWindow
    from hrneowave.gui.acquisition import AcquisitionSetupWindow
    from hrneowave.gui.views.acquisition_view import AcquisitionView
    from hrneowave.gui.views.analysis_view import AnalysisView
    from hrneowave.gui.modern_acquisition_ui import ModernAcquisitionUI
    from hrneowave.gui.controllers.acquisition_controller import create_acquisition_controller, AcquisitionController
    LEGACY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Modules legacy non disponibles: {e}")
    LEGACY_AVAILABLE = False
    # Import minimal pour QWidget
    try:
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
    except ImportError:
        QWidget = object  # Fallback

class HRNeoWaveApp:
    """Application principale HRNeoWave - Wrapper pour compatibilité legacy
    
    Cette classe maintient la compatibilité avec l'ancien code tout en
    utilisant le nouveau MainController pour les nouvelles fonctionnalités.
    """
    
    def __init__(self, use_new_interface=True):
        self.use_new_interface = use_new_interface
        self.main_controller = None
        self.legacy_app = None
        
        if use_new_interface and MainController:
            self._init_new_interface()
        elif LEGACY_AVAILABLE:
            self._init_legacy_interface()
        else:
            raise RuntimeError("Aucune interface disponible")
            
    def _init_new_interface(self):
        """Initialise la nouvelle interface avec MainController"""
        try:
            # Configuration par défaut
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            
            # Créer contrôleur principal
            self.main_controller = MainController(config_path if os.path.exists(config_path) else None)
            
            print("✅ Nouvelle interface initialisée avec succès")
            
        except Exception as e:
            print(f"❌ Erreur initialisation nouvelle interface: {e}")
            if LEGACY_AVAILABLE:
                print("🔄 Basculement vers interface legacy")
                self._init_legacy_interface()
            else:
                raise
                
    def _init_legacy_interface(self):
        """Initialise l'interface legacy (ancienne version)"""
        print("⚠️ Utilisation interface legacy")
        self.legacy_app = LegacyHRNeoWaveApp()
        
    def show(self):
        """Affiche l'application"""
        if self.main_controller:
            self.main_controller.show()
        elif self.legacy_app:
            self.legacy_app.show()
            
    def exec_(self):
        """Lance la boucle d'événements (pour compatibilité)"""
        # La boucle d'événements est gérée par QApplication
        pass
        
    def close(self):
        """Ferme l'application"""
        if self.main_controller:
            self.main_controller.close()
        elif self.legacy_app:
            self.legacy_app.close()

class LegacyHRNeoWaveApp(QWidget):
    """Application legacy HRNeoWave (ancienne interface simplifiée)"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HRNeoWave - Interface Legacy")
        self.setGeometry(50, 50, 800, 600)
        
        # Interface simplifiée pour éviter les erreurs
        layout = QVBoxLayout(self)
        
        warning = QLabel(
            "⚠️ Interface Legacy\n\n"
            "Cette version utilise l'ancienne interface.\n"
            "Pour utiliser la nouvelle interface optimisée,\n"
            "assurez-vous que tous les modules sont disponibles.\n\n"
            "Utilisez 'py main.py --new' pour la nouvelle interface."
        )
        warning.setStyleSheet(
            "QLabel { "
            "background-color: #2d2d2d; "
            "color: #ffffff; "
            "padding: 20px; "
            "border-radius: 8px; "
            "font-size: 14px; "
            "}"
        )
        warning.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(warning)
        
        # Initialisation minimale
        self.acquisition_controller = None
        if LEGACY_AVAILABLE:
            try:
                self.acquisition_controller = create_acquisition_controller('simulate', 32.0)
                print("✅ Contrôleur d'acquisition legacy initialisé")
            except Exception as e:
                print(f"⚠️ Erreur init legacy: {e}")
                
    def show(self):
        """Affiche l'interface legacy"""
        super().show()
        print("📱 Interface Legacy affichée")
        
    def close(self):
        """Ferme l'interface legacy"""
        if self.acquisition_controller:
            try:
                self.acquisition_controller.stop()
                self.acquisition_controller.disconnect()
            except:
                pass
        super().close()
        
    def _init_modern_ui(self):
        """Interface legacy simplifiée"""
        layout = QVBoxLayout(self)
        label = QLabel("Interface Legacy - Utilisez --new pour la nouvelle interface")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
    def _create_title_bar(self):
        """Méthode legacy simplifiée"""
        pass
        
    def _create_status_bar(self):
        """Méthode legacy simplifiée"""
        pass

    def _init_acquisition_controller(self):
        """Initialise le contrôleur d'acquisition avec les paramètres d'environnement"""
        try:
            # Récupérer les paramètres depuis les variables d'environnement ou valeurs par défaut
            mode = os.getenv('CHNW_MODE', 'simulate')  # simulate, ni, iotech, arduino
            fs = float(os.getenv('CHNW_FS', '32.0'))   # Fréquence d'échantillonnage
            sensor_type = os.getenv('CHNW_SENSOR_TYPE', 'wave_probe')
            
            # Créer le contrôleur d'acquisition
            self.acquisition_controller = create_acquisition_controller(
                mode_str=mode,
                fs=fs,
                sensor_type=sensor_type
            )
            
            print(f"✓ Contrôleur d'acquisition initialisé: mode={mode}, fs={fs}Hz")
            
        except Exception as e:
            print(f"⚠️ Erreur initialisation contrôleur: {e}")
            # Fallback sur simulation
            self.acquisition_controller = create_acquisition_controller(
                mode_str='simulate',
                fs=32.0
            )

    def setup_connections(self):
        """Méthode legacy simplifiée"""
        pass
        
    def go_to_calibration(self):
        """Méthode legacy simplifiée"""
        pass

    def go_to_acquisition_setup(self):
        """Méthode legacy simplifiée"""
        pass
        
    def go_to_modern_acquisition(self):
        """Méthode legacy simplifiée"""
        pass
        
    def go_to_processing(self):
        """Méthode legacy simplifiée"""
        pass
                
    def _on_tab_changed(self, index):
        """Méthode legacy simplifiée"""
        pass
            
    def _on_calibration_completed(self, calibration_data):
        """Méthode legacy simplifiée"""
        pass
        
    def _on_acquisition_completed(self, data_file):
        """Méthode legacy simplifiée"""
        pass
        
    def _on_modern_acquisition_stopped(self):
        """Méthode legacy simplifiée"""
        pass
        
    def _on_modern_data_exported(self, data_file):
        """Méthode legacy simplifiée"""
        pass

    def change_acquisition_backend(self, mode_str: str, fs: float = None):
        """Méthode legacy simplifiée"""
        pass

    def handle_restart(self):
        """Méthode legacy simplifiée"""
        pass

    def setup_theme_sync(self):
        """Méthode legacy simplifiée"""
        pass
        
    def _toggle_theme(self):
        """Méthode legacy simplifiée"""
        pass
            
    def _show_help(self):
        """Méthode legacy simplifiée"""
        pass
        
    def _apply_professional_theme(self):
        """Méthode legacy simplifiée"""
        pass
            
    def _apply_dark_professional_theme(self):
        """Méthode legacy simplifiée"""
        pass
        
    def _apply_light_professional_theme(self):
        """Méthode legacy simplifiée"""
        pass

def main():
    """Point d'entrée principal de l'application HRNeoWave"""
    try:
        # Vérifier l'aide
        if '--help' in sys.argv or '-h' in sys.argv:
            show_help()
            return 0
            
        # Configuration de l'application
        app = QApplication(sys.argv)
        app.setApplicationName("HRNeoWave")
        app.setApplicationVersion("3.0")
        app.setOrganizationName("Laboratoire Maritime")
        app.setStyle('Fusion')
        
        # Configuration des icônes et ressources
        if os.path.exists('assets/icon.png'):
            from PyQt5.QtGui import QIcon
            app.setWindowIcon(QIcon('assets/icon.png'))
        
        # Déterminer quelle interface utiliser
        use_new_interface = True
        
        # Vérifier les arguments de ligne de commande
        if '--legacy' in sys.argv:
            use_new_interface = False
            print("🔄 Mode legacy forcé via --legacy")
        elif '--new' in sys.argv:
            use_new_interface = True
            print("✨ Mode nouvelle interface forcé via --new")
        
        # Créer et afficher l'application principale
        main_app = HRNeoWaveApp(use_new_interface=use_new_interface)
        main_app.show()
        
        print(f"🚀 HRNeoWave v3.0 démarré ({'nouvelle' if use_new_interface else 'legacy'} interface)")
        
        # Lancer la boucle d'événements
        return app.exec_()
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("Vérifiez que PyQt5 est installé: pip install PyQt5")
        return 1
    except Exception as e:
        print(f"❌ Erreur critique lors du lancement: {e}")
        traceback.print_exc()
        
        # Afficher une boîte de dialogue d'erreur si possible
        try:
            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(
                None, 
                "Erreur Critique - HRNeoWave", 
                f"Impossible de lancer HRNeoWave:\n\n{str(e)}\n\n"
                f"Solutions possibles:\n"
                f"• Essayez avec --legacy pour l'interface legacy\n"
                f"• Vérifiez que tous les modules sont installés\n"
                f"• Consultez les logs pour plus de détails"
            )
        except:
            pass
        
        return 1

def show_help():
    """Affiche l'aide de l'application"""
    help_text = """
HRNeoWave v3.0 - Système d'Analyse de Houle

Usage: python main.py [options]

Options:
  --new      Force l'utilisation de la nouvelle interface (défaut)
  --legacy   Force l'utilisation de l'interface legacy
  --help     Affiche cette aide

Exemples:
  python main.py                # Nouvelle interface (défaut)
  python main.py --legacy       # Interface legacy
  python main.py --new          # Force nouvelle interface

Pour plus d'informations, consultez la documentation.
"""
    print(help_text)

if __name__ == '__main__':
    sys.exit(main())