class Utilisateur:
    """
    Classe contenant toutes les informations liées à l'utilisateur
    """

    def __init__(
        self,
        nom_entr: str ,
        adr: str,
        tel: str,
        num_siren: str,
        email: str = None,
        logo = None,
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        """
        self.logo = logo  # image
        self.nom_entr = nom_entr  # string
        self.email = email  # string
        self.adr = adr  # string
        self.tel = tel  # string
        self.num_siren = num_siren  # string

    def __str__(self):
        return f"{self.logo } | {self.nom_entr} | {self.email} | " \
               f"{self.adr}  | {self.tel} | {self.num_siren}"

    def __repr__(self):
        return self.__str__()