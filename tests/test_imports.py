def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        # Core modules
        from mediterrania_orchestrator.core.orchestrator import OrchestratoreAlimentare
        from mediterrania_orchestrator.core.nutritional_verifier import VerificatoreNutrizionale
        from mediterrania_orchestrator.core.substitution_handler import GestoreSostituzioni
        
        # Database
        from mediterrania_orchestrator.database.database_handler import DatabaseRicette
        
        # Utils
        from mediterrania_orchestrator.utils.logger import LoggerMediterranIA
        
        print("All imports successful!")
        return True
    except ImportError as e:
        print(f"Import error: {str(e)}")
        return False

if __name__ == "__main__":
    test_imports()