import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt

def test_minimal_window():
    """Test fenêtre minimale pour vérifier l'affichage Qt"""
    app = QApplication(sys.argv)
    
    # Fenêtre minimale pour test
    window = QMainWindow()
    window.setWindowTitle("Test CHNeoWave - Interface Visible")
    window.setGeometry(100, 100, 800, 600)
    
    # Label simple sans CSS problématique
    label = QLabel("Interface CHNeoWave - Test Visuel")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color: #1565C0; font-size: 24px; padding: 20px;")
    
    window.setCentralWidget(label)
    
    # FORCER L'AFFICHAGE (CRITIQUE)
    window.show()
    window.raise_()
    window.activateWindow()
    
    print("✅ Fenêtre de test affichée")
    print("✅ Si vous voyez cette fenêtre, Qt fonctionne")
    print(f"✅ Géométrie : {window.geometry()}")
    print(f"✅ Visible : {window.isVisible()}")
    
    # Timer pour fermer automatiquement après 5 secondes
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(5000)  # 5 secondes
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_minimal_window()