#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk
import i18n
from facturio.classes.client import Company, Client
from facturio.classes.user import User
from facturio.classes.invoice_misc import Article, Invoice, Estimate, Advance
from facturio.gui.home import HeaderBarSwitcher
from facturio.db.invoicedao import InvoiceDAO
from facturio.db.userdao import UserDAO
from facturio.db.estimatedao import EstimateDAO
from facturio.db.advancedao import AdvanceDAO
from datetime import datetime
import re
from datetime import date


class ShowInvoicePage(Gtk.ScrolledWindow):
    """Page pour montrer des factures et ajouter des accomptes."""

    __instance = None

    def get_instance():
        """Renvoie l'instance."""
        if ShowInvoicePage.__instance is None:
            ShowInvoicePage.__instance = ShowInvoicePage()
        return ShowInvoicePage.__instance

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
        # self._plus_btn_row()

        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 5, 1, 1)
        self._init_advances_grid()
        self.advances_grid.set_halign(Gtk.Align.CENTER)
        self.main_grid.attach(self.advances_grid, 2, 6, 1, 1)
        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 7, 1, 1)

        self._init_total_grid()
        self.total_grid.set_halign(Gtk.Align.END)

        # self._init_taxes_grid()
        self._union_taxes_total_grid()
        self.main_grid.attach(self.taxes_total_grid, 2, 8, 1, 1)

        sep = Gtk.HSeparator()
        self.main_grid.attach(sep, 2, 9, 1, 1)

        # self.create_inv_btn = Gtk.Button(label="Creer Facture")
        # self.create_inv_btn.set_halign(Gtk.Align.END)
        self.save_modifs_btn = Gtk.Button(label="Sauvegarder modifications")
        self.save_modifs_btn.connect("clicked", self._update_receipt)

        hbox = Gtk.HBox()
        self.error_label = Gtk.Label()
        hbox.pack_start(self.error_label, True, True, 20)
        hbox.pack_start(self.save_modifs_btn, True, True, 20)
        # hbox.pack_start(self.create_inv_btn, True, True, 0)
        hbox.set_halign(Gtk.Align.END)
        self.main_grid.attach(hbox, 2, 10, 1, 1)

        space = Gtk.Label("")
        self.main_grid.attach(space, 2, 11, 1, 1)
        self.add(self.main_grid)

    def _update_receipt(self, btn=None):
        # Validation de la date
        for adv_dict in self.all_adv_entries:
            if not self._validate_date(adv_dict["date"]):
                return None
        adv_insts = []
        for adv_dict in self.all_adv_entries:
            amount = round(float(adv_dict["amount"].get_text()), 2)
            date_text = adv_dict["date"].get_text()
            date = datetime.strptime(date_text, "%d/%m/%Y")
            epoch_date = date.timestamp()
            adv_insts.append(Advance(amount=amount,
                                     date=epoch_date,
                                     id_invoice=self.receipt.id_)
                             )
        dao = AdvanceDAO.get_instance()
        for adv in adv_insts:
            dao.insert(adv)

    def _init_advances_grid(self):
        self.advances_grid = Gtk.Grid(column_homogeneous=False,
                                      row_homogeneous=True,
                                      column_spacing=20, row_spacing=20)
        label = Gtk.Label(label="Accomptes")
        label.set_halign(Gtk.Align.CENTER)
        self.advances_grid.attach(label, 1, 1, 4, 1)
        btn = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                            Gtk.IconSize.BUTTON)

        label = Gtk.Label(label="Date")
        label.set_halign(Gtk.Align.CENTER)
        label.set_size_request(200, -1)
        self.advances_grid.attach(label, 2, 2, 1, 1)
        label = Gtk.Label(label="Montant")
        label.set_size_request(200, -1)
        label.set_halign(Gtk.Align.CENTER)
        self.advances_grid.attach(label, 3, 2, 1, 1)
        btn.connect("clicked", self._new_adv_row)
        self.advances_grid.attach(btn, 1, 3, 1, 1)

        self.row_pbtn = 3
        self.btns_row = {}
        self.all_adv_entries = []

    def _delete_row(self, btn):
        row = self.btns_row.pop(btn)
        self.all_adv_entries.pop(row - 3)
        self.advances_grid.remove_row(row)
        for btn in self.btns_row.keys():
            if row < self.btns_row[btn]:
                self.btns_row[btn] -= 1
        self.row_pbtn -= 1
        self._update_adv_total()

    def _clean_advance_grid(self):
        n = len(self.all_adv_entries)
        for i in range(n):
            self.advances_grid.remove_row(3)
        self.all_adv_entries = []
        self._update_adv_total()
        self.row_pbtn = 3



        return
    def _validate_date(self, entry):
        date_regex = "[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}"
        error = True
        if not re.fullmatch(date_regex, entry.get_text()):
            self.set_error(entry)
            error = False
        return error

    def _update_adv_total(self, *args):
        total = 0
        for adv_dict in self.all_adv_entries:
            entry = adv_dict["amount"]
            if entry.get_text() != "":
                total += float(entry.get_text())
        self.adv_total.set_text(str(round(total, 2)) + " €")
        self._update_total()

    def _update_total(self):
        sub_total = float(self.sub_total.get_text()[:-2])
        total_taxes = float(self.total_taxes.get_text()[:-2])
        adv_total = float(self.adv_total.get_text()[:-2])
        total = round(sub_total + total_taxes - adv_total, 2)
        self.total.set_text(f"{total} €")

    def _new_grayed_adv_row(self):
        i = self.row_pbtn
        self.advances_grid.insert_row(i)
        btn = Gtk.Button.new_from_icon_name("window-close-symbolic",
                                            Gtk.IconSize.BUTTON)
        adv_entries = {}
        # self.btns_row[btn] = i
        # btn.connect("clicked", self._delete_row)
        # btn.show()
        # self.advances_grid.attach(btn, 1, i, 1, 1)
        entry = self._grayed_entry()
        entry.show()
        adv_entries["date"] = entry
        self.advances_grid.attach(entry, 2, i, 1, 1)
        entry = self._grayed_entry()
        adv_entries["amount"] = entry
        entry.show()
        self.advances_grid.attach(entry, 3, i, 1, 1)
        self.row_pbtn += 1
        self.all_adv_entries.append(adv_entries)

    def _new_adv_row(self, *args):
        i = self.row_pbtn
        self.advances_grid.insert_row(i)
        btn = Gtk.Button.new_from_icon_name("window-close-symbolic",
                                            Gtk.IconSize.BUTTON)
        adv_entries = {}
        self.btns_row[btn] = i
        btn.connect("clicked", self._delete_row)
        btn.show()
        self.advances_grid.attach(btn, 1, i, 1, 1)
        entry = Gtk.Entry(placeholder_text="dd/mm/YYYY")
        entry.set_text(date.today().strftime("%d/%m/%Y"))
        entry.connect("insert-text", self._allow_only_date)
        entry.show()
        entry.set_max_length(10)
        adv_entries["date"] = entry
        self.advances_grid.attach(entry, 2, i, 1, 1)
        entry = Gtk.Entry(placeholder_text="Montant")
        adv_entries["amount"] = entry
        entry.connect("insert-text", self._allow_only_float)
        entry.connect("changed", self._update_adv_total)
        entry.show()
        self.advances_grid.attach(entry, 3, i, 1, 1)
        self.row_pbtn += 1
        self.all_adv_entries.append(adv_entries)

    def _allow_only_date(self, entry, string, *args):
        for char in string:
            if not char.isdigit() and char != "/":
                GObject.signal_stop_emission_by_name(entry, "insert-text")

    def _allow_only_float(self, entry, string, *args):
        txt = entry.get_text()
        for char in string:
            if "." not in txt:
                if not char.isdigit() and char != ".":
                    GObject.signal_stop_emission_by_name(entry, "insert-text")
            else:
                if not char.isdigit():
                    GObject.signal_stop_emission_by_name(entry, "insert-text")
        return

    def _grayed_entry(self, *args, **kwargs):
        """Renvoie une entry grise'."""
        entry = Gtk.Entry(*args, **kwargs)
        entry.set_sensitive(False)
        return entry

    def _article_header(self):
        """Entete pour l'ajout des articles."""
        self.article_grid = Gtk.Grid(column_homogeneous=False,
                                     row_homogeneous=True,
                                     column_spacing=20, row_spacing=20)

        self.btns = {}
        self.label = Gtk.Label("")
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 1, 1, 1, 1)

        self.label = Gtk.Label(i18n.t('gui.article'))
        self.label.set_halign(Gtk.Align.START)
        self.label.set_hexpand(True)
        self.article_grid.attach(self.label, 2, 1, 2, 1)

        self.label = Gtk.Label(i18n.t('gui.price'))
        self.label.set_xalign(0.9)
        self.article_grid.attach(self.label, 4, 1, 1, 1)

        self.label = Gtk.Label(i18n.t('gui.quantity'))
        self.label.set_xalign(0.9)
        self.article_grid.attach(self.label, 5, 1, 1, 1)

        self.label = Gtk.Label(i18n.t('gui.sum'))
        self.article_grid.attach(self.label, 6, 1, 1, 1)

    def _init_header_grid(self):
        """Facture texte et logo."""
        self.header_grid = Gtk.Grid(row_homogeneous=True,
                                    column_homogeneous=True)
        label = Gtk.Label("<big>" + i18n.t('gui.invoice') + "</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        self.header_grid.attach(label, 1, 1, 4, 1)
    def reset_context(self, entry):
        context = entry.get_style_context()
        context.remove_class("entry_error")
    def load_receipt(self, receipt):
        """Charge les informations de receipt dans la page."""
        user = User.get_instance()
        self.receipt = receipt
        for name, entry in self.user_entries.items():
            entry.set_text(user.get_attr(name))
        client_dict = vars(receipt.client)
        if type(receipt.client) == Client:
            self.client_entries["company_name"].hide()
            self.client_labels["company_name"].hide()
            self.client_entries["business_number"].hide()
            self.client_labels["business_number"].hide()
            names = ("first_name", "last_name", "address", "email",
                     "phone_number")
            for name in names:
                self.client_entries[name].set_text(client_dict[name])
        else:
            assert(type(receipt.client) == Company)
            self.client_entries["company_name"].show()
            self.client_labels["company_name"].show()
            self.client_entries["business_number"].show()
            self.client_labels["business_number"].show()
            for name, entry in self.client_entries.items():
                entry.set_text(client_dict[name])

        # articles
        # nettoyage des lignes precedents
        self._clean_article_form()
        for _ in range(len(receipt.articles_list) - 1):
            self._new_article()

        assert(len(self.article_list) == len(receipt.articles_list))
        data = zip(self.article_list, receipt.articles_list)
        for art_entries, article in data:
            labels = ("title", "price", "quantity", "description")
            art_dict = vars(article)
            for label in labels:
                art_entries[label].set_text(str(art_dict[label]))

            total_art = str(article.quantity * article.price) + " €"
            art_entries["total_label"].set_text(total_art)

        self.sub_total.set_text(str(receipt.subtotal()) + " €")
        self.total_taxes.set_text(str(receipt.total_of_taxes()) + " €")
        self.total.set_text(str(receipt.total_with_taxes()) + " €")
        if type(receipt) == Invoice:
            print(receipt.advances_list)
            self._clean_advance_grid()
            self.adv_label.show()
            self.adv_total.show()
            self.adv_total.set_text(str(receipt.total_of_advances()) + " €")
            for _ in range(len(receipt.advances_list)):
                self._new_grayed_adv_row()
            for advance, dict_entry in zip(receipt.advances_list,
                                           self.all_adv_entries):
                dict_entry["date"].set_text(advance.date_string())
                dict_entry["amount"].set_text(str(advance.amount))
            self._update_adv_total()


        else:
            self.adv_label.hide()
            self.adv_total.hide()

    def _init_client_grid(self):
        self.client_grid = Gtk.Grid(column_homogeneous=True,
                                    row_homogeneous=True,
                                    column_spacing=20,
                                    row_spacing=20)
        self.client_entries = {}
        self.client_labels= {}

        label = Gtk.Label("<big>" + i18n.t('gui.client') + "</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        hbox = Gtk.HBox()

        self.client_grid.attach(label, 1, 1, 1, 1)
        self.client_grid.attach(hbox, 2, 1, 3, 1)

        label = Gtk.Label(i18n.t('gui.business_name'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 4, 1, 1)
        label.set_hexpand(True)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.client_entries["company_name"] = entry
        self.client_labels["company_name"] = label

        self.client_grid.attach(entry, 2, 4, 3, 1)

        label = Gtk.Label(i18n.t('gui.surname'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 5, 1, 1)
        label.set_hexpand(True)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.client_grid.attach(entry, 2, 5, 3, 1)
        self.client_entries["last_name"] = entry
        self.client_labels["last_name"] = label

        label = Gtk.Label(i18n.t('gui.name'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 6, 1, 1)
        label.set_hexpand(True)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.client_grid.attach(entry, 2, 6, 3, 1)
        self.client_entries["first_name"] = entry
        self.client_labels["first_name"] = label

        label = Gtk.Label(i18n.t('gui.address'))
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 7, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(100)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 7, 3, 1)
        self.client_entries["address"] = entry
        self.client_labels["address"] = label

        label = Gtk.Label(i18n.t('gui.email'))
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 8, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 8, 3, 1)
        self.client_entries["email"] = entry
        self.client_labels["email"] = label

        label = Gtk.Label(i18n.t('gui.phone_number'))
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_grid.attach(label, 1, 9, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 9, 3, 1)
        self.client_entries["phone_number"] = entry
        self.client_labels["phone_number"] = label

        label = Gtk.Label(i18n.t('gui.siret_number'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 10, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 10, 3, 1)
        self.client_entries["business_number"] = entry
        self.client_labels["business_number"] = label

    def _init_user_grid(self):
        self.user_grid = Gtk.Grid(column_homogeneous=True,
                                  row_homogeneous=True, column_spacing=20,
                                  row_spacing=20)
        self.user_entries = {}
        label = Gtk.Label("<big>" + i18n.t('gui.user') + "</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        self.user_grid.attach(label, 1, 3, 1, 1)


        label = Gtk.Label(i18n.t('gui.business_name'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 4, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 4, 3, 1)
        self.user_entries["company_name"] = entry

        label = Gtk.Label(i18n.t('gui.surname'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 5, 1, 1)
        label.set_hexpand(True)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 5, 3, 1)
        self.user_entries["last_name"] = entry

        label = Gtk.Label(i18n.t('gui.name'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 6, 1, 1)
        label.set_hexpand(True)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 6, 3, 1)
        self.user_entries["first_name"] = entry

        label = Gtk.Label(i18n.t('gui.address'))
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 7, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(100)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 7, 3, 1)
        self.user_entries["address"] = entry

        label = Gtk.Label(i18n.t('gui.email'))
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 8, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 8, 3, 1)
        self.user_entries["email"] = entry

        label = Gtk.Label(i18n.t('gui.phone_number'))
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.user_grid.attach(label, 1, 9, 1, 1)
        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 9, 3, 1)
        self.user_entries["phone_number"] = entry

        label = Gtk.Label(i18n.t('gui.siret_number'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 10, 1, 1)

        entry = self._grayed_entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 10, 3, 1)
        self.user_entries["business_number"] = entry


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

    def _init_total_grid(self):
        self.total_grid = Gtk.Grid(column_homogeneous=True,
                                   row_homogeneous=True, column_spacing=20,
                                   row_spacing=20)
        self.label = Gtk.Label(i18n.t('gui.subtotal'))
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 1, 1, 1)

        self.adv_label = Gtk.Label("Accomptes")
        self.adv_label.set_xalign(0)
        self.total_grid.attach(self.adv_label, 1, 2, 1, 1)

        self.tax_label = Gtk.Label(i18n.t('gui.tax') + "(21%)")
        self.tax_label.set_xalign(0)
        self.total_grid.attach(self.tax_label, 1, 3, 1, 1)
        self.label = Gtk.Label(i18n.t('gui.total'))
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 4, 1, 1)

        self.space = Gtk.Label("")
        self.total_grid.attach(self.space, 2, 1, 1, 3)

        self.sub_total = Gtk.Label("0.00 €")
        self.sub_total.set_xalign(1)
        self.total_grid.attach(self.sub_total, 3, 1, 1, 1)

        self.adv_total = Gtk.Label("0.00 €")
        self.adv_total.set_xalign(1)
        self.total_grid.attach(self.adv_total, 3, 2, 1, 1)

        self.total_taxes = Gtk.Label("0.00 €")
        self.total_taxes.set_xalign(1)
        self.total_grid.attach(self.total_taxes, 3, 3, 1, 1)

        self.total = Gtk.Label("0.00 €")
        self.total.set_xalign(1)
        self.total_grid.attach(self.total, 3, 4, 1, 1)

    def _union_taxes_total_grid(self):
        self.taxes_total_grid = Gtk.Grid(row_homogeneous=False,
                                         column_homogeneous=False)
        # self.taxes_total_grid.attach(self.taxes_grid, 1, 1, 1, 1)
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
        self.user_client_grid = Gtk.Grid(column_spacing=20)
        self.user_client_grid.attach(self.user_grid, 1, 1, 1, 1)
        self.user_client_grid.attach(self.client_grid, 2, 1, 1, 1)

    def set_error(self, entry):
        context = entry.get_style_context()
        context.add_class("entry_error")

    def _raise_error(self):
        self.error_label.set_text(i18n.t('gui.invalid_fields'))
        self.error_label.show()

    def _first_article_row(self):
        """
        Premier ligne des articles.

        Premier ligne des article different des autres
        car pas de button supprimer
        """
        self.article_list = []
        article_entries = {}
        left_space = Gtk.Label("")
        left_space.set_hexpand(True)
        self.article_grid.attach(left_space, 1, 2, 1, 1)

        entry = self._grayed_entry(placeholder_text=i18n.t('gui.article_name'))
        entry.connect("changed", self.reset_context)
        self.article_grid.attach(entry, 2, 2, 2, 1)
        article_entries["title"] = entry

        price_entry = self._grayed_entry(placeholder_text="0.00")
        price_entry.set_alignment(1)
        self.article_grid.attach(price_entry , 4, 2, 1, 1)
        article_entries["price"] = price_entry

        qty_entry = self._grayed_entry(placeholder_text="1")
        qty_entry.set_alignment(1)
        self.article_grid.attach(qty_entry , 5, 2, 1, 1)
        article_entries["quantity"] = qty_entry

        label = Gtk.Label("0.00 €")
        self.article_grid.attach(label, 6, 2, 1, 1)
        article_entries["total_label"] = label

        des_entry = self._grayed_entry(placeholder_text=i18n.t('gui.additional_details'))
        des_entry.set_max_length(100)
        self.article_grid.attach(des_entry, 2, 3, 2, 2)
        des_entry.connect("changed", self.reset_context)
        article_entries["description"] = des_entry
        self.article_list.append(article_entries)
        self.plus_btn_row = 5

    def _new_article(self):
        """Insere une nouvelle formulaire pour ajouter un article."""
        i = self.plus_btn_row
        self.plus_btn_row += 3
        for _ in range(3):
            self.article_grid.insert_row(i)
        row_widgets = []
        article_entries = {}
        # button = Gtk.Button.new_from_icon_name("window-close-symbolic",
        #                                             Gtk.IconSize.BUTTON)
        # row_widgets.append(button)
        # self.article_grid.attach(button, 1, i, 1, 1)
        # self.btns[button] = i
        # button.connect("clicked", self._remove_article_form)

        title_entry = self._grayed_entry(
            placeholder_text=i18n.t('gui.article_name'))
        title_entry.connect("changed", self.reset_context)
        title_entry.set_max_length(25)
        self.article_grid.attach(title_entry, 2, i, 2, 1)
        row_widgets.append(title_entry)
        article_entries["title"] = title_entry

        price_entry = self._grayed_entry(placeholder_text="0.00")
        price_entry.connect("changed", self.reset_context)
        price_entry.set_alignment(1)
        row_widgets.append(price_entry)
        self.article_grid.attach(price_entry , 4, i, 1, 1)
        article_entries["price"] = price_entry

        qty_entry = self._grayed_entry(placeholder_text="1")
        qty_entry.set_alignment(1)
        self.article_grid.attach(qty_entry , 5, i, 1, 1)
        row_widgets.append(qty_entry)
        article_entries["quantity"] = qty_entry

        label = Gtk.Label("0.00 €")
        # self.total_articles.append(label)
        self.article_grid.attach(label, 6, i, 1, 1)
        row_widgets.append(label)
        article_entries["total_label"] = label

        des_entry = self._grayed_entry(
            placeholder_text=i18n.t('gui.additional_details'))
        des_entry.set_max_length(100)
        # self.entry.set_hexpand(True)
        self.article_grid.attach(des_entry, 2, i + 1, 2, 2)
        row_widgets.append(des_entry)
        article_entries["description"] = des_entry
        self.article_list.append(article_entries)

        # self.row_box.pack_start(self.article_grid, True, True, 0)
        for wid in row_widgets:
            wid.set_visible(True)


    def _clean_article_form(self):
        """Supprime le formulaire article correspondant au button."""
        # line = self.btns.pop(btn)
        for i in range(len(self.article_list)):
            self.article_grid.remove_row(5)
            self.article_grid.remove_row(5)
            self.article_grid.remove_row(5)
        while len(self.article_list) > 1:
            self.article_list.pop()
            # self.total_articles.pop()
        self.plus_btn_row = 5
