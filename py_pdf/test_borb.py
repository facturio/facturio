
from facture_devis import *

#Import de borb
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF
from borb.pdf.canvas.layout.page_layout.multi_column_layout \
                                        import SingleColumnLayout
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.fixed_column_width_table \
                            import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.layout.table.fixed_column_width_table \
                            import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.table.flexible_column_width_table \
                                            import FlexibleColumnWidthTable

from borb.pdf.canvas.layout.layout_element import LayoutElement


#Import librairie standard
from datetime import datetime
from decimal import Decimal
import random
from pathlib import Path




mail_icon: LayoutElement = Image(
    image=Path("icones/mail.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3),
    # horizontal_alignment=Alignment.CENTERED
)

email_icon: LayoutElement = Image(
    image=Path("icones/email.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)

phone_icon: LayoutElement = Image(
    image=Path("icones/phone.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)

business_icon: LayoutElement = Image(
    image=Path("icones/business.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)

person_icon: LayoutElement = Image(
    image=Path("icones/person.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)



def pdf_entete_logo(facture_devis, identifiant):
    table = FlexibleColumnWidthTable(number_of_rows= 3, number_of_columns=4)
    
    if(facture_devis.utilisateur.logo != None):
        table.add(TableCell(   
        Image(        
        image=Path(facture_devis.utilisateur.logo),        
        width=Decimal(75),        
        height=Decimal(75),    
        ), row_span=3))
    else:
        table.add(TableCell(Paragraph(" ", padding_left=Decimal(50)),
                                                                row_span=3))

    table.add(Paragraph(" ", padding_left=Decimal(190)))

    if isinstance(facture_devis, Facture):      
        table.add(Paragraph("Facture", 
                font="Helvetica-Bold",horizontal_alignment=Alignment.LEFT))

    elif isinstance(facture_devis, Devis):
        table.add(Paragraph(f"Devis", 
                font="Helvetica-Bold",horizontal_alignment=Alignment.LEFT))
                
    
    table.add(Paragraph(f" # {identifiant}",respect_spaces_in_text=True)) 

    table.add(Paragraph(" "))
    table.add(Paragraph(" "))
    table.add(Paragraph(" "))

    table.add(Paragraph(" "))
    table.add(Paragraph("Date", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.LEFT))       
    table.add(Paragraph(f" {facture_devis.date_string()}", 
                                        respect_spaces_in_text=True))  
    table.no_borders()

    return table


def pdf_champs_prestataire_client(facture_devis):    
    """
    Retourne une table liée aux informations du prestataire
    """

    de = facture_devis.utilisateur
    a = facture_devis.client

    #Première Ligne
    table = FlexibleColumnWidthTable(number_of_rows=7, number_of_columns=4) 
    table.add(Paragraph("De ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.LEFT))

    table.add(Paragraph(" ", padding_left=Decimal(240)))
    table.add(Paragraph("A ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.RIGHT))

    table.add(Paragraph(" "))
      
    
	#Deuxième Ligne
    table.add(business_icon)
    table.add(Paragraph(de.nom_entr))

    if(isinstance(a,Entreprise)):
        table.add(business_icon)
        table.add(Paragraph(a.nom_entr))
    
    else:
        table.add(person_icon)
        table.add(Paragraph(f"{a.prenom} {a.nom}"))
       

    #Troisième Ligne
    if(de.email == None):
        table.add(Paragraph(" "))  
        table.add(Paragraph(" "))  
    else:
        table.add(email_icon)  
        table.add(Paragraph(de.email))

    if(a.email == None):
        table.add(Paragraph(" "))
        table.add(Paragraph(" "))

    else:
        table.add(email_icon)  
        table.add(Paragraph(a.email))  

    
    
    
    #Quatrième Ligne
    table.add(mail_icon)
    table.add(Paragraph(de.adr))

    if(a.adr == None):
        table.add(Paragraph(" "))
        table.add(Paragraph(" "))

    else:
        table.add(mail_icon)  
        table.add(Paragraph(a.adr))
 
	
    #Cinquième Ligne
    
    table.add(phone_icon)
    table.add(Paragraph(de.tel))

    if(a.tel == None):
        table.add(Paragraph(" "))
        table.add(Paragraph(" "))

    else:
        table.add(phone_icon)  
        table.add(Paragraph(a.tel))

    #Sixième Ligne
    
    table.add(Paragraph("N°", font="Helvetica-Bold", horizontal_alignment=Alignment.CENTERED))
    table.add(Paragraph(f"{de.num_siren}"))

    if(isinstance(a, Entreprise)):
        table.add(Paragraph("N°", font="Helvetica-Bold", horizontal_alignment=Alignment.CENTERED))
        table.add(Paragraph(f"{a.num_siren}"))

    else :
        table.add(Paragraph(" "))
        table.add(Paragraph(" "))

    #Septième Ligne
    table.add(Paragraph(" "))
    table.add(Paragraph(" "))
    if(isinstance(a, Entreprise)):
        table.add(person_icon)
        table.add(Paragraph(f"{a.prenom} {a.nom}"))

    else :
        table.add(Paragraph(" "))
        table.add(Paragraph(" "))


    table.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), 
                                                                    Decimal(1))    		
    table.no_borders()
    return table

def pdf_articles_taxes(facture_devis, monnaie, taxe, remises):


    list_articles = facture_devis.liste_articles
    nb_articles = len(list_articles)
    
    nb_lignes = nb_articles + 5
    if(nb_lignes < 15):
        nb_lignes = 15
    
    table = Table(number_of_rows=nb_lignes, number_of_columns=4)  
    for h in ["DESCRIPTION", "QUANTITÉ", "PRIX UNITAIRE", "TOTAL"]:  
        table.add(  
            TableCell(  
                Paragraph(h, font_color=X11Color("White")),  
                background_color=HexColor("5f5f5f"),  
            )  
        )  
    couleur_impaire = HexColor("BBBBBB")  
    couleur_paire = HexColor("FFFFFF")  

    parite = True

    for article in list_articles:  
        c = couleur_paire if parite else couleur_impaire 
        parite ^= True
        table.add(TableCell(Paragraph(f"{article[0].nom_article}", 
                            respect_newlines_in_text=True), 
                                                    background_color=c))  
        table.add(TableCell(Paragraph(f"{article[1]}"), background_color=c))  
        table.add(TableCell(Paragraph(f"{article[0].prix} {monnaie}"), 
                                                        background_color=c))   
        table.add(TableCell(Paragraph(
                        f"{round(article[1] * article[0].prix,2)} {monnaie}")
                                                        , background_color=c))    
	  
	
    #Si on a moins de 10 articles alors on rajoute des lignes vides
    while(nb_articles < 10):
        c = couleur_paire if parite else couleur_impaire 
        parite ^= True
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        nb_articles += 1 
  
 
    table.add(TableCell(Paragraph("Sous-total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT,), col_span=3,))  
    table.add(TableCell(Paragraph(f"{facture_devis.total()} {monnaie}", 
                                        horizontal_alignment=Alignment.RIGHT)))
    if(isinstance(facture_devis, Facture)):
        #Calcule du total et des taxe
        tt = facture_devis.total_avec_acomptes()-remises
        tx = tt*taxe   
        table.add(TableCell(Paragraph("Remises/Acomptes", 
            font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),
                                                                col_span=3,))
        table.add(TableCell(Paragraph(
                       f"{facture_devis.total_acomptes() + remises} {monnaie}", 
                                       horizontal_alignment=Alignment.RIGHT)))
    else:
        #Calcule du total et des taxe
        tt = round(facture_devis.total()-remises, 2)
        tx = round(tt*taxe,2)  
        table.add(TableCell(Paragraph("Remises", 
            font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),
                                                                col_span=3,))
        table.add(TableCell(Paragraph(f"{remises} {monnaie}", 
                                       horizontal_alignment=Alignment.RIGHT)))
    
    table.add(TableCell(Paragraph(f"Taxes ({taxe*100}%)", 
    font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3,)) 

    table.add(TableCell(Paragraph(f"{round(tx, 2)} {monnaie}", 
                                        horizontal_alignment=Alignment.RIGHT)))  
    table.add(TableCell(Paragraph("Total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT  ), col_span=3,))  
    table.add(TableCell(Paragraph(f"{round(tt + tx, 2)} {monnaie} ", 
                    horizontal_alignment=Alignment.RIGHT)))  
    table.set_padding_on_all_cells(Decimal(2), 
                                        Decimal(15), Decimal(2), Decimal(2))  
    
    return table



  

def construire_pdf(facture_devis, identifiant, monnaie, taxe, remise, 
                                                                chemin= None):

    # Créer un document pdf
    pdf = Document()

    # Créer une page pour le pdf
    page = Page()

    page_layout = SingleColumnLayout(page)

    page_layout.vertical_margin = page.get_page_info().get_height() \
                                                                * Decimal(0.02)
    page_layout.add(pdf_entete_logo(facture_devis, identifiant))


    # Informations du prestatire et du client
    page_layout.add(pdf_champs_prestataire_client(facture_devis))

    # Espace pour séparer
    page_layout.add(Paragraph(" "))

    # Tableaux des articles et des taxes
    page_layout.add(pdf_articles_taxes(facture_devis, 
                                                monnaie, taxe, remise))
    
    if(chemin == None):
        chemin = "output.pdf"
    
    #On rajoute l'extension si elle n'est pas déjà présente
    if(chemin[-4:] != ".pdf"):
        chemin += ".pdf"

    pdf.append_page(page)

    with open(chemin, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
    
    

if __name__ == "__main__":
    artisan = Utilisateur("Facturio","15 rue des champs Cuers","0734567221", 
                                       "128974654", "facturio@gmail.com",
                                                                "logo.jpg")

    client_physique = Client("Lombardo", "Quentin", 
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")
                    
    client_moral = Entreprise("LeRoy", "Ben", "Karim", "287489404",
                "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")

    ordinateur = Article("ordinateur", 1684.33)
    cable_ethernet = Article("cable ethernet", 9.99)
    telephone = Article("telephone", 399.99)
    casque = Article("casque", 69.99)

    paiements = [Acompte(1230.0), Acompte(654)]

    articles = [(ordinateur, 3), (cable_ethernet, 10), (telephone,1), (casque, 6)]


    fact = Facture(artisan, client_moral, articles, liste_acomptes =paiements, 
                            commentaire="Facture de matériel informatiques")


    dev = Devis(artisan, client_physique, articles, 
                            commentaire="Facture de matériel informatiques")
    mon = "€"

    construire_pdf(dev, 2, mon, 0, 150, "exemple_devis.pdf")
    construire_pdf(fact, 4, mon, 0.2, 130, "exemple_facture")