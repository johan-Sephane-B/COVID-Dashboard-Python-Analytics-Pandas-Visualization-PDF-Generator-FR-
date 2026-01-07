"""
Générateur de données de test COVID-19
Crée un fichier CSV avec des données synthétiques pour tester le projet
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
import os


def generate_sample_data(n_days=365, n_countries=10, output_path='data/raw/covid_data.csv'):
    """
    Génère un dataset COVID-19 synthétique pour tests
    
    Args:
        n_days (int): Nombre de jours à générer
        n_countries (int): Nombre de pays à inclure
        output_path (str): Chemin du fichier de sortie
    """
    print("🔄 Génération de données de test COVID-19...")
    
    # Liste de pays
    countries = [
        'France', 'Germany', 'Italy', 'Spain', 'United Kingdom',
        'United States', 'Canada', 'Brazil', 'India', 'Australia',
        'Japan', 'South Korea', 'Mexico', 'South Africa', 'Turkey'
    ][:n_countries]
    
    # Date de début
    start_date = datetime(2020, 3, 1)
    
    # Initialisation des données
    data = []
    
    for country in countries:
        print(f"   Génération : {country}")
        
        # Paramètres de base par pays (variabilité)
        base_cases = random.randint(100, 1000)
        growth_rate = random.uniform(0.03, 0.15)
        peak_day = random.randint(90, 180)
        mortality_rate = random.uniform(0.01, 0.03)
        
        # Variables cumulatives
        total_cases = base_cases
        total_deaths = int(total_cases * mortality_rate)
        total_recovered = 0
        people_vaccinated = 0
        people_fully_vaccinated = 0
        
        for day in range(n_days):
            current_date = start_date + timedelta(days=day)
            
            # Simulation d'une courbe épidémique réaliste
            # Phase de croissance exponentielle puis décroissance
            t = (day - peak_day) / 30
            wave_factor = np.exp(-t**2 / 2)  # Distribution gaussienne
            
            # Calcul des nouveaux cas avec variabilité
            if day < 30:
                # Démarrage lent
                new_cases = int(base_cases * (day / 30) * random.uniform(0.8, 1.2))
            else:
                # Croissance avec vagues
                new_cases = int(base_cases * growth_rate * wave_factor * 
                              random.uniform(0.7, 1.3) * (1 + 0.5 * np.sin(day / 60)))
            
            new_cases = max(0, new_cases)  # Pas de valeurs négatives
            total_cases += new_cases
            
            # Calcul des décès (avec délai)
            new_deaths = int(new_cases * mortality_rate * random.uniform(0.8, 1.2))
            total_deaths += new_deaths
            
            # Calcul des guérisons
            new_recovered = int(new_cases * 0.95 * random.uniform(0.9, 1.1))
            total_recovered += new_recovered
            
            # Calcul des tests
            new_tests = int(new_cases * random.uniform(5, 15))
            total_tests = int(total_cases * random.uniform(8, 20))
            
            # Vaccination (commence après jour 270 environ)
            if day > 270:
                new_vaccinations = int(base_cases * 50 * random.uniform(0.8, 1.2))
                people_vaccinated += new_vaccinations
                
                # Vaccination complète (2e dose après 30 jours)
                if day > 300:
                    people_fully_vaccinated += int(new_vaccinations * 0.85)
            else:
                new_vaccinations = 0
            
            # Hospitalisation (5% des cas actifs)
            hosp_patients = int((total_cases - total_recovered - total_deaths) * 0.05)
            icu_patients = int(hosp_patients * 0.15)
            
            # Taux de positivité
            positive_rate = (new_cases / new_tests * 100) if new_tests > 0 else 0
            
            # Ajout des données manquantes aléatoires (réalisme)
            def maybe_null(value, null_prob=0.05):
                return None if random.random() < null_prob else value
            
            # Construction de la ligne de données
            row = {
                'date': current_date.strftime('%Y-%m-%d'),
                'location': country,
                'total_cases': total_cases,
                'new_cases': maybe_null(new_cases, 0.02),
                'total_deaths': total_deaths,
                'new_deaths': maybe_null(new_deaths, 0.03),
                'total_recovered': maybe_null(total_recovered, 0.10),
                'new_recovered': maybe_null(new_recovered, 0.15),
                'active_cases': total_cases - total_recovered - total_deaths,
                'total_tests': maybe_null(total_tests, 0.08),
                'new_tests': maybe_null(new_tests, 0.10),
                'positive_rate': maybe_null(positive_rate, 0.12),
                'people_vaccinated': maybe_null(people_vaccinated if day > 270 else None, 0.05),
                'people_fully_vaccinated': maybe_null(people_fully_vaccinated if day > 300 else None, 0.05),
                'new_vaccinations': maybe_null(new_vaccinations if day > 270 else None, 0.08),
                'hosp_patients': maybe_null(hosp_patients, 0.15),
                'icu_patients': maybe_null(icu_patients, 0.20),
                'reproduction_rate': maybe_null(1.2 * wave_factor * random.uniform(0.8, 1.2), 0.25),
                'stringency_index': maybe_null(random.uniform(30, 80), 0.20)
            }
            
            data.append(row)
    
    # Création du DataFrame
    df = pd.DataFrame(data)
    
    # Ajout de quelques doublons intentionnels (pour tester le nettoyage)
    n_duplicates = int(len(df) * 0.01)  # 1% de doublons
    duplicates = df.sample(n=n_duplicates)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Sauvegarde
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    # Statistiques
    print(f"\n✅ Données générées avec succès !")
    print(f"   📁 Fichier : {output_path}")
    print(f"   📊 Dimensions : {len(df)} lignes × {len(df.columns)} colonnes")
    print(f"   📅 Période : {df['date'].min()} → {df['date'].max()}")
    print(f"   🌍 Pays : {df['location'].nunique()}")
    print(f"   ⚠️  Valeurs manquantes : {df.isnull().sum().sum()} ({(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100):.1f}%)")
    print(f"   🔄 Doublons ajoutés : {n_duplicates}")
    
    return df


def create_metadata_file(output_path='data/raw/metadata.txt'):
    """
    Crée un fichier de métadonnées explicatif
    """
    metadata = """
