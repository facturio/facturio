import time

class Acompte:
    """
    Classe contenant toutes les informations liées à un acomptes
    """
    def __init__(self, montant:float, date:int = None):
        self.montant = montant
        
        #On vérifie si la date est au format Unix time epoch
        if isinstance(date, int):
            self.date = date
        else:                              
            self.date = int(time.time())

    def __str__(self):
        return f"""{time.strftime("%d/%m/%Y  %H:%M:%S",
                time.localtime(self.date))} | {self.montant}"""

    def __repr__(self):
        return self.__str__()   
    
    def date_string(self):
        """
        Retourne la date sous forme de chaîne de caractères
        """
        return time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))

    