#!/usr/bin/env python3
import gi
from facturio.gui.displayclient import DisplayClient
from facturio.gui.page_gui import PageGui
from facturio.gui.home import HeaderBarSwitcher
from facturio.gui.add_customer import Add_Customer
from facturio.gui.omnisearch import FacturioOmnisearch
from facturio.gui.autocompletion import FacturioEntryCompletion
from facturio.gui.page_gui import PageGui
from facturio.gui.home import HeaderBarSwitcher
from facturio.gui.add_customer import Add_Customer
from facturio.gui.headerbar import HeaderBarSwitcher
from facturio.db.db import Data_base
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class Customer(PageGui):
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
        self.cent = Gtk.Grid(column_homogeneous=True,
                                  row_homogeneous=True, column_spacing=20,
                                  row_spacing=20)
        self.header_bar = HeaderBarSwitcher.get_instance()
        self.__init_grid()
        self.__space_info()
        self.init_result(["Nom","Prenom","adress"],
                         (1, 4, 2, 3))
        self.search_bar_client()
        self.add_result(["prout","prout","prout",])
        self.__summon_button()


    def __space_info(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spacel = Gtk.Label("")
        self.cent.attach(spacel, 0, 1, 1, 1)
        spacer = Gtk.Label("")
        self.cent.attach(spacer, 10, 2, 1, 1)
        spaceb = Gtk.Label("")


    def __init_grid(self):
        """
        Propriete de la Grid Gtk
        voir doc
        """
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(False)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
        self.grid.attach(self.cent, 1, 3, 2, 1)
        return self


    def __summon_button(self):
        """
        Invoque les boutons: Importer,Exporter,Creer
        """
        p_button=(("Importer", (4,3,1,1)), ("Plus", (4,4,1,1)),
                  ("Exporter", (4,5,1,1)))
        but = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                    Gtk.IconSize.BUTTON)
        but.connect("clicked", self.header_bar.active_button, "add_customer")
        self.cent.attach(but, *p_button[1][1])
        but = Gtk.Button.new_from_icon_name("document-save-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.cent.attach(but, *p_button[0][1])
        but = Gtk.Button.new_from_icon_name("document-open-symbolic",
                                                    Gtk.IconSize.BUTTON)
        but.connect("clicked", self.file_explorer)
        self.cent.attach(but, *p_button[2][1])


    def file_explorer(self,button):
        """
        ouvrent un explorateur de fichier et ajoute la
        bd le contenue du fichier en *.clt et *csv
        """
        filechooserdialog = Gtk.FileChooserDialog(title=" Importer client",
             parent=None,
             action=Gtk.FileChooserAction.OPEN)
        filechooserdialog.add_buttons("_Open", Gtk.ResponseType.OK)
        filechooserdialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)
        filechooserdialog.set_default_response(Gtk.ResponseType.OK)
        filter_ = Gtk.FileFilter()
        filter_.set_name("Client")
        filter_.add_pattern("*.clt")
        filter_.add_pattern("*.csv")
        filechooserdialog.set_filter(filter_)
        response = filechooserdialog.run()
        if response == Gtk.ResponseType.OK:
            is_coorect=True
            l_clients=[]
            if filechooserdialog.get_filename()[-4:]==".csv":
                with open(filechooserdialog.get_filename(), 'r') as f:
                    lines=f.readlines()
                    for line in lines:
                        l_clients.append((line.split(",")))
            else:
                l_clients.append([])
                with open(filechooserdialog.get_filename(), 'r') as f:
                    lines=f.readlines()
                    for line in lines:
                        line=line.strip('\n')
                        if line=="#" and len(l_clients)!=1:
                            break
                        elif line == "-":
                            l_clients.append([])
                        elif line != "#":
                            l_clients[len(l_clients)-1].append(line)
            for clients in l_clients:
                print(l_clients)
                if self.is_valid_for_db(clients[1:]):
                    self.db.insertion_client_or_company(clients[1:],
                                                    clients[0])
                else:
                    print("section incorrect :",clients)
            filechooserdialog.destroy()


    def search_bar_client(self):
        """
        Affiche tout les clients de la base de donner
        """
        list_client= self.db.selection_table("client",)
        searchbar = FacturioOmnisearch(list_client)
        searchbar.completion.connect('match-selected', self.switch_to_display)
        self.cent.attach(searchbar, 1,3,2,1)

    def fill_tree(self, completion, model, iter):
        """
        Remplit la treeview
        """
        print(completion)

    def switch_to_display(self, completion, model, iter):
        """
        recupere les info de la completion et les affiche
        avec la page info_persone
        """
        num_client = str(list((completion.props.model.get_value(iter, 0)))[1])
        page=DisplayClient(False,num_client)
        page.is_ut=False
        page.num_client=int(num_client)
        if num_client.isnumeric():
            self.header_bar.switch_page(None,"client_page")


    def add_result(self,res):
        """
        Prend une liste de 3 str et les ajoute aux resultat de la barre
        """
        self.liste_customer.append(res)
