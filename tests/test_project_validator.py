# -*- coding: utf-8 -*-
"""
Tests pour le module de validation de projet CHNeoWave
"""

import pytest
from pathlib import Path
from hrneowave.core.validators import (
    ProjectValidator, 
    AcquisitionValidator, 
    FileValidator,
    ValidationLevel, 
    ValidationResult
)

class TestProjectValidator:
    """Tests pour ProjectValidator"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.validator = ProjectValidator()
        
    def test_validate_project_name_valid(self):
        """Test validation nom de projet valide"""
        valid_names = [
            "Projet_Test_2024",
            "Etude-Maritime-01",
            "CHNeoWave_Calibration",
            "Test123"
        ]
        
        for name in valid_names:
            result = self.validator.validate_project_name(name)
            assert result.is_valid, f"Le nom '{name}' devrait être valide"
            assert result.level == ValidationLevel.INFO
            
    def test_validate_project_name_invalid(self):
        """Test validation nom de projet invalide"""
        invalid_names = [
            "",  # Vide
            "a",  # Trop court
            "a" * 101,  # Trop long
            "Projet/Test",  # Caractère interdit
            "Projet<Test>",  # Caractères interdits
            "CON",  # Nom réservé Windows
            "aux.txt",  # Extension interdite
        ]
        
        for name in invalid_names:
            result = self.validator.validate_project_name(name)
            assert not result.is_valid, f"Le nom '{name}' devrait être invalide"
            assert result.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL]
            
    def test_validate_chief_name_valid(self):
        """Test validation nom de chef valide"""
        valid_names = [
            "Jean Dupont",
            "Marie-Claire Martin",
            "Dr. Pierre Durand",
            "Prof. Anne-Sophie Leblanc"
        ]
        
        for name in valid_names:
            result = self.validator.validate_chief_name(name)
            assert result.is_valid, f"Le nom '{name}' devrait être valide"
            
    def test_validate_chief_name_invalid(self):
        """Test validation nom de chef invalide"""
        invalid_names = [
            "",  # Vide
            "A",  # Trop court
            "123",  # Que des chiffres
            "Jean@Dupont",  # Caractère interdit
            "a" * 101,  # Trop long
        ]
        
        for name in invalid_names:
            result = self.validator.validate_chief_name(name)
            assert not result.is_valid, f"Le nom '{name}' devrait être invalide"
            
    def test_validate_laboratory_valid(self):
        """Test validation laboratoire valide"""
        valid_labs = [
            "Laboratoire d'Études Maritimes",
            "LEM - Université de Marseille",
            "IFREMER Brest",
            "Centre de Recherche Océanographique"
        ]
        
        for lab in valid_labs:
            result = self.validator.validate_laboratory(lab)
            assert result.is_valid, f"Le laboratoire '{lab}' devrait être valide"
            
    def test_validate_laboratory_invalid(self):
        """Test validation laboratoire invalide"""
        invalid_labs = [
            "",  # Vide
            "AB",  # Trop court
            "a" * 201,  # Trop long
            "Lab<script>",  # Caractères dangereux
        ]
        
        for lab in invalid_labs:
            result = self.validator.validate_laboratory(lab)
            assert not result.is_valid, f"Le laboratoire '{lab}' devrait être invalide"
            
    def test_validate_description_valid(self):
        """Test validation description valide"""
        valid_descriptions = [
            "Étude des vagues en bassin d'essai",
            "Calibration des capteurs de houle pour modèle réduit",
            "Analyse spectrale des signaux de vagues irrégulières",
            "Test de résistance des structures offshore"
        ]
        
        for desc in valid_descriptions:
            result = self.validator.validate_description(desc)
            assert result.is_valid, f"La description '{desc}' devrait être valide"
            
    def test_validate_description_invalid(self):
        """Test validation description invalide"""
        invalid_descriptions = [
            "",  # Vide
            "Test",  # Trop court
            "a" * 1001,  # Trop long
            "Description<script>alert('hack')</script>",  # Code malveillant
        ]
        
        for desc in invalid_descriptions:
            result = self.validator.validate_description(desc)
            assert not result.is_valid, f"La description '{desc}' devrait être invalide"
            
    def test_validate_project_data_complete(self):
        """Test validation complète d'un projet valide"""
        project_data = {
            'project_name': 'Etude_Houle_2024',
            'project_manager': 'Dr. Jean Dupont',
            'laboratory': 'Laboratoire d\'Études Maritimes',
            'description': 'Étude complète des caractéristiques de houle en bassin d\'essai pour validation de modèles numériques'
        }
        
        results = self.validator.validate_project_data(project_data)
        
        # Tous les champs doivent être valides
        for field, result in results.items():
            assert result.is_valid, f"Le champ '{field}' devrait être valide: {result.message}"
            
    def test_validate_project_data_incomplete(self):
        """Test validation avec données incomplètes"""
        project_data = {
            'project_name': '',  # Invalide
            'project_manager': 'Dr. Jean Dupont',
            'laboratory': '',  # Invalide
            'description': 'Test'  # Trop court
        }
        
        results = self.validator.validate_project_data(project_data)
        
        # Vérifier que les champs invalides sont détectés
        assert not results['project_name'].is_valid
        assert results['project_manager'].is_valid
        assert not results['laboratory'].is_valid
        assert not results['description'].is_valid
        
    def test_validate_all_legacy_method(self):
        """Test de la méthode validate_all (compatibilité)"""
        project_data = {
            'name': 'Projet_Test',
            'chief': 'Dr. Marie Martin',
            'laboratory': 'LEM Marseille',
            'description': 'Description complète du projet de test'
        }
        
        result = self.validator.validate_all(project_data)
        
        # validate_all retourne un seul ValidationResult, pas un dictionnaire
        assert result.is_valid, f"La validation globale devrait être valide: {result.message}"
        assert result.level in [ValidationLevel.INFO, ValidationLevel.WARNING]

