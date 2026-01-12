# 🔧 Guide de Dépannage - COVID-19 Dashboard

## ❌ Problème : "⚠️ Impossible de charger les modules"

### 🔍 Causes possibles

1. **Le dossier `scripts/` n'existe pas ou est mal placé**
2. **Les fichiers Python dans `scripts/` sont manquants**
3. **Le fichier `__init__.py` n'existe pas dans `scripts/`**
4. **Problème de chemins relatifs**

---

## ✅ Solutions Étape par Étape

### Solution 1 : Vérifier la structure des dossiers

```bash
# Depuis la racine du projet COVID-19-Dashboard/

# Afficher la structure
ls -la scripts/

# Vous devriez voir :
# scripts/
# ├── __init__.py          # ⚠️ IMPORTANT
# ├── data_loader.py
# ├── data_cleaner.py
# ├── visualizations.py
# └── report_generator.py
```

### Solution 2 : Créer le fichier `__init__.py`

```bash
# Créer un fichier __init__.py vide dans scripts/
touch scripts/__init__.py

# Ou avec contenu (recommandé) - copier le fichier fourni
```

**Contenu minimal de `scripts/__init__.py` :**

```python
"""Module scripts"""
from .data_loader import load_covid_data
from .data_cleaner import clean_covid_data
```

### Solution 3 : Vérifier les imports dans vos fichiers

**Dans chaque page Streamlit, vérifiez que vous avez :**

```python
import sys
import os

# Obtenir le répertoire parent (racine du projet)
parent_dir = os.path.dirname(os.path.dirname(__file__))
scripts_dir = os.path.join(parent_dir, 'scripts')

# Ajouter au PATH
sys.path.insert(0, parent_dir)
sys.path.insert(0, scripts_dir)

# Importer
try:
    from scripts.data_loader import load_covid_data
    from scripts.data_cleaner import clean_covid_data
except ImportError as e:
    st.error(f"⚠️ Erreur d'import: {e}")
    st.stop()
```

### Solution 4 : Tester les imports manuellement

```bash
# Depuis la racine du projet
python -c "from scripts.data_loader import load_covid_data; print('✅ Import OK')"

# Si erreur, vérifier :
# 1. Que scripts/data_loader.py existe
# 2. Qu'il n'y a pas d'erreurs de syntaxe dans le fichier
# 3. Que toutes les dépendances sont installées
```

---

## 🐍 Vérifier l'environnement Python

### Vérifier que vous êtes dans le bon environnement

```bash
# Afficher le chemin Python utilisé
which python
# ou
where python  # Windows

# Afficher la version
python --version

# Lister les packages installés
pip list | grep -E "(pandas|numpy|streamlit)"
```

### Réinstaller les dépendances

```bash
# Méthode 1 : Depuis requirements
pip install -r requirements_updated.txt

# Méthode 2 : Manuellement
pip install pandas numpy streamlit plotly

# Méthode 3 : Avec upgrade
pip install --upgrade pandas numpy streamlit plotly
```

---

## 📂 Vérifier les chemins de fichiers

### Script de diagnostic

Créez un fichier `test_imports.py` à la racine :

```python
import os
import sys

print("=== DIAGNOSTIC DES IMPORTS ===\n")

# 1. Chemin actuel
print(f"📂 Répertoire actuel: {os.getcwd()}")

# 2. Vérifier que scripts/ existe
scripts_path = os.path.join(os.getcwd(), 'scripts')
print(f"\n📂 Dossier scripts/: {'✅ Existe' if os.path.exists(scripts_path) else '❌ Manquant'}")

# 3. Lister les fichiers dans scripts/
if os.path.exists(scripts_path):
    files = os.listdir(scripts_path)
    print(f"\n📄 Fichiers dans scripts/:")
    for f in files:
        print(f"   - {f}")

# 4. Tester les imports
print("\n🔍 Test des imports:")

try:
    sys.path.insert(0, scripts_path)
    from scripts.data_loader import load_covid_data
    print("   ✅ data_loader.py - OK")
except Exception as e:
    print(f"   ❌ data_loader.py - ERREUR: {e}")

try:
    from scripts.data_cleaner import clean_covid_data
    print("   ✅ data_cleaner.py - OK")
except Exception as e:
    print(f"   ❌ data_cleaner.py - ERREUR: {e}")

try:
    from scripts.visualizations import create_all_visualizations
    print("   ✅ visualizations.py - OK")
except Exception as e:
    print(f"   ❌ visualizations.py - ERREUR: {e}")

try:
    from scripts.report_generator import generate_report
    print("   ✅ report_generator.py - OK")
except Exception as e:
    print(f"   ❌ report_generator.py - ERREUR: {e}")

print("\n=== FIN DU DIAGNOSTIC ===")
```

**Exécutez :**

```bash
python test_imports.py
```

---

## 🚨 Erreurs Spécifiques et Solutions

### Erreur : "No module named 'scripts'"

**Solution :**

```bash
# Créer __init__.py dans scripts/
echo "" > scripts/__init__.py

# Ou vérifier que vous êtes à la racine du projet
pwd  # Doit afficher .../COVID-19-Dashboard/
```

### Erreur : "No module named 'pandas'" (ou numpy, etc.)

**Solution :**

```bash
# Réinstaller les dépendances
pip install pandas numpy matplotlib seaborn
```

### Erreur : "cannot import name 'load_covid_data'"

**Solutions :**

1. Vérifier que `data_loader.py` contient bien la fonction `load_covid_data()`
2. Vérifier qu'il n'y a pas d'erreurs de syntaxe
3. Essayer d'exécuter le fichier directement :

