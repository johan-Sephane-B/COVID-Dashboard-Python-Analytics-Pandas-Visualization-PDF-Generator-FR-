"""
Page Génération de Rapports
Création de rapports PDF personnalisés depuis l'interface
"""

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
import base64

# Configuration
st.set_page_config(
    page_title="Génération de Rapports",
    page_icon="📄",
    layout="wide"
)

# Imports - Correction du chemin
parent_dir = os.path.dirname(os.path.dirname(__file__))
scripts_dir = os.path.join(parent_dir, 'scripts')
sys.path.insert(0, parent_dir)
sys.path.insert(0, scripts_dir)

try:
    from scripts.data_utils import load_covid_data, clean_covid_data
    from scripts.report_generator import generate_report
    from scripts.visualizations import create_all_visualizations
except ImportError as e:
    st.error(f"⚠️ Impossible de charger les modules: {e}")
    st.info("""
    **Solutions possibles:**
    1. Vérifiez que le dossier `scripts/` existe à la racine du projet
    2. Vérifiez que les fichiers suivants existent:
       - scripts/data_utils.py
       - scripts/report_generator.py
       - scripts/visualizations.py
    3. Assurez-vous que `scripts/__init__.py` existe (même vide)
    """)
    st.stop()


@st.cache_data(ttl=3600)
def load_data():
    """Charge les données"""
    try:
        # Essayer processed d'abord
        processed_path = os.path.join(parent_dir, 'data', 'processed', 'covid_cleaned.csv')
        if os.path.exists(processed_path):
            df = pd.read_csv(processed_path)
        else:
            # Sinon charger depuis raw
            raw_path = os.path.join(parent_dir, 'data', 'raw', 'covid_data.csv')
            if os.path.exists(raw_path):
                df = load_covid_data(raw_path)
                df = clean_covid_data(df)
            else:
                st.error("❌ Aucun fichier de données trouvé.")
                st.info("""
                **Générez des données d'abord:**
                ```bash
                python generate_sample_data.py
                ```
                """)
                return None
        
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")
        return None


def get_download_link(file_path, link_text):
    """Crée un lien de téléchargement pour un fichier"""
    with open(file_path, "rb") as f:
        data = f.read()
    
    b64 = base64.b64encode(data).decode()
    file_name = os.path.basename(file_path)
    
    if file_path.endswith('.pdf'):
        mime = 'application/pdf'
    else:
        mime = 'text/html'
    
    href = f'<a href="data:{mime};base64,{b64}" download="{file_name}">{link_text}</a>'
    return href