class TestAcquisitionValidator:
    """Tests pour AcquisitionValidator"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.validator = AcquisitionValidator()
        
    def test_validate_sampling_frequency_valid(self):
        """Test validation fréquence d'échantillonnage valide"""
        valid_frequencies = [100, 500, 1000, 2000, 5000]
        
        for freq in valid_frequencies:
            result = self.validator.validate_sampling_frequency(freq)
            assert result.is_valid, f"La fréquence {freq} Hz devrait être valide"
            
    def test_validate_sampling_frequency_invalid(self):
        """Test validation fréquence d'échantillonnage invalide"""
        invalid_frequencies = [0, -100, 50, 15000, 50000]
        
        for freq in invalid_frequencies:
            result = self.validator.validate_sampling_frequency(freq)
            assert not result.is_valid, f"La fréquence {freq} Hz devrait être invalide"
            
    def test_validate_duration_valid(self):
        """Test validation durée valide"""
        valid_durations = [10, 30, 60, 300, 600]
        
        for duration in valid_durations:
            result = self.validator.validate_duration(duration)
            assert result.is_valid, f"La durée {duration}s devrait être valide"
            
    def test_validate_duration_invalid(self):
        """Test validation durée invalide"""
        invalid_durations = [0, -10, 4, 3700]  # Trop court ou trop long
        
        for duration in invalid_durations:
            result = self.validator.validate_duration(duration)
            assert not result.is_valid, f"La durée {duration}s devrait être invalide"
            
    def test_validate_acquisition_params_complete(self):
        """Test validation complète des paramètres d'acquisition"""
        params = {
            'sampling_frequency': 1000,
            'duration': 120,
            'channels': 4,
            'gain': 1.0
        }
        
        results = self.validator.validate_acquisition_params(params)
        
        # Les paramètres obligatoires doivent être valides
        assert results['sampling_frequency'].is_valid
        assert results['duration'].is_valid

