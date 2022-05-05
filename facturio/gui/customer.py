#!/usr/bin/env python3
import gi
from facturio.gui.page_gui import PageGui
from facturio.gui.home import HeaderBarSwitcher
from facturio.gui.add_customer import Add_Customer
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
    def __init__(self, header_bar: HeaderBarSwitcher):
        super().__init__()
        self.header_bar = header_bar
        self.init_grid()
        self.title("Clients")
        self.space()
        self.search((1,3,4,1))
        self.__summon_button()
        self.init_result(["Nom","Entreprise","Adresse",""],
                         (1,4,4,10))


    def __summon_button(self):
        """
        Invoque les boutons: Importer,Exporter,Creer
        """
        p_button=(("Importer", (5,3,1,1)), ("Plus", (5,4,1,1)),
                  ("Exporter", (5,5,1,1)))
        but = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                    Gtk.IconSize.BUTTON)
        but.connect("clicked", self.header_bar.active_button, "add_customer")
        self.grid.attach(but, *p_button[1][1])
        but = Gtk.Button.new_from_icon_name("document-save-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.grid.attach(but, *p_button[0][1])
        but = Gtk.Button.new_from_icon_name("document-open-symbolic",
                                                    Gtk.IconSize.BUTTON)
        but.connect("clicked", self.file_explorer)
        self.grid.attach(but, *p_button[2][1])


    def file_explorer(self,button):
        """
        ouvrent un explorateur de fichier et ajoute la
        bd le contenue du fichier en *.clt
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
        filechooserdialog.set_filter(filter_)
        response = filechooserdialog.run()
        if response == Gtk.ResponseType.OK:
            is_coorect=True
            l_clients=[[]]
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
                    if self.is_valid_for_db(clients[1:]):
                        self.db.insertion_client_or_company(clients[1:],
                                                        clients[0])
                    else:
                        print("section incorrect :",clients)
            print("File selected: %s" % filechooserdialog.get_filename())
            print(l_clients)
        filechooserdialog.destroy()


    def add_result(self,res):
        """
        Prend une liste de 3 str et les ajoute aux resultat de la barre
        """
        self.liste_customer.append(res)
