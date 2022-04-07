
from Info_Facture_Devis import *

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

#Import librairie standard
from datetime import datetime
from decimal import Decimal
import random
from pathlib import Path






def pdf_champs_prestataire(info, date, identifiant):    
    """
    Retourne une table liée aux informations du prestataire
    """
    table_001 = Table(number_of_rows=6, number_of_columns=2)  
    table_001.add(  
        Paragraph(  
            "De",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    )  
    table_001.add(  
        Paragraph(  
            "A",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    )  

    table_001 = Table(number_of_rows=5, number_of_columns=3)
	
    table_001.add(Paragraph(info.nom_entr))    
    table_001.add(Paragraph("Date", font="Helvetica-Bold", 
                                        horizontal_alignment=Alignment.RIGHT))    
    # now = datetime.now()    
    table_001.add(Paragraph("%d/%d/%d" % (date.day, date.month, date.year)))
	
    table_001.add(Paragraph(date))    
    table_001.add(Paragraph("Invoice #", font="Helvetica-Bold", 
                                        horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d" % random.randint(1000, 10000)))   
	
    table_001.add(Paragraph("[Phone]"))    
    # table_001.add(Paragraph("Due Date", font="Helvetica-Bold", 
    #                                     horizontal_alignment=Alignment.RIGHT))
    # table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year))) 
	
    table_001.add(Paragraph("[Email Address]"))    
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.add(Paragraph("[Company Website]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
    table_001.no_borders()
    return table_001

def _build_invoice_information():    
    table_001 = Table(number_of_rows=6, number_of_columns=3)

    table_001.add(  
        Paragraph(  
            "De",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    )  
    table_001.add(  
        Paragraph(  
            "A",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    ) 
	
    table_001.add(Paragraph("[Street Address]"))    
    table_001.add(Paragraph("Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))    
    now = datetime.now()    
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
	
    table_001.add(Paragraph("[City, State, ZIP Code]"))    
    table_001.add(Paragraph("Invoice #", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d" % random.randint(1000, 10000)))   
	
    table_001.add(Paragraph("[Phone]"))    
    table_001.add(Paragraph("Due Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year))) 
	
    table_001.add(Paragraph("[Email Address]"))    
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.add(Paragraph("[Company Website]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
    table_001.no_borders()
    return table_001

def _build_billing_and_shipping_information():  
    table_001 = Table(number_of_rows=6, number_of_columns=2)  
    table_001.add(  
        Paragraph(  
            "De",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    )  
    table_001.add(  
        Paragraph(  
            "A",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    )  
    table_001.add(Paragraph("[Recipient Name]"))        # BILLING  
    table_001.add(Paragraph("[Recipient Name]"))        # SHIPPING  
    table_001.add(Paragraph("[Company Name]"))          # BILLING  
    table_001.add(Paragraph("[Company Name]"))          # SHIPPING  
    table_001.add(Paragraph("[Street Address]"))        # BILLING  
    table_001.add(Paragraph("[Street Address]"))        # SHIPPING  
    table_001.add(Paragraph("[City, State, ZIP Code]")) # BILLING  
    table_001.add(Paragraph("[City, State, ZIP Code]")) # SHIPPING  
    table_001.add(Paragraph("[Phone]"))                 # BILLING  
    table_001.add(Paragraph("[Phone]"))                 # SHIPPING  
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001

def _build_itemized_description_table():  
    table_001 = Table(number_of_rows=15, number_of_columns=4)  
    for h in ["DESCRIPTION", "QTY", "UNIT PRICE", "AMOUNT"]:  
        table_001.add(  
            TableCell(  
                Paragraph(h, font_color=X11Color("White")),  
                background_color=HexColor("016934"),  
            )  
        )  
  
    odd_color = HexColor("BBBBBB")  
    even_color = HexColor("FFFFFF")  
    for row_number, item in enumerate([("Product 1", 2, 50), ("Product 2", 4, 60), ("Labor", 14, 60)]):  
        c = even_color if row_number % 2 == 0 else odd_color  
        table_001.add(TableCell(Paragraph(item[0]), background_color=c))  
        table_001.add(TableCell(Paragraph(str(item[1])), background_color=c))  
        table_001.add(TableCell(Paragraph("$ " + str(item[2])), background_color=c))  
        table_001.add(TableCell(Paragraph("$ " + str(item[1] * item[2])), background_color=c))  
	  
	# Optionally add some empty rows to have a fixed number of rows for styling purposes
    for row_number in range(3, 10):  
        c = even_color if row_number % 2 == 0 else odd_color  
        for _ in range(0, 4):  
            table_001.add(TableCell(Paragraph(" "), background_color=c))  
  
    table_001.add(TableCell(Paragraph("Subtotal", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,), col_span=3,))  
    table_001.add(TableCell(Paragraph("$ 1,180.00", horizontal_alignment=Alignment.RIGHT)))  
    table_001.add(TableCell(Paragraph("Discounts", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),col_span=3,))  
    table_001.add(TableCell(Paragraph("$ 177.00", horizontal_alignment=Alignment.RIGHT)))  
    table_001.add(TableCell(Paragraph("Taxes", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3,))  
    table_001.add(TableCell(Paragraph("$ 100.30", horizontal_alignment=Alignment.RIGHT)))  
    table_001.add(TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT  ), col_span=3,))  
    table_001.add(TableCell(Paragraph("$ 1163.30", horizontal_alignment=Alignment.RIGHT)))  
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001


dte = datetime.now()   

# create an empty Document
pdf = Document()

# add an empty Page
page = Page()

page_layout = SingleColumnLayout(page)

page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
page_layout.add(    
        Image(        
        image=Path("logo.jpg"),        
        width=Decimal(75),        
        height=Decimal(75),    
        ))
# Invoice information table  
page_layout.add(_build_invoice_information())  
  
# Empty paragraph for spacing  
page_layout.add(Paragraph(" "))
page_layout.add(_build_billing_and_shipping_information())
page_layout.add(Paragraph(" "))
page_layout.add(_build_itemized_description_table())


pdf.append_page(page)


    
# store the PDF
with open(Path("output.pdf"), "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, pdf)
    