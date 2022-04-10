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
        # self.main_grid = Gtk.Grid(column_homogeneous=False, row_homogeneous=False,
        #                      column_spacing=20, row_spacing=20)
        # self.vspacer = Gtk.Label("")
        # self.main_grid.attach(self.vspacer, 1, 1, 1, 3)
        # self.vspacer.set_hexpand(True)
        # self.vspacel = Gtk.Label("")
        # self.main_grid.attach(self.vspacel, 3, 1, 1, 3)
        # self.vspacel.set_hexpand(True)


        # self.main_grid.attach(self.box, 2, 1, 1, 1)
        # self.article_header()
        # self.main_grid.attach(self.article_header_box, 2,2,1,1)
        # self.main_grid.attach(self.box1, 2, 2, 1, 1)
        # self.new_article_row()
        # # self.article_header_box.pack_start(self.row_box, True, True, 0)

        # self.add(self.main_grid)
        #
        self.main_box = Gtk.VBox()
        self.add(self.main_box)
        self.box.set_halign(Gtk.Align.CENTER)
        self.main_box.pack_start(self.box, True, True, 0)
        self.article_header()
        self.initial_article_row()
        self.article_grid.set_halign(Gtk.Align.CENTER)
        self.main_box.pack_start(self.article_grid, True, True, 0)
        self.plus_btn_box()
        # self.article_header_box.pack_start(self.row_box, True, True, 0)
        # self.plus_btn_box()

    def article_header(self):
        self.article_grid = Gtk.Grid(column_homogeneous=False,
                                     row_homogeneous=True,
                             column_spacing=20, row_spacing=20)

        self.btns = {}
        self.label = Gtk.Label("")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 1, 1, 1, 1)

        self.label = Gtk.Label("Description")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 2, 1, 2, 1)

        self.label = Gtk.Label("Prix")
        self.article_grid.attach(self.label, 4, 1, 1, 1)

        self.label = Gtk.Label("Quantite")
        self.article_grid.attach(self.label, 5, 1, 1, 1)

        self.label = Gtk.Label("Somme")
        self.article_grid.attach(self.label, 6, 1, 1, 1)

        self.label = Gtk.Label("Taxes")
        self.article_grid.attach(self.label, 7, 1, 1, 1)

    def plus_btn_box(self):
        self.plus_btn_row = 5
        button = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.article_grid.attach(button, 1, 5, 1, 1)

        button.connect("clicked", self.new_article_row)


    def new_article_row(self, btn=None):
        i = self.plus_btn_row
        self.plus_btn_row += 3
        self.article_grid.insert_row(i)
        self.article_grid.insert_row(i)
        self.article_grid.insert_row(i)
        # self.article_grid.insert_row(i+1)
        # self.article_grid.insert_row(i+2)
        row_widgets = []
        button = Gtk.Button.new_from_icon_name("process-stop-symbolic",
                                                    Gtk.IconSize.BUTTON)
        row_widgets.append(button)
        self.article_grid.attach(button, 1, i, 1, 1)
        self.btns[button] = i
        button.connect("clicked", self.des_widgets)


        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 2, i, 2, 1)
        row_widgets.append(self.entry)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 4, i, 1, 1)
        row_widgets.append(self.entry)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 5, i, 1, 1)
        row_widgets.append(self.entry)

        self.label = Gtk.Label("7$")
        self.article_grid.attach(self.label, 6, i, 1, 1)
        row_widgets.append(self.label)

        self.checkbutton = Gtk.CheckButton()
        self.checkbutton.set_valign(Gtk.Align.CENTER)
        self.checkbutton.set_halign(Gtk.Align.CENTER)
        self.article_grid.attach(self.checkbutton, 7, i, 1, 1)
        row_widgets.append(self.checkbutton)

        self.entry = Gtk.Entry()
        # self.entry.set_hexpand(True)
        self.article_grid.attach(self.entry , 2, i+1, 2, 2)
        row_widgets.append(self.entry)

        # self.row_box.pack_start(self.article_grid, True, True, 0)
        for wid in row_widgets:
            wid.set_visible(True)

    def initial_article_row(self):
        self.label = Gtk.Label("")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 1, 2, 1, 1)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 2, 2, 2, 1)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 4, 2, 1, 1)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 5, 2, 1, 1)

        self.label = Gtk.Label("7$")
        self.article_grid.attach(self.label, 6, 2, 1, 1)

        self.checkbutton = Gtk.CheckButton()
        self.checkbutton.set_valign(Gtk.Align.CENTER)
        self.checkbutton.set_halign(Gtk.Align.CENTER)
        self.article_grid.attach(self.checkbutton, 7, 2, 1, 1)

        self.entry = Gtk.Entry()
        self.article_grid.attach(self.entry , 2, 3, 2, 2)




    def update_dict(self, i):
        for btn, row in self.btns.items():
            if row > i:
                self.btns[btn] = row-3


    def des_widgets(self, btn ):
        line = self.btns.pop(btn)
        self.article_grid.remove_row(line)
        self.article_grid.remove_row(line)
        self.article_grid.remove_row(line)
        self.update_dict(line)
        self.plus_btn_row -= 3
