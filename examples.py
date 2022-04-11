from Invoice_classes.client import Client, Article
clement = Client("Bazan", "Clement", "clement.bazan@email.com",
                 "AAAAAAAAAAAAAAAAAA", "0123456789")
quentin = Client("Lombardo", "Quentin", "quentin.lombardo@email.com",
                 "AAAAAAAAAAAAAAAAAAAAAA", "0000000000")
youssef = Client("Benjelloun", "Youssef",
                 "youssef.benjelloun@email.com",
                 "AAAAAAAAAAAAAAAAAAAAA", "0101010101")

ordinateur = Article("ordinateur", 1684.33, "Un ordinateur portable.")
cable_ethernet = Article("cable ethernet", 9.99, "Un câble ethernet.")
telephone = Article("telephone", 399.99, "Un téléphone.")
casque = Article("casque", 69.99, "Un casque audio.")

clients = [clement, quentin, youssef]
articles = [ordinateur, cable_ethernet, telephone, casque]
