#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gui.page_gui import Page_Gui
from gi.repository import Gtk

class History(Page_Gui):
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
        (
            self.init_grid()
                .title("Historique")
                .search((1,3,5,1))
                .space()
                .init_result(["Nom", "date", "Description"],
                          (1,4,5,10))
                .add(self.grid)
        )
