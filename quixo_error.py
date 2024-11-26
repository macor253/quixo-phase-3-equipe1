"""Module Quixo_Error

Classes:
    * QuixoError - Classe principale des erreurs du jeu Quixo.
"""


class QuixoError(Exception):
    """
    QuixoError - Classe principale des erreurs du jeu Quixo.
    """

    def __init__(self, message):
        """Constructeur de la classe QuixoError

        Args:
            message (str): Le message d'erreur.
        """
        super().__init__(message)
