# -*- coding: utf-8 -*-
"""
Tests pour le module de gestion d'erreurs CHNeoWave
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from hrneowave.core.error_handler import (
    ErrorSeverity,
    ErrorCategory,
    ErrorContext,
    CHNeoWaveError,
    ErrorHandler,
    get_error_handler,
    handle_errors
)

class TestErrorSeverity:
    """Tests pour ErrorSeverity"""
    
    def test_error_severity_values(self):
        """Test des valeurs de sévérité"""
        assert ErrorSeverity.LOW.value == "low"
        assert ErrorSeverity.MEDIUM.value == "medium"
        assert ErrorSeverity.HIGH.value == "high"
        assert ErrorSeverity.CRITICAL.value == "critical"
        
    def test_error_severity_comparison(self):
        """Test comparaison des sévérités"""
        assert ErrorSeverity.LOW < ErrorSeverity.MEDIUM
        assert ErrorSeverity.MEDIUM < ErrorSeverity.HIGH
        assert ErrorSeverity.HIGH < ErrorSeverity.CRITICAL
        
    def test_error_severity_string(self):
        """Test représentation string"""
        assert str(ErrorSeverity.LOW) == "ErrorSeverity.LOW"
        assert str(ErrorSeverity.CRITICAL) == "ErrorSeverity.CRITICAL"

class TestErrorCategory:
    """Tests pour ErrorCategory"""
    
    def test_error_category_values(self):
        """Test des catégories d'erreur"""
        categories = [
            ErrorCategory.SYSTEM,
            ErrorCategory.HARDWARE,
            ErrorCategory.PROCESSING,
            ErrorCategory.USER_INPUT,
            ErrorCategory.NETWORK,
            ErrorCategory.USER_INPUT,
            ErrorCategory.UNKNOWN
        ]
        
        for category in categories:
            assert isinstance(category.value, str)
            assert len(category.value) > 0

class TestErrorContext:
    """Tests pour ErrorContext"""
    
    def test_error_context_creation(self):
        """Test création d'un contexte d'erreur"""
        context = ErrorContext(
            operation="test_operation",
            component="test_component",
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.HIGH,
            user_data={"action": "Test action", "data": {"cpu": 50, "memory": 75}}
        )
        
        assert context.operation == "test_operation"
        assert context.component == "test_component"
        assert context.category == ErrorCategory.SYSTEM
        assert context.severity == ErrorSeverity.HIGH
        assert context.user_data["data"]["cpu"] == 50
        
    def test_error_context_to_dict(self):
        """Test conversion en dictionnaire"""
        context = ErrorContext(
            operation="test_operation",
            component="test_component"
        )
        
        context_dict = context.to_dict()
        
        assert context_dict["operation"] == "test_operation"
        assert context_dict["component"] == "test_component"
        assert "timestamp" in context_dict
        
    def test_error_context_from_dict(self):
        """Test création depuis dictionnaire"""
        data = {
            "operation": "test_operation",
            "component": "test_component",
            "category": "system",
            "severity": "high",
            "timestamp": "2024-01-01T12:00:00"
        }
        
        context = ErrorContext.from_dict(data)
        
        assert context.operation == "test_operation"
        assert context.component == "test_component"
        assert context.category == ErrorCategory.SYSTEM
        assert context.severity == ErrorSeverity.HIGH

class TestCHNeoWaveError:
    """Tests pour CHNeoWaveError"""
    
    def test_chneowave_error_creation(self):
        """Test création d'une exception CHNeoWave"""
        context = ErrorContext(operation="test", component="test_func")
        
        error = CHNeoWaveError(
            message="Test error",
            context=context,
            user_message="User friendly message"
        )
        
        assert str(error) == "Test error"
        assert error.context == context
        assert error.user_message == "User friendly message"
        assert error.error_id.startswith("CHN_")
        
    def test_chneowave_error_without_context(self):
        """Test création sans contexte"""
        error = CHNeoWaveError(
            message="Simple error"
        )
        
        assert str(error) == "Simple error"
        assert error.context is None
        assert error.user_message is None
        assert error.error_id.startswith("CHN_")

