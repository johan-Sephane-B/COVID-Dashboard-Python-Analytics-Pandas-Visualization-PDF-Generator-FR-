"""
Téléchargement Données COVID-19 depuis GitHub
Source : Our World in Data (GitHub Repository)
230+ pays inclus
"""

import requests
import os
import pandas as pd
from datetime import datetime

def download_from_github():
    """Télécharge les données depuis le repository GitHub OWID"""
    
    print("\n" + "=" * 70)
    print("  🌍 TÉLÉCHARGEMENT DONNÉES COVID-19 DEPUIS GITHUB")
    print("  Repository : github.com/owid/covid-19-data")
    print("  Couverture : 230+ pays et territoires")
    print("=" * 70 + "\n")
    
    # URL GitHub Raw (accès direct au fichier CSV)
    github_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    
    # Alternative : URL du CDN GitHub
    # github_url = "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
    
    # Créer le répertoire
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/covid_data.csv"
    
    print(f"📦 Repository GitHub : owid/covid-19-data")
    print(f"🌐 URL : {github_url}")
    print(f"📁 Destination : {output_path}\n")
    
    try:
        # Télécharger
        print("⏳ Téléchargement en cours...")
        print("   Fichier : ~80-100 MB")
        print("   Durée estimée : 1-3 minutes selon votre connexion\n")
        
        # Headers pour GitHub
        headers = {
            'User-Agent': 'COVID-Dashboard-Python/1.0',
            'Accept': 'application/vnd.github.v3.raw'
        }
        
        response = requests.get(github_url, headers=headers, stream=True)
        response.raise_for_status()
        
        # Taille totale
        total_size = int(response.headers.get('content-length', 0))
        
        # Télécharger avec progression
        downloaded = 0
        chunk_size = 8192
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        mb_downloaded = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        
                        # Barre de progression
                        bar_length = 40
                        filled = int(bar_length * downloaded / total_size)
                        bar = '█' * filled + '░' * (bar_length - filled)
                        
                        print(f"\r   [{bar}] {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="")
        
        print("\n")
        
        # Analyser les données
        print("🔍 Analyse des données téléchargées...\n")
        
        df = pd.read_csv(output_path)
        
        # Statistiques
        countries = df['location'].nunique()
        date_min = pd.to_datetime(df['date']).min()
        date_max = pd.to_datetime(df['date']).max()
        total_rows = len(df)
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        
        print("=" * 70)
        print("  ✅ TÉLÉCHARGEMENT RÉUSSI DEPUIS GITHUB")
        print("=" * 70 + "\n")
        
        print(f"📊 Statistiques :")
        print(f"   🌍 Pays/Territoires : {countries}")
        print(f"   📅 Période : {date_min.strftime('%d/%m/%Y')} → {date_max.strftime('%d/%m/%Y')}")
        print(f"   📈 Lignes : {total_rows:,}")
        print(f"   💾 Taille : {file_size:.1f} MB")
        print(f"   📋 Colonnes : {len(df.columns)}")
        
        # Vérifier vaccination
        has_vaccination = 'people_vaccinated' in df.columns
        if has_vaccination:
            vax_data = df['people_vaccinated'].notna().sum()
            print(f"   💉 Vaccination : ✅ Oui ({vax_data:,} entrées)")
        
        # Top 10 pays
        latest = df[df['date'] == df['date'].max()].nlargest(10, 'total_cases')
        
        print(f"\n🏆 Top 10 Pays (dernière date) :")
        for i, (_, row) in enumerate(latest.iterrows(), 1):
            cases = row['total_cases']
            deaths = row['total_deaths']
            print(f"   {i:2}. {row['location']:25} {cases:>15,.0f} cas | {deaths:>12,.0f} décès")
        
        # Info sur les colonnes
        essential_cols = ['date', 'location', 'total_cases', 'new_cases', 
                         'total_deaths', 'new_deaths', 'people_vaccinated']
        available = [c for c in essential_cols if c in df.columns]
        
        print(f"\n📋 Colonnes essentielles disponibles :")
        for col in available:
            print(f"   ✅ {col}")
        
        # Info GitHub
        print(f"\n📦 Source GitHub :")
        print(f"   Repository : owid/covid-19-data")
        print(f"   Branch : master")
        print(f"   Path : public/data/owid-covid-data.csv")
        print(f"   Commit : Latest (téléchargé le {datetime.now().strftime('%d/%m/%Y %H:%M')})")
        
        print(f"\n📁 Fichier sauvegardé :")
        print(f"   {os.path.abspath(output_path)}")
        
        print("\n" + "=" * 70)
        print("  🚀 PRÊT À UTILISER")
        print("=" * 70)
        print(f"\n💡 Lancez le dashboard :")
        print(f"   streamlit run app.py")
        print(f"\n   → {countries} pays disponibles dans l'interface !")
        print("=" * 70 + "\n")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERREUR lors du téléchargement depuis GitHub\n")
        print(f"   {e}\n")
        
        print("💡 Solutions :")
        print("   1. Vérifiez votre connexion internet")
        print("   2. Réessayez dans quelques minutes")
        print("   3. GitHub peut avoir des limites de taux - attendez 1h")
        print("\n   4. Téléchargement manuel :")
        print("      a) Allez sur : https://github.com/owid/covid-19-data")
        print("      b) Naviguez : public/data/owid-covid-data.csv")
        print("      c) Clic droit sur 'Raw' → Enregistrer sous")
        print("      d) Sauvegardez dans : data/raw/covid_data.csv\n")
        
        return False
    
    except Exception as e:
        print(f"\n❌ ERREUR inattendue : {e}\n")
        import traceback
        traceback.print_exc()
        return False


def show_github_info():
    """Affiche les informations sur le repository GitHub"""
    
    print("\n" + "=" * 70)
    print("  📦 INFORMATIONS GITHUB REPOSITORY")
    print("=" * 70 + "\n")
    
    print("🔗 Repository :")
    print("   https://github.com/owid/covid-19-data\n")
    
    print("📂 Structure :")
    print("   covid-19-data/")
    print("   └── public/")
    print("       └── data/")
    print("           └── owid-covid-data.csv  ← Ce fichier\n")
    
    print("📊 Contenu :")
    print("   - 230+ pays et territoires")
    print("   - Données depuis janvier 2020")
    print("   - Mis à jour quotidiennement")
    print("   - ~2.5 millions de lignes")
    print("   - 67 colonnes de données\n")
    
    print("📋 Colonnes principales :")
    columns = [
        "date, location, population",
        "total_cases, new_cases, total_deaths, new_deaths",
        "people_vaccinated, people_fully_vaccinated",
        "total_tests, new_tests",
        "hosp_patients, icu_patients",
        "stringency_index (mesures gouvernementales)",
        "Et beaucoup plus..."
    ]
    for col in columns:
        print(f"   • {col}")
    
    print("\n🔄 Mise à jour :")
    print("   - Automatique chaque jour")
    print("   - Données validées par Oxford University")
    print("   - Sources multiples agrégées\n")
    
    print("=" * 70 + "\n")


def verify_github_data():
    """Vérifie les données téléchargées depuis GitHub"""
    
    data_path = "data/raw/covid_data.csv"
    
    if not os.path.exists(data_path):
        print("\n⚠️  Aucune donnée trouvée")
        print("   Exécutez : python download_from_github_v2.py\n")
        return False
    
    try:
        print("\n" + "=" * 70)
        print("  ✅ VÉRIFICATION DES DONNÉES GITHUB")
        print("=" * 70 + "\n")
        
        df = pd.read_csv(data_path)
        
        print(f"📊 Statistiques :")
        print(f"   Pays : {df['location'].nunique()}")
        print(f"   Lignes : {len(df):,}")
        print(f"   Colonnes : {len(df.columns)}")
        print(f"   Période : {df['date'].min()} → {df['date'].max()}")
        
        # Taille du fichier
        file_size = os.path.getsize(data_path) / (1024 * 1024)
        file_date = datetime.fromtimestamp(os.path.getmtime(data_path))
        print(f"   Taille : {file_size:.1f} MB")
        print(f"   Téléchargé : {file_date.strftime('%d/%m/%Y %H:%M')}")
        
        # Vérifier colonnes
        required = ['date', 'location', 'total_cases', 'total_deaths']
        missing = [c for c in required if c not in df.columns]
        
        if missing:
            print(f"\n⚠️  Colonnes manquantes : {', '.join(missing)}")
            return False
        
        print(f"\n✅ Toutes les colonnes essentielles présentes")
        print(f"✅ Données GitHub valides et prêtes")
        
        print("\n" + "=" * 70 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}\n")
        return False


def main():
    """Fonction principale"""
    
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--info":
            show_github_info()
        elif sys.argv[1] == "--verify":
            verify_github_data()
        else:
            print("\nUsage :")
            print("  python download_from_github_v2.py          # Télécharger")
            print("  python download_from_github_v2.py --info   # Infos GitHub")
            print("  python download_from_github_v2.py --verify # Vérifier données\n")
    else:
        success = download_from_github()
        
        if success:
            print("\n" + "🎉" * 35)
            print("\n   Données GitHub téléchargées avec succès !")
            print("   230+ pays disponibles dans le dashboard !")
            print("\n" + "🎉" * 35 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Téléchargement annulé")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nAppuyez sur Entrée pour fermer...")