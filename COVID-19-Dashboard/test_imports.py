import os
import sys

print("=== DIAGNOSTIC DES IMPORTS ===\n")

# 1. Chemin actuel
print(f"📂 Répertoire actuel: {os.getcwd()}")

# 2. Vérifier que scripts/ existe
scripts_path = os.path.join(os.getcwd(), 'scripts')
print(f"\n📂 Dossier scripts/: {'✅ Existe' if os.path.exists(scripts_path) else '❌ Manquant'}")

# 3. Lister les fichiers dans scripts/
if os.path.exists(scripts_path):
    files = os.listdir(scripts_path)
    print(f"\n📄 Fichiers dans scripts/:")
    for f in files:
        print(f"   - {f}")

# 4. Tester les imports
print("\n🔍 Test des imports:")

try:
    sys.path.insert(0, scripts_path)
    from scripts.data_loader import load_covid_data
    print("   ✅ data_loader.py - OK")
except Exception as e:
    print(f"   ❌ data_loader.py - ERREUR: {e}")

try:
    from scripts.data_cleaner import clean_data
    print("   ✅ data_cleaner.py - OK")
except Exception as e:
    print(f"   ❌ data_cleaner.py - ERREUR: {e}")

try:
    from scripts.visualizations import create_all_visualizations
    print("   ✅ visualizations.py - OK")
except Exception as e:
    print(f"   ❌ visualizations.py - ERREUR: {e}")

try:
    from scripts.report_generator import generate_pdf_report
    print("   ✅ report_generator.py - OK")
except Exception as e:
    print(f"   ❌ report_generator.py - ERREUR: {e}")

print("\n=== FIN DU DIAGNOSTIC ===")