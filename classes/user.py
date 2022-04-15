class User:
    """
    Classe contenant toutes les informations liées à l'user
    """

    def __init__(
        self,
        company_name: str ,
        adr: str,
        phone: str,
        buisness_number: str,
        first_name: str,
        last_name: str,
        email: str = None,
        logo: str = None,
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        """
        self.logo = logo
        self.company_name = company_name
        self.email = email
        self.adr = adr
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.buisness_number = buisness_number

    def __str__(self):
        return f"{self.logo } | {self.company_name} | {self.email} | " \
               f"{self.adr}  | {self.phone} | "\
               f"{self.first_name} {self.last_name} | {self.buisness_number}"

    def __repr__(self):
        return self.__str__()
    
    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.logo, self.company_name, self.email, 
self.adr, self.phone, self.first_name, self.last_name, self.buisness_number]

    def dump_to_field(self):
        """
        Renvoie la liste des variables utiles pour l'affichage des champs
        liés au client moral
        """
        return [self.company_name, self.email, self.adr, self.phone, 
             f"{self.first_name} {self.last_name}", self.buisness_number]