"""
Page Analyses Avancées
Visualisations statistiques approfondies
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sys
import os

# Configuration
st.set_page_config(
    page_title="Analyses Avancées",
    page_icon="📊",
    layout="wide"
)

# Imports des modules - Correction
parent_dir = os.path.dirname(os.path.dirname(__file__))
scripts_dir = os.path.join(parent_dir, 'scripts')
sys.path.insert(0, parent_dir)
sys.path.insert(0, scripts_dir)

try:
    from scripts.data_utils import load_covid_data, clean_covid_data
except ImportError as e:
    st.error(f"⚠️ Impossible de charger les modules: {e}")
    st.stop()


@st.cache_data(ttl=3600)
def load_data():
    """Charge les données"""
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


def calculate_growth_rate(df, country, metric='total_cases'):
    """Calcule le taux de croissance"""
    country_data = df[df['location'] == country].sort_values('date')
    country_data['growth_rate'] = country_data[metric].pct_change() * 100
    return country_data


def main():
    st.title("📊 Analyses Avancées COVID-19")
    st.markdown("### Analyses statistiques et comparaisons détaillées")
    st.markdown("---")

    # Chargement des données
    with st.spinner("📈 Chargement des analyses..."):
        df = load_data()

    # Sidebar
    st.sidebar.header("🎯 Paramètres d'Analyse")

    # Sélection des pays
    all_countries = sorted(df['location'].unique())
    selected_countries = st.sidebar.multiselect(
        "🌍 Pays à comparer",
        options=all_countries,
        default=all_countries[:5] if len(all_countries) >= 5 else all_countries[:3]
    )

    if not selected_countries:
        st.warning("⚠️ Veuillez sélectionner au moins un pays.")
        return

    # Filtre de données
    df_filtered = df[df['location'].isin(selected_countries)].copy()

    # ========== SECTION 1 : COMPARAISON MULTI-PAYS ==========
    st.header("🌐 Comparaison Multi-Pays")

    tab1, tab2, tab3 = st.tabs(["📈 Cas Totaux", "💀 Décès", "📊 Taux de Croissance"])

    with tab1:
        fig_cases = px.line(
            df_filtered,
            x='date',
            y='total_cases',
            color='location',
            title="Évolution des Cas Totaux par Pays",
            labels={'total_cases': 'Cas Totaux', 'date': 'Date', 'location': 'Pays'},
            log_y=st.sidebar.checkbox("Échelle logarithmique (Cas)", value=False)
        )
        fig_cases.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig_cases, use_container_width=True)

    with tab2:
        fig_deaths = px.line(
            df_filtered,
            x='date',
            y='total_deaths',
            color='location',
            title="Évolution des Décès Totaux par Pays",
            labels={'total_deaths': 'Décès Totaux', 'date': 'Date', 'location': 'Pays'},
            log_y=st.sidebar.checkbox("Échelle logarithmique (Décès)", value=False)
        )
        fig_deaths.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig_deaths, use_container_width=True)

    with tab3:
        # Calcul du taux de croissance
        growth_data = []
        for country in selected_countries:
            country_growth = calculate_growth_rate(df, country, 'total_cases')
            growth_data.append(country_growth)

        df_growth = pd.concat(growth_data)

        fig_growth = px.line(
            df_growth,
            x='date',
            y='growth_rate',
            color='location',
            title="Taux de Croissance Quotidien (%)",
            labels={'growth_rate': 'Taux de Croissance (%)', 'date': 'Date', 'location': 'Pays'}
        )
        fig_growth.update_layout(height=500, hovermode='x unified')
        fig_growth.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_growth, use_container_width=True)

    st.markdown("---")

    # ========== SECTION 2 : MATRICE DE CORRÉLATION ==========
    st.header("🔗 Matrice de Corrélation")

    # Préparer les données pour la corrélation
    numeric_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']

    if 'people_vaccinated' in df.columns:
        numeric_cols.append('people_vaccinated')

    # Calculer la corrélation pour chaque pays
    selected_country_corr = st.selectbox(
        "Sélectionnez un pays pour l'analyse de corrélation",
        options=selected_countries
    )

    df_corr = df[df['location'] == selected_country_corr][numeric_cols].corr()

    fig_corr = px.imshow(
        df_corr,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        title=f"Matrice de Corrélation - {selected_country_corr}",
        labels={'color': 'Corrélation'}
    )

    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")

    # ========== SECTION 3 : DISTRIBUTION DES NOUVEAUX CAS ==========
    st.header("📊 Distribution des Nouveaux Cas")

    col1, col2 = st.columns(2)

    with col1:
        # Histogramme
        fig_hist = px.histogram(
            df_filtered,
            x='new_cases',
            color='location',
            title="Distribution des Nouveaux Cas Quotidiens",
            labels={'new_cases': 'Nouveaux Cas', 'count': 'Fréquence'},
            marginal='box',
            nbins=50
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # Box plot
        fig_box = px.box(
            df_filtered,
            x='location',
            y='new_cases',
            color='location',
            title="Box Plot - Nouveaux Cas par Pays",
            labels={'new_cases': 'Nouveaux Cas', 'location': 'Pays'}
        )
        fig_box.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # ========== SECTION 4 : TAUX DE MORTALITÉ ==========
    st.header("💀 Analyse du Taux de Mortalité")

    # Calculer le taux de mortalité par pays
    latest_date = df['date'].max()
    df_latest = df[df['date'] == latest_date].copy()
    df_latest = df_latest[df_latest['location'].isin(selected_countries)]
    df_latest['mortality_rate'] = (df_latest['total_deaths'] / df_latest['total_cases'] * 100).round(2)
    df_latest = df_latest.sort_values('mortality_rate', ascending=True)

    fig_mortality = px.bar(
        df_latest,
        x='mortality_rate',
        y='location',
        orientation='h',
        color='mortality_rate',
        color_continuous_scale='Reds',
        title="Taux de Mortalité par Pays (%)",
        labels={'mortality_rate': 'Taux de Mortalité (%)', 'location': 'Pays'},
        text='mortality_rate'
    )

    fig_mortality.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_mortality.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_mortality, use_container_width=True)

    st.markdown("---")

    # ========== SECTION 5 : VACCINATION (SI DISPONIBLE) ==========
    if 'people_vaccinated' in df.columns:
        st.header("💉 Progression de la Vaccination")

        df_vax = df_filtered[df_filtered['people_vaccinated'].notna()].copy()

        if not df_vax.empty:
            fig_vax = px.area(
                df_vax,
                x='date',
                y='people_vaccinated',
                color='location',
                title="Évolution de la Vaccination par Pays",
                labels={'people_vaccinated': 'Personnes Vaccinées', 'date': 'Date', 'location': 'Pays'}
            )
            fig_vax.update_layout(height=500, hovermode='x unified')
            st.plotly_chart(fig_vax, use_container_width=True)
        else:
            st.info("ℹ️ Données de vaccination non disponibles pour les pays sélectionnés.")

    st.markdown("---")

    # ========== SECTION 6 : TABLEAU RÉCAPITULATIF ==========
    st.header("📋 Tableau Récapitulatif")

    # Statistiques par pays
    summary_stats = []
    for country in selected_countries:
        country_data = df[df['location'] == country]
        latest = country_data[country_data['date'] == latest_date].iloc[0]

        stats = {
            'Pays': country,
            'Cas Totaux': f"{latest['total_cases']:,.0f}",
            'Décès Totaux': f"{latest['total_deaths']:,.0f}",
            'Taux Mortalité': f"{(latest['total_deaths'] / latest['total_cases'] * 100):.2f}%",
            'Pic Cas/Jour': f"{country_data['new_cases'].max():,.0f}",
            'Moyenne Cas/Jour': f"{country_data['new_cases'].mean():,.0f}"
        }

        if 'people_vaccinated' in df.columns and pd.notna(latest['people_vaccinated']):
            stats['Vaccinés'] = f"{latest['people_vaccinated']:,.0f}"

        summary_stats.append(stats)

    df_summary = pd.DataFrame(summary_stats)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

    # Bouton de téléchargement
    csv = df_summary.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger le tableau (CSV)",
        data=csv,
        file_name=f"covid_summary_{latest_date.strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    # ========== NOTES ==========
    st.markdown("---")
    st.info("""
    💡 **Interprétation des analyses:**
    - **Taux de croissance** : Variation quotidienne en pourcentage
    - **Corrélation** : Valeurs proches de 1 = forte relation positive
    - **Box plot** : Montre la médiane, quartiles et valeurs aberrantes
    - **Taux de mortalité** : Décès / Cas confirmés × 100
    """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8ed;'>
        <p>📊 Analyses statistiques mises à jour en temps réel</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()