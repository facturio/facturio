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
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.table.fixed_column_width_table \
                            import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.table.flexible_column_width_table \
                                            import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.layout_element import LayoutElement
#Import librairie standard
from decimal import Decimal
from pathlib import Path
from typing import Union
from facturio.classes.invoice_misc import Advance, Article, Invoice, Estimate
from facturio.classes.client import Company, Client
from facturio.classes.user import User

#Layout Element pour l'insertion d'icônes dans le pdf
mail_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/mail.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
email_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/email.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
phone_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/phone.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
business_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/business.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)
person_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/person.png"),
    width=Decimal(10),
    height=Decimal(10),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)

dot_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/dot.png"),
    width=Decimal(3),
    height=Decimal(3),
    padding_top=Decimal(5),
    padding_left=Decimal(3)
)


small_phone_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/phone.png"),
    width=Decimal(7),
    height=Decimal(7),
    padding_top=Decimal(3),
    padding_left=Decimal(3)
)

small_mail_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/mail.png"),
    width=Decimal(7),
    height=Decimal(7),
    padding_top=Decimal(3),
    padding_left=Decimal(3)
)
small_email_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/email.png"),
    width=Decimal(7),
    height=Decimal(7),
    padding_top=Decimal(3),
    padding_left=Decimal(3)
)

small_person_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/person.png"),
    width=Decimal(7),
    height=Decimal(7),
    padding_top=Decimal(3),
    padding_left=Decimal(3)
)

small_business_icon: LayoutElement = Image(
    image=Path("build_pdf/icons/business.png"),
    width=Decimal(7),
    height=Decimal(7),
    padding_top=Decimal(3),
    padding_left=Decimal(3)
)

#Fonction pour les couleurs
def hex_to_rgb(value: str):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(red: int, green: int, blue: int):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

def shade_color(color: tuple[int, int, int], factor:int):
        """
        Retourne la couleur rgb assombri ou éclaircir
        """
        shaded_color= []
        for c in color:
            x = int(c * factor)
            if(x > 255):
                x = 255
            if(x < 0):
                x = 0
            shaded_color.append(x)
        return shaded_color

def pdf_header(receipt: Union[Invoice, Estimate], id: int):
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

def pdf_provider_client(receipt: Union[Estimate,Invoice]):
    """
    Retourne une table liée aux informations du prestataire et du client
    """
    provider = receipt.user
    client = receipt.client
    ### Première Ligne
    table = FlexibleColumnWidthTable(number_of_rows=6, number_of_columns=4) 
    business_number_table = FlexibleColumnWidthTable(number_of_rows=1, number_of_columns=5) 

    table.add(Paragraph("De ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.LEFT))
    table.add(Paragraph(" ", padding_left=Decimal(240)))
    table.add(Paragraph("A ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(" "))
         
    #On met les champs client, et utilisateur dans des listes
    #On fait cela car certains champs sont optionnels en utilisant
    #une liste on évite d'avoir des trous aux endroits où un champ
    #optionnel n'a pas été rempli
    provider_list = provider.dump_to_field()
    client_list = client.dump_to_field()
    provider_icon_list = [business_icon, email_icon, mail_icon, phone_icon, 
                   person_icon]
    #Numero SIREN de l'artisan
    business_number_table.add(Paragraph("N°SIREN", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.LEFT))
    business_number_table.add(Paragraph(provider_list[-1], 
                                        horizontal_alignment=Alignment.RIGHT))
    business_number_table.add(Paragraph(" ", padding_left=Decimal(145)))
    
    #Si le champ email pour l'utilisateur n'est pas remplit,
    #On supprime l'élément dans la liste
    if(provider_list[1] == None):
        del provider_icon_list[1]
        del provider_list[1]
    #On appelle une fonction si le client est une entité morale
    #ou physique
    if(isinstance(client, Company)):
        table, business_number_table = provider_company_table(table, 
        business_number_table, provider_list, provider_icon_list, client_list)  

    elif(isinstance(client, Client)):
        table, business_number_table = provider_individual_table(table, 
        business_number_table, provider_list, provider_icon_list, client_list)
    
    table.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), 
                                                                Decimal(1))    		
    table.no_borders()
    business_number_table.set_padding_on_all_cells(Decimal(1), Decimal(1), 
                                                        Decimal(1), Decimal(1))    		
    business_number_table.no_borders()

    return table, business_number_table

def provider_company_table(
        table : FlexibleColumnWidthTable, 
        business_number_table : FlexibleColumnWidthTable, 
        provider_list: list,
        provider_icon_list: list, 
        client_list: list
                            ):  
        """
        Met en place le layout correspondant aux champs de l'artisan
        et aux champs du client lorsqu'il est moral
        """
        company_icon_list = [business_icon, email_icon, mail_icon, phone_icon, 
                   person_icon]
        length_min = len(provider_icon_list)
        i = 0
        while(i < length_min):
            table.add(provider_icon_list[i])  
            table.add(Paragraph(provider_list[i]))
            table.add(company_icon_list[i])  
            table.add(Paragraph(client_list[i]))
            i+=1
    #Un bloc if dans l'éventualité ou un utilisateur n'a pas d'email
        if(i != 5):
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))
            table.add(company_icon_list[-1])
            table.add(Paragraph(client_list[-2]))
        
        #Comme toutes les colones d'un tableu doivent être de même
        #taille on fait un 2ème tableu pour le numero SIREN
        business_number_table.add(Paragraph("N°SIREN", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.LEFT))
        business_number_table.add(Paragraph(client_list[-1])) 

        return table, business_number_table
        
