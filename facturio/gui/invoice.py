#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from classes.client import Company
from classes.user import User

class InvoicePage(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.total_labels = []
        self.main_grid = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.__init_header_grid()
        self.__init_user_grid()
        self.__init_client_grid()
        self.__union_user_client_grid()
        self.main_grid.attach(self.header_grid, 2, 1, 1, 1)
        self.main_grid.attach(self.user_client_grid, 2, 2, 1, 1)
        # spaces sur les cotes

        spacel = Gtk.Label("")
        spacel.set_hexpand(True)
        self.main_grid.attach(spacel, 1, 1, 1, 3)
        spacer = Gtk.Label("")
        spacer.set_hexpand(True)
        self.main_grid.attach(spacer, 3, 1, 1, 3)

        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 3, 1, 1)

        self.article_header()
        self.initial_article_row()
        self.main_grid.attach(self.article_grid, 2, 4, 1, 1)
        self.plus_btn_box()

        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 5, 1, 1)

        self.__init_total_grid()
        self.total_grid.set_halign(Gtk.Align.END)

        self.__init_taxes_grid()
        self.__union_taxes_total_grid()
        self.main_grid.attach(self.taxes_total_grid, 2, 6, 1, 1)

        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 7, 1, 1)

        self.button = Gtk.Button(label='Créer')
        self.button.connect("clicked", self.test)
        self.button.set_halign(Gtk.Align.END)
        self.main_grid.attach(self.button, 2, 8, 1, 1)
        self.add(self.main_grid)

    def test(self, btn):
        self.client_data = {}
        for name, entry in self.client_entries.items():
            self.client_data[name] = entry.get_text()
        self.client_data["note"] = None
        company = Company.from_dict(self.client_data)
        self.user_data = {}
        for name, entry in self.user_entries.items():
            self.user_data[name] = entry.get_text()
        self.user_data["logo"] = None
        for art_dict in self.article_list:
            for name, entry in art_dict.items():
                print(name, entry.get_text())

        user = User.from_dict(self.user_data)
        print(company, user)

    def __init_header_grid(self):
        """Facture texte et logo"""
        self.header_grid = Gtk.Grid(row_homogeneous=True,
                                    column_homogeneous=True)
        label = Gtk.Label("<big>Facture</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        self.header_grid.attach(label, 1, 1, 4, 1)
        logo_button = Gtk.Button.new_from_icon_name("image-x-generic-symbolic",
                                                    Gtk.IconSize.BUTTON)
        logo_button.set_label('+ Logo')
        logo_button.set_always_show_image(True)
        logo_button.set_hexpand(True)
        self.header_grid.attach(logo_button, 7, 1, 2, 4)
    def __init_client_grid(self):
        self.client_grid = Gtk.Grid(column_homogeneous=True,
                                    row_homogeneous=True, column_spacing=20,
                                    row_spacing=20)
        self.client_entries = {}
        label = Gtk.Label("<big>Client</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        self.client_grid.attach(label, 1, 1, 1, 1)

        label = Gtk.Label("Nom\nEntreprise")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 4, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        self.client_entries["company_name"] = entry

        self.client_grid.attach(entry, 2, 4, 3, 1)

        label = Gtk.Label("Nom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 5, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        self.client_grid.attach(entry, 2, 5, 3, 1)
        self.client_entries["last_name"] = entry

        label = Gtk.Label("Prenom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 6, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        self.client_grid.attach(entry, 2, 6, 3, 1)
        self.client_entries["first_name"] = entry

        label = Gtk.Label("Adresse")
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 7, 1, 1)
        entry = Gtk.Entry()
        self.client_grid.attach(entry, 2, 7, 3, 1)
        self.client_entries["adress"] = entry

        label = Gtk.Label("E-mail")
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 8, 1, 1)
        entry = Gtk.Entry()
        self.client_grid.attach(entry, 2, 8, 3, 1)
        self.client_entries["email"] = entry

        label = Gtk.Label("Numéro\ntéléphone")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_grid.attach(label, 1, 9, 1, 1)
        entry = Gtk.Entry()
        self.client_grid.attach(entry, 2, 9, 3, 1)
        self.client_entries["phone_number"] = entry

        label = Gtk.Label("Numéro\nSIRET/SIREN")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 10, 1, 1)
        entry = Gtk.Entry()
        self.client_grid.attach(entry, 2, 10, 3, 1)
        self.client_entries["business_number"] = entry

        button = Gtk.Button(label="Importer client")
        self.client_grid.attach(button, 3, 11, 2, 1)

        button = Gtk.Button(label="Sauvegarder client")
        self.client_grid.attach(button, 1, 11, 2, 1)

    def __init_user_grid(self):
        self.user_grid = Gtk.Grid(column_homogeneous=True,
                                  row_homogeneous=True, column_spacing=20,
                                  row_spacing=20)
        self.user_entries = {}
        label = Gtk.Label("<big>Utilisateur</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        self.user_grid.attach(label, 1, 3, 1, 1)

        label = Gtk.Label("Nom\nEntreprise")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 4, 1, 1)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 4, 3, 1)
        self.user_entries["company_name"] = entry

        label = Gtk.Label("Nom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 5, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 5, 3, 1)
        self.user_entries["last_name"] = entry

        label = Gtk.Label("Prenom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 6, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 6, 3, 1)
        self.user_entries["first_name"] = entry

        label = Gtk.Label("Adresse")
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 7, 1, 1)
        entry = Gtk.Entry()
        self.user_grid.attach(entry, 2, 7, 3, 1)
        self.user_entries["adress"] = entry

        label = Gtk.Label("E-mail")
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 8, 1, 1)
        entry = Gtk.Entry()
        self.user_grid.attach(entry, 2, 8, 3, 1)
        self.user_entries["email"] = entry

        label = Gtk.Label("Numéro\ntéléphone")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.user_grid.attach(label, 1, 9, 1, 1)
        entry = Gtk.Entry()
        self.user_grid.attach(entry, 2, 9, 3, 1)
        self.user_entries["phone_number"] = entry

        label = Gtk.Label("Numéro\nSIRET/SIREN")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 10, 1, 1)
        entry = Gtk.Entry()
        self.user_grid.attach(entry, 2, 10, 3, 1)
        self.user_entries["business_number"] = entry

        button = Gtk.Button(label="Sauvegarder utilisateur")
        self.user_grid.attach(button, 1, 11, 2, 1)

        button = Gtk.Button(label="Charger utilisateur")
        self.user_grid.attach(button, 3, 11, 2, 1)

    def __init_taxes_grid(self):
        self.taxes_grid = Gtk.Grid(row_spacing=20)
        label = Gtk.Label("Tax")
        adj = Gtk.Adjustment(value=21, lower=0, upper=100, step_increment=1)
        self.spin_btn = Gtk.SpinButton(adjustment=adj, climb_rate=1, digits=2)
        self.spin_btn.connect("output", self.put_percentage)
        self.spin_btn.connect("change-value", self.modify_taxed_price)
        self.spin_btn.connect("value-changed", self.modify_taxed_price)
        self.taxes_grid.attach(label, 1,1,1,1)
        space = Gtk.Label("")
        space.set_hexpand(True)
        self.taxes_grid.attach(space, 2,1,1,1)
        self.taxes_grid.attach(self.spin_btn, 3,1,1,1)

        label = Gtk.Label("Date")
        self.taxes_grid.attach(label, 1,2,1,1)
        vbox = Gtk.HBox()
        date_entry = Gtk.Entry(placeholder_text="dd/mm/yyyy")
        # self.taxes_grid.attach(date_entry, 3,2,1,1)
        self.show_calendar = Gtk.ToggleButton(label="Montrer calendrier")
        vbox.pack_start(date_entry, True, True, 0)
        vbox.pack_start(self.show_calendar , True, True, 5)
        self.init_calendar()
        self.show_calendar.connect("clicked", self.test2)
        self.taxes_grid.attach(vbox, 3,2,1,1)
    def init_calendar(self):
        self.calendar_vbox = Gtk.VBox()
        validate_btn = Gtk.Button(label="Valider")
        calendar = Gtk.Calendar()
        self.calendar_vbox.pack_start(calendar, True, True, 10)
        self.calendar_vbox.pack_start(validate_btn, True, True, 0)
        self.taxes_grid.attach(self.calendar_vbox, 3,3,1,1)
    def test2(self, btn):
        if self.show_calendar.get_active():
            self.calendar_vbox.hide()
        else:
            print("here")
            self.calendar_vbox.show_all()
            self.do_scroll_child(self, Gtk.ScrollType.END, False)




    def __union_taxes_total_grid(self):
        self.taxes_total_grid= Gtk.Grid(row_homogeneous=False,
                                        column_homogeneous=False)
        self.taxes_total_grid.attach(self.taxes_grid, 1, 1, 1, 1)
        space = Gtk.Label("")
        space.set_hexpand(True)
        self.taxes_total_grid.attach(space,2, 1, 1, 1)
        vsep = Gtk.VSeparator()
        self.taxes_total_grid.attach(vsep, 3, 1, 1, 1)
        space = Gtk.Label("")
        space.set_hexpand(True)
        self.taxes_total_grid.attach(space, 4, 1, 1, 1)
        self.taxes_total_grid.attach(self.total_grid, 5, 1, 1, 1)

    def __union_user_client_grid(self):
        self.user_client_grid = Gtk.Grid(column_spacing = 20)
        self.user_client_grid.attach(self.user_grid, 1, 1, 1, 1)
        self.user_client_grid.attach(self.client_grid, 2, 1, 1, 1)

    def put_percentage(self, spin_box):
        adjustement = spin_box.get_adjustment()
        value = spin_box.get_value()
        spin_box.set_text(f"{value} %")

    def modify_taxed_price(self, spin_box= None):
        if spin_box == None:
            spin_box = self.spin_btn
        adjustement = spin_box.get_adjustment()
        value = adjustement.get_value()
        if value.is_integer():
            value = int(value)
        self.tax_label.set_text(f"Tax ({value}%)")
        sub_total_val = float(self.sub_total.get_text()[:-2])
        res = round((value/100+1) * sub_total_val, 2)
        self.price_with_taxes.set_text(f"{res} €")
        self.put_percentage(spin_box)

    def article_header(self):
        self.article_grid = Gtk.Grid(column_homogeneous=False,
                                     row_homogeneous=True,
                             column_spacing=20, row_spacing=20)

        self.btns = {}
        self.label = Gtk.Label("")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 1, 1, 1, 1)

        self.label = Gtk.Label("Article")
        self.label.set_halign(Gtk.Align.START)
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

    def plus_btn_box(self):
        self.plus_btn_row = 5
        button = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.article_grid.attach(button, 1, 5, 1, 1)

        button.connect("clicked", self.new_article_row)

    def new_article_row(self, btn=None):
        i = self.plus_btn_row
        self.plus_btn_row += 3
        for _ in range(3):
            self.article_grid.insert_row(i)
        row_widgets = []
        article_entries = {}
        button = Gtk.Button.new_from_icon_name("window-close-symbolic",
                                                    Gtk.IconSize.BUTTON)
        row_widgets.append(button)
        self.article_grid.attach(button, 1, i, 1, 1)
        self.btns[button] = i
        button.connect("clicked", self.des_widgets)

        title_entry = Gtk.Entry(placeholder_text="Nom de l'article")
        self.article_grid.attach(title_entry , 2, i, 2, 1)
        row_widgets.append(title_entry)
        article_entries["title"] = title_entry

        price_entry = Gtk.Entry(placeholder_text="0.00")
        price_entry.set_alignment(1)
        self.article_grid.attach(price_entry , 4, i, 1, 1)
        row_widgets.append(price_entry)
        article_entries["price"] = price_entry

        qty_entry = Gtk.Entry(placeholder_text="1")
        qty_entry.set_alignment(1)
        self.article_grid.attach(qty_entry , 5, i, 1, 1)
        row_widgets.append(qty_entry)
        article_entries["quantity"] = qty_entry

        label = Gtk.Label("0.00 €")
        self.total_labels.append(label)
        self.article_grid.attach(label, 6, i, 1, 1)
        row_widgets.append(label)

        price_entry.connect("changed", self.modify_label, article_entries,
                            label)
        qty_entry.connect("changed", self.modify_label, article_entries, label)

        des_entry = Gtk.Entry(placeholder_text="Détails additionnels")
        # self.entry.set_hexpand(True)
        self.article_grid.attach(des_entry , 2, i+1, 2, 2)
        row_widgets.append(des_entry)
        article_entries["description"] = des_entry
        self.article_list.append(article_entries)

        # self.row_box.pack_start(self.article_grid, True, True, 0)
        for wid in row_widgets:
            wid.set_visible(True)

    def modify_label(self, entry, entries: dict, label):
        price = int(entries["price"].get_text())
        qty = int(entries["quantity"].get_text())
        label.set_text(f"{price * qty} €")
        self.modify_total()

    def modify_total(self):
        total = 0
        for label in self.total_labels:
            print(label.get_text())
            total += int(label.get_text()[:-2])
        self.sub_total.set_text(f"{total} $")
        self.modify_taxed_price()

    def initial_article_row(self):
        self.article_list = []
        article_entries = {}
        left_space= Gtk.Label("")
        left_space.set_hexpand(True)
        self.article_grid.attach(left_space, 1, 2, 1, 1)

        entry = Gtk.Entry(placeholder_text="Nom de l'article")
        self.article_grid.attach(entry , 2, 2, 2, 1)
        article_entries["title"] = entry

        price_entry = Gtk.Entry(placeholder_text="0.00")
        price_entry.set_alignment(1)
        self.article_grid.attach(price_entry , 4, 2, 1, 1)
        article_entries["price"] = price_entry

        qty_entry = Gtk.Entry(placeholder_text="1")
        qty_entry.set_alignment(1)
        self.article_grid.attach(qty_entry , 5, 2, 1, 1)
        article_entries["quantity"] = qty_entry

        label = Gtk.Label("0.00 €")
        self.total_labels.append(label)
        self.article_grid.attach(label, 6, 2, 1, 1)

        des_entry = Gtk.Entry(placeholder_text="Détails additionnels")
        self.article_grid.attach(des_entry, 2, 3, 2, 2)
        article_entries["description"] = des_entry

        price_entry.connect("changed", self.modify_label, article_entries,
                            label)
        qty_entry.connect("changed", self.modify_label, article_entries, label)
        self.article_list.append(article_entries)


    def __init_total_grid(self):
        self.total_grid = Gtk.Grid(column_homogeneous=True,
                                     row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self.label= Gtk.Label("Subtotal")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 1, 1, 1)
        self.tax_label = Gtk.Label("Tax (21%)")
        self.tax_label.set_xalign(0)
        self.total_grid.attach(self.tax_label, 1, 2, 1, 1)
        self.label = Gtk.Label("Total")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 3, 1, 1)
        self.label = Gtk.Label("Montant Du")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 4, 1, 1)

        self.space = Gtk.Label("")
        self.total_grid.attach(self.space, 2, 1, 1, 3)

        self.sub_total = Gtk.Label("0.00 €")
        self.sub_total.set_xalign(1)
        self.total_grid.attach(self.sub_total, 3, 1, 1, 1)

        self.price_with_taxes = Gtk.Label("0.00 €")
        self.price_with_taxes.set_xalign(1)
        self.total_grid.attach(self.price_with_taxes, 3, 2, 1, 1)

        self.label = Gtk.Label("0.00 €")
        self.label.set_xalign(1)
        self.total_grid.attach(self.label, 3, 3, 1, 1)
        self.label = Gtk.Label("0.00 €")
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
