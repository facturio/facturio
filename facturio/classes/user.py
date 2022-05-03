class User:
    """
    Classe contenant toutes les informations liées à l'user
    """
    def __init__(
        self,
        company_name: str ,
        adress: str,
        phone_number: str,
        business_number: str,
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
        self.adress = adress
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.business_number = business_number

    def __str__(self):
        return f"{self.logo } | {self.company_name} | {self.email} | " \
               f"{self.adress}  | {self.phone_number} | "\
               f"{self.first_name} {self.last_name} | {self.business_number}"

    def __repr__(self):
        return self.__str__()
    
    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.logo, self.company_name, self.email, 
self.adress, self.phone_number, self.first_name, self.last_name, self.business_number]

    def dump_to_field(self):
        """
        Renvoie la liste des variables utiles pour l'affichage des champs
        liés au client moral
        """
        return [self.company_name, self.email, self.adress, self.phone_number,
             f"{self.first_name} {self.last_name}", self.business_number]
    @classmethod
    def from_dict(cls, data_dict):
        res = cls(data_dict["company_name"], data_dict["adress"],
                  data_dict["phone_number"], data_dict["business_number"],
                  data_dict["first_name"], data_dict["last_name"],
                  data_dict["email"], data_dict["logo"])
        return res
