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

import sys

from numpy import isin
#Import classes objet
sys.path.append('../')
from classes.estimate_invoice import *
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

def pdf_provider_client(receipt: Union[Estimate,Invoice]):   
    """
    Retourne une table liée aux informations du prestataire et du client
    """
    provider = receipt.user
    client = receipt.client
    ### Première Ligne
    table = FlexibleColumnWidthTable(number_of_rows=6, number_of_columns=4) 
    buisness_number_table = FlexibleColumnWidthTable(number_of_rows=1, number_of_columns=5) 

    table.add(Paragraph("De ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.LEFT))
    table.add(Paragraph(" ", padding_left=Decimal(240)))
    table.add(Paragraph("A ", font="Helvetica-Bold",
                                        horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(" "))
         
    provider_list = provider.dump_to_field()
    client_list = client.dump_to_field()
    provider_icon_list = [business_icon, email_icon, mail_icon, phone_icon, 
                   person_icon]
     
    buisness_number_table.add(Paragraph("N°SIREN", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.LEFT))
    buisness_number_table.add(Paragraph(provider_list[-1], 
                                        horizontal_alignment=Alignment.RIGHT))
    buisness_number_table.add(Paragraph(" ", padding_left=Decimal(145)))

    if(provider_list[1] == None):
        del provider_icon_list[1]
        del provider_list[1]
    

    if(isinstance(client, Company)):
        table, buisness_number_table = provider_company_table(table, 
        buisness_number_table, provider_list, provider_icon_list, client_list)  

    elif(isinstance(client, Client)):
        table, buisness_number_table = provider_individual_table(table, 
        buisness_number_table, provider_list, provider_icon_list, client_list)
    
    table.set_padding_on_all_cells(Decimal(1), Decimal(1), Decimal(1), 
                                                                Decimal(1))    		
    table.no_borders()
    buisness_number_table.set_padding_on_all_cells(Decimal(1), Decimal(1), 
                                                        Decimal(1), Decimal(1))    		
    buisness_number_table.no_borders()

    return table, buisness_number_table

def provider_company_table(
        table : FlexibleColumnWidthTable, 
        buisness_number_table : FlexibleColumnWidthTable, 
        provider_list: list,
        provider_icon_list: list, 
        client_list: list
                            ):  
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

        if(i != 5):
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))
            table.add(company_icon_list[-1])
            table.add(Paragraph(client_list[-2]))
        

        buisness_number_table.add(Paragraph("N°SIREN", font="Helvetica-Bold", 
                                    horizontal_alignment=Alignment.LEFT))
        buisness_number_table.add(Paragraph(client_list[-1])) 

        return table, buisness_number_table
        

def provider_individual_table(
        table : FlexibleColumnWidthTable, 
        buisness_number_table : FlexibleColumnWidthTable, 
        provider_list: list,
        provider_icon_list: list, 
        client_list: list
                            ):   
        print(client_list)
        client_icon_list = [person_icon, email_icon, mail_icon, phone_icon]
        for i in range(3, 0, -1):  
            if(client_list[i] == None):
                del client_icon_list[i]
                del client_list[i]
        i = 0
        print(client_list)
        length_min = len(client_icon_list)
        while(i < length_min):
            table.add(provider_icon_list[i])  
            table.add(Paragraph(provider_list[i]))
            table.add(client_icon_list[i])  
            table.add(Paragraph(client_list[i]))
            i+=1

        i = length_min
        length_min = len(provider_icon_list)
        while(i < length_min):
            table.add(provider_icon_list[i])  
            table.add(Paragraph(provider_list[i]))
            table.add(Paragraph(" "))  
            table.add(Paragraph(" "))
            i+=1

        if(i != 5):
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))
            table.add(Paragraph(" "))

        buisness_number_table.add(Paragraph(" "))
        buisness_number_table.add(Paragraph(" "))     

        return table, buisness_number_table

def build_pdf(receipt: Union[Invoice, Estimate], id: int, 
                                 path: str ="output.pdf", currency: str = "€"):
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

    # Informations du prestatire et du client
    tb1, tb2 = pdf_provider_client(receipt)
    page_layout.add(tb1)
    page_layout.add(tb2)

    
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
                        "128974654", "Tom", "Pommier", "facturio@gmail.com",
                                                            "logo.jpg")
    client_physique = Client("Lombardo", "Quentin", 
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")  
                        
    client_moral = Company("LeRoy",  "LeRoy83@sfr.fr", "12 ZAC de La Crau",
                             "0345678910", "Ben", "Karim","287489404")
    ordinateur = Article("ordinateur", 1684.33)
    cable_ethernet = Article("cable ethernet", 9.99)
    telephone = Article("telephone", 399.99)
    casque = Article("casque", 69.99)
    paiements = [Advance(1230.0), Advance(654)]
    articles = [(ordinateur, 3), (cable_ethernet, 10), (telephone,1), 
                                                                (casque, 6)]
    fact = Invoice(artisan, client_moral, articles, advances_list =paiements, 
                        taxes = 0.2, note="Invoice de matériel informatiques")
    dev = Estimate(artisan, client_physique, articles, taxes=0,
                            note="Invoice de matériel informatiques")

    build_pdf(dev, 27, "exemple_devis.pdf")
    #build_pdf(fact, 490, "exemple_facture")
