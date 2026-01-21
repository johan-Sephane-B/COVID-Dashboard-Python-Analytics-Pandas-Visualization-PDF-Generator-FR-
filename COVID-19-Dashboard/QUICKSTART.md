# COVID Analytics - Guide de Démarrage Rapide

## Lancer le Dashboard Streamlit

### Option 1: Depuis le répertoire examples
```bash
cd examples/streamlit_dashboard
streamlit run app.py
```

### Option 2: Depuis la racine
```bash
streamlit run examples/streamlit_dashboard/app.py
```

## Lancer l'API REST

```bash
# Depuis la racine
uvicorn examples.api_server.main:app --reload

# Ou avec Python
python -m uvicorn examples.api_server.main:app --reload
```

Documentation API: http://localhost:8000/docs

## Exécuter les Tests

```bash
# Tous les tests
pytest

# Avec coverage
pytest --cov=covid_analytics --cov-report=html

# Tests spécifiques
pytest tests/unit/
pytest tests/integration/
```

## Benchmarks

```bash
python benchmarks/performance_benchmarks.py
```

## Installation en mode développement

```bash
pip install -e ".[dev]"
```

## Problèmes Courants

### Streamlit ne trouve pas app.py
**Solution**: Lancer depuis le bon répertoire ou spécifier le chemin complet

### Import errors
**Solution**: Installer en mode éditable `pip install -e .`

### Tests échouent
**Solution**: Vérifier que toutes les dépendances sont installées `pip install -e ".[dev]"`
