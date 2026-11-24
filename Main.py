from Graphe import Graphe


def verifier_erreur(nom_test: str, action) -> None:
    """Vérifie qu'une action invalide lève bien une exception."""
    try:
        action()
        raise AssertionError(f"Échec du test '{nom_test}' : aucune erreur n'a été levée.")
    except (ValueError, TypeError, FileNotFoundError):
        print(f"[OK] {nom_test}")


def lancer_tests() -> None:
    # Ajout correct d'un sommet et refus d'un doublon
    g = Graphe()
    g.ajouter_sommet("A")
    g.ajouter_sommet("B")
    assert g.obtenir_sommets() == ["A", "B"]
    verifier_erreur("Test 1 - Refus d'un sommet doublon", lambda: g.ajouter_sommet("A"))
    print("[OK] Test 1 - Ajout d'un sommet")

    # Refus d'un arc dont une extrémité est inconnue
    verifier_erreur("Test 2 - Arc avec sommet inconnu", lambda: g.ajouter_arc("A", "Z", 5))

    # Lecture correcte du fichier et réaction à une donnée invalide
    g_reseau = Graphe.from_file("reseau.txt")
    assert len(g_reseau.obtenir_sommets()) == 8
    assert len(g_reseau.obtenir_arcs()) == 11
    print("[OK] Test 3a - Lecture correcte de reseau.txt")

    with open("fichier_invalide.txt", "w", encoding="utf-8") as f:
        f.write("Sommets: A, B\n")
        f.write("A; B; -5\n")  # Poids négatif invalide

    verifier_erreur("Test 3b - Fichier inexistant", lambda: Graphe.from_file("inexistant.txt"))
    verifier_erreur("Test 3c - Donnée invalide dans fichier", lambda: Graphe.from_file("fichier_invalide.txt"))

    # Degrés d'un sommet isolé (H dans reseau.txt)
    assert g_reseau.degre_entrant("H") == 0
    assert g_reseau.degre_sortant("H") == 0
    assert g_reseau.degre_total("H") == 0
    assert g_reseau.predecesseurs("H") == []
    assert g_reseau.successeurs("H") == []
    print("[OK] Test 4 - Degrés et voisins du sommet isolé H")

    # Plus court chemin entre deux sommets connectés (A -> G)
    chemin, cout = g_reseau.shortest_path("A", "G")
    assert chemin == ["A", "C", "B", "D", "E", "F", "G"]
    assert cout == 14.0
    print(f"[OK] Test 5 - Plus court chemin A -> G : {chemin} (coût : {cout})")

    # --- TEST 6 : Absence de chemin entre deux sommets (A -> H)
    chemin_h, cout_h = g_reseau.shortest_path("A", "H")
    assert chemin_h is None
    assert cout_h == float("inf")
    print("[OK] Test 6 - Absence de chemin vers H")

    # Itinéraire avec sommet interdit (A -> G sans B)
    chemin_sans_b, cout_sans_b = g_reseau.shortest_path_avoiding("A", "G", "B")
    assert chemin_sans_b == ["A", "C", "E", "F", "G"]
    assert cout_sans_b == 16.0
    verifier_erreur("Test 7b - Sommet interdit égal au départ", lambda: g_reseau.shortest_path_avoiding("A", "G", "A"))
    print(f"[OK] Test 7 - Chemin A -> G sans B : {chemin_sans_b} (coût : {cout_sans_b})")

    # Intersection sans modification des graphes initiaux
    g2 = Graphe.from_file("reseau2.txt")
    sommets_g1_avant = set(g_reseau.sommets)
    arcs_g1_avant = list(g_reseau.arcs)
    sommets_g2_avant = set(g2.sommets)
    arcs_g2_avant = list(g2.arcs)

    g_inter = g_reseau.intersection(g2)
    assert g_inter.obtenir_sommets() == ["A", "B", "C"]
    assert len(g_inter.obtenir_arcs()) == 2
    assert g_reseau.sommets == sommets_g1_avant and g_reseau.arcs == arcs_g1_avant
    assert g2.sommets == sommets_g2_avant and g2.arcs == arcs_g2_avant
    print("[OK] Test 8 - Intersection validée sans altération des graphes d'origine")

    print("\nTous les tests obligatoires ont réussi !")


if __name__ == "__main__":
    lancer_tests()