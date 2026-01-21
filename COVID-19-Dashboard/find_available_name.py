"""Générer et vérifier des noms créatifs disponibles sur PyPI."""
import requests
import time

def check_pypi_name(name):
    """Vérifie si un nom est disponible sur PyPI."""
    url = f"https://pypi.org/project/{name}/"
    try:
        response = requests.get(url, timeout=5)
        time.sleep(0.5)  # Rate limiting
        if response.status_code == 404:
            return True, f"✅ '{name}' DISPONIBLE"
        elif response.status_code == 200:
            return False, f"❌ '{name}' pris"
        else:
            return None, f"⚠️ '{name}' - Statut {response.status_code}"
    except Exception as e:
        return None, f"⚠️ '{name}' - Erreur"

if __name__ == "__main__":
    # Noms créatifs et uniques
    creative_names = [
        # Basés sur "epi" + suffixe unique
        "epiflow",
        "epikit",
        "epilytics",
        "epistat",
        "epitrack",
        
        # Basés sur "pandemic" + suffixe
        "pandemix",
        "pandekit",
        "pandalytics",
        
        # Basés sur "covid" + suffixe
        "covilytics",
        "covitrack",
        "covistat",
        
        # Noms descriptifs uniques
        "outbreak-analytics",
        "disease-analytics",
        "health-analytics-py",
        "epidemic-toolkit",
        "pandemic-toolkit",
        
        # Noms courts et mémorables
        "epix",
        "pandakit",
        "healthkit-py",
        "diseasekit"
    ]
    
    print("=" * 70)
    print("RECHERCHE DE NOMS CRÉATIFS DISPONIBLES")
    print("=" * 70)
    print()
    
    available = []
    
    for name in creative_names:
        is_available, message = check_pypi_name(name)
        print(message)
        if is_available:
            available.append(name)
    
    print()
    print("=" * 70)
    print(f"RÉSULTAT: {len(available)} nom(s) disponible(s)")
    print("=" * 70)
    
    if available:
        print()
        print("🎯 NOMS DISPONIBLES (TOP 5):")
        for i, name in enumerate(available[:5], 1):
            print(f"   {i}. {name}")
        print()
        print(f"✅ RECOMMANDATION FINALE: '{available[0]}'")
        print()
        print("💡 JUSTIFICATION:")
        print(f"   - Court et mémorable")
        print(f"   - Facile à taper (pip install {available[0]})")
        print(f"   - Évoque l'épidémiologie")
    else:
        print()
        print("⚠️ Tous les noms testés sont pris.")
        print("💡 SOLUTION: Utiliser un nom avec votre username/org:")
        print("   Exemple: 'johan-epi-analytics' ou 'epi-analytics-fr'")
