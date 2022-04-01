# Python program to create
# a pdf file


from fpdf import FPDF
from datetime import datetime

class Utilisateur:
    
    def __init__(self, nom_entr=None, email=None, adr=None, tel=None, num_siren=None, logo=None) :
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        logo : image
        autres attributs : chaîne de caractères
        """
        self.logo = logo
        self.nom_entr = nom_entr
        self.email = email
        self.adr = adr
        self.tel = tel
        self.num_siren = num_siren


class Particulier:
    def __init__(self, nom=None, prenom=None, email=None, adr=None, tel=None):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        attributs : chaîne de caractères
        """
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.adr = adr
        self.tel = tel


class Entreprise(Particulier):
    def __init__(self, nom_entr=None, nom=None, prenom=None, email=None, adr=None, tel=None, num_siren=None,):
        """
        Les attributs sont initialisés selon leur ordre d'apparition
        dans le pdf
        attributs : chaîne de caractères
        """
        self.nom_entr = nom_entr
        super().__init__(nom, prenom, adr, tel, email)
        self.num_siren = num_siren
        


# save FPDF() class into a
# variable pdf


def cell_artisan(Artisan):
    """
    Récupère un objet de la classe Utilisateur
    Et traduit ses informations en une chaîne de caractères
    """
    artisan_cell = "De :\n"
    if Artisan.logo:
        pass
    if Artisan.nom_entr:
        artisan_cell += Artisan.nom_entr+'\n'

    if Artisan.email:
        artisan_cell += Artisan.email+'\n'

    if Artisan.adr:
        artisan_cell += Artisan.adr+'\n'

    if Artisan.tel:
        artisan_cell += Artisan.tel+'\n'

    if Artisan.num_siren:
        artisan_cell += "NUMERO SIREN/SIRET : "+Artisan.num_siren+'\n'

    return artisan_cell

def cell_client_moral(Client):
    """
    Récupère un objet de la classe Entreprise
    Et traduit ses informations en une chaîne de caractères
    """
    client_cell = "Client :\n"

    if Client.nom_entr:
        client_cell += Client.nom_entr+'\n'

    if Client.nom:
        client_cell += Client.nom+'\n'

    if Client.prenom:
        client_cell += Client.prenom+'\n'
        
    if Client.email:
        client_cell += Client.email+'\n'

    if Client.adr:
        client_cell += Client.adr+'\n'

    if Client.tel:
        client_cell += Client.tel+'\n'

    if Client.num_siren:
        client_cell += "Num SIREN/SIRET : "+Client.num_siren+'\n'

    
    return client_cell

def cell_client_physique(Client):
    """
    Récupère un objet de la classe Particulier
    Et traduit ses informations en une chaîne de caractères
    """
    client_cell = "Client :\n"

    if Client.nom:
        client_cell += Client.nom+'\n'

    if Client.nom:
        client_cell += Client.prenom+'\n'
        
    if Client.email:
        client_cell += Client.email+'\n'

    if Client.adr:
        client_cell += Client.adr+'\n'

    if Client.tel:
        client_cell += Client.tel+'\n'

    if Client.num_siren:
        client_cell += "Num SIREN/SIRET : "+Client.num_siren+'\n'

    
    return client_cell

   

def creation_devis(Artisan, Client, date, mont, desc):
    """
    Genere un pdf pour un devis avec les infos
    utilisateur et client ...
    """
    #default
    #pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf = FPDF()
    pdf.add_page()
    pdf.rect(5.0, 5.0, 200.0,287.0)

    # Entete
    pdf.set_font("Arial", size=30)
    pdf.cell(200, 10, txt="Devis",
             ln=1, align='C')

    pdf.set_font("Arial", size=10)

    #Utilisateur
    
    pdf.multi_cell(200, 10, cell_artisan(Artisan),border="1",align="L")
    
    #Client qui peut être une entreprise ou un particulier
    if isinstance(Client, Entreprise):
        pdf.multi_cell(200, 10, cell_client_moral(Client),border="1",align="L")
        
    
    elif isinstance(Client, Particulier):
        pdf.multi_cell(200, 10, cell_client_physique(Client),border="1",align="L")
    
    #Date et Montant
    pdf.cell(200, 10, txt="Le :"+date+" Montant : "+mont,
             ln=1, align='C')
    
    #Description
    pdf.multi_cell(200, 10, desc,border="0",align="C")

    pdf.output("Devis.pdf")

    
    
if __name__ == "__main__":

    montant = "80"
    now = datetime.now()
    date = now.strftime("%d/%m/%Y  %H:%M:%S")
    moi = Utilisateur("Les 3 pins", "thierry.lemaire@neuf.com","6 Place de la Revolution Toulon", "(+33)6.01.02.03.04", "3458789" )
    client = Entreprise("Le Roy Merlin", "Azan","Pauline","leroy.contact@gmail.com","27 Zone Industrielle Cuers", "(+33)6.01.02.03.04", "5686968" )
    desc = "Changement d'ampoules 20"
    creation_devis(moi, client, date, montant, desc)


    


# # Add a page
# pdf.add_page()

# # set style and size of font
# # that you want in the pdf
# pdf.set_font("Arial", size=15)

# # create a cell
# pdf.cell(200, 10, txt="GeeksforGeeks",
#          ln=1, align='C')

# # add another cell
# pdf.cell(200, 10, txt="A Computer Science portal for geeks.",
#          ln=2, align='C')

# # save the pdf with name .pdf
# pdf.output("GFG.pdf")
