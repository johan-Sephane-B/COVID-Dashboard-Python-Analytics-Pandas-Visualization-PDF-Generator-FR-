"""
Module de génération de rapports PDF
Crée un rapport automatisé avec statistiques et visualisations
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, 
                                PageBreak, Table, TableStyle)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import pandas as pd
from pathlib import Path


def generate_pdf_report(df, figure_files, output_dir='output/reports'):
    """
    Génère un rapport PDF complet
    
    Args:
        df (pd.DataFrame): DataFrame des données nettoyées
        figure_files (list): Liste des fichiers de visualisations
        output_dir (str): Dossier de destination
    
    Returns:
        str: Chemin du fichier PDF créé
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Nom du fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/COVID_Report_{timestamp}.pdf"
    
    # Création du document
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Conteneur pour les éléments du PDF
    story = []
    styles = getSampleStyleSheet()
    
    # Styles personnalisés
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # 1. Page de garde
    story.extend(create_cover_page(df, styles, title_style))
    story.append(PageBreak())
    
    # 2. Résumé exécutif
    story.extend(create_executive_summary(df, styles, heading_style))
    story.append(PageBreak())
    
    # 3. Statistiques descriptives
    story.extend(create_statistics_section(df, styles, heading_style))
    story.append(PageBreak())
    
    # 4. Visualisations
    story.extend(create_visualizations_section(figure_files, styles, heading_style))
    
    # 5. Conclusions
    story.append(PageBreak())
    story.extend(create_conclusions(df, styles, heading_style))
    
    # Génération du PDF
    doc.build(story)
    
    print(f"✅ Rapport PDF généré : {filename}")
    return filename


def create_cover_page(df, styles, title_style):
    """Crée la page de garde"""
    elements = []
    
    # Espacement initial
    elements.append(Spacer(1, 2*inch))
    
    # Titre principal
    title = Paragraph("Rapport d'Analyse COVID-19", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*inch))
    
    # Sous-titre
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    subtitle = Paragraph("Tableau de Bord Interactif - Analyse des Données", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 1*inch))
    
    # Informations du rapport
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"<b>Date de génération :</b> {date_str}", info_style))
    elements.append(Paragraph(f"<b>Nombre d'enregistrements :</b> {len(df):,}", info_style))
    
    if 'date' in df.columns:
        date_min = df['date'].min().strftime("%d/%m/%Y") if pd.notna(df['date'].min()) else "N/A"
        date_max = df['date'].max().strftime("%d/%m/%Y") if pd.notna(df['date'].max()) else "N/A"
        elements.append(Paragraph(f"<b>Période couverte :</b> {date_min} - {date_max}", info_style))
    
    if 'location' in df.columns:
        n_countries = df['location'].nunique()
        elements.append(Paragraph(f"<b>Nombre de pays/régions :</b> {n_countries}", info_style))
    
    elements.append(Spacer(1, 2*inch))
    
    # Pied de page
    footer = Paragraph("Généré automatiquement par Python - Pandas, Matplotlib, ReportLab", 
                      info_style)
    elements.append(footer)
    
    return elements