def main():
    st.title("📄 Génération de Rapports COVID-19")
    st.markdown("### Créez des rapports PDF/HTML personnalisés")
    st.markdown("---")
    
    # Chargement des données
    with st.spinner("📊 Chargement des données..."):
        df = load_data()
    
    if df is None:
        st.stop()
    
    # ========== SECTION 1 : CONFIGURATION DU RAPPORT ==========
    st.header("⚙️ Configuration du Rapport")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_title = st.text_input(
            "📝 Titre du rapport",
            value="Rapport COVID-19 - Analyse Mondiale"
        )
        
        report_author = st.text_input(
            "👤 Auteur",
            value="Équipe d'Analyse COVID-19"
        )
        
        report_format = st.selectbox(
            "📋 Format de sortie",
            options=['PDF', 'HTML', 'Les deux'],
            index=0
        )
    
    with col2:
        # Sélection des pays pour le rapport
        all_countries = sorted(df['location'].unique())
        selected_countries = st.multiselect(
            "🌍 Pays à inclure",
            options=all_countries,
            default=all_countries[:10] if len(all_countries) >= 10 else all_countries[:5]
        )
        
        # Période d'analyse
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        date_range = st.date_input(
            "📅 Période d'analyse",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Options avancées
    with st.expander("🔧 Options Avancées"):
        include_stats = st.checkbox("📊 Inclure les statistiques descriptives", value=True)
        include_graphs = st.checkbox("📈 Inclure les visualisations", value=True)
        include_table = st.checkbox("📋 Inclure le tableau de données", value=True)
        include_conclusions = st.checkbox("📝 Inclure les conclusions", value=True)
        
        dpi_quality = st.slider(
            "🖼️ Qualité des images (DPI)",
            min_value=150,
            max_value=600,
            value=300,
            step=50
        )
    
    st.markdown("---")
    
    # ========== SECTION 2 : APERÇU DES DONNÉES ==========
    st.header("👀 Aperçu des Données Sélectionnées")
    
    if selected_countries and len(date_range) == 2:
        start_date, end_date = date_range
        df_preview = df[
            (df['location'].isin(selected_countries)) &
            (df['date'].dt.date >= start_date) &
            (df['date'].dt.date <= end_date)
        ].copy()
        
        # Statistiques rapides
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Pays sélectionnés", len(selected_countries))
        
        with col2:
            st.metric("📅 Jours analysés", (end_date - start_date).days + 1)
        
        with col3:
            total_cases = df_preview['total_cases'].max()
            st.metric("🦠 Cas Totaux", f"{total_cases:,.0f}")
        
        with col4:
            total_deaths = df_preview['total_deaths'].max()
            st.metric("💀 Décès Totaux", f"{total_deaths:,.0f}")
        
        # Tableau de prévisualisation
        st.subheader("📋 Aperçu des Dernières Données")
        latest_date = df_preview['date'].max()
        df_latest = df_preview[df_preview['date'] == latest_date][
            ['location', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths']
        ].sort_values('total_cases', ascending=False)
        
        st.dataframe(df_latest.reset_index(drop=True), use_container_width=True, hide_index=True)
    
    else:
        st.warning("⚠️ Veuillez sélectionner au moins un pays et une plage de dates valide.")
    
    st.markdown("---")
    
    # ========== SECTION 3 : GÉNÉRATION DU RAPPORT ==========
    st.header("🚀 Génération du Rapport")
    
    # Informations avant génération
    st.info("""
    💡 **Informations importantes :**
    - La génération peut prendre 30-60 secondes selon les options sélectionnées
    - Les rapports PDF nécessitent ReportLab (pip install reportlab)
    - Les rapports HTML sont toujours disponibles comme alternative
    - Les fichiers seront sauvegardés dans `output/reports/`
    """)
    
    # Bouton de génération
    if st.button("🎨 Générer le Rapport", type="primary", use_container_width=True):
        if not selected_countries:
            st.error("❌ Veuillez sélectionner au moins un pays.")
        elif len(date_range) != 2:
            st.error("❌ Veuillez sélectionner une plage de dates valide.")
        else:
            # Filtrer les données
            start_date, end_date = date_range
            df_report = df[
                (df['location'].isin(selected_countries)) &
                (df['date'].dt.date >= start_date) &
                (df['date'].dt.date <= end_date)
            ].copy()
            
            # Barre de progression
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Étape 1 : Préparation
                status_text.text("📊 Préparation des données...")
                progress_bar.progress(20)
                
                # Créer le répertoire de sortie
                output_dir = os.path.join(parent_dir, 'output', 'reports')
                os.makedirs(output_dir, exist_ok=True)
                
                # Étape 2 : Génération des visualisations
                status_text.text("📈 Création des visualisations...")
                progress_bar.progress(40)
                
                # Répertoire des figures
                figures_dir = os.path.join(parent_dir, 'output', 'figures')
                os.makedirs(figures_dir, exist_ok=True)
                
                # Créer les visualisations avec les données filtrées
                created_files = create_all_visualizations(df_report, figures_dir)
                
                # Étape 3 : Génération du rapport
                status_text.text("📄 Génération du rapport...")
                progress_bar.progress(70)
                
                # Timestamp pour le nom de fichier
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Générer le rapport selon le format choisi
                report_files = []
                
                if report_format in ['PDF', 'Les deux']:
                    try:
                        pdf_file = os.path.join(output_dir, f"COVID_Report_{timestamp}.pdf")
                        generate_report(df_report, created_files, pdf_file, format='pdf')
                        report_files.append(('PDF', pdf_file))
                    except ImportError:
                        st.warning("⚠️ ReportLab non installé. Génération HTML à la place.")
                        report_format = 'HTML'
                
                if report_format in ['HTML', 'Les deux'] or len(report_files) == 0:
                    html_file = os.path.join(output_dir, f"COVID_Report_{timestamp}.html")
                    generate_report(df_report, created_files, html_file, format='html')
                    report_files.append(('HTML', html_file))
                
                # Étape 4 : Finalisation
                progress_bar.progress(100)
                status_text.text("✅ Rapport généré avec succès !")
                
                # Afficher les résultats
                st.success("🎉 Rapport généré avec succès !")
                
                # Liens de téléchargement
                st.markdown("---")
                st.subheader("📥 Télécharger le Rapport")
                
                for format_type, file_path in report_files:
                    if os.path.exists(file_path):
                        try:
                            with open(file_path, 'rb') as f:
                                file_data = f.read()
                            
                            file_name = os.path.basename(file_path)
                            mime_type = 'application/pdf' if format_type == 'PDF' else 'text/html'
                            
                            st.download_button(
                                label=f"📄 Télécharger le rapport {format_type}",
                                data=file_data,
                                file_name=file_name,
                                mime=mime_type,
                                use_container_width=True,
                                key=f"download_{format_type}_{timestamp}"  # Clé unique
                            )
                        except PermissionError:
                            st.error(f"❌ Impossible d'ouvrir {file_name}")
                            st.warning(f"""
                            **Le fichier est probablement ouvert dans un autre programme.**
                            
                            💡 Solutions :
                            1. Fermez le fichier PDF s'il est ouvert
                            2. Utilisez le lien direct ci-dessous pour le télécharger
                            """)
                            
                            # Afficher le chemin absolu pour accès direct
                            abs_path = os.path.abspath(file_path)
                            st.code(abs_path, language=None)
                            
                            if st.button(f"🔄 Réessayer {format_type}", key=f"retry_{format_type}_{timestamp}"):
                                st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                
                # Informations sur les fichiers
                st.info(f"""
                📁 **Fichiers sauvegardés :**
                - Rapport(s) : `{output_dir}/`
                - Visualisations : `{figures_dir}/`
                """)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération : {str(e)}")
                st.exception(e)
            
            finally:
                progress_bar.empty()
                status_text.empty()
    
    st.markdown("---")
    
    # ========== SECTION 4 : RAPPORTS EXISTANTS ==========
    st.header("📚 Rapports Existants")
    
    reports_dir = os.path.join(parent_dir, 'output', 'reports')
    if os.path.exists(reports_dir):
        report_files = [f for f in os.listdir(reports_dir) if f.endswith(('.pdf', '.html'))]
        
        if report_files:
            st.write(f"**{len(report_files)} rapport(s) trouvé(s) :**")
            
            # Trier par date (du plus récent au plus ancien)
            report_files.sort(reverse=True)
            
            # Afficher dans un tableau
            for i, report_file in enumerate(report_files[:10], 1):  # Afficher les 10 plus récents
                file_path = os.path.join(reports_dir, report_file)
                
                try:
                    file_size = os.path.getsize(file_path) / 1024  # en KB
                    file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.text(f"📄 {report_file}")
                    
                    with col2:
                        st.text(f"{file_size:.1f} KB")
                    
                    with col3:
                        st.text(file_date.strftime("%d/%m/%Y"))
                    
                    with col4:
                        # Bouton pour ouvrir le dossier
                        if st.button("📁", key=f"open_folder_{i}", help="Ouvrir le dossier"):
                            abs_dir = os.path.abspath(reports_dir)
                            
                            # Ouvrir l'explorateur selon l'OS
                            import platform
                            if platform.system() == "Windows":
                                os.startfile(abs_dir)
                            elif platform.system() == "Darwin":  # macOS
                                os.system(f'open "{abs_dir}"')
                            else:  # Linux
                                os.system(f'xdg-open "{abs_dir}"')
                
                except Exception as e:
                    st.error(f"❌ Erreur avec {report_file}: {e}")
        else:
            st.info("ℹ️ Aucun rapport existant. Générez-en un ci-dessus !")
    else:
        st.info("ℹ️ Le dossier de rapports n'existe pas encore.")
    
    # ========== CONSEILS ==========
    st.markdown("---")
    st.info("""
    💡 **Conseils pour un rapport optimal :**
    - Sélectionnez 5-10 pays maximum pour une lisibilité optimale
    - Utilisez une période d'analyse pertinente (ex: 6 mois, 1 an)
    - Activez toutes les options pour un rapport complet
    - Augmentez le DPI à 600 pour des présentations professionnelles
    - Le format HTML est idéal pour une consultation web
    - Le format PDF est parfait pour l'impression et le partage
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>📄 Générateur de rapports automatisé | Format professionnel</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()