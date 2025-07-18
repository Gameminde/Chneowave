# field_validator.py - Validation des champs obligatoires pour HRNeoWave
from typing import Dict, List, Any, Optional, Tuple
from PyQt5.QtWidgets import QWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPalette, QColor

class FieldValidator(QObject):
    """Validateur de champs pour assurer la qualité des données d'entrée"""
    
    validationChanged = pyqtSignal(bool)  # True si tous les champs sont valides
    fieldError = pyqtSignal(str, str)     # nom_champ, message_erreur
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fields = {}  # nom_champ -> {widget, rules, required}
        self.errors = {}  # nom_champ -> message_erreur
        
    def add_field(self, name: str, widget: QWidget, required: bool = True, 
                  rules: Optional[Dict[str, Any]] = None):
        """Ajoute un champ à valider
        
        Args:
            name: Nom unique du champ
            widget: Widget Qt à valider
            required: Si le champ est obligatoire
            rules: Règles de validation spécifiques
        """
        if rules is None:
            rules = {}
            
        self.fields[name] = {
            'widget': widget,
            'required': required,
            'rules': rules
        }
        
        # Connecter les signaux de changement
        self._connect_widget_signals(widget, name)
        
    def _connect_widget_signals(self, widget: QWidget, field_name: str):
        """Connecte les signaux de changement du widget"""
        if isinstance(widget, QLineEdit):
            widget.textChanged.connect(lambda: self._validate_field(field_name))
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.valueChanged.connect(lambda: self._validate_field(field_name))
        elif isinstance(widget, QComboBox):
            widget.currentTextChanged.connect(lambda: self._validate_field(field_name))
        elif isinstance(widget, QCheckBox):
            widget.stateChanged.connect(lambda: self._validate_field(field_name))
            
    def _validate_field(self, field_name: str) -> bool:
        """Valide un champ spécifique"""
        if field_name not in self.fields:
            return True
            
        field_info = self.fields[field_name]
        widget = field_info['widget']
        required = field_info['required']
        rules = field_info['rules']
        
        # Obtenir la valeur du widget
        value = self._get_widget_value(widget)
        
        # Vérifier si le champ est requis et vide
        if required and self._is_empty_value(value):
            error_msg = f"Le champ '{field_name}' est obligatoire"
            self._set_field_error(field_name, error_msg, widget)
            return False
            
        # Appliquer les règles de validation
        error_msg = self._apply_validation_rules(value, rules)
        if error_msg:
            self._set_field_error(field_name, error_msg, widget)
            return False
            
        # Champ valide
        self._clear_field_error(field_name, widget)
        return True
        
    def _get_widget_value(self, widget: QWidget) -> Any:
        """Obtient la valeur d'un widget"""
        if isinstance(widget, QLineEdit):
            return widget.text().strip()
        elif isinstance(widget, QSpinBox):
            return widget.value()
        elif isinstance(widget, QDoubleSpinBox):
            return widget.value()
        elif isinstance(widget, QComboBox):
            return widget.currentText().strip()
        elif isinstance(widget, QCheckBox):
            return widget.isChecked()
        else:
            return None
            
    def _is_empty_value(self, value: Any) -> bool:
        """Vérifie si une valeur est considérée comme vide"""
        if value is None:
            return True
        if isinstance(value, str):
            return len(value) == 0
        if isinstance(value, (int, float)):
            return False  # Les nombres ne sont jamais "vides"
        if isinstance(value, bool):
            return False  # Les booléens ne sont jamais "vides"
        return False
        
    def _apply_validation_rules(self, value: Any, rules: Dict[str, Any]) -> Optional[str]:
        """Applique les règles de validation"""
        # Règle: longueur minimale
        if 'min_length' in rules and isinstance(value, str):
            if len(value) < rules['min_length']:
                return f"Minimum {rules['min_length']} caractères requis"
                
        # Règle: longueur maximale
        if 'max_length' in rules and isinstance(value, str):
            if len(value) > rules['max_length']:
                return f"Maximum {rules['max_length']} caractères autorisés"
                
        # Règle: valeur minimale
        if 'min_value' in rules and isinstance(value, (int, float)):
            if value < rules['min_value']:
                return f"Valeur minimale: {rules['min_value']}"
                
        # Règle: valeur maximale
        if 'max_value' in rules and isinstance(value, (int, float)):
            if value > rules['max_value']:
                return f"Valeur maximale: {rules['max_value']}"
                
        # Règle: expression régulière
        if 'regex' in rules and isinstance(value, str):
            import re
            if not re.match(rules['regex'], value):
                return rules.get('regex_error', "Format invalide")
                
        # Règle: valeurs autorisées
        if 'allowed_values' in rules:
            if value not in rules['allowed_values']:
                return f"Valeur autorisée: {', '.join(map(str, rules['allowed_values']))}"
                
        # Règle: validation personnalisée
        if 'custom_validator' in rules:
            validator_func = rules['custom_validator']
            try:
                result = validator_func(value)
                if result is not True:
                    return str(result) if result else "Valeur invalide"
            except Exception as e:
                return f"Erreur de validation: {str(e)}"
                
        return None
        
    def _set_field_error(self, field_name: str, error_msg: str, widget: QWidget):
        """Marque un champ comme ayant une erreur"""
        self.errors[field_name] = error_msg
        
        # Appliquer le style d'erreur
        widget.setStyleSheet("""
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                border: 2px solid #e74c3c;
                background-color: #fdf2f2;
            }
        """)
        
        # Définir le tooltip d'erreur
        widget.setToolTip(f"❌ {error_msg}")
        
        # Émettre le signal d'erreur
        self.fieldError.emit(field_name, error_msg)
        self._check_overall_validity()
        
    def _clear_field_error(self, field_name: str, widget: QWidget):
        """Efface l'erreur d'un champ"""
        if field_name in self.errors:
            del self.errors[field_name]
            
        # Effacer le style d'erreur
        widget.setStyleSheet("""
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                border: 2px solid #27ae60;
                background-color: #f8fff8;
            }
        """)
        
        # Définir le tooltip de succès
        widget.setToolTip("✅ Valeur valide")
        
        self._check_overall_validity()
        
    def _check_overall_validity(self):
        """Vérifie la validité globale et émet le signal"""
        is_valid = len(self.errors) == 0
        self.validationChanged.emit(is_valid)
        
    def validate_all(self) -> Tuple[bool, List[str]]:
        """Valide tous les champs
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        self.errors.clear()
        
        for field_name in self.fields:
            self._validate_field(field_name)
            
        error_messages = list(self.errors.values())
        is_valid = len(error_messages) == 0
        
        return is_valid, error_messages
        
    def get_field_values(self) -> Dict[str, Any]:
        """Obtient toutes les valeurs des champs"""
        values = {}
        for field_name, field_info in self.fields.items():
            widget = field_info['widget']
            values[field_name] = self._get_widget_value(widget)
        return values
        
    def set_field_value(self, field_name: str, value: Any):
        """Définit la valeur d'un champ"""
        if field_name not in self.fields:
            return
            
        widget = self.fields[field_name]['widget']
        
        if isinstance(widget, QLineEdit):
            widget.setText(str(value))
        elif isinstance(widget, QSpinBox):
            widget.setValue(int(value))
        elif isinstance(widget, QDoubleSpinBox):
            widget.setValue(float(value))
        elif isinstance(widget, QComboBox):
            index = widget.findText(str(value))
            if index >= 0:
                widget.setCurrentIndex(index)
        elif isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))
            
    def clear_all_errors(self):
        """Efface toutes les erreurs"""
        for field_name, field_info in self.fields.items():
            widget = field_info['widget']
            widget.setStyleSheet("")
            widget.setToolTip("")
            
        self.errors.clear()
        self.validationChanged.emit(True)
        
    def get_validation_summary(self) -> str:
        """Obtient un résumé de la validation"""
        if not self.errors:
            return "✅ Tous les champs sont valides"
            
        summary = f"❌ {len(self.errors)} erreur(s) détectée(s):\n"
        for field_name, error_msg in self.errors.items():
            summary += f"• {field_name}: {error_msg}\n"
            
        return summary.strip()


