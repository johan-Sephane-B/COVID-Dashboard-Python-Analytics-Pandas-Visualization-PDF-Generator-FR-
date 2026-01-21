"""
Application de Démonstration - Epi Analytics v0.3.0-alpha

Cette application montre les capacités de la bibliothèque epi-analytics.
"""

import sys
from pathlib import Path

# Ajouter src_new au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src_new"))

from epi_analytics import load_data, analyze, visualize
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("=" * 80)
print("  🦠 EPI ANALYTICS - DÉMONSTRATION v0.3.0-alpha")
print("=" * 80)
print()

# Charger les données
print("📊 Chargement des données...")
data = load_data()
print(f"✅ {len(data):,} lignes chargées")
print(f"   Pays : {', '.join(data['location'].unique())}")
print(f"   Période : {data['date'].min()} → {data['date'].max()}")
print()

# Pays disponibles
countries = data['location'].unique().tolist()

# ============================================================================
# DÉMONSTRATION 1 : Analyse de Mortalité
# ============================================================================
print("=" * 80)
print("  DÉMONSTRATION 1 : Analyse de Mortalité par Pays")
print("=" * 80)
print()

mortality_results = {}
for country in countries:
    mortality = analyze(data, metric="mortality", country=country)
    mortality_results[country] = mortality
    print(f"  {country:20s} : {mortality:6.2f}% de mortalité")

print()

# Créer graphique mortalité
fig_mortality = go.Figure(data=[
    go.Bar(
        x=list(mortality_results.keys()),
        y=list(mortality_results.values()),
        marker_color='indianred',
        text=[f"{v:.2f}%" for v in mortality_results.values()],
        textposition='auto',
    )
])

fig_mortality.update_layout(
    title="Taux de Mortalité COVID-19 par Pays",
    xaxis_title="Pays",
    yaxis_title="Mortalité (%)",
    template="plotly_white",
    height=500
)

output_file_1 = Path("demo_output_mortality.html")
fig_mortality.write_html(str(output_file_1))
print(f"📊 Graphique sauvegardé : {output_file_1}")
print()

# ============================================================================
# DÉMONSTRATION 2 : Comparaison des Pays
# ============================================================================
print("=" * 80)
print("  DÉMONSTRATION 2 : Comparaison des Cas Totaux")
print("=" * 80)
print()

comparison = analyze(
    data,
    metric="compare",
    countries=countries,
    metric_col="total_cases"
)

print(comparison.to_string(index=False))
print()

# ============================================================================
# DÉMONSTRATION 3 : Évolution Temporelle
# ============================================================================
print("=" * 80)
print("  DÉMONSTRATION 3 : Évolution Temporelle des Cas")
print("=" * 80)
print()

fig_timeline = visualize(
    data,
    chart_type="timeline",
    countries=countries,
    metric="total_cases"
)

fig_timeline.update_layout(
    title="Évolution des Cas Totaux COVID-19",
    height=600,
    template="plotly_white"
)

output_file_2 = Path("demo_output_timeline.html")
fig_timeline.write_html(str(output_file_2))
print(f"📈 Graphique sauvegardé : {output_file_2}")
print()

# ============================================================================
# DÉMONSTRATION 4 : Dashboard Complet
# ============================================================================
print("=" * 80)
print("  DÉMONSTRATION 4 : Dashboard Complet")
print("=" * 80)
print()

# Créer un dashboard avec plusieurs graphiques
fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Taux de Mortalité",
        "Évolution des Cas (France)",
        "Comparaison Totale",
        "Nouveaux Cas Quotidiens (France)"
    ),
    specs=[
        [{"type": "bar"}, {"type": "scatter"}],
        [{"type": "bar"}, {"type": "scatter"}]
    ]
)

# 1. Mortalité
fig_dashboard.add_trace(
    go.Bar(
        x=list(mortality_results.keys()),
        y=list(mortality_results.values()),
        name="Mortalité",
        marker_color='indianred'
    ),
    row=1, col=1
)

# 2. Évolution France
france_data = data[data['location'] == 'France'].copy()
fig_dashboard.add_trace(
    go.Scatter(
        x=france_data['date'],
        y=france_data['total_cases'],
        name="Cas Totaux",
        line=dict(color='royalblue', width=2)
    ),
    row=1, col=2
)

# 3. Comparaison
fig_dashboard.add_trace(
    go.Bar(
        x=comparison['location'],
        y=comparison['total_cases'],
        name="Cas Totaux",
        marker_color='steelblue'
    ),
    row=2, col=1
)

# 4. Nouveaux cas France
fig_dashboard.add_trace(
    go.Scatter(
        x=france_data['date'],
        y=france_data['new_cases'],
        name="Nouveaux Cas",
        line=dict(color='orange', width=2),
        fill='tozeroy'
    ),
    row=2, col=2
)

# Mise en page
fig_dashboard.update_layout(
    title_text="Dashboard COVID-19 - Epi Analytics Demo",
    height=800,
    showlegend=False,
    template="plotly_white"
)

output_file_3 = Path("demo_output_dashboard.html")
fig_dashboard.write_html(str(output_file_3))
print(f"📊 Dashboard complet sauvegardé : {output_file_3}")
print()

# ============================================================================
# DÉMONSTRATION 5 : Exemple de Code Simple
# ============================================================================
print("=" * 80)
print("  DÉMONSTRATION 5 : Exemple d'Utilisation Simple")
print("=" * 80)
print()

example_code = """
# Installation
pip install epi-analytics

# Utilisation en 3 lignes
from epi_analytics import load_data, analyze, visualize

data = load_data()  # Auto-download et cache
mortality = analyze(data, metric="mortality", country="France")
fig = visualize(data, chart_type="timeline", countries=["France"])

print(f"Mortalité France : {mortality:.2f}%")
fig.show()
"""

print("Code d'exemple :")
print(example_code)

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("=" * 80)
print("  ✅ DÉMONSTRATION TERMINÉE")
print("=" * 80)
print()
print("📁 Fichiers créés :")
print(f"   1. {output_file_1} - Graphique mortalité")
print(f"   2. {output_file_2} - Timeline évolution")
print(f"   3. {output_file_3} - Dashboard complet")
print()
print("🎯 Capacités démontrées :")
print("   ✓ Chargement automatique des données")
print("   ✓ Analyse de mortalité par pays")
print("   ✓ Comparaison entre pays")
print("   ✓ Visualisations interactives")
print("   ✓ Dashboard multi-graphiques")
print()
print("🚀 La bibliothèque epi-analytics fonctionne parfaitement !")
print()
print("💡 Ouvrez les fichiers HTML dans votre navigateur pour voir les graphiques.")
print("=" * 80)
