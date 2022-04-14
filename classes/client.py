class Client:
    """
    Classe contenant toutes les informations liées à un client physique
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str = None,
        adr: str = None,
        phone: str = None,
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
        self.adr = adr
        self.phone = phone
        self.note = note

    def __str__(self):
        return f"{self.first_name} | {self.last_name} | {self.email} | " \
               f"{self.adr}  | {self.phone} | {self.note}"

    def __repr__(self):
        return self.__str__()
    
    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.first_name, self.last_name, self.email, self.adr, 
                self.phone, self.note]


class Company(Client):
    """
    Classe contenant toutes les informations liées à un client moral
    """

    def __init__(
        self,
        company_name: str,
        email: str,
        adr: str,
        phone: str,
        buisness_number: str,
        first_name: str,
        last_name: str,
        note: str = None
        
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        self.company_name = company_name
        super().__init__(first_name, last_name, email, adr, phone, note)
        self.buisness_number = buisness_number

    def __str__(self):
        return f"{self.company_name} | {self.email} | {self.adr} | " \
               f"{self.phone} | {self.buisness_number} | "\
               f"{self.first_name} | {self.last_name} | {self.note}"
        
    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.company_name, self.email, self.adr, self.phone, 
            self.buisness_number, self.first_name, self.last_name, self.note]
        


if __name__ == "__main__":
    client_moral = Client("Lombardo", "Quentin", 
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")
    print(client_moral.dump_to_list())

    client_moral = Company("LeRoy", "Ben", "Karim", "287489404",
                "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")
    print(client_moral.dump_to_list())