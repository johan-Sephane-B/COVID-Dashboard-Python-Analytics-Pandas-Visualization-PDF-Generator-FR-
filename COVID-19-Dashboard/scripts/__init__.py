"""
Module scripts - COVID-19 Dashboard
Import automatique depuis data_utils (wrapper universel)
"""

# Importer depuis le wrapper universel
try:
    from .data_utils import (
        load_covid_data,
        clean_covid_data,
        clean_data,
        create_all_visualizations,
        generate_report,
        generate_html_report,
        generate_pdf_report
    )
    
    __all__ = [
        'load_covid_data',
        'clean_covid_data',
        'clean_data',
        'create_all_visualizations',
        'generate_report',
        'generate_html_report',
        'generate_pdf_report'
    ]
    
    print("✅ Imports depuis data_utils réussis")
    
except ImportError as e:
    print(f"⚠️ Erreur d'import data_utils: {e}")
    print("   Tentative d'import depuis les modules originaux...")
    
    # Fallback vers les modules originaux
    try:
        from .data_loader import load_covid_data
        from .data_cleaner import clean_covid_data
        print("✅ Import data_loader et data_cleaner OK")
    except ImportError:
        print("❌ Impossible d'importer les fonctions de base")
    
    try:
        from .visualizations import create_all_visualizations
        print("✅ Import visualizations OK")
    except ImportError:
        print("⚠️ visualizations non disponible")
    
    try:
        from .report_generator import generate_report
        print("✅ Import report_generator OK")
    except ImportError:
        print("⚠️ report_generator non disponible")
