"""Module Plateau

Classes:
    * Plateau - Classe principale du plateau de jeu Quixo.
"""

from copy import deepcopy

from quixo_error import QuixoError


class Plateau:
    """
    Plateau - Classe principale du plateau de jeu Quixo.
    """
    def __init__(self, plateau=None):
        """Constructeur de la classe Plateau

        Vous ne devez rien modifier dans cette méthode.

        Args:
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par
                défaut.
        """
        self.plateau = self.générer_le_plateau(deepcopy(plateau))

    def état_plateau(self):
        """Retourne une copie du plateau

        Retourne une copie du plateau pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            list[list[str]]: La représentation du plateau
            tel que retourné par le serveur de jeu.
        """
        return deepcopy(self.plateau)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères du plateau

        Déplacer le code de votre fonction formater_plateau ici et ajuster le
        en conséquence.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        lignes = []
        lignes.append('   -------------------')

        for i, ligne in enumerate(self.plateau):
            lignes.append(f'{i + 1} | {" | ".join(ligne)} |')
            if i < len(self.plateau) - 1:
                lignes.append('  |---|---|---|---|---|')

        lignes.append('--|---|---|---|---|---|')
        lignes.append('  | 1   2   3   4   5 |\n')

        return '\n'.join(lignes)

    def __getitem__(self, position):
        """Retourne la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le
            plateau.

        Returns:
            str: La valeur à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5
            inclusivement.
        """
        if not all(1 <= i <= 5 for i in position):
            raise QuixoError(
                'Les positions x et y doivent être entre 1 et 5 inclusivement.'
            )
        return self.plateau[position[1] - 1][position[0] - 1]

    def __setitem__(self, position, valeur):
        """Modifie la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le
                plateau.
            value (str): La valeur à insérer à la position donnée, soit "X",
                "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5
                inclusivement.
            QuixoError: Valeur du cube invalide.
        """
        if not all(1 <= i <= 5 for i in position):
            raise QuixoError(
                'Les positions x et y doivent être entre 1 et 5 inclusivement.'
            )
        if valeur not in ['X', 'O', ' ']:
            raise QuixoError('Valeur du cube invalide.')
        self.plateau[position[1] - 1][position[0] - 1] = valeur

    def générer_le_plateau(self, plateau):
        """Génère un plateau de jeu

        Si un plateau est fourni, il est retourné tel quel.
        Sinon, si la valeur est None, un plateau vide de 5x5 est retourné.

        Args:
            plateau (list[list[str]] | None): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None.

        Returns:
            list[list[str]]: La représentation du plateau
                tel que retourné par le serveur de jeu.

        Raises:
            QuixoError: Format du plateau invalide.
            QuixoError: Valeur du cube invalide.
        """
        if plateau is None:
            return [[' '] * 5 for _ in range(5)]

        if not isinstance(plateau, list) or len(plateau) != 5:
            raise QuixoError('Format du plateau invalide.')

        for ligne in plateau:
            if not isinstance(ligne, list) or len(ligne) != 5:
                raise QuixoError('Format du plateau invalide.')
            for cube in ligne:
                if cube not in ['X', 'O', ' ']:
                    raise QuixoError('Valeur du cube invalide.')

        return plateau

    def insérer_un_cube(self, cube, origine, direction):
        """Insère un cube dans le plateau

        Cette méthode appelle la méthode d'insertion appropriée selon la
        direction donnée.

        À noter que la validation des positions sont faites dans
        les méthodes __setitem__ et __getitem__. Vous devez donc en faire usage
        dans les diverses méthodes d'insertion pour vous assurez que les
        positions sont valides.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] initiale du cube à insérer.
            direction (str): La direction de l'insertion, soit "haut", "bas",
            "gauche" ou "droite".

        Raises:
            QuixoError: La direction doit être "haut", "bas", "gauche" ou
            "droite".
            QuixoError: Le cube à insérer ne peut pas être vide.
        """
        cube = cube.strip()
        if cube not in ['X', 'O']:
            raise QuixoError('Le cube à insérer ne peut pas être vide.')
        if direction == 'haut':
            self.insérer_par_le_haut(cube, origine)
        elif direction == 'bas':
            self.insérer_par_le_bas(cube, origine)
        elif direction == 'gauche':
            self.insérer_par_la_gauche(cube, origine)
        elif direction == 'droite':
            self.insérer_par_la_droite(cube, origine)
        else:
            raise QuixoError(
                'La direction doit être "haut", "bas", "gauche" ou "droite".'
            )

    def insérer_par_le_bas(self, cube, origine):
        """Insère un cube dans le plateau en direction du bas

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] initiale du cube à insérer.
        """
        x, y = origine
        for i in range(y, 5):
            self[x, i] = self[x, i + 1]
        self[x, 5] = cube

    def insérer_par_le_haut(self, cube, origine):
        """Insère un cube dans le plateau en direction du haut

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] initiale du cube à insérer.
        """
        x, y = origine
        for i in range(y - 1, 0, -1):
            self[x, i + 1] = self[x, i]
        self[x, 1] = cube

    def insérer_par_la_gauche(self, cube, origine):
        """Insère un cube dans le plateau en direction de la gauche

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] initiale du cube à insérer.
        """
        x, y = origine
        for i in range(x, 0, -1):
            self[i + 1, y] = self[i, y]
        self[1, y] = cube

    def insérer_par_la_droite(self, cube, origine):
        """Insère un cube dans le plateau en direction de la droite

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] initiale du cube à insérer.
        """
        x, y = origine
        for i in range(x, 0, -1):
            self[i, y] = self[i + 1, y]
        self[5, y] = cube
