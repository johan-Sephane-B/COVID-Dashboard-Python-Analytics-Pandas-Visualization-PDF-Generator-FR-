"""
Wrapper Universel pour les Fonctions de Données
Gère les différentes versions et noms de fonctions
Inclut : chargement, nettoyage, visualisations, rapports
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# ========== CHARGEMENT DES DONNÉES ==========

def load_covid_data(filepath):
    """
    Charge les données COVID-19 depuis un fichier CSV
    
    Args:
        filepath (str): Chemin vers le fichier CSV
    
    Returns:
        pandas.DataFrame: Données COVID-19
    """
    try:
        # Charger le CSV
        df = pd.read_csv(filepath)
        
        # Convertir la date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        print(f"✅ Données chargées : {len(df)} lignes, {len(df.columns)} colonnes")
        
        return df
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        raise


# ========== NETTOYAGE DES DONNÉES ==========

def clean_covid_data(df):
    """
    Nettoie les données COVID-19
    Compatible avec tous les formats de données
    
    Args:
        df (pandas.DataFrame): Données brutes
    
    Returns:
        pandas.DataFrame: Données nettoyées
    """
    print("🧹 Nettoyage des données...")
    
    df_clean = df.copy()
    
    # 1. Supprimer les doublons
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_rows - len(df_clean)
    if duplicates_removed > 0:
        print(f"   ✅ {duplicates_removed} doublons supprimés")
    
    # 2. Gérer les valeurs manquantes
    if 'date' in df_clean.columns:
        df_clean = df_clean.dropna(subset=['date'])
    
    if 'location' in df_clean.columns:
        df_clean = df_clean.dropna(subset=['location'])
    
    # 3. Remplir les valeurs manquantes numériques
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if df_clean[col].isna().any():
            # Remplir avec 0 pour les colonnes de comptage
            if any(keyword in col.lower() for keyword in ['total', 'new', 'cases', 'deaths', 'vaccinated']):
                df_clean[col] = df_clean[col].fillna(0)
            else:
                # Remplir avec la médiane pour les autres
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    # 4. S'assurer que les valeurs sont positives
    for col in numeric_columns:
        if any(keyword in col.lower() for keyword in ['total', 'new', 'cases', 'deaths']):
            df_clean[col] = df_clean[col].clip(lower=0)
    
    # 5. Trier par date et location
    if 'date' in df_clean.columns and 'location' in df_clean.columns:
        df_clean = df_clean.sort_values(['location', 'date'])
    
    # 6. Réinitialiser l'index
    df_clean = df_clean.reset_index(drop=True)
    
    print(f"✅ Nettoyage terminé : {len(df_clean)} lignes conservées")
    
    return df_clean


# Alias pour compatibilité
clean_data = clean_covid_data


# ========== FONCTIONS UTILITAIRES ==========

def get_data_summary(df):
    """
    Obtient un résumé des données
    
    Args:
        df (pandas.DataFrame): Données
    
    Returns:
        dict: Résumé des données
    """
    summary = {
        'rows': len(df),
        'columns': len(df.columns),
        'countries': df['location'].nunique() if 'location' in df.columns else 0,
        'date_range': (df['date'].min(), df['date'].max()) if 'date' in df.columns else None,
        'missing_values': df.isna().sum().sum(),
        'duplicates': df.duplicated().sum()
    }
    
    return summary


def validate_data(df):
    """
    Valide que les données ont les colonnes requises
    
    Args:
        df (pandas.DataFrame): Données à valider
    
    Returns:
        tuple: (is_valid, missing_columns)
    """
    required_columns = ['date', 'location', 'total_cases', 'total_deaths']
    missing = [col for col in required_columns if col not in df.columns]
    
    return len(missing) == 0, missing


def add_missing_columns(df):
    """
    Ajoute les colonnes manquantes avec des valeurs par défaut
    
    Args:
        df (pandas.DataFrame): Données
    
    Returns:
        pandas.DataFrame: Données avec colonnes ajoutées
    """
    df_complete = df.copy()
    
    # Colonnes optionnelles à ajouter si manquantes
    optional_columns = {
        'new_cases': 0,
        'new_deaths': 0,
        'people_vaccinated': 0,
        'new_vaccinations': 0,
        'total_tests': 0,
        'new_tests': 0,
        'hosp_patients': 0
    }
    
    for col, default_value in optional_columns.items():
        if col not in df_complete.columns:
            df_complete[col] = default_value
            print(f"   ℹ️  Colonne '{col}' ajoutée (valeur par défaut: {default_value})")
    
    return df_complete


def ensure_data_quality(df):
    """
    S'assure que les données sont de bonne qualité
    Fonction complète qui combine toutes les vérifications
    
    Args:
        df (pandas.DataFrame): Données brutes
    
    Returns:
        pandas.DataFrame: Données nettoyées et validées
    """
    print("\n" + "="*70)
    print("  🔍 VÉRIFICATION DE LA QUALITÉ DES DONNÉES")
    print("="*70)
    
    # 1. Validation
    is_valid, missing = validate_data(df)
    if not is_valid:
        print(f"⚠️  Colonnes manquantes : {', '.join(missing)}")
        raise ValueError(f"Colonnes requises manquantes : {missing}")
    
    print("✅ Colonnes requises présentes")
    
    # 2. Nettoyage
    df_clean = clean_covid_data(df)
    
    # 3. Ajout des colonnes optionnelles
    df_complete = add_missing_columns(df_clean)
    
    # 4. Résumé
    summary = get_data_summary(df_complete)
    print(f"\n📊 Résumé :")
    print(f"   Lignes : {summary['rows']:,}")
    print(f"   Colonnes : {summary['columns']}")
    print(f"   Pays : {summary['countries']}")
    if summary['date_range']:
        print(f"   Période : {summary['date_range'][0].date()} → {summary['date_range'][1].date()}")
    
    print("="*70 + "\n")
    
    return df_complete


# ========== VISUALISATIONS ==========

def create_all_visualizations(df, output_dir='output/figures'):
    """
    Crée toutes les visualisations COVID-19
    
    Args:
        df (pandas.DataFrame): Données COVID-19
        output_dir (str): Répertoire de sortie
    
    Returns:
        list: Liste des fichiers créés
    """
    print(f"📊 Création des visualisations dans {output_dir}...")
    
    # Créer le répertoire
    os.makedirs(output_dir, exist_ok=True)
    
    created_files = []
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        
        # Configuration globale
        plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
        
        # 1. Évolution temporelle
        try:
            fig, ax = plt.subplots(figsize=(14, 7))
            
            # Top 5 pays
            latest_date = df['date'].max()
            top_countries = df[df['date'] == latest_date].nlargest(5, 'total_cases')['location'].tolist()
            
            for country in top_countries:
                country_data = df[df['location'] == country].sort_values('date')
                ax.plot(country_data['date'], country_data['total_cases'], 
                       marker='o', label=country, linewidth=2)
            
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Cas Totaux', fontsize=12)
            ax.set_title('Évolution des Cas Totaux - Top 5 Pays', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            filepath = os.path.join(output_dir, '01_time_series.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            created_files.append('01_time_series.png')
            print(f"   ✅ 01_time_series.png")
        except Exception as e:
            print(f"   ⚠️ Erreur graphique 1: {e}")
        
        # 2. Comparaison par pays
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
            
            latest_data = df[df['date'] == latest_date].nlargest(10, 'total_cases')
            
            ax1.barh(latest_data['location'], latest_data['total_cases'], color='steelblue')
            ax1.set_xlabel('Cas Totaux', fontsize=12)
            ax1.set_title('Top 10 - Cas Totaux', fontsize=14, fontweight='bold')
            
            ax2.barh(latest_data['location'], latest_data['total_deaths'], color='crimson')
            ax2.set_xlabel('Décès Totaux', fontsize=12)
            ax2.set_title('Top 10 - Décès Totaux', fontsize=14, fontweight='bold')
            
            filepath = os.path.join(output_dir, '02_country_comparison.png')
            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            created_files.append('02_country_comparison.png')
            print(f"   ✅ 02_country_comparison.png")
        except Exception as e:
            print(f"   ⚠️ Erreur graphique 2: {e}")
        
        # 3. Distribution des nouveaux cas
        try:
            fig, ax = plt.subplots(figsize=(14, 7))
            
            new_cases_data = df[df['new_cases'] > 0]['new_cases']
            ax.hist(new_cases_data, bins=50, color='orange', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Nouveaux Cas Quotidiens', fontsize=12)
            ax.set_ylabel('Fréquence', fontsize=12)
            ax.set_title('Distribution des Nouveaux Cas Quotidiens', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            filepath = os.path.join(output_dir, '03_distribution.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            created_files.append('03_distribution.png')
            print(f"   ✅ 03_distribution.png")
        except Exception as e:
            print(f"   ⚠️ Erreur graphique 3: {e}")
        
        # 4. Taux de mortalité
        try:
            fig, ax = plt.subplots(figsize=(14, 7))
            
            mortality_data = df[df['date'] == latest_date].nlargest(10, 'total_cases').copy()
            mortality_data['mortality_rate'] = (mortality_data['total_deaths'] / mortality_data['total_cases'] * 100)
            mortality_data = mortality_data.sort_values('mortality_rate')
            
            bars = ax.barh(mortality_data['location'], mortality_data['mortality_rate'])
            
            # Colorer selon le taux
            colors = plt.cm.Reds(mortality_data['mortality_rate'] / mortality_data['mortality_rate'].max())
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            ax.set_xlabel('Taux de Mortalité (%)', fontsize=12)
            ax.set_title('Taux de Mortalité par Pays', fontsize=14, fontweight='bold')
            
            filepath = os.path.join(output_dir, '04_mortality_rate.png')
            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            created_files.append('04_mortality_rate.png')
            print(f"   ✅ 04_mortality_rate.png")
        except Exception as e:
            print(f"   ⚠️ Erreur graphique 4: {e}")
        
        print(f"✅ {len(created_files)} visualisation(s) créée(s)")
        
    except ImportError:
        print("⚠️ matplotlib non disponible, visualisations ignorées")
    
    return created_files


# ========== GÉNÉRATION DE RAPPORTS ==========

def generate_report(df, figure_files, output_path, format='pdf'):
    """
    Génère un rapport COVID-19
    
    Args:
        df (pandas.DataFrame): Données
        figure_files (list): Liste des fichiers de figures
        output_path (str): Chemin du fichier de sortie
        format (str): Format de sortie ('pdf' ou 'html')
    
    Returns:
        str: Chemin du fichier créé
    """
    print(f"📄 Génération du rapport {format.upper()}...")
    
    if format.lower() == 'pdf':
        return generate_pdf_report(df, figure_files, output_path)
    else:
        return generate_html_report(df, figure_files, output_path)


def generate_html_report(df, figure_files, output_path):
    """Génère un rapport HTML"""
    
    # Statistiques
    latest_date = df['date'].max()
    total_cases = df[df['date'] == latest_date]['total_cases'].sum()
    total_deaths = df[df['date'] == latest_date]['total_deaths'].sum()
    countries = df['location'].nunique()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport COVID-19</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            h1 {{
                color: #667eea;
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .date {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 25px;
                border-radius: 10px;
                color: white;
                text-align: center;
            }}
            .stat-value {{
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
            }}
            .stat-label {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .section {{
                margin: 40px 0;
            }}
            h2 {{
                color: #333;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-top: 40px;
            }}
            .figure {{
                margin: 30px 0;
                text-align: center;
            }}
            .figure img {{
                max-width: 100%;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            tr:hover {{
                background: #f5f5f5;
            }}
            .footer {{
                text-align: center;
                margin-top: 50px;
                padding-top: 20px;
                border-top: 2px solid #eee;
                color: #999;
            }}
            @media print {{
                body {{
                    background: white;
                }}
                .container {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦠 Rapport d'Analyse COVID-19</h1>
            <div class="date">Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-label">🌍 Cas Totaux</div>
                    <div class="stat-value">{total_cases:,.0f}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">💀 Décès Totaux</div>
                    <div class="stat-value">{total_deaths:,.0f}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">🗺️ Pays Analysés</div>
                    <div class="stat-value">{countries}</div>
                </div>
            </div>
            
            <h2>📊 Visualisations</h2>
    """
    
    # Ajouter les figures
    figures_dir = os.path.dirname(os.path.join(os.path.dirname(output_path), 'figures', ''))
    for fig_file in figure_files:
        fig_path = os.path.join(figures_dir, fig_file)
        if os.path.exists(fig_path):
            html_content += f"""
            <div class="figure">
                <img src="../figures/{fig_file}" alt="{fig_file}">
            </div>
            """
    
    # Tableau des données
    html_content += f"""
            <h2>📋 Données par Pays (Dernière Date)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Pays</th>
                        <th>Cas Totaux</th>
                        <th>Décès Totaux</th>
                        <th>Taux Mortalité</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    latest_data = df[df['date'] == latest_date].nlargest(10, 'total_cases')
    for _, row in latest_data.iterrows():
        mortality = (row['total_deaths'] / row['total_cases'] * 100) if row['total_cases'] > 0 else 0
        html_content += f"""
                    <tr>
                        <td>{row['location']}</td>
                        <td>{row['total_cases']:,.0f}</td>
                        <td>{row['total_deaths']:,.0f}</td>
                        <td>{mortality:.2f}%</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <div class="footer">
                <p>📄 Rapport généré automatiquement par COVID-19 Dashboard</p>
                <p>Développé avec ❤️ en Python</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Sauvegarder
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Rapport HTML créé : {output_path}")
    return output_path


