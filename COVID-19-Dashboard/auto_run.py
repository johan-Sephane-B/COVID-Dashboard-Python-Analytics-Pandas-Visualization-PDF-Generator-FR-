"""
Script d'exécution automatique complète
Génère les données si nécessaire et lance l'analyse
"""

import os
import sys
from pathlib import Path


def check_data_exists():
    """Vérifie si les données existent"""
    data_path = 'data/raw/covid_data.csv'
    
    if os.path.exists(data_path):
        file_size = os.path.getsize(data_path)
        if file_size > 1000:  # Plus de 1KB
            print(f"✅ Données trouvées : {data_path} ({file_size / 1024:.2f} KB)")
            return True
    
    print(f"❌ Données manquantes : {data_path}")
    return False

def generate_data():
    """Génère des données synthétiques"""
    print("\n" + "=" * 70)
    print("  GÉNÉRATION DE DONNÉES SYNTHÉTIQUES")
    print("=" * 70)
    print()
    
    try:
        # Importer la fonction de génération depuis la racine
        from generate_sample_data import generate_sample_data
        
        print("🔄 Génération de données COVID-19...")
        
        # Génération des données
        df = generate_sample_data(
            n_days=365,
            n_countries=10,
            output_path='data/raw/covid_data.csv'
        )
        
        print(f"\n✅ Données générées avec succès !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la génération : {e}")
        import traceback
        traceback.print_exc()
        return False

def run_analysis():
    """Lance l'analyse principale"""
    print("\n" + "=" * 70)
    print("  LANCEMENT DE L'ANALYSE")
    print("=" * 70)
    print()
    
    try:
        # Importer et exécuter main
        from main import main as run_main
        run_main()
        return True
    except Exception as e:
        print(f"\n❌ Erreur lors de l'analyse : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("=" * 70)
    print("  COVID-19 DASHBOARD - EXÉCUTION AUTOMATIQUE")
    print("=" * 70)
    print()
    
    # Vérifier les données
    if not check_data_exists():
        print("\n💡 Génération automatique de données synthétiques...")
        
        if not generate_data():
            print("\n❌ Impossible de générer les données")
            print("\n💡 Solutions :")
            print("   1. Téléchargez manuellement depuis :")
            print("      https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv")
            print("   2. Placez le fichier dans : data/raw/covid_data.csv")
            print("   3. Ou utilisez : python download_from_github.py")
            return
    
    # Lancer l'analyse
    if run_analysis():
        print("\n" + "=" * 70)
        print("  ✅ ANALYSE TERMINÉE AVEC SUCCÈS")
        print("=" * 70)
        print()
        print("📁 Résultats disponibles :")
        print("   • Visualisations : output/figures/")
        print("   • Rapport : output/reports/")
        print()
        
        # Lister les fichiers générés
        figures_dir = Path('output/figures')
        if figures_dir.exists():
            figures = list(figures_dir.glob('*.png'))
            if figures:
                print(f"📊 {len(figures)} visualisations créées :")
                for fig in figures:
                    print(f"   ✓ {fig.name}")
        
        reports_dir = Path('output/reports')
        if reports_dir.exists():
            reports = list(reports_dir.glob('*'))
            if reports:
                print(f"\n📄 {len(reports)} rapport(s) généré(s) :")
                for rep in reports:
                    print(f"   ✓ {rep.name}")
        
        print()
    else:
        print("\n❌ L'analyse a échoué")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Exécution interrompue")
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
        import traceback
        traceback.print_exc()


