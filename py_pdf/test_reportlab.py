# Importing Required Module
from reportlab.pdfgen import canvas
# Creating Canvas
c = canvas.Canvas("invoice.pdf",pagesize=(200,250),bottomup=0)
# Logo Section
# Setting th origin to (10,40)
c.translate(10,40)
# Inverting the scale for getting mirror Image of logo
c.scale(1,-1)
# Inserting Logo into the Canvas at required position
c.drawImage("logo.jpg",0,0,width=50,height=30)
# Title Section
# Again Inverting Scale For strings insertion
c.scale(1,-1)
# Again Setting the origin back to (0,0) of top-left
c.translate(-10,-40)
# Setting the font for Name title of company
c.setFont("Helvetica-Bold",10)
# Inserting the name of the company
c.drawCentredString(125,20,"XYZ PRIVATE LIMITED")
# For under lining the title
c.line(70,22,180,22)
# Changing the font size for Specifying Address
c.setFont("Helvetica-Bold",5)
c.drawCentredString(125,30,"Block No. 101, Triveni Apartments, Pitam Pura,")
c.drawCentredString(125,35,"New Delhi - 110034, India")
# Changing the font size for Specifying GST Number of firm
c.setFont("Helvetica-Bold",6)
c.drawCentredString(125,42,"GSTIN : 07AABCS1429B1Z")
# Line Seprating the page header from the body
c.line(5,45,195,45)
# Document Information
# Changing the font for Document title
c.setFont("Courier-Bold",8)
c.drawCentredString(100,55,"TAX-INVOICE")
# This Block Consist of Costumer Details
c.roundRect(15,63,170,40,10,stroke=1,fill=0)
c.setFont("Times-Bold",5)
c.drawRightString(70,70,"INVOICE No. :")
c.drawRightString(70,80,"DATE :")
c.drawRightString(70,90,"CUSTOMER NAME :")
c.drawRightString(70,100,"PHONE No. :")
# This Block Consist of Item Description
c.roundRect(15,108,170,130,10,stroke=1,fill=0)
c.line(15,120,185,120)
c.drawCentredString(25,118,"SR No.")
c.drawCentredString(75,118,"GOODS DESCRIPTION")
c.drawCentredString(125,118,"RATE")
c.drawCentredString(148,118,"QTY")
c.drawCentredString(173,118,"TOTAL")
# Drawing table for Item Description
c.line(15,210,185,210)
c.line(35,108,35,220)
c.line(115,108,115,220)
c.line(135,108,135,220)
c.line(160,108,160,220)
# Declaration and Signature
c.line(15,220,185,220)
c.line(100,220,100,238)
c.drawString(20,225,"We declare that above mentioned")
c.drawString(20,230,"information is true.")
c.drawString(20,235,"(This is system generated invoive)")
c.drawRightString(180,235,"Authorised Signatory")
# End the Page and Start with new
c.showPage()
# Saving the PDF
c.save()