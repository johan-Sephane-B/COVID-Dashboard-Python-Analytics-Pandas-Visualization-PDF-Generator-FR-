"""
COVID-19 Interactive Dashboard - Script Principal
Auteur: Bahou Johan Stephane
Date: 2026-01-07

Ce script orchestre l'ensemble du pipeline d'analyse :
1. Chargement des données
2. Nettoyage et préparation
3. Génération des visualisations
4. Création du rapport PDF
"""

import os
import sys
from datetime import datetime

# Import des modules du projet
sys.path.append(os.path.dirname(__file__))

try:
    from scripts.data_loader import load_covid_data
    from scripts.data_cleaner import clean_data
    from scripts.visualizations import create_all_visualizations
    from scripts.report_generator import generate_pdf_report
except ImportError as e:
    print(f"⚠️  Erreur d'importation: {e}")
    print("Assurez-vous que tous les scripts sont présents dans le dossier 'scripts/'")
    sys.exit(1)


def create_directories():
    """Crée les dossiers nécessaires s'ils n'existent pas"""
    directories = [
        'data/raw',
        'data/processed',
        'output/figures',
        'output/reports',
        'notebooks'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Structure des dossiers vérifiée")


def main():
    """
    Fonction principale qui exécute l'ensemble du pipeline
    """
    print("=" * 60)
    print("    COVID-19 INTERACTIVE DASHBOARD")
    print("    Démarrage du pipeline d'analyse")
    print("=" * 60)
    print()
    
    start_time = datetime.now()
    
    # Étape 0 : Création des dossiers
    print("📁 Étape 0 : Vérification de la structure des dossiers")
    create_directories()
    print()
    
    # Étape 1 : Chargement des données
    print("📊 Étape 1 : Chargement des données COVID-19")
    print("-" * 60)
    try:
        df = load_covid_data('data/raw/covid_data.csv')
        print(f"✅ Données chargées avec succès : {len(df)} lignes")
        print(f"   Colonnes disponibles : {list(df.columns)}")
    except FileNotFoundError:
        print("❌ Erreur : Fichier 'data/raw/covid_data.csv' introuvable")
        print("   Veuillez télécharger les données et les placer dans data/raw/")
        print("\n💡 Sources de données suggérées :")
        print("   - https://github.com/owid/covid-19-data")
        print("   - https://covid19.who.int/data")
        return
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        return
    print()
    
    # Étape 2 : Nettoyage des données
    print("🧹 Étape 2 : Nettoyage et préparation des données")
    print("-" * 60)
    try:
        df_clean = clean_data(df)
        print(f"✅ Données nettoyées : {len(df_clean)} lignes conservées")
        
        # Sauvegarde des données nettoyées
        output_path = 'data/processed/covid_data_clean.csv'
        df_clean.to_csv(output_path, index=False)
        print(f"💾 Données sauvegardées dans : {output_path}")
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage : {e}")
        return
    print()
    
    # Étape 3 : Création des visualisations
    print("📈 Étape 3 : Génération des visualisations")
    print("-" * 60)
    try:
        figures = create_all_visualizations(df_clean)
        print(f"✅ {len(figures)} visualisations créées avec succès")
        for fig_name in figures:
            print(f"   ✓ {fig_name}")
    except Exception as e:
        print(f"❌ Erreur lors de la création des visualisations : {e}")
        return
    print()
    
    # Étape 4 : Génération du rapport PDF
    print("📄 Étape 4 : Génération du rapport PDF")
    print("-" * 60)
    try:
        report_path = generate_pdf_report(df_clean, figures)
        print(f"✅ Rapport PDF généré : {report_path}")
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport : {e}")
        return
    print()
    
    # Résumé final
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 60)
    print("    ✅ PIPELINE TERMINÉ AVEC SUCCÈS")
    print("=" * 60)
    print(f"\n⏱️  Durée totale : {duration:.2f} secondes")
    print(f"\n📊 Résultats disponibles dans :")
    print(f"   - Données nettoyées : data/processed/")
    print(f"   - Visualisations : output/figures/")
    print(f"   - Rapport PDF : output/reports/")
    print("\n💡 Conseil : Consultez le rapport PDF pour une vue d'ensemble complète")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Exécution interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
