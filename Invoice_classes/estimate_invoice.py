from Invoice_classes.advance import *
from Invoice_classes.article import *
from Invoice_classes.client import *
from Invoice_classes.user import *

                 


class Receipt:
    """
    Classe contenant toutes les informations communes liées aux 
    factures et devis
    """

    def __init__(
        self,
        user: User,
        client: Client,
        articles_list: list[(Article, int)],
        date: int = None,
        amount: float = None,
        note: str = None,
    ):
        self.user = user 
        self.client = client  
        
        #On vérifie si la date est au format Unix time epoch
        if isinstance(date, int):
            self.date = date
        else:                              
            self.date = int(time.time())
        
        self.articles_list = articles_list 
        self.amount = amount 
        self.note = note
        
        
    def __str__(self):
        dte = time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))
        return f"User :\n{self.user}\nClient :\n" \
        f"{self.client}\nDate :\n {dte}\nListe des articles :\n"\
        f"{self.articles_list}\nMontants :\n{str(self.amount)}\n"\
        f"Commentaire :\n{self.note}"
        
    def __repr__(self):
        return self.__str__()
        
    def total(self):
        """
        Calcule le montant à partir de la liste des articles
        """
        amount = 0
        for art in self.articles_list:
            amount += art[0].price * art[1]
        return round(amount,2)
    
    def date_string(self):
        """
        Retourne la date sous forme de chaîne de caractères
        """
        return time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))
            



class Invoice(Receipt):
    """
        Classe contenant toutes les informations liées aux factures
    """
    def __init__(
        self,
        user: User,
        client: Client,
        articles_list: list[(Article, int)],
        advances_list: list[Advance] = None,
        date: int = None,
        amount: float = None,
        note: str = None,
    ):
        
        super().__init__(
            user, client, articles_list, date, amount, note
        )
        self.advances_list = advances_list  

        if amount == None:
            amount = self.total_with_advances()

    def __str__(self):
        dte = time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))
        return f"User :\n{self.user}\nClient :\n" \
            f"{self.client}\nDate :\n{dte} \nListe des articles :\n"\
            f"{self.articles_list}\nListe des acomptes :\n" \
            f"{self.advances_list}\nMontants : \n{str(self.amount)}\n"\
            f"Commentaire :\n{self.note}"

    def __repr__(self):
        return self.__str__()
    
    def total_with_advances(self):
        """
        Calcule le total soustrait du total des advances
        """
        amount = self.total()
        if(self.advances_list != None):
            for adv in self.advances_list:
                amount -= adv.amount
        return round(amount,2)

    def total_of_advances(self):
        """
        Calcule le total des acomptes
        """
        amount = 0
        if(self.advances_list != None):
            for adv in self.advances_list:
                amount += adv.amount
        return round(amount,2)




    


class Estimate(Receipt):
    """
        Classe contenant toutes les informations communes liées aux 
        devis.
    """
    def __init__(
        self,
        user: User,
        client: Client,
        articles_list: list[(Article, int)],
        date: int = None ,
        amount: float = None,
        note: str = None,
    ):
        
        super().__init__(
            user, client, articles_list, date, amount, note
        )  # attribut classe Receipt

        if amount == None:
            amount = self.total()

    def __str__(self):
        dte = time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))
        return f"User :\n{self.user}\nClient :\n" \
        f"{self.client}\nDate :\n {dte}\nListe des articles :\n"\
        f"{self.articles_list}\nMontants :\n{str(self.amount)}\n"\
        f"Commentaire :\n{self.note}"
    
    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    artisan = User("Facturio","15 rue des champs Cuers","0734567221", 
                                        "128974654", "facturio@gmail.com",
                                                                    "logo.jpg")

    client_physique = Client("Lombardo", "Quentin", "quentin.lombardo@email.com",
                                            "HLM Sainte-Muse Toulon", "0678905324")
                    
    client_moral = Company("LeRoy", "Ben", "Karim", "287489404"
                                "LeRoy83@sfr.fr","12 ZAC de La Crau", "0345678910")

    ordinateur = Article("Ordinateur", 1684.33)
    cable_ethernet = Article("Cable ethernet")
    telephone = Article("Telephone", 399.99)
    casque = Article("Casque", 69.99)

    paiements = [Advance(1230.0), Advance(654)]

    articles = [(ordinateur, 3), (cable_ethernet, 10), (telephone,1), (casque, 6)]


    fact = Invoice(artisan, client_moral, articles, advances_list =paiements, 
                                note="Facture de matériel informatiques" )


    dev = Estimate(artisan, client_physique, articles, 
                                note="Facture de matériel informatiques" )
