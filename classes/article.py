class Article:
    """
    Classe contenant toutes les informations liées à un article
    """

    def __init__(self, title: str,  price: float, description: str = None):
        self.title = title
        self.description = description 
        self.price = price  

    def __str__(self):
        return f"{self.title} | {self.description} | {str(self.price)}"

    def __repr__(self):
        return self.__str__()
    
    def dump_to_list(self):
        """
        Renvoie une liste de toutes les variables de classes
        """
        return [self.title, self.description, self.price]
