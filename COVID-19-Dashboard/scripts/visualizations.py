"""
Module de création des visualisations COVID-19
Génère différents types de graphiques avec matplotlib et seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration du style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def create_all_visualizations(df, output_dir='output/figures'):
    """
    Crée toutes les visualisations et les sauvegarde
    
    Args:
        df (pd.DataFrame): DataFrame nettoyé
        output_dir (str): Dossier de destination
    
    Returns:
        list: Liste des noms de fichiers créés
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    created_files = []
    
    print("🎨 Création des visualisations...")
    
    # 1. Évolution temporelle des cas
    if 'date' in df.columns and 'total_cases' in df.columns:
        file = plot_time_series(df, output_dir)
        if file:
            created_files.append(file)
    
    # 2. Comparaison par pays
    if 'location' in df.columns:
        file = plot_country_comparison(df, output_dir)
        if file:
            created_files.append(file)
    
    # 3. Distribution des cas
    if 'new_cases' in df.columns:
        file = plot_distribution(df, output_dir)
        if file:
            created_files.append(file)
    
    # 4. Taux de mortalité
    if 'total_cases' in df.columns and 'total_deaths' in df.columns:
        file = plot_mortality_rate(df, output_dir)
        if file:
            created_files.append(file)
    
    # 5. Heatmap de corrélation
    file = plot_correlation_heatmap(df, output_dir)
    if file:
        created_files.append(file)
    
    # 6. Progression vaccinale
    if 'people_vaccinated' in df.columns:
        file = plot_vaccination_progress(df, output_dir)
        if file:
            created_files.append(file)
    
    print(f"✅ {len(created_files)} visualisations créées\n")
    return created_files


