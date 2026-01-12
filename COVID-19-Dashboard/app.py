"""
COVID-19 Interactive Dashboard
Application Streamlit Principale
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Configuration de la page (doit être en premier)
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajout du chemin des scripts
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Import des modules existants
try:
    from data_utils import load_covid_data, clean_covid_data
except ImportError:
    st.error("⚠️ Module 'data_utils' introuvable. Assurez-vous que le fichier data_utils.py est présent dans le dossier scripts/.")
    st.stop()


# Styles CSS personnalisés
def load_css():
    st.markdown("""
    <style>
        /* Thème principal */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Cards de métriques */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Titres */
        h1 {
            color: #2c3e50;
            font-weight: 700;
        }
        
        h2 {
            color: #34495e;
            font-weight: 600;
            margin-top: 30px;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #2c3e50;
        }
        
        /* Boutons */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Info boxes */
        .info-box {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
            margin: 10px 0;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
            margin-top: 50px;
        }
    </style>
    """, unsafe_allow_html=True)


# Fonction de chargement des données avec cache
@st.cache_data(ttl=3600)
def load_data():
    """Charge et nettoie les données COVID-19"""
    try:
        # Essayer de charger depuis data/processed/ en premier
        processed_path = 'data/processed/covid_cleaned.csv'
        if os.path.exists(processed_path):
            df = pd.read_csv(processed_path)
            df['date'] = pd.to_datetime(df['date'])
            return df
        
        # Sinon charger depuis data/raw/ et nettoyer
        raw_path = 'data/raw/covid_data.csv'
        if os.path.exists(raw_path):
            df = load_covid_data(raw_path)
            df = clean_covid_data(df)
            df['date'] = pd.to_datetime(df['date'])
            return df
        
        st.error("❌ Aucun fichier de données trouvé. Veuillez exécuter 'generate_sample_data.py' ou 'download_from_github.py'")
        st.stop()
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {e}")
        st.stop()


# Fonction pour calculer les statistiques globales
def calculate_global_stats(df):
    """Calcule les statistiques globales"""
    latest_date = df['date'].max()
    latest_data = df[df['date'] == latest_date]
    
    total_cases = latest_data['total_cases'].sum()
    total_deaths = latest_data['total_deaths'].sum()
    
    # Vérifier si la colonne vaccination existe
    has_vaccination = 'people_vaccinated' in df.columns
    total_vaccinated = latest_data['people_vaccinated'].sum() if has_vaccination else 0
    
    # Calculer les variations (7 derniers jours)
    week_ago = latest_date - timedelta(days=7)
    week_data = df[df['date'] == week_ago]
    
    cases_change = total_cases - week_data['total_cases'].sum()
    deaths_change = total_deaths - week_data['total_deaths'].sum()
    
    return {
        'total_cases': total_cases,
        'total_deaths': total_deaths,
        'total_vaccinated': total_vaccinated,
        'cases_change': cases_change,
        'deaths_change': deaths_change,
        'mortality_rate': (total_deaths / total_cases * 100) if total_cases > 0 else 0,
        'countries': df['location'].nunique(),
        'latest_date': latest_date,
        'has_vaccination': has_vaccination
    }


# Interface principale
def main():
    load_css()
    
    # En-tête
    st.title("🦠 COVID-19 Interactive Dashboard")
    st.markdown("### Analyse en temps réel des données mondiales de la pandémie")
    st.markdown("---")
    
    # Chargement des données
    with st.spinner("📊 Chargement des données..."):
        df = load_data()
    
    # Calcul des statistiques globales
    stats = calculate_global_stats(df)
    
    # ========== SECTION 1 : KPIs GLOBAUX ==========
    st.header("📈 Aperçu Global")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌍 Cas Totaux",
            value=f"{stats['total_cases']:,.0f}",
            delta=f"+{stats['cases_change']:,.0f} (7j)"
        )
    
    with col2:
        st.metric(
            label="💀 Décès Totaux",
            value=f"{stats['total_deaths']:,.0f}",
            delta=f"+{stats['deaths_change']:,.0f} (7j)",
            delta_color="inverse"
        )
    
    with col3:
        if has_vaccination and total_vaccinated > 0:
            st.metric(
                label="💉 Personnes Vaccinées",
                value=f"{total_vaccinated:,.0f}"
            )
        else:
            st.metric(
                label="💉 Personnes Vaccinées",
                value="Données non disponibles"
            )
    
    with col4:
        st.metric(
            label="📊 Taux de Mortalité",
            value=f"{stats['mortality_rate']:.2f}%"
        )
    
    st.markdown("---")
    
    # ========== SECTION 2 : FILTRES ==========
    st.sidebar.header("🎛️ Filtres")
    st.sidebar.markdown("Personnalisez votre analyse")
    
    # Filtre de pays
    all_countries = sorted(df['location'].unique())
    selected_countries = st.sidebar.multiselect(
        "🌍 Sélectionner des pays",
        options=all_countries,
        default=all_countries[:5] if len(all_countries) >= 5 else all_countries
    )
    
    # Filtre de dates
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Plage de dates",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filtre de métriques
    available_metrics = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']
    
    # Ajouter vaccination seulement si disponible
    if 'people_vaccinated' in df.columns:
        available_metrics.append('people_vaccinated')
    
    metric_labels = {
        'total_cases': 'Cas Totaux',
        'total_deaths': 'Décès Totaux',
        'new_cases': 'Nouveaux Cas',
        'new_deaths': 'Nouveaux Décès',
        'people_vaccinated': 'Personnes Vaccinées'
    }
    
    selected_metric = st.sidebar.selectbox(
        "📊 Métrique à visualiser",
        options=available_metrics,
        format_func=lambda x: metric_labels[x]
    )
    
    # Appliquer les filtres
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[
            (df['location'].isin(selected_countries)) &
            (df['date'].dt.date >= start_date) &
            (df['date'].dt.date <= end_date)
        ].copy()
    else:
        df_filtered = df[df['location'].isin(selected_countries)].copy()
    
    # ========== SECTION 3 : TIMELINE ANIMÉE ==========
    st.header("📽️ Timeline Animée de l'Évolution")
    
    if not df_filtered.empty:
        fig_timeline = px.line(
            df_filtered,
            x='date',
            y=selected_metric,
            color='location',
            title=f"Évolution de {metric_labels[selected_metric]} au fil du temps",
            labels={
                'date': 'Date',
                selected_metric: metric_labels[selected_metric],
                'location': 'Pays'
            },
            hover_data={'total_cases': ':,.0f', 'total_deaths': ':,.0f'} if 'total_cases' in df_filtered.columns else None
        )
        
        fig_timeline.update_layout(
            hovermode='x unified',
            height=500,
            template='plotly_white',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.warning("⚠️ Aucune donnée disponible pour les filtres sélectionnés.")
    
    st.markdown("---")
    
    # ========== SECTION 4 : INFORMATIONS SYSTÈME ==========
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ℹ️ Informations")
        st.info(f"""
        **Dernière mise à jour:** {stats['latest_date'].strftime('%d/%m/%Y')}
        
        **Pays analysés:** {stats['countries']}
        
        **Période:** {min_date} → {max_date}
        """)
        
        # Lien vers les autres pages
        st.markdown("---")
        st.markdown("### 📑 Navigation")
        st.markdown("""
        - 🗺️ **Carte Mondiale** (à venir)
        - 📊 **Analyses Avancées** (à venir)
        - 📄 **Rapports PDF** (à venir)
        """)
    
    # ========== FOOTER ==========
    st.markdown("---")
    st.markdown("""
    <div class='footer'>
        <p>🦠 <b>COVID-19 Dashboard</b> | Données mises à jour quotidiennement</p>
        <p>Développé avec ❤️ en Python & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
