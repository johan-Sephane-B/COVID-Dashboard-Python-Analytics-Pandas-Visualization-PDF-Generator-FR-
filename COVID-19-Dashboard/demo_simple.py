"""
Démonstration Simple - Epi Analytics

Exécute directement sans installation.
"""

import sys
from pathlib import Path

# Ajouter src_new au path
sys.path.insert(0, str(Path(__file__).parent / "src_new"))

print("=" * 80)
print("  🦠 EPI ANALYTICS - DÉMONSTRATION RAPIDE")
print("=" * 80)
print()

# Import et test
print("📦 Import de la bibliothèque...")
try:
    from epi_analytics import load_data, analyze, visualize
    print("✅ Import réussi !")
except Exception as e:
    print(f"❌ Erreur : {e}")
    sys.exit(1)

print()

# Charger données
print("📊 Chargement des données...")
data = load_data()
print(f"✅ {len(data):,} lignes chargées")
print(f"   Pays : {', '.join(data['location'].unique())}")
print()

# Analyse simple
print("🧮 Analyse de mortalité...")
countries = ["France", "Germany", "Italy", "Spain", "United Kingdom"]

for country in countries:
    mortality = analyze(data, metric="mortality", country=country)
    print(f"   {country:20s} : {mortality:5.2f}%")

print()

# Visualisation
print("📈 Création de visualisations...")

# Timeline
fig1 = visualize(data, chart_type="timeline", countries=["France", "Germany"], metric="total_cases")
fig1.update_layout(title="Évolution COVID-19 - France vs Germany", height=500)
fig1.write_html("demo_timeline.html")
print("   ✅ demo_timeline.html créé")

# Comparaison
fig2 = visualize(data, chart_type="comparison", metric="total_cases", top_n=5)
fig2.update_layout(title="Top 5 Pays - Cas Totaux", height=500)
fig2.write_html("demo_comparison.html")
print("   ✅ demo_comparison.html créé")

print()
print("=" * 80)
print("  ✅ DÉMONSTRATION TERMINÉE")
print("=" * 80)
print()
print("📁 Fichiers créés :")
print("   - demo_timeline.html")
print("   - demo_comparison.html")
print()
print("💡 Ouvrez ces fichiers dans votre navigateur !")
print()
