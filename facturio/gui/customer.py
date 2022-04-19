#!/usr/bin/env python3
import gi
from gui.page_gui import Page_Gui
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

class Customer(Page_Gui):
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
        self.search((1,3,4,1))
        self.__summon_button()
        self.init_result(["Nom","Entreprise","Adresse",""],
                         (1,4,4,10))
        self.add_result(["test","test","test"])
        self.add_result(["test1","test2","test3"])


    def __summon_button(self):
        """
        Invoque les boutons: Importer,Exporter,Creer
        """
        p_button=(("Importer", (5,3,1,1)), ("Plus", (5,4,1,1)),
                  ("Exporter", (5,5,1,1)))
        for para in p_button:
            but = Gtk.Button(label=para[0])
            self.grid.attach(but, *para[1])

    def add_result(self,res):
        """
        Prend une liste de 3 str et les ajoute aux resultat de la barre
        """
        self.liste_customer.append(res)
