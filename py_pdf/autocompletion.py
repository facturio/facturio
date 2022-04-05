"""Module d'autocomplétion."""
from Info_Facture_Devis import Particulier, Article
import argparse
import re

clement = Particulier("Bazan", "Clement", "clement.bazan@email.com",
                      "AAAAAAAAAAAAAAAAAA", "0123456789")
quentin = Particulier("Lombardo", "Quentin", "quentin.lombardo@email.com",
                      "AAAAAAAAAAAAAAAAAAAAAA", "0000000000")
youssef = Particulier("Benjelloun", "Youssef",
                      "youssef.benjelloun@email.com",
                      "AAAAAAAAAAAAAAAAAAAAA", "0101010101")

ordinateur = Article("ordinateur", 1684.33, "Un ordinateur portable.")
cable_ethernet = Article("cable ethernet", 9.99, "Un câble ethernet.")
telephone = Article("telephone", 399.99, "Un téléphone.")
casque = Article("casque", 69.99, "Un casque audio.")

clients = [clement, quentin, youssef]
articles = [ordinateur, cable_ethernet, telephone, casque]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Autocompletion test.")
    parser.add_argument('text', type=str, help="text to autocomplete")
    args = parser.parse_args()

    args.text

    req = re.compile(".*" + args.text + ".*", re.IGNORECASE)
    cls = []
    art = []

    for client in clients:
        if any([req.match(el) for el in vars(client).values()]):
            cls.append(client)

    for article in articles:
        if any([req.match(str(el)) for el in vars(article).values()]):
            art.append(article)

    print([str(c) for c in cls])
    print([str(c) for c in art])
