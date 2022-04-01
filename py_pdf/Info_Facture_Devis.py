

class Utilisateur:
    """
    Classe contenant toutes les informations liées à l'utilisateur
    """
    def __init__(self, nom_entr:str=None, email:str=None, adr:str=None, 
                                  tel:str=None, num_siren:str=None, logo=None):
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
    def __init__(self, nom:str=None, prenom:str=None, email:str=None, 
                                                adr:str=None, tel:str=None):
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
    def __init__(self, nom_entr:str=None, nom:str=None, prenom:str=None, 
                                email:str=None, adr:str=None, tel:str=None, 
                                                           num_siren:str=None):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        """
        self.nom_entr = nom_entr                        #string
        super().__init__(nom, prenom, adr, tel, email)  #strings
        self.num_siren = num_siren                      #string


class Article():
    """
    Classe contenant toutes les informations liées à un article
    """
    def __init__(self, nom_article:str, prix:float, description:str):
        self.nom_article = nom_article                  #string
        self.prix = prix                                #flottant
        self.description = description                  #string


class Acompte():
    """
    Classe contenant toutes les informations liées à un acomptes
    """
    def __init__(self, date:str, montant:float):
        self.date = date                               #string
        self.montant = montant                         #flottant

class F_D():
    """
    Classe contenant toutes les informations communes liées aux 
    factures et devis
    """
    def __init__(self, utilisateur:Utilisateur, client, date:str, 
                                liste_articles:list, montant:float = None,
                                                        commentaire:str=None):
        
        #instance de classe utilisateur
        self.utilisateur = utilisateur    
        #instance de classe client physique ou moral
        self.client = client   
        #string                         
        self.date = date                                
        #liste de tuples avec comme couple (Article, int)
        #   une instance  de classe article et la quantité en int
        self.liste_articles = liste_articles 

        self.montant = montant                         
        self.commentaire = commentaire                  #entier


class Facture():

    def __init__(self, utilisateur:Utilisateur, client, date:str,               
        liste_articles:list, liste_acomptes:list = None, 
                                montant:float = None, commentaire:str=None):
        """
        Classe contenant toutes les informations liées aux factures
        """
        #attribut de la classe F_D
        super().__init__(utilisateur, client, date, liste_articles, 
            montant,commentaire) 
        #liste d'instances de classes d'acomptes
        self.liste_acomptes = liste_acomptes             


class Devis():

    def __init__(self, utilisateur, client, date, liste_articles,      
                                             montant = None,commentaire=None):  
        """
        Classe contenant toutes les informations communes liées 
        aux devis
        """
        super().__init__(utilisateur, client, date, liste_articles,
                             montant,commentaire) #attribut classe F_D
        




        


       