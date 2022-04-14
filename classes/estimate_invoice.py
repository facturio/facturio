from classes.advance import *
from classes.article import *
from classes.client import *
from classes.user import *
from typing import Union
                 


class Receipt:
    """
    Classe contenant toutes les informations communes liées aux 
    factures et devis
    """

    def __init__(
        self,
        user: User,
        client: Union[Client, Company],
        articles_list: list[(Article, int)],
        date: int = None,
        taxes: float = None,
        amount: float = None,
        note: str = None,
    ):
        self.user = user 
        self.client = client  
        #On vérifie si la date est au format Unix time epoch
        if date:
            self.date = date
        else:                              
            self.date = int(time.time())
        
        self.articles_list = articles_list 
        self.taxes = taxes
        self.amount = amount 
        self.note = note
           
    def __str__(self):
        return f"User :\n{self.user}\nClient :\n" \
        f"{self.client}\nDate :\n {self.date_string()}\nListe des articles :"\
        f"\n{self.articles_list}\nTaxes :\n{self.taxes}Montants :\n"\
        f"{str(self.amount)}\nCommentaire :\n{self.note}"
        
    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """ 
        return [self.user, self.client, self.date, self.articles_list, 
                                            self.taxes, self.amount, self.note]

    def subtotal(self):
        """
        Calcule le sous-total à partir de la liste des articles
        """
        amount = 0
        for art in self.articles_list:
            amount += art[0].price * art[1]
        return round(amount,2)

    def total_with_taxes(self):
        """
        Calcule le total avec les taxes
        """
        return self.subtotal() * (1 + self.taxes)

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
        client: Union[Client, Company],
        articles_list: list[(Article, int)],
        advances_list: list[Advance] = None,
        date: int = None,
        taxes: float = None,
        amount: float = None,
        note: str = None,
    ):
        super().__init__(user, client, articles_list, date, taxes, amount, note)
        self.advances_list = advances_list  

        if amount == None:
            amount = self.total_with_advances()

    def __str__(self):
        return f"User :\n{self.user}\nClient :\n" \
        f"{self.client}\nDate :\n{self.date_string()}\nListe des articles :"\
        f"{self.articles_list}\n"\
        f"\nListe des acomptes :\n{self.advances_list}"\
        f"Taxes :\n{self.taxes}\n" \
        f"Montants :\n{self.amount}\nCommentaire :\n{self.note}"

    def __repr__(self):
        return self.__str__()
    
    def dump_to_list(self):
        return [self.user, self.client, self.date, self.articles_list,
                self.advances_list, self.taxes, self.amount, self.note]
    
    def total_with_advances(self):
        """
        Calcule le total soustrait du total des advances
        """
        return round(self.total_with_taxes() - self.total_of_advances(), 2)

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
        client: Union[Client, Company],
        articles_list: list[(Article, int)],
        date: int = None ,
        amount: float = None,
        taxes: float = None,
        note: str = None,
    ):
        
        super().__init__(user, client, articles_list, date, amount, taxes, note)
        if amount == None:
            amount = self.total_with_taxes()

    def __str__(self):
        return f"User :\n{self.user}\nClient :\n" \
        f"{self.client}\nDate :\n {self.date_string()}\nListe des articles :"\
        f"\n{self.articles_list}\nTaxes :\n{self.taxes}Montants :\n"\
        f"{str(self.amount)}\nCommentaire :\n{self.note}"
    
    def __repr__(self):
        return self.__str__()
    
    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """ 
        return [self.user, self.client, self.date, self.articles_list, 
                                            self.taxes, self.amount, self.note]

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
