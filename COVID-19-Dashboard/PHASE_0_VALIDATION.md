# Phase 0 : Validation Marché - LANCÉE

**Date de lancement** : 21 janvier 2026  
**Statut** : 🟢 EN COURS  
**Responsable** : Chef de projet  
**Durée** : 1 semaine (21-28 janvier)

---

## Objectif

Valider qu'il existe une **demande réelle** pour Epi Analytics AVANT d'investir 27,543€ et 11 semaines.

## Critères de Succès

**GO vers Phase 1 si** :
- ✅ 60%+ des répondants intéressés
- ✅ 2+ professeurs confirment utilisation potentielle
- ✅ 1+ early adopter prêt à tester

**NO-GO (arrêt projet) si** :
- ❌ < 40% intéressés
- ❌ 0 professeur intéressé
- ❌ Feedback API très négatif

---

## Tâche 0.1 : Sondage Communauté (3 jours)

### Questions du Sondage

**Sondage Google Forms : "Epi Analytics - Validation Concept"**

#### Section 1 : Profil

1. **Vous êtes :**
   - [ ] Étudiant en data science / informatique
   - [ ] Professeur / Enseignant
   - [ ] Data scientist professionnel
   - [ ] Chercheur en épidémiologie
   - [ ] Autre : _______

2. **Niveau Python :**
   - [ ] Débutant (< 6 mois)
   - [ ] Intermédiaire (6 mois - 2 ans)
   - [ ] Avancé (2+ ans)

#### Section 2 : Besoin

3. **Avez-vous déjà analysé des données épidémiologiques (COVID, grippe, etc.) ?**
   - [ ] Oui, régulièrement
   - [ ] Oui, occasionnellement
   - [ ] Non, mais j'aimerais apprendre
   - [ ] Non, pas intéressé

4. **Quels outils utilisez-vous actuellement ?**
   - [ ] Pandas brut
   - [ ] R
   - [ ] Excel
   - [ ] Outils spécialisés (SAS, Stata)
   - [ ] Aucun
   - [ ] Autre : _______

5. **Quelle est votre principale difficulté ?**
   - [ ] Trouver les données
   - [ ] Nettoyer les données
   - [ ] Calculer les métriques
   - [ ] Créer des visualisations
   - [ ] Comprendre les concepts épidémiologiques
   - [ ] Autre : _______

#### Section 3 : Solution Proposée

**Concept : Epi Analytics**

Une bibliothèque Python éducative pour analyser des données de pandémies avec une API ultra-simple :

```python
from epi_analytics import load_data, analyze, visualize

# Charger données COVID-19 (auto-download)
data = load_data()

# Analyser mortalité
mortality = analyze(data, metric="mortality", country="France")

# Visualiser
fig = visualize(data, chart_type="timeline", countries=["France", "Germany"])
fig.show()
```

