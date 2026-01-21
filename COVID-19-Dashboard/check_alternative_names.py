"""Vérifier la disponibilité des noms alternatifs sur PyPI."""
import requests

def check_pypi_name(name):
    """Vérifie si un nom est disponible sur PyPI."""
    url = f"https://pypi.org/project/{name}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            return f"✅ '{name}' est DISPONIBLE"
        elif response.status_code == 200:
            return f"❌ '{name}' est PRIS"
        else:
            return f"⚠️ '{name}' - Statut {response.status_code}"
    except Exception as e:
        return f"⚠️ '{name}' - Erreur: {e}"

if __name__ == "__main__":
    # Noms alternatifs créatifs
    alternative_names = [
        "epi-tools",
        "epidata",
        "pandemic-py",
        "epipy-analytics",
        "covid-data-tools",
        "epi-insights",
        "pandemic-insights",
        "epi-viz",
        "covid-viz",
        "epi-learn",
        "pandemic-learn",
        "epi-edu",
        "covid-edu-analytics"
    ]
    
    print("=" * 70)
    print("VÉRIFICATION NOMS ALTERNATIFS PyPI")
    print("=" * 70)
    print()
    
    available = []
    taken = []
    
    for name in alternative_names:
        result = check_pypi_name(name)
        print(result)
        if "DISPONIBLE" in result:
            available.append(name)
        elif "PRIS" in result:
            taken.append(name)
    
    print()
    print("=" * 70)
    print(f"RÉSUMÉ: {len(available)} noms disponibles, {len(taken)} noms pris")
    print("=" * 70)
    
    if available:
        print()
        print("🎯 NOMS DISPONIBLES (par ordre de préférence):")
        for i, name in enumerate(available, 1):
            print(f"   {i}. {name}")
        print()
        print(f"✅ RECOMMANDATION: Utiliser '{available[0]}'")
    else:
        print()
        print("⚠️ AUCUN NOM DISPONIBLE - Générer de nouvelles alternatives")
