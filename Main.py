from Graphe import Graphe
from Arc import Arc

def tester_erreurs(nom_test: str, action) -> None:
    """Exécute une action censée échouer et vérifie qu'une erreur est bien levée."""
    try:
        action()
        print(f"[ÉCHEC] {nom_test} : aucune erreur levée !")
    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"[OK]    {nom_test} -> erreur bien bloquée ({e})")


if __name__ == "__main__":
    print("Tests création")
    g = Graphe()
    g.ajouter_sommet("A")
    g.ajouter_sommet("B")
    g.ajouter_sommet("C")
    g.ajouter_arc("A", "B", 4)
    g.ajouter_arc("B", "C", 2.5)
    print(g)

    print("\nTests des vérifications d'erreur")
    tester_erreurs("Sommet doublon", lambda: g.ajouter_sommet("A"))
    tester_erreurs("Sommet vide", lambda: g.ajouter_sommet("   "))
    tester_erreurs("Arc vers sommet inconnu", lambda: g.ajouter_arc("A", "Z", 5))
    tester_erreurs("Arc doublon (même avec poids différent)", lambda: g.ajouter_arc("A", "B", 10))
    tester_erreurs("Arc avec poids négatif", lambda: g.ajouter_arc("A", "C", -3))



    print("\nTest lecture fichier")
    # Création d'un petit fichier de test temporaire
    with open("test_reseau.txt", "w", encoding="utf-8") as f:
        f.write("Sommets: Paris, Lyon, Marseille, Bordeaux\n")
        f.write("Paris; Lyon; 465\n")
        f.write("Lyon; Marseille; 315\n")
        f.write("Paris; Bordeaux; 584\n")

    g_fichier = Graphe.from_file("test_reseau.txt")
    print(g_fichier)

    tester_erreurs("Fichier inexistant", lambda: Graphe.from_file("introuvable.txt"))



    print("\nTets des entrant et sortant")
    g_test = Graphe()
    for s in ["A", "B", "C", "D"]:
        g_test.ajouter_sommet(s)

    g_test.ajouter_arc("A", "B", 2)
    g_test.ajouter_arc("A", "C", 5)
    g_test.ajouter_arc("B", "C", 1)
    g_test.ajouter_arc("C", "A", 3)
    # Note : "D" reste volontairement isolé (aucun arc entrant ni sortant)

    # Vérifications sur B (1 entrant : A ; 1 sortant : C)
    assert g_test.predecesseurs("B") == ["A"], "Erreur prédécesseurs de B"
    assert g_test.successeurs("B") == ["C"], "Erreur successeurs de B"
    assert g_test.degre_entrant("B") == 1, "Erreur degré entrant de B"
    assert g_test.degre_sortant("B") == 1, "Erreur degré sortant de B"
    assert g_test.degre_total("B") == 2, "Erreur degré total de B"

    # Vérifications sur A (1 entrant : C ; 2 sortants : B, C)
    assert g_test.predecesseurs("A") == ["C"], "Erreur prédécesseurs de A"
    assert g_test.successeurs("A") == ["B", "C"], "Erreur successeurs de A"
    assert g_test.degre_total("A") == 3, "Erreur degré total de A"

    # Vérifications sur D (sommet isolé : tout à 0 / vide)
    assert g_test.predecesseurs("D") == [], "Erreur prédécesseurs de D"
    assert g_test.successeurs("D") == [], "Erreur successeurs de D"
    assert g_test.degre_total("D") == 0, "Erreur degré total de D"

    print("[OK]    Voisins (prédécesseurs/successeurs) et degrés validés !")

    # Vérification des cas d'erreur
    tester_erreurs("Prédécesseurs d'un sommet inconnu", lambda: g_test.predecesseurs("Z"))
    tester_erreurs("Successeurs d'un sommet non-str", lambda: g_test.successeurs(123))
    tester_erreurs("Degré total d'un sommet inconnu", lambda: g_test.degre_total("Inexistant"))


    print("\nTest shortest_path")
    g_reseau = Graphe.from_file("reseau.txt")

    # 1. Trajet demandé dans l'énoncé : de A vers G
    # Chemin optimal attendu : A -> C (2) -> B (1) -> D (5) -> E (2) -> F (3) -> G (1) = 14.0
    chemin_ag, cout_ag = g_reseau.shortest_path("A", "G")
    print(f"Trajet A -> G : {chemin_ag} (coût total : {cout_ag})")
    assert chemin_ag == ["A", "C", "B", "D", "E", "F", "G"], f"Chemin A->G incorrect : {chemin_ag}"
    assert cout_ag == 14.0, f"Coût A->G incorrect : {cout_ag}"

    tester_erreurs("Trajet A -> A interdit", lambda: g_reseau.shortest_path("A", "A"))

    # 3. Cas limite : aucun chemin n'existe (vers le sommet isolé H)[cite: 1, 2]
    chemin_ah, cout_ah = g_reseau.shortest_path("A", "H")
    assert chemin_ah is None and cout_ah == float("inf"), "Erreur sur trajet impossible A -> H"

    # 4. Cas d'erreur : sommet inconnu
    tester_erreurs("Shortest path avec sommet inconnu", lambda: g_reseau.shortest_path("A", "Z"))

    print("[OK]    Algorithme de Dijkstra (shortest_path) validé sur tous les cas !")

    print("\n=== 6. TESTS DE LA PARTIE E (SOMMET INTERDIT & INTERSECTION) ===")
    # 1. Itinéraire en évitant un sommet (ex: A -> G en évitant B)
    # Sans B, le chemin optimal passe par A -> C (2) -> D (8) -> E (2) -> F (3) -> G (1) = 16.0[cite: 1, 2]
    chemin_sans_b, cout_sans_b = g_reseau.shortest_path_avoiding("A", "G", "B")
    print(f"Trajet A -> G sans passer par B : {chemin_sans_b} (coût : {cout_sans_b})")
    assert chemin_sans_b == ["A", "C", "E", "F", "G"], f"Chemin sans B incorrect : {chemin_sans_b}"
    assert cout_sans_b == 16.0, f"Coût sans B incorrect : {cout_sans_b}"

    # Cas limite : sommet interdit = départ ou arrivée[cite: 2]
    tester_erreurs("Interdit égal au départ", lambda: g_reseau.shortest_path_avoiding("A", "G", "A"))
    tester_erreurs("Interdit égal à l'arrivée", lambda: g_reseau.shortest_path_avoiding("A", "G", "G"))

    # 2. Intersection avec un second graphe (sans modifier les originaux)[cite: 2, 3]
    with open("reseau2.txt", "w", encoding="utf-8") as f:
        f.write("Sommets: A, B, C, Z\n")
        f.write("A; B; 4\n")   # Identique à reseau.txt[cite: 1, 3]
        f.write("A; C; 99\n")  # Poids différent -> ne doit PAS être gardé[cite: 1, 3]
        f.write("C; B; 1\n")   # Identique à reseau.txt[cite: 1, 3]
        f.write("B; Z; 7\n")   # Sommet Z absent de reseau.txt[cite: 1, 3]

    g_reseau2 = Graphe.from_file("reseau2.txt")
    nb_sommets_avant = len(g_reseau.sommets)
    nb_arcs_avant = len(g_reseau.arcs)

    g_inter = g_reseau.intersection(g_reseau2)
    assert g_inter.sommets == {"A", "B", "C"}, f"Sommets communs incorrects : {g_inter.sommets}"
    assert len(g_inter.arcs) == 2, f"Nombre d'arcs communs incorrect : {len(g_inter.arcs)}"
    assert len(g_reseau.sommets) == nb_sommets_avant and len(g_reseau.arcs) == nb_arcs_avant, "g_reseau a été modifié !"

    print("[OK]    Partie E (shortest_path_avoiding et intersection) validée !")