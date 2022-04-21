#Import de borb
import numbers
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import Paragraph
from borb.pdf import PDF
from borb.pdf.canvas.layout.page_layout.multi_column_layout \
                                        import SingleColumnLayout

#######################################
from borb.pdf.canvas.layout.page_layout.browser_layout \
                                        import BrowserLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
#######################################

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
from typing import Union

from matplotlib import table
from facturio.classes.invoice_misc import Advance, Article, Invoice, \
                                              Estimate
from facturio.classes.client import Company, Client
from facturio.classes.user import User



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



def pdf_articles_total(receipt: Union[Invoice, Estimate], currency: str, 
                                                        color: str):
    """
    Construit la listes des articles et des taxes
    """
    art_list = receipt.articles_list
    articles_nb = len(art_list)
    #Calcule du nombre de lignes que le tableau va prendre
    
    total_part = 4
    if(isinstance(receipt, Estimate)):
        total_part -= 1
    
    rows_nb = 2 * articles_nb + total_part + 1
    if(articles_nb > 5):
        #Premier tableau avec l'entete
        table_array = [Table(number_of_rows=11, number_of_columns=4)]
        current_rows_nb = rows_nb - (11+total_part)
        #Tableaux intermédiaires
        while(current_rows_nb > 10):
            table_array.append(Table(number_of_rows=10, number_of_columns=4,))
            current_rows_nb -= 10
        #Tableaux avec les totaux
        table_array.append(Table(number_of_rows=current_rows_nb + total_part, 
                                                         number_of_columns=4))
    else:
        table_array = [Table(number_of_rows=rows_nb, number_of_columns=4)]
     
    for h in ["DESCRIPTION", "QUANTITÉ", "PRIX UNITAIRE", "TOTAL"]:  
        table_array[0].add(  
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
    list_art = receipt.articles_list
    cpt_art = 0
    #Construction des tableaux intermédiaires
    for i in range(len(table_array)-1):
        for j in range(5):
            c = even if parity else odd 
            parity ^= True
            table_array[i].add(TableCell(Paragraph(f"{list_art[cpt_art].title}"),
                                                        background_color=c))  
            table_array[i].add(TableCell(Paragraph(f"{list_art[cpt_art].quantity}"), 
                                                            background_color=c))  

            table_array[i].add(TableCell(Paragraph(
            f"{list_art[cpt_art].price} {currency}"), background_color=c))   
            table_array[i].add(TableCell(Paragraph(
 f"{round(list_art[cpt_art].quantity * list_art[cpt_art].price,2)} {currency}")
                                                        , background_color=c))  
            table_array[i].add(TableCell(Paragraph(
                                        f"{list_art[cpt_art].description}",
                        font_size=Decimal(8)),  background_color=c))
            table_array[i].add(TableCell(Paragraph(" "), background_color=c)) 
            table_array[i].add(TableCell(Paragraph(" "), background_color=c)) 
            table_array[i].add(TableCell(Paragraph(" "), background_color=c))
            table_array[i].set_padding_on_all_cells(Decimal(2), 
                                        Decimal(15), Decimal(2), Decimal(2)) 
            cpt_art+=1
    left_art = articles_nb - cpt_art

    #Derniere table
    while(left_art > 0):
        c = even if parity else odd 
        parity ^= True
        table_array[-1].add(TableCell(Paragraph(f"{list_art[cpt_art].title}"),
                                                        background_color=c))  
        table_array[-1].add(TableCell(Paragraph(f"{list_art[cpt_art].quantity}"), 
                                                            background_color=c))  

        table_array[-1].add(TableCell(Paragraph(f"{list_art[cpt_art].price} {currency}"), 
                                                            background_color=c))   
        table_array[-1].add(TableCell(Paragraph(
                        f"{round(list_art[cpt_art].quantity * list_art[cpt_art].price,2)} {currency}")
                                                            , background_color=c))  
        table_array[-1].add(TableCell(Paragraph(f"{list_art[cpt_art].description}",
                        font_size=Decimal(8)),  background_color=c))
        table_array[-1].add(TableCell(Paragraph(" "), background_color=c)) 
        table_array[-1].add(TableCell(Paragraph(" "), background_color=c)) 
        table_array[-1].add(TableCell(Paragraph(" "), background_color=c))
        cpt_art += 1
        left_art -= 1

    table_array[-1].add(TableCell(Paragraph("Sous-total", font="Helvetica-Bold", 
                        horizontal_alignment=Alignment.RIGHT,), col_span=3,))  
    table_array[-1].add(TableCell(Paragraph(f"{receipt.subtotal()} {currency}", 
                                        horizontal_alignment=Alignment.RIGHT)))
    if(isinstance(receipt, Invoice)):
        table_array[-1] = pdf_invoice_total(table_array[-1], receipt, currency) 

    elif(isinstance(receipt, Estimate)):
        table_array[-1] = pdf_estimate_total(table_array[-1], receipt, currency) 

    table_array[-1].set_padding_on_all_cells(Decimal(2), 
                                        Decimal(15), Decimal(2), Decimal(2))
    return table_array

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
                   inline: bool = False, prominent_article_table: bool = False,
                   show_advances_table: bool = False):
    """
    Fonction d'assemblage du pdf
    """
    # Créer un document pdf
    doc : Document = Document()
    # Créer une page pour le pdf
    page_array  = [Page()]
    
    # Ajout de Page au document
    doc.append_page(page_array[0])
    #Disposition de la page

    layout_array = [BrowserLayout(page_array[0])]
    #Calcul des marge
    #page_layout.vertical_margin = page.get_page_info().get_height() \
                                                               # * Decimal(0.02)
    
    arr_tb = pdf_articles_total(receipt, currency, color)
    i = 0
    cpt = 0
    for tab in arr_tb:
        if(i == 2):
            page_array.append(Page())
            doc.append_page(page_array[-1])
            layout_array.append(BrowserLayout(page_array[-1]))

        layout_array[-1].add(tab)
        i = (i+1)%3
    #On rajoute l'extension pdf si elle n'est pas déjà présente
    if(path[-4:] != ".pdf"):
        path += ".pdf"
    #On ajoute la page au pdf
    #pdf.append_page(page)
    #Écriture du pdf au chemin indiqué
    with open(path, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)




