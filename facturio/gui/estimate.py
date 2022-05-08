#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk
import i18n
from facturio.classes.client import Company, Client
from facturio.classes.user import User
from facturio.classes.invoice_misc import Article, Invoice, Estimate
from facturio.gui.home import HeaderBarSwitcher
from facturio.build_pdf.build_pdf import build_pdf
from facturio.gui.autocompletion import FacturioEntryCompletion
from facturio.db.invoicedao import InvoiceDAO
from facturio.db.userdao import UserDAO
from facturio import examples
from datetime import datetime
import re
from datetime import date
import webbrowser

class EstimatePage(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        # client | date | solde restant
        self.grid = Gtk.Grid(row_homogeneous=True,
                             column_spacing=20, row_spacing=20)
        self._init_treeview()

        header_bar = HeaderBarSwitcher.get_instance()
        self.hb = header_bar
        hbox = Gtk.HBox()
        self.paid_switch = Gtk.RadioButton(label=i18n.t('gui.paid'))
        self.not_paid_switch = Gtk.RadioButton(group=self.paid_switch,
                                               label=i18n.t('gui.unpaid'))
        self.paid_switch.set_mode(False)
        self.not_paid_switch.set_mode(False)
        hbox.pack_start(self.paid_switch, True, True, 0)
        hbox.pack_start(self.not_paid_switch, True, True, 0)
        Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")

        vbox = Gtk.VBox()
        create_btn = Gtk.Button(label=i18n.t('gui.create_new_invoice'))
        create_btn.connect("clicked", self.switch_to_create_invoice)
        export_btn = Gtk.Button(label=i18n.t('gui.export_to_pdf'))
        export_btn.connect("clicked", self._gen_invoice)
        add_advance_btn = Gtk.Button(label=i18n.t('gui.add_deposit'))
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

    def show_hide_style_settings(self, *args):
        """Affiche ou cache la grid des styles."""
        if self.show_style.get_active():
            self.style_grid.show()
        else:
            self.style_grid.hide()

    def switch_to_create_invoice(self, *args):
        hb = HeaderBarSwitcher.get_instance()
        hb.active_button(page="create_invoice_page")

    # def style_update_window(self, *args):
    #     self.set_sensitive(False)
    #     box = Gtk.VBox()
    #     rb = Gtk.RadioButton(label=i18n.t('gui.lines'))
    #     rb1 = Gtk.RadioButton(group=rb, label=i18n.t('gui.columns'))
    #     window = Gtk.Window(title=i18n.t('gui.edit_style'), type=Gtk.WindowType.TOPLEVEL)
    #     color_chooser = Gtk.ColorChooserWidget(show_editor=False)
    #     box.pack_start(color_chooser, True, True, 5)
    #     box.pack_start(rb, True, True, 5)
    #     box.pack_start(rb1, True, True, 5)
    #     window.add(box)
    #     window.show_all()

    def _init_treeview(self):
        self.treeview_scroll = Gtk.ScrolledWindow()
        self.store = Gtk.ListStore(str, str, str, float, int)
        # self.refresh_store()
        self.treeview = Gtk.TreeView(model=self.store, headers_clickable=True)
        self.treeview_scroll.add(self.treeview)
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
        column_text.get_button().connect("clicked", self.refresh_store)
        column_text.set_clickable(True)
        # column_text.set_halign(Gtk.Align.END)
        # column_text.set_widget(btn)
        # btn.show()
        self.treeview.append_column(column_text)

    def refresh_store(self, *args):
        """Syncro avec la bd."""
        inv_dao = InvoiceDAO.get_instance()
        invoices = inv_dao.get_all()
        self.store.clear()
        for invoice in inv_dao.get_all():
            iter_ = self.store.append([invoice.client.first_name,
                                      invoice.client.last_name,
                                      invoice.date_string(),
                                      invoice.balance,
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
        print(color)
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