def provider_individual_table(
        table : FlexibleColumnWidthTable, 
        business_number_table : FlexibleColumnWidthTable, 
        provider_list: list,
        provider_icon_list: list, 
        client_list: list
                            ):
        """
        Met en place le layout correspondant aux champs de l'artisan
        et aux champs du client lorsqu'il est physique
        """   
        client_icon_list = [person_icon, email_icon, mail_icon, phone_icon]
        for i in range(3, 0, -1):
            #On supprime tous les champs optionnels qui n'ont pas été
            #remplit
            if(client_list[i] == None):
                del client_icon_list[i]
                del client_list[i]
        i = 0
        length_min = len(client_icon_list)
        
        while(i < length_min):
            table.add(provider_icon_list[i])  
            table.add(Paragraph(provider_list[i]))
            table.add(client_icon_list[i])  
            table.add(Paragraph(client_list[i]))
            i+=1

        i = length_min
        length_min = len(provider_icon_list)
        #Comme l'utilisateur a plus de champs que clients alors on
        #fait une autre boucle a part
        while(i < length_min):
            table.add(provider_icon_list[i])  
            table.add(Paragraph(provider_list[i]))
            table.add(Paragraph(" "))  
            table.add(Paragraph(" "))
            i+=1
        #Si l'utilisateur n'a pas d'email alors on fait une ligne vide
        if(i != 5):
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))

        #Un cleint physique n'a pas de numero SIREN
        business_number_table.add(Paragraph(" "))
        business_number_table.add(Paragraph(" "))     

        return table, business_number_table

