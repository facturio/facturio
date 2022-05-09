from facturio.classes.client import Company, Client
from facturio.classes.user import User
import time
from typing import Union


class Article:
    """
    Classe contenant toutes les informations liées à un article
    """

    def __init__(self, title,  price, quantity,
                 description=None, id_=None,
                 id_receipt=None):
        self.title = title
        self.price = price
        self.quantity = quantity
        self.description = description
        self.id_ = id_
        self.id_receipt = id_receipt

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [
            self.title, self.description, self.price, self.quantity, self.id_,
            self.id_receipt
        ]

    @classmethod
    def from_dict(cls, data_dict):
        res = cls(data_dict["title"], data_dict["price"],
                  data_dict["quantity"], data_dict["description"])
        return res


class Advance:
    """Classe contenant toutes les informations liées à un devis."""

    def __init__(self,
                 amount,
                 date=None,
                 id_=None,
                 id_invoice=None):
        self.amount = amount
        self.id_ = id_
        self.id_invoice = id_invoice

        # On vérifie si la date est au format Unix time epoch
        if date:
            self.date = date
        else:
            self.date = int(time.time())

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__()

    def date_string(self):
        """
        Retourne la date sous forme de chaîne de caractères
        """
        return time.strftime("%d/%m/%Y", time.localtime(self.date))

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.amount, self.date, self.id_, self.id_invoice]


class Receipt:
    """
    Classe contenant toutes les informations communes liées aux
    factures et devis
    """

    def __init__(self,
                 user,
                 client,
                 articles_list,
                 date,
                 taxes,
                 balance,
                 note,
                 id_=None):
        self.user = user
        self.client = client
        self.articles_list = articles_list
        self.taxes = taxes
        self.balance = balance
        self.note = note
        self.id_ = id_
        if date:
            self.date = date
        else:
            self.date = int(time.time())

    def __str__(self):
        return f"User :\n{self.user}\nClient :\n{self.client}\n" \
            f"Date :\n {self.date_string()}\nListe des articles :"\
            f"\n{self.articles_list}\nTaxes :\n{self.taxes}\nMontants :\n"\
            f"{str(self.balance)}\nCommentaire :\n{self.note}"

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [
            self.user, self.client, self.date, self.articles_list, self.taxes,
            self.balance, self.note, self.id_
        ]

    def subtotal(self):
        """
        Calcule le sous-total à partir de la liste des articles
        """
        balance = 0
        for art in self.articles_list:
            balance += art.price * art.quantity
        return round(balance, 2)

    def total_of_taxes(self):
        """
        Calcul le total des taxes
        """
        return self.subtotal() * self.taxes

    def total_with_taxes(self):
        """
        Calcule le total avec les taxes
        """
        return self.subtotal() * (1 + self.taxes)

    def date_string(self):
        """
        Retourne la date sous forme de chaîne de caractères
        """
        return time.strftime("%d/%m/%Y", time.localtime(self.date))


class Invoice(Receipt):
    """
        Classe contenant toutes les informations liées aux factures
    """

    def __init__(self,
                 user,
                 client,
                 articles_list,
                 date,
                 taxes,
                 balance,
                 advances_list=[],
                 note=None,
                 id_=None):
        super().__init__(user, client, articles_list, date, taxes, balance,
                         note, id_)
        self.advances_list = advances_list

    def __str__(self):
        return (
            f"User :\n{self.user}\nClient :\n {self.client}\n"
            f"Date :\n{self.date_string()}\nListe des articles :"
            f"{self.articles_list}\n"
            f"\nListe des acomptes :\n{self.advances_list}"
            f"\nTaxes :\n{self.taxes}\n"
            f"Montants :\n{self.balance}\nCommentaire :\n{self.note}"
        )

    def __repr__(self):
        return self.__str__()

    def dump_to_list(self):
        return [
            self.user, self.client, self.date, self.articles_list,
            self.advances_list, self.taxes, self.balance, self.note,
            self.id_
        ]

    def total_with_advances(self):
        """
        Calcule le total soustrait du total des advances
        """
        return round(self.total_with_taxes() - self.total_of_advances(), 2)

    def total_of_advances(self):
        """
        Calcule le total des acomptes
        """
        balance = 0
        if(self.advances_list is not None):
            for adv in self.advances_list:
                balance += adv.amount
        return round(balance, 2)


class Estimate(Receipt):
    """
        Classe contenant toutes les informations communes liées aux
        devis.
    """

    def __init__(
        self,
        user: User,
        client: Union[Client, Company],
        articles_list,
        date: int = None,
        balance: float = None,
        taxes: float = None,
        note: str = None,
        id_: int = None
    ):
        super().__init__(user, client, articles_list, date, taxes, balance,
                         note, id_)


if __name__ == "__main__":
    artisan = User(
        company_name="Facturio",
        address="15 rue des champs Cuers",
        phone_number="0734567221",
        business_number="128974654",
        first_name="Tom",
        last_name="Pommier",
        email="facturio@gmail.com",
        logo="logo.jpg",
        id_=3
    )

    client_physique = Client(
        last_name="Lombardo",
        first_name="Quentin",
        email="quentin.lombardo@email.com",
        address="HLM Sainte-Muse Toulon",
        phone_number="0678905324",
        id_=4
    )

    client_moral = Company(
        company_name="LeRoy",
        email="LeRoy83@sfr.fr",
        address="12 ZAC de La Crau",
        phone_number="0345678910",
        first_name="Ben",
        last_name="Karim",
        business_number="287489404",
        id_=6
    )
    ordinateur = Article("ordinateur", 1684.33, 3, "Asus spire", 5, 2)
    cable_ethernet = Article("cable ethernet", 9.99, 10, "15m", 6, 2)
    telephone = Article("telephone", 399.99, 1, "téléphone clapet", 8, 2)
    casque = Article("casque", 69.99, 6, "casque sans fils", 7, 2)
    bureau = Article("Bureau", 500, 2, "Bureau à 6pieds", 9, 2)
    print(ordinateur.dump_to_list())
    paiements = [Advance(1230.0), Advance(654)]

    articles = [ordinateur, cable_ethernet, telephone, casque]

    fact = Invoice(user=artisan, client=client_moral, articles_list=articles,
                   advances_list=paiements, date=0, taxes=0.2, balance=12,
                   note="Facture de matériel informatiques")

    dev = Estimate(
        artisan, client_physique, articles,
        note="Facture de matériel informatiques"
    )
    print(fact, dev)
