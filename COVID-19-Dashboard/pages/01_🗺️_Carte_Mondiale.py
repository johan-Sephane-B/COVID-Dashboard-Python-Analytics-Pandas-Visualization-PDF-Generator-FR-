"""
Page Carte Mondiale Interactive
Visualisation géographique des données COVID-19
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Configuration de la page
st.set_page_config(
    page_title="Carte Mondiale COVID-19",
    page_icon="🗺️",
    layout="wide"
)

# Ajout du chemin des scripts - Correction
parent_dir = os.path.dirname(os.path.dirname(__file__))
scripts_dir = os.path.join(parent_dir, 'scripts')
sys.path.insert(0, parent_dir)
sys.path.insert(0, scripts_dir)

try:
    # Essayer d'importer depuis data_utils (wrapper)
    from scripts.data_utils import load_covid_data, clean_covid_data
    print("✅ Import depuis data_utils")
except ImportError:
    try:
        # Fallback vers les imports originaux
        from scripts.data_loader import load_covid_data
        from scripts.data_cleaner import clean_covid_data
        print("✅ Import depuis modules originaux")
    except ImportError as e:
        st.error(f"⚠️ Impossible de charger les modules: {e}")
        st.info("""
        **Solution :**
        1. Vérifiez que `scripts/data_utils.py` existe
        2. Ou que `scripts/data_loader.py` et `scripts/data_cleaner.py` existent
        3. Exécutez `python check_functions.py` pour diagnostiquer
        """)
        st.stop()


# Fonction de chargement des données
@st.cache_data(ttl=3600)
def load_data():
    """Charge les données COVID-19"""
    try:
        processed_path = os.path.join(parent_dir, 'data', 'processed', 'covid_cleaned.csv')
        if os.path.exists(processed_path):
            df = pd.read_csv(processed_path)
        else:
            raw_path = os.path.join(parent_dir, 'data', 'raw', 'covid_data.csv')
            df = load_covid_data(raw_path)
            df = clean_covid_data(df)
        
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"Erreur: {e}")
        st.stop()


# Mapping des noms de pays vers codes ISO
def get_country_iso_codes(df):
    """Convertit les noms de pays en codes ISO-3"""
    # Mapping manuel pour les pays courants
    country_mapping = {
        'United States': 'USA',
        'United Kingdom': 'GBR',
        'France': 'FRA',
        'Germany': 'DEU',
        'Italy': 'ITA',
        'Spain': 'ESP',
        'Brazil': 'BRA',
        'India': 'IND',
        'China': 'CHN',
        'Russia': 'RUS',
        'Japan': 'JPN',
        'Canada': 'CAN',
        'Australia': 'AUS',
        'Mexico': 'MEX',
        'South Korea': 'KOR',
        'Indonesia': 'IDN',
        'Turkey': 'TUR',
        'Saudi Arabia': 'SAU',
        'Argentina': 'ARG',
        'South Africa': 'ZAF',
        'Netherlands': 'NLD',
        'Belgium': 'BEL',
        'Switzerland': 'CHE',
        'Sweden': 'SWE',
        'Poland': 'POL',
        'Austria': 'AUT',
        'Norway': 'NOR',
        'Denmark': 'DNK',
        'Finland': 'FIN',
        'Portugal': 'PRT',
        'Greece': 'GRC',
        'Czech Republic': 'CZE',
        'Romania': 'ROU',
        'Chile': 'CHL',
        'Peru': 'PER',
        'Colombia': 'COL',
        'Egypt': 'EGY',
        'Pakistan': 'PAK',
        'Bangladesh': 'BGD',
        'Vietnam': 'VNM',
        'Thailand': 'THA',
        'Malaysia': 'MYS',
        'Philippines': 'PHL',
        'Singapore': 'SGP',
        'New Zealand': 'NZL',
        'Ireland': 'IRL',
        'Ukraine': 'UKR',
        'Israel': 'ISR',
        'Hungary': 'HUN',
        'Serbia': 'SRB',
        'Morocco': 'MAR',
        'Nigeria': 'NGA',
        'Kenya': 'KEN',
        'Ethiopia': 'ETH',
        'Ghana': 'GHA'
    }
    
    df['iso_code'] = df['location'].map(country_mapping)
    return df


def main():
    st.title("🗺️ Carte Mondiale COVID-19")
    st.markdown("### Visualisation géographique de la pandémie")
    st.markdown("---")
    
    # Chargement des données
    with st.spinner("🌍 Chargement de la carte mondiale..."):
        df = load_data()
        df = get_country_iso_codes(df)
    
    # Sidebar - Paramètres
    st.sidebar.header("⚙️ Paramètres de la Carte")
    
    # Sélection de la métrique
    metric_options = {
        'total_cases': 'Cas Totaux',
        'total_deaths': 'Décès Totaux',
        'new_cases': 'Nouveaux Cas (quotidiens)',
        'new_deaths': 'Nouveaux Décès (quotidiens)'
    }
    
    # Ajouter vaccination si disponible
    if 'people_vaccinated' in df.columns:
        metric_options['people_vaccinated'] = 'Personnes Vaccinées'
    
    selected_metric = st.sidebar.selectbox(
        "📊 Métrique à afficher",
        options=list(metric_options.keys()),
        format_func=lambda x: metric_options[x]
    )
    
    # Sélection de la date
    available_dates = sorted(df['date'].dt.date.unique())
    selected_date = st.sidebar.select_slider(
        "📅 Date",
        options=available_dates,
        value=available_dates[-1]
    )
    
    # Type de projection
    projection_type = st.sidebar.selectbox(
        "🌐 Projection de la carte",
        options=['natural earth', 'equirectangular', 'mercator', 'orthographic', 'robinson'],
        index=0
    )
    
    # Palette de couleurs
    color_scheme = st.sidebar.selectbox(
        "🎨 Palette de couleurs",
        options=['Reds', 'YlOrRd', 'Oranges', 'Blues', 'Viridis', 'Plasma', 'Inferno'],
        index=0
    )
    
    # Filtrer les données pour la date sélectionnée
    df_map = df[df['date'].dt.date == selected_date].copy()
    
    # Supprimer les lignes sans code ISO
    df_map = df_map.dropna(subset=['iso_code'])
    
    # ========== CARTE CHOROPLÈTHE ==========
    st.header(f"🗺️ {metric_options[selected_metric]} - {selected_date}")
    
    if not df_map.empty:
        fig_map = px.choropleth(
            df_map,
            locations='iso_code',
            color=selected_metric,
            hover_name='location',
            hover_data={
                'iso_code': False,
                'total_cases': ':,.0f',
                'total_deaths': ':,.0f',
                selected_metric: ':,.0f'
            },
            color_continuous_scale=color_scheme,
            projection=projection_type,
            title=f"Distribution mondiale - {metric_options[selected_metric]}",
            labels={selected_metric: metric_options[selected_metric]}
        )
        
        fig_map.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type=projection_type
            ),
            coloraxis_colorbar=dict(
                title=metric_options[selected_metric],
                thickness=15,
                len=0.7
            )
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.error("❌ Aucune donnée disponible pour cette date.")
    
    st.markdown("---")
    
    # ========== TOP 10 PAYS ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 - Cas Totaux")
        top_cases = df_map.nlargest(10, 'total_cases')[['location', 'total_cases', 'total_deaths']]
        top_cases.columns = ['Pays', 'Cas Totaux', 'Décès']
        st.dataframe(
            top_cases.reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.subheader("💀 Top 10 - Décès Totaux")
        top_deaths = df_map.nlargest(10, 'total_deaths')[['location', 'total_cases', 'total_deaths']]
        top_deaths.columns = ['Pays', 'Cas Totaux', 'Décès']
        st.dataframe(
            top_deaths.reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # ========== GRAPHIQUE EN BARRES INTERACTIF ==========
    st.header("📊 Top 20 Pays par Métrique Sélectionnée")
    
    top_countries = df_map.nlargest(20, selected_metric)
    
    fig_bar = px.bar(
        top_countries,
        x=selected_metric,
        y='location',
        orientation='h',
        color=selected_metric,
        color_continuous_scale=color_scheme,
        title=f"Top 20 - {metric_options[selected_metric]}",
        labels={
            selected_metric: metric_options[selected_metric],
            'location': 'Pays'
        },
        hover_data={
            'total_cases': ':,.0f',
            'total_deaths': ':,.0f'
        }
    )
    
    fig_bar.update_layout(
        height=600,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # ========== STATISTIQUES GLOBALES ==========
    st.markdown("---")
    st.header("📈 Statistiques Globales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌍 Cas Mondiaux",
            f"{df_map['total_cases'].sum():,.0f}"
        )
    
    with col2:
        st.metric(
            "💀 Décès Mondiaux",
            f"{df_map['total_deaths'].sum():,.0f}"
        )
    
    with col3:
        mortality = (df_map['total_deaths'].sum() / df_map['total_cases'].sum() * 100)
        st.metric(
            "📊 Taux de Mortalité Global",
            f"{mortality:.2f}%"
        )
    
    with col4:
        st.metric(
            "🗺️ Pays Affectés",
            f"{len(df_map)}"
        )
    
    # ========== NOTES ==========
    st.markdown("---")
    st.info("""
    💡 **Conseils d'utilisation:**
    - Utilisez le curseur de date pour explorer l'évolution temporelle
    - Changez la projection pour différentes perspectives géographiques
    - Survolez les pays pour voir les détails
    - Les couleurs plus foncées indiquent des valeurs plus élevées
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>🗺️ Carte mondiale mise à jour quotidiennement | Données: Our World in Data</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()