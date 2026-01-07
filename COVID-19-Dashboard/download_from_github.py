"""
Téléchargement des données COVID-19 directement depuis GitHub
Alternative quand les sites principaux sont inaccessibles
"""

import urllib.request
import os
from pathlib import Path
from datetime import datetime


def download_file(url, output_path):
    """Télécharge un fichier avec progression"""
    print(f"   📥 Téléchargement depuis : {url}")
    print("   ⏳ En cours...", end='', flush=True)
    
    try:
        urllib.request.urlretrieve(url, output_path)
        print(" ✅ Terminé !")
        return True
    except Exception as e:
        print(f" ❌ Erreur : {e}")
        return False

def main():
    print("=" * 70)
    print("  TÉLÉCHARGEMENT COVID-19 - VERSION GITHUB")
    print("=" * 70)
    print()
    
    output_path = 'data/raw/covid_data.csv'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Liste d'URLs alternatives depuis GitHub
    sources = [
        {
            'name': 'Our World in Data (GitHub)',
            'url': 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv',
            'size': '~50 MB'
        },
        {
            'name': 'Johns Hopkins (GitHub)',
            'url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
            'size': '~5 MB'
        },
        {
            'name': 'COVID-19 Dataset (GitHub)',
            'url': 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
            'size': '~2 MB'
        }
    ]
    
    print("📋 Sources GitHub disponibles :")
    for i, source in enumerate(sources, 1):
        print(f"   {i}. {source['name']} ({source['size']})")
    print()
    
    # Essayer chaque source
    for i, source in enumerate(sources, 1):
        print(f"🔄 Tentative {i}/{len(sources)} : {source['name']}")
        print("-" * 70)
        
        if download_file(source['url'], output_path):
            # Vérifier le fichier
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            
            if file_size < 0.1:
                print(f"   ⚠️  Fichier trop petit ({file_size:.2f} MB), essai suivant...")
                continue
            
            print(f"\n   ✅ Fichier téléchargé : {file_size:.2f} MB")
            
            # Vérifier le contenu
            try:
                import pandas as pd
                df = pd.read_csv(output_path, nrows=5)
                
                print(f"   ✅ Format valide")
                print(f"   📊 Colonnes : {len(df.columns)}")
                print(f"   📋 Aperçu : {', '.join(df.columns[:5].tolist())}...")
                
                print("\n" + "=" * 70)
                print("  ✅ TÉLÉCHARGEMENT RÉUSSI !")
                print("=" * 70)
                print(f"\n📁 Fichier : {output_path}")
                print(f"📅 Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                print("\n✅ Lancez maintenant : python main.py")
                print()
                return
                
            except Exception as e:
                print(f"   ⚠️  Erreur de lecture : {e}")
                continue
        
        print()
    
    # Si tout échoue
    print("=" * 70)
    print("  ❌ TOUTES LES SOURCES ONT ÉCHOUÉ")
    print("=" * 70)
    print()
    print("💡 SOLUTIONS :")
    print()
    print("1️⃣  PROBLÈME DE CONNEXION")
    print("   • Vérifiez votre connexion internet")
    print("   • Désactivez temporairement VPN/Proxy")
    print("   • Essayez depuis un autre réseau")
    print()
    print("2️⃣  TÉLÉCHARGEMENT MANUEL")
    print("   Ouvrez votre navigateur et téléchargez depuis :")
    print("   https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv")
    print(f"   Sauvegardez dans : {os.path.abspath(output_path)}")
    print()
    print("3️⃣  UTILISER DES DONNÉES SYNTHÉTIQUES")
    print("   python generate_sample_data.py")
    print()

if __name__ == "__main__":
    main()


