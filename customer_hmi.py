#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class Customer(Gtk.ScrolledWindow):
    """
    Classe IHM de le fenetre client. Elle permet d'importer, exporter,
    creer.
    +--------+
    |--| [I] |
    |  | [C] |
    |__| [E] |
    +--------+
    """
    def __init__(self):
        super().__init__()
        self.init_grid()
        self.title("Client")
        self.space()
        self.search((3,4,4,1))
        self.summon_button()
        self.init_result(["Nom","Entreprise","Adresse",""])
        self.add_result(["test","test","test"])
        self.add_result(["test1","test2","test3"])

    def title(self, ttl):
        facturio_label = Gtk.Label(label=ttl)
        facturio_label.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        self.grid.attach(facturio_label, 0, 2, 6, 1 )

    def space(self):
        """
        Ajoute les espace pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        self.grid.attach(spaceh,1,1,10,10)

    def search(self, l_attach):
        """
        Prend un emplacement et invoque la barre de recherche
        a cette emplacement
        """
        searchbar = Gtk.SearchEntry()
        self.grid.attach(searchbar, *l_attach)


    def summon_button(self):
        """
        Invoque les boutons: Importer,Exporter,Creer
        """
        p_button=(("Importer", (7,4,2,1)), ("Plus", (7,5,2,1)),
                  ("Exporter", (7,6,2,1)))
        for para in p_button:
            but = Gtk.Button(label=para[0])
            self.grid.attach(but, *para[1])


    def init_result(self,para):
        """
        Initialise la barre de recherche et permet l'ajout grace a la methode
        add_result
        """
        l_client = []
        self.liste_client = Gtk.ListStore(str, str, str)
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

    def add_result(self,res):
        """
        Prend une liste de 3 str et les ajoute aux resultat de la barre
        """
        self.liste_client.append(res)

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

