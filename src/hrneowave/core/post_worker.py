# src/hrneowave/core/post_worker.py

# Import conditionnel des modules Qt
def _ensure_qt_imports():
    """Assure que les modules Qt sont importés correctement"""
    global QThread, Signal
    try:
        from PySide6.QtCore import QThread, Signal
        return True
    except ImportError:
        try:
            from PyQt6.QtCore import QThread, pyqtSignal as Signal
            return True
        except ImportError:
            try:
                from PySide6.QtCore import QThread, Signal
                return True
            except ImportError:
                return False

class PostWorker(QThread):
    analysisDone = Signal(dict)

    def __init__(self, file_path: str, config: dict):
        _ensure_qt_imports()
        super().__init__()
        self.file_path = file_path
        self.config = config

    def run(self):
        """Exécute le post-traitement dans un thread séparé."""
        from hrneowave.gui.post_processor import PostProcessor
        
        # Crée une instance de PostProcessor avec la configuration
        processor = PostProcessor(config=self.config)
        
        # Charge les données et exécute l'analyse
        if processor.load_data_file(self.file_path):
            result = processor.run_analysis()
            if result:
                self.analysisDone.emit(processor.current_analysis)
            else:
                # Émettre un dictionnaire vide ou avec une erreur en cas d'échec de l'analyse
                self.analysisDone.emit({'error': 'Analysis failed'})
        else:
            # Émettre un dictionnaire vide ou avec une erreur en cas d'échec de chargement
            self.analysisDone.emit({'error': f'Failed to load data from {self.file_path}'})