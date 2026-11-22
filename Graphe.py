from Arc import Arc

class Graphe:
    def __init__(self):
        self.sommets = set()
        self.arcs = []

    def ajouter_sommet(self, sommet: str) -> None:
        # Vérif du type
        if not isinstance(sommet, str):
            raise ValueError("Le sommet n'est pas une chaine de caractère")

        # Nettoyage
        sommet = sommet.strip()

        # Vérif de la longueur de la chaine de caractère des sommets
        if len(sommet)==0:
            raise ValueError("La chaine sommet est vide")
        
        # Contrôle si un sommet existe déjà
        elif sommet in self.sommets:
            raise ValueError("Sommet déjà présent")

        # Ajout du nouveau sommet
        self.sommets.add(sommet)


    def ajouter_arc(self, origine: str, destination: str, poids: float) -> None:
        # Vérification des types
        if not isinstance(origine, str) or not isinstance(destination, str) or not isinstance(poids, (int, float)):
            raise ValueError("Problème avec le type des données reçu")

        # Nettoyage
        origine = origine.strip()
        destination = destination.strip()

        # Vérification de la longueur de la chaine de caractère des sommets
        if len(origine)==0 or len(destination)==0:
            raise ValueError("Un sommet est vide")

        # Contrôle si l'origine ou la destination sont bien des sommets existans
        if origine not in self.sommets or destination not in self.sommets:
            raise ValueError("Un sommet n'existe pas")

        # Contrôle si un arc entre 2 sommets existes déjà
        for arc in self.arcs:
            if arc.origine == origine and arc.destination == destination:
                raise ValueError("Un arc entre ces deux sommets existe déjà.")
        
        # Ajout du nouvel arc
        nouvel_arc = Arc(origine, destination, float(poids))
        self.arcs.append(nouvel_arc)


    def obtenir_sommets(self) -> list[str]:
        return sorted(self.sommets)


    def obtenir_arcs(self) -> list[Arc]:
        return list(self.arcs)

    
    def __str__(self) -> str:
        arcs_lst = "\n".join(str(arc) for arc in self.arcs)
        return f"Les sommets présents dans le graphe sont : {self.obtenir_sommets()}.\nLes arcs présents le graphe sont :\n{arcs_lst}"

    @classmethod
    def from_file(Graphe, chemin: str) -> "Graphe":
        graphe = Graphe()
        with open(chemin, "r", encoding="utf-8") as fichier:

            ligne_sommet = False
            for ligne in fichier:
                ligne_propre = ligne.strip()

                # Continue la boucle si la ligne est vide
                if ligne_propre=="":
                    continue
                
                # Lecture des sommets
                if ligne_propre.startswith("Sommets"):
                    new_ligne = ligne_propre.split(":",1)[1]
                    new_ligne =new_ligne.split(",")
                    for element in new_ligne:
                        graphe.ajouter_sommet(element)
                    
                    # Pour générer un cas d'erreur si ma première ligne n'existe pas
                    ligne_sommet = True
                
                elif not ligne_sommet:
                    raise ValueError("Erreur lors de la lecture des sommets.")
                
                # Lecture des arcs
                else:
                    new_ligne = ligne_propre.split(";")
                    if len(new_ligne)==3:
                        try:
                            poids = float(new_ligne[2])
                        except ValueError:
                            raise ValueError("Une ligne d'arc n'a pas un poids valide")
                        graphe.ajouter_arc(new_ligne[0],new_ligne[1],poids)
                    else:
                        raise ValueError("Une ligne n'est pas reconnue comme arc ou sommets")

            if not ligne_sommet:
                raise ValueError("Fichier vide ou sans sommets.")

        return graphe


    def predecesseurs(self, sommet: str) -> list[str]:
        # Vérif du type
        if not isinstance(sommet, str):
            raise ValueError("Le sommet n'est pas une chaîne de caractères")

        # Nettoyage
        sommet = sommet.strip()

        # Contrôle si un sommet existe déjà
        if sommet not in self.sommets:
            raise ValueError("Sommet inconnu dans le graphe")

        # Récupération des predecesseurs
        predecesseurs = []
        for arc in self.arcs:
            if arc.destination == sommet:
                predecesseurs.append(arc.origine)

        return sorted(predecesseurs)

    
    def successeurs(self, sommet: str) -> list[str]:
        # Vérif du type
        if not isinstance(sommet, str):
            raise ValueError("Le sommet n'est pas une chaîne de caractères")

        # Nettoyage
        sommet = sommet.strip()

        # Contrôle si un sommet existe déjà
        if sommet not in self.sommets:
            raise ValueError("Sommet inconnu dans le graphe")

        # Récupération des successeurs
        successeurs = []
        for arc in self.arcs:
            if arc.origine == sommet:
                successeurs.append(arc.destination)

        return sorted(successeurs)


    def degre_entrant(self, sommet: str) -> int:
        return len(self.predecesseurs(sommet))


    def degre_sortant(self, sommet: str) -> int:
        return len(self.successeurs(sommet))


    def degre_total(self, sommet: str) -> int:
        return self.degre_entrant(sommet) + self.degre_sortant(sommet)


    def shortest_path(self, depart: str, arrivee: str) -> tuple[list[str] | None, float]:
        # Algorithme Dijkstra
        # Vérification des types
        if not isinstance(depart, str) or not isinstance(arrivee, str):
            raise ValueError("Les sommets doivent être des chaînes de caractères")

        # Nettoyage
        depart = depart.strip()
        arrivee = arrivee.strip()

        if depart not in self.sommets or arrivee not in self.sommets:
            raise ValueError("Un des sommets n'existe pas dans le graphe")

        if depart == arrivee:
            raise ValueError("Même arrivée que le départ")

        # Initialisation des variable de suivi de l'algorithme
        distances = {}
        precedents = {}
        for sommet in self.sommets:
            distances[sommet] = float("inf")
            precedents[sommet] = None

        distances[depart] = 0.0
        non_visites = set(self.sommets)

        while non_visites:
            # On récupère le sommet non visité ayant la plus petite distance actuelle
            courant = None
            min_distance = float("inf")

            for sommet in non_visites:
                if distances[sommet] < min_distance:
                    min_distance = distances[sommet]
                    courant = sommet

            # Si aucun sommet n'est atteignable ou si on est arrivé
            if courant is None or courant == arrivee:
                break

            # On retire le sommet actuel des sommets non visités
            non_visites.remove(courant)

            # On parcourt tous les arcs sortants de 'courant'
            for arc in self.arcs:
                if arc.origine == courant and arc.destination in non_visites:
                    new_distance = distances[courant] + arc.poids

                    if new_distance < distances[arc.destination]:
                        distances[arc.destination] = new_distance
                        precedents[arc.destination] = courant

        # Vérification si aucun chemin a été trouvé
        if distances[arrivee] == float("inf"):
            return None, float("inf")

        # Construction du chemin en remontant les sommets
        chemin = []
        actuel = arrivee
        while actuel is not None:
            chemin.append(actuel)
            actuel = precedents[actuel]

        # On retourne la liste
        chemin.reverse()

        return chemin, distances[arrivee]


    def shortest_path_avoiding(self, depart: str, arrivee:str , interdit: str) -> tuple[list[str] | None, float]:
        # Algorithme Dijkstra
        # Vérification des types
        if not isinstance(depart, str) or not isinstance(arrivee, str) or not isinstance(interdit, str):
            raise ValueError("Les sommets doivent être des chaînes de caractères")

        # Nettoyage
        depart = depart.strip()
        arrivee = arrivee.strip()
        interdit = interdit.strip()

        if depart not in self.sommets or arrivee not in self.sommets or interdit not in self.sommets:
            raise ValueError("Un des sommets n'existe pas dans le graphe")

        if depart == arrivee:
            raise ValueError("Même arrivée que le départ")

        if depart == interdit or arrivee == interdit:
            raise ValueError("L'arrivée ou le départ sont le sommet interdit")

        # Initialisation des variable de suivi de l'algorithme
        distances = {}
        precedents = {}
        for sommet in self.sommets:
            distances[sommet] = float("inf")
            precedents[sommet] = None

        distances[depart] = 0.0
        non_visites = set(self.sommets)
        non_visites.remove(interdit)

        while non_visites:
            # On récupère le sommet non visité ayant la plus petite distance actuelle
            courant = None
            min_distance = float("inf")

            for sommet in non_visites:
                if distances[sommet] < min_distance:
                    min_distance = distances[sommet]
                    courant = sommet

            # Si aucun sommet n'est atteignable ou si on est arrivé
            if courant is None or courant == arrivee:
                break

            # On retire le sommet actuel des sommets non visités
            non_visites.remove(courant)

            # On parcourt tous les arcs sortants de 'courant'
            for arc in self.arcs:
                if arc.origine == courant and arc.destination in non_visites:
                    new_distance = distances[courant] + arc.poids

                    if new_distance < distances[arc.destination]:
                        distances[arc.destination] = new_distance
                        precedents[arc.destination] = courant

        # Vérification si aucun chemin a été trouvé
        if distances[arrivee] == float("inf"):
            return None, float("inf")

        # Construction du chemin en remontant les sommets
        chemin = []
        actuel = arrivee
        while actuel is not None:
            chemin.append(actuel)
            actuel = precedents[actuel]

        # On retourne la liste
        chemin.reverse()

        return chemin, distances[arrivee]