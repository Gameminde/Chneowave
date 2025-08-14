# Script de validation des corrections MCP
Write-Host "🔍 Validation des corrections MCP Windsurf..." -ForegroundColor Green

# Test 1: Vérifier la jonction Windsurf
Write-Host "`n1. Vérification de la jonction Windsurf..." -ForegroundColor Yellow
$windsurfPath = "C:\Users\youcef cheriet\AppData\Local\Programs\Windsurf\chneowave"
if (Test-Path $windsurfPath) {
    Write-Host "✅ Jonction Windsurf créée avec succès" -ForegroundColor Green
    $itemCount = (Get-ChildItem $windsurfPath | Measure-Object).Count
    Write-Host "   📁 $itemCount éléments accessibles via la jonction" -ForegroundColor Cyan
} else {
    Write-Host "❌ Jonction Windsurf manquante" -ForegroundColor Red
}

# Test 2: Vérifier le script uvx
Write-Host "`n2. Vérification du script uvx..." -ForegroundColor Yellow
$uvxPath = "C:\Users\youcef cheriet\Desktop\chneowave\uvx.bat"
if (Test-Path $uvxPath) {
    Write-Host "✅ Script uvx.bat créé avec succès" -ForegroundColor Green
} else {
    Write-Host "❌ Script uvx.bat manquant" -ForegroundColor Red
}

# Test 3: Vérifier UV dans l'environnement virtuel
Write-Host "`n3. Vérification d'UV dans l'environnement virtuel..." -ForegroundColor Yellow
$uvVenvPath = "C:\Users\youcef cheriet\Desktop\chneowave\venv\Scripts\uv.exe"
if (Test-Path $uvVenvPath) {
    Write-Host "✅ UV installé dans l'environnement virtuel" -ForegroundColor Green
    try {
        $uvVersion = & $uvVenvPath --version 2>$null
        Write-Host "   📦 Version: $uvVersion" -ForegroundColor Cyan
    } catch {
        Write-Host "   ⚠️ UV présent mais version non accessible" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ UV manquant dans l'environnement virtuel" -ForegroundColor Red
}

# Test 4: Vérifier le PATH utilisateur
Write-Host "`n4. Vérification du PATH utilisateur..." -ForegroundColor Yellow
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$projectPath = "C:\Users\youcef cheriet\Desktop\chneowave"
if ($userPath -like "*$projectPath*") {
    Write-Host "✅ Répertoire du projet ajouté au PATH utilisateur" -ForegroundColor Green
} else {
    Write-Host "⚠️ Répertoire du projet non trouvé dans le PATH utilisateur" -ForegroundColor Yellow
    Write-Host "   (Redémarrage de la session requis pour prendre effet)" -ForegroundColor Cyan
}

# Test 5: Vérifier les fichiers de documentation
Write-Host "`n5. Vérification de la documentation..." -ForegroundColor Yellow
$docFiles = @("MCP_SOLUTIONS.md", "INSTALLATION_REPORT.md")
foreach ($docFile in $docFiles) {
    $docPath = "C:\Users\youcef cheriet\Desktop\chneowave\$docFile"
    if (Test-Path $docPath) {
        Write-Host "✅ $docFile créé" -ForegroundColor Green
    } else {
        Write-Host "❌ $docFile manquant" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Validation terminée !" -ForegroundColor Green
Write-Host "📋 Actions recommandées :" -ForegroundColor Cyan
Write-Host "   1. Redémarrez Windsurf pour appliquer les changements MCP" -ForegroundColor White
Write-Host "   2. Redémarrez votre session Windows pour le PATH" -ForegroundColor White
Write-Host "   3. Testez les fonctionnalités MCP dans Windsurf" -ForegroundColor White
