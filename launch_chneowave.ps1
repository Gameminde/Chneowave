# CHNeoWave - Script de lancement PowerShell
# Logiciel d'etude maritime - Modeles reduits
# Laboratoire Mediterraneen - Bassins et canaux

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    CHNeoWave - Logiciel d'etude maritime" -ForegroundColor Yellow
Write-Host "    Laboratoire de modeles reduits" -ForegroundColor Yellow
Write-Host "    Mediterranee - Bassins et canaux" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obtenir le repertoire du script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppDir = Join-Path $ScriptDir "logciel hrneowave"
$VenvPython = Join-Path $ScriptDir "venv\Scripts\python.exe"

Write-Host "Verification de l'environnement..." -ForegroundColor Green

# Verifier que le repertoire de l'application existe
if (-not (Test-Path $AppDir)) {
    Write-Host "ERREUR: Repertoire de l'application non trouve!" -ForegroundColor Red
    Write-Host "Chemin attendu: $AppDir" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

# Verifier que l'environnement virtuel existe
if (-not (Test-Path $VenvPython)) {
    Write-Host "ERREUR: Environnement virtuel non trouve!" -ForegroundColor Red
    Write-Host "Chemin attendu: $VenvPython" -ForegroundColor Yellow
    Write-Host "Veuillez d'abord installer les dependances avec:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Cyan
    Write-Host "  venv\Scripts\pip install -r requirements.txt" -ForegroundColor Cyan
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

# Verifier PyQt5
Write-Host "Test de PyQt5..." -ForegroundColor Green
$TestResult = & $VenvPython -c "import PyQt5; print('PyQt5 OK')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: PyQt5 non disponible!" -ForegroundColor Red
    Write-Host "Installation de PyQt5..." -ForegroundColor Yellow
    & (Join-Path $ScriptDir "venv\Scripts\pip.exe") install PyQt5
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Echec de l'installation de PyQt5" -ForegroundColor Red
        Read-Host "Appuyez sur Entree pour quitter"
        exit 1
    }
} else {
    Write-Host "PyQt5 disponible" -ForegroundColor Green
}

# Changer vers le repertoire de l'application
Set-Location $AppDir

Write-Host ""
Write-Host "Lancement de l'interface graphique CHNeoWave..." -ForegroundColor Green
Write-Host "Repertoire: $AppDir" -ForegroundColor Gray
Write-Host "Python: $VenvPython" -ForegroundColor Gray
Write-Host ""

# Lancer l'application
& $VenvPython "main.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERREUR: Echec du lancement de l'application (code: $LASTEXITCODE)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solutions possibles:" -ForegroundColor Yellow
    Write-Host "1. Verifiez les dependances: venv\Scripts\pip list" -ForegroundColor Cyan
    Write-Host "2. Testez le module: venv\Scripts\python -c 'import hrneowave'" -ForegroundColor Cyan
    Write-Host "3. Lancez la demo: venv\Scripts\python demo_chneowave.py" -ForegroundColor Cyan
    Write-Host "4. Consultez les logs d'erreur ci-dessus" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
} else {
    Write-Host ""
    Write-Host "Application fermee normalement." -ForegroundColor Green
}