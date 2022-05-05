class User:
    """
    Classe singleton contenant toutes les informations liées à l'user
    """

    instance = None

    def __init__(
        self,
        company_name: str,
        first_name: str,
        last_name: str,
        email: str,
        adress: str,
        phone_number: str,
        business_number: str,
        logo: str = None,
    ):
        """Les attributs sont initialisés selon leur ordre d'apparition."""
        # Si l'utilisateur cree une deuxieme instance on leve une
        # exception
        if User.instance is None:
            User.instance = self
        else:
            print("Class singleton User already exits")
            raise ValueError

        self.logo = logo
        self.company_name = company_name
        self.email = email
        self.adress = adress
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.business_number = business_number

    def get_attr(self, name: str) :
        """Renvoie l'attribut passe en parametre."""
        if name == "company_name":
            return self.company_name
        elif name == "last_name":
            return self.last_name
        elif name == "first_name":
            return self.first_name
        elif name == "email":
            return self.email
        elif name == "adress":
            return self.adress
        elif name == "phone_number":
            return self.phone_number
        elif name == "business_number":
            return self.business_number
        elif name == "logo":
            return self.logo
        else:
            print(f"No attribute {name} found")
            raise KeyError

    def set_attr(self, name: str, val: str) :
        """Maj l'attribut name passe en parametre."""
        if name == "company_name":
            self.company_name = val
        elif name == "last_name":
            self.last_name = val
        elif name == "first_name":
            self.first_name = val
        elif name == "email":
            self.email = val
        elif name == "adress":
            self.adress = val
        elif name == "phone_number":
            self.phone_number = val
        elif name == "business_number":
            self.business_number = val
        elif name == "logo":
            self.logo = val
        else:
            print(f"No attribute {name} found")
            raise KeyError
    @staticmethod
    def get_instance():
        """Recupere l'instance."""
        if User.instance is None:
            print("Class singleton User already exits")
            raise ValueError
        return User.instance

    @staticmethod
    def exits():
        """Renvoie vrai si il exist une instance du singleton."""
        return True if User.instance else False


    def __str__(self):
        return (f"{self.logo } | {self.company_name} | {self.email} | "
                f"{self.adress}  | {self.phone_number} | "
                f"{self.first_name} {self.last_name} | {self.business_number}")

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """Renvoie une liste de toutes les variables de classes."""
        return [self.logo, self.company_name, self.email,
                self.adress, self.phone_number, self.first_name,
                self.last_name, self.business_number]

    def dump_to_field(self):
        """
        Renvoie la liste des variables utiles pour l'affichage des champs
        liés au client moral
        """
        return [self.company_name, self.email, self.adress, self.phone_number,
                f"{self.first_name} {self.last_name}", self.business_number]

    @classmethod
    def from_dict(cls, data_dict):
        res = cls(company_name=data_dict["company_name"],
                  adress=data_dict["adress"],
                  phone_number=data_dict["phone_number"],
                  business_number=data_dict["business_number"],
                  first_name=data_dict["first_name"],
                  last_name=data_dict["last_name"],
                  email=data_dict["email"], logo=data_dict["logo"])
        User.instance = res
        return res
