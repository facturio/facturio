#!/usr/bin/env python3
import i18n
from facturio.gui.page_gui import PageGui
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class History(PageGui):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        (
            self.init_grid()
                .title(i18n.t('gui.history'))
                .search((1,3,5,1))
                .space()
        )