def create_executive_summary(df, styles, heading_style):
    """Crée le résumé exécutif"""
    elements = []
    
    elements.append(Paragraph("Résumé Exécutif", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Calcul des statistiques clés
    summary_text = "Ce rapport présente une analyse complète des données COVID-19, "
    summary_text += "incluant les statistiques descriptives, les tendances temporelles, "
    summary_text += "et les comparaisons géographiques.<br/><br/>"
    
    # Statistiques principales
    if 'total_cases' in df.columns:
        total_cases = df['total_cases'].max()
        summary_text += f"<b>Cas totaux maximum observé :</b> {total_cases:,.0f}<br/>"
    
    if 'total_deaths' in df.columns:
        total_deaths = df['total_deaths'].max()
        summary_text += f"<b>Décès totaux maximum observé :</b> {total_deaths:,.0f}<br/>"
    
    if 'total_cases' in df.columns and 'total_deaths' in df.columns:
        mortality = (df['total_deaths'].sum() / df['total_cases'].sum()) * 100
        summary_text += f"<b>Taux de mortalité global estimé :</b> {mortality:.2f}%<br/>"
    
    summary_text += "<br/>Les visualisations suivantes illustrent les principales tendances "
    summary_text += "et permettent d'identifier les patterns clés dans l'évolution de la pandémie."
    
    summary_para = Paragraph(summary_text, styles['BodyText'])
    elements.append(summary_para)
    elements.append(Spacer(1, 0.3*inch))
    
    return elements


def create_statistics_section(df, styles, heading_style):
    """Crée la section des statistiques"""
    elements = []
    
    elements.append(Paragraph("Statistiques Descriptives", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Sélection des colonnes numériques
    numeric_cols = df.select_dtypes(include=['number']).columns[:6]  # Top 6 colonnes
    
    if len(numeric_cols) > 0:
        # Création du tableau de statistiques
        stats_data = [['Variable', 'Moyenne', 'Médiane', 'Min', 'Max', 'Écart-type']]
        
        for col in numeric_cols:
            row = [
                col,
                f"{df[col].mean():,.2f}",
                f"{df[col].median():,.2f}",
                f"{df[col].min():,.2f}",
                f"{df[col].max():,.2f}",
                f"{df[col].std():,.2f}"
            ]
            stats_data.append(row)
        
        # Style du tableau
        table = Table(stats_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Texte descriptif
    desc_text = "Le tableau ci-dessus présente les statistiques descriptives des principales "
    desc_text += "variables numériques du dataset. Ces métriques permettent de comprendre "
    desc_text += "la distribution et la variabilité des données."
    
    elements.append(Paragraph(desc_text, styles['BodyText']))
    
    return elements


def create_visualizations_section(figure_files, styles, heading_style):
    """Crée la section des visualisations"""
    elements = []
    
    elements.append(Paragraph("Visualisations Graphiques", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    intro_text = "Les graphiques suivants illustrent différents aspects de l'analyse COVID-19, "
    intro_text += "incluant les tendances temporelles, les comparaisons géographiques, et les "
    intro_text += "distributions statistiques."
    
    elements.append(Paragraph(intro_text, styles['BodyText']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Ajout des images
    for fig_file in figure_files:
        fig_path = f"output/figures/{fig_file}"
        
        if Path(fig_path).exists():
            # Titre de la figure
            fig_title = fig_file.replace('_', ' ').replace('.png', '').title()
            elements.append(Paragraph(fig_title, styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Image (redimensionnée pour tenir sur la page)
            img = Image(fig_path, width=6*inch, height=3*inch)
            elements.append(img)
            elements.append(Spacer(1, 0.3*inch))
            
            # Saut de page après chaque 2 images
            if figure_files.index(fig_file) % 2 == 1 and fig_file != figure_files[-1]:
                elements.append(PageBreak())
    
    return elements


def create_conclusions(df, styles, heading_style):
    """Crée la section des conclusions"""
    elements = []
    
    elements.append(Paragraph("Conclusions et Recommandations", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    conclusion_text = """
    <b>Principales observations :</b><br/><br/>
    
    1. <b>Évolution temporelle :</b> Les données montrent des variations significatives 
    dans l'évolution des cas au fil du temps, reflétant les différentes vagues de la pandémie.<br/><br/>
    
    2. <b>Disparités géographiques :</b> Des différences importantes sont observées entre 
    les pays/régions, influencées par divers facteurs sanitaires, économiques et sociaux.<br/><br/>
    
    3. <b>Tendances statistiques :</b> Les analyses de corrélation et de distribution révèlent 
    des patterns intéressants dans la propagation et l'impact de la pandémie.<br/><br/>
    
    <b>Recommandations :</b><br/><br/>
    
    • Continuer la surveillance épidémiologique avec des mises à jour régulières des données<br/>
    • Approfondir l'analyse des facteurs explicatifs des disparités observées<br/>
    • Développer des modèles prédictifs pour anticiper les évolutions futures<br/>
    • Renforcer la collecte et la qualité des données pour améliorer les analyses<br/><br/>
    
    Ce rapport constitue une base solide pour la prise de décision et l'élaboration 
    de stratégies de santé publique basées sur les données.
    """
    
    elements.append(Paragraph(conclusion_text, styles['BodyText']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Note de fin
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    footer_text = f"Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
    elements.append(Paragraph(footer_text, footer_style))
    
    return elements


# Test du module
if __name__ == "__main__":
    print("=== Test du module report_generator ===\n")
    print("⚠️  Ce module nécessite des données et visualisations")
    print("   Exécutez le pipeline complet avec main.py")
