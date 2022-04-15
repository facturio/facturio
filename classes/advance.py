import time

class Advance:
    """
    Classe contenant toutes les informations liées à un devis
    """
    def __init__(self, amount:float, date:int = None):
        self.amount = amount
        
        #On vérifie si la date est au format Unix time epoch
        if isinstance(date, int):
            self.date = date
        else:                              
            self.date = int(time.time())

    def __str__(self):
        return f"""{time.strftime("%d/%m/%Y  %H:%M:%S",
                time.localtime(self.date))} | {self.amount}"""

    def __repr__(self):
        return self.__str__()   
    
    def date_string(self):
        """
        Retourne la date sous forme de chaîne de caractères
        """
        return time.strftime("%d/%m/%Y  %H:%M:%S",time.localtime(self.date))

    