class TestErrorHandler:
    """Tests pour ErrorHandler"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        # Réinitialiser le singleton ErrorHandler
        if hasattr(ErrorHandler, '_instance'):
            ErrorHandler._instance = None
        
        # Réinitialiser le gestionnaire global
        import hrneowave.core.error_handler as eh
        eh._global_error_handler = None
        
        # Créer un répertoire temporaire pour les logs
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = Path(self.temp_dir) / "test_errors.log"
        
        # Obtenir le gestionnaire d'erreurs singleton
        self.error_handler = get_error_handler()
        self.error_handler.error_log_file = self.log_file
        self.error_handler.clear_error_history()
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        # Nettoyer les fichiers temporaires
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_error_handler_initialization(self):
        """Test initialisation du gestionnaire d'erreurs"""
        assert self.error_handler.error_log_file == self.log_file
        assert len(self.error_handler.error_history) == 0
        assert self.error_handler.logger is not None
        
    def test_log_error_basic(self):
        """Test journalisation d'erreur basique"""
        error = Exception("Test error")
        context = ErrorContext(
            operation="test",
            component="test_component",
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.HIGH
        )
        
        self.error_handler.handle_error(error, context)
        
        # Vérifier que l'erreur est dans l'historique
        assert len(self.error_handler.error_history) == 1
        logged_error = self.error_handler.error_history[0]
        assert "Test error" in logged_error["exception_message"]
        assert logged_error["context"]["category"] == ErrorCategory.SYSTEM.value
        assert logged_error["context"]["severity"] == ErrorSeverity.HIGH.value
        
    def test_log_error_with_context(self):
        """Test journalisation avec contexte"""
        context = ErrorContext(
            operation="test_operation",
            component="test_component",
            category=ErrorCategory.PROCESSING,
            user_data={"module": "test_module", "function": "test_function", "user_action": "Testing"}
        )
        
        error = Exception("Context error")
        
        self.error_handler.handle_error(error, context)
        
        logged_error = self.error_handler.error_history[0]
        assert "context" in logged_error
        assert logged_error["context"]["operation"] == "test_operation"
        assert logged_error["context"]["component"] == "test_component"
        
    def test_log_error_from_exception(self):
        """Test journalisation depuis une exception standard"""
        try:
            raise ValueError("Test exception")
        except Exception as e:
            context = ErrorContext(
                operation="test_exception",
                component="test_component",
                category=ErrorCategory.USER_INPUT,
                user_data={"module": "test", "function": "test_exception"}
            )
            self.error_handler.handle_error(e, context)
            
        assert len(self.error_handler.error_history) == 1
        logged_error = self.error_handler.error_history[0]
        assert "Test exception" in logged_error["exception_message"]
        assert logged_error["context"]["category"] == ErrorCategory.USER_INPUT.value
        
    def test_get_errors_by_category(self):
        """Test récupération d'erreurs par catégorie"""
        # Ajouter des erreurs de différentes catégories
        errors_data = [
            (Exception("System error"), ErrorContext(operation="test1", component="test", category=ErrorCategory.SYSTEM)),
            (Exception("Data error"), ErrorContext(operation="test2", component="test", category=ErrorCategory.PROCESSING)),
            (Exception("Another system error"), ErrorContext(operation="test3", component="test", category=ErrorCategory.SYSTEM))
        ]
        
        for error, context in errors_data:
            self.error_handler.handle_error(error, context)
            
        # Récupérer les erreurs système
        system_errors = self.error_handler.get_errors_by_category(ErrorCategory.SYSTEM.value)
        assert len(system_errors) == 2
        
        # Récupérer les erreurs de données
        data_errors = self.error_handler.get_errors_by_category(ErrorCategory.PROCESSING.value)
        assert len(data_errors) == 1
        
    def test_get_errors_by_severity(self):
        """Test récupération d'erreurs par sévérité"""
        errors_data = [
            (Exception("Low error"), ErrorContext(operation="test1", component="test", category=ErrorCategory.USER_INPUT, severity=ErrorSeverity.LOW)),
            (Exception("High error"), ErrorContext(operation="test2", component="test", category=ErrorCategory.SYSTEM, severity=ErrorSeverity.HIGH)),
            (Exception("Critical error"), ErrorContext(operation="test3", component="test", category=ErrorCategory.HARDWARE, severity=ErrorSeverity.CRITICAL))
        ]
        
        for error, context in errors_data:
            self.error_handler.handle_error(error, context)
            
        # Récupérer les erreurs critiques
        critical_errors = self.error_handler.get_errors_by_severity(ErrorSeverity.CRITICAL.value)
        assert len(critical_errors) == 1
        assert "Critical error" in critical_errors[0]["exception_message"]
        
    def test_get_recent_errors(self):
        """Test récupération des erreurs récentes"""
        # Ajouter plusieurs erreurs
        for i in range(10):
            error = Exception(f"Error {i}")
            context = ErrorContext(operation=f"test_{i}", component="test", category=ErrorCategory.SYSTEM)
            self.error_handler.handle_error(error, context)
            
        # Récupérer les 5 plus récentes
        recent_errors = self.error_handler.get_recent_errors(5)
        assert len(recent_errors) == 5
        
        # Vérifier l'ordre (plus récent à la fin)
        assert "Error 5" in recent_errors[0]["exception_message"]
        assert "Error 9" in recent_errors[4]["exception_message"]
        
    def test_clear_history(self):
        """Test nettoyage de l'historique"""
        # Ajouter des erreurs
        for i in range(5):
            error = Exception(f"Error {i}")
            context = ErrorContext(operation=f"test_{i}", component="test", category=ErrorCategory.SYSTEM)
            self.error_handler.handle_error(error, context)
            
        assert len(self.error_handler.error_history) == 5
        
        # Nettoyer l'historique
        self.error_handler.clear_error_history()
        assert len(self.error_handler.error_history) == 0
        
    def test_save_errors_to_file(self):
        """Test sauvegarde des erreurs dans un fichier"""
        # Ajouter des erreurs
        errors_data = [
            (Exception("Error 1"), ErrorContext(operation="test1", component="test", category=ErrorCategory.SYSTEM)),
            (Exception("Error 2"), ErrorContext(operation="test2", component="test", category=ErrorCategory.PROCESSING))
        ]
        
        for error, context in errors_data:
            self.error_handler.handle_error(error, context)
            
        # Sauvegarder dans un fichier
        save_file = Path(self.temp_dir) / "saved_errors.json"
        self.error_handler.save_errors_to_file(save_file)
        
        # Vérifier que le fichier existe et contient les données
        assert save_file.exists()
        
        saved_data = []
        with open(save_file, 'r', encoding='utf-8') as f:
            for line in f:
                saved_data.append(json.loads(line.strip()))
            
        assert len(saved_data) == 2
        assert "Error 1" in saved_data[0]["exception_message"]
        assert "Error 2" in saved_data[1]["exception_message"]
        
    def test_load_errors_from_file(self):
        """Test chargement des erreurs depuis un fichier"""
        # Créer un fichier d'erreurs
        error_data = [
            {
                "exception_message": "Loaded error 1",
                "context": {
                    "category": ErrorCategory.SYSTEM.value,
                    "severity": ErrorSeverity.HIGH.value,
                    "operation": "test1",
                    "component": "test"
                },
                "timestamp": datetime.now().isoformat()
            },
            {
                "exception_message": "Loaded error 2",
                "context": {
                    "category": ErrorCategory.PROCESSING.value,
                    "severity": ErrorSeverity.MEDIUM.value,
                    "operation": "test2",
                    "component": "test"
                },
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        load_file = Path(self.temp_dir) / "load_errors.json"
        with open(load_file, 'w', encoding='utf-8') as f:
            for error in error_data:
                json.dump(error, f, ensure_ascii=False, default=str)
                f.write('\n')
            
        # Charger les erreurs
        self.error_handler.load_errors_from_file(load_file)
        
        assert len(self.error_handler.error_history) == 2
        assert "Loaded error 1" in self.error_handler.error_history[0]["exception_message"]
        assert "Loaded error 2" in self.error_handler.error_history[1]["exception_message"]
        
    def test_error_statistics(self):
        """Test statistiques d'erreurs"""
        # Ajouter des erreurs variées
        errors_data = [
            (Exception("System 1"), ErrorContext(operation="test1", component="test", category=ErrorCategory.SYSTEM, severity=ErrorSeverity.HIGH)),
            (Exception("System 2"), ErrorContext(operation="test2", component="test", category=ErrorCategory.SYSTEM, severity=ErrorSeverity.LOW)),
            (Exception("Data 1"), ErrorContext(operation="test3", component="test", category=ErrorCategory.PROCESSING, severity=ErrorSeverity.CRITICAL)),
            (Exception("Hardware 1"), ErrorContext(operation="test4", component="test", category=ErrorCategory.HARDWARE, severity=ErrorSeverity.MEDIUM))
        ]
        
        for error, context in errors_data:
            self.error_handler.handle_error(error, context)
            
        stats = self.error_handler.get_error_statistics()
        
        # Vérifier les statistiques par catégorie
        assert stats["by_category"][ErrorCategory.SYSTEM.value] == 2
        assert stats["by_category"][ErrorCategory.PROCESSING.value] == 1
        assert stats["by_category"][ErrorCategory.HARDWARE.value] == 1
        
        # Vérifier les statistiques par sévérité
        assert stats["by_severity"][ErrorSeverity.CRITICAL.value] == 1
        assert stats["by_severity"][ErrorSeverity.HIGH.value] == 1
        assert stats["by_severity"][ErrorSeverity.MEDIUM.value] == 1
        assert stats["by_severity"][ErrorSeverity.LOW.value] == 1
        
        # Vérifier le total
        assert stats["total_errors"] == 4

class TestErrorHandlerSingleton:
    """Tests pour le singleton ErrorHandler"""
    
    def test_get_error_handler_singleton(self):
        """Test que get_error_handler retourne toujours la même instance"""
        handler1 = get_error_handler()
        handler2 = get_error_handler()
        
        assert handler1 is handler2
        
    def test_get_error_handler_with_config(self):
        """Test configuration du gestionnaire d'erreurs"""
        # get_error_handler ne prend pas de paramètres de configuration
        # Il retourne toujours la même instance singleton
        handler = get_error_handler()
        assert handler is not None
        assert hasattr(handler, 'error_log_file')
        assert hasattr(handler, 'max_error_history')

class TestHandleErrorsDecorator:
    """Tests pour le décorateur handle_errors"""
    
    def setup_method(self):
        """Initialisation avant chaque test"""
        # Réinitialiser le singleton pour les tests
        import hrneowave.core.error_handler as eh
        if hasattr(eh.ErrorHandler, '_instance'):
            eh.ErrorHandler._instance = None
        eh._global_error_handler = None
        
        # Créer une nouvelle instance et vider l'historique
        from hrneowave.core.error_handler import get_error_handler
        handler = get_error_handler()
        handler.clear_error_history()
        
    def test_handle_errors_decorator_success(self):
        """Test décorateur avec fonction qui réussit"""
        @handle_errors(operation="test_operation", component="test_component", category=ErrorCategory.SYSTEM)
        def successful_function(x, y):
            return x + y
            
        result = successful_function(2, 3)
        assert result == 5
        
    def test_handle_errors_decorator_exception(self):
        """Test décorateur avec fonction qui lève une exception"""
        @handle_errors(operation="test_operation", component="test_component", category=ErrorCategory.PROCESSING)
        def failing_function():
            raise ValueError("Test exception")
            
        # La fonction devrait lever l'exception après l'avoir loggée
        with pytest.raises(CHNeoWaveError):
            failing_function()
            
        # Vérifier que l'erreur a été loggée
        handler = get_error_handler()
        assert len(handler.error_history) == 1
        assert "Test exception" in handler.error_history[0]["exception_message"]
        
    def test_handle_errors_decorator_with_context(self):
        """Test décorateur avec contexte personnalisé"""
        @handle_errors(operation="test_operation", component="test_component", category=ErrorCategory.PROCESSING)
        def function_with_context():
            raise RuntimeError("Context test")
            
        with pytest.raises(CHNeoWaveError):
            function_with_context()
            
        # Vérifier le contexte dans l'erreur loggée
        handler = get_error_handler()
        logged_error = handler.error_history[0]
        assert logged_error["context"]["operation"] == "test_operation"
        assert logged_error["context"]["component"] == "test_component"
        
    def test_handle_errors_decorator_severity(self):
        """Test décorateur avec sévérité personnalisée"""
        @handle_errors(operation="test_operation", component="test_component", category=ErrorCategory.HARDWARE, severity=ErrorSeverity.CRITICAL)
        def critical_function():
            raise Exception("Critical error")
            
        with pytest.raises(CHNeoWaveError):
            critical_function()
            
        handler = get_error_handler()
        logged_error = handler.error_history[0]
        assert logged_error["context"]["severity"] == ErrorSeverity.CRITICAL.value
        
    def test_handle_errors_decorator_no_raise(self):
        """Test décorateur avec gestion d'exception"""
        @handle_errors(operation="test_operation", component="test_component", category=ErrorCategory.USER_INPUT)
        def silent_function():
            raise ValueError("Silent error")
            return "Should not reach here"
            
        # Le décorateur re-lève maintenant toujours l'exception
        with pytest.raises(CHNeoWaveError):
            silent_function()
        
        # Vérifier que l'erreur a été loggée
        handler = get_error_handler()
        assert len(handler.error_history) == 1
        
    def test_handle_errors_decorator_show_dialog(self):
        """Test décorateur avec gestion d'erreur"""
        @handle_errors(operation="test_operation", component="test_component", category=ErrorCategory.SYSTEM)
        def dialog_function():
            raise Exception("Dialog error")
            
        with pytest.raises(CHNeoWaveError):
            dialog_function()
            
        # Vérifier que l'erreur a été loggée
        handler = get_error_handler()
        assert len(handler.error_history) >= 1

class TestErrorHandlerIntegration:
    """Tests d'intégration pour le gestionnaire d'erreurs"""
    
    def test_complete_error_workflow(self):
        """Test workflow complet de gestion d'erreur"""
        # Réinitialiser le singleton
        if hasattr(ErrorHandler, '_instance'):
            ErrorHandler._instance = None
        
        # Créer un gestionnaire temporaire
        temp_dir = tempfile.mkdtemp()
        log_file = Path(temp_dir) / "integration_test.log"
        
        try:
            handler = get_error_handler()
            handler.error_log_file = log_file
            handler.clear_error_history()
            
            # Créer un contexte riche
            context = ErrorContext(
                operation="test_complete_workflow",
                component="integration_test",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                user_data={"memory_usage": 75, "cpu_usage": 45}
            )
            
            # Logger une erreur
            handler.handle_error(Exception("Integration test error"), context)
            
            # Vérifier la journalisation
            assert len(handler.error_history) == 1
            
            # Sauvegarder et recharger
            save_file = Path(temp_dir) / "saved_integration.json"
            handler.save_errors_to_file(str(save_file))
            
            # Vider l'historique et recharger
            handler.clear_error_history()
            handler.load_errors_from_file(str(save_file))
            
            assert len(handler.error_history) == 1
            loaded_error = handler.error_history[0]
            assert loaded_error["exception_message"] == "Integration test error"
            assert loaded_error["context"]["component"] == "integration_test"
            
            # Vérifier les statistiques
            stats = handler.get_error_statistics()
            assert stats["total_errors"] == 1
            assert stats["by_category"][ErrorCategory.SYSTEM.value] == 1
            
        finally:
            # Nettoyer
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    def test_error_handler_performance(self):
        """Test performance du gestionnaire d'erreurs"""
        import time
        
        # Utiliser le singleton et vider l'historique
        handler = get_error_handler()
        handler.clear_error_history()
        
        # Mesurer le temps pour logger 100 erreurs (réduit pour la performance)
        start_time = time.time()
        
        for i in range(100):
            context = ErrorContext(
                operation=f"performance_test_{i}",
                component="performance_test",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.LOW
            )
            handler.handle_error(Exception(f"Performance test error {i}"), context)
            
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Le logging devrait être rapide (moins de 1 seconde pour 100 erreurs)
        assert elapsed < 1.0, f"Logging trop lent: {elapsed:.3f}s pour 100 erreurs"
        
        print(f"Performance logging: {elapsed:.3f}s pour 100 erreurs")
        
        # Vérifier que toutes les erreurs sont présentes
        assert len(handler.error_history) == 100

if __name__ == '__main__':
    # Exécuter les tests si le script est lancé directement
    pytest.main([__file__, '-v'])