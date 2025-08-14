# Script PowerShell pour installer les dépendances CHNeoWave
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation des dépendances CHNeoWave" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nVérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERREUR: Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python depuis python.org ou Microsoft Store" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour continuer"
    exit 1
}

Write-Host "`nCréation de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Suppression de l'ancien environnement virtuel..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}
python -m venv venv

Write-Host "`nActivation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host "`nMise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "`nInstallation des dépendances principales..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`nInstallation des dépendances de développement..." -ForegroundColor Yellow
pip install -r requirements-dev.txt

Write-Host "`nInstallation du projet en mode développement..." -ForegroundColor Yellow
pip install -e .

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Installation terminée avec succès!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nPour activer l'environnement virtuel:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White

Write-Host "`nPour lancer CHNeoWave:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor White

Read-Host "`nAppuyez sur Entrée pour continuer"