if __name__ == "__main__":
    artisan = User("Facturio", "15 rue des champs Cuers", "0734567221", 
                        "128974654", "Tom", "Pommier", "facturio@gmail.com",
                                                            "logo.jpg")
    client_physique = Client("Lombardo", "Quentin", 
        "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon", "0678905324")
                        
    client_moral = Company("LeRoy",  "LeRoy83@sfr.fr", "12 ZAC de La Crau",
                             "0345678910", "Ben", "Karim","287489404")
    ordinateur = Article("ordinateur", 1684.33, 3,"Asus spire")
    cable_ethernet = Article("cable ethernet", 9.99, 10,"15m")
    telephone = Article("telephone", 399.99, 1,"téléphone clapet")
    casque = Article("casque", 69.99, 6,"casque sans fils")
    bureau = Article("Bureau", 500,2,"Bureau à 6pieds")
    articles = [ordinateur, cable_ethernet, telephone, casque, bureau]
    
    for i in range(100):
        articles.append(Article("truc",35))
    paiements = [Advance(1230.0), Advance(654)]
    
    print(len(articles))
    fact = Invoice(artisan, client_moral, articles, advances_list =paiements,
                        taxes = 0.2, note="Invoice de matériel informatiques",
                   date = 0, amount=100)
    dev = Estimate(artisan, client_physique, articles, taxes=0,
                            note="Invoice de matériel informatiques")

    build_pdf(dev, 27, "exemple_devis.pdf")
    build_pdf(fact, 490, "exemple_facture", color="#de260d", 
                show_advances_table=True)

