import random

mur = -1
debut = -2
fin = -3
obstacle = -4
apparitionEnemi = -5


class Maze:
    def __init__(self, tailleX : int = 11, tailleY : int = 11, graine : int = None, debut : tuple[int, int] = (1, 1), fin : tuple[int, int] = (1, 1)) -> None:
        """
        TailleX doit être impaire
        TailleY doit être impaire
        La taille comprend la brodure extérieur du labyrinthe
        """
        if graine is None:
            graine = random.randint(0, 10000)

        self.__graine = graine
        self.__tailleX = tailleX
        self.__tailleY = tailleY

        self.__debut = debut
        self.__fin = fin

        self.grille = [[-1 for _ in range(self.__tailleY)] for _ in range(self.__tailleX)]

        # On place le début et la fin dans la grille dans deux composantes différente
        debutX, debutY = self.__debut
        finX, finY = self.__fin
        self.grille[debutX][debutY] = 0
        self.grille[finX][finY] = 1

    def recupTaille(self) -> tuple[int, int]:
        return self.__tailleX, self.__tailleY

    def recupGraine(self) -> int:
        return self.__graine

    def changeTaille(self, tailleX : int = 11, tailleY : int = 11) -> None:
        self.__tailleX = tailleX
        self.__tailleY = tailleY
        self.grille = [[-1 for _ in range(self.__tailleY)] for _ in range(self.__tailleX)]

    def changeGraine(self, graine : int = 0) -> None:
        self.__graine = graine

    def changeDebutFin(self, debut : tuple[int, int] = (0, 0), fin : tuple[int, int] = (0, 0)) -> None:
        self.__debut = debut
        self.__fin = fin

    def fusionnerClasse(self, classe1 : int, classe2 : int):
        nouvelleClasse = min(classe1, classe2)
        ancienneClasse = max(classe1, classe2)
        for i in range(self.__tailleX):
            for j in range(self.__tailleY):
                if self.grille[i][j] == ancienneClasse:
                    self.grille[i][j] = nouvelleClasse

    def creerLabyrinthe(self) -> None:
        """
        Approche par composante connexe
        """

        # On initialise le random sur la graine
        random.seed(self.__graine)

        # On note l'ensemble des positons à traiter
        # On traite une case sur deux pour laisser un mur entre les cases
        ensemblePose = [(i, j) for j in range(1, self.__tailleY, 2) for i in range(1, self.__tailleX, 2)]
        ensemblePose.remove(self.__debut)
        ensemblePose.remove(self.__fin)

        # On ordonne en fonction du random et par extension la graine
        random.shuffle(ensemblePose)

        # On a déjà deux composantes connexes : le départ et l'arrivée
        nombreComposanteConnexe = 2

        for (i, j) in ensemblePose:

            dejaComposanteConnexe = False  # Permet de ne pas écraser la case si la case fait déjà partie d'une composante connexe
            caseTester = [(-2, 0), (0, -2), (2, 0), (0, 2)]
            random.shuffle(caseTester)  # Permet d'éviter de créer des schémas répétitifs

            for (deltaI, deltaJ) in caseTester:
                caseObserveI = i + deltaI
                caseObserveJ = j + deltaJ

                if 0 <= caseObserveI < self.__tailleX and 0 <= caseObserveJ < self.__tailleY:  # Si on observe une case dans la grille
                    caseObserve = self.grille[caseObserveI][caseObserveJ]

                    if caseObserve >= 0:  # On observe une composante connexe

                        if dejaComposanteConnexe:
                            if caseObserve != self.grille[i][
                                j]:  # Si la case observée fait partie d'une autre composante connexe que la nôtre
                                # On supprime le mur entre les composantes connexes
                                self.grille[i + deltaI // 2][j + deltaJ // 2] = caseObserve

                                # On fusionne les deux composantes connexes
                                self.fusionnerClasse(caseObserve, self.grille[i][j])

                        else:  # On a pas de composante
                            dejaComposanteConnexe = True

                            # On ajoute notre case dans la composante connexe
                            self.grille[i][j] = caseObserve

                            # On supprime le mur entre les cases
                            self.grille[i + deltaI // 2][j + deltaJ // 2] = caseObserve

            if not dejaComposanteConnexe:  # Si on n'a pas trouvé de composante connexe alors on en créer une nouvelle pour notre case
                self.grille[i][j] = nombreComposanteConnexe
                nombreComposanteConnexe += 1

        for i in range(self.__tailleX):
            for j in range(self.__tailleY):
                if self.grille[i][j] == -1:
                    self.grille[i][j] = mur

        debutX, debutY = self.__debut
        finX, finY = self.__fin
        self.grille[debutX][debutY] = debut
        self.grille[finX][finY] = fin

    def remplacerMurObstacles(self, nombreObstacles : int = 1) -> None:
        ensembleCaseMur = [(i, j) for i in range(1, self.__tailleX - 1) for j in range(1, self.__tailleY - 1) if self.grille[i][j] == -1]
        for _ in range(nombreObstacles):
            caseI, caseJ = random.choice(ensembleCaseMur)
            self.grille[caseI][caseJ] = obstacle

    def ajouterApparitionEnemi(self, nombreEnemi : int = 1) -> None:
        ensembleCaseMur = [(i, j) for i in range(1, self.__tailleX - 1) for j in range(1, self.__tailleY - 1) if self.grille[i][j] == 0]
        for _ in range(nombreEnemi):
            caseI, caseJ = random.choice(ensembleCaseMur)
            self.grille[caseI][caseJ] = apparitionEnemi


if __name__ == "__main__":
    l = Maze(21,11, fin= (19,9))
    l.creerLabyrinthe()
    l.remplacerMurObstacles(10)
    l.ajouterApparitionEnemi(5)
    for ligne in l.grille:
        txt = ""
        for elt in ligne:
            if elt == mur:
                txt += "###"
            elif elt == debut:
                txt += " D "
            elif elt == fin:
                txt += " F "
            elif elt == obstacle:
                txt += "#O#"
            elif elt == apparitionEnemi:
                txt += " E "
            else:
                txt += "   "
        print(txt)