"""
Test d'exécution du code epi-analytics.

Ce script teste que le code créé fonctionne réellement.
"""

import sys
from pathlib import Path

# Ajouter src_new au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src_new"))

print("=" * 70)
print("  TEST D'EXÉCUTION - Epi Analytics v0.3.0-alpha")
print("=" * 70)
print()

# Test 1 : Imports
print("📦 Test 1 : Imports")
print("-" * 70)

try:
    from epi_analytics import load_data, analyze, visualize
    print("✅ Imports réussis")
    print(f"   - load_data: {load_data}")
    print(f"   - analyze: {analyze}")
    print(f"   - visualize: {visualize}")
except Exception as e:
    print(f"❌ Erreur d'import : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 2 : Chargement données
print("📊 Test 2 : Chargement données")
print("-" * 70)

try:
    data = load_data()
    print(f"✅ Données chargées")
    print(f"   - Lignes : {len(data):,}")
    print(f"   - Colonnes : {len(data.columns)}")
    print(f"   - Pays : {data['location'].nunique()}")
    print(f"   - Période : {data['date'].min()} → {data['date'].max()}")
except Exception as e:
    print(f"❌ Erreur chargement : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 3 : Analyse mortalité
print("🧮 Test 3 : Analyse mortalité")
print("-" * 70)

try:
    mortality = analyze(data, metric="mortality", country="France")
    print(f"✅ Analyse réussie")
    print(f"   - Mortalité France : {mortality:.2f}%")
    
    # Vérification cohérence
    if 0 <= mortality <= 100:
        print(f"   ✓ Valeur cohérente (0-100%)")
    else:
        print(f"   ⚠️  Valeur incohérente : {mortality}%")
        
except Exception as e:
    print(f"❌ Erreur analyse : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4 : Visualisation
print("📈 Test 4 : Visualisation")
print("-" * 70)

try:
    fig = visualize(data, chart_type="timeline", countries=["France"], metric="total_cases")
    print(f"✅ Visualisation créée")
    print(f"   - Type : {type(fig)}")
    print(f"   - Titre : {fig.layout.title.text if hasattr(fig.layout, 'title') else 'N/A'}")
    
    # Sauvegarder pour vérification visuelle
    output_file = Path("test_output_timeline.html")
    fig.write_html(str(output_file))
    print(f"   - Sauvegardé : {output_file}")
    
except Exception as e:
    print(f"❌ Erreur visualisation : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 5 : Workflow complet
print("🔄 Test 5 : Workflow complet")
print("-" * 70)

try:
    # Charger
    data = load_data()
    
    # Analyser plusieurs métriques
    mortality_fr = analyze(data, metric="mortality", country="France")
    mortality_de = analyze(data, metric="mortality", country="Germany")
    
    # Comparer
    comparison = analyze(
        data,
        metric="compare",
        countries=["France", "Germany", "Italy"],
        metric_col="total_cases"
    )
    
    print(f"✅ Workflow complet réussi")
    print(f"   - Mortalité France : {mortality_fr:.2f}%")
    print(f"   - Mortalité Germany : {mortality_de:.2f}%")
    print(f"   - Comparaison :")
    print(comparison.to_string(index=False))
    
except Exception as e:
    print(f"❌ Erreur workflow : {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("✅ TOUS LES TESTS RÉUSSIS !")
print("=" * 70)
print()
print("📝 Résumé :")
print("   ✓ Imports fonctionnent")
print("   ✓ Chargement données OK")
print("   ✓ Analyse mortalité OK")
print("   ✓ Visualisation OK")
print("   ✓ Workflow complet OK")
print()
print("🎉 Le code fonctionne réellement !")
