#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class Historique(Gtk.Window):
    """
    Classe IHM de le fenetre Historique,
    Elle permet de chercher un devis ou
    une facture

    +--------+
    ||------||
    ||      ||
    ||      ||
    ||------||
    +--------+
    """
    def __init__(self):
        super().__init__(title="Facturio: Historique")
        self.resize(1920, 1080)
        self.set_hexpand(False)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.init_grid()
        facturio_label = Gtk.Label(label="Historique")
        self.grid.attach(facturio_label, 3, 2, 6, 1 )
        self.space()
        self.search((3,4,6,1))
        self.init_result(["Nom", "date", "Description"])


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


    def init_result(self,para):
        """
        Initialise la barre de recherche
        et permet l'ajout grace a la methode
        add_result
        """
        l_client= [
        ]
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
        Ajoute les espace
        pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        self.grid.attach(spaceh,1,1,10,10)
        spacef = Gtk.Label(label="")
        self.grid.attach(spacef,7,5,1,1)


    def search(self,l_attach):
        """
        Invoque les bouton:
        Importer,Exporter,Creer
        """
        searchbar = Gtk.SearchEntry()
        self.grid.attach(searchbar, *l_attach)



#########################
#######TEST##############
#########################
win =Historique()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
