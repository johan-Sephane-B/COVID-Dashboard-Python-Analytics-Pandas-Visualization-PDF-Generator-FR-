#!/bin/bash
echo "🔍 Vérification de la structure..."

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 - MANQUANT"
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ $1/ - MANQUANT"
    fi
}

check_file "app.py"
check_dir "pages"
check_file "pages/01_🗺️_Carte_Mondiale.py"
check_file "pages/02_📊_Analyses_Avancées.py"
check_file "pages/03_📄_Rapports_PDF.py"
check_dir "scripts"
check_file "scripts/__init__.py"
check_file "scripts/data_loader.py"
check_file "scripts/data_cleaner.py"
check_file "scripts/visualizations.py"
check_file "scripts/report_generator.py"
check_dir "data"
check_dir "data/raw"
check_dir "data/processed"

echo ""
echo "📊 Si tout est ✅, le dashboard devrait fonctionner"