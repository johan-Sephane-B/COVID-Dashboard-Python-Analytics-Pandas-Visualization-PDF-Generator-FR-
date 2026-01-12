"""
Script de Lancement Rapide du Dashboard
Vérifie tout et lance automatiquement le dashboard Streamlit
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header():
    """Affiche l'en-tête"""
    print("=" * 70)
    print("🦠 COVID-19 DASHBOARD - LANCEMENT RAPIDE")
    print("=" * 70)
    print()


def check_python_version():
    """Vérifie la version de Python"""
    print("🔍 Vérification de Python...")
    version = sys.version_info

    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Version trop ancienne")
        print("   Requis : Python 3.8 ou supérieur")
        return False


def check_dependencies():
    """Vérifie les dépendances requises"""
    print("\n🔍 Vérification des dépendances...")

    required = {
        'streamlit': 'Interface web',
        'plotly': 'Graphiques interactifs',
        'pandas': 'Manipulation de données',
        'numpy': 'Calculs numériques'
    }

    missing = []

    for package, description in required.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - MANQUANT")
            missing.append(package)

    if missing:
        print(f"\n⚠️  {len(missing)} dépendance(s) manquante(s)")
        print("\nPour installer :")
        print(f"   pip install {' '.join(missing)}")
        return False

    return True


def check_project_structure():
    """Vérifie la structure du projet"""
    print("\n🔍 Vérification de la structure du projet...")

    required_files = {
        'app.py': 'Application principale',
        'scripts/data_loader.py': 'Module de chargement',
        'scripts/data_cleaner.py': 'Module de nettoyage'
    }

    required_dirs = {
        'data': 'Dossier de données',
        'output': 'Dossier de sortie',
        'pages': 'Pages du dashboard'
    }

    all_ok = True

    # Vérifier les fichiers
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path:30} - {description}")
        else:
            print(f"❌ {file_path:30} - MANQUANT")
            all_ok = False

    # Vérifier les dossiers
    for dir_path, description in required_dirs.items():
        if os.path.exists(dir_path):
            print(f"✅ {dir_path:30} - {description}")
        else:
            print(f"⚠️  {dir_path:30} - Création...")
            os.makedirs(dir_path, exist_ok=True)

    return all_ok


def check_data():
    """Vérifie la présence de données"""
    print("\n🔍 Vérification des données...")

    data_paths = [
        'data/processed/covid_cleaned.csv',
        'data/raw/covid_data.csv'
    ]

    for path in data_paths:
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024 * 1024)  # en MB
            print(f"✅ {path:40} ({size:.1f} MB)")
            return True

    print("❌ Aucun fichier de données trouvé")
    print("\n💡 Solutions :")
    print("   1. Générer des données synthétiques :")
    print("      python generate_sample_data.py")
    print("\n   2. Télécharger des données réelles :")
    print("      python download_from_github.py")

    return False


def create_config():
    """Crée le fichier de configuration Streamlit"""
    print("\n🔧 Configuration de Streamlit...")

    config_dir = Path(".streamlit")
    config_file = config_dir / "config.toml"

    if not config_dir.exists():
        config_dir.mkdir()
        print("✅ Dossier .streamlit créé")

    if not config_file.exists():
        config_content = """[theme]
primaryColor = "#667eea"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#2c3e50"
font = "sans serif"

[server]
headless = false
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
"""
        config_file.write_text(config_content)
        print("✅ Fichier config.toml créé")
    else:
        print("✅ Configuration existante trouvée")

    return True


def launch_dashboard():
    """Lance le dashboard Streamlit"""
    print("\n" + "=" * 70)
    print("🚀 LANCEMENT DU DASHBOARD")
    print("=" * 70)
    print("\n⏳ Démarrage de Streamlit...")
    print("📱 Le dashboard s'ouvrira automatiquement dans votre navigateur")
    print("🌐 URL : http://localhost:8501")
    print("\n💡 Pour arrêter : Ctrl+C dans ce terminal")
    print("\n" + "=" * 70 + "\n")

    try:
        subprocess.run(['streamlit', 'run', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard arrêté proprement")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors du lancement : {e}")
        return False
    except FileNotFoundError:
        print("\n❌ Streamlit n'est pas installé ou pas dans le PATH")
        print("   Installez avec : pip install streamlit")
        return False

    return True


def show_manual_start():
    """Affiche les instructions de lancement manuel"""
    print("\n" + "=" * 70)
    print("📋 LANCEMENT MANUEL")
    print("=" * 70)
    print("\n1️⃣  Installez les dépendances manquantes :")
    print("   pip install streamlit plotly pandas numpy")
    print("\n2️⃣  Générez des données (si nécessaire) :")
    print("   python generate_sample_data.py")
    print("\n3️⃣  Lancez le dashboard :")
    print("   streamlit run app.py")
    print("\n" + "=" * 70 + "\n")


def main():
    """Fonction principale"""
    print_header()

    # Vérifications
    checks = [
        ("Python", check_python_version()),
        ("Dépendances", check_dependencies()),
        ("Structure", check_project_structure()),
        ("Données", check_data()),
        ("Configuration", create_config())
    ]

    # Résumé des vérifications
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES VÉRIFICATIONS")
    print("=" * 70)

    for name, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name:20} {'OK' if status else 'PROBLÈME'}")

    # Décision de lancement
    all_ok = all(status for _, status in checks)

    if all_ok:
        print("\n✅ Toutes les vérifications sont passées !")

        # Demander confirmation
        try:
            response = input("\n🚀 Lancer le dashboard maintenant ? (O/n) : ").strip().lower()
            if response in ['', 'o', 'oui', 'y', 'yes']:
                launch_dashboard()
            else:
                print("\n📝 Pour lancer plus tard, utilisez :")
                print("   streamlit run app.py")
        except KeyboardInterrupt:
            print("\n\n✅ Annulé par l'utilisateur")

    else:
        print("\n⚠️  Certaines vérifications ont échoué")
        show_manual_start()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Au revoir !")
        input("\nAppuyez sur Entrée pour fermer...")