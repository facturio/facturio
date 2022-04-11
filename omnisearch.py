"""Module d'autocomplétion."""
from Info_Facture_Devis import clients, articles
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402

# clement = Client("Bazan", "Clement", "clement.bazan@email.com",
#                       "AAAAAAAAAAAAAAAAAA", "0123456789")
# quentin = Client("Lombardo", "Quentin", "quentin.lombardo@email.com",
#                       "AAAAAAAAAAAAAAAAAAAAAA", "0000000000")
# youssef = Client("Benjelloun", "Youssef",
#                       "youssef.benjelloun@email.com",
#                       "AAAAAAAAAAAAAAAAAAAAA", "0101010101")

# ordinateur = Article("ordinateur", 1684.33, "Un ordinateur portable.")
# cable_ethernet = Article("cable ethernet", 9.99, "Un câble ethernet.")
# telephone = Article("telephone", 399.99, "Un téléphone.")
# casque = Article("casque", 69.99, "Un casque audio.")

# clients = [clement, quentin, youssef]
# articles = [ordinateur, cable_ethernet, telephone, casque]



class ItemRow(Gtk.ListBoxRow):
    """Classe container d'une ligne de resultat de recherche."""

    def __init__(self, data):
        """Ajoute un label au resultat de recherche."""
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class FacturioOmnisearch(Gtk.SearchEntry):
    """Barre Omnisearch de Facturio, liste tout ce qui peut etre recherche."""

    box = Gtk.Box(orientation=1, spacing=6)
    results = Gtk.ListBox()

    def __init__(self, *args, **kwargs):
        """Initialise la recherche et le container des resultats."""
        super().__init__(*args, **kwargs)

        self.connect("search-changed", self.on_search_changed)
        self.connect("stop-search", self.on_stop_search)

        self.results.connect("row-activated", self.on_row_activated)

        self.box.pack_start(self, False, True, 0)
        self.box.pack_start(self.results, False, True, 0)

    def on_search_changed(self, entry):
        """Met a jour la liste des resultats."""
        for row in self.results.get_children():
            self.results.remove(row)

        if entry.get_text() != "":
            for item in complete(clients+articles, entry.get_text()):
                self.results.add(ItemRow(item))

        self.results.show_all()

    def on_stop_search(self, entry):
        """Nettoie la liste des resultats."""
        for row in self.results.get_children():
            self.results.remove(row)

    def on_row_activated(self, list_box, row):
        """Montre le resultat selectionne."""
        print(vars(row.data))


def complete(items, text):
    """Affiche les items correspondant a la saisie text."""
    req = re.compile(".*" + re.escape(text) + ".*", re.IGNORECASE)
    res = []

    for item in items:
        if any([req.match(str(el)) for el in vars(item).values()]):
            res.append(item)

    return res


if __name__ == '__main__':
    win = Gtk.Window()
    win.add(FacturioOmnisearch(placeholder_text="Recherche").box)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
