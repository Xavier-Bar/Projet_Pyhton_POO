# Projet Python POO — Modélisation et analyse d'un réseau de transport

Application développée en Python en programmation orientée objet permettant de modéliser sous forme de graphe orienté et pondéré, de charger des données depuis un fichier texte, d'analyser la topologie du réseau (degrés, prédécesseurs, successeurs), de rechercher des itinéraires optimaux (algorithme de Dijkstra avec ou sans sommet interdit) et de comparer deux graphes par intersection.

---

## Prérequis et installation

* **Version de Python recommandée :** Python 3.10 ou supérieur.
* **Bibliothèques utilisées :** Uniquement la bibliothèque standard Python (aucune bibliothèque externe comme `networkx` ou `igraph` n'est utilisée, aucune installation via `pip` n'est nécessaire).

---

## Structure du projet

* `Arc.py` : Définition de la classe `Arc` (origine, destination, poids positif ou nul, validation des données et comparaison d'égalité).
* `Graphe.py` : Définition de la classe `Graphe` (gestion des sommets et arcs, chargement depuis fichier, calculs de degrés/voisins, algorithme de Dijkstra `shortest_path` et `shortest_path_avoiding`, intersection de graphes).
* `Main.py` : Script principal regroupant la démonstration et la suite de tests.
* `reseau.txt` : Jeu de données principal fourni dans l'énoncé.
* `reseau2.txt` : Second graphe utilisé pour tester l'intersection de deux réseaux.

---

## Lancement du programme et des tests

Ouvrir un terminal à la racine du dossier contenant les fichiers du projet, puis exécuter la commande suivante (les chemins vers `reseau.txt` et `reseau2.txt` sont relatifs et fonctionnent sans modification manuelle) :

```bash
python Main.py
```

## Ressources externes et usage de l'IA

### Documentation consultés
* **Algorithme de Dijkstra :**
  * [Major-Prépa — L'algorithme de Dijkstra en Python](https://major-prepa.com/python/algorithme-dijkstra/)
  * [DataCamp — Dijkstra's Algorithm in Python](https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python)

### Assistance par Intelligence Artificielle
* **Outil utilisé :** Gemini (modèle Gemini 4 Hydrogen) ainsi que l'autocomplétion intégrée dans l'IDE Antigravity.
* **Usage effectué et parties concernées :**
  * **Compréhension du sujet et de la théorie des graphes :** Aide à la clarification des consignes de l'énoncé et des notions fondamentales de graphes orientés pondérés avant que le sujet ne soit abordé en cours.
  * **Conception (`Arc.py` — Partie E.2) :** Rappel de la nécessité de comparer strictement les trois attributs (`origine`, `destination` et `poids`) dans la méthode `__eq__` de la classe `Arc` afin de pouvoir réutiliser cette comparaison lors de l'intersection de deux graphes.
  * **Algorithme de Dijkstra (`Graphe.py` — Parties D et E.1) :** Accompagnement pas à pas sur la structure de l'algorithme (dictionnaires `distances`, `precedents` et ensemble `non_visites`) afin d'écrire une implémentation lisible avec des boucles classiques.
  * **Tests (`Main.py` — Partie 5) :** Co-écriture et structuration des assertions automatisées couvrant l'ensemble des cas nominaux et cas limites demandés.