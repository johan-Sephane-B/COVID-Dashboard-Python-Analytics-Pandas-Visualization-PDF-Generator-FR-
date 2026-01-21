"""
Script pour créer un dataset sample FICTIF pour tests.

Utilisé quand le téléchargement OWID échoue.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

def create_mock_sample_dataset():
    """Crée un dataset sample fictif pour tests."""
    
    print("🔄 Création dataset sample fictif...")
    
    # Paramètres
    countries = ["France", "Germany", "Italy", "Spain", "United Kingdom"]
    days = 200
    start_date = datetime(2023, 6, 1)
    
    # Populations (approximatives)
    populations = {
        "France": 67000000,
        "Germany": 83000000,
        "Italy": 60000000,
        "Spain": 47000000,
        "United Kingdom": 67000000
    }
    
    data_list = []
    
    for country in countries:
        print(f"   Génération données pour {country}...")
        
        # Générer série temporelle
        for day in range(days):
            date = start_date + timedelta(days=day)
            
            # Simuler progression épidémie
            base_cases = 1000 + day * 50
            noise = np.random.randint(-100, 100)
            new_cases = max(0, base_cases + noise)
            
            # Mortalité ~2%
            new_deaths = int(new_cases * 0.02 * np.random.uniform(0.8, 1.2))
            
            # Cumulatifs
            if day == 0:
                total_cases = new_cases
                total_deaths = new_deaths
            else:
                prev_row = [r for r in data_list if r['location'] == country][-1]
                total_cases = prev_row['total_cases'] + new_cases
                total_deaths = prev_row['total_deaths'] + new_deaths
            
            data_list.append({
                'location': country,
                'date': date.strftime('%Y-%m-%d'),
                'total_cases': total_cases,
                'total_deaths': total_deaths,
                'new_cases': new_cases,
                'new_deaths': new_deaths,
                'population': populations[country],
                'continent': 'Europe',
                'iso_code': country[:3].upper()
            })
    
    # Créer DataFrame
    df = pd.DataFrame(data_list)
    
    # Créer dossier
    output_dir = Path("data/sample")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder
    output_file = output_dir / "covid_sample.csv"
    df.to_csv(output_file, index=False)
    
    # Stats
    file_size = output_file.stat().st_size / 1024
    
    print(f"\n✅ Dataset sample fictif créé !")
    print(f"   📁 Fichier : {output_file}")
    print(f"   📊 Lignes : {len(df):,}")
    print(f"   🌍 Pays : {df['location'].nunique()}")
    print(f"   📅 Période : {df['date'].min()} → {df['date'].max()}")
    print(f"   💾 Taille : {file_size:.1f} KB")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("  Création Dataset Sample FICTIF - Epi Analytics")
    print("=" * 60)
    print()
    
    success = create_mock_sample_dataset()
    
    print()
    print("=" * 60)
    if success:
        print("✅ SUCCÈS - Dataset sample prêt")
    else:
        print("❌ ÉCHEC")
    print("=" * 60)
