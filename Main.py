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