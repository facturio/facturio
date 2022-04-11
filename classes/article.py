class Article:
    """
    Classe contenant toutes les informations liées à un article
    """

    def __init__(self, description: str, price: float):
        self.description = description 
        self.price = price  

    def __str__(self):
        return f"{self.description} | {str(self.price)}"

    def __repr__(self):
        return self.__str__()
