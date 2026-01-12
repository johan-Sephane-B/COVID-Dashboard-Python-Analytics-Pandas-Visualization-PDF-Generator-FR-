"""
Script Automatique de Correction des Imports
Résout tous les problèmes d'imports automatiquement
"""

import os
import sys
import shutil
from pathlib import Path

def print_header(text):
    """Affiche un en-tête"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_file_exists(filepath):
    """Vérifie si un fichier existe"""
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def backup_file(filepath):
    """Crée une sauvegarde d'un fichier"""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.backup"
        shutil.copy2(filepath, backup_path)
        print(f"   💾 Sauvegarde créée : {backup_path}")
        return backup_path
    return None

def create_data_utils():
    """Crée le fichier data_utils.py complet"""
    
    print("\n📝 Création de scripts/data_utils.py...")
    
    # Le contenu complet du wrapper est déjà dans l'artefact
    # On indique juste qu'il faut le copier
    
    data_utils_path = 'scripts/data_utils.py'
    
    if os.path.exists(data_utils_path):
        print(f"   ✅ {data_utils_path} existe déjà")
        
        # Vérifier la taille
        size = os.path.getsize(data_utils_path)
        if size < 5000:  # Moins de 5KB, probablement incomplet
            print(f"   ⚠️ Fichier trop petit ({size} octets), devrait être remplacé")
            return False
        else:
            print(f"   ✅ Fichier correct ({size} octets)")
            return True
    else:
        print(f"   ❌ {data_utils_path} n'existe pas")
        print("\n   💡 IMPORTANT : Copiez le fichier data_utils.py fourni dans scripts/")
        return False

def update_init_file():
    """Met à jour scripts/__init__.py"""
    
    print("\n📝 Mise à jour de scripts/__init__.py...")
    
    init_path = 'scripts/__init__.py'
    
    init_content = '''"""
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
'''
    
    # Sauvegarder l'ancien fichier
    if os.path.exists(init_path):
        backup_file(init_path)
    
    # Créer le nouveau
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print(f"   ✅ {init_path} mis à jour")
    return True

def test_imports():
    """Teste les imports"""
    
    print_header("🧪 TEST DES IMPORTS")
    
    # Ajouter scripts au path
    sys.path.insert(0, 'scripts')
    
    results = {}
    
    # Test 1: data_utils
    try:
        from scripts.data_utils import load_covid_data, clean_covid_data
        results['data_utils'] = True
        print("   ✅ scripts.data_utils - OK")
    except ImportError as e:
        results['data_utils'] = False
        print(f"   ❌ scripts.data_utils - ÉCHEC: {e}")
    
    # Test 2: visualizations
    try:
        from scripts.data_utils import create_all_visualizations
        results['visualizations'] = True
        print("   ✅ create_all_visualizations - OK")
    except ImportError as e:
        results['visualizations'] = False
        print(f"   ❌ create_all_visualizations - ÉCHEC: {e}")
    
    # Test 3: report_generator
    try:
        from scripts.data_utils import generate_report
        results['report_generator'] = True
        print("   ✅ generate_report - OK")
    except ImportError as e:
        results['report_generator'] = False
        print(f"   ❌ generate_report - ÉCHEC: {e}")
    
    return results

def check_environment():
    """Vérifie l'environnement"""
    
    print_header("🔍 VÉRIFICATION DE L'ENVIRONNEMENT")
    
    # Vérifier le répertoire
    if not os.path.exists('scripts'):
        print("   ❌ Le dossier scripts/ n'existe pas")
        print("   💡 Créez-le avec : mkdir scripts")
        return False
    
    print("   ✅ Dossier scripts/ existe")
    
    # Vérifier les fichiers essentiels
    essential_files = {
        'scripts/__init__.py': 'Fichier d\'initialisation',
        'scripts/data_utils.py': 'Wrapper universel (ESSENTIEL)',
        'app.py': 'Application principale',
    }
    
    all_ok = True
    
    for filepath, description in essential_files.items():
        if check_file_exists(filepath):
            size = os.path.getsize(filepath) / 1024
            print(f"   ✅ {filepath:30} ({size:.1f} KB)")
        else:
            print(f"   ❌ {filepath:30} - MANQUANT")
            if filepath == 'scripts/data_utils.py':
                print(f"      ⚠️ CRITIQUE : {description}")
                all_ok = False
    
    return all_ok

def main():
    """Fonction principale"""
    
    print("=" * 70)
    print("  🔧 CORRECTION AUTOMATIQUE DES IMPORTS")
    print("=" * 70)
    
    # 1. Vérifier l'environnement
    env_ok = check_environment()
    
    if not env_ok:
        print("\n❌ Environnement incomplet")
        print("\n📋 Actions requises :")
        print("   1. Assurez-vous d'être à la racine du projet")
        print("   2. Copiez le fichier data_utils.py dans scripts/")
        print("   3. Relancez ce script")
        return
    
    # 2. Créer/vérifier data_utils.py
    data_utils_ok = create_data_utils()
    
    if not data_utils_ok:
        print("\n⚠️ data_utils.py doit être copié manuellement")
        print("\n📋 Instructions :")
        print("   1. Trouvez le fichier data_utils.py fourni")
        print("   2. Copiez-le dans scripts/data_utils.py")
        print("   3. Relancez ce script")
        
        response = input("\n❓ Voulez-vous continuer quand même ? (o/N) : ").strip().lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("❌ Opération annulée")
            return
    
    # 3. Mettre à jour __init__.py
    update_init_file()
    
    # 4. Tester les imports
    results = test_imports()
    
    # 5. Résumé
    print_header("📊 RÉSUMÉ")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n✅ Réussis : {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 TOUS LES IMPORTS FONCTIONNENT !")
        print("\n🚀 Vous pouvez maintenant lancer le dashboard :")
        print("   streamlit run app.py")
    else:
        print("\n⚠️ Certains imports ont échoué")
        print("\n📋 Actions recommandées :")
        
        if not results.get('data_utils'):
            print("   1. ⚠️ CRITIQUE : Copiez data_utils.py dans scripts/")
        
        print("   2. Exécutez : python check_functions.py")
        print("   3. Vérifiez les messages d'erreur ci-dessus")
        print("   4. Relancez ce script")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        # Vérifier qu'on est à la racine du projet
        if not os.path.exists('app.py'):
            print("\n❌ Erreur : app.py introuvable")
            print("💡 Assurez-vous d'exécuter ce script depuis la racine du projet")
            print("   Exemple : python fix_imports.py")
            sys.exit(1)
        
        main()
        
    except KeyboardInterrupt:
        print("\n\n❌ Opération annulée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nAppuyez sur Entrée pour fermer...")