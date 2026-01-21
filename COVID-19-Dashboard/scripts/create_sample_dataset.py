"""
Script pour créer le dataset sample COVID-19.

Ce script télécharge les données OWID et crée un fichier sample
avec 5 pays et ~200 derniers jours de données.
"""

import pandas as pd
import requests
from pathlib import Path
import sys

def create_sample_dataset():
    """Crée le dataset sample pour epi-analytics."""
    
    print("🔄 Téléchargement des données OWID...")
    
    # URL des données OWID
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    
    try:
        # Télécharger les données
        df = pd.read_csv(url)
        print(f"✅ Téléchargé : {len(df):,} lignes, {len(df.columns)} colonnes")
        
        # Sélectionner 5 pays représentatifs
        countries = ["France", "Germany", "Italy", "Spain", "United Kingdom"]
        print(f"\n🌍 Sélection de {len(countries)} pays : {', '.join(countries)}")
        
        sample = df[df['location'].isin(countries)].copy()
        print(f"   Données filtrées : {len(sample):,} lignes")
        
        # Prendre les 200 derniers jours par pays
        sample = sample.groupby('location').tail(200)
        print(f"   Après tail(200) : {len(sample):,} lignes")
        
        # Créer le dossier de destination
        output_dir = Path("data/sample")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder
        output_file = output_dir / "covid_sample.csv"
        sample.to_csv(output_file, index=False)
        
        # Statistiques
        file_size = output_file.stat().st_size / 1024  # KB
        
        print(f"\n✅ Dataset sample créé avec succès !")
        print(f"   📁 Fichier : {output_file}")
        print(f"   📊 Lignes : {len(sample):,}")
        print(f"   🌍 Pays : {sample['location'].nunique()}")
        print(f"   📅 Période : {sample['date'].min()} → {sample['date'].max()}")
        print(f"   💾 Taille : {file_size:.1f} KB")
        
        # Vérifications
        print(f"\n🔍 Vérifications :")
        print(f"   ✓ Taille < 500 KB : {file_size < 500}")
        print(f"   ✓ 5 pays présents : {sample['location'].nunique() == 5}")
        print(f"   ✓ Colonnes essentielles présentes :")
        
        essential_cols = ['location', 'date', 'total_cases', 'total_deaths', 
                         'new_cases', 'new_deaths', 'population']
        for col in essential_cols:
            present = col in sample.columns
            print(f"      {'✓' if present else '✗'} {col}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de téléchargement : {e}")
        print("\n💡 Solution : Vérifiez votre connexion internet")
        return False
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Création du Dataset Sample - Epi Analytics")
    print("=" * 60)
    print()
    
    success = create_sample_dataset()
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ SUCCÈS - Dataset sample prêt à l'emploi")
        sys.exit(0)
    else:
        print("❌ ÉCHEC - Voir erreurs ci-dessus")
        sys.exit(1)
