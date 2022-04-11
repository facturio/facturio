#!/usr/bin/env python3
from gi.repository import Gtk
class InvoicePage(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.box = Gtk.VBox()
        self.grid = Gtk.Grid(column_homogeneous=True, row_homogeneous=True,
                             column_spacing=20, row_spacing=20)

        self.label = Gtk.Label("<big>Facture</big>")
        self.label.set_hexpand(True)
        self.label.set_use_markup(True)
        self.grid.attach(self.label, 1, 1, 4, 1)
        self.logo_button = Gtk.Button.new_from_icon_name("image-x-generic-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.logo_button.set_label('+ Logo')
        self.logo_button.set_always_show_image(True)
        self.logo_button.set_hexpand(True)
        self.grid.attach(self.logo_button, 7, 1, 2, 2)

        self.label = Gtk.Label("<big>De</big>")
        self.label.set_hexpand(True)
        self.label.set_use_markup(True)
        self.grid.attach(self.label, 1, 3, 1, 1)

        self.label = Gtk.Label("Nom\nEntreprise")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 1, 4, 1, 1)
        self.label.set_hexpand(True)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.grid.attach(self.entry, 2, 4, 3, 1)

        self.label = Gtk.Label("Nom")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 1, 5, 1, 1)
        self.label.set_hexpand(True)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.grid.attach(self.entry, 2, 5, 3, 1)

        self.label = Gtk.Label("Prenom")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 1, 6, 1, 1)
        self.label.set_hexpand(True)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.grid.attach(self.entry, 2, 6, 3, 1)

        self.label = Gtk.Label("Adresse")
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 1, 7, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 7, 3, 1)

        self.label = Gtk.Label("E-mail")
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 1, 8, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 8, 3, 1)

        self.label = Gtk.Label("Numéro\ntéléphone")
        self.label.set_hexpand(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 1, 9, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 9, 3, 1)

        self.label = Gtk.Label("Numéro\nSIRET/SIREN")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 1, 10, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 2, 10, 3, 1)

        self.button = Gtk.Button(label="Sauvegarder utilisateur")
        self.grid.attach(self.button, 1, 11, 2, 1)

        self.button = Gtk.Button(label="Charger utilisateur")
        self.grid.attach(self.button, 3, 11, 2, 1)

        ##########################################
        self.label = Gtk.Label("<big>A</big>")
        self.label.set_hexpand(True)
        self.label.set_use_markup(True)
        self.grid.attach(self.label, 5, 3, 1, 1)

        self.label = Gtk.Label("Nom\nEntreprise")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 5, 4, 1, 1)
        self.label.set_hexpand(True)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.grid.attach(self.entry, 6, 4, 3, 1)

        self.label = Gtk.Label("Nom")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 5, 5, 1, 1)
        self.label.set_hexpand(True)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.grid.attach(self.entry, 6, 5, 3, 1)

        self.label = Gtk.Label("Prenom")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 5, 6, 1, 1)
        self.label.set_hexpand(True)
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.grid.attach(self.entry, 6, 6, 3, 1)

        self.label = Gtk.Label("Adresse")
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 5, 7, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 6, 7, 3, 1)

        self.label = Gtk.Label("E-mail")
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 5, 8, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 6, 8, 3, 1)

        self.label = Gtk.Label("Numéro\ntéléphone")
        self.label.set_hexpand(True)
        self.label.set_justify(Gtk.Justification.CENTER)
        self.grid.attach(self.label, 5, 9, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 6, 9, 3, 1)

        self.label = Gtk.Label("Numéro\nSIRET/SIREN")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_hexpand(True)
        self.grid.attach(self.label, 5, 10, 1, 1)
        self.entry = Gtk.Entry()
        self.grid.attach(self.entry, 6, 10, 3, 1)


        self.button = Gtk.Button(label="Importer client")
        self.grid.attach(self.button, 7, 11, 2, 1)

        self.button = Gtk.Button(label="Sauvegarder client")
        self.grid.attach(self.button, 5, 11, 2, 1)
        # self.vsep = Gtk.VSeparator()
        # self.grid.insert_column(5)
        # self.grid.attach(self.vsep, 5,4, 1, 11)
        self.main_grid = Gtk.Grid(column_homogeneous=False,
                                     row_homogeneous=False,
                             column_spacing=20, row_spacing=20)
        self.add(self.main_grid)
        spacel = Gtk.Label("")
        spacel.set_hexpand(True)
        self.main_grid.attach(spacel, 1, 1, 1, 3)
        spacer = Gtk.Label("")
        spacer.set_hexpand(True)
        self.main_grid.attach(spacer, 3, 1, 1, 3)
        # self.box.set_hexpand(True)
        # self.box.set_halign(Gtk.Align.CENTER)
        self.main_grid.attach(self.grid, 2, 1, 1, 1)
        self.article_header()
        self.initial_article_row()
        self.sep = Gtk.HSeparator()
        self.main_grid.attach(self.sep, 2, 2, 1, 1)
        self.main_grid.attach(self.article_grid, 2, 3, 1, 1)
        self.plus_btn_box()
        self.sep = Gtk.HSeparator()
        self.main_grid.attach(self.sep, 2, 4, 1, 1)
        self.total()
        self.total_grid.set_halign(Gtk.Align.END)
        self.main_grid.attach(self.total_grid, 2, 5, 1, 1)
        self.sep = Gtk.HSeparator()
        self.main_grid.attach(self.sep, 2, 6, 1, 1)
        self.button = Gtk.Button(label='Créer')
        self.button.set_halign(Gtk.Align.END)
        self.main_grid.attach(self.button, 2, 7, 1, 1)

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
        self.label.set_xalign(0.9)
        self.article_grid.attach(self.label, 4, 1, 1, 1)

        self.label = Gtk.Label("Quantité")
        self.label.set_xalign(0.9)
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

        self.entry = Gtk.Entry(placeholder_text="Description")
        self.article_grid.attach(self.entry , 2, i, 2, 1)
        row_widgets.append(self.entry)

        self.price_entry = Gtk.Entry(placeholder_text="0.00")
        self.price_entry.set_alignment(1)
        self.article_grid.attach(self.price_entry , 4, i, 1, 1)
        row_widgets.append(self.price_entry)

        self.qty_entry = Gtk.Entry(placeholder_text="1")
        self.qty_entry.set_alignment(1)
        self.article_grid.attach(self.qty_entry , 5, i, 1, 1)
        row_widgets.append(self.qty_entry)

        entries = (self.price_entry, self.qty_entry)
        self.label = Gtk.Label("0,00 €")
        self.article_grid.attach(self.label, 6, i, 1, 1)
        row_widgets.append(self.label)

        self.price_entry.connect("changed", self.modify_label, *entries, self.label)
        self.qty_entry.connect("changed", self.modify_label, *entries, self.label)

        self.checkbutton = Gtk.CheckButton()
        self.checkbutton.set_valign(Gtk.Align.CENTER)
        self.checkbutton.set_halign(Gtk.Align.CENTER)
        self.article_grid.attach(self.checkbutton, 7, i, 1, 1)
        row_widgets.append(self.checkbutton)

        self.entry = Gtk.Entry(placeholder_text="Détails additionnels")
        # self.entry.set_hexpand(True)
        self.article_grid.attach(self.entry , 2, i+1, 2, 2)
        row_widgets.append(self.entry)

        # self.row_box.pack_start(self.article_grid, True, True, 0)
        for wid in row_widgets:
            wid.set_visible(True)


    def modify_label(self, entry, price_ent, qty_ent, label):
        price = int(price_ent.get_text())
        qty = int(qty_ent.get_text())
        label.set_text(f"{price * qty} €")

    def initial_article_row(self):
        self.label = Gtk.Label("")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 1, 2, 1, 1)

        self.entry = Gtk.Entry(placeholder_text="Description")
        self.article_grid.attach(self.entry , 2, 2, 2, 1)

        self.price_entry = Gtk.Entry(placeholder_text="0.00")
        self.price_entry.set_alignment(1)
        self.article_grid.attach(self.price_entry , 4, 2, 1, 1)

        self.qty_entry = Gtk.Entry(placeholder_text="1")
        self.qty_entry.set_alignment(1)
        self.article_grid.attach(self.qty_entry , 5, 2, 1, 1)

        self.entries = (self.price_entry, self.qty_entry)
        self.label = Gtk.Label("0,00 €")
        self.article_grid.attach(self.label, 6, 2, 1, 1)

        self.price_entry.connect("changed", self.modify_label, *self.entries, self.label)
        self.qty_entry.connect("changed", self.modify_label, *self.entries, self.label)

        self.checkbutton = Gtk.CheckButton()
        self.checkbutton.set_valign(Gtk.Align.CENTER)
        self.checkbutton.set_halign(Gtk.Align.CENTER)
        self.article_grid.attach(self.checkbutton, 7, 2, 1, 1)

        self.entry = Gtk.Entry(placeholder_text="Détails additionnels")
        self.article_grid.attach(self.entry , 2, 3, 2, 2)


    def total(self):
        self.total_grid = Gtk.Grid(column_homogeneous=True,
                                     row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self.label = Gtk.Label("Subtotal")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 1, 1, 1)
        self.label = Gtk.Label("Tax (21%)")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 2, 1, 1)
        self.label = Gtk.Label("Total")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 3, 1, 1)
        self.label = Gtk.Label("Montant Du")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 4, 1, 1)

        self.space = Gtk.Label("")
        self.total_grid.attach(self.space, 2, 1, 1, 3)

        self.label = Gtk.Label("0,00 €")
        self.label.set_xalign(1)
        self.total_grid.attach(self.label, 3, 1, 1, 1)
        self.label = Gtk.Label("0,00 €")
        self.label.set_xalign(1)
        self.total_grid.attach(self.label, 3, 2, 1, 1)
        self.label = Gtk.Label("0,00 €")
        self.label.set_xalign(1)
        self.total_grid.attach(self.label, 3, 3, 1, 1)
        self.label = Gtk.Label("0,00 €")
        self.label.set_xalign(1)
        self.total_grid.attach(self.label, 3, 4, 1, 1)

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
