<#
.SYNOPSIS
    Script de nettoyage automatique du projet.
#>

Write-Host "Nettoyage du projet..." -ForegroundColor Cyan

$root = Get-Location

# 1. Nettoyage Caches Python
Get-ChildItem -Path $root -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $root -Recurse -File -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

# 2. Nettoyage Caches Tests & Coverage
if (Test-Path "$root\.pytest_cache") { Remove-Item "$root\.pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue }
if (Test-Path "$root\.coverage") { Remove-Item "$root\.coverage" -Force -ErrorAction SilentlyContinue }
if (Test-Path "$root\htmlcov") { Remove-Item "$root\htmlcov" -Recurse -Force -ErrorAction SilentlyContinue }

# 3. Nettoyage Backups
Get-ChildItem -Path $root -Recurse -File -Include "*.tmp", "*.temp", "*.bak", "*.backup", "*.old", "*~" | Remove-Item -Force -ErrorAction SilentlyContinue

# 4. Suppression des gros artefacts HTML racine
Get-ChildItem -Path $root -File -Filter "demo_*.html" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $root -File -Filter "test_output_*.html" | Remove-Item -Force -ErrorAction SilentlyContinue

# 5. OS Junk
Get-ChildItem -Path $root -Recurse -File -Include ".DS_Store", "Thumbs.db" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "Nettoyage termine !" -ForegroundColor Green
$stats = Get-ChildItem -Path $root -Recurse | Measure-Object -Property Length -Sum
$mb = "{0:N2}" -f ($stats.Sum / 1MB)
Write-Host "Espace utilisé: $mb MB"
