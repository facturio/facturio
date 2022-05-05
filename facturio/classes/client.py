class Client:
    """
    Classe contenant toutes les informations liées à un client physique
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str = None,
        adress: str = None,
        phone_number: str = None,
        note: str =None
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        attributs : chaîne de caractères
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.adress = adress
        self.phone_number = phone_number
        self.note = note

    def __str__(self):
        return f"{self.first_name} | {self.last_name} | {self.email} | " \
               f"{self.adress}  | {self.phone_number} | {self.note}"

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.first_name, self.last_name, self.email, self.adress,
                self.phone_number, self.note]

    def dump_to_field(self):
        """
        Renvoie la liste des variables utiles pour l'affichage des champs
        liés au client physique
        """
        return [f"{self.first_name} {self.last_name}", self.email, self.adress,
                self.phone_number]

class Company(Client):
    """
    Classe contenant toutes les informations liées à un client moral
    """

    def __init__(
        self,
        company_name: str,
        first_name: str,
        last_name: str,
        email: str,
        adress: str,
        phone_number: str,
        business_number: str,
        note: str = None

    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        super().__init__(first_name, last_name, email, adress, phone_number, note)
        self.company_name = company_name
        self.business_number = business_number

    def __str__(self):
        return f"{self.company_name} | {self.email} | {self.adress} | " \
               f"{self.phone_number} | {self.business_number} | "\
               f"{self.first_name} {self.last_name} | {self.note}"

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.company_name, self.email, self.adress, self.phone_number,
             self.first_name, self.last_name, self.business_number, self.note]

    def dump_to_field(self):
        """
        Renvoie la liste des variables utiles pour l'affichage des champs
        liés au client moral
        """
        return [self.company_name, self.email, self.adress, self.phone_number,
             f"{self.first_name} {self.last_name}", self.business_number]
    @classmethod
    def from_dict(cls, data_dict):
        res = cls(data_dict["company_name"], data_dict["email"],
                  data_dict["adress"], data_dict["phone_number"],
                  data_dict["first_name"], data_dict["last_name"],
                  data_dict["business_number"], data_dict["note"])
        return res



if __name__ == "__main__":
    client_moral = Client("Lombardo", "Quentin",
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")
    print(client_moral.dump_to_list())

    client_moral = Company("LeRoy", "Ben", "Karim", "287489404",
                "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")
    print(client_moral.dump_to_list())
