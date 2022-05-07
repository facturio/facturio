#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import re
from facturio.db.db import Data_base
from facturio.gui.omnisearch import FacturioOmnisearch
from facturio.gui.autocompletion import FacturioEntryCompletion
from facturio import examples

class PageGui(Gtk.ScrolledWindow):
    """
    Classe servant de socle commun de methode
    gtk pour les page gui de Facturio
    """

    def __init__(self) -> None:
        self.liste_customer= Gtk.ListStore(str, str, str)
        self.db= Data_base("facturio")
        super().__init__()


    def is_valid_for_db(self,l_client):
        """
        retourn si les element de la liste
        l_client est correct ou non pour
        la base de donnee
        """
        regex_mail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not l_client[0].isalpha():
            print(l_client[0],"est incorrect")
            return False
        if not l_client[1].isalpha():
            print(l_client[1],"est incorrect")
            return False
        if not (re.fullmatch(regex_mail, l_client[2])):
            print(l_client[2],"est incorrect")
            return False
        if not l_client[4][1:].strip(" ").isnumeric():
            print(l_client[4],"est incorrect")
            return False
        return True

    def is_usr_valid_for_db(self,l_client):
        """
        retourn si les element de la liste
        l_client est correct ou non pour
        la base de donnee
        """
        print(l_client)
        regex_mail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not l_client[1].isalpha():
            print(l_client[1],"est incorrect")
            return False
        if not (re.fullmatch(regex_mail, l_client[2])):
            print(l_client[2],"est incorrect")
            return False
        if not l_client[4][1:].strip(" ").isnumeric():
            print(l_client[4],"est incorrect")
            return False
        if not l_client[5].strip(" ").isnumeric():
            print(l_client[5],"est incorrect")
            return False
        return True


    def space(self):
        """
        Ajoute les espace
        pour l'ergonomie
        """
        spaceh = Gtk.Label(label="")
        self.grid.attach(spaceh,1,1,6,10)
        return self


    def title(self, ttl):
        facturio_label = Gtk.Label(label=ttl)
        facturio_label.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        self.grid.attach(facturio_label, 1, 2, 1, 1 )
        return self


    def search(self,l_attach):
        """
        Prend un emplacement et
        Invoque la barre de recherche
        a cette emplacement
        """
        searchbar = FacturioOmnisearch(examples.clients, placeholder_text="Recherche")
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
        for customer in l_customer:
            self.liste_customer.append(customer)
        self.treeview = Gtk.TreeView(model=self.liste_customer)
        for i, column_title in enumerate(para):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.cent.attach(self.scrollable_treelist, *pos)
        self.scrollable_treelist.add(self.treeview)
        return self
