


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
from decimal import Decimal
from pathlib import Path
import sys
#Import classes objet
sys.path.append('../')
from Invoice_classes.estimate_invoice import *
#Layout Element pour l'insertion d'icônes dans le pdf
mail_icon: LayoutElement = Image(
    image=Path("icons/mail.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
email_icon: LayoutElement = Image(
    image=Path("icons/email.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
phone_icon: LayoutElement = Image(
    image=Path("icons/phone.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
business_icon: LayoutElement = Image(
    image=Path("icons/business.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
person_icon: LayoutElement = Image(
    image=Path("icons/person.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
def pdf_header(receipt, id):
    """
    Construction de l'entête du pdf
    """
    #Initialisation d'une table avec des colones flexibles
    table = FlexibleColumnWidthTable(number_of_rows= 2, number_of_columns=4) 
    ### Première ligne
    #Insertion du logo si il existe
    if(receipt.user.logo != None):
        table.add(TableCell(   
        Image(        
        image=Path(receipt.user.logo),        
        width=Decimal(75),        
        height=Decimal(75),    
        ), row_span=2))
    else:
        table.add(TableCell(Paragraph(" ", padding_left=Decimal(50)),
                                                                row_span=2))

    table.add(Paragraph(" ", padding_left=Decimal(190)))

    #Numéro de la facture ou du devis
    if isinstance(receipt, Invoice):      
        table.add(Paragraph("Facture", 
                font="Helvetica-Bold",horizontal_alignment=Alignment.LEFT))

    elif isinstance(receipt, Estimate):
        table.add(Paragraph(f"Devis", 
                font="Helvetica-Bold",horizontal_alignment=Alignment.LEFT))
                  
    table.add(Paragraph(f" # {id}",respect_spaces_in_text=True)) 
    ### Deuxième Ligne
    table.add(Paragraph(" "))
    table.add(Paragraph("Date", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.LEFT))       
    table.add(Paragraph(f" {receipt.date_string()}", 
                                        respect_spaces_in_text=True))  
    table.no_borders()
    return table

def pdf_customer_company(table,customer, provider):
    """
    Construit la partie client lorsqu'il s'agit d'une entreprise
    """
    #Deuxième moitié deuxième ligne
    table.add(business_icon)
    table.add(Paragraph(customer.company_name))
    ### Troisième Ligne
    #On affiche l'email du client et du prestataire si ils existent
    if(provider.email == None):
        table.add(Paragraph(" ")); table.add(Paragraph(" "))  
    else:
        table.add(email_icon)  
        table.add(Paragraph(provider.email))

    table.add(email_icon)  
    table.add(Paragraph(customer.email))  
    ### Quatrième Ligne
    table.add(mail_icon)
    table.add(Paragraph(provider.adr))
    table.add(mail_icon)  
    table.add(Paragraph(customer.adr))
    ### Cinquième Ligne
    table.add(phone_icon)
    table.add(Paragraph(provider.phone))
    table.add(phone_icon)  
    table.add(Paragraph(customer.phone))
    ### Sixième Ligne
    table.add(Paragraph("N°", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.CENTERED))
    table.add(Paragraph(f"{provider.siren_number}"))
    table.add(Paragraph("N°", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.CENTERED))
    table.add(Paragraph(f"{customer.siren_number}"))
    ### Septième Ligne
    table.add(Paragraph(" ")); table.add(Paragraph(" "))
    # On affiche la ligne correspondant au représentant de l'entreprise  
    table.add(person_icon)
    table.add(Paragraph(f"{customer.first_name} {customer.surname}")) 
    return table

def pdf_customer_individual(table, customer, provider):
    """
    Construit la partie client lorsqu'il s'agit d'une entreprise
    """
    #Deuxième moitié deuxième ligne
    table.add(person_icon)
    table.add(Paragraph(f"{customer.first_name} {customer.surname}"))      
    ### Troisième Ligne
    #On affiche l'email du client et du prestataire si ils existent
    if(provider.email == None):
        table.add(Paragraph(" ")); table.add(Paragraph(" "))  
    else:
        table.add(email_icon)  
        table.add(Paragraph(provider.email))

    if(customer.email == None):
        table.add(Paragraph(" ")); table.add(Paragraph(" "))
    else:
        table.add(email_icon)  
        table.add(Paragraph(customer.email))  

    ### Quatrième Ligne
    table.add(mail_icon)
    table.add(Paragraph(provider.adr))
    #On affiche l'adresse du client si elle existe
    if(customer.adr == None):
        table.add(Paragraph(" ")); table.add(Paragraph(" "))
    else:
        table.add(mail_icon)  
        table.add(Paragraph(customer.adr))

    ### Cinquième Ligne
    #On affiche le numéro téléphone du client si il existe
    table.add(phone_icon)
    table.add(Paragraph(provider.phone))

    if(customer.phone == None):
        table.add(Paragraph(" ")); table.add(Paragraph(" "))
    else:
        table.add(phone_icon)  
        table.add(Paragraph(customer.phone))

    ### Sixième Ligne
    table.add(Paragraph("N°", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.CENTERED))
    table.add(Paragraph(f"{provider.siren_number}"))
    table.add(Paragraph(" ")); table.add(Paragraph(" ")) 
    ### Septième Ligne
    table.add(Paragraph(" ")); table.add(Paragraph(" "))
    table.add(Paragraph(" "));table.add(Paragraph(" "))   
    return table

def pdf_provider_customer(receipt):   
    """
    Retourne une table liée aux informations du prestataire et du client
    """
    provider = receipt.user
    customer = receipt.client
    ### Première Ligne
    table = FlexibleColumnWidthTable(number_of_rows=7, number_of_columns=4) 
    table.add(Paragraph("De ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.LEFT))
    table.add(Paragraph(" ", padding_left=Decimal(240)))
    table.add(Paragraph("A ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(" "))
         
	### Deuxième Ligne
    table.add(business_icon)
    table.add(Paragraph(provider.company_name))
    #On vérifie si l'on traite une entreprise ou un particulier
    if(isinstance(customer, Company)):
        table = pdf_customer_company(table, customer, provider)
    else:
        table = pdf_customer_individual(table, customer, provider)
    
    table.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), 
                                                                Decimal(1))    		
    table.no_borders()
    return table

def pdf_articles_tax(receipt, currency, tax, discount):
    """
    Construit la listes des articles et des taxes
    """
    art_list = receipt.articles_list
    articles_nb = len(art_list)
    #Calcule du nombre de lignes que le tableau va prendre
    rows_nb = articles_nb + 5
    if(rows_nb < 15):
        rows_nb = 15
    
    table = Table(number_of_rows=rows_nb, number_of_columns=4)  
    for h in ["DESCRIPTION", "QUANTITÉ", "PRIX UNITAIRE", "TOTAL"]:  
        table.add(  
            TableCell(  
                Paragraph(h, font_color=X11Color("White")),  
                background_color=HexColor("5f5f5f"),  
            )  
        ) 
    #Couleur différente pour chaque lignes qui se suivent 
    odd = HexColor("BBBBBB")  
    even = HexColor("FFFFFF")  
    #Variable pour savoir la parité de la ligne
    parity = True
    for article in art_list:  
        c = even if parity else odd 
        parity ^= True
        table.add(TableCell(Paragraph(f"{article[0].description}", 
                            respect_newlines_in_text=True), 
                                                    background_color=c))  
        table.add(TableCell(Paragraph(f"{article[1]}"), background_color=c))  
        table.add(TableCell(Paragraph(f"{article[0].price} {currency}"), 
                                                        background_color=c))   
        table.add(TableCell(Paragraph(
                        f"{round(article[1] * article[0].price,2)} {currency}")
                                                        , background_color=c))    
    #Si on a moins de 10 articles alors on rajoute des lignes vides
    # pour le style
    while(articles_nb < 10):
        c = even if parity else odd 
        parity ^= True
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        table.add(TableCell(Paragraph(" "), background_color=c)) 
        articles_nb += 1 
    table = pdf_taxes(table, receipt, currency, tax, discount)
    table.set_padding_on_all_cells(Decimal(2), 
                                        Decimal(15), Decimal(2), Decimal(2))  
    return table

def pdf_taxes(table, receipt, currency, tax, discount):
    """
    Construit la partie liée aux taxes pour les factures
    """
    #Calcul du sous total
    table.add(TableCell(Paragraph("Sous-total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT,), col_span=3,))  
    table.add(TableCell(Paragraph(f"{receipt.total()} {currency}", 
                                        horizontal_alignment=Alignment.RIGHT)))
    #Si il s'agit d'une facture on fait apparaître les acomptes
    # à l'affichage et dans le calcul
    if(isinstance(receipt, Invoice)):
        #Calcule du total et des taxes
        tt = receipt.total_with_advances()-discount
        tx = tt*tax   
        table.add(TableCell(Paragraph("Remises/Acomptes", 
            font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),
                                                                col_span=3,))
        table.add(TableCell(Paragraph(
                       f"{receipt.total_of_advances() + discount} {currency}", 
                                       horizontal_alignment=Alignment.RIGHT)))
    else:
        #Calcule du total et des taxes
        tt = round(receipt.total()-discount, 2)
        tx = round(tt*tax,2)  
        table.add(TableCell(Paragraph("Remises", 
            font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),
                                                                col_span=3,))
        table.add(TableCell(Paragraph(f"{discount} {currency}", 
                                       horizontal_alignment=Alignment.RIGHT)))
    #Calcul de la partie taxe
    table.add(TableCell(Paragraph(f"Taxes ({tax*100}%)", 
    font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3,)) 
    table.add(TableCell(Paragraph(f"{round(tx, 2)} {currency}", 
                                        horizontal_alignment=Alignment.RIGHT))) 
    #Cacul du total 
    table.add(TableCell(Paragraph("Total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT  ), col_span=3,))  
    table.add(TableCell(Paragraph(f"{round(tt + tx, 2)} {currency} ", 
                    horizontal_alignment=Alignment.RIGHT)))   
    return table

def build_pdf(receipt, id, currency, tax, discount, path="output.pdf"):
    """
    Fonction d'assemblage du pdf
    """
    # Créer un document pdf
    pdf = Document()
    # Créer une page pour le pdf
    page = Page()
    #Disposition de la page
    page_layout = SingleColumnLayout(page)
    #Calcul des marge
    page_layout.vertical_margin = page.get_page_info().get_height() \
                                                                * Decimal(0.02)
    #Construction de l'entête
    page_layout.add(pdf_header(receipt, id))
    # Informations du prestatire et du client
    page_layout.add(pdf_provider_customer(receipt))
    # Espace pour séparer
    page_layout.add(Paragraph(" "))
    # Tableaux des articles et des tax
    page_layout.add(pdf_articles_tax(receipt, currency, tax, discount))
    #On rajoute l'extension pdf si elle n'est pas déjà présente
    if(path[-4:] != ".pdf"):
        path += ".pdf"
    #On ajoute la page au pdf
    pdf.append_page(page)
    #Écriture du pdf au chemin indiqué
    with open(path, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
    
if __name__ == "__main__":
    artisan = User("Facturio","15 rue des champs Cuers","0734567221", 
                                       "128974654", "facturio@gmail.com",
                                                                "logo.jpg")
    client_physique = Client("Lombardo", "Quentin", 
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")                  
    client_moral = Company("LeRoy", "Ben", "Karim", "287489404",
                "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")
    ordinateur = Article("ordinateur", 1684.33)
    cable_ethernet = Article("cable ethernet", 9.99)
    telephone = Article("telephone", 399.99)
    casque = Article("casque", 69.99)
    paiements = [Advance(1230.0), Advance(654)]
    articles = [(ordinateur, 3), (cable_ethernet, 10), (telephone,1), 
                                                                (casque, 6)]
    fact = Invoice(artisan, client_moral, articles, advances_list =paiements, 
                            note="Invoice de matériel informatiques")
    dev = Estimate(artisan, client_physique, articles, 
                            note="Invoice de matériel informatiques")
    mon = "€"
    build_pdf(dev, 27, mon, 0, 150, "exemple_devis.pdf")
    build_pdf(fact, 490, mon, 0.2, 130, "exemple_facture")