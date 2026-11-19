class Arc:
    def __init__(self, origine: str, destination: str, poids: float):
        self.origine = origine
        self.destination = destination
        self.poids = poids

    @property
    def origine(self) -> str:
        return self._origine

    @origine.setter
    def origine(self, valeur: str) -> None:
        if not isinstance(valeur, str) or len(valeur.strip()) == 0:
            raise ValueError("L'origine doit être une chaîne de caractères non vide.")
        self._origine = valeur.strip()

    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, valeur: str) -> None:
        if not isinstance(valeur, str) or len(valeur.strip()) == 0:
            raise ValueError("La destination doit être une chaîne de caractères non vide.")
        self._destination = valeur.strip()

    @property
    def poids(self) -> float:
        return self._poids

    @poids.setter
    def poids(self, valeur: float) -> None:
        if not isinstance(valeur, (int,float)) or valeur < 0:
            raise ValueError("Le poids n'est pas reconnu ou inférieur ou égale à 0.")
        self._poids = float(valeur)

    def __str__(self) -> str:
        return f"De {self.origine} à {self.destination}, poids : {self.poids}"

    def __eq__(self, autre_arc: object) -> bool:
        if not isinstance(autre_arc, Arc):
            return False
        return (self.origine == autre_arc.origine and self.destination == autre_arc.destination and self.poids == autre_arc.poids)