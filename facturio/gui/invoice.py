#!/usr/bin/env python3
import re
import gi
import i18n
import webbrowser
from facturio.classes.client import Company, Client
from facturio.classes.user import User
from facturio.classes.invoice_misc import Article, Invoice, Estimate
from facturio.gui.headerbar import HeaderBarSwitcher
from facturio.gui.showreceipt import ShowReceiptPage
from facturio.build_pdf.build_pdf import build_pdf
from facturio.gui.autocompletion import FacturioEntryCompletion
from facturio.db.invoicedao import InvoiceDAO
from facturio.db.userdao import UserDAO
from facturio.db.estimatedao import EstimateDAO
from facturio import examples
from datetime import datetime
from datetime import date
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk

class InvoicePage(Gtk.ScrolledWindow):
    __instance = None

    def get_instance():
        """Return l'instance de invoice page."""
        if InvoicePage.__instance is None:
            InvoicePage.__instance = InvoicePage()
        return InvoicePage.__instance

    def __init__(self):
        super().__init__()
        InvoicePage.__instance = self
        # client | date | solde restant
        self.grid = Gtk.Grid(row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self._init_treeview()

        header_bar = HeaderBarSwitcher.get_instance()
        self.hb = header_bar
        hbox = Gtk.HBox()
        self.paid_switch = Gtk.RadioButton(label=i18n.t('gui.paid'))
        self.unpaid_switch = Gtk.RadioButton(group=self.paid_switch,
                                               label=i18n.t('gui.unpaid'))
        self.paid_switch.connect("clicked", self.refresh)
        self.unpaid_switch.connect("clicked", self.refresh)
        self.paid_switch.set_mode(False)
        self.unpaid_switch.set_mode(False)
        hbox.pack_start(self.paid_switch, True, True, 0)
        hbox.pack_start(self.unpaid_switch, True, True, 0)
        Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")

        vbox = Gtk.VBox()
        create_btn = Gtk.Button(label=i18n.t('gui.create_new_invoice'))
        create_btn.connect("clicked", self.switch_to_create_invoice)
        export_btn = Gtk.Button(label=i18n.t('gui.export_to_pdf'))
        export_btn.connect("clicked", self._gen_invoice)
        add_advance_btn = Gtk.Button(label=i18n.t('gui.add_deposit'))
        add_advance_btn.connect("clicked", self.load_and_switch)
        self.delete_btn = Gtk.Button(label=i18n.t('gui.delete'))
        self.show_style = Gtk.ToggleButton(label=i18n.t("gui.pdf_style"))
        self._init_style_settings()
        self.show_style.connect("clicked", self.show_hide_style_settings)

        vbox.pack_start(create_btn, True, True, 5)
        vbox.pack_start(add_advance_btn, True, True, 5)
        vbox.pack_start(self.delete_btn, True, True, 5)
        vbox.pack_start(export_btn, True, True, 5)
        vbox.pack_start(self.show_style, True, True, 5)
        # vbox.pack_start(self.style_grid, True, True, 0)

        # vbox1 = Gtk.VBox()
        # rb = Gtk.RadioButton(label=i18n.t('gui.lines'))
        # rb1 = Gtk.RadioButton(group=rb, label=i18n.t('gui.columns'))

        # vbox1.pack_start(rb, True, True, 0)
        # vbox1.pack_start(rb1, True, True, 0)
        # update_style_btn.connect("clicked", self.style_update_window)
        # hbox1 = Gtk.HBox()
        # hbox1.pack_start(color_btn, True, True, 5)
        # hbox1.pack_start(vbox1, True, True, 5)

        # vbox.pack_start(hbox1, True, True, 5)

        # self.grid.attach(hbox, 1, 1, 1, 1)
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        # self.grid.attach(self.treeview, 1, 2, 2, 7)
        # self.grid.attach(vbox, 11, 2, 1, 3)


        main_grid = Gtk.Grid(column_spacing=20, row_spacing=20)
        vspace = Gtk.Label(label="")
        vspace.set_hexpand(True)
        vspace.set_vexpand(True)
        main_grid.attach(vspace, 1, 1, 1, 1)

        vspace = Gtk.Label(label="")
        vspace.set_hexpand(True)
        vspace.set_vexpand(True)
        main_grid.attach(vspace, 5, 1, 1, 1)

        hbox.set_halign(Gtk.Align.START)

        search = Gtk.SearchEntry()

        main_grid.attach(search, 2, 1, 3, 1)
        main_grid.attach(hbox, 2, 2, 1, 1)

        main_grid.attach(self.treeview_scroll, 2, 3, 2, 9)
        main_grid.attach(vbox, 4, 3, 1, 1)
        main_grid.attach(self.style_grid, 4, 4, 1, 1)

        self.add(main_grid)
    def load_and_switch(self, *args):
        model, sel_iter = self.treeview.get_selection().get_selected()
        id_ = model[sel_iter][-1]
        inv_dao = InvoiceDAO.get_instance()
        invoice = inv_dao.get_with_id(id_)
        show_inv = ShowReceiptPage.get_instance()
        show_inv.load_receipt(invoice, add_adv=True)
        self.hb.switch_page(page="show_invoice_page")
    def switch_to_show_inv(self, *args):
        model, sel_iter = self.treeview.get_selection().get_selected()
        id_ = model[sel_iter][-1]
        inv_dao = InvoiceDAO.get_instance()
        invoice = inv_dao.get_with_id(id_)
        # print(invoice)
        show_inv = ShowReceiptPage.get_instance()
        # print(show_inv)
        show_inv.load_receipt(invoice, add_adv=False)
        self.hb.switch_page(page="show_invoice_page")

    def show_hide_style_settings(self, *args):
        """Affiche ou cache la grid des styles."""
        if self.show_style.get_active():
            self.style_grid.show()
        else:
            self.style_grid.hide()

    def switch_to_create_invoice(self, *args):
        hb = HeaderBarSwitcher.get_instance()
        hb.switch_page(page="create_invoice_page")

    def _init_treeview(self):
        self.treeview_scroll = Gtk.ScrolledWindow()
        self.store = Gtk.ListStore(str, str, str, float, int)
        # self.refresh_store()
        self.treeview = Gtk.TreeView(model=self.store, headers_clickable=True)
        self.treeview_scroll.add(self.treeview)
        self.treeview.connect("row-activated", self.switch_to_show_inv)
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(i18n.t('gui.name'), renderer_text, text=0)
        column_text.set_clickable(True)
        column_text.set_resizable(True)
        column_text.get_button().connect("clicked", self.sort_first_name)
        self.treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(i18n.t('gui.surname'), renderer_text, text=1)
        column_text.set_clickable(True)
        column_text.set_resizable(True)
        column_text.get_button().connect("clicked", self.sort_last_name)
        self.treeview.append_column(column_text)

        # column_text.set_clickable(True)
        # column_text.get_button().connect("clicked", self.sort_first_name)

        # renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(i18n.t('gui.date'), renderer_text, text=2)
        column_text.set_clickable(True)
        column_text.get_button().connect("clicked", self.sort_date)
        self.treeview.append_column(column_text)

        # renderer_text = Gtk.CellRendererText()
        column_text= Gtk.TreeViewColumn(i18n.t('gui.balance_left'), renderer_text, text=3)
        column_text.set_clickable(True)
        column_text.get_button().connect("clicked", self.sort_balance)
        self.treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        invisible_column = Gtk.TreeViewColumn("", renderer_text)
        invisible_column.set_expand(True)
        self.treeview.append_column(invisible_column)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(title=i18n.t('gui.refresh'),
                                         cell_renderer=renderer_text)
        column_text.get_button().connect("clicked", self.refresh)
        column_text.set_clickable(True)
        # column_text.set_halign(Gtk.Align.END)
        # column_text.set_widget(btn)
        # btn.show()
        self.treeview.append_column(column_text)

    def refresh(self, *args):
        """Syncro avec la bd."""
        inv_dao = InvoiceDAO.get_instance()
        invoices = inv_dao.get_all()
        self.store.clear()
        for invoice in inv_dao.get_all():
            if self.unpaid_switch.get_active() \
               and invoice.total_with_advances() > 0:
                iter_ = self.store.append([invoice.client.first_name,
                                        invoice.client.last_name,
                                        invoice.date_string(),
                                        invoice.total_with_advances(),
                                        invoice.id_])
            if self.paid_switch.get_active() \
               and invoice.total_with_advances() <= 0:
                iter_ = self.store.append([invoice.client.first_name,
                                        invoice.client.last_name,
                                        invoice.date_string(),
                                        invoice.total_with_advances(),
                                        invoice.id_])

    def _gen_invoice(self, btn):
        model, sel_iter = self.treeview.get_selection().get_selected()
        id_ = model[sel_iter][-1]
        inv_dao = InvoiceDAO.get_instance()
        invoice = inv_dao.get_with_id(id_)
        color = self.color.get_rgba().to_string()
        color = self.str_rgb_to_hex(color)
        prominent = self.inf_footer.get_active()
        show_adv = self.detail.get_active()
        inline = self.radio_line.get_active()
        # print(color)
        build_pdf(invoice, path="facture.pdf", color=color, inline=inline,
                  prominent_article_table=prominent,
                  show_advances_table=show_adv)
        webbrowser.open_new("facture.pdf")

    @staticmethod
    def str_rgb_to_hex(str_color):
        """Return color as rrggbb for the given color values."""
        # format de str_color rgb(XXX, XXX, XXX)
        color = str_color.strip("rgba()")
        color = [int(x) for x in color.split(',')]
        hex_rgb_list = []
        for x in color:
            hex_x = hex(x)[2:]
            if len(hex_x) == 1:
                hex_x = "0" + hex_x
            hex_rgb_list.append(hex_x)
        return "".join(hex_rgb_list)

    def on_combo_changed(self, widget, path, text):
        self.liststore_hardware[path][1] = text

    def _init_style_settings(self):
        """Creation de la grid avec le style."""
        self.color = Gtk.ColorButton()
        curr_color = Gdk.RGBA()
        curr_color.parse("#5f5f5f")
        self.color.set_rgba(curr_color)

        self.style_grid = Gtk.Grid(row_spacing=5, row_homogeneous=False)
        self.radio_col = Gtk.RadioButton(label="En colonnes")
        self.radio_line = Gtk.RadioButton(group=self.radio_col,
                                          label="En lignes")
        self.detail = Gtk.CheckButton(label="Détails des accomptes")
        self.inf_footer = Gtk.CheckButton(label="Données pied de page")

        self.style_grid.attach(self.color, 1, 1, 1, 2)
        # self.style_grid.attach_next_to(self.color, style_pdf,
        #                                Gtk.PositionType.BOTTOM, 1, 2)
        self.style_grid.attach_next_to(self.radio_col, self.color,
                                       Gtk.PositionType.RIGHT, 1, 1)
        self.style_grid.attach_next_to(self.radio_line, self.radio_col,
                                       Gtk.PositionType.BOTTOM, 1, 1)
        # self.style_grid.attach_next_to(self.detail, self.radio_col,
        #                                Gtk.PositionType.BOTTOM, 1, 1)
        self.style_grid.attach_next_to(self.inf_footer, self.color,
                                       Gtk.PositionType.BOTTOM, 2, 1)
        self.style_grid.attach_next_to(self.detail, self.inf_footer,
                                       Gtk.PositionType.BOTTOM, 2, 1)

    def sort_first_name(self, *args):
        """Tri par prenom."""
        raise NotImplementedError()

    def sort_last_name(self, *args):
        """Tri par nom."""
        raise NotImplementedError()

    def sort_date(self, *args):
        """Tri par date."""
        raise NotImplementedError()

    def sort_balance(self, *args):
        """Tri par solde restant."""
        raise NotImplementedError()


class CreateInvoicePage(Gtk.ScrolledWindow):
    """Page pour la creation invoice."""

    def __init__(self):
        super().__init__()
        self.main_grid = Gtk.Grid(column_homogeneous=False,
                                  row_homogeneous=False, column_spacing=20,
                                  row_spacing=20)
        self.userdao = UserDAO.get_instance()
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

        self.create_inv_btn = Gtk.Button(label=i18n.t('gui.create_invoice'))
        self.create_inv_btn.connect("clicked", self._gen_invoice)
        self.create_inv_btn.set_halign(Gtk.Align.END)
        self.create_estimate_btn = Gtk.Button(label=i18n.t('gui.create_estimate'))
        self.create_estimate_btn.connect("clicked", self._gen_estimate)

        hbox = Gtk.HBox()
        self.error_label = Gtk.Label()
        hbox.pack_start(self.error_label, True, True, 20)
        hbox.pack_start(self.create_estimate_btn, True, True, 20)
        hbox.pack_start(self.create_inv_btn, True, True, 0)
        hbox.set_halign(Gtk.Align.END)
        self.main_grid.attach(hbox, 2, 8, 1, 1)
        self.company_switch.set_active(True)

        space = Gtk.Label("")
        self.main_grid.attach(space, 2, 9, 1, 1)
        self.clean_page()
        self.add(self.main_grid)


    def _init_header_grid(self):
        """Facture texte et logo."""
        self.header_grid = Gtk.Grid(row_homogeneous=True,
                                    column_homogeneous=True)
        label = Gtk.Label("<big>" + i18n.t('gui.invoice') + "</big>")
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

    def _switch_private_company(self, entry):
        if entry == self.private_switch:
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
                                    row_homogeneous=True, column_spacing=20,
                                    row_spacing=20)
        self.client_entries = {}
        self.client_labels= {}
        self.client_completions = [
            FacturioEntryCompletion(lambda x: x.first_name),
            FacturioEntryCompletion(lambda x: x.last_name),
            FacturioEntryCompletion(lambda x: x.email),
            FacturioEntryCompletion(lambda x: x.address),
            FacturioEntryCompletion(lambda x: x.phone_number),
            # FacturioEntryCompletion(lambda x: (x.company_name or None)),
            # FacturioEntryCompletion(lambda x: (x.business_number or None)),
        ]

        for c in self.client_completions:
            c.fill_entry(examples.clients)
            c.to_update = self.client_completions

        label = Gtk.Label("<big>" + i18n.t('gui.client') + "</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        hbox = Gtk.HBox()
        # hbox.pack_start(label, True, True, 10)
        self.private_switch = Gtk.RadioButton(label=i18n.t('gui.private_individual'))
        self.company_switch = Gtk.RadioButton(group=self.private_switch,
                                              label=i18n.t('gui.business'))
        self.company_switch.connect("clicked", self._switch_private_company)
        self.private_switch.connect("clicked", self._switch_private_company)
        self.private_switch.set_mode(False)
        self.company_switch.set_mode(False)
        hbox.pack_start(self.private_switch, True, True, 0)
        hbox.pack_start(self.company_switch, True, True, 0)
        Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")

        self.client_grid.attach(label, 1, 1, 1, 1)
        self.client_grid.attach(hbox, 2, 1, 3, 1)

        label = Gtk.Label(i18n.t('gui.business_name'))
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

        label = Gtk.Label(i18n.t('gui.surname'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 5, 1, 1)
        label.set_hexpand(True)
        entry = self.client_completions[1]
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
        entry = self.client_completions[0]
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.client_grid.attach(entry, 2, 6, 3, 1)
        self.client_entries["first_name"] = entry
        self.client_labels["first_name"] = label

        label = Gtk.Label(i18n.t('gui.address'))
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 7, 1, 1)
        entry = self.client_completions[3]
        entry.set_max_length(100)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 7, 3, 1)
        self.client_entries["address"] = entry
        self.client_labels["address"] = label

        label = Gtk.Label(i18n.t('gui.email'))
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 8, 1, 1)
        entry = Gtk.Entry()
        entry = self.client_completions[2]
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 8, 3, 1)
        self.client_entries["email"] = entry
        self.client_labels["email"] = label

        label = Gtk.Label(i18n.t('gui.phone_number'))
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.client_grid.attach(label, 1, 9, 1, 1)
        entry = self.client_completions[4]
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.connect("insert-text", self.allow_only_phone)
        self.client_grid.attach(entry, 2, 9, 3, 1)
        self.client_entries["phone_number"] = entry
        self.client_labels["phone_number"] = label

        label = Gtk.Label(i18n.t('gui.siret_number'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.client_grid.attach(label, 1, 10, 1, 1)
        entry = Gtk.Entry()
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.client_grid.attach(entry, 2, 10, 3, 1)
        self.client_entries["business_number"] = entry
        self.client_labels["business_number"] = label

        button = Gtk.Button(label=i18n.t('gui.import_client'))
        self.client_grid.attach(button, 3, 11, 2, 1)

        self.update_client_btn = Gtk.ToggleButton(label=i18n.t('gui.save_client'))
        self.update_client_btn.set_sensitive(False)
        self.client_grid.attach(self.update_client_btn, 1, 11, 2, 1)

    def _init_user_grid(self):
        self.user_grid = Gtk.Grid(column_homogeneous=True,
                                  row_homogeneous=True, column_spacing=20,
                                  row_spacing=20)
        self.user_entries = {}
        label = Gtk.Label("<big>" + i18n.t('gui.user') + "</big>")
        label.set_hexpand(True)
        label.set_use_markup(True)
        self.user_grid.attach(label, 1, 3, 1, 1)

        self.user_completions = [
            FacturioEntryCompletion(lambda x: x.company_name),
            FacturioEntryCompletion(lambda x: x.first_name),
            FacturioEntryCompletion(lambda x: x.last_name),
            FacturioEntryCompletion(lambda x: x.email),
            FacturioEntryCompletion(lambda x: x.address),
            FacturioEntryCompletion(lambda x: x.phone_number),
            FacturioEntryCompletion(lambda x: x.business_number),
        ]

        for c in self.user_completions:
            #c.fill_entry([self.userdao.get()])
            c.to_update = self.user_completions

        label = Gtk.Label(i18n.t('gui.business_name'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 4, 1, 1)
        entry = self.user_completions[0]
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
        entry = self.user_completions[2]
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
        entry = self.user_completions[1]
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.set_hexpand(True)
        self.user_grid.attach(entry, 2, 6, 3, 1)
        self.user_entries["first_name"] = entry

        label = Gtk.Label(i18n.t('gui.address'))
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 7, 1, 1)
        entry = self.user_completions[4]
        entry.set_max_length(100)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 7, 3, 1)
        self.user_entries["address"] = entry

        label = Gtk.Label(i18n.t('gui.email'))
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 8, 1, 1)
        entry = self.user_completions[3]
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 8, 3, 1)
        self.user_entries["email"] = entry

        label = Gtk.Label(i18n.t('gui.phone_number'))
        label.set_hexpand(True)
        label.set_justify(Gtk.Justification.CENTER)
        self.user_grid.attach(label, 1, 9, 1, 1)
        entry = self.user_completions[5]
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        entry.connect("insert-text", self.allow_only_phone)
        self.user_grid.attach(entry, 2, 9, 3, 1)
        self.user_entries["phone_number"] = entry

        label = Gtk.Label(i18n.t('gui.siret_number'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_hexpand(True)
        self.user_grid.attach(label, 1, 10, 1, 1)

        entry = self.user_completions[6]
        entry.set_max_length(25)
        entry.connect("changed", self.reset_context)
        self.user_grid.attach(entry, 2, 10, 3, 1)
        self.user_entries["business_number"] = entry

        # self.save_user_btn = Gtk.Button(label=i18n.t('gui.save_user'))
        # self.save_user_btn.connect("clicked", self._save_user)
        # self.user_grid.attach(self.save_user_btn, 1, 11, 2, 1)

        self.update_user_btn = Gtk.ToggleButton(label=i18n.t('gui.edit_user'))
        self.update_user_btn.connect("clicked", self._update_user)
        self.user_grid.attach(self.update_user_btn, 3, 11, 2, 1)

    def _load_user_entries(self):
        user = User.get_instance()
        for name, entry in self.user_entries.items():
            print(name,user.get_attr(name))
            entry.set_text(str(user.get_attr(name)))
            entry.set_sensitive(False)

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


    def _save_user(self, btn):
        self.reset_context(btn)
        if self._validate_user_entries() is False:
            return
        if User.exists():
            user = User.get_instance()
            for name, entry in self.user_entries.items():
                user.set_attr(name, entry.get_text())
        else:
            user_data = {}
            for name, entry in self.user_entries.items():
                user_data[name] = entry.get_text()
            user_data["logo"] = self.logo_fn
            User.from_dict(user_data)

        # ihm modif
        user = User.get_instance()
        for entry in self.user_entries.values():
            entry.set_sensitive(False)
        self.logo_button.set_sensitive(False)
        self.logo_button.set_label(i18n.t('gui.added'))
        self.update_user_btn.set_sensitive(True)
        self.save_user_btn.set_sensitive(False)
        return

    def _update_user(self, btn):
        UserDAO.get_instance().get()
        user = User.get_instance()
        for name, entry in self.user_entries.items():
            entry.set_sensitive(True)
        self.logo_button.set_label(i18n.t('gui.edit_picture'))
        self.logo_button.set_sensitive(True)
        self.update_user_btn.set_sensitive(False)
        # self.save_user_btn.set_sensitive(True)

    def reset_context(self, entry):
        context = entry.get_style_context()
        context.remove_class("entry_error")

    def _init_taxes_grid(self):
        self.taxes_grid = Gtk.Grid(row_spacing=20)
        label = Gtk.Label(i18n.t('gui.tax'))
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

        label = Gtk.Label(i18n.t('gui.date'))
        self.taxes_grid.attach(label, 1,2,1,1)
        vbox = Gtk.HBox()
        self.date_entry = Gtk.Entry(placeholder_text="dd/mm/yyyy")
        self.date_entry.connect("changed", self.reset_context)
        today = date.today()
        self.date_entry.set_text(date.today().strftime("%d/%m/%Y"))
        # self.taxes_grid.attach(date_entry, 3,2,1,1)
        self.show_calendar = Gtk.ToggleButton(label=i18n.t('gui.show_calendar'))
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
        self.label= Gtk.Label(i18n.t('gui.subtotal'))
        self.label.set_xalign(0)
        self.total_grid.attach(self.label, 1, 1, 1, 1)
        self.tax_label = Gtk.Label(i18n.t('gui.tax') + "(21%)")
        self.tax_label.set_xalign(0)
        self.total_grid.attach(self.tax_label, 1, 2, 1, 1)
        self.label= Gtk.Label(i18n.t('gui.total'))
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
        # print(entry)
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
        if self.private_switch.get_active():
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
        self.error_label.set_text(i18n.t('gui.invalid_fields'))
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
        # print(error)
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

    def _get_user(self):
        self.userdao = UserDAO.get_instance()
        self.userdao.get()
        if not User.exists():
            self.user_data = {}
            for name, entry in self.user_entries.items():
                self.user_data[name] = entry.get_text()
            self.user_data["logo"] = self.logo_fn
            user = User.from_dict(self.user_data)
            self.userdao.insert(user)
        elif self.update_user_btn.get_active():
            # l'update a ete active
            user = User.get_instance()
            for name, entry in self.user_entries.items():
                user.set_attr(name, entry.get_text())
            user.logo = self.logo_fn
            # TODO: user_dao.update()
        else:
            user = User.get_instance()
        return user

    def _get_client(self):
        """Renvoie une instance du client."""
        if self.update_client_btn.get_active():
            # TODO: Faire les updates
            raise NotImplementedError
        else:
            client_data = {}
            client_data["note"] = None
            if self.company_switch.get_active():
                for name, entry in self.client_entries.items():
                    txt = self.client_entries[name].get_text()
                    client_data[name] = txt
                    if txt == "":
                        client_data[name] = None
                client = Company.from_dict(client_data)
            else:
                assert(self.private_switch.get_active())
                names = ("first_name", "last_name", "address", "email",
                         "phone_number")
                for name in names:
                    txt = self.client_entries[name].get_text()
                    client_data[name] = txt
                    if txt == "":
                        client_data[name] = None
                client = Client.from_dict(client_data)
        return client

    def _get_articles_list(self):
        """Renvoie une list d'instances article."""
        articles_dict = []
        for art_dict in self.article_list:
            dict_ = {}
            for name, entry in art_dict.items():
                txt = entry.get_text()
                dict_[name] = txt
                # pas de try car les champs ont ete deja valides
                if name == "price" or name == "quantity":
                    dict_[name] = float(entry.get_text())
                dict_[name] = txt
                if txt == "":
                    dict_[name] = None
            articles_dict.append(dict_)
        art_instances = []
        for art_dict in articles_dict:
            art_instances.append(Article.from_dict(art_dict))
        return art_instances

    def _gen_estimate(self, *args):
        self.error_label.hide()
        if self.validate_entries():
            self._raise_error()
            return

        user = self._get_user()
        client = self._get_client()
        articles_list = self._get_articles_list()

        date_text = self.date_entry.get_text()
        date = datetime.strptime(date_text, "%d/%m/%Y")
        epoch_date = date.timestamp()

        tax = self.spin_btn.get_adjustment().get_value() / 100
        total = float(self.total.get_text()[:-2])
        estimate = Estimate(user=user, client=client,
                            articles_list=articles_list,
                            date=epoch_date, taxes=tax, balance=total)
        estimatedao = EstimateDAO.get_instance()
        estimatedao.insert(estimate)
        self.clean_page()
        # redirect
        hb = HeaderBarSwitcher.get_instance()
        hb.switch_page(page="estimate_page")

    def _gen_invoice(self, btn):
        self.error_label.hide()
        if self.validate_entries():
            self._raise_error()
            return

        user = self._get_user()
        client = self._get_client()
        articles_list = self._get_articles_list()

        date_text = self.date_entry.get_text()
        date = datetime.strptime(date_text, "%d/%m/%Y")
        epoch_date = date.timestamp()

        tax = self.spin_btn.get_adjustment().get_value() / 100
        total = float(self.total.get_text()[:-2])
        inv = Invoice(user=user, client=client, articles_list=articles_list,
                      date=epoch_date, taxes=tax, balance=total)
        invoicedao = InvoiceDAO.get_instance()
        invoicedao.insert(inv)
        self.clean_page()
        # redirect
        hb = HeaderBarSwitcher.get_instance()
        hb.switch_page(page="invoice_page")

    def clean_page(self):
        """Nettoyage de la page."""
        dao = UserDAO.get_instance().get()
        self.update_user_btn.set_active(False)
        if User.exists():
            self._load_user_entries()
            self.logo_button.set_label(i18n.t('gui.added'))
            self.logo_button.set_sensitive(False)
            self.update_user_btn.set_sensitive(True)
            self.update_user_btn.set_active(False)
            # self.save_user_btn.set_sensitive(False)
        else:
            self.update_user_btn.set_sensitive(False)
        for entry in self.client_entries.values():
            entry.set_text("")
        for art_dict in self.article_list:
            for name, entry in art_dict.items():
                entry.set_text("")
    def _logo_dialog(self, *args):
        file_chooser = Gtk.FileChooserNative(title=i18n.t('gui.select_picture'),
                                             accept_label=i18n.t('gui.select'),
                                             cancel_label=i18n.t('gui.cancel'))
        filter_ = Gtk.FileFilter()
        filter_.set_name(i18n.t('gui.pictures'))
        filter_.add_pattern("*.jpg")
        filter_.add_pattern("*.png")
        filter_.add_pattern("*.jpeg")
        file_chooser.set_filter(filter_)
        if file_chooser.run() == Gtk.ResponseType.ACCEPT:
            self.logo_fn = file_chooser.get_filename()
            print(self.logo_fn)
            # self.logo_button.set_sensitive(False)
            self.logo_button.set_label(i18n.t('gui.added'))

    def _put_percentage(self, spin_btn):
        """Ajout d'un pourcentage(%) a la fin pour les taxes."""
        value = spin_btn.get_value()
        spin_btn.set_text(f"{value} %")
    def _modify_tax_fields(self, spin_btn=None):
        """
        Modifie le porcentage.

        Modifie le porcentage des taxes ainsi que la valeur et le total
        """
        if spin_btn is None:
            spin_btn = self.spin_btn
        adjustement = spin_btn.get_adjustment()
        value = adjustement.get_value()
        if value.is_integer():
            value = int(value)
        self.tax_label.set_text(i18n.t('gui.tax') + f" ({value}%)")
        sub_total_val = float(self.sub_total.get_text()[:-2])
        res = round((value / 100) * sub_total_val, 2)
        self.total_taxes.set_text(f"{res} €")
        self._put_percentage(spin_btn)
        self._modify_total()

    def _modify_sub_total(self):
        """Modifie le sous total."""
        total = 0
        for label in self.total_articles:
            # print(label.get_text())
            total += float(label.get_text()[:-2])
        self.sub_total.set_text(f"{total} €")
        self._modify_tax_fields()
        self._modify_total()

    def _modify_total(self):
        sub_total = float(self.sub_total.get_text()[:-2])
        total_taxes = float(self.total_taxes.get_text()[:-2])
        self.total.set_text(f"{round(sub_total + total_taxes, 2)} €")

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

    def _first_article_row(self):
        """
        Premier ligne des articles.

        Premier ligne des article different des autres
        car pas de button supprimer
        """
        self.article_list = []
        self.total_articles = []
        article_entries = {}
        left_space = Gtk.Label("")
        left_space.set_hexpand(True)
        self.article_grid.attach(left_space, 1, 2, 1, 1)

        entry = Gtk.Entry(placeholder_text=i18n.t('gui.article_name'))
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

        des_entry = Gtk.Entry(placeholder_text=i18n.t('gui.additional_details'))
        des_entry.set_max_length(100)
        self.article_grid.attach(des_entry, 2, 3, 2, 2)
        des_entry.connect("changed", self.reset_context)
        article_entries["description"] = des_entry

        price_entry.connect("changed", self._update_total_article, article_entries,
                            label)
        qty_entry.connect("changed", self._update_total_article, article_entries, label)
        self.article_list.append(article_entries)

    def _plus_btn_row(self):
        """Ajoute un linge avec un button plus."""
        self.plus_btn_row = 5
        button = Gtk.Button.new_from_icon_name("list-add-symbolic",
                                               Gtk.IconSize.BUTTON)
        self.article_grid.attach(button, 1, 5, 1, 1)

        button.connect("clicked", self._new_article)

    def _new_article(self, btn=None):
        """Insere une nouvelle formulaire pour ajouter un article."""
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

        title_entry = Gtk.Entry(placeholder_text=i18n.t('gui.article_name'))
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

        des_entry = Gtk.Entry(placeholder_text=i18n.t('gui.additional_details'))
        # des_entry.connect("insert-text", self.allow_only_float)
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
        """Met a jour le total prix * quantite."""
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
        Mis a jour du dictionaire.

        Mis a jour liant chaque button supprimer a la ligne
        dans la grille
        """
        for btn, row in self.btns.items():
            if row > i:
                self.btns[btn] = row - 3

    def _remove_article_form(self, btn):
        """Supprime le formulaire article correspondant au button."""
        line = self.btns.pop(btn)
        self.total_articles.pop(line // 3)
        self.article_list.pop(line // 3)
        self.article_grid.remove_row(line)
        self.article_grid.remove_row(line)
        self.article_grid.remove_row(line)
        self._update_dict(line)
        self.plus_btn_row -= 3

        self._modify_sub_total()
