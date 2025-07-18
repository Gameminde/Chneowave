
import subprocess
import pytest

def test_cli_help_commands():
    """Test que toutes les commandes CLI affichent l'aide"""
    commands = [
        'hr-complete-guide',
        'hr-lab-config', 
        'hr-quick-start',
        'hr-final-validate',
        'hr-deploy',
        'hr-update-manager'
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--help'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            assert result.returncode == 0, f"{cmd} --help failed"
        except FileNotFoundError:
            pytest.skip(f"Command {cmd} not installed")
