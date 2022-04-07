
class Acompte:
    """
    Classe contenant toutes les informations liées à un acomptes
    """
    def __init__(self, date:str, montant:float):
        self.date = date                              
        self.montant = montant

    def __str__(self):
        return f"{self.date} | {str(self.montant)}"

    def __repr__(self):
        return self.__str__()   