import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class ButtonIcon(Gtk.ToggleButton):
    def __init__(self, label, icon_name):
        super().__init__()
        self.icon_name = icon_name
        self.label = label
        self.icon = Gio.ThemedIcon(name=self.icon_name)
        self.image = Gtk.Image.new_from_gicon(self.icon, Gtk.IconSize.BUTTON)
        self.set_image(self.image)
        self.set_label(self.label)
        self.set_always_show_image(True)


class HeaderBar(Gtk.HeaderBar):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.set_has_subtitle(False)
        self.set_show_close_button(True)
        # Creation et activation du button home
        btn = ButtonIcon("","go-home-symbolic")
        btn.set_active(True)
        self.button_dict = {}
        self.button_dict["home_page"] = btn
        self.active_now = btn
        btn.connect("toggled", self.switch_toggle, "home_page")
        self.pack_start(btn)

        page_names = ("user_page", "quotation_page", "invoice_page",
                      "customer_page")
        labels = ("Utilisateur", "Devis", "Factures", "Clients")
        icons = ("avatar-default-symbolic", "x-office-document-symbolic",
                 "emblem-documents-symbolic", "system-users-symbolic")
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.box.get_style_context(), "linked")
        for name, label, icon in zip(page_names, labels, icons):
            btn = ButtonIcon(label, icon)
            btn.connect('toggled', self.switch_toggle, name)
            self.box.pack_start(btn, True, True, 10)
            self.button_dict[name] = btn
        self.set_custom_title(self.box)

    def set_visible(self, flag: bool):
        if flag:
            self.button_dict["home_page"].set_visible(True)
            self.box.set_visible(True)
        else:
            self.button_dict["home_page"].set_visible(False)
            self.box.set_visible(False)

    def switch_toggle(self, button, page):
        if button == None:
            button = self.button_dict[page]
        if button != self.active_now :
            self.active_now.set_active(False)
            self.active_now = button
            if page == "home_page":
                self.set_visible(False)
            else :
                self.set_visible(True)
            self.window.switch_page(page=page)


class MainPage(Gtk.ScrolledWindow):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        # spaces
        space = Gtk.Label(label="")
        self.grid.attach(space,1,1,10,1)
        # logo
        self.facturio_label = Gtk.Label(label="Facturio")
        self.grid.attach(self.facturio_label, 3, 2, 6, 1 )

        space = Gtk.Label(label="")
        self.grid.attach(space,1,4,10,1)

        #search bar
        self.searchbar = Gtk.SearchEntry()
        self.grid.attach(self.searchbar, 3, 3, 6, 1)

        labels = ("Facture", "Historique", "Devis", "Carte", "Client",
                  "Utilisateur")
        positions = ((3, 5, 2, 1), (5, 5, 2, 1), (7, 5, 2, 1), (3, 6, 2, 1),
                     (5, 6, 2, 1), (7, 6, 2, 1))
        page_names = ("invoice_page", "history_page", "quotation_page",
                    "map_page", "customer_page", "user_page")
        self.buttons = []
        for label, pos, page in zip(labels, positions, page_names):
            btn = Gtk.Button(label=label)
            self.grid.attach(btn, *pos)
            btn.connect("clicked", window.switch_page, page)
            self.buttons.append(btn)

        space = Gtk.Label(label="")
        self.grid.attach(space,1,7,10,1)
        space = Gtk.Label(label="")
        self.grid.attach(space,1,8,10,1)
        self.add(self.grid)
