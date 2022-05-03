from facturio.classes.client import Company, Client
from facturio.classes.user import User
from typing import Union
import time

class Article:
    """
    Classe contenant toutes les informations liées à un article
    """

    def __init__(self, title: str,  price: float, quantity: int = 1,
                 description: str = " "):
        self.title = title
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return (f"{self.title} | {self.description} | {self.price}"
                f"| {self.quantity}")

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.title, self.description, self.price, self.quantity]

    @classmethod
    def from_dict(cls, data_dict):
        res = cls(data_dict["title"], data_dict["price"],
                  data_dict["quantity"], data_dict["description"])
        return res

class Advance:
    """
    Classe contenant toutes les informations liées à un devis
    """
    def __init__(self, amount: float, date: int = None):
        self.amount = amount

        #On vérifie si la date est au format Unix time epoch
        if date:
            self.date = date
        else:
            self.date = int(time.time())

    def __str__(self):
        return f" {self.date_string()} | {self.amount}"

    def __repr__(self):
        return self.__str__()

    def date_string(self):
        """
        Retourne la date sous forme de chaîne de caractères
        """
        return time.strftime("%d/%m/%Y",time.localtime(self.date))

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.amount, self.date]



class Receipt:
    """
    Classe contenant toutes les informations communes liées aux 
    factures et devis
    """
    def __init__(self, user: User, client: Union[Client, Company],
                 articles_list: list[Article], date: int, taxes: float,
                 amount: float, note: str = None):
        self.user = user 
        self.client = client  
        self.articles_list = articles_list
        self.taxes = taxes
        self.amount = amount 
        self.note = note
        
        if date:
            self.date = date
        else:
            self.date = int(time.time())
        
    def __str__(self):
        return f"User :\n{self.user}\nClient :\n" \
        f"{self.client}\nDate :\n {self.date_string()}\nListe des articles :"\
        f"\n{self.articles_list}\nTaxes :\n{self.taxes}\nMontants :\n"\
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
            amount += art.price * art.quantity
        return round(amount,2)
    
    def total_of_taxes(self):
        """
        Calcul le total des taxes
        """
        return self.subtotal()*self.taxes

    def total_with_taxes(self):
        """
        Calcule le total avec les taxes
        """
        return self.subtotal() * (1 + self.taxes)

    def date_string(self):
        """
        Retourne la date sous forme de chaîne de caractères
        """
        return time.strftime("%d/%m/%Y",time.localtime(self.date))
            

class Invoice(Receipt):
    """
        Classe contenant toutes les informations liées aux factures
    """
    def __init__(self, user: User, client: Union[Client, Company],
                 articles_list: list[Article], date: int,  taxes: float,
                 amount: float, advances_list: list[Advance] = None,
                 note: str = None):
        super().__init__(user, client, articles_list, date, taxes, amount,
                         note)
        self.advances_list = advances_list  
    def __str__(self):
        return (f"User :\n{self.user}\nClient :\n {self.client}\n"
                f"Date :\n{self.date_string()}\nListe des articles :"
                f"{self.articles_list}\n"
                f"\nListe des acomptes :\n{self.advances_list}"
                f"\nTaxes :\n{self.taxes}\n"
                f"Montants :\n{self.amount}\nCommentaire :\n{self.note}")

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
        
        super().__init__(user, client, articles_list, date, taxes, amount, 
                                                                         note)

if __name__ == "__main__":
    artisan = User("Facturio","15 rue des champs Cuers","0734567221", 
                                        "128974654", "facturio@gmail.com",
                                                                "logo.jpg")

    client_physique = Client("Lombardo", "Quentin", 
    "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")
                    
    client_moral = Company(company_name="LeRoy", last_name="Ben",
                           first_name="Karim", business_number="287489404",
                           email="LeRoy83@sfr.fr", adress="12 ZAC de La Crau",
                           phone_number="0345678910")

    ordinateur = Article("Ordinateur", 1684.33, 3)
    cable_ethernet = Article("Cable ethernet", 5, 10)
    telephone = Article("Telephone", 399.99, 1)
    casque = Article("Casque", 69.99, 6)

    paiements = [Advance(1230.0), Advance(654)]

    articles = [ordinateur, cable_ethernet, telephone, casque]


    fact = Invoice(user=artisan, client=client_moral, articles_list=articles,
                   advances_list=paiements, date=0, taxes=0.2, amount=12,
                   note="Facture de matériel informatiques")


    dev = Estimate(artisan, client_physique, articles, 
                                note="Facture de matériel informatiques" )
    print(fact, dev)