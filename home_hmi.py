import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class ButtonIcon(Gtk.RadioButton):
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


class HeaderBarSwitcher(Gtk.HeaderBar):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.set_has_subtitle(False)
        self.set_show_close_button(True)
        # Creation et activation du button home
        self.invisible_btn = Gtk.RadioButton()
        self.buttons = set(["home_page", "invoice_page", "quotation_page",
                            "customer_page"])
        self.button_dict = {}
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.box.get_style_context(), "linked")
        btn = ButtonIcon("","go-home-symbolic")
        self.button_dict["home_page"] = btn
        btn.connect("clicked", self.switch_page, "home_page")
        btn.join_group(self.invisible_btn)

        self.active_now = btn
        self.pack_start(btn)


        page_names = ("invoice_page", "quotation_page", "customer_page")
        labels = ("Factures", "Devis", "Clients")
        icons = ("emblem-documents-symbolic", "x-office-document-symbolic",
                 "system-users-symbolic")
        for name, label, icon in zip(page_names, labels, icons):
            self.button_dict[name] = ButtonIcon(label, icon)
            self.button_dict[name].connect("clicked", self.switch_page, name)
            self.button_dict[name].join_group(self.invisible_btn)
            self.box.pack_start(self.button_dict[name], True, True, 10)
        self.set_custom_title(self.box)


    def set_visible(self, flag: bool):
        if flag:
            self.button_dict["home_page"].set_visible(True)
            self.box.set_visible(True)
        else:
            self.button_dict["home_page"].set_visible(False)
            self.box.set_visible(False)

    def switch_page(self, btn, page):
        if self.stack.get_visible_child_name() != page:
            if page in self.buttons:
                button = self.button_dict[page]
                self.active_now = button
            else:
                self.invisible_btn.set_active(True)
            if page == "home_page" :
                self.set_visible(False)
            else:
                self.set_visible(True)
            self.stack.set_visible_child_name(page)
    def active_button(self, btn, page):
        if page in self.buttons:
            self.button_dict[page].set_active(True)
        else:
            self.invisible_btn.set_active(True)
            self.switch_page(btn, page)



class HomePage(Gtk.Box):
    def __init__(self, header_bar):
        super().__init__()
        self.header_bar = header_bar
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        # spaces
        space = Gtk.Label(label="")
        self.grid.attach(space,1,1,10,1)
        # logo

        space = Gtk.Label(label="")
        self.grid.attach(space,1,4,10,1)
        self.title("Facturio")
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
            btn.connect("clicked", self.header_bar.active_button, page)

            self.buttons.append(btn)

        space = Gtk.Label(label="")
        self.grid.attach(space,1,7,10,1)
        space = Gtk.Label(label="")
        self.grid.attach(space,1,8,10,1)
        # self.add(self.grid)
        self.pack_start(self.grid, True, True, 0)

    def title(self, ttl):
        facturio_label = Gtk.Label(label=ttl)
        facturio_label.set_markup("<span font_weight=\"bold\" size=\"xx-large\">"+ttl+"</span>")
        self.grid.attach(facturio_label, 3, 2, 6, 1 )
