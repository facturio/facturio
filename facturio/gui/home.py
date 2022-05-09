import i18n
from facturio.gui.omnisearch import FacturioOmnisearch
from facturio import examples
from facturio.gui.headerbar import HeaderBarSwitcher
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class ButtonIcon(Gtk.RadioButton):
    """
    Spécialise la classe Gtk.RadioButton en ajoutant un icon et un label
    """
    def __init__(self, label, icon_name):
        super().__init__()
        self.icon_name = icon_name
        self.label = label
        self.icon = Gio.ThemedIcon(name=self.icon_name)
        self.image = Gtk.Image.new_from_gicon(self.icon, Gtk.IconSize.BUTTON)
        self.set_image(self.image)
        self.set_label(self.label)
        self.set_always_show_image(True)
        self.set_mode(False)


class HomePage(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.header_bar = HeaderBarSwitcher.get_instance()
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        # ajout d'un space sur le logo Facturio
        space = Gtk.Label(label="")
        self.grid.attach(space,1,1,10,1)
        # logo
        self.facturio_label = Gtk.Label(label="Facturio")
        self.grid.attach(self.facturio_label, 3, 2, 6, 1 )
        # ajout d'un space sous le logo Facturio
        space = Gtk.Label(label="")
        self.grid.attach(space, 1, 4, 10, 1)
        # ajout de la search bar
        self.searchbar = FacturioOmnisearch(examples.clients,
                                            placeholder_text=i18n.t('home.search'))
        self.grid.attach(self.searchbar, 3, 3, 6, 1)
        # creation des buttons
        self.__init_buttons()
        #ajout d'un space au dessous des buttons
        space = Gtk.Label(label="")
        self.grid.attach(space, 1, 7, 10, 2)
        self.pack_start(self.grid, True, True, 0)


    def __init_buttons(self):
        """
        Création des buttons et atach dans la self.grid
        """
        labels = (i18n.t('home.invoice'), i18n.t('home.history'), i18n.t('home.estimate'),
                  i18n.t('home.map'), i18n.t('home.client'), i18n.t('home.user'))
        positions = ((3, 5, 2, 1), (5, 5, 2, 1), (7, 5, 2, 1), (3, 6, 2, 1),
                     (5, 6, 2, 1), (7, 6, 2, 1))
        page_names = ("invoice_page", "history_page", "estimate_page",
                    "map_page", "customer_page", "user_page")
        self.buttons = []
        for label, pos, page in zip(labels, positions, page_names):
            btn = Gtk.Button(label=label)
            self.grid.attach(btn, *pos)
            btn.connect("clicked", self.header_bar.active_button, page)
            self.buttons.append(btn)