COVID-19 Sample Data - Métadonnées
===================================

Ce fichier contient des données synthétiques générées pour tester le projet
COVID-19 Dashboard. Les données ne sont PAS réelles mais simulent des patterns
épidémiologiques réalistes.

COLONNES :
----------
- date : Date de l'observation (YYYY-MM-DD)
- location : Pays/région
- total_cases : Nombre cumulatif de cas confirmés
- new_cases : Nouveaux cas quotidiens
- total_deaths : Nombre cumulatif de décès
- new_deaths : Nouveaux décès quotidiens
- total_recovered : Nombre cumulatif de guérisons
- new_recovered : Nouvelles guérisons quotidiennes
- active_cases : Cas actifs (total - recovered - deaths)
- total_tests : Nombre cumulatif de tests
- new_tests : Nouveaux tests quotidiens
- positive_rate : Taux de positivité des tests (%)
- people_vaccinated : Nombre de personnes ayant reçu au moins 1 dose
- people_fully_vaccinated : Nombre de personnes complètement vaccinées
- new_vaccinations : Nouvelles vaccinations quotidiennes
- hosp_patients : Patients hospitalisés
- icu_patients : Patients en soins intensifs
- reproduction_rate : Taux de reproduction effectif (R)
- stringency_index : Indice de sévérité des mesures (0-100)

CARACTÉRISTIQUES :
-----------------
- Période couverte : ~365 jours
- Nombre de pays : 10-15
- Valeurs manquantes : ~5-10% (réaliste)
- Doublons : ~1% (pour tester le nettoyage)
- Patterns : Courbe épidémique gaussienne avec vagues

UTILISATION :
-------------
Ces données sont parfaites pour :
1. Tester le pipeline complet du projet
2. Développer et déboguer le code
3. Créer des exemples de visualisations
4. Former à l'analyse de données

Pour utiliser des données réelles, téléchargez-les depuis :
- Our World in Data : https://ourworldindata.org/coronavirus
- WHO : https://covid19.who.int/data
- Johns Hopkins : https://github.com/CSSEGISandData/COVID-19

Date de génération : {}""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(metadata)
    
    print(f"   📝 Métadonnées créées : {output_path}")


def main():
    """
    Fonction principale
    """
    print("=" * 60)
    print("    GÉNÉRATEUR DE DONNÉES DE TEST COVID-19")
    print("=" * 60)
    print()
    
    # Génération des données
    df = generate_sample_data(
        n_days=365,
        n_countries=10,
        output_path='data/raw/covid_data.csv'
    )
    
    # Création des métadonnées
    create_metadata_file()
    
    print("\n" + "=" * 60)
    print("✅ GÉNÉRATION TERMINÉE")
    print("=" * 60)
    print("\n💡 Vous pouvez maintenant exécuter :")
    print("   python main.py")
    print("\nOu pour une analyse interactive :")
    print("   jupyter notebook notebooks/exploratory_analysis.ipynb")
    print()


if __name__ == "__main__":
    main()


