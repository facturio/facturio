from facturio.classes.client import Client
from facturio.classes.invoice_misc import Article
from facturio.classes.user import User
clement = Client("Clément", "Bazan", "clement.bazan@email.com",
                 "AAAAAAAAAAAAAAAAAA", "0123456789")
quentin = Client("Quentin", "Lombardo", "quentin.lombardo@email.com",
                 "AAAAAAAAAAAAAAAAAAAAAA", "0000000000")
youssef = Client("Youssef", "Benjelloun",
                 "youssef.benjelloun@email.com",
                 "AAAAAAAAAAAAAAAAAAAAA", "0101010101")
theo = Client("Theo", "Alphaoui", "tropdrole@email.com", "AEU", "010101")

# test = User("Company", "Address", "Phone number", "Business Number", "First Name",
#             "Last Name", "Email@email.com", logo=None)
test = User(company_name="Facturio INC", last_name="BENJELLOUN",
            first_name="Youssef", email="yb@gmail.com",
            address="427 Boulevard des armoaris 83100 Toulon",
            phone_number="07 67 31 58 20",
            business_number="12348921 2341")

ordinateur = Article("ordinateur", 1684.33, 1)
cable_ethernet = Article("cable ethernet", 9.99, 3)
telephone = Article("telephone", 399.99, 2)
casque = Article("casque", 69.99, 10)

clients = [clement, quentin, youssef, theo]
articles = [ordinateur, cable_ethernet, telephone, casque]
utilisateurs = [placeholder]
