#!/usr/bin/env python3
from gi.repository import Gtk
class InvoicePage(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.box = Gtk.VBox()
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)

        self.label = Gtk.Label("<big>Facture</big>")
        self.label.set_use_markup(True)
        self.grid.attach(self.label, 1, 1, 4, 1)
        self.logo_button = Gtk.Button(label="Logo")
        self.logo_button.set_hexpand(True)
        self.grid.attach(self.logo_button, 7, 1, 2, 2)

        self.label = Gtk.Label("<big>From</big>")
        self.label.set_use_markup(True)
        self.grid.attach(self.label, 1, 3, 1, 1)

        self.label = Gtk.Label("Name")
        self.grid.attach(self.label, 1, 4, 1, 1)
        self.label.set_hexpand(True)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.grid.attach(self.entry, 2, 4, 3, 1)

        self.label = Gtk.Label("Email")
        self.grid.attach(self.label, 1, 5, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 5, 3, 1)

        self.label = Gtk.Label("Adress")
        self.grid.attach(self.label, 1, 6, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 6, 3, 1)

        self.label = Gtk.Label("Phone")
        self.grid.attach(self.label, 1, 7, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 7, 3, 1)

        self.label = Gtk.Label("Business\nNumber")
        self.grid.attach(self.label, 1, 8, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 8, 3, 1)


        ##########################################
        self.label = Gtk.Label("<big>To</big>")
        self.label.set_use_markup(True)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 5, 3, 1, 1)

        self.label = Gtk.Label("Name")
        self.grid.attach(self.label, 5, 4, 1, 1)
        self.entry = Gtk.Entry()
        self.label.set_hexpand(True)
        self.grid.attach(self.entry, 6, 4, 3, 1)

        self.label = Gtk.Label("Email")
        self.grid.attach(self.label, 5, 5, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 6, 5, 3, 1)

        self.label = Gtk.Label("Adress")
        self.grid.attach(self.label, 5, 6, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 6, 6, 3, 1)

        self.label = Gtk.Label("Phone")
        self.grid.attach(self.label, 5, 7, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 6, 7, 3, 1)

        self.button = Gtk.Button(label="Importer Clients")
        self.grid.attach(self.button, 7, 8, 2, 1)
        self.box.pack_start(self.grid, False, False, 20)

        # self.article_grid()
        # self.box.pack_start(self.box1, False, False, 0)
        self.main_grid = Gtk.Grid(column_homogeneous=False, row_homogeneous=False,
                             column_spacing=20, row_spacing=20)
        self.vspacer = Gtk.Label("")
        self.main_grid.attach(self.vspacer, 1, 1, 1, 3)
        self.vspacer.set_hexpand(True)
        self.vspacel = Gtk.Label("")
        self.main_grid.attach(self.vspacel, 3, 1, 1, 3)
        self.vspacel.set_hexpand(True)


        self.main_grid.attach(self.box, 2, 1, 1, 1)
        self.article_header()
        self.main_grid.attach(self.article_header_box, 2,2,1,1)
        # self.main_grid.attach(self.box1, 2, 2, 1, 1)
        self.new_article_row()
        # self.article_header_box.pack_start(self.row_box, True, True, 0)
        self.plus_btn_box()
        self.main_grid.attach(self.btn_box, 2,4,1,1)

        self.add(self.main_grid)

    def article_header(self):
        self.article_header_box= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.article_grid = Gtk.Grid(column_homogeneous=False, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self.article_header_box.pack_start(self.article_grid, True, True, 0)

        self.label = Gtk.Label("")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 1, 1, 1, 1)

        self.label = Gtk.Label("Description")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 2, 1, 3, 1)

        self.label = Gtk.Label("Prix")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 5, 1, 1, 1)

        self.label = Gtk.Label("Quantite")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 6, 1, 1, 1)

        self.label = Gtk.Label("Somme")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 8, 1, 1, 1)

        self.label = Gtk.Label("Taxes")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 9, 1, 1, 1)

    def plus_btn_box(self):
        self.btn_box = Gtk.Box()
        grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        button = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                    Gtk.IconSize.BUTTON)
        button.set_hexpand(True)
        grid.attach(button, 1, 1, 1, 1)

        space = Gtk.Label("")
        grid.attach(space, 2, 1, 15, 1)
        button.connect("clicked", self.new_article_row)

        self.btn_box.pack_start(grid, True, True, 0)

    def new_article_row(self, btn=None):
        print("dfadfasfasfadsfasdf")
        row_widgets = []
        self.button = Gtk.Button.new_from_icon_name("process-stop-symbolic",
                                                    Gtk.IconSize.BUTTON)
        row_widgets.append(self.button)
        # self.button.connect("clicked", self.remove_box, self.row_box)
        self.article_grid.attach(self.button, 1, 2, 1, 1)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 2, 2, 3, 1)
        row_widgets.append(self.entry)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 5, 2, 1, 1)
        row_widgets.append(self.entry)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 6, 2, 1, 1)
        row_widgets.append(self.entry)

        self.label = Gtk.Label("7$")
        self.article_grid.attach(self.label, 8, 2, 1, 1)
        row_widgets.append(self.label)

        self.checkbutton = Gtk.CheckButton()
        self.article_grid.attach(self.checkbutton, 9, 2, 1, 1)
        row_widgets.append(self.checkbutton)

        self.entry = Gtk.Entry()
        # self.entry.set_hexpand(True)
        self.article_grid.attach(self.entry , 2, 3, 3, 2)
        row_widgets.append(self.entry)

        self.button.connect("clicked", self.des_widgets, row_widgets)
        # self.row_box.pack_start(self.article_grid, True, True, 0)
        for wid in row_widgets:
            wid.set_visible(True)

    def des_widgets(self, btn, widgets):
        for wid in widgets:
            wid.hide()
