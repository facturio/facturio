



class Client:
    """
    Classe contenant toutes les informations liées à un client physique
    """

    def __init__(
        self,
        nom: str,
        prenom: str,
        email: str = None,
        adr: str = None,
        tel: str = None,
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        attributs : chaîne de caractères
        """
        self.nom = nom  
        self.prenom = prenom  
        self.email = email  
        self.adr = adr
        self.tel = tel  

    def __str__(self):
        return f"{self.nom} | {self.prenom} | {self.email} | " \
               f"{self.adr}  | {self.tel}"

    def __repr__(self):
        return self.__str__()


class Entreprise(Client):
    """
    Classe contenant toutes les informations liées à un client moral
    """

    def __init__(
        self,
        nom_entr: str,
        nom: str,
        prenom: str,
        num_siren: str,
        email: str = None,
        adr: str = None,
        tel: str = None,
        
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        self.nom_entr = nom_entr 
        super().__init__(nom, prenom, adr, tel, email) 
        self.num_siren = num_siren  

        def __str__(self):
            return f"{self.nom_entr} | {self.nom} | {self.prenom} | " \
                   f" | {self.email} | {self.adr} | {self.tel} |"\
                   f"{self.num_siren}"
        
        def __repr__(self):
            return self.__str__()
        