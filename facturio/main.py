import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GObject
import sys
from facturio.gui.invoice  import InvoicePage
from facturio.gui.home import HomePage, HeaderBarSwitcher
from facturio.gui.customer import Customer
from facturio.gui.history import History
from facturio.gui.map import Map
from facturio.gui.display_info import InfoPerson


class Window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # proprietés divers pour la window
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.resize(960, 540)
        provider = Gtk.CssProvider()
        provider.load_from_path("./main.css")
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
        self.header_bar = HeaderBarSwitcher()
        self.header_bar.set_stack(self.stack)
        self.set_titlebar(self.header_bar)

        self.main_page = HomePage(self.header_bar)
        self.stack.add_named(self.main_page, "home_page")
        self.invoice_page = InvoicePage()
        self.stack.add_named(self.invoice_page, "invoice_page")
        self.customer_page = Customer()
        self.stack.add_named(self.customer_page, "customer_page")
        self.history_page = History()
        self.stack.add_named(self.history_page, "history_page")
        self.map_page = Map()
        self.stack.add_named(self.map_page, "map_page")
        self.user_page = InfoPerson(True)
        self.stack.add_named(self.user_page, "user_page")

        self.add(self.stack)

    def initial_show(self):
        self.show_all()
        self.stack.set_visible_child_name("home_page")
        self.header_bar.set_visible(False)
        self.invoice_page.calendar.set_visible(False)


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
