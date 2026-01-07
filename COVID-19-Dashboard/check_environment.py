"""
Script de vérification de l'environnement
Vérifie que toutes les dépendances sont installées et que l'environnement est prêt
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Vérifie la version de Python"""
    print("🐍 Vérification de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (3.8+ requis)")
        return False


def check_package(package_name, import_name=None):
    """Vérifie si un package est installé"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"   ✅ {package_name}")
        return True
    except ImportError:
        print(f"   ❌ {package_name} (manquant)")
        return False


def check_file_exists(filepath):
    """Vérifie si un fichier existe"""
    if Path(filepath).exists():
        print(f"   ✅ {filepath}")
        return True
    else:
        print(f"   ❌ {filepath} (manquant)")
        return False


def check_directory_exists(dirpath):
    """Vérifie si un dossier existe"""
    if Path(dirpath).exists():
        print(f"   ✅ {dirpath}/")
        return True
    else:
        print(f"   ⚠️  {dirpath}/ (sera créé automatiquement)")
        return True  # Pas critique, sera créé


def main():
    """Fonction principale"""
    print("=" * 70)
    print("  VÉRIFICATION DE L'ENVIRONNEMENT")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # 1. Vérification Python
    print("\n📋 VERSIONS ET PACKAGES")
    print("-" * 70)
    if not check_python_version():
        all_ok = False
    
    # 2. Vérification des packages essentiels
    print("\n📦 PACKAGES PYTHON")
    print("-" * 70)
    
    packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('reportlab', 'reportlab'),
        ('jupyter', 'jupyter'),
    ]
    
    missing_packages = []
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
            all_ok = False
    
    # 3. Vérification de la structure
    print("\n📁 STRUCTURE DU PROJET")
    print("-" * 70)
    
    files_to_check = [
        'main.py',
        'requirements.txt',
        '.gitignore',
    ]
    
    for filepath in files_to_check:
        if not check_file_exists(filepath):
            all_ok = False
    
    # 4. Vérification des dossiers
    print("\n📂 DOSSIERS")
    print("-" * 70)
    
    directories = [
        'scripts',
        'data/raw',
        'data/processed',
        'output/figures',
        'output/reports',
        'notebooks'
    ]
    
    for dirpath in directories:
        check_directory_exists(dirpath)
    
    # 5. Vérification des scripts
    print("\n🔧 SCRIPTS")
    print("-" * 70)
    
    scripts = [
        'scripts/data_loader.py',
        'scripts/data_cleaner.py',
        'scripts/visualizations.py',
        'scripts/report_generator.py',
    ]
    
    for script in scripts:
        if not check_file_exists(script):
            all_ok = False
    
    # Résumé
    print("\n" + "=" * 70)
    if all_ok:
        print("  ✅ ENVIRONNEMENT PRÊT !")
        print("=" * 70)
        print()
        print("💡 Vous pouvez maintenant :")
        print("   • Générer des données : python generate_sample_data.py")
        print("   • Télécharger des données : python download_from_github.py")
        print("   • Lancer l'analyse : python main.py")
        print("   • Exécution automatique : python auto_run.py")
        print()
    else:
        print("  ⚠️  PROBLÈMES DÉTECTÉS")
        print("=" * 70)
        print()
        if missing_packages:
            print("📦 Pour installer les packages manquants :")
            print("   python install_dependencies.py")
            print("   ou")
            print(f"   pip install {' '.join(missing_packages)}")
            print()
        print("💡 Corrigez les problèmes ci-dessus puis relancez ce script")
        print()
    
    return all_ok


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erreur lors de la vérification : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


