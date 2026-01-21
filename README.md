# Epi Analytics

[![PyPI version](https://img.shields.io/pypi/v/epi-analytics)](https://pypi.org/project/epi-analytics/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

**La boîte à outils Data Science pour l'analyse épidémiologique.**
*Apprenez l'analyse de données en manipulant des données réelles de pandémie.*

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Démo](#-démo)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [Tests](#-tests)
- [Contribution](#-contribution)
- [License](#-license)

---

## 🎯 À propos

**Epi Analytics** est conçu pour les étudiants, data scientists juniors et éducateurs qui cherchent un moyen pratique d'apprendre l'analyse de données (Pandas) et la visualisation (Plotly) via un cas d'usage concret : l'épidémiologie COVID-19.

Contrairement aux datasets statiques, ce projet fournit une couche d'abstraction simple pour récupérer, nettoyer et visualiser des données en temps réel, accompagnée d'un dashboard interactif prêt à l'emploi.

**Pourquoi ce projet ?**
Fournir un support pédagogique "clé en main" qui dépasse le simple "Hello World" de la data science, en offrant une structure de projet professionnelle (tests, typage, CI/CD).

---

## ✨ Fonctionnalités

✅ **Chargement Automatique** : Récupération intelligente des données depuis *Our World in Data* avec mise en cache locale.
✅ **Nettoyage Robuste** : Pipelines de traitement pour gérer les valeurs manquantes et incohérentes.
✅ **Visualisation Interactive** : Wrappers simples autour de Plotly pour créer des courbes épidémiques et des cartes.
✅ **Dashboard Streamlit** : Application web complète incluse pour explorer les données sans coder.
✅ **Rapports PDF** : (En cours) Module de génération de rapports automatisés.

---

## 🎬 Démo

### Dashboard Interactif
Lancez l'application Streamlit incluse pour explorer les données visuellement :

![Dashboard Preview](https://raw.githubusercontent.com/covid-analytics/assets/main/dashboard_preview_v2.png)
*(Note: Capture d'écran représentative)*

---

## 📦 Prérequis

- **Python** 3.9 ou supérieur
- **Git** (pour cloner le projet)
- Connexion internet (pour le premier téléchargement des données)

Systèmes supportés :
✅ Windows (PowerShell / CMD / WSL2)
✅ macOS
✅ Linux

---

## � Installation

### 1. Installation Standard (Utilisateur)
Si vous souhaitez juste utiliser la librairie dans vos scripts :

```bash
pip install epi-analytics
```

### 2. Installation Complète (Développeur / Dashboard)
Pour lancer le dashboard ou contribuer au code :

```bash
# Cloner le repository
git clone https://github.com/votre-username/epi-analytics.git
cd epi-analytics

# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement
# Windows :
.\venv\Scripts\Activate
# Linux/Mac :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## 💻 Utilisation

### Mode Librairie (Script Python)

```python
from epi_analytics import load_data, analyze, visualize

# 1. Charger les données (auto-cache)
df = load_data()

# 2. Analyser un pays
stats = analyze(df, country="France", metric="mortality")
print(f"Taux de mortalité actuel : {stats['mortality_rate']:.2f}%")

# 3. Visualiser
fig = visualize(df, 
    chart_type="timeline", 
    countries=["France", "Germany"],
    metric="new_cases"
)
fig.show()
```

### Mode Dashboard (Application Web)

Une fois installé, lancez le dashboard localement :

```bash
# Depuis la racine du projet
streamlit run app.py
```
Accédez ensuite à `http://localhost:8501` dans votre navigateur.

---

## ⚙️ Configuration

Le projet utilise un système de configuration par variables d'environnement (si nécessaire) ou arguments par défaut.

| Variable | Description | Défaut |
|---|---|---|
| `DATA_CACHE_DIR` | Dossier de stockage des données | `./data/cache` |
| `REFRESH_INTERVAL` | Temps avant re-téléchargement (heures) | `24` |

---

## �️ Architecture

```
epi-analytics/
├── app.py                 # Point d'entrée Dashboard Streamlit
├── src/                   # (Legacy) Code source en migration
├── src_new/               # Code source de la librairie cible
│   └── epi_analytics/
│       ├── data.py        # Logique de chargement
│       ├── metrics.py     # Calculs statistiques
│       └── viz.py         # Visualisations Plotly
├── scripts/               # Scripts utilitaires (clean, data gen)
├── tests_new/             # Tests unitaires Pytest
├── data/                  # Stockage local (raw/processed)
└── pages/                 # Pages additionnelles Streamlit
```

---

## 🧪 Tests

Le projet vise une couverture de test > 80%. Pour lancer les tests :

```bash
# Lancer tous les tests
pytest

# Avec rapport de couverture
pytest --cov=epi_analytics --cov-report=html
```

---

## � Déploiement

Le dashboard est prêt à être déployé sur **Streamlit Community Cloud** :

1. Forkez ce repo sur GitHub.
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io).
3. Sélectionnez votre repo et le fichier principal `app.py`.
4. Cliquez sur **Deploy** !

---

## 🤝 Contribution

Les contributions sont les bienvenues, surtout en cette phase Beta !

1. **Fork** le projet
2. Créez votre branche (`git checkout -b featured/MaSuperFeature`)
3. **Commit** vos changements (`git commit -m 'Add: MaSuperFeature'`)
4. **Push** (`git push origin featured/MaSuperFeature`)
5. Ouvrez une **Pull Request**

Veuillez consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails.

---

## �️ Roadmap

- [x] Phase 0 : Validation et Proof of Concept `app.py`
- [ ] Phase 1 : Migration complète vers `src_new/`
- [ ] Phase 2 : Documentation complète et Type Hinting strict
- [ ] Phase 3 : Publication sur PyPI

---

## � License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Auteurs

**BAHOU Johan Stéphane**
*email:stephanejohanbahou@gmail.com*

---

*Dernière mise à jour : 21 Janvier 2026*
