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