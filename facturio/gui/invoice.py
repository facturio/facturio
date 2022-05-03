#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from facturio.classes.client import Company, Client
from facturio.classes.user import User
from facturio.classes.invoice_misc import Article, Invoice, Advance, Estimate
from facturio.build_pdf.build_pdf import build_pdf
from datetime import datetime
import re
from datetime import date





class InvoicePage(Gtk.ScrolledWindow):
    """Page pour la creation invoice."""

    def __init__(self):
        super().__init__()
        self.main_grid = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self._init_header_grid()
        self._init_user_grid()
        self._init_client_grid()
        self._union_user_client_grid()
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

        self._article_header()
        self._first_article_row()
        self.main_grid.attach(self.article_grid, 2, 4, 1, 1)
        self._plus_btn_row()

        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 5, 1, 1)

        self._init_total_grid()
        self.total_grid.set_halign(Gtk.Align.END)

        self._init_taxes_grid()
        self._union_taxes_total_grid()
        self.main_grid.attach(self.taxes_total_grid, 2, 6, 1, 1)

        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 7, 1, 1)

        self.spinner = Gtk.Spinner()
        self.create_button = Gtk.Button(label='Créer')
        self.create_button.connect("clicked", self._gen_invoice)
        self.create_button.set_halign(Gtk.Align.END)
        hbox = Gtk.HBox()
        hbox.pack_start(self.spinner, True, True, 20)
        self.error_label = Gtk.Label()
        hbox.pack_start(self.error_label, True, True, 20)
        hbox.pack_start(self.create_button, True, True, 0)
        hbox.set_halign(Gtk.Align.END)
        self.main_grid.attach(hbox, 2, 8, 1, 1)
        self.company_switch.set_active(True)

        space = Gtk.Label("")
        self.main_grid.attach(space, 2, 9, 1, 1)
        self.add(self.main_grid)

    def _init_header_grid(self):
        """Facture texte et logo"""
        self.header_grid = Gtk.Grid(row_homogeneous=True,
                                    column_homogeneous=True)
        label = Gtk.Label("<big>Facture</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        self.header_grid.attach(label, 1, 1, 4, 1)
        self.logo_button = Gtk.Button.new_from_icon_name("image-x-generic-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.logo_button.set_label('+ Logo')
        self.logo_button.set_always_show_image(True)
        self.logo_button.set_hexpand(True)
        self.header_grid.attach(self.logo_button, 7, 1, 2, 4)
        self.logo_fn = None
        self.logo_button.connect("clicked", self._logo_dialog)

    def test(self, entry):
        if entry == self.client_switch:
            self.client_entries["company_name"].hide()
            self.client_labels["company_name"].hide()
            self.client_entries["business_number"].hide()
            self.client_labels["business_number"].hide()
            # supression de soulignemet rouge
            for entry in self.client_entries.values():
                self.reset_context(entry)

        elif entry == self.company_switch:
            self.client_entries["company_name"].show()
            self.client_labels["company_name"].show()
            self.client_entries["business_number"].show()
            self.client_labels["business_number"].show()
            # supression de soulignemet rouge
            for entry in self.client_entries.values():
                self.reset_context(entry)

    @staticmethod
    def valid_email(email: str):
        """Valid a email."""
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        res = False
        if(re.fullmatch(regex, email)):
            res = True
        return res

    def _init_client_grid(self):
        self.client_grid = Gtk.Grid(column_homogeneous=True,
                                    column_spacing=20,
                                    row_spacing=20)
        self.client_entries = {}
        self.client_labels= {}
        label = Gtk.Label("<big>Client</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        hbox = Gtk.HBox()
        # hbox.pack_start(label, True, True, 10)
        self.client_switch = Gtk.RadioButton(label="Particulier")
        self.company_switch = Gtk.RadioButton(group=self.client_switch,
                                              label="Entreprise")
        self.company_switch.connect("clicked", self.test)
        self.client_switch.connect("clicked", self.test)
        self.client_switch.set_mode(False)
        self.company_switch.set_mode(False)
        hbox.pack_start(self.client_switch, True, True, 0)
        hbox.pack_start(self.company_switch, True, True, 0)
        Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")

        self.client_grid.attach(label, 1, 1, 1, 1)
        self.client_grid.attach(hbox, 2, 1, 3, 1)

        label = Gtk.Label("Nom\nEntreprise")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 4, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.client_entries["company_name"] = entry
        self.client_labels["company_name"] = label

        self.client_grid.attach(entry, 2, 4, 3, 1)

        label = Gtk.Label("Nom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 5, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.client_grid.attach(entry, 2, 5, 3, 1)
        self.client_entries["last_name"] = entry
        self.client_labels["last_name"] = label

        label = Gtk.Label("Prenom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 6, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.client_grid.attach(entry, 2, 6, 3, 1)
        self.client_entries["first_name"] = entry
        self.client_labels["first_name"] = label

        label = Gtk.Label("Adresse")
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 7, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(100)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 7, 3, 1)
        self.client_entries["adress"] = entry
        self.client_labels["adress"] = label

        label = Gtk.Label("E-mail")
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 8, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 8, 3, 1)
        self.client_entries["email"] = entry
        self.client_labels["email"] = label

        label = Gtk.Label("Numéro\ntéléphone")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_grid.attach(label, 1, 9, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.connect("insert-text", self.allow_only_phone)
        self.client_grid.attach(entry, 2, 9, 3, 1)
        self.client_entries["phone_number"] = entry
        self.client_labels["phone_number"] = label

        label = Gtk.Label("Numéro\nSIRET/SIREN")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 10, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 10, 3, 1)
        self.client_entries["business_number"] = entry
        self.client_labels["business_number"] = label

        button = Gtk.Button(label="Importer client")
        self.client_grid.attach(button, 3, 11, 2, 1)

        button = Gtk.Button(label="Sauvegarder client")
        self.client_grid.attach(button, 1, 11, 2, 1)
    # def _get_active_btn(self):
    #     self.client_switch.get_group
    def allow_only_phone(self, entry, string, *args):
        for char in string:
            if not char.isdigit() and char != " " and char != "-":
                GObject.signal_stop_emission_by_name(entry,"insert-text")

    def allow_only_digits(self, entry, string, *args):
        for char in string:
            if not char.isdigit():
                GObject.signal_stop_emission_by_name(entry,"insert-text")

    def allow_only_float(self, entry, string, *args):
        txt = entry.get_text()
        for char in string:
            if "." not in txt:
                if not char.isdigit() and char != ".":
                    GObject.signal_stop_emission_by_name(entry, "insert-text")
            else:
                if not char.isdigit():
                    GObject.signal_stop_emission_by_name(entry, "insert-text")
        return

    def _init_user_grid(self):
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
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 4, 3, 1)
        self.user_entries["company_name"] = entry

        label = Gtk.Label("Nom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 5, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 5, 3, 1)
        self.user_entries["last_name"] = entry

        label = Gtk.Label("Prenom")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 6, 1, 1)
        label.set_hexpand(True)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 6, 3, 1)
        self.user_entries["first_name"] = entry

        label = Gtk.Label("Adresse")
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 7, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(100)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 7, 3, 1)
        self.user_entries["adress"] = entry

        label = Gtk.Label("E-mail")
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 8, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 8, 3, 1)
        self.user_entries["email"] = entry

        label = Gtk.Label("Numéro\ntéléphone")
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.user_grid.attach(label, 1, 9, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.connect("insert-text", self.allow_only_phone)
        self.user_grid.attach(entry, 2, 9, 3, 1)
        self.user_entries["phone_number"] = entry

        label = Gtk.Label("Numéro\nSIRET/SIREN")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 10, 1, 1)

        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 10, 3, 1)
        self.user_entries["business_number"] = entry

        button = Gtk.Button(label="Sauvegarder utilisateur")
        self.user_grid.attach(button, 1, 11, 2, 1)

        button = Gtk.Button(label="Charger utilisateur")
        self.user_grid.attach(button, 3, 11, 2, 1)

    def reset_context(self, entry):
        context = entry.get_style_context()
        context.remove_class("entry_error")

    def _init_taxes_grid(self):
        self.taxes_grid = Gtk.Grid(row_spacing=20)
        label = Gtk.Label("Tax")
        adj = Gtk.Adjustment(value=21, lower=0, upper=100, step_increment=1)
        self.spin_btn = Gtk.SpinButton(adjustment=adj, climb_rate=1, digits=2)
        self.spin_btn.connect("output", self._put_percentage)
        self.spin_btn.connect("change-value", self._modify_tax_fields)
        self.spin_btn.connect("value-changed", self._modify_tax_fields)
        self.taxes_grid.attach(label, 1,1,1,1)
        space = Gtk.Label("")
        space.set_hexpand(True)
        self.taxes_grid.attach(space, 2,1,1,1)
        self.taxes_grid.attach(self.spin_btn, 3,1,1,1)

        label = Gtk.Label("Date")
        self.taxes_grid.attach(label, 1,2,1,1)
        vbox = Gtk.HBox()
        self.date_entry = Gtk.Entry(placeholder_text="dd/mm/yyyy")
        self.date_entry.connect("changed", self.reset_context)
        today = date.today()
        self.date_entry.set_text(date.today().strftime("%d/%m/%Y"))
        # self.taxes_grid.attach(date_entry, 3,2,1,1)
        self.show_calendar = Gtk.ToggleButton(label="Montrer calendrier")
        vbox.pack_start(self.date_entry, True, True, 0)
        vbox.pack_start(self.show_calendar , True, True, 5)
        self._init_calendar()
        self.show_calendar.connect("clicked", self._wcalendar_logic)
        self.taxes_grid.attach(vbox, 3,2,1,1)

    def _init_calendar(self):
        self.calendar = Gtk.Calendar()
        self.calendar.connect("day-selected-double-click", self._wcalendar_logic)
        self.calendar.connect("day-selected", self._calendar_entry_update)
        self.calendar.connect("size-allocate", self._scroll_down)
        self.taxes_grid.attach(self.calendar, 3,3,1,1)
        adj = self.get_vadjustment()
        # variable pour gerer le scroll down lors de la activation de la datej
        self.activated_btn = False
        # variable pour gerer les signals indesirables
        self.second_signal = False

    def _init_total_grid(self):
        self.total_grid = Gtk.Grid(column_homogeneous=True,
                                   row_homogeneous=True, column_spacing=20,
                                   row_spacing=20)
        self.label= Gtk.Label("Subtotal")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 1, 1, 1)
        self.tax_label = Gtk.Label("Tax (21%)")
        self.tax_label.set_xalign(0)
        self.total_grid.attach(self.tax_label, 1, 2, 1, 1)
        self.label = Gtk.Label("Total")
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 3, 1, 1)

        self.space = Gtk.Label("")
        self.total_grid.attach(self.space, 2, 1, 1, 3)

        self.sub_total = Gtk.Label("0.00 €")
        self.sub_total.set_xalign(1)
        self.total_grid.attach(self.sub_total, 3, 1, 1, 1)

        self.total_taxes = Gtk.Label("0.00 €")
        self.total_taxes.set_xalign(1)
        self.total_grid.attach(self.total_taxes, 3, 2, 1, 1)

        self.total = Gtk.Label("0.00 €")
        self.total.set_xalign(1)
        self.total_grid.attach(self.total, 3, 3, 1, 1)

    def _union_taxes_total_grid(self):
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
        self.total_grid.set_valign(Gtk.Align.END)
        self.taxes_total_grid.attach(self.total_grid, 5, 1, 1, 1)

    def _union_user_client_grid(self):
        self.user_client_grid = Gtk.Grid(column_spacing = 20)
        self.user_client_grid.attach(self.user_grid, 1, 1, 1, 1)
        self.user_client_grid.attach(self.client_grid, 2, 1, 1, 1)

    def _calendar_entry_update(self, btn=None):
        date = (list(self.calendar.get_date()))
        date.reverse()
        # update date entry
        self.date_entry.set_text(f"{date[0]}/{date[1]}/{date[2]}")
    def _wcalendar_logic(self, btn):
        """
        Logic derriere le widget du calendrier.

        Montre et cache le widget de calendrier selon les cas de utilisation
        """
        # deuxieme signal indesirable
        if self.second_signal:
            self.second_signal = False
        else:
            if self.calendar.get_visible():
                # get date renvoi en tuple en format american
                self._calendar_entry_update()
                self.calendar.hide()
                # set active cree un nouveau appel a cette function qu'on empeche
                # grace a la variable second_signal
                self.second_signal = True
                self.show_calendar.set_active(False)
            else:
                self.calendar.show()
                self.activated_btn = True

    def _scroll_down(self, *args):
        """Scroll la barre jusqu'en bas lorsque on affiche le calendrier."""
        # scroll down seulement si le button pour montrer le calendrier
        # a ete presse'
        if self.activated_btn:
            adj = self.get_vadjustment()
            adj.set_value(adj.get_upper())
            self.activated_btn = False


    def set_error(self, entry):
        print(entry)
        data = entry.get_text()
        context = entry.get_style_context()
        context.add_class("entry_error")

    def _validate_user_entries(self):
        """Renvoi True si les donnees saisis sont valides."""
        error = True
        for name, entry in self.user_entries.items():
            data = entry.get_text()
            if name == "email":
                if not self.valid_email(entry.get_text()) and data != "":
                    self.set_error(entry)
                    error = False
            if data == "":
                self.set_error(entry)
                error = False
        return error

    def _validate_client_entries(self):
        """Renvoi True si les donnees saisis sont valides."""
        error = True
        if self.client_switch.get_active():
            for name, entry in self.client_entries.items():
                data = entry.get_text()
                if name == "email":
                    if not self.valid_email(entry.get_text()) and data != "":
                        self.set_error(entry)
                        error = False
                elif ((name == "first_name" or name == "last_name") and data == ""):
                    self.set_error(entry)
                    error = False
        else:
            assert(self.company_switch.get_active())
            for name, entry in self.client_entries.items():
                data = entry.get_text()
                if name == "email":
                    if not self.valid_email(entry.get_text()) and data != "":
                        self.set_error(entry)
                        error = False
                if data == "":
                    self.set_error(entry)
                    error = False
        return error

    def _raise_error(self):
        self.spinner.stop()
        self.spinner.hide()
        self.error_label.set_text("Champs non valides")
        self.error_label.show()

    def _validate_date(self):
        date_regex = "[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}"
        error = True
        if not re.fullmatch(date_regex, self.date_entry.get_text()):
            self.set_error(self.date_entry)
            error = False
        return error

    def _validate_article_entries(self):
        error = False   # error_found
        for art_dict in self.article_list:
            try:
                float(art_dict["price"].get_text())
            except ValueError:
                self.set_error(art_dict["price"])
                error = True
            if not art_dict["quantity"].get_text().isdigit():
                self.set_error(art_dict["quantity"])
                error = True
            if art_dict["title"].get_text() == "":
                self.set_error(art_dict["title"])
                error = True
        print(error)
        return not error

    def validate_entries(self):
        """Retrouve si il a des erreurs sur les entry."""
        error_found = False
        if self._validate_user_entries() is False:
            error_found = True
        if self._validate_client_entries() is False:
            error_found = True
        if self._validate_article_entries() is False:
            error_found = True
        if self._validate_date() is False:
            error_found = True
        return error_found

    def _gen_invoice(self, btn):

        self.spinner.start()
        self.spinner.show()
        self.error_label.hide()

        if self.validate_entries():
            self._raise_error()
            return

        self.user_data = {}
        for name, entry in self.user_entries.items():
            self.user_data[name] = entry.get_text()
        self.user_data["logo"] = self.logo_fn

        self.client_data = {}
        self.client_data["note"] = None
        if self.company_switch.get_active():
            for name, entry in self.client_entries.items():
                self.client_data[name] = entry.get_text()
            client = Company.from_dict(self.client_data)
        else:
            assert(self.client_switch.get_active())
            names = ("first_name", "last_name", "adress", "email",
                     "phone_number")
            for name in names:
                txt = self.client_entries[name].get_text()
                if txt == "":
                    self.client_data[name] = None
                else:
                    self.client_data[name] = txt
            client = Client.from_dict(self.client_data)

        articles_dict = []
        for art_dict in self.article_list:
            dict_ = {}
            for name, entry in art_dict.items():
                dict_[name] = entry.get_text()
                # pas de try car les champs ont ete deja valides
                if name == "price" or name == "quantity":
                    dict_[name] = float(entry.get_text())

                txt = dict_[name]
                if txt == "":
                    self.client_data[name] = None
                else:
                    self.client_data[name] = txt
            articles_dict.append(dict_)


        art_instances = []
        for art_dict in articles_dict:
            art_instances.append(Article.from_dict(art_dict))

        date_text = self.date_entry.get_text()
        date = datetime.strptime(date_text, "%d/%m/%Y")
        epoch_date = date.timestamp()
        user = User.from_dict(self.user_data)

        tax = self.spin_btn.get_adjustment().get_value() / 100
        total = float(self.total.get_text()[:-2])
        inv = Invoice(user=user, client=client, articles_list=art_instances,
                      date=epoch_date, taxes=tax, amount=total)
        print(inv)
        build_pdf(inv, 27, "exemple_avec_gui.pdf")
        import webbrowser
        webbrowser.open_new("exemple_avec_gui.pdf")

    def _logo_dialog(self, *args):
        file_chooser = Gtk.FileChooserNative(title="Selectionnez une image",
                                             accept_label="Selectionner",
                                             cancel_label="Annuler")
        filter_ = Gtk.FileFilter()
        filter_.set_name("Images")
        filter_.add_pattern("*.jpg")
        filter_.add_pattern("*.png")
        filter_.add_pattern("*.jpeg")
        file_chooser.set_filter(filter_)
        if file_chooser.run() == Gtk.ResponseType.ACCEPT:
           self.logo_fn = file_chooser.get_filename()
           self.logo_button.set_sensitive(False)
           self.logo_button.set_label(" Ajouté")

    def _put_percentage(self, spin_btn):
        """
        ajoute un pourcentage a la fin pour les taxes
        """
        adjustement = spin_btn.get_adjustment()
        value = spin_btn.get_value()
        spin_btn.set_text(f"{value} %")
    def _modify_tax_fields(self, spin_btn=None):
        """
        modifie le porcentage des taxes ainsi que la valeur et le total
        """
        if spin_btn == None:
            spin_btn = self.spin_btn
        adjustement = spin_btn.get_adjustment()
        value = adjustement.get_value()
        if value.is_integer():
            value = int(value)
        self.tax_label.set_text(f"Tax ({value}%)")
        sub_total_val = float(self.sub_total.get_text()[:-2])
        res = round((value/100) * sub_total_val, 2)
        self.total_taxes.set_text(f"{res} €")
        self._put_percentage(spin_btn)
        self._modify_total()

    def _modify_sub_total(self):
        """
        modifie le sous total
        """
        total = 0
        for label in self.total_articles:
            print(label.get_text())
            total += float(label.get_text()[:-2])
        self.sub_total.set_text(f"{total} €")
        self._modify_tax_fields()
        self._modify_total()

    def _modify_total(self):
        sub_total = float(self.sub_total.get_text()[:-2])
        total_taxes = float(self.total_taxes.get_text()[:-2])
        self.total.set_text(f"{round(sub_total + total_taxes, 2)} €")

    def _article_header(self):
        """
        Entete pour l'ajout des articles
        """
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

    def _first_article_row(self):
        """
        premier ligne des article different des autres car pas de button
        supprimer
        """
        self.article_list = []
        self.total_articles= []
        article_entries = {}
        left_space= Gtk.Label("")
        left_space.set_hexpand(True)
        self.article_grid.attach(left_space, 1, 2, 1, 1)

        entry = Gtk.Entry(placeholder_text="Nom de l'article")
        entry.connect("changed", self.reset_context)
        entry.set_max_length(25)
        self.article_grid.attach(entry , 2, 2, 2, 1)
        article_entries["title"] = entry

        price_entry = Gtk.Entry(placeholder_text="0.00")
        price_entry.connect("insert-text", self.allow_only_float)
        price_entry.connect("changed", self.reset_context)
        price_entry.set_alignment(1)
        self.article_grid.attach(price_entry , 4, 2, 1, 1)
        article_entries["price"] = price_entry

        qty_entry = Gtk.Entry(placeholder_text="1")
        qty_entry.set_alignment(1)
        qty_entry.connect("insert-text", self.allow_only_digits)
        qty_entry.connect("changed", self.reset_context)
        self.article_grid.attach(qty_entry , 5, 2, 1, 1)
        article_entries["quantity"] = qty_entry

        label = Gtk.Label("0.00 €")
        self.total_articles.append(label)
        self.article_grid.attach(label, 6, 2, 1, 1)

        des_entry = Gtk.Entry(placeholder_text="Détails additionnels")
        des_entry.set_max_length(100)
        self.article_grid.attach(des_entry, 2, 3, 2, 2)
        des_entry.connect("changed", self.reset_context)
        article_entries["description"] = des_entry

        price_entry.connect("changed", self._update_total_article, article_entries,
                            label)
        qty_entry.connect("changed", self._update_total_article, article_entries, label)
        self.article_list.append(article_entries)

    def _plus_btn_row(self):
        """Ajoute un lige avec un button plus."""
        self.plus_btn_row = 5
        button = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                                    Gtk.IconSize.BUTTON)
        self.article_grid.attach(button, 1, 5, 1, 1)

        button.connect("clicked", self._new_article)

    def _new_article(self, btn=None):
        """
        insere une nouvelle formulaire pour ajouter un article
        """
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
        button.connect("clicked", self._remove_article_form)

        title_entry = Gtk.Entry(placeholder_text="Nom de l'article")
        title_entry.connect("changed", self.reset_context)
        title_entry.set_max_length(25)
        self.article_grid.attach(title_entry, 2, i, 2, 1)
        row_widgets.append(title_entry)
        article_entries["title"] = title_entry

        price_entry = Gtk.Entry(placeholder_text="0.00")
        price_entry.connect("changed", self.reset_context)
        price_entry.set_alignment(1)
        price_entry.connect("insert-text", self.allow_only_float)
        self.article_grid.attach(price_entry , 4, i, 1, 1)
        row_widgets.append(price_entry)
        article_entries["price"] = price_entry

        qty_entry = Gtk.Entry(placeholder_text="1")
        qty_entry.connect("insert-text", self.allow_only_digits)
        qty_entry.connect("changed", self.reset_context)
        qty_entry.set_alignment(1)
        self.article_grid.attach(qty_entry , 5, i, 1, 1)
        row_widgets.append(qty_entry)
        article_entries["quantity"] = qty_entry

        label = Gtk.Label("0.00 €")
        self.total_articles.append(label)
        self.article_grid.attach(label, 6, i, 1, 1)
        row_widgets.append(label)

        price_entry.connect("changed", self._update_total_article, article_entries,
                            label)
        qty_entry.connect("changed", self._update_total_article, article_entries, label)

        des_entry = Gtk.Entry(placeholder_text="Détails additionnels")
        des_entry.connect("insert-text", self.allow_only_float)
        des_entry.set_max_length(100)
        # self.entry.set_hexpand(True)
        self.article_grid.attach(des_entry , 2, i+1, 2, 2)
        row_widgets.append(des_entry)
        article_entries["description"] = des_entry
        self.article_list.append(article_entries)

        # self.row_box.pack_start(self.article_grid, True, True, 0)
        for wid in row_widgets:
            wid.set_visible(True)

    def _update_total_article(self, entry, entries: dict, label):
        """
        Met a jour le total prix * quantite
        """
        price_txt = entries["price"].get_text()
        qty_txt = entries["quantity"].get_text()
        # Si le text n'a pas ete saisi sur un des champs arrete du program
        if price_txt == "" or qty_txt == "":
            return
        price = float(entries["price"].get_text())
        qty = int(entries["quantity"].get_text())
        label.set_text(f"{round(price * qty, 2)} €")
        self._modify_sub_total()

    def _update_dict(self, i):
        """
        mis a jour du dictionaire liant chaque button supprimer a la ligne
        dans la grille
        """
        for btn, row in self.btns.items():
            if row > i:
                self.btns[btn] = row-3

    def _remove_article_form(self, btn):
        """
        supprime le formulaire article correspondant au button
        """
        line = self.btns.pop(btn)
        self.total_articles.pop(line//3)
        self.article_list.pop(line//3)
        self.article_grid.remove_row(line)
        self.article_grid.remove_row(line)
        self.article_grid.remove_row(line)
        self._update_dict(line)
        self.plus_btn_row -= 3
        self._modify_sub_total()
