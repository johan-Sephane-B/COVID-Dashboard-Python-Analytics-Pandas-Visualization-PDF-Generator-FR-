# 🚀 Guide de Publication - COVID Analytics

Ce guide documente les étapes pour publier la bibliothèque sur PyPI.

## Prérequis

1. **Compte PyPI**: Créer un compte sur [pypi.org](https://pypi.org)
2. **API Token**: Générer un token API dans les paramètres PyPI
3. **GitHub Secret**: Ajouter le token comme `PYPI_API_TOKEN` dans les secrets GitHub

## Étapes de Publication

### 1. Préparation (✅ FAIT)

- [x] Créer `LICENSE` (MIT)
- [x] Créer `CHANGELOG.md`
- [x] Créer `CONTRIBUTING.md`
- [x] Configurer workflow GitHub Actions pour publication automatique
- [x] Finaliser `pyproject.toml`
- [x] Vérifier README.md

### 2. Tests Locaux

```bash
# Installer les outils de build
pip install build twine

# Construire le package
python -m build

# Vérifier le package
twine check dist/*

# Test d'installation locale
pip install dist/covid_analytics-1.0.0-py3-none-any.whl
```

### 3. Publication sur TestPyPI (Recommandé)

```bash
# Publier sur TestPyPI d'abord
twine upload --repository testpypi dist/*

# Tester l'installation depuis TestPyPI
pip install --index-url https://test.pypi.org/simple/ covid-analytics
```

### 4. Publication sur PyPI

**Option A: Automatique (Recommandé)**
1. Créer un tag git: `git tag v1.0.0`
2. Pousser le tag: `git push origin v1.0.0`
3. Créer une release sur GitHub
4. GitHub Actions publiera automatiquement sur PyPI

**Option B: Manuel**
```bash
# Publier sur PyPI
twine upload dist/*
```

### 5. Vérification Post-Publication

```bash
# Installer depuis PyPI
pip install covid-analytics

# Tester l'import
python -c "from covid_analytics import DataSource, Analytics; print('✅ OK')"
```

## Checklist de Publication

- [x] **Code**
  - [x] Tous les tests passent
  - [x] Coverage >70%
  - [x] Pas de warnings de linting
  - [x] Type hints complets

- [x] **Documentation**
  - [x] README.md à jour
  - [x] CHANGELOG.md complété
  - [x] Docstrings complètes
  - [x] Exemples fonctionnels

- [x] **Configuration**
  - [x] `pyproject.toml` finalisé
  - [x] Version correcte (1.0.0)
  - [x] Dépendances listées
  - [x] Classifiers PyPI corrects

- [ ] **Publication**
  - [ ] Test sur TestPyPI
  - [ ] Publication sur PyPI
  - [ ] Vérification installation
  - [ ] Annonce (Reddit, Twitter)

## Commandes Utiles

```bash
# Nettoyer les builds précédents
rm -rf dist/ build/ *.egg-info

# Construire
python -m build

# Vérifier
twine check dist/*

# Publier (TestPyPI)
twine upload --repository testpypi dist/*

# Publier (PyPI)
twine upload dist/*

# Installer localement en mode éditable
pip install -e ".[dev]"
```

## Après Publication

1. **Créer GitHub Release** avec notes de version
2. **Annoncer sur**:
   - Reddit: r/Python, r/datascience
   - Twitter/X avec hashtags #Python #DataScience
   - LinkedIn
3. **Monitorer**:
   - Issues GitHub
   - Downloads PyPI
   - Feedback utilisateurs
4. **Mettre à jour**:
   - awesome-python
   - awesome-datascience

## Versioning

Suivre [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.x.x): Breaking changes
- **MINOR** (x.1.x): Nouvelles fonctionnalités (backward compatible)
- **PATCH** (x.x.1): Bug fixes

## Support

Pour toute question sur la publication:
- GitHub Discussions
- Email: contact@covid-analytics.org