def pdf_provider_inline(receipt: Union[Invoice, Estimate]):
    """
    Retourne une table avec les informations liées à l'utilisateur
    en ligne
    """
    artisan = receipt.user
    if(artisan.email == None):
        table_01 = FlexibleColumnWidthTable(number_of_rows=1, 
                                                        number_of_columns=14)
    else:
        table_01 = FlexibleColumnWidthTable(number_of_rows=1, 
                                                        number_of_columns=17)
    

    table_01.add(small_business_icon)
    table_01.add(Paragraph(artisan.company_name, font_size=Decimal(8)))
    table_01.add(dot_icon)

    if(artisan.email):
        table_01.add(small_email_icon)
        table_01.add(Paragraph(artisan.email, font_size=Decimal(8)))
        table_01.add(dot_icon)
    
    table_01.add(small_mail_icon)
    table_01.add(Paragraph(artisan.adress, font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(small_phone_icon)
    table_01.add(Paragraph(artisan.phone_number, font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(small_person_icon)
    table_01.add(Paragraph(f"{artisan.first_name} {artisan.last_name}", font="Helvetica",
                                                        font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(Paragraph("N°SIREN", font="Helvetica-Bold",
                    font_size=Decimal(8),horizontal_alignment=Alignment.LEFT))
    table_01.add(Paragraph(artisan.business_number, font_size=Decimal(8)))


    table_01.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), 
                                                                Decimal(1))    		
    table_01.no_borders()

    return table_01

def pdf_company_inline(receipt: Union[Invoice, Estimate]):
    """
    Retourne une table avec les informations liées à un client moral
    en ligne
    """
    client = receipt.client
    
    table_01 = FlexibleColumnWidthTable(number_of_rows=1,  number_of_columns=17)
    table_01.add(small_business_icon)
    table_01.add(Paragraph(client.company_name, font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(small_email_icon)
    table_01.add(Paragraph(client.email, font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(small_mail_icon)
    table_01.add(Paragraph(client.adress, font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(small_phone_icon)
    table_01.add(Paragraph(client.phone_number, font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(small_person_icon)
    table_01.add(Paragraph(f"{client.first_name} {client.last_name}", 
                                                        font_size=Decimal(8)))
    table_01.add(dot_icon)
    table_01.add(Paragraph("N°SIREN", font="Helvetica-Bold",
                    font_size=Decimal(8),horizontal_alignment=Alignment.LEFT))
    table_01.add(Paragraph(client.business_number, font_size=Decimal(8)))
    table_01.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), 
                                                                Decimal(1))    		
    table_01.no_borders()

    return table_01

def pdf_individual_inline(receipt: Union[Invoice, Estimate]):
    """
    Retourne une table avec les informations liées à un client moral
    en ligne
    """
    client = receipt.client
    client_list = client.dump_to_field()[1:]
    client_icon_list = [small_email_icon, small_mail_icon, small_phone_icon]
    #On supprime tous les champs optionnels qui n'ont pas été
    #remplit
    for i in range(2, -1, -1):
        if(client_list[i] == None):
            del client_icon_list[i]
            del client_list[i]

    n = len(client_list)
    column_numbers = 2 + 3 * n
    table_01 = FlexibleColumnWidthTable(number_of_rows=1,  
                                             number_of_columns=column_numbers)
    table_01.add(small_person_icon)
    table_01.add(Paragraph(f"{client.first_name} {client.last_name}", 
                                                        font_size=Decimal(8)))
    i = 0
    while(i < n):
        table_01.add(dot_icon)   
        table_01.add(client_icon_list[i])
        table_01.add(Paragraph(client_list[i], font_size=Decimal(8)))
        i+=1

    table_01.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), 
                                                                Decimal(1))    		
    table_01.no_borders()

    return table_01

def pdf_client_inline(receipt: Union[Invoice, Estimate]):
    """
    Retourne une table avec les informations liées à un client
    """
    if(isinstance(receipt.client, Company)):
        return pdf_company_inline(receipt)

    elif(isinstance(receipt.client, Client)):
        return pdf_individual_inline(receipt)
    
def pdf_articles_total(receipt: Union[Invoice, Estimate], currency: str, 
                                                        color: str):
    """
    Construit la listes des articles et des taxes
    """
    art_list = receipt.articles_list
    articles_nb = len(art_list)
    #Calcule du nombre de lignes que le tableau va prendre
    rows_nb = articles_nb + 5
    if(rows_nb < 15):
        rows_nb = 15
    if(isinstance(receipt, Estimate)):
        rows_nb -= 1

    table = Table(number_of_rows=rows_nb, number_of_columns=4)  
    for h in ["DESCRIPTION", "QUANTITÉ", "PRIX UNITAIRE", "TOTAL"]:  
        table.add(  
            TableCell(  
                Paragraph(h, font_color = HexColor("ffffff")),  
                background_color = HexColor(color),  
            )  
        ) 
    #Couleur différente pour chaque lignes qui se suivent 
    odd = HexColor(rgb_to_hex(*shade_color(hex_to_rgb(color),1.6)))  
    even = HexColor("FFFFFF")  
    #Variable pour savoir la parité de la ligne
    parity = True
    for article in art_list:  
        c = even if parity else odd 
        parity ^= True
        table.add(TableCell(Paragraph(f"{article.title}", 
                            respect_newlines_in_text=True), 
                                                    background_color=c))  
        table.add(TableCell(Paragraph(f"{article.quantity}"), background_color=c))  
        table.add(TableCell(Paragraph(f"{article.price} {currency}"), 
                                                        background_color=c))   
        table.add(TableCell(Paragraph(
                    f"{round(article.quantity * article.price,2)} {currency}")
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
    
    #Calcul du sous total
    table.add(TableCell(Paragraph("Sous-total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT,), col_span=3,))  
    table.add(TableCell(Paragraph(f"{receipt.subtotal()} {currency}", 
                                        horizontal_alignment=Alignment.RIGHT)))

    if(isinstance(receipt, Invoice)):
        table = pdf_invoice_total(table, receipt, currency) 
    elif(isinstance(receipt, Estimate)):
        table = pdf_estimate_total(table, receipt, currency) 

    table.set_padding_on_all_cells(Decimal(2), 
                                        Decimal(15), Decimal(2), Decimal(2))
    return table

def pdf_invoice_total(table: Table, receipt:Invoice, currency: str):
    """
    Construit la partie liée aux calcul des totaux pour les factures
    """
    #Calcul des Acomptes
    table.add(TableCell(Paragraph("Acomptes", 
        font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),
                                                                col_span=3,))
    table.add(TableCell(Paragraph(f"{receipt.total_of_advances()} {currency}", 
                                       horizontal_alignment=Alignment.RIGHT)))

    #Calcul de la partie taxe
    table.add(TableCell(Paragraph(f"Taxes ({receipt.taxes*100}%)", 
    font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3,)) 
    table.add(TableCell(Paragraph(f"{round(receipt.total_of_taxes(), 2)} "\
                                  f"{currency}", 
                                        horizontal_alignment=Alignment.RIGHT))) 
    #Cacul du total 
    table.add(TableCell(Paragraph("Total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT  ), col_span=3,))  
    table.add(TableCell(Paragraph(f"{round(receipt.total_with_advances(), 2)}"\
                                  f" {currency} ", 
                    horizontal_alignment=Alignment.RIGHT)))   
    return table

def pdf_estimate_total(table: Table, receipt:Estimate, currency: str):
    """
    Construit la partie liée aux taxes pour les factures

    """
    #Calcul de la partie taxe
    table.add(TableCell(Paragraph(f"Taxes ({receipt.taxes*100}%)", 
    font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3,)) 
    table.add(TableCell(Paragraph(f"{round(receipt.total_of_taxes(), 2)} "\
                                  f"{currency}", 
                                        horizontal_alignment=Alignment.RIGHT))) 
    #Cacul du total 
    table.add(TableCell(Paragraph("Total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT  ), col_span=3,))  
    table.add(TableCell(Paragraph(f"{round(receipt.total_with_taxes())} "\
                                  f"{currency} ", 
                    horizontal_alignment=Alignment.RIGHT)))   
    return table

def build_pdf(receipt: Union[Invoice, Estimate], id: int,
    path: str ="output.pdf", color: str = "5f5f5f", currency: str = "€", 
                   inline: bool = False, prominent_article_table: bool = False):
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

    if(prominent_article_table):
        # Tableaux des articles et des tax
        page_layout.add(pdf_articles_total(receipt, currency,color))
    # Informations du prestatire et du client
    if(inline):
        page_layout.add(Paragraph("Prestataire", font="Helvetica-Bold", 
                                                        font_size= Decimal(8)))
        page_layout.add(pdf_provider_inline(receipt))
        page_layout.add(Paragraph("Client", font="Helvetica-Bold", 
                                                        font_size= Decimal(8)))
        page_layout.add(pdf_client_inline(receipt))
   
    else:
        tb1, tb2 = pdf_provider_client(receipt)
        page_layout.add(tb1)
        page_layout.add(tb2)

    if(not prominent_article_table):
        # Tableaux des articles et des tax
        page_layout.add(pdf_articles_total(receipt, currency, color))
    
    #On rajoute l'extension pdf si elle n'est pas déjà présente
    if(path[-4:] != ".pdf"):
        path += ".pdf"
    #On ajoute la page au pdf
    pdf.append_page(page)
    #Écriture du pdf au chemin indiqué
    with open(path, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
    
if __name__ == "__main__":
    artisan = User("Facturio", "15 rue des champs Cuers", "0734567221", 
                        "128974654", "Tom", "Pommier", "facturio@gmail.com")
                                                            
    client_physique = Client("Lombardo", "Quentin", 
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")
                        
    client_moral = Company("LeRoy",  "LeRoy83@sfr.fr", "12 ZAC de La Crau",
                             "0345678910", "Ben", "Karim","287489404")
    ordinateur = Article("ordinateur", 1684.33, 3)
    cable_ethernet = Article("cable ethernet", 9.99, 10)
    telephone = Article("telephone", 399.99, 1)
    casque = Article("casque", 69.99, 6)
    paiements = [Advance(1230.0), Advance(654)]
    articles = [ordinateur, cable_ethernet, telephone, casque]
    fact = Invoice(artisan, client_moral, articles, advances_list =paiements,
                        taxes = 0.2, note="Invoice de matériel informatiques",
                   date = 1230, amount=100)
    dev = Estimate(artisan, client_physique, articles, taxes=0,
                            note="Invoice de matériel informatiques")

    build_pdf(dev, 27, "exemple_devis.pdf")
    build_pdf(fact, 490, "exemple_facture", inline=True)