def plot_time_series(df, output_dir):
    """
    Graphique d'évolution temporelle des cas
    """
    try:
        print("   📈 Création : Évolution temporelle des cas...")
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Sélection des principaux pays
        if 'location' in df.columns:
            top_countries = df.groupby('location')['total_cases'].max().nlargest(5).index
            for country in top_countries:
                country_data = df[df['location'] == country].sort_values('date')
                ax.plot(country_data['date'], country_data['total_cases'], 
                       marker='o', markersize=3, label=country, linewidth=2)
        else:
            df_sorted = df.sort_values('date')
            ax.plot(df_sorted['date'], df_sorted['total_cases'], 
                   marker='o', markersize=3, linewidth=2)
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre total de cas', fontsize=12, fontweight='bold')
        ax.set_title('Évolution Temporelle des Cas COVID-19', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper left', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filename = f"{output_dir}/01_time_series.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"      ✓ Sauvegardé : {filename}")
        return "01_time_series.png"
    except Exception as e:
        print(f"      ⚠️  Erreur : {e}")
        return None


def plot_country_comparison(df, output_dir):
    """
    Graphique de comparaison entre pays
    """
    try:
        print("   🌍 Création : Comparaison par pays...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Top 10 pays par cas totaux
        if 'total_cases' in df.columns:
            top_cases = df.groupby('location')['total_cases'].max().nlargest(10).sort_values()
            ax1.barh(range(len(top_cases)), top_cases.values, color=plt.cm.Reds(np.linspace(0.4, 0.8, len(top_cases))))
            ax1.set_yticks(range(len(top_cases)))
            ax1.set_yticklabels(top_cases.index)
            ax1.set_xlabel('Nombre total de cas', fontsize=11, fontweight='bold')
            ax1.set_title('Top 10 Pays - Cas Totaux', fontsize=13, fontweight='bold')
            ax1.grid(axis='x', alpha=0.3)
        
        # Top 10 pays par décès
        if 'total_deaths' in df.columns:
            top_deaths = df.groupby('location')['total_deaths'].max().nlargest(10).sort_values()
            ax2.barh(range(len(top_deaths)), top_deaths.values, color=plt.cm.Greys(np.linspace(0.4, 0.8, len(top_deaths))))
            ax2.set_yticks(range(len(top_deaths)))
            ax2.set_yticklabels(top_deaths.index)
            ax2.set_xlabel('Nombre total de décès', fontsize=11, fontweight='bold')
            ax2.set_title('Top 10 Pays - Décès Totaux', fontsize=13, fontweight='bold')
            ax2.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        filename = f"{output_dir}/02_country_comparison.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"      ✓ Sauvegardé : {filename}")
        return "02_country_comparison.png"
    except Exception as e:
        print(f"      ⚠️  Erreur : {e}")
        return None


def plot_distribution(df, output_dir):
    """
    Distribution des nouveaux cas quotidiens
    """
    try:
        print("   📊 Création : Distribution des cas...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Histogramme
        data = df['new_cases'].dropna()
        data = data[data > 0]  # Seulement les valeurs positives
        
        ax1.hist(data, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Nouveaux cas quotidiens', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Fréquence', fontsize=11, fontweight='bold')
        ax1.set_title('Distribution des Nouveaux Cas', fontsize=13, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Boxplot
        ax2.boxplot(data, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightblue', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        ax2.set_ylabel('Nouveaux cas quotidiens', fontsize=11, fontweight='bold')
        ax2.set_title('Boxplot des Nouveaux Cas', fontsize=13, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        filename = f"{output_dir}/03_distribution.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"      ✓ Sauvegardé : {filename}")
        return "03_distribution.png"
    except Exception as e:
        print(f"      ⚠️  Erreur : {e}")
        return None


def plot_mortality_rate(df, output_dir):
    """
    Taux de mortalité par pays
    """
    try:
        print("   💀 Création : Taux de mortalité...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Calcul du taux de mortalité
        df_mortality = df.groupby('location').agg({
            'total_cases': 'max',
            'total_deaths': 'max'
        })
        df_mortality = df_mortality[df_mortality['total_cases'] > 1000]  # Filtrer les petits pays
        df_mortality['mortality_rate'] = (df_mortality['total_deaths'] / df_mortality['total_cases']) * 100
        df_mortality = df_mortality.sort_values('mortality_rate', ascending=False).head(15)
        
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(df_mortality)))
        bars = ax.barh(range(len(df_mortality)), df_mortality['mortality_rate'], color=colors)
        ax.set_yticks(range(len(df_mortality)))
        ax.set_yticklabels(df_mortality.index)
        ax.set_xlabel('Taux de mortalité (%)', fontsize=12, fontweight='bold')
        ax.set_title('Taux de Mortalité COVID-19 par Pays', fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        # Ajout des valeurs sur les barres
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'{width:.2f}%', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        
        filename = f"{output_dir}/04_mortality_rate.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"      ✓ Sauvegardé : {filename}")
        return "04_mortality_rate.png"
    except Exception as e:
        print(f"      ⚠️  Erreur : {e}")
        return None


def plot_correlation_heatmap(df, output_dir):
    """
    Heatmap de corrélation entre variables
    """
    try:
        print("   🔥 Création : Heatmap de corrélation...")
        
        # Sélection des colonnes numériques
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col not in ['Unnamed: 0', 'index']]
        
        if len(numeric_cols) < 2:
            print("      ⚠️  Pas assez de colonnes numériques")
            return None
        
        corr_matrix = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax)
        ax.set_title('Matrice de Corrélation des Variables COVID-19', 
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        filename = f"{output_dir}/05_correlation_heatmap.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"      ✓ Sauvegardé : {filename}")
        return "05_correlation_heatmap.png"
    except Exception as e:
        print(f"      ⚠️  Erreur : {e}")
        return None


def plot_vaccination_progress(df, output_dir):
    """
    Progression de la vaccination
    """
    try:
        print("   💉 Création : Progression vaccinale...")
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Top 10 pays par vaccination
        if 'location' in df.columns:
            top_vacc = df.groupby('location')['people_vaccinated'].max().nlargest(10).index
            for country in top_vacc:
                country_data = df[df['location'] == country].sort_values('date')
                ax.plot(country_data['date'], country_data['people_vaccinated'], 
                       marker='o', markersize=3, label=country, linewidth=2)
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre de personnes vaccinées', fontsize=12, fontweight='bold')
        ax.set_title('Progression de la Vaccination COVID-19', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper left', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filename = f"{output_dir}/06_vaccination_progress.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"      ✓ Sauvegardé : {filename}")
        return "06_vaccination_progress.png"
    except Exception as e:
        print(f"      ⚠️  Erreur : {e}")
        return None


# Test du module
if __name__ == "__main__":
    print("=== Test du module visualizations ===\n")
    print("⚠️  Ce module nécessite des données réelles pour être testé")
    print("   Exécutez le pipeline complet avec main.py")