class TestFileValidator:
    """Tests pour FileValidator"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        self.validator = FileValidator()
        
    def test_validate_file_path_valid(self):
        """Test validation chemin de fichier valide"""
        valid_paths = [
            "C:\\Projects\\test.hdf5",
            "./data/experiment.h5",
            "/home/user/data.txt",
            "relative/path/file.csv"
        ]
        
        for path in valid_paths:
            result = self.validator.validate_file_path(path)
            # Le chemin peut être valide même si le fichier n'existe pas
            assert result.level in [ValidationLevel.INFO, ValidationLevel.WARNING]
            
    def test_validate_file_path_invalid(self):
        """Test validation chemin de fichier invalide"""
        invalid_paths = [
            "",  # Vide
            "file<name>.txt",  # Caractères interdits
            "CON.txt",  # Nom réservé
            "file|name.txt",  # Caractère interdit
        ]
        
        for path in invalid_paths:
            result = self.validator.validate_file_path(path)
            assert not result.is_valid, f"Le chemin '{path}' devrait être invalide"
            
    def test_validate_extension_valid(self):
        """Test validation extension valide"""
        valid_extensions = [
            (".hdf5", ['.hdf5', '.h5']),
            (".h5", ['.hdf5', '.h5']),
            (".txt", ['.txt', '.csv']),
            (".csv", ['.txt', '.csv'])
        ]
        
        for ext, allowed in valid_extensions:
            result = self.validator.validate_extension("test" + ext, allowed)
            assert result.is_valid, f"L'extension '{ext}' devrait être valide"
            
    def test_validate_extension_invalid(self):
        """Test validation extension invalide"""
        invalid_cases = [
            (".exe", ['.hdf5', '.h5']),
            (".bat", ['.txt', '.csv']),
            (".pdf", ['.hdf5']),
            ("", ['.txt'])  # Pas d'extension
        ]
        
        for ext, allowed in invalid_cases:
            result = self.validator.validate_extension("test" + ext, allowed)
            assert not result.is_valid, f"L'extension '{ext}' devrait être invalide pour {allowed}"

class TestValidationResult:
    """Tests pour ValidationResult"""
    
    def test_validation_result_creation(self):
        """Test création d'un ValidationResult"""
        result = ValidationResult(
            is_valid=True,
            level=ValidationLevel.INFO,
            message="Test réussi",
            field="test_field",
            suggestions=["Suggestion 1", "Suggestion 2"]
        )
        
        assert result.is_valid
        assert result.level == ValidationLevel.INFO
        assert result.message == "Test réussi"
        assert result.field == "test_field"
        assert len(result.suggestions) == 2
        
    def test_validation_result_to_dict(self):
        """Test conversion en dictionnaire"""
        result = ValidationResult(
            is_valid=False,
            level=ValidationLevel.ERROR,
            message="Erreur de validation",
            field="error_field"
        )
        
        result_dict = result.to_dict()
        
        assert result_dict['is_valid'] == False
        assert result_dict['level'] == 'ERROR'
        assert result_dict['message'] == "Erreur de validation"
        assert result_dict['field'] == "error_field"
        assert 'suggestions' in result_dict

class TestValidationIntegration:
    """Tests d'intégration pour la validation"""
    
    def test_complete_project_validation_workflow(self):
        """Test du workflow complet de validation d'un projet"""
        # Données de projet complètes et valides
        project_data = {
            'project_name': 'Etude_Houle_Mediterranee_2024',
            'project_manager': 'Dr. Sophie Martineau',
            'laboratory': 'Laboratoire d\'Études Maritimes - Université de Marseille',
            'description': 'Étude expérimentale des caractéristiques de houle en Méditerranée '
                          'avec modèles réduits en bassin d\'essai. Analyse spectrale et '
                          'validation de modèles numériques de propagation des vagues.'
        }
        
        # Paramètres d'acquisition
        acquisition_params = {
            'sampling_frequency': 1000,
            'duration': 300,
            'channels': 8,
            'gain': 2.0
        }
        
        # Validation du projet
        project_validator = ProjectValidator()
        project_results = project_validator.validate_project_data(project_data)
        
        # Validation de l'acquisition
        acquisition_validator = AcquisitionValidator()
        acquisition_results = acquisition_validator.validate_acquisition_params(acquisition_params)
        
        # Vérifier que tout est valide
        for field, result in project_results.items():
            assert result.is_valid, f"Validation projet échouée pour {field}: {result.message}"
            
        for field, result in acquisition_results.items():
            assert result.is_valid, f"Validation acquisition échouée pour {field}: {result.message}"
            
        # Vérifier les suggestions pour améliorer la qualité
        for field, result in project_results.items():
            if result.suggestions:
                print(f"Suggestions pour {field}: {result.suggestions}")
                
    def test_validation_error_handling(self):
        """Test gestion des erreurs de validation"""
        validator = ProjectValidator()
        
        # Test avec données None
        result = validator.validate_project_name(None)
        assert not result.is_valid
        assert result.level == ValidationLevel.CRITICAL
        
        # Test avec type incorrect
        result = validator.validate_project_name(123)
        assert not result.is_valid
        
    def test_validation_performance(self):
        """Test performance de la validation"""
        import time
        
        validator = ProjectValidator()
        project_data = {
            'project_name': 'Test_Performance',
            'project_manager': 'Test User',
            'laboratory': 'Test Lab',
            'description': 'Test de performance de validation'
        }
        
        # Mesurer le temps de validation
        start_time = time.time()
        
        # Effectuer 100 validations
        for _ in range(100):
            results = validator.validate_project_data(project_data)
            
        end_time = time.time()
        elapsed = end_time - start_time
        
        # La validation devrait être rapide (moins de 1 seconde pour 100 validations)
        assert elapsed < 1.0, f"Validation trop lente: {elapsed:.3f}s pour 100 validations"
        
        print(f"Performance validation: {elapsed:.3f}s pour 100 validations")

if __name__ == '__main__':
    # Exécuter les tests si le script est lancé directement
    pytest.main([__file__, '-v'])