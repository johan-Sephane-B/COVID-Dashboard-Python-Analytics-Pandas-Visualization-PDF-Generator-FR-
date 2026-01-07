"""
Script d'installation automatique des dépendances
Exécutez ce script pour installer toutes les bibliothèques nécessaires
"""

import subprocess
import sys

def install_package(package):
    """Installe un package Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 60)
    print("  INSTALLATION DES DÉPENDANCES - COVID-19 DASHBOARD")
    print("=" * 60)
    print()
    
    packages = [
        ("pandas", "pandas>=2.0.0"),
        ("matplotlib", "matplotlib>=3.7.0"),
        ("seaborn", "seaborn>=0.12.0"),
        ("reportlab", "reportlab>=4.0.0"),
        ("numpy", "numpy>=1.24.0"),
        ("jupyter", "jupyter>=1.0.0"),
        ("scipy", "scipy>=1.10.0")
    ]
    
    installed = []
    failed = []
    
    for name, package in packages:
        print(f"📦 Installation de {name}...", end=" ")
        
        # Vérifier si déjà installé
        try:
            __import__(name)
            print("✅ Déjà installé")
            installed.append(name)
            continue
        except ImportError:
            pass
        
        # Installer
        if install_package(package):
            print("✅ Installé avec succès")
            installed.append(name)
        else:
            print("❌ Échec")
            failed.append(name)
    
    print("\n" + "=" * 60)
    print("  RÉSUMÉ DE L'INSTALLATION")
    print("=" * 60)
    print(f"\n✅ Installés avec succès : {len(installed)}/{len(packages)}")
    for pkg in installed:
        print(f"   ✓ {pkg}")
    
    if failed:
        print(f"\n❌ Échecs : {len(failed)}")
        for pkg in failed:
            print(f"   ✗ {pkg}")
        print("\n💡 Pour installer manuellement :")
        print(f"   pip install {' '.join(failed)}")
    else:
        print("\n🎉 Toutes les dépendances sont installées !")
        print("\n✅ Vous pouvez maintenant exécuter :")
        print("   python main.py")
    
    print()

if __name__ == "__main__":
    main()


