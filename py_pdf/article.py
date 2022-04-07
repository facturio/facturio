class Article:
    """
    Classe contenant toutes les informations liées à un article
    """

    def __init__(self, nom_article: str, prix: float, description: str):
        self.nom_article = nom_article 
        self.prix = prix  
        self.description = description 

    def __str__(self):
        return f"{self.nom_article} | {str(self.prix)} | {self.description}"

    def __repr__(self):
        return self.__str__()
