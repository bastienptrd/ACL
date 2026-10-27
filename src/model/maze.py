import random
import config

class Maze:
    def __init__(self, tailleX : int = 11, tailleY : int = 11, graine : int = None, debut : tuple[int, int] = (1, 1), fin : tuple[int, int] = None) -> None:
        """
        :param tailleX : TailleX doit être impaire
        :param tailleY : TailleY doit être impaire
        La taille comprend la brodure extérieur du labyrinthe
        """
        if graine is None:
            graine = random.randint(0, 10000)
        if fin is None:
            fin = (tailleX - 2, tailleY - 2)

        self.__graine = graine
        self.__tailleX = tailleX
        self.__tailleY = tailleY

        self.__debut = debut
        self.__fin = fin

        self.grille = [[-1 for _ in range(self.__tailleY)] for _ in range(self.__tailleX)]

        # On place le début et la fin dans la grille dans deux composantes différentes arbitraires
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

    def recupDebut(self) -> tuple[int, int]:
        return self.__debut

    def recupFin(self) -> tuple[int, int]:
        return self.__fin

    def __fusionnerClasse(self, classe1 : int, classe2 : int) -> None:
        """
        Fusionne deux classes en prenant le nombre de classes le plus petit comme nouvelle classe
        :param classe1:  à fusionner
        :param classe2: classe à fusionner
        """
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
                            if caseObserve != self.grille[i][j]:  # Si la case observée fait partie d'une autre composante connexe que la nôtre
                                # On supprime le mur entre les composantes connexes
                                self.grille[i + deltaI // 2][j + deltaJ // 2] = caseObserve

                                # On fusionne les deux composantes connexes
                                self.__fusionnerClasse(caseObserve, self.grille[i][j])

                        else:  # On a pas de composante
                            dejaComposanteConnexe = True

                            # On ajoute notre case dans la composante connexe
                            self.grille[i][j] = caseObserve

                            # On supprime le mur entre les cases
                            self.grille[i + deltaI // 2][j + deltaJ // 2] = caseObserve

            if not dejaComposanteConnexe:  # Si on n'a pas trouvé de composante connexe alors on en créer une nouvelle pour notre case
                self.grille[i][j] = nombreComposanteConnexe
                nombreComposanteConnexe += 1

        # On ajuste les valeurs des cases par rapport à la config
        for i in range(self.__tailleX):
            for j in range(self.__tailleY):
                if self.grille[i][j] == -1:
                    self.grille[i][j] = config.caseMur
        debutX, debutY = self.__debut
        finX, finY = self.__fin
        self.grille[debutX][debutY] = config.caseDebut
        self.grille[finX][finY] = config.caseFin

    def remplacerMurObstacles(self, nombreObstacles : int = 1) -> None:
        # On récupère ensemble des case qui peuvent accueillir une apparition d'obstacle
        ensembleCaseMur = [(i, j) for i in range(1, self.__tailleX - 1) for j in range(1, self.__tailleY - 1) if self.grille[i][j] == -1]
        for _ in range(nombreObstacles):
            # On choisit une case aléatoire
            caseI, caseJ = random.choice(ensembleCaseMur)
            self.grille[caseI][caseJ] = config.caseObstacle

    def ajouterApparitionEnemi(self, nombreEnemi : int = 1) -> None:
        # On récupère ensemble des case qui peuvent accueillir une apparition d'ennemi
        ensembleCaseMur = [(i, j) for i in range(1, self.__tailleX - 1) for j in range(1, self.__tailleY - 1) if self.grille[i][j] == 0]
        for _ in range(nombreEnemi):
            # On choisit une case aléatoire
            caseI, caseJ = random.choice(ensembleCaseMur)
            self.grille[caseI][caseJ] = config.caseApparitionEnemi


if __name__ == "__main__":
    # Teste d'execution propre au fichier
    l = Maze(21,11, fin= (19,9))
    l.creerLabyrinthe()
    l.remplacerMurObstacles(10)
    l.ajouterApparitionEnemi(5)
    for ligne in l.grille:
        txt = ""
        for elt in ligne:
            if elt == config.caseMur:
                txt += "###"
            elif elt == config.caseDebut:
                txt += " D "
            elif elt == config.caseFin:
                txt += " F "
            elif elt == config.caseObstacle:
                txt += "#O#"
            elif elt == config.caseApparitionEnemi:
                txt += " E "
            else:
                txt += "   "
        print(txt)