6. **Ce concept vous intéresse-t-il ?**
   - [ ] Très intéressé (j'utiliserais régulièrement)
   - [ ] Intéressé (je testerais)
   - [ ] Peu intéressé
   - [ ] Pas intéressé

7. **Quelle serait votre utilisation principale ?**
   - [ ] Apprentissage personnel
   - [ ] Enseignement (cours)
   - [ ] Recherche académique
   - [ ] Projet professionnel
   - [ ] Autre : _______

8. **Seriez-vous prêt à tester une version beta ?**
   - [ ] Oui, immédiatement
   - [ ] Oui, dans quelques semaines
   - [ ] Peut-être
   - [ ] Non

#### Section 4 : Feedback

9. **Que manque-t-il à ce concept ?**
   (Texte libre)

10. **Si vous êtes enseignant : utiliseriez-vous cet outil dans vos cours ?**
    - [ ] Oui, certainement
    - [ ] Probablement
    - [ ] Peu probable
    - [ ] Non
    - [ ] N/A (pas enseignant)

11. **Email (optionnel, pour interview ou beta testing) :**
    _________________

---

### Plan de Diffusion

#### Jour 1 (21 janvier) : Création et premiers posts

**Reddit** :
- r/Python (800k+ membres)
- r/datascience (1M+ membres)
- r/learnpython (500k+ membres)

**Post type** :
```
Title: [Feedback] Building an educational Python library for epidemiological data analysis - would you use it?

Hi r/Python,

I'm building Epi Analytics, a Python library to make pandemic data analysis 
accessible for students and beginners.

The idea: 3-function API (load, analyze, visualize) that works in 5 minutes.

Example:
[code snippet]

Would this be useful for you? 
Quick survey (2 min): [link]

Feedback appreciated!
```

**Twitter/X** :
```
🔬 Building Epi Analytics - Python library for learning pandemic data analysis

📊 3-function API: load, analyze, visualize
🎓 Perfect for students & educators
⚡ Works in 5 minutes

Would you use this? Quick survey: [link]

#Python #DataScience #Epidemiology
```

#### Jour 2 (22 janvier) : Emails professeurs

**Liste cible** : 20 professeurs d'universités françaises/européennes

**Template email** :

```
Objet : Nouvel outil Python pour enseigner l'analyse de données épidémiologiques

Bonjour Professeur [Nom],

Je développe Epi Analytics, une bibliothèque Python éducative pour 
simplifier l'enseignement de l'analyse de données épidémiologiques.

Objectif : Permettre aux étudiants d'analyser des données COVID/grippe 
en 5 minutes au lieu de 2-3 heures de setup.

API ultra-simple :
[code snippet]

Seriez-vous intéressé pour l'utiliser dans vos cours ?

Sondage rapide (2 min) : [link]

Je serais ravi d'avoir votre retour.

Cordialement,
[Nom]
```

**Universités cibles** :
- Sorbonne Université
- Université Paris-Saclay
- École Polytechnique
- EPFL (Suisse)
- ETH Zurich
- TU Munich
- (+ 14 autres)

#### Jour 3 (23 janvier) : Relances et analyse

- Relance Reddit si peu de réponses
- Relance emails professeurs
- Analyse premiers résultats
- Ajustements si nécessaire

---

## Tâche 0.2 : Interviews Utilisateurs (2 jours)

### Sélection Participants

**Cible** : 10 interviews
- 5 étudiants (data science, informatique)
- 3 professeurs
- 2 data scientists professionnels

### Questions Interview (30 min)

#### Introduction (5 min)
- Présentation du concept
- Démo rapide (slides)

#### Questions (20 min)

1. **Contexte actuel**
   - Comment analysez-vous les données actuellement ?
   - Quelles sont vos principales frustrations ?
   - Combien de temps passez-vous sur le setup ?

2. **Validation concept**
   - L'API proposée est-elle intuitive ?
   - Manque-t-il des fonctionnalités essentielles ?
   - Quelle serait votre fréquence d'utilisation ?

3. **Willingness to adopt**
   - Seriez-vous prêt à l'utiliser dès la sortie ?
   - Recommanderiez-vous à vos collègues/étudiants ?
   - Quels seraient vos critères pour l'adopter ?

4. **Pricing (si applicable)**
   - Paieriez-vous pour des features premium ?
   - Quel prix serait acceptable ?

#### Conclusion (5 min)
- Feedback libre
- Inscription beta testing

### Documentation Résultats

**Template compte-rendu** :

```markdown
# Interview #[N] - [Profil]

**Date** : [Date]
**Durée** : [Durée]
**Profil** : [Étudiant/Prof/Pro]

## Insights Clés
- [Insight 1]
- [Insight 2]
- [Insight 3]

## Feedback API
- Positif : [...]
- Négatif : [...]
- Suggestions : [...]

## Willingness to Adopt
- [ ] Early adopter (immédiat)
- [ ] Intéressé (quelques semaines)
- [ ] Peut-être
- [ ] Non

## Actions
- [Action 1]
- [Action 2]
```

---

## Décision GO/NO-GO (28 janvier)

### Critères Quantitatifs

| Métrique | Cible | Résultat | ✓/✗ |
|----------|-------|----------|-----|
| Réponses sondage | 50+ | ___ | ___ |
| % Intéressés | 60%+ | ___% | ___ |
| Profs intéressés | 2+ | ___ | ___ |
| Early adopters | 1+ | ___ | ___ |
| Interviews réalisées | 8+ | ___ | ___ |

### Critères Qualitatifs

- [ ] Feedback API majoritairement positif
- [ ] Aucun red flag majeur
- [ ] Use cases clairs identifiés
- [ ] Différenciation vs existant validée

### Décision

**[ ] GO** - Passer à Phase 1 (Fondations)  
**[ ] NO-GO** - Arrêter le projet  
**[ ] PIVOT** - Ajuster concept et re-valider

**Justification** :
_[À compléter après analyse résultats]_

---

## Prochaines Étapes si GO

1. **Créer dataset sample** (Phase 1.1)
2. **Implémenter code core** (Phase 1.2)
3. **Tests unitaires** (Phase 1.3)

## Prochaines Étapes si NO-GO

1. Documenter leçons apprises
2. Archiver le projet proprement
3. Remercier participants

## Prochaines Étapes si PIVOT

1. Analyser feedback
2. Ajuster concept
3. Re-valider (Phase 0 bis)

---

**Statut** : 🟢 Sondage en cours de création  
**Prochaine action** : Créer Google Form et poster sur Reddit
