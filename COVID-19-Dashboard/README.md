# 🚀 Guide d'Installation - COVID-19 Dashboard Streamlit

## 📋 Table des Matières

1. [Installation des Dépendances](#installation)
2. [Structure du Projet](#structure)
3. [Lancement du Dashboard](#lancement)
4. [Fonctionnalités](#fonctionnalités)
5. [Résolution de Problèmes](#problemes)

---

## 🔧 Installation des Dépendances {#installation}

### Étape 1 : Mettre à jour requirements.txt

Remplacez votre fichier `requirements.txt` par celui fourni ou ajoutez ces lignes :

```bash
# Nouvelles dépendances pour le dashboard
streamlit>=1.32.0
plotly>=5.18.0
kaleido>=0.2.1
pycountry>=23.12.11
country-converter>=1.2
```

### Étape 2 : Installer les dépendances

```bash
# Avec pip
pip install -r requirements_updated.txt

# Ou manuellement
pip install streamlit plotly kaleido pycountry country-converter
```

### Étape 3 : Vérifier l'installation

```bash
streamlit --version
```

Vous devriez voir : `Streamlit, version 1.32.0` (ou supérieur)

---

## 📂 Structure du Projet {#structure}

Créez cette nouvelle structure dans votre projet existant :

```
COVID-19-Dashboard/
│
├── main.py                         # ✨ NOUVEAU - Application principale
│
├── pages/                          # ✨ NOUVEAU - Pages multiples
│   ├── 01_🗺️_Carte_Mondiale.py
│   ├── 02_📊_Analyses_Avancées.py
│   └── 03_📄_Rapports_PDF.py
│
├── assets/                         # ✨ NOUVEAU - Ressources
│   └── styles.css
│
├── scripts/                        # ✅ Existants (conservés)
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── visualizations.py
│   └── report_generator.py
│
├── data/
│   ├── raw/
│   └── processed/
│
└── output/
    ├── figures/
    └── reports/
```

### 📝 Fichiers à créer :

1. **main.py** (racine du projet)
2. **pages/** (dossier à créer)
   - 01_🗺️_Carte_Mondiale.py
   - 02_📊_Analyses_Avancées.py
   - 03_📄_Rapports_PDF.py
3. **assets/** (dossier à créer)
   - styles.css

---

## 🎮 Lancement du Dashboard {#lancement}

### Méthode 0 : Lancement Automatique (Recommandé) ⭐

Pour une expérience optimale, utilisez le script de lancement rapide qui vérifie automatiquement tout :

```bash
# Depuis la racine du projet
python quick_start.py
```

**Ce que fait le script :**

- ✅ Vérifie la version de Python (3.8+ requis)
- ✅ Contrôle toutes les dépendances installées
- ✅ Valide la structure du projet
- ✅ Vérifie la présence des données
- ✅ Crée la configuration Streamlit automatiquement
- ✅ Lance le dashboard avec confirmation

### Méthode 1 : Lancement Standard

```bash
# Depuis la racine du projet
streamlit run app.py
```

### Méthode 2 : Avec Port Personnalisé

```bash
streamlit run app.py --server.port 8501
```

### Méthode 3 : En Mode Production

```bash
streamlit run app.py --server.headless true
```

### 🌐 Accès au Dashboard

Une fois lancé, ouvrez votre navigateur à :

- **Local :** http://localhost:8501
- **Réseau :** http://[votre-ip]:8501

---

## ✨ Fonctionnalités Disponibles {#fonctionnalités}

### 🏠 Page Principale (main.py)

- ✅ KPIs globaux en temps réel
- ✅ Timeline animée interactive
- ✅ Filtres multi-pays
- ✅ Sélection de plages de dates
- ✅ Graphiques Plotly interactifs (zoom, hover, export)

### 🗺️ Carte Mondiale

- ✅ Carte choroplèthe mondiale
- ✅ Sélecteur de métriques (cas, décès, vaccination)
- ✅ Curseur temporel (explorer jour par jour)
- ✅ 7 projections géographiques différentes
- ✅ 7 palettes de couleurs
- ✅ Top 10 pays dynamique
- ✅ Graphiques en barres interactifs

### 📊 Analyses Avancées

- ✅ Comparaison multi-pays (3 onglets)
- ✅ Taux de croissance calculé
- ✅ Matrice de corrélation interactive
- ✅ Distribution des nouveaux cas (histogramme + box plot)
- ✅ Analyse du taux de mortalité
- ✅ Progression de la vaccination
- ✅ Tableau récapitulatif exportable (CSV)

### 📄 Génération de Rapports

- ✅ Configuration personnalisée du rapport
- ✅ Sélection des pays et dates
- ✅ Options avancées (stats, graphiques, tables)
- ✅ Génération PDF/HTML depuis l'interface
- ✅ Barre de progression en temps réel
- ✅ Téléchargement direct depuis le navigateur
- ✅ Historique des rapports générés

---

## 🎨 Personnalisation

### Modifier le Thème

Éditez `.streamlit/config.toml` (à créer) :

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#2c3e50"
font = "sans serif"
```

### Modifier les Couleurs des Graphiques

Dans chaque page, changez les paramètres `color_continuous_scale` :

```python
# Exemples de palettes
color_continuous_scale='Viridis'  # Violet-jaune
color_continuous_scale='Reds'     # Rouge
color_continuous_scale='Blues'    # Bleu
color_continuous_scale='YlOrRd'   # Jaune-Orange-Rouge
```

---

## 🔍 Navigation dans le Dashboard

### Menu Latéral (Sidebar)

- 🎛️ Filtres globaux
- 📅 Sélection de dates
- 🌍 Choix des pays
- 📊 Métriques à afficher

### Pages Multiples

Streamlit crée automatiquement un menu de navigation à partir du dossier `pages/` :

```
🏠 app.py (Page d'accueil)
   ↓
📑 Navigation automatique :
   ├── 🗺️ Carte Mondiale
   ├── 📊 Analyses Avancées
   └── 📄 Rapports PDF
```

---

## ❓ Résolution de Problèmes {#problemes}

### Problème 1 : "ModuleNotFoundError: No module named 'streamlit'"

**Solution :**

```bash
pip install streamlit
```

### Problème 2 : "No such file or directory: 'data/raw/covid_data.csv'"

**Solution :**

```bash
# Générer des données synthétiques
python generate_sample_data.py

# Ou télécharger des données réelles
python download_from_github.py
```

### Problème 3 : Les pages ne s'affichent pas

**Solution :**

- Vérifiez que le dossier `pages/` existe
- Les noms de fichiers doivent commencer par un chiffre : `01_`, `02_`, etc.
- Les émojis dans les noms sont obligatoires pour l'affichage

### Problème 4 : Erreur "Cannot import name 'load_covid_data'"

**Solution :**

```python
# Vérifiez que vos scripts sont dans le bon dossier
COVID-19-Dashboard/
├── scripts/
│   ├── data_loader.py   # Doit contenir load_covid_data()
│   └── data_cleaner.py  # Doit contenir clean_covid_data()
```

### Problème 5 : Les graphiques ne s'affichent pas

**Solution :**

```bash
# Réinstallez plotly
pip uninstall plotly
pip install plotly>=5.18.0
```

### Problème 6 : Erreur lors de la génération PDF

**Solution :**

```bash
# Installez reportlab
pip install reportlab

# Si le problème persiste, utilisez le format HTML
# Dans la page Rapports, sélectionnez "HTML" ou "Les deux"
```

---

## 🚀 Commandes Utiles

### Lancer avec rechargement automatique

```bash
streamlit run app.py
# Le dashboard se recharge automatiquement à chaque modification du code
```

### Vider le cache

```bash
# Depuis le dashboard : Appuyez sur 'C' puis 'Clear cache'
# Ou dans le code :
st.cache_data.clear()
```

### Arrêter le serveur

```bash
# Dans le terminal : Ctrl + C
```

### Mode Debug

```bash
streamlit run app.py --logger.level=debug
```

---

## 📊 Données Requises

### Format Minimum CSV

Votre fichier `data/raw/covid_data.csv` doit contenir au minimum :

```csv
date,location,total_cases,total_deaths,new_cases,new_deaths
2020-03-01,France,100,10,50,5
2020-03-02,France,150,15,50,5
...
```

### Colonnes Optionnelles (Recommandées)

```csv
people_vaccinated,new_vaccinations,total_tests,hosp_patients
1000000,50000,5000000,2000
...
```

---

## 🎯 Prochaines Étapes

### Phase 1 ✅ (Complété)

- [x] Dashboard Streamlit fonctionnel
- [x] Carte mondiale interactive
- [x] Analyses avancées
- [x] Génération de rapports depuis l'interface

### Phase 2 🚧 (À venir)

- [ ] Mode sombre/clair
- [ ] Export Excel avancé
- [ ] Prédictions avec modèles ML
- [ ] API REST pour les données

### Phase 3 🔮 (Futur)

- [ ] Authentification utilisateurs
- [ ] Déploiement cloud (Heroku/AWS)
- [ ] Application mobile
- [ ] Alertes par email

---

## 🆘 Besoin d'Aide ?

### Ressources

- **Documentation Streamlit :** https://docs.streamlit.io
- **Documentation Plotly :** https://plotly.com/python/
- **Exemples Streamlit :** https://streamlit.io/gallery

### Support

- Ouvrez une issue sur GitHub
- Consultez les logs : `streamlit run app.py --logger.level=debug`
- Vérifiez les dépendances : `pip list`

---

## ✅ Checklist de Vérification

Avant de lancer le dashboard, vérifiez :

- [ ] Python 3.8+ installé
- [ ] Toutes les dépendances installées (`pip install -r requirements.txt`)
- [ ] Structure de dossiers correcte
- [ ] Fichier `main.py` à la racine
- [ ] Dossier `pages/` créé avec les 3 fichiers
- [ ] Données disponibles dans `data/raw/` ou `data/processed/`
- [ ] Scripts originaux dans `scripts/` conservés

---

## 🎉 Prêt à Démarrer !

### 🚀 Lancement Recommandé (Automatique)

```bash
# Lancez simplement le script de démarrage rapide
python quick_start.py
```

Le script vérifie tout automatiquement et lance le dashboard !

### 🔧 Lancement Manuel (Si nécessaire)

```bash
# 1. Vérifiez l'installation
streamlit --version

# 2. Générez des données (si nécessaire)
python generate_sample_data.py

# 3. Lancez le dashboard
streamlit run main.py

# 4. Ouvrez votre navigateur
# http://localhost:8501

# 5. Profitez du dashboard interactif ! 🚀
```

---

<div align="center">

**🦠 COVID-19 Dashboard Streamlit**

_Développé avec ❤️ en Python & Streamlit_

</div>

## Auteurs

- Votre nom
- Licence : MIT
