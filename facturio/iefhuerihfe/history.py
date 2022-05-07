#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class History(Gtk.ScrolledWindow):
    """
    Classe IHM de le fenetre Historique. Elle permet de chercher
    un devis ou une facture

    +--------+
    ||------||
    ||      ||
    ||      ||
    ||------||
    +--------+
    """
    def __init__(self):
        super().__init__()
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        facturio_label = Gtk.Label(label="Historique")
        self.grid.attach(facturio_label, 3, 2, 6, 1 )
        self.space()
        self.search((3,4,6,1))
        self.init_result(["Nom", "date", "Description"])
        self.add(self.grid)


    def init_result(self, para):
        """
        Initialise la barre de recherche et permet l'ajout grace
        a la methode add_result
        """
        l_client= []
        self.liste_client= Gtk.ListStore(str, str, str)
        for client in l_client:
            self.liste_client.append(client)
        self.treeview = Gtk.TreeView(model=self.liste_client)
        for i, column_title in enumerate(para):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.grid.attach(self.scrollable_treelist, 3, 5, 4, 10)
        self.scrollable_treelist.add(self.treeview)

    def space(self):
        """
        Ajoute les espace pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        self.grid.attach(spaceh,1,1,10,10)
        spacef = Gtk.Label(label="")
        self.grid.attach(spacef,7,5,1,1)


    def search(self, l_attach):
        """
        Prend un emplacement et invoque la barre de recherche
        a cette emplacement
        """
        searchbar = Gtk.SearchEntry()
        self.grid.attach(searchbar, *l_attach)


