class Client:
    """
    Classe contenant toutes les informations liées à un client physique
    """
	
    def __init__(
        self,
        first_name,
        last_name,
        email=None,
        address=None,
        phone_number=None,
        note=None,
        id_=None
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        attributs : chaîne de caractères
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.note = note
        self.id_ = id_

    def __str__(self):
        return str(vars(self))
        # return f"{self.first_name} | {self.last_name} | {self.email} | " \
        #        f"{self.address}  | {self.phone_number} | {self.note} | {self.id_}"

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """Renvoie une liste de toutes les variables de classes."""
        return [self.first_name, self.last_name, self.email, self.address,
                self.phone_number, self.note]

    def dump_to_field(self):
        """
        Renvoie la liste des variables utiles pour l'affichage des champs
        liés au client physique
        """
        return [f"{self.first_name} {self.last_name}", self.email, self.address,
                self.phone_number]

    @classmethod
    def from_dict(cls, data_dict):
        res = cls(email=data_dict["email"],
                  address=data_dict["address"],
                  phone_number=data_dict["phone_number"],
                  first_name=data_dict["first_name"],
                  last_name=data_dict["last_name"],
                  note=data_dict["note"])
        return res


class Company(Client):
    """
    Classe contenant toutes les informations liées à un client moral
    """


    def __init__(
        self,
        company_name,
        first_name,
        last_name,
        email,
        address,
        phone_number,
        business_number,
        note=None,
        id_=None
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        super().__init__(first_name, last_name, email, address, phone_number, note)
        self.company_name = company_name
        self.business_number = business_number
        self.id_ = id_

    def __str__(self):
        return str(vars(self))

        # return f"{company_mame = {self.company_name} | {self.email} | {self.address} | " \
        #        f"{self.phone_number} | {self.business_number} | "\
        #        f"{self.first_name} {self.last_name} | {self.note} | {self.id_}"

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.company_name, self.email, self.address, self.phone_number,
             self.first_name, self.last_name, self.business_number, self.note]

    def dump_to_field(self):
        """
        Renvoie la liste des variables utiles pour l'affichage des champs
        liés au client moral
        """
        return [self.company_name, self.email, self.address, self.phone_number,
             f"{self.first_name} {self.last_name}", self.business_number]
    @classmethod
    def from_dict(cls, data_dict):
        res = cls(company_name=data_dict["company_name"],
                  email=data_dict["email"],
                  address=data_dict["address"],
                  phone_number=data_dict["phone_number"],
                  first_name=data_dict["first_name"],
                  last_name=data_dict["last_name"],
                  business_number=data_dict["business_number"],
                  note=data_dict["note"])
        return res



if __name__ == "__main__":
    client_moral = Client("Lombardo", "Quentin",
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")
    print(client_moral.dump_to_list())

    client_moral = Company("LeRoy", "Ben", "Karim", "287489404",
                "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")
    print(client_moral.dump_to_list())
