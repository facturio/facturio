class User:
    """
    Classe contenant toutes les informations liées à l'user
    """

    def __init__(
        self,
        company_name: str ,
        adr: str,
        phone: str,
        siren_number: str,
        email: str = None,
        logo = None,
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        """
        self.logo = logo  # image
        self.company_name = company_name  # string
        self.email = email  # string
        self.adr = adr  # string
        self.phone = phone  # string
        self.siren_number = siren_number  # string

    def __str__(self):
        return f"{self.logo } | {self.company_name} | {self.email} | " \
               f"{self.adr}  | {self.phone} | {self.siren_number}"

    def __repr__(self):
        return self.__str__()