"""Module d'autocomplétion."""
from Info_Facture_Devis import clients, articles
import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Autocompletion test.")
    parser.add_argument('text', type=str, help="text to autocomplete")
    args = parser.parse_args()

    args.text

    req = re.compile(".*" + re.escape(args.text) + ".*", re.IGNORECASE)
    cls = []
    art = []

    for client in clients:
        if any([req.match(el) for el in vars(client).values()]):
            cls.append(client)

    for article in articles:
        if any([req.match(str(el)) for el in vars(article).values()]):
            art.append(article)

    print(art)
    print(cls)