def generate_pdf_report(df, figure_files, output_path):
    """Génère un rapport PDF (nécessite reportlab)"""
    
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        # Créer le PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        story.append(Paragraph("🦠 Rapport d'Analyse COVID-19", title_style))
        story.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 0.5*inch))
        
        # Statistiques
        latest_date = df['date'].max()
        total_cases = df[df['date'] == latest_date]['total_cases'].sum()
        total_deaths = df[df['date'] == latest_date]['total_deaths'].sum()
        
        stats_data = [
            ['Métrique', 'Valeur'],
            ['Cas Totaux', f'{total_cases:,.0f}'],
            ['Décès Totaux', f'{total_deaths:,.0f}'],
            ['Pays Analysés', str(df['location'].nunique())]
        ]
        
        stats_table = Table(stats_data)
        stats_table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        
        story.append(stats_table)
        story.append(PageBreak())
        
        # Ajouter les figures
        figures_dir = os.path.dirname(os.path.join(os.path.dirname(output_path), 'figures', ''))
        for fig_file in figure_files:
            fig_path = os.path.join(figures_dir, fig_file)
            if os.path.exists(fig_path):
                story.append(Paragraph(fig_file.replace('_', ' ').replace('.png', ''), styles['Heading2']))
                img = Image(fig_path, width=6*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
        
        # Construire le PDF
        doc.build(story)
        
        print(f"✅ Rapport PDF créé : {output_path}")
        return output_path
        
    except ImportError:
        print("⚠️ reportlab non disponible, génération HTML à la place")
        html_path = output_path.replace('.pdf', '.html')
        return generate_html_report(df, figure_files, html_path)


# ========== FONCTIONS DE COMPATIBILITÉ ==========

# ========== FONCTIONS DE COMPATIBILITÉ ==========

# Essayer d'importer depuis les modules originaux
try:
    from .data_loader import load_covid_data as original_load
    print("✅ Utilisation de load_covid_data original")
    load_covid_data = original_load
except ImportError:
    print("ℹ️  Utilisation de load_covid_data du wrapper")

try:
    from .data_cleaner import clean_covid_data as original_clean
    print("✅ Utilisation de clean_covid_data original")
    clean_covid_data = original_clean
    clean_data = original_clean
except ImportError:
    try:
        from .data_cleaner import clean_data as original_clean_alt
        print("✅ Utilisation de clean_data original")
        clean_covid_data = original_clean_alt
        clean_data = original_clean_alt
    except ImportError:
        print("ℹ️  Utilisation de clean_covid_data du wrapper")

try:
    from .visualizations import create_all_visualizations as original_viz
    print("✅ Utilisation de create_all_visualizations original")
    create_all_visualizations = original_viz
except ImportError:
    print("ℹ️  Utilisation de create_all_visualizations du wrapper")

try:
    from .report_generator import generate_report as original_report
    print("✅ Utilisation de generate_report original")
    generate_report = original_report
except ImportError:
    print("ℹ️  Utilisation de generate_report du wrapper")


# ========== EXPORTS ==========

__all__ = [
    'load_covid_data',
    'clean_covid_data',
    'clean_data',
    'create_all_visualizations',
    'generate_report',
    'generate_html_report',
    'generate_pdf_report',
    'get_data_summary',
    'validate_data',
    'add_missing_columns',
    'ensure_data_quality'
]


# ========== TEST ==========

if __name__ == "__main__":
    print("🧪 Test du wrapper de données\n")
    
    # Créer des données de test
    test_data = {
        'date': pd.date_range('2020-01-01', periods=10),
        'location': ['France'] * 10,
        'total_cases': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
        'total_deaths': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    }
    
    df_test = pd.DataFrame(test_data)
    
    print("📊 Données de test créées")
    print(df_test.head())
    
    # Test du nettoyage
    df_clean = clean_covid_data(df_test)
    print("\n✅ Nettoyage réussi")
    
    # Test de validation
    is_valid, missing = validate_data(df_clean)
    print(f"\n✅ Validation : {'OK' if is_valid else 'ÉCHEC'}")
    
    # Test d'ajout de colonnes
    df_complete = add_missing_columns(df_clean)
    print(f"\n✅ Colonnes ajoutées : {len(df_complete.columns)}")
    
    print("\n🎉 Tous les tests sont passés !")