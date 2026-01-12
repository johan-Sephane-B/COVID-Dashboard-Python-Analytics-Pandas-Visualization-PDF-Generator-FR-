Write-Host "Verification de la structure..."

# Fonction de vérification
function check-file { param($path) if (Test-Path $path) { "OK: $path" } else { "MANQUANT: $path" } }
function check-dir { param($path) if (Test-Path $path -PathType Container) { "OK: $path\" } else { "MANQUANT: $path\" } }

# Vérifications
check-file "app.py"
check-dir "pages"
check-file "pages\01_🗺️_Carte_Mondiale.py"
check-file "pages\02_📊_Analyses_Avancées.py"
check-file "pages\03_📄_Rapports_PDF.py"
check-dir "scripts"
check-file "scripts\__init__.py"
check-file "scripts\data_loader.py"
check-file "scripts\data_cleaner.py"
check-file "scripts\visualizations.py"
check-file "scripts\report_generator.py"
check-dir "data"
check-dir "data\raw"
check-dir "data\processed"

""
"Si tout est OK, le dashboard devrait fonctionner"