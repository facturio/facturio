

class Utilisateur:
    """
    Classe contenant toutes les informations liées à l'utilisateur
    """
    def __init__(self, nom_entr=None, email=None, adr=None, tel=None, num_siren=None, logo=None) :
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        """
        self.logo = logo                    #image
        self.nom_entr = nom_entr            #string
        self.email = email                  #string
        self.adr = adr                      #string
        self.tel = tel                      #string
        self.num_siren = num_siren          #string


class Particulier:
    """
    Classe contenant toutes les informations liées à un client physique
    """
    def __init__(self, nom=None, prenom=None, email=None, adr=None, tel=None):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        attributs : chaîne de caractères
        """
        self.nom = nom                      #string
        self.prenom = prenom                #string
        self.email = email                  #string
        self.adr = adr                      #string
        self.tel = tel                      #string


class Entreprise(Particulier):
    """
    Classe contenant toutes les informations liées à un client moral
    """
    def __init__(self, nom_entr=None, nom=None, prenom=None, email=None, adr=None, tel=None, num_siren=None,):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        self.nom_entr = nom_entr                        #string
        super().__init__(nom, prenom, adr, tel, email)  #string, string, string, string, string
        self.num_siren = num_siren                      #string


class Article():
    """
    Classe contenant toutes les informations liées à un article
    """
    def __init__(self, nom_article, prix, description):
        self.nom_article = nom_article                  #string
        self.prix = prix                                #flottant
        self.description = description                  #string


class Acompte():
    """
    Classe contenant toutes les informations liées à un acomptes
    """
    def __init__(self, date, montant):
        
        self.date = date                               #string
        self.montant = montant                         #flottant

class F_D():
    """
    Classe contenant toutes les informations communes liées aux factures et devis
    """
    def __init__(self, utilisateur, client, date, liste_articles, montant = None,commentaire=None):
        
        self.utilisateur = utilisateur                  #instance de classe utilisateur
        self.client = client                            #instance de classe client physique ou moral
        self.date = date                                #string
        self.liste_articles = liste_articles            #liste de tuples avec comme couple instance classe article et la quantité en int
        self.montant = montant                          #flottant
        self.commentaire = commentaire                  #entier


class Facture():

    def __init__(self, utilisateur, client, date, liste_articles, liste_acomptes, montant = None,commentaire=None):
        """
        Classe contenant toutes les informations communes liées aux factures et devis
        """
        super().__init__(utilisateur, client, date, liste_articles, montant,commentaire) #attribut classe F_D
        self.liste_acomptes = liste_acomptes             #liste d'instances de classes d'acomptes


class Devis():

    def __init__(self, utilisateur, client, date, liste_articles, montant = None,commentaire=None):
        """
        Classe contenant toutes les informations communes liées aux factures et devis
        """
        super().__init__(utilisateur, client, date, liste_articles, montant,commentaire) #attribut classe F_D
        




        


       