```bash
python scripts/data_loader.py
```

### Erreur : "Streamlit ne trouve pas les pages"

**Solution :**

```bash
# Vérifier la structure du dossier pages/
ls -la pages/

# Les noms DOIVENT commencer par un chiffre + émoji
# Correct : 01_🗺️_Carte_Mondiale.py
# Incorrect : carte_mondiale.py
```

---

## 🔄 Redémarrage Complet

Si rien ne fonctionne, essayez un redémarrage complet :

```bash
# 1. Arrêter Streamlit (Ctrl+C)

# 2. Nettoyer le cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 3. Nettoyer le cache Streamlit
rm -rf .streamlit/cache

# 4. Réinstaller les dépendances
pip uninstall -y streamlit pandas numpy
pip install streamlit pandas numpy plotly

# 5. Relancer
streamlit run app.py
```

---

## 📊 Vérification Complète de la Structure

### Checklist finale

```bash
# ✅ Structure correcte
COVID-19-Dashboard/
├── app.py                          # ✅ À la racine
├── pages/                          # ✅ Dossier pages/
│   ├── 01_🗺️_Carte_Mondiale.py
│   ├── 02_📊_Analyses_Avancées.py
│   └── 03_📄_Rapports_PDF.py
├── scripts/                        # ✅ Dossier scripts/
│   ├── __init__.py                 # ⚠️ IMPORTANT
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── visualizations.py
│   └── report_generator.py
└── data/                           # ✅ Dossier data/
    ├── raw/
    └── processed/
```

### Commande de vérification automatique

**Windows (PowerShell) :**

```powershell
# Créer un script de vérification
@'
🔍 Vérification de la structure...

# Fonction de vérification
function check-file { param($path) if (Test-Path $path) { "✅ $path" } else { "❌ $path - MANQUANT" } }
function check-dir { param($path) if (Test-Path $path -PathType Container) { "✅ $path\" } else { "❌ $path\ - MANQUANT" } }

# Vérifications
check-file "app.py"
check-dir "pages"
check-file "pages\01_🗺️_Carte_Mondiale.py"
check-file "pages\02_📊_Analyses_Avancées.py"
check-file "pages\03_📄_Rapports_PDF.py"
check-dir "scripts"
check-file "scripts\__init__.py"
check-file "scripts\data_loader.py"
check-file "scripts\data_cleaner.py"
check-file "scripts\visualizations.py"
check-file "scripts\report_generator.py"
check-dir "data"
check-dir "data\raw"
check-dir "data\processed"

""
"📊 Si tout est ✅, le dashboard devrait fonctionner"
'@ | Out-File -FilePath check_structure.ps1 -Encoding UTF8

# Exécuter
.\check_structure.ps1
```

**Linux/Mac :**

```bash
# Créer un script de vérification
cat > check_structure.sh << 'EOF'
#!/bin/bash
echo "🔍 Vérification de la structure..."

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 - MANQUANT"
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ $1/ - MANQUANT"
    fi
}

check_file "app.py"
check_dir "pages"
check_file "pages/01_🗺️_Carte_Mondiale.py"
check_file "pages/02_📊_Analyses_Avancées.py"
check_file "pages/03_📄_Rapports_PDF.py"
check_dir "scripts"
check_file "scripts/__init__.py"
check_file "scripts/data_loader.py"
check_file "scripts/data_cleaner.py"
check_file "scripts/visualizations.py"
check_file "scripts/report_generator.py"
check_dir "data"
check_dir "data/raw"
check_dir "data/processed"

echo ""
echo "📊 Si tout est ✅, le dashboard devrait fonctionner"
EOF

chmod +x check_structure.sh
./check_structure.sh
```

---

## 💡 Astuces Supplémentaires

### Activer le mode Debug de Streamlit

```bash
# Lancer avec logs détaillés
streamlit run app.py --logger.level=debug
```

### Vérifier les permissions

```bash
# Linux/Mac - Donner les permissions
chmod +x app.py
chmod -R 755 scripts/
chmod -R 755 pages/
```

### Utiliser un environnement virtuel

```bash
# Créer un environnement propre
python -m venv venv_dashboard

# Activer
source venv_dashboard/bin/activate  # Linux/Mac
venv_dashboard\Scripts\activate     # Windows

# Installer
pip install -r requirements_updated.txt

# Lancer
streamlit run app.py
```

---

## 📞 Besoin d'Aide Supplémentaire ?

### Informations à fournir

Si le problème persiste, fournissez :

1. **Sortie de la commande :**

```bash
python test_imports.py
```

2. **Votre structure :**

```bash
tree -L 2  # ou ls -R
```

3. **Versions installées :**

```bash
pip list | grep -E "(streamlit|pandas|numpy|plotly)"
```

4. **Message d'erreur complet** de Streamlit

---

## ✅ Solution Rapide Finale

**Si vraiment rien ne fonctionne, essayez cette configuration minimale :**

1. **Créez `scripts/__init__.py` avec ce contenu :**

```python
from .data_loader import load_covid_data
from .data_cleaner import clean_covid_data
```

2. **Dans CHAQUE page (01, 02, 03), remplacez les imports par :**

```python
import sys
import os

# Configuration des chemins
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

# Imports
try:
    from scripts.data_loader import load_covid_data
    from scripts.data_cleaner import clean_covid_data
except ImportError as e:
    import streamlit as st
    st.error(f"❌ Erreur: {e}")
    st.info("Vérifiez que scripts/__init__.py existe")
    st.stop()
```

3. **Relancez :**

```bash
streamlit run app.py
```

---

**Ça devrait fonctionner maintenant ! 🚀**
