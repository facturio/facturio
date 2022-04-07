

from acompte import *
from article import *
from client import *
from utilisateur import *

                 


class F_D:
    """
    Classe contenant toutes les informations communes liées aux 
    factures et devis
    """

    def __init__(
        self,
        utilisateur: Utilisateur,
        client: Client,
        liste_articles: list[(Article, int)],
        date: int = None,
        montant: float = None,
        commentaire: str = None,
    ):
        self.utilisateur = utilisateur 
        self.client = client  
        
        #On vérifie si la date est au format Unix time epoch
        if isinstance(date, int):
            self.date = date
        else:                              
            self.date = int(time.time())
        
        self.liste_articles = liste_articles 
        self.montant = montant 
        self.commentaire = commentaire
        
        
    def __str__(self):
        dte = time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))
        return f"Utilisateur :\n{self.utilisateur}\nClient :\n" \
        f"{self.client}\nDate :\n {dte}\nListe des articles :\n"\
        f"{self.liste_articles}\nMontants :\n{str(self.montant)}\n"\
        f"Commentaire :\n{self.commentaire}"
        
    def __repr__(self):
        return self.__str__()
        
    def total(self):
        """
        Calcule le montant à partir de la liste des articles
        """
        self.montant = 0
        for art in self.liste_articles:
            self.montant += art[0].prix * art[1]
            



class Facture(F_D):
    """
        Classe contenant toutes les informations liées aux factures
    """
    def __init__(
        self,
        utilisateur: Utilisateur,
        client: Client,
        liste_articles: list[(Article, int)],
        liste_acomptes: list[Acompte] = None,
        date: int = None,
        montant: float = None,
        commentaire: str = None,
    ):
        
        super().__init__(
            utilisateur, client, liste_articles, date, montant, commentaire
        )
        self.liste_acomptes = liste_acomptes  

        if montant == None:
            self.total_acompte()

    def __str__(self):
        dte = time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))
        return f"Utilisateur :\n{self.utilisateur}\nClient :\n" \
            f"{self.client}\nDate :\n{dte} \nListe des articles :\n"\
            f"{self.liste_articles}\nListe des acomptes :\n" \
            f"{self.liste_acomptes}\nMontants : \n{str(self.montant)}\n"\
            f"Commentaire :\n{self.commentaire}"
        
    # def __str__(self):
    #     return f"{self.utilisateur} | {self.client} | {self.date} | "\
    #                f"{self.liste_articles} | {str(self.montant)} | "\
    #                f"{self.commentaire}"
        
    def __repr__(self):
        return self.__str__()
    
    def total_acompte(self):
        self.total()
        if(self.liste_acomptes != None):
            for ac in self.liste_acomptes:
                self.montant -= ac.montant



    


class Devis(F_D):
    """
        Classe contenant toutes les informations communes liées aux 
        devis.
    """
    def __init__(
        self,
        utilisateur: Utilisateur,
        client: Client,
        liste_articles: list[(Article, int)],
        date: int = None ,
        montant: float = None,
        commentaire: str = None,
    ):
        
        super().__init__(
            utilisateur, client, liste_articles, date, montant, commentaire
        )  # attribut classe F_D

        if montant == None:
            self.total()

    def __str__(self):
        dte = time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))
        return f"Utilisateur :\n{self.utilisateur}\nClient :\n" \
        f"{self.client}\nDate :\n {dte}\nListe des articles :\n"\
        f"{self.liste_articles}\nMontants :\n{str(self.montant)}\n"\
        f"Commentaire :\n{self.commentaire}"
    
    def __repr__(self):
        return self.__str__()


artisan = Utilisateur("Facturio","15 rue des champs Cuers","0734567221", 
                                       "128974654", "facturio@gmail.com",
                                                                "logo.jpg")

client_physique = Client("Lombardo", "Quentin", "quentin.lombardo@email.com",
                                        "HLM Sainte-Muse Toulon", "0678905324")
                
client_moral = Entreprise("LeRoy", "Ben", "Karim", "287489404"
                            "LeRoy83@sfr.fr","12 ZAC de La Crau", "0345678910")

ordinateur = Article("ordinateur", 1684.33, "Un ordinateur portable.")
cable_ethernet = Article("cable ethernet", 9.99, "Un câble ethernet.")
telephone = Article("telephone", 399.99, "Un téléphone.")
casque = Article("casque", 69.99, "Un casque audio.")

paiements = [Acompte(1230.0), Acompte(654)]

articles = [(ordinateur, 3), (cable_ethernet, 10), (telephone,1), (casque, 6)]
# print(articles)

fact = Facture(artisan, client_moral, articles, liste_acomptes =paiements, 
                            commentaire="Facture de matériel informatiques" )


dev = Devis(artisan, client_physique, articles, 
                            commentaire="Facture de matériel informatiques" )
