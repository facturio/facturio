#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class Client(Gtk.Window):
    """
    Classe IHM de le fenetre client,
    Elle permet d'importer, exporter,
    creer.

    +--------+
    |--| [I] |
    |  | [C] |
    |__| [E] |
    +--------+
    """
    def __init__(self):
        super().__init__(title="Facturio: Client")
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.resize(1920, 1080)
        self.set_hexpand(False)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
        facturio_label = Gtk.Label(label="Client")
        self.grid.attach(facturio_label, 3, 2, 6, 1 )
        self.space()
        self.search((3,4,4,1))
        self.summon_button()
        self.init_result()

    def space(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spaceHeader = Gtk.Label(label="")
        self.grid.attach(spaceHeader,1,1,10,10)
        spaceFooter = Gtk.Label(label="")
        self.grid.attach(spaceFooter,7,5,1,1)
        space = Gtk.Label(label="")
        self.grid.attach(space,1,5,10,10)
        space2 = Gtk.Label(label="")
        self.grid.attach(space2,1,6,10,10)

    def search(self,l_attach):
        """
        Invoque les bouton:
        Importer,Exporter,Creer
        """
        searchbar = Gtk.SearchEntry()
        self.grid.attach(searchbar, *l_attach)


    def summon_button(self):
        """
        Invoque les bouton:
        Importer,Exporter,Creer
        """
        p_button=(("Importer",(7,4,2,1)),
                  ("Plus",(7,5,2,1)),
                  ("Exporter",(7,6,2,1)))
        for p in p_button:
            but = Gtk.Button(label=p[0])
            self.grid.attach(but, *p[1])


    def init_result(self):
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
        for i, column_title in enumerate(
            ["Nom", "entreprise", "Adresse"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.grid.attach(self.scrollable_treelist, 3, 5, 4, 10)
        self.scrollable_treelist.add(self.treeview)

    def add_result(self,res):
        """
        Prend une liste de 3 str
        et les ajoute aux resultat de la barre
        """
        self.liste_client.append(res)

#########################
#######TEST##############
#########################
win =Client()
win.show_all()
Gtk.main()