class CalibrationValidator(FieldValidator):
    """Validateur spécialisé pour la calibration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def setup_calibration_fields(self, widgets: Dict[str, QWidget]):
        """Configure les champs de calibration avec leurs règles"""
        
        # Nombre de sondes
        if 'n_sondes' in widgets:
            self.add_field('n_sondes', widgets['n_sondes'], True, {
                'min_value': 1,
                'max_value': 16
            })
            
        # Fréquence d'échantillonnage
        if 'frequency' in widgets:
            self.add_field('frequency', widgets['frequency'], True, {
                'min_value': 0.1,
                'max_value': 1000.0
            })
            
        # Durée d'acquisition
        if 'duration' in widgets:
            self.add_field('duration', widgets['duration'], True, {
                'min_value': 1,
                'max_value': 3600
            })
            
        # Dossier de sauvegarde
        if 'save_folder' in widgets:
            self.add_field('save_folder', widgets['save_folder'], True, {
                'min_length': 1,
                'custom_validator': self._validate_folder_path
            })
            
        # Noms des sondes
        for i in range(16):  # Maximum 16 sondes
            sonde_key = f'sonde_name_{i}'
            if sonde_key in widgets:
                self.add_field(sonde_key, widgets[sonde_key], False, {
                    'min_length': 1,
                    'max_length': 50,
                    'regex': r'^[a-zA-Z0-9_\-\s]+$',
                    'regex_error': 'Seuls les lettres, chiffres, tirets et espaces sont autorisés'
                })
                
    def _validate_folder_path(self, path: str) -> bool:
        """Valide un chemin de dossier"""
        import os
        try:
            # Vérifier si le chemin parent existe
            parent_dir = os.path.dirname(path)
            if parent_dir and not os.path.exists(parent_dir):
                return "Le dossier parent n'existe pas"
                
            # Vérifier les caractères invalides
            invalid_chars = '<>:"|?*'
            if any(char in path for char in invalid_chars):
                return "Caractères invalides dans le chemin"
                
            return True
        except Exception:
            return "Chemin invalide"


class AcquisitionValidator(FieldValidator):
    """Validateur spécialisé pour l'acquisition"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def setup_acquisition_fields(self, widgets: Dict[str, QWidget]):
        """Configure les champs d'acquisition avec leurs règles"""
        
        # Fréquence d'échantillonnage
        if 'sample_rate' in widgets:
            self.add_field('sample_rate', widgets['sample_rate'], True, {
                'min_value': 0.1,
                'max_value': 10000.0
            })
            
        # Nombre de canaux
        if 'n_channels' in widgets:
            self.add_field('n_channels', widgets['n_channels'], True, {
                'min_value': 1,
                'max_value': 16
            })
            
        # Taille du buffer
        if 'buffer_size' in widgets:
            self.add_field('buffer_size', widgets['buffer_size'], True, {
                'min_value': 1000,
                'max_value': 1000000
            })
            
        # Durée d'acquisition (optionnelle)
        if 'duration' in widgets:
            self.add_field('duration', widgets['duration'], False, {
                'min_value': 1,
                'max_value': 86400  # 24 heures max
            })
            
        # Mode d'acquisition
        if 'mode' in widgets:
            self.add_field('mode', widgets['mode'], True, {
                'allowed_values': ['simulate', 'ni', 'iotech', 'arduino']
            })
            
        # Intervalle de mise à jour
        if 'update_interval' in widgets:
            self.add_field('update_interval', widgets['update_interval'], True, {
                'min_value': 10,
                'max_value': 1000
            })