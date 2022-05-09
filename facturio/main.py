import sys
import i18n
from facturio.gui.invoice import InvoicePage, CreateInvoicePage
from facturio.gui.estimate import EstimatePage
from facturio.gui.home import HomePage
from facturio.gui.headerbar import HeaderBarSwitcher
from facturio.gui.displayclient import DisplayClient
from facturio.gui.customer import Customer
from facturio.gui.add_customer import Add_Customer
from facturio.gui.modify_usr import ModifyUsr
from facturio.gui.modify_client import ModifyClient
from facturio.gui.display_info import DisplayUser
from facturio.gui.history import History
from facturio.gui.showinvoice import ShowInvoicePage
from facturio.gui.map import Map
from pathlib import Path
from facturio import __path__
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GObject

i18n.load_path.append(__path__[0] + "/data/translations/")
i18n.set('filename_format', '{namespace}.{format}')
i18n.set('locale', 'fr')

class Window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.resize(960, 540)
        provider = Gtk.CssProvider()
        provider.load_from_path(__path__[0] + "/main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider,
                                       Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.set_border_width(10)

        # Création du stack et ajout des pages
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.
                                       SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)

        # Création de la header bar et ajout a l'écran
        self.header_bar = HeaderBarSwitcher.get_instance()
        self.header_bar.set_stack(self.stack)
        self.set_titlebar(self.header_bar)

        self.main_page = HomePage()
        self.stack.add_named(self.main_page, "home_page")
        self.invoice_page = InvoicePage()
        self.stack.add_named(self.invoice_page, "invoice_page")
        self.create_invoice_page = CreateInvoicePage()
        self.stack.add_named(self.create_invoice_page, "create_invoice_page")
        self.estimate_page = EstimatePage()
        self.stack.add_named(self.estimate_page, "estimate_page")
        self.show_invoice_page = ShowInvoicePage.get_instance()
        self.stack.add_named(self.show_invoice_page, "show_invoice_page")
        self.add_customer = Add_Customer()
        self.stack.add_named(self.add_customer, "add_customer")
        self.modify_usr = ModifyUsr()
        self.stack.add_named(self.modify_usr, "modify_usr")
        self.modify_client = ModifyClient.get_instance()
        self.stack.add_named(self.modify_client, "modify_client")
        self.customer_page = Customer()
        self.stack.add_named(self.customer_page, "customer_page")
        self.history_page = History()
        self.stack.add_named(self.history_page, "history_page")
        self.map_page = Map()
        self.stack.add_named(self.map_page, "map_page")
        self.user_page = DisplayUser.get_instance()
        self.stack.add_named(self.user_page, "user_page")
        self.client_page = DisplayClient.get_instance()
        self.stack.add_named(self.client_page, "client_page")
        self.add(self.stack)

    def initial_show(self):
        self.show_all()
    #     self.stack.set_visible_child_name("home_page")
    #     self.header_bar.set_visible(False)
        # self.create_invoice_page.calendar.set_visible(False)


class App(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.connect('activate', self.on_activate)
    def on_activate(self, app):
        self.window = Window()
        self.window.initial_show()
        self.add_window(self.window)


def main():
    app = App()
    app.run(sys.argv)

if __name__ == "__main__":
    main()
