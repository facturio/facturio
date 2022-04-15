#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Page_Gui(Gtk.ScrolledWindow):
    """
    Classe servant de socle commun de methode
    gtk pour les page gui de Facturio
    """

    def __init__(self) -> None:
        super().__init__()


    def space(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        self.grid.attach(spaceh,1,1,5,10)
        return self


    def title(self, ttl):
        facturio_label = Gtk.Label(label=ttl)
        facturio_label.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        self.grid.attach(facturio_label, 0, 2, 6, 1 )
        return self


    def search(self,l_attach):
        """
        Prend un emplacement et
        Invoque la barre de recherche
        a cette emplacement
        """
        searchbar = Gtk.SearchEntry()
        self.grid.attach(searchbar, *l_attach)
        return self


    def init_grid(self):
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
        return self


    def init_result(self, para, pos):
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
        self.grid.attach(self.scrollable_treelist, *pos)
        self.scrollable_treelist.add(self.treeview)
        return self
