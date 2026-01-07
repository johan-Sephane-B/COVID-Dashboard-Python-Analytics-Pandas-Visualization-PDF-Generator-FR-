# COVID-19 Dashboard

Dashboard analytique autour de la pandémie COVID-19 utilisant Python, Pandas, Matplotlib, et PDF Report Generator.

## Structure du projet

```
COVID-19-Dashboard/
│
├── data/                      # Données brutes et nettoyées
│   ├── raw/                   # Données CSV originales
│   └── processed/             # Données après nettoyage
│
├── notebooks/                 # Jupyter notebooks pour exploration
│   └── exploratory_analysis.ipynb
│
├── scripts/                   # Scripts Python principaux
│   ├── data_loader.py        # Chargement des données
│   ├── data_cleaner.py       # Nettoyage des données
│   ├── visualizations.py     # Création des graphiques
│   └── report_generator.py   # Génération du PDF
│
├── output/                    # Résultats générés
│   ├── figures/              # Graphiques PNG/PDF
│   └── reports/              # Rapports PDF finaux
│
├── main.py                    # Script principal d'exécution
├── requirements.txt           # Dépendances Python
├── README.md                  # Documentation du projet
└── .gitignore                # Fichiers à ignorer par Git
```

## Installation

1. Cloner le dépôt :
   ```bash
   git clone <repo_url>
   cd COVID-19-Dashboard
   ```
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Placez vos fichiers CSV dans `data/raw/`.
2. Lancez `main.py` pour générer les analyses et rapports.
3. Consultez les figures dans `output/figures/` et les rapports PDF dans `output/reports/`.

## Auteurs
- Votre nom
- Licence : MIT


