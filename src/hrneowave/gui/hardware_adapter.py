"""
Adaptateur pour intégrer l'interface hardware dans l'interface graphique
"""

from PyQt5.QtWidgets import (QGroupBox, QPushButton, QComboBox, QLabel, 
                           QVBoxLayout, QMessageBox)
from hardware_interface import HardwareInterface, AcquisitionDevice

class HardwareAcquisitionAdapter:
    """
    Adaptateur pour intégrer le hardware dans RealTimeAcquisitionWindow
    """
    
    def __init__(self, acquisition_window):
        self.window = acquisition_window
        self.hardware = HardwareInterface()
        self.selected_device = None
        self.active_channels = []
        
    def setup_hardware_controls(self):
        """
        Ajoute les contrôles hardware à l'interface existante
        """
        # Créer le groupe de contrôles hardware
        hardware_group = QGroupBox("🔌 Configuration Hardware")
        hardware_layout = QVBoxLayout(hardware_group)
        
        # Bouton de scan
        self.scan_btn = QPushButton("🔍 Détecter Périphériques")
        self.scan_btn.clicked.connect(self.scan_and_update_devices)
        hardware_layout.addWidget(self.scan_btn)
        
        # Liste déroulante des périphériques
        self.device_combo = QComboBox()
        hardware_layout.addWidget(self.device_combo)
        
        # Bouton de connexion
        self.connect_btn = QPushButton("🔗 Connecter")
        self.connect_btn.clicked.connect(self.connect_selected_device)
        hardware_layout.addWidget(self.connect_btn)
        
        # Statut
        self.status_label = QLabel("⚪ Non connecté")
        hardware_layout.addWidget(self.status_label)
        
        # Insérer dans l'interface existante
        # (À adapter selon la structure exacte de votre UI)
        self.window.left_panel_vbox.insertWidget(1, hardware_group)
        
    def scan_and_update_devices(self):
        """Scanne et met à jour la liste des périphériques"""
        devices = self.hardware.scan_devices()
        
        self.device_combo.clear()
        for device in devices:
            self.device_combo.addItem(
                f"{device.description} ({device.port_name})",
                userData=device
            )
            
        if devices:
            self.status_label.setText(f"✅ {len(devices)} périphérique(s) trouvé(s)")
        else:
            self.status_label.setText("❌ Aucun périphérique détecté")
            
    def connect_selected_device(self):
        """Connecte le périphérique sélectionné"""
        if self.device_combo.currentIndex() < 0:
            return
            
        device = self.device_combo.currentData()
        if self.hardware.connect(device):
            self.selected_device = device
            self.status_label.setText(f"🟢 Connecté à {device.description}")
            self.connect_btn.setText("🔌 Déconnecter")
            self.connect_btn.clicked.disconnect()
            self.connect_btn.clicked.connect(self.disconnect_device)
            
            # Configurer les canaux actifs
            self.active_channels = list(range(min(self.window.n_sondes_total_calib, 
                                                 device.max_channels)))
            
            # Configurer l'échantillonnage
            self.hardware.configure_sampling(self.window.freq, self.active_channels)
            
            # Remplacer la méthode d'acquisition
            self.window.hardware_interface = self.hardware
            self.override_acquisition_method()
        else:
            self.status_label.setText("❌ Échec de connexion")
            
    def disconnect_device(self):
        """Déconnecte le périphérique"""
        self.hardware.disconnect()
        self.selected_device = None
        self.status_label.setText("⚪ Non connecté")
        self.connect_btn.setText("🔗 Connecter")
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self.connect_selected_device)
        
    def override_acquisition_method(self):
        """
        Remplace la méthode d'acquisition simulée par l'acquisition hardware
        """
        def hardware_acquire_data_sample(self_window):
            if not self_window.running:
                return
            if self_window.sample_count >= self_window.max_samples:
                self_window.finalize_acquisition()
                return

            current_t = self_window.sample_count / self_window.freq
            self_window.time_storage_full.append(current_t)

            try:
                # Lire tous les canaux actifs
                raw_values = self.hardware.read_all_channels()
                
                for i in range(self_window.n_sondes_total_calib):
                    if i < len(raw_values):
                        # Appliquer la calibration
                        raw_value = raw_values[i]
                        calib = self_window.calibration_params_all[i]
                        
                        # Convertir tension en hauteur selon calibration
                        calibrated_value = raw_value * calib['slope'] + calib['intercept']
                        
                        # Gérer les unités
                        if calib['unit'] == 'cm':
                            calibrated_value /= 100.0  # Convertir en mètres
                            
                        self_window.data_storage_full[i].append(calibrated_value)
                    else:
                        # Pas assez de canaux hardware, utiliser 0
                        self_window.data_storage_full[i].append(0.0)
                        
            except Exception as e:
                print(f"❌ Erreur acquisition hardware: {e}")
                # Fallback sur données nulles
                for i in range(self_window.n_sondes_total_calib):
                    self_window.data_storage_full[i].append(0.0)

            self_window.sample_count += 1
        
        # Remplacer la méthode
        import types
        self.window.acquire_data_sample = types.MethodType(hardware_acquire_data_sample, 
                                                          self.window) 