"""Vérifier la disponibilité des noms sur PyPI."""
import requests

def check_pypi_name(name):
    """Vérifie si un nom est disponible sur PyPI."""
    url = f"https://pypi.org/project/{name}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            return f"✅ '{name}' est DISPONIBLE sur PyPI"
        elif response.status_code == 200:
            return f"❌ '{name}' est DÉJÀ PRIS sur PyPI"
        else:
            return f"⚠️ '{name}' - Statut inconnu ({response.status_code})"
    except Exception as e:
        return f"⚠️ Erreur lors de la vérification de '{name}': {e}"

if __name__ == "__main__":
    names_to_check = [
        "epi-analytics",
        "covid-analytics",
        "pandemic-analytics",
        "epi-tools",
        "epidata"
    ]
    
    print("=" * 60)
    print("VÉRIFICATION DISPONIBILITÉ NOMS PyPI")
    print("=" * 60)
    print()
    
    for name in names_to_check:
        result = check_pypi_name(name)
        print(result)
    
    print()
    print("=" * 60)
    print("RECOMMANDATION:")
    print("Choisir le premier nom DISPONIBLE dans la liste ci-dessus")
    print("=" * 60)
