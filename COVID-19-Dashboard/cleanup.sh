#!/bin/bash
# cleanup.sh - Nettoyage régulier du projet

echo "🧹 Nettoyage du projet..."

# Supprimer fichiers temporaires recursif
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.tmp" -delete
find . -name "*.temp" -delete
find . -name "*~" -delete
find . -name ".DS_Store" -delete
find . -name "Thumbs.db" -delete
find . -name "*.bak" -delete
find . -name "*.backup" -delete

# Supprimer caches tests
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov

# Supprimer artefacts HTML racine
find . -maxdepth 1 -name "demo_*.html" -delete
find . -maxdepth 1 -name "test_output_*.html" -delete

# Statistiques
echo "✅ Nettoyage terminé!"
echo "📊 Espace disque utilisé:"
du -sh .
