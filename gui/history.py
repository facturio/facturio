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
        self.__init_grid()
        self.__title("Historique")
        self.__search((2,4,3,1))
        self.__space()
        self.__init_result(["Nom", "date", "Description"])
        self.add(self.grid)


    def __title(self, ttl):
        facturio_label = Gtk.Label(label=ttl)
        facturio_label.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        self.grid.attach(facturio_label, 2, 2, 1, 1 )


    def __init_result(self, para):
        """
        Initialise la barre de recherche et permet l'ajout grace
        a la methode add_result
        """
        l_customer= []
        self.liste_customer= Gtk.ListStore(str, str, str)
        for customer in l_customer:
            self.liste_customer.append(customer)
        self.treeview = Gtk.TreeView(model=self.liste_customer)
        for i, column_title in enumerate(para):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.grid.attach(self.scrollable_treelist, 2, 5, 3, 10)
        self.scrollable_treelist.add(self.treeview)


    def __space(self):
        """
        Ajoute les espace pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        self.grid.attach(spaceh,1,1,5,1)


    def __search(self, l_attach):
        """
        Prend un emplacement et invoque la barre de recherche
        a cette emplacement
        """
        searchbar = Gtk.SearchEntry()
        self.grid.attach(searchbar, *l_attach)


    def __init_grid(self):
        """
        Propriete de la Grid Gtk
        voir doc
        """
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)

