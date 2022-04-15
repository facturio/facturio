class Client:
    """
    Classe contenant toutes les informations liées à un client physique
    """

    def __init__(
        self,
        last_name: str,
        first_name: str,
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
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.adr = adr
        self.phone = phone
        self.note = note

    def __str__(self):
        return f"{self.last_name} | {self.first_name} | {self.email} | " \
               f"{self.adr}  | {self.phone} | {self.note}"

    def __repr__(self):
        return self.__str__()


class Company(Client):
    """
    Classe contenant toutes les informations liées à un client moral
    """

    def __init__(
        self,
        company_name: str,
        last_name: str,
        first_name: str,
        siren_number: str,
        email: str,
        adr: str,
        phone: str,
        note: str = None
        
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        self.company_name = company_name
        super().__init__(last_name, first_name, email, adr, phone, note)
        self.siren_number = siren_number

        def __str__(self):
            return f"{self.company_name} | {self.last_name} | {self.first_name} | " \
                   f" | {self.email} | {self.adr} | {self.phone} | "\
                   f"{self.siren_number} | {self.note}"
        
        def __repr__(self):
            return self.__str__()
        
