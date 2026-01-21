# Rapport d'Audit et de Nettoyage : COVID-19-Dashboard

**Date d'audit :** 21 Janvier 2026
**Projet :** COVID-19-Dashboard
**Auditeur :** Antigravity

---

## 📊 PHASE 1 : Inventaire Synthétique

Le projet présente une structure en cours de refonte majeure, caractérisée par une forte redondance entre l'ancien code (`src`) et le nouveau code cible (`src_new`). De nombreux artefacts de génération se trouvent à la racine.

### Statistiques Globales (Estimées)
*   **Nombre total de fichiers :** ~250
*   **Nombre total de dossiers :** ~60
*   **Taille totale du projet :** ~40 Mo
*   **Espace récupérable immédiatement :** ~15-20 Mo (soit ~50% de la taille actuelle)

---

## 📋 PHASE 2 & 3 : Analyse et Classification

### 🔴 CATÉGORIE 1 : À SUPPRIMER IMMÉDIATEMENT (Sans Risque)
*Ces fichiers polluent la vue et l'indexation sans apporter de valeur.*

| Type | Description | Localisation | Action | Gain |
| :--- | :--- | :--- | :--- | :--- |
| **Cache Python** | `__pycache__`, `*.pyc` | Partout (`scripts/`, `src/`, `tests/`...) | **SUPPRIMER** | ~0.5 Mo + Clarté |
| **Cache Tests** | `.pytest_cache` | Racine | **SUPPRIMER** | Négligeable |
| **Coverage** | `.coverage`, `htmlcov/` | Racine | **SUPPRIMER** | Négligeable |
| **Backups** | `*.backup`, `*.bak` | `scripts/__init__.py.backup` | **SUPPRIMER** | Clarté |
| **Artefacts HTML** | Rapports générés | `demo_comparison.html` (4.8Mo), `demo_timeline.html` (4.8Mo), `test_output_timeline.html` (4.8Mo) | **SUPPRIMER** (ou déplacer dans `output/`) | **~15 Mo** |

### 🟡 CATÉGORIE 2 : À EXAMINER / CONSOLIDER (Caution)
*Ces fichiers semblent redondants en raison de la refactorisation "covid-analytics" vers "epi-analytics".*

| Type | Fichier Actuel (Legacy?) | Fichier Cible (New?) | Recommandation |
| :--- | :--- | :--- | :--- |
| **Configuration** | `pyproject.toml` | `pyproject_NEW.toml` | **Garder les deux pour l'instant**. `New` est incomplet mais est la cible. |
| **Code Source** | `src/covid_analytics` | `src_new/epi_analytics` | **GARDER**. `src_new` (4 fichiers) ne couvre pas encore `src` (50+ fichiers). Migrer progressivement. |
| **Tests** | `tests/` | `tests_new/` | **GARDER**. Même logique que le code source. |
| **Documentation** | `README.md` | `README_NEW.md`, `GETTING_STARTED_NEW.md` | **CONSOLIDER**. Fusionner les infos pertinentes dans `README.md`. |
| **CI/CD** | `.github/` | `.github_new/` | **CONSOLIDER**. Vérifier les workflows actifs. |

### 🔍 Fichiers Suspects (Racine)
*Fichiers qui devraient être rangés dans des sous-dossiers.*
*   `check_alternative_names.py`, `check_environment.py`, `fix_imports.py` → **Déplacer dans `scripts/`**
*   `demo_app.py`, `demo_simple.py`, `app.py` → **Clarifier l'entrée (Entrypoint)**.

---

## 🧹 PHASE 5 : Plan de Nettoyage

### Actions Immédiates (Automatisables)
1.  Suppression récursive des caches (`__pycache__`, `.pytest_cache`).
2.  Suppression des fichiers de couverture de code (`.coverage`, `htmlcov`).
3.  Suppression des gros fichiers HTML générés à la racine.
4.  Suppression des fichiers de backup explicites (`.backup`).

### Actions de Consolidation (Manuelles / Futur)
1.  Migrer les scripts utilitaires de la racine vers `scripts/`.
2.  Comparer et fusionner `pyproject.toml`.
3.  Finaliser la migration de `src` vers `src_new` avant de supprimer `src`.

---

## 🛡️ PHASE 7 : Mise à jour .gitignore

Ajouts recommandés pour éviter la pollution future :
```gitignore
# Gen
*.html
!output/reports/*.html # Exception pour les rapports voulus

# Backups
*.bak
*.backup
*.old
*_new.* # Temporaire, pour éviter de commit les fichiers de transition si non voulu
```

---

## 🚦 Conclusion
Le projet est en **pleine mutation**. Un nettoyage agressif des dossiers `src` ou `tests` briserait le projet.
**L'action recommandée est un nettoyage "sanitaire" (caches, logs, builds) et une organisation des fichiers racine.**
