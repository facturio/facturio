class Utilisateur:
    """
    Classe contenant toutes les informations liées à l'utilisateur
    """

    def __init__(
        self,
        nom_entr: str = None,
        email: str = None,
        adr: str = None,
        tel: str = None,
        num_siren: str = None,
        logo=None,
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        """
        self.logo = logo  # image
        self.nom_entr = nom_entr  # string
        self.email = email  # string
        self.adr = adr  # string
        self.tel = tel  # string
        self.num_siren = num_siren  # string

    def __str__(self):
        return f"{self.logo } | {self.nom_entr} | {self.email} | " \
               f"{self.adr}  | {self.tel} | {self.num_siren}"
                                               

class Client:
    """
    Classe contenant toutes les informations liées à un client physique
    """

    def __init__(
        self,
        nom: str = None,
        prenom: str = None,
        email: str = None,
        adr: str = None,
        tel: str = None,
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        attributs : chaîne de caractères
        """
        self.nom = nom  # string
        self.prenom = prenom  # string
        self.email = email  # string
        self.adr = adr  # string
        self.tel = tel  # string

    def __str__(self):
        return self.nom + " " + self.prenom + " | " + self.email + " | " + self.tel


class Entreprise(Client):
    """
    Classe contenant toutes les informations liées à un client moral
    """

    def __init__(
        self,
        nom_entr: str = None,
        nom: str = None,
        prenom: str = None,
        email: str = None,
        adr: str = None,
        tel: str = None,
        num_siren: str = None,
    ):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        self.nom_entr = nom_entr  # string
        super().__init__(
            nom, prenom, adr, tel, email
        )  # string, string, string, string, string
        self.num_siren = num_siren  # string


class Article:
    """
    Classe contenant toutes les informations liées à un article
    """

    def __init__(self, nom_article: str, prix: float, description: str):
        self.nom_article = nom_article  # string
        self.prix = prix  # flottant
        self.description = description  # string

    def __str__(self):
        return self.nom_article + " | " + str(self.prix)


class Acompte:
    """
    Classe contenant toutes les informations liées à un acomptes
    """
    def __init__(self, date:str, montant:float):
        self.date = date                               #string
        self.montant = montant                         #flottant


class F_D:
    """
    Classe contenant toutes les informations communes liées aux 
    factures et devis
    """

    def __init__(
        self,
        utilisateur: Utilisateur,
        client: Client,
        date: str,
        liste_articles: list[(Article, int)],
        montant=None,
        commentaire=None,
    ):
        self.utilisateur = utilisateur  # instance de classe utilisateur
        self.client = client  # instance de classe client physique ou moral
        self.date = date  # string
        self.liste_articles = liste_articles  # liste de tuples (instance classe article, quantité en int)
        self.montant = montant  # flottant
        self.commentaire = commentaire  # entier


class Facture:
    def __init__(
        self,
        utilisateur,
        client,
        date,
        liste_articles,
        liste_acomptes,
        montant=None,
        commentaire=None,
    ):
        """
        Classe contenant toutes les informations liées aux factures
        """
        super().__init__(
            utilisateur, client, date, liste_articles, montant, commentaire
        )  # attribut classe F_D
        self.liste_acomptes = liste_acomptes  # liste d'instances de classes d'acomptes


class Devis:
    def __init__(
        self, utilisateur, client, date, liste_articles, montant=None, commentaire=None
    ):
        """
        Classe contenant toutes les informations communes liées aux factures et
        devis.
        """
        super().__init__(
            utilisateur, client, date, liste_articles, montant, commentaire
        )  # attribut classe F_D


clement = Client("Bazan", "Clement", "clement.bazan@email.com",
                      "AAAAAAAAAAAAAAAAAA", "0123456789")
quentin = Client("Lombardo", "Quentin", "quentin.lombardo@email.com",
                      "AAAAAAAAAAAAAAAAAAAAAA", "0000000000")
youssef = Client("Benjelloun", "Youssef",
                      "youssef.benjelloun@email.com",
                      "AAAAAAAAAAAAAAAAAAAAA", "0101010101")

ordinateur = Article("ordinateur", 1684.33, "Un ordinateur portable.")
cable_ethernet = Article("cable ethernet", 9.99, "Un câble ethernet.")
telephone = Article("telephone", 399.99, "Un téléphone.")
casque = Article("casque", 69.99, "Un casque audio.")

clients = [clement, quentin, youssef]
articles = [ordinateur, cable_ethernet, telephone, casque]
