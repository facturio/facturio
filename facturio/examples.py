from facturio.classes.client import Client
from facturio.classes.invoice_misc import Article
clement = Client("Bazan", "Clement", "clement.bazan@email.com",
                 "AAAAAAAAAAAAAAAAAA", "0123456789")
quentin = Client("Lombardo", "Quentin", "quentin.lombardo@email.com",
                 "AAAAAAAAAAAAAAAAAAAAAA", "0000000000")
youssef = Client("Benjelloun", "Youssef",
                 "youssef.benjelloun@email.com",
                 "AAAAAAAAAAAAAAAAAAAAA", "0101010101")
theo = Client("Theo", "Alphaoui", "tropdrole@email.com", "AEU", "010101")

ordinateur = Article("ordinateur", 1684.33, 1)
cable_ethernet = Article("cable ethernet", 9.99, 3)
telephone = Article("telephone", 399.99, 2)
casque = Article("casque", 69.99, 10)

clients = [clement, quentin, youssef, theo]
articles = [ordinateur, cable_ethernet, telephone, casque]
