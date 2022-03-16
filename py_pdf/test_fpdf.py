# Python program to create
# a pdf file


from fpdf import FPDF


<<<<<<< HEAD
    def __init__(self, nom_entr = None, num_siren = None, adr= None, tel = None, email=None, logo=None):
=======
class Utilisateur:
    def __init__(self, nom_entr=None, nom=None, prenom=None, adr=None, tel=None, email=None, logo=None):
>>>>>>> bfdaf36487b7cc9877f78faa149b2a645093d82c
        self.nom_entr = nom_entr
        self.num_siren = num_siren
        self.adr = adr
        self.tel = tel
        self.email = email
        self.logo = logo


class Particulier:
    def __init__(self, nom=None, prenom=None, adr=None, tel=None, email=None):
        self.nom = nom
        self.prenom = prenom
        self.adr = adr
        self.tel = tel
        self.email = email


<<<<<<< HEAD
    def __init__(self, nom_entr = None,num_siren = None, nom =None, prenom = None, adr = None, tel =None, email = None):
        super().__init__(nom,prenom,adr,tel,email)
        self.num_siren= num_siren
=======
class Entreprise(Particulier):
    def __init__(self, nom_entr=None, num_siren=None, nom=None, prenom=None, adr=None, tel=None, email=None):
        super().__init__(nom, prenom, adr, tel, email)
        self.num_siren = num_siren
>>>>>>> bfdaf36487b7cc9877f78faa149b2a645093d82c
        self.nom_entr = nom_entr


# save FPDF() class into a
# variable pdf



def creation_devis(Artisan, Client, date, mont, desc):
    """
    Genere un pdf pour un devis avec les infos
    utilisateur et client ...
    """
<<<<<<< HEAD
    pdf = FPDF()
    artisan_cell =  ""
    pdf.set_font("Arial", size = 30)
    pdf.cell(200, 10, txt = "Devis",
		ln = 1, align = 'C')
    pdf.set_font("Arial", size = 15)
    if not Artisan.logo:
        pass
    if not Artisan.nom_entr:
        artisan_cell += Artisan.nom_entr+'\n'
    if not Artisan.adr:
        artisan_cell += Artisan.adr+'\n'
    if not Artisan.email:
        artisan_cell += Artisan
        
=======
    artisan_cell = ""
    pdf.set_font("Arial", size=30)
    pdf.cell(200, 10, txt="Devis",
             ln=1, align='C')
    pdf.set_font("Arial", size=15)
    if not Artisan.logo:
        pass
    if not Artisan.nom_entr:
        artisan_cell += Artisan.nom_entr
    if not Artisan.
>>>>>>> bfdaf36487b7cc9877f78faa149b2a645093d82c

    pdf.multi_cell(200, 10)


# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf
pdf.set_font("Arial", size=15)

# create a cell
pdf.cell(200, 10, txt="GeeksforGeeks",
         ln=1, align='C')

# add another cell
pdf.cell(200, 10, txt="A Computer Science portal for geeks.",
         ln=2, align='C')

# save the pdf with name .pdf
pdf.output("GFG.pdf")
