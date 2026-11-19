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