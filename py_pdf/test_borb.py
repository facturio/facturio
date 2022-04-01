from datetime import datetime

from Info_Facture_Devis import *




def creer_devis(Artisan, Client, Date, Montant, Desc, Commentaire):
    pass





if __name__ == "__main__":

    montant = "80"
    now = datetime.now()
    date = now.strftime("%d/%m/%Y  %H:%M:%S")
    moi = Utilisateur("Les 3 pins", "thierry.lemaire@neuf.com","6 Place de la Revolution Toulon", "(+33)6.01.02.03.04", "3458789" )
    client = Entreprise("Le Roy Merlin", "Azan","Pauline","leroy.contact@gmail.com","27 Zone Industrielle Cuers", "(+33)6.01.02.03.04", "5686968" )
    desc = "Changement d'ampoules 20"
    #creation_devis(moi, client, date, montant, desc)


    