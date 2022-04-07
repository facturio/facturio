#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class Client(Gtk.Window):
    def __init__(self):
        super().__init__(title="Facturio: Client")
        self.resize(1920, 1080)
        self.set_hexpand(False)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        #grid
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
        # spaces
        self.spaceHeader = Gtk.Label(label="")
        self.grid.attach(self.spaceHeader,1,1,10,10)
        self.spaceFooter = Gtk.Label(label="")
        self.grid.attach(self.spaceFooter,7,5,1,1)
        # logo
        self.facturio_label = Gtk.Label(label="Historique")
        #                                     L  T  W  H
        self.grid.attach(self.facturio_label, 3, 2, 6, 1 )
        self.space = Gtk.Label(label="")
        self.grid.attach(self.space,1,5,10,10)
        self.space2 = Gtk.Label(label="")
        self.grid.attach(self.space2,1,6,10,10)
        #search bar
        self.searchbar = Gtk.SearchEntry()
        self.grid.attach(self.searchbar, 3, 4, 6, 1)
        #Button
        self.init_result()

    def init_result(self):
        """
        init the list box to add result
        from search
        """
        l_client= [
        ]
        self.liste_client= Gtk.ListStore(str, str, str)
        for client in l_client:
            self.liste_client.append(client)
        self.treeview = Gtk.TreeView(model=self.liste_client)
        for i, column_title in enumerate(
            ["Nom", "Date", "descrition"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.grid.attach(self.scrollable_treelist, 3, 5, 6, 10)
        self.scrollable_treelist.add(self.treeview)

    def add_result(self,res):
        """
        take a list of 3 str and add
        it to the listBox
        """
        self.liste_client.append(res)

#########################
#######TEST##############
#########################
win =Client